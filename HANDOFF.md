# Project handoff — Discord RPC for TurboWarp

Read this file first when continuing work in another chat.

## Goal

Connect a TurboWarp game to Discord Rich Presence through a local Python WebSocket bridge at `127.0.0.1:32123`.

## Current files

- `extension.js`: TurboWarp custom extension; must be loaded **unsandboxed**.
- `resources/rpc/rpc_bridge.py`: bridge and all editable settings, including Application ID and executable path.
- `resources/rpc/requirements.txt`: Python dependencies.
- `game.bat`: creates `.venv`, installs/updates dependencies, starts bridge, and launches the game.
- `tests/test_rpc_bridge.py`: payload validation tests.
- `.github/workflows/ci.yml`: Python compilation/tests and JavaScript syntax check.
- `README.md`: setup and troubleshooting.

There is intentionally no `setup.bat` and no generated `config.json`.

## Settings

Edit the constants near the top of `resources/rpc/rpc_bridge.py`:

- `APP_ID = "YOUR_DISCORD_APPLICATION_ID"`
- `GAME_EXE = GAME_DIR / "testdiscordrpc.exe"`
- `DEFAULT_DETAILS`
- `DEFAULT_STATE`
- `DEFAULT_LARGE_IMAGE`
- `DEFAULT_LARGE_TEXT`

Do not commit Discord bot tokens or client secrets. The Application ID is not a bot token.

## Launch

1. Install Python 3 on Windows and enable the `py` launcher.
2. Put `testdiscordrpc.exe` beside `game.bat`.
3. Set `APP_ID` in `resources/rpc/rpc_bridge.py`.
4. Load `extension.js` as an unsandboxed TurboWarp extension.
5. Run `game.bat`. It creates the local `.venv` and installs dependencies automatically.

## Protocol

Extension → bridge JSON over WebSocket:
- `{"action":"update", ...}`: full presence snapshot.
- `{"action":"clear"}`: clear presence.

Fields: `details`, `state`, `start`, `end`, `largeImage`, `largeText`, `smallImage`, `smallText`, `partyId`, `partySize`, `partyMax`, `joinSecret`, `spectateSecret`, `instance`.

The bridge maps these camelCase fields to pypresence keyword names. Change both sides together if modifying the protocol.

## Verification

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r resources/rpc/requirements.txt
.venv\Scripts\python.exe -m py_compile resources/rpc/rpc_bridge.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check extension.js
```

CI does not prove that a live Discord IPC session works. Test with the actual Windows game and Discord desktop app.

## Known checks

- Confirm CI passes after latest changes.
- Test first launch and a second launch of `game.bat`.
- Test update, changing fields and updating again, clear, closing/reopening the game, and closing/reopening Discord.
- Discord image keys must exist in the application's Rich Presence Art Assets.
- Visiting `http://127.0.0.1:32123/` in a browser is not a valid test because the endpoint is WebSocket.
- Keep the bridge bound to `127.0.0.1`.


## Silent EXE launcher
- Optional source: `launcher.py`; build script: `build_exe.bat`.
- Build with Python 3 installed by running `build_exe.bat`; output is `dist\GameLauncher.exe`.
- Copy the built EXE beside `testdiscordrpc.exe` in the game folder.
- It silently creates `.venv`, installs `resources\rpc\requirements.txt`, starts `resources\rpc\rpc_bridge.py` without a console, then starts the game.
- Python 3 is still required on the target PC. Failures are shown with a Windows message box and logged to `discord-rpc-launcher.log`.
- Keep `game.bat` as a visible/debug fallback. The compiled EXE is a local build artifact and is not committed.
