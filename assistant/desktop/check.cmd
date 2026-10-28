@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Run setup.cmd first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" selftest.py
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto failed
echo Local checks passed. These checks do not call OpenAI.
pause
exit /b 0
:failed
echo A check failed. Review the error above.
pause
exit /b 1
