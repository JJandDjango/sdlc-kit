"""Turn an AskUserQuestion dialog back to the stop rule while a loop is on.

A plugin hook for `PreToolUse` (hooks/hooks.json, matcher `AskUserQuestion`).
Claude Code sends the event as one JSON object on stdin. The repo is the one
holding the event's `cwd`, else the process's own folder. When the event is an
`AskUserQuestion` call and `{git folder}/sdlc-loop/loop.json` exists, whatever
it holds, the hook refuses the call: it prints one line on stderr that points
the session at the stop rule (L3 in skills/sdlc/flows/loop.md) and exits 2. A
dialog that waits is no idle session, so the loop's timer would never land.

Every other case prints nothing and exits 0: any other tool, no loop, outside a
git repository, and any error, an unreadable event included. It writes no file.
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


def is_ask(data: bytes) -> bool:
    """True when the input is a JSON object whose tool_name is AskUserQuestion."""
    try:
        event = json.loads(data)
    except ValueError:
        return False
    return isinstance(event, dict) and event.get("tool_name") == "AskUserQuestion"


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
    """Refuse an AskUserQuestion call while a loop is on (exit 2); else exit 0."""
    try:
        data = sys.stdin.buffer.read()
        if not is_ask(data):
            return 0
        folder = git_folder(event_cwd(data))
        if folder is not None and (folder / "sdlc-loop" / "loop.json").exists():
            print(f"A session loop is on in this repo: this question is a stop. Run the stop rule (L3) in {PLUGIN}/skills/sdlc/flows/loop.md, then ask in a plain message that ends on the question.", file=sys.stderr)
            return 2
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
