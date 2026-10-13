"""Discord Rich Presence bridge for the TurboWarp extension.

The bridge is deliberately local-only: it listens on 127.0.0.1 and accepts
JSON messages from the extension over WebSocket.
"""
from __future__ import annotations

import json
import os
import threading
import time
from contextlib import suppress
from pathlib import Path
from typing import Any

import psutil
from pypresence import Presence
from websockets.exceptions import ConnectionClosed
from websockets.sync.server import Server, serve

RPC_DIR = Path(__file__).resolve().parent
GAME_DIR = RPC_DIR.parent.parent

HOST = os.getenv("DISCORD_RPC_HOST", "127.0.0.1")
PORT = int(os.getenv("DISCORD_RPC_PORT", "32123"))
POLL_INTERVAL = 1.0
CONNECT_RETRY_SECONDS = 5.0
SESSION_START = int(time.time())

# EDIT THESE VALUES DIRECTLY IN THIS FILE.
# Find the Application ID in Discord Developer Portal > General Information.
APP_ID = "YOUR_DISCORD_APPLICATION_ID"
GAME_EXE = GAME_DIR / "testdiscordrpc.exe"
DEFAULT_DETAILS = "Playing a game"
DEFAULT_STATE = "In the game"
DEFAULT_LARGE_IMAGE = ""
DEFAULT_LARGE_TEXT = ""
MAX_MESSAGE_BYTES = 64 * 1024

rpc: Presence | None = None
rpc_connected = False
rpc_lock = threading.RLock()
server_instance: Server | None = None
server_ready = threading.Event()
server_error: str | None = None
pending_update: dict[str, Any] | None = None
shutdown_event = threading.Event()


def clean_text(value: Any, limit: int = 128) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text[:limit] if text else None


def optional_int(data: dict[str, Any], key: str) -> int | None:
    value = data.get(key)
    if value in (None, "") or isinstance(value, bool):
        return None
    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number


def parse_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off", ""}


def build_party_size(data: dict[str, Any]) -> list[int] | None:
    current = optional_int(data, "partySize")
    maximum = optional_int(data, "partyMax")
    if current is None or maximum is None:
        return None
    if maximum <= 0 or current < 0 or current > maximum:
        return None
    return [current, maximum]


def game_is_running(game_exe: Path) -> bool:
    target = game_exe.name.casefold()
    for process in psutil.process_iter(["name"]):
        try:
            name = process.info.get("name")
            if name and name.casefold() == target:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False


def make_presence_kwargs(data: dict[str, Any]) -> dict[str, Any]:
    """Convert the extension's camelCase JSON fields to pypresence kwargs."""
    return {
        "details": clean_text(data.get("details")),
        "state": clean_text(data.get("state")),
        # Keep one stable session timer when the extension leaves this field blank.
        # Passing None here would remove/reset the timestamp on every presence update.
        "start": optional_int(data, "start") or SESSION_START,
        "end": optional_int(data, "end"),
        "large_image": clean_text(data.get("largeImage"), 256),
        "large_text": clean_text(data.get("largeText")),
        "small_image": clean_text(data.get("smallImage"), 256),
        "small_text": clean_text(data.get("smallText")),
        "party_id": clean_text(data.get("partyId")),
        "party_size": build_party_size(data),
        "join": clean_text(data.get("joinSecret")),
        "spectate": clean_text(data.get("spectateSecret")),
        "instance": parse_bool(data.get("instance"), True),
    }


def apply_presence(data: dict[str, Any]) -> bool:
    """Apply an update. Caller must hold rpc_lock."""
    global rpc, rpc_connected
    if not rpc_connected or rpc is None:
        print("[RPC] Discord is not connected; update will be queued.")
        return False
    try:
        rpc.update(**make_presence_kwargs(data))
        print(
            "[RPC] Presence updated | "
            f"details={clean_text(data.get('details'))!r} | "
            f"state={clean_text(data.get('state'))!r}"
        )
        return True
    except Exception as exc:
        # A failed RPC write often means Discord closed or reset the IPC pipe.
        # Drop the broken client so the main loop can reconnect and replay the
        # most recent queued update instead of getting stuck in a false-connected state.
        failed_rpc = rpc
        rpc = None
        rpc_connected = False
        if failed_rpc is not None:
            with suppress(Exception):
                failed_rpc.close()
        print(f"[RPC] Update failed; will reconnect: {type(exc).__name__}: {exc}")
        return False


