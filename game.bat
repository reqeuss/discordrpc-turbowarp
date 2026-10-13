
@echo off
setlocal
title Lancement du jeu

cd /d "%~dp0"

set "GAME=%~dp0testdiscordrpc.exe"
set "RPC_DIR=%~dp0resources\rpc"
set "RPC_SCRIPT=%RPC_DIR%\rpc_bridge.py"

if not exist "%GAME%" (
    echo ERREUR : jeu introuvable.
    pause
    exit /b 1
)

if not exist "%RPC_SCRIPT%" (
    echo ERREUR : rpc_bridge.py introuvable.
    pause
    exit /b 1
)

REM Find Python or install it if missing.
where py >nul 2>&1
if errorlevel 1 (
    echo Python est absent. Installe Python 3 depuis python.org,
    echo puis relance ce fichier.
    start "" "https://www.python.org/downloads/windows/"
    pause
    exit /b 1
)

REM Install dependencies before starting the game.
py -3 -m pip install -r "%RPC_DIR%\requirements.txt"
if errorlevel 1 (
    echo ERREUR : installation des dependances impossible.
    pause
    exit /b 1
)

REM Start RPC in background, without a console window.
start "" /B pyw -3 "%RPC_SCRIPT%"

REM Start the actual game.
start "" "%GAME%"

exit /b 0
