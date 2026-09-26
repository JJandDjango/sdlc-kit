"""The progress suite for ADR 0031 (contract tree-view, unit t4-check-runs,
then unit t5-task-writers after its banner below).

`taskcontract progress run CHECK [--expect red|green] -- COMMAND` runs a
check's command in the repo root and records red or green beside the result
the run expected, with the command, the HEAD id, a `dirty` mark and the time,
in `.sdlc/progress/<contract>.yaml`. It exits 0 when the result met the
expectation, else 1. The tree then reads a check `to do`, `doing`, `done` or
`failed` (SC3.2, SC3.3), and a done check names the command of its run and
the commit it ran on, marked `dirty` when a tracked file differed from HEAD
(SC7.1). Three errors exit 2 and write nothing: a command that cannot
start, an id that names no check, and a progress file the writer cannot read.

Each test drives the CLI in process against a fixture repo under tmp_path.
The commands under test are this interpreter's `-c` one-liners, so the suite
runs the same on Windows and Linux; a fixture that needs HEAD makes its own
git repo, with its own config.
"""

from __future__ import annotations

import datetime
import re
import shlex
import shutil
import subprocess
import sys

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")

INTENT = ("A fixture contract for the check-run suite; its units carry the "
          "sketch shapes that check ids come from.")

# An item line: its indent, its id, then its plain name when it has one
# (project-tree o2), then its status in brackets, then the rest of the line.
ROW = re.compile(r"^(?P<indent> *)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                 r"(?P<rest>.*)$")
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
UNKNOWN = "no node '{id}' - print the tree to list every node id\n"
KIND = "taskcontract progress: '{id}' is a {kind}, not a check - run takes a check id\n"

PY = [sys.executable, "-S"]  # no site import: a faster start
GREEN = [*PY, "-c", "raise SystemExit(0)"]
RED = [*PY, "-c", "raise SystemExit(1)"]
CHECK = "alpha/a1-core/SC1.1"
SKETCH = "verify the core prints (SC1.1)"


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


# alpha/a1-core checks SC1.1 and SC5.1+SC5.2, alpha/a2-edges sketch-1, SC2.1
# and sketch-3, beta/b1-solo sketch-1, gamma/l1-lone sketch-1.
ALPHA = [
    _unit("a1-core", [SKETCH, "verify both links print (SC5.1, SC5.2)"]),
    _unit("a2-edges", ["verify an edge holds",
                       "verify it again (SC2.1)",
                       "verify it once more (SC2.1)"], depends_on=["a1-core"]),
]
BETA = [_unit("b1-solo", ["verify the price rounds (by the house rule)"])]
LONE = [_unit("l1-lone", ["verify it holds"])]


def _contract(cid, units):
    """A contract that reads ready-green."""
    return {
        "id": cid,
        "intent": INTENT,
        "scope": ["src/"],
        "non_goals": ["No other work"],
        "decomposition": units,
        "dependencies": [],
        "entities": [],
        "provenance": {"origin": "human-request"},
    }


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _repo(tmp_path, gates=()):
    """alpha and beta, both ready-green, one finding under G0, a README and
    no progress. No gate is active unless named, so no print runs the
    validator (gates/G0 still prints, named by the finding)."""
    root = tmp_path / "repo"
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates)})
    _dump(root / ".sdlc" / "findings" / "slow-gate.yaml", {
        "finding": "slow-gate", "date": "2026-09-22", "kit_pinned": "v0.14.0",
        "diagnostic": "none", "gate": "G0", "kind": "friction", "count": 1,
        "statement": "A fixture finding for the check-run suite.", "proposal": "none"})
    _dump(root / "specs" / "alpha" / "contract.yaml", _contract("alpha", ALPHA))
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA))
    write_seat_roster(root)
    (root / "README.md").write_text("a fixture repo\n", encoding="utf-8")
    return root


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, so a command started in the
    wrong folder shows, and never look for a git repo above the fixture."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    return cwd


# --- git ------------------------------------------------------------------------

def _git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                          encoding="utf-8", errors="replace").stdout


def _commit_all(root):
    """Make `root` a git repo with one commit, free of the machine's git
    config; return its short HEAD id."""
    _git(root, "init", "-q")
    _git(root, "config", "core.autocrlf", "false")  # status compares bytes, here and later
    _git(root, "add", "-A")
    _git(root, "-c", "user.email=t@example.com", "-c", "user.name=t",
         "-c", "commit.gpgsign=false", "-c", "core.hooksPath=no-hooks",
         "commit", "-q", "-m", "seed")
    return _git(root, "rev-parse", "--short", "HEAD").strip()


# --- the CLI --------------------------------------------------------------------

