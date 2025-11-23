@echo off
title KisanAI - Starting Application
color 0A

echo ========================================
echo        KisanAI Application Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first or create a virtual environment.
    pause
    exit /b 1
)

echo [1/3] Starting Backend Server...
echo.
start "KisanAI Backend" cmd /k "cd /d %~dp0backend && %~dp0.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend Development Server...
echo.
start "KisanAI Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 2 /nobreak >nul

echo [3/3] Opening Browser...
echo.
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo ========================================
echo    KisanAI is now running!
echo ========================================
echo.
echo Backend:  http://localhost:9000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:9000/api/docs
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /FI "WINDOWTITLE eq KisanAI Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq KisanAI Frontend*" /T /F >nul 2>&1

echo All servers stopped.
echo.
pause
