"""`taskcontract tree` - print the derived tree (ADR 0031).

One item per line, two spaces of indent per level. The line opens on the
item's full id, the node path ADR 0031 gives it, so the print states every
id whole. Then the status in brackets, or a finding's kind in its place,
then the item's marks (`inactive` on a gate a finding names that is not
active, `current` on the current task), then its evidence (on a `G0`
verdict, the validator command and the `HEAD` it read). Then its links
(`depends_on: <contract>/<unit>` on a unit, `gate: <value>` on a finding),
then a contract's feature doc reference (`doc: docs/features/<id>.md`), and
last its summary after ` | `. Each part but the id and status prints only
when the item has it, after exactly one space.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .tree import Item, build

INDENT = "  "


def render(items: list[Item]) -> str:
    """The tree as text, one line per item, byte-identical across runs."""
    lines: list[str] = []

    def walk(item: Item, depth: int) -> None:
        tag = f"kind: {item.kind}" if item.level == "finding" else item.status
        marks = "".join(f" {mark}" for mark in item.marks)
        evidence = f" {item.evidence}" if item.evidence else ""
        links = "".join(f" {link}" for link in item.links)
        doc = f" doc: {item.doc}" if item.doc else ""
        summary = f" | {item.summary}" if item.summary else ""
        lines.append(f"{INDENT * depth}{item.id} [{tag}]{marks}{evidence}"
                     f"{links}{doc}{summary}")
        for child in item.children:
            walk(child, depth + 1)

    for item in items:
        walk(item, 0)
    return "".join(line + "\n" for line in lines)


def main_tree(args) -> int:
    """The whole tree on stdout; each unreadable source as one line on stderr.

    An unreadable file never stops the print: the rest of the tree is still
    the product, so the command exits 0 and names the file it skipped.
    """
    items, problems = build(Path(args.root))
    sys.stdout.write(render(items))
    for problem in problems:
        print(f"taskcontract tree: {problem}", file=sys.stderr)
    return 0
