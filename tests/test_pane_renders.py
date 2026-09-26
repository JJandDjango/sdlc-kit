"""The pane's renders and its notify command (contract project-tree, unit
o6-pane-keys: SC4.3 and SC3.3).

`taskcontract.pane.PaneApp(root, interval=1.0)` lists its sources as 0.15.0's
pane did (every file under specs/, .sdlc/findings/, .sdlc/progress/ and
docs/features/, plus .sdlc/config.yaml and the kit's two lists) every
`interval` seconds, and renders again when the listing changed, never while
nothing changes. `app.check()` is one such tick, called by hand: it lists
the sources and renders once when they changed, then collects each notify
command that has ended, a nonzero end adding its line to `#reported` after
that render's lines, so no render drops a failure unseen.
Each contract keeps its G0 reading until its file changes; a change under
specs/vocabulary/ drops every reading.

A render keeps the cursor on the same item and every item open or closed as
it was, each item known by its path from the root, so two items that share
an id never trade places. An item new to the tree opens as at the start.
When the item at the cursor is gone, the cursor moves to its nearest parent
that remains. Labels are cut to the width again. When a render moves the
current task to another task, the items above the new one open and the
window scrolls to it; the cursor stays where it was.

The waiting line (`#waiting`) stays the pane's first line, word for word:
`waiting on a seat: <approval> for <contract>/<unit>`. The notify command
(`tree: notify:` in .sdlc/config.yaml) runs through the shell at the repo
root once each time the current task arrives at an approval, never on a
render that leaves it where it was, with the item's id in `SDLC_NODE` and
its output discarded; the pane never waits on it. One that ends nonzero
shows `notify failed, exit <code>: <command>` in `#reported`, whole; a shell
that cannot start reads code 127. A notify failure stays until the next
render; a render replaces the lines the render before it reported. The pane
writes nothing to stderr and no file. Ctrl-C ends the pane with exit 0.

Each test drives the app headless through `App.run_test()` inside
`asyncio.run`, against a fixture repo under tmp_path. Tests that change
sources by hand pass `interval=3600`, so only `check()` renders; two tests
keep the default interval and a real clock.
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import inspect
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest
import yaml

import taskcontract
from conftest import write_seat_roster
from taskcontract import tree
from taskcontract.__main__ import main

KIT = Path(taskcontract.__file__).resolve().parent.parent
DATA = KIT / "taskcontract" / "data"

SIZE = (80, 24)
WIDE = (240, 60)
HAND = 3600  # an interval no test outlives: only check() renders

TITLE = "Apply one discount code per order"
LONG = ("the work for a4-wide is done when every discount code a customer types at "
        "checkout is checked against the list, applied once, and shown on the receipt")
PARTS_IGNORED = ("taskcontract tree: pane parts ignored: shade - give a list from "
                 "id, status, marks, evidence, links, doc, summary")
COMMIT_SKETCH = "verify the commit lands whole (commit)"

UNITS = """\
  - unit: work for a1-core
    id: a1-core
    confirmed_by: [user]
    done_means: the work for a1-core is done
    acceptance_sketch:
      - verify the core prints (SC1.1)
{a1_more}  - unit: work for a2-edges
    id: a2-edges
    depends_on: [a1-core]
    confirmed_by: [user]
    done_means: the work for a2-edges is done
    acceptance_sketch:
      - {a2_sketch}
{a3}{a4}"""

A3 = """\
  - unit: work for a3-long
    id: a3-long
    confirmed_by: [user]
    done_means: the work for a3-long is done
    acceptance_sketch:
      - verify it holds
"""


def _alpha(title=TITLE, a1_more="", a2_sketch="verify an edge holds", a3=True, a4=""):
    """The alpha contract's text: three units, and the parts a test changes."""
    return (f"id: alpha\ntitle: {title}\nintent: A fixture contract for the render suite.\n"
            "scope: [src/]\nnon_goals: [No other work]\ndependencies: []\nentities: []\n"
            "provenance: {origin: human-request}\ndecomposition:\n"
            + UNITS.format(a1_more=a1_more, a2_sketch=a2_sketch, a3=A3 if a3 else "", a4=a4))


def _beta(title=None):
    doc = {"id": "beta", "intent": "A second fixture contract.", "scope": ["src/"],
           "non_goals": ["No other work"],
           "decomposition": [{"unit": "work for b1-solo", "id": "b1-solo",
                              "confirmed_by": ["user"],
                              "done_means": "the work for b1-solo is done",
                              "acceptance_sketch": ["verify the price rounds"]}],
           "dependencies": [], "entities": [], "provenance": {"origin": "human-request"}}
    if title is not None:
        doc["title"] = title
    return doc


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


