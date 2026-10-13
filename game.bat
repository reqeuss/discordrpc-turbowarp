@echo off
setlocal EnableExtensions
title Launch game with Discord Rich Presence
cd /d "%~dp0"

set "GAME=%~dp0testdiscordrpc.exe"
set "RPC_DIR=%~dp0resources\rpc"
set "RPC_SCRIPT=%RPC_DIR%\rpc_bridge.py"
set "REQUIREMENTS=%RPC_DIR%\requirements.txt"
set "VENV_DIR=%~dp0.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

echo.
echo ==========================================
echo   Game + Discord Rich Presence launcher
echo ==========================================
echo.

if not exist "%GAME%" (
  echo ERROR: Game executable not found:
  echo "%GAME%"
  echo Put testdiscordrpc.exe beside game.bat or edit GAME_EXE in rpc_bridge.py.
  pause
  exit /b 1
)
if not exist "%RPC_SCRIPT%" (
  echo ERROR: Python bridge not found: "%RPC_SCRIPT%"
  pause
  exit /b 1
)
if not exist "%REQUIREMENTS%" (
  echo ERROR: Python requirements file not found: "%REQUIREMENTS%"
  pause
  exit /b 1
)

where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python 3 was not found.
  echo Install Python 3 from https://www.python.org/downloads/windows/
  echo Enable the Python launcher, then run game.bat again.
  pause
  exit /b 1
)

if not exist "%VENV_PY%" (
  echo [1/3] Creating a local Python environment...
  py -3 -m venv "%VENV_DIR%"
  if errorlevel 1 (
    echo ERROR: Could not create the Python environment.
    pause
    exit /b 1
  )
) else (
  echo [1/3] Local Python environment already exists.
)

echo [2/3] Installing or updating Python dependencies...
"%VENV_PY%" -m pip install --disable-pip-version-check -r "%REQUIREMENTS%"
if errorlevel 1 (
  echo ERROR: Dependency installation failed.
  echo Check your internet connection and Python installation.
  pause
  exit /b 1
)

echo [3/3] Starting Discord RPC bridge...
start "Discord RPC Bridge" /D "%RPC_DIR%" "%VENV_PY%" "%RPC_SCRIPT%"
timeout /t 2 /nobreak >nul

echo Starting game...
start "" "%GAME%"
echo.
echo Game launched. Keep the Discord RPC Bridge window open.
exit /b 0
