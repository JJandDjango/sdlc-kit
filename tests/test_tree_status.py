"""The status suite for ADR 0031 (contract tree-view, unit t3-status-and-cursor).

Every item of `taskcontract tree` shows one of six statuses, and a parent
reads `done` only when every item under it reads `done` (SC3.1). A
contract's G0 verdict reads from the validator at the ready and draft
profiles, and names the validator command and the HEAD id (SC7.3). The
current task derives from the records in `.sdlc/progress/<contract>.yaml`,
never from a stored marker (the cursor sketch).

The writers came later, in units t4 and t5, so each test here writes its
records by hand, in the format this unit fixes, and drives the command as
a user would.
"""

from __future__ import annotations

import datetime
import re
import shutil
import subprocess

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

STATUSES = {"to do", "doing", "done", "failed", "blocked", "waiting on a seat"}
TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]
HEAD = "1a2b3c4"  # what a hand-written record carries; no t3 status reads it

INTENT = ("A fixture contract for the status suite; its units carry the "
          "sketch shapes that check ids come from.")

# One item per line: its full id, then its plain name when it has one
# (project-tree o2), then its status (a finding: its kind) in brackets, then
# its marks, then its evidence, then what later units add.
ROW = re.compile(r"^(?P<indent> *)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                 r"(?P<rest>.*)$")
UNREADABLE = re.compile(
    r"^taskcontract tree: unreadable progress: \.sdlc/progress/alpha\.yaml \(.+\)$")


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


# The shapes of test_tree.py: alpha/a1-core checks SC1.1 and SC5.1+SC5.2,
# alpha/a2-edges checks sketch-1, SC2.1 and sketch-3, beta/b1-solo sketch-1.
ALPHA = [
    _unit("a1-core", ["verify the core prints (SC1.1)",
                      "verify both links print (SC5.1, SC5.2)"]),
    _unit("a2-edges", ["verify an edge holds",
                       "verify it again (SC2.1)",
                       "verify it once more (SC2.1)"], depends_on=["a1-core"]),
]
BETA = [_unit("b1-solo", ["verify the price rounds (by the house rule)"])]
LONE = [_unit("l1-lone", ["verify it holds"])]


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


def _finding(slug, gate, kind):
    return {
        "finding": slug, "date": "2026-09-22", "kit_pinned": "v0.14.0",
        "diagnostic": "none", "gate": gate, "kind": kind, "count": 1,
        "statement": "A fixture finding for the status suite.", "proposal": "none",
    }


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _config(root, gates):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates)})


def _repo(tmp_path):
    """alpha and beta, both ready-green, with G0 active and no progress."""
    root = tmp_path / "repo"
    _config(root, ["G0"])
    _dump(root / "specs" / "alpha" / "contract.yaml", _contract("alpha", ALPHA))
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA))
    write_seat_roster(root)
    return root


VERDICT_IDS = ("alpha", "beta", "delta", "epsilon", "gamma")  # folder order


def _verdict_repo(tmp_path):
    """One contract per G0 reading: alpha ready-green; beta parked on a
    blocked dependency (TC003 at ready); gamma with no `entities` (TC017 at
    ready); delta with a short intent (TC007, red at draft); epsilon
    ready-green with a warning (W001: a deprecated term inside its notice
    window), which the validator never counts against green."""
    root = _repo(tmp_path)
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA, dependencies=[
        {"ref": "vendor-feed", "status": "blocked", "blocked_by": "the vendor feed"}]))
    _dump(root / "specs" / "gamma" / "contract.yaml",
          _contract("gamma", LONE, entities=None))
    _dump(root / "specs" / "delta" / "contract.yaml",
          _contract("delta", LONE, intent="Too short."))
    _dump(root / "specs" / "vocabulary" / "old-term.yaml", {
        "term": "old-term", "name": "Old term",
        "definition": "A fixture term, deprecated with its sunset still ahead.",
        "kind": "entity", "status": "deprecated", "since": "2026-01-01",
        "sunset": "2099-01-01"})
    _dump(root / "specs" / "epsilon" / "contract.yaml",
          _contract("epsilon", LONE, entities=["old-term"]))
    return root


# --- records, written by hand in the t3 format ------------------------------

def _at(clock):
    """A record time on the fixture day, UTC: _at("10:05")."""
    return f"2026-09-22T{clock}:00Z"


def _step(item, state, clock, **more):
    """A task-step record; on a unit or a contract id with `done`, a close."""
    return {"item": item, "state": state, "at": _at(clock), "head": HEAD, **more}


