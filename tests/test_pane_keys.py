"""The pane's keys suite (contract project-tree, unit o6-pane-keys, SC4.2).

`taskcontract tree --follow` runs `taskcontract.pane.PaneApp(root)`, whose
outline (`#outline`, a Textual Tree) holds every line `taskcontract tree`
prints (unit o5-pane-outline). This suite pins how the outline answers the
keys, the pointer and the wheel, and what a closed item's line shows:

- Up and Down move the cursor one line. Right opens the item at the cursor
  and Left closes it; on an item that holds nothing, or one already open or
  closed, they change nothing. A click opens or closes the item it lands on
  and puts the cursor there. The wheel scrolls the window and leaves the
  cursor where it is.
- A closed item's line shows what it holds, in parentheses right after its
  status: `(<n> items: <counts>)`, `<n>` the items it holds and the counts
  by status in the six statuses' order, zeros left out; under `tree: pane:
  fold: names`, `(<n> items: <id> [<status>], ...)`, each id as its own line
  opens (the last segment). A closed condition counts its diagnostics,
  `(<n> diagnostics)`. One item reads `(1 items: ...)`. An open item and an
  item that holds nothing show no parentheses; opening an item drops them
  and closing it adds them back. When `tree: pane: parts:` leaves the status
  out, the parentheses follow the plain name. A bad `fold:` value keeps the
  counts.
- A plain name that would push the status and the parentheses past the
  outline's right edge is cut where they still fit, ending in `...`.

Each test drives the app headless through `App.run_test()` inside
`asyncio.run`, at a fixed terminal size, against a fixture repo under
tmp_path, outside any git repository. Keys go through `pilot.press`, clicks
through `pilot.click` on `#outline` at the cell of the line's row, and the
wheel as `MouseScrollUp` events posted at the outline the way the pilot
posts its own mouse events.
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main
from taskcontract.tree import STATUSES, build

SIZE = (80, 24)   # the terminal a test runs at unless it names another
WIDE = (240, 60)  # wide enough that no line of the fixture is cut
WIDEST = (400, 60)  # the same under `fold: names`, whose parentheses run long

TITLE = "Apply one discount code per order"
INTENT = "A fixture contract for the pane suite."
PIN = "The stale-pin finding, in its own words."
LONG_HEAD = "the work for a3-long is done when every discount code a customer types"
LONG_TAIL = ("at checkout is checked against the list, applied once, and shown on the "
             "receipt beside the total it changed")
LONG = f"{LONG_HEAD} {LONG_TAIL}"  # the plain name: its source's line break read as one space
MARKUP = "verify [bold]brackets[/bold] stay text (SC1.2)"
TASKS = ("approve-tests", "write-tests", "prove-red", "green", "approve-commit", "commit",
         "two-key")

ALPHA = f"""\
# alpha: the keys suite's fixture contract, written by hand.
id: alpha
title: {TITLE}
intent: {INTENT}
scope: [src/]
non_goals: [No other work]
dependencies: []
entities: []
provenance: {{origin: human-request}}
decomposition:
  - unit: work for a1-core
    id: a1-core
    confirmed_by: [user]
    done_means: the work for a1-core is done
    acceptance_sketch:
      - verify the core prints (SC1.1)
      - "{MARKUP}"
  - unit: work for a2-edges
    id: a2-edges
    depends_on: [a1-core]
    confirmed_by: [user]
    done_means: the work for a2-edges is done
    acceptance_sketch:
      - verify an edge holds
  - unit: work for a3-long
    id: a3-long
    confirmed_by: [user]
    done_means: |-
      {LONG_HEAD}
      {LONG_TAIL}
    acceptance_sketch:
      - verify it holds
