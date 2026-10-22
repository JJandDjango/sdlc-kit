"""Tell the session once when its context passes 200K and 400K tokens.

A plugin hook for `PostToolUse` and `UserPromptSubmit` (hooks/hooks.json).
Claude Code sends the event as one JSON object on stdin. The size is the
newest main-thread assistant line's input, cache-write and cache-read
tokens in the event's transcript, read backward from the end so a large
transcript costs one or two chunks.

Each message shows once a session id, to the user (`systemMessage`) and to
the agent (`additionalContext`). A marker file per threshold in the temp
directory records that it showed; the hook writes nothing else. A step
past 400K writes both markers, so the 200K message never follows it.

The hook never blocks: it exits 0 in every case and prints nothing on an
error, below a threshold, or in a repo with no `.sdlc/workflow.md`.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

TARGET = 200000
LIMIT = 400000

MESSAGES = {
    TARGET: "This session has passed 200K tokens, the target. Finish the deliverable and close.",
    LIMIT: "This session has passed 400K tokens, the limit. Save the notes and close now.",
}

USAGE_FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
CHUNK = 64 * 1024


def newest_assistant(path: str) -> dict | None:
    """The newest assistant line that is not a sidechain, read backward; None if there is none.

    Lines older than it are never parsed. A line after it that is not JSON raises.
    """
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        pos = f.tell()
        head = b""
        while True:
            if pos == 0:
                lines = [head]
            else:
                step = min(CHUNK, pos)
                pos -= step
                f.seek(pos)
                lines = (f.read(step) + head).split(b"\n")
                head = lines.pop(0)
            for raw in reversed(lines):
                raw = raw.strip()
                if not raw:
                    continue
                line = json.loads(raw.decode("utf-8"))
                if not isinstance(line, dict):
                    raise ValueError("a transcript line is not an object")
                if line.get("type") == "assistant" and line.get("isSidechain") is not True:
                    return line
            if pos == 0:
                return None


def context_size(line: dict) -> int:
    """The line's input, cache-write and cache-read tokens; a missing field counts 0."""
    usage = line.get("message", {}).get("usage", {})
    total = 0
    for field in USAGE_FIELDS:
        value = usage.get(field, 0)
        if type(value) is not int:
            raise ValueError(f"usage {field} is not an int")
        total += value
    return total


def claim(session_id: str, threshold: int) -> bool:
    """Create the session's marker for threshold; False if it already exists."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "", session_id)
    path = os.path.join(tempfile.gettempdir(), f"sdlc-context-{safe}-{threshold}")
    try:
        os.close(os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        return False
    return True


def respond(data: bytes) -> str:
    """The hook's stdout for one event: one JSON object, or "" when nothing shows."""
    event = json.loads(data.decode("utf-8"))
    if not isinstance(event, dict):
        return ""
    cwd = event.get("cwd")
    if not isinstance(cwd, str) or not (Path(cwd) / ".sdlc" / "workflow.md").is_file():
        return ""
    session_id = event["session_id"]
    if not isinstance(session_id, str):
        return ""
    line = newest_assistant(event["transcript_path"])
    if line is None:
        return ""
    size = context_size(line)
    if size > LIMIT:
        shown = claim(session_id, LIMIT)
        claim(session_id, TARGET)
        text = MESSAGES[LIMIT] if shown else None
    elif size > TARGET:
        text = MESSAGES[TARGET] if claim(session_id, TARGET) else None
    else:
        text = None
    if text is None:
        return ""
    return json.dumps({
        "systemMessage": text,
        "hookSpecificOutput": {
            "hookEventName": event["hook_event_name"],
            "additionalContext": text,
        },
    }) + "\n"


def main() -> int:
    """Read the event from stdin and print the response; every error prints nothing."""
    try:
        out = respond(sys.stdin.buffer.read())
    except Exception:
        out = ""
    if out:
        sys.stdout.write(out)
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
