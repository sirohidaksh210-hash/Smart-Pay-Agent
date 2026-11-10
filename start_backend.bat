@echo off
title SmartPay Backend Server
cd /d "C:\Users\Daksh\OneDrive\Desktop\paypal\backend"

echo =====================================
echo   SmartPay Agent - Backend Server
echo =====================================
echo.

call venv\Scripts\activate.bat

echo [1] Checking Python version...
python --version

echo [2] Checking if uvicorn is installed...
uvicorn --version

echo [3] Starting backend server on port 8000...
echo.

uvicorn main:app --reload --port 8000

echo.
echo =====================================
echo  SERVER STOPPED! See error above.
echo =====================================
pause