def _repo(tmp_path, alpha=None, **config):
    """G0 active; alpha (titled, with a feature doc) and beta (no title, no
    doc); one finding under G0."""
    root = tmp_path / "repo"
    _config(root, **config)
    write_seat_roster(root)
    _write(root / "specs" / "alpha" / "contract.yaml", alpha or _alpha())
    _dump(root / "specs" / "beta" / "contract.yaml", _beta())
    _write(root / "docs" / "features" / "alpha.md", f"# alpha - {TITLE}\n")
    _finding(root, "stale-pin", "G0", "The stale-pin finding, in its own words.")
    return root


def _record(item, state="doing", clock="10:00", **more):
    return {"item": item, "state": state, "at": f"2026-09-26T{clock}:00Z",
            "head": "1a2b3c4", **more}


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


def _tall(tmp_path):
    """Fourteen contracts of three units, no gate active; the current task is
    work-14/u3/write-tests, far below the first window."""
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
    _progress(root, "work-14", _record("work-14/u3/write-tests"))
    return root


def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


# --- the notify command ---------------------------------------------------------------

NOTIFY = """\
import os, sys, time
out, code, delay = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
print("NOISE-OUT", flush=True)
print("NOISE-ERR", file=sys.stderr, flush=True)
time.sleep(delay)
with open(out, "a", encoding="utf-8") as handle:
    handle.write(os.environ.get("SDLC_NODE", "<unset>") + "|" + os.getcwd() + "\\n")
sys.exit(code)
"""


def _notify(tmp_path, code=0, delay=0.0):
    """A notify command: a Python script under tmp_path (outside the repo)
    that prints to stdout and stderr, waits `delay` seconds, appends
    `<SDLC_NODE>|<cwd>` to tmp_path/notified.txt and exits `code`. Returns
    (command, the file)."""
    script = tmp_path / "notify.py"
    script.write_text(NOTIFY, encoding="utf-8")
    out = tmp_path / "notified.txt"
    return f'"{sys.executable}" "{script}" "{out}" {code} {delay}', out


def _runs(out):
    """(SDLC_NODE, cwd) per run the file recorded."""
    if not out.is_file():
        return []
    return [tuple(line.split("|", 1)) for line in out.read_text(encoding="utf-8").splitlines()]


