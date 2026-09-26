"""`taskcontract tree` - print the derived tree (ADR 0031).

One item per line, two spaces of indent per level. The line opens on the
item's full id, the node path ADR 0031 gives it, so the print states every
id whole, then its plain name (the name the kit's lists give a gate, a
verdict's gate, a condition or a task; a unit's `done_means`; a check's
sketch line; a finding's statement; a contract's `title`, else `(no
title)`). Then the status in brackets, or a finding's kind in its place,
then the item's marks (`inactive` on a gate a finding names that is not
active and on a contract's next gate, `current` on the current task, and
on a contract its drift mark: `no feature document`, `no "Ready:" row` or
`stale: document rD, contract from rM`), then
its evidence (on a `G0` verdict, the validator command and the `HEAD` it
read; on a check whose last run was green as expected, that run's command
and `HEAD`; on a task done by its own record, `by <seat>` on an approval
and the record's `HEAD`; on a unit or contract done by its close, the
close's `HEAD`; each with `dirty` when it applies; on a task blocked by its
own record, `because <reason>`; on the approval that holds the current
task, `seat: <seats>`, its unit's `confirmed_by` joined by `, `).
Then its links (`depends_on: <contract>/<unit>` on a unit, `gate: <value>`
on a finding), then a contract's feature doc reference (`doc:
docs/features/<id>.md`), and last a contract's summary, its intent, after
` | `. Each part but the id and status prints only when the item has it,
after exactly one space. A line break inside a part reads as one space, so
an item keeps one line.
Under a condition that is not done, each of its diagnostics prints on a
line of its own, one level deeper, as `- ` and the validator's message
without its code; such a line is not an item and has no id.

`taskcontract tree <id>` queries one item: the id matched whole, as the model
holds it or as the tree prints it, every item with it printed as one block,
in the tree's order, with one empty line between blocks. A block opens on
the item's line cut after the evidence, then gives one labeled field per
line, each only when the item has it: `summary:` whole, on a contract
with an intent, one line per link kind with its targets joined by `, `,
`doc:` with the feature doc's path at line 1, `file: <path>:<line>` (a contract or verdict at line 1, a unit or
check at its entry's first line, a finding's file at line 1), and `page:`,
the kit page that defines a gate, a verdict's or a condition's gate, or a
task. A condition's diagnostics never print here. So a block never passes
seven lines, whatever a field holds. The unreadable sources follow on
stderr. An unknown id prints `no node '<id>' - print the tree to list every
node id` on stderr alone and exits 2; an id with `--follow` exits 2 too.

`--follow` runs the interactive pane, taskcontract/pane.py, imported only
then; without the `pane` extra it prints `taskcontract tree: --follow
needs the pane extra - pip install 'sdlc-taskcontract[pane]'` on stderr
and exits 2. The pane is described there. What it needs from here needs
no Textual and stays here: the line an item prints, the path to the
current task, a closed item's group (the counts by status, or under `tree:
pane: fold: names` each item's name and status), the listing of the
pane's sources, and the `G0` readings a change to them drops.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import tree
from .progress import _no_node
from .tree import CURRENT, STATUSES, G0Reading, Item, build

INDENT = "  "
# The folders the pane lists afresh at every scan, every file under each.
WATCHED = ("specs", ".sdlc/findings", ".sdlc/progress", "docs/features")
CONFIG = ".sdlc/config.yaml"
VOCABULARY = "specs/vocabulary/"


def render(items: list[Item]) -> str:
    """The tree as text, one line per item, each condition's diagnostics
    right under it one level deeper, byte-identical across runs."""
    lines: list[str] = []

    def walk(item: Item, depth: int) -> None:
        lines.append(INDENT * depth + line(item))
        lines.extend(f"{INDENT * (depth + 1)}- {message}" for message in item.diagnostics)
        for child in item.children:
            walk(child, depth + 1)

    for item in items:
        walk(item, 0)
    return "".join(text + "\n" for text in lines)


def line(item: Item, parts: list[str] | None = None) -> str:
    """One item's line without its indent: the id and the plain name, then
    every field it has, or with `parts` only the fields it names, in the
    same order."""
    fields = {
        "status": f" [{_tag(item)}]",
        "marks": "".join(f" {mark}" for mark in item.marks),
        "evidence": f" {item.evidence}" if item.evidence else "",
        "links": "".join(f" {link}" for link in item.links),
        "doc": f" doc: {item.doc}" if item.doc else "",
        "summary": f" | {item.summary}" if item.summary else "",
    }
    return (_flat(item.id) + (_flat(f" {item.name}") if item.name else "")
            + "".join(_flat(text) for name, text in fields.items()
                      if parts is None or name in parts))


def _tag(item: Item) -> str:
    """What a line shows in brackets: the status, or a finding's kind."""
    return f"kind: {item.kind}" if item.level == "finding" else item.status


