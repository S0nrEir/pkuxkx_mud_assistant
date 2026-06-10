"""Persistent message-trigger configuration service."""

import json
import os
import re


TRIGGER_DIR = os.path.join(os.path.dirname(__file__), 'triggers')
_CLEAN_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\[[0-9]*z|<[^>]+>')
_SAFE_ID_RE = re.compile(r'[^\w\u4e00-\u9fff.-]+', flags=re.UNICODE)


class TriggerConfigService:
    """File-backed service for trigger configuration CRUD operations."""

    def __init__(self, trigger_dir=None):
        self.trigger_dir = trigger_dir or TRIGGER_DIR

    def safe_id(self, name):
        name = str(name or '').strip()
        slug = _SAFE_ID_RE.sub('_', name).strip('._')
        return slug or 'trigger'

    def path_for(self, trigger_id):
        return os.path.join(self.trigger_dir, f'{self.safe_id(trigger_id)}.json')

    def normalize(self, config):
        config = config if isinstance(config, dict) else {}
        rules = config.get('rules') if isinstance(config.get('rules'), list) else []
        clean_rules = []
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            keyword = str(rule.get('keyword') or '').strip()
            command = str(rule.get('command') or '').strip()
            try:
                delay = float(rule.get('delay') or 0)
            except (TypeError, ValueError):
                delay = 0
            delay = max(0, min(delay, 3600))
            if keyword or command:
                clean_rules.append({'keyword': keyword, 'command': command, 'delay': delay})
        return {
            'name': str(config.get('name') or '').strip(),
            'notes': str(config.get('notes') or ''),
            'rules': clean_rules,
        }

    def validate(self, config):
        config = self.normalize(config)
        if not config['name']:
            raise ValueError('必须填写触发器名称')
        return config

    def save(self, config, trigger_id=None):
        config = self.validate(config)
        os.makedirs(self.trigger_dir, exist_ok=True)
        old_id = self.safe_id(trigger_id) if trigger_id else ''
        new_id = self.safe_id(config['name'])
        with open(self.path_for(new_id), 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        if old_id and old_id != new_id:
            old_path = self.path_for(old_id)
            if os.path.exists(old_path):
                os.remove(old_path)
        return new_id, config

    def load(self, trigger_id):
        with open(self.path_for(trigger_id), 'r', encoding='utf-8-sig') as f:
            return self.normalize(json.load(f))

    def delete(self, trigger_id):
        path = self.path_for(trigger_id)
        if os.path.exists(path):
            os.remove(path)

    def list(self):
        items = []
        if not os.path.isdir(self.trigger_dir):
            return items
        for filename in sorted(os.listdir(self.trigger_dir)):
            if not filename.endswith('.json'):
                continue
            trigger_id = filename[:-5]
            try:
                config = self.load(trigger_id)
            except Exception:
                continue
            items.append({
                'id': trigger_id,
                'name': config.get('name') or trigger_id,
                'rules_count': len(config.get('rules') or []),
                'config': config,
            })
        return items


default_trigger_service = TriggerConfigService()


def _safe_id(name):
    return default_trigger_service.safe_id(name)


def _path(trigger_id):
    return default_trigger_service.path_for(trigger_id)


def normalize_config(config):
    return default_trigger_service.normalize(config)


def validate_config(config):
    return default_trigger_service.validate(config)


def save_config(config, trigger_id=None):
    return default_trigger_service.save(config, trigger_id)


def load_config(trigger_id):
    return default_trigger_service.load(trigger_id)


def delete_config(trigger_id):
    return default_trigger_service.delete(trigger_id)


def list_configs():
    return default_trigger_service.list()


class TriggerRuntime:
    def __init__(self, config_service=None):
        self.config_service = config_service or default_trigger_service
        self.active_id = ''
        self.config = None

    @property
    def active(self):
        return bool(self.config)

    def load(self, trigger_id, config=None):
        self.active_id = self.config_service.safe_id(trigger_id)
        source_config = config if config is not None else self.config_service.load(trigger_id)
        self.config = self.config_service.normalize(source_config)
        return self.config

    def stop(self):
        self.active_id = ''
        self.config = None

    def match(self, text):
        if not self.config:
            return []
        text = _CLEAN_RE.sub('', str(text or ''))
        matched = []
        for rule in self.config.get('rules') or []:
            if rule['keyword'] and rule['command'] and rule['keyword'] in text:
                matched.append(rule)
        return matched
