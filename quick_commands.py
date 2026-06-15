"""Persistent quick-command configuration service."""

import json
import os
import re


QUICK_COMMAND_DIR = os.path.join(os.path.dirname(__file__), 'quick_commands')
_SAFE_ID_RE = re.compile(r'[^\w\u4e00-\u9fff.-]+', flags=re.UNICODE)


class QuickCommandService:
    """File-backed service for quick command CRUD operations."""

    def __init__(self, command_dir=None):
        self.command_dir = command_dir or QUICK_COMMAND_DIR

    def safe_id(self, name):
        name = str(name or '').strip()
        slug = _SAFE_ID_RE.sub('_', name).strip('._')
        return slug or 'quick_command'

    def path_for(self, command_id):
        return os.path.join(self.command_dir, f'{self.safe_id(command_id)}.json')

    def normalize(self, config):
        config = config if isinstance(config, dict) else {}
        steps = config.get('commands') if isinstance(config.get('commands'), list) else []
        clean_steps = []
        for step in steps:
            if isinstance(step, dict):
                command = str(step.get('command') or '').strip()
                delay_raw = step.get('delay')
            else:
                command = str(step or '').strip()
                delay_raw = 0
            try:
                delay = float(delay_raw or 0)
            except (TypeError, ValueError):
                delay = 0
            delay = max(0, min(delay, 3600))
            if command:
                clean_steps.append({'command': command, 'delay': delay})
        return {
            'name': str(config.get('name') or '').strip(),
            'alias': str(config.get('alias') or '').strip(),
            'notes': str(config.get('notes') or ''),
            'commands': clean_steps,
        }

    def validate(self, config):
        config = self.normalize(config)
        if not config['name']:
            raise ValueError('必须填写快捷命令名称')
        if not config['commands']:
            raise ValueError('至少填写一条指令')
        return config

    def save(self, config, command_id=None):
        config = self.validate(config)
        os.makedirs(self.command_dir, exist_ok=True)
        old_id = self.safe_id(command_id) if command_id else ''
        new_id = self.safe_id(config['name'])
        with open(self.path_for(new_id), 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        if old_id and old_id != new_id:
            old_path = self.path_for(old_id)
            if os.path.exists(old_path):
                os.remove(old_path)
        return new_id, config

    def load(self, command_id):
        with open(self.path_for(command_id), 'r', encoding='utf-8-sig') as f:
            return self.normalize(json.load(f))

    def delete(self, command_id):
        path = self.path_for(command_id)
        if os.path.exists(path):
            os.remove(path)

    def list(self):
        items = []
        if not os.path.isdir(self.command_dir):
            return items
        for filename in sorted(os.listdir(self.command_dir)):
            if not filename.endswith('.json'):
                continue
            command_id = filename[:-5]
            try:
                config = self.load(command_id)
            except Exception:
                continue
            items.append({
                'id': command_id,
                'name': config.get('name') or command_id,
                'commands_count': len(config.get('commands') or []),
                'config': config,
            })
        return items


default_quick_command_service = QuickCommandService()


def list_configs():
    return default_quick_command_service.list()


def save_config(config, command_id=None):
    return default_quick_command_service.save(config, command_id)


def load_config(command_id):
    return default_quick_command_service.load(command_id)


def delete_config(command_id):
    return default_quick_command_service.delete(command_id)