def _ran(item, run, expect, clock):
    """A check-run record: the result and the result the run expected."""
    return {"item": item, "run": run, "expect": expect,
            "command": "python -m pytest tests/", "dirty": False,
            "at": _at(clock), "head": HEAD}


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


# --- the print ----------------------------------------------------------------

def _print(root, capsys):
    """(rows, stderr) of one print; the command exits 0 whatever it reads."""
    code = main(["tree", "--root", str(root)])
    captured = capsys.readouterr()
    assert code == 0
    return _rows(captured.out), captured.err


def _rows(out):
    """[(depth, id, tag, rest)] for every item line, in print order."""
    rows = []
    for line in out.splitlines():
        match = ROW.match(line)
        if match:
            rows.append((len(match["indent"]) // 2, match["id"], match["tag"],
                         match["rest"]))
    return rows


def _row(rows, rid):
    for row in rows:
        if row[1] == rid:
            return row
    raise AssertionError(f"{rid} not printed")


def _tag(rows, rid):
    return _row(rows, rid)[2]


def _children(rows, parent):
    """Ids one level under `parent`, in print order."""
    for i, (depth, rid, _, _) in enumerate(rows):
        if rid == parent:
            found = []
            for child_depth, cid, _, _ in rows[i + 1:]:
                if child_depth <= depth:
                    break
                if child_depth == depth + 1:
                    found.append(cid)
            return found
    raise AssertionError(f"{parent} not printed")


def _current(rows):
    """Ids whose line carries the mark `current` right after the status."""
    return [rid for _, rid, _, rest in rows if rest.split()[:1] == ["current"]]


def _evidence(cid, head):
    """The tokens a G0 verdict line carries right after its status."""
    return (f"via python -m taskcontract validate specs/{cid}/contract.yaml "
            f"--profile ready at {head}").split()


def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True,
                          capture_output=True, encoding="utf-8").stdout


def _commit_all(root):
    """Make `root` a git repo with one commit; return its short HEAD id."""
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed")
    return _git(root, "rev-parse", "--short", "HEAD").strip()


# --- SC3.1 task steps and checks read their records ---------------------------

def test_a_task_reads_the_state_of_its_last_record(tmp_path, capsys):
    root = _repo(tmp_path)
    unit = "alpha/a1-core"
    _progress(root, "alpha",
              _step(f"{unit}/approve-tests", "done", "10:00", by="user"),
              _step(f"{unit}/write-tests", "doing", "10:01"),
              _step(f"{unit}/write-tests", "done", "10:02"),
              _step(f"{unit}/prove-red", "blocked", "10:03", reason="the runner is down"),
              _step(f"{unit}/green", "doing", "10:04"))
    rows, _ = _print(root, capsys)
    assert [_tag(rows, f"{unit}/{task}") for task in TASK_KEYS] == [
        "done", "done", "blocked", "doing", "to do", "to do", "to do"]


def test_a_check_reads_its_last_run_judged_by_its_expectation(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _ran("alpha/a1-core/SC1.1", "green", "red", "10:00"),
              _ran("alpha/a1-core/SC1.1", "red", "red", "10:01"),
              _ran("alpha/a1-core/SC5.1+SC5.2", "red", "red", "10:02"),
              _ran("alpha/a1-core/SC5.1+SC5.2", "green", "green", "10:03"),
              _ran("alpha/a2-edges/sketch-1", "green", "red", "10:04"),
              _ran("alpha/a2-edges/SC2.1", "red", "green", "10:05"))
    rows, _ = _print(root, capsys)
    assert _tag(rows, "alpha/a1-core/SC1.1") == "doing"         # red, as expected
    assert _tag(rows, "alpha/a1-core/SC5.1+SC5.2") == "done"     # green, as expected
    assert _tag(rows, "alpha/a2-edges/sketch-1") == "failed"     # green, expecting red
    assert _tag(rows, "alpha/a2-edges/SC2.1") == "failed"        # red, expecting green
    assert _tag(rows, "alpha/a2-edges/sketch-3") == "to do"      # never run


# --- closes: a done record on a unit or a contract ----------------------------

