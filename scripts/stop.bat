@echo off
title KisanAI - Stopping Services
color 0C

echo ========================================
echo      Stopping KisanAI Services
echo ========================================
echo.

echo Stopping Backend Server (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Stopping Frontend Server (Port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ========================================
echo    Services Stopped Successfully!
echo ========================================
pause
