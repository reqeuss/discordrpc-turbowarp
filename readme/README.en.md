# Discord Rich Presence for TurboWarp

Add Discord Rich Presence to a TurboWarp game using a custom extension and a local bridge.

**Important:** the extension must be integrated into the TurboWarp project during development, **before the game is exported or compiled**. This project cannot inject RPC into an already-exported game that was built without the extension.

[🇫🇷 Français](README.fr.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md)

## Features

- Custom Discord activity details and state.
- Start/end timestamps.
- Discord image assets, party information, Join/Spectate secrets, and instance flag.
- Automatic reconnection to the bridge.
- Local WebSocket communication on `127.0.0.1:32123`.
- Windows launch through `game.bat`.
- Optional compiled bridge to avoid requiring Python on the player's PC.

## How it works

1. During development, load `extension.js` into TurboWarp as an **unsandboxed custom extension**.
2. Use the extension blocks in the project.
3. Export or compile the game with the extension included.
4. Configure the Discord Application ID in the bridge.
5. Copy the contents of `ingame/` beside the game's executable.
6. Launch the game with `game.bat`.

If the game was exported without the extension, adding the bridge files afterward is not enough.

## Setup

### 1. Integrate the extension before exporting

Add `extension.js` to TurboWarp as an **unsandboxed** custom extension. Use its blocks to set fields and call **update presence**. The extension must be included in the project before export or compilation.

### 2. Configure Discord

In the [Discord Developer Portal](https://discord.com/developers/applications), create or select an application and copy its **Application ID** from General Information.

In `resources/rpc/rpc_bridge.py`, replace:

```python
APP_ID = "YOUR_DISCORD_APPLICATION_ID"
```

Use your numeric Application ID. For images, configure Rich Presence assets in the Discord application and use their asset keys. **Never add a bot token or client secret.**

If distributing `rpc_bridge.exe`, configure the ID before building the executable.

### 3. Prepare the game folder

Copy the **contents** of `ingame/` beside the exported game executable:

```text
MyGame/
├── MyGame.exe
├── game.bat
└── resources/
    └── rpc/
        ├── rpc_bridge.py
        └── requirements.txt
```

The bridge looks for `testdiscordrpc.exe` by default. If your executable has a different name, update `GAME_EXE` in `rpc_bridge.py`.

### 4. Launch

Double-click `game.bat`. It checks for `resources/rpc/rpc_bridge.exe` first. If it is missing, the script looks for Python 3 and installs dependencies into a local `.venv` on first launch.

To avoid requiring Python on the player's PC, provide a correctly configured compiled bridge at `resources/rpc/rpc_bridge.exe`. The Discord **desktop app** must be running and signed in.

## Extension blocks

- **set [field] to [value]** — configure a field.
- **update presence** — send the fields to Discord.
- **clear presence** — clear the activity.
- **reconnect to bridge** — retry the connection.
- **RPC connection status** — read the connection state and last error.
- **current value of [field]** — read a field's current value.

Timestamps use Unix seconds, not milliseconds. Image fields use Discord asset keys, not image URLs.

## Troubleshooting

- **No connection:** ensure the bridge is running and the extension was loaded unsandboxed.
- **No activity:** check Discord Desktop and the Application ID.
- **Missing images:** verify the Rich Presence asset keys.
- **Python error:** install Python 3 or provide the compiled bridge.
- Opening `http://127.0.0.1:32123/` in a browser is not a valid test; the endpoint expects WebSocket connections.

## Credit and usage

If you use, redistribute, or adapt this project in your game or another project, **please credit Reqeuss** and link to this repository:

- Author: **Reqeuss**
- Repository: https://github.com/reqeuss/discordrpc-turbowarp

Suggested credit:

> Discord RPC integration powered by [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss.

Please retain this credit when redistributing modified versions. This credit request does not replace any applicable third-party license terms.

## Development checks

Run from the repository root:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r resources/rpc/requirements.txt
.venv\Scripts\python.exe -m py_compile resources/rpc/rpc_bridge.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check extension.js
```

CI checks syntax and unit tests, but a live test with the game and Discord Desktop is still recommended.

## Security

The bridge listens on `127.0.0.1` (local machine only). Do not expose it to other devices unless you understand the risks.
