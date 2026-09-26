"""The blocked-and-waiting suite (contract project-tree, unit o4-statuses).

Each unit and each task shows `done`, `doing` or `to do` from the progress
record, as the six statuses read them; a closed unit reads `done`, and a
closed contract reads `done` whatever its verdicts read, each verdict still
showing the validator's reading on its own line (SC3.1). A task blocked by its own record
names its reason on its own line, `because <reason>`; a unit or contract
that reads `blocked` through one of its tasks names none. The approval that
holds the current task reads `waiting on a seat` and names the seats it
waits on, `seat: <seats>`: its unit's `confirmed_by`, each seat once in the
order it first appears, joined by `, `. A unit whose `confirmed_by` gives no
seat names none, and no other item names a seat (SC3.2).

The seat and the reason are the line's evidence: they print on the whole
tree, on the query's first line and on the pane's item line, after the
marks, and a `tree: pane: parts:` list without `evidence` leaves them out.
The pane's waiting line keeps its words, the notify command still gets the
approval's id in SDLC_NODE, and `taskcontract progress` stays the only
writer, every state it records reading as before.

Each test drives the CLI in process against a fixture repo under tmp_path,
outside any git repository. The records are written by hand in the progress
file's format, save in the writer's test, which records through
`taskcontract progress`.
"""

from __future__ import annotations

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract import tree
from taskcontract.__main__ import main

HEAD = "1a2b3c4"  # what a hand-written record carries
SEATS = ("user", "po")  # the fixture's ratified intake seats
INTENT = ("A fixture contract for the waiting suite; its units wait on the "
          "seats that confirmed them.")
TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]
TASK_NAMES = dict(zip(TASK_KEYS, ["Approve the test list", "Write the tests", "Prove red",
                                  "Green", "Approve the commit", "Commit", "Two-Key PASS"]))
WAITING = "[waiting on a seat] current"
MISSING = object()  # a unit with no `confirmed_by` key at all


def _unit(uid, seats=("user",), depends_on=None):
    unit = {"unit": "work for " + uid, "id": uid}
    if depends_on is not None:
        unit["depends_on"] = list(depends_on)
    if seats is not MISSING:
        unit["confirmed_by"] = list(seats) if isinstance(seats, tuple) else seats
    unit["done_means"] = "the work for " + uid + " is done"
    unit["acceptance_sketch"] = ["verify the " + uid + " holds (SC1.1)"]
    return unit


# alpha/a1-core is confirmed by one seat, alpha/a2-edges by two, and
# beta/b1-solo by the other seat alone.
ALPHA = [_unit("a1-core"),
         _unit("a2-edges", ("user", "po"), depends_on=["a1-core"]),
         _unit("a3-rest")]
BETA = [_unit("b1-solo", ("po",))]


def _contract(cid, units):
    """A contract that reads ready-green when every seat it names is ratified."""
    return {"id": cid, "intent": INTENT, "scope": ["src/"], "non_goals": ["No other work"],
            "decomposition": units, "dependencies": [], "entities": [],
            "provenance": {"origin": "human-request"}}


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _config(root, gates=(), **more):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates), **more})


def _repo(tmp_path, gates=(), alpha=ALPHA, **config):
    """alpha and beta, each ready-green, with no progress; no gate active
    unless named, so no print runs the validator."""
    root = tmp_path / "repo"
    _config(root, gates, **config)
    _dump(root / "specs" / "alpha" / "contract.yaml", _contract("alpha", alpha))
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA))
    write_seat_roster(root, values=SEATS)
    return root


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, find no git repo above the
    fixture, and give the pane a wide terminal."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


# --- records, written by hand ---------------------------------------------------------

def _step(item, state, clock, **more):
    """A task-step record; on a unit or a contract id with `done`, a close."""
    return {"item": item, "state": state, "at": f"2026-09-25T{clock}:00Z", "head": HEAD,
            **more}


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


# --- driving the CLI ----------------------------------------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _lines(root, capsys):
    """The whole tree's stdout lines; the print exits 0 with nothing on stderr."""
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert (code, err) == (0, "")
    return out.splitlines()


def _line(lines, rid):
    """The one line whose item id is `rid`, indent kept."""
    found = [text for text in lines if text.lstrip(" ").split(" ", 1)[0] == rid]
    assert len(found) == 1, (rid, found)
    return found[0]


