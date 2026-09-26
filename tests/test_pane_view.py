"""The pane-view suite (contract pane-view, units p1-where-line, p2-short-ids,
p3-line-parts and p4-fold-names).

`taskcontract tree --follow` prints one where-am-I line for the current
task: `specs/<contract>/contract.yaml > <contract> > <unit> > <task>`, the
contract's file from the repository root with forward slashes, then the
contract's id, then the last segment of the unit's id and of the task's id,
joined by ` > `, with no indent. When the current task is `approve-tests` or
`approve-commit` the line stands directly under the waiting line, which stays
the pane's first line word for word; otherwise it is the pane's first line.
Either way it stands above the rest of the pane: the top-level fold line, or
the contract's line when the top level holds no other item (SC1.1). A
where-am-I line longer than the pane's width is cut to the width and ends in
`...`, as every pane line is, and with no current task the pane prints none
(SC1.2).

In the pane, each item line under another item opens on the last segment of
its id, the part after the id's last `/`: a unit's line on `a2-edges`, not
`alpha/a2-edges`, and a task's on `prove-red`, not
`alpha/a2-edges/prove-red`. A top-level item's line opens on its full id.
After the id each item line reads exactly as the whole tree's line for that
item, at the same indent, and only the id that opens the line shortens: a
plain name that names a full id keeps it (SC3.1). `taskcontract tree` prints
the same bytes as before; the waiting line, every link (`depends_on:
<contract>/<unit>` on a unit's line) and the notify command's `SDLC_NODE`
keep full ids (SC3.2).

`tree: pane: parts:` in .sdlc/config.yaml lists the fields each item line
of the pane shows after its id, which always shows: status, marks,
evidence, links, doc and summary, each read exactly as on the whole tree's
line (` [<status>]`, each mark after one space, ` <evidence>`, each link
after one space, ` doc: <path>`, ` | <summary>`), and a field the item lacks
prints nothing. The fields print in that fixed order whatever order the
list gives; listing `id` changes nothing, a repeated name shows its field
once, and `[]` shows the id and its plain name alone (SC2.1). Since
project-tree's o2-titles each item line opens on its id, then its plain
name (a contract's `title`, else `(no title)`; a unit's `done_means`; a
task's name), then the fields; the summary holds only a contract's intent. With `parts:` unset (no config,
no `tree:`, no `pane:`, a `pane:` without `parts:`, or a `tree:` or `pane:`
that is not a mapping) each item line shows every field it has. Set, valid
or not, it leaves the waiting line, the where-am-I line, the fold lines and
the `no current task` render byte for byte, the cut applies to each line as
`parts:` leaves it, `tree: notify:` still runs beside it, and `taskcontract
tree` prints the same stdout and stderr as without it (SC2.2). A `parts:`
that is not a list (text, a number, a mapping, null), or a list with an
entry that is not one of the seven names exactly, is ignored as a whole:
each item line shows every field it has, and each render prints one line on
stderr after its unreadable-source lines, `taskcontract tree: pane parts
ignored: {value} - give a list from id, status, marks, evidence, links, doc,
summary`, `{value}` the first entry that names no field, else the whole
value, as str() gives it. The pane reads the key at each render (SC2.3).

`tree: pane: fold: names` in .sdlc/config.yaml makes each fold line name
the items it folds in place of the counts: at the fold line's own indent,
`<n> more: `, then each folded item as `<id> [<status>]`, joined by `, `, in
the tree's order. The id reads as the item's own line would open: the full
id at the top level (`gates/G0`, `gates/none`, `beta`), the last segment
under another item (`G0` for a contract's verdict, `a1-core` for a unit,
`sketch-1` or `SC5.1+SC5.2` for a check). With no current task the `<n>
items:` line names the top-level items the same way, and with no item at all
reads `0 items`. A fold line under names is cut to the pane's width like
every other line, and `parts:` never changes a fold line: each folded item
shows its status whatever `parts:` lists. The waiting line, the where-am-I
line, every item line, the order and count of the lines, the notify command
and `SDLC_NODE` stay as they were (SC4.1). `fold: counts`, no `fold:`, no
config, and a `tree:` or `pane:` that is not a mapping keep the counts with
nothing on stderr. Any other value (another word, `Names`, a number, a list,
a mapping, null) keeps the counts, and each render prints one line on
stderr, `taskcontract tree: pane fold ignored: {value} - give names or
counts`, `{value}` the value as str() gives it, after the render's
unreadable-source lines and after its parts line. The pane reads the key at
each render, and reads `parts:` and `fold:` apart: a bad one leaves the
other working. `taskcontract tree` prints the same stdout and stderr with
the key set, valid or not (SC4.2).

The rest of the pane reads as tree-view t7 and t8 built it: the fold lines'
counts when `fold:` does not name the items, the cut to the pane's width,
the `no current task` render; and `taskcontract tree` prints no where-am-I
line. The loop runs in-process: `follow(root, out, sleep=...)` takes an
injected sleep, which changes source files between scans and raises
KeyboardInterrupt to end the loop, as Ctrl-C does. No test waits on a real
second.
"""

from __future__ import annotations

import importlib
import io
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from conftest import ROW, cut_lines, short_line, write_seat_roster
from taskcontract.__main__ import main

tree_view = importlib.import_module("taskcontract.tree_view")

CLEAR = "\x1b[H\x1b[2J"  # cursor home, then clear the screen: every render opens on it
HEAD = "1a2b3c4"
INTENT = ("A fixture contract for the pane-view suite; its units carry the "
          "sketch shapes that check ids come from.")

WHERE_PROVE_RED = "specs/alpha/contract.yaml > alpha > a2-edges > prove-red"
WHERE_WRITE_TESTS = "specs/alpha/contract.yaml > alpha > a1-core > write-tests"
WHERE_APPROVE_COMMIT = "specs/alpha/contract.yaml > alpha > a2-edges > approve-commit"
WAIT_APPROVE_COMMIT = "waiting on a seat: approve-commit for alpha/a2-edges"
# the request's own example: 60 and 73 columns
WAIT_QUERY_FACE = "waiting on a seat: approve-tests for tree-view/t6-query-face"
WHERE_QUERY_FACE = "specs/tree-view/contract.yaml > tree-view > t6-query-face > approve-tests"


@pytest.fixture(autouse=True)
def _wide_and_outside_git(tmp_path, monkeypatch):
    """A wide pane unless a test sets its own width, and no repo above the fixture."""
    monkeypatch.setenv("COLUMNS", "500")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))


# --- the fixture repository -----------------------------------------------------

def _unit(uid, sketches, depends_on=None):
    unit = {
        "unit": "work for " + uid,
        "id": uid,
        "confirmed_by": ["user"],
        "done_means": "the work for " + uid + " is done",
        "acceptance_sketch": list(sketches),
    }
    if depends_on is not None:
        unit["depends_on"] = depends_on
    return unit


ALPHA = [
    _unit("a1-core", ["verify the core prints (SC1.1)",
                      "verify both links print (SC5.1, SC5.2)"]),
    _unit("a2-edges", ["verify an edge holds",
                       "verify it again (SC2.1)",
                       "verify it once more (SC2.1)"], depends_on=["a1-core"]),
]
BETA = [_unit("b1-solo", ["verify the price rounds (by the house rule)"])]


def _contract(cid, units, **fields):
    """A contract that reads ready-green; a field given as None is dropped."""
    doc = {
        "id": cid,
        "intent": INTENT,
        "scope": ["src/"],
        "non_goals": ["No other work"],
        "decomposition": units,
        "dependencies": [],
        "entities": [],
        "provenance": {"origin": "human-request"},
    }
    for key, value in fields.items():
        if value is None:
            doc.pop(key)
        else:
            doc[key] = value
    return doc


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _config(root, gates, **more):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates), **more})


def _repo(tmp_path, gates=("G0",)):
    """alpha and beta, both ready-green, with the given gates active and no progress."""
    root = tmp_path / "repo"
    _config(root, gates)
    _dump(root / "specs" / "alpha" / "contract.yaml", _contract("alpha", ALPHA))
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA))
    write_seat_roster(root)
    return root


def _query_face_repo(tmp_path):
    """The request's example: tree-view's t6-query-face at approve-tests, beside
    pane-view; no active gate, so no render runs the validator or git."""
    root = tmp_path / "repo"
    _config(root, [])
    _dump(root / "specs" / "tree-view" / "contract.yaml", _contract("tree-view", [
        _unit("t5-pane-face", ["verify the pane follows (SC2.1)"]),
        _unit("t6-query-face", ["verify one node prints (SC6.1)"],
              depends_on=["t5-pane-face"]),
    ]))
    _dump(root / "specs" / "pane-view" / "contract.yaml", _contract("pane-view", [
        _unit("p1-where-line", ["verify the line reads (SC1.1)"]),
    ]))
    write_seat_roster(root)
    _progress(root, "tree-view",
              _step("tree-view/t6-query-face/approve-tests", "doing", "10:00"))
    return root


