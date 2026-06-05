"""
北大侠客行 Wiki 爬虫
抓取 https://www.pkuxkx.net/wiki/ 所有页面，转为 markdown 保存到本地
按 Wiki 自身的命名空间（分类）组织文件
"""

import os
import re
import time
import json
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
from collections import defaultdict

WIKI_BASE = "https://www.pkuxkx.net/wiki/"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "wiki_db")
STATE_FILE = os.path.join(OUTPUT_DIR, "_state.json")
DELAY = 0.5  # 每次请求间隔秒数，避免给服务器造成压力


class DokuWikiTextExtractor(HTMLParser):
    """从 DokuWiki HTML 中提取纯文本/简易 markdown"""

    def __init__(self):
        super().__init__()
        self.output = []
        self.skip_tags = {"script", "style", "head"}
        self.skip_depth = 0
        self.list_stack = []  # 追踪嵌套列表
        self.in_td = False
        self.td_cells = []
        self.in_tr = False
        self.tr_rows = []
        self.in_table = False
        self.table_rows = []
        self.in_h = 0  # h1=1, h2=2 ...
        self.in_pre = False
        self.in_code = False
        self.in_a = False
        self.a_href = ""

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if tag in self.skip_tags:
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.in_h = int(tag[1])
            self.output.append("\n")
        elif tag == "p":
            self.output.append("\n")
        elif tag == "br":
            self.output.append("\n")
        elif tag == "hr":
            self.output.append("\n---\n")
        elif tag == "li":
            depth = len(self.list_stack)
            indent = "  " * depth
            if self.list_stack and self.list_stack[-1] == "ol":
                self.output.append(f"{indent}- ")
            else:
                self.output.append(f"{indent}- ")
        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
        elif tag == "table":
            self.in_table = True
            self.table_rows = []
        elif tag == "tr":
            self.in_tr = True
            self.tr_rows = []
        elif tag == "td":
            self.in_td = True
            self.td_cells = []
        elif tag == "th":
            self.in_td = True
            self.td_cells = []
        elif tag == "pre":
            self.in_pre = True
            self.output.append("\n```\n")
        elif tag == "code":
            if not self.in_pre:
                self.in_code = True
                self.output.append("`")
        elif tag == "a":
            self.in_a = True
            self.a_href = attrs_dict.get("href", "")
        elif tag == "strong" or tag == "b":
            self.output.append("**")
        elif tag == "em" or tag == "i":
            self.output.append("*")
        elif tag == "img":
            alt = attrs_dict.get("alt", "")
            src = attrs_dict.get("src", "")
            if alt or src:
                self.output.append(f"[图片:{alt}]")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.skip_tags:
            self.skip_depth -= 1
            return
        if self.skip_depth > 0:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.output.append("\n")
            self.in_h = 0
        elif tag == "p":
            self.output.append("\n")
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "li":
            self.output.append("\n")
        elif tag == "td" or tag == "th":
            cell_text = "".join(self.td_cells).strip()
            self.tr_rows.append(cell_text)
            self.in_td = False
        elif tag == "tr":
            self.table_rows.append(list(self.tr_rows))
            self.in_tr = False
        elif tag == "table":
            self.in_table = False
            # 渲染表格为 markdown
            if self.table_rows:
                self.output.append("\n")
                for i, row in enumerate(self.table_rows):
                    line = "| " + " | ".join(cell.replace("\n", " ") for cell in row) + " |"
                    self.output.append(line + "\n")
                    if i == 0:
                        sep = "|" + "|".join("---" for _ in row) + "|"
                        self.output.append(sep + "\n")
                self.output.append("\n")
        elif tag == "pre":
            self.in_pre = False
            self.output.append("\n```\n")
        elif tag == "code":
            if self.in_code:
                self.in_code = False
                self.output.append("`")
        elif tag == "a":
            self.in_a = False
        elif tag == "strong" or tag == "b":
            self.output.append("**")
        elif tag == "em" or tag == "i":
            self.output.append("*")

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        if self.in_td:
            self.td_cells.append(data)
            return
        self.output.append(data)

    def get_text(self):
        text = "".join(self.output)
        # 清理多余空行
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def fetch_url(url):
    """获取 URL 内容"""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def get_all_pages():
    """通过 DokuWiki 索引页获取所有页面链接"""
    print("[1/3] 获取页面索引...")
    url = WIKI_BASE + "start?do=index"
    html = fetch_url(url)

    # 从索引页提取所有 wiki 链接
    pages = set()
    for match in re.finditer(r'href="(/wiki/([^"?]+))"', html):
        path = match.group(2)
        # 过滤掉媒体文件和特殊页面
        if any(x in path for x in ["_media", "_detail", "_export", "lib/exe", "feed.php"]):
            continue
        if path in ("", "start"):
            pages.add("start")
        else:
            pages.add(urllib.parse.unquote(path))

    # 也从首页内容中提取链接（首页有很多重要链接索引页不一定覆盖）
    start_html = fetch_url(WIKI_BASE + "start")
    for match in re.finditer(r'href="(/wiki/([^"?]+))"', start_html):
        path = match.group(2)
        if any(x in path for x in ["_media", "_detail", "_export", "lib/exe", "feed.php"]):
            continue
        pages.add(urllib.parse.unquote(path) if path != "start" else "start")

    print(f"  找到 {len(pages)} 个页面链接")
    return sorted(pages)


