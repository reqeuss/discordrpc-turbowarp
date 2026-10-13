from __future__ import annotations

import ctypes
import os
import subprocess
import sys
import time
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008


def app_dir() -> Path:
    # When compiled with PyInstaller, use the folder containing the EXE.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


ROOT = app_dir()
GAME = ROOT / "testdiscordrpc.exe"
RPC_DIR = ROOT / "resources" / "rpc"
BRIDGE = RPC_DIR / "rpc_bridge.py"
REQUIREMENTS = RPC_DIR / "requirements.txt"
VENV = ROOT / ".venv"
PYTHON = VENV / "Scripts" / "python.exe"
LOG = ROOT / "discord-rpc-launcher.log"


def show_error(message: str) -> None:
    ctypes.windll.user32.MessageBoxW(None, message, "Game Launcher", 0x10)


def run_hidden(args: list[str], *, cwd: Path, log_handle, timeout: int | None = None) -> subprocess.CompletedProcess:
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    return subprocess.run(
        args,
        cwd=str(cwd),
        stdin=subprocess.DEVNULL,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        startupinfo=startup,
        creationflags=CREATE_NO_WINDOW,
        timeout=timeout,
        check=False,
    )


def main() -> int:
    with LOG.open("a", encoding="utf-8", errors="replace") as log:
        log.write("\n--- Game launcher started ---\n")
        log.flush()

        for required in (GAME, BRIDGE, REQUIREMENTS):
            if not required.is_file():
                message = f"Required file not found:\n{required}\n\nSee {LOG.name} for details."
                log.write(message + "\n")
                show_error(message)
                return 1

        py_launcher = os.environ.get("PY_LAUNCHER", "py")
        try:
            if not PYTHON.is_file():
                log.write("Creating local Python virtual environment...\n")
                log.flush()
                result = run_hidden(
                    [py_launcher, "-3", "-m", "venv", str(VENV)],
                    cwd=ROOT, log_handle=log, timeout=180,
                )
                if result.returncode != 0 or not PYTHON.is_file():
                    raise RuntimeError(
                        "Python 3 was not found or the virtual environment could not be created. "
                        "Install Python 3 and enable the Python launcher."
                    )

            log.write("Installing/checking bridge dependencies...\n")
            log.flush()
            result = run_hidden(
                [str(PYTHON), "-m", "pip", "install", "--disable-pip-version-check",
                 "-r", str(REQUIREMENTS)],
                cwd=ROOT, log_handle=log, timeout=600,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Dependency installation failed (exit code {result.returncode}). "
                    f"Check {LOG.name} and your internet connection."
                )

            log.write("Starting hidden Discord RPC bridge...\n")
            log.flush()
            bridge_log = LOG.open("a", encoding="utf-8", errors="replace")
            startup = subprocess.STARTUPINFO()
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup.wShowWindow = 0
            try:
                subprocess.Popen(
                    [str(PYTHON), "-u", str(BRIDGE)],
                    cwd=str(RPC_DIR),
                    stdin=subprocess.DEVNULL,
                    stdout=bridge_log,
                    stderr=subprocess.STDOUT,
                    startupinfo=startup,
                    creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
                    close_fds=True,
                )
            except Exception:
                bridge_log.close()
                raise

            # Give the bridge a moment to validate its settings and start its socket.
            time.sleep(1.5)
            log.write("Starting game...\n")
            log.flush()
            subprocess.Popen([str(GAME)], cwd=str(ROOT))
            return 0

        except FileNotFoundError:
            message = (
                "Python 3 was not found. Install Python 3 from python.org, "
                "enable the Python launcher, then try again."
            )
            log.write(message + "\n")
            show_error(message)
            return 1
        except Exception as exc:
            message = f"Could not start the game:\n{exc}\n\nSee {LOG.name} for details."
            log.write(message + "\n")
            log.flush()
            show_error(message)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