def _hyphens_and_digits_repo(tmp_path):
    """pane-view-2, whose ids carry hyphens and digits, at its unit
    p10-where-line-3's two-key; no active gate."""
    root = tmp_path / "repo"
    _config(root, [])
    _dump(root / "specs" / "pane-view-2" / "contract.yaml", _contract("pane-view-2", [
        _unit("p9-short-ids-2", ["verify it holds (SC3.1)"]),
        _unit("p10-where-line-3", ["verify it reads (SC1.1)"], depends_on=["p9-short-ids-2"]),
    ]))
    write_seat_roster(root)
    _progress(root, "pane-view-2",
              _step("pane-view-2/p10-where-line-3/two-key", "doing", "10:00"))
    return root


def _at(clock):
    return f"2026-09-22T{clock}:00Z"


def _step(item, state, clock, **more):
    """A task-step record; on a unit or a contract id with `done`, a close."""
    return {"item": item, "state": state, "at": _at(clock), "head": HEAD, **more}


def _ran(item, run, expect, clock):
    return {"item": item, "run": run, "expect": expect,
            "command": "python -m pytest tests/", "dirty": False,
            "at": _at(clock), "head": HEAD}


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


def _append(path, text="\n# a note\n"):
    """Grow a file, so its size differs whatever its time reads."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


def _path_repo(tmp_path):
    """alpha, beta closed; the current task is alpha/a2-edges/prove-red, the
    only task doing, so it is not an approval."""
    root = _repo(tmp_path)
    _progress(root, "beta", _step("beta", "done", "09:00"))
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "10:00", by="user"),
              _step("alpha/a1-core/write-tests", "blocked", "10:01", reason="the runner is down"),
              _step("alpha/a2-edges/approve-tests", "done", "10:02", by="user"),
              _step("alpha/a2-edges/write-tests", "done", "10:03"),
              _step("alpha/a2-edges/prove-red", "doing", "10:04"),
              _ran("alpha/a2-edges/sketch-1", "green", "red", "10:05"))
    return root


# --- driving the pane -----------------------------------------------------------

class Sleeper:
    """The injected sleep: each call notes its argument and the renders so
    far, then runs the next step; with no step left it raises
    KeyboardInterrupt, as Ctrl-C does."""

    def __init__(self, out, steps):
        self.out = out
        self.steps = list(steps)
        self.args = []
        self.renders = []  # renders written before each call

    def __call__(self, seconds):
        self.args.append(seconds)
        self.renders.append(self.out.getvalue().count(CLEAR))
        if not self.steps:
            raise KeyboardInterrupt
        step = self.steps.pop(0)
        if step is not None:
            step()


def _pane(root, *steps):
    """(sleeper, renders) of one pane run: each step runs in one sleep, and
    the call after the last step ends the loop. Each render is its lines."""
    follow = getattr(tree_view, "follow", None)
    assert callable(follow), "taskcontract.tree_view has no follow(root, out, sleep=...)"
    out = io.StringIO()
    sleeper = Sleeper(out, steps)
    code = follow(Path(root), out, sleep=sleeper)
    assert code == 0, f"the pane ended with {code!r}, not 0"
    return sleeper, _renders(out.getvalue())


def _renders(text):
    assert text.startswith(CLEAR), f"the pane output opens on {text[:20]!r}"
    return [chunk.splitlines() for chunk in text.split(CLEAR)[1:]]


def _whole(root, capsys):
    """The whole tree's lines by id, as `taskcontract tree` prints them."""
    code = main(["tree", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 0
    lines = {}
    for line in out.splitlines():
        match = ROW.match(line)
        if match:
            lines[match["id"]] = line
    return lines


def _where_lines(render):
    """The render's lines that open on a contract file's path."""
    return [line for line in render if line.startswith("specs/")]


# --- SC1.1 the where-am-I line and its place ----------------------------------------

def test_sc1_1_at_a_task_that_is_not_an_approval_the_where_line_is_the_panes_first_line(
        tmp_path, capsys):
    root = _path_repo(tmp_path)
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert renders == [[
        WHERE_PROVE_RED,                              # first, above the top-level fold line
        "2 more: 1 to do, 1 done",                    # gates/G0, beta
        whole["alpha"],
        "  3 more: 1 to do, 1 done, 1 blocked",       # alpha/G0, alpha/G1 inactive, alpha/a1-core
        short_line(whole["alpha/a2-edges"]),
        "    9 more: 6 to do, 2 done, 1 failed",      # the other tasks and the checks
        short_line(whole["alpha/a2-edges/prove-red"]),
    ]]
    assert _where_lines(renders[0]) == [WHERE_PROVE_RED]


def test_sc1_1_at_approve_tests_the_where_line_stands_directly_under_the_waiting_line(
        tmp_path, capsys):
    root = _query_face_repo(tmp_path)
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert renders == [[
        WAIT_QUERY_FACE,
        WHERE_QUERY_FACE,
        "1 more: 1 to do",                            # pane-view
        whole["tree-view"],
        "  2 more: 2 to do",                          # tree-view/G0 inactive, tree-view/t5-pane-face
        short_line(whole["tree-view/t6-query-face"]),
        "    7 more: 7 to do",                        # six tasks and one check
        short_line(whole["tree-view/t6-query-face/approve-tests"]),
    ]]
    assert _where_lines(renders[0]) == [WHERE_QUERY_FACE]


def test_sc1_1_at_approve_commit_the_where_line_stands_directly_under_the_waiting_line(
        tmp_path, capsys):
    root = _repo(tmp_path, gates=())
    _progress(root, "alpha", _step("alpha/a2-edges/green", "done", "10:00"),
              _step("alpha/a2-edges/approve-commit", "doing", "10:01"))
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert renders == [[
        WAIT_APPROVE_COMMIT,
        WHERE_APPROVE_COMMIT,
        "1 more: 1 to do",                            # beta
        whole["alpha"],
        "  2 more: 2 to do",                          # alpha/G0 inactive, alpha/a1-core
        short_line(whole["alpha/a2-edges"]),
        "    9 more: 8 to do, 1 done",                # the other tasks and the checks
        short_line(whole["alpha/a2-edges/approve-commit"]),
    ]]


def test_sc1_1_the_where_line_names_a_contract_and_a_unit_whose_ids_carry_hyphens_and_digits(
        tmp_path, capsys):
    root = _hyphens_and_digits_repo(tmp_path)
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    where = "specs/pane-view-2/contract.yaml > pane-view-2 > p10-where-line-3 > two-key"
    assert renders == [[
        where,
        whole["pane-view-2"],
        "  2 more: 2 to do",                          # pane-view-2/G0 inactive, pane-view-2/p9-short-ids-2
        short_line(whole["pane-view-2/p10-where-line-3"]),
        "    7 more: 7 to do",                        # six tasks and one check
        short_line(whole["pane-view-2/p10-where-line-3/two-key"]),
    ]]
    assert where.isascii()


def test_sc1_1_the_where_line_follows_the_current_task_to_another_unit(tmp_path):
    root = _repo(tmp_path, gates=())
    first = _step("alpha/a1-core/write-tests", "doing", "10:00")
    _progress(root, "alpha", first)
    _, renders = _pane(root, lambda: _progress(
        root, "alpha", first, _step("alpha/a2-edges/prove-red", "doing", "10:01")))
    assert [render[0] for render in renders] == [WHERE_WRITE_TESTS, WHERE_PROVE_RED]
    assert [_where_lines(render) for render in renders] == [
        [WHERE_WRITE_TESTS], [WHERE_PROVE_RED]]


def test_sc1_1_the_where_line_follows_the_current_task_to_another_contract_and_its_place(
        tmp_path):
    root = _repo(tmp_path, gates=())
    _progress(root, "alpha", _step("alpha/a1-core/write-tests", "doing", "10:00"))
    approve = _step("beta/b1-solo/approve-commit", "doing", "10:01")
    _, renders = _pane(
        root,
        lambda: _progress(root, "beta", approve),                       # beta, at an approval
        lambda: _progress(root, "beta", approve,
                          _step("beta/b1-solo/commit", "doing", "10:02")))  # off it
    assert len(renders) == 3
    assert renders[0][0] == WHERE_WRITE_TESTS
    assert renders[1][:2] == [
        "waiting on a seat: approve-commit for beta/b1-solo",
        "specs/beta/contract.yaml > beta > b1-solo > approve-commit"]
    assert renders[2][0] == "specs/beta/contract.yaml > beta > b1-solo > commit"
    assert [len(_where_lines(render)) for render in renders] == [1, 1, 1]


def test_sc1_1_the_where_line_is_the_panes_alone_and_the_pane_still_writes_no_file(
        tmp_path, capsys):
    root = _path_repo(tmp_path)
    before = _snapshot(root)
    _, renders = _pane(root, lambda: _append(root / ".sdlc" / "config.yaml"), None)
    after = _snapshot(root)
    assert [render[0] for render in renders] == [WHERE_PROVE_RED, WHERE_PROVE_RED]
    assert all(line.isascii() for render in renders for line in render)
    # only the step's own edit changed a file; the pane wrote none
    before.pop(str(Path(".sdlc") / "config.yaml"))
    after.pop(str(Path(".sdlc") / "config.yaml"))
    assert after == before
    # the whole tree prints no where-am-I line
    code = main(["tree", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 0
    assert not any(line.startswith("specs/") or " > " in line for line in out.splitlines())


# --- SC1.2 the waiting line stays first, the cut, and no current task ----------------------

def test_sc1_2_the_waiting_line_stays_first_and_whole_while_a_wider_where_line_is_cut(
        tmp_path, monkeypatch):
    root = _query_face_repo(tmp_path)
    monkeypatch.setenv("COLUMNS", "64")  # the waiting line fits; the where-am-I line does not
    _, (render,) = _pane(root)
    assert render[0] == WAIT_QUERY_FACE
    assert render[1] == WHERE_QUERY_FACE[:61] + "..."
    assert len(render[1]) == 64
    assert all(len(line) <= 64 for line in render)


def test_sc1_2_a_where_line_exactly_the_panes_width_stays_whole_and_one_column_less_cuts_it(
        tmp_path, monkeypatch):
    root = _path_repo(tmp_path)
    width = len(WHERE_PROVE_RED)
    monkeypatch.setenv("COLUMNS", str(width))

    def narrower():
        monkeypatch.setenv("COLUMNS", str(width - 1))
        _append(root / ".sdlc" / "config.yaml")  # a change that moves no line

    _, renders = _pane(root, narrower)
    assert [render[0] for render in renders] == [
        WHERE_PROVE_RED, WHERE_PROVE_RED[:width - 4] + "..."]


def test_sc1_2_with_no_current_task_the_pane_prints_no_where_line(tmp_path):
    root = _repo(tmp_path, gates=())
    doing = _step("alpha/a1-core/write-tests", "doing", "10:00")
    _, renders = _pane(
        root,
        lambda: _progress(root, "alpha", doing),                                   # a task
        lambda: _progress(root, "alpha", doing, _step("alpha", "done", "10:05")))  # closed
    assert len(renders) == 3
    assert renders[0] == ["no current task", "2 items: 2 to do"]
    assert renders[1][0] == WHERE_WRITE_TESTS
    assert renders[2] == ["no current task", "2 items: 1 to do, 1 done"]


# --- SC3.1 short ids under a parent ------------------------------------------------------
#
# The pane's item lines are the lines that open, after their indent, on an id
# and its plain name, then ` [`; the where-am-I line, the waiting line and the fold lines are not
# item lines. On the path to the current task the top-level item is a
# contract, whose id has no `/`, the unit's id is `<contract>/<unit>` and the
# task's `<contract>/<unit>/<task>`.

PROVE_RED_UNIT = "  a2-edges the work for a2-edges is done [failed] depends_on: alpha/a1-core"
PROVE_RED_TASK = "    prove-red Prove red [doing] current"


def _item_lines(render):
    """(indent width, id) of each item line in a render, top to bottom."""
    rows = [ROW.match(line) for line in render]
    return [(len(row["indent"]), row["id"]) for row in rows if row is not None]


def test_sc3_1_a_unit_line_and_a_task_line_open_on_the_last_segment_of_their_ids(
        tmp_path, capsys):
    root = _path_repo(tmp_path)
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert renders == [[
        WHERE_PROVE_RED,
        "2 more: 1 to do, 1 done",
        f"alpha (no title) [failed] | {INTENT}",
        "  3 more: 1 to do, 1 done, 1 blocked",
        PROVE_RED_UNIT,                               # not `  alpha/a2-edges [failed] ...`
        "    9 more: 6 to do, 2 done, 1 failed",
        PROVE_RED_TASK,                               # not `    alpha/a2-edges/prove-red ...`
    ]]
    # after the short id, each line reads as the whole tree's line for its item
    assert whole["alpha/a2-edges"] == (
        "  alpha/a2-edges the work for a2-edges is done [failed] depends_on: alpha/a1-core")
    assert whole["alpha/a2-edges/prove-red"] == (
        "    alpha/a2-edges/prove-red Prove red [doing] current")


def test_sc3_1_the_top_level_line_opens_on_its_full_id_and_every_line_under_it_on_a_last_segment(
        tmp_path, capsys):
    root = _query_face_repo(tmp_path)
    _, (render,) = _pane(root)
    whole = _whole(root, capsys)
    # the request's own example: `t6-query-face`, `approve-tests`
    assert _item_lines(render) == [
        (0, "tree-view"), (2, "t6-query-face"), (4, "approve-tests")]
    assert render[3] == whole["tree-view"] == f"tree-view (no title) [waiting on a seat] | {INTENT}"
    assert render[5] == ("  t6-query-face the work for t6-query-face is done [waiting on a seat] "
                         "depends_on: tree-view/t5-pane-face")
    assert render[7] == "    approve-tests Approve the test list [waiting on a seat] current"


def test_sc3_1_ids_whose_segments_carry_hyphens_and_digits_open_on_their_whole_last_segment(
        tmp_path, capsys):
    root = _hyphens_and_digits_repo(tmp_path)
    _, (render,) = _pane(root)
    assert _item_lines(render) == [
        (0, "pane-view-2"), (2, "p10-where-line-3"), (4, "two-key")]
    assert render[1] == f"pane-view-2 (no title) [doing] | {INTENT}"
    assert render[3] == ("  p10-where-line-3 the work for p10-where-line-3 is done [doing]"
                         " depends_on: pane-view-2/p9-short-ids-2")
    assert render[5] == "    two-key Two-Key PASS [doing] current"


def test_sc3_1_only_the_opening_id_shortens_and_a_plain_name_that_names_a_full_id_keeps_it(
        tmp_path, capsys):
    root = _repo(tmp_path, gates=())
    edges = _unit("a2-edges", ["verify an edge holds"], depends_on=["a1-core"])
    edges["done_means"] = "alpha/a2-edges is done when alpha/a1-core is"
    _dump(root / "specs" / "alpha" / "contract.yaml",
          _contract("alpha", [ALPHA[0], edges]))
    _progress(root, "alpha", _step("alpha/a2-edges/write-tests", "doing", "10:00"))
    _, (render,) = _pane(root)
    whole = _whole(root, capsys)
    assert render[-3] == ("  a2-edges alpha/a2-edges is done when alpha/a1-core is [doing]"
                          " depends_on: alpha/a1-core")
    assert render[-1] == "    write-tests Write the tests [doing] current"
    assert render[-3] == short_line(whole["alpha/a2-edges"])


def test_sc3_1_the_cut_to_the_panes_width_applies_to_the_shortened_line(
        tmp_path, monkeypatch):
    root = _path_repo(tmp_path)
    width = len(PROVE_RED_TASK)   # the task's short line fits exactly; its full line would not
    monkeypatch.setenv("COLUMNS", str(width))
    _, (render,) = _pane(root)
    assert render[-1] == PROVE_RED_TASK
    assert render[-3] == PROVE_RED_UNIT[:width - 3] + "..."
    assert render == cut_lines([
        WHERE_PROVE_RED, "2 more: 1 to do, 1 done", f"alpha (no title) [failed] | {INTENT}",
        "  3 more: 1 to do, 1 done, 1 blocked", PROVE_RED_UNIT,
        "    9 more: 6 to do, 2 done, 1 failed", PROVE_RED_TASK], width)


def test_sc3_1_the_short_ids_follow_the_current_task_to_another_unit_and_another_contract(
        tmp_path):
    root = _repo(tmp_path, gates=())
    first = _step("alpha/a1-core/write-tests", "doing", "10:00")
    _progress(root, "alpha", first)
    _, renders = _pane(
        root,
        lambda: _progress(root, "alpha", first,
                          _step("alpha/a2-edges/prove-red", "doing", "10:01")),
        lambda: _progress(root, "beta", _step("beta/b1-solo/commit", "doing", "10:02")))
    assert [_item_lines(render) for render in renders] == [
        [(0, "alpha"), (2, "a1-core"), (4, "write-tests")],
        [(0, "alpha"), (2, "a2-edges"), (4, "prove-red")],
        [(0, "beta"), (2, "b1-solo"), (4, "commit")],
    ]
    assert renders[2][-3:] == [
        "  b1-solo the work for b1-solo is done [doing]",
        "    7 more: 7 to do",                        # six tasks and one check
        "    commit Commit [doing] current",
    ]


# --- SC3.2 full ids everywhere else -------------------------------------------------------

SOLO_TREE = f"""\
solo-2 (no title) [waiting on a seat] | {INTENT}
  solo-2/G0 Planning / Intake [to do] inactive
    solo-2/G0/G0.1 Definition-of-ready [to do]
    solo-2/G0/G0.2 Vocabulary coverage [to do]
    solo-2/G0/G0.3 Unit confirmation [to do]
  solo-2/s1-base the work for s1-base is done [done] at {HEAD}
    solo-2/s1-base/approve-tests Approve the test list [done]
    solo-2/s1-base/write-tests Write the tests [done]
    solo-2/s1-base/prove-red Prove red [done]
    solo-2/s1-base/green Green [done]
    solo-2/s1-base/approve-commit Approve the commit [done]
    solo-2/s1-base/commit Commit [done]
    solo-2/s1-base/two-key Two-Key PASS [done]
    solo-2/s1-base/SC3.1 verify it holds (SC3.1) [done]
  solo-2/s2-top the work for s2-top is done [waiting on a seat] depends_on: solo-2/s1-base
    solo-2/s2-top/approve-tests Approve the test list [waiting on a seat] current
    solo-2/s2-top/write-tests Write the tests [to do]
    solo-2/s2-top/prove-red Prove red [to do]
    solo-2/s2-top/green Green [to do]
    solo-2/s2-top/approve-commit Approve the commit [to do]
    solo-2/s2-top/commit Commit [to do]
    solo-2/s2-top/two-key Two-Key PASS [to do]
    solo-2/s2-top/SC3.2 verify it stays (SC3.2) [to do]
"""


def _solo_repo(tmp_path):
    """solo-2: s1-base closed, s2-top at approve-tests; no active gate."""
    root = tmp_path / "repo"
    _config(root, [])
    _dump(root / "specs" / "solo-2" / "contract.yaml", _contract("solo-2", [
        _unit("s1-base", ["verify it holds (SC3.1)"]),
        _unit("s2-top", ["verify it stays (SC3.2)"], depends_on=["s1-base"]),
    ]))
    write_seat_roster(root)
    _progress(root, "solo-2", _step("solo-2/s1-base", "done", "09:00"),
              _step("solo-2/s2-top/approve-tests", "doing", "10:00"))
    return root


def test_sc3_2_taskcontract_tree_prints_the_same_bytes_with_every_id_full(tmp_path, capsys):
    root = _solo_repo(tmp_path)
    _, (render,) = _pane(root)
    capsys.readouterr()
    code = main(["tree", "--root", str(root)])
    printed = capsys.readouterr()
    assert code == 0
    assert printed.out == SOLO_TREE
    assert printed.err == ""
    # the pane beside it shortens the same two items the tree prints whole
    assert render[-3:] == [
        "  s2-top the work for s2-top is done [waiting on a seat] depends_on: solo-2/s1-base",
        "    7 more: 7 to do",                        # six tasks and one check
        "    approve-tests Approve the test list [waiting on a seat] current",
    ]


class _Starts:
    """The spy on subprocess.Popen: each start through the shell notes its
    `SDLC_NODE` and returns a process that has already ended with 0; every
    other call passes through."""

    def __init__(self, real):
        self.real = real
        self.nodes = []

    def __call__(self, args, *more, **kwargs):
        if not kwargs.get("shell"):
            return self.real(args, *more, **kwargs)
        self.nodes.append((kwargs.get("env") or {}).get("SDLC_NODE"))
        return _Ended()


class _Ended:
    returncode = 0

    def poll(self):
        return 0

    def wait(self, timeout=None):
        return 0


def test_sc3_2_at_an_approval_the_waiting_line_and_sdlc_node_keep_the_full_ids(
        tmp_path, capsys, monkeypatch):
    starts = _Starts(subprocess.Popen)
    monkeypatch.setattr(subprocess, "Popen", starts)
    root = _repo(tmp_path, gates=())
    _config(root, [], tree={"notify": "notify-the-seat"})
    _progress(root, "alpha", _step("alpha/a2-edges/green", "done", "10:00"),
              _step("alpha/a2-edges/approve-commit", "doing", "10:01"))
    _, (render,) = _pane(root)
    assert render[0] == WAIT_APPROVE_COMMIT          # `for alpha/a2-edges`, whole
    assert starts.nodes == ["alpha/a2-edges/approve-commit"]
    assert capsys.readouterr().err == ""
    assert render[-3] == ("  a2-edges the work for a2-edges is done [waiting on a seat]"
                          " depends_on: alpha/a1-core")
    assert render[-1] == "    approve-commit Approve the commit [waiting on a seat] current"


def test_sc3_2_every_depends_on_link_on_a_short_unit_line_keeps_its_full_id(tmp_path):
    root = tmp_path / "repo"
    _config(root, [])
    _dump(root / "specs" / "gamma-7" / "contract.yaml", _contract("gamma-7", [
        _unit("g1-first", ["verify it holds"]),
        _unit("g2-second", ["verify it holds"]),
        _unit("g3-third", ["verify it holds"], depends_on=["g1-first", "g2-second"]),
    ]))
    write_seat_roster(root)
    _progress(root, "gamma-7", _step("gamma-7/g3-third/prove-red", "doing", "10:00"))
    _, (render,) = _pane(root)
    assert render[-3] == ("  g3-third the work for g3-third is done [doing] depends_on: gamma-7/g1-first"
                          " depends_on: gamma-7/g2-second")
    assert render[0] == "specs/gamma-7/contract.yaml > gamma-7 > g3-third > prove-red"


# --- SC2 the parts of an item line ----------------------------------------------------
#
# `tree: pane: parts:` in .sdlc/config.yaml lists the fields each item line
# of the pane shows after its id. On the fixture's path every field but
# evidence shows on some line: the contract's status, doc reference and
# summary, the unit's status, depends_on link and summary, the task's status,
# `current` mark and summary. The path never carries evidence: the current
# task is doing, to do or waiting on a seat, never done or blocked by its own
# record, and its unit and contract read done only when every child does. So
# evidence's place in the order shows only as nothing where it stands.

PARTS_IGNORED = ("taskcontract tree: pane parts ignored: {} - give a list from id, "
                 "status, marks, evidence, links, doc, summary")
UNREADABLE_BETA = re.compile(
    r"^taskcontract tree: unreadable progress: \.sdlc/progress/beta\.yaml \(.+\)$")

# each item line opens on its id and its plain name (project-tree o2)
ALPHA_NAMED = "alpha (no title)"
UNIT_NAMED = "  a2-edges the work for a2-edges is done"
TASK_NAMED = "    prove-red Prove red"
FULL_CONTRACT = f"{ALPHA_NAMED} [doing] doc: docs/features/alpha.md | {INTENT}"
FULL_UNIT = f"{UNIT_NAMED} [doing] depends_on: alpha/a1-core"
FULL_TASK = f"{TASK_NAMED} [doing] current"


def _doc_render(contract, unit, task):
    """The fixture's pane with the given item lines: the where-am-I line and
    the three fold lines as p1 and p2 print them."""
    return [
        WHERE_PROVE_RED,
        "1 more: 1 to do",                            # beta
        contract,
        "  2 more: 1 to do, 1 doing",                 # alpha/G0 inactive, alpha/a1-core
        unit,
        "    9 more: 9 to do",                        # the other tasks and the checks
        task,
    ]


FULL = _doc_render(FULL_CONTRACT, FULL_UNIT, FULL_TASK)
BARE = _doc_render(ALPHA_NAMED, UNIT_NAMED, TASK_NAMED)
STATUS_ONLY = _doc_render(f"{ALPHA_NAMED} [doing]", f"{UNIT_NAMED} [doing]",
                          f"{TASK_NAMED} [doing]")


def _doc_repo(tmp_path):
    """alpha and beta, no active gate, alpha's feature doc on disk; the
    current task is alpha/a2-edges/prove-red, doing, not an approval."""
    root = _repo(tmp_path, gates=())
    _append(root / "docs" / "features" / "alpha.md", "# Alpha\n")
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "10:00", by="user"),
              _step("alpha/a2-edges/prove-red", "doing", "10:04"))
    return root


def _parts(root, parts, gates=(), **tree):
    """The config with `tree: pane: parts:` set to `parts`, beside any other
    `tree:` key given."""
    _config(root, gates, tree={**tree, "pane": {"parts": parts}})


def _err_at_each_tick(capsys, *steps):
    """(the stderr noted at each tick, the steps to hand the pane): each tick
    notes the stderr printed since the last, then runs its step."""
    errs = []

    def noting(step):
        def run():
            errs.append(capsys.readouterr().err)
            if step is not None:
                step()
        return run

    return errs, [noting(step) for step in steps]


# --- SC2.1 the listed fields, in the fixed order ----------------------------------------

ALONE = [
    pytest.param("status", (f"{ALPHA_NAMED} [doing]", f"{UNIT_NAMED} [doing]",
                            f"{TASK_NAMED} [doing]"), id="status"),
    pytest.param("marks", (ALPHA_NAMED, UNIT_NAMED, f"{TASK_NAMED} current"), id="marks"),
    pytest.param("evidence", (ALPHA_NAMED, UNIT_NAMED, TASK_NAMED), id="evidence"),
    pytest.param("links", (ALPHA_NAMED, f"{UNIT_NAMED} depends_on: alpha/a1-core", TASK_NAMED),
                 id="links"),
    pytest.param("doc", (f"{ALPHA_NAMED} doc: docs/features/alpha.md", UNIT_NAMED, TASK_NAMED),
                 id="doc"),
    # only a contract has a summary: every other item's source text is its plain name
    pytest.param("summary", (f"{ALPHA_NAMED} | {INTENT}", UNIT_NAMED, TASK_NAMED),
                 id="summary"),
]


@pytest.mark.parametrize("field, lines", ALONE)
def test_sc2_1_each_field_alone_shows_the_id_then_that_field_and_nothing_where_the_item_lacks_it(
        tmp_path, capsys, field, lines):
    root = _doc_repo(tmp_path)
    _parts(root, [field])
    _, renders = _pane(root)
    assert renders == [_doc_render(*lines)]
    assert capsys.readouterr().err == ""


def test_sc2_1_each_field_shown_reads_exactly_as_on_the_whole_trees_line(tmp_path, capsys):
    root = _doc_repo(tmp_path)
    whole = _whole(root, capsys)
    _parts(root, ["doc", "links", "evidence", "marks", "status"])   # all but summary
    _, (render,) = _pane(root)
    assert capsys.readouterr().err == ""
    # each item line is the whole tree's line, short id first, up to its summary
    assert render[2] == whole["alpha"].split(" | ")[0]
    assert render[4] == short_line(whole["alpha/a2-edges"]).split(" | ")[0]
    assert render[6] == short_line(whole["alpha/a2-edges/prove-red"]).split(" | ")[0]
    assert render == _doc_render(f"{ALPHA_NAMED} [doing] doc: docs/features/alpha.md",
                                 f"{UNIT_NAMED} [doing] depends_on: alpha/a1-core",
                                 f"{TASK_NAMED} [doing] current")


ORDERS = [
    pytest.param(["summary", "links", "status"],
                 (f"{ALPHA_NAMED} [doing] | {INTENT}",
                  f"{UNIT_NAMED} [doing] depends_on: alpha/a1-core", f"{TASK_NAMED} [doing]"),
                 id="summary-links-status"),
    pytest.param(["summary", "marks", "doc"],
                 (f"{ALPHA_NAMED} doc: docs/features/alpha.md | {INTENT}",
                  UNIT_NAMED,
                  f"{TASK_NAMED} current"),
                 id="summary-marks-doc"),
    pytest.param(["links", "marks", "status"],
                 (f"{ALPHA_NAMED} [doing]", f"{UNIT_NAMED} [doing] depends_on: alpha/a1-core",
                  f"{TASK_NAMED} [doing] current"),
                 id="links-marks-status"),
]


@pytest.mark.parametrize("parts, lines", ORDERS)
def test_sc2_1_the_fields_keep_the_fixed_order_whatever_order_the_list_gives(
        tmp_path, capsys, parts, lines):
    root = _doc_repo(tmp_path)
    _parts(root, parts)
    _, renders = _pane(root)
    assert renders == [_doc_render(*lines)]
    assert capsys.readouterr().err == ""


LISTING_ID = [
    pytest.param(["id"], BARE, id="id-alone-reads-as-the-empty-list"),
    pytest.param(["id", "status"], STATUS_ONLY, id="id-and-status-reads-as-status"),
    pytest.param(["status", "id"], STATUS_ONLY, id="status-and-id-reads-as-status"),
]


@pytest.mark.parametrize("parts, render", LISTING_ID)
def test_sc2_1_listing_id_changes_nothing(tmp_path, capsys, parts, render):
    root = _doc_repo(tmp_path)
    _parts(root, parts)
    _, renders = _pane(root)
    assert renders == [render]
    assert capsys.readouterr().err == ""


def test_sc2_1_an_empty_list_shows_the_id_and_the_plain_name_on_the_top_level_the_unit_and_the_task_lines(
        tmp_path, capsys):
    root = _doc_repo(tmp_path)
    _parts(root, [])
    _, renders = _pane(root)
    assert renders == [BARE]
    # the top-level line keeps its full id; the unit and the task their last
    # segments; each then its plain name, which parts never leaves out
    assert [renders[0][2], renders[0][4], renders[0][6]] == [
        "alpha (no title)", "  a2-edges the work for a2-edges is done", "    prove-red Prove red"]
    assert capsys.readouterr().err == ""


def test_sc2_1_a_repeated_name_shows_its_field_once(tmp_path, capsys):
    root = _doc_repo(tmp_path)
    _parts(root, ["marks", "status", "marks", "status"])
    _, renders = _pane(root)
    assert renders == [_doc_render(f"{ALPHA_NAMED} [doing]", f"{UNIT_NAMED} [doing]",
                                   f"{TASK_NAMED} [doing] current")]
    assert capsys.readouterr().err == ""


def test_sc2_1_each_depends_on_link_of_a_unit_line_prints_after_one_space(tmp_path, capsys):
    root = tmp_path / "repo"
    _dump(root / "specs" / "gamma-7" / "contract.yaml", _contract("gamma-7", [
        _unit("g1-first", ["verify it holds"]),
        _unit("g2-second", ["verify it holds"]),
        _unit("g3-third", ["verify it holds"], depends_on=["g1-first", "g2-second"]),
    ]))
    write_seat_roster(root)
    _progress(root, "gamma-7", _step("gamma-7/g3-third/prove-red", "doing", "10:00"))
    _parts(root, ["links"])
    _, (render,) = _pane(root)
    assert render == [
        "specs/gamma-7/contract.yaml > gamma-7 > g3-third > prove-red",
        "gamma-7 (no title)",
        "  3 more: 3 to do",                          # gamma-7/G0 inactive, g1-first, g2-second
        ("  g3-third the work for g3-third is done depends_on: gamma-7/g1-first"
         " depends_on: gamma-7/g2-second"),
        "    7 more: 7 to do",                        # six tasks and one check
        "    prove-red Prove red",
    ]
    assert capsys.readouterr().err == ""


# --- SC2.2 what the setting leaves unchanged ----------------------------------------------

UNSET = [
    pytest.param({}, id="no-tree-key"),
    pytest.param({"tree": {}}, id="a-tree-key-without-pane"),
    pytest.param({"tree": {"pane": {}}}, id="a-pane-key-without-parts"),
]


@pytest.mark.parametrize("config", UNSET)
def test_sc2_2_with_parts_unset_each_item_line_shows_every_field_it_has(
        tmp_path, capsys, config):
    root = _doc_repo(tmp_path)
    _config(root, [], **config)
    _, renders = _pane(
        root,
        lambda: _parts(root, []),                     # set: the id alone
        lambda: _config(root, [], **config))          # unset again
    assert renders == [FULL, BARE, FULL]
    # the where-am-I line and the fold lines read the same set or unset
    assert [[render[i] for i in (0, 1, 3, 5)] for render in renders] == [
        [WHERE_PROVE_RED, "1 more: 1 to do", "  2 more: 1 to do, 1 doing",
         "    9 more: 9 to do"]] * 3
    assert capsys.readouterr().err == ""


def test_sc2_2_a_missing_config_reads_as_parts_unset(tmp_path, capsys):
    root = _doc_repo(tmp_path)
    (root / ".sdlc" / "config.yaml").unlink()
    _, renders = _pane(root, lambda: _parts(root, []))
    assert renders == [FULL, BARE]
    assert capsys.readouterr().err == ""


NOT_A_MAPPING = [
    pytest.param({"tree": "status"}, id="tree-text"),
    pytest.param({"tree": ["pane"]}, id="tree-a-list"),
    pytest.param({"tree": {"pane": "status"}}, id="pane-text"),
    pytest.param({"tree": {"pane": ["status"]}}, id="pane-a-list"),
]


@pytest.mark.parametrize("config", NOT_A_MAPPING)
def test_sc2_2_a_tree_or_pane_key_that_is_not_a_mapping_reads_as_parts_unset_with_no_message(
        tmp_path, capsys, config):
    root = _doc_repo(tmp_path)
    _config(root, [], **config)
    errs, steps = _err_at_each_tick(capsys, lambda: _parts(root, []), None)
    _, renders = _pane(root, *steps)
    assert renders == [FULL, BARE]
    assert errs == ["", ""]


def test_sc2_2_at_an_approval_the_parts_leave_the_waiting_line_and_the_where_line_unchanged(
        tmp_path, capsys):
    root = _query_face_repo(tmp_path)
    _parts(root, ["status", "marks"])
    _, renders = _pane(root)
    # the request's own example, at t6's first approval
    assert renders == [[
        WAIT_QUERY_FACE,
        WHERE_QUERY_FACE,
        "1 more: 1 to do",                            # pane-view
        "tree-view (no title) [waiting on a seat]",
        "  2 more: 2 to do",                          # tree-view/G0 inactive, tree-view/t5-pane-face
        "  t6-query-face the work for t6-query-face is done [waiting on a seat]",
        "    7 more: 7 to do",                        # six tasks and one check
        "    approve-tests Approve the test list [waiting on a seat] current",
    ]]
    assert capsys.readouterr().err == ""


def test_sc2_2_with_no_current_task_the_parts_leave_the_render_unchanged(tmp_path, capsys):
    root = _repo(tmp_path, gates=())
    _parts(root, ["status"])
    doing = _step("alpha/a1-core/write-tests", "doing", "10:00")
    _, renders = _pane(
        root,
        lambda: _progress(root, "alpha", doing),                                   # a task
        lambda: _progress(root, "alpha", doing, _step("alpha", "done", "10:05")))  # closed
    assert len(renders) == 3
    assert renders[0] == ["no current task", "2 items: 2 to do"]
    assert renders[1] == [WHERE_WRITE_TESTS, "1 more: 1 to do", "alpha (no title) [doing]",
                          "  2 more: 2 to do", "  a1-core the work for a1-core is done [doing]",
                          "    8 more: 8 to do", "    write-tests Write the tests [doing]"]
    assert renders[2] == ["no current task", "2 items: 1 to do, 1 done"]
    assert capsys.readouterr().err == ""


def test_sc2_2_the_cut_to_the_panes_width_applies_to_the_line_as_parts_leaves_it(
        tmp_path, capsys, monkeypatch):
    root = _doc_repo(tmp_path)
    _parts(root, ["summary", "status"])
    unit = f"{UNIT_NAMED} [doing]"
    width = len(unit)          # the unit's line as parts leaves it fits exactly; its full line would not
    assert len(FULL_UNIT) > width
    monkeypatch.setenv("COLUMNS", str(width))
    _, (render,) = _pane(root)
    assert render[4] == unit
    assert render == cut_lines(_doc_render(f"{ALPHA_NAMED} [doing] | {INTENT}", unit,
                                           f"{TASK_NAMED} [doing]"), width)
    assert render[2] == f"{ALPHA_NAMED} [doing] | {INTENT}"[:width - 3] + "..."
    assert capsys.readouterr().err == ""


def test_sc2_2_the_notify_command_keeps_working_beside_the_pane_key(
        tmp_path, capsys, monkeypatch):
    starts = _Starts(subprocess.Popen)
    monkeypatch.setattr(subprocess, "Popen", starts)
    root = _repo(tmp_path, gates=())
    _parts(root, ["status"], notify="notify-the-seat")
    _progress(root, "alpha", _step("alpha/a2-edges/green", "done", "10:00"),
              _step("alpha/a2-edges/approve-commit", "doing", "10:01"))
    _, (render,) = _pane(root)
    assert render == [
        WAIT_APPROVE_COMMIT,
        WHERE_APPROVE_COMMIT,
        "1 more: 1 to do",                            # beta
        "alpha (no title) [waiting on a seat]",
        "  2 more: 2 to do",                          # alpha/G0 inactive, alpha/a1-core
        "  a2-edges the work for a2-edges is done [waiting on a seat]",
        "    9 more: 8 to do, 1 done",                # the other tasks and the checks
        "    approve-commit Approve the commit [waiting on a seat]",
    ]
    assert starts.nodes == ["alpha/a2-edges/approve-commit"]
    assert capsys.readouterr().err == ""


WHOLE_TREE = [
    pytest.param(["status"], id="a-valid-parts"),
    pytest.param(["status", "colour"], id="a-bad-parts"),
]


@pytest.mark.parametrize("parts", WHOLE_TREE)
def test_sc2_2_taskcontract_tree_prints_the_same_stdout_and_stderr_with_parts_set(
        tmp_path, capsys, parts):
    root = _doc_repo(tmp_path)
    (root / ".sdlc" / "progress" / "beta.yaml").write_text("records: [unclosed\n",
                                                           encoding="utf-8")
    _parts(root, parts)
    _, (render,) = _pane(root)
    pane_err = capsys.readouterr().err.splitlines()
    # the pane reads the key: only the --follow mode does
    if parts == ["status"]:
        assert render == STATUS_ONLY
        assert len(pane_err) == 1 and UNREADABLE_BETA.match(pane_err[0]), pane_err
    else:
        assert render == FULL
        assert pane_err[1:] == [PARTS_IGNORED.format("colour")], pane_err
    code = main(["tree", "--root", str(root)])
    with_key = capsys.readouterr()
    assert code == 0
    _config(root, [])
    code = main(["tree", "--root", str(root)])
    without_key = capsys.readouterr()
    assert code == 0
    assert with_key.out == without_key.out
    assert with_key.err == without_key.err
    assert "pane parts ignored" not in with_key.err
    assert UNREADABLE_BETA.match(with_key.err.splitlines()[0])


# --- SC2.3 a bad parts setting ----------------------------------------------------------------

BAD = [
    pytest.param("status", "status", id="text"),
    pytest.param(3, "3", id="a-number"),
    pytest.param({"a": "b"}, "{'a': 'b'}", id="a-mapping"),
    pytest.param(None, "None", id="null"),
    pytest.param(["status", "colour"], "colour", id="an-unknown-entry-after-a-known-one"),
    pytest.param(["status", "colour", "shade"], "colour", id="the-first-unknown-entry"),
    pytest.param(["Status"], "Status", id="a-name-in-another-case"),
    pytest.param(["status", 3], "3", id="an-entry-that-is-not-text"),
]


@pytest.mark.parametrize("value, named", BAD)
def test_sc2_3_a_bad_parts_is_ignored_as_a_whole_and_named_on_stderr(
        tmp_path, capsys, value, named):
    root = _doc_repo(tmp_path)
    _parts(root, value)
    _, renders = _pane(root)
    assert renders == [FULL]                          # every field, as if unset
    message = PARTS_IGNORED.format(named)
    assert capsys.readouterr().err == message + "\n"
    assert message.isascii()


def test_sc2_3_the_message_prints_once_at_each_render_and_the_pane_writes_no_file(
        tmp_path, capsys):
    root = _doc_repo(tmp_path)
    _parts(root, ["status", "colour"])
    before = _snapshot(root)
    errs, steps = _err_at_each_tick(
        capsys,
        lambda: _append(root / ".sdlc" / "progress" / "alpha.yaml"),   # a redraw
        None,                                                          # no change, no render
        None)
    _, renders = _pane(root, *steps)
    message = PARTS_IGNORED.format("colour") + "\n"
    assert renders == [FULL, FULL]
    assert errs == [message, message, ""]
    after = _snapshot(root)
    before.pop(str(Path(".sdlc") / "progress" / "alpha.yaml"))
    after.pop(str(Path(".sdlc") / "progress" / "alpha.yaml"))
    assert after == before


def test_sc2_3_a_change_to_parts_shows_at_the_next_render_and_the_message_follows_the_value(
        tmp_path, capsys):
    root = _doc_repo(tmp_path)
    _parts(root, "status")
    errs, steps = _err_at_each_tick(
        capsys,
        lambda: _parts(root, []),                     # valid: the id alone, no message
        lambda: _parts(root, ["summary", "shade"]),   # bad again, another value
        lambda: _config(root, []),                    # unset: no message
        None)
    _, renders = _pane(root, *steps)
    assert renders == [FULL, BARE, FULL, FULL]
    assert errs == [PARTS_IGNORED.format("status") + "\n", "",
                    PARTS_IGNORED.format("shade") + "\n", ""]


def test_sc2_3_the_message_follows_the_renders_unreadable_source_lines(tmp_path, capsys):
    root = _doc_repo(tmp_path)
    (root / ".sdlc" / "progress" / "beta.yaml").write_text("records: [unclosed\n",
                                                           encoding="utf-8")
    _parts(root, 3)
    errs, steps = _err_at_each_tick(
        capsys, lambda: _append(root / ".sdlc" / "progress" / "alpha.yaml"), None)
    _, renders = _pane(root, *steps)
    assert len(renders) == 2
    for err in errs:
        lines = err.splitlines()
        assert len(lines) == 2, lines
        assert UNREADABLE_BETA.match(lines[0]), lines
        assert lines[1] == PARTS_IGNORED.format("3")


# --- SC4 the fold lines ------------------------------------------------------------------
#
# `tree: pane: fold:` in .sdlc/config.yaml chooses what each fold line holds:
# the counts by status (`counts`, or no key), or each folded item by its id and
# status (`names`). Each fold line keeps its place and its indent; only the
# text after `<n> more: ` (or `<n> items`) changes.

FOLD_IGNORED = "taskcontract tree: pane fold ignored: {} - give names or counts"


def _fold(root, fold, gates=(), **pane):
    """The config with `tree: pane: fold:` set to `fold`, beside any other
    `tree: pane:` key given."""
    _config(root, gates, tree={"pane": {**pane, "fold": fold}})


def _no_gate_finding(root):
    """A finding with `gate: none`, so the top level holds a `gates/none` item."""
    _dump(root / ".sdlc" / "findings" / "idea.yaml", {
        "finding": "idea", "date": "2026-09-22", "kit_pinned": "v0.14.0",
        "diagnostic": "none", "gate": "none", "kind": "proposal", "count": 1,
        "statement": "A fixture finding for the pane-view suite.", "proposal": "none"})


def _named_repo(tmp_path):
    """The path fixture (gate G0 active, beta closed, alpha/a2-edges/prove-red
    doing) with a finding under the no-gate item, and `fold: names`: the top
    level holds gates/G0, gates/none, alpha and beta, in that order."""
    root = _path_repo(tmp_path)
    _no_gate_finding(root)
    _fold(root, "names", gates=("G0",))
    return root


# the ruling's own example: a gate item and the no-gate item by their full ids
NAMED_TOP = "3 more: gates/G0 [to do], gates/none [to do], beta [done]"
NAMED_UNITS = "  3 more: G0 [done], G1 [to do], a1-core [blocked]"  # alpha/G1 inactive
NAMED_TASKS = ("    9 more: approve-tests [done], write-tests [done], green [to do], "
               "approve-commit [to do], commit [to do], two-key [to do], sketch-1 [failed], "
               "SC2.1 [to do], sketch-3 [to do]")


def _path_render(top, units, tasks):
    """The path fixture's pane with the given fold lines."""
    return [WHERE_PROVE_RED, top, f"alpha (no title) [failed] | {INTENT}", units, PROVE_RED_UNIT,
            tasks, PROVE_RED_TASK]


NAMED = _path_render(NAMED_TOP, NAMED_UNITS, NAMED_TASKS)

# the feature-doc fixture of SC2 (no gate, beta to do, a1-core doing), named
DOC_NAMED_TASKS = ("    9 more: approve-tests [to do], write-tests [to do], green [to do], "
                   "approve-commit [to do], commit [to do], two-key [to do], "
                   "sketch-1 [to do], SC2.1 [to do], sketch-3 [to do]")
DOC_NAMED = [WHERE_PROVE_RED, "1 more: beta [to do]", FULL_CONTRACT,
             "  2 more: G0 [to do], a1-core [doing]", FULL_UNIT, DOC_NAMED_TASKS, FULL_TASK]


# --- SC4.1 fold names -------------------------------------------------------------------------

def test_sc4_1_fold_names_names_each_folded_item_by_id_and_status_at_all_three_depths(
        tmp_path, capsys):
    root = _named_repo(tmp_path)
    _, renders = _pane(root)
    assert capsys.readouterr().err == ""
    whole = _whole(root, capsys)
    assert renders == [[
        WHERE_PROVE_RED,
        NAMED_TOP,                                    # the top level
        whole["alpha"],
        NAMED_UNITS,                                  # the contract's verdict and other unit
        short_line(whole["alpha/a2-edges"]),
        NAMED_TASKS,                                  # the unit's other tasks and its checks
        short_line(whole["alpha/a2-edges/prove-red"]),
    ]]
    # each folded item reads as its own line opens: the id (whole at the top
    # level, else its last segment) and the status tag, in the whole tree's order
    for depth, fold, ids in (
            (0, NAMED_TOP, ["gates/G0", "gates/none", "beta"]),
            (1, NAMED_UNITS, ["alpha/G0", "alpha/G1", "alpha/a1-core"]),
            (2, NAMED_TASKS, [i for i in whole if i.startswith("alpha/a2-edges/")
                              and i != "alpha/a2-edges/prove-red"])):
        named = [(i if depth == 0 else i.rsplit("/", 1)[-1]) + f" [{ROW.match(whole[i])['tag']}]"
                 for i in ids]
        assert fold == "  " * depth + f"{len(ids)} more: " + ", ".join(named)
    assert all(line.isascii() for line in renders[0])


def test_sc4_1_a_check_whose_id_joins_check_ids_folds_by_its_whole_last_segment(
        tmp_path, capsys):
    root = _repo(tmp_path, gates=())
    _fold(root, "names")
    _progress(root, "alpha", _step("alpha/a1-core/write-tests", "doing", "10:00"))
    _, renders = _pane(root)
    assert renders == [[
        WHERE_WRITE_TESTS,
        "1 more: beta [to do]",
        f"alpha (no title) [doing] | {INTENT}",
        "  2 more: G0 [to do], a2-edges [to do]",
        "  a1-core the work for a1-core is done [doing]",
        ("    8 more: approve-tests [to do], prove-red [to do], green [to do], "
         "approve-commit [to do], commit [to do], two-key [to do], SC1.1 [to do], "
         "SC5.1+SC5.2 [to do]"),
        "    write-tests Write the tests [doing] current",
    ]]
    assert capsys.readouterr().err == ""


def test_sc4_1_at_an_approval_fold_names_leaves_the_waiting_line_the_where_line_and_the_notify_command(
        tmp_path, capsys, monkeypatch):
    starts = _Starts(subprocess.Popen)
    monkeypatch.setattr(subprocess, "Popen", starts)
    root = _query_face_repo(tmp_path)
    _config(root, [], tree={"notify": "notify-the-seat", "pane": {"fold": "names"}})
    _, renders = _pane(root)
    assert capsys.readouterr().err == ""
    whole = _whole(root, capsys)
    assert renders == [[
        WAIT_QUERY_FACE,
        WHERE_QUERY_FACE,
        "1 more: pane-view [to do]",
        whole["tree-view"],
        "  2 more: G0 [to do], t5-pane-face [to do]",
        short_line(whole["tree-view/t6-query-face"]),
        ("    7 more: write-tests [to do], prove-red [to do], green [to do], "
         "approve-commit [to do], commit [to do], two-key [to do], SC6.1 [to do]"),
        short_line(whole["tree-view/t6-query-face/approve-tests"]),
    ]]
    assert starts.nodes == ["tree-view/t6-query-face/approve-tests"]


def test_sc4_1_the_requests_own_example_at_80_columns_cuts_the_long_fold_line(
        tmp_path, capsys, monkeypatch):
    root = _query_face_repo(tmp_path)
    _fold(root, "names", parts=["status", "marks"])
    monkeypatch.setenv("COLUMNS", "80")
    _, renders = _pane(root)
    assert renders == [[
        WAIT_QUERY_FACE,
        WHERE_QUERY_FACE,
        "1 more: pane-view [to do]",
        "tree-view (no title) [waiting on a seat]",
        "  2 more: G0 [to do], t5-pane-face [to do]",
        "  t6-query-face the work for t6-query-face is done [waiting on a seat]",
        "    7 more: write-tests [to do], prove-red [to do], green [to do], approve-co...",
        "    approve-tests Approve the test list [waiting on a seat] current",
    ]]
    assert len(renders[0][6]) == 80
    assert capsys.readouterr().err == ""


def test_sc4_1_a_fold_line_under_names_is_cut_to_the_panes_width_like_every_other_line(
        tmp_path, capsys, monkeypatch):
    root = _named_repo(tmp_path)
    width = len(NAMED_TOP)        # the top-level fold line fits exactly; the tasks' does not
    monkeypatch.setenv("COLUMNS", str(width))

    def narrower():
        monkeypatch.setenv("COLUMNS", str(width - 1))
        _append(root / ".sdlc" / "config.yaml")  # a change that moves no line

    _, renders = _pane(root, narrower)
    assert renders == [cut_lines(NAMED, width), cut_lines(NAMED, width - 1)]
    assert renders[0][1] == NAMED_TOP
    assert renders[0][5] == NAMED_TASKS[:width - 3] + "..."
    assert renders[1][1] == NAMED_TOP[:width - 4] + "..."
    assert capsys.readouterr().err == ""


LEAVE_STATUS_OUT = [
    pytest.param([], (ALPHA_NAMED, UNIT_NAMED, TASK_NAMED), id="the-empty-list"),
    pytest.param(["marks", "summary"],
                 (f"{ALPHA_NAMED} | {INTENT}", UNIT_NAMED, f"{TASK_NAMED} current"),
                 id="marks-and-summary"),
]


@pytest.mark.parametrize("parts, lines", LEAVE_STATUS_OUT)
def test_sc4_1_a_parts_that_leaves_status_out_never_changes_a_fold_line(
        tmp_path, capsys, parts, lines):
    root = _doc_repo(tmp_path)
    _fold(root, "names", parts=parts)
    _, renders = _pane(root)
    contract, unit, task = lines
    # the item lines as parts leaves them; each folded item still shows its status
    assert renders == [[WHERE_PROVE_RED, "1 more: beta [to do]", contract,
                        "  2 more: G0 [to do], a1-core [doing]", unit, DOC_NAMED_TASKS, task]]
    assert capsys.readouterr().err == ""


def test_sc4_1_with_no_current_task_the_items_line_names_the_top_level_items(tmp_path, capsys):
    root = _repo(tmp_path)                            # gate G0 active
    _no_gate_finding(root)
    _fold(root, "names", gates=("G0",))
    doing = _step("alpha/a1-core/write-tests", "doing", "10:00")
    _, renders = _pane(
        root,
        lambda: _progress(root, "alpha", doing),                                   # a task
        lambda: _progress(root, "alpha", doing, _step("alpha", "done", "10:05")))  # closed
    assert len(renders) == 3
    assert renders[0] == [
        "no current task",
        "4 items: gates/G0 [to do], gates/none [to do], alpha [to do], beta [to do]"]
    assert renders[1][:4] == [
        WHERE_WRITE_TESTS,
        "3 more: gates/G0 [to do], gates/none [to do], beta [to do]",
        f"alpha (no title) [doing] | {INTENT}",
        "  3 more: G0 [done], G1 [to do], a2-edges [to do]"]
    assert renders[2] == [
        "no current task",
        "4 items: gates/G0 [to do], gates/none [to do], alpha [done], beta [to do]"]
    assert capsys.readouterr().err == ""


def test_sc4_1_with_no_item_at_all_the_items_line_reads_0_items_and_names_the_first_that_lands(
        tmp_path, capsys):
    root = tmp_path / "repo"
    _fold(root, "names")

    def land():
        _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA))
        write_seat_roster(root)

    _, renders = _pane(root, land)
    assert renders == [["no current task", "0 items"],
                       ["no current task", "1 items: beta [to do]"]]
    assert capsys.readouterr().err == ""