def _same_dir(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def _count_g0(monkeypatch):
    """Record the contract folder of each G0 reading the validator makes."""
    seen = []
    real = tree.g0_status

    def counting(path, schema):
        seen.append(Path(path).parent.name)
        return real(path, schema)

    monkeypatch.setattr(tree, "g0_status", counting)
    return seen


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


def _drive(root, script, size=SIZE, **options):
    """Run PaneApp(root, **options) headless at `size`, let it settle, and
    return what `await script(app, pilot)` returns."""
    pane = _pane_module()
    if options:
        taken = inspect.signature(pane.PaneApp).parameters
        missing = [name for name in options if name not in taken]
        assert not missing, (f"PaneApp takes no {', '.join(missing)}: the pane never "
                             "lists its sources again")

    async def go():
        app = pane.PaneApp(Path(root), **options)
        async with app.run_test(size=size) as pilot:
            await _settle(pilot)
            return await script(app, pilot)

    return asyncio.run(go())


async def _render(app, pilot):
    """One tick by hand: app.check(), then let the pane settle."""
    check = getattr(app, "check", None)
    assert callable(check), "PaneApp has no check(): the pane never lists its sources again"
    check()
    await _settle(pilot)


async def _until(pilot, condition, seconds):
    """Pause until `condition()` holds or `seconds` pass; whether it held."""
    deadline = time.monotonic() + seconds
    while not condition():
        if time.monotonic() > deadline:
            return False
        await pilot.pause(0.05)
    return True


async def _ticks_until(app, pilot, condition, seconds=6.0):
    """Call app.check() until `condition()` holds or `seconds` pass."""
    deadline = time.monotonic() + seconds
    while not condition():
        if time.monotonic() > deadline:
            return False
        await _render(app, pilot)
        await pilot.pause(0.05)
    return True


def _outline(app):
    return app.query_one("#outline")


def _head(node):
    return node.label.plain.split(" ", 1)[0]


def _walk(node, depth=0):
    for child in node.children:
        yield depth, child
        yield from _walk(child, depth + 1)


def _keyed(node, above=()):
    """(key, node) for every node under `node`: the key is the path from the
    root, one (head, n) per level, n counting earlier siblings with that head."""
    counts: dict[str, int] = {}
    for child in node.children:
        head = _head(child)
        key = (*above, (head, counts.get(head, 0)))
        counts[head] = counts.get(head, 0) + 1
        yield key, child
        yield from _keyed(child, key)


def _key_of(app, wanted):
    return next(key for key, node in _keyed(_outline(app).root) if node is wanted)


def _opened(app):
    """Each item that holds anything, by key: whether it is open."""
    return {key: node.is_expanded for key, node in _keyed(_outline(app).root)
            if node.children}


def _find(app, *heads, pick=0):
    """The node reached by label heads from the root; at the last level, the
    `pick`-th child with that head."""
    node = _outline(app).root
    for n, head in enumerate(heads):
        found = [child for child in node.children if _head(child) == head]
        last = n == len(heads) - 1
        assert found if last else len(found) == 1, (heads, head, [_head(c) for c in node.children])
        node = found[pick] if last else found[0]
    return node


def _labels(app):
    return [node.label.plain for _, node in _walk(_outline(app).root)]


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


def _reported(app):
    shown = _text(app, "#reported")
    return shown.splitlines() if shown else []


async def _visit(app, pilot, node):
    """Open every item above `node` and put the cursor on it."""
    up = node.parent
    while up is not None and up.parent is not None:
        up.expand()
        up = up.parent
    await _settle(pilot)
    _outline(app).move_cursor(node)
    await _settle(pilot)


def _cursor(app):
    tree_widget = _outline(app)
    node = tree_widget.cursor_node
    return None if node is None else _key_of(app, node)


def _printed(root, capsys):
    try:
        code = main(["tree", "--root", str(root)])
    except SystemExit as exc:
        code = exc.code
    out = capsys.readouterr().out
    assert code == 0
    return out.splitlines()


def _expected_outline(lines):
    wanted = []
    for line in lines:
        body = line.lstrip(" ")
        depth = (len(line) - len(body)) // 2
        if depth and not body.startswith("- "):
            rid = body.split(" ", 1)[0]
            body = rid.rsplit("/", 1)[-1] + body[len(rid):]
        wanted.append((depth, body))
    return wanted


# --- SC4.3 a render lands within two seconds of a change, never while nothing changes -----

def test_sc4_3_a_source_change_renders_within_two_seconds(tmp_path):
    root = _repo(tmp_path)

    async def script(app, pilot):
        task = _find(app, "alpha", "a2-edges", "prove-red")
        before = task.label.plain
        _progress(root, "alpha", _record("alpha/a2-edges/prove-red"))
        start = time.monotonic()
        landed = await _until(pilot, lambda: "current" in _find(
            app, "alpha", "a2-edges", "prove-red").label.plain, 4.0)
        return before, landed, time.monotonic() - start

    before, landed, took = _drive(root, script)
    assert "current" not in before
    assert landed, "no render within four seconds of a change to .sdlc/progress/"
    assert took <= 2.0, f"the render landed {took:.2f} seconds after the change"


def test_sc4_3_no_render_while_nothing_changes(tmp_path, monkeypatch):
    command, out = _notify(tmp_path, code=3)
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))
    readings = _count_g0(monkeypatch)
    line = f"notify failed, exit 3: {command}"

    async def script(app, pilot):
        shown = await _until(pilot, lambda: line in _reported(app), 6.0)
        read = len(readings)
        await pilot.pause(3.0)  # three ticks of the default interval, nothing changed
        return shown, line in _reported(app), read, len(readings)

    shown, kept, read, later = _drive(root, script)
    assert shown, "the failed notify command's line never showed"
    assert kept, "a render replaced the notify failure while no source changed"
    assert later == read, "the pane read a G0 verdict again while nothing changed"


SOURCES = ["specs", "findings", "progress", "features", "config", "gates", "tasks"]


@pytest.mark.parametrize("source", SOURCES)
def test_sc4_3_a_change_to_each_source_renders_again(tmp_path, monkeypatch, source):
    root = _repo(tmp_path)
    for name, path in (("GATES_PATH", tree.GATES_PATH), ("TASKS_PATH", tree.TASKS_PATH)):
        copy = tmp_path / "kit" / path.name
        copy.parent.mkdir(exist_ok=True)
        shutil.copyfile(path, copy)
        monkeypatch.setattr(tree, name, copy)

    def change():
        """Change the source; return (the label's opening, text the label then holds)."""
        if source == "specs":
            _dump(root / "specs" / "beta" / "contract.yaml", _beta("Round prices once"))
            return "beta ", "Round prices once"
        if source == "findings":
            _finding(root, "fresh-find", "G0", "A finding added while the pane runs.")
            return "fresh-find ", "A finding added while the pane runs."
        if source == "progress":
            _progress(root, "alpha", _record("alpha/a2-edges/prove-red"))
            return "prove-red ", "current"
        if source == "features":
            (root / "docs" / "features" / "alpha.md").unlink()
            return "alpha ", "no feature document"
        if source == "config":
            _config(root, gates=("G0", "G1"))  # G2 becomes each contract's next gate
            return "G2 ", "Design / Architecture"
        path = tmp_path / "kit" / ("gates.yaml" if source == "gates" else "tasks.yaml")
        old, new = (("Planning / Intake", "Planning and intake, renamed") if source == "gates"
                    else ("Prove red", "Prove it red, renamed"))
        path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
        return "", new

    async def script(app, pilot):
        before = _labels(app)
        wanted = change()
        await pilot.pause(0.2)
        untouched = _labels(app) == before
        await _render(app, pilot)
        return before, wanted, untouched, _labels(app)

    def holds(label, wanted):
        return label.startswith(wanted[0]) and wanted[1] in label

    before, wanted, untouched, after = _drive(root, script, interval=HAND)
    assert not any(holds(label, wanted) for label in before)
    assert untouched, "the pane rendered with no tick (interval=3600)"
    assert any(holds(label, wanted) for label in after), (
        f"a change under the {source} source did not render: no label holds {wanted!r}")


