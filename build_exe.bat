@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
  echo Python 3 and the Python launcher are required to build these EXEs.
  pause
  exit /b 1
)

echo [1/3] Installing PyInstaller...
py -3 -m pip install --upgrade pyinstaller
if errorlevel 1 (
  echo Failed to install PyInstaller.
  pause
  exit /b 1
)

echo [2/3] Building Discord RPC bridge EXE...
py -3 -m PyInstaller --noconfirm --clean --onefile --console --name rpc_bridge resources\rpc\rpc_bridge.py
if errorlevel 1 (
  echo Bridge build failed.
  pause
  exit /b 1
)

echo [3/3] Building silent game launcher EXE...
py -3 -m PyInstaller --noconfirm --clean --onefile --noconsole --name GameLauncher launcher.py
if errorlevel 1 (
  echo Launcher build failed.
  pause
  exit /b 1
)

if not exist "dist\resources\rpc" mkdir "dist\resources\rpc"
copy /y "dist\rpc_bridge.exe" "dist\resources\rpc\rpc_bridge.exe" >nul
if errorlevel 1 (
  echo Failed to stage rpc_bridge.exe.
  pause
  exit /b 1
)

echo.
echo Build complete:
echo   dist\GameLauncher.exe
echo   dist\resources\rpc\rpc_bridge.exe
echo.
echo Copy GameLauncher.exe beside testdiscordrpc.exe in the game folder.
echo Copy the resources folder from dist into the game folder too.
pause