def fetch_page_content(page_id):
    """抓取单个 wiki 页面并转为 markdown"""
    url = WIKI_BASE + urllib.parse.quote(page_id, safe="/:")
    try:
        html = fetch_url(url)
    except urllib.error.HTTPError as e:
        return f"# {page_id}\n\n（页面获取失败: {e.code}）"
    except Exception as e:
        return f"# {page_id}\n\n（页面获取失败: {e}）"

    # 提取主内容区域
    # DokuWiki 的主内容在 <div class="dw-content"> 或 <div id="dokuwiki__content">
    content_match = re.search(
        r'<div[^>]*(?:class="[^"]*dw-content|id="dokuwiki__content")[^>]*>(.*)</div>\s*<!--',
        html, re.DOTALL
    )
    if not content_match:
        # 回退: 取 <h1> 到页面工具之间
        content_match = re.search(
            r'<h[12][^>]*>.*?</h[12]>(.*?)<div[^>]*class="[^"]*pageinfo',
            html, re.DOTALL
        )
    if not content_match:
        content_match = re.search(
            r'<div[^>]*class="[^"]*page[^"]*"[^>]*>(.*?)</div>\s*<div',
            html, re.DOTALL
        )

    content_html = content_match.group(1) if content_match else html

    parser = DokuWikiTextExtractor()
    parser.feed(content_html)
    text = parser.get_text()

    # 获取标题
    title_match = re.search(r'<h[12][^>]*>(.*?)</h[12]>', html, re.DOTALL)
    title = ""
    if title_match:
        title_parser = DokuWikiTextExtractor()
        title_parser.feed(title_match.group(1))
        title = title_parser.get_text()

    result = ""
    if title:
        result = f"# {title}\n\n"
    result += text

    # 在尾部添加源链接
    result += f"\n\n---\n> 来源: {url}\n"

    return result


def page_id_to_filepath(page_id):
    """将 wiki 页面 ID 映射为本地文件路径"""
    # DokuWiki 用 : 作为命名空间分隔符
    parts = page_id.split(":")
    if len(parts) == 1:
        filename = parts[0] + ".md"
        return os.path.join(OUTPUT_DIR, filename)
    else:
        namespace = os.path.join(*parts[:-1])
        filename = parts[-1] + ".md"
        return os.path.join(OUTPUT_DIR, namespace, filename)


def load_state():
    """加载已完成的爬取状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"done": [], "failed": []}


def save_state(state):
    """保存爬取状态"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def crawl_all():
    """爬取所有页面"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    state = load_state()
    done_set = set(state["done"])

    pages = get_all_pages()
    total = len(pages)
    new_pages = [p for p in pages if p not in done_set]

    print(f"[2/3] 开始抓取: 共 {total} 页，已完成 {len(done_set)} 页，待抓取 {len(new_pages)} 页")

    for i, page_id in enumerate(new_pages, 1):
        filepath = page_id_to_filepath(page_id)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        print(f"  [{i}/{len(new_pages)}] {page_id} ...", end=" ", flush=True)

        try:
            content = fetch_page_content(page_id)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            state["done"].append(page_id)
            print("OK")
        except Exception as e:
            state["failed"].append({"page": page_id, "error": str(e)})
            print(f"FAIL: {e}")

        # 每 20 页保存一次状态
        if i % 20 == 0:
            save_state(state)

        time.sleep(DELAY)

    # 重试失败的页面
    if state["failed"]:
        print(f"\n[3/3] 重试 {len(state['failed'])} 个失败页面...")
        retry_list = list(state["failed"])
        state["failed"] = []
        for item in retry_list:
            page_id = item["page"]
            filepath = page_id_to_filepath(page_id)
            print(f"  重试 {page_id} ...", end=" ", flush=True)
            try:
                content = fetch_page_content(page_id)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                state["done"].append(page_id)
                print("OK")
            except Exception as e:
                state["failed"].append({"page": page_id, "error": str(e)})
                print(f"FAIL: {e}")
            time.sleep(DELAY)

    save_state(state)
    print(f"\n[完成] 共 {len(state['done'])} 页，失败 {len(state['failed'])} 页")
    print(f"[输出目录] {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    crawl_all()
