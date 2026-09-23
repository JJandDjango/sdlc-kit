"""The check-run suite for ADR 0031 (contract tree-view, unit t4-check-runs).

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

ROW = re.compile(r"^(?P<indent> *)(?P<id>\S+) \[(?P<tag>[^\]]*)\](?P<rest>.*)$")
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
    """[(depth, id, tag, rest)] for every item line of one tree print."""
    code = main(["tree", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 0
    rows = []
    for line in out.splitlines():
        match = ROW.match(line)
        if match:
            rows.append((len(match["indent"]) // 2, match["id"], match["tag"], match["rest"]))
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
    assert _rest(_print(root, capsys), CHECK) == _evidence(GREEN, head) + f" | {SKETCH}"


@needs_git
def test_sc7_1_a_tracked_change_marks_the_run_dirty(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    (root / "README.md").write_text("an edit\n", encoding="utf-8")
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert _records(root)[0]["dirty"] is True
    assert _rest(_print(root, capsys), CHECK) == (
        _evidence(GREEN, head, dirty=True) + f" | {SKETCH}")


@needs_git
def test_sc7_1_an_untracked_file_never_marks_a_run_dirty(tmp_path, capsys):
    root = _repo(tmp_path)
    head = _commit_all(root)
    (root / "notes.txt").write_text("untracked\n", encoding="utf-8")
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    assert _records(root)[0]["dirty"] is False
    assert _rest(_print(root, capsys), CHECK) == _evidence(GREEN, head) + f" | {SKETCH}"


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
    assert _rest(rows, "alpha/a1-core/SC5.1+SC5.2").startswith(_evidence(GREEN, head) + " |")
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
    assert _rest(rows, "alpha/a1-core/SC5.1+SC5.2").startswith(_evidence(GREEN, head) + " |")


def test_sc7_1_outside_git_the_head_reads_no_commit_and_no_dirty_is_set(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _run(root, capsys, CHECK, GREEN)[0] == 0
    record = _records(root)[0]
    assert record["head"] == "no commit"
    assert "dirty" not in record
    assert _rest(_print(root, capsys), CHECK) == _evidence(GREEN, "no commit") + f" | {SKETCH}"


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
        after[cid] = tokens[len(expected)]
    assert after == {"alpha": "dirty", "beta": "|", "gamma": "dirty"}
