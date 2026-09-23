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
Then its links (`depends_on: <contract>/<unit>` on a unit, `gate: <value>`
on a finding), then a contract's feature doc reference (`doc:
docs/features/<id>.md`), and last its summary after ` | `. Each part but the
id and status prints only when the item has it, after exactly one space.

`taskcontract tree <id>` queries one item: the id matched whole, every item
with it printed as one block, in the tree's order, with one empty line
between blocks. A block opens on the item's line cut after the evidence,
then gives one labeled field per line, each only when the item has it:
`summary:` whole, one line per link kind with its targets joined by `, `,
`doc:` with the feature doc's path at line 1, `file: <path>:<line>` (a
contract or verdict at line 1, a unit or check at its entry's first line, a
finding's file at line 1), and `page:`, the kit page that defines a gate, a
verdict's gate or a task. So a block never passes seven lines. The
unreadable sources follow on stderr. An unknown id prints `no node '<id>' -
print the tree to list every node id` on stderr alone and exits 2; an id
with `--follow` exits 2 too.

`--follow` keeps a pane on the current task. It prints the where-am-I line,
`specs/<contract>/contract.yaml > <contract> > <unit> > <task>`, the unit
and the task by the last segment of their ids. Under it the path to the
task, a top-level item, its unit and the task, each line as the whole tree
prints it, save that the unit's and the task's lines open on the last
segment of their ids; links, the waiting line and `SDLC_NODE` keep full
ids. Above each, when the level holds other items, one line folds them as
`<n> more: <counts>`, the count per status in the six statuses' order,
zeros left out; `tree: pane: fold: names` names them instead (see below).
So the task is always the last line. When the task is `approve-tests` or
`approve-commit`, the first line reads `waiting on a seat: <approval> for
<contract>/<unit>`, above the where-am-I line. With no current task the
pane reads `no current task`, then `<n> items: <counts>` for the top level.

`tree: pane: parts:` in .sdlc/config.yaml, read afresh at each render,
lists the fields each item line shows, from id, status, marks, evidence,
links, doc and summary. The line still opens on its id, then shows only the
listed fields, in the order above whatever order the list gives; `id`
changes nothing, and `[]` shows the id alone. Unset, a line shows every
field. Any other value, or a list naming anything else, is ignored as a
whole, and each render then prints `pane parts ignored: <value> - give a
list from id, status, marks, evidence, links, doc, summary` on stderr,
after the unreadable sources. The key changes no other line.

`tree: pane: fold:`, read the same way, set to `names` makes each fold
line, and the `<n> items` line, name the items it folds in place of the
counts: `<id> [<status>]` per item, the id as its own line would open,
joined by `, ` in the tree's order; `parts:` changes none of it. `counts`,
or unset, keeps the counts. Any other value keeps them too, and each
render then prints `pane fold ignored: <value> - give names or counts` on
stderr, after the parts line. The key changes no item line.

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
from .progress import _no_node
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


def line(item: Item, parts: list[str] | None = None) -> str:
    """One item's line without its indent: the id, then every field it has,
    or with `parts` only the fields it names, in the same order."""
    tag = f"kind: {item.kind}" if item.level == "finding" else item.status
    fields = {
        "status": f" [{tag}]",
        "marks": "".join(f" {mark}" for mark in item.marks),
        "evidence": f" {item.evidence}" if item.evidence else "",
        "links": "".join(f" {link}" for link in item.links),
        "doc": f" doc: {item.doc}" if item.doc else "",
        "summary": f" | {item.summary}" if item.summary else "",
    }
    return item.id + "".join(text for name, text in fields.items()
                             if parts is None or name in parts)


def block(root: Path, item: Item) -> str:
    """One item as the query prints it: its line cut after the evidence,
    then one labeled field per line, each only when the item has it."""
    lines = [line(item, ["status", "marks", "evidence"])]
    if item.summary:
        lines.append(f"summary: {item.summary}")
    kinds: dict[str, list[str]] = {}  # each link kind's targets, in first-seen order
    for link in item.links:
        kind, _, target = link.partition(": ")
        kinds.setdefault(kind, []).append(target)
    lines += [f"{kind}: {', '.join(targets)}" for kind, targets in kinds.items()]
    if item.doc:
        lines.append(f"doc: {item.doc}:1")
    reference = tree.reference(root, item)
    if reference:
        lines.append(f"file: {reference}")
    if item.page:
        lines.append(f"page: {item.page}")
    return "".join(text + "\n" for text in lines)


def _matches(items: list[Item], item_id: str) -> list[Item]:
    """Every item with this id, in print order."""
    found: list[Item] = []
    for item in items:
        if item.id == item_id:
            found.append(item)
        found += _matches(item.children, item_id)
    return found


def pane(items: list[Item], parts: list[str] | None = None,
         fold: str | None = None) -> list[str]:
    """The `--follow` lines, uncut: the where-am-I line, then the path to
    the current task, each level's other items folded above the item on
    the path, the unit and the task by the last segment of their ids; the
    waiting line first when the current task is an approval. `parts`, when
    given, picks the fields of each item line; `fold` set to `names` names
    the folded items in place of their counts."""
    path = _path(items)
    if path is None:
        folded = _fold(items, 0, fold)
        return ["no current task", f"{len(items)} items" + (f": {folded}" if folded else "")]
    lines: list[str] = []
    unit, _, key = path[-1].id.rpartition("/")
    if key in APPROVALS:
        lines.append(f"waiting on a seat: {key} for {unit}")
    contract = path[0].id
    lines.append(f"specs/{contract}/contract.yaml > {contract} > "
                 f"{unit.rpartition('/')[2]} > {key}")
    siblings = items
    for depth, chosen in enumerate(path):
        others = [item for item in siblings if item is not chosen]
        if others:
            lines.append(f"{INDENT * depth}{len(others)} more: {_fold(others, depth, fold)}")
        text = line(chosen, parts)
        if depth:  # under another item: the id's last segment, the rest whole
            text = chosen.id.rpartition("/")[2] + text[len(chosen.id):]
        lines.append(INDENT * depth + text)
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


def _fold(items: list[Item], depth: int, fold: str | None) -> str:
    """A fold line's text after its opening: with `fold` set to `names`,
    `<id> [<status>]` per item in the tree's order, the id whole at the top
    level and by its last segment under another item; else the counts."""
    if fold != "names":
        return _counts(items)
    return ", ".join(f"{item.id.rpartition('/')[2] if depth else item.id} [{item.status}]"
                     for item in items)


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
    neither stops nor waits on the commands it started."""
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
    """One render in one write, then each unreadable source on stderr, then
    a bad `tree: pane:` key; returns the current task's id, or None."""
    items, problems = build(root, cache)
    settings = tree.pane_settings(root, problems)
    width = max(shutil.get_terminal_size().columns, MIN_WIDTH)
    out.write(CLEAR + "".join(cut(text, width) + "\n"
                              for text in pane(items, settings.get("parts"),
                                               settings.get("fold"))))
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
    With `--follow`, the pane instead, until Ctrl-C. With an id, the query:
    one block per item with that id, then the unreadable sources, exit 0;
    an unknown id prints one line and exits 2, as does an id with `--follow`.
    """
    node = getattr(args, "node", None)
    if node is not None and getattr(args, "follow", False):
        print("taskcontract tree: --follow takes no id - give the id or --follow, not both",
              file=sys.stderr)
        return 2
    if getattr(args, "follow", False):
        _ansi_on()
        return follow(Path(args.root), sys.stdout)
    items, problems = build(Path(args.root))
    if node is None:
        sys.stdout.write(render(items))
    else:
        found = _matches(items, node)
        if not found:
            print(_no_node(node), file=sys.stderr)
            return 2
        sys.stdout.write("\n".join(block(Path(args.root), item) for item in found))
    for problem in problems:
        print(f"taskcontract tree: {problem}", file=sys.stderr)
    return 0