def _run(root, capsys, check, command, *options):
    """(exit code, stdout, stderr) of one `progress run`; `capsys` may be capfd."""
    try:
        code = main(["progress", "run", check, "--root", str(root), *options,
                     "--", *command])
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _print(root, capsys):
    """[(depth, id, tag, rest, name)] for every item line of one tree print."""
    code = main(["tree", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 0
    rows = []
    for line in out.splitlines():
        match = ROW.match(line)
        if match:
            rows.append((len(match["indent"]) // 2, match["id"], match["tag"], match["rest"],
                         match["name"]))
    return rows


def _row(rows, rid):
    for row in rows:
        if row[1] == rid:
            return row
    raise AssertionError(f"{rid} not printed")


def _tag(rows, rid):
    return _row(rows, rid)[2]


def _rest(rows, rid):
    return _row(rows, rid)[3]


def _name(rows, rid):
    """The plain name between an item's id and its status, or None."""
    return _row(rows, rid)[4]


def _records(root, cid="alpha"):
    return yaml.safe_load((root / ".sdlc" / "progress" / f"{cid}.yaml")
                          .read_text(encoding="utf-8"))["records"]


def _snapshot(root):
    """Every path under the root but .git, with each file's bytes."""
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*") if ".git" not in p.relative_to(root).parts}


def _marking(path):
    """A command that leaves a file at `path` when it runs, and exits 0."""
    return [*PY, "-c", f"open({str(path)!r}, 'w').close()"]


def _evidence(command, head, dirty=False):
    return f" via {shlex.join(command)} at {head}" + (" dirty" if dirty else "")


# --- SC3.2 a run judged by its expectation -------------------------------------

def test_sc3_2_never_run_reads_to_do_red_under_expect_red_doing_green_done(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _run(root, capsys, CHECK, RED, "--expect", "red")[0] == 0
    assert _run(root, capsys, "alpha/a1-core/SC5.1+SC5.2", GREEN)[0] == 0
    rows = _print(root, capsys)
    assert _tag(rows, CHECK) == "doing"
    assert _tag(rows, "alpha/a1-core/SC5.1+SC5.2") == "done"
    assert _tag(rows, "alpha/a2-edges/sketch-1") == "to do"


def test_sc3_2_a_met_expectation_exits_0_with_one_result_line(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _run(root, capsys, CHECK, RED, "--expect", "red") == (
        0, f"{CHECK}: red, expected red\n", "")
    assert _run(root, capsys, CHECK, GREEN) == (0, f"{CHECK}: green, expected green\n", "")


def test_sc3_2_expect_green_given_is_the_default(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _run(root, capsys, CHECK, GREEN, "--expect", "green")[0] == 0
    assert _run(root, capsys, "alpha/a1-core/SC5.1+SC5.2", GREEN)[0] == 0
    assert [(r["run"], r["expect"]) for r in _records(root)] == [
        ("green", "green"), ("green", "green")]
    rows = _print(root, capsys)
    assert (_tag(rows, CHECK), _tag(rows, "alpha/a1-core/SC5.1+SC5.2")) == ("done", "done")


def test_sc3_2_a_later_run_is_appended_and_the_tree_reads_the_last(tmp_path, capsys):
    root = _repo(tmp_path)
    hand = {"item": "alpha/a1-core/write-tests", "state": "done",
            "at": "2026-09-22T09:00:00Z", "head": "1a2b3c4", "note": "kept as written"}
    _dump(root / ".sdlc" / "progress" / "alpha.yaml", {"records": [hand]})
    assert _run(root, capsys, CHECK, RED, "--expect", "red")[0] == 0
    assert _tag(_print(root, capsys), CHECK) == "doing"
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    records = _records(root)
    assert records[0] == hand
    assert [(r["item"], r["run"], r["expect"]) for r in records[1:]] == [
        (CHECK, "red", "red"), (CHECK, "green", "green")]
    rows = _print(root, capsys)
    assert (_tag(rows, CHECK), _tag(rows, "alpha/a1-core/write-tests")) == ("done", "done")


# --- SC3.3 a missed expectation --------------------------------------------------

def test_sc3_3_green_under_expect_red_reads_failed_and_exits_1(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _run(root, capsys, CHECK, GREEN, "--expect", "red") == (
        1, f"{CHECK}: green, expected red\n", "")
    assert [(r["run"], r["expect"]) for r in _records(root)] == [("green", "red")]
    assert _tag(_print(root, capsys), CHECK) == "failed"


def test_sc3_3_red_under_the_default_reads_failed_and_exits_1(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _run(root, capsys, CHECK, RED) == (1, f"{CHECK}: red, expected green\n", "")
    assert [(r["run"], r["expect"]) for r in _records(root)] == [("red", "green")]
    rows = _print(root, capsys)
    assert (_tag(rows, CHECK), _tag(rows, "alpha/a1-core"), _tag(rows, "alpha")) == (
        "failed", "failed", "failed")


def test_sc3_3_any_nonzero_exit_is_red(tmp_path, capsys):
    root = _repo(tmp_path)
    three = [*PY, "-c", "raise SystemExit(3)"]
    assert _run(root, capsys, CHECK, three, "--expect", "red")[0] == 0
    assert _records(root)[0]["run"] == "red"


# --- SC7.1 a done check's evidence ------------------------------------------------

@needs_git
def test_sc7_1_a_done_check_names_the_command_of_its_run_and_the_head_id(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    rows = _print(root, capsys)
    assert (_name(rows, CHECK), _rest(rows, CHECK)) == (SKETCH, _evidence(GREEN, head))


@needs_git
def test_sc7_1_a_tracked_change_marks_the_run_dirty(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    (root / "README.md").write_text("an edit\n", encoding="utf-8")
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert _records(root)[0]["dirty"] is True
    rows = _print(root, capsys)
    assert (_name(rows, CHECK), _rest(rows, CHECK)) == (
        SKETCH, _evidence(GREEN, head, dirty=True))


@needs_git
def test_sc7_1_an_untracked_file_never_marks_a_run_dirty(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    (root / "notes.txt").write_text("untracked\n", encoding="utf-8")
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert _records(root)[0]["dirty"] is False
    rows = _print(root, capsys)
    assert (_name(rows, CHECK), _rest(rows, CHECK)) == (SKETCH, _evidence(GREEN, head))


@needs_git
def test_sc7_1_dirty_is_read_before_the_command_runs(tmp_path, capsys):
    root = _repo(tmp_path)
    _commit_all(root)
    edits = [*PY, "-c", "open('README.md', 'w').write('edited by the check')"]
    assert _run(root, capsys, CHECK, edits)[0] == 0
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert [r["dirty"] for r in _records(root)] == [False, True]


@needs_git
def test_sc7_1_only_a_check_whose_last_run_proved_it_names_that_run(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    assert _run(root, capsys, CHECK, RED, "--expect", "red")[0] == 0              # doing
    assert _run(root, capsys, "alpha/a2-edges/SC2.1", RED)[0] == 1                 # failed
    assert _run(root, capsys, "alpha/a1-core/SC5.1+SC5.2", GREEN)[0] == 0         # done
    rows = _print(root, capsys)
    assert _rest(rows, "alpha/a1-core/SC5.1+SC5.2") == _evidence(GREEN, head)
    assert "via" not in _rest(rows, CHECK)
    assert "via" not in _rest(rows, "alpha/a2-edges/SC2.1")
    # a close reads the red check done, but no run proved it green
    records = _records(root) + [{"item": "alpha/a1-core", "state": "done",
                                 "at": "2099-01-01T00:00:00Z", "head": head}]
    _dump(root / ".sdlc" / "progress" / "alpha.yaml", {"records": records})
    rows = _print(root, capsys)
    assert _tag(rows, CHECK) == "done"
    assert "via" not in _rest(rows, CHECK)
    # the same close neither adds nor hides a run: the green check keeps its own
    assert _rest(rows, "alpha/a1-core/SC5.1+SC5.2") == _evidence(GREEN, head)


def test_sc7_1_outside_git_the_head_reads_no_commit_and_no_dirty_is_set(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    record = _records(root)[0]
    assert record["head"] == "no commit"
    assert "dirty" not in record
    rows = _print(root, capsys)
    assert (_name(rows, CHECK), _rest(rows, CHECK)) == (SKETCH, _evidence(GREEN, "no commit"))


# --- the record -------------------------------------------------------------------

@needs_git
def test_a_run_record_holds_item_run_expect_command_head_dirty_and_at(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    before = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    assert _run(root, capsys, CHECK, RED, "--expect", "red")[0] == 0
    after = datetime.datetime.now(datetime.timezone.utc)
    [record] = _records(root)
    assert set(record) == {"item", "run", "expect", "command", "head", "dirty", "at"}
    assert (record["item"], record["run"], record["expect"]) == (CHECK, "red", "red")
    assert record["command"] == shlex.join(RED)
    assert (record["head"], record["dirty"]) == (head, False)
    assert isinstance(record["at"], str) and STAMP.match(record["at"]), record["at"]
    at = datetime.datetime.strptime(record["at"], "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc)
    assert before <= at <= after


# --- where and how the command runs ---------------------------------------------------

def test_the_command_runs_in_the_root_from_its_argv_with_no_shell(tmp_path, capsys, _isolated):
    root = _repo(tmp_path)
    argv = [*PY, "-c",
            "import sys; open('seen.txt', 'w').write(repr(sys.argv[1:]))",
            "a b", ">", "out.txt", "$HOME"]
    assert _run(root, capsys, CHECK, argv)[0] == 0
    assert (root / "seen.txt").read_text() == repr(["a b", ">", "out.txt", "$HOME"])
    assert not (root / "out.txt").exists()
    assert not (_isolated / "seen.txt").exists()
    assert _records(root)[0]["command"] == shlex.join(argv)


def test_the_commands_output_passes_through_before_the_result_line(tmp_path, capfd):
    root = _repo(tmp_path)
    talks = [*PY, "-c",
             "import sys; print('out from the check'); print('err from the check', file=sys.stderr)"]
    code, out, err = _run(root, capfd, CHECK, talks)
    assert "out from the check" in out and "err from the check" in err
    assert out.splitlines()[-1] == f"{CHECK}: green, expected green"
    assert code == 0
    assert out.index("out from the check") < out.index(f"{CHECK}: green")


# --- the folder's .gitignore ------------------------------------------------------

def test_the_first_write_makes_the_folder_with_a_gitignore_of_star(tmp_path, capsys):
    root = _repo(tmp_path)
    folder = root / ".sdlc" / "progress"
    assert not folder.exists()
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert sorted(p.name for p in folder.iterdir()) == [".gitignore", "alpha.yaml"]
    assert (folder / ".gitignore").read_bytes() == b"*\n"


def test_a_folder_without_a_gitignore_gains_one_and_an_existing_one_stays(tmp_path, capsys):
    root = _repo(tmp_path)
    folder = root / ".sdlc" / "progress"
    _dump(folder / "beta.yaml", {"records": []})
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert (folder / ".gitignore").read_bytes() == b"*\n"
    (folder / ".gitignore").write_bytes(b"# kept by hand\n*.yaml\n")
    assert _run(root, capsys, "beta/b1-solo/sketch-1", GREEN)[0] == 0
    assert (folder / ".gitignore").read_bytes() == b"# kept by hand\n*.yaml\n"
    assert _records(root, "beta")[0]["item"] == "beta/b1-solo/sketch-1"


# --- a command that cannot start ------------------------------------------------------

def test_a_command_that_cannot_start_exits_2_and_writes_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    before = _snapshot(root)
    missing = ["no-such-command-t4-check-runs", "--flag"]
    code, out, err = _run(root, capsys, CHECK, missing, "--expect", "red")
    assert re.fullmatch(r"taskcontract progress: cannot start "
                        + re.escape(shlex.join(missing)) + r" \(.+\)\n", err), err
    assert (code, out) == (2, "")
    assert _snapshot(root) == before


# --- the id is checked against the tree, and only a check runs -----------------------

def test_an_unknown_id_exits_2_and_writes_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    marker = tmp_path / "ran"
    before = _snapshot(root)
    for rid in ("alpha/a1-core/SC9.9", "nowhere"):
        code, out, err = _run(root, capsys, rid, _marking(marker))
        assert (code, out, err) == (2, "", UNKNOWN.format(id=rid))
    assert not marker.exists()
    assert _snapshot(root) == before


KINDS = [
    pytest.param("alpha/a1-core/write-tests", "task", id="task"),
    pytest.param("alpha/a1-core", "unit", id="unit"),
    pytest.param("alpha", "contract", id="contract"),
    pytest.param("alpha/G0", "verdict", id="verdict"),
    pytest.param("gates/G0", "gate", id="gate"),
    pytest.param("gates/G0/slow-gate", "finding", id="finding"),
]


@pytest.mark.parametrize("rid, kind", KINDS)
def test_an_id_of_another_kind_exits_2_and_writes_nothing(tmp_path, capsys, rid, kind):
    root = _repo(tmp_path, gates=["G0"])
    marker = tmp_path / "ran"
    before = _snapshot(root)
    code, out, err = _run(root, capsys, rid, _marking(marker))
    assert (code, out, err) == (2, "", KIND.format(id=rid, kind=kind))
    assert not marker.exists()
    assert _snapshot(root) == before


# --- the writer never rewrites records it cannot read --------------------------------

MALFORMED = [
    pytest.param("records: [unclosed\n", id="yaml-error"),
    pytest.param("records:\n- item: alpha/a1-core/write-tests\n  state: finished\n"
                 "  at: '2026-09-22T09:00:00Z'\n", id="unknown-state"),
]


@pytest.mark.parametrize("text", MALFORMED)
def test_a_malformed_progress_file_stops_the_writer_with_one_line(
        tmp_path, capsys, text):
    root = _repo(tmp_path)
    (root / ".sdlc" / "progress").mkdir(parents=True)
    (root / ".sdlc" / "progress" / "alpha.yaml").write_text(text, encoding="utf-8")
    marker = tmp_path / "ran"
    before = _snapshot(root)
    code, out, err = _run(root, capsys, CHECK, _marking(marker))
    assert re.fullmatch(r"taskcontract progress: unreadable progress: "
                        r"\.sdlc/progress/alpha\.yaml \(.+\)\n", err), err
    assert (code, out) == (2, "")
    assert not marker.exists()
    assert _snapshot(root) == before


def test_another_contracts_malformed_file_never_stops_the_writer(tmp_path, capsys):
    root = _repo(tmp_path)
    folder = root / ".sdlc" / "progress"
    folder.mkdir(parents=True)
    (folder / "beta.yaml").write_text("records: [unclosed\n", encoding="utf-8")
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert (folder / "beta.yaml").read_text(encoding="utf-8") == "records: [unclosed\n"
    assert [r["item"] for r in _records(root)] == [CHECK]


# --- a G0 verdict reads dirty when its contract file differs from HEAD ---------------

def _verdict_evidence(cid, head):
    return (f"via python -m taskcontract validate specs/{cid}/contract.yaml "
            f"--profile ready at {head}").split()


@needs_git
def test_a_g0_verdict_reads_dirty_when_its_contract_file_differs_from_head(
        tmp_path, capsys):
    root = _repo(tmp_path, gates=["G0"])
    head = _commit_all(root)
    alpha = root / "specs" / "alpha" / "contract.yaml"
    alpha.write_text(alpha.read_text(encoding="utf-8") + "# an edit\n", encoding="utf-8")
    _dump(root / "specs" / "gamma" / "contract.yaml", _contract("gamma", LONE))  # untracked
    (root / "README.md").write_text("an edit outside every contract\n", encoding="utf-8")
    rows = _print(root, capsys)
    after = {}
    for cid in ("alpha", "beta", "gamma"):
        tokens = _rest(rows, f"{cid}/G0").split()
        expected = _verdict_evidence(cid, head)
        assert tokens[:len(expected)] == expected, cid
        after[cid] = tokens[len(expected):]
    assert after == {"alpha": ["dirty"], "beta": [], "gamma": ["dirty"]}


# ==================================================================================
# Unit t5-task-writers: `progress start`, `done` and `block` (ADR 0031)
#
# `taskcontract progress start|done|block ID` appends one task-step record to
# the contract's progress file, with its time, the HEAD id and a `dirty` mark.
# `done` on approve-tests or approve-commit needs `--by SEAT`, and `block`
# needs `--reason TEXT`. `done` on a unit or a contract closes every task and
# check under it, which backfills history. Each writer checks its id against
# the tree first and never rewrites a file it cannot read. The tree shows a
# done task `at <head>`, a done approval `by <seat> at <head>`, each with
# `dirty` when a tracked file differed from HEAD, and a blocked task
# `because <reason>`.
# ==================================================================================

UNIT = "alpha/a1-core"
TASK = f"{UNIT}/write-tests"
APPROVALS = ("approve-tests", "approve-commit")
REASON = "the runner is down"
NEEDS_BY = "taskcontract progress: '{id}' is an approval - done needs --by <seat>\n"
NO_BY = ("taskcontract progress: '{id}' is not an approval - "
         "only approve-tests and approve-commit take --by\n")
NEEDS_REASON = ("taskcontract progress: block needs --reason <text> - "
                "say why '{id}' is blocked\n")
NOT_A_TASK = ("taskcontract progress: '{id}' is a {kind}, not a task - "
              "{action} takes a task id\n")
NOT_CLOSABLE = ("taskcontract progress: '{id}' is a {kind}, not a task, unit or contract - "
                "done takes a task, unit or contract id\n")
UNREADABLE_ALPHA = (r"taskcontract progress: unreadable progress: "
                    r"\.sdlc/progress/alpha\.yaml \(.+\)\n")


def _mark(root, capsys, action, rid, *options):
    """(exit code, stdout, stderr) of one `progress start|done|block`."""
    try:
        code = main(["progress", action, rid, "--root", str(root), *options])
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _shown(rows, rid):
    """What an item's line shows between its status and its summary (marks,
    evidence, links), with its leading space; '' when it shows none."""
    return _rest(rows, rid).split(" | ", 1)[0]


def _recommit(root, name):
    """Commit one new file at the root; return the new short HEAD id."""
    (root / name).write_text(name + "\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "-c", "user.email=t@example.com", "-c", "user.name=t",
         "-c", "commit.gpgsign=false", "-c", "core.hooksPath=no-hooks",
         "commit", "-q", "-m", name)
    return _git(root, "rev-parse", "--short", "HEAD").strip()


def _hand(root, *records):
    """Seed alpha's progress file by hand."""
    _dump(root / ".sdlc" / "progress" / "alpha.yaml", {"records": list(records)})


# --- the three writers, their lines and their records ---------------------------

def test_each_writer_prints_one_line_on_stdout_and_exits_0(tmp_path, capsys):
    root = _repo(tmp_path)
    approval = f"{UNIT}/approve-tests"
    assert _mark(root, capsys, "start", TASK) == (0, f"{TASK}: doing\n", "")
    assert _mark(root, capsys, "block", TASK, "--reason", REASON) == (
        0, f"{TASK}: blocked\n", "")
    assert _mark(root, capsys, "done", TASK) == (0, f"{TASK}: done\n", "")
    assert _mark(root, capsys, "done", approval, "--by", "user") == (
        0, f"{approval}: done by user\n", "")
    assert _mark(root, capsys, "done", UNIT) == (0, f"{UNIT}: done\n", "")
    assert _mark(root, capsys, "done", "alpha") == (0, "alpha: done\n", "")


@needs_git
def test_each_record_holds_item_state_head_dirty_and_at_plus_by_or_reason(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    approval, prove = f"{UNIT}/approve-tests", f"{UNIT}/prove-red"
    before = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    for call in (("start", TASK), ("done", TASK), ("done", approval, "--by", "user"),
                 ("block", prove, "--reason", REASON), ("done", UNIT)):
        assert _mark(root, capsys, *call)[0] == 0, call
    after = datetime.datetime.now(datetime.timezone.utc)
    records = _records(root)
    base = {"item", "state", "head", "dirty", "at"}
    assert [set(r) for r in records] == [base, base, base | {"by"}, base | {"reason"}, base]
    assert [(r["item"], r["state"]) for r in records] == [
        (TASK, "doing"), (TASK, "done"), (approval, "done"), (prove, "blocked"),
        (UNIT, "done")]
    assert (records[2]["by"], records[3]["reason"]) == ("user", REASON)
    for record in records:
        assert (record["head"], record["dirty"]) == (head, False)
        assert isinstance(record["at"], str) and STAMP.match(record["at"]), record["at"]
        at = datetime.datetime.strptime(record["at"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc)
        assert before <= at <= after


def test_start_reads_doing_and_holds_the_current_task(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _mark(root, capsys, "start", TASK)[0] == 0
    rows = _print(root, capsys)
    assert (_tag(rows, TASK), _shown(rows, TASK)) == ("doing", " current")
    assert (_tag(rows, UNIT), _tag(rows, "alpha")) == ("doing", "doing")


def test_block_reads_blocked_and_shows_its_reason_while_blocked(tmp_path, capsys):
    root = _repo(tmp_path)
    task = "alpha/a2-edges/write-tests"
    assert _mark(root, capsys, "block", task, "--reason", REASON)[0] == 0
    assert _records(root)[0]["reason"] == REASON
    rows = _print(root, capsys)
    assert (_tag(rows, task), _shown(rows, task)) == ("blocked", f" because {REASON}")
    assert _tag(rows, "alpha/a2-edges") == "blocked"
    assert _mark(root, capsys, "start", task)[0] == 0
    rows = _print(root, capsys)
    assert (_tag(rows, task), _shown(rows, task)) == ("doing", " current")


def test_block_without_a_reason_exits_2_and_writes_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    _hand(root, {"item": TASK, "state": "doing", "at": "2026-09-22T09:00:00Z",
                 "head": "1a2b3c4"})
    before = _snapshot(root)
    for options in ((), ("--reason", ""), ("--reason", "   ")):  # missing, empty, blank
        assert _mark(root, capsys, "block", TASK, *options) == (
            2, "", NEEDS_REASON.format(id=TASK)), options
    assert _snapshot(root) == before


def test_start_and_block_take_an_approval_and_every_call_appends_a_record(tmp_path, capsys):
    root = _repo(tmp_path)
    hand = {"item": "alpha/a2-edges/write-tests", "state": "done",
            "at": "2026-09-22T09:00:00Z", "head": "1a2b3c4", "note": "kept as written"}
    _hand(root, hand)
    approval = f"{UNIT}/approve-commit"
    assert _mark(root, capsys, "start", approval)[0] == 0
    rows = _print(root, capsys)
    assert (_tag(rows, approval), _shown(rows, approval)) == ("waiting on a seat", " current")
    assert _mark(root, capsys, "block", approval, "--reason", "the seat is away")[0] == 0
    assert _mark(root, capsys, "done", TASK)[0] == 0
    assert _mark(root, capsys, "done", TASK)[0] == 0
    records = _records(root)
    assert records[0] == hand
    assert [(r["item"], r["state"]) for r in records[1:]] == [
        (approval, "doing"), (approval, "blocked"), (TASK, "done"), (TASK, "done")]
    rows = _print(root, capsys)
    assert (_tag(rows, approval), _shown(rows, approval)) == (
        "blocked", " because the seat is away")


# --- SC7.2 a done task's evidence -----------------------------------------------

@needs_git
def test_sc7_2_a_done_task_shows_the_head_id_of_its_done_call_and_an_approval_its_seat(
        tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    assert _mark(root, capsys, "done", TASK)[0] == 0
    for approval in APPROVALS:
        assert _mark(root, capsys, "done", f"{UNIT}/{approval}", "--by", "user")[0] == 0
    assert _recommit(root, "later.txt") != head  # HEAD moves on after the calls
    rows = _print(root, capsys)
    assert (_tag(rows, TASK), _shown(rows, TASK)) == ("done", f" at {head}")
    assert (_name(rows, TASK), _rest(rows, TASK)) == ("Write the tests", f" at {head}")
    for approval in APPROVALS:
        rid = f"{UNIT}/{approval}"
        assert (_tag(rows, rid), _shown(rows, rid)) == ("done", f" by user at {head}"), rid
    assert (_name(rows, f"{UNIT}/approve-tests"), _rest(rows, f"{UNIT}/approve-tests")) == (
        "Approve the test list", f" by user at {head}")


@needs_git
def test_sc7_2_a_tracked_change_marks_the_done_call_dirty_and_an_untracked_file_never(
        tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    approval = f"{UNIT}/approve-tests"
    (root / "notes.txt").write_text("untracked\n", encoding="utf-8")
    assert _mark(root, capsys, "done", TASK)[0] == 0
    (root / "README.md").write_text("an edit\n", encoding="utf-8")
    assert _mark(root, capsys, "done", approval, "--by", "user")[0] == 0
    assert [r["dirty"] for r in _records(root)] == [False, True]
    rows = _print(root, capsys)
    assert _shown(rows, TASK) == f" at {head}"
    assert _shown(rows, approval) == f" by user at {head} dirty"


def test_sc7_2_outside_git_a_done_task_shows_no_commit_and_records_no_dirty(tmp_path, capsys):
    root = _repo(tmp_path)
    approval = f"{UNIT}/approve-commit"
    assert _mark(root, capsys, "done", TASK)[0] == 0
    assert _mark(root, capsys, "done", approval, "--by", "user")[0] == 0
    records = _records(root)
    assert [r["head"] for r in records] == ["no commit", "no commit"]
    assert not any("dirty" in r for r in records)
    rows = _print(root, capsys)
    assert (_shown(rows, TASK), _shown(rows, approval)) == (
        " at no commit", " by user at no commit")


def test_sc7_2_only_a_task_whose_last_record_is_done_shows_evidence(tmp_path, capsys):
    root = _repo(tmp_path)
    prove = f"{UNIT}/prove-red"
    assert _mark(root, capsys, "done", TASK)[0] == 0
    assert _mark(root, capsys, "start", TASK)[0] == 0  # reopened: doing, the current task
    assert _mark(root, capsys, "done", prove)[0] == 0
    rows = _print(root, capsys)
    assert (_tag(rows, TASK), _shown(rows, TASK)) == ("doing", " current")
    assert (_tag(rows, prove), _shown(rows, prove)) == ("done", " at no commit")
    assert (_tag(rows, f"{UNIT}/green"), _shown(rows, f"{UNIT}/green")) == ("to do", "")


# --- sketch 2: done on an approval needs --by ---------------------------------------

NO_SEAT = ((), ("--by", ""), ("--by", "   "))  # missing, empty, blank


@pytest.mark.parametrize("approval", APPROVALS)
def test_sketch_2_done_on_an_approval_without_by_exits_2_and_writes_nothing(
        tmp_path, capsys, approval):
    root = _repo(tmp_path)
    rid = f"{UNIT}/{approval}"
    _hand(root, {"item": rid, "state": "doing", "at": "2026-09-22T09:00:00Z",
                 "head": "1a2b3c4"})
    before = _snapshot(root)
    for options in NO_SEAT:
        assert _mark(root, capsys, "done", rid, *options) == (
            2, "", NEEDS_BY.format(id=rid)), options
    assert _snapshot(root) == before


def test_sketch_2_with_no_progress_file_a_refused_approval_makes_no_folder(tmp_path, capsys):
    root = _repo(tmp_path)
    before = _snapshot(root)
    for approval in APPROVALS:
        rid = f"{UNIT}/{approval}"
        assert _mark(root, capsys, "done", rid) == (2, "", NEEDS_BY.format(id=rid))
    assert _snapshot(root) == before
    assert not (root / ".sdlc" / "progress").exists()


def test_by_on_a_done_that_is_not_an_approval_exits_2_and_writes_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    before = _snapshot(root)
    for rid in (TASK, UNIT, "alpha"):  # a task, a unit, a contract
        assert _mark(root, capsys, "done", rid, "--by", "user") == (
            2, "", NO_BY.format(id=rid)), rid
    assert _snapshot(root) == before


def test_by_takes_the_seat_as_written_even_off_the_roster(tmp_path, capsys):
    root = _repo(tmp_path)  # the roster lists `user` only
    for approval, seat in (("approve-tests", "claude"), ("approve-commit", "PO seat")):
        rid = f"{UNIT}/{approval}"
        assert _mark(root, capsys, "done", rid, "--by", seat) == (
            0, f"{rid}: done by {seat}\n", "")
    assert [r["by"] for r in _records(root)] == ["claude", "PO seat"]
    rows = _print(root, capsys)
    assert _shown(rows, f"{UNIT}/approve-tests") == " by claude at no commit"
    assert _shown(rows, f"{UNIT}/approve-commit") == " by PO seat at no commit"


# --- sketch 3: done on a contract closes everything under it ------------------------

def test_sketch_3_done_on_a_contract_closes_every_step_and_check_and_reads_it_done(
        tmp_path, capsys):
    root = _repo(tmp_path, gates=["G0"])  # alpha reads ready-green, so its G0 reads done
    assert _mark(root, capsys, "done", "alpha") == (0, "alpha: done\n", "")
    assert [(r["item"], r["state"]) for r in _records(root)] == [("alpha", "done")]
    rows = _print(root, capsys)
    # the inactive next gate, alpha/G1, and its conditions read to do and never count
    under = [row for row in rows if (row[1] == "alpha" or row[1].startswith("alpha/"))
             and not row[1].startswith("alpha/G1")]
    assert len(under) == 26  # the contract, its verdict and its conditions, two units, ...
    assert {tag for _, _, tag, _, _ in under} == {"done"}
    assert _tag(rows, "beta") == "to do"


def test_sketch_3_a_close_reads_done_over_earlier_failed_blocked_and_doing(tmp_path, capsys):
    root = _repo(tmp_path)  # no gate active: G0 inactive, which never counts, and the units
    prove = f"{UNIT}/prove-red"
    assert _run(root, capsys, CHECK, RED)[0] == 1                                # failed
    assert _mark(root, capsys, "block", prove, "--reason", REASON)[0] == 0       # blocked
    assert _mark(root, capsys, "start", "alpha/a2-edges/green")[0] == 0          # doing
    assert _tag(_print(root, capsys), "alpha") == "failed"
    assert _mark(root, capsys, "done", "alpha")[0] == 0
    rows = _print(root, capsys)
    under = [row for row in rows if (row[1] == "alpha" or row[1].startswith("alpha/"))
             and not row[1].startswith("alpha/G0")]
    assert {tag for _, _, tag, _, _ in under} == {"done"}
    assert _shown(rows, prove) == ""  # closed: neither its reason nor evidence of its own


def test_sketch_3_done_on_a_unit_closes_its_steps_and_checks_and_no_other(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _mark(root, capsys, "done", UNIT)[0] == 0
    rows = _print(root, capsys)
    under = [rid for _, rid, _, _, _ in rows if rid.startswith(UNIT + "/")]
    assert len(under) == 9  # seven tasks and two checks
    assert {_tag(rows, rid) for rid in under + [UNIT]} == {"done"}
    assert [_tag(rows, f"alpha/a2-edges/{key}")
            for key in ("write-tests", "sketch-1", "SC2.1", "sketch-3")] == ["to do"] * 4


@needs_git
def test_sketch_3_a_close_shows_its_head_on_its_own_item_and_keeps_each_tasks_own(
        tmp_path, capsys):
    root = _repo(tmp_path)
    first = _commit_all(root)
    approval = f"{UNIT}/approve-tests"
    assert _mark(root, capsys, "done", TASK)[0] == 0
    assert _mark(root, capsys, "done", approval, "--by", "user")[0] == 0
    second = _recommit(root, "second.txt")
    assert _mark(root, capsys, "done", UNIT)[0] == 0
    third = _recommit(root, "third.txt")
    assert _mark(root, capsys, "done", "alpha")[0] == 0
    rows = _print(root, capsys)
    assert _shown(rows, TASK) == f" at {first}"
    assert _shown(rows, approval) == f" by user at {first}"
    assert _shown(rows, f"{UNIT}/prove-red") == ""       # done by a close alone
    assert _shown(rows, "alpha/a2-edges/green") == ""
    assert _shown(rows, UNIT) == f" at {second}"
    # the contract's drift mark (project-tree o3) stands before its evidence
    assert _shown(rows, "alpha") == f" no feature document at {third}"


def test_sketch_3_a_close_never_covers_the_verdict(tmp_path, capsys):
    root = _repo(tmp_path, gates=["G0"])
    beta = _contract("beta", BETA)
    del beta["entities"]  # draft-green, TC017 at ready: the verdict reads to do
    _dump(root / "specs" / "beta" / "contract.yaml", beta)
    assert _mark(root, capsys, "done", "beta")[0] == 0
    rows = _print(root, capsys)
    assert _tag(rows, "beta/b1-solo") == "done"
    assert (_tag(rows, "beta/G0"), _tag(rows, "beta")) == ("to do", "doing")
    # evidence shows only on an item that reads done; the drift mark (project-tree o3) stays
    assert _shown(rows, "beta") == " no feature document"


def test_sketch_3_a_backfill_with_no_progress_file_makes_the_file_and_its_gitignore(
        tmp_path, capsys):
    root = _repo(tmp_path)
    folder = root / ".sdlc" / "progress"
    assert not folder.exists()
    assert _mark(root, capsys, "done", "beta")[0] == 0
    assert sorted(p.name for p in folder.iterdir()) == [".gitignore", "beta.yaml"]
    assert (folder / ".gitignore").read_bytes() == b"*\n"
    assert _tag(_print(root, capsys), "beta") == "done"


# --- each writer checks its id against the tree first ---------------------------------

# Each call is (action, options); an unknown id wins over a missing --by or --reason.
UNKNOWN_CALLS = (("start", ()), ("done", ()), ("done", ("--by", "user")),
                 ("block", ("--reason", REASON)), ("block", ()))


def test_a_task_writer_with_an_unknown_id_exits_2_and_writes_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    before = _snapshot(root)
    for action, options in UNKNOWN_CALLS:
        for rid in ("alpha/a1-core/review", "alpha/a9-none/approve-tests", "nowhere"):
            assert _mark(root, capsys, action, rid, *options) == (
                2, "", UNKNOWN.format(id=rid)), (action, options, rid)
    assert _snapshot(root) == before


# G4 is active so a verdict prints; the kit computes no G4 verdict, so no
# print runs the validator or git.
NOT_TASKS = (("alpha/a1-core/SC1.1", "check"), ("alpha/a1-core", "unit"),
             ("alpha", "contract"), ("alpha/G4", "verdict"), ("gates/G4", "gate"),
             ("gates/G0", "gate"), ("gates/G0/slow-gate", "finding"))


def test_start_and_block_take_only_a_task(tmp_path, capsys):
    root = _repo(tmp_path, gates=["G4"])
    before = _snapshot(root)
    for rid, kind in NOT_TASKS:
        for action, options in (("start", ()), ("block", ("--reason", REASON))):
            assert _mark(root, capsys, action, rid, *options) == (
                2, "", NOT_A_TASK.format(id=rid, kind=kind, action=action)), (action, rid)
    assert _snapshot(root) == before


def test_done_takes_only_a_task_a_unit_or_a_contract(tmp_path, capsys):
    root = _repo(tmp_path, gates=["G4"])
    before = _snapshot(root)
    for rid, kind in NOT_TASKS:
        if kind in ("unit", "contract"):
            continue
        for options in ((), ("--by", "user")):
            assert _mark(root, capsys, "done", rid, *options) == (
                2, "", NOT_CLOSABLE.format(id=rid, kind=kind)), (rid, options)
    assert _snapshot(root) == before


# --- a task writer never rewrites records it cannot read ------------------------------

WRITES = (("start", TASK), ("done", TASK), ("done", f"{UNIT}/approve-tests", "--by", "user"),
          ("block", TASK, "--reason", REASON), ("done", UNIT), ("done", "alpha"))


@pytest.mark.parametrize("text", MALFORMED)
def test_a_malformed_progress_file_stops_every_task_writer_with_one_line(
        tmp_path, capsys, text):
    root = _repo(tmp_path)
    (root / ".sdlc" / "progress").mkdir(parents=True)
    (root / ".sdlc" / "progress" / "alpha.yaml").write_text(text, encoding="utf-8")
    before = _snapshot(root)
    for call in WRITES:
        code, out, err = _mark(root, capsys, *call)
        assert re.fullmatch(UNREADABLE_ALPHA, err), (call, err)
        assert (code, out) == (2, ""), call
    assert _snapshot(root) == before


def test_another_contracts_malformed_file_never_stops_a_task_writer(tmp_path, capsys):
    root = _repo(tmp_path)
    folder = root / ".sdlc" / "progress"
    folder.mkdir(parents=True)
    (folder / "beta.yaml").write_text("records: [unclosed\n", encoding="utf-8")
    assert _mark(root, capsys, "done", TASK) == (0, f"{TASK}: done\n", "")
    assert (folder / "beta.yaml").read_text(encoding="utf-8") == "records: [unclosed\n"
    assert [(r["item"], r["state"]) for r in _records(root)] == [(TASK, "done")]
