@echo off
REM Juiced Setup Script for Windows
REM This script creates a virtual environment and installs all dependencies

echo ========================================
echo Juiced Setup for Windows
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo.
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip
echo ✓ pip upgraded
echo.

echo Step 3: Installing dependencies...
venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Step 4: Setting up config file...
if not exist "configs\config.yaml" (
    if exist "configs\config.yaml.example" (
        copy "configs\config.yaml.example" "configs\config.yaml"
        echo ✓ Created configs\config.yaml from example
        echo.
        echo IMPORTANT: Edit configs\config.yaml with your CyTube credentials
    ) else (
        echo WARNING: configs\config.yaml.example not found
    )
) else (
    echo ✓ configs\config.yaml already exists
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit configs\config.yaml with your CyTube server and credentials
echo   2. Run juiced.bat to start the application
echo.
echo For help, see README.md or BETA_TESTING.md
echo.
pause