def _flat(text: str) -> str:
    """A field or a line by the text rule, save that it keeps its leading
    space: each line break inside it reads as one space, so it prints on
    one line."""
    return " ".join(text.splitlines())


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
    return "".join(_flat(text) + "\n" for text in lines)


def _matches(items: list[Item], item_id: str) -> list[Item]:
    """Every item with this id, as the model holds it or as the tree prints
    it, in print order."""
    found: list[Item] = []
    for item in items:
        if item_id in (item.id, _flat(item.id)):
            found.append(item)
        found += _matches(item.children, item_id)
    return found


def _path(items: list[Item]) -> list[Item] | None:
    """[top-level item, unit, task] down to the current task, or None."""
    for top in items:
        for unit in top.children:
            for task in unit.children:
                if CURRENT in task.marks:
                    return [top, unit, task]
    return None


def _fold(items: list[Item], depth: int, fold: str | None) -> str:
    """What a closed item's group says of the items it holds: with `fold`
    set to `names`, `<id> [<status>]` per item in the tree's order, the id
    whole at the top level and by its last segment under another item, a
    finding's kind in its status's place; else the counts."""
    if fold != "names":
        return _counts(items)
    return ", ".join(f"{item.id.rpartition('/')[2] if depth else item.id} [{_tag(item)}]"
                     for item in items)


def _counts(items: list[Item]) -> str:
    """`<n> <status>` per status in order, then `<n> kind: <kind>` per
    finding kind in the order it first shows, zeros left out."""
    tags = [_tag(item) for item in items]
    kinds = [tag for tag in dict.fromkeys(tags) if tag not in STATUSES]
    return ", ".join(f"{tags.count(tag)} {tag}"
                     for tag in [*STATUSES, *kinds] if tag in tags)


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


def forget(cache: dict[str, G0Reading], before: dict, after: dict) -> None:
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


def _key(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def main_tree(args) -> int:
    """The whole tree on stdout; each unreadable source as one line on stderr.

    An unreadable file never stops the print: the rest of the tree is still
    the product, so the command exits 0 and names the file it skipped.
    With `--follow`, the interactive pane instead, or without the pane
    extra one install line and exit 2. With an id, the query: one block
    per item with that id, then the unreadable sources, exit 0; an unknown
    id prints one line and exits 2, as does an id with `--follow`.
    """
    node = getattr(args, "node", None)
    if node is not None and getattr(args, "follow", False):
        print("taskcontract tree: --follow takes no id - give the id or --follow, not both",
              file=sys.stderr)
        return 2
    if getattr(args, "follow", False):
        try:
            from . import pane as interactive  # Textual, the pane extra
        except ImportError:
            print("taskcontract tree: --follow needs the pane extra"
                  " - pip install 'sdlc-taskcontract[pane]'", file=sys.stderr)
            return 2
        return interactive.run(Path(args.root))
    items, problems = build(Path(args.root))
    if node is None:
        sys.stdout.write(render(items))
    else:
        found = _matches(items, node)
        if not found:
            print(_no_node(_flat(node)), file=sys.stderr)
            return 2
        sys.stdout.write("\n".join(block(Path(args.root), item) for item in found))
    for problem in problems:
        print(f"taskcontract tree: {problem}", file=sys.stderr)
    return 0
