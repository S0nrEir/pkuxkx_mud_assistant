"""桃花阵自动行走脚本。

使用方式：
1. 启用机器人。
2. 找陆乘风接任务并让他算卦。
3. 如果脚本没有看到铁八卦表，会使用日志中稳定出现的默认八卦表。
4. 自己走进东面的桃花林后，脚本会按卦象方向循环行走。

天色大变处理：
- 迷宫中检测到「天色大变，陆乘风给你算的卦也不那么准了」时，卦象失效。
- 脚本会自动走出桃花阵，回到大厅陆乘风处 ask lu about job 重新接取任务，
  等到陆乘风重新给出新卦象后，再走回东面的桃花阵继续自动行走。
"""

import asyncio
import re


RETRY_DELAY_SECONDS = 3.0
MOVE_DELAY_SECONDS = 0.8
RECONNECT_MOVE_DELAY = 1.0      # 重连路径每一步之间的间隔
ASK_RETRY_DELAY = 5.0           # 任务冷却时重试 ask 的间隔
ASK_MAX_RETRIES = 12            # 最多重试 ask 的次数（约 1 分钟）

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

# 走出/走回桃花阵的固定路线（按房间顺序）。
# 出迷宫：leave 后到后花园，再一路向西到大厅（陆乘风）。
# 进迷宫：从大厅一路向东到后花园，再向东进入桃花阵。
EXIT_MAZE_PATH = ['w', 'w', 'w']           # 后花园 -> 归云馆 -> 走廊 -> 大厅
EXIT_MAZE_ROOMS = ['归云馆', '走廊', '大厅']
ENTER_MAZE_PATH = ['e', 'e', 'e', 'e']     # 大厅 -> 走廊 -> 归云馆 -> 后花园 -> 桃花阵
ENTER_MAZE_ROOMS = ['走廊', '归云馆', '后花园', '桃花阵']

# 陆乘风任务不可用的提示（冷却/忙碌）：等待后重试 ask。
JOB_UNAVAILABLE_HINTS = (
    '你刚做完鉴定任务',
    '你请稍等片刻再来吧',
    '没看我正忙着嘛',
)

# 房间标题（清理后）出现的特征文本。
ROOM_HOUGARDEN = '后花园 -'
ROOM_GUIYUNGUAN = '归云馆 -'
ROOM_ZOULANG = '走廊 -'
ROOM_DATING = '大厅 -'
ROOM_TAOHUA = '桃花阵 -'


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
    # ── 重连（天色大变后重新接取任务）状态 ──
    'reconnecting': False,        # 是否处于重连流程中
    'reconnect_phase': '',        # 'leave' / 'walk_out' / 'ask' / 'walk_in'
    'reconnect_step': 0,          # 当前路径走到了第几步
    'reconnect_token': 0,         # 重连流程的代际，用于作废旧延迟任务
    'ask_retries': 0,             # ask lu about job 重试次数
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


def _is_maze_walking():
    """是否正在桃花阵里自动行走（或正准备发下一步）。"""
    return state.get('in_maze') or state.get('waiting') or bool(state.get('pending_task'))


def _start_reconnect(tools, reason):
    """天色大变时启动重连：先停止迷宫自动行走，再 leave 走出桃花阵。"""
    _cancel_pending_send()
    state['in_maze'] = False
    state['waiting'] = False
    state['last_command'] = ''
    state['busy_retries'] = 0
    state['reconnecting'] = True
    state['reconnect_phase'] = 'leave'
    state['reconnect_step'] = 0
    state['ask_retries'] = 0
    tools.log(f'桃花阵启动重连流程：{reason}')
    tools.notify(f'⚠ 桃花阵：{reason}，自动返回陆乘风处重新接取任务')
    _schedule_reconnect(tools, 0)


def _abort_reconnect(tools, reason):
    """取消重连流程（例如手动走出迷宫、脚本停用）。"""
    state['reconnecting'] = False
    state['reconnect_phase'] = ''
    state['reconnect_step'] = 0
    state['ask_retries'] = 0
    _cancel_reconnect_task()
    if reason:
        tools.log(f'桃花阵取消重连流程：{reason}')


def _cancel_reconnect_task():
    task = state.get('reconnect_task')
    if task and not task.done():
        task.cancel()
    state['reconnect_task'] = None


async def _reconnect_send_step(tools, command, label):
    state['waiting'] = True
    state['last_command'] = command
    tools.log(f'重连-{label}：发送 {command}')
    await tools.send(command)


