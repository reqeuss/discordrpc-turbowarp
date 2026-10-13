# Discord Rich Presence for TurboWarp

Add Discord Rich Presence to a TurboWarp game with a custom extension and a local bridge.

**Important:** the extension must be added to the TurboWarp project while the game is being developed, **before exporting or compiling the game**. This project does not inject RPC into an arbitrary game that was already exported without the extension.

🌍 **Languages:** [Français](readme/README.fr.md) · [English](readme/README.en.md) · [Español](readme/README.es.md)

## What it does

- Displays custom Discord activity details and state.
- Supports start/end timestamps, image assets, party information, Join/Spectate secrets, and instance status.
- Reconnects automatically when the local bridge is temporarily unavailable.
- Communicates with the bridge over WebSocket on `127.0.0.1:32123`.
- Uses `game.bat` to launch the bridge and game on Windows.
- Can use a compiled `rpc_bridge.exe` so players do not need to install Python.

## How it works

1. The developer adds `extension.js` to the TurboWarp project as an **unsandboxed custom extension**.
2. The developer uses the extension's blocks in the project and exports/compiles the game.
3. The developer configures the Discord Application ID in the bridge.
4. The developer copies the contents of `ingame/` next to the exported game's executable.
5. The player starts the game using `game.bat` (or a prepared compiled launcher).

If the game was exported without the extension integrated, adding the bridge files afterward is **not enough**.

## Quick start

### 1. Integrate the extension during development

Load `extension.js` into TurboWarp as a custom **unsandboxed** extension. Use its blocks to set activity fields and call **update presence**. Include this extension in the project before exporting or compiling.

### 2. Configure the Discord application

Create or select an application in the [Discord Developer Portal](https://discord.com/developers/applications). Copy its **Application ID** from General Information.

Edit `resources/rpc/rpc_bridge.py` and set:

```python
APP_ID = "YOUR_DISCORD_APPLICATION_ID"
```

Replace the placeholder with your numeric Application ID. Configure image asset keys in the application's Rich Presence Art Assets if you want to use images. **Do not add a bot token or client secret.**

If distributing a compiled `rpc_bridge.exe`, configure the ID before building that executable.

### 3. Prepare the exported game folder

Copy the **contents** of `ingame/` beside the game's executable. Example:

```text
MyGame/
├── MyGame.exe
├── game.bat
└── resources/
    └── rpc/
        ├── rpc_bridge.py
        └── requirements.txt
```

The bridge currently looks for `testdiscordrpc.exe` by default. If your game's executable has a different name, update `GAME_EXE` in `rpc_bridge.py` to match it.

### 4. Launch

Double-click `game.bat`. The script tries `resources/rpc/rpc_bridge.exe` first. If that file is absent, it looks for Python 3 and installs the bridge dependencies in a local `.venv` on first launch.

For distribution without requiring Python on the player's PC, place a correctly configured compiled bridge at `resources/rpc/rpc_bridge.exe`. The Discord **desktop app** must be running and signed in.

## Extension blocks

- **set [field] to [value]** — configure a presence field.
- **update presence** — send the configured fields to Discord.
- **clear presence** — clear the activity.
- **reconnect to bridge** — retry the local connection.
- **RPC connection status** — read the connection state and last error.
- **current value of [field]** — read a field's current value.

Timestamps use Unix seconds, not milliseconds. Image fields use asset keys from Discord Developer Portal, not image URLs.

## Troubleshooting

- **No connection:** confirm that the bridge is running and the extension was loaded unsandboxed.
- **No activity appears:** check that Discord Desktop is running and `APP_ID` is correct.
- **Images do not appear:** check the asset keys in the Discord application.
- **Python error:** install Python 3 or provide the compiled bridge executable.
- Opening `http://127.0.0.1:32123/` in a browser is not a valid test; the endpoint expects WebSocket connections.

## Attribution and usage

If you use, redistribute, or adapt this project in your game or another project, **please credit Reqeuss** and link back to this repository:

- Author: **Reqeuss**
- Repository: https://github.com/reqeuss/discordrpc-turbowarp

Suggested credit:

> Discord RPC integration powered by [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss.

Please keep the attribution when redistributing modified versions. This credit request does not replace any applicable third-party license terms.

## Development checks

Run from the repository root on a Windows/Python development machine:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r resources/rpc/requirements.txt
.venv\Scripts\python.exe -m py_compile resources/rpc/rpc_bridge.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check extension.js
```

CI checks syntax and unit tests, but a live test with the game and Discord Desktop is still recommended.

## Security

The bridge binds to `127.0.0.1` (local machine only). Keep it local unless you deliberately understand the risks of exposing it to other devices.

---

Full guides: [Français](readme/README.fr.md) · [English](readme/README.en.md) · [Español](readme/README.es.md)
