@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%tools\sync_skills_to_codex.ps1" %*

if errorlevel 1 (
    echo.
    echo Failed to sync Codex skills.
    exit /b 1
)

echo.
echo Codex skills synced. Restart Codex or start a new session to load updated skills.
