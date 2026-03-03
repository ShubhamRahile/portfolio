@echo off
echo ================================================
echo   Flask Portfolio Server - Windows Launcher
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Python found!
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created!
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/Update dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
echo.

REM Start the Flask server
echo ================================================
echo   Starting Flask Server...
echo   Press Ctrl+C to stop the server
echo ================================================
echo.
python app.py

pause
