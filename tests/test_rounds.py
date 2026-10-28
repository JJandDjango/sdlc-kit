"""Rounds suite (contract: execution-team, unit e5-rounds, checks SC4.1, SC4.2,
SC4.3, SC5.1 and SC5.2).

The unit adds three commands to `workflows/tools/task.py` (`fail`, `stop` and
`end`), the rounds file `sdlc-rounds.json` beside the task file in the
repository's git folder, and the draft PR to the Orchestrator's flow
`skills/sdlc/flows/execute.md`. A FAIL goes back to its channel with its
reasons (the members `qa` and `developer` read them as the argument `reasons`);
a third failed round or a question stops the run with the design's own lines;
a run whose last task passes opens one draft PR and never marks it ready or
merges it.

`task.py` runs as a subprocess beside the package the tests import
(`Path(taskcontract.__file__).parents[1]`), so a run against a prototype runs
the prototype's script. Every test builds its own repository under tmp_path,
with `git init`, a config and a ready contract, and passes `--root` to it:
nothing is written into the real repository. The flow and the usage page are
read as text; where `node` is on PATH the members run under a small harness
with a mock `agent`.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract

ROOT = Path(taskcontract.__file__).resolve().parents[1]
TASK_PY = ROOT / "workflows" / "tools" / "task.py"
FLOW = ROOT / "skills" / "sdlc" / "flows" / "execute.md"
PAGE = ROOT / "docs" / "usage" / "the-team.md"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="node is not on PATH")

CONTRACT, U, U2 = "exec-fix", "u1-work", "u2-more"
UNIT, UNIT2 = f"{CONTRACT}/{U}", f"{CONTRACT}/{U2}"
INTENT = ("A fixture contract for the rounds suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")
OPERATORS = [("qa", "QA"), ("qa-verifier", "QA verifier"), ("developer", "Developer"),
             ("dev-verifier", "Dev verifier"), ("receipts", "receipts"),
             ("orchestrator", "Orchestrator")]

STOPPED = "Task {task} failed 3 rounds. The run stops here; the failures follow.\n"
QUESTION = "Task {task} stopped on a question from {operator}: {question}\n"
STARTED = "Task {task}: {operator}, round {round}\n"
NO_GIT = "No git repository at {root}.\n"
REASONS_3 = [
    "2 sketches failed: SC5.1 (src/command_line.cpp:41), SC5.2 (src/command_line.cpp:58)",
    "1 sketch failed: SC5.2 (src/command_line.cpp:58)",
    "1 sketch failed: SC5.2 (src/command_line.cpp:60)",
]


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
                          encoding="utf-8", errors="replace")
    return done.stdout


def make_repo(tmp_path: Path, git_repo: bool = True) -> Path:
    """<tmp>/repo: a declared test command, a ready contract with two units, a
    ratified seat roster, and a git repository."""
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
    if git_repo:
        git(root, "init", "-q")
    return root


def call(tmp_path: Path, root: Path, *args: str):
    """(exit code, stdout, stderr) of `task.py ARGS --root ROOT`, run from a
    folder that is not the repository and with no git repository above the fixture."""
    argv = [sys.executable, str(TASK_PY), *args, "--root", str(root)]
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1"}
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100)
    return done.returncode, done.stdout, done.stderr


def start(tmp_path, root, task="green", operator="developer", unit=UNIT):
    return call(tmp_path, root, "start", "--unit", unit, "--task", task, "--operator", operator)


def fail(tmp_path, root, task="green", reason=None, unit=UNIT):
    extra = ["--reason", reason] if reason is not None else []
    return call(tmp_path, root, "fail", "--unit", unit, "--task", task, *extra)


def end(tmp_path, root, task="green", by=None, unit=UNIT):
    extra = ["--by", by] if by else []
    return call(tmp_path, root, "end", "--unit", unit, "--task", task, *extra)


def stop(tmp_path, root, question="Which exit code?", task="green", operator="developer"):
    return call(tmp_path, root, "stop", "--task", task, "--operator", operator,
                "--question", question)


def task_file(root: Path) -> Path:
    return root / ".git" / "sdlc-task.json"


def rounds_file(root: Path) -> Path:
    return root / ".git" / "sdlc-rounds.json"


def task_json(root: Path) -> dict:
    return json.loads(task_file(root).read_text(encoding="utf-8"))


def records(root: Path) -> list[dict]:
    path = root / ".sdlc" / "progress" / f"{CONTRACT}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["records"] if path.is_file() else []


def snapshot(root: Path) -> dict:
    """Every path under the repository except its git folder, with the bytes."""
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*") if ".git" not in p.relative_to(root).parts}


def failed_rounds(tmp_path, root, task="green", reasons=(None, None)):
    """Fail `task` once per reason, each silent."""
    for reason in reasons:
        assert fail(tmp_path, root, task, reason) == (0, "", "")


# --- SC4.1: a FAIL goes back to its channel; the next round starts from it ----------

def test_sc4_1_a_first_failed_round_is_silent_removes_the_task_file_and_keeps_the_count(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert task_file(root).is_file()
    held = records(root)
    assert fail(tmp_path, root, "green", REASONS_3[0]) == (0, "", "")
    assert not task_file(root).exists()
    assert rounds_file(root) == root / ".git" / "sdlc-rounds.json" and rounds_file(root).is_file()
    assert records(root) == held, "fail writes no progress record"


def test_sc4_1_the_next_start_of_the_task_prints_round_2_then_round_3(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert fail(tmp_path, root, "green", REASONS_3[0]) == (0, "", "")
    assert start(tmp_path, root) == (
        0, STARTED.format(task="green", operator="Developer", round=2), "")
    assert task_json(root) == {"task": "green", "operator": "developer", "round": 2}
    assert fail(tmp_path, root, "green", REASONS_3[1]) == (0, "", "")
    assert not task_file(root).exists()
    assert start(tmp_path, root) == (
        0, STARTED.format(task="green", operator="Developer", round=3), "")
    assert task_json(root) == {"task": "green", "operator": "developer", "round": 3}


def test_sc4_1_a_fail_counts_without_a_task_file_and_each_task_counts_its_own_rounds(tmp_path):
    root = make_repo(tmp_path)
    assert not task_file(root).exists()
    failed_rounds(tmp_path, root, "green", [None])
    failed_rounds(tmp_path, root, "two-key", [None])
    assert start(tmp_path, root, "green") == (
        0, STARTED.format(task="green", operator="Developer", round=2), "")
    task_file(root).unlink()
    assert start(tmp_path, root, "two-key", "dev-verifier") == (
        0, STARTED.format(task="two-key", operator="Dev verifier", round=2), "")
    task_file(root).unlink()
    assert start(tmp_path, root, "write-tests", "qa") == (
        0, STARTED.format(task="write-tests", operator="QA", round=1), "")


def test_sc4_1_a_task_that_ends_keeps_the_failed_rounds_of_its_channel(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [REASONS_3[0]])
    assert start(tmp_path, root)[0] == 0
    assert end(tmp_path, root, "green") == (0, "", "")
    assert not task_file(root).exists() and rounds_file(root).is_file()
    # The two-key FAIL of a later round is the green channel's second failed round.
    assert fail(tmp_path, root, "green", REASONS_3[1]) == (0, "", "")
    assert start(tmp_path, root) == (
        0, STARTED.format(task="green", operator="Developer", round=3), "")


def test_sc4_1_the_rounds_belong_to_one_unit(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [REASONS_3[0], REASONS_3[1]])
    assert start(tmp_path, root, unit=UNIT2) == (
        0, STARTED.format(task="green", operator="Developer", round=1), "")
    # The other unit's first failed round is silent: it carries none of the two above.
    assert fail(tmp_path, root, "green", REASONS_3[2], unit=UNIT2) == (0, "", "")
    assert not task_file(root).exists()


@pytest.mark.parametrize("text", ["", "not json", "[]", "{}", "\"green\"", "{\"rounds\": 3}"],
                         ids=["empty", "not-json", "list", "empty-object", "string", "number"])
def test_sc4_1_a_rounds_file_that_holds_no_counts_is_replaced_by_the_next_fail(tmp_path, text):
    root = make_repo(tmp_path)
    rounds_file(root).write_text(text, encoding="utf-8")
    assert fail(tmp_path, root, "green", REASONS_3[0]) == (0, "", "")
    assert start(tmp_path, root) == (
        0, STARTED.format(task="green", operator="Developer", round=2), "")


def test_sc4_1_in_a_linked_worktree_the_rounds_file_is_in_the_worktrees_own_git_folder(tmp_path):
    root = make_repo(tmp_path)
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@example.com", "-c", "user.name=t",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=no-hooks",
        "commit", "-q", "-m", "seed")
    wt = tmp_path / "wt"
    git(root, "worktree", "add", "-q", "--detach", str(wt))
    wt_git = Path(git(wt, "rev-parse", "--absolute-git-dir").strip())
    assert wt_git != root / ".git" and (wt / ".git").is_file()
    assert fail(tmp_path, wt, "green", REASONS_3[0]) == (0, "", "")
    assert (wt_git / "sdlc-rounds.json").is_file()
    assert not rounds_file(root).exists()
    assert start(tmp_path, wt) == (
        0, STARTED.format(task="green", operator="Developer", round=2), "")


def test_sc4_1_fail_without_a_git_repository_refuses_and_writes_nothing(tmp_path):
    root = make_repo(tmp_path, git_repo=False)
    before = snapshot(root)
    assert fail(tmp_path, root, "green", REASONS_3[0]) == (1, "", NO_GIT.format(root=root))
    assert snapshot(root) == before
    assert not any(p.name == "sdlc-rounds.json" for p in tmp_path.rglob("*"))


# --- SC4.1: the reasons reach the next round's member --------------------------------

HARNESS = r"""
const fs = require('fs')
const [file, cfg] = process.argv.slice(2)
const { args, responses } = JSON.parse(fs.readFileSync(cfg, 'utf8'))
const src = fs.readFileSync(file, 'utf8').replace(/^export const meta/m, 'const meta')
const calls = []
const logs = []
let next = 0
const agent = async (prompt, opts) => {
  calls.push({ prompt, opts })
  return next < responses.length ? responses[next++] : null
}
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const run = new AsyncFunction('args', 'agent', 'log', 'phase', src)
run(args, agent, m => logs.push(String(m)), () => {})
  .then(result => console.log(JSON.stringify({ result: result === undefined ? null : result, calls, logs })))
  .catch(err => console.log(JSON.stringify({ thrown: String((err && err.stack) || err) })))
