
import json
import threading
import time
from pathlib import Path
from contextlib import suppress

import psutil
from pypresence import Presence
from websockets.sync.server import serve


# ============================================================
# CONFIGURATION
# ============================================================

RPC_DIR = Path(__file__).resolve().parent
GAME_DIR = RPC_DIR.parent.parent

APP_ID = "ID APP"
GAME_EXE = GAME_DIR / "game.exe"

HOST = "127.0.0.1"
PORT = 32123
POLL_INTERVAL = 0.25

DEFAULT_DETAILS = "Playing Solo"
DEFAULT_STATE = "In the game"
DEFAULT_LARGE_IMAGE = "icon"
DEFAULT_LARGE_TEXT = "My game"

# ============================================================


rpc = None
rpc_connected = False

rpc_lock = threading.RLock()
server_instance = None
server_ready = threading.Event()

session_start = int(time.time())

# Keep the latest update if the extension sends it before
# Discord RPC has finished connecting.
pending_update = None


# ============================================================
# GAME DETECTION
# ============================================================

def game_is_running():
    target = GAME_EXE.name.casefold()

    for process in psutil.process_iter(["name"]):
        try:
            name = process.info.get("name")

            if name and name.casefold() == target:
                return True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return False


# ============================================================
# VALUE VALIDATION
# ============================================================

def optional_text(data, key, limit=128):
    value = data.get(key)

    if value is None:
        return None

    value = str(value).strip()

    return value[:limit] if value else None


def optional_int(data, key):
    value = data.get(key)

    if value in (None, ""):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def build_party_size(data):
    """
    pypresence expects party_size=[current_size, maximum_size].
    Both values must be valid.
    """
    current_size = optional_int(data, "partySize")
    maximum_size = optional_int(data, "partyMax")

    if current_size is None or maximum_size is None:
        return None

    if maximum_size <= 0:
        return None

    if current_size < 0 or current_size > maximum_size:
        return None

    return [current_size, maximum_size]


# ============================================================
# APPLY DISCORD RICH PRESENCE
# ============================================================

def apply_presence(data):
    """
    Apply all activity fields received from discord-rpc.js.
    Must be called while rpc_lock is held.
    """
    global rpc, rpc_connected

    if not rpc_connected or rpc is None:
        print("[RPC] Update ignored: Discord is not connected.")
        return

    secrets = {}

    join_secret = optional_text(data, "joinSecret", 128)
    spectate_secret = optional_text(data, "spectateSecret", 128)

    if join_secret:
        secrets["join"] = join_secret

    if spectate_secret:
        secrets["spectate"] = spectate_secret

    try:
        rpc.update(
            # Main activity
            details=optional_text(data, "details"),
            state=optional_text(data, "state"),

            # Timestamps: Unix timestamps in seconds
            start=optional_int(data, "start"),
            end=optional_int(data, "end"),

            # Images
            large_image=optional_text(data, "largeImage", 256),
            large_text=optional_text(data, "largeText"),
            small_image=optional_text(data, "smallImage", 256),
            small_text=optional_text(data, "smallText"),

            # Party
            party_id=optional_text(data, "partyId", 128),
            party_size=build_party_size(data),

            # Join / Spectate secrets
            secrets=secrets or None,

            # Instance
            instance=bool(data.get("instance", True)),
        )

        print(
            "[RPC] Presence updated | "
            f"details={optional_text(data, 'details')!r} | "
            f"state={optional_text(data, 'state')!r}"
        )

    except Exception as error:
        print(f"[RPC] Update failed: {type(error).__name__}: {error}")


# ============================================================
# WEBSOCKET MESSAGE HANDLER
# ============================================================

