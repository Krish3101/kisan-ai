@echo off
title KisanAI - Starting Services
color 0A

echo ========================================
echo      Starting KisanAI Services
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run scripts\setup.bat first.
    pause
    exit /b 1
)

REM Check if Node modules exist
if not exist "frontend\node_modules\" (
    echo ERROR: Node modules not found!
    echo Please run scripts\setup.bat first.
    pause
    exit /b 1
)

echo [1/2] Starting Backend Server (Port 8000)...
start "KisanAI Backend" cmd /k ".venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo.
echo [2/2] Starting Frontend Development Server (Port 3000)...
start "KisanAI Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo    Services Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to close this window...
pause >nul
