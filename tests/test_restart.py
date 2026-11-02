"""Restart suite (contract: run-restart, unit rs2-restart, checks SC2.1, SC2.2, SC2.3
and SC5.3).

A unit's first `task.py start` writes `run.json` in the unit's run folder
`{git folder}/sdlc-run/{contract}/{unit}/` (the unit, the branch, HEAD as the base, the
task in hand, and the values kept). `task.py keep` stores what a passed task hands on.
`task.py restart --unit C/U` reads the run folder and prints one JSON line;
`--go --scratch DIR` removes the stop record and a leftover task file and writes the
kept draft into DIR/draft/. On another branch the SC2.3 line goes to stderr and
nothing starts. The flow `restart.md`, `execute.md`, `SKILL.md` and the four member
scripts are read as text, and the members also run under a mock `agent`.

`task.py` runs as a subprocess on a fixture repository under tmp_path (the way
tests/test_stop_record.py does); nothing is imported from it.
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
WORKFLOWS = ROOT / "workflows"
EXECUTE = ROOT / "skills" / "sdlc" / "flows" / "execute.md"
RESTART = ROOT / "skills" / "sdlc" / "flows" / "restart.md"
SKILL = ROOT / "skills" / "sdlc" / "SKILL.md"
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="node is not on PATH")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
CEILING = 12_000

CONTRACT, U, U2 = "exec-fix", "u1-work", "u2-more"
UNIT, UNIT2 = f"{CONTRACT}/{U}", f"{CONTRACT}/{U2}"
BRANCH = "feat/exec-fix-u1-work"
INTENT = ("A fixture contract for the restart suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")
STARTED = "Task {task}: {operator}, round {round}\n"
R3 = ["2 sketches failed: SC1.1 (a.py:4), SC1.2 (a.py:9)", "1 sketch failed: SC1.2 (a.py:9)",
      "1 sketch failed: SC1.2 (a.py:11)"]
DRAFT = {"test_file": "tests/test_cli.py", "interface": "parse_args(argv) -> Args",
         "tests": [{"name": "t1", "proves": "SC1.1", "intent": "pins parse_args"}],
         "red_proof": {"command": "prove", "summary": "red"}, "questions": []}
DRAFT_BYTES = b"def test_parse_args():\n    assert False\n"
KEPT_AT_GREEN = {"draft": DRAFT, "draft-file": "draft/test_cli.py"}
KEYS = {"state", "task", "operator", "round", "kind", "text", "kept"}
NONE = {"state": "none", "task": None, "operator": None, "round": None, "kind": None,
        "text": None, "kept": {}}
WRONG_BRANCH = "Execution did not restart: the run stopped on branch {branch}; this session is on {current}.\n"
NOT_PARSED = "Execution did not restart: {name} of {contract} unit {unit} does not parse.\n"
NO_RUN_JSON = "Execution did not restart: stop.json of {contract} unit {unit} has no run.json.\n"


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


def make_repo(tmp_path: Path, with_commit: bool = True) -> Path:
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
    if with_commit:
        commit(root)
    return root


def call(tmp_path: Path, root: Path, *args: str):
    argv = [sys.executable, str(TASK_PY), *args, "--root", str(root)]
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1"}
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100,
                          creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


def start(tmp_path, root, task="green", operator="developer", unit=UNIT):
    return call(tmp_path, root, "start", "--unit", unit, "--task", task, "--operator", operator)


def end(tmp_path, root, task="green", by=None, unit=UNIT):
    extra = ["--by", by] if by else []
    return call(tmp_path, root, "end", "--unit", unit, "--task", task, *extra)


def fail(tmp_path, root, task="green", reason=None, unit=UNIT, operator=None):
    extra = ["--reason", reason] if reason is not None else []
    extra += ["--operator", operator] if operator else []
    return call(tmp_path, root, "fail", "--unit", unit, "--task", task, *extra)


def stop(tmp_path, root, question="Which exit code?", task="green", operator="developer",
         kind="question", unit=UNIT):
    return call(tmp_path, root, "stop", "--unit", unit, "--task", task, "--operator", operator,
                "--kind", kind, "--question", question)


def keep(tmp_path, root, key, value=None, file=None, unit=UNIT):
    extra = ["--value", value] if value is not None else ["--file", str(file)]
    return call(tmp_path, root, "keep", "--unit", unit, "--key", key, *extra)


def restart(tmp_path, root, *extra, unit=UNIT):
    return call(tmp_path, root, "restart", "--unit", unit, *extra)


def gitdir(root: Path) -> Path:
    return root / ".git"


def run_dir(root: Path, unit: str = UNIT) -> Path:
    return gitdir(root) / "sdlc-run" / unit


def task_file(root: Path) -> Path:
    return gitdir(root) / "sdlc-task.json"


def load(path: Path):
    assert path.is_file(), f"{path} is not written"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        raise AssertionError(f"{path} does not hold JSON") from None


def run_json(root: Path, unit: str = UNIT) -> dict:
    return load(run_dir(root, unit) / "run.json")


def head(root: Path) -> str:
    return git(root, "rev-parse", "HEAD").strip()


def records(root: Path) -> list[dict]:
    path = root / ".sdlc" / "progress" / f"{CONTRACT}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["records"] if path.is_file() else []


def snapshot(root: Path) -> dict:
    """Every path under the repository, git folder's sdlc-* entries included, with the bytes."""
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*")
            if ".git" not in p.relative_to(root).parts
            or (len(p.relative_to(root).parts) > 1
                and p.relative_to(root).parts[1].startswith("sdlc-"))}


