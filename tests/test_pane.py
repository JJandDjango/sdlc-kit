"""The interactive pane suite (contract project-tree, unit o5-pane-outline).

With the pane extra, `taskcontract tree --follow` runs a Textual app,
`taskcontract.pane.PaneApp(root)`, through `taskcontract.pane.run(root)`.
The pane holds, top to bottom: the waiting line (`#waiting`) when the
current task is an approval; the outline (`#outline`, a Textual Tree); the
lines the pane reports (`#reported`), each line 0.15.0 printed on stderr at
a render, word for word; and the cursor line (`#cursor`). The app writes
nothing to stderr and no file (SC4.1).

The outline holds every line `taskcontract tree` prints, in its order: each
item, and each diagnostic under its condition. An item's line opens on its
full id at the top level and on the last segment of its id under another
item, then its plain name and the parts `tree: pane: parts:` selects; the
current task's line carries `current` whatever `parts:` selects. Labels are
plain text, never markup. The pane opens each feature (every contract) down
to its units and every other item closed; a current task also opens its own
unit. The cursor starts on the current task, with the window scrolled to
it, else on the first line. A plain name that would push the status past
the outline's right edge is cut where the status still fits, ending in
`...` (SC4.1).

The cursor line shows the item at the cursor: `<reference> | <plain name>`,
the name whole, the reference the one `taskcontract tree <id>` prints (a
feature's `doc:` value, else its `file:`; a unit's, a check's and a
finding's `file:`; a gate's, a verdict's, a condition's and a task's
`page:`). No plain name: the reference alone; neither: the id. On a
diagnostic: the diagnostic whole (SC1.2).

Without the extra, `--follow` prints one line on stderr and exits 2. Only
`taskcontract/pane.py` imports Textual, and only when `--follow` runs.

Each test drives the app headless through `App.run_test()` inside
`asyncio.run`, at a fixed terminal size (80 by 24 unless it says), against
a fixture repo under tmp_path, outside any git repository. A missing extra
is simulated by setting every `textual` entry of sys.modules to None and
dropping `taskcontract.pane` from sys.modules and from the package.
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import json
import os
import subprocess
import sys
import time
import tomllib
from pathlib import Path

import pytest
import yaml

import taskcontract
from conftest import write_seat_roster
from taskcontract import tree_view
from taskcontract.__main__ import main

KIT = Path(taskcontract.__file__).resolve().parent.parent
DATA = KIT / "taskcontract" / "data"

SIZE = (80, 24)   # the terminal every test runs at unless it names another
WIDE = (240, 60)  # wide enough that no line of the fixture is cut

TITLE = "Apply one discount code per order"
INTENT = "A fixture contract for the pane suite."
PIN = "The stale-pin finding, in its own words."
LONG_HEAD = "the work for a3-long is done when every discount code a customer types"
LONG_TAIL = ("at checkout is checked against the list, applied once, and shown on the "
             "receipt beside the total it changed")
LONG = f"{LONG_HEAD} {LONG_TAIL}"  # the plain name: its source's line break read as one space
MARKUP = "verify [bold]brackets[/bold] stay text (SC1.2)"
INSTALL = ("taskcontract tree: --follow needs the pane extra - pip install "
           "'sdlc-taskcontract[pane]'")
TAKES_NO_ID = "taskcontract tree: --follow takes no id - give the id or --follow, not both"
PARTS_IGNORED = ("taskcontract tree: pane parts ignored: shade - give a list from "
                 "id, status, marks, evidence, links, doc, summary")
FOLD_IGNORED = "taskcontract tree: pane fold ignored: sideways - give names or counts"
TEXTUAL_PIN = "textual>=8.2,<9"

ALPHA = f"""\
# alpha: the pane suite's fixture contract, written by hand so that each
# unit and each sketch starts on a line the tests can name.
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
    """G0 active; alpha (titled, ready-green, with a feature doc) and beta (no
    title, no doc, G0.2 to do); a finding under G0 and a bare one under none."""
    root = tmp_path / "repo"
    _config(root, **config)
    write_seat_roster(root)
    _write(root / "specs" / "alpha" / "contract.yaml", ALPHA)
    _dump(root / "specs" / "beta" / "contract.yaml", BETA)
    _write(root / "docs" / "features" / "alpha.md", f"# alpha - {TITLE}\n")
    _finding(root, "stale-pin", "G0", PIN)
    _finding(root, "bare", "none")
    return root


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


