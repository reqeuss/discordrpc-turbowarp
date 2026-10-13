@echo off
setlocal EnableExtensions
title Discord Rich Presence - Setup
cd /d "%~dp0"
set "RPC_DIR=%~dp0resources\rpc"
set "CONFIG=%RPC_DIR%\config.json"

echo.
echo ==========================================
echo   Discord Rich Presence - First-time setup
echo ==========================================
echo.

where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python 3 was not found.
  echo Install Python 3 from https://www.python.org/downloads/windows/
  echo Make sure the Python launcher is enabled during installation.
  pause
  exit /b 1
)

if not exist "%RPC_DIR%\requirements.txt" (
  echo ERROR: resources\rpc\requirements.txt was not found.
  pause
  exit /b 1
)

if not exist "%CONFIG%" (
  echo Enter your Discord Application ID.
  echo You can find it in the Discord Developer Portal under General Information.
  set "APP_ID="
  set /p "APP_ID=Application ID: "
  if not defined APP_ID (
    echo ERROR: Application ID cannot be empty.
    pause
    exit /b 1
  )
  >"%CONFIG%" echo {
  >>"%CONFIG%" echo   "app_id": "%APP_ID%",
  >>"%CONFIG%" echo   "game_exe": "testdiscordrpc.exe",
  >>"%CONFIG%" echo   "defaults": {
  >>"%CONFIG%" echo     "details": "Playing a game",
  >>"%CONFIG%" echo     "state": "In the game",
  >>"%CONFIG%" echo     "large_image": "",
  >>"%CONFIG%" echo     "large_text": ""
  >>"%CONFIG%" echo   }
  >>"%CONFIG%" echo }
  echo Created resources\rpc\config.json
) else (
  echo Local config already exists; keeping it.
)

echo.
echo Installing Python dependencies...
py -3 -m pip install --upgrade pip
if errorlevel 1 goto :failed
py -3 -m pip install -r "%RPC_DIR%\requirements.txt"
if errorlevel 1 goto :failed

echo.
echo Setup complete.
echo Start the game using game.bat.
pause
exit /b 0

:failed
echo.
echo ERROR: Dependency installation failed.
echo Check your internet connection and Python installation.
pause
exit /b 1