def handle_message(websocket: Any) -> None:
    global pending_update
    print("[RPC] TurboWarp extension connected.")
    try:
        for raw_message in websocket:
            try:
                data = json.loads(raw_message)
            except (json.JSONDecodeError, TypeError):
                print("[RPC] Ignored invalid JSON.")
                continue

            if not isinstance(data, dict):
                print("[RPC] Ignored message: expected a JSON object.")
                continue

            action = data.get("action")
            with rpc_lock:
                if action == "update":
                    pending_update = data
                    if rpc_connected and rpc is not None:
                        if apply_presence(data):
                            pending_update = None
                elif action == "clear":
                    pending_update = None
                    if rpc_connected and rpc is not None:
                        try:
                            rpc.clear()
                            print("[RPC] Presence cleared.")
                        except Exception as exc:
                            print(f"[RPC] Clear failed: {type(exc).__name__}: {exc}")
                elif action == "ping":
                    # The socket itself is the liveness signal; no response required.
                    continue
                else:
                    print(f"[RPC] Ignored unknown action: {action!r}")
    except ConnectionClosed:
        pass
    except Exception as exc:
        print(f"[RPC] WebSocket client error: {type(exc).__name__}: {exc}")
    finally:
        print("[RPC] TurboWarp extension disconnected.")


def websocket_server() -> None:
    global server_instance, server_error
    try:
        with serve(
            handle_message,
            HOST,
            PORT,
            max_size=MAX_MESSAGE_BYTES,
            ping_interval=20,
            ping_timeout=20,
        ) as server:
            server_instance = server
            server_ready.set()
            print(f"[RPC] WebSocket ready at ws://{HOST}:{PORT}")
            server.serve_forever()
    except Exception as exc:
        server_error = f"{type(exc).__name__}: {exc}"
        print(f"[RPC] WebSocket server failed: {server_error}")
        server_ready.set()


def connect_discord(app_id: str) -> bool:
    global rpc, rpc_connected
    candidate = Presence(app_id)
    try:
        candidate.connect()
    except Exception as exc:
        with suppress(Exception):
            candidate.close()
        print(f"[RPC] Discord connection failed: {type(exc).__name__}: {exc}")
        return False
    rpc = candidate
    rpc_connected = True
    return True


def run_bridge() -> int:
    global rpc, rpc_connected, pending_update
    game_exe = GAME_EXE.resolve()
    app_id = APP_ID.strip()

    print("[RPC] Discord Rich Presence bridge starting.")
    print(f"[RPC] Game executable: {game_exe}")
    print("[RPC] Settings are configured at the top of rpc_bridge.py.")

    if not app_id.isdigit():
        print("[RPC] ERROR: Edit APP_ID near the top of resources/rpc/rpc_bridge.py.")
        return 2
    if not game_exe.is_file():
        print("[RPC] ERROR: Game executable not found.")
        print(f"[RPC] Expected: {game_exe}")
        print("[RPC] Edit GAME_EXE near the top of resources/rpc/rpc_bridge.py.")
        return 2

    thread = threading.Thread(target=websocket_server, name="rpc-websocket", daemon=True)
    thread.start()
    if not server_ready.wait(timeout=5):
        print("[RPC] ERROR: WebSocket server did not start within 5 seconds.")
        return 3
    if server_error:
        print("[RPC] ERROR: Another process may already be using this port.")
        return 3

    print(f"[RPC] Waiting for {game_exe.name} to start...")
    try:
        while not shutdown_event.is_set() and not game_is_running(game_exe):
            time.sleep(POLL_INTERVAL)
        if shutdown_event.is_set():
            return 0

        print("[RPC] Game detected.")
        while not shutdown_event.is_set() and game_is_running(game_exe):
            if not rpc_connected:
                connected = False
                # Serialize connection setup with WebSocket updates. This keeps
                # an early custom update from being overwritten by the default.
                with rpc_lock:
                    if not rpc_connected:
                        connected = connect_discord(app_id)
                        if connected:
                            print("[RPC] Connected to Discord.")
                            try:
                                rpc.update(
                                    details=DEFAULT_DETAILS,
                                    state=DEFAULT_STATE,
                                    start=SESSION_START,
                                    large_image=clean_text(DEFAULT_LARGE_IMAGE, 256),
                                    large_text=clean_text(DEFAULT_LARGE_TEXT, 128),
                                )
                            except Exception as exc:
                                print(f"[RPC] Default presence failed: {type(exc).__name__}: {exc}")
                                with suppress(Exception):
                                    rpc.close()
                                rpc = None
                                rpc_connected = False
                                connected = False
                            if connected and pending_update is not None:
                                if apply_presence(pending_update):
                                    pending_update = None
                if not connected:
                    time.sleep(CONNECT_RETRY_SECONDS)
                    continue
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("[RPC] Shutdown requested.")
    finally:
        shutdown_event.set()
        with rpc_lock:
            if rpc is not None:
                with suppress(Exception):
                    rpc.clear()
                with suppress(Exception):
                    rpc.close()
            rpc = None
            rpc_connected = False
        if server_instance is not None:
            with suppress(Exception):
                server_instance.shutdown()
        print("[RPC] Bridge stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_bridge())
