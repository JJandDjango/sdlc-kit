"""Restart-sources suite (contract: run-restart, unit rs5-release, check SC4.2).

The design's Sources row 'The tasks already finished': `task.py restart --unit C/U` reads the
progress records of the unit, run.json wins, and a progress record that disagrees with the run is
shown in one line. The JSON line gains one key, `progress`, after `kept`: a list of strings, one
per task BEFORE the task in hand whose last record for C/U/{task} is missing or is not `done`,
in the order write-tests, approve-tests, prove-red, green, approve-commit, commit, two-key:

    Progress record disagrees: {task} reads {state}, but the run is at {in_hand}.

`restart.md` shows each entry before its two questions and names its sources (the run folder, the
progress records, the branch) and no transcript. A flow acts only through its upper-case
instruction words, so the source check is an allow-list lint over `<instructions>`, never a
deny-list: (1) every all-caps word outside the two R4 command spans is in a closed set the test
holds; (2) every RUN is one of the two closed R4 commands, whole from backtick to backtick, or
the R6 prose; (3) the READ sentences equal a closed list; (4) the words `transcript`,
`session log`, `.claude/`, `.jsonl`, `--resume`, `--continue` stand nowhere in the file; (5) a
line holds an even count of backticks. The all-caps check blanks only the contents of the two R4
command spans: an all-caps word inside {braces} or inside any other backticks counts. Each
mutant runs against a copy of `restart.md` in tmp_path, never the real file.
`task.py restart` itself opens the stop record and each progress record and no turn of the
stopped session (an audit hook on `open`): every path it opens under the repository stands in
`.git/` (the run folder, the task file, the rounds file) or is `.sdlc/progress/*.yaml`, besides
python's own imports of the kit. The `--go` help text and the module docstring of
`task.py` say the task file is removed only when it names this unit.

`task.py` runs as a subprocess on a fixture repository under tmp_path (the way
tests/test_restart.py and tests/test_abandoned.py do); nothing is imported from it. The flow is
read as text.
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract
from taskcontract.progress import read_progress

ROOT = Path(taskcontract.__file__).resolve().parents[1]
TASK_PY = ROOT / "workflows" / "tools" / "task.py"
EXECUTE = ROOT / "skills" / "sdlc" / "flows" / "execute.md"
RESTART = ROOT / "skills" / "sdlc" / "flows" / "restart.md"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
CEILING = 12_000

CONTRACT, U, U2 = "exec-fix", "u1-work", "u2-more"
UNIT, UNIT2 = f"{CONTRACT}/{U}", f"{CONTRACT}/{U2}"
BRANCH = "feat/exec-fix-u1-work"
INTENT = ("A fixture contract for the restart-sources suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")
STARTED = "Task {task}: {operator}, round {round}\n"
WRONG_BRANCH = ("Execution did not restart: the run stopped on branch {branch}; "
                "this session is on {current}.\n")
QUESTION = "Which header declares parse_args?"
REASONS = ["2 sketches failed: SC1.1 (a.py:4), SC1.2 (a.py:9)",
           "1 sketch failed: SC1.2 (a.py:9)", "1 sketch failed: SC1.2 (a.py:11)"]
KEYS = ["state", "task", "operator", "round", "kind", "text", "kept", "progress"]

TASKS = ["write-tests", "approve-tests", "prove-red", "green", "approve-commit", "commit",
         "two-key"]
OPERATOR = {"write-tests": "qa", "approve-tests": "qa-verifier", "prove-red": "qa-verifier",
            "green": "developer", "approve-commit": "receipts", "commit": "orchestrator",
            "two-key": "orchestrator"}
PRINTED = {"qa": "QA", "qa-verifier": "QA verifier", "developer": "Developer",
           "receipts": "receipts", "orchestrator": "Orchestrator"}


def disagrees(task: str, state: str, in_hand: str) -> str:
    return f"Progress record disagrees: {task} reads {state}, but the run is at {in_hand}."


# --- the scratch repository ---------------------------------------------------------

def _dump(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _unit(uid: str) -> dict:
    return {"unit": "work for " + uid, "id": uid, "confirmed_by": ["po"],
            "done_means": "the work for " + uid + " is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}


def _document(revision: int) -> str:
    def row(text, by="Ann Lee"):
        return f"| 2026-10-07 | {by} | {text} |\n"
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{CONTRACT}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return (f"# {CONTRACT} - A fixture feature\n\n"
            "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"
            + rows + ready + "\n## Statement\n\nWords.\n")


def _roster(root: Path) -> None:
    vocab = root / "specs" / "vocabulary"
    vocab.mkdir(parents=True, exist_ok=True)
    (vocab / "intake-seat.yaml").write_text(yaml.safe_dump({
        "term": "intake-seat", "name": "Intake seat",
        "definition": "A human position that answers for a decomposition unit at intake.",
        "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
        "since": "2026-08-26"}, sort_keys=False), encoding="utf-8")


def git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                          encoding="utf-8", errors="replace", creationflags=NO_WINDOW)
    return done.stdout


def commit(root: Path, message: str = "seed") -> None:
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@example.com", "-c", "user.name=t",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=no-hooks",
        "commit", "-q", "--allow-empty", "-m", message)


def make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    (tmp_path / "cwd").mkdir()
    (root / ".sdlc").mkdir()
    (root / ".sdlc" / "config.yaml").write_text(
        "kit: fixture\ntest:\n  command: [test.bat]\n", encoding="utf-8")
    _dump(root / "specs" / CONTRACT / "contract.yaml", {
        "id": CONTRACT, "title": "A fixture feature", "intent": INTENT,
        "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
        "decomposition": [_unit(U), _unit(U2)], "dependencies": [], "entities": [],
        "provenance": {"origin": "human-request"}})
    (root / "docs" / "features").mkdir(parents=True)
    (root / "docs" / "features" / f"{CONTRACT}.md").write_text(_document(5), encoding="utf-8")
    (root / "docs" / "features" / f"{CONTRACT}.design.md").write_text(
        _document(4), encoding="utf-8")
    _roster(root)
    git(root, "init", "-q")
    git(root, "symbolic-ref", "HEAD", f"refs/heads/{BRANCH}")
    commit(root)
    return root


def call(tmp_path: Path, root: Path, *args: str, env: dict | None = None):
    argv = [sys.executable, str(TASK_PY), *args, "--root", str(root)]
    full = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1",
            **(env or {})}
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=full, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100,
                          creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


def start(tmp_path, root, task="green", unit=UNIT):
    return call(tmp_path, root, "start", "--unit", unit, "--task", task,
                "--operator", OPERATOR[task])


def end(tmp_path, root, task="green", unit=UNIT):
    by = ["--by", "qa-verifier"] if task == "approve-tests" else []
    return call(tmp_path, root, "end", "--unit", unit, "--task", task, *by)


def fail(tmp_path, root, task="green", reason=REASONS[0], unit=UNIT):
    return call(tmp_path, root, "fail", "--unit", unit, "--task", task, "--reason", reason,
                "--operator", "dev-verifier")


def stop(tmp_path, root, task="green", unit=UNIT):
    return call(tmp_path, root, "stop", "--unit", unit, "--task", task,
                "--operator", OPERATOR[task], "--kind", "question", "--question", QUESTION)


def restart(tmp_path, root, *extra, unit=UNIT):
    return call(tmp_path, root, "restart", "--unit", unit, *extra)


def run_dir(root: Path, unit: str = UNIT) -> Path:
    return root / ".git" / "sdlc-run" / unit


def task_file(root: Path) -> Path:
    return root / ".git" / "sdlc-task.json"


def progress_file(root: Path, stem: str = CONTRACT) -> Path:
    return root / ".sdlc" / "progress" / f"{stem}.yaml"


def snapshot(root: Path) -> dict:
    """Every path under the repository, git folder's sdlc-* entries included, with the bytes."""
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*")
            if ".git" not in p.relative_to(root).parts
            or (len(p.relative_to(root).parts) > 1
                and p.relative_to(root).parts[1].startswith("sdlc-"))}


