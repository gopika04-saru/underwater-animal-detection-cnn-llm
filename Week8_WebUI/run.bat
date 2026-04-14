@echo off
REM Underwater Animal Detection Web UI - Quick Start Script for Windows

echo ========================================
echo 🐠 Underwater Animal Detection Web UI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Check if model exists
set MODEL_PATH=..\week6_ModelTraining\outputs\mobilenet_model.h5
if not exist "%MODEL_PATH%" (
    echo ⚠️  Warning: Trained model not found at %MODEL_PATH%
    echo Please train the model first:
    echo   cd ..\week6_ModelTraining
    echo   python train_mobilenet.py
    echo.
    set /p CONTINUE="Do you want to continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
) else (
    echo ✅ Model found: %MODEL_PATH%
)

echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask not found. Installing dependencies...
    pip install flask werkzeug
    echo.
)

REM Check for OpenAI (optional)
python -c "import openai" >nul 2>&1
if errorlevel 1 (
    echo ℹ️  OpenAI package not found (optional - will use fallback descriptions)
) else (
    echo ✅ OpenAI package found (optional)
)

echo.
echo 🚀 Starting web server...
echo 📍 Access the app at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Run the Flask app
python app.py

pause

@REM Made with Bob