def test_a_unit_close_reads_every_task_and_check_under_it_done(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha", _step("alpha/a1-core", "done", "10:00"))
    rows, _ = _print(root, capsys)
    under = _children(rows, "alpha/a1-core")
    assert len(under) == len(TASK_KEYS) + 2
    assert {_tag(rows, rid) for rid in under + ["alpha/a1-core"]} == {"done"}
    # the sibling unit stays open
    assert _tag(rows, "alpha/a2-edges/write-tests") == "to do"
    assert [_tag(rows, f"alpha/a2-edges/{check}")
            for check in ("sketch-1", "SC2.1", "sketch-3")] == ["to do"] * 3


def test_a_close_counts_at_its_place_in_the_file(tmp_path, capsys):
    root = _repo(tmp_path)
    unit = "alpha/a1-core"
    _progress(root, "alpha",
              _step(f"{unit}/prove-red", "blocked", "09:00", reason="the runner is down"),
              _ran(f"{unit}/SC1.1", "red", "green", "09:01"),
              _step(unit, "done", "10:00"),
              _step(f"{unit}/write-tests", "doing", "10:05"),
              _ran(f"{unit}/SC5.1+SC5.2", "red", "green", "10:06"))
    rows, _ = _print(root, capsys)
    # before the close, the close wins
    assert _tag(rows, f"{unit}/prove-red") == "done"
    assert _tag(rows, f"{unit}/SC1.1") == "done"
    # after the close, the later record wins again
    assert _tag(rows, f"{unit}/write-tests") == "doing"
    assert _tag(rows, f"{unit}/SC5.1+SC5.2") == "failed"
    assert _tag(rows, unit) == "failed"


def test_a_contract_close_reads_the_contract_done_all_the_way_down(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha", _step("alpha", "done", "10:00"))
    rows, _ = _print(root, capsys)
    # the inactive next gate, alpha/G1, and its conditions read to do and never count
    under = [row for row in rows if (row[1] == "alpha" or row[1].startswith("alpha/"))
             and not row[1].startswith("alpha/G1")]
    assert len(under) == 26  # the contract, its verdict and its conditions, two units, ...
    assert {tag for _, _, tag, _ in under} == {"done"}


def test_a_close_leaves_the_verdict_to_the_validator(tmp_path, capsys):
    root = _repo(tmp_path)
    # no `entities`: draft-green, TC017 at ready, so the verdict reads to do
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA, entities=None))
    _progress(root, "beta", _step("beta", "done", "10:00"))
    rows, _ = _print(root, capsys)
    assert _tag(rows, "beta/b1-solo") == "done"
    assert _tag(rows, "beta/G0") == "to do"
    # a closed contract reads done whatever its verdicts read (project-tree o4)
    assert _tag(rows, "beta") == "done"


# --- SC3.1 the rollup -----------------------------------------------------------

# Each case adds one record to the one before: a doing task, a blocked task,
# an approval marked doing last (the current task), a check that missed.
PRECEDENCE = [
    pytest.param(1, "doing", id="doing"),
    pytest.param(2, "blocked", id="blocked-over-doing"),
    pytest.param(3, "waiting on a seat", id="waiting-over-blocked"),
    pytest.param(4, "failed", id="failed-over-waiting"),
]


@pytest.mark.parametrize("count, status", PRECEDENCE)
def test_a_parent_takes_the_first_of_failed_waiting_blocked_and_doing(
        tmp_path, capsys, count, status):
    root = _repo(tmp_path)
    unit = "alpha/a1-core"
    records = [
        _step(f"{unit}/write-tests", "doing", "10:00"),
        _step(f"{unit}/prove-red", "blocked", "10:01", reason="the runner is down"),
        _step(f"{unit}/approve-tests", "doing", "10:02"),
        _ran(f"{unit}/SC1.1", "green", "red", "10:03"),
    ]
    _progress(root, "alpha", *records[:count])
    rows, _ = _print(root, capsys)
    assert (_tag(rows, unit), _tag(rows, "alpha")) == (status, status)


def test_a_parent_reads_done_only_when_every_child_reads_done(tmp_path, capsys):
    root = _repo(tmp_path)
    records = []
    for hour, unit in (("10", "alpha/a1-core"), ("11", "alpha/a2-edges")):
        for n, task in enumerate(TASK_KEYS):
            seat = {"by": "user"} if task.startswith("approve-") else {}
            records.append(_step(f"{unit}/{task}", "done", f"{hour}:0{n}", **seat))
    records += [_ran("alpha/a1-core/SC1.1", "green", "green", "12:00"),
                _ran("alpha/a1-core/SC5.1+SC5.2", "green", "green", "12:01"),
                _ran("alpha/a2-edges/sketch-1", "green", "green", "12:02"),
                _ran("alpha/a2-edges/SC2.1", "green", "green", "12:03")]
    _progress(root, "alpha", *records)  # alpha/a2-edges/sketch-3 never runs
    rows, _ = _print(root, capsys)
    assert _tag(rows, "alpha/a1-core") == "done"
    assert _tag(rows, "alpha/a2-edges") == "doing"
    assert _tag(rows, "alpha") == "doing"
    for _, rid, tag, _ in rows:
        if tag == "done":
            assert {_tag(rows, child) for child in _children(rows, rid)} <= {"done"}, rid


