@echo off
title AI Career Counsellor - Stop Servers
color 0C

echo.
echo ========================================
echo    STOPPING ALL SERVERS
echo ========================================
echo.

echo Stopping Python/Flask processes on port 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo Stopping Node.js processes on port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo [OK] All servers stopped!
echo.
pause