# --- SC4.2 counts, and a bad fold setting -------------------------------------------------------

def _unlink_config(root):
    (root / ".sdlc" / "config.yaml").unlink()


COUNTS = [
    pytest.param(lambda root: _fold(root, "counts"), id="fold-counts"),
    pytest.param(lambda root: _config(root, [], tree={"pane": {}}), id="a-pane-key-without-fold"),
    pytest.param(lambda root: _config(root, [], tree={}), id="a-tree-key-without-pane"),
    pytest.param(lambda root: _config(root, []), id="no-tree-key"),
    pytest.param(_unlink_config, id="no-config"),
    pytest.param(lambda root: _config(root, [], tree="names"), id="tree-text"),
    pytest.param(lambda root: _config(root, [], tree=["pane"]), id="tree-a-list"),
    pytest.param(lambda root: _config(root, [], tree={"pane": "names"}), id="pane-text"),
    pytest.param(lambda root: _config(root, [], tree={"pane": ["fold", "names"]}),
                 id="pane-a-list"),
]


@pytest.mark.parametrize("setting", COUNTS)
def test_sc4_2_fold_counts_or_no_fold_keeps_the_counts_with_nothing_on_stderr_for_the_key(
        tmp_path, capsys, setting):
    root = _doc_repo(tmp_path)
    setting(root)
    errs, steps = _err_at_each_tick(
        capsys,
        lambda: _fold(root, "names"),                 # names: the items by id
        lambda: setting(root),                        # back: the counts
        None)
    _, renders = _pane(root, *steps)
    assert renders == [FULL, DOC_NAMED, FULL]
    assert errs == ["", "", ""]


