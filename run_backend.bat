@echo off
title AI Career Counsellor - Backend Server
color 0B

echo.
echo ========================================
echo       BACKEND SERVER (Flask)
echo ========================================
echo.

cd /d %~dp0backend

echo Activating virtual environment...
call .\venv\Scripts\activate.bat

echo.
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python run.py

