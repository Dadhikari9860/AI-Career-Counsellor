@echo off
title AI Career Counsellor - Frontend Server
color 0D

echo.
echo ========================================
echo      FRONTEND SERVER (React + Vite)
echo ========================================
echo.

cd /d %~dp0frontend

echo Starting Vite dev server on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm run dev