def _task(unit, key, rest, depth=2):
    """A task's whole-tree line: indent, full id, plain name, then `rest`."""
    return f"{'  ' * depth}{unit}/{key} {TASK_NAMES[key]} {rest}"


def _seated(lines):
    """The ids of the lines that name a seat."""
    return [text.lstrip(" ").split(" ", 1)[0] for text in lines if " seat: " in text]


# --- SC3.1 done, doing and to do from the records ------------------------------------------

def test_sc3_1_each_unit_and_each_of_its_seven_tasks_read_done_doing_or_to_do_from_the_records(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "09:00", by="user"),
              _step("alpha/a1-core/write-tests", "doing", "09:01"),
              _step("alpha/a1-core/write-tests", "done", "09:02"),
              _step("alpha/a1-core/prove-red", "done", "09:03"),
              _step("alpha/a1-core/green", "doing", "09:04"),
              _step("alpha/a2-edges/approve-tests", "done", "09:05", by="po"),
              _step("alpha/a2-edges/write-tests", "doing", "09:06"),
              _step("alpha/a1-core/approve-commit", "doing", "09:07"))  # the latest doing
    lines = _lines(root, capsys)
    unit = "alpha/a1-core"
    assert [_line(lines, f"{unit}/{key}") for key in TASK_KEYS] == [
        _task(unit, "approve-tests", f"[done] by user at {HEAD}"),
        _task(unit, "write-tests", f"[done] at {HEAD}"),
        _task(unit, "prove-red", f"[done] at {HEAD}"),
        _task(unit, "green", "[doing]"),
        _task(unit, "approve-commit", f"{WAITING} seat: user"),
        _task(unit, "commit", "[to do]"),
        _task(unit, "two-key", "[to do]")]
    assert [_line(lines, uid) for uid in ("alpha/a1-core", "alpha/a2-edges", "alpha/a3-rest")] == [
        "  alpha/a1-core the work for a1-core is done [waiting on a seat]",
        "  alpha/a2-edges the work for a2-edges is done [doing] depends_on: alpha/a1-core",
        "  alpha/a3-rest the work for a3-rest is done [to do]"]
    assert _line(lines, "alpha/a2-edges/write-tests") == _task(
        "alpha/a2-edges", "write-tests", "[doing]")
    assert _line(lines, "alpha/a3-rest/approve-tests") == _task(
        "alpha/a3-rest", "approve-tests", "[to do]")
    assert _seated(lines) == ["alpha/a1-core/approve-commit"]


