"""MUD Web client server entry."""

import os
import webbrowser
import threading
import asyncio
import http.cookiejar
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

import config
from mud_session import MudSession

HTML_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'web_mud.html')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')


def load_html_page():
    with open(HTML_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()


from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import HTMLResponse, PlainTextResponse, Response
from starlette.staticfiles import StaticFiles

_fullme_cookie_jar = http.cookiejar.CookieJar()
_fullme_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_fullme_cookie_jar))


async def index_page(request):
    return HTMLResponse(load_html_page())


def _is_allowed_fullme_url(url):
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in ('http', 'https'):
        return False
    host = (parsed.hostname or '').lower()
    return (
        host == 'fullme.pkuxkx.net'
        or host == 'fullme.pkuxkx.com'
        or (host.startswith('fullme.') and host.endswith('.pkuxkx.com'))
        or host.endswith('.fullme.pkuxkx.com')
    )


def _proxied_fullme_attr_url(attr_url, base_url):
    attr_url = (attr_url or '').strip()
    if (
        not attr_url
        or attr_url.startswith('#')
        or attr_url.lower().startswith(('data:', 'javascript:', 'mailto:'))
    ):
        return attr_url

    absolute_url = urllib.parse.urljoin(base_url, attr_url)
    if not _is_allowed_fullme_url(absolute_url):
        return attr_url
    return '/fullme-proxy?url=' + urllib.parse.quote(absolute_url, safe='')


def _rewrite_fullme_html(body, content_type, base_url):
    charset = 'utf-8'
    content_type_match = re.search(r'charset=([^;\s]+)', content_type or '', re.I)
    if content_type_match:
        charset = content_type_match.group(1).strip('"')

    try:
        text = body.decode(charset, errors='replace')
    except LookupError:
        charset = 'utf-8'
        text = body.decode(charset, errors='replace')

    def replace_quoted(match):
        attr, quote, value = match.groups()
        return f'{attr}={quote}{_proxied_fullme_attr_url(value, base_url)}{quote}'

    def replace_unquoted(match):
        attr, value = match.groups()
        return f'{attr}={_proxied_fullme_attr_url(value, base_url)}'

    text = re.sub(
        r'\b(src|href|action)\s*=\s*(["\'])(.*?)\2',
        replace_quoted,
        text,
        flags=re.I | re.S,
    )
    text = re.sub(
        r'\b(src|href|action)\s*=\s*([^\s>"\']+)',
        replace_unquoted,
        text,
        flags=re.I,
    )
    return text.encode(charset, errors='replace')


def _fetch_fullme_url(url):
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 mud_assistant',
            'Referer': 'http://fullme.pkuxkx.net/',
        },
    )
    with _fullme_opener.open(req, timeout=10) as resp:
        body = resp.read()
        content_type = resp.headers.get('Content-Type') or 'application/octet-stream'
        return resp.status, content_type, body, resp.geturl()


async def fullme_proxy(request):
    url = request.query_params.get('url', '')
    if not _is_allowed_fullme_url(url):
        return PlainTextResponse('invalid fullme url', status_code=400)

    try:
        status, content_type, body, final_url = await asyncio.to_thread(_fetch_fullme_url, url)
    except urllib.error.HTTPError as e:
        body = e.read() or str(e).encode('utf-8', errors='replace')
        content_type = e.headers.get('Content-Type') if e.headers else 'text/plain; charset=utf-8'
        return Response(
            body,
            status_code=e.code,
            headers={'Cache-Control': 'no-store', 'Content-Type': content_type},
        )
    except Exception as e:
        return PlainTextResponse(f'fullme proxy error: {e}', status_code=502)

    if 'text/html' in (content_type or '').lower():
        body = _rewrite_fullme_html(body, content_type, final_url or url)

    return Response(
        body,
        status_code=status,
        headers={'Cache-Control': 'no-store', 'Content-Type': content_type},
    )


async def websocket_handler(websocket):
    _rt_log('[WS] 新连接')
    await websocket.accept()
    session = MudSession(runtime_log=_rt_log)
    await session.run(websocket)
    _rt_log('[WS] 连接结束')


routes = [
    Route('/', endpoint=index_page),
    Route('/fullme-proxy', endpoint=fullme_proxy),
    WebSocketRoute('/ws', endpoint=websocket_handler),
]

app = Starlette(routes=routes)
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


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