def test_sc4_3_a_file_outside_the_sources_renders_nothing(tmp_path, monkeypatch):
    command, out = _notify(tmp_path, code=3)
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))
    readings = _count_g0(monkeypatch)
    line = f"notify failed, exit 3: {command}"

    async def script(app, pilot):
        shown = await _ticks_until(app, pilot, lambda: line in _reported(app))
        read = len(readings)
        _write(root / "README.md", "# a file the tree does not read\n")
        _write(root / "src" / "discount.py", "RATE = 1\n")
        _write(root / ".sdlc" / "notes.txt", "not a source\n")
        await _render(app, pilot)
        return shown, line in _reported(app), read, len(readings)

    shown, kept, read, later = _drive(root, script, interval=HAND)
    assert shown, "the failed notify command's line never showed"
    assert kept, "a change outside the pane's sources rendered again"
    assert later == read


def test_sc4_3_each_contract_keeps_its_g0_reading_until_its_file_changes(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    readings = _count_g0(monkeypatch)

    async def script(app, pilot):
        counts = [sorted(readings)]
        _progress(root, "alpha", _record("alpha/a2-edges/prove-red"))
        await _render(app, pilot)
        counts.append(sorted(readings))
        _write(root / "specs" / "alpha" / "contract.yaml", _alpha(title="A retitled alpha"))
        await _render(app, pilot)
        counts.append(sorted(readings))
        write_seat_roster(root, values=("user", "product-owner"))
        await _render(app, pilot)
        counts.append(sorted(readings))
        return counts, "current" in _find(app, "alpha", "a2-edges", "prove-red").label.plain

    counts, rendered = _drive(root, script, interval=HAND)
    assert rendered, "the progress change did not render"
    assert counts[0] == ["alpha", "beta"]
    assert counts[1] == ["alpha", "beta"], "a progress change read a G0 verdict again"
    assert counts[2] == ["alpha", "alpha", "beta"], "a contract change must re-read that contract alone"
    assert counts[3] == ["alpha", "alpha", "alpha", "beta", "beta"], (
        "a change under specs/vocabulary/ must drop every reading")


# --- SC4.3 a render keeps the cursor and each open or closed item ----------------------------

def test_sc4_3_a_render_keeps_the_cursor_and_each_open_or_closed_item(tmp_path):
    root = _repo(tmp_path)
    _progress(root, "alpha", _record("alpha/a2-edges/prove-red"))

    async def script(app, pilot):
        _find(app, "alpha", "a1-core").expand()           # closed at the start
        _find(app, "gates/G0").expand()                   # closed at the start
        _find(app, "beta").collapse()                     # open at the start
        _find(app, "alpha", "a2-edges").collapse()        # opened for the current task
        await _visit(app, pilot, _find(app, "alpha", "a3-long", "sketch-1"))
        before = (_opened(app), _cursor(app), _text(app, "#cursor"))
        _dump(root / "specs" / "beta" / "contract.yaml", _beta("Round prices once"))
        await _render(app, pilot)
        after = (_opened(app), _cursor(app), _text(app, "#cursor"))
        return before, after, _find(app, "beta").label.plain

    before, after, beta = _drive(root, script, interval=HAND)
    assert "Round prices once" in beta, "the change did not render"
    assert after[0] == before[0], "a render changed which items are open"
    assert after[1] == before[1], "a render moved the cursor"
    assert after[2] == before[2]


def test_sc4_3_two_items_that_share_an_id_never_trade_places_under_the_cursor(tmp_path):
    root = _repo(tmp_path, alpha=_alpha(a1_more=f"      - {COMMIT_SKETCH}\n"))

    async def script(app, pilot):
        seen = []
        for pick, title in ((0, "First retitle"), (1, "Second retitle")):
            await _visit(app, pilot, _find(app, "alpha", "a1-core", "commit", pick=pick))
            before = (_cursor(app), _text(app, "#cursor"))
            _dump(root / "specs" / "beta" / "contract.yaml", _beta(title))
            await _render(app, pilot)
            seen.append((before, (_cursor(app), _text(app, "#cursor")),
                         title in _find(app, "beta").label.plain))
        return seen

    seen = _drive(root, script, interval=HAND)
    (task_before, task_after, rendered_1), (check_before, check_after, rendered_2) = seen
    assert rendered_1 and rendered_2, "the changes did not render"
    assert task_before[1] == "USAGE.md | Commit"
    assert COMMIT_SKETCH in check_before[1]
    assert task_after == task_before, "the cursor left the task commit for another item"
    assert check_after == check_before, "the cursor left the check commit for another item"


def test_sc4_3_two_items_that_share_an_id_keep_their_own_open_or_closed_state(tmp_path):
    """A contract named `gates` holds a verdict `gates/G0`, the top-level gate's id."""
    root = _repo(tmp_path)
    _dump(root / "specs" / "gates" / "contract.yaml", {
        **_beta(), "id": "gates", "title": "A contract that shares the gates' ids"})

    async def script(app, pilot):
        seen = []
        for opened, title in (("verdict", "First retitle"), ("gate", "Second retitle")):
            gate, verdict = _find(app, "gates/G0"), _find(app, "gates", "G0")
            (verdict.expand() if opened == "verdict" else verdict.collapse())
            (gate.expand() if opened == "gate" else gate.collapse())
            await _settle(pilot)
            before = _opened(app)
            _dump(root / "specs" / "beta" / "contract.yaml", _beta(title))
            await _render(app, pilot)
            seen.append((opened, before, _opened(app),
                         _find(app, "gates/G0").is_expanded,
                         _find(app, "gates", "G0").is_expanded,
                         title in _find(app, "beta").label.plain))
        return seen

    for opened, before, after, gate_open, verdict_open, rendered in _drive(
            root, script, interval=HAND):
        assert rendered, "the change did not render"
        assert (gate_open, verdict_open) == (opened == "gate", opened == "verdict"), (
            f"with the {opened} open, a render traded the gate's and the verdict's state")
        assert after == before


def test_sc4_3_an_item_new_to_the_tree_opens_as_at_the_start(tmp_path):
    root = _repo(tmp_path)

    async def script(app, pilot):
        _find(app, "alpha").collapse()
        await _settle(pilot)
        _dump(root / "specs" / "gamma" / "contract.yaml", {
            **_beta(), "id": "gamma", "title": "A contract new to the tree"})
        _write(root / "specs" / "alpha" / "contract.yaml", _alpha(a4=(
            "  - unit: work for a4-new\n    id: a4-new\n    confirmed_by: [user]\n"
            "    done_means: the work for a4-new is done\n"
            "    acceptance_sketch:\n      - verify it is new\n")))
        await _render(app, pilot)
        gamma = _find(app, "gamma")
        return (gamma.is_expanded, [child.is_expanded for child in gamma.children
                                    if child.children],
                _find(app, "alpha").is_expanded, _find(app, "alpha", "a4-new").is_expanded)

    gamma_open, gamma_children, alpha_open, new_unit_open = _drive(root, script, interval=HAND)
    assert gamma_open, "a new contract did not open as at the start"
    assert gamma_children and not any(gamma_children), "a new contract's units must start closed"
    assert not alpha_open, "a render reopened a contract the reader closed"
    assert not new_unit_open, "a new unit must start closed"


def test_sc4_3_the_cursor_moves_to_the_nearest_parent_that_remains(tmp_path):
    root = _repo(tmp_path)

    async def script(app, pilot):
        await _visit(app, pilot, _find(app, "alpha", "a2-edges", "sketch-1"))
        _write(root / "specs" / "alpha" / "contract.yaml",
               _alpha(a2_sketch="verify an edge holds (SC9.9)"))
        await _render(app, pilot)
        first = (_cursor(app), _text(app, "#cursor"))
        await _visit(app, pilot, _find(app, "alpha", "a3-long", "green"))
        _write(root / "specs" / "alpha" / "contract.yaml",
               _alpha(a2_sketch="verify an edge holds (SC9.9)", a3=False))
        await _render(app, pilot)
        second = (_cursor(app), _text(app, "#cursor"))
        return first, second

    first, second = _drive(root, script, interval=HAND)
    assert first[0] == (("alpha", 0), ("a2-edges", 0)), (
        f"with its check gone, the cursor must rest on unit a2-edges, not {first[0]}")
    assert first[1].endswith("| the work for a2-edges is done")
    assert second[0] == (("alpha", 0),), (
        f"with its unit gone, the cursor must rest on contract alpha, not {second[0]}")


def test_sc4_3_labels_are_cut_to_the_width_again_after_a_render(tmp_path):
    root = _repo(tmp_path)

    async def script(app, pilot):
        _write(root / "specs" / "alpha" / "contract.yaml", _alpha(a4=(
            "  - unit: work for a4-wide\n    id: a4-wide\n    confirmed_by: [user]\n"
            f"    done_means: {LONG}\n"
            "    acceptance_sketch:\n      - verify it is wide\n")))
        await _render(app, pilot)
        tree_widget = _outline(app)
        node = _find(app, "alpha", "a4-wide")
        room = (tree_widget.scrollable_content_region.width - tree_widget.guide_depth - 2)
        return node.label.plain, room

    shown, room = _drive(root, script, interval=HAND)
    assert LONG not in shown
    # the new unit starts closed, so its group of eight items stays in view after the status
    assert shown.endswith("... [to do] (8 items: 8 to do)"), (
        f"the new unit's label was not cut: {shown!r}")
    assert len(shown) <= room


# --- SC4.3 a render that moves the current task -----------------------------------------------

def test_sc4_3_a_render_that_moves_the_current_task_opens_it_and_scrolls_it_into_view(tmp_path):
    root = _tall(tmp_path)

    async def script(app, pilot):
        tree_widget = _outline(app)
        tree_widget.move_cursor(tree_widget.get_node_at_line(0))
        await _settle(pilot)
        before = (_cursor(app), _opened(app))
        _progress(root, "work-13", _record("work-13/u2/prove-red", clock="11:00"))
        await _render(app, pilot)
        new = _find(app, "work-13", "u2", "prove-red")
        top, height = tree_widget.scroll_offset.y, tree_widget.scrollable_content_region.height
        return (before, _cursor(app), _opened(app), new.label.plain, new.line, top, height)

    before, cursor, opened, label, line, top, height = _drive(root, script, interval=HAND)
    assert "current" in label, "the progress change did not render"
    unit = (("work-13", 0), ("u2", 0))
    assert not before[1][unit] and opened[unit], "the new current task's unit did not open"
    assert top <= line < top + height, "the window did not scroll to the new current task"
    assert cursor == before[0], "the cursor left the item it was on"
    rest = {key: state for key, state in opened.items() if key != unit}
    assert rest == {key: state for key, state in before[1].items() if key != unit}, (
        "the render changed an item other than the ones above the new current task")


# --- SC4.3 the waiting line ------------------------------------------------------------------------

def test_sc4_3_the_waiting_line_stays_the_first_line_word_for_word(tmp_path):
    root = _repo(tmp_path)
    _progress(root, "alpha", _record("alpha/a2-edges/prove-red"))

    async def script(app, pilot):
        def seen():
            regions = {name: app.query_one(f"#{name}").region for name in ("waiting", "outline")}
            return _text(app, "#waiting"), regions["waiting"].y, regions["outline"].y

        shots = [seen()]
        _progress(root, "alpha", _record("alpha/a2-edges/prove-red"),
                  _record("alpha/a2-edges/approve-tests", clock="11:00"))
        await _render(app, pilot)
        shots.append(seen())
        _progress(root, "alpha", _record("alpha/a2-edges/prove-red"),
                  _record("alpha/a2-edges/approve-tests", clock="11:00"),
                  _record("alpha/a2-edges/green", clock="12:00"))
        await _render(app, pilot)
        shots.append(seen())
        return shots

    at_start, arrived, left = _drive(root, script, interval=HAND)
    assert at_start[0] is None and at_start[2] == 0
    assert arrived[0] == "waiting on a seat: approve-tests for alpha/a2-edges", (
        "a render that brings the current task to an approval must show the waiting line")
    assert arrived[1] == 0 and arrived[2] == 1, "the waiting line must be the pane's first line"
    assert left[0] is None and left[2] == 0, "the waiting line must go when the task leaves"


# --- SC4.3 Ctrl-C --------------------------------------------------------------------------------------

def test_sc4_3_ctrl_c_ends_the_pane_with_exit_0(tmp_path):
    root = _repo(tmp_path)

    async def script(app, pilot):
        await pilot.press("ctrl+c")
        ended = await _until(pilot, lambda: not app.is_running, 3.0)
        return ended, app.return_code

    ended, code = _drive(root, script)
    assert ended, "Ctrl-C did not end the pane"
    assert code == 0


# --- SC3.3 the notify command --------------------------------------------------------------------

def test_sc3_3_a_pane_that_starts_on_an_approval_runs_the_command_at_the_repo_root(
        tmp_path, capfd):
    command, out = _notify(tmp_path)
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))

    async def script(app, pilot):
        ran = await _until(pilot, lambda: _runs(out), 6.0)
        await pilot.pause(0.5)
        return ran, _reported(app)

    ran, reported = _drive(root, script)
    runs = _runs(out)
    assert ran, "a pane that starts on an approval did not run the notify command"
    assert [node for node, _ in runs] == ["alpha/a2-edges/approve-tests"]
    assert _same_dir(runs[0][1], root), f"the command ran in {runs[0][1]}, not the repo root"
    captured = capfd.readouterr()
    assert "NOISE" not in captured.out + captured.err, "the command's output was not discarded"
    assert captured.err == ""
    assert not any("NOISE" in line for line in reported)


