@echo off
title AI Career Counsellor - First Time Setup
color 0E

echo.
echo ========================================
echo    AI CAREER COUNSELLOR - SETUP
echo ========================================
echo    Run this ONLY for first time setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo [OK] Node.js found
echo.

:: Backend Setup
echo ========================================
echo Step 1: Setting up Backend...
echo ========================================
cd /d %~dp0backend

:: Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call .\venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Step 2: Training ML Models...
echo ========================================
echo This may take 5-10 minutes...
echo.

python scripts/create_and_train_datasets.py

echo.
echo ========================================
echo Step 3: Setting up Frontend...
echo ========================================
cd /d %~dp0frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo ========================================
echo    SETUP COMPLETE!
echo ========================================
echo.
echo You can now run the project using:
echo   - Double-click "run_project.bat"
echo.
echo Or run servers separately:
echo   - Double-click "run_backend.bat"
echo   - Double-click "run_frontend.bat"
echo.
pause

