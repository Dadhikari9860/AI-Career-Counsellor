@echo off
title AI Career Counsellor - Project Runner
color 0A

echo.
echo ========================================
echo    AI CAREER COUNSELLOR - LAUNCHER
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo [OK] Node.js found
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d %~dp0backend && .\venv\Scripts\activate.bat && python run.py"

:: Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo    SERVERS ARE STARTING...
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Two new terminal windows have opened.
echo Keep them running while using the app.
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

:: Open browser
start http://localhost:3000

echo.
echo Press any key to close this window...
pause >nul