def _line_of(text, entry):
    """The 1-based line of `text` that is exactly `entry`, found once."""
    lines = text.splitlines()
    assert lines.count(entry) == 1, entry
    return lines.index(entry) + 1


def _pages(name):
    doc = yaml.safe_load((DATA / f"{name}.yaml").read_text(encoding="utf-8"))
    return {entry["id"]: (entry["name"], entry["page"]) for entry in doc[name]}


def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


# --- the CLI ------------------------------------------------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _printed(root, capsys):
    """The whole tree's stdout lines; the print exits 0."""
    code, out, _ = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    return out.splitlines()


def _expected_outline(lines):
    """(depth, label) per printed line, as the outline holds it: the indent
    read as the depth, an item under another item opening on the last segment
    of its id, a diagnostic as printed."""
    wanted = []
    for line in lines:
        body = line.lstrip(" ")
        depth = (len(line) - len(body)) // 2
        if depth and not body.startswith("- "):
            rid = body.split(" ", 1)[0]
            body = rid.rsplit("/", 1)[-1] + body[len(rid):]
        wanted.append((depth, body))
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
    """What a widget shows as plain text, or None when the pane has no such
    widget or does not display it."""
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


async def _visit(app, pilot, node):
    """Open every item above `node`, move the cursor onto it, and return the
    cursor line's text."""
    up = node.parent
    while up is not None and up.parent is not None:
        up.expand()
        up = up.parent
    await _settle(pilot)
    _outline(app).move_cursor(node)
    await _settle(pilot)
    return _text(app, "#cursor")


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
        "waiting": _text(app, "#waiting"),
        "reported": _text(app, "#reported"),
        "cursor_text": _text(app, "#cursor"),
        "regions": {name: app.query_one(f"#{name}").region
                    for name in ("waiting", "outline", "reported", "cursor")
                    if app.query(f"#{name}") and app.query_one(f"#{name}").display},
    }


async def _just_shot(app, pilot):
    return _shot(app)


def _open(root, size=SIZE):
    """The pane as it opens."""
    return _drive(root, _just_shot, size)


def _interrupt(seconds):
    """A sleep that meets Ctrl-C, so a loop that sleeps ends at once."""
    raise KeyboardInterrupt


def _ids(lines):
    """The item id each shown line opens on (a diagnostic line opens on `-`)."""
    return [line.split(" ", 1)[0] for line in lines]


# --- SC4.1 the outline holds every line the tree prints ---------------------------------------

def test_sc4_1_the_outline_holds_every_line_the_tree_prints_in_its_order(tmp_path, capsys):
    root = _current(_repo(tmp_path))
    printed = _printed(root, capsys)
    assert any(line.lstrip().startswith("- ") for line in printed)  # a diagnostic, under beta's G0.2
    shot = _open(root, WIDE)
    assert [(depth, label) for depth, label, _ in shot["nodes"]] == _expected_outline(printed)


def test_sc4_1_the_outline_shows_its_text_as_written_never_as_markup(tmp_path, capsys):
    root = _current(_repo(tmp_path))
    sketch = _line_of(ALPHA, f'      - "{MARKUP}"')

    async def script(app, pilot):
        node = _node(app, "alpha/a1-core/SC1.2")
        cursor = await _visit(app, pilot, node)
        shot = _shot(app)
        return _label(node), cursor, shot

    label, cursor, shot = _drive(root, script, WIDE)
    assert label == f"SC1.2 {MARKUP} [to do]"
    assert any(row.rstrip().endswith(label) for row in shot["rows"]), shot["rows"]
    assert cursor == f"specs/alpha/contract.yaml:{sketch} | {MARKUP}"
    assert "prove-red Prove red [doing] current" in shot["lines"]  # a status in brackets too