"""

TEST = {"command": ["run-all.bat"], "file": ["run-one.bat", "{file}"], "build": ["build.bat"]}
WALL = {"functional": ["tests/run_*.bat"], "unit": ["tests/*.cpp"], "code": ["src/"],
        "interface": ["src/*.h"]}
BASE = {"model": "m-from-args", "effort": "e-from-args", "unit": "u1", "contract": "contract-1",
        "repo": "/r"}
DRAFT = {
    "test_file": "tests/run_x.bat", "interface": "NOTE-TEXT",
    "tests": [{"name": "t1", "proves": "SC1.1", "intent": "pins x"}],
    "red_proof": {"command": "prove", "summary": "red", "every_failure_on_the_missing_behavior": True},
    "details_fixed": ["d1"], "questions": [],
}
DEV = {"files_changed": ["src/a.cpp"], "summary": "s", "unit_tests": "1 passed", "suite": "9 passed",
       "deviations": [], "questions": []}
MEMBERS = {
    "qa": ({**BASE, "scratch": "/s", "pluginRoot": "/p", "test": TEST, "wall": WALL,
            "sources": ["specs/c1/contract.yaml"]}, DRAFT),
    "developer": ({**BASE, "branch": "b1", "testFile": "tests/run_x.bat", "scratchRoot": "/s",
                   "files": ["src/a.cpp"], "sources": ["s1"], "interface": "NOTE-TEXT",
                   "test": TEST, "wall": WALL}, DEV),
}
FAILURE_REASONS = ["2 sketches failed: SC5.1 (src/command_line.cpp:41)",
                   "the test list pins no exit code for --frames 0"]


def first_prompt(tmp_path: Path, member: str, **extra) -> str:
    """The prompt of the member's first agent call, run under node with a mock agent."""
    args, response = MEMBERS[member]
    file = ROOT / "workflows" / f"{member}.js"
    assert file.is_file(), f"workflows/{member}.js is not written"
    (tmp_path / "harness.js").write_text(HARNESS, encoding="utf-8")
    (tmp_path / "cfg.json").write_text(
        json.dumps({"args": {**args, **extra}, "responses": [response]}), encoding="utf-8")
    done = subprocess.run([NODE, str(tmp_path / "harness.js"), str(file),
                           str(tmp_path / "cfg.json")], capture_output=True, encoding="utf-8",
                          errors="replace", timeout=60, creationflags=NO_WINDOW)
    assert done.returncode == 0, f"node failed: {done.stderr.strip()}"
    out = json.loads(done.stdout.strip().splitlines()[-1])
    assert "thrown" not in out, out["thrown"]
    assert out["calls"], f"{member} made no agent call"
    return out["calls"][0]["prompt"]


