@echo off
setlocal
cd /d "%~dp0"
title Arafat Assistant - Setup
echo Arafat Assistant - Windows starter setup
echo This installs Python packages and Chromium into your user environment.
echo No API key is needed until you open the app. No API request is made here.
echo.
if exist ".venv\Scripts\python.exe" goto install
py -3.12 -c "import sys" >nul 2>&1
if not errorlevel 1 (
    py -3.12 -m venv .venv
    goto install
)
py -3.11 -c "import sys" >nul 2>&1
if not errorlevel 1 (
    py -3.11 -m venv .venv
    goto install
)
python -c "import sys; assert sys.version_info[:2] in [(3,11),(3,12)]" >nul 2>&1
if not errorlevel 1 (
    python -m venv .venv
    goto install
)
echo Install Python 3.12, 64-bit, from https://www.python.org/downloads/windows/
echo Include Tcl/Tk and the Python launcher, then run setup.cmd again.
pause
exit /b 1

:install
if not exist ".venv\Scripts\python.exe" goto failed
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m playwright install chromium
if errorlevel 1 goto failed
".venv\Scripts\python.exe" selftest.py
if errorlevel 1 goto failed
echo.
echo Setup completed. Double-click start.cmd to open the assistant.
pause
exit /b 0

:failed
echo.
echo Setup did not finish. Review the error above and run setup.cmd again.
echo If this folder is protected or read-only, extract the ZIP into your user folder.
pause
exit /b 1