def test_sc3_3_the_command_runs_once_per_arrival_at_an_approval_never_on_a_render(tmp_path):
    command, out = _notify(tmp_path)
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/prove-red"))
    steps = [
        ("approve-tests", "11:00", 1),
        (None, None, 1),              # a render that leaves the task where it was
        ("green", "12:00", 1),
        ("approve-commit", "13:00", 2),
        ("approve-tests", "14:00", 3),
    ]

    async def script(app, pilot):
        records = [_record("alpha/a2-edges/prove-red")]
        counts = [len(_runs(out))]
        await pilot.pause(1.0)
        counts.append(len(_runs(out)))
        for n, (task, clock, wanted) in enumerate(steps):
            if task is None:
                _dump(root / "specs" / "beta" / "contract.yaml", _beta(f"Retitle {n}"))
            else:
                records.append(_record(f"alpha/a2-edges/{task}", clock=clock))
                _progress(root, "alpha", *records)
            await _render(app, pilot)
            await _until(pilot, lambda: len(_runs(out)) >= wanted, 6.0)
            await pilot.pause(1.0)
            counts.append(len(_runs(out)))
        return counts

    counts = _drive(root, script, interval=HAND)
    assert counts[:2] == [0, 0], "the command ran while no approval was current"
    assert counts[2:] == [wanted for _, _, wanted in steps], (
        f"runs after each render {counts[2:]}, wanted {[w for _, _, w in steps]}")
    assert [node for node, _ in _runs(out)] == [
        "alpha/a2-edges/approve-tests", "alpha/a2-edges/approve-commit",
        "alpha/a2-edges/approve-tests"]


