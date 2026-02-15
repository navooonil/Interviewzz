@echo off
setlocal EnableDelayedExpansion

echo ==========================================
echo   Interview Analyzer - Setup ^& Run
echo ==========================================

:: 1. Check Python
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org
    pause
    exit /b
)

:: 2. Upgrade pip
echo.
echo [1/4] Upgrading pip...
python -m pip install --upgrade pip

:: 3. Install Dependencies
echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

:: 4. Check FFmpeg (Simple Check first)
echo.
echo [3/4] Checking FFmpeg...

:: Try adding the exact known location to PATH
set "FFMPEG_DIR=%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
if exist "!FFMPEG_DIR!" (
    set "PATH=!PATH!;!FFMPEG_DIR!"
)

ffmpeg -version >nul 2>&1
if !errorlevel! equ 0 (
    echo FFmpeg is ready!
    goto :START_SERVER
)

:: If we are here, FFmpeg is missing. Try to install.
echo FFmpeg not found in PATH. Attempting automatic install...
winget install Gyan.FFmpeg --accept-source-agreements --accept-package-agreements

:: Check again after install
ffmpeg -version >nul 2>&1
if !errorlevel! equ 0 (
    echo FFmpeg installed successfully!
    echo NOTE: You might need to restart your terminal if it fails later.
    goto :START_SERVER
)

:: If still failing, check the hardcoded path again (maybe it just installed there)
if exist "!FFMPEG_DIR!" (
    set "PATH=!PATH!;!FFMPEG_DIR!"
    echo FFmpeg found at explicit path.
)

:: Final check
ffmpeg -version >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARNING] Automatic FFmpeg installation failed or not found in PATH.
    echo Please install FFmpeg manually or restart the script as Administrator.
    echo.
    echo Press any key to try running the server anyway ^(transcription might fail^)...
    pause
)

:START_SERVER
echo.
echo [4/4] Starting Server...
echo Open your browser to: http://127.0.0.1:8000/docs
uvicorn app.main:app --reload

pause
