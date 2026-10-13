@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "GAME=%~dp0testdiscordrpc.exe"
set "RPC_DIR=%~dp0resources\rpc"
set "RPC_EXE=%RPC_DIR%\rpc_bridge.exe"
set "RPC_SCRIPT=%RPC_DIR%\rpc_bridge.py"
set "REQUIREMENTS=%RPC_DIR%\requirements.txt"
set "VENV_DIR=%~dp0.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "DEPS_MARKER=%VENV_DIR%\.rpc-deps-installed"

if not exist "%GAME%" (
  echo ERROR: Game executable not found: "%GAME%"
  pause
  exit /b 1
)
if not exist "%REQUIREMENTS%" (
  echo ERROR: Missing requirements file: "%REQUIREMENTS%"
  pause
  exit /b 1
)

rem Fast path: use the compiled bridge immediately, without checking Python.
if exist "%RPC_EXE%" goto launch_compiled

rem Fallback path: use Python only when the compiled bridge is absent.
if not exist "%RPC_SCRIPT%" (
  echo ERROR: Neither rpc_bridge.exe nor rpc_bridge.py was found in "%RPC_DIR%".
  pause
  exit /b 1
)

if exist "%VENV_PY%" goto python_ready

where py >nul 2>&1
if not errorlevel 1 (
  py -3 -m venv "%VENV_DIR%"
  if errorlevel 1 goto python_error
  goto python_ready
)

where python >nul 2>&1
if not errorlevel 1 (
  python -c "import sys; raise SystemExit(0 if sys.version_info.major == 3 else 1)" >nul 2>&1
  if not errorlevel 1 (
    python -m venv "%VENV_DIR%"
    if not errorlevel 1 goto python_ready
  )
)

echo ERROR: No Python 3 installation was detected, and rpc_bridge.exe is missing.
echo Install Python 3 or place the compiled bridge at resources\rpc\rpc_bridge.exe.
pause
exit /b 1

:python_ready
if not exist "%VENV_PY%" goto python_error
if exist "%DEPS_MARKER%" goto launch_python

echo Installing bridge dependencies for the first time...
"%VENV_PY%" -m pip install --disable-pip-version-check -r "%REQUIREMENTS%"
if errorlevel 1 (
  echo ERROR: Dependency installation failed.
  pause
  exit /b 1
)
type nul > "%DEPS_MARKER%"

:launch_python
echo Starting Python RPC bridge...
start "Discord RPC Bridge" /D "%RPC_DIR%" "%VENV_PY%" "%RPC_SCRIPT%"
goto launch_game

:launch_compiled
echo Starting compiled RPC bridge...
start "" /D "%RPC_DIR%" "%RPC_EXE%"
goto launch_game

:launch_game
rem No fixed 2-second wait: the extension retries the WebSocket connection itself.
start "" "%GAME%"
exit /b 0

:python_error
echo ERROR: Could not create or find the local Python environment.
pause
exit /b 1