async def _delayed_reconnect(tools, delay, token):
    await tools.delay(delay)
    if token != state.get('reconnect_token') or not state.get('reconnecting'):
        return
    state['reconnect_task'] = None
    await _reconnect_advance(tools)


async def _reconnect_advance(tools):
    """根据当前重连阶段，发送下一条命令。"""
    phase = state.get('reconnect_phase')
    if phase == 'leave':
        # 发送 leave 离开桃花阵，等「你莫名其妙地走出了桃花阵」后由消息处理切到 walk_out。
        await _reconnect_send_step(tools, 'leave', '离开桃花阵')
        return
    if phase == 'ask':
        await _reconnect_send_step(tools, 'ask lu about job', '向陆乘风接取任务')
        return
    if phase == 'walk_in':
        step = state.get('reconnect_step', 0)
        path = ENTER_MAZE_PATH
        if step >= len(path):
            return
        await _reconnect_send_step(tools, path[step], f'走向桃花阵 {step + 1}/{len(path)}')
        return
    if phase == 'walk_out':
        step = state.get('reconnect_step', 0)
        path = EXIT_MAZE_PATH
        if step >= len(path):
            return
        await _reconnect_send_step(tools, path[step], f'返回大厅 {step + 1}/{len(path)}')
        return


def _schedule_reconnect(tools, delay=0):
    if not state.get('reconnecting'):
        return
    _cancel_reconnect_task()
    state['reconnect_token'] += 1
    token = state['reconnect_token']
    state['pending_task'] = None
    if delay <= 0:
        state['reconnect_task'] = asyncio.create_task(_delayed_reconnect(tools, 0, token))
    else:
        state['reconnect_task'] = asyncio.create_task(_delayed_reconnect(tools, delay, token))


def _reconnect_handle_room(tools, text):
    """重连流程中，根据看到的房间标题推进路径。"""
    phase = state.get('reconnect_phase')
    if phase == 'walk_out':
        step = state.get('reconnect_step', 0)
        rooms = EXIT_MAZE_ROOMS
        path = EXIT_MAZE_PATH
        if step < len(rooms) and rooms[step] + ' -' in text:
            tools.log(f'重连-返回大厅：到达 {rooms[step]}')
            state['reconnect_step'] = step + 1
            state['waiting'] = False
            if state['reconnect_step'] >= len(path):
                # 到达大厅，准备 ask lu about job
                state['reconnect_phase'] = 'ask'
                _schedule_reconnect(tools, RECONNECT_MOVE_DELAY)
                return True
            _schedule_reconnect(tools, RECONNECT_MOVE_DELAY)
            return True
    if phase == 'walk_in':
        step = state.get('reconnect_step', 0)
        rooms = ENTER_MAZE_ROOMS
        path = ENTER_MAZE_PATH
        if step < len(rooms) and rooms[step] + ' -' in text:
            tools.log(f'重连-走向桃花阵：到达 {rooms[step]}')
            state['reconnect_step'] = step + 1
            state['waiting'] = False
            if state['reconnect_step'] >= len(path):
                # 已经到达桃花阵，结束重连，恢复自动行走
                _finish_reconnect(tools)
                return True
            _schedule_reconnect(tools, RECONNECT_MOVE_DELAY)
            return True
    return False


