"""验证码图片本地存档。

MUD 服务器（北大侠客行）在 fullme 验证码出现时，会下发一行：

    <img src="http://fullme.pkuxkx.net/zmud/<filename>.jpg">

本模块负责：
1. 从文本中检测这种验证码图片 URL；
2. 把图片字节保存到 captcha_images/ 目录；
3. 同一 filename 在一次进程内只保存一次，避免重复堆积。

被两处复用：
- mud_session.MudSession：收到 MUD 行时主动异步下载（主路径，可靠）；
- web_mud.fullme_proxy：代理图片时顺带保存（兜底，覆盖前端走 iframe 等情况）。
"""

import os
import re
import urllib.parse
import urllib.request
import http.cookiejar
from datetime import datetime

# 验证码图片本地存档目录（项目根下）。
CAPTCHA_DIR = os.path.join(os.path.dirname(__file__), 'captcha_images')

# fullme 站点共用一套 Cookie，保证下载验证码图片时能带上会话。
_cookie_jar = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cookie_jar))

# 进程级去重：同一 filename 只缓存一次。
_saved_filenames = set()

# 缓存最新一张验证码图片：(filename, bytes)；出现时缓存，提交验证码后才落盘。
_cached_image = None
_cached_ext = 'jpg'  # 缓存图片的扩展名

# data:image/jpeg;base64,xxxx 解析用
_DATAURL_RE = re.compile(r'data:([^;,]+)?(;base64)?,(.*)', re.I | re.S)
_MIME_TO_EXT = {'image/jpeg': 'jpg', 'image/jpg': 'jpg', 'image/png': 'png',
                'image/gif': 'gif', 'image/webp': 'webp'}

# 日志回调，默认丢弃；由调用方注入（例如 web_mud._rt_log）。
_log = lambda msg: None


def set_logger(fn):
    """注入日志回调，便于把保存情况写入运行时日志。"""
    global _log
    _log = fn or (lambda msg: None)


# 提取 fullme 验证码图片 URL：
#   形如 http://fullme.pkuxkx.net/zmud/<filename>.jpg
# 同时支持被 HTML/转义包裹的情况（src="..."、&amp;）。
_CAPTCHA_URL_RE = re.compile(
    r'https?://(?:fullme\.pkuxkx\.net|fullme\.pkuxkx\.com'
    r'|fullme\.[a-z0-9-]+\.pkuxkx\.com|[a-z0-9-]+\.fullme\.pkuxkx\.com)'
    r'/zmud/[A-Za-z0-9_\-]+\.jpg',
    re.IGNORECASE,
)


def find_captcha_urls(text):
    """从一段文本中找出全部验证码图片 URL，按出现顺序去重返回。"""
    if not text:
        return []
    cleaned = str(text).replace('&amp;', '&')
    seen = []
    for m in _CAPTCHA_URL_RE.finditer(cleaned):
        url = m.group(0)
        if url not in seen:
            seen.append(url)
    return seen


def filename_from_url(url):
    """从 fullme 验证码图片 URL 提取 filename（不含扩展名），失败返回 None。"""
    try:
        path = urllib.parse.urlparse(url).path
    except Exception:
        return None
    match = re.search(r'/zmud/([^/?#]+)\.jpg$', path, re.I)
    return match.group(1) if match else None


def save_bytes(url, body):
    """缓存最新一张验证码图片字节（不落盘）。

    验证码图片一出现就缓存，但只有用户真正提交 report/fullme 验证码时，
    才由 commit_cached(code) 用验证码内容命名落盘——这样图片与答案才能对上。
    同一张图（按 filename）重复缓存会被忽略。
    """
    filename = filename_from_url(url) or _tail_name_from_url(url)
    if not filename or not body:
        return False
    if filename in _saved_filenames:
        return False
    global _cached_image
    _cached_image = (filename, body)
    _saved_filenames.add(filename)
    _log(f'[CAPTCHA] 验证码图片已缓存（等待提交验证码后保存）: {filename}')
    return True


