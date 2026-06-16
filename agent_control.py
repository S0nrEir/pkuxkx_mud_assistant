"""Local agent control surface for the active Web MUD session."""

import asyncio
import os
import re
from collections import deque
from datetime import datetime

import config


_ANSI_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07|\x1b\[[0-9]*z|<[^>]+>')
_TOKEN_RE = re.compile(r'^\s*([^\s;]+)', re.I)

_SENSITIVE_PATTERNS = [
    (re.compile(r'^\s*(?:quit|suicide|passwd|password)\b', re.I), 'system_or_account'),
    (re.compile(r'^\s*(?:drop|give|sell|auction|paimai|discard|destroy)\b', re.I), 'item_or_trade'),
    (re.compile(r'^\s*(?:kill|k|fight|f|hit|attack|touxi|ansha)\b', re.I), 'combat'),
    (re.compile(r'^\s*(?:join|leave|dismiss|expel|betray|panshi|tuoli)\b', re.I), 'affiliation'),
    (re.compile(r'\b(?:to\s+\S+|with\s+\S+)\b.*\b(?:gold|coin|silver|cash|money)\b', re.I), 'trade'),
]


def clean_text(text):
    return _ANSI_RE.sub('', str(text or '')).strip()


class AgentControlService:
    """Tracks the active session and exposes safe local command execution."""

    def __init__(self, max_events=500):
        self._session = None
        self._paused = False
        self._events = deque(maxlen=max_events)
        self._seq = 0
        self._lock = asyncio.Lock()
        self.log_dir = os.path.join(os.path.dirname(__file__), config.LOG_DIR)

    @property
    def active_session(self):
        if self._session and getattr(self._session, 'running', False):
            return self._session
        return None

    def register_session(self, session):
        self._session = session
        self.record_event('session', {'status': 'connected'})

    def unregister_session(self, session):
        if self._session is session:
            self._session = None
        self.record_event('session', {'status': 'disconnected'})

    def record_event(self, kind, data=None):
        self._seq += 1
        event = {
            'seq': self._seq,
            'time': datetime.now().isoformat(timespec='seconds'),
            'kind': str(kind or 'event'),
            'data': data or {},
        }
        self._events.append(event)
        return event

    def status(self):
        session = self.active_session
        return {
            'active': bool(session),
            'paused': self._paused,
            'last_seq': self._seq,
            'mud_host': config.MUD_HOST,
            'mud_port': config.MUD_PORT,
            'history_count': len(getattr(session, 'cmd_history', []) if session else []),
        }

    def observe(self, since=0, limit=100, include_runtime=True):
        try:
            since = int(since or 0)
        except (TypeError, ValueError):
            since = 0
        try:
            limit = int(limit or 100)
        except (TypeError, ValueError):
            limit = 100
        limit = max(1, min(limit, 500))
        events = [event for event in self._events if event['seq'] > since][-limit:]
        payload = {
            'status': self.status(),
            'events': events,
        }
        if include_runtime:
            payload['runtime_tail'] = self._runtime_tail()
        return payload

    def pause(self):
        self._paused = True
        self.record_event('agent_state', {'paused': True})
        return self.status()

    def resume(self):
        self._paused = False
        self.record_event('agent_state', {'paused': False})
        return self.status()

    def assess_command(self, command):
        command = str(command or '').strip()
        if not command:
            return {'ok': False, 'reason': 'empty_command'}
        for pattern, reason in _SENSITIVE_PATTERNS:
            if pattern.search(command):
                return {
                    'ok': False,
                    'needs_approval': True,
                    'reason': reason,
                    'command': command,
                }
        token_match = _TOKEN_RE.match(command)
        token = token_match.group(1).lower() if token_match else ''
        if token in {'rm', 'del', 'delete'}:
            return {
                'ok': False,
                'needs_approval': True,
                'reason': 'destructive_alias',
                'command': command,
            }
        return {'ok': True, 'command': command}

    async def send_command(self, command, reason='', approved=False):
        command = str(command or '').strip()
        if self._paused:
            return {'ok': False, 'error': 'agent_paused'}
        session = self.active_session
        if not session:
            return {'ok': False, 'error': 'no_active_session'}
        assessment = self.assess_command(command)
        if not assessment.get('ok') and not approved:
            self.record_event('blocked_command', {
                'command': command,
                'reason': assessment.get('reason'),
                'needs_approval': bool(assessment.get('needs_approval')),
            })
            return assessment
        async with self._lock:
            await session.send_agent_command(command, reason=reason)
        event = self.record_event('agent_command', {
            'command': command,
            'reason': str(reason or ''),
            'approved': bool(approved),
        })
        return {'ok': True, 'event': event}

    async def send_batch(self, commands):
        if not isinstance(commands, list):
            return {'ok': False, 'error': 'commands_must_be_list'}
        results = []
        for item in commands:
            if isinstance(item, dict):
                command = item.get('command', '')
                reason = item.get('reason', '')
                approved = bool(item.get('approved', False))
                delay = item.get('delay', 0)
            else:
                command = str(item or '')
                reason = ''
                approved = False
                delay = 0
            try:
                delay = max(0, min(float(delay or 0), 3600))
            except (TypeError, ValueError):
                delay = 0
            if delay:
                await asyncio.sleep(delay)
            result = await self.send_command(command, reason=reason, approved=approved)
            results.append({'command': command, 'result': result})
            if not result.get('ok'):
                break
        return {'ok': all(r['result'].get('ok') for r in results), 'results': results}

    def _runtime_tail(self, max_lines=80):
        path = os.path.join(self.log_dir, 'runtime.log')
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
        except OSError:
            return []
        return [line.rstrip('\n') for line in lines[-max_lines:]]


agent_control = AgentControlService()
