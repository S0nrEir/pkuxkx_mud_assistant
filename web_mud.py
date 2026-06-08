"""MUD Web client server entry."""

import os
import webbrowser
import threading
from datetime import datetime

import config
from mud_session import MudSession

HTML_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'web_mud.html')


def load_html_page():
    with open(HTML_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()


from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import HTMLResponse


async def index_page(request):
    return HTMLResponse(load_html_page())


async def websocket_handler(websocket):
    _rt_log('[WS] 新连接')
    await websocket.accept()
    session = MudSession(runtime_log=_rt_log)
    await session.run(websocket)
    _rt_log('[WS] 连接结束')


routes = [
    Route('/', endpoint=index_page),
    WebSocketRoute('/ws', endpoint=websocket_handler),
]

app = Starlette(routes=routes)


# ═══════════════════════════════════════════
#  运行时日志（每次启动覆盖）
# ═══════════════════════════════════════════

_runtime_log_path = os.path.join(os.path.dirname(__file__), config.LOG_DIR, 'runtime.log')
_runtime_log_file = None


def _rt_log(msg):
    """写入运行时日志"""
    global _runtime_log_file
    if _runtime_log_file is None:
        return
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    try:
        _runtime_log_file.write(f'[{timestamp}] {msg}\n')
        _runtime_log_file.flush()
    except Exception:
        pass


def _init_runtime_log():
    """初始化运行时日志文件（覆盖模式）"""
    global _runtime_log_file
    os.makedirs(os.path.dirname(_runtime_log_path), exist_ok=True)
    _runtime_log_file = open(_runtime_log_path, 'w', encoding='utf-8')
    _rt_log('=== 运行时日志启动 ===')


def _close_runtime_log():
    """关闭运行时日志文件"""
    global _runtime_log_file
    if _runtime_log_file:
        _rt_log('=== 运行时日志结束 ===')
        _runtime_log_file.close()
        _runtime_log_file = None

def run_server():
    import uvicorn

    host = '127.0.0.1'
    port = 58080

    _init_runtime_log()
    _rt_log(f'服务器启动 http://{host}:{port}')
    _rt_log(f'MUD 服务器: {config.MUD_HOST}:{config.MUD_PORT}')
    _rt_log(f'运行时日志: {_runtime_log_path}')

    print('=' * 50)
    print('  MUD Web 客户端')
    print('=' * 50)
    print()
    print(f'  浏览器访问: http://{host}:{port}')
    print(f'  MUD 服务器: {config.MUD_HOST}:{config.MUD_PORT}')
    print(f'  运行时日志: {_runtime_log_path}')
    print()
    print('  即将自动打开浏览器...')
    print()

    # 延迟打开浏览器（等服务器启动）
    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open(f'http://{host}:{port}')

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        uvicorn.run(app, host=host, port=port, log_level='warning')
    finally:
        _close_runtime_log()
