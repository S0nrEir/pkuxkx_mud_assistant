"""
MUD 助手 - 主入口

用法:
  python start.py          # 启动代理（带聊天监听窗口）
  python start.py proxy    # 同上
  python start.py web      # 启动 Web 客户端（浏览器玩 MUD）
  python start.py cmdlog   # 生成命令分类日志
  python start.py cmdlog 2026-06-02  # 指定日期
"""

import sys
import os


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "proxy":
        print("=" * 50)
        print("  MUD 助手 - Telnet 代理模式")
        print("=" * 50)
        print()
        print("使用方法:")
        print("  1. 启动本代理（就是现在）")
        print("  2. 打开 zMUD，连接地址改为: 127.0.0.1 端口: 6666")
        print("  3. 正常游戏，所有日志会自动记录")
        print("  4. 会自动打开聊天监听窗口，显示聊天频道消息")
        print("  5. 运行 'python start.py cmdlog' 查看命令分类日志")
        print()
        from proxy import MudProxy
        proxy = MudProxy(chat_monitor=True)
        proxy.start()

    elif sys.argv[1] == "web":
        print("=" * 50)
        print("  MUD 助手 - Web 客户端模式")
        print("=" * 50)
        print()
        from web_mud import run_server
        run_server()

    elif sys.argv[1] == "cmdlog":
        from skill_cmdlog import build_cmdlog
        date = sys.argv[2] if len(sys.argv) > 2 else None
        result = build_cmdlog(date)
        if result:
            # 读取并打印结果
            with open(result, "r", encoding="utf-8") as f:
                print(f.read())

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