def state_of(tmp_path, root, unit=UNIT) -> dict:
    code, out, err = restart(tmp_path, root, unit=unit)
    assert (code, err) == (0, ""), (code, out, err)
    assert out.endswith("\n") and out.count("\n") == 1, f"not one JSON line: {out!r}"
    got = json.loads(out)
    assert set(got) == KEYS, sorted(got)
    return got


def scratch_draft(tmp_path: Path) -> Path:
    path = tmp_path / "qa-scratch" / "draft" / "tests" / "test_cli.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(DRAFT_BYTES)
    return path


def passes_to_green(tmp_path: Path, root: Path, unit: str = UNIT) -> None:
    """QA's tasks pass and keep what they hand on; green is then in hand (task file standing)."""
    assert start(tmp_path, root, "write-tests", "qa", unit)[0] == 0
    assert keep(tmp_path, root, "draft", json.dumps(DRAFT), unit=unit) == (0, "", "")
    assert keep(tmp_path, root, "draft-file", file=scratch_draft(tmp_path), unit=unit) == (0, "", "")
    assert end(tmp_path, root, "write-tests", unit=unit) == (0, "", "")
    assert start(tmp_path, root, "approve-tests", "qa-verifier", unit)[0] == 0
    assert end(tmp_path, root, "approve-tests", "qa-verifier", unit) == (0, "", "")
    assert start(tmp_path, root, "prove-red", "qa-verifier", unit)[0] == 0
    assert end(tmp_path, root, "prove-red", unit=unit) == (0, "", "")
    assert start(tmp_path, root, "green", "developer", unit)[0] == 0


def stopped_at_green(tmp_path: Path, root: Path, question="Which header declares parse_args?"):
    """QA passed, green failed one round, green's second round stopped on a question."""
    passes_to_green(tmp_path, root)
    assert fail(tmp_path, root, "green", R3[0]) == (0, "", "")
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert stop(tmp_path, root, question)[0] == 1


# --- run.json: written by task.py start, stop and kept by keep -----------------------

def test_sc2_1_the_first_start_of_a_unit_writes_run_json_and_prints_the_line_as_today(tmp_path):
    root = make_repo(tmp_path)
    assert not (gitdir(root) / "sdlc-run").exists()
    assert start(tmp_path, root, "write-tests", "qa") == (
        0, STARTED.format(task="write-tests", operator="QA", round=1), "")
    assert run_json(root) == {"unit": UNIT, "branch": BRANCH, "base": head(root),
                              "task": "write-tests", "kept": {}}


def test_sc2_1_a_later_start_sets_the_task_in_hand_and_keeps_branch_base_and_kept(tmp_path):
    root = make_repo(tmp_path)
    first = head(root)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert keep(tmp_path, root, "commit", "3f2a1bc") == (0, "", "")
    assert end(tmp_path, root, "write-tests") == (0, "", "")
    commit(root, "moves HEAD on")
    assert head(root) != first
    assert start(tmp_path, root, "approve-tests", "qa-verifier")[0] == 0
    assert run_json(root) == {"unit": UNIT, "branch": BRANCH, "base": first,
                              "task": "approve-tests", "kept": {"commit": "3f2a1bc"}}


def test_sc2_1_a_repository_with_no_commit_gives_a_null_base(tmp_path):
    root = make_repo(tmp_path, with_commit=False)
    assert start(tmp_path, root, "write-tests", "qa") == (
        0, STARTED.format(task="write-tests", operator="QA", round=1), "")
    assert run_json(root) == {"unit": UNIT, "branch": BRANCH, "base": None,
                              "task": "write-tests", "kept": {}}


