@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
  echo Python 3 and the Python launcher are required to build this EXE.
  pause
  exit /b 1
)

py -3 -m pip install --upgrade pyinstaller
if errorlevel 1 (
  echo Failed to install PyInstaller.
  pause
  exit /b 1
)

py -3 -m PyInstaller --noconfirm --clean --onefile --noconsole --name GameLauncher launcher.py
if errorlevel 1 (
  echo Build failed. Check the error above.
  pause
  exit /b 1
)

echo.
echo Build complete: dist\GameLauncher.exe
echo Copy GameLauncher.exe into the game folder beside testdiscordrpc.exe.
pause
