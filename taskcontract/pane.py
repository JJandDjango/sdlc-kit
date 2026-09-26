"""`taskcontract tree --follow` - the interactive pane (ADR 0031).

The only module that imports Textual, the `pane` extra; `taskcontract tree
--follow` imports it only when it runs. The pane holds, top to bottom: the
waiting line, `waiting on a seat: <approval> for <contract>/<unit>`, while
the current task is `approve-tests` or `approve-commit`; the outline; the
lines the pane reports, each whole; and the cursor line.

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

A closed item that holds something shows it in a group right after its
status, or after its plain name when `parts:` leaves the status out:
`(<n> items: <counts>)`, the items one level below it counted by status
(a finding by its kind), or under `tree: pane: fold: names` each named as
`<id> [<status>]`; a closed condition with diagnostics reads `(<k>
diagnostics)`. An open item shows no group, so opening an item drops it
and closing the item adds it back.

A plain name that would push the status, the group, and on the current task
`current`, past the outline's right edge is cut where they still fit,
ending in `...`, those three kept in that order; the other parts are then
left off, since they would lie past the edge. The cursor line shows the
item at the cursor: its reference, the one `taskcontract tree <id>`
prints, then ` | ` and its plain name whole; the reference alone when it
has no plain name, its id when it has neither, and on a diagnostic the
message alone.

Up and Down move the cursor one line. Right opens the closed item at the
cursor and Left closes the open one; either leaves the cursor where it is,
and on a leaf, or an item already open or closed, changes nothing. A click
on a line, its icon or its text, puts the cursor there and opens or closes
the item once when it holds something. The wheel scrolls the window and
leaves the cursor where it is.

Every `interval` seconds the pane lists its sources, the files 0.15.0's
pane listed, and renders again only when one was added, removed or
changed. It keeps each `G0` reading until its contract or the vocabulary
changes. A render keeps every item open or closed as it was and the cursor
on the same item, each item known by its path from the root; an item new
to the tree opens as at the start, and when the item at the cursor is gone
the cursor moves to its nearest parent that remains. A render that moves
the current task to another task opens the items above it and scrolls it
into view, the cursor left where it was.

Each render replaces the reported lines: each unreadable source and a bad
`tree: pane:` key as `taskcontract tree: <problem>`. Each time a render
arrives at an approval, the first render included, the pane starts the
command set as `tree: notify:` through the shell at the root, with the
task's id in `SDLC_NODE`, and never waits on it; one that cannot start
reports `notify failed, exit 127: <command>` at once, and one found ended
nonzero at a later tick reports `notify failed, exit <code>: <command>`
after that tick's render, kept until the next render. Ctrl-C ends the
pane with exit 0 and leaves the commands it started running. The pane
writes no file and nothing on stderr.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Static, Tree
from textual.widgets.tree import TreeNode

from . import tree
from .tree import APPROVALS, CURRENT, G0Reading, Item, build
from .tree_view import _flat, _fold, _path, _tag, forget, line, scan

TOGGLE = 2  # the cells Textual's open or closed icon takes before a label


@dataclass(frozen=True)
class Row:
    """What one outline node shows: an item, or with `message` set, one of
    its diagnostics; `depth` counts the levels above it."""

    item: Item
    depth: int
    message: str | None = None


def label(item: Item, depth: int, parts: list[str] | None = None,
          room: int | None = None, group: str | None = None) -> str:
    """An item's outline label: its line with the id's last segment below
    the top level, `group` right after the status, `current` kept on the
    current task whatever `parts` picks. With `room`, the cells the label
    may take, a plain name that would push the status, the group and
    `current` past them is cut to end in `...` with those three last."""
    picked = parts if parts is None or CURRENT not in item.marks else [*parts, "marks"]
    short = _flat(item.id.rpartition("/")[2] if depth else item.id)
    text = short + line(item, picked)[len(_flat(item.id)):]
    status = f" [{_tag(item)}]" if parts is None or "status" in parts else ""
    held = f" {group}" if group else ""
    if held:  # after the status, or after the plain name when the status is left out
        at = len(short) + len(_flat(f" {item.name}") if item.name else "") + len(_flat(status))
        text = text[:at] + held + text[at:]
    if room is None or not item.name:
        return text
    name = _flat(item.name)
    kept = status + held + (f" {CURRENT}" if CURRENT in item.marks else "")
    if len(short) + 1 + len(name) + len(kept) <= room:
        return text
    keep = max(room - len(short) - 1 - len(kept) - 3, 0)
    return f"{short} {name[:keep]}...{kept}"


def group(item: Item, depth: int, fold: str | None) -> str:
    """What a closed item holds, in parentheses: a condition's diagnostics
    counted, else the items one level below it, counted by status or, with
    `fold` set to `names`, named."""
    if item.diagnostics:
        return f"({len(item.diagnostics)} diagnostics)"
    return f"({len(item.children)} items: {_fold(item.children, depth + 1, fold)})"


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
    """The tree as a Textual Tree: labels as plain text, each closed item's
    with its group, cut to the width they get once the layout gives one;
    Right opens the item at the cursor and Left closes it."""

    BINDINGS = [
        Binding("right", "open_item", "Open", show=False),
        Binding("left", "close_item", "Close", show=False),
    ]

    def __init__(self, parts: list[str] | None = None, **kwargs) -> None:
        super().__init__("", **kwargs)
        self.show_root = False
        self.parts = parts
        self.fold: str | None = None
        self.fitted: int | None = None  # the width the labels were cut to

    def process_label(self, label) -> Text:
        return Text(label) if isinstance(label, str) else label

    def text(self, row: Row, closed: bool) -> str:
        """A node's label: a diagnostic's line, else its item's label, with
        the group while it is closed, cut to the width last fitted."""
        if row.message is not None:
            return f"- {row.message}"
        held = bool(row.item.diagnostics or row.item.children)
        room = None if self.fitted is None else (
            self.fitted - row.depth * self.guide_depth - (TOGGLE if held else 0))
        return label(row.item, row.depth, self.parts, room,
                     group(row.item, row.depth, self.fold) if held and closed else None)

    def relabel(self, node: TreeNode) -> None:
        """Set a node's label afresh when it changed."""
        if node.data is not None:
            text = self.text(node.data, not node.is_expanded)
            if text != node.label.plain:
                node.set_label(text)

    def fit(self) -> None:
        """Cut each item's label to the width it now gets, once per width."""
        width = self.scrollable_content_region.width
        if width <= 0 or width == self.fitted:
            return
        self.fitted = width
        for node in _nodes(self.root):
            self.relabel(node)
        self._invalidate()  # line widths changed with the labels

    def put(self, node: TreeNode | None) -> None:
        """Put the cursor on `node`, else the first line, leaving the window
        where it is."""
        self._build()  # fresh nodes learn their lines
        self.cursor_line = node.line if node is not None else 0

    def on_resize(self) -> None:
        self.call_after_refresh(self.fit)
        self.call_after_refresh(self.follow_cursor)

    def watch_show_vertical_scrollbar(self) -> None:
        self.call_after_refresh(self.fit)

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        self.relabel(event.node)

    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        self.relabel(event.node)

    def on_click(self, event: events.Click) -> None:
        """A click on the open or closed icon puts the cursor on its line
        too; Tree's own handler, run next, flips the item once."""
        meta = event.style.meta
        if "line" in meta and meta.get("toggle", False):
            self.cursor_line = meta["line"]

    def action_open_item(self) -> None:
        node = self.cursor_node
        if node is not None and node.allow_expand and not node.is_expanded:
            node.expand()

    def action_close_item(self) -> None:
        node = self.cursor_node
        if node is not None and node.allow_expand and node.is_expanded:
            node.collapse()

    def follow_cursor(self) -> None:
        """Scroll the cursor's line back into the window."""
        if self.cursor_node is not None:
            self.scroll_to_node(self.cursor_node, animate=False)


