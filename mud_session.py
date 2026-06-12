"""WebSocket/TCP session bridge for the web MUD client."""

import asyncio
import json
import os
import re
from datetime import datetime

import config
from chat_monitor import is_chat_message
from mud_telnet import gbk_safe_split, strip_iac_and_respond
from triggers import TriggerRuntime, delete_config, list_configs, load_config, save_config

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07')

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
        self.muted_channels = set()   # 本地屏蔽的频道（终端不显示，右侧仍显示）
        self.triggers = TriggerRuntime()
        self._trigger_lock = asyncio.Lock()
        self._trigger_tasks = set()
        self._trigger_queue = []
        self._trigger_waiting_response = False
        self._trigger_response_parts = []
        self._trigger_waiting_chunk = 0
        self._trigger_generation = 0
        self._mud_chunk_seq = 0
        self._raw_log_file = None   # 原始字节日志文件句柄

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

    async def _send_mud_command(self, command):
        command = str(command or '').strip()
        if not command or not self.writer:
            return
        self.writer.write((command + '\r\n').encode('gbk', errors='replace'))
        await self.writer.drain()
        self._trigger_response_parts = []
        self._trigger_waiting_chunk = self._mud_chunk_seq
        self._log_data(command, 'send')
        await self._send_ws_json({
            'type': 'trigger_event',
            'command': command,
            'active': self.triggers.active,
        })

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
            await self._advance_trigger_queue()

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
            try:
                trigger_id = msg.get('id') or ''
                self._cancel_trigger_tasks()
                config_data = self.triggers.load(trigger_id, load_config(trigger_id))
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

    async def _handle_trigger_text(self, text):
        if self._trigger_waiting_response:
            self._trigger_response_parts.append(str(text or ''))
            return

        await self._match_trigger_text(text)

    async def _match_trigger_text(self, text):
        if self._trigger_queue or self._trigger_waiting_response:
            return
        active_id = self.triggers.active_id
        generation = self._trigger_generation
        matches = self.triggers.match(text)
        if not matches:
            return
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
                await self._handle_trigger_text(line_text)

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
                    await self._handle_trigger_text(text)

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

