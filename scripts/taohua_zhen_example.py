"""桃花阵自动行走脚本。

使用方式：
1. 启用脚本系统。
2. 找陆乘风接任务并让他算卦。
3. 如果脚本没有看到铁八卦表，会使用日志中稳定出现的默认八卦表。
4. 自己走进东面的桃花林后，脚本会按卦象方向循环行走。
"""

import asyncio
import re


RETRY_DELAY_SECONDS = 3.0
MOVE_DELAY_SECONDS = 0.8

TRIGRAM_DIRECTIONS = {
    '乾天': ['东', '东北', '西', '南'],
    '兑泽': ['北', '西南', '西北', '南'],
    '离火': ['南', '北', '东南', '西北'],
    '震雷': ['西', '东南', '北', '北'],
    '巽风': ['东南', '东', '南', '西南'],
    '坎水': ['东北', '北', '西南', '西北'],
    '艮山': ['西南', '西', '西', '南'],
    '坤地': ['西北', '西北', '南', '东'],
}

DIRECTION_COMMANDS = {
    '东': 'e',
    '西': 'w',
    '南': 's',
    '北': 'n',
    '东北': 'ne',
    '西北': 'nw',
    '东南': 'se',
    '西南': 'sw',
}

TRIGRAM_PATTERN = re.compile(r'(乾天|兑泽|离火|震雷|巽风|坎水|艮山|坤地)[：:]\s*(.+)')
DIVINATION_PATTERN = re.compile(r'占得一卦[：:]\s*(乾天|兑泽|离火|震雷|巽风|坎水|艮山|坤地)')


state = {
    'gua': '',
    'directions': [],
    'commands': [],
    'step': 0,
    'in_maze': False,
    'waiting': False,
    'last_command': '',
    'pending_task': None,
    'send_token': 0,
    'busy_retries': 0,
    'round_completed': False,
    'stopped': False,
}


def _directions_to_commands(directions):
    commands = []
    for direction in directions:
        command = DIRECTION_COMMANDS.get(direction)
        if not command:
            return []
        commands.append(command)
    return commands


def _remember_gua(gua, tools):
    directions = TRIGRAM_DIRECTIONS.get(gua) or []
    commands = _directions_to_commands(directions)
    state['gua'] = gua
    state['directions'] = list(directions)
    state['commands'] = commands
    state['step'] = 0
    state['waiting'] = False
    state['last_command'] = ''
    state['busy_retries'] = 0
    state['round_completed'] = False
    state['stopped'] = False
    if commands:
        tools.log(f'记录桃花阵卦象：{gua} -> {" ".join(directions)} -> {" ".join(commands)}')
    else:
        tools.log(f'记录桃花阵卦象：{gua}，但还没有对应方向')


def _parse_trigram_table_line(text, tools):
    match = TRIGRAM_PATTERN.search(text)
    if not match:
        return
    gua = match.group(1)
    directions = [part.strip() for part in match.group(2).split() if part.strip()]
    commands = _directions_to_commands(directions)
    if len(commands) != len(directions) or not commands:
        return
    old = TRIGRAM_DIRECTIONS.get(gua)
    TRIGRAM_DIRECTIONS[gua] = directions
    if old != directions:
        tools.log(f'更新铁八卦：{gua} -> {" ".join(directions)}')
    if state.get('gua') == gua:
        _remember_gua(gua, tools)


def _cancel_pending_send():
    task = state.get('pending_task')
    if task and not task.done():
        task.cancel()
    state['pending_task'] = None


def _stop_auto_walking(tools, reason, message=''):
    """停止自动行走并清理待发送命令。

    天色大变等导致卦象失效时调用：取消后台延迟任务、清掉迷宫等待状态，
    并在网页消息列表输出一条醒目的大号加粗消息提示脚本已停止。
    message 留空时使用默认提示。
    """
    _cancel_pending_send()
    was_running = state.get('in_maze') or state.get('waiting')
    state['in_maze'] = False
    state['waiting'] = False
    state['last_command'] = ''
    state['stopped'] = True
    tools.log(f'桃花阵停止自动行走：{reason}')
    if was_running:
        tools.notify(message or f'桃花阵脚本已停止：{reason}')


