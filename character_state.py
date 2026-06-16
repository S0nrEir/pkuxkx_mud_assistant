"""Persistent character state snapshots captured from MUD command output."""

import json
import os
from datetime import datetime

import config


SECTION_LABELS = {
    'score': '人物属性',
    'hp': '状态',
    'inventory': '道具',
}

COMMAND_SECTIONS = {
    'sc': 'score',
    'score': 'score',
    'hp': 'hp',
    'i': 'inventory',
    'inventory': 'inventory',
}


class CharacterStateStore:
    def __init__(self, path=None):
        self.path = path or os.path.join(os.path.dirname(__file__), config.LOG_DIR, 'character_state.json')

    def default_state(self):
        return {
            'updated_at': '',
            'sections': {
                key: {
                    'label': label,
                    'command': '',
                    'updated_at': '',
                    'text': '',
                }
                for key, label in SECTION_LABELS.items()
            },
        }

    def load(self):
        state = self.default_state()
        try:
            with open(self.path, 'r', encoding='utf-8-sig') as f:
                saved = json.load(f)
        except Exception:
            return state

        if not isinstance(saved, dict):
            return state
        state['updated_at'] = str(saved.get('updated_at') or '')
        saved_sections = saved.get('sections') if isinstance(saved.get('sections'), dict) else {}
        for section, defaults in state['sections'].items():
            source = saved_sections.get(section)
            if not isinstance(source, dict):
                continue
            defaults['command'] = str(source.get('command') or '')
            defaults['updated_at'] = str(source.get('updated_at') or '')
            defaults['text'] = str(source.get('text') or '')
        return state

    def save(self, state):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def update(self, section, command, text):
        if section not in SECTION_LABELS:
            return self.load()
        now = datetime.now().isoformat(timespec='seconds')
        state = self.load()
        state['updated_at'] = now
        state['sections'][section] = {
            'label': SECTION_LABELS[section],
            'command': str(command or ''),
            'updated_at': now,
            'text': str(text or '').strip(),
        }
        self.save(state)
        return state


def section_for_command(command):
    command = str(command or '').strip().lower()
    if not command:
        return None
    first = command.split()[0]
    if first != command:
        return None
    return COMMAND_SECTIONS.get(first)


default_character_state_store = CharacterStateStore()
