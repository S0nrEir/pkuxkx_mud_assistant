"""WebSocket/TCP session bridge for the web MUD client."""

import asyncio
import json
import os
import re
from datetime import datetime

import config
from character_state import default_character_state_store, section_for_command
from chat_monitor import is_chat_message
from mud_telnet import gbk_safe_split, strip_iac_and_respond
import captcha_saver
from quick_commands import (
    delete_config as delete_quick_command_config,
    list_configs as list_quick_command_configs,
    save_config as save_quick_command_config,
)
from bot_system import (
    BotRuntime,
    delete_config as delete_script_config,
    list_configs as list_script_configs,
    load_config as load_script_config,
    save_config as save_script_config,
)
from triggers import TriggerRuntime, delete_config, list_configs, load_config, save_config

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07')

# 提交验证码的命令：report/fullme + 验证码内容（中文或任意词）。
_CAPTCHA_CMD_RE = re.compile(r'^\s*(report|fullme)\b\s*(.*)$', re.IGNORECASE)


def _extract_captcha_code(command):
    """从用户命令中提取验证码内容。

    形如 `report 山药`、`fullme 黄药师` → 返回验证码内容（'山药'/'黄药师'）。
    裸 `report`/`fullme`（仅触发验证码面板，无内容）→ 返回 None。
    其它命令 → 返回 None。
    """
    m = _CAPTCHA_CMD_RE.match(str(command or ''))
    if not m:
        return None
    code = m.group(2).strip()
    return code or None


# 频道中文关键字 → 频道 ID 映射（用于本地屏蔽）
_CHANNEL_MAP = {
    '闲聊': 'chat', 'chat': 'chat',
    '谣言': 'rumor', 'rumor': 'rumor',
    '交易': 'jy', 'jy': 'jy',
    'QQ群': 'qq', 'qq': 'qq', 'QQ群转发': 'qq',
    '帮派': 'group', 'group': 'group',
    '组队': 'team',
    '大喊': 'shout', 'shout': 'shout',
    '回答': 'answer',
}


def _get_channel_id(text):
    """从聊天消息文本中提取频道 ID，无法识别返回 None"""
    for keyword, ch_id in _CHANNEL_MAP.items():
        if keyword in text:
            return ch_id
    # 备用：匹配 (chat) (rumor) 等标记
    for marker in ('(chat)', '(rumor)', '(jy)', '(qq)', '(group)'):
        if marker in text:
            return marker.strip('()')
    return None


# ═══════════════════════════════════════════
#  GBK 分包安全处理
# ═══════════════════════════════════════════