def test_sc3_1_a_closed_unit_reads_done_and_the_next_approval_waits_on_its_units_seats(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha", _step("alpha/a1-core", "done", "10:00"))
    lines = _lines(root, capsys)
    assert _line(lines, "alpha/a1-core") == (
        f"  alpha/a1-core the work for a1-core is done [done] at {HEAD}")
    # a close reads every task and check under it done, and adds them no evidence
    assert [_line(lines, f"alpha/a1-core/{key}") for key in TASK_KEYS] == [
        _task("alpha/a1-core", key, "[done]") for key in TASK_KEYS]
    assert _line(lines, "alpha/a1-core/SC1.1") == (
        "    alpha/a1-core/SC1.1 verify the a1-core holds (SC1.1) [done]")
    # the first task to do in the latest contract: an approval of a unit two seats confirmed
    assert _line(lines, "alpha/a2-edges/approve-tests") == _task(
        "alpha/a2-edges", "approve-tests", f"{WAITING} seat: user, po")
    assert _seated(lines) == ["alpha/a2-edges/approve-tests"]


def test_sc3_1_a_closed_contract_reads_done_whatever_its_verdicts_read(tmp_path, capsys):
    root = _repo(tmp_path, gates=["G0"])
    _progress(root, "alpha", _step("alpha", "done", "10:00"))
    _progress(root, "beta", _step("beta/b1-solo/approve-tests", "doing", "10:05"))
    lines = _lines(root, capsys)
    alpha = _line(lines, "alpha")
    assert alpha.startswith("alpha (no title) [done] no feature document at 1a2b3c4 | "), alpha
    assert _line(lines, "alpha/G0").startswith("  alpha/G0 Planning / Intake [done] via ")
    assert _line(lines, "alpha/G1") == "  alpha/G1 Requirements / Spec [to do] inactive"
    # its units read done through the close, and name no close of their own
    assert [_line(lines, f"alpha/{uid}") for uid in ("a1-core", "a2-edges", "a3-rest")] == [
        "  alpha/a1-core the work for a1-core is done [done]",
        "  alpha/a2-edges the work for a2-edges is done [done] depends_on: alpha/a1-core",
        "  alpha/a3-rest the work for a3-rest is done [done]"]
    assert _line(lines, "beta/b1-solo/approve-tests") == _task(
        "beta/b1-solo", "approve-tests", f"{WAITING} seat: po")
    # with G1 active too, its verdict reads to do on its own line, and the closed
    # contract still reads done and names its close; its units still read done
    _config(root, ["G0", "G1"])
    lines = _lines(root, capsys)
    alpha = _line(lines, "alpha")
    assert alpha.startswith("alpha (no title) [done] no feature document at 1a2b3c4 | "), alpha
    assert _line(lines, "alpha/G1") == "  alpha/G1 Requirements / Spec [to do]"
    assert _line(lines, "alpha/G2").startswith("  alpha/G2 ")
    assert _line(lines, "alpha/G2").endswith(" [to do] inactive")
    assert _line(lines, "alpha/a1-core") == "  alpha/a1-core the work for a1-core is done [done]"
    assert _seated(lines) == ["beta/b1-solo/approve-tests"]


@pytest.mark.parametrize("breaks, verdict", [
    ({"non_goals": None}, "failed"),  # draft-red: a required field is gone
    ({"dependencies": [{"ref": "gamma", "status": "blocked", "blocked_by": "gamma"}]},
     "blocked"),  # draft-green with TC003 at ready
], ids=["g0-failed", "g0-blocked"])
def test_sc3_1_a_closed_contract_reads_done_while_its_g0_verdict_keeps_its_own_reading(
        tmp_path, capsys, breaks, verdict):
    root = _repo(tmp_path, gates=["G0"])
    doc = _contract("alpha", ALPHA)
    for key, value in breaks.items():
        if value is None:
            del doc[key]
        else:
            doc[key] = value
    _dump(root / "specs" / "alpha" / "contract.yaml", doc)
    _progress(root, "alpha", _step("alpha", "done", "10:00"))
    lines = _lines(root, capsys)
    alpha = _line(lines, "alpha")
    assert alpha.startswith("alpha (no title) [done] no feature document at 1a2b3c4 | "), alpha
    assert _line(lines, "alpha/G0").startswith(f"  alpha/G0 Planning / Intake [{verdict}] via ")
    assert _line(lines, "alpha/a1-core") == "  alpha/a1-core the work for a1-core is done [done]"
    # a task reopened after the close shows through, as it does under a closed unit
    # (the contract has units: see the next test for one that has none)
    _progress(root, "alpha", _step("alpha", "done", "10:00"),
              _step("alpha/a3-rest/green", "doing", "10:30"))
    lines = _lines(root, capsys)
    assert _line(lines, "alpha").startswith("alpha (no title) [doing] no feature document | ")
    assert _line(lines, "alpha/a3-rest").startswith("  alpha/a3-rest the work for a3-rest is done [doing]")


def test_sc3_1_a_closed_contract_the_tree_cannot_read_reads_done(tmp_path, capsys):
    # the one contract with no units: the tree cannot read it as a mapping
    root = _repo(tmp_path, gates=["G0"])
    path = root / "specs" / "broken" / "contract.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("id: [\n", encoding="utf-8")
    _progress(root, "broken", _step("broken", "done", "10:00"))
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    assert err == ("taskcontract tree: unreadable contract: specs/broken/contract.yaml "
                   "(YAML error at line 2)\n")
    lines = out.splitlines()
    assert _line(lines, "broken") == "broken (no title) [done] no feature document at 1a2b3c4"
    assert _line(lines, "broken/G0").startswith("  broken/G0 Planning / Intake [failed] via ")


# --- SC3.2 a blocked task names its reason ---------------------------------------------------

def test_sc3_2_a_blocked_task_names_its_reason_and_its_unit_and_contract_name_none(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/prove-red", "blocked", "10:00",
                    reason="the runner\nis down"))
    _progress(root, "beta", _step("beta/b1-solo/approve-commit", "doing", "10:05"))
    lines = _lines(root, capsys)
    assert _line(lines, "alpha/a1-core/prove-red") == _task(
        "alpha/a1-core", "prove-red", "[blocked] because the runner is down")
    assert _line(lines, "alpha/a1-core") == "  alpha/a1-core the work for a1-core is done [blocked]"
    alpha = _line(lines, "alpha")
    assert alpha.startswith("alpha (no title) [blocked] no feature document | "), alpha
    assert [text.lstrip(" ").split(" ", 1)[0] for text in lines if "because" in text] == [
        "alpha/a1-core/prove-red"]
    assert _line(lines, "beta/b1-solo/approve-commit") == _task(
        "beta/b1-solo", "approve-commit", f"{WAITING} seat: po")


# --- SC3.2 the approval that holds the current task names its seats ----------------------------

@pytest.mark.parametrize("unit, key, seats", [
    pytest.param("a1-core", "approve-tests", "user", id="approve-tests-one-seat"),
    pytest.param("a1-core", "approve-commit", "user", id="approve-commit-one-seat"),
    pytest.param("a2-edges", "approve-tests", "user, po", id="approve-tests-two-seats"),
    pytest.param("a2-edges", "approve-commit", "user, po", id="approve-commit-two-seats"),
])
def test_sc3_2_the_approval_holding_the_current_task_names_its_units_confirmed_by_seats(
        tmp_path, capsys, unit, key, seats):
    root = _repo(tmp_path)
    _progress(root, "alpha", _step(f"alpha/{unit}/{key}", "doing", "10:00"))
    lines = _lines(root, capsys)
    assert _line(lines, f"alpha/{unit}/{key}") == _task(
        f"alpha/{unit}", key, f"{WAITING} seat: {seats}")
    assert _seated(lines) == [f"alpha/{unit}/{key}"]  # no other approval names a seat


def test_sc3_2_the_usage_example_line_prints_word_for_word(tmp_path, capsys):
    root = _repo(tmp_path)
    _dump(root / "specs" / "apply-discount" / "contract.yaml",
          _contract("apply-discount", [_unit("u1-code-field")]))
    _progress(root, "apply-discount",
              _step("apply-discount/u1-code-field/approve-commit", "doing", "10:00"))
    lines = _lines(root, capsys)
    assert ("    apply-discount/u1-code-field/approve-commit Approve the commit "
            "[waiting on a seat] current seat: user") in lines


def test_sc3_2_the_seats_print_in_confirmed_by_order_each_once(tmp_path, capsys):
    root = _repo(tmp_path, alpha=[_unit("a1-core", ("user", "po", "user"))])
    _progress(root, "alpha", _step("alpha/a1-core/approve-tests", "doing", "10:00"))
    lines = _lines(root, capsys)
    assert _line(lines, "alpha/a1-core/approve-tests") == _task(
        "alpha/a1-core", "approve-tests", f"{WAITING} seat: user, po")


@pytest.mark.parametrize("confirmed_by, rest", [
    pytest.param(MISSING, WAITING, id="no-confirmed-by"),
    pytest.param([], WAITING, id="an-empty-list"),
    pytest.param("user", WAITING, id="not-a-list"),
    pytest.param(None, WAITING, id="null"),
    pytest.param([42, None, "   "], WAITING, id="no-seat-that-is-text"),
    pytest.param(["po", 42, None, "   ", "user"], f"{WAITING} seat: po, user",
                 id="the-text-entries-only"),
])
def test_sc3_2_a_unit_whose_confirmed_by_gives_no_seat_names_none(
        tmp_path, capsys, confirmed_by, rest):
    root = _repo(tmp_path)
    _progress(root, "alpha", _step("alpha/a1-core/approve-tests", "doing", "10:00"))
    # first the unit as intake leaves it: its one seat names itself
    assert _line(_lines(root, capsys), "alpha/a1-core/approve-tests") == _task(
        "alpha/a1-core", "approve-tests", f"{WAITING} seat: user")
    _dump(root / "specs" / "alpha" / "contract.yaml",
          _contract("alpha", [_unit("a1-core", confirmed_by)] + ALPHA[1:]))
    lines = _lines(root, capsys)  # the schema may fail the unit; the tree still prints it
    assert _line(lines, "alpha/a1-core/approve-tests") == _task(
        "alpha/a1-core", "approve-tests", rest)


def test_sc3_2_an_approval_that_does_not_hold_the_current_task_names_no_seat(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "doing", "10:00"),
              _step("alpha/a2-edges/approve-tests", "done", "10:01", by="po"))
    _progress(root, "beta", _step("beta/b1-solo/approve-tests", "doing", "10:05"))
    lines = _lines(root, capsys)
    assert _line(lines, "alpha/a1-core/approve-tests") == _task(
        "alpha/a1-core", "approve-tests", "[doing]")
    assert _line(lines, "alpha/a2-edges/approve-tests") == _task(
        "alpha/a2-edges", "approve-tests", f"[done] by po at {HEAD}")
    assert _line(lines, "alpha/a1-core/approve-commit") == _task(
        "alpha/a1-core", "approve-commit", "[to do]")
    assert _line(lines, "beta/b1-solo/approve-tests") == _task(
        "beta/b1-solo", "approve-tests", f"{WAITING} seat: po")
    assert _seated(lines) == ["beta/b1-solo/approve-tests"]