def test_a_verdict_counts_toward_failed_and_blocked_but_never_starts_its_contract(
        tmp_path, capsys):
    rows, _ = _print(_verdict_repo(tmp_path), capsys)
    assert _tag(rows, "alpha/G0") == "done"
    assert _tag(rows, "alpha") == "to do"  # nothing under it started
    assert _tag(rows, "beta") == "blocked"
    assert _tag(rows, "delta") == "failed"


def test_a_gate_item_reads_to_do_whatever_its_contracts_read(tmp_path, capsys):
    root = _repo(tmp_path)
    _dump(root / ".sdlc" / "findings" / "idea.yaml", _finding("idea", "none", "proposal"))
    _progress(root, "alpha", _step("alpha", "done", "10:00"))
    _progress(root, "beta", _step("beta", "done", "10:01"))
    rows, _ = _print(root, capsys)
    assert [_tag(rows, rid) for rid in ("alpha/G0", "beta/G0", "alpha", "beta")] == ["done"] * 4
    assert _tag(rows, "gates/G0") == "to do"    # no finding under it
    assert _tag(rows, "gates/none") == "to do"  # a finding under it, which holds no status


def test_every_status_printed_is_one_of_the_six(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "10:00", by="user"),
              _step("alpha/a1-core/write-tests", "doing", "10:01"),
              _step("alpha/a1-core/prove-red", "blocked", "10:02", reason="the runner is down"),
              _ran("alpha/a2-edges/SC2.1", "green", "red", "10:03"),
              _step("alpha/a2-edges/approve-tests", "doing", "10:04"))
    rows, _ = _print(root, capsys)
    assert {tag for _, _, tag, _ in rows} == STATUSES  # no finding here: every tag is a status


# --- SC7.3 the verdict at G0 ----------------------------------------------------

def test_a_g0_verdict_reads_done_only_at_ready_green(tmp_path, capsys):
    rows, _ = _print(_verdict_repo(tmp_path), capsys)
    assert {cid: _tag(rows, f"{cid}/G0") for cid in VERDICT_IDS} == {
        "alpha": "done",     # ready-green
        "beta": "blocked",   # draft-green, TC003 at ready
        "delta": "failed",   # draft-red
        "epsilon": "done",   # ready-green; a warning is not an error
        "gamma": "to do",    # draft-green, TC017 at ready
    }


@pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
def test_each_g0_verdict_names_the_validator_command_and_the_head_id(tmp_path, capsys):
    root = _verdict_repo(tmp_path)
    head = _commit_all(root)
    rows, _ = _print(root, capsys)
    for cid in VERDICT_IDS:
        expected = _evidence(cid, head)
        assert _row(rows, f"{cid}/G0")[3].split()[:len(expected)] == expected, cid


def test_a_g0_verdict_outside_git_names_no_commit(tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))  # no repo above the fixture
    rows, _ = _print(_verdict_repo(tmp_path), capsys)
    for cid in VERDICT_IDS:
        expected = _evidence(cid, "no commit")
        assert _row(rows, f"{cid}/G0")[3].split()[:len(expected)] == expected, cid


def test_a_verdict_at_another_gate_reads_to_do_with_no_evidence(tmp_path, capsys):
    root = _repo(tmp_path)
    _config(root, ["G0", "G4"])
    rows, _ = _print(root, capsys)
    _, _, tag, rest = _row(rows, "alpha/G0")
    assert tag == "done" and "python -m taskcontract validate" in rest
    _, _, tag, rest = _row(rows, "alpha/G4")
    assert tag == "to do" and "python -m taskcontract validate" not in rest


# --- the current task -----------------------------------------------------------