def test_sc3_3_the_pane_never_waits_on_the_command_and_ctrl_c_leaves_it_running(tmp_path):
    command, out = _notify(tmp_path, delay=3.0)
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))

    async def script(app, pilot):
        waiting = _text(app, "#waiting")
        written = out.exists()
        await pilot.press("ctrl+c")
        ended = await _until(pilot, lambda: not app.is_running, 3.0)
        return waiting, written, ended, app.return_code

    waiting, written, ended, code = _drive(root, script)
    assert waiting == "waiting on a seat: approve-tests for alpha/a2-edges"
    assert not written, "the pane waited on the notify command"
    assert ended and code == 0, "Ctrl-C did not end the pane with exit 0"
    deadline = time.monotonic() + 10.0
    while not _runs(out) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert [node for node, _ in _runs(out)] == ["alpha/a2-edges/approve-tests"], (
        "the command started at the approval never ran to its end")


def test_sc3_3_a_failed_command_shows_whole_in_the_pane_until_the_next_render(tmp_path, capfd):
    command, out = _notify(tmp_path, code=3)
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))
    line = f"notify failed, exit 3: {command}"
    assert len(line) > SIZE[0]

    async def script(app, pilot):
        shown = await _ticks_until(app, pilot, lambda: line in _reported(app))
        await _render(app, pilot)  # nothing changed: no render
        kept = line in _reported(app)
        _dump(root / "specs" / "beta" / "contract.yaml", _beta("Round prices once"))
        await _render(app, pilot)
        return shown, kept, _reported(app), _find(app, "beta").label.plain

    shown, kept, after, beta = _drive(root, script, interval=HAND)
    assert shown, f"the pane never showed {line!r} whole in #reported"
    assert kept, "the notify failure went before the next render"
    assert "Round prices once" in beta
    assert line not in after, "a render must replace the notify failure"
    assert len(_runs(out)) == 1, "the render ran the command again"
    assert capfd.readouterr().err == "", "the pane wrote on stderr"


