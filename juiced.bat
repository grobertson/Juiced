@echo off
REM Juiced - CyTube TUI Chat Client Launcher for Windows

cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\python.exe" (
    echo Starting Juiced with virtual environment...
    venv\Scripts\python.exe -m juiced configs\config.yaml
) else (
    echo Starting Juiced with system Python...
    echo.
    echo WARNING: No virtual environment found.
    echo It's recommended to create one with:
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    echo.
    echo Attempting to run with system Python...
    python -m juiced configs\config.yaml
)

pause