def one_line(out: str) -> dict:
    assert out.endswith("\n") and out.count("\n") == 1, f"not one JSON line: {out!r}"
    doc = json.loads(out)
    assert "progress" in doc, f"the line has no progress key: {sorted(doc)}"
    return doc


def state_of(tmp_path, root, unit=UNIT) -> dict:
    code, out, err = restart(tmp_path, root, unit=unit)
    assert (code, err) == (0, ""), (code, out, err)
    return one_line(out)


# --- the progress records a test writes ---------------------------------------------

def put_progress(root: Path, rows, stem: str = CONTRACT) -> None:
    """Write `.sdlc/progress/{stem}.yaml` in the format taskcontract/progress.py reads.

    A row is (task, state) or (task, state, seconds); a task without a `/` is the unit's task
    (UNIT/{task}), else the row names the whole item id. The records stand in the rows' order.
    """
    records = []
    for index, row in enumerate(rows):
        item, state, *rest = row
        seconds = rest[0] if rest else index
        record = {"item": item if "/" in item else f"{UNIT}/{item}", "state": state,
                  "head": "abc1234", "dirty": False,
                  "at": f"2026-11-02T10:{seconds // 60:02d}:{seconds % 60:02d}Z"}
        if state == "blocked":
            record["reason"] = "waiting on the user"
        records.append(record)
    _dump(progress_file(root, stem), {"records": records})
    problems: list[str] = []
    held = read_progress(root, problems)
    assert problems == [] and len(held[stem]) == len(rows), (problems, held)


def done_before(task: str) -> list[tuple[str, str]]:
    return [(t, "done") for t in TASKS[:TASKS.index(task)]]


# --- the runs a test starts -----------------------------------------------------------

def abandoned_at(tmp_path: Path, root: Path, task: str = "green") -> None:
    """The session dies with `task` running: its task file stands and no stop is written."""
    assert start(tmp_path, root, task) == (
        0, STARTED.format(task=task, operator=PRINTED[OPERATOR[task]], round=1), "")


def stopped_at(tmp_path: Path, root: Path, task: str = "green") -> None:
    """The task's member asks a question: stop.json is written and the task file is gone."""
    abandoned_at(tmp_path, root, task)
    assert stop(tmp_path, root, task)[0] == 1
    assert not task_file(root).exists()


def failed_thrice(tmp_path: Path, root: Path) -> None:
    """Green fails three rounds: a stop of kind fail."""
    assert start(tmp_path, root, "green")[0] == 0
    for reason in REASONS[:2]:
        assert fail(tmp_path, root, "green", reason) == (0, "", "")
        assert start(tmp_path, root, "green")[0] == 0
    assert fail(tmp_path, root, "green", REASONS[2])[0] == 1
    assert not task_file(root).exists()


def make_run(tmp_path: Path, root: Path, how: str, task: str = "green") -> None:
    {"abandoned": abandoned_at, "stopped": stopped_at}[how](tmp_path, root, task)


HOW = pytest.mark.parametrize("how", ["abandoned", "stopped"])


# --- SC4.2: the progress key on the JSON line ------------------------------------------

@HOW
def test_sc4_2_progress_is_the_last_key_after_kept_and_empty_when_every_earlier_task_is_done(
        tmp_path, how):
    root = make_repo(tmp_path)
    make_run(tmp_path, root, how)
    put_progress(root, done_before("green") + [("green", "doing")])
    code, out, err = restart(tmp_path, root)
    assert (code, err) == (0, ""), (code, out, err)
    line = one_line(out)
    assert list(line) == KEYS, "progress is one more key, the last, after kept"
    assert line["state"] == how and line["task"] == "green"
    assert line["progress"] == []


def test_sc4_2_a_unit_with_no_run_folder_reads_none_with_an_empty_progress(tmp_path):
    root = make_repo(tmp_path)
    put_progress(root, [("green", "doing")])
    before = snapshot(root)
    assert state_of(tmp_path, root) == {
        "state": "none", "task": None, "operator": None, "round": None, "kind": None,
        "text": None, "kept": {}, "progress": []}
    assert snapshot(root) == before


@pytest.mark.parametrize("how, in_hand", [("abandoned", t) for t in TASKS]
                         + [("stopped", "write-tests"), ("stopped", "green"),
                            ("stopped", "two-key")])