def test_sc3_3_a_failure_that_ends_before_a_render_shows_after_it(tmp_path, capfd):
    command, out = _notify(tmp_path, code=3)
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))
    line = f"notify failed, exit 3: {command}"

    async def script(app, pilot):
        ran = await _until(pilot, lambda: bool(_runs(out)), 10.0)
        await pilot.pause(1.0)  # the command wrote its run; let it end before any tick
        _dump(root / "specs" / "beta" / "contract.yaml", _beta("Round prices once"))
        await _render(app, pilot)  # one tick that both renders and finds the failure
        return ran, _reported(app), _find(app, "beta").label.plain

    ran, reported, beta = _drive(root, script, interval=HAND)
    assert ran, "the pane never ran the notify command"
    assert "Round prices once" in beta, "the tick did not render"
    assert line in reported, "a render dropped a failure that ended before it, unseen"
    assert capfd.readouterr().err == "", "the pane wrote on stderr"


def test_sc3_3_a_shell_that_cannot_start_reads_code_127(tmp_path, monkeypatch, capfd):
    command = "notify-shell-that-cannot-start --now"
    root = _repo(tmp_path, tree={"notify": command})
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))
    real = subprocess.Popen
    tried = []

    def no_shell(*args, **kwargs):
        if kwargs.get("shell"):
            tried.append(args[0] if args else kwargs.get("args"))
            raise FileNotFoundError(2, "the shell cannot start")
        return real(*args, **kwargs)

    monkeypatch.setattr(subprocess, "Popen", no_shell)

    async def script(app, pilot):
        return _reported(app)

    reported = _drive(root, script)
    assert tried == [command], "the pane did not start the command through the shell"
    assert f"notify failed, exit 127: {command}" in reported
    assert capfd.readouterr().err == ""