"""

# beta: no title, no feature document, and no `entities`, so its G0.2 reads
# `to do` with one diagnostic (TC017).
BETA = {
    "id": "beta", "intent": "A second fixture contract.", "scope": ["src/"],
    "non_goals": ["No other work"],
    "decomposition": [{"unit": "work for b1-solo", "id": "b1-solo", "confirmed_by": ["user"],
                       "done_means": "the work for b1-solo is done",
                       "acceptance_sketch": ["verify the price rounds"]}],
    "dependencies": [], "provenance": {"origin": "human-request"},
}

# The lines the fixture's items open with, as the outline shows them.
A1 = "a1-core the work for a1-core is done [to do]"
A2 = "a2-edges the work for a2-edges is done [to do]"
A2_LINKS = " depends_on: alpha/a1-core"
ALPHA_HEAD = f"alpha {TITLE} [failed]"
ALPHA_TAIL = f' no "Ready:" row doc: docs/features/alpha.md | {INTENT}'
G0_HEAD = "G0 Planning / Intake [failed]"
G0_TAIL = " via python -m taskcontract validate specs/alpha/contract.yaml --profile ready at no commit"
A1_NAMES = ", ".join([f"{task} [to do]" for task in TASKS] + ["SC1.1 [to do]", "SC1.2 [to do]"])


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root and find no git repo above the fixture."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))


# --- the fixture repository ---------------------------------------------------------

def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _config(root, gates=("G0",), **more):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates), **more})


def _finding(root, slug, gate, statement=None):
    doc = {"finding": slug, "date": "2026-09-26", "kit_pinned": "v0.15.0",
           "diagnostic": "none", "gate": gate, "kind": "gap", "count": 1, "proposal": "none"}
    if statement is not None:
        doc["statement"] = statement
    _dump(root / ".sdlc" / "findings" / f"{slug}.yaml", doc)


def _repo(tmp_path, **config):
    """G0 active; alpha (titled, with a feature doc, its G0 failed on G0.1) and
    beta (no title, no doc, its G0.2 to do with one diagnostic); a finding
    under G0 and a bare one under none, so `gates/none` holds one item."""
    root = tmp_path / "repo"
    _config(root, **config)
    write_seat_roster(root)
    _write(root / "specs" / "alpha" / "contract.yaml", ALPHA)
    _dump(root / "specs" / "beta" / "contract.yaml", BETA)
    _write(root / "docs" / "features" / "alpha.md", f"# alpha - {TITLE}\n")
    _finding(root, "stale-pin", "G0", PIN)
    _finding(root, "bare", "none")
    return root


def _pane_config(**pane):
    return {"tree": {"pane": pane}}


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


def _doing(item, clock="10:00"):
    return {"item": item, "state": "doing", "at": f"2026-09-26T{clock}:00Z", "head": "1a2b3c4"}


def _current(root, item="alpha/a2-edges/prove-red"):
    """Make `item` the current task: the only task doing."""
    _progress(root, item.split("/", 1)[0], _doing(item))
    return root


def _tall(tmp_path):
    """Fourteen contracts of three units, no gate active; the current task is
    the last contract's last unit's write-tests, far below the first window."""
    root = tmp_path / "tall"
    _config(root, gates=())
    write_seat_roster(root)
    units = [{"unit": f"work for u{n}", "id": f"u{n}", "confirmed_by": ["user"],
              "done_means": f"the work for u{n} is done",
              "acceptance_sketch": [f"verify part {n} holds (SC1.{n})"]} for n in (1, 2, 3)]
    for c in range(1, 15):
        _dump(root / "specs" / f"work-{c:02}" / "contract.yaml", {
            "id": f"work-{c:02}", "intent": "A tall fixture contract.", "scope": ["src/"],
            "non_goals": ["No other work"], "decomposition": units, "dependencies": [],
            "entities": [], "provenance": {"origin": "human-request"}})
    _progress(root, "work-14", _doing("work-14/u3/write-tests"))
    return root


# --- the CLI ------------------------------------------------------------------------------

def _printed(root, capsys):
    """The whole tree's stdout lines; the print exits 0."""
    try:
        code = main(["tree", "--root", str(root)])
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    out = capsys.readouterr().out
    assert code == 0
    return out.splitlines()


def _by_id(items):
    """Every item of the model by its id."""
    found = {}
    for item in items:
        found[item.id] = item
        found.update(_by_id(item.children))
    return found


def _counts(tags):
    """`<n> <status>` per status in the six statuses' order, zeros left out,
    then `<n> kind: <kind>` per finding kind in the order it first shows."""
    kinds = [tag for tag in dict.fromkeys(tags) if tag not in STATUSES]
    return ", ".join(f"{tags.count(tag)} {tag}"
                     for tag in [*STATUSES, *kinds] if tags.count(tag))


def _tag(item):
    """What an item's line shows in its status's place: a finding its kind."""
    return f"kind: {item.kind}" if item.level == "finding" else item.status