# --- SC4.1 the opening shape ----------------------------------------------------------------

def test_sc4_1_the_pane_opens_each_feature_down_to_its_units_and_every_other_item_closed(
        tmp_path, capsys):
    root = _repo(tmp_path)  # no progress: no current task
    printed = _printed(root, capsys)
    shot = _open(root, WIDE)
    opened = [label.split(" ", 1)[0] for depth, label, is_open in shot["nodes"] if is_open]
    assert opened == ["alpha", "beta"]  # the features, and nothing else
    # the top level, and one level under each feature: its verdicts and its units
    wanted, feature = [], False
    for line in printed:
        depth = (len(line) - len(line.lstrip(" "))) // 2
        rid = line.strip().split(" ", 1)[0]
        if depth == 0:
            wanted.append(rid)
            feature = not rid.startswith("gates/")
        elif depth == 1 and feature:
            wanted.append(rid.rsplit("/", 1)[-1])
    assert _ids(shot["lines"]) == wanted
    assert "a1-core" in wanted and "G1" in wanted and "b1-solo" in wanted


def test_sc4_1_a_current_task_opens_its_own_unit_and_the_rest_of_the_outline_stays_the_same(
        tmp_path):
    root = _repo(tmp_path)
    before = _open(root)
    _current(root)
    after = _open(root)
    opened = [label.split(" ", 1)[0] for depth, label, is_open in after["nodes"] if is_open]
    assert opened == ["alpha", "a2-edges", "beta"]
    at = _ids(after["lines"]).index("a2-edges")
    held = [key for key in ("approve-tests", "write-tests", "prove-red", "green",
                            "approve-commit", "commit", "two-key", "sketch-1")]
    assert _ids(after["lines"])[at + 1:at + 1 + len(held)] == held
    # take the unit's own lines away and the outline is the one without a task
    assert _ids(after["lines"][:at + 1] + after["lines"][at + 1 + len(held):]) == (
        _ids(before["lines"]))


# --- SC4.1 the current task: its mark, the cursor, the window ----------------------------------

def test_sc4_1_the_current_task_carries_current_and_the_cursor_starts_on_it(tmp_path):
    shot = _open(_current(_repo(tmp_path)))
    assert shot["cursor_label"] == "prove-red Prove red [doing] current"
    assert shot["lines"][shot["cursor"]] == shot["cursor_label"]
    assert [line for line in shot["lines"] if line.split()[-1] == "current"] == [
        "prove-red Prove red [doing] current"]


@pytest.mark.parametrize("parts, current, unit", [
    pytest.param([], "prove-red Prove red current", "a1-core the work for a1-core is done",
                 id="parts-empty"),
    pytest.param(["status"], "prove-red Prove red [doing] current",
                 "a1-core the work for a1-core is done [to do]", id="parts-status"),
])
def test_sc4_1_the_current_task_carries_current_whatever_parts_selects(
        tmp_path, parts, current, unit):
    root = _current(_repo(tmp_path, tree={"pane": {"parts": parts}}))
    shot = _open(root)
    assert shot["cursor_label"] == current
    assert unit in shot["lines"]  # every other line shows the parts selected


def test_sc4_1_the_window_scrolls_to_the_current_task_in_a_tree_taller_than_the_pane(tmp_path):
    shot = _open(_tall(tmp_path))
    assert shot["cursor_label"] == "write-tests Write the tests [doing] current"
    assert shot["cursor"] >= shot["height"]  # below the first window: the pane scrolled
    assert shot["top"] <= shot["cursor"] < shot["top"] + shot["height"]
    assert shot["rows"][shot["cursor"] - shot["top"]].rstrip().endswith(shot["cursor_label"])


def test_sc4_1_with_no_current_task_the_cursor_starts_on_the_first_line(tmp_path):
    shot = _open(_repo(tmp_path))
    assert shot["cursor"] == 0 and shot["top"] == 0
    assert shot["cursor_label"] == shot["lines"][0] == "gates/G0 Planning / Intake [to do]"
    name, page = _pages("gates")["G0"]
    assert shot["cursor_text"] == f"{page} | {name}"


