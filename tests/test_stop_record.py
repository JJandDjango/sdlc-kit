"""Stop-record suite (contract: run-restart, unit rs1-stop-record, checks SC1.1,
SC1.2 and SC1.3).

A question, an error, a refused task start or a third failed round writes
`stop.json` in the unit's run folder `{git folder}/sdlc-run/{contract}/{unit}/`;
the rounds file moves there as `rounds.json` and is kept; `task.py end --run
--unit` removes the whole folder. The flow `skills/sdlc/flows/execute.md` passes
the unit and the kind to every stop, the operator to every fail, and stops with
no PR after a refused start.

`task.py` runs as a subprocess on a fixture repository under tmp_path (the way
tests/test_rounds.py does); nothing is imported from it. The flow is read as text.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

import taskcontract

ROOT = Path(taskcontract.__file__).resolve().parents[1]
TASK_PY = ROOT / "workflows" / "tools" / "task.py"
FLOW = ROOT / "skills" / "sdlc" / "flows" / "execute.md"

CONTRACT, U, U2 = "exec-fix", "u1-work", "u2-more"
UNIT, UNIT2 = f"{CONTRACT}/{U}", f"{CONTRACT}/{U2}"
INTENT = ("A fixture contract for the stop-record suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")
OPERATORS = [("qa", "QA"), ("qa-verifier", "QA verifier"), ("developer", "Developer"),
             ("dev-verifier", "Dev verifier"), ("receipts", "receipts"),
             ("orchestrator", "Orchestrator")]

STOPPED = "Task {task} failed 3 rounds. The run stops here; the failures follow.\n"
QUESTION = "Task {task} stopped on a question from {operator}: {question}\n"
STARTED = "Task {task}: {operator}, round {round}\n"
NO_GIT = "No git repository at {root}.\n"
R3 = ["2 sketches failed: SC1.1 (a.py:4), SC1.2 (a.py:9)", "1 sketch failed: SC1.2 (a.py:9)",
      "1 sketch failed: SC1.2 (a.py:11)"]
AT = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")


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
    argv = [sys.executable, str(TASK_PY), *args, "--root", str(root)]
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1"}
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100)
    return done.returncode, done.stdout, done.stderr


def start(tmp_path, root, task="green", operator="developer", unit=UNIT):
    return call(tmp_path, root, "start", "--unit", unit, "--task", task, "--operator", operator)


def fail(tmp_path, root, task="green", reason=None, unit=UNIT, operator=None):
    extra = ["--reason", reason] if reason is not None else []
    extra += ["--operator", operator] if operator else []
    return call(tmp_path, root, "fail", "--unit", unit, "--task", task, *extra)


def end(tmp_path, root, task="green", unit=UNIT):
    return call(tmp_path, root, "end", "--unit", unit, "--task", task)


def stop(tmp_path, root, question="Which exit code?", task="green", operator="developer",
         kind="question", unit=UNIT):
    return call(tmp_path, root, "stop", "--unit", unit, "--task", task, "--operator", operator,
                "--kind", kind, "--question", question)


def gitdir(root: Path) -> Path:
    return root / ".git"


def run_dir(root: Path, unit: str = UNIT) -> Path:
    return gitdir(root) / "sdlc-run" / unit


def task_file(root: Path) -> Path:
    return gitdir(root) / "sdlc-task.json"


def old_rounds(root: Path) -> Path:
    return gitdir(root) / "sdlc-rounds.json"


def load(path: Path):
    assert path.is_file(), f"{path} is not written"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        raise AssertionError(f"{path} does not hold JSON") from None


def stop_json(root: Path, unit: str = UNIT) -> dict:
    return load(run_dir(root, unit) / "stop.json")


def rounds_json(root: Path, unit: str = UNIT) -> dict:
    return load(run_dir(root, unit) / "rounds.json")


def records(root: Path) -> list[dict]:
    path = root / ".sdlc" / "progress" / f"{CONTRACT}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["records"] if path.is_file() else []


def snapshot(root: Path) -> dict:
    """Every path under the repository, git folder included, with the bytes."""
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*")
            if ".git" not in p.relative_to(root).parts
            or (len(p.relative_to(root).parts) > 1
                and p.relative_to(root).parts[1].startswith("sdlc-"))}


def failed_rounds(tmp_path, root, task="green", reasons=(None, None), unit=UNIT):
    for reason in reasons:
        assert fail(tmp_path, root, task, reason, unit) == (0, "", "")


def without_at(record: dict) -> dict:
    assert AT.match(record["at"]), record["at"]
    return {k: v for k, v in record.items() if k != "at"}


# --- SC1.1: a question or an error stops the run with a record ---------------------

@pytest.mark.parametrize("kind", ["question", "error"])
def test_sc1_1_a_stop_writes_the_record_prints_the_line_and_exits_1(tmp_path, kind):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert fail(tmp_path, root, "green", R3[0]) == (0, "", "")
    assert start(tmp_path, root)[0] == 0
    assert task_file(root).is_file()
    question = "Which header declares parse_args?"
    assert stop(tmp_path, root, question, "green", "developer", kind) == (
        1, QUESTION.format(task="green", operator="Developer", question=question), "")
    assert not task_file(root).exists(), f"a stop of kind {kind} leaves no task file"
    assert without_at(stop_json(root)) == {
        "unit": UNIT, "task": "green", "operator": "developer", "kind": kind, "round": 2,
        "failed": {"write-tests": 0, "green": 1}, "text": question}


@pytest.mark.parametrize("operator, printed", OPERATORS, ids=[o for o, _ in OPERATORS])
def test_sc1_1_every_operator_stops_with_its_name_printed_and_its_id_recorded(
        tmp_path, operator, printed):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "Which flag?", "commit", operator, "question") == (
        1, QUESTION.format(task="commit", operator=printed, question="Which flag?"), "")
    record = stop_json(root)
    assert (record["task"], record["operator"], record["kind"]) == ("commit", operator, "question")


def test_sc1_1_a_stop_removes_the_task_file_and_keeps_the_rounds_file(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert fail(tmp_path, root, "green", R3[0]) == (0, "", "")
    assert start(tmp_path, root)[0] == 0
    assert task_file(root).is_file()
    assert (run_dir(root) / "rounds.json").is_file(), "fail writes rounds.json in the run folder"
    kept = (run_dir(root) / "rounds.json").read_bytes()
    assert stop(tmp_path, root, "Which flag?")[0] == 1
    assert not task_file(root).exists()
    assert (run_dir(root) / "rounds.json").read_bytes() == kept
    assert stop_json(root)["task"] == "green"


def test_sc1_1_a_stop_writes_only_the_two_files_in_the_run_folder_and_no_progress(tmp_path):
    root = make_repo(tmp_path)
    assert fail(tmp_path, root, "write-tests", R3[0]) == (0, "", "")
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    held = records(root)
    assert stop(tmp_path, root, "Which flag?", "write-tests", "qa")[0] == 1
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["rounds.json", "stop.json"]
    assert records(root) == held
    assert not old_rounds(root).exists()


def test_sc1_1_the_run_folder_is_made_on_the_first_write(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert not (gitdir(root) / "sdlc-run").exists()
    assert stop(tmp_path, root, "Which flag?")[0] == 1
    assert (run_dir(root) / "stop.json").is_file()


def test_sc1_1_the_time_is_utc_to_the_second_with_a_trailing_z(tmp_path):
    root = make_repo(tmp_path)
    before = datetime.now(timezone.utc).replace(microsecond=0)
    assert stop(tmp_path, root)[0] == 1
    after = datetime.now(timezone.utc)
    at = stop_json(root)["at"]
    assert AT.match(at), at
    moment = datetime.strptime(at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    assert before - timedelta(seconds=2) <= moment <= after + timedelta(seconds=2)


def test_sc1_1_the_record_holds_the_question_as_given_and_the_line_collapses_it(tmp_path):
    root = make_repo(tmp_path)
    question = "Which\n  exit   code?\t "
    assert stop(tmp_path, root, question) == (
        1, QUESTION.format(task="green", operator="Developer", question="Which exit code?"), "")
    assert stop_json(root)["text"] == question


def test_sc1_1_a_stop_round_is_one_past_the_larger_of_the_tasks_and_its_channels_failures(
        tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [R3[0]])
    failed_rounds(tmp_path, root, "two-key", [None, None])
    failed_rounds(tmp_path, root, "write-tests", [R3[1]])
    # Its own two failed rounds outweigh the channel's one.
    assert stop(tmp_path, root, "q one", "two-key", "dev-verifier")[0] == 1
    assert without_at(stop_json(root)) == {
        "unit": UNIT, "task": "two-key", "operator": "dev-verifier", "kind": "question",
        "round": 3, "failed": {"write-tests": 1, "green": 1}, "text": "q one"}
    # The channel's one failed round counts for a peer that has none of its own.
    assert stop(tmp_path, root, "q two", "commit", "orchestrator", "error")[0] == 1
    got = stop_json(root)
    assert (got["task"], got["round"], got["kind"]) == ("commit", 2, "error")
    # A peer of the write-tests channel reads that channel.
    assert stop(tmp_path, root, "q three", "prove-red", "qa-verifier")[0] == 1
    assert stop_json(root)["round"] == 2


def test_sc1_1_a_stop_with_no_failed_round_is_round_1_and_counts_zero(tmp_path):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "q", "write-tests", "qa")[0] == 1
    got = stop_json(root)
    assert got["round"] == 1 and got["failed"] == {"write-tests": 0, "green": 0}


def test_sc1_1_the_stop_round_is_the_round_start_printed_for_the_task(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [R3[0], R3[1]])
    assert start(tmp_path, root) == (
        0, STARTED.format(task="green", operator="Developer", round=3), "")
    assert stop(tmp_path, root, "q")[0] == 1
    assert stop_json(root)["round"] == 3


def test_sc1_1_a_second_stop_of_the_unit_replaces_the_first(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert fail(tmp_path, root, "green", R3[2], operator="dev-verifier")[0] == 1
    assert stop_json(root)["kind"] == "fail"
    assert stop(tmp_path, root, "second", "green", "developer", "error")[0] == 1
    got = stop_json(root)
    assert got["kind"] == "error" and got["text"] == "second" and "reasons" not in got
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["rounds.json", "stop.json"]


def test_sc1_1_two_units_keep_a_stop_record_each(tmp_path):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "one", unit=UNIT)[0] == 1
    assert stop(tmp_path, root, "two", unit=UNIT2)[0] == 1
    assert (stop_json(root, UNIT)["unit"], stop_json(root, UNIT)["text"]) == (UNIT, "one")
    assert (stop_json(root, UNIT2)["unit"], stop_json(root, UNIT2)["text"]) == (UNIT2, "two")


def test_sc1_1_a_unit_with_dots_inside_its_halves_gets_a_folder_of_that_name(tmp_path):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "q", unit="a.b/c..d")[0] == 1
    assert stop_json(root, "a.b/c..d")["unit"] == "a.b/c..d"


def test_sc1_1_in_a_linked_worktree_the_run_folder_is_in_the_worktrees_git_folder(tmp_path):
    root = make_repo(tmp_path)
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@example.com", "-c", "user.name=t",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=no-hooks",
        "commit", "-q", "-m", "seed")
    wt = tmp_path / "wt"
    git(root, "worktree", "add", "-q", "--detach", str(wt))
    wt_git = Path(git(wt, "rev-parse", "--absolute-git-dir").strip())
    assert wt_git != gitdir(root)
    assert stop(tmp_path, wt, "q")[0] == 1
    assert (wt_git / "sdlc-run" / UNIT / "stop.json").is_file()
    assert not (gitdir(root) / "sdlc-run").exists()


def test_sc1_1_without_a_git_repository_a_stop_prints_its_line_writes_no_record_and_exits_1(
        tmp_path):
    root = make_repo(tmp_path, git_repo=False)
    before = snapshot(root)
    assert stop(tmp_path, root, "Which flag?") == (
        1, QUESTION.format(task="green", operator="Developer", question="Which flag?"), "")
    assert snapshot(root) == before
    assert not any(p.name in ("stop.json", "sdlc-run") for p in tmp_path.rglob("*"))


# --- SC1.1: a refused task start stops with a record --------------------------------

def test_sc1_1_a_refusal_stop_prints_nothing_removes_the_task_file_and_writes_the_record(
        tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer")[0] == 0
    code, out, err = start(tmp_path, root, "two-key", "dev-verifier")
    refused = (out + err).strip()
    assert code == 1 and refused, "task.py start refuses while a task file stands"
    assert stop(tmp_path, root, refused, "two-key", "dev-verifier", "refusal") == (1, "", "")
    assert not task_file(root).exists()
    assert without_at(stop_json(root)) == {
        "unit": UNIT, "task": "two-key", "operator": "dev-verifier", "kind": "refusal",
        "round": 1, "failed": {"write-tests": 0, "green": 0}, "text": refused}


def test_sc1_1_a_refusal_after_failed_rounds_counts_them(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "write-tests", [R3[0]])
    assert stop(tmp_path, root, "the refusal", "prove-red", "qa-verifier", "refusal") == (1, "", "")
    got = stop_json(root)
    assert (got["round"], got["failed"], got["kind"]) == (
        2, {"write-tests": 1, "green": 0}, "refusal")


# --- SC1.2: a third failed round stops with a record -------------------------------

def test_sc1_2_the_first_and_second_failed_rounds_are_silent_and_write_rounds_json(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root)[0] == 0
    assert fail(tmp_path, root, "green", R3[0]) == (0, "", "")
    assert not task_file(root).exists()
    assert rounds_json(root) == {"unit": UNIT, "rounds": {"green": [R3[0]]}}
    assert fail(tmp_path, root, "green", None) == (0, "", "")
    assert rounds_json(root) == {"unit": UNIT, "rounds": {"green": [R3[0], None]}}
    assert not (run_dir(root) / "stop.json").exists()
    assert not old_rounds(root).exists()


def test_sc1_2_a_third_failed_round_prints_the_lines_removes_the_task_file_and_keeps_rounds(
        tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert start(tmp_path, root)[0] == 0
    assert fail(tmp_path, root, "green", R3[2]) == (
        1, STOPPED.format(task="green") + "".join(
            f"  Round {n}: {r}\n" for n, r in enumerate(R3, 1)), "")
    assert not task_file(root).exists()
    assert rounds_json(root) == {"unit": UNIT, "rounds": {"green": R3}}
    assert not old_rounds(root).exists()


def test_sc1_2_a_third_failed_round_writes_the_fail_record_with_each_reason(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert fail(tmp_path, root, "green", R3[2], operator="dev-verifier")[0] == 1
    assert without_at(stop_json(root)) == {
        "unit": UNIT, "task": "green", "operator": "dev-verifier", "kind": "fail",
        "round": 3, "failed": {"write-tests": 0, "green": 3}, "reasons": R3}
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["rounds.json", "stop.json"]


def test_sc1_2_the_operator_is_null_when_fail_names_none(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert fail(tmp_path, root, "green", R3[2])[0] == 1
    got = stop_json(root)
    assert "operator" in got and got["operator"] is None and got["kind"] == "fail"


def test_sc1_2_a_missing_reason_is_an_empty_string_in_the_record(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [None, R3[1]])
    assert fail(tmp_path, root, "green", None, operator="receipts")[0] == 1
    got = stop_json(root)
    assert got["reasons"] == ["", R3[1], ""] and got["operator"] == "receipts"
    assert "text" not in got


def test_sc1_2_the_record_counts_both_channels_and_the_third_one_reads_three(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [R3[0]])
    failed_rounds(tmp_path, root, "write-tests", R3[:2])
    assert fail(tmp_path, root, "write-tests", R3[2], operator="qa-verifier")[0] == 1
    got = stop_json(root)
    assert got["task"] == "write-tests" and got["round"] == 3
    assert got["failed"] == {"write-tests": 3, "green": 1} and got["reasons"] == R3


def test_sc1_2_the_operator_of_fail_is_one_of_the_operators(tmp_path):
    root = make_repo(tmp_path)
    assert fail(tmp_path, root, "green", R3[0], operator="dev-verifier") == (0, "", "")
    before = snapshot(root)
    code, out, err = fail(tmp_path, root, "green", R3[1], operator="bogus")
    assert code == 2 and out == "" and "usage:" in err and "bogus" in err
    assert snapshot(root) == before


def test_sc1_2_start_counts_its_round_from_the_run_folders_rounds_file(tmp_path):
    root = make_repo(tmp_path)
    (run_dir(root)).mkdir(parents=True)
    (run_dir(root) / "rounds.json").write_text(
        json.dumps({"unit": UNIT, "rounds": {"green": ["a", "b"]}}), encoding="utf-8")
    assert start(tmp_path, root, "green", "developer") == (
        0, STARTED.format(task="green", operator="Developer", round=3), "")
    task_file(root).unlink()
    assert start(tmp_path, root, "two-key", "dev-verifier") == (
        0, STARTED.format(task="two-key", operator="Dev verifier", round=3), "")
    task_file(root).unlink()
    assert start(tmp_path, root, "write-tests", "qa") == (
        0, STARTED.format(task="write-tests", operator="QA", round=1), "")


def test_sc1_2_the_kept_rounds_count_after_a_third_failed_round(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert fail(tmp_path, root, "green", R3[2])[0] == 1
    assert start(tmp_path, root) == (
        0, STARTED.format(task="green", operator="Developer", round=4), "")


def test_sc1_2_a_task_that_ends_keeps_the_rounds_in_the_run_folder(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", [R3[0]])
    assert start(tmp_path, root)[0] == 0
    assert end(tmp_path, root, "green") == (0, "", "")
    assert rounds_json(root) == {"unit": UNIT, "rounds": {"green": [R3[0]]}}


def test_sc1_2_each_unit_has_its_own_rounds_and_a_start_removes_no_other_units(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert start(tmp_path, root, "green", unit=UNIT2) == (
        0, STARTED.format(task="green", operator="Developer", round=1), "")
    task_file(root).unlink()
    assert fail(tmp_path, root, "green", "other", unit=UNIT2) == (0, "", "")
    assert rounds_json(root, UNIT) == {"unit": UNIT, "rounds": {"green": R3[:2]}}
    assert rounds_json(root, UNIT2) == {"unit": UNIT2, "rounds": {"green": ["other"]}}
    assert start(tmp_path, root, "green", unit=UNIT) == (
        0, STARTED.format(task="green", operator="Developer", round=3), "")


def test_sc1_2_the_old_rounds_file_is_neither_read_written_nor_removed(tmp_path):
    root = make_repo(tmp_path)
    old = json.dumps({"unit": UNIT, "rounds": {"green": ["x", "y"]}}).encode()
    old_rounds(root).write_bytes(old)
    assert start(tmp_path, root) == (
        0, STARTED.format(task="green", operator="Developer", round=1), "")
    task_file(root).unlink()
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert rounds_json(root) == {"unit": UNIT, "rounds": {"green": R3[:2]}}
    assert fail(tmp_path, root, "green", R3[2])[0] == 1
    assert stop(tmp_path, root, "q")[0] == 1
    assert end(tmp_path, root, "green") == (0, "", "")
    assert call(tmp_path, root, "end", "--run", "--unit", UNIT) == (0, "", "")
    assert old_rounds(root).read_bytes() == old


@pytest.mark.parametrize("text", ["", "not json", "[]"], ids=["empty", "not-json", "list"])
def test_sc1_2_a_rounds_file_that_holds_no_counts_is_replaced_by_the_next_fail(tmp_path, text):
    root = make_repo(tmp_path)
    run_dir(root).mkdir(parents=True)
    (run_dir(root) / "rounds.json").write_text(text, encoding="utf-8")
    assert fail(tmp_path, root, "green", R3[0]) == (0, "", "")
    assert rounds_json(root) == {"unit": UNIT, "rounds": {"green": [R3[0]]}}
    assert sorted(p.name for p in run_dir(root).iterdir()) == ["rounds.json"]


# --- SC1.3: after any stop, no PR and no task file ----------------------------------

def test_sc1_3_end_run_removes_the_task_file_and_the_whole_run_folder_of_the_unit(tmp_path):
    root = make_repo(tmp_path)
    failed_rounds(tmp_path, root, "green", R3[:2])
    assert stop(tmp_path, root, "q")[0] == 1
    (run_dir(root) / "draft").mkdir()
    (run_dir(root) / "draft" / "test_x.py").write_text("x", encoding="utf-8")
    assert stop(tmp_path, root, "other", unit=UNIT2)[0] == 1
    other = (run_dir(root, UNIT2) / "stop.json").read_bytes()
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    held = records(root)
    assert call(tmp_path, root, "end", "--run", "--unit", UNIT) == (0, "", "")
    assert not task_file(root).exists() and not run_dir(root).exists()
    assert (run_dir(root, UNIT2) / "stop.json").read_bytes() == other
    assert records(root) == held
    # With nothing standing it is the same call, the same silence.
    assert call(tmp_path, root, "end", "--run", "--unit", UNIT) == (0, "", "")


def test_sc1_3_end_run_needs_the_unit_and_removes_nothing_without_it(tmp_path):
    root = make_repo(tmp_path)
    assert stop(tmp_path, root, "q")[0] == 1
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    before = snapshot(root)
    code, out, err = call(tmp_path, root, "end", "--run")
    assert code == 2 and out == "" and "usage:" in err and "--unit" in err
    assert snapshot(root) == before


# --- the options: stop needs its unit and kind; every --unit is two halves ----------

STOP_USAGE = [
    (["stop", "--task", "green", "--operator", "developer", "--kind", "question",
      "--question", "q"], "--unit"),
    (["stop", "--unit", UNIT, "--task", "green", "--operator", "developer",
      "--question", "q"], "--kind"),
    (["stop", "--unit", UNIT, "--task", "green", "--operator", "developer", "--kind", "bogus",
      "--question", "q"], "bogus"),
    (["stop", "--unit", UNIT, "--task", "green", "--operator", "developer", "--kind", "fail",
      "--question", "q"], "fail"),
]


@pytest.mark.parametrize("argv, named", STOP_USAGE,
                         ids=["no-unit", "no-kind", "kind-bogus", "kind-fail"])
def test_sc1_1_a_stop_without_its_unit_or_kind_is_a_usage_error_and_writes_nothing(
        tmp_path, argv, named):
    root = make_repo(tmp_path)
    assert fail(tmp_path, root, "green", R3[0]) == (0, "", "")
    assert rounds_json(root) == {"unit": UNIT, "rounds": {"green": [R3[0]]}}, \
        "fail writes rounds.json in the run folder"
    before = snapshot(root)
    code, out, err = call(tmp_path, root, *argv)
    assert code == 2 and out == ""
    assert "usage:" in err and named in err
    assert snapshot(root) == before


BAD_UNITS = ["a", "a/", "/b", "a/b/c", "./b", "a/.", "../b", "a/..", "a\\b", "a/b\\c"]
COMMANDS = {
    "start": lambda u: ["start", "--unit", u, "--task", "green", "--operator", "developer"],
    "end": lambda u: ["end", "--unit", u, "--task", "green"],
    "fail": lambda u: ["fail", "--unit", u, "--task", "green", "--reason", "r"],
    "stop": lambda u: ["stop", "--unit", u, "--task", "green", "--operator", "developer",
                       "--kind", "question", "--question", "q"],
    "end-run": lambda u: ["end", "--run", "--unit", u],
}


@pytest.mark.parametrize("verb", list(COMMANDS))
@pytest.mark.parametrize("unit", BAD_UNITS, ids=[repr(u) for u in BAD_UNITS])
def test_sc1_1_a_unit_that_is_not_two_plain_halves_is_a_usage_error_and_writes_nothing(
        tmp_path, verb, unit):
    root = make_repo(tmp_path)
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


# --- the flow ----------------------------------------------------------------------

TASKPY = "python {skill-dir}/../../workflows/tools/task.py"
REMOVE_TASK_FILE = "rm -f {gitdir}/sdlc-task.json"
REFUSAL_SPAN = (f"{TASKPY} stop --unit {{contract}}/{{unit}} --task {{task}} "
                "--operator {operator} --kind refusal --question '{line}'")


def flow() -> str:
    assert FLOW.is_file(), "skills/sdlc/flows/execute.md is not written"
    return FLOW.read_text(encoding="utf-8")


def spans(text: str) -> list[tuple[int, str]]:
    return [(m.start(), m[1]) for m in re.finditer(r"`([^`\n]+)`", text)
            if m[1].startswith(("python ", "git ", "rm ", "gh "))]


def task_spans(text: str, verb: str) -> list[tuple[int, str]]:
    return [(at, c) for at, c in spans(text) if c.startswith(f"{TASKPY} {verb} ")
            or c == f"{TASKPY} {verb}"]


def reading(text: str, at: int, command: str) -> str:
    """What the flow says after a command: up to the next command span or blank line."""
    later = [o for o, _ in spans(text) if o > at]
    tail = text[at + len(command) + 2:(later[0] if later else len(text))]
    return tail.split("\n\n")[0]


def test_sc1_1_every_stop_call_of_the_flow_passes_the_unit_and_a_kind():
    found = task_spans(flow(), "stop")
    assert found, "the flow runs no task.py stop"
    kinds = set()
    for _, command in found:
        assert "--unit {contract}/{unit}" in command, command
        assert "--task {task}" in command and "--operator {operator}" in command, command
        kind = re.search(r"--kind (question|error|refusal)(?= )", command)
        assert kind, command
        kinds.add(kind[1])
        assert re.search(r"--question '\{\w+\}'", command), command
    assert kinds == {"question", "error", "refusal"}, kinds


def test_sc1_1_a_members_question_stops_with_kind_question_and_its_error_with_kind_error():
    text = flow()
    found = task_spans(text, "stop")
    kinds = set()
    for number, (at, command) in enumerate(found):
        named = re.search(r"--kind (\w+)", command)
        assert named, command
        kind = named[1]
        kinds.add(kind)
        if kind not in ("question", "error"):
            continue
        # The clause that leads to the call: back to the previous stop call, or to the
        # start of the sentence (a full stop before a space, or a line start).
        floor = found[number - 1][0] + len(found[number - 1][1]) + 2 if number else 0
        before = text[floor:at]
        start_at = max([m.end() for m in re.finditer(r"[.!?](?=\s)|\n", before)], default=0)
        clause = before[start_at:]
        if kind == "question":
            assert re.search(r"\bquestions\b", clause), \
                f"the clause before the --kind question call does not name questions: {clause!r}"
        else:
            assert re.search(r"\berror\b", clause), \
                f"the clause before the --kind error call does not name error: {clause!r}"
            assert not re.search(r"\bquestions\b", clause), \
                f"the clause before the --kind error call names questions: {clause!r}"
    assert {"question", "error"} <= kinds, f"stop calls with --kind {sorted(kinds)}"


def test_sc1_2_every_fail_call_of_the_flow_passes_the_operator():
    found = [c for _, c in task_spans(flow(), "fail")]
    assert found, "the flow runs no task.py fail"
    for command in found:
        assert "--unit {contract}/{unit}" in command, command
        assert re.search(r"--operator \{operator\}(?= |$)", command), command
        assert "--reason '{reasons}'" in command, command


def test_sc1_3_every_stop_and_fail_of_the_flow_shows_what_it_prints_and_stops_with_no_pr():
    text = flow()
    for verb in ("stop", "fail"):
        found = task_spans(text, verb)
        assert found, f"the flow runs no task.py {verb}"
        for at, command in found:
            assert ("--kind " in command) if verb == "stop" else ("--operator " in command),                 command
            if "--kind refusal" in command:
                continue
            after = reading(text, at, command)
            assert "STOP" in after and "no PR" in after, (command, after)


def test_sc1_1_a_refused_task_start_runs_the_refusal_stop_in_one_bash_call_then_stops_with_no_pr():
    text = flow()
    found = [(at, c) for at, c in task_spans(text, "stop") if "--kind refusal" in c]
    assert [c for _, c in found] == [REFUSAL_SPAN], found
    at, command = found[0]
    assert not re.search(r"exits 1, SHOW its line and STOP\.", text), \
        "a refused start still stops with no stop record"
    phrase = text.index("`task.py start` exits 1")
    between = text[phrase:at]
    assert phrase < at and "SHOW" in between and "STOP" not in between, between
    assert re.search(r"quoted as \{reasons\} is|'\\''", text[phrase:at + len(command) + 300])
    after = reading(text, at, command)
    assert "one Bash call" in after, after
    assert "STOP" in after and "no PR" in after, after


def test_sc1_1_the_refusal_stop_does_not_remove_the_task_file_first():
    text = flow()
    commands = spans(text)
    index = [i for i, (_, c) in enumerate(commands) if "--kind refusal" in c]
    assert len(index) == 1, index
    assert commands[index[0] - 1][1] != REMOVE_TASK_FILE, \
        "the refused start leaves the task file standing"


def test_sc1_3_the_last_step_ends_the_run_of_the_unit():
    text = flow()
    found = [c for _, c in task_spans(text, "end") if " --run" in c]
    assert found == [f"{TASKPY} end --run --unit {{contract}}/{{unit}}"], found


def test_sc1_3_the_flow_stays_within_its_character_ceiling_with_the_refusal_step_in():
    text = flow()
    assert "--kind refusal" in text, "the refused-start step is not written"
    assert len(text) <= 12_000, len(text)