def _finish_reconnect(tools):
    """重连成功：到达桃花阵，恢复迷宫自动行走。"""
    state['reconnecting'] = False
    state['reconnect_phase'] = ''
    state['reconnect_step'] = 0
    state['ask_retries'] = 0
    _cancel_reconnect_task()
    state['in_maze'] = True
    state['waiting'] = False
    state['last_command'] = ''
    state['busy_retries'] = 0
    state['round_completed'] = False
    tools.log('桃花阵重连完成，重新开始按新卦象自动行走')
    tools.notify('✓ 桃花阵：已重新接取任务，继续自动行走')


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

    # 新卦象：无论是首次算卦还是重连后的重新算卦，都重新记录方向。
    match = DIVINATION_PATTERN.search(text)
    if match:
        gua = match.group(1)
        was_reconnecting = state.get('reconnecting')
        _remember_gua(gua, tools)
        if was_reconnecting and state.get('reconnect_phase') == 'ask':
            # 重连期间拿到了新卦象：从大厅走回桃花阵。
            tools.log('重连期间获得新卦象，开始走回桃花阵')
            state['reconnect_phase'] = 'walk_in'
            state['reconnect_step'] = 0
            state['waiting'] = False
            _schedule_reconnect(tools, RECONNECT_MOVE_DELAY)
        return

    # 天色大变：卦象失效。如果正在迷宫自动行走，启动重连；否则只标记停止。
    if '天色大变' in text and '卦' in text:
        if state.get('reconnecting'):
            # 已经在重连流程里，忽略重复的天色大变提示，避免重置流程。
            tools.log('天色大变，但已在重连流程中，忽略')
        elif _is_maze_walking():
            # 正在桃花阵里自动行走，需要重新接取任务。
            _start_reconnect(tools, '天色大变，卦象失效')
        else:
            state['stopped'] = True
            tools.log('天色大变，但当前不在桃花阵自动行走，等待玩家进入')
        return

    # 离开桃花阵：结束迷宫状态。如果不在重连流程中，说明是手动离开。
    if '你莫名其妙地走出了桃花阵' in text:
        if state.get('reconnecting'):
            # 重连流程主动 leave 触发的离开：切到走回大厅阶段。
            if state.get('reconnect_phase') == 'leave':
                tools.log('重连-已离开桃花阵，开始返回大厅')
                state['reconnect_phase'] = 'walk_out'
                state['reconnect_step'] = 0
                state['waiting'] = False
                _schedule_reconnect(tools, RECONNECT_MOVE_DELAY)
            else:
                tools.log('重连流程中意外走出桃花阵')
        else:
            state['in_maze'] = False
            state['waiting'] = False
            state['last_command'] = ''
            state['stopped'] = False
            _cancel_pending_send()
            tools.log('已经离开桃花阵，停止自动行走')
        return

    # 动作未完成：迷宫行走和重连路径都会遇到，按当前阶段重试同一步。
    if '你的动作还没有完成，不能移动' in text or '你上一个动作还没有完成' in text:
        if state.get('reconnecting'):
            if state.get('waiting'):
                tools.log(f'重连路径上一动作未完成，{RETRY_DELAY_SECONDS:g} 秒后重试')
                _schedule_reconnect(tools, RETRY_DELAY_SECONDS)
            return
        if state.get('waiting') and state.get('in_maze'):
            state['waiting'] = False
            state['busy_retries'] = state.get('busy_retries', 0) + 1
            tools.log(f'上一条方向未发成，{RETRY_DELAY_SECONDS:g} 秒后重试第 {state.get("step", 0) + 1} 步')
            _schedule_send(tools, RETRY_DELAY_SECONDS)
        return

    # 重连流程优先处理房间推进和 ask 结果。
    if state.get('reconnecting'):
        # ask lu about job 的结果处理。
        if state.get('reconnect_phase') == 'ask' and state.get('waiting'):
            # 任务不可用（冷却/忙碌）：等待后重试 ask。
            if any(hint in text for hint in JOB_UNAVAILABLE_HINTS):
                retries = state.get('ask_retries', 0) + 1
                state['ask_retries'] = retries
                state['waiting'] = False
                if retries > ASK_MAX_RETRIES:
                    tools.log(f'ask lu about job 连续 {retries} 次仍不可用，停止重连')
                    tools.notify('⚠ 桃花阵：陆乘风一直没给新任务，已停止重连，请人工处理')
                    _abort_reconnect(tools, 'ask 重试超限')
                    state['stopped'] = True
                    return
                tools.log(f'陆乘风任务暂时不可用，{ASK_RETRY_DELAY:g} 秒后重试 ask（第 {retries} 次）')
                _schedule_reconnect(tools, ASK_RETRY_DELAY)
                return
            # 占得一卦的情况已在上面统一处理；这里不再阻塞。
        # 走回/走出路径：根据房间标题推进。
        if _reconnect_handle_room(tools, text):
            return

    # 以下为正常迷宫自动行走逻辑。
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

    if '你来到了一片桃花林里' in text or ROOM_TAOHUA in text:
        if state.get('reconnecting'):
            # 重连期间走到桃花阵：结束重连。
            if state.get('reconnect_phase') == 'walk_in':
                _finish_reconnect(tools)
                return
        if not state.get('in_maze'):
            tools.log('进入桃花阵，准备自动行走')
        state['in_maze'] = True
        state['stopped'] = False
        if not state.get('waiting') and not state.get('pending_task'):
            _schedule_send(tools, MOVE_DELAY_SECONDS)
        return


def cleanup():
    _cancel_pending_send()
    _cancel_reconnect_task()
    state['in_maze'] = False
    state['waiting'] = False
    state['last_command'] = ''
    state['stopped'] = False
    state['reconnecting'] = False
    state['reconnect_phase'] = ''
    state['reconnect_step'] = 0
    state['ask_retries'] = 0
