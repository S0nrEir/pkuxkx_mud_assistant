"""Example custom script.

Required interface:
    handle_message(message, tools)

The message argument is the current server message text. The tools argument
provides helpers such as clean(), contains(), regex(), send(), log(), and now().
"""


state = {
    'last_seen': '',
}


async def handle_message(message, tools):
    text = tools.clean(message)
    if not text:
        return

    if tools.contains(text, '桃花阵'):
        state['last_seen'] = text
        tools.log('检测到桃花阵相关消息')
        # await tools.send('look')
