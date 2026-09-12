import os
import time
from pathlib import Path

PID_FILE = Path(__file__).with_name("cycle.pid")
HEARTBEAT_FILE = Path(__file__).with_name("cycle_status.txt")


def is_pid_running(pid: int) -> bool:
    """Check whether the given PID exists and is still active."""
    if pid <= 0:
        return False

    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def mark_cycle_running() -> None:
    """Write current process ID and a heartbeat to show the cycle is active."""
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    HEARTBEAT_FILE.write_text(str(time.time()), encoding="utf-8")


def cycle_is_running(timeout_seconds: int = 30) -> bool:
    """
    Return True when either:
    - the PID from the last cycle is still alive, or
    - the heartbeat file was updated recently.
    """
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text(encoding="utf-8").strip())
        except (ValueError, OSError):
            pid = -1

        if is_pid_running(pid):
            return True

    if HEARTBEAT_FILE.exists():
        try:
            last_seen = float(HEARTBEAT_FILE.read_text(encoding="utf-8").strip())
        except (ValueError, OSError):
            last_seen = 0.0

        if time.time() - last_seen <= timeout_seconds:
            return True

    return False


def main() -> None:
    status = "RUNNING" if cycle_is_running() else "NOT RUNNING"
    print(f"Cycle status: {status}")


if __name__ == "__main__":
    main()