BAD_FOLD = [
    pytest.param("sideways", "sideways", id="another-word"),
    pytest.param("Names", "Names", id="names-in-another-case"),
    pytest.param("COUNTS", "COUNTS", id="counts-in-another-case"),
    pytest.param(3, "3", id="a-number"),
    pytest.param(["names"], "['names']", id="a-list"),
    pytest.param({"names": "counts"}, "{'names': 'counts'}", id="a-mapping"),
    pytest.param(None, "None", id="null"),
]


@pytest.mark.parametrize("value, named", BAD_FOLD)
def test_sc4_2_a_bad_fold_keeps_the_counts_and_names_the_value_on_stderr(
        tmp_path, capsys, value, named):
    root = _doc_repo(tmp_path)
    _fold(root, value)
    _, renders = _pane(root)
    assert renders == [FULL]                          # the counts, as if unset
    message = FOLD_IGNORED.format(named)
    assert capsys.readouterr().err == message + "\n"
    assert message.isascii()


def test_sc4_2_the_fold_message_prints_once_at_each_render_and_the_pane_writes_no_file(
        tmp_path, capsys):
    root = _doc_repo(tmp_path)
    _fold(root, "sideways")
    before = _snapshot(root)
    errs, steps = _err_at_each_tick(
        capsys,
        lambda: _append(root / ".sdlc" / "progress" / "alpha.yaml"),   # a redraw
        None,                                                          # no change, no render
        None)
    _, renders = _pane(root, *steps)
    message = FOLD_IGNORED.format("sideways") + "\n"
    assert renders == [FULL, FULL]
    assert errs == [message, message, ""]
    after = _snapshot(root)
    before.pop(str(Path(".sdlc") / "progress" / "alpha.yaml"))
    after.pop(str(Path(".sdlc") / "progress" / "alpha.yaml"))
    assert after == before


