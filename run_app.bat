@echo off
echo ==========================================
echo      Starting KisanAI Smart Assistant
echo ==========================================

cd /d "%~dp0"

set PYTHON_CMD=python

REM Check if python is in PATH
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 'python' command not found in PATH.
    echo Checking known installation paths...
    
    if exist "C:\Users\krish\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\krish\AppData\Local\Programs\Python\Python311\python.exe"
        echo Found Python at C:\Users\krish\AppData\Local\Programs\Python\Python311\python.exe
    ) else (
        echo Python not found. Please install Python 3.10+ and add to PATH.
        pause
        exit /b
    )
)

REM Install dependencies if needed
if not exist "backend\venv" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv backend\venv
)

echo Activating virtual environment...
call backend\venv\Scripts\activate

echo Installing/Updating dependencies...
pip install -r backend\requirements.txt >nul 2>&1

echo.
echo Starting Backend Server...
echo The application will be available at http://127.0.0.1:9000/frontend/index.html
echo.

REM Start server in background and open browser
start "" "http://127.0.0.1:9000/frontend/index.html"
%PYTHON_CMD% backend\fastapi_server.py

pause