@needs_node
@pytest.mark.parametrize("member", ["qa", "developer"])
def test_sc4_1_the_next_round_prompt_carries_each_reason_of_the_failure(tmp_path, member):
    prompt = first_prompt(tmp_path, member, reasons=FAILURE_REASONS)
    for reason in FAILURE_REASONS:
        assert reason in prompt, reason
    assert prompt.index(FAILURE_REASONS[0]) < prompt.index(FAILURE_REASONS[1])
    # Round 1 has no reasons: an empty list and no argument give the same prompt.
    first = first_prompt(tmp_path, member)
    assert first_prompt(tmp_path, member, reasons=[]) == first
    assert first != prompt and not any(reason in first for reason in FAILURE_REASONS)


@needs_node
@pytest.mark.parametrize("member", ["qa", "developer"])
def test_sc4_1_a_bare_string_reason_reaches_the_prompt_as_one_reason(tmp_path, member):
    prompt = first_prompt(tmp_path, member, reasons="1 sketch failed: SC5.2 (src/a.cpp:58)")
    assert "1 sketch failed: SC5.2 (src/a.cpp:58)" in prompt


# --- SC4.2: a third failed round stops the run ---------------------------------------

def test_sc4_2_a_third_failed_round_prints_the_message_and_one_line_a_round_and_exits_1(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", REASONS_3[:2])
    expected = STOPPED.format(task="green") + "".join(
        f"  Round {n}: {reason}\n" for n, reason in enumerate(REASONS_3, 1))
    assert fail(tmp_path, root, "green", REASONS_3[2]) == (1, expected, "")


def test_sc4_2_a_run_of_three_rounds_ends_with_both_files_removed_and_a_fresh_run_after(tmp_path):
    root = make_repo(tmp_path)
    for round_no, reason in enumerate(REASONS_3[:2], 1):
        assert start(tmp_path, root)[1] == STARTED.format(
            task="green", operator="Developer", round=round_no)
        assert fail(tmp_path, root, "green", reason) == (0, "", "")
    assert start(tmp_path, root)[1] == STARTED.format(
        task="green", operator="Developer", round=3)
    assert task_file(root).is_file() and rounds_file(root).is_file()
    code, out, err = fail(tmp_path, root, "green", REASONS_3[2])
    assert (code, err) == (1, "") and out.startswith(STOPPED.format(task="green"))
    assert not task_file(root).exists() and not rounds_file(root).exists()
    # The stopped run starts no fourth round: what follows is a new run, at round 1.
    assert start(tmp_path, root)[1] == STARTED.format(
        task="green", operator="Developer", round=1)


@pytest.mark.parametrize("task", ["write-tests", "prove-red", "two-key"])
def test_sc4_2_the_message_names_the_task_that_failed_three_rounds(tmp_path, task):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, task, REASONS_3[:2])
    code, out, err = fail(tmp_path, root, task, REASONS_3[2])
    assert (code, err) == (1, "")
    assert out.startswith(STOPPED.format(task=task))
    assert out.count("\n") == 4