def test_sc2_1_the_task_file_names_its_unit(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer", UNIT)[0] == 0
    assert load(task_file(root)).get("unit") == UNIT
    task_file(root).unlink()
    assert start(tmp_path, root, "green", "developer", UNIT2)[0] == 0
    assert load(task_file(root)).get("unit") == UNIT2


def test_sc2_1_each_unit_has_a_run_json_of_its_own(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa", UNIT)[0] == 0
    assert end(tmp_path, root, "write-tests", unit=UNIT) == (0, "", "")
    assert start(tmp_path, root, "green", "developer", UNIT2)[0] == 0
    assert run_json(root, UNIT)["task"] == "write-tests" and run_json(root, UNIT)["unit"] == UNIT
    assert run_json(root, UNIT2)["task"] == "green" and run_json(root, UNIT2)["unit"] == UNIT2


def test_sc2_1_a_refused_start_writes_nothing_first_or_later(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer", UNIT)[0] == 0
    before = snapshot(root)
    # The task file of UNIT stands, so the first start of UNIT2 is refused.
    assert start(tmp_path, root, "write-tests", "qa", UNIT2)[0] == 1
    assert not run_dir(root, UNIT2).exists()
    # And a later start of UNIT is refused with its run.json untouched.
    assert start(tmp_path, root, "two-key", "dev-verifier", UNIT)[0] == 1
    assert run_json(root, UNIT)["task"] == "green"
    assert snapshot(root) == before


def test_sc2_1_a_stop_with_no_run_json_writes_one_with_the_stops_task(tmp_path):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "Which flag?", "green", "developer", "question")[0] == 1
    assert run_json(root) == {"unit": UNIT, "branch": BRANCH, "base": head(root),
                              "task": "green", "kept": {}}


def test_sc2_1_a_refused_first_start_then_its_refusal_stop_leaves_a_run_json_to_restart_from(
        tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer", UNIT)[0] == 0
    code, out, err = start(tmp_path, root, "two-key", "dev-verifier", UNIT2)
    refused = (out + err).strip()
    assert code == 1 and refused
    assert stop(tmp_path, root, refused, "two-key", "dev-verifier", "refusal", UNIT2) == (1, "", "")
    assert run_json(root, UNIT2) == {"unit": UNIT2, "branch": BRANCH, "base": head(root),
                                     "task": "two-key", "kept": {}}
    got = state_of(tmp_path, root, UNIT2)
    assert (got["state"], got["task"], got["kind"], got["text"]) == (
        "stopped", "two-key", "refusal", refused)


def test_sc2_1_a_stop_keeps_the_run_json_that_stands_byte_for_byte(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert keep(tmp_path, root, "commit", "3f2a1bc") == (0, "", "")
    assert end(tmp_path, root, "write-tests") == (0, "", "")
    held = (run_dir(root) / "run.json").read_bytes()
    assert stop(tmp_path, root, "Which flag?", "green", "developer", "question")[0] == 1
    assert (run_dir(root) / "run.json").read_bytes() == held
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["run.json", "stop.json"]


def test_sc2_1_the_failed_rounds_and_a_third_fail_keep_the_run_json_byte_for_byte(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert (run_dir(root) / "run.json").is_file(), "the start wrote run.json"
    held = (run_dir(root) / "run.json").read_bytes()
    assert fail(tmp_path, root, "green", R3[0], operator="dev-verifier") == (0, "", "")
    assert (run_dir(root) / "run.json").read_bytes() == held
    assert fail(tmp_path, root, "green", R3[1], operator="dev-verifier") == (0, "", "")
    assert fail(tmp_path, root, "green", R3[2], operator="dev-verifier")[0] == 1
    assert (run_dir(root) / "run.json").read_bytes() == held
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["rounds.json", "run.json", "stop.json"]


# --- task.py keep -------------------------------------------------------------------

def test_sc2_1_keep_stores_a_draft_and_receipts_as_parsed_json_and_a_commit_as_text(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    receipts = {"ok": True, "commands": [{"command": ["test.bat"], "exit_code": 0}]}
    assert keep(tmp_path, root, "draft", json.dumps(DRAFT)) == (0, "", "")
    assert keep(tmp_path, root, "receipts", json.dumps(receipts)) == (0, "", "")
    # All digits, yet text: a commit is never parsed.
    assert keep(tmp_path, root, "commit", "1234567") == (0, "", "")
    held = run_json(root)
    assert held["kept"] == {"draft": DRAFT, "receipts": receipts, "commit": "1234567"}
    assert held["task"] == "write-tests"


def test_sc2_1_keep_with_a_file_reads_the_json_of_a_draft_from_it(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    source = tmp_path / "draft.json"
    source.write_text(json.dumps(DRAFT), encoding="utf-8")
    assert keep(tmp_path, root, "draft", file=source) == (0, "", "")
    assert run_json(root)["kept"] == {"draft": DRAFT}


def test_sc2_1_keep_a_draft_file_copies_it_into_the_run_folder_and_names_it_in_kept(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert keep(tmp_path, root, "draft-file", file=scratch_draft(tmp_path)) == (0, "", "")
    assert run_json(root)["kept"] == {"draft-file": "draft/test_cli.py"}
    assert (run_dir(root) / "draft" / "test_cli.py").read_bytes() == DRAFT_BYTES
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["draft", "run.json"]


def test_sc2_1_a_second_keep_replaces_its_key_and_leaves_the_others_and_the_run_alone(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert keep(tmp_path, root, "draft", json.dumps(DRAFT)) == (0, "", "")
    assert keep(tmp_path, root, "commit", "aaaaaaa") == (0, "", "")
    first = run_json(root)
    assert keep(tmp_path, root, "commit", "bbbbbbb") == (0, "", "")
    second = run_json(root)
    assert second["kept"] == {"draft": DRAFT, "commit": "bbbbbbb"}
    assert {k: v for k, v in second.items() if k != "kept"} == {
        k: v for k, v in first.items() if k != "kept"}
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["run.json"], "no temporary file is left"


KEEP_USAGE = [
    (["keep", "--unit", UNIT, "--key", "commit"], "--value"),
    (["keep", "--unit", UNIT, "--key", "commit", "--value", "abc1234", "--file", "x.txt"], "--file"),
    (["keep", "--unit", UNIT, "--key", "bogus", "--value", "abc1234"], "bogus"),
    (["keep", "--key", "commit", "--value", "abc1234"], "--unit"),
    (["keep", "--unit", UNIT, "--value", "abc1234"], "--key"),
]


@pytest.mark.parametrize("argv, named", KEEP_USAGE,
                         ids=["no-source", "both-sources", "key-bogus", "no-unit", "no-key"])
def test_sc2_1_keep_with_a_bad_option_is_a_usage_error_and_writes_nothing(tmp_path, argv, named):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert keep(tmp_path, root, "commit", "abc1234") == (0, "", ""), "keep is not a command yet"
    before = snapshot(root)
    code, out, err = call(tmp_path, root, *argv)
    assert code == 2 and out == ""
    assert "usage:" in err and named in err
    assert snapshot(root) == before


# --- SC2.1: task.py restart on a stopped run ----------------------------------------

def test_sc2_1_a_restart_after_a_stop_at_green_reads_green_and_what_qa_kept(tmp_path):
    root = make_repo(tmp_path)
    stopped_at_green(tmp_path, root, "Which header declares parse_args?")
    assert state_of(tmp_path, root) == {
        "state": "stopped", "task": "green", "operator": "developer", "round": 2,
        "kind": "question", "text": "Which header declares parse_args?", "kept": KEPT_AT_GREEN}


def test_sc2_1_a_restart_runs_no_earlier_task_again_it_changes_no_record(tmp_path):
    root = make_repo(tmp_path)
    stopped_at_green(tmp_path, root)
    held_records = records(root)
    assert held_records, "the earlier tasks are recorded done"
    before = snapshot(root)
    assert state_of(tmp_path, root)["task"] == "green"
    assert snapshot(root) == before, "restart without --go is read-only"
    code, out, err = restart(tmp_path, root, "--go", "--scratch", str(tmp_path / "scratch"))
    assert (code, err) == (0, "")
    assert records(root) == held_records
    assert run_json(root)["task"] == "green"


@pytest.mark.parametrize("kind", ["question", "error", "refusal"])
def test_sc2_2_a_stop_of_each_kind_restarts_with_its_text_as_the_record_holds_it(tmp_path, kind):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "prove-red", "qa-verifier")[0] == 0
    text = "Which\n  exit   code?\t "
    assert stop(tmp_path, root, text, "prove-red", "qa-verifier", kind)[0] == 1
    assert state_of(tmp_path, root) == {
        "state": "stopped", "task": "prove-red", "operator": "qa-verifier", "round": 1,
        "kind": kind, "text": text, "kept": {}}


def test_sc2_2_a_third_fail_restarts_with_its_reasons_joined_by_semicolons(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert fail(tmp_path, root, "green", R3[0], operator="dev-verifier") == (0, "", "")
    assert fail(tmp_path, root, "green", R3[1], operator="dev-verifier") == (0, "", "")
    assert fail(tmp_path, root, "green", R3[2], operator="dev-verifier")[0] == 1
    assert state_of(tmp_path, root) == {
        "state": "stopped", "task": "green", "operator": "dev-verifier", "round": 3,
        "kind": "fail", "text": "; ".join(R3), "kept": {}}


def test_sc2_2_a_third_fail_that_names_no_operator_has_a_null_operator(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer")[0] == 0
    for reason in R3[:2]:
        assert fail(tmp_path, root, "green", reason) == (0, "", "")
    assert fail(tmp_path, root, "green", R3[2])[0] == 1
    got = state_of(tmp_path, root)
    assert got["operator"] is None and got["kind"] == "fail" and got["round"] == 3


def test_sc2_1_the_stop_records_task_wins_over_the_task_in_hand_and_the_task_file(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert stop(tmp_path, root, "Which flag?", "green", "developer", "question")[0] == 1
    assert run_json(root)["task"] == "write-tests"
    got = state_of(tmp_path, root)
    assert (got["state"], got["task"], got["operator"]) == ("stopped", "green", "developer")


# --- SC2.1: an abandoned run and a unit with nothing to restart ----------------------

def test_sc2_1_a_run_json_with_a_task_file_of_its_unit_reads_abandoned_at_that_task(tmp_path):
    root = make_repo(tmp_path)
    for reason in R3[:2]:
        assert fail(tmp_path, root, "green", reason) == (0, "", "")
    assert start(tmp_path, root, "green", "developer") == (
        0, STARTED.format(task="green", operator="Developer", round=3), "")
    assert state_of(tmp_path, root) == {
        "state": "abandoned", "task": "green", "operator": "developer", "round": 3,
        "kind": None, "text": None, "kept": {}}


def test_sc2_1_a_run_json_with_no_task_file_reads_abandoned_at_the_task_in_hand(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert keep(tmp_path, root, "commit", "3f2a1bc") == (0, "", "")
    assert end(tmp_path, root, "write-tests") == (0, "", "")
    assert state_of(tmp_path, root) == {
        "state": "abandoned", "task": "write-tests", "operator": None, "round": 1,
        "kind": None, "text": None, "kept": {"commit": "3f2a1bc"}}


def test_sc2_1_a_task_file_of_another_unit_is_not_this_units_task_in_hand(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa", UNIT)[0] == 0
    assert end(tmp_path, root, "write-tests", unit=UNIT) == (0, "", "")
    assert start(tmp_path, root, "green", "developer", UNIT2)[0] == 0
    one = state_of(tmp_path, root, UNIT)
    assert (one["state"], one["task"], one["operator"]) == ("abandoned", "write-tests", None)
    two = state_of(tmp_path, root, UNIT2)
    assert (two["state"], two["task"], two["operator"]) == ("abandoned", "green", "developer")


def test_sc5_3_a_unit_with_no_run_folder_reads_none_and_the_command_writes_nothing(tmp_path):
    root = make_repo(tmp_path)
    before = snapshot(root)
    assert state_of(tmp_path, root) == NONE
    assert snapshot(root) == before
    assert not (gitdir(root) / "sdlc-run").exists()


def test_sc5_3_the_run_folder_of_another_unit_leaves_this_unit_at_none(tmp_path):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "q", unit=UNIT2)[0] == 1
    assert state_of(tmp_path, root, UNIT) == NONE
    assert state_of(tmp_path, root, UNIT2)["state"] == "stopped"


def test_sc5_3_none_reads_the_same_on_any_branch_and_go_starts_nothing(tmp_path):
    root = make_repo(tmp_path)
    git(root, "checkout", "-q", "-b", "elsewhere")
    assert state_of(tmp_path, root) == NONE
    scratch = tmp_path / "scratch"
    code, out, err = restart(tmp_path, root, "--go", "--scratch", str(scratch))
    assert (code, err) == (0, "")
    assert json.loads(out) == NONE
    assert not scratch.exists() and not (gitdir(root) / "sdlc-run").exists()


# --- SC2.3: another branch starts nothing -------------------------------------------

def _stopped(tmp_path, root):
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert stop(tmp_path, root, "Which flag?")[0] == 1


def _abandoned(tmp_path, root):
    assert start(tmp_path, root, "green", "developer")[0] == 0


@pytest.mark.parametrize("make", [_stopped, _abandoned], ids=["stopped", "abandoned"])
@pytest.mark.parametrize("go", [False, True], ids=["read", "go"])
def test_sc2_3_on_another_branch_the_line_goes_to_stderr_and_nothing_changes(tmp_path, make, go):
    root = make_repo(tmp_path)
    make(tmp_path, root)
    git(root, "checkout", "-q", "-b", "other")
    before = snapshot(root)
    scratch = tmp_path / "scratch"
    extra = ["--go", "--scratch", str(scratch)] if go else []
    assert restart(tmp_path, root, *extra) == (
        1, "", WRONG_BRANCH.format(branch=BRANCH, current="other"))
    assert snapshot(root) == before
    assert not scratch.exists()


def test_sc2_3_back_on_the_runs_branch_the_same_restart_reads_the_stop(tmp_path):
    root = make_repo(tmp_path)
    _stopped(tmp_path, root)
    git(root, "checkout", "-q", "-b", "other")
    assert restart(tmp_path, root)[0] == 1
    git(root, "checkout", "-q", BRANCH)
    assert state_of(tmp_path, root)["state"] == "stopped"


# --- a record that does not parse is reported, never guessed -------------------------

def _stopped_pair(tmp_path, root):
    _stopped(tmp_path, root)
    assert (run_dir(root) / "run.json").is_file() and (run_dir(root) / "stop.json").is_file()


@pytest.mark.parametrize("name", ["run.json", "stop.json"])
@pytest.mark.parametrize("text", ["", "not json", "[]"], ids=["empty", "not-json", "list"])
@pytest.mark.parametrize("go", [False, True], ids=["read", "go"])
def test_sc2_3_a_record_that_does_not_parse_is_reported_on_stderr_and_starts_nothing(
        tmp_path, name, text, go):
    root = make_repo(tmp_path)
    _stopped_pair(tmp_path, root)
    (run_dir(root) / name).write_text(text, encoding="utf-8")
    before = snapshot(root)
    scratch = tmp_path / "scratch"
    extra = ["--go", "--scratch", str(scratch)] if go else []
    assert restart(tmp_path, root, *extra) == (
        1, "", NOT_PARSED.format(name=name, contract=CONTRACT, unit=U))
    assert snapshot(root) == before
    assert not scratch.exists()


@pytest.mark.parametrize("go", [False, True], ids=["read", "go"])
def test_sc2_3_a_stop_json_with_no_run_json_is_reported_on_stderr_and_starts_nothing(tmp_path, go):
    root = make_repo(tmp_path)
    _stopped_pair(tmp_path, root)
    (run_dir(root) / "run.json").unlink()
    before = snapshot(root)
    scratch = tmp_path / "scratch"
    extra = ["--go", "--scratch", str(scratch)] if go else []
    assert restart(tmp_path, root, *extra) == (
        1, "", NO_RUN_JSON.format(contract=CONTRACT, unit=U))
    assert snapshot(root) == before
    assert not scratch.exists()


# --- task.py restart --go -----------------------------------------------------------

def test_sc2_1_go_removes_the_stop_record_and_the_leftover_task_file_and_writes_the_draft(
        tmp_path):
    root = make_repo(tmp_path)
    stopped_at_green(tmp_path, root)
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert task_file(root).is_file(), "a task file is left standing"
    asked = restart(tmp_path, root)
    run_bytes = (run_dir(root) / "run.json").read_bytes()
    rounds_bytes = (run_dir(root) / "rounds.json").read_bytes()
    scratch = tmp_path / "fresh-session" / "scratch"
    code, out, err = restart(tmp_path, root, "--go", "--scratch", str(scratch))
    assert (code, err) == (0, "")
    assert out == asked[1], "--go prints the line the read-only restart printed"
    assert not (run_dir(root) / "stop.json").exists()
    assert not task_file(root).exists()
    assert (scratch / "draft" / "tests" / "test_cli.py").read_bytes() == DRAFT_BYTES
    # What the next task start counts from stays.
    assert (run_dir(root) / "rounds.json").read_bytes() == rounds_bytes
    assert (run_dir(root) / "run.json").read_bytes() == run_bytes
    assert run_json(root)["kept"] == KEPT_AT_GREEN


def test_sc2_1_after_go_green_starts_at_the_round_after_the_failed_ones(tmp_path):
    root = make_repo(tmp_path)
    stopped_at_green(tmp_path, root)
    scratch = tmp_path / "scratch"
    assert restart(tmp_path, root, "--go", "--scratch", str(scratch))[0] == 0
    assert start(tmp_path, root, "green", "developer") == (
        0, STARTED.format(task="green", operator="Developer", round=2), "")
    assert run_json(root)["task"] == "green"
    assert run_json(root)["kept"] == KEPT_AT_GREEN


def test_sc2_1_go_with_no_draft_kept_writes_nothing_into_the_scratch_folder(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert stop(tmp_path, root, "Which flag?", "write-tests", "qa", "question")[0] == 1
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    code, out, err = restart(tmp_path, root, "--go", "--scratch", str(scratch))
    assert (code, err) == (0, "")
    assert json.loads(out)["task"] == "write-tests"
    assert not (run_dir(root) / "stop.json").exists()
    assert [p for p in scratch.rglob("*") if p.is_file()] == []


def test_sc2_1_go_without_a_scratch_folder_is_a_usage_error_and_changes_nothing(tmp_path):
    root = make_repo(tmp_path)
    stopped_at_green(tmp_path, root)
    assert state_of(tmp_path, root)["state"] == "stopped", "restart is not a command yet"
    before = snapshot(root)
    code, out, err = restart(tmp_path, root, "--go")
    assert code == 2 and out == ""
    assert "usage:" in err and "--scratch" in err
    assert snapshot(root) == before
    assert (run_dir(root) / "stop.json").is_file()


# --- every --unit is two plain halves, a colon in a half is a drive ------------------

BAD_UNITS = ["c:/u", "a/c:"]
COMMANDS = {
    "start": lambda u: ["start", "--unit", u, "--task", "green", "--operator", "developer"],
    "end": lambda u: ["end", "--unit", u, "--task", "green"],
    "fail": lambda u: ["fail", "--unit", u, "--task", "green", "--reason", "r"],
    "stop": lambda u: ["stop", "--unit", u, "--task", "green", "--operator", "developer",
                       "--kind", "question", "--question", "q"],
    "end-run": lambda u: ["end", "--run", "--unit", u],
    "keep": lambda u: ["keep", "--unit", u, "--key", "commit", "--value", "abc1234"],
    "restart": lambda u: ["restart", "--unit", u],
}


@pytest.mark.parametrize("verb", list(COMMANDS))
@pytest.mark.parametrize("unit", BAD_UNITS, ids=[repr(u) for u in BAD_UNITS])
def test_sc2_3_a_unit_half_holding_a_colon_is_a_usage_error_and_writes_nothing(
        tmp_path, verb, unit):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert end(tmp_path, root, "write-tests") == (0, "", "")
    # The same call with a plain unit is no usage error.
    code, out, err = call(tmp_path, root, *COMMANDS[verb](UNIT))
    assert code != 2 and "usage:" not in err, (code, err)
    before = snapshot(root)
    listing = sorted(os.listdir(gitdir(root)))
    code, out, err = call(tmp_path, root, *COMMANDS[verb](unit))
    assert code == 2 and out == "", (code, out, err)
    assert "usage:" in err
    assert snapshot(root) == before
    assert sorted(os.listdir(gitdir(root))) == listing


# --- SC2.2: each member takes the answer --------------------------------------------

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
TEST_FILE = "tests/run_x.bat"
MEMBER_DRAFT = {"test_file": TEST_FILE, "interface": "NOTE-TEXT",
                "tests": [{"name": "t1", "proves": "SC1.1", "intent": "pins x"}],
                "red_proof": {"command": "prove", "summary": "red",
                              "every_failure_on_the_missing_behavior": True},
                "details_fixed": ["d1"], "questions": []}
RECEIPTS_OK = {"ok": True, "commands": [{"command": ["run-all.bat"], "exit_code": 0}]}


def _verifier(task: str) -> dict:
    extra = {
        "approve-tests": {"contractPath": "specs/c1/contract.yaml",
                          "requestPath": "docs/features/c1.md", "draft": MEMBER_DRAFT},
        "prove-red": {},
        "two-key": {"commit": "abc1234", "contractPath": "specs/c1/contract.yaml",
                    "requestPath": "docs/features/c1.md"},
    }[task]
    return {**BASE, "scratch": "/s", "pluginRoot": "/p", "task": task, "testFile": TEST_FILE, **extra}


ARGS = {
    "qa": {**BASE, "scratch": "/s", "pluginRoot": "/p", "test": TEST, "wall": WALL,
           "sources": ["specs/c1/contract.yaml"]},
    "qa-verifier:approve-tests": _verifier("approve-tests"),
    "qa-verifier:prove-red": _verifier("prove-red"),
    "qa-verifier:two-key": _verifier("two-key"),
    "developer": {**BASE, "branch": "b1", "testFile": TEST_FILE, "scratchRoot": "/s",
                  "files": ["src/a.cpp"], "sources": ["s1"], "interface": "NOTE-TEXT",
                  "test": TEST, "wall": WALL},
    "dev-verifier": {**BASE, "branch": "b1", "commit": "abc1234",
                     "contractPath": "specs/c1/contract.yaml",
                     "requestPath": "docs/features/c1.md", "receiptsResult": RECEIPTS_OK},
}
ANSWER = {"stopped": "Which header declares parse_args?", "reply": "Use the header cli.h"}


def run_member(tmp_path: Path, case: str, args: dict) -> dict:
    file = WORKFLOWS / f"{case.split(':')[0]}.js"
    assert file.is_file(), f"{file.relative_to(ROOT).as_posix()} is not written"
    (tmp_path / "harness.js").write_text(HARNESS, encoding="utf-8")
    (tmp_path / "cfg.json").write_text(json.dumps({"args": args, "responses": []}),
                                       encoding="utf-8")
    done = subprocess.run([NODE, str(tmp_path / "harness.js"), str(file), str(tmp_path / "cfg.json")],
                          capture_output=True, encoding="utf-8", errors="replace", timeout=60,
                          creationflags=NO_WINDOW)
    assert done.returncode == 0, f"node failed: {done.stderr.strip()}"
    out = json.loads(done.stdout.strip().splitlines()[-1])
    assert "thrown" not in out, out["thrown"]
    return out


@pytest.mark.parametrize("member", ["qa", "qa-verifier", "developer", "dev-verifier"])
def test_sc2_2_each_member_script_reads_an_answer_argument(member):
    text = (WORKFLOWS / f"{member}.js").read_text(encoding="utf-8")
    assert re.search(r"\ba\.answer\b", text), f"workflows/{member}.js reads no a.answer"


@needs_node
@pytest.mark.parametrize("case", list(ARGS))
def test_sc2_2_a_member_given_an_answer_puts_the_stop_and_the_reply_into_its_prompt(
        tmp_path, case):
    out = run_member(tmp_path, case, {**ARGS[case], "answer": ANSWER})
    assert len(out["calls"]) == 1
    prompt = out["calls"][0]["prompt"]
    assert ANSWER["stopped"] in prompt, "the stop's question or reasons are in the prompt"
    assert ANSWER["reply"] in prompt, "the user's reply is in the prompt"


@needs_node
@pytest.mark.parametrize("case", list(ARGS))
def test_sc2_2_a_null_answer_changes_no_prompt_and_an_answer_does(tmp_path, case):
    plain = run_member(tmp_path, case, ARGS[case])["calls"][0]["prompt"]
    null = run_member(tmp_path, case, {**ARGS[case], "answer": None})["calls"][0]["prompt"]
    assert null == plain
    answered = run_member(tmp_path, case, {**ARGS[case], "answer": ANSWER})["calls"][0]["prompt"]
    assert answered != plain


# --- the flows ----------------------------------------------------------------------

TASKPY = "python {skill-dir}/../../workflows/tools/task.py"
TASKS = [("E3", "write-tests"), ("E4", "approve-tests"), ("E5", "prove-red"), ("E6", "green"),
         ("E7", "approve-commit"), ("E8", "commit"), ("E9", "two-key")]
QUESTION_LINE = re.compile(
    r"Execution stopped: \{contract\} unit \{unit\}, task \{task\}, round \{\w+\} of 3: "
    r"\{\w+\}\. Your answer\?")


def read(path: Path) -> str:
    assert path.is_file(), f"{path.relative_to(ROOT).as_posix()} is not written"
    return path.read_text(encoding="utf-8")


def spans(text: str) -> list[tuple[int, str]]:
    return [(m.start(), m[1]) for m in re.finditer(r"`([^`\n]+)`", text)
            if m[1].startswith(("python ", "git ", "rm ", "gh "))]


def task_spans(text: str, verb: str) -> list[tuple[int, str]]:
    return [(at, c) for at, c in spans(text) if c.startswith(f"{TASKPY} {verb} ")
            or c == f"{TASKPY} {verb}"]


def reading(text: str, at: int, command: str) -> str:
    later = [o for o, _ in spans(text) if o > at]
    tail = text[at + len(command) + 2:(later[0] if later else len(text))]
    return tail.split("\n\n")[0]


def steps_of(text: str) -> dict[str, str]:
    block = re.search(r"<instructions>\n(.*?)</instructions>", text, re.DOTALL)
    assert block, "the flow's steps stand inside one instructions block"
    found = {}
    for part in re.split(r"^(?=E\d+\. )", block[1], flags=re.MULTILINE):
        label = re.match(r"(E\d+)\. ", part)
        if label:
            found[label[1]] = part
    return found


def member_segments(step: str) -> list[tuple[str, str]]:
    found = list(re.finditer(r"\{plugin\}:([a-z][a-z-]*)", step))
    return [(m[1], step[m.start():(found[i + 1].start() if i + 1 < len(found) else len(step))])
            for i, m in enumerate(found)]


def args_of(segment: str) -> str:
    found = re.search(r"args `([^`]*)`", segment)
    assert found, f"no args span after {segment[:40]!r}"
    return found[1]


def test_sc2_1_execute_md_and_restart_md_stay_under_the_character_ceiling():
    assert len(read(EXECUTE)) < CEILING, len(read(EXECUTE))
    assert len(read(RESTART)) < CEILING, len(read(RESTART))


def test_sc2_3_e2_runs_task_py_restart_once_before_any_task_starts():
    text = read(EXECUTE)
    found = task_spans(text, "restart")
    assert [c for _, c in found] == [f"{TASKPY} restart --unit {{contract}}/{{unit}}"], found
    at, command = found[0]
    assert "one Bash call" in text[at + len(command):at + len(command) + 40]
    assert command in steps_of(text)["E2"]
    assert at < min(o for o, _ in task_spans(text, "start"))


def test_sc2_3_e2_shows_the_line_and_stops_when_restart_exits_1():
    text = read(EXECUTE)
    found = task_spans(text, "restart")
    assert found, "E2 runs no task.py restart"
    at, command = found[0]
    after = reading(text, at, command)
    assert "exits 1" in after and "SHOW" in after and "STOP" in after, after


def test_sc2_3_e2_loads_restart_md_on_a_stopped_or_abandoned_run_and_starts_as_today_on_none():
    text = read(EXECUTE)
    e2 = steps_of(text)["E2"]
    assert "task.py restart" in e2, "E2 runs no task.py restart"
    after = e2[e2.index("task.py restart"):]
    assert "{skill-dir}/flows/restart.md" in after
    assert re.search(r"`stopped`.{0,200}`abandoned`|`abandoned`.{0,200}`stopped`", after, re.DOTALL)
    assert re.search(r"`none`[^\n]{0,200}(E3|write-tests)", after), "none starts write-tests as today"


def test_sc2_2_e2_holds_the_users_answer_from_dash_dash_answer_else_null():
    e2 = steps_of(read(EXECUTE))["E2"]
    assert "--answer" in e2 and "{answer}" in e2 and "null" in e2


def test_sc2_2_every_member_start_of_the_flow_passes_the_answer():
    steps = steps_of(read(EXECUTE))
    count = 0
    for label, _task in TASKS:
        for _name, segment in member_segments(steps[label]):
            assert '"answer": {answer}' in args_of(segment), (label, segment[:60])
            count += 1
    assert count == 6, count


def _ordered(text: str, step: str, *needles: str) -> None:
    body = steps_of(text)[step]
    at = -1
    for needle in needles:
        found = body.find(needle, at + 1)
        assert found > at, f"{step}: {needle!r} does not follow the one before it"
        at = found


KEEP = f"{TASKPY} keep --unit {{contract}}/{{unit}} --key "


def test_sc2_1_e3_keeps_the_draft_and_its_file_after_qa_before_the_task_ends():
    text = read(EXECUTE)
    keep_draft = f"{KEEP}draft --value '{{draft}}'"
    keep_file = f"{KEEP}draft-file --file {{scratch}}/draft/{{testFile}}"
    found = [c for _, c in task_spans(text, "keep")]
    assert keep_draft in found and keep_file in found, found
    end = f"{TASKPY} end --unit {{contract}}/{{unit}} --task write-tests"
    _ordered(text, "E3", "{plugin}:qa", "as {draft}", keep_draft, end)
    _ordered(text, "E3", "{plugin}:qa", keep_file, end)
    for command in (keep_draft, keep_file):
        at = text.index(command)
        assert "one Bash call" in text[at + len(command):at + len(command) + 40], command


def test_sc2_1_e7_keeps_the_receipts_after_receipts_py_before_the_task_ends():
    text = read(EXECUTE)
    command = f"{KEEP}receipts --value '{{receipts}}'"
    assert command in [c for _, c in task_spans(text, "keep")]
    end = f"{TASKPY} end --unit {{contract}}/{{unit}} --task approve-commit"
    _ordered(text, "E7", "receipts.py", command, end)
    at = text.index(command)
    assert "one Bash call" in text[at + len(command):at + len(command) + 40]


def test_sc2_1_e8_keeps_the_commit_after_git_commit_before_the_task_ends():
    text = read(EXECUTE)
    command = f"{KEEP}commit --value {{sha}}"
    assert command in [c for _, c in task_spans(text, "keep")]
    end = f"{TASKPY} end --unit {{contract}}/{{unit}} --task commit"
    _ordered(text, "E8", "git rev-parse --short HEAD", command, end)
    at = text.index(command)
    assert "one Bash call" in text[at + len(command):at + len(command) + 40]


def test_sc2_1_no_other_task_keeps_anything():
    found = task_spans(read(EXECUTE), "keep")
    assert len(found) == 4, [c for _, c in found]


def test_sc2_1_restart_md_is_a_promptlang_flow_file_beside_execute_md():
    text = read(RESTART)
    lines = text.split("\n")
    assert lines[0] == "---" and lines[1] == "name: sdlc-flow-restart"
    assert lines[2].startswith("description: ") and lines[3] == "---"
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    assert text.index("</purpose>") < text.index("<instructions>")


def test_sc2_2_restart_md_shows_the_stop_then_asks_the_answer_then_runs_go():
    text = read(RESTART)
    shown = QUESTION_LINE.search(text)
    assert shown, "the verbatim 'Execution stopped: ... Your answer?' line is not in restart.md"
    go = f"{TASKPY} restart --unit {{contract}}/{{unit}} --go --scratch {{scratch}}"
    found = [c for _, c in task_spans(text, "restart")]
    assert go in found, found
    assert shown.end() < text.index(go), "nothing starts before the user's answer"
    at = text.index(go)
    assert "one Bash call" in text[at + len(go):at + len(go) + 40]


def test_sc2_2_restart_md_takes_dash_dash_answer_first_and_a_headless_session_ends_its_turn():
    text = read(RESTART)
    assert "--answer" in text and "headless" in text
    assert re.search(r"headless[^\n]*(end|ends)[^\n]*turn|turn[^\n]*headless", text), \
        "a headless session ends its turn at the question"


def test_sc2_2_restart_md_gives_the_member_the_stop_and_the_reply_as_its_answer():
    text = read(RESTART)
    assert '"stopped"' in text and '"reply"' in text and "{answer}" in text
    assert re.search(r'"stopped": "\{\w+\}", "reply": "\{\w+\}"', text), \
        "the answer is held as {\"stopped\": ..., \"reply\": ...}"


def test_sc2_2_restart_md_shows_the_answer_and_runs_the_command_of_a_task_with_no_member():
    text = read(RESTART)
    for operator in ("receipts", "orchestrator"):
        assert operator in text, operator
    windows = [text[max(0, m.start() - 300):m.end() + 300]
               for m in re.finditer(r"orchestrator", text)]
    assert any("receipts" in w and "answer" in w and "SHOW" in w for w in windows), \
        "a stopped receipts or orchestrator task shows the answer and runs its command"


def test_sc2_1_restart_md_names_each_task_with_the_step_of_execute_md_it_starts_at():
    text = read(RESTART)
    for label, task in TASKS:
        assert any(label in line and task in line for line in text.splitlines()), (label, task)
    assert re.search(r"earlier (task|step)", text), "no earlier task runs again"


def test_sc2_1_restart_md_holds_what_qa_and_the_later_tasks_kept_under_the_flows_own_names():
    text = read(RESTART)
    for name in ("{draft}", "{note}", "{testFile}", "{receipts}", "{sha}", "kept"):
        assert name in text, name
    assert "draft-file" in text or "{scratch}/draft" in text


def test_sc2_1_a_stop_of_kind_fail_restarts_nothing_until_the_enough_ruling_exists():
    text = read(RESTART)
    assert any("fail" in line and "STOP" in line for line in text.splitlines()), \
        "a stop of kind fail stops the flow with no task started"


def test_sc2_1_skill_md_names_restart_md_among_its_flow_files():
    skill = read(SKILL)
    context = re.search(r"<context>\n(.*?)</context>", skill, re.DOTALL)[1]
    assert "restart.md" in context
    assert "execute.md" in context
    assert len(skill) < CEILING
