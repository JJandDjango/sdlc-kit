"""`taskcontract tree` - print the derived tree (ADR 0031).

One item per line, two spaces of indent per level. The line opens on the
item's full id, the node path ADR 0031 gives it, so the print states every
id whole. Then the status in brackets, or a finding's kind in its place,
then the item's marks (`inactive` on a gate a finding names that is not
active, `current` on the current task), then its evidence (on a `G0`
verdict, the validator command and the `HEAD` it read; on a check whose last
run was green as expected, that run's command and `HEAD`; on a task done by
its own record, `by <seat>` on an approval and the record's `HEAD`; on a
unit or contract done by its close, the close's `HEAD`; each with `dirty`
when it applies; on a task blocked by its own record, `because <reason>`).
Then its links
(`depends_on: <contract>/<unit>` on a unit, `gate: <value>` on a finding),
then a contract's feature doc reference (`doc: docs/features/<id>.md`), and
last its summary after ` | `. Each part but the id and status prints only
when the item has it, after exactly one space.

`--follow` keeps a pane on the current task. It prints the path to it, a
top-level item, its unit and the task, each line as the whole tree prints
it; above each, when the level holds other items, one line folds them as
`<n> more: <counts>`, the count per status in the six statuses' order, zeros
left out. So the task is always the last line. When the task is
`approve-tests` or `approve-commit`, the first line reads `waiting on a
seat: <approval> for <contract>/<unit>`. With no current task the pane
reads `no current task`, then `<n> items: <counts>` for the top level.
Each line longer than the pane's width is cut to it and ends in `...`. The
pane lists its sources' files once a second and redraws, clearing the
screen with ANSI escapes, only when a file was added, removed or changed;
it keeps each `G0` reading in memory until its contract or the vocabulary
changes, and writes no file. Ctrl-C ends it.

Each time a render arrives at an approval, the pane starts the command set
as `tree: notify:` in .sdlc/config.yaml through the shell, once, with the
task's id in `SDLC_NODE`; with none set, it starts nothing. It never waits
on the command: at each second it checks the commands it started, and one
that ended nonzero prints `notify failed, exit <code>: <command>` on
stderr, as does one that cannot start, with code 127.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from . import tree
from .tree import APPROVALS, CURRENT, STATUSES, Item, build

INDENT = "  "
CLEAR = "\x1b[H\x1b[2J"  # cursor home, then erase the screen
MIN_WIDTH = 10
# The folders the pane lists afresh at every scan, every file under each.
WATCHED = ("specs", ".sdlc/findings", ".sdlc/progress", "docs/features")
CONFIG = ".sdlc/config.yaml"
VOCABULARY = "specs/vocabulary/"


def render(items: list[Item]) -> str:
    """The tree as text, one line per item, byte-identical across runs."""
    lines: list[str] = []

    def walk(item: Item, depth: int) -> None:
        lines.append(INDENT * depth + line(item))
        for child in item.children:
            walk(child, depth + 1)

    for item in items:
        walk(item, 0)
    return "".join(text + "\n" for text in lines)


def line(item: Item) -> str:
    """One item's line without its indent."""
    tag = f"kind: {item.kind}" if item.level == "finding" else item.status
    marks = "".join(f" {mark}" for mark in item.marks)
    evidence = f" {item.evidence}" if item.evidence else ""
    links = "".join(f" {link}" for link in item.links)
    doc = f" doc: {item.doc}" if item.doc else ""
    summary = f" | {item.summary}" if item.summary else ""
    return f"{item.id} [{tag}]{marks}{evidence}{links}{doc}{summary}"


def pane(items: list[Item]) -> list[str]:
    """The `--follow` lines, uncut: the path to the current task, each
    level's other items folded above the item on the path; the waiting
    line first when the current task is an approval."""
    path = _path(items)
    if path is None:
        counts = _counts(items)
        return ["no current task", f"{len(items)} items" + (f": {counts}" if counts else "")]
    lines: list[str] = []
    unit, _, key = path[-1].id.rpartition("/")
    if key in APPROVALS:
        lines.append(f"waiting on a seat: {key} for {unit}")
    siblings = items
    for depth, chosen in enumerate(path):
        others = [item for item in siblings if item is not chosen]
        if others:
            lines.append(f"{INDENT * depth}{len(others)} more: {_counts(others)}")
        lines.append(INDENT * depth + line(chosen))
        siblings = chosen.children
    return lines


def _path(items: list[Item]) -> list[Item] | None:
    """[top-level item, unit, task] down to the current task, or None."""
    for top in items:
        for unit in top.children:
            for task in unit.children:
                if CURRENT in task.marks:
                    return [top, unit, task]
    return None


