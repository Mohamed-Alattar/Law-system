@echo off
title Law Office Management System - Setup and Run
echo.
echo =========================================================
echo  Law Office Management System
echo  نظام إدارة مكتب المحاماة
echo =========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

REM Check if this is first run
if not exist "data\" (
    echo 🔧 First time setup detected...
    echo Running setup script...
    echo.
    python setup.py
    if errorlevel 1 (
        echo.
        echo ❌ Setup failed. Please check the error messages above.
        pause
        exit /b 1
    )
    echo.
    echo ✅ Setup completed successfully!
    echo.
)

echo 🚀 Starting Law Office Management System...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo ❌ Application failed to start. Please check for error messages above.
    echo.
    echo Common solutions:
    echo - Run: python setup.py
    echo - Check Python version: python --version
    echo - Install dependencies: pip install -r requirements.txt
    echo.
)

pause