def test_sc4_2_a_round_with_no_reason_reads_no_reason_given(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [None, REASONS_3[1]])
    expected = (STOPPED.format(task="green") + "  Round 1: no reason given\n"
                f"  Round 2: {REASONS_3[1]}\n  Round 3: no reason given\n")
    assert fail(tmp_path, root, "green") == (1, expected, "")


def test_sc4_2_a_reason_prints_on_one_line_with_its_whitespace_collapsed(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", ["a\n  b", "  c   d  "])
    code, out, err = fail(tmp_path, root, "green", "e\tf\r\ng")
    assert (code, err) == (1, "")
    assert out == (STOPPED.format(task="green")
                   + "  Round 1: a b\n  Round 2: c d\n  Round 3: e f g\n")


def test_sc4_2_the_failures_of_other_tasks_do_not_join_the_lines(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "write-tests", ["other one", "other two"])
    failed_rounds(tmp_path, root, "green", REASONS_3[:2])
    code, out, err = fail(tmp_path, root, "green", REASONS_3[2])
    assert (code, err) == (1, "")
    assert "other" not in out and out.count("  Round ") == 3


# --- SC4.3: a question stops its task ------------------------------------------------

@pytest.mark.parametrize("operator, printed", OPERATORS, ids=[o for o, _ in OPERATORS])
def test_sc4_3_stop_prints_the_question_message_with_the_operator_name_and_exits_1(
        tmp_path, operator, printed):
    root = make_repo(tmp_path)
    question = "Which exit code does --frames 0 take?"
    assert stop(tmp_path, root, question, "green", operator) == (
        1, QUESTION.format(task="green", operator=printed, question=question), "")


def test_sc4_3_stop_removes_the_task_file_and_the_rounds_file(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert fail(tmp_path, root, "green", REASONS_3[0]) == (0, "", "")
    assert start(tmp_path, root)[0] == 0
    assert task_file(root).is_file() and rounds_file(root).is_file()
    assert stop(tmp_path, root, "Which flag?", "green", "developer") == (
        1, QUESTION.format(task="green", operator="Developer", question="Which flag?"), "")
    assert not task_file(root).exists() and not rounds_file(root).exists()


def test_sc4_3_stop_writes_nothing_else_and_records_no_progress(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    before, held = snapshot(root), records(root)
    assert stop(tmp_path, root, "Which flag?", "write-tests", "qa")[0] == 1
    assert snapshot(root) == before and records(root) == held


def test_sc4_3_a_question_prints_on_one_line_with_its_whitespace_collapsed(tmp_path):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "Which\n  exit   code?\t ") == (
        1, QUESTION.format(task="green", operator="Developer", question="Which exit code?"), "")


def test_sc4_3_stop_needs_no_git_repository(tmp_path):
    root = make_repo(tmp_path, git_repo=False)
    assert stop(tmp_path, root, "Which flag?") == (
        1, QUESTION.format(task="green", operator="Developer", question="Which flag?"), "")


# --- the options of fail, stop and end -----------------------------------------------

USAGE_CASES = [
    (["fail", "--task", "green"], "--unit"),
    (["fail", "--unit", UNIT, "--task", "bogus"], "bogus"),
    (["fail", "--unit", UNIT], "--task"),
    (["stop", "--task", "bogus", "--operator", "developer", "--question", "q"], "bogus"),
    (["stop", "--task", "green", "--operator", "bogus", "--question", "q"], "bogus"),
    (["stop", "--task", "green", "--operator", "developer"], "--question"),
    (["end", "--task", "green"], "--unit"),
    (["end", "--unit", UNIT, "--task", "bogus"], "bogus"),
    (["end", "--unit", UNIT], "--task"),
]


@pytest.mark.parametrize("argv, named", USAGE_CASES,
                         ids=[" ".join(a[:2]) + " -> " + n for a, n in USAGE_CASES])
def test_sc4_1_a_missing_or_unknown_option_is_a_usage_error_and_writes_nothing(
        tmp_path, argv, named):
    root = make_repo(tmp_path)
    before = snapshot(root)
    code, out, err = call(tmp_path, root, *argv)
    assert code == 2 and out == ""
    assert "usage:" in err and named in err
    assert snapshot(root) == before
    assert not task_file(root).exists() and not rounds_file(root).exists()


# --- SC5.1: a run's end ---------------------------------------------------------------

def test_sc5_1_end_records_the_task_done_prints_nothing_and_removes_the_task_file(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert end(tmp_path, root, "write-tests") == (0, "", "")
    assert not task_file(root).exists()
    got = records(root)
    assert [(r["item"], r["state"]) for r in got] == [
        (f"{UNIT}/write-tests", "doing"), (f"{UNIT}/write-tests", "done")]


@pytest.mark.parametrize("task, holder, operator", [
    ("approve-tests", "qa-verifier", "qa-verifier"), ("approve-commit", "receipts", "receipts")])
def test_sc5_1_end_records_an_approval_by_its_holder(tmp_path, task, holder, operator):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, task, operator)[0] == 0
    assert end(tmp_path, root, task, by=holder) == (0, "", "")
    assert not task_file(root).exists()
    last = records(root)[-1]
    assert (last["item"], last["state"], last["by"]) == (f"{UNIT}/{task}", "done", holder)


def test_sc5_1_end_of_an_approval_with_no_holder_prints_the_progress_line_and_keeps_the_file(
        tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "approve-tests", "qa-verifier")[0] == 0
    held, kept = records(root), task_file(root).read_bytes()
    assert end(tmp_path, root, "approve-tests") == (
        1, "", f"taskcontract progress: '{UNIT}/approve-tests' is an approval - done needs "
               "--by <seat>\n")
    assert records(root) == held and task_file(root).read_bytes() == kept


def test_sc5_1_end_of_an_unknown_unit_prints_the_progress_line_and_exits_1(tmp_path):
    root = make_repo(tmp_path)
    assert end(tmp_path, root, "green", unit=f"{CONTRACT}/u9-none") == (
        1, "", f"no node '{CONTRACT}/u9-none/green' - print the tree to list every node id\n")
    assert records(root) == []


def test_sc5_1_end_works_when_no_task_file_stands(tmp_path):
    # The flow removes the task file before it names the task (the wall would refuse a
    # command naming a walled contract id otherwise); end then finds none to remove.
    root = make_repo(tmp_path)
    assert not task_file(root).exists()
    assert end(tmp_path, root, "green") == (0, "", "")
    assert [(r["item"], r["state"]) for r in records(root)] == [(f"{UNIT}/green", "done")]


def test_sc5_1_end_run_removes_both_files_prints_nothing_and_exits_0(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert fail(tmp_path, root, "green", REASONS_3[0]) == (0, "", "")
    assert start(tmp_path, root)[0] == 0
    assert task_file(root).is_file() and rounds_file(root).is_file()
    held = records(root)
    assert call(tmp_path, root, "end", "--run") == (0, "", "")
    assert not task_file(root).exists() and not rounds_file(root).exists()
    assert records(root) == held
    # With no file standing it is the same call, the same silence.
    assert call(tmp_path, root, "end", "--run") == (0, "", "")


# --- the flow: the draft PR, the rounds and the stops --------------------------------

TASKPY = "python {skill-dir}/../../workflows/tools/task.py"
REMOVE_TASK_FILE = "rm -f {gitdir}/sdlc-task.json"
TASKS = ["write-tests", "approve-tests", "prove-red", "green", "approve-commit", "commit",
         "two-key"]
HOLDERS = {"approve-tests": " --by qa-verifier", "approve-commit": " --by receipts"}


def flow() -> str:
    assert FLOW.is_file(), "skills/sdlc/flows/execute.md is not written"
    return FLOW.read_text(encoding="utf-8")


def spans(text: str) -> list[tuple[int, str]]:
    """(offset, text) of each command the flow shows in backticks, in order."""
    return [(m.start(), m[1]) for m in re.finditer(r"`([^`\n]+)`", text)
            if m[1].startswith(("python ", "git ", "rm ", "gh "))]


def task_spans(text: str, verb: str) -> list[tuple[int, str]]:
    return [(at, c) for at, c in spans(text) if c.startswith(f"{TASKPY} {verb} ")
            or c == f"{TASKPY} {verb}"]


def reading(text: str, at: int, command: str) -> str:
    """What the flow says after a command: the text up to the next command span or
    the next blank line."""
    later = [o for o, _ in spans(text) if o > at]
    tail = text[at + len(command) + 2:(later[0] if later else len(text))]
    return tail.split("\n\n")[0]


MEMBER_TASK = {"qa": "write-tests", "developer": "green", "dev-verifier": "two-key"}
CHANNEL_OF = [("qa-verifier", "approve-tests", "write-tests"),
              ("qa-verifier", "prove-red", "write-tests"),
              ("dev-verifier", "two-key", "green"),
              ("qa-verifier", "two-key", "write-tests")]
FAIL_SPAN = f'{TASKPY} fail --unit {{contract}}/{{unit}} --task {{channel}} --reason "{{reasons}}"'
STOP_SPAN = (f'{TASKPY} stop --task {{task}} --operator {{operator}} '
             '--question "{question}"')


def member_segments(text: str) -> list[tuple[str, str, str]]:
    """(member, task, text) for each member the flow starts: the text runs from the
    member's name to the next member, the next `task.py start` or the `gh` command."""
    commands = spans(text)
    cuts = [o for o, c in commands if c.startswith(f"{TASKPY} start ") or c.startswith("gh ")]
    starts = [(m.start(), m[1]) for m in re.finditer(r"\{plugin\}:([\w-]+)", text)]
    out = []
    for i, (at, name) in enumerate(starts):
        stops = [o for o in cuts if o > at] + ([starts[i + 1][0]] if i + 1 < len(starts) else [])
        segment = text[at:min(stops) if stops else len(text)]
        args = re.search(r"args `([^`]*)`", segment)
        named = re.search(r'"task": "([\w-]+)"', args[1]) if args else None
        out.append((name, named[1] if named else MEMBER_TASK.get(name), segment))
    return out


def test_sc5_1_the_flow_runs_one_gh_command_and_it_opens_a_draft_pr_on_the_units_branch():
    found = [c for _, c in spans(flow()) if c.startswith("gh ")]
    assert len(found) == 1, found
    assert found[0].startswith("gh pr create --draft"), found[0]
    assert "--head {branch}" in found[0], found[0]
    # Never ready, never merged: no other gh command, and no flag that does either.
    assert not re.search(r"--ready|--merge|--auto|--no-draft", found[0])
    assert "Draft PR: #{number} {url}" in flow()


def test_sc5_1_the_pr_opens_after_the_last_task_ends_and_before_the_run_ends():
    text = flow()
    last = f"{TASKPY} end --unit {{contract}}/{{unit}} --task two-key"
    assert "`gh pr create --draft" in text, "the flow opens no draft PR"
    assert last in text, "the flow never ends two-key"
    assert text.count(f"{TASKPY} end --run") == 1, "the flow ends the run once"
    pr = text.index("`gh pr create --draft")
    assert text.rindex(last) < pr < text.index(f"{TASKPY} end --run")


@pytest.mark.parametrize("verb", ["fail", "stop"])
def test_sc5_2_a_failed_round_or_a_question_ends_in_a_stop_with_no_pr(verb):
    text = flow()
    found = task_spans(text, verb)
    assert found, f"the flow runs no task.py {verb}"
    commands = spans(text)
    for at, command in found:
        after = reading(text, at, command)
        assert "STOP" in after and "no PR" in after, (command, after)


# The flow holds its rounds in one rule, E2's: a FAIL of a verifier goes back to the
# channel's task through one `task.py fail` command, and a question stops its task
# through one `task.py stop` command. The members' steps (E3 to E9) name the channel.

def test_sc4_1_the_flow_has_one_fail_command_with_the_unit_the_channel_and_the_reasons_whole():
    found = [c for _, c in task_spans(flow(), "fail")]
    assert found == [FAIL_SPAN], found


def test_sc4_1_the_flow_holds_the_reasons_of_the_verifiers_result_as_the_reasons():
    text = flow()
    assert re.search(
        r"HOLD[^\n]*(`reasons`[^\n]*\{reasons\}|\{reasons\}[^\n]*`reasons`)", text), \
        "no line holds the `reasons` of a result as {reasons}"


def test_sc4_1_the_reasons_are_an_empty_list_in_round_1():
    lines = [line for line in flow().split("\n") if "{reasons}" in line and "`[]`" in line]
    assert any("round 1" in line.lower() for line in lines), lines


def test_sc4_1_each_verifier_names_the_channel_a_fail_returns_to():
    segments = member_segments(flow())
    for member, task, channel in CHANNEL_OF:
        mine = [s for m, t, s in segments if (m, t) == (member, task)]
        assert len(mine) == 1, f"the flow starts {member} for {task} {len(mine)} times"
        assert re.findall(r"HOLD \{channel\} as `([\w-]+)`", mine[0]) == [channel], \
            (member, task, mine[0])


def test_sc4_1_after_fail_exit_0_the_flow_starts_the_next_round_of_the_channel_with_the_reasons():
    text = flow()
    found = task_spans(text, "fail")
    assert len(found) == 1, found
    at, command = found[0]
    after = reading(text, at, command)
    assert "exit 0" in after, after
    assert "next round" in after.lower(), after
    assert "{reasons}" in after, after
    # The channel's own step starts the round again: E3 for write-tests, E6 for green.
    assert re.search(r"E3[^\n]*`write-tests`|`write-tests`[^\n]*E3", after), after
    assert re.search(r"E6[^\n]*`green`|`green`[^\n]*E6", after), after


def test_sc4_2_after_fail_exit_1_the_flow_shows_the_output_and_stops_with_no_pr():
    text = flow()
    found = task_spans(text, "fail")
    assert len(found) == 1, found
    at, command = found[0]
    after = reading(text, at, command)
    assert re.search(r"exit 1.*?SHOW.*?output.*?STOP", after, re.S), after
    assert "no PR" in after, after


def test_sc4_3_the_flow_has_one_stop_command_with_the_task_the_operator_and_the_question():
    found = [c for _, c in task_spans(flow(), "stop")]
    assert found == [STOP_SPAN], found


def test_sc4_3_the_flow_holds_the_task_the_operator_and_the_question_of_the_result():
    text = flow()
    assert re.search(r"HOLD[^\n]*\{task\}[^\n]*\{operator\}", text), \
        "no line holds {task} and {operator}"
    assert re.search(
        r"HOLD[^\n]*(`questions`[^\n]*\{question\}|\{question\}[^\n]*`questions`)", text), \
        "no line holds a question of the `questions` of a result as {question}"


def test_sc4_3_after_stop_the_flow_shows_the_output_to_the_user_and_stops_with_no_pr():
    text = flow()
    found = task_spans(text, "stop")
    assert len(found) == 1, found
    at, command = found[0]
    after = reading(text, at, command)
    assert re.search(r"SHOW.*?output.*?STOP", after, re.S), after
    assert "no PR" in after, after


@pytest.mark.parametrize("name", ["qa", "developer"])
def test_sc4_1_the_flow_passes_the_reasons_to_the_member_of_the_next_round(name):
    text = flow()
    starts = [m for m in re.finditer(r"\{plugin\}:" + name + r"(?![\w-])", text)]
    assert starts, f"the flow starts no {name}"
    for found in starts:
        rest = text[found.start():]
        stop_at = re.search(r"\{plugin\}:", rest[1:])
        segment = rest[:stop_at.start() + 1] if stop_at else rest
        args = re.search(r"args `([^`]*)`", segment)
        assert args, f"no args span after {name}"
        assert '"reasons": {reasons}' in args[1], args[1]


def test_sc5_1_the_flow_ends_each_task_through_task_py_end_and_no_longer_calls_progress_done():
    text = flow()
    commands = [c for _, c in spans(text)]
    assert not [c for c in commands if c.startswith("python -m taskcontract progress done")]
    ends = [c for _, c in task_spans(text, "end") if " --run" not in c]
    for task in TASKS:
        prefix = f"{TASKPY} end --unit {{contract}}/{{unit}} --task {task}"
        mine = [c[len(prefix):] for c in ends if c.startswith(prefix)
                and c[len(prefix):len(prefix) + 1] in ("", " ")]
        assert mine, f"the flow never ends {task}"
        assert set(mine) == {HOLDERS.get(task, "")}, (task, mine)


def test_sc5_1_the_flow_removes_the_task_file_just_before_each_command_that_names_the_unit():
    # Backlog Next actions 12: with the task file standing, the wall refuses a command
    # naming a contract id that starts a walled path.
    text = flow()
    commands = spans(text)
    named = [i for i, (_, c) in enumerate(commands)
             if c.startswith((f"{TASKPY} end --unit", f"{TASKPY} fail", f"{TASKPY} stop"))]
    assert len(named) >= 9, f"{len(named)} task.py end, fail and stop commands"
    for i in named:
        assert i > 0 and commands[i - 1][1] == REMOVE_TASK_FILE, commands[i][1]


# --- the usage page -------------------------------------------------------------------

def test_done_means_the_usage_page_marks_rounds_stops_and_the_draft_pr_shipped():
    assert PAGE.is_file(), "docs/usage/the-team.md is not written"
    text = PAGE.read_text(encoding="utf-8")
    assert "#### Rounds, stops and the draft PR 🟢" in text
    for stale in ("until the rounds file ships", "once rounds and the draft PR ship",
                  "Each task runs one round today"):
        assert stale not in text, stale
    for command in ("task.py fail", "task.py stop", "task.py end"):
        assert command in text, command