def test_sc4_2_each_earlier_task_with_no_record_is_shown_in_the_tasks_order(
        tmp_path, how, in_hand):
    root = make_repo(tmp_path)
    make_run(tmp_path, root, how, in_hand)
    progress_file(root).unlink()
    assert state_of(tmp_path, root)["progress"] == [
        disagrees(t, "no record", in_hand) for t in TASKS[:TASKS.index(in_hand)]]


@pytest.mark.parametrize("state", ["doing", "blocked"])
def test_sc4_2_an_earlier_task_that_reads_doing_or_blocked_is_shown_with_its_state(
        tmp_path, state):
    root = make_repo(tmp_path)
    stopped_at(tmp_path, root, "green")
    put_progress(root, [("write-tests", "done"), ("approve-tests", state),
                        ("prove-red", "done"), ("green", "doing")])
    line = state_of(tmp_path, root)
    assert line["progress"] == [disagrees("approve-tests", state, "green")]
    assert (line["state"], line["task"]) == ("stopped", "green"), "run.json wins"


def test_sc4_2_several_disagreements_are_listed_in_the_tasks_order_not_the_files(tmp_path):
    root = make_repo(tmp_path)
    abandoned_at(tmp_path, root, "two-key")
    put_progress(root, [("green", "blocked"), ("approve-commit", "done"),
                        ("approve-tests", "doing"), ("prove-red", "done"),
                        ("two-key", "doing")])
    assert state_of(tmp_path, root)["progress"] == [
        disagrees("write-tests", "no record", "two-key"),
        disagrees("approve-tests", "doing", "two-key"),
        disagrees("green", "blocked", "two-key"),
        disagrees("commit", "no record", "two-key")]


@pytest.mark.parametrize("states, shown", [
    (["doing", "done"], None),
    (["blocked", "done"], None),
    (["doing", "blocked", "doing", "done"], None),
    (["done", "doing"], "doing"),
    (["done", "blocked"], "blocked"),
    (["done", "doing", "done", "doing"], "doing"),
], ids=["doing-done", "blocked-done", "long-ends-done", "done-doing", "done-blocked",
        "long-ends-doing"])
def test_sc4_2_a_tasks_state_is_its_last_record_in_the_files_order(tmp_path, states, shown):
    root = make_repo(tmp_path)
    abandoned_at(tmp_path, root, "green")
    put_progress(root, [("write-tests", "done"), ("prove-red", "done")]
                 + [("approve-tests", s) for s in states] + [("green", "doing")])
    assert state_of(tmp_path, root)["progress"] == (
        [] if shown is None else [disagrees("approve-tests", shown, "green")])


def test_sc4_2_the_last_record_is_the_one_last_in_the_file_whatever_its_instant(tmp_path):
    root = make_repo(tmp_path)
    abandoned_at(tmp_path, root, "green")
    put_progress(root, [("write-tests", "done"), ("prove-red", "done"),
                        ("approve-tests", "done", 50), ("approve-tests", "doing", 10),
                        ("green", "doing", 60)])
    assert state_of(tmp_path, root)["progress"] == [disagrees("approve-tests", "doing", "green")]


@pytest.mark.parametrize("how, in_hand", [("abandoned", t) for t in TASKS]
                         + [("stopped", "approve-tests"), ("stopped", "green")])
@pytest.mark.parametrize("reads", ["done", "blocked", "no record"])
def test_sc4_2_the_task_in_hand_and_the_tasks_after_it_are_never_compared(
        tmp_path, how, in_hand, reads):
    root = make_repo(tmp_path)
    make_run(tmp_path, root, how, in_hand)
    rows = done_before(in_hand)
    if reads != "no record":
        rows.append((in_hand, reads))
    rows += [(t, "doing") for t in TASKS[TASKS.index(in_hand) + 1:]]
    put_progress(root, rows)
    line = state_of(tmp_path, root)
    assert line["task"] == in_hand
    assert line["progress"] == []


def test_sc4_2_after_a_fail_the_old_record_of_a_later_task_stands_unseen(tmp_path):
    root = make_repo(tmp_path)
    failed_thrice(tmp_path, root)
    put_progress(root, done_before("green") + [("green", "done"), ("approve-commit", "blocked"),
                                               ("commit", "doing"), ("two-key", "doing")])
    line = state_of(tmp_path, root)
    assert (line["state"], line["kind"], line["task"], line["round"]) == (
        "stopped", "fail", "green", 3)
    assert line["progress"] == []
    put_progress(root, [("write-tests", "done"), ("green", "done")])
    assert state_of(tmp_path, root)["progress"] == [
        disagrees("approve-tests", "no record", "green"),
        disagrees("prove-red", "no record", "green")]


@HOW
def test_sc4_2_only_the_records_of_this_contract_and_unit_count(tmp_path, how):
    root = make_repo(tmp_path)
    make_run(tmp_path, root, how, "green")
    put_progress(root, [
        (f"{UNIT2}/write-tests", "done"), (f"{UNIT2}/approve-tests", "done"),
        (f"{UNIT2}/prove-red", "done"), (f"{CONTRACT}/{U}-extra/write-tests", "done"),
        ("approve-tests", "done"), ("prove-red", "done"), ("green", "doing")])
    put_progress(root, [("other/u1-work/write-tests", "done"),
                        ("other/u1-work/approve-tests", "done")], stem="other")
    assert state_of(tmp_path, root)["progress"] == [disagrees("write-tests", "no record", "green")]


