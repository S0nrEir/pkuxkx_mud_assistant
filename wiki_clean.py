"""
清理 Wiki 抓取文档中的网页垃圾内容（二次清理）
"""

import re
import os
import glob

WIKI_DIR = os.path.join(os.path.dirname(__file__), "wiki_db")

# 整行匹配即删除的模式
LINE_JUNK = [
    re.compile(r"\[图片[:\]]"),
    re.compile(r"跳至内容"),
    re.compile(r"^北大侠客行MUD百科$"),
    re.compile(r"^用户工具$"),
    re.compile(r"^站点工具$"),
    re.compile(r"^搜索$"),
    re.compile(r"^工具$"),
    re.compile(r"^登录>?$"),
    re.compile(r"^您的足迹"),
    re.compile(r"^目录$"),
    re.compile(r"^最近更改$"),
    re.compile(r"^媒体管理器$"),
    re.compile(r"^网站地图$"),
    re.compile(r"^页面工具$"),
    re.compile(r"^修订记录$"),
    re.compile(r"^反向链接$"),
    re.compile(r"^回到顶部$"),
    re.compile(r"\.txt\s*·\s*最后更改"),
    re.compile(r"taskrunner"),
    re.compile(r"北大侠客行Wiki基于"),
    re.compile(r"北大侠客行Wiki中有关"),
    re.compile(r"转载自北大侠客行百科"),
    re.compile(r"北大侠客行自1996年开放以来"),
    re.compile(r"捐款全部用于托管"),
    re.compile(r"^捐助入口$"),
    re.compile(r"除了捐助之外"),
    re.compile(r"我可以为北侠做些什么"),
    re.compile(r"^更多$"),
    # DokuWiki 命名空间行
    re.compile(r"^[a-z_]+:[a-z_]+$"),
]

# 行内删除（替换为空）
INLINE_REMOVE = [
    re.compile(r"\[图片:[^\]]*\]"),
    re.compile(r"\[图片\]"),
]


def clean_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    result = []
    in_tail = False

    for line in lines:
        stripped = line.strip()

        # 已经进入尾部垃圾区，只保留来源行
        if in_tail:
            if stripped.startswith("> 来源:"):
                result.append(stripped + "\n")
            continue

        # 检测尾部垃圾区的开始
        if any(p.search(stripped) for p in [
            re.compile(r"^页面工具$"),
            re.compile(r"\.txt\s*·\s*最后更改"),
        ]):
            in_tail = True
            continue

        # 空行保留
        if not stripped:
            result.append("\n")
            continue

        # 行级垃圾
        if any(p.search(stripped) for p in LINE_JUNK):
            continue

        # 行内替换
        cleaned = stripped
        for pat in INLINE_REMOVE:
            cleaned = pat.sub("", cleaned)
        cleaned = cleaned.strip()

        if cleaned:
            result.append(cleaned + "\n")

    # 合并连续空行
    final = []
    prev_empty = False
    for line in result:
        if line.strip() == "":
            if not prev_empty:
                final.append("\n")
            prev_empty = True
        else:
            prev_empty = False
            final.append(line)

    # 确保来源行前有空行
    text = "".join(final).strip() + "\n"
    if not text.endswith("\n"):
        text += "\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    files = glob.glob(os.path.join(WIKI_DIR, "**", "*.md"), recursive=True)
    print(f"找到 {len(files)} 个文件，开始清理...")
    for f in files:
        try:
            clean_file(f)
        except Exception as e:
            print(f"  [错误] {f}: {e}")
    print(f"[完成] 已清理 {len(files)} 个文件")


if __name__ == "__main__":
    main()
