"""`taskcontract tree --follow` - the interactive pane (ADR 0031).

The only module that imports Textual, the `pane` extra; `taskcontract tree
--follow` imports it only when it runs. The pane holds, top to bottom: the
waiting line, when the current task is `approve-tests` or `approve-commit`;
the outline; the lines 0.15.0's pane printed on stderr, each whole; and the
cursor line.

The outline holds every line `taskcontract tree` prints, in its order and
nested as it indents them: each item, and each condition's diagnostics as
leaves right under it, before its child items. An item's label opens on its
full id at the top level and on the last segment of its id below it, then
its plain name and the parts `tree: pane: parts:` selects; the current
task's label carries `current` whatever the parts. A label is plain text,
never markup, so `[to do]` keeps its brackets. The pane opens with each
contract open down to its units and every other item closed; a current task
opens its unit too, and the cursor starts on it with the window scrolled to
it, else on the first line.

A plain name that would push the status, and on the current task `current`,
past the outline's right edge is cut where they still fit, ending in `...`;
a cut keeps `current` right after the status, and the other parts after
the status are then left off, since they would lie past the edge. The cursor
line shows the item at the cursor: its reference, the one `taskcontract tree
<id>` prints, then ` | ` and its plain name whole; the reference alone when
it has no plain name, its id when it has neither, and on a diagnostic the
message alone. The pane writes no file and nothing on stderr.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Static, Tree
from textual.widgets.tree import TreeNode

from . import tree
from .tree import APPROVALS, CURRENT, Item, build
from .tree_view import _flat, _path, line

TOGGLE = 2  # the cells Textual's open or closed icon takes before a label


@dataclass(frozen=True)
class Row:
    """What one outline node shows: an item, or with `message` set, one of
    its diagnostics; `depth` counts the levels above it."""

    item: Item
    depth: int
    message: str | None = None


def label(item: Item, depth: int, parts: list[str] | None = None,
          room: int | None = None) -> str:
    """An item's outline label: its line with the id's last segment below
    the top level, `current` kept on the current task whatever `parts`
    picks. With `room`, the cells the label may take, a plain name that
    would push the status and `current` past them is cut to end in `...`
    with the status, then `current`, last."""
    picked = parts if parts is None or CURRENT not in item.marks else [*parts, "marks"]
    short = _flat(item.id.rpartition("/")[2] if depth else item.id)
    text = short + line(item, picked)[len(_flat(item.id)):]
    if room is None or not item.name:
        return text
    name = _flat(item.name)
    tag = f"kind: {item.kind}" if item.level == "finding" else item.status
    status = f" [{tag}]" if parts is None or "status" in parts else ""
    kept = status + (f" {CURRENT}" if CURRENT in item.marks else "")
    if len(short) + 1 + len(name) + len(kept) <= room:
        return text
    keep = max(room - len(short) - 1 - len(kept) - 3, 0)
    return f"{short} {name[:keep]}...{kept}"


def cursor_text(root: Path, row: Row) -> str:
    """The cursor line for one node: the reference and the plain name, the
    reference alone, or the id; on a diagnostic, its message."""
    if row.message is not None:
        return row.message
    item = row.item
    if item.level == "contract" and item.doc:
        reference = f"{item.doc}:1"
    elif item.level in ("gate", "verdict", "condition", "task"):
        reference = item.page
    else:
        reference = tree.reference(root, item)
    shown = [text for text in (reference, _flat(item.name) if item.name else None) if text]
    return " | ".join(shown) or _flat(item.id)


class Outline(Tree):
    """The tree as a Textual Tree: labels as plain text, cut to the width
    they get once the layout gives one."""

    def __init__(self, parts: list[str] | None = None, **kwargs) -> None:
        super().__init__("", **kwargs)
        self.show_root = False
        self.parts = parts
        self.fitted: int | None = None  # the width the labels were cut to

    def process_label(self, label) -> Text:
        return Text(label) if isinstance(label, str) else label

    def fit(self) -> None:
        """Cut each item's label to the width it now gets, once per width."""
        width = self.scrollable_content_region.width
        if width <= 0 or width == self.fitted:
            return
        self.fitted = width
        for node in _nodes(self.root):
            row = node.data
            if row is None or row.message is not None:
                continue
            room = (width - row.depth * self.guide_depth
                    - (TOGGLE if node.allow_expand else 0))
            text = label(row.item, row.depth, self.parts, room)
            if text != node.label.plain:
                node.set_label(text)
        self._invalidate()  # line widths changed with the labels

    def on_resize(self) -> None:
        self.call_after_refresh(self.fit)
        self.call_after_refresh(self.follow_cursor)

    def watch_show_vertical_scrollbar(self) -> None:
        self.call_after_refresh(self.fit)

    def follow_cursor(self) -> None:
        """Scroll the cursor's line back into the window."""
        if self.cursor_node is not None:
            self.scroll_to_node(self.cursor_node, animate=False)