def _wanted(root, lines, fold=None):
    """(depth, closed label, open label, holds a finding) per printed line, as
    the outline should show it at WIDE, every part shown: an item under
    another item opening on the last segment of its id; an item that holds
    something gains, when closed, its parentheses right after its status.
    None for a closed label when the line holds nothing."""
    model = _by_id(build(root)[0])
    rows = []
    for line in lines:
        body = line.lstrip(" ")
        rows.append(((len(line) - len(body)) // 2, body))
    wanted = []
    for n, (depth, body) in enumerate(rows):
        if body.startswith("- "):
            wanted.append((depth, None, body, False))
            continue
        rid = body.split(" ", 1)[0]
        shown = (rid.rsplit("/", 1)[-1] if depth else rid) + body[len(rid):]
        under = []
        for later_depth, later in rows[n + 1:]:
            if later_depth <= depth:
                break
            if later_depth == depth + 1:
                under.append(later)
        if not under:
            wanted.append((depth, None, shown, False))
            continue
        item = model[rid]
        if under[0].startswith("- "):
            held = f"({len(under)} diagnostics)"
            finding = False
        else:
            kids = [model[text.split(" ", 1)[0]] for text in under]
            finding = any(kid.level == "finding" for kid in kids)
            if fold == "names":
                what = ", ".join(f"{kid.id.rsplit('/', 1)[-1]} [{_tag(kid)}]" for kid in kids)
            else:
                what = _counts([_tag(kid) for kid in kids])
            held = f"({len(kids)} items: {what})"
        head = (rid.rsplit("/", 1)[-1] if depth else rid) + (f" {item.name}" if item.name else "")
        head += f" [{item.status}]"
        assert shown.startswith(head), (shown, head)
        wanted.append((depth, f"{head} {held}{shown[len(head):]}", shown, finding))
    return wanted


# --- driving the pane -----------------------------------------------------------------------

def _pane_module():
    assert importlib.util.find_spec("taskcontract.pane") is not None, (
        "taskcontract/pane.py does not exist: there is no interactive pane")
    return importlib.import_module("taskcontract.pane")


async def _settle(pilot):
    for _ in range(3):
        await pilot.pause()
        await pilot.wait_for_scheduled_animations()
    await pilot.pause()


def _drive(root, script, size=SIZE):
    """Run PaneApp(root) headless at `size`, let it settle, and return what
    `await script(app, pilot)` returns."""
    pane = _pane_module()

    async def go():
        app = pane.PaneApp(Path(root))
        async with app.run_test(size=size) as pilot:
            await _settle(pilot)
            return await script(app, pilot)

    return asyncio.run(go())


def _outline(app):
    return app.query_one("#outline")


def _label(node):
    return node.label.plain


def _walk(node, depth=0):
    """(depth, node) for every node under `node`, open or closed, in order."""
    for child in node.children:
        yield depth, child
        yield from _walk(child, depth + 1)


def _text(app, selector):
    """What a widget shows as plain text, or None when it is not displayed."""
    found = app.query(selector)
    if not found:
        return None
    widget = found.first()
    if not widget.display:
        return None
    shown = widget.render()
    return shown.plain if hasattr(shown, "plain") else str(shown)


def _node(app, rid):
    """The outline's node for the item id `rid`: the top-level node whose
    label opens on the id's head, then each child whose label opens on the
    next segment."""
    tree = _outline(app)
    for top in tree.root.children:
        head = _label(top).split(" ", 1)[0]
        if rid == head or rid.startswith(head + "/"):
            node = top
            rest = rid[len(head) + 1:]
            for segment in rest.split("/") if rest else []:
                found = [child for child in node.children
                         if _label(child).split(" ", 1)[0] == segment]
                assert len(found) == 1, (rid, segment, [_label(c) for c in node.children])
                node = found[0]
            return node
    raise AssertionError(f"no top-level line opens {rid!r}")


def _shot(app):
    """What the pane shows, as plain data."""
    tree = _outline(app)
    region = tree.scrollable_content_region
    return {
        "nodes": [(depth, _label(node), node.is_expanded and bool(node.children))
                  for depth, node in _walk(tree.root)],
        "lines": [_label(tree.get_node_at_line(n)) for n in range(tree.last_line + 1)],
        "top": tree.scroll_offset.y,
        "height": region.height,
        "width": region.width,
        "rows": [tree.render_line(y).text[:region.width] for y in range(region.height)],
        "cursor": tree.cursor_line,
        "cursor_label": _label(tree.cursor_node) if tree.cursor_node is not None else None,
        "cursor_text": _text(app, "#cursor"),
    }


def _is_open(shot, opening):
    """Whether the one node whose label opens with `opening` is open."""
    found = [expanded for _, text, expanded in shot["nodes"] if text.startswith(opening)]
    assert len(found) == 1, (opening, found)
    return found[0]


async def _just_shot(app, pilot):
    return _shot(app)


def _open(root, size=WIDE):
    """The pane as it opens."""
    return _drive(root, _just_shot, size)


async def _press(pilot, *keys):
    for key in keys:
        await pilot.press(key)
        await _settle(pilot)


async def _put(app, pilot, rid):
    """Open every item above `rid`'s node and move the cursor onto it."""
    node = _node(app, rid)
    up = node.parent
    while up is not None and up.parent is not None:
        up.expand()
        up = up.parent
    await _settle(pilot)
    _outline(app).move_cursor(node)
    await _settle(pilot)
    return node


def _row_of(app, node):
    """The window row, from the outline's top, that shows `node`'s line."""
    tree = _outline(app)
    line = node.line
    assert line >= 0, f"not shown: {_label(node)!r}"
    row = line - tree.scroll_offset.y
    assert 0 <= row < tree.scrollable_content_region.height, f"out of the window: {_label(node)!r}"
    return row


def _cell(app, row, column):
    """The click offset, from the outline's own origin, of a cell of the window."""
    tree = _outline(app)
    content, region = tree.scrollable_content_region, tree.region
    return (content.x - region.x + column, content.y - region.y + row)


async def _click(app, pilot, node, on_icon):
    """Click `node`'s line: on its open or closed icon, else on its label."""
    tree = _outline(app)
    row = _row_of(app, node)
    text = tree.render_line(row).text
    label = _label(node)
    start = text.index(label[:12])
    column = start - 2 if on_icon else start + 2
    if on_icon:
        assert text[column] in (tree.ICON_NODE[0], tree.ICON_NODE_EXPANDED[0]), text
    assert await pilot.click("#outline", offset=_cell(app, row, column))
    await _settle(pilot)


async def _wheel_up(app, pilot, times):
    """Turn the wheel up `times` notches with the pointer over the outline."""
    from textual import events
    for _ in range(times):
        await pilot._post_mouse_events([events.MouseScrollUp], widget="#outline",
                                       offset=_cell(app, 3, 10))
        await _settle(pilot)


# --- SC4.2 the keys ---------------------------------------------------------------------------

def test_sc4_2_up_and_down_move_the_cursor_one_line_through_what_right_opened(tmp_path):
    """Up and Down step one line at a time, into the lines an item opened by
    Right now shows."""
    root = _repo(tmp_path)

    async def script(app, pilot):
        seen = [_shot(app)]
        for key in ("down",) * 5 + ("right", "down", "down", "up", "up", "up"):
            await _press(pilot, key)
            seen.append(_shot(app))
        return seen

    seen = _drive(root, script, WIDE)
    assert [shot["cursor"] for shot in seen] == [0, 1, 2, 3, 4, 5, 5, 6, 7, 6, 5, 4]
    assert seen[5]["cursor_label"].startswith("a1-core ")
    assert seen[6]["cursor_label"] == A1, "Right changes no line's position but the cursor's item"
    assert seen[7]["cursor_label"] == "approve-tests Approve the test list [to do]", (
        "Down after Right lands on the first item the opened unit holds")
    assert seen[8]["cursor_label"] == "write-tests Write the tests [to do]"
    assert seen[10]["cursor_label"] == A1
    assert seen[11]["cursor_label"].startswith("G1 Requirements / Spec [to do]")


def test_sc4_2_right_opens_the_closed_item_at_the_cursor_and_else_changes_nothing(tmp_path):
    """Right opens a closed item; pressed on an open item or an item that
    holds nothing, it changes nothing."""
    root = _repo(tmp_path)

    async def script(app, pilot):
        await _put(app, pilot, "alpha/a1-core")
        closed = _shot(app)
        await _press(pilot, "right")
        opened = _shot(app)
        await _press(pilot, "right")
        again = _shot(app)
        await _put(app, pilot, "alpha/a1-core/green")
        leaf = _shot(app)
        await _press(pilot, "right")
        return closed, opened, again, leaf, _shot(app)

    closed, opened, again, leaf, leaf_after = _drive(root, script, WIDE)
    unit = closed["lines"].index(closed["cursor_label"])
    assert closed["cursor"] == unit and not _is_open(closed, "a1-core ")
    assert _is_open(opened, "a1-core "), "Right opens the item at the cursor"
    assert (1, A1, True) in opened["nodes"]
    assert [line.split(" ", 1)[0] for line in opened["lines"][unit + 1:unit + 10]] == [
        *TASKS, "SC1.1", "SC1.2"]
    assert opened["cursor"] == unit, "the cursor stays on the item Right opened"
    assert again == opened, "Right on an open item changes nothing"
    assert leaf_after == leaf, "Right on an item that holds nothing changes nothing"


def test_sc4_2_left_closes_the_open_item_at_the_cursor_and_else_changes_nothing(tmp_path):
    """Left closes an open item; pressed on an item that holds nothing, or on
    a closed item, it changes nothing: it never moves to the item above."""
    root = _current(_repo(tmp_path))

    async def script(app, pilot):
        start = _shot(app)
        await _press(pilot, "left")
        on_leaf = _shot(app)
        await _press(pilot, "up", "up", "up")
        on_unit = _shot(app)
        await _press(pilot, "left")
        closed = _shot(app)
        await _press(pilot, "left")
        return start, on_leaf, on_unit, closed, _shot(app)

    start, on_leaf, on_unit, closed, again = _drive(root, script, WIDE)
    assert start["cursor_label"] == "prove-red Prove red [doing] current"
    assert on_leaf == start, "Left on an item that holds nothing changes nothing"
    assert on_unit["cursor_label"] == A2.replace("[to do]", "[doing]") + A2_LINKS
    assert (1, on_unit["cursor_label"], True) in on_unit["nodes"]
    assert not _is_open(closed, "a2-edges "), "Left closes the item at the cursor"
    assert (1, A2.replace("[to do]", "[doing]") + " (8 items: 7 to do, 1 doing)" + A2_LINKS,
            False) in closed["nodes"], "Left closes the item at the cursor"
    assert closed["cursor"] == on_unit["cursor"], "the cursor stays on the item Left closed"
    assert len(closed["lines"]) == len(on_unit["lines"]) - 8
    assert again == closed, "Left on a closed item changes nothing"


# --- SC4.2 the pointer and the wheel -----------------------------------------------------------

def test_sc4_2_a_click_opens_or_closes_the_item_it_lands_on_and_puts_the_cursor_there(tmp_path):
    """A click on an item's line, on its icon or on its text, flips it open or
    closed and moves the cursor onto it; a click on an item that holds nothing
    only moves the cursor."""
    root = _repo(tmp_path)

    async def script(app, pilot):
        start = _shot(app)
        await _click(app, pilot, _node(app, "alpha/a1-core"), on_icon=True)
        icon_open = _shot(app)
        await _click(app, pilot, _node(app, "alpha/a1-core"), on_icon=False)
        text_closed = _shot(app)
        await _click(app, pilot, _node(app, "alpha/a2-edges"), on_icon=False)
        text_open = _shot(app)
        await _click(app, pilot, _node(app, "alpha/a2-edges"), on_icon=True)
        icon_closed = _shot(app)
        await _click(app, pilot, _node(app, "alpha/G1"), on_icon=True)
        g1_open = _node(app, "alpha/G1").is_expanded
        await _click(app, pilot, _node(app, "alpha/G1/G1.2"), on_icon=False)
        return (start, icon_open, text_closed, text_open, icon_closed, g1_open, _shot(app),
                _node(app, "alpha/G1").is_expanded)

    (start, icon_open, text_closed, text_open, icon_closed, g1_open, leaf,
     g1_still) = _drive(root, script, WIDE)
    assert start["cursor"] == 0
    a1 = [line.startswith("a1-core ") for line in start["lines"]].index(True)
    assert _is_open(icon_open, "a1-core "), "a click on the icon opens the item"
    assert icon_open["cursor"] == a1 and icon_open["cursor_label"] == A1, (
        "a click on the icon puts the cursor on the item it opened")
    assert not _is_open(text_closed, "a1-core "), "a click on the text closes the open item"
    assert text_closed["cursor"] == a1
    assert _is_open(text_open, "a2-edges "), "a click on the text opens the closed item"
    assert text_open["cursor"] == a1 + 1 and text_open["cursor_label"] == A2 + A2_LINKS
    assert not _is_open(icon_closed, "a2-edges "), "a click on the icon closes the open item"
    assert icon_closed["cursor"] == a1 + 1, "the cursor stays on the item the click closed"
    assert leaf["cursor_label"] == "G1.2 Model checking [to do]", (
        "a click on an item that holds nothing puts the cursor there")
    assert g1_open and g1_still, "a click on an item that holds nothing closes nothing"
    assert (1, A1 + " (9 items: 9 to do)", False) in text_closed["nodes"]
    assert (1, A2 + " (8 items: 8 to do)" + A2_LINKS, False) in icon_closed["nodes"]


def test_sc4_2_the_wheel_scrolls_the_window_and_leaves_the_cursor_where_it_is(tmp_path):
    """The wheel steps the window up through the outline, each row the line at
    its place, closed lines with their parentheses; the cursor stays on the
    current task, out of the window, and the cursor line stays."""
    root = _tall(tmp_path)

    async def script(app, pilot):
        start = _shot(app)
        await _wheel_up(app, pilot, 4)
        return start, _shot(app)

    start, after = _drive(root, script, SIZE)
    assert start["cursor_label"] == "write-tests Write the tests [doing] current"
    assert after["top"] < start["top"], "the wheel scrolls the window"
    assert after["cursor"] == start["cursor"], "the wheel leaves the cursor where it is"
    assert after["cursor_label"] == start["cursor_label"]
    assert after["cursor_text"] == start["cursor_text"]
    assert not after["top"] <= after["cursor"] < after["top"] + after["height"], (
        "the window is not pulled back to the cursor")
    shown = after["lines"][after["top"]:after["top"] + after["height"]]
    for row, label in zip(after["rows"], shown):
        assert label in row, (row, label)
    units = [label for label in shown if label.startswith("u1 ")]
    assert units and all(label == "u1 the work for u1 is done [to do] (8 items: 8 to do)"
                         for label in units), shown


# --- SC4.2 a closed item's line ------------------------------------------------------------------

def test_sc4_2_a_closed_item_counts_what_it_holds_after_its_status(tmp_path, capsys):
    """Each closed line carries `(<n> items: <counts>)` right after its status,
    the counts by status in the six statuses' order, zeros left out; a closed
    condition `(<n> diagnostics)`; an open line and a line that holds nothing
    read as the tree prints them."""
    root = _repo(tmp_path)
    wanted = _wanted(root, _printed(root, capsys))
    shot = _open(root)
    assert len(shot["nodes"]) == len(wanted)
    for (depth, text, expanded), (want_depth, closed, opened, finding) in zip(shot["nodes"], wanted):
        assert depth == want_depth
        if closed is None or expanded:
            assert text == opened, "an open line, or a line that holds nothing, shows no parentheses"
        else:
            assert text == closed
    nodes = shot["nodes"]
    assert (1, A1 + " (9 items: 9 to do)", False) in nodes
    assert (1, G0_HEAD + " (3 items: 2 done, 1 failed)" + G0_TAIL, False) in nodes
    assert (2, "G0.2 Vocabulary coverage [to do] (1 diagnostics)", False) in nodes
    # a finding counts by what its own line shows in the status's place, its kind
    assert (0, "gates/G0 Planning / Intake [to do] (4 items: 3 to do, 1 kind: gap)",
            False) in nodes
    assert (0, "gates/none [to do] (1 items: 1 kind: gap)", False) in nodes


def test_sc4_2_opening_an_item_drops_its_parentheses_and_closing_it_adds_them_back(tmp_path):
    """Right on a closed condition shows its diagnostic and drops `(1
    diagnostics)`; Left brings them back; the same for a contract."""
    root = _repo(tmp_path)

    async def script(app, pilot):
        await _put(app, pilot, "beta/G0/G0.2")
        closed = _label(_node(app, "beta/G0/G0.2"))
        await _press(pilot, "right")
        opened = _label(_node(app, "beta/G0/G0.2"))
        shown = _shot(app)["lines"]
        await _press(pilot, "left")
        again = _label(_node(app, "beta/G0/G0.2"))
        await _put(app, pilot, "alpha")
        top_open = _label(_node(app, "alpha"))
        await _press(pilot, "left")
        top_closed = _label(_node(app, "alpha"))
        await _press(pilot, "right")
        return closed, opened, shown, again, top_open, top_closed, _label(_node(app, "alpha"))

    closed, opened, shown, again, top_open, top_closed, top_reopened = _drive(root, script, WIDE)
    assert closed == "G0.2 Vocabulary coverage [to do] (1 diagnostics)"
    assert opened == "G0.2 Vocabulary coverage [to do]"
    assert shown[shown.index(opened) + 1].startswith("- contract declares no entities")
    assert again == closed
    assert top_open == ALPHA_HEAD + ALPHA_TAIL
    assert top_closed == ALPHA_HEAD + " (5 items: 4 to do, 1 failed)" + ALPHA_TAIL
    assert top_reopened == top_open


def test_sc4_2_under_fold_names_a_closed_item_names_what_it_holds(tmp_path, capsys):
    """`fold: names` names each held item as `<id> [<status>]`, the id by its
    last segment, joined by `, `; a closed condition still counts its
    diagnostics."""
    root = _repo(tmp_path, **_pane_config(fold="names"))
    wanted = _wanted(root, _printed(root, capsys), fold="names")
    shot = _open(root, WIDEST)
    for (depth, text, expanded), (_, closed, opened, finding) in zip(shot["nodes"], wanted):
        if closed is not None and not expanded:
            assert text == closed
    nodes = shot["nodes"]
    assert (0, "gates/none [to do] (1 items: bare [kind: gap])", False) in nodes
    assert (1, f"{A1} (9 items: {A1_NAMES})", False) in nodes
    assert (1, G0_HEAD + " (3 items: G0.1 [failed], G0.2 [done], G0.3 [done])" + G0_TAIL,
            False) in nodes
    assert (2, "G0.2 Vocabulary coverage [to do] (1 diagnostics)", False) in nodes


def test_sc4_2_a_bad_fold_value_keeps_the_counts(tmp_path):
    """Any `fold:` value but `names` counts, as unset does."""
    root = _repo(tmp_path, **_pane_config(fold="sideways"))
    nodes = _open(root)["nodes"]
    assert (1, A1 + " (9 items: 9 to do)", False) in nodes
    assert (1, G0_HEAD + " (3 items: 2 done, 1 failed)" + G0_TAIL, False) in nodes


@pytest.mark.parametrize("parts", [[], ["marks"], ["marks", "evidence", "links"]])
def test_sc4_2_without_the_status_the_parentheses_follow_the_plain_name(tmp_path, parts):
    """When `parts:` leaves the status out, a closed line's parentheses come
    right after its plain name, before the parts it keeps."""
    root = _repo(tmp_path, **_pane_config(parts=parts))
    nodes = _open(root)["nodes"]
    marks = "marks" in parts
    assert (1, "a1-core the work for a1-core is done (9 items: 9 to do)", False) in nodes
    links = A2_LINKS if "links" in parts else ""
    assert (1, "a2-edges the work for a2-edges is done (8 items: 8 to do)" + links,
            False) in nodes
    evidence = G0_TAIL if "evidence" in parts else ""
    assert (1, "G0 Planning / Intake (3 items: 2 done, 1 failed)" + evidence, False) in nodes
    inactive = " inactive" if marks else ""
    assert (1, "G1 Requirements / Spec (3 items: 3 to do)" + inactive, False) in nodes


# --- SC4.2 the cut keeps the parentheses ---------------------------------------------------------

def test_sc4_2_a_cut_plain_name_keeps_the_status_and_the_parentheses_in_view(tmp_path):
    """At 80 columns a3-long's plain name is cut where its status and its
    parentheses still fit, ending in `...`; opened, the parentheses go and the
    name is cut where the status alone still fits."""
    root = _repo(tmp_path)

    async def script(app, pilot):
        await _put(app, pilot, "alpha/a3-long")
        closed = _shot(app)
        await _press(pilot, "right")
        return closed, _shot(app)

    closed, opened = _drive(root, script, SIZE)
    room = closed["width"] - 1 * 4 - 2  # the unit's depth of guides, then its icon

    def cut(kept):
        keep = room - len("a3-long") - 1 - len(kept) - 3
        return f"a3-long {LONG[:keep]}...{kept}"

    held = " [to do] (8 items: 8 to do)"
    assert closed["cursor_label"] == cut(held)
    assert len(closed["cursor_label"]) == room
    row = closed["rows"][closed["cursor"] - closed["top"]]
    assert row.rstrip().endswith("..." + held), row
    assert opened["cursor_label"] == cut(" [to do]")
