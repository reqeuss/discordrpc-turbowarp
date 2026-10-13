# Discord Rich Presence for TurboWarp

A TurboWarp custom extension connects to Discord Rich Presence through a local Python WebSocket bridge.

## Features

- Activity details and state.
- Start/end timestamps (Unix seconds).
- Large/small image asset keys and hover text.
- Party ID, size and maximum size.
- Join/Spectate secrets and instance flag.
- Automatic WebSocket reconnect and queued updates.
- Automatic Python virtual environment and dependency installation through `game.bat`.
- Local-only bridge bound to `127.0.0.1`.

## Project layout

```text
game-folder/
├── testdiscordrpc.exe
├── game.bat
├── extension.js
├── .venv/                         # created automatically; ignored by Git
└── resources/
    └── rpc/
        ├── rpc_bridge.py          # edit settings here
        └── requirements.txt
```

## One-time configuration

Open `resources/rpc/rpc_bridge.py` and edit the settings near the top:

- `APP_ID`: numeric Application ID from Discord Developer Portal > General Information.
- `GAME_EXE`: path to the game's executable. By default it points to `testdiscordrpc.exe` in the project root.
- `DEFAULT_DETAILS` and `DEFAULT_STATE`: default activity text.
- `DEFAULT_LARGE_IMAGE` and `DEFAULT_LARGE_TEXT`: optional large image asset key and hover text.

No separate setup script or config JSON is needed. Do not put a Discord bot token or client secret in this file or commit it.

## Launch on Windows

1. Install Python 3 for Windows and enable the Python launcher (`py`). This is the only manual software prerequisite.
2. Edit `APP_ID` in `resources/rpc/rpc_bridge.py`.
3. Ensure `testdiscordrpc.exe` is beside `game.bat` (or edit `GAME_EXE` in the Python file).
4. Add `extension.js` to TurboWarp as a custom **unsandboxed extension**.
5. Double-click `game.bat`.

The first launch creates a local `.venv` folder and installs everything listed in `resources/rpc/requirements.txt`. Later launches reuse that environment and check/install the dependencies again. No administrator rights should normally be needed.

## Extension blocks

- **set [field] to [value]** — configure a field.
- **update presence** — send the current field values to the bridge.
- **clear presence** — clear the current activity.
- **reconnect to bridge** — retry the local WebSocket connection.
- **RPC connection status** — show connection status and the last error.
- **current value of [field]** — read a configured field.

Set the fields, then call **update presence**. Timestamps are Unix timestamps in seconds, not milliseconds. Image fields must match asset keys configured in Discord Developer Portal > Rich Presence Art Assets; image keys are not image URLs.

## Requirements and troubleshooting

- The Discord **desktop app** must be running and signed in.
- The Application ID must be numeric and belong to the Discord application with the configured Rich Presence assets.
- If the extension stays disconnected, check that the bridge console is open and that the extension was loaded unsandboxed.
- If presence does not update, read the `[RPC]` messages in the bridge console.
- A browser visit to `http://127.0.0.1:32123/` is not a health check: the endpoint speaks WebSocket.
- If Python or dependency installation fails, install/reinstall Python 3, enable `py`, then launch `game.bat` again.

## Developer checks

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r resources/rpc/requirements.txt
.venv\Scripts\python.exe -m py_compile resources/rpc/rpc_bridge.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check extension.js
```

CI runs Python compilation, unit tests and JavaScript syntax checks. Those checks do not replace a live Windows test with the game and Discord desktop running.

## Security

The bridge listens only on loopback (`127.0.0.1`). Do not change the host to `0.0.0.0` unless you intentionally want other devices to reach the bridge.


## Optional silent EXE launcher (Windows)

You can keep using `game.bat`, or build a GUI-subsystem launcher that hides the bridge and install windows:

1. Install Python 3 on the computer used to build the launcher.
2. Run `build_exe.bat`.
3. Copy `dist\GameLauncher.exe` into the game folder, beside `testdiscordrpc.exe`.
4. Launch `GameLauncher.exe`.

The launcher creates `.venv`, installs the packages from `resources\rpc\requirements.txt`, starts the Python bridge without a console, then launches the game. Python 3 is still required on the target computer because the launcher uses the local Python runtime to create the environment. Errors are shown in a Windows message box and written to `discord-rpc-launcher.log`. The EXE is not included in GitHub; build it locally with `build_exe.bat`.