def test_sc4_2_each_unit_of_a_contract_is_judged_by_its_own_records(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", UNIT)[0] == 0
    task_file(root).unlink()
    assert start(tmp_path, root, "green", UNIT2)[0] == 0
    put_progress(root, [(f"{UNIT}/write-tests", "done"), (f"{UNIT}/approve-tests", "done"),
                        (f"{UNIT}/prove-red", "done"), (f"{UNIT2}/write-tests", "done")])
    assert state_of(tmp_path, root, UNIT)["progress"] == []
    assert state_of(tmp_path, root, UNIT2)["progress"] == [
        disagrees("approve-tests", "no record", "green"),
        disagrees("prove-red", "no record", "green")]


def test_sc4_2_an_abandoned_task_in_hand_that_is_not_one_of_the_seven_compares_nothing(tmp_path):
    root = make_repo(tmp_path)
    abandoned_at(tmp_path, root, "two-key")
    task_file(root).unlink()
    path = run_dir(root) / "run.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["task"] = "elsewhere"
    path.write_text(json.dumps(doc), encoding="utf-8")
    progress_file(root).unlink()
    line = state_of(tmp_path, root)
    assert (line["state"], line["task"]) == ("abandoned", "elsewhere")
    assert list(line) == KEYS and line["progress"] == []


def test_sc4_2_a_stopped_task_that_is_not_one_of_the_seven_compares_nothing(tmp_path):
    root = make_repo(tmp_path)
    stopped_at(tmp_path, root, "green")
    path = run_dir(root) / "stop.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["task"] = "elsewhere"
    path.write_text(json.dumps(doc), encoding="utf-8")
    put_progress(root, [("green", "doing")])
    line = state_of(tmp_path, root)
    assert (line["state"], line["task"]) == ("stopped", "elsewhere")
    assert list(line) == KEYS and line["progress"] == []


@pytest.mark.parametrize("text", [
    "records: [",
    yaml.safe_dump({"records": [{"item": f"{UNIT}/write-tests", "state": "finished",
                                 "at": "2026-11-02T10:00:00Z"}]}),
], ids=["not-yaml", "bad-state"])
def test_sc4_2_a_progress_file_that_read_progress_drops_counts_as_no_records(tmp_path, text):
    root = make_repo(tmp_path)
    abandoned_at(tmp_path, root, "green")
    progress_file(root).write_text(text, encoding="utf-8")
    problems: list[str] = []
    assert CONTRACT not in read_progress(root, problems), "the fixture is a file that is dropped"
    code, out, err = restart(tmp_path, root)
    assert code == 0, (code, out, err)
    line = one_line(out)
    assert (line["state"], line["task"]) == ("abandoned", "green")
    assert line["progress"] == [disagrees(t, "no record", "green") for t in TASKS[:3]]


# --- SC4.2: run.json wins; the read-only restart writes nothing --------------------------

def test_sc4_2_run_json_wins_the_other_values_stand_and_restart_exits_zero(tmp_path):
    root = make_repo(tmp_path)
    stopped_at(tmp_path, root, "green")
    put_progress(root, [("write-tests", "done"), ("approve-tests", "blocked"),
                        ("green", "done")])
    assert restart(tmp_path, root) == (0, json.dumps({
        "state": "stopped", "task": "green", "operator": "developer", "round": 1,
        "kind": "question", "text": QUESTION, "kept": {},
        "progress": [disagrees("approve-tests", "blocked", "green"),
                     disagrees("prove-red", "no record", "green")]},
        separators=(",", ":")) + "\n", "")
    (tmp_path / "second").mkdir()
    root2 = make_repo(tmp_path / "second")
    abandoned_at(tmp_path / "second", root2, "approve-commit")
    put_progress(root2, [("write-tests", "done")])
    assert state_of(tmp_path / "second", root2) == {
        "state": "abandoned", "task": "approve-commit", "operator": "receipts", "round": 1,
        "kind": None, "text": None, "kept": {},
        "progress": [disagrees("approve-tests", "no record", "approve-commit"),
                     disagrees("prove-red", "no record", "approve-commit"),
                     disagrees("green", "no record", "approve-commit")]}


@HOW
def test_sc4_2_the_read_only_restart_writes_nothing_with_or_without_disagreeing_records(
        tmp_path, how):
    root = make_repo(tmp_path)
    make_run(tmp_path, root, how, "green")
    put_progress(root, [("write-tests", "doing"), ("prove-red", "done"), ("green", "doing")])
    before = snapshot(root)
    assert state_of(tmp_path, root)["progress"] == [
        disagrees("write-tests", "doing", "green"),
        disagrees("approve-tests", "no record", "green")]
    assert snapshot(root) == before, "a disagreeing record is shown, never mended"
    put_progress(root, done_before("green") + [("green", "doing")])
    before = snapshot(root)
    assert state_of(tmp_path, root)["progress"] == []
    assert snapshot(root) == before


@pytest.mark.parametrize("flags", [[], ["--fresh"]], ids=["go", "go-fresh"])
@pytest.mark.parametrize("how", ["abandoned", "stopped", "fail"])
def test_sc4_2_go_prints_the_same_line_as_the_read_only_restart_progress_included(
        tmp_path, how, flags):
    root = make_repo(tmp_path)
    if how == "fail":
        failed_thrice(tmp_path, root)
    else:
        make_run(tmp_path, root, how, "green")
    put_progress(root, [("write-tests", "done"), ("prove-red", "blocked"), ("green", "done")])
    code, read_only, err = restart(tmp_path, root)
    assert (code, err) == (0, ""), (code, read_only, err)
    expected = [disagrees("approve-tests", "no record", "green"),
                disagrees("prove-red", "blocked", "green")]
    assert one_line(read_only)["progress"] == expected
    held = progress_file(root).read_bytes()
    scratch = tmp_path / "fresh-session" / "scratch"
    assert restart(tmp_path, root, "--go", *flags, "--scratch", str(scratch)) == (
        0, read_only, "")
    assert progress_file(root).read_bytes() == held, "--go writes no progress record"
    assert not task_file(root).exists()
    assert not (run_dir(root) / "stop.json").exists()


def test_sc4_2_a_refusal_still_prints_no_json_and_leaves_the_records_alone(tmp_path):
    root = make_repo(tmp_path)
    stopped_at(tmp_path, root, "green")
    put_progress(root, [("write-tests", "done"), ("green", "doing")])
    assert state_of(tmp_path, root)["progress"] == [
        disagrees("approve-tests", "no record", "green"),
        disagrees("prove-red", "no record", "green")]
    git(root, "checkout", "-q", "-b", "other")
    before = snapshot(root)
    assert restart(tmp_path, root) == (
        1, "", WRONG_BRANCH.format(branch=BRANCH, current="other"))
    scratch = tmp_path / "scratch"
    assert restart(tmp_path, root, "--go", "--scratch", str(scratch)) == (
        1, "", WRONG_BRANCH.format(branch=BRANCH, current="other"))
    assert snapshot(root) == before and not scratch.exists()


# --- SC4.2: the records task.py writes itself ----------------------------------------------

def test_sc4_2_the_records_start_and_end_write_agree_with_the_run_and_their_lines_stand(
        tmp_path):
    root = make_repo(tmp_path)
    for task in TASKS[:3]:
        assert start(tmp_path, root, task) == (
            0, STARTED.format(task=task, operator=PRINTED[OPERATOR[task]], round=1), "")
        assert end(tmp_path, root, task) == (0, "", "")
    assert start(tmp_path, root, "green") == (
        0, STARTED.format(task="green", operator="Developer", round=1), "")
    line = state_of(tmp_path, root)
    assert (line["state"], line["task"]) == ("abandoned", "green")
    assert line["progress"] == []


def test_sc4_2_a_task_start_never_ended_shows_as_doing_in_the_real_records(tmp_path):
    root = make_repo(tmp_path)
    for task in ("write-tests", "approve-tests"):
        assert start(tmp_path, root, task)[0] == 0
        assert end(tmp_path, root, task) == (0, "", "")
    assert start(tmp_path, root, "prove-red")[0] == 0
    task_file(root).unlink()
    assert start(tmp_path, root, "green")[0] == 0
    assert state_of(tmp_path, root)["progress"] == [disagrees("prove-red", "doing", "green")]


# --- SC4.2: what `task.py restart` opens -------------------------------------------------------

RUNNER = '''\
import json, os, runpy, sys
from pathlib import Path

opened, calls = [], []


def hook(event, args):
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        opened.append(os.path.abspath(os.fsdecode(args[0])))
    elif event == "subprocess.Popen":
        argv = args[1]
        calls.append(argv if isinstance(argv, str) else [os.fsdecode(a) for a in argv])


task, log = sys.argv[1], sys.argv[2]
sys.argv = [task] + sys.argv[3:]
sys.path.insert(0, os.path.dirname(task))
sys.addaudithook(hook)
code = 0
try:
    runpy.run_path(task, run_name="__main__")
except SystemExit as exc:
    code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
sys.stdout.flush()
Path(log).write_text(json.dumps({"opened": opened, "calls": calls}), encoding="utf-8")
sys.exit(code)
'''


def norm(path) -> str:
    return os.path.normcase(os.path.abspath(str(path)))


def inside(path: str, root: Path) -> bool:
    """True when the normalised path is the repository or stands under it."""
    top = norm(root)
    return path == top or path.startswith(top + os.sep)


def relative(path: str, root: Path) -> str:
    """The normalised path under the repository, with forward slashes."""
    return os.path.relpath(path, norm(root)).replace(os.sep, "/")


def audited_restart(tmp_path: Path, root: Path, *extra: str):
    """Run `task.py restart` under an audit hook; the home folder holds a trap session turn."""
    home = tmp_path / "home"
    trap = home / ".claude" / "projects" / "-repo" / "session.jsonl"
    trap.parent.mkdir(parents=True)
    trap.write_text('{"type": "user", "message": "SENTINEL-TURN"}\n', encoding="utf-8")
    runner, log = tmp_path / "audit_runner.py", tmp_path / "audit.json"
    runner.write_text(RUNNER, encoding="utf-8")
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1",
           "HOME": str(home), "USERPROFILE": str(home)}
    argv = [sys.executable, str(runner), str(TASK_PY), str(log), "restart", "--unit", UNIT,
            *extra, "--root", str(root)]
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100,
                          creationflags=NO_WINDOW)
    assert log.exists(), (done.returncode, done.stdout, done.stderr)
    seen = json.loads(log.read_text(encoding="utf-8"))
    return done, [norm(p) for p in seen["opened"]], seen["calls"], norm(home)


