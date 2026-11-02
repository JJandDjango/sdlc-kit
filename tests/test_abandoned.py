"""Abandoned-run suite (contract: run-restart, unit rs4-abandoned, checks SC5.1 and SC5.2).

A run folder with run.json and no stop.json is an abandoned run. `task.py restart --unit
C/U` (no --go) reads it and changes nothing. The flow `restart.md` shows the abandoned
question, takes the user's word and starts nothing before it: on yes it holds {answer} as
null, runs `task.py restart --unit C/U --go --scratch DIR` (never --fresh) and continues at
the step of the task in hand; on any other reply it shows the no line and stops with no PR.
`task.py restart --go` removes the task file only when its "unit" is the unit restarted:
another unit's task file stays. The flow is read as text.

`task.py` runs as a subprocess on a fixture repository under tmp_path (the way
tests/test_restart.py does); nothing is imported from it.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract

ROOT = Path(taskcontract.__file__).resolve().parents[1]
TASK_PY = ROOT / "workflows" / "tools" / "task.py"
EXECUTE = ROOT / "skills" / "sdlc" / "flows" / "execute.md"
RESTART = ROOT / "skills" / "sdlc" / "flows" / "restart.md"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
CEILING = 12_000
EXECUTE_CHARS = 11_991

CONTRACT, U, U2 = "exec-fix", "u1-work", "u2-more"
UNIT, UNIT2 = f"{CONTRACT}/{U}", f"{CONTRACT}/{U2}"
BRANCH = "feat/exec-fix-u1-work"
INTENT = ("A fixture contract for the abandoned-run suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")
STARTED = "Task {task}: {operator}, round {round}\n"
REASONS = ["one: 2 sketches failed: SC1.1 (a.py:4), SC1.2 (a.py:9)",
           "two: 1 sketch failed: SC1.2 (a.py:9)"]
DRAFT = {"test_file": "tests/test_cli.py", "interface": "parse_args(argv) -> Args",
         "tests": [{"name": "t1", "proves": "SC1.1", "intent": "pins parse_args"}],
         "red_proof": {"command": "prove", "summary": "red"}, "questions": []}
DRAFT_BYTES = b"def test_parse_args():\n    assert False\n"
KEPT_AT_GREEN = {"draft": DRAFT, "draft-file": "draft/test_cli.py"}
# The task in hand, its operator and the name the start line prints for it.
TASKS = {"green": ("developer", "Developer"),
         "approve-commit": ("receipts", "receipts"),
         "commit": ("orchestrator", "Orchestrator")}


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


def go(tmp_path, root, scratch, unit=UNIT):
    return restart(tmp_path, root, "--go", "--scratch", str(scratch), unit=unit)


def run_dir(root: Path, unit: str = UNIT) -> Path:
    return root / ".git" / "sdlc-run" / unit


def task_file(root: Path) -> Path:
    return root / ".git" / "sdlc-task.json"


def load(path: Path):
    assert path.is_file(), f"{path} is not written"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        raise AssertionError(f"{path} does not hold JSON") from None


def run_json(root: Path, unit: str = UNIT) -> dict:
    return load(run_dir(root, unit) / "run.json")


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


def abandon_at(tmp_path: Path, root: Path, task: str, unit: str = UNIT) -> None:
    """The session dies with `task` running: its task file stands and no stop is written."""
    passes_to_green(tmp_path, root, unit)
    operator, printed = TASKS[task]
    if task == "green":
        for reason in REASONS:
            assert fail(tmp_path, root, "green", reason, unit=unit,
                        operator="dev-verifier") == (0, "", "")
        assert start(tmp_path, root, "green", "developer", unit) == (
            0, STARTED.format(task="green", operator="Developer", round=3), "")
        return
    assert end(tmp_path, root, "green", unit=unit) == (0, "", "")
    assert start(tmp_path, root, "approve-commit", "receipts", unit)[0] == 0
    if task == "commit":
        assert end(tmp_path, root, "approve-commit", "receipts", unit) == (0, "", "")
        assert start(tmp_path, root, "commit", "orchestrator", unit)[0] == 0


def one_line(out: str) -> dict:
    assert out.endswith("\n") and out.count("\n") == 1, out
    return json.loads(out)


# --- SC5.1 and SC5.2: task.py restart on an abandoned run ------------------------------

@pytest.mark.parametrize("task", list(TASKS))
def test_sc5_2_an_abandoned_task_restarts_by_go_and_a_task_file_of_another_unit_stays(
        tmp_path, task):
    operator, printed = TASKS[task]
    root = make_repo(tmp_path)
    abandon_at(tmp_path, root, task)
    held_records = records(root)
    assert held_records, "the earlier tasks are recorded done"
    assert task_file(root).is_file(), "the dead session leaves its task file"
    # SC5.1: the read-only restart shows the run and changes nothing.
    before = snapshot(root)
    code, out, err = restart(tmp_path, root)
    assert (code, err) == (0, ""), (code, out, err)
    line = one_line(out)
    assert (line["state"], line["task"], line["operator"]) == ("abandoned", task, operator)
    assert isinstance(line["round"], int) and line["kind"] is None and line["text"] is None
    assert line["kept"] == KEPT_AT_GREEN
    assert snapshot(root) == before, "restart with no --go changes nothing"
    # SC5.2: --go removes the task file of its own unit, writes the draft, keeps the rest.
    run_bytes = (run_dir(root) / "run.json").read_bytes()
    scratch = tmp_path / "fresh-session" / "scratch"
    assert go(tmp_path, root, scratch) == (0, out, "")
    assert not task_file(root).exists()
    assert not (run_dir(root) / "stop.json").exists()
    assert (scratch / "draft" / "tests" / "test_cli.py").read_bytes() == DRAFT_BYTES
    assert (run_dir(root) / "run.json").read_bytes() == run_bytes
    assert records(root) == held_records, "no earlier task runs again"
    assert start(tmp_path, root, task, operator) == (
        0, STARTED.format(task=task, operator=printed, round=line["round"]), "")
    # A task file that names another unit stays, and then stops this unit's start.
    task_file(root).unlink()
    assert start(tmp_path, root, "write-tests", "qa", UNIT2)[0] == 0
    other = task_file(root).read_bytes()
    assert json.loads(other)["unit"] == UNIT2
    other_run = (run_dir(root, UNIT2) / "run.json").read_bytes()
    assert go(tmp_path, root, tmp_path / "second-session" / "scratch")[0] == 0
    assert task_file(root).is_file(), "the task file of another unit is removed"
    assert task_file(root).read_bytes() == other
    assert (run_dir(root, UNIT2) / "run.json").read_bytes() == other_run
    assert start(tmp_path, root, task, operator)[0] != 0
    assert task_file(root).read_bytes() == other


def test_sc5_2_go_with_another_units_task_file_standing_leaves_it_byte_identical(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert end(tmp_path, root, "write-tests") == (0, "", "")
    assert start(tmp_path, root, "green", "developer", UNIT2)[0] == 0
    other = task_file(root).read_bytes()
    assert json.loads(other)["unit"] == UNIT2
    # SC5.1, with no task file of this unit: the read-only restart changes nothing.
    before = snapshot(root)
    code, out, err = restart(tmp_path, root)
    assert (code, err) == (0, ""), (code, out, err)
    assert one_line(out) == {"state": "abandoned", "task": "write-tests", "operator": None,
                             "round": 1, "kind": None, "text": None, "kept": {},
                             "progress": []}
    assert snapshot(root) == before
    # SC5.2: --go leaves the other unit's file and run folder as they were.
    run_bytes = (run_dir(root) / "run.json").read_bytes()
    other_run = (run_dir(root, UNIT2) / "run.json").read_bytes()
    scratch = tmp_path / "fresh-session" / "scratch"
    assert go(tmp_path, root, scratch) == (0, out, "")
    assert task_file(root).is_file(), "the task file of another unit is removed"
    assert task_file(root).read_bytes() == other
    assert (run_dir(root) / "run.json").read_bytes() == run_bytes
    assert (run_dir(root, UNIT2) / "run.json").read_bytes() == other_run
    code, out, err = start(tmp_path, root, "write-tests", "qa")
    assert code != 0, "a task file stands, so the start refuses"
    assert task_file(root).read_bytes() == other


def test_sc5_2_go_on_a_stopped_run_removes_its_stop_and_keeps_another_units_task_file(tmp_path):
    root = make_repo(tmp_path)
    passes_to_green(tmp_path, root)
    assert stop(tmp_path, root, "Which header declares parse_args?")[0] == 1
    assert not task_file(root).exists()
    assert start(tmp_path, root, "write-tests", "qa", UNIT2)[0] == 0
    other = task_file(root).read_bytes()
    assert json.loads(other)["unit"] == UNIT2
    scratch = tmp_path / "fresh-session" / "scratch"
    code, out, err = go(tmp_path, root, scratch)
    assert (code, err) == (0, ""), (code, out, err)
    assert one_line(out)["state"] == "stopped"
    assert not (run_dir(root) / "stop.json").exists(), "a stopped run still loses its stop"
    assert (scratch / "draft" / "tests" / "test_cli.py").read_bytes() == DRAFT_BYTES
    assert task_file(root).is_file(), "the task file of another unit is removed"
    assert task_file(root).read_bytes() == other
    assert start(tmp_path, root, "green", "developer")[0] != 0
    assert task_file(root).read_bytes() == other


# --- the flow: restart.md -------------------------------------------------------------

TASKPY = "python {skill-dir}/../../workflows/tools/task.py"
RESTART_CMD = f"{TASKPY} restart --unit {{contract}}/{{unit}}"
FRESH_GO = f"{RESTART_CMD} --go --fresh --scratch {{scratch}}"
PLAIN_GO = f"{RESTART_CMD} --go --scratch {{scratch}}"
ABANDONED_Q = ("Execution was abandoned: {contract} unit {unit}, task {task}, round {n}. "
               "Restart at {task}?")
NO_LINE = "Execution did not restart: {contract} unit {unit} stays abandoned at {task}."


def read(path: Path) -> str:
    assert path.is_file(), f"{path.relative_to(ROOT).as_posix()} is not written"
    return path.read_text(encoding="utf-8")


def spans(text: str) -> list[tuple[int, str]]:
    return [(m.start(), m[1]) for m in re.finditer(r"`([^`\n]+)`", text)
            if m[1].startswith(("python ", "git ", "rm ", "gh "))]


def step(text: str, label: str) -> str:
    """The text of one instruction step: from its label to the next label (or the end)."""
    found = re.search(rf"^{label}\. ", text, re.MULTILINE)
    assert found, f"restart.md has no step {label}"
    later = re.search(r"^R\d\. ", text[found.end():], re.MULTILINE)
    return text[found.start():found.end() + later.start()] if later else text[found.start():]


def r1() -> str:
    return step(read(RESTART), "R1")


def test_sc5_1_restart_md_shows_the_abandoned_question_verbatim_in_r1_and_no_longer_waits_for_rs4():
    text = read(RESTART)
    assert text.count(ABANDONED_Q) == 1, "the abandoned question stands once, verbatim"
    window = r1()
    assert ABANDONED_Q in window, "the abandoned path stays in R1"
    assert "SHOW" in window[:window.index(ABANDONED_Q)][-400:], "R1 SHOWs the question"
    assert "`round` as {n}" in window, "{n} is the round of the JSON line"
    assert "until rs4" not in text and "rs4" not in text
    assert "abandoned" in window and "`abandoned`" in window


def test_sc5_1_restart_md_takes_the_word_from_answer_first_else_chat_and_a_headless_session_waits():
    window = r1()
    assert re.search(r"`?--answer`?[^\n]*first[^\n]*chat|`?--answer`? first[^\n]*chat", window), \
        "the word comes from --answer first, else from chat"
    assert "R2" in window, "the word is read as R2 reads the answer"
    assert re.search(r"headless session with no `?--answer`? ends its turn at (that|the) question",
                     window), "a headless session with no --answer ends its turn at the question"
    after = window[window.index("headless session with no"):]
    assert "starting nothing" in after[:300], "it starts nothing"
    assert "run folder" in after[:300] and "task file" in after[:300] \
        and re.search(r"(stay|stays|remain|remains)", after[:300]), \
        "the run folder and the task file stay"


def test_sc5_1_restart_md_runs_nothing_before_the_word():
    text = read(RESTART)
    assert ABANDONED_Q in text, "the abandoned question is not in restart.md"
    window = r1()
    assert spans(window) == [], "R1 runs no command: no --go and no task.py start before a yes"
    assert "task.py" not in window
    assert text.index(ABANDONED_Q) < text.index(PLAIN_GO), "no --go before the question"
    assert text.index(ABANDONED_Q) < text.index("R4. "), "R4 follows the question"
    assert text.index(ABANDONED_Q) < text.index("R6. "), "R6 follows the question"


def test_sc5_1_restart_md_reads_yes_as_the_word_and_any_other_reply_as_no():
    window = r1()
    assert re.search(r"\byes\b[^\n]*restart", window, re.IGNORECASE), "a yes restarts"
    assert re.search(r"any other reply (is|as) (a )?no\b|any other reply is `?no`?", window), \
        "any other reply is no"
    assert window.index(ABANDONED_Q) < re.search(r"any other reply", window).start(), \
        "the word follows the question"


def test_sc5_1_restart_md_shows_the_no_line_and_stops_with_no_pr_removing_nothing():
    text = read(RESTART)
    assert text.count(NO_LINE) == 1, "the no line stands once, verbatim"
    assert NO_LINE in r1(), "the no line stands in R1"
    assert text.index(ABANDONED_Q) < text.index(NO_LINE)
    window = r1()
    near = window[max(0, window.index(NO_LINE) - 300):]
    assert "SHOW" in near and "STOP" in near and "no PR" in near, near
    assert re.search(r"[Nn]o `?--go`? runs", near), "on no, no --go runs"
    assert re.search(r"nothing is removed", near), "on no, nothing is removed"
    assert "task.py" not in near, "the no path runs no task.py command"


def test_sc5_2_restart_md_holds_answer_as_null_after_the_word_on_an_abandoned_run():
    window = r1()
    assert re.search(r"HOLD \{answer\} as `null`", window), \
        "R1 holds {answer} as null after the word"
    assert window.index(ABANDONED_Q) < re.search(r"HOLD \{answer\} as `null`", window).start(), \
        "the null is held after the word"
    assert "E2" in window and "--answer" in window, "E2's raw --answer text is the word"


def test_sc5_2_restart_md_runs_the_plain_go_for_an_abandoned_run_and_never_fresh():
    text = read(RESTART)
    found = [c for _, c in spans(text) if c.startswith(RESTART_CMD)]
    assert sorted(found) == sorted([PLAIN_GO, FRESH_GO]), "no new command form: " + repr(found)
    window, r4 = r1(), step(text, "R4")
    assert PLAIN_GO in r4 and "abandoned" in r4, "R4 runs the plain --go for an abandoned run"
    assert re.search(r"never `?--fresh`?", window + r4), "an abandoned run never takes --fresh"
    assert "R4" in window and "R6" in window, "on yes, R1 goes on to R4 and R6"


def test_sc5_2_restart_md_continues_at_the_step_of_the_task_with_no_answer_to_show():
    r6 = step(read(RESTART), "R6")
    assert "No earlier task and no earlier step runs again" in r6
    assert "abandoned" in r6, "R6 names the abandoned run at a task with no member"
    assert "approve-commit" in r6 and "commit" in r6 and "execute.md" in r6
    assert re.search(r"abandoned[^\n]*no answer to show|no answer to show[^\n]*abandoned", r6), \
        "an abandoned run has no answer to show at a task with no member"
    assert re.search(r"as execute\.md says", r6)


def test_sc5_2_restart_md_stays_under_the_ceiling_and_execute_md_is_unchanged():
    text = read(RESTART)
    assert ABANDONED_Q in text and NO_LINE in text
    assert len(text) < CEILING, len(text)
    execute = read(EXECUTE)
    assert len(execute) == EXECUTE_CHARS, len(execute)
    assert "--fresh" not in execute and "--enough" not in execute