# --- SC3.2 the query's first line and the pane's approval line ------------------------------

def test_sc3_2_the_querys_first_line_names_the_seat_and_a_blocked_tasks_reason(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha",
              _step("alpha/a2-edges/prove-red", "blocked", "09:00", reason="the runner is down"),
              _step("alpha/a2-edges/approve-commit", "doing", "10:00"))
    pages = {task["id"]: task["page"] for task in tree.task_list()}
    assert _call(["tree", "alpha/a2-edges/approve-commit", "--root", str(root)], capsys) == (0, (
        "alpha/a2-edges/approve-commit Approve the commit [waiting on a seat] current "
        "seat: user, po\n"
        f"page: {pages['approve-commit']}\n"), "")
    assert _call(["tree", "alpha/a2-edges/prove-red", "--root", str(root)], capsys) == (0, (
        "alpha/a2-edges/prove-red Prove red [blocked] because the runner is down\n"
        f"page: {pages['prove-red']}\n"), "")
    assert _call(["tree", "alpha/a2-edges", "--root", str(root)], capsys)[1].splitlines()[0] == (
        "alpha/a2-edges the work for a2-edges is done [waiting on a seat]")


# --- existing behavior 6: taskcontract progress stays the only writer --------------------------

def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


def test_taskcontract_progress_stays_the_only_writer_and_every_state_it_records_reads_as_before(
        tmp_path, capsys):
    root = _repo(tmp_path)
    for argv in (["done", "alpha/a1-core/approve-tests", "--by", "user"],
                 ["start", "alpha/a1-core/write-tests"],
                 ["done", "alpha/a1-core/write-tests"],
                 ["block", "alpha/a1-core/prove-red", "--reason", "the runner is down"],
                 ["done", "beta/b1-solo"],
                 ["start", "alpha/a2-edges/approve-tests"]):
        assert _call(["progress", *argv, "--root", str(root)], capsys)[0] == 0, argv
    before = _snapshot(root)
    lines = _lines(root, capsys)
    _call(["tree", "alpha/a2-edges/approve-tests", "--root", str(root)], capsys)
    assert _snapshot(root) == before  # the print and the query write nothing
    assert [_line(lines, f"alpha/a1-core/{key}") for key in TASK_KEYS[:4]] == [
        _task("alpha/a1-core", "approve-tests", "[done] by user at no commit"),
        _task("alpha/a1-core", "write-tests", "[done] at no commit"),
        _task("alpha/a1-core", "prove-red", "[blocked] because the runner is down"),
        _task("alpha/a1-core", "green", "[to do]")]
    assert _line(lines, "beta/b1-solo") == "  beta/b1-solo the work for b1-solo is done [done] at no commit"
    assert _line(lines, "alpha/a2-edges/approve-tests") == _task(
        "alpha/a2-edges", "approve-tests", f"{WAITING} seat: user, po")