def test_the_current_task_is_the_doing_task_with_the_latest_record(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/write-tests", "doing", "10:00"),
              _step("alpha/a2-edges/prove-red", "doing", "10:02"),
              _step("alpha/a1-core/write-tests", "done", "10:10"))  # the last change, not doing
    _progress(root, "beta", _step("beta/b1-solo/write-tests", "doing", "10:05"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["beta/b1-solo/write-tests"]
    assert _tag(rows, "beta/b1-solo/write-tests") == "doing"
    assert _tag(rows, "alpha/a2-edges/prove-red") == "doing"


def test_with_none_doing_the_current_task_is_the_first_to_do_in_the_latest_contract(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "10:00", by="user"),
              _step("alpha/a1-core/write-tests", "done", "10:01"))
    _progress(root, "beta",
              _step("beta/b1-solo/approve-tests", "done", "11:00", by="user"),
              _step("beta/b1-solo/write-tests", "blocked", "11:01", reason="the runner is down"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["beta/b1-solo/prove-red"]
    assert _tag(rows, "beta/b1-solo/prove-red") == "to do"


def test_no_current_task_shows_without_a_progress_file(tmp_path, capsys):
    root = _repo(tmp_path)
    folder = root / ".sdlc" / "progress"
    _progress(root, "alpha", _step("alpha/a1-core/write-tests", "doing", "10:00"))
    (folder / ".gitignore").write_text("*\n", encoding="utf-8")  # t4's file, never progress
    rows, err = _print(root, capsys)
    assert (_current(rows), err) == (["alpha/a1-core/write-tests"], "")
    _dump(folder / "alpha.yaml", {"records": []})
    rows, err = _print(root, capsys)
    assert (_current(rows), err) == ([], "")
    (folder / "alpha.yaml").unlink()
    rows, err = _print(root, capsys)
    assert (_current(rows), err) == ([], "")


def test_no_current_task_when_the_latest_contract_has_no_task_to_do(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "beta", _step("beta/b1-solo/approve-tests", "done", "09:00", by="user"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["beta/b1-solo/write-tests"]
    _progress(root, "alpha", _step("alpha", "done", "10:00"))  # a later change, nothing to do
    rows, _ = _print(root, capsys)
    assert _current(rows) == []


def test_the_current_task_is_derived_and_moves_on_when_marked_done(tmp_path, capsys):
    root = _repo(tmp_path)
    records = [_step("alpha/a1-core/approve-tests", "done", "09:00", by="user"),
               _step("alpha/a1-core/write-tests", "doing", "10:00")]
    _progress(root, "alpha", *records)
    before = _snapshot(root)
    rows, _ = _print(root, capsys)
    assert _snapshot(root) == before  # the print stores no marker
    assert _current(rows) == ["alpha/a1-core/write-tests"]
    _progress(root, "alpha", *records, _step("alpha/a1-core/write-tests", "done", "10:05"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["alpha/a1-core/prove-red"]


def test_an_approval_holding_the_current_task_reads_waiting_on_a_seat(tmp_path, capsys):
    root = _repo(tmp_path)
    close = _step("alpha/a1-core", "done", "10:00")
    _progress(root, "alpha", close)
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["alpha/a2-edges/approve-tests"]  # the first to do, an approval
    assert [_tag(rows, rid) for rid in (
        "alpha/a2-edges/approve-tests", "alpha/a2-edges", "alpha")] == ["waiting on a seat"] * 3
    assert _tag(rows, "alpha/a2-edges/approve-commit") == "to do"  # an approval not current
    _progress(root, "alpha", close, _step("alpha/a2-edges/approve-tests", "doing", "10:01"))
    _progress(root, "beta", _step("beta/b1-solo/approve-tests", "doing", "10:05"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["beta/b1-solo/approve-tests"]  # the latest doing, an approval
    assert _tag(rows, "beta/b1-solo/approve-tests") == "waiting on a seat"
    assert _tag(rows, "alpha/a2-edges/approve-tests") == "doing"  # doing, not current
    assert _tag(rows, "alpha") == "doing"


def test_ties_on_at_go_to_the_later_record_then_the_later_contract(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/write-tests", "doing", "10:00"),
              _step("alpha/a2-edges/write-tests", "doing", "10:00"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["alpha/a2-edges/write-tests"]  # the later record in its file
    _progress(root, "beta", _step("beta/b1-solo/write-tests", "doing", "10:00"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["beta/b1-solo/write-tests"]  # the contract later in folder order


def test_at_reads_as_a_string_or_a_yaml_timestamp(tmp_path, capsys):
    root = _repo(tmp_path)
    stamp = datetime.datetime(2026, 9, 22, 11, 0, tzinfo=datetime.timezone.utc)
    _progress(root, "beta",
              {"item": "beta/b1-solo/write-tests", "state": "doing", "at": stamp, "head": HEAD})
    text = (root / ".sdlc" / "progress" / "beta.yaml").read_text(encoding="utf-8")
    assert "at: 2026-09-22 11:00:00+00:00" in text  # a YAML timestamp, unquoted
    _progress(root, "alpha", _step("alpha/a1-core/write-tests", "doing", "10:00"))  # a string
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["beta/b1-solo/write-tests"]
    _progress(root, "alpha", _step("alpha/a1-core/write-tests", "doing", "12:00"))
    rows, _ = _print(root, capsys)
    assert _current(rows) == ["alpha/a1-core/write-tests"]


# --- the file: malformed, and records the tree cannot place ---------------------

def _text(doc):
    return yaml.safe_dump(doc, sort_keys=False)


GOOD = _step("alpha/a1-core/approve-tests", "done", "10:00", by="user")
TASK = "alpha/a1-core/green"
CHECK = "alpha/a1-core/SC1.1"
MALFORMED = [
    pytest.param("records: [unclosed\n", id="yaml-error"),
    pytest.param(_text([GOOD]), id="not-a-mapping"),
    pytest.param(_text({"records": GOOD}), id="records-not-a-list"),
    pytest.param(_text({"records": [GOOD, TASK]}), id="record-not-a-mapping"),
    pytest.param(_text({"records": [GOOD, {"state": "done", "at": _at("10:01")}]}),
                 id="no-item"),
    pytest.param(_text({"records": [GOOD, _step(TASK, "finished", "10:01")]}),
                 id="unknown-state"),
    pytest.param(_text({"records": [GOOD, _ran(CHECK, "amber", "green", "10:01")]}),
                 id="unknown-run"),
    pytest.param(_text({"records": [GOOD, {"item": CHECK, "run": "red", "at": _at("10:01")}]}),
                 id="no-expect"),
    pytest.param(_text({"records": [GOOD, {**_ran(CHECK, "green", "green", "10:01"),
                                            "state": "done"}]}),
                 id="state-and-run"),
    pytest.param(_text({"records": [GOOD, {"item": TASK, "at": _at("10:01")}]}),
                 id="neither-state-nor-run"),
    pytest.param(_text({"records": [GOOD, {"item": TASK, "state": "done"}]}), id="no-at"),
    pytest.param(_text({"records": [GOOD, {"item": TASK, "state": "done", "at": "yesterday"}]}),
                 id="unreadable-at"),
]


@pytest.mark.parametrize("text", MALFORMED)
def test_a_malformed_progress_file_prints_one_line_and_its_contract_reads_no_progress(
        tmp_path, capsys, text):
    root = _repo(tmp_path)
    (root / ".sdlc" / "progress").mkdir(parents=True)
    (root / ".sdlc" / "progress" / "alpha.yaml").write_text(text, encoding="utf-8")
    _progress(root, "beta", _step("beta/b1-solo/write-tests", "doing", "09:00"))
    rows, err = _print(root, capsys)
    lines = err.splitlines()
    assert len(lines) == 1 and UNREADABLE.match(lines[0]), err
    assert _tag(rows, "alpha/a1-core/approve-tests") == "to do"  # not even its good record
    assert _current(rows) == ["beta/b1-solo/write-tests"]        # beta's file still reads


def test_a_record_the_tree_cannot_place_is_ignored(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "10:00", by="user"),
              _ran("alpha/a1-core/SC9.9", "green", "green", "12:00"),   # no sketch names SC9.9
              _step("beta/b1-solo/write-tests", "doing", "12:30"),      # another contract's item
              _step("alpha/a1-core/SC1.1", "done", "12:45"))            # a state on a check
    _progress(root, "beta", _step("beta/b1-solo/approve-tests", "done", "11:00", by="user"))
    rows, err = _print(root, capsys)
    assert err == ""
    assert not any(rid.endswith("/SC9.9") for _, rid, _, _ in rows)
    assert _tag(rows, "alpha/a1-core/approve-tests") == "done"
    assert _tag(rows, "alpha/a1-core/SC1.1") == "to do"
    # beta holds the latest record the tree can place, and its own task is not doing
    assert _current(rows) == ["beta/b1-solo/write-tests"]
    assert _tag(rows, "beta/b1-solo/write-tests") == "to do"