class MudSession:
    def __init__(self, runtime_log=None):
        self.reader = None
        self.writer = None
        self.ws = None
        self.runtime_log = runtime_log or (lambda msg: None)
        self.running = False
        self.cmd_history = []
        self.log_dir = os.path.join(os.path.dirname(__file__), config.LOG_DIR)
        self._raw_buf = bytearray()   # 原始字节行缓冲
        self.muted_channels = set()   # 本地屏蔽的频道
        self._minimap_active = False  # 是否正在收集小地图行
        self._minimap_lines = []      # 自动捕获的小地图行
        self._quit_pending = False    # 等待 save 回复后发 quit
        self._captcha_tasks = set()   # 正在后台下载的验证码图片任务
        self.muted_channels = set()   # 本地屏蔽的频道（终端不显示，右侧仍显示）
        self.triggers = TriggerRuntime()
        self.scripts = BotRuntime(
            runtime_log=self.runtime_log,
            send_command=self._send_script_command,
            notify=self._send_script_notify,
        )
        self._script_lock = asyncio.Lock()
        self._trigger_lock = asyncio.Lock()
        self._trigger_tasks = set()
        self._trigger_queue = []
        self._trigger_waiting_response = False
        self._trigger_response_parts = []
        self._trigger_waiting_chunk = 0
        self._trigger_rule_pending = False
        self._trigger_generation = 0
        self._mud_chunk_seq = 0
        self._raw_log_file = None   # 原始字节日志文件句柄
        self.character_state_store = default_character_state_store
        self._character_capture = None

    async def connect(self):
        """连接 MUD 服务器"""
        self.reader, self.writer = await asyncio.open_connection(
            config.MUD_HOST, config.MUD_PORT
        )
        self.running = True
        print(f"[已连接 MUD 服务器] {config.MUD_HOST}:{config.MUD_PORT}")

    async def run(self, websocket):
        """主循环：WebSocket ↔ MUD 双向桥接"""
        self.ws = websocket

        try:
            await self.connect()
            await self._send_character_state()

            # 并发执行：读 MUD + 读 WebSocket
            mud_task = asyncio.create_task(self._read_mud_loop())
            ws_task = asyncio.create_task(self._read_ws_loop())
            done, pending = await asyncio.wait(
                [mud_task, ws_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for t in pending:
                t.cancel()
        except Exception as e:
            print(f"[会话错误] {e}")
        finally:
            await self.cleanup()

    async def cleanup(self):
        self.running = False
        self._cancel_trigger_tasks()
        if self._raw_log_file:
            try:
                self._raw_log_file.close()
            except Exception:
                pass
            self._raw_log_file = None
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass
        print("[会话已关闭]")

    async def _send_ws_json(self, payload):
        try:
            await self.ws.send_text(json.dumps(payload, ensure_ascii=False))
        except Exception:
            pass

    async def _send_character_state(self, state=None):
        await self._send_ws_json({
            'type': 'character_state',
            'data': state or self.character_state_store.load(),
        })

    async def _start_character_capture(self, command):
        await self._finish_character_capture()
        section = section_for_command(command)
        if not section:
            return
        self._character_capture = {
            'section': section,
            'command': str(command or '').strip(),
            'parts': [],
            'started': False,
        }

    async def _append_character_capture(self, text):
        if not self._character_capture:
            return
        text = str(text or '')
        clean = self._clean_line(text)
        if self._character_capture_prompt_seen(clean):
            await self._finish_character_capture()
            return
        if not self._character_capture.get('started'):
            if self._character_capture_marker_found(self._character_capture.get('section'), clean):
                self._character_capture['started'] = True
            else:
                return
        line = self._character_capture_storage_line(self._character_capture.get('section'), text)
        if not line:
            return
        self._character_capture['parts'].append(line)

    @staticmethod
    def _character_capture_prompt_seen(clean):
        clean = str(clean or '').strip()
        return clean == '>' or clean.startswith('>') or clean.endswith('>')

    @classmethod
    def _character_capture_storage_line(cls, section, text):
        clean = cls._clean_line(text)
        clean = str(clean or '').replace('\r', '').strip()
        if not clean or cls._character_capture_prompt_seen(clean):
            return ''
        clean = cls._character_capture_simplify_line(clean)
        if not clean or '\ufffd' in clean:
            return ''
        if cls._character_capture_noise_line(section, clean):
            return ''
        return clean

    @staticmethod
    def _character_capture_simplify_line(clean):
        clean = str(clean or '')
        clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]?', ' ', clean)
        clean = re.sub(r'(?<![A-Za-z0-9])\[[0-9;]{1,24}[A-Za-z]?', ' ', clean)
        clean = re.sub(r'(?<![A-Za-z0-9]);[0-9;]{1,24}[A-Za-z]?', ' ', clean)
        clean = re.sub(r'(?<![A-Za-z0-9])m(?=\d|$)', ' ', clean)
        clean = re.sub(r'[┌┐└┘├┤┬┴┼─│╭╮╰╯═║╔╗╚╝╠╣╦╩╬╞╡╥╨╪]', ' ', clean)
        clean = re.sub(r'[▁▂▃▄▅▆▇█▀▌▐■□◆◇●○·—]+', ' ', clean)
        clean = re.sub(r'(?<![A-Za-z0-9])o(?![A-Za-z0-9])', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean)
        return clean.strip()

    @staticmethod
    def _character_capture_noise_line(section, clean):
        compact = re.sub(r'[┌┐└┘├┤┬┴┼─│╭╮╰╯═║╔╗╚╝╠╣╦╩╬╞╡╥╨╪]', '', str(clean or ''))
        compact = re.sub(r'[\s\-_=+|·.。:：,，、\[\]()（）【】<>]+', '', compact)
        if not compact:
            return True
        if compact in {'人物详情', '个人状态', '个人信息', '门派履历', '北大侠客行', '装备', '财宝', '货币', '食物', '其它', '其他'}:
            return True
        has_text = re.search(r'[\u4e00-\u9fffA-Za-z0-9]', compact) is not None
        if not has_text:
            return True
        if section in {'score', 'hp'} and re.fullmatch(r'[▁▂▃▄▅▆▇█▀▌▐■□◆◇●○·—]+', compact):
            return True
        return False

    @staticmethod
    def _character_capture_marker_found(section, clean):
        clean = str(clean or '')
        if section == 'score':
            return '人物详情' in clean
        if section == 'hp':
            return '个人状态' in clean
        if section == 'inventory':
            return (
                '你共携带' in clean
                or '你身上没有' in clean
                or '身上没有任何' in clean
                or '[装' in clean
                or '[货' in clean
                or '[食' in clean
            )
        return False

    async def _finish_character_capture(self):
        capture = self._character_capture
        self._character_capture = None
        if not capture:
            return
        text = '\n'.join(capture.get('parts') or []).strip()
        if not text:
            return
        state = self.character_state_store.update(
            capture.get('section'),
            capture.get('command'),
            text,
        )
        await self._send_character_state(state)

    async def _send_mud_command(self, command, event_type='trigger_event', track_trigger=True):
        command = str(command or '').strip()
        if not command or not self.writer:
            return
        self.writer.write((command + '\r\n').encode('gbk', errors='replace'))
        await self.writer.drain()
        await self._start_character_capture(command)
        if track_trigger:
            self._trigger_response_parts = []
            self._trigger_waiting_chunk = self._mud_chunk_seq
        self._log_data(command, 'send')
        await self._send_ws_json({
            'type': event_type,
            'command': command,
            'active': self.triggers.active,
        })

    async def _send_script_command(self, command):
        await self._send_mud_command(command, event_type='script_event', track_trigger=False)
        self._add_history(str(command or '').strip())

    def _send_script_notify(self, message):
        """把脚本要醒目显示的消息推送到网页消息列表（聊天面板）。"""
        payload = {
            'type': 'script_notify',
            'data': {
                'time': datetime.now().strftime('%H:%M:%S'),
                'text': str(message or ''),
            },
        }
        msg = json.dumps(payload, ensure_ascii=False)

        async def _send():
            try:
                await self.ws.send_text(msg)
            except Exception:
                pass

        try:
            asyncio.create_task(_send())
        except RuntimeError:
            pass

    def _maybe_capture_captcha(self, text):
        """检测行内是否出现 fullme 验证码图片，若有则异步下载保存到本地。

        MUD 下发形如 <img src="http://fullme.pkuxkx.net/zmud/<filename>.jpg">，
        这是验证码出现的可靠信号。下载放到后台线程执行，不阻塞消息流；
        captcha_saver 自带进程级去重，同一张图不会重复下载/保存。
        下载失败会记入运行日志，不会静默吞掉异常。
        """
        if not text:
            return
        try:
            urls = captcha_saver.find_captcha_urls(text)
        except Exception:
            return
        for url in urls:
            self._schedule_captcha_download(url)

    def _schedule_captcha_download(self, url):
        """后台下载一张验证码图片并保存，异常与结果都记入运行日志。"""
        async def _runner():
            try:
                ok = await asyncio.to_thread(captcha_saver.download_and_save, url)
                if ok:
                    self.runtime_log(f'[CAPTCHA] 已保存验证码图片: {url}')
                # ok=False 表示进程内已保存过（去重），无需额外日志
            except Exception as e:
                self.runtime_log(f'[CAPTCHA] 验证码图片下载失败 {url}: {e}')

        try:
            task = asyncio.create_task(_runner())
            self._captcha_tasks.add(task)
            task.add_done_callback(self._captcha_tasks.discard)
        except RuntimeError:
            # 无事件循环时降级为同步下载（极少见）。
            try:
                captcha_saver.download_and_save(url)
            except Exception as e:
                self.runtime_log(f'[CAPTCHA] 验证码图片下载失败 {url}: {e}')

    @staticmethod
    def _split_trigger_commands(command):
        commands = []
        for part in re.split(r'[;\n]+', str(command or '')):
            part = part.strip()
            if part:
                commands.append(part)
        return commands

    def _cancel_trigger_tasks(self):
        self._trigger_generation += 1
        for task in list(self._trigger_tasks):
            task.cancel()
        self._trigger_tasks.clear()
        self._trigger_queue.clear()
        self._trigger_waiting_response = False
        self._trigger_response_parts = []
        self._trigger_waiting_chunk = 0
        self._trigger_rule_pending = False

    def _trigger_is_current(self, active_id, generation):
        return (
            self.triggers.active
            and self.triggers.active_id == active_id
            and self._trigger_generation == generation
        )

    def _queue_trigger_commands(self, commands, active_id, generation):
        for command in commands:
            self._trigger_queue.append({
                'command': command,
                'active_id': active_id,
                'generation': generation,
            })

    async def _advance_trigger_queue(self):
        if self._trigger_waiting_response or not self._trigger_queue:
            return
        item = None
        while self._trigger_queue:
            candidate = self._trigger_queue.pop(0)
            if self._trigger_is_current(candidate['active_id'], candidate['generation']):
                item = candidate
                break
        if not item:
            return
        self._trigger_waiting_response = True
        await self._send_mud_command(item['command'])

    async def _finish_trigger_response(self):
        if not self._trigger_waiting_response:
            return
        if self._trigger_waiting_chunk >= self._mud_chunk_seq:
            return
        response_text = '\n'.join(self._trigger_response_parts)
        self._trigger_response_parts = []
        self._trigger_waiting_response = False
        self._trigger_waiting_chunk = 0
        if self._trigger_queue:
            await self._advance_trigger_queue()
            return
        if response_text.strip():
            await self._match_trigger_text(response_text)

    async def _run_trigger_rule(self, rule, active_id, generation):
        try:
            commands = self._split_trigger_commands(rule.get('command'))
            if not commands or not self._trigger_is_current(active_id, generation):
                return
            try:
                delay = float(rule.get('delay') or 0)
            except (TypeError, ValueError):
                delay = 0
            delay = max(0, min(delay, 3600))
            async with self._trigger_lock:
                if not self._trigger_is_current(active_id, generation):
                    return
                if delay:
                    await asyncio.sleep(delay)
                    if not self._trigger_is_current(active_id, generation):
                        return
                self._queue_trigger_commands(commands, active_id, generation)
                self._trigger_rule_pending = False
                await self._advance_trigger_queue()
        finally:
            if not self._trigger_queue and not self._trigger_waiting_response:
                self._trigger_rule_pending = False

    async def _send_trigger_list(self, status=''):
        payload = {
            'type': 'trigger_list',
            'items': list_configs(),
            'active_id': self.triggers.active_id,
            'active': self.triggers.active,
        }
        if status:
            payload['status'] = status
        await self._send_ws_json(payload)

    async def _send_quick_command_list(self, status=''):
        payload = {
            'type': 'quick_command_list',
            'items': list_quick_command_configs(),
        }
        if status:
            payload['status'] = status
        await self._send_ws_json(payload)

    async def _send_script_list(self, status=''):
        payload = {
            'type': 'script_list',
            'items': list_script_configs(),
            'active_id': self.scripts.active_id,
            'active': self.scripts.active,
        }
        if status:
            payload['status'] = status
        await self._send_ws_json(payload)

    async def _handle_quick_command_ws(self, msg):
        action = msg.get('action')
        if action == 'list':
            await self._send_quick_command_list()
            return

        if action == 'save':
            try:
                command_id, config_data = save_quick_command_config(
                    msg.get('config') or {},
                    msg.get('id') or '',
                )
            except ValueError as e:
                await self._send_ws_json({
                    'type': 'quick_command_status',
                    'ok': False,
                    'status': f'保存失败：{e}',
                })
                return
            await self._send_ws_json({
                'type': 'quick_command_status',
                'ok': True,
                'status': '已保存快捷命令',
                'id': command_id,
                'config': config_data,
            })
            await self._send_quick_command_list()
            return

        if action == 'delete':
            delete_quick_command_config(msg.get('id') or '')
            await self._send_quick_command_list('已删除快捷命令')
            return

        if action == 'execute':
            config_data = msg.get('config') or {}
            commands = config_data.get('commands') if isinstance(config_data, dict) else []
            sent = 0
            for step in commands if isinstance(commands, list) else []:
                if not isinstance(step, dict):
                    continue
                command = str(step.get('command') or '').strip()
                if not command:
                    continue
                try:
                    delay = float(step.get('delay') or 0)
                except (TypeError, ValueError):
                    delay = 0
                delay = max(0, min(delay, 3600))
                if delay:
                    await asyncio.sleep(delay)
                await self._send_mud_command(command, event_type='quick_command_event', track_trigger=False)
                self._add_history(command)
                sent += 1
            await self._send_ws_json({
                'type': 'quick_command_status',
                'ok': sent > 0,
                'status': f'已发送 {sent} 条指令' if sent else '没有可发送的指令',
            })

    async def _handle_trigger_ws(self, msg):
        action = msg.get('action')
        if action == 'list':
            await self._send_trigger_list()
            return

        if action == 'save':
            try:
                original_id = msg.get('id') or ''
                was_active = bool(original_id and self.triggers.active_id == original_id)
                trigger_id, config_data = save_config(msg.get('config') or {}, original_id)
                if was_active or self.triggers.active_id == trigger_id:
                    self._cancel_trigger_tasks()
                    self.triggers.load(trigger_id, config_data)
            except ValueError as e:
                await self._send_ws_json({'type': 'trigger_status', 'ok': False, 'status': f'保存失败：{e}'})
                return
            payload = {
                'type': 'trigger_status',
                'ok': True,
                'status': '已保存触发器',
                'id': trigger_id,
                'config': config_data,
            }
            if self.triggers.active_id == trigger_id:
                payload['active'] = True
            await self._send_ws_json(payload)
            await self._send_trigger_list()
            return

        if action == 'load':
            if self.scripts.active:
                await self._send_ws_json({
                    'type': 'trigger_status',
                    'ok': False,
                    'status': '机器人正在启用，请先停用机器人再启用触发器',
                })
                return
            try:
                trigger_id = msg.get('id') or ''
                config_data = self.triggers.load(trigger_id, load_config(trigger_id))
                self._cancel_trigger_tasks()
            except Exception as e:
                await self._send_ws_json({'type': 'trigger_status', 'ok': False, 'status': f'加载失败：{e}'})
                return
            await self._send_ws_json({
                'type': 'trigger_status',
                'ok': True,
                'status': '已加载触发器',
                'id': self.triggers.active_id,
                'config': config_data,
                'active': True,
            })
            await self._send_trigger_list()
            await self._send_script_list()
            return

        if action == 'delete':
            trigger_id = msg.get('id') or ''
            if self.triggers.active_id == trigger_id:
                self._cancel_trigger_tasks()
                self.triggers.stop()
            delete_config(trigger_id)
            await self._send_trigger_list('已删除触发器')
            return

        if action == 'stop':
            self._cancel_trigger_tasks()
            self.triggers.stop()
            await self._send_ws_json({
                'type': 'trigger_status',
                'ok': True,
                'status': '已停止触发器',
                'active': False,
            })
            await self._send_trigger_list()

    async def _handle_script_ws(self, msg):
        action = msg.get('action')
        if action == 'list':
            await self._send_script_list()
            return

        if action == 'save':
            reload_active = False
            try:
                original_id = msg.get('id') or ''
                was_active = bool(original_id and self.scripts.active_id == original_id)
                script_id, config_data = save_script_config(msg.get('config') or {}, original_id)
                reload_active = was_active or self.scripts.active_id == script_id
                if reload_active:
                    self.scripts.load(script_id, config_data)
            except ValueError as e:
                await self._send_ws_json({'type': 'script_status', 'ok': False, 'status': f'保存失败：{e}'})
                return
            except Exception as e:
                if reload_active:
                    self.scripts.stop()
                await self._send_ws_json({'type': 'script_status', 'ok': False, 'status': f'保存成功，但加载失败：{e}'})
                await self._send_script_list()
                return
            payload = {
                'type': 'script_status',
                'ok': True,
                'status': '已保存脚本配置',
                'id': script_id,
                'config': config_data,
            }
            if self.scripts.active_id == script_id:
                payload['active'] = True
            await self._send_ws_json(payload)
            await self._send_script_list()
            return

        if action == 'load':
            if self.triggers.active:
                await self._send_ws_json({
                    'type': 'script_status',
                    'ok': False,
                    'status': '触发器正在启用，请先停用触发器再启用机器人',
                })
                return
            try:
                script_id = msg.get('id') or ''
                config_data = self.scripts.load(script_id, load_script_config(script_id))
            except Exception as e:
                await self._send_ws_json({'type': 'script_status', 'ok': False, 'status': f'加载失败：{e}'})
                return
            await self._send_ws_json({
                'type': 'script_status',
                'ok': True,
                'status': '已启用机器人',
                'id': self.scripts.active_id,
                'config': config_data,
                'active': True,
            })
            await self._send_script_list()
            await self._send_trigger_list()
            return

        if action == 'delete':
            script_id = msg.get('id') or ''
            if self.scripts.active_id == script_id:
                self.scripts.stop()
            delete_script_config(script_id)
            await self._send_script_list('已删除脚本配置')
            return

        if action == 'stop':
            self.scripts.stop()
            await self._send_ws_json({
                'type': 'script_status',
                'ok': True,
                'status': '已停用机器人',
                'active': False,
            })
            await self._send_script_list()

    async def _handle_script_text(self, text):
        if not self.scripts.active:
            return
        async with self._script_lock:
            await self.scripts.handle_message(text)

    async def _handle_trigger_text(self, text):
        if self._trigger_waiting_response:
            self._trigger_response_parts.append(str(text or ''))
            return

        await self._match_trigger_text(text)

    async def _match_trigger_text(self, text):
        if self._trigger_queue or self._trigger_waiting_response or self._trigger_rule_pending:
            return
        active_id = self.triggers.active_id
        generation = self._trigger_generation
        matches = self.triggers.match(text)
        if not matches:
            return
        self._trigger_rule_pending = True
        task = asyncio.create_task(self._run_trigger_rule(matches[0], active_id, generation))
        self._trigger_tasks.add(task)
        task.add_done_callback(self._trigger_tasks.discard)

    # ─── 小地图检测辅助函数 ───
    _CLEAN_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\[[0-9]*z|<[^>]+>')
    _BOX_CHARS = set('─│┌┐└┘├┤┬┴┼━┃╭╮╰╯╠╣╦╩╬═║╳⊕｜\uff5c')

    @classmethod
    def _clean_line(cls, text):
        """去除 ANSI 转义码和 MXP 标签，返回纯文本"""
        return cls._CLEAN_RE.sub('', text).strip()

    @classmethod
    def _is_minimap_line(cls, text):
        """判断一行是否是小地图行（包含 box-drawing 连接字符或 ----）"""
        clean = cls._clean_line(text)
        if not clean:
            return False
        if '----' in clean:
            return True
        for ch in clean:
            if ch in cls._BOX_CHARS:
                return True
        return False

    @classmethod
    def _get_room_name(cls, text):
        """如果是房间名行，返回房间名；否则返回 None"""
        clean = cls._clean_line(text)
        if clean and clean.endswith(' -'):
            return clean[:-2].strip()
        return None

    @staticmethod
    def _leading_spaces(text):
        """计算行首空格数（跳过 ANSI 转义码）"""
        n = 0
        i = 0
        while i < len(text):
            if text[i] == '\x1b':
                # skip ANSI sequence
                j = text.find('m', i + 1)
                if j != -1:
                    i = j + 1
                    continue
            if text[i] == ' ':
                n += 1
                i += 1
            else:
                break
        return n

    # ─── 读取 MUD 服务器 ───
    async def _read_mud_loop(self):
        """持续读取 MUD 服务器数据，转发到浏览器"""
        while self.running:
            try:
                data = await self.reader.read(4096)
                if not data:
                    break
            except (ConnectionResetError, OSError):
                break

            # 0. 记录原始字节（完全未经处理，含 Telnet IAC）
            self._log_raw_bytes(data, 'recv')

            # 1. 剥离 Telnet IAC 并回应协商
            clean = await strip_iac_and_respond(data, self.writer)
            self._mud_chunk_seq += 1

            # 2. 累积到原始字节缓冲区
            self._raw_buf.extend(clean)
            script_messages = []

            # 3. 按行分割：只解码完整的行（以 \n 结尾）
            #    这样不会在 GBK 字符中间截断
            while b'\n' in self._raw_buf:
                line_raw, rest = self._raw_buf.split(b'\n', 1)
                self._raw_buf = bytearray(rest)
                line_raw = line_raw.rstrip(b'\r')

                # GBK 解码完整行
                try:
                    line_text = line_raw.decode('gbk')
                except (UnicodeDecodeError, ValueError):
                    line_text = line_raw.decode('gbk', errors='replace')

                # 检测聊天消息
                stripped = line_text.strip()
                is_chat = stripped and is_chat_message(stripped)
                channel_id = _get_channel_id(stripped) if is_chat else None

                # 聊天消息始终推送到右侧面板（不受本地屏蔽影响）
                if is_chat:
                    clean_text = _ANSI_RE.sub('', stripped).strip()
                    msg = json.dumps({
                        'type': 'chat',
                        'data': {
                            'time': datetime.now().strftime('%H:%M:%S'),
                            'text': clean_text,
                        }
                    }, ensure_ascii=False)
                    try:
                        await self.ws.send_text(msg)
                    except Exception:
                        pass

                # 主终端：本地屏蔽的频道不显示
                if channel_id and channel_id in self.muted_channels:
                    pass  # 跳过，不发送到终端
                else:
                    utf8_line = line_text.encode('utf-8') + b'\r\n'
                    try:
                        await self.ws.send_bytes(utf8_line)
                    except Exception:
                        return

                # 记录日志
                self._log_data(line_text, 'recv')
                await self._append_character_capture(line_text)
                await self._handle_trigger_text(line_text)
                # 验证码图片捕获：出现 fullme 验证码时异步下载保存到本地。
                self._maybe_capture_captcha(line_text)

                # save 回复检测：收到提示符说明 save 完成，发送 quit
                if self._quit_pending and stripped.startswith('>'):
                    self._quit_pending = False
                    self.writer.write(b'quit\r\n')
                    await self.writer.drain()
                    self._log_data('quit', 'send')

                # 自动小地图捕获：检测每行特征
                if self._is_minimap_line(stripped):
                    if not self._minimap_active:
                        self._minimap_active = True
                        self._minimap_lines = []
                    self._minimap_lines.append(line_text)
                elif self._minimap_active:
                    room_name = self._get_room_name(stripped)
                    if room_name is not None:
                        self._minimap_lines.append(line_text)
                        if self._minimap_lines:
                            map_text = '\n'.join(self._minimap_lines) + '\n'
                            map_msg = {'type': 'map', 'data': map_text}
                            area_info = config.ROOM_TO_AREA.get(room_name)
                            if area_info:
                                map_msg['area'] = {'code': area_info[0], 'name': area_info[1]}
                            msg = json.dumps(map_msg, ensure_ascii=False)
                            try:
                                await self.ws.send_text(msg)
                            except Exception:
                                pass
                            self.runtime_log(f'[MAP] 自动小地图，{len(self._minimap_lines)} 行'
                                             f'{f" · {area_info[1]}" if area_info else ""}')
                        self._minimap_active = False
                        self._minimap_lines = []
                    elif self._leading_spaces(line_text) >= 10:
                        # 高缩进的纯文本行也是地图内容（相邻房间名等）
                        self._minimap_lines.append(line_text)
                    else:
                        self._minimap_active = False
                        self._minimap_lines = []

                script_messages.append(line_text)

            # 4. 处理缓冲区中剩余的不完整行（提示符等，无 \n 结尾）
            if self._raw_buf:
                # 确保不在 GBK 字符中间截断
                safe, rest = gbk_safe_split(self._raw_buf)
                self._raw_buf = bytearray(rest)
                if safe:
                    try:
                        text = safe.decode('gbk')
                    except (UnicodeDecodeError, ValueError):
                        text = safe.decode('gbk', errors='replace')

                    utf8_bytes = text.encode('utf-8')
                    try:
                        await self.ws.send_bytes(utf8_bytes)
                    except Exception:
                        return

                    self._log_data(text, 'recv')
                    await self._append_character_capture(text)
                    await self._handle_trigger_text(text)
                    script_messages.append(text)

                    # 检测编码选择提示
                    if 'Input 1 for GBK' in text:
                        await asyncio.sleep(0.3)
                        self.writer.write(b'1\r\n')
                        await self.writer.drain()

            # 5. 兼容：检测编码选择提示（行内匹配）
            if b'Input 1 for GBK' in clean:
                await asyncio.sleep(0.3)
                self.writer.write(b'1\r\n')
                await self.writer.drain()

            # 6. 自动跳过 MXP 检测兜底
            if b'MXP' in clean:
                for seg in clean.split(b'\n'):
                    try:
                        t = seg.decode('gbk', errors='replace')
                    except Exception:
                        continue
                    if 'MXP' in t and '\u6309\u56de\u8f66' in t:
                        await asyncio.sleep(0.5)
                        self.writer.write(b'\r\n')
                        await self.writer.drain()

            await self._finish_trigger_response()
            for script_text in script_messages:
                await self._handle_script_text(script_text)

    # ─── 读取浏览器 WebSocket ───
    async def _read_ws_loop(self):
        """持续读取浏览器 WebSocket 消息，转发到 MUD 服务器"""
        while self.running:
            try:
                msg = await self.ws.receive()
            except Exception:
                break

            if msg.get('type') == 'websocket.disconnect':
                break

            if msg.get('bytes'):
                # 二进制数据 → 原始转发
                data = bytes(msg['bytes'])
                self._log_raw_bytes(data, 'send')
                self.writer.write(data)
                await self.writer.drain()
                # 尝试解码用于日志
                try:
                    text = data.decode('utf-8', errors='replace')
                    self._log_data(text, 'send')
                except Exception:
                    pass
                continue

            text_data = msg.get('text', '')
            if not text_data:
                continue

            # JSON 消息（命令历史追踪 / MXP 回复 / 频道屏蔽）
            if text_data.startswith('{'):
                try:
                    j = json.loads(text_data)
                    if j.get('type') == 'command':
                        self._add_history(j['data'])
                        # 用户提交验证码（report/fullme + 内容）时，
                        # 用验证码内容作文件名把缓存的验证码图片落盘，
                        # 保证图片与答案一一对应。
                        cmd = str(j.get('data', '') or '').strip()
                        code = _extract_captcha_code(cmd)
                        if code is not None:
                            saved = captcha_saver.commit_cached(code)
                            if saved:
                                self.runtime_log(f'[CAPTCHA] 验证码已记录: {code} -> {saved}')
                    elif j.get('type') == 'captcha_image':
                        # 前端回传小窗里已成功加载的验证码图片(base64)，落盘存档。
                        # 这是验证码图片最可靠的来源（后端裸下载会因图片过期 404）。
                        try:
                            captcha_saver.save_base64(j.get('url', ''), j.get('data', ''))
                        except Exception as e:
                            self.runtime_log(f'[CAPTCHA] 小窗图片保存失败: {e}')
                    elif j.get('type') == 'mxp_reply':
                        reply = j.get('data', '')
                        if reply:
                            raw = reply.encode('gbk', errors='replace')
                            self._log_raw_bytes(raw, 'send')
                            self.writer.write(raw)
                            await self.writer.drain()
                    elif j.get('type') == 'mute_channels':
                        self.muted_channels = set(j.get('data', []))
                    elif j.get('type') == 'trigger':
                        await self._handle_trigger_ws(j)
                    elif j.get('type') == 'quick_command':
                        await self._handle_quick_command_ws(j)
                    elif j.get('type') == 'script':
                        await self._handle_script_ws(j)
                    elif j.get('type') == 'quit_game':
                        self._quit_pending = True
                        self.writer.write(b'save\r\n')
                        await self.writer.drain()
                        self._log_data('save', 'send')
                except (json.JSONDecodeError, KeyError):
                    pass
                continue

            # 普通文本 → 转码为 GBK 发送到 MUD
            try:
                data = text_data.encode('gbk')
            except Exception:
                data = text_data.encode('utf-8', errors='replace')

            self._log_raw_bytes(data, 'send')
            self.writer.write(data)
            await self.writer.drain()
            await self._start_character_capture(text_data)
            self._log_data(text_data, 'send')

    # ─── 命令历史 ───
    def _add_history(self, cmd):
        """添加命令到历史，保持最近 20 条"""
        if not cmd or not cmd.strip():
            return
        cmd = cmd.strip()
        # 去重：如果和最后一条相同则跳过
        if self.cmd_history and self.cmd_history[-1] == cmd:
            return
        self.cmd_history.append(cmd)
        if len(self.cmd_history) > 20:
            self.cmd_history = self.cmd_history[-20:]

        # 推送到浏览器
        msg = json.dumps({
            'type': 'history',
            'data': self.cmd_history,
        }, ensure_ascii=False)

        async def _send():
            try:
                await self.ws.send_text(msg)
            except Exception:
                pass

        asyncio.create_task(_send())

    # ─── 日志 ───
    def _open_raw_log(self):
        """打开当天的原始字节日志文件（追加模式）"""
        if self._raw_log_file:
            return
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_path = os.path.join(self.log_dir, f'{date_str}_raw.bin')
        try:
            self._raw_log_file = open(log_path, 'ab')
        except Exception:
            self._raw_log_file = None

    def _log_raw_bytes(self, data, direction):
        """记录原始字节到 .bin 日志（未经任何转码、剥离、解码处理）

        格式：每条消息一行，[HH:MM:SS.mmm] >>>/<<< 后跟原始字节，以 \\n 结尾。
        注意：如果原始数据本身含 \\n，解析时需按时间戳行首分割。
        """
        if not data:
            return
        if not self._raw_log_file:
            self._open_raw_log()
        if not self._raw_log_file:
            return
        marker = b'>>>' if direction == 'send' else b'<<<'
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:12].encode('ascii')
        try:
            self._raw_log_file.write(b'[' + timestamp + b'] ' + marker + b' ')
            self._raw_log_file.write(data)
            self._raw_log_file.write(b'\n')
            self._raw_log_file.flush()
        except Exception:
            pass

    def _log_data(self, text, direction):
        """记录日志（与 proxy.py 格式一致）"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        marker = '>>>' if direction == 'send' else '<<<'
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_path = os.path.join(self.log_dir, f'{date_str}_raw.log')

        text = text.replace('\r\n', '\n').replace('\r', '\n')
        try:
            with open(log_path, 'a', encoding=config.LOG_ENCODING) as f:
                for line in text.split('\n'):
                    if line.strip():
                        f.write(f'[{timestamp}] {marker} {line}\n')
        except Exception:
            pass

        # 运行时日志
        for line in text.split('\n'):
            stripped = line.strip()
            if stripped:
                self.runtime_log(f'[{marker}] {stripped[:500]}')


# ═══════════════════════════════════════════
#  Starlette 路由
# ═══════════════════════════════════════════

