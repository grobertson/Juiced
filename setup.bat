@echo off
REM Juiced Setup Script for Windows
REM This script creates a virtual environment and installs all dependencies

echo ====================================================
echo Juiced Setup for Windows
echo ====================================================
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
echo  Virtual environment created
echo.

echo Step 2: Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip
echo  pip upgraded
echo.

echo Step 3: Installing dependencies...
venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    pause
    exit /b 1
)
echo  Dependencies installed
echo.

echo Step 4: Setting up config file...
if not exist "configs\config.yaml" (
    if exist "configs\config.yaml.example" (
        copy "configs\config.yaml.example" "configs\config.yaml"
        echo  Created configs\config.yaml from example
        echo.
        echo ====================================================
        echo Configuration Setup
        echo ====================================================
        echo.
        echo Please enter your CyTube connection details:
        echo.

        set /p "CYTUBE_CHANNEL=Channel name: "
        set /p "CYTUBE_USERNAME=Username (or press Enter for guest): "

        if not "%CYTUBE_USERNAME%"=="" (
            set /p "CYTUBE_PASSWORD=Password: "
        ) else (
            set "CYTUBE_USERNAME=null"
            set "CYTUBE_PASSWORD=null"
        )

        echo.
        echo Updating config file...

        REM Use PowerShell to update the YAML file
        REM Note: We replace the quoted values to preserve quotes
        powershell -Command "(Get-Content configs\config.yaml) -replace '\"your-channel-name\"', '\"%CYTUBE_CHANNEL%\"' | Set-Content configs\config.yaml"

        if not "%CYTUBE_USERNAME%"=="null" (
            powershell -Command "(Get-Content configs\config.yaml) -replace '\"your-username\"', '\"%CYTUBE_USERNAME%\"' | Set-Content configs\config.yaml"
            powershell -Command "(Get-Content configs\config.yaml) -replace '\"your-password\"', '\"%CYTUBE_PASSWORD%\"' | Set-Content configs\config.yaml"
        ) else (
            powershell -Command "(Get-Content configs\config.yaml) -replace 'user:\r?\n  - \"your-username\"\r?\n  - \"your-password\"', 'user: null' | Set-Content configs\config.yaml"
        )

        echo  Config file updated with your credentials
        echo.
    ) else (
        echo WARNING: configs\config.yaml.example not found
    )
) else (
    echo  configs\config.yaml already exists (keeping existing config)
)
echo.

echo ====================================================
echo Setup Complete!
echo ====================================================
echo.
echo Next steps:
echo   1. Edit configs\config.yaml with your CyTube server and credentials
echo   2. Run juiced.bat to start the application
echo.
echo For help, see README.md or BETA_TESTING.md
echo.
pause