@HOW
def test_sc4_2_the_restart_opens_the_stop_record_and_each_progress_record_and_no_session_turn(
        tmp_path, how):
    root = make_repo(tmp_path)
    make_run(tmp_path, root, how, "green")
    put_progress(root, [("write-tests", "done"), ("green", "doing")])
    put_progress(root, [("other/u1-work/write-tests", "done")], stem="other")
    done, opened, calls, home = audited_restart(tmp_path, root)
    assert (done.returncode, done.stderr) == (0, ""), (done.returncode, done.stdout, done.stderr)
    line = one_line(done.stdout)
    assert (line["state"], line["task"]) == (how, "green")
    assert line["progress"] == [disagrees("approve-tests", "no record", "green"),
                                disagrees("prove-red", "no record", "green")]
    assert "SENTINEL-TURN" not in done.stdout
    assert norm(run_dir(root) / "run.json") in opened, "the run record is read"
    if how == "stopped":
        assert norm(run_dir(root) / "stop.json") in opened, "the stop record is read"
    assert norm(progress_file(root)) in opened, "the progress records are read"
    turns = [p for p in opened if p.startswith(home) or p.endswith(".jsonl")
             or f"{os.sep}.claude{os.sep}" in p]
    assert turns == [], f"the restart opened a turn of a session: {turns}"
    assert all(inside(p, root) or not p.startswith(norm(tmp_path)) for p in opened), (
        "nothing is opened in the test's folder outside the repository")
    strays = [rel for rel in (relative(p, root) for p in opened if inside(p, root))
              if not (rel.startswith(".git/") or re.fullmatch(r"\.sdlc/progress/[^/]+\.yaml", rel))]
    assert strays == [], (f"the restart opens a path of the repository that is not under .git/ "
                          f"or a progress record: {strays}")
    git_only = [c for c in calls
                if os.path.basename((c if isinstance(c, str) else c[0]).split(" ")[0]
                                    ).lower().split(".")[0] != "git"]
    assert git_only == [], f"the restart starts a process that is not git: {git_only}"


# --- SC4.2: the --go help text and the module docstring ----------------------------------------

def collapsed(text: str) -> str:
    return " ".join(text.split())


def test_sc4_2_the_go_help_says_the_task_file_goes_only_when_it_names_this_unit(tmp_path):
    (tmp_path / "cwd").mkdir()
    code, out, err = call(tmp_path, tmp_path, "restart", "--help", env={"COLUMNS": "400"})
    assert code == 0, (code, out, err)
    entry = re.search(r"^\s+--go\s+(.*?)(?=^\s+--fresh)", out, re.M | re.S)
    assert entry, out
    text = collapsed(entry.group(1)).lower()
    assert "task file" in text, text
    assert "only when it names this unit" in text, text


