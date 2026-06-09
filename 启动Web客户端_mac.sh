#!/bin/bash
cd "$(dirname "$0")"

# 杀掉占用 58080 端口的旧进程
PID=$(lsof -ti :58080 2>/dev/null)
if [ -n "$PID" ]; then
    kill -9 $PID 2>/dev/null
    echo "已关闭旧进程 (PID: $PID)"
fi

# 自动检测 python3 还是 python
if command -v python3 &>/dev/null; then
    PY=python3
else
    PY=python
fi

exec $PY start.py web