def save_base64(url, b64):
    """前端回传的小窗图片(base64)，同样只缓存不落盘。"""
    import base64
    filename = filename_from_url(url)
    if not filename:
        filename = datetime.now().strftime('%H%M%S%f')
    if filename in _saved_filenames:
        return False
    ext = 'jpg'
    raw = b64 or ''
    m = _DATAURL_RE.match(raw.strip())
    if m:
        mime = (m.group(1) or '').lower()
        ext = _MIME_TO_EXT.get(mime, 'jpg')
        raw = m.group(3) or ''
    try:
        body = base64.b64decode(raw)
    except Exception as e:
        _log(f'验证码图片(base64)解码失败: {e}')
        return False
    if not body:
        return False
    global _cached_image, _cached_ext
    _cached_image = (filename, body)
    _cached_ext = ext
    _saved_filenames.add(filename)
    _log(f'[CAPTCHA] 验证码图片已缓存(来自小窗，等待提交): {filename}')
    return True


# 文件名中非法字符（Windows/Linux 通用），保存时替换为下划线。
_BAD_FN_CHARS = re.compile(r'[\\/:*?"<>|\r\n\t]+')


def _safe_filename_component(code):
    """把用户输入的验证码转成安全的文件名片段。"""
    s = str(code or '').strip()
    if not s:
        return ''
    s = _BAD_FN_CHARS.sub('_', s)
    # 限制长度，避免过长文件名。
    return s[:40]


def commit_cached(code):
    """用用户提交的验证码内容作文件名，把缓存的图片落盘。

    只有真正输入 report/fullme 验证码时才调用本函数，保证文件名（验证码答案）
    与图片内容一一对应。无缓存图片或验证码为空时返回 False。
    返回实际写入的文件名（不含目录）。
    """
    global _cached_image
    safe = _safe_filename_component(code)
    if not safe:
        return None
    if not _cached_image:
        _log('[CAPTCHA] 提交了验证码但没有缓存的图片，跳过保存')
        return None
    filename, body = _cached_image
    ext = _cached_ext
    try:
        os.makedirs(CAPTCHA_DIR, exist_ok=True)
        dest = os.path.join(CAPTCHA_DIR, f'{safe}.{ext}')
        # 同名（验证码）已存在则加序号，避免覆盖。
        dest = _unique_path(dest)
        with open(dest, 'wb') as f:
            f.write(body)
        _log(f'验证码图片已保存: {dest}')
        # 提交后清空缓存，等待下一张。
        _cached_image = None
        return os.path.basename(dest)
    except Exception as e:
        _log(f'验证码图片保存失败: {e}')
        return None


def _unique_path(path):
    """若 path 已存在，则在文件名后加 _2、_3… 直到不冲突。"""
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 2
    while os.path.exists(f'{base}_{i}{ext}'):
        i += 1
    return f'{base}_{i}{ext}'


def _tail_name_from_url(url):
    """从任意 URL 取路径末段文件名（不含扩展名），失败返回 None。"""
    try:
        path = urllib.parse.urlparse(url).path
    except Exception:
        return None
    name = path.rstrip('/').split('/')[-1]
    if not name:
        return None
    return os.path.splitext(name)[0] or name


# 真实验证码图片：fullme 的 robot.php 页面里 <img src="./b2evo_captcha_tmp/xxx.jpg">
_CAPTCHA_PAGE_IMG_RE = re.compile(
    r'src=(["\'])([^"\']*b2evo_captcha_tmp/[^"\']+\.jpg)\1',
    re.IGNORECASE,
)


def find_captcha_image_in_html(html_text, page_url):
    """从 robot.php 页面 HTML 提取真实验证码图片的绝对 URL。

    页面里图片是相对路径 ./b2evo_captcha_tmp/b2evo_captcha_<hash>.jpg，
    这里转成绝对 URL 返回；找不到返回 None。
    """
    if not html_text:
        return None
    m = _CAPTCHA_PAGE_IMG_RE.search(html_text)
    if not m:
        return None
    rel = m.group(2)
    try:
        return urllib.parse.urljoin(page_url, rel)
    except Exception:
        return None


def download_and_save(url):
    """同步下载一张验证码图片并保存。供异步线程调用。

    带 fullme Referer，复用会话 Cookie。下载失败仅记日志，不抛异常。
    """
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 mud_assistant',
            'Referer': 'http://fullme.pkuxkx.net/',
        },
    )
    with _opener.open(req, timeout=10) as resp:
        body = resp.read()
    return save_bytes(url, body)


def handle_text(text):
    """检测一段文本中的验证码图片 URL 并逐张下载保存。

    同步阻塞函数（含网络下载），调用方应放进线程/任务里执行。
    返回实际保存的张数。
    """
    saved = 0
    for url in find_captcha_urls(text):
        try:
            if download_and_save(url):
                saved += 1
        except Exception as e:
            _log(f'验证码图片下载失败 {url}: {e}')
    return saved