def test_sc4_2_a_change_to_fold_shows_at_the_next_render_and_the_message_follows_the_value(
        tmp_path, capsys):
    root = _doc_repo(tmp_path)
    _fold(root, "counts")
    errs, steps = _err_at_each_tick(
        capsys,
        lambda: _fold(root, "names"),                 # the items by id, no message
        lambda: _fold(root, "Names"),                 # bad: the counts, named
        lambda: _fold(root, 3),                       # bad again, another value
        lambda: _config(root, []),                    # unset: the counts, no message
        None)
    _, renders = _pane(root, *steps)
    assert renders == [FULL, DOC_NAMED, FULL, FULL, FULL]
    assert errs == ["", "", FOLD_IGNORED.format("Names") + "\n",
                    FOLD_IGNORED.format("3") + "\n", ""]


def test_sc4_2_a_bad_parts_leaves_fold_names_working_and_a_bad_fold_leaves_parts_working(
        tmp_path, capsys):
    root = _doc_repo(tmp_path)
    _fold(root, "names", parts="status")              # parts bad, fold good
    errs, steps = _err_at_each_tick(
        capsys,
        lambda: _fold(root, "sideways", parts=[]),    # parts good, fold bad
        lambda: _fold(root, "sideways", parts="status"),  # both bad
        None)
    _, renders = _pane(root, *steps)
    assert renders == [DOC_NAMED, BARE, FULL]
    assert errs == [PARTS_IGNORED.format("status") + "\n",
                    FOLD_IGNORED.format("sideways") + "\n",
                    PARTS_IGNORED.format("status") + "\n" + FOLD_IGNORED.format("sideways") + "\n"]


