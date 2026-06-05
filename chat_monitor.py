"""
MUD 聊天消息监听器
在独立命令行窗口中实时显示聊天频道消息

用法:
  由 proxy.py 自动调用，不需要手动运行
"""

import sys
import re
import time

# 聊天频道匹配正则
# 北大侠客行的频道消息格式：
#   【闲聊】某人(chat): 消息
#   【谣言】某人: 消息
#   【北大QQ群转发】某人(qq): 消息
#   【交易】某人(jy): 消息
CHAT_PATTERN = re.compile(
    r"[\【\[]"
    r"[^\】\]]*"
    r"(?:闲聊|谣言|交易|QQ群|帮派|组队|大喊|回答)"
    r"[^\】\]]*"
    r"[\】\]]"
)


def is_chat_message(text):
    """判断一条文本是否为聊天频道消息"""
    text = text.strip()
    if not text:
        return False
    if CHAT_PATTERN.search(text):
        return True
    # 备用：带频道标记且有说话内容的行
    for marker in ("(chat)", "(rumor)", "(jy)", "(qq)", "(group)"):
        if marker in text and (":" in text or "：" in text):
            return True
    return False


def main():
    """从 stdin 逐行读取，过滤并显示聊天消息"""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    print("=" * 60)
    print("  MUD 聊天消息监听器")
    print("  实时显示所有聊天频道消息")
    print("  关闭此窗口不影响游戏")
    print("=" * 60)
    print()

    count = 0
    while True:
        try:
            line = sys.stdin.readline()
        except (KeyboardInterrupt, EOFError):
            break
        if not line:
            break

        text = line.rstrip("\n").strip()
        if not text:
            continue

        if is_chat_message(text):
            count += 1
            timestamp = time.strftime("%H:%M:%S")
            print(f"  [{timestamp}] {text}")
            print()
            sys.stdout.flush()

    print(f"\n[聊天监听器已退出，共显示 {count} 条消息]")


if __name__ == "__main__":
    main()