class PaneApp(App):
    """The pane on the repository at `root`, rendered on mount and again
    at each tick, every `interval` seconds, that finds a source changed."""

    CSS = """
    #outline { height: 1fr; overflow-x: hidden; }
    #waiting, #reported, #cursor { height: auto; }
    """
    BINDINGS = [Binding("ctrl+c", "quit", "Quit", show=False, priority=True)]

    def __init__(self, root: Path, interval: float = 1.0) -> None:
        super().__init__()
        self.root = root
        self.interval = interval
        self.current: TreeNode | None = None  # the current task's node
        self.arrived: str | None = None  # the current task's id at the last render
        self.cache: dict[str, G0Reading] = {}
        self.seen: dict[str, tuple[int, int]] = {}
        self.running: list[tuple[subprocess.Popen, str]] = []
        self.problems: list[str] = []  # the last render's reported lines
        self.failed: list[str] = []  # notify failures since the last render

    def compose(self) -> ComposeResult:
        yield Static("", id="waiting", markup=False)
        yield Outline(id="outline")
        yield Static("", id="reported", markup=False)
        yield Static("", id="cursor", markup=False)

    def on_mount(self) -> None:
        self.seen = scan(self.root)
        self.draw()
        self.query_one(Outline).focus()
        self.set_interval(self.interval, self.check)
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

    def check(self) -> None:
        """One tick: render once when the sources changed since the last
        listing, then report each notify command that ended nonzero after
        that render's lines, so no render drops a failure unseen."""
        now = scan(self.root)
        if now != self.seen:
            forget(self.cache, self.seen, now)
            self.seen = now
            self.draw()
        still = []
        for run, command in self.running:
            code = run.poll()
            if code is None:
                still.append((run, command))
            elif code:
                self.failed.append(f"notify failed, exit {code}: {command}")
        ended = len(still) < len(self.running)
        self.running = still
        if ended:
            self.report()

    def draw(self) -> None:
        """Rebuild the outline, each item open or closed as it was and the
        cursor on the same item; the waiting line and the reported lines
        afresh; the notify command when the render arrived at an approval."""
        items, problems = build(self.root, self.cache)
        settings = tree.pane_settings(self.root, problems)
        outline = self.query_one(Outline)
        outline.parts, outline.fold = settings.get("parts"), settings.get("fold")
        path = _path(items)
        task = path[-1].id if path else None
        moved = task is not None and task != self.arrived
        before = _index(outline.root)
        at = next((key for key, node in before.items() if node is outline.cursor_node), None)
        outline.clear()
        self.current = _grow(outline, outline.root, items, 0, path[-1] if path else None,
                             {key: node.is_expanded for key, node in before.items()},
                             path[:-1] if moved else [])
        if at is not None:
            after = _index(outline.root)
            outline.put(next((after[at[:n]] for n in range(len(at), 0, -1)
                              if at[:n] in after), None))
            if moved and self.current is not None:
                outline.scroll_to_node(self.current, animate=False)
            self.point(outline.cursor_node)
        waiting = self.query_one("#waiting", Static)
        unit, _, key = task.rpartition("/") if task else ("", "", "")
        waiting.display = key in APPROVALS
        waiting.update(f"waiting on a seat: {key} for {unit}" if waiting.display else "")
        self.problems = [f"taskcontract tree: {problem}" for problem in problems]
        self.failed = []
        if moved and key in APPROVALS:
            self.start_notify(task)
        self.arrived = task
        self.report()

    def start_notify(self, task: str) -> None:
        """Start the `tree: notify:` command with the task's id in
        `SDLC_NODE`, never waiting on it; one that cannot start is reported
        with code 127."""
        command = tree.notify_command(self.root)
        if command is None:
            return
        try:
            run = subprocess.Popen(command, shell=True, cwd=self.root,
                                   env={**os.environ, "SDLC_NODE": task},
                                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        except OSError:
            self.failed.append(f"notify failed, exit 127: {command}")
            return
        self.running.append((run, command))

    def report(self) -> None:
        """Show the render's lines, then the notify failures since it."""
        reported = self.query_one("#reported", Static)
        lines = self.problems + self.failed
        reported.update("\n".join(lines))
        reported.display = bool(lines)

    def point(self, node: TreeNode | None) -> None:
        """Show the node at the cursor on the cursor line."""
        row = node.data if node is not None else None
        self.query_one("#cursor", Static).update(
            cursor_text(self.root, row) if row is not None else "")

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        self.point(event.node)


def _grow(outline: Outline, node: TreeNode, items: list[Item], depth: int,
          current: Item | None, state: dict[tuple, bool], opening: list[Item],
          above: tuple = ()) -> TreeNode | None:
    """Add each item under `node` with its diagnostics and children, open
    or closed as `state` holds it by its path, else a contract open and the
    current task's unit open; each of `opening` open whatever `state` holds.
    Returns the current task's node, when it is under `node`."""
    found = None
    seen: dict = {}
    for item in items:
        key = (*above, _step(item.id, seen))
        row = Row(item, depth)
        if item.diagnostics or item.children:
            opened = any(item is up for up in opening) or state.get(
                key, (depth == 0 and not item.id.startswith("gates/"))
                or any(child is current for child in item.children))
            child = node.add(outline.text(row, not opened), row, expand=opened)
        else:
            child = node.add_leaf(outline.text(row, True), row)
        if item is current:
            found = child
        for message in item.diagnostics:
            child.add_leaf(f"- {message}", Row(item, depth + 1, message))
        found = _grow(outline, child, item.children, depth + 1, current, state,
                      opening, key) or found
    return found


def _index(node: TreeNode, above: tuple = ()) -> dict[tuple, TreeNode]:
    """Every node under `node` by its path from the root: one (id, n) per
    level, n counting the earlier siblings with that id; a diagnostic by its
    message in the id's place."""
    found: dict[tuple, TreeNode] = {}
    seen: dict = {}
    for child in node.children:
        row = child.data
        key = (*above, _step(row.item.id if row.message is None else ("-", row.message), seen))
        found[key] = child
        found.update(_index(child, key))
    return found


def _step(ident, seen: dict) -> tuple:
    """One level of a path: `ident` and how many earlier siblings had it."""
    n = seen.get(ident, 0)
    seen[ident] = n + 1
    return (ident, n)


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
