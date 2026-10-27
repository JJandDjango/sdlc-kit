"""Refuse a tool call that reaches across the wall during a task.

A plugin hook for `PreToolUse` (hooks/hooks.json). Claude Code sends the
event as one JSON object on stdin. While `{git folder}/sdlc-task.json` names
a running task for the `developer` or `qa` operator, each path the call names
is held against the repository's `wall:` block (`.sdlc/config.yaml`): the
Developer reads no functional test, QA reads no unit test and no
implementation body. QA may still read a code file's interface: an entry
under `wall.interface`, or the file `python -m taskcontract interface` is run
on.

A refusal prints one line on stderr and exits 2. Every other case exits 0
with nothing printed, and so does any error: the hook never raises. It reads
no config, and imports nothing from taskcontract, until a task file is found.
The hook writes no file.
"""

from __future__ import annotations

import fnmatch
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
NAMES = {"developer": "Developer", "qa": "QA"}
INTERFACE_CALL = ["-m", "taskcontract", "interface"]
GLOB_CHARS = "*?["


def git(cwd: str, *args: str) -> str | None:
    """The stripped stdout of `git -C cwd ARGS`; None when git fails or cannot start."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, *args],
            capture_output=True, encoding="utf-8", errors="replace",
            creationflags=NO_WINDOW)
    except OSError:
        return None
    out = (result.stdout or "").strip()
    return out if result.returncode == 0 and out else None


def named_strings(tool: str, tool_input: dict) -> list[tuple[str, bool]]:
    """The strings the call names, in order, each with whether it is the
    file argument of `-m taskcontract interface`; a value that is no string is left out."""
    fields = {
        "Read": ["file_path"], "Edit": ["file_path"], "Write": ["file_path"],
        "NotebookEdit": ["notebook_path"],
        "Grep": ["path", "glob"],  # its `pattern` is a regex, never a path
        "Glob": ["path", "pattern"],
    }.get(tool)
    if fields is not None:
        values = [tool_input.get(key) for key in fields]
        return [(value, False) for value in values if isinstance(value, str)]
    if tool != "Bash":
        return []
    command = tool_input.get("command")
    if not isinstance(command, str):
        return []
    if os.name == "nt":
        command = command.replace("\\", "/")
    try:
        words = shlex.split(command)
    except ValueError:  # an unclosed quote
        words = command.split()
    words = [w.split("=", 1)[1] if w.startswith("-") and "=" in w else w for w in words]
    return [(w, i >= 3 and words[i - 3:i] == INTERFACE_CALL) for i, w in enumerate(words)]


def relative(word: str, root: Path) -> str | None:
    """The word as a path from the root with `/` separators; None when it
    leaves the root or cannot be made relative to it."""
    if os.name == "nt":
        word = word.replace("\\", "/")
    try:
        path = os.path.relpath(os.path.normpath(os.path.join(root, word)), root)
    except (ValueError, OSError):  # another drive
        return None
    path = path.replace(os.sep, "/")
    if path == ".." or path.startswith("../"):
        return None
    return path


def holds(entry: str, path: str, glob_word: bool, reverse: bool = True) -> bool:
    """Whether the wall entry holds the path. A folder entry (a trailing `/`)
    holds the folder and all below it; any other entry is a glob over the path.
    For a glob word, `reverse` also matches the entry's text against the word."""
    if os.name == "nt":
        entry, path = entry.lower(), path.lower()
    reverse = reverse and glob_word
    if entry.endswith("/"):
        folder = entry[:-1]
        if path == folder or path.startswith(folder + "/"):
            return True
        return reverse and fnmatch.fnmatchcase(entry, path)
    return fnmatch.fnmatchcase(path, entry) or (reverse and fnmatch.fnmatchcase(entry, path))


def crossing(operator: str, wall, path: str, glob_word: bool, exempt: bool) -> str | None:
    """What the path is, as the wall refuses it for the operator; None when it passes."""
    if operator == "developer":
        if any(holds(e, path, glob_word) for e in wall.functional):
            return "functional test"
        return None
    if any(holds(e, path, glob_word) for e in wall.unit):
        return "unit test"
    if any(holds(e, path, glob_word) for e in wall.code):
        if exempt or any(holds(e, path, glob_word, reverse=False) for e in wall.interface):
            return None
        return "implementation body"
    return None


def respond(data: bytes) -> str | None:
    """The refusal line for one event, or None to let the call through."""
    event = json.loads(data)
    if not isinstance(event, dict) or not isinstance(event.get("cwd"), str) or not event["cwd"]:
        return None
    cwd = event["cwd"]
    folder = git(cwd, "rev-parse", "--absolute-git-dir")
    if folder is None:
        return None
    try:
        task = json.loads((Path(folder) / "sdlc-task.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(task, dict) or not isinstance(task.get("task"), str):
        return None
    operator = task.get("operator")
    if operator not in NAMES:
        return None
    top = git(cwd, "rev-parse", "--show-toplevel")
    if top is None:
        return None
    root = Path(top)
    # the taskcontract beside the hook, ahead of any other package of that name
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from taskcontract.declaration import read_wall
    wall = read_wall(root)
    if wall is None:
        return None
    tool_input = event.get("tool_input")
    tool = event.get("tool_name")
    if not isinstance(tool_input, dict) or not isinstance(tool, str):
        return None
    for word, exempt in named_strings(tool, tool_input):
        path = relative(word, root)
        if path is None:
            continue
        what = crossing(operator, wall, path, any(c in word for c in GLOB_CHARS), exempt)
        if what is not None:
            return f"Task {task['task']}: {NAMES[operator]} reads no {what}: {word}"
    return None


def main() -> int:
    """Read the event from stdin; refuse with exit 2, else exit 0 and print nothing."""
    try:
        line = respond(sys.stdin.buffer.read())
        if line is None:
            return 0
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        print(line, file=sys.stderr)
    except Exception:
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