@pytest.mark.parametrize("notify", [
    pytest.param(None, id="unset"),
    pytest.param("   ", id="blanks"),
    pytest.param(5, id="a-number"),
    pytest.param(["echo", "x"], id="a-list"),
])
def test_sc3_3_a_notify_that_holds_no_command_starts_nothing_and_keeps_the_waiting_line(
        tmp_path, monkeypatch, capfd, notify):
    root = _repo(tmp_path, **({} if notify is None else {"tree": {"notify": notify}}))
    _progress(root, "alpha", _record("alpha/a2-edges/approve-tests"))
    real = subprocess.Popen
    tried = []

    def spy(*args, **kwargs):
        if kwargs.get("shell"):
            tried.append(args[0] if args else kwargs.get("args"))
            raise FileNotFoundError(2, "no command should start")
        return real(*args, **kwargs)

    monkeypatch.setattr(subprocess, "Popen", spy)

    async def script(app, pilot):
        # arrive at approve-tests (the start), leave it, then arrive at approve-commit
        _progress(root, "alpha", _record("alpha/a2-edges/write-tests"))
        await _render(app, pilot)
        _progress(root, "alpha", _record("alpha/a2-edges/approve-commit"))
        await _render(app, pilot)
        return _text(app, "#waiting"), _reported(app)

    waiting, reported = _drive(root, script, interval=3600)
    assert tried == [], "a notify: that holds no command started one"
    assert waiting == "waiting on a seat: approve-commit for alpha/a2-edges"
    assert not [line for line in reported if line.startswith("notify failed")]
    assert capfd.readouterr().err == ""


# --- SC4.3 / SC3.3 what a render reports, and what it leaves alone ---------------------------

def test_sc4_3_a_render_replaces_the_lines_the_render_before_it_reported(tmp_path, capfd):
    root = _repo(tmp_path, tree={"pane": {"parts": ["shade"]}})

    async def script(app, pilot):
        first = _reported(app)
        _config(root)
        _write(root / ".sdlc" / "findings" / "broken.yaml", "finding: [unclosed\n")
        await _render(app, pilot)
        return first, _reported(app)

    first, second = _drive(root, script, interval=HAND)
    assert first == [PARTS_IGNORED]
    wanted = [f"taskcontract tree: {problem}" for problem in tree.build(root)[1]]
    assert wanted and "broken.yaml" in wanted[0]
    assert second == wanted, "a render must replace the lines the render before it reported"
    assert capfd.readouterr().err == "", "the pane wrote on stderr"


def test_sc3_3_after_a_render_each_recorded_state_reads_as_the_tree_prints_it(tmp_path, capsys):
    root = _repo(tmp_path)
    records = [
        _record("alpha/a1-core/approve-tests", "done", "09:00", by="user"),
        _record("alpha/a1-core/write-tests", "done", "09:10"),
        _record("alpha/a1-core/prove-red", "blocked", "09:20", reason="the fixture is missing"),
    ]
    _progress(root, "alpha", *records)

    async def script(app, pilot):
        _progress(root, "alpha", *records, _record("alpha/a2-edges/write-tests", clock="10:00"))
        before = _snapshot(root)
        await _render(app, pilot)
        await pilot.pause(0.5)
        return ([(depth, node.label.plain, node.is_expanded or not node.children)
                 for depth, node in _walk(_outline(app).root)], before, _snapshot(root))

    shown, before, after = _drive(root, script, size=WIDE, interval=HAND)
    assert any("write-tests Write the tests [doing] current" in label for _, label, _ in shown), (
        "the progress change did not render")
    # a closed item's line adds what it holds in parentheses (the keys' half of the unit);
    # without them, each line reads as the tree prints it
    held = re.compile(r" \(\d+ (?:items: .*?|diagnostics)\)")
    assert [(depth, label if opened else held.sub("", label, count=1))
            for depth, label, opened in shown] == _expected_outline(_printed(root, capsys))
    assert after == before, "the pane wrote a file"