def test_sc4_2_the_module_docstring_says_go_removes_the_task_file_only_when_it_names_this_unit():
    doc = ast.get_docstring(ast.parse(TASK_PY.read_text(encoding="utf-8")))
    assert doc
    text = collapsed(doc)
    assert "only when it names this unit" in text, "the --go paragraph of the docstring"


# --- SC4.2: the flow restart.md --------------------------------------------------------------

def restart_text() -> str:
    return RESTART.read_text(encoding="utf-8")


def purpose_of(text: str) -> str:
    match = re.search(r"<purpose>(.*?)</purpose>", text, re.S)
    assert match, "restart.md has a <purpose> block"
    return collapsed(match.group(1))


def step_of(text: str, step: str, following: str) -> str:
    match = re.search(rf"^{step}\. (.*?)(?=^{following}\. )", text, re.M | re.S)
    assert match, f"restart.md has step {step} before step {following}"
    return match.group(1)


def before_question(step_text: str, question: str) -> str:
    at = step_text.find(question)
    assert at >= 0, f"the step shows {question!r}"
    return collapsed(step_text[:at])


SHOWS_PROGRESS = re.compile(r"\bSHOW\b.{0,200}?\bprogress\b.{0,200}?\bown line\b", re.S)
NEGATION = re.compile(r"\b(?:no|never)\b[^.;]{0,40}\bturn of the stopped session", re.I)

# The source check is an ALLOW-LIST lint over <instructions>: a flow acts only through its
# upper-case instruction words, so anything that is not listed here fails. The sets below are
# read off the restart.md of rs4 (the file this unit extends) and hold nothing else.
DENIED = ("transcript", "session log", ".claude/", ".jsonl", "--resume", "--continue")
STEP_LABELS = {f"R{n}" for n in range(1, 7)} | {f"E{n}" for n in range(2, 10)}
INSTRUCTION_WORDS = {"HOLD", "SHOW", "STOP", "RUN", "READ"}
OTHER_CAPS = {"JSON", "PR", "FAIL", "QA"}
ALLOWED_CAPS = frozenset(STEP_LABELS | INSTRUCTION_WORDS | OTHER_CAPS)
RUN_SHAPES = (
    "python {skill-dir}/../../workflows/tools/task.py restart --unit {contract}/{unit}"
    " --go --scratch {scratch}",
    "python {skill-dir}/../../workflows/tools/task.py restart --unit {contract}/{unit}"
    " --go --fresh --scratch {scratch}",
)
RUN_TAIL_SPANS = frozenset({"fail", "--fresh"})
RUN_PROSE = re.compile(r"RUN\s+the\s+command\s+of\s+its\s+step\s+by\s+the\s+answer\.(?=\s|$)")
READ_SENTENCES = (
    "READ {gitdir}/sdlc-run/{contract}/{unit}/run.json and HOLD its `base` as {base} for E5.",
)
CAPS = re.compile(r"\b[A-Z][A-Z0-9]+\b")
SENTENCE_END = re.compile(r"\.(?=\s|$)")


def instructions_of(text: str) -> str:
    match = re.search(r"<instructions>(.*?)</instructions>", text, re.S)
    assert match, "restart.md has an <instructions> block"
    return match.group(1)


