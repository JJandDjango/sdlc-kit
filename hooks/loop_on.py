"""Tell a fresh session that a session loop is on in its repo.

A plugin hook for `SessionStart` (hooks/hooks.json). Claude Code sends the
event as one JSON object on stdin. The repo is the one holding the event's
`cwd`, else the process's own folder. While `{git folder}/sdlc-loop/loop.json`
exists, whatever it holds, the hook prints one line that points the session at
the loop's rules (skills/sdlc/flows/loop.md), the stop rule too.

The hook never blocks: it exits 0 in every case and prints nothing outside a
loop, outside a git repository, or on an error. It writes no file.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
PLUGIN = Path(__file__).resolve().parents[1].as_posix()


def event_cwd(data: bytes) -> str | None:
    """The event's non-empty string `cwd`; None when the input is no such object."""
    try:
        event = json.loads(data)
    except ValueError:
        return None
    if isinstance(event, dict) and isinstance(event.get("cwd"), str) and event["cwd"]:
        return event["cwd"]
    return None


def git_folder(cwd: str | None) -> Path | None:
    """The absolute git folder of the repo holding cwd (the process's folder when
    None); None when git fails or cannot start."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=cwd, capture_output=True, encoding="utf-8", errors="replace",
            creationflags=NO_WINDOW)
    except (OSError, ValueError):
        return None
    out = (result.stdout or "").strip()
    return Path(out) if result.returncode == 0 and out else None


def main() -> int:
    """Print the loop line when a loop is on; always exit 0."""
    try:
        folder = git_folder(event_cwd(sys.stdin.buffer.read()))
        if folder is not None and (folder / "sdlc-loop" / "loop.json").exists():
            print(f"A session loop is on in this repo, and the user may be away. Every question to the user is a stop: first run the stop rule (L3) in {PLUGIN}/skills/sdlc/flows/loop.md, then ask in a plain message, never by AskUserQuestion. Follow the same file at every wrap. Run loop.py as python {PLUGIN}/workflows/tools/loop.py.")
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