class PaneApp(App):
    """The pane on the repository at `root`, built once on mount."""

    CSS = """
    #outline { height: 1fr; overflow-x: hidden; }
    #waiting, #reported, #cursor { height: auto; }
    """

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root
        self.current: TreeNode | None = None

    def compose(self) -> ComposeResult:
        yield Static("", id="waiting", markup=False)
        yield Outline(id="outline")
        yield Static("", id="reported", markup=False)
        yield Static("", id="cursor", markup=False)

    def on_mount(self) -> None:
        items, problems = build(self.root)
        settings = tree.pane_settings(self.root, problems)
        outline = self.query_one(Outline)
        outline.parts = settings.get("parts")
        path = _path(items)
        self.current = _grow(outline.root, items, 0, outline.parts,
                             path[-1] if path else None)
        waiting = self.query_one("#waiting", Static)
        unit, _, key = path[-1].id.rpartition("/") if path else ("", "", "")
        waiting.display = key in APPROVALS
        waiting.update(f"waiting on a seat: {key} for {unit}" if waiting.display else "")
        reported = self.query_one("#reported", Static)
        reported.update("\n".join(f"taskcontract tree: {problem}" for problem in problems))
        reported.display = bool(problems)
        outline.focus()
        self.call_after_refresh(self.start)

    def start(self) -> None:
        """Put the cursor on the current task, the window on it, else on the
        first line."""
        outline = self.query_one(Outline)
        outline.fit()
        if self.current is not None:
            outline.move_cursor(self.current)
        else:
            outline.cursor_line = 0

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        row = event.node.data
        self.query_one("#cursor", Static).update(
            cursor_text(self.root, row) if row is not None else "")


def _grow(node: TreeNode, items: list[Item], depth: int, parts: list[str] | None,
          current: Item | None) -> TreeNode | None:
    """Add each item under `node` with its diagnostics and children, a
    contract open, and the current task's unit open; the current task's
    node, when it is under `node`."""
    found = None
    for item in items:
        text = label(item, depth, parts)
        row = Row(item, depth)
        if item.diagnostics or item.children:
            opened = ((depth == 0 and not item.id.startswith("gates/"))
                      or any(child is current for child in item.children))
            child = node.add(text, row, expand=opened)
        else:
            child = node.add_leaf(text, row)
        if item is current:
            found = child
        for message in item.diagnostics:
            child.add_leaf(f"- {message}", Row(item, depth + 1, message))
        found = _grow(child, item.children, depth + 1, parts, current) or found
    return found


def _nodes(node: TreeNode):
    """Every node under `node`, in outline order."""
    for child in node.children:
        yield child
        yield from _nodes(child)


def run(root: Path) -> int:
    """Run the pane until it ends; its exit code, 0 on a normal end."""
    app = PaneApp(root)
    app.run()
    return app.return_code or 0