def blank(pattern: str, text: str) -> str:
    """The text with each match turned to spaces, newlines and positions kept."""
    return re.sub(pattern, lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def without_ticks(block: str) -> str:
    return blank(r"`[^`\n]*`", block)


def without_run_commands(block: str) -> str:
    """The text with only the contents of the two R4 command spans turned to spaces.

    A span is the backtick pair after a RUN whose whole content is one of the two closed shapes.
    Braces and every other backtick pair stay in the text, so a word inside them is still read.
    """
    def hide(match: re.Match) -> str:
        if collapsed(match.group(2)) not in RUN_SHAPES:
            return match.group(0)
        return match.group(1) + re.sub(r"[^\n]", " ", match.group(2)) + "`"
    return re.sub(r"(\bRUN\s+`)([^`\n]*)`", hide, block)


def sentence_end(masked: str, start: int) -> int:
    hit = SENTENCE_END.search(masked, start)
    return hit.end() if hit else len(masked)


def source_problems(path: Path) -> list[str]:
    """Every way the flow file at `path` leaves the allow-list; [] when it stays inside."""
    text = path.read_text(encoding="utf-8")
    problems = []
    lower = text.lower()
    for word in DENIED:
        if word in lower:
            problems.append(f"the file names {word!r}")
    block = instructions_of(text)
    for line in block.splitlines():
        if line.count("`") % 2:
            problems.append(f"an unclosed backtick: {line.strip()!r}")
    ticks, bare = without_ticks(block), without_run_commands(block)
    for word in sorted(set(CAPS.findall(bare)) - ALLOWED_CAPS):
        problems.append(f"the all-caps word {word} is not in the closed set")
    for hit in re.finditer(r"\bRUN\b", bare):
        after = block[hit.start():]
        command = re.match(r"RUN\s+`([^`\n]*)`", after)
        if command:
            if collapsed(command.group(1)) not in RUN_SHAPES:
                problems.append(f"RUN of a command outside the two R4 shapes: {command.group(1)!r}")
            tail_from = hit.start() + command.end()
            tail = block[tail_from:sentence_end(ticks, tail_from)]
            if re.search(r"[;&|<>]", tail):
                problems.append(f"a command after the RUN command: {tail!r}")
            spans = re.findall(r"`([^`\n]*)`", tail)
            if set(spans) - RUN_TAIL_SPANS or tail.count("`") != 2 * len(spans):
                problems.append(f"a second command after the RUN command: {tail!r}")
        elif not RUN_PROSE.match(after):
            problems.append(f"RUN of something that is not a command of R4 or the R6 prose: "
                            f"{after[:60]!r}")
    reads = [collapsed(block[hit.start():sentence_end(ticks, hit.start())])
             for hit in re.finditer(r"\bREAD\b", bare)]
    if reads != list(READ_SENTENCES):
        problems.append(f"the READ sentences are {reads}, not the closed list")
    return problems


def shipped_restart() -> str:
    """restart.md as the unit leaves it: it shows the progress entries (so it is the finished
    file the mutations below start from)."""
    text = restart_text()
    assert SHOWS_PROGRESS.search(collapsed(text)), "restart.md shows the progress entries"
    return text


def lint_copy(tmp_path: Path, text: str) -> list[str]:
    """Lint a copy of restart.md in tmp_path; the real file is never touched."""
    copy = tmp_path / "copy" / "restart.md"
    copy.parent.mkdir(exist_ok=True)
    copy.write_text(text, encoding="utf-8")
    return source_problems(copy)


def test_sc4_2_restart_md_names_its_sources_and_no_transcript_source_anywhere():
    text = shipped_restart()
    purpose = purpose_of(text)
    lower = purpose.lower()
    for source in ("run folder", "progress records", "branch"):
        assert source in lower, f"the purpose names {source!r}"
    assert NEGATION.search(purpose), purpose
    assert re.search(r"`progress`|\{progress\}", text), "the flow names the JSON line's progress"
    held = text.lower()
    for word in DENIED:
        assert word not in held, f"restart.md names {word!r}"


def test_sc4_2_restart_md_holds_only_the_closed_instruction_words_commands_and_reads(tmp_path):
    text = shipped_restart()
    block = collapsed(instructions_of(text))
    for shape in RUN_SHAPES:
        assert f"RUN `{shape}`" in block, f"R4 runs {shape!r}"
    assert RUN_PROSE.search(block), "R6 runs the command of its step by the answer"
    assert READ_SENTENCES[0] in block, "R5 reads the run record"
    assert lint_copy(tmp_path, text) == []


MUTATIONS = {
    # an unlisted all-caps verb, with nothing else wrong
    "REPLAY the stopped session":
        lambda t: add_line(t, "REPLAY the stopped session's last turns."),
    "REVIEW the earlier turns":
        lambda t: add_line(t, "REVIEW the earlier turns."),
    "GET the last turns":
        lambda t: add_line(t, "GET the last turns of the stopped session."),
    "CONSULT the earlier turns":
        lambda t: add_line(t, "CONSULT the earlier turns."),
    "RECALL the earlier turns":
        lambda t: add_line(t, "RECALL the earlier turns."),
    "RECALL with no word about turns":
        lambda t: add_line(t, "RECALL the last answer."),
    # an unlisted verb inside braces or inside any backticks other than the two R4 command spans
    "REPLAY inside braces":
        lambda t: add_line(t, "HOLD the value as {REPLAY the turns}."),
    "REPLAY inside nested braces":
        lambda t: add_line(t, "HOLD the value as {a {b REPLAY} c}."),
    "REPLAY inside backticks":
        lambda t: add_line(t, "HOLD the value of `REPLAY` as {x}."),
    "REPLAY inside backticks inside braces":
        lambda t: add_line(t, "HOLD the value as {`REPLAY` the turns}."),
    "REPLAY inside the span of a RUN that is not an R4 command":
        lambda t: add_line(t, "RUN `REPLAY the earlier turns`."),
    # an odd count of backticks on a line, which would hide a verb in a pair that closes late
    "an odd backtick count that would hide REPLAY in a pair":
        lambda t: add_line(t, "HOLD the value of `x and REPLAY the turns` as `y."),
    "an odd backtick count that would hide RECALL in a pair":
        lambda t: add_line(t, "SHOW `the answer and RECALL the earlier turns` and `{x}."),
    "an odd backtick count with nothing else wrong":
        lambda t: add_line(t, "HOLD the value of `task as {task}."),
    "an odd backtick count in the run read":
        lambda t: sub(t, "HOLD its `base` as", "HOLD its `base as"),
    "a step label outside the set":
        lambda t: add_line(t, "R7. HOLD {x} as {y}."),
    "LOAD the session's messages":
        lambda t: add_line(t, "LOAD the stopped session's messages."),
    # a RUN that is not the two closed shapes
    "a second command after ; in the R4 command":
        lambda t: sub(t, "--go --scratch {scratch}`", "--go --scratch {scratch}; type notes.txt`"),
    "a second command after && in the R4 command":
        lambda t: sub(t, "--go --scratch {scratch}`", "--go --scratch {scratch} && cat notes.txt`"),
    "a pipe in the R4 command":
        lambda t: sub(t, "--go --scratch {scratch}`", "--go --scratch {scratch} | more`"),
    "a redirect in the R4 command":
        lambda t: sub(t, "--go --scratch {scratch}`", "--go --scratch {scratch} > out.txt`"),
    "a second command after ; in the fresh R4 command":
        lambda t: sub(t, "--go --fresh --scratch {scratch}`",
                      "--go --fresh --scratch {scratch}; type notes.txt`"),
    "an extra argument in the R4 command":
        lambda t: sub(t, "--go --scratch {scratch}`", "--go --scratch {scratch} --verbose`"),
    "a second command after the closing backtick":
        lambda t: sub(t, "--go --scratch {scratch}`, one Bash call",
                      "--go --scratch {scratch}`; type notes.txt, one Bash call"),
    "a second command after the closing backtick by &&":
        lambda t: sub(t, "--go --scratch {scratch}`, one Bash call",
                      "--go --scratch {scratch}` && cat notes.txt, one Bash call"),
    "a second backticked command after the first":
        lambda t: sub(t, "--go --scratch {scratch}`, one Bash call",
                      "--go --scratch {scratch}`, then `type notes.txt`, one Bash call"),
    "a second backticked command that is one word":
        lambda t: sub(t, "--go --scratch {scratch}`, one Bash call",
                      "--go --scratch {scratch}`, then `more`, one Bash call"),
    "a command before task.py in the R4 command":
        lambda t: sub(t, "RUN `python {skill-dir}", "RUN `type notes.txt; python {skill-dir}"),
    "a path to another script":
        lambda t: sub(t, "workflows/tools/task.py restart --unit {contract}/{unit} --go --scratch",
                      "workflows/tools/other.py restart --unit {contract}/{unit} --go --scratch"),
    "the R6 prose with a second command":
        lambda t: sub(t, "RUN the command of its step by the answer.",
                      "RUN the command of its step by the answer; type notes.txt."),
    "a RUN of prose that is not the R6 prose":
        lambda t: add_line(t, "RUN the earlier turns."),
    "a RUN of git history":
        lambda t: add_line(t, "RUN `git log -5`."),
    "a RUN that reads a session file":
        lambda t: add_line(t, "RUN `cat ~/.claude/projects/x/session.jsonl`."),
    "a RUN that resumes the session":
        lambda t: add_line(t, "RUN `claude --resume`."),
    # a READ outside the closed list
    "a turn inside the run read":
        lambda t: sub(t, "run.json and HOLD",
                      "run.json and the stopped session's earlier turns, and HOLD"),
    "a turn after the run read":
        lambda t: sub(t, "as {base} for E5.",
                      "as {base} for E5 and the stopped session's earlier turns."),
    "a second source in the run read":
        lambda t: sub(t, "run.json and HOLD", "run.json and the session transcript, and HOLD"),
    "a READ of a progress record":
        lambda t: add_line(t, "READ .sdlc/progress/{contract}.yaml and HOLD each record."),
    "a READ of the branch":
        lambda t: add_line(t, "READ `git branch --show-current` and HOLD it as {current}."),
    "a READ of the stop record":
        lambda t: add_line(t, "READ {gitdir}/sdlc-run/{contract}/{unit}/stop.json."),
    "a READ of the task file":
        lambda t: add_line(t, "READ {gitdir}/sdlc-task.json."),
    "a READ of the backlog":
        lambda t: add_line(t, "READ docs/backlog.md."),
    "the run read twice":
        lambda t: add_line(t, READ_SENTENCES[0]),
    "a READ in the continuation step":
        lambda t: re.sub(r"^(\s*)(On an abandoned run there is no answer)",
                         r"\1READ the earlier turns of the session.\n\1\2", t, count=1,
                         flags=re.M),
    # the words that stand nowhere
    "the session transcript":
        lambda t: add_line(t, "READ the stopped session's transcript."),
    "the session log":
        lambda t: add_line(t, "READ the session log for the last turns."),
    "a transcript in the purpose":
        lambda t: NEGATION.sub(lambda m: m.group(0) + ", but its transcript", t, 1),
    "a transcript in the front matter":
        lambda t: sub(t, "description: The Restart flow", "description: The transcript Restart flow"),
    "a session log in the purpose":
        lambda t: NEGATION.sub(lambda m: m.group(0) + ", but its session log", t, 1),
    "a .claude/ folder in a SHOW":
        lambda t: add_line(t, "SHOW the folder `~/.claude/projects`."),
    "a .jsonl file in a SHOW":
        lambda t: add_line(t, "SHOW `session.jsonl`."),
    "--resume in a SHOW":
        lambda t: add_line(t, "SHOW `claude --resume`."),
    "--continue in a SHOW":
        lambda t: add_line(t, "SHOW `claude --continue`."),
}

CONTROLS = {
    "the run read wrapped over two lines":
        lambda t: sub(t, "run.json and HOLD", "run.json\n    and HOLD"),
    "the R6 prose wrapped over two lines":
        lambda t: sub(t, "RUN the command of its step", "RUN the command\n    of its step"),
    "a SHOW line added":
        lambda t: add_line(t, "SHOW the progress entries, each on its own line."),
    "a HOLD line added":
        lambda t: add_line(t, "HOLD the stopped session's `task` as {task}."),
    "lower-case words inside backticks and braces":
        lambda t: add_line(t, "HOLD the value of `path` as {home-dir}, `x` and {y}."),
}


def sub(text: str, old: str, new: str) -> str:
    assert text.count(old) >= 1, f"restart.md holds {old!r}"
    return text.replace(old, new, 1)


def add_line(text: str, line: str) -> str:
    """The text with `line` as a new instruction line after the READ of the run record (R5)."""
    done = re.sub(r"^([^\n]*\bREAD \{gitdir\}/sdlc-run/[^\n]*\n)", lambda m: m.group(1)
                  + "    " + line + "\n", text, count=1, flags=re.M)
    assert done != text, "the READ of the run record stands in restart.md"
    return done


@pytest.mark.parametrize("name", list(MUTATIONS))
def test_sc4_2_a_restart_md_that_leaves_the_allow_list_fails_the_source_check(tmp_path, name):
    text = shipped_restart()
    assert lint_copy(tmp_path, text) == [], "the finished file passes the check it is mutated from"
    mutated = MUTATIONS[name](text)
    assert mutated != text, f"the mutation {name!r} changed the file"
    assert lint_copy(tmp_path, mutated), f"restart.md with {name}, and the check does not fail"


@pytest.mark.parametrize("name", list(CONTROLS))
def test_sc4_2_a_restart_md_edited_inside_the_allow_list_still_passes_the_source_check(
        tmp_path, name):
    text = shipped_restart()
    mutated = CONTROLS[name](text)
    assert mutated != text
    assert lint_copy(tmp_path, mutated) == []


def test_sc4_2_the_mutants_run_on_copies_and_leave_the_real_flow_alone(tmp_path):
    before = restart_text()
    shipped_restart()
    lint_copy(tmp_path, add_line(before, "REPLAY the stopped session's last turns."))
    assert restart_text() == before
    assert (tmp_path / "copy" / "restart.md").read_text(encoding="utf-8") != before


def test_sc4_2_restart_md_shows_each_progress_entry_before_the_abandoned_question():
    r1 = step_of(restart_text(), "R1", "R2")
    pre = before_question(r1, "Execution was abandoned:")
    assert SHOWS_PROGRESS.search(pre), pre


def test_sc4_2_restart_md_shows_each_progress_entry_before_the_stopped_question():
    r2 = step_of(restart_text(), "R2", "R3")
    pre = before_question(r2, "Execution stopped:")
    assert SHOWS_PROGRESS.search(pre), pre


def test_sc4_2_restart_md_and_execute_md_stay_under_the_ceiling_and_restart_md_shows_progress():
    text = shipped_restart()
    assert len(text) <= CEILING, f"restart.md holds {len(text)} of {CEILING} characters"
    held = len(EXECUTE.read_text(encoding="utf-8"))
    assert held <= CEILING, f"execute.md holds {held} of {CEILING} characters"
