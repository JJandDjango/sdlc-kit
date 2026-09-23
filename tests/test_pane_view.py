"""The pane-view suite (contract pane-view, unit p1-where-line).

`taskcontract tree --follow` prints one where-am-I line for the current
task: `specs/<contract>/contract.yaml > <contract> > <unit> > <task>`, the
contract's file from the repository root with forward slashes, then the
contract's id, then the last segment of the unit's id and of the task's id,
joined by ` > `, with no indent. When the current task is `approve-tests` or
`approve-commit` the line stands directly under the waiting line, which stays
the pane's first line word for word; otherwise it is the pane's first line,
above the top-level fold line (SC1.1). A where-am-I line longer than the
pane's width is cut to the width and ends in `...`, as every pane line is,
and with no current task the pane prints none (SC1.2).

The rest of the pane reads as tree-view t7 and t8 built it: each item line
equals the whole tree's line for its item, and `taskcontract tree` prints no
where-am-I line. The loop runs in-process: `follow(root, out, sleep=...)`
takes an injected sleep, which changes source files between scans and raises
KeyboardInterrupt to end the loop, as Ctrl-C does. No test waits on a real
second.
"""

from __future__ import annotations

import importlib
import io
import re
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

tree_view = importlib.import_module("taskcontract.tree_view")

CLEAR = "\x1b[H\x1b[2J"  # cursor home, then clear the screen: every render opens on it
HEAD = "1a2b3c4"
INTENT = ("A fixture contract for the pane-view suite; its units carry the "
          "sketch shapes that check ids come from.")
ROW = re.compile(r"^(?P<indent> *)(?P<id>\S+) \[(?P<tag>[^\]]*)\](?P<rest>.*)$")

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
        "  2 more: 1 done, 1 blocked",                # alpha/G0, alpha/a1-core
        whole["alpha/a2-edges"],
        "    9 more: 6 to do, 2 done, 1 failed",      # the other tasks and the checks
        whole["alpha/a2-edges/prove-red"],
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
        "  1 more: 1 to do",                          # tree-view/t5-pane-face
        whole["tree-view/t6-query-face"],
        "    7 more: 7 to do",                        # six tasks and one check
        whole["tree-view/t6-query-face/approve-tests"],
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
        "  1 more: 1 to do",                          # alpha/a1-core
        whole["alpha/a2-edges"],
        "    9 more: 8 to do, 1 done",                # the other tasks and the checks
        whole["alpha/a2-edges/approve-commit"],
    ]]


def test_sc1_1_the_where_line_names_a_contract_and_a_unit_whose_ids_carry_hyphens_and_digits(
        tmp_path, capsys):
    root = tmp_path / "repo"
    _config(root, [])
    _dump(root / "specs" / "pane-view-2" / "contract.yaml", _contract("pane-view-2", [
        _unit("p9-short-ids-2", ["verify it holds (SC3.1)"]),
        _unit("p10-where-line-3", ["verify it reads (SC1.1)"], depends_on=["p9-short-ids-2"]),
    ]))
    write_seat_roster(root)
    _progress(root, "pane-view-2",
              _step("pane-view-2/p10-where-line-3/two-key", "doing", "10:00"))
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    where = "specs/pane-view-2/contract.yaml > pane-view-2 > p10-where-line-3 > two-key"
    assert renders == [[
        where,
        whole["pane-view-2"],
        "  1 more: 1 to do",                          # pane-view-2/p9-short-ids-2
        whole["pane-view-2/p10-where-line-3"],
        "    7 more: 7 to do",                        # six tasks and one check
        whole["pane-view-2/p10-where-line-3/two-key"],
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
