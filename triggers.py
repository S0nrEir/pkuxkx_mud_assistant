"""Persistent message-trigger configuration."""

import json
import os
import re


TRIGGER_DIR = os.path.join(os.path.dirname(__file__), 'triggers')


def _safe_id(name):
    name = str(name or '').strip()
    slug = re.sub(r'[^\w\u4e00-\u9fff.-]+', '_', name, flags=re.UNICODE).strip('._')
    return slug or 'trigger'


def _path(trigger_id):
    return os.path.join(TRIGGER_DIR, f'{_safe_id(trigger_id)}.json')


def normalize_config(config):
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
        if keyword and command:
            clean_rules.append({'keyword': keyword, 'command': command, 'delay': delay})
    return {
        'name': str(config.get('name') or '').strip(),
        'notes': str(config.get('notes') or ''),
        'rules': clean_rules,
    }


def validate_config(config):
    config = normalize_config(config)
    if not config['name']:
        raise ValueError('必须填写触发器名称')
    return config


def save_config(config, trigger_id=None):
    config = validate_config(config)
    os.makedirs(TRIGGER_DIR, exist_ok=True)
    old_id = _safe_id(trigger_id) if trigger_id else ''
    new_id = _safe_id(config['name'])
    with open(_path(new_id), 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    if old_id and old_id != new_id:
        old_path = _path(old_id)
        if os.path.exists(old_path):
            os.remove(old_path)
    return new_id, config


def load_config(trigger_id):
    with open(_path(trigger_id), 'r', encoding='utf-8') as f:
        return normalize_config(json.load(f))


def delete_config(trigger_id):
    path = _path(trigger_id)
    if os.path.exists(path):
        os.remove(path)


def list_configs():
    items = []
    if not os.path.isdir(TRIGGER_DIR):
        return items
    for filename in sorted(os.listdir(TRIGGER_DIR)):
        if not filename.endswith('.json'):
            continue
        trigger_id = filename[:-5]
        try:
            config = load_config(trigger_id)
        except Exception:
            continue
        items.append({
            'id': trigger_id,
            'name': config.get('name') or trigger_id,
            'rules_count': len(config.get('rules') or []),
            'config': config,
        })
    return items


class TriggerRuntime:
    def __init__(self):
        self.active_id = ''
        self.config = None

    @property
    def active(self):
        return bool(self.config)

    def load(self, trigger_id, config=None):
        self.active_id = _safe_id(trigger_id)
        self.config = normalize_config(config if config is not None else load_config(trigger_id))
        return self.config

    def stop(self):
        self.active_id = ''
        self.config = None

    def match(self, text):
        if not self.config:
            return []
        text = str(text or '')
        matched = []
        for rule in self.config.get('rules') or []:
            if rule['keyword'] in text:
                matched.append(rule)
        return matched
