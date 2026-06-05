"""
MUD Telnet 代理
zMUD -> 本代理(localhost:6666) -> mud.pkuxkx.net:5555
双向转发数据，同时记录日志
"""

import socket
import threading
import time
import os
import re
import subprocess
import sys
from datetime import datetime

import config

# ANSI 转义序列正则（颜色、光标控制等）
ANSI_RE = re.compile(rb"\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07|\x1b\[.*?[a-zA-Z]")


def strip_telnet_and_ansi(data):
    """移除 Telnet 协议控制字节和 ANSI 转义序列，返回干净的文本"""
    buf = bytearray(data)
    out = bytearray()
    i = 0
    while i < len(buf):
        # Telnet IAC (0xFF) 序列: FF [命令 [选项]]
        if buf[i] == 0xFF and i + 1 < len(buf):
            cmd = buf[i + 1]
            if cmd == 0xFF:  # 转义的 0xFF
                out.append(0xFF)
                i += 2
            elif cmd in (0xF0, 0xF1, 0xF2, 0xF3, 0xF4):  # SE/NOP/DM/BK/GA — 2字节
                i += 2
            elif cmd == 0xFB and i + 2 < len(buf):  # WILL — 3字节
                i += 3
            elif cmd == 0xFC and i + 2 < len(buf):  # WONT
                i += 3
            elif cmd == 0xFD and i + 2 < len(buf):  # DO
                i += 3
            elif cmd == 0xFE and i + 2 < len(buf):  # DONT
                i += 3
            elif cmd == 0xFA:  # SB...SE 子协商，找到 SE (0xF0)
                i += 2
                while i < len(buf):
                    if buf[i] == 0xFF and i + 1 < len(buf) and buf[i + 1] == 0xF0:
                        i += 2
                        break
                    i += 1
            else:
                i += 2
            continue
        # NULL 字节
        if buf[i] == 0x00:
            i += 1
            continue
        out.append(buf[i])
        i += 1

    # 移除 ANSI 转义序列
    out = ANSI_RE.sub(b"", out)
    return bytes(out)


class MudProxy:
    def __init__(self, chat_monitor=False):
        self.running = False
        self.log_dir = os.path.join(os.path.dirname(__file__), config.LOG_DIR)
        os.makedirs(self.log_dir, exist_ok=True)
        self.chat_monitor = chat_monitor
        self._chat_pipe = None
        self._chat_proc = None

    def _log_path(self, suffix):
        date_str = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"{date_str}_{suffix}.log")

    def _start_chat_monitor(self):
        """在新命令行窗口中启动聊天监听器，通过 stdin 管道接收消息"""
        monitor_script = os.path.join(os.path.dirname(__file__), "chat_monitor.py")
        python_exe = sys.executable

        # CREATE_NEW_CONSOLE 让子进程拥有独立的控制台窗口
        proc = subprocess.Popen(
            [python_exe, monitor_script],
            stdin=subprocess.PIPE,
            encoding="utf-8",
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        self._chat_proc = proc
        self._chat_pipe = proc.stdin
        print("[聊天监听窗口已启动]")

    def _send_to_chat_monitor(self, text):
        """将解码后的文本发送到聊天监听器"""
        if not self._chat_pipe:
            return
        try:
            for line in text.split("\n"):
                line = line.strip()
                if line:
                    self._chat_pipe.write(line + "\n")
            self._chat_pipe.flush()
        except (BrokenPipeError, OSError):
            self._chat_pipe = None

    def _append_log(self, filepath, data, direction):
        timestamp = datetime.now().strftime("%H:%M:%S")
        marker = ">>>" if direction == "send" else "<<<"
        # 清理 Telnet 控制字节和 ANSI 转义序列
        clean = strip_telnet_and_ansi(data)
        # 优先用 gbk 解码（MUD 服务器通常用 GBK），回退到 utf-8
        try:
            text = clean.decode("gbk", errors="replace")
        except Exception:
            text = clean.decode("utf-8", errors="replace")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        with open(filepath, "a", encoding=config.LOG_ENCODING) as f:
            for line in text.split("\n"):
                if line.strip():
                    f.write(f"[{timestamp}] {marker} {line}\n")
        # 只把服务器发来的消息转发到聊天监听器
        if direction == "recv":
            self._send_to_chat_monitor(text)

    def _forward(self, src, dst, direction, log_file):
        try:
            while self.running:
                try:
                    data = src.recv(4096)
                    if not data:
                        break
                    dst.sendall(data)
                    self._append_log(log_file, data, direction)
                except (ConnectionResetError, ConnectionAbortedError, OSError):
                    break
        except Exception as e:
            print(f"[转发错误] {e}")
        finally:
            self.running = False
            print("[连接断开]")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((config.PROXY_HOST, config.PROXY_PORT))
        server.listen(1)

        print(f"[代理已启动] zMUD 请连接 {config.PROXY_HOST}:{config.PROXY_PORT}")
        print(f"[将转发到] {config.MUD_HOST}:{config.MUD_PORT}")

        # 启动聊天监听窗口
        if self.chat_monitor:
            self._start_chat_monitor()

        print("[等待 zMUD 连接...]")

        while True:
            try:
                client_sock, addr = server.accept()
                print(f"[zMUD 已连接] {addr}")

                mud_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mud_sock.connect((config.MUD_HOST, config.MUD_PORT))
                print(f"[已连接 MUD 服务器] {config.MUD_HOST}:{config.MUD_PORT}")

                self.running = True
                raw_log = self._log_path("raw")

                t1 = threading.Thread(
                    target=self._forward,
                    args=(client_sock, mud_sock, "send", raw_log),
                    daemon=True,
                )
                t2 = threading.Thread(
                    target=self._forward,
                    args=(mud_sock, client_sock, "recv", raw_log),
                    daemon=True,
                )
                t1.start()
                t2.start()
                t1.join()
                t2.join()

                client_sock.close()
                mud_sock.close()
                print("[连接已关闭，等待重新连接...]")

            except KeyboardInterrupt:
                print("\n[代理已停止]")
                break
            except Exception as e:
                print(f"[错误] {e}")
                time.sleep(1)

        server.close()


if __name__ == "__main__":
    proxy = MudProxy()
    proxy.start()