# --- SC4.1 the plain-name cut ---------------------------------------------------------------

def test_sc4_1_a_plain_name_too_long_for_the_pane_is_cut_where_the_status_still_fits(tmp_path):
    root = _current(_repo(tmp_path))
    unit = _line_of(ALPHA, "  - unit: work for a3-long")

    async def script(app, pilot):
        node = _node(app, "alpha/a3-long")
        cursor = await _visit(app, pilot, node)
        return _label(node), cursor, _shot(app)

    label, cursor, shot = _drive(root, script)
    assert len(f"a3-long {LONG} [to do]") > shot["width"]
    assert label.startswith("a3-long ") and label.endswith("... [to do]"), label
    cut = label[len("a3-long "):-len("... [to do]")]
    assert cut and LONG.startswith(cut), label
    row = shot["rows"][shot["cursor"] - shot["top"]]
    # the status ends on the outline's last column: the name gave up no more than it had to
    assert row.rstrip().endswith(label) and len(row.rstrip()) == shot["width"], (row, shot["width"])
    # the cursor line shows the name whole, on as many rows as it needs
    assert cursor == f"specs/alpha/contract.yaml:{unit} | {LONG}"
    assert shot["regions"]["cursor"].height >= -(-len(cursor) // SIZE[0])
    # a line that fits keeps its name whole
    assert "a1-core the work for a1-core is done [to do]" in shot["lines"]


# --- SC4.1 the pane's parts, top to bottom ----------------------------------------------------

def test_sc4_1_the_pane_holds_the_waiting_line_the_outline_the_reported_lines_and_the_cursor_line(
        tmp_path, capfd):
    root = _repo(tmp_path, tree={"pane": {"parts": ["status", "shade"], "fold": "sideways"}})
    _current(root, "alpha/a1-core/approve-tests")
    _write(root / ".sdlc" / "progress" / "beta.yaml", "records: [unclosed\n")
    code = main(["tree", "--root", str(root)])
    unreadable = [line for line in capfd.readouterr().err.splitlines()]
    assert code == 0 and len(unreadable) == 1
    assert unreadable[0].startswith("taskcontract tree: unreadable progress: .sdlc/progress/beta.yaml (")
    shot = _open(root)
    captured = capfd.readouterr()
    assert shot["waiting"] == "waiting on a seat: approve-tests for alpha/a1-core"
    assert shot["reported"].splitlines() == [unreadable[0], PARTS_IGNORED, FOLD_IGNORED]
    regions = shot["regions"]
    assert list(regions) == ["waiting", "outline", "reported", "cursor"]
    assert regions["waiting"].y == 0
    assert (regions["waiting"].bottom <= regions["outline"].y
            and regions["outline"].bottom <= regions["reported"].y
            and regions["reported"].bottom <= regions["cursor"].y)
    assert regions["reported"].height >= 3  # each line whole, wrapped when it must
    assert shot["cursor_label"] == ("approve-tests Approve the test list "
                                    "[waiting on a seat] current seat: user")
    assert captured.err == ""  # the pane writes nothing to stderr


def test_sc4_1_without_an_approval_the_outline_is_the_first_line_of_the_pane(tmp_path):
    shot = _open(_current(_repo(tmp_path)))
    assert shot["waiting"] is None
    assert shot["regions"]["outline"].y == 0
    assert shot["regions"]["cursor"].y >= shot["regions"]["outline"].bottom


@pytest.mark.parametrize("with_task", [pytest.param(True, id="a-current-task"),
                                       pytest.param(False, id="no-current-task")])
def test_sc4_1_the_pane_shows_no_where_am_i_line_no_fold_line_and_no_no_current_task_line(
        tmp_path, with_task):
    root = _repo(tmp_path)
    if with_task:
        _current(root)
    shot = _open(root)
    shown = [label for _, label, _ in shot["nodes"]] + [
        line for key in ("waiting", "reported", "cursor_text") if shot[key]
        for line in shot[key].splitlines()]
    assert shot["nodes"]
    assert not [line for line in shown if " > " in line and line.startswith("specs/")]
    assert not [line for line in shown
                if line.split(" ", 2)[1:2] in (["more:"], ["items:"], ["items"])]
    assert "no current task" not in shown


# --- SC4.1 the command and the extra ----------------------------------------------------------

def test_sc4_1_follow_runs_the_textual_app_in_taskcontract_pane(tmp_path, capsys, monkeypatch):
    root = _current(_repo(tmp_path))
    pane = _pane_module()
    from textual.app import App

    assert issubclass(pane.PaneApp, App)
    calls = []
    monkeypatch.setattr(pane, "run", lambda where: calls.append(where) or 0)
    assert _call(["tree", "--follow", "--root", str(root)], capsys) == (0, "", "")
    assert calls == [root]
    assert callable(tree_view.follow)  # the 0.15.0 loop stays callable until o6


def test_sc4_1_without_the_pane_extra_follow_prints_the_install_line_and_exits_2(
        tmp_path, capsys, monkeypatch):
    root = _current(_repo(tmp_path))
    monkeypatch.setattr(time, "sleep", _interrupt)  # a pane that loops ends at its first tick
    for name in [name for name in sys.modules if name == "textual" or name.startswith("textual.")]:
        monkeypatch.setitem(sys.modules, name, None)
    monkeypatch.setitem(sys.modules, "textual", None)
    monkeypatch.delitem(sys.modules, "taskcontract.pane", raising=False)
    monkeypatch.delattr(taskcontract, "pane", raising=False)
    assert _call(["tree", "--follow", "--root", str(root)], capsys) == (2, "", INSTALL + "\n")
    # an id with --follow still gets its own line first, extra or not
    code, out, err = _call(["tree", "alpha", "--follow", "--root", str(root)], capsys)
    assert (code, out) == (2, "")
    assert err.splitlines()[0] == TAKES_NO_ID


def test_sc4_1_only_the_pane_imports_textual_and_the_pane_writes_no_file(tmp_path, capsys):
    root = _current(_repo(tmp_path))
    script = (
        "import json, sys\n"
        "import taskcontract.tree_view\n"
        "from taskcontract.__main__ import main\n"
        f"codes = [main(['tree', '--root', {str(root)!r}]),\n"
        f"         main(['tree', 'alpha/a1-core', '--root', {str(root)!r}])]\n"
        "before = 'textual' in sys.modules\n"
        "try:\n"
        "    import taskcontract.pane\n"
        "    pane = True\n"
        "except ImportError:\n"
        "    pane = False\n"
        "print(json.dumps({'codes': codes, 'before': before, 'pane': pane,\n"
        "                  'after': 'textual' in sys.modules}))\n")
    env = {**os.environ, "PYTHONPATH": str(KIT)}
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, env=env,
                            encoding="utf-8", errors="replace", cwd=tmp_path, timeout=120)
    assert result.returncode == 0, result.stderr
    seen = json.loads(result.stdout.splitlines()[-1])
    assert seen == {"codes": [0, 0], "before": False, "pane": True, "after": True}
    before = _snapshot(root)
    _open(root)
    assert _snapshot(root) == before