def handle_message(ws):
    global pending_update

    print("[RPC] Extension connected.")

    try:
        for raw_message in ws:
            try:
                data = json.loads(raw_message)

                if not isinstance(data, dict):
                    print("[RPC] Invalid message: expected an object.")
                    continue

                action = data.get("action")

                with rpc_lock:
                    if action == "update":
                        if not rpc_connected or rpc is None:
                            # Keep the latest update until Discord connects.
                            pending_update = data
                            print(
                                "[RPC] Update queued: "
                                "waiting for Discord connection."
                            )
                            continue

                        apply_presence(data)

                    elif action == "clear":
                        pending_update = None

                        if rpc_connected and rpc is not None:
                            try:
                                rpc.clear()
                                print("[RPC] Presence cleared.")
                            except Exception as error:
                                print(f"[RPC] Clear failed: {error}")

                    else:
                        print(f"[RPC] Unknown action: {action!r}")

            except json.JSONDecodeError:
                print("[RPC] Invalid JSON received.")

            except Exception as error:
                print(
                    f"[RPC] Message error: "
                    f"{type(error).__name__}: {error}"
                )

    except Exception as error:
        print(f"[RPC] WebSocket connection ended: {error}")

    finally:
        print("[RPC] Extension disconnected.")


# ============================================================
# WEBSOCKET SERVER
# ============================================================

def websocket_server():
    global server_instance

    try:
        with serve(
            handle_message,
            HOST,
            PORT,
            max_size=64 * 1024,
        ) as server:
            server_instance = server
            server_ready.set()

            print(f"[RPC] WebSocket server ready at {HOST}:{PORT}")

            server.serve_forever()

    except Exception as error:
        print(
            f"[RPC] WebSocket server error: "
            f"{type(error).__name__}: {error}"
        )
        server_ready.set()


# ============================================================
# MAIN
# ============================================================

def main():
    global rpc, rpc_connected, pending_update

    print("[RPC] Starting bridge...")
    print(f"[RPC] Game path: {GAME_EXE}")

    if not GAME_EXE.is_file():
        print("[RPC] ERROR: Game executable not found.")
        print("[RPC] Check GAME_DIR and GAME_EXE.")
        return

    if not APP_ID.isdigit():
        print("[RPC] ERROR: APP_ID must be your Discord Application ID.")
        return

    # Start WebSocket server before waiting for the game.
    thread = threading.Thread(
        target=websocket_server,
        daemon=True,
    )
    thread.start()

    if not server_ready.wait(timeout=5):
        print("[RPC] ERROR: WebSocket server did not start in time.")
        return

    if server_instance is None:
        print("[RPC] ERROR: WebSocket server failed to start.")
        return

    print(f"[RPC] Waiting for {GAME_EXE.name}...")

    try:
        while not game_is_running():
            time.sleep(POLL_INTERVAL)

        print("[RPC] Game detected!")

        with rpc_lock:
            rpc = Presence(APP_ID)
            rpc.connect()
            rpc_connected = True

            # Default activity while waiting for extension updates.
            rpc.update(
                details=DEFAULT_DETAILS,
                state=DEFAULT_STATE,
                start=session_start,
                large_image=DEFAULT_LARGE_IMAGE or None,
                large_text=DEFAULT_LARGE_TEXT or None,
            )

            print("[RPC] Discord connected. Default presence active.")

            # Apply an update that arrived before Discord connected.
            if pending_update is not None:
                saved_update = pending_update
                pending_update = None
                apply_presence(saved_update)

        # Stop the bridge when the game closes.
        while game_is_running():
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("[RPC] Shutdown requested.")

    except Exception as error:
        print(
            f"[RPC] Runtime error: "
            f"{type(error).__name__}: {error}"
        )

    finally:
        print("[RPC] Shutting down...")

        with rpc_lock:
            if rpc is not None and rpc_connected:
                with suppress(Exception):
                    rpc.clear()

                with suppress(Exception):
                    rpc.close()

            rpc_connected = False
            rpc = None

        if server_instance is not None:
            with suppress(Exception):
                server_instance.shutdown()

        print("[RPC] Bridge stopped.")


if __name__ == "__main__":
    main()
