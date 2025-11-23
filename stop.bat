@echo off
title KisanAI - Stop Servers
color 0C

echo ========================================
echo     Stopping KisanAI Servers
echo ========================================
echo.

echo Stopping Backend Server...
taskkill /FI "WINDOWTITLE eq KisanAI Backend*" /T /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

echo Stopping Frontend Server...
taskkill /FI "WINDOWTITLE eq KisanAI Frontend*" /T /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

echo.
echo All servers stopped.
echo.
pause
