"""Persistent script configuration and runtime service."""

import asyncio
import importlib.util
import json
import os
import re
import time
import traceback


SCRIPT_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
SCRIPT_INDEX = os.path.join(SCRIPT_DIR, 'index.json')
_CLEAN_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\[[0-9]*z|<[^>]+>')
_SAFE_ID_RE = re.compile(r'[^\w\u4e00-\u9fff.-]+', flags=re.UNICODE)


class ScriptConfigService:
    """File-backed service for script index CRUD operations."""

    def __init__(self, script_dir=None, index_path=None):
        self.script_dir = script_dir or SCRIPT_DIR
        self.index_path = index_path or SCRIPT_INDEX

    def safe_id(self, name):
        name = str(name or '').strip()
        slug = _SAFE_ID_RE.sub('_', name).strip('._')
        return slug or 'script'

    def _default_index(self):
        return {'scripts': []}

    def _read_index(self):
        if not os.path.exists(self.index_path):
            return self._default_index()
        with open(self.index_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        return data if isinstance(data, dict) else self._default_index()

    def _write_index(self, data):
        os.makedirs(self.script_dir, exist_ok=True)
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def normalize(self, config):
        config = config if isinstance(config, dict) else {}
        return {
            'name': str(config.get('name') or '').strip(),
            'notes': str(config.get('notes') or ''),
            'path': str(config.get('path') or '').strip().replace('\\', '/'),
        }

    def validate(self, config):
        config = self.normalize(config)
        if not config['name']:
            raise ValueError('必须填写脚本名称')
        if not config['path']:
            raise ValueError('必须填写脚本路径')
        if self._is_unsafe_path(config['path']):
            raise ValueError('脚本路径必须位于 scripts 目录内')
        if not config['path'].endswith('.py'):
            raise ValueError('脚本路径必须是 .py 文件')
        return config

    @staticmethod
    def _is_unsafe_path(path):
        path = str(path or '').replace('\\', '/')
        return (
            os.path.isabs(path)
            or path.startswith('/')
            or bool(re.match(r'^[a-zA-Z]:', path))
            or '..' in path.split('/')
        )

    def resolve_script_path(self, path):
        safe_path = str(path or '').replace('\\', '/')
        if self._is_unsafe_path(safe_path):
            raise ValueError('脚本路径必须位于 scripts 目录内')
        full_path = os.path.abspath(os.path.join(self.script_dir, safe_path))
        root = os.path.abspath(self.script_dir)
        if os.path.commonpath([root, full_path]) != root:
            raise ValueError('脚本路径必须位于 scripts 目录内')
        return full_path

    def save(self, config, script_id=None):
        config = self.validate(config)
        data = self._read_index()
        scripts = data.get('scripts') if isinstance(data.get('scripts'), list) else []
        old_id = self.safe_id(script_id) if script_id else ''
        new_id = self.safe_id(config['name'])
        found = False
        normalized = {'id': new_id, **config}
        next_scripts = []
        for item in scripts:
            item_id = self.safe_id((item or {}).get('id') or (item or {}).get('name'))
            if old_id and item_id == old_id:
                if not found:
                    next_scripts.append(normalized)
                    found = True
                continue
            if item_id == new_id:
                continue
            next_scripts.append(self._normalize_index_item(item))
        if not found:
            next_scripts.append(normalized)
        data['scripts'] = next_scripts
        self._write_index(data)
        return new_id, config

    def _normalize_index_item(self, item):
        item = item if isinstance(item, dict) else {}
        item_id = self.safe_id(item.get('id') or item.get('name'))
        config = self.normalize(item)
        return {'id': item_id, **config}

    def load(self, script_id):
        script_id = self.safe_id(script_id)
        for item in self.list():
            if item['id'] == script_id:
                return item['config']
        raise FileNotFoundError(script_id)

    def delete(self, script_id):
        script_id = self.safe_id(script_id)
        data = self._read_index()
        scripts = data.get('scripts') if isinstance(data.get('scripts'), list) else []
        data['scripts'] = [
            self._normalize_index_item(item)
            for item in scripts
            if self.safe_id((item or {}).get('id') or (item or {}).get('name')) != script_id
        ]
        self._write_index(data)

    def list(self):
        data = self._read_index()
        scripts = data.get('scripts') if isinstance(data.get('scripts'), list) else []
        items = []
        for raw in scripts:
            item = self._normalize_index_item(raw)
            config = {'name': item['name'], 'notes': item['notes'], 'path': item['path']}
            exists = False
            try:
                exists = os.path.exists(self.resolve_script_path(config['path']))
            except ValueError:
                exists = False
            items.append({
                'id': item['id'],
                'name': config.get('name') or item['id'],
                'path': config.get('path') or '',
                'exists': exists,
                'config': config,
            })
        return items


class ScriptTools:
    """Helpers passed into custom scripts."""

    def __init__(self, send_command=None, runtime_log=None):
        self._send_command = send_command
        self._runtime_log = runtime_log or (lambda msg: None)

    def clean(self, text):
        return _CLEAN_RE.sub('', str(text or '')).strip()

    def contains(self, text, keyword):
        keyword = str(keyword or '')
        return bool(keyword) and keyword in self.clean(text)

    def contains_any(self, text, keywords):
        clean = self.clean(text)
        return any(keyword in clean for keyword in (str(item or '') for item in (keywords or [])) if keyword)

    def regex(self, text, pattern, flags=0):
        return re.search(pattern, self.clean(text), flags)

    async def send(self, command):
        if self._send_command:
            await self._send_command(command)

    async def delay(self, seconds):
        try:
            seconds = float(seconds or 0)
        except (TypeError, ValueError):
            seconds = 0
        await asyncio.sleep(max(0, seconds))

    def log(self, message):
        self._runtime_log(f'[SCRIPT] {message}')

    def now(self):
        return time.time()


class ScriptRuntime:
    def __init__(self, config_service=None, runtime_log=None, send_command=None):
        self.config_service = config_service or default_script_service
        self.runtime_log = runtime_log or (lambda msg: None)
        self.send_command = send_command
        self.active_id = ''
        self.config = None
        self.module = None

    @property
    def active(self):
        return bool(self.config and self.module)

    def _cleanup_module(self, module):
        cleanup = getattr(module, 'cleanup', None)
        if not callable(cleanup):
            return
        try:
            result = cleanup()
            if hasattr(result, '__await__'):
                try:
                    asyncio.get_running_loop().create_task(result)
                except RuntimeError:
                    close = getattr(result, 'close', None)
                    if callable(close):
                        close()
                    self.runtime_log('[SCRIPT] 异步清理需要在事件循环中执行，已跳过')
        except Exception:
            self.runtime_log('[SCRIPT] 清理失败:\n' + traceback.format_exc())

    def load(self, script_id, config=None):
        script_id = self.config_service.safe_id(script_id)
        source_config = config if config is not None else self.config_service.load(script_id)
        loaded_config = self.config_service.normalize(source_config)
        script_path = self.config_service.resolve_script_path(loaded_config['path'])
        if not os.path.exists(script_path):
            raise FileNotFoundError(script_path)
        module_name = f'mud_user_script_{script_id}_{int(time.time() * 1000)}'
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if not spec or not spec.loader:
            raise ImportError(f'无法加载脚本模块: {script_path}')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        handler = getattr(module, 'handle_message', None)
        if not callable(handler):
            raise ValueError('脚本必须实现 handle_message(message, tools) 接口')
        self._cleanup_module(self.module)
        self.active_id = script_id
        self.config = loaded_config
        self.module = module
        return loaded_config

    def stop(self):
        self._cleanup_module(self.module)
        self.active_id = ''
        self.config = None
        self.module = None

    async def handle_message(self, message):
        if not self.active:
            return
        tools = ScriptTools(send_command=self.send_command, runtime_log=self.runtime_log)
        handler = getattr(self.module, 'handle_message', None)
        try:
            result = handler(message, tools)
            if hasattr(result, '__await__'):
                await result
        except Exception:
            self.runtime_log('[SCRIPT] 执行失败:\n' + traceback.format_exc())


default_script_service = ScriptConfigService()


def list_configs():
    return default_script_service.list()


def save_config(config, script_id=None):
    return default_script_service.save(config, script_id)


def load_config(script_id):
    return default_script_service.load(script_id)


def delete_config(script_id):
    return default_script_service.delete(script_id)
