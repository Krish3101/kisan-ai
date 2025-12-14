@echo off
title KisanAI - Setup
color 0A

echo ========================================
echo        KisanAI Project Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo [1/5] Creating Python virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo [2/5] Installing Python dependencies...
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt

echo.
echo [3/5] Installing Node.js dependencies...
cd frontend
call npm install
cd ..

echo.
echo [4/5] Setting up database and demo user...
.venv\Scripts\python.exe backend\seed.py

echo.
echo [5/5] Setup complete!
echo.
echo ========================================
echo    Setup Completed Successfully!
echo ========================================
echo.
echo Demo User Credentials:
echo   Username: demo
echo   Password: demo123
echo.
echo Next Steps:
echo   1. Copy backend\.env.example to backend\.env
echo   2. Add your API keys to backend\.env
echo   3. Run scripts\start.bat to launch the application
echo.
echo ========================================
pause
