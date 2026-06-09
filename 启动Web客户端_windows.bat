@echo off
cd /d "%~dp0"
:: 杀掉占用端口的旧进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":58080 "') do (
    taskkill /F /PID %%a >nul 2>&1
)
python start.py web
pause