def test_sc4_2_the_fold_message_follows_the_unreadable_source_lines_and_the_parts_message(
        tmp_path, capsys):
    root = _doc_repo(tmp_path)
    (root / ".sdlc" / "progress" / "beta.yaml").write_text("records: [unclosed\n",
                                                           encoding="utf-8")
    _fold(root, ["names"], parts=3)
    errs, steps = _err_at_each_tick(
        capsys, lambda: _append(root / ".sdlc" / "progress" / "alpha.yaml"), None)
    _, renders = _pane(root, *steps)
    assert renders == [FULL, FULL]
    for err in errs:
        lines = err.splitlines()
        assert len(lines) == 3, lines
        assert UNREADABLE_BETA.match(lines[0]), lines
        assert lines[1:] == [PARTS_IGNORED.format("3"), FOLD_IGNORED.format("['names']")]


FOLD_WHOLE_TREE = [
    pytest.param("names", id="fold-names"),
    pytest.param("sideways", id="a-bad-fold"),
]


@pytest.mark.parametrize("fold", FOLD_WHOLE_TREE)
def test_sc4_2_taskcontract_tree_prints_the_same_stdout_and_stderr_with_fold_set(
        tmp_path, capsys, fold):
    root = _doc_repo(tmp_path)
    (root / ".sdlc" / "progress" / "beta.yaml").write_text("records: [unclosed\n",
                                                           encoding="utf-8")
    _fold(root, fold)
    _, (render,) = _pane(root)
    pane_err = capsys.readouterr().err.splitlines()
    # the pane reads the key: only the --follow mode does
    if fold == "names":
        assert render == DOC_NAMED
        assert len(pane_err) == 1 and UNREADABLE_BETA.match(pane_err[0]), pane_err
    else:
        assert render == FULL
        assert pane_err[1:] == [FOLD_IGNORED.format("sideways")], pane_err
    code = main(["tree", "--root", str(root)])
    with_key = capsys.readouterr()
    assert code == 0
    _config(root, [])
    code = main(["tree", "--root", str(root)])
    without_key = capsys.readouterr()
    assert code == 0
    assert with_key.out == without_key.out
    assert with_key.err == without_key.err
    assert "pane fold ignored" not in with_key.err
    assert UNREADABLE_BETA.match(with_key.err.splitlines()[0])
