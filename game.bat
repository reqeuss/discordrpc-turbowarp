@echo off
setlocal EnableExtensions
title Launch game with Discord Rich Presence
cd /d "%~dp0"

set "GAME=%~dp0testdiscordrpc.exe"
set "RPC_DIR=%~dp0resources\rpc"
set "RPC_SCRIPT=%RPC_DIR%\rpc_bridge.py"
set "CONFIG=%RPC_DIR%\config.json"

if not exist "%GAME%" (
  echo ERROR: Game executable not found:
  echo "%GAME%"
  pause
  exit /b 1
)
if not exist "%RPC_SCRIPT%" (
  echo ERROR: Python bridge not found:
  echo "%RPC_SCRIPT%"
  pause
  exit /b 1
)
if not exist "%CONFIG%" (
  echo First-time setup has not been completed.
  echo Run setup.bat first.
  pause
  exit /b 1
)
where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python 3 was not found. Run setup.bat after installing Python.
  pause
  exit /b 1
)

echo Starting local Discord RPC bridge...
start "Discord RPC Bridge" /D "%RPC_DIR%" py -3 "%RPC_SCRIPT%"
timeout /t 1 /nobreak >nul

echo Starting game...
start "" "%GAME%"
exit /b 0