def _counts(items: list[Item]) -> str:
    """`<n> <status>` per status in order, zeros left out."""
    statuses = [item.status for item in items]
    return ", ".join(f"{statuses.count(status)} {status}"
                     for status in STATUSES if status in statuses)


def cut(text: str, width: int) -> str:
    """The line whole when it fits, else its prefix ending in `...`."""
    return text if len(text) <= width else text[:width - 3] + "..."


def scan(root: Path) -> dict[str, tuple[int, int]]:
    """(modification time, size) per watched file, keyed by its path from
    the root; a file outside the root, such as the kit's lists, by its own
    path."""
    files = [root / CONFIG, tree.GATES_PATH, tree.TASKS_PATH]
    for folder in WATCHED:
        if (root / folder).is_dir():
            files += (root / folder).rglob("*")
    seen: dict[str, tuple[int, int]] = {}
    for path in files:
        try:
            if path.is_file():
                stat = path.stat()
                seen[_key(path, root)] = (stat.st_mtime_ns, stat.st_size)
        except OSError:
            continue  # gone between the listing and the stat
    return seen


def forget(cache: dict[str, str], before: dict, after: dict) -> None:
    """Drop the `G0` readings a change may alter: all of them when the
    vocabulary changed, else each contract whose file changed."""
    changed = {key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}
    if any(key.startswith(VOCABULARY) for key in changed):
        cache.clear()
        return
    for key in changed:
        parts = key.split("/")
        if len(parts) == 3 and parts[0] == "specs" and parts[2] == "contract.yaml":
            cache.pop(parts[1], None)


def follow(root: Path, out, sleep=None) -> int:
    """The pane: render, then each second check the notify commands still
    running and render again when a source changed; Ctrl-C exits 0 and
    leaves the commands running."""
    cache: dict[str, str] = {}
    running: list[tuple[subprocess.Popen, str]] = []
    try:
        seen = scan(root)
        current = _draw(root, out, cache)
        _arrive(root, current, None, running)
        while True:
            (sleep or time.sleep)(1)
            running[:] = [run for run in running if not _ended(*run)]
            now = scan(root)
            if now != seen:
                forget(cache, seen, now)
                seen = now
                current, before = _draw(root, out, cache), current
                _arrive(root, current, before, running)
    except KeyboardInterrupt:
        return 0


def _draw(root: Path, out, cache: dict[str, str]) -> str | None:
    """One render in one write, then each unreadable source on stderr;
    returns the current task's id, or None."""
    items, problems = build(root, cache)
    width = max(shutil.get_terminal_size().columns, MIN_WIDTH)
    out.write(CLEAR + "".join(cut(text, width) + "\n" for text in pane(items)))
    out.flush()
    for problem in problems:
        print(f"taskcontract tree: {problem}", file=sys.stderr)
    path = _path(items)
    return path[-1].id if path else None


def _arrive(root: Path, current: str | None, before: str | None,
            running: list[tuple[subprocess.Popen, str]]) -> None:
    """Start the notify command when the render arrived at an approval: the
    current task is one, and the previous render's was another task or none."""
    if current is None or current == before or current.rsplit("/", 1)[-1] not in APPROVALS:
        return
    command = tree.notify_command(root)
    if command is None:
        return
    try:
        run = subprocess.Popen(command, shell=True, cwd=root,
                               env={**os.environ, "SDLC_NODE": current},
                               stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
    except OSError:
        print(f"notify failed, exit 127: {command}", file=sys.stderr)
        return
    running.append((run, command))


def _ended(run: subprocess.Popen, command: str) -> bool:
    """Whether the command has ended; a nonzero exit prints one line."""
    code = run.poll()
    if code is None:
        return False
    if code != 0:
        print(f"notify failed, exit {code}: {command}", file=sys.stderr)
    return True


def _key(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _ansi_on() -> None:
    """Let a Windows console act on the escapes; any failure leaves it as is."""
    try:
        if os.name != "nt" or not sys.stdout.isatty():
            return
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # the console's output
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # virtual terminal
    except Exception:
        pass


def main_tree(args) -> int:
    """The whole tree on stdout; each unreadable source as one line on stderr.

    An unreadable file never stops the print: the rest of the tree is still
    the product, so the command exits 0 and names the file it skipped.
    With `--follow`, the pane instead, until Ctrl-C.
    """
    if getattr(args, "follow", False):
        _ansi_on()
        return follow(Path(args.root), sys.stdout)
    items, problems = build(Path(args.root))
    sys.stdout.write(render(items))
    for problem in problems:
        print(f"taskcontract tree: {problem}", file=sys.stderr)
    return 0