def test_sc4_1_pyproject_gains_the_pane_extra_and_the_test_extra_pins_textual():
    project = tomllib.loads((KIT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    extras = project.get("optional-dependencies", {})
    assert extras.get("pane") == [TEXTUAL_PIN]
    assert extras.get("test") == ["pytest>=8", TEXTUAL_PIN]
    assert not any("textual" in dependency.lower() for dependency in project["dependencies"])


# --- SC1.2 the cursor line --------------------------------------------------------------------

def _sources():
    """Each kind's (id, reference, plain name, the query line that names the
    reference), read from the item's own source."""
    gates, tasks = _pages("gates"), _pages("tasks")
    g0_name, g0_page = gates["G0"]
    condition = next(c for c in yaml.safe_load((DATA / "gates.yaml").read_text(encoding="utf-8"))
                     ["gates"][0]["conditions"] if c["id"] == "G0.2")
    a1 = _line_of(ALPHA, "  - unit: work for a1-core")
    check = _line_of(ALPHA, "      - verify the core prints (SC1.1)")
    return {
        "feature": ("alpha", "docs/features/alpha.md:1", TITLE, "doc"),
        "feature-without-a-document": ("beta", "specs/beta/contract.yaml:1", "(no title)", "file"),
        "unit": ("alpha/a1-core", f"specs/alpha/contract.yaml:{a1}",
                 "the work for a1-core is done", "file"),
        "check": ("alpha/a1-core/SC1.1", f"specs/alpha/contract.yaml:{check}",
                  "verify the core prints (SC1.1)", "file"),
        "finding": ("gates/G0/stale-pin", ".sdlc/findings/stale-pin.yaml:1", PIN, "file"),
        "gate": ("gates/G0", g0_page, g0_name, "page"),
        "verdict": ("alpha/G0", g0_page, g0_name, "page"),
        "condition": ("alpha/G0/G0.2", g0_page, condition["name"], "page"),
        "task": ("alpha/a1-core/approve-tests", tasks["approve-tests"][1],
                 tasks["approve-tests"][0], "page"),
    }


@pytest.mark.parametrize("kind", ["feature", "feature-without-a-document", "unit", "check",
                                  "finding", "gate", "verdict", "condition", "task"])
def test_sc1_2_the_cursor_line_and_the_query_read_the_plain_name_and_reference_from_the_source(
        tmp_path, capsys, kind):
    rid, reference, name, field = _sources()[kind]
    root = _current(_repo(tmp_path))
    # the query: its first line opens on the id and the plain name, and it names the reference
    code, out, err = _call(["tree", rid, "--root", str(root)], capsys)
    assert (code, err) == (0, "")
    lines = out.splitlines()
    assert lines[0].startswith(f"{rid} {name} ["), lines[0]
    assert f"{field}: {reference}" in lines[1:], lines

    async def script(app, pilot):
        return await _visit(app, pilot, _node(app, rid))

    assert _drive(root, script) == f"{reference} | {name}"


@pytest.mark.parametrize("rid, shown", [
    pytest.param("gates/none/bare", ".sdlc/findings/bare.yaml:1", id="no-plain-name"),
    pytest.param("gates/none", "gates/none", id="neither"),
])
def test_sc1_2_an_item_without_a_plain_name_shows_its_reference_and_one_with_neither_its_id(
        tmp_path, rid, shown):
    root = _current(_repo(tmp_path))

    async def script(app, pilot):
        return await _visit(app, pilot, _node(app, rid))

    assert _drive(root, script) == shown


def test_sc1_2_on_a_diagnostic_the_cursor_line_shows_the_diagnostic_whole(tmp_path, capsys):
    root = _current(_repo(tmp_path))
    printed = _printed(root, capsys)
    at = printed.index("    beta/G0/G0.2 Vocabulary coverage [to do]")
    diagnostic = printed[at + 1].strip()
    assert diagnostic.startswith("- ")

    async def script(app, pilot):
        condition = _node(app, "beta/G0/G0.2")
        (line,) = condition.children
        return _label(line), await _visit(app, pilot, line)

    label, cursor = _drive(root, script, WIDE)
    assert label == diagnostic
    assert cursor == diagnostic[2:]


def test_sc1_2_the_cursor_line_follows_the_cursor_up_and_down(tmp_path):
    root = _current(_repo(tmp_path))
    tasks = _pages("tasks")

    async def script(app, pilot):
        seen = [_text(app, "#cursor")]
        for keys in (("up",), ("down", "down")):
            await pilot.press(*keys)
            await _settle(pilot)
            seen.append((_label(_outline(app).cursor_node), _text(app, "#cursor")))
        return seen

    first, up, down = _drive(root, script)
    assert first == f"{tasks['prove-red'][1]} | Prove red"
    assert up == ("write-tests Write the tests [to do]", f"{tasks['write-tests'][1]} | Write the tests")
    assert down == ("green Green [to do]", f"{tasks['green'][1]} | Green")