async def _send_current_direction(tools):
    commands = state.get('commands') or []
    if not commands:
        tools.log('还没有可用的桃花阵方向，先找陆乘风算卦或 look tu')
        return
    step = state.get('step', 0) % len(commands)
    command = commands[step]
    direction = state.get('directions', [''])[step]
    state['waiting'] = True
    state['last_command'] = command
    tools.log(f'发送桃花阵第 {step + 1}/{len(commands)} 步：{direction} ({command})')
    await tools.send(command)


async def _delayed_send(tools, delay, token):
    await tools.delay(delay)
    if token != state.get('send_token'):
        return
    state['pending_task'] = None
    if state.get('in_maze'):
        await _send_current_direction(tools)


def _schedule_send(tools, delay=0):
    if not state.get('in_maze'):
        return
    _cancel_pending_send()
    state['send_token'] += 1
    token = state['send_token']
    if delay <= 0:
        state['pending_task'] = asyncio.create_task(_delayed_send(tools, 0, token))
    else:
        state['pending_task'] = asyncio.create_task(_delayed_send(tools, delay, token))


def _advance_after_success(tools):
    if not state.get('waiting'):
        return
    commands = state.get('commands') or []
    if not commands:
        return
    state['step'] = (state.get('step', 0) + 1) % len(commands)
    state['waiting'] = False
    state['last_command'] = ''
    state['busy_retries'] = 0
    state['round_completed'] = False
    _schedule_send(tools, MOVE_DELAY_SECONDS)


def _reset_round(tools):
    if not state.get('commands'):
        return
    if state.get('round_completed'):
        return
    state['in_maze'] = True
    state['step'] = 0
    state['waiting'] = False
    state['last_command'] = ''
    state['busy_retries'] = 0
    state['round_completed'] = True
    tools.log('桃花阵一轮完成，方向从头开始')
    _schedule_send(tools, MOVE_DELAY_SECONDS)


async def handle_message(message, tools):
    text = tools.clean(message)
    if not text:
        return

    _parse_trigram_table_line(text, tools)

    match = DIVINATION_PATTERN.search(text)
    if match:
        _remember_gua(match.group(1), tools)
        return

    if '天色大变' in text and '卦' in text:
        # 天色大变，陆乘风给你算的卦也不那么准了：卦象失效，必须停止自动行走。
        # 只有脚本正在桃花阵里自动行走时才提示，避免走出阵后的重复通知。
        if state.get('in_maze') or state.get('waiting') or state.get('pending_task'):
            _stop_auto_walking(tools, '天色大变，卦象失效', '⚠ 桃花阵脚本已停止：天色大变，卦象失效了')
        else:
            state['stopped'] = True
            tools.log('天色大变，但当前不在桃花阵自动行走，跳过停止提示')
        return

    if '你莫名其妙地走出了桃花阵' in text:
        state['in_maze'] = False
        state['waiting'] = False
        state['last_command'] = ''
        state['stopped'] = False
        _cancel_pending_send()
        tools.log('已经离开桃花阵，停止自动行走')
        return

    if '你的动作还没有完成，不能移动' in text or '你上一个动作还没有完成' in text:
        if state.get('waiting') and state.get('in_maze'):
            state['waiting'] = False
            state['busy_retries'] = state.get('busy_retries', 0) + 1
            tools.log(f'上一条方向未发成，{RETRY_DELAY_SECONDS:g} 秒后重试第 {state.get("step", 0) + 1} 步')
            _schedule_send(tools, RETRY_DELAY_SECONDS)
        return

    if '你充满自信的向前走去' in text:
        _advance_after_success(tools)
        return

    if '你顺利地回到了起点' in text:
        _reset_round(tools)
        return

    if re.search(r'你获得了.+点经验', text) or re.search(r'你获得了.+点潜能', text):
        if state.get('in_maze'):
            _reset_round(tools)
        return

    if '你来到了一片桃花林里' in text or '桃花阵 -' in text:
        if not state.get('in_maze'):
            tools.log('进入桃花阵，准备自动行走')
        state['in_maze'] = True
        state['stopped'] = False
        if not state.get('waiting') and not state.get('pending_task'):
            _schedule_send(tools, MOVE_DELAY_SECONDS)
        return


def cleanup():
    _cancel_pending_send()
    state['in_maze'] = False
    state['waiting'] = False
    state['last_command'] = ''
    state['stopped'] = False
