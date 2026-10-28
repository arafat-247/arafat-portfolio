@echo off
setlocal
cd /d "%~dp0"
title Arafat Assistant
if not exist ".venv\Scripts\python.exe" (
    echo Run setup.cmd first, then open start.cmd again.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" app.py
if errorlevel 1 (
    echo The assistant closed with an error. Review the message above.
    pause
    exit /b 1
)
