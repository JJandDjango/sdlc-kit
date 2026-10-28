"""Declaration suite (contract: execution-team, unit e1-declaration, check SC2.3).

The unit adds the declaration (`test:` and `wall:` blocks of
`.sdlc/config.yaml`, read for `test:` by `taskcontract.declaration.read_test`)
and `workflows/tools/task.py start`, the one place a task starts. With no
usable `test.command` a task does not start: SC2.3's line on stderr, exit 1,
nothing written. The kit declares its own blocks.

`task.py` runs as a subprocess beside the package the tests import
(`Path(taskcontract.__file__).parents[1]`, as tests/test_node_start.py finds the
repo), so a run against a prototype runs the prototype's script. Every test
builds its own repository under tmp_path, with `git init`, a config and a
ready contract, and passes `--root` to it: nothing is written into the real
repository, its `.git` folder or its `.sdlc/progress`.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract
from conftest import write_seat_roster

ROOT = Path(taskcontract.__file__).resolve().parents[1]
TASK_PY = ROOT / "workflows" / "tools" / "task.py"

CONTRACT, U = "exec-fix", "u1-work"
UNIT = f"{CONTRACT}/{U}"
TASKS = ["approve-tests", "write-tests", "prove-red", "green", "approve-commit", "commit",
         "two-key"]
OPERATORS = [("qa", "QA"), ("qa-verifier", "QA verifier"), ("developer", "Developer"),
             ("dev-verifier", "Dev verifier"), ("receipts", "receipts"),
             ("orchestrator", "Orchestrator")]
INTENT = ("A fixture contract for the declaration suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")

NO_COMMAND = "Task {task} did not start: the repository declares no test command.\n"
NO_GIT = "Task {task} did not start: no git repository at {root}.\n"
RUNNING = "Task {task} did not start: task {running} is running.\n"
STARTED = "Task {task}: {operator}, round 1\n"
G1_LINE = f"{U} cannot start: G1 has not passed for {CONTRACT}\n"

# The engine's blocks, as the design draws them.
DECLARED = """\
kit: fixture
test:
  command: [test.bat]
  file: ["{file}"]
  build: [build.bat]
wall:
  functional: [tests/run_*.bat]
  unit: [tests/*.cpp]
  code: [src/]
  interface: [src/*.h]
"""

# Declarations that hold no usable test.command: (id, config text; None = no file).
UNUSABLE = [
    ("no-config-file", None),
    ("config-does-not-parse", "test: [unclosed\n"),
    ("config-is-a-list", "- test\n- command\n"),
    ("no-test-block", "kit: fixture\nwall:\n  functional: [tests/]\n"),
    ("test-is-a-string", "test: pytest\n"),
    ("test-is-a-list", "test: [command]\n"),
    ("no-command", "test:\n  file: ['{file}']\n"),
    ("command-is-null", "test:\n  command:\n"),
    ("command-is-an-empty-list", "test:\n  command: []\n"),
    ("command-is-a-string", "test:\n  command: python -m pytest\n"),
    ("command-is-a-mapping", "test:\n  command: {a: b}\n"),
    ("command-holds-a-non-string", "test:\n  command: [python, 3]\n"),
    ("command-holds-an-empty-string", "test:\n  command: [python, '']\n"),
]
UNUSABLE_IDS = [name for name, _ in UNUSABLE]


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


def git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                          encoding="utf-8", errors="replace")
    return done.stdout


def make_repo(tmp_path: Path, config: str | None = DECLARED, git_repo: bool = True,
              g1: bool = False) -> Path:
    """<tmp>/repo: a config, a ready contract with one unit, a ratified seat
    roster, and a git repository. With `g1`, G1 is an active gate and the
    feature's G1 has not passed."""
    root = tmp_path / "repo"
    root.mkdir()
    (tmp_path / "cwd").mkdir()
    if config is not None:
        text = config + ("active_gates: [G0, G1]\n" if g1 else "")
        (root / ".sdlc").mkdir()
        (root / ".sdlc" / "config.yaml").write_text(text, encoding="utf-8")
    _dump(root / "specs" / CONTRACT / "contract.yaml", {
        "id": CONTRACT, "title": "A fixture feature", "intent": INTENT,
        "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
        "decomposition": [_unit(U)], "dependencies": [], "entities": [],
        "provenance": {"origin": "human-request"}})
    (root / "docs" / "features").mkdir(parents=True)
    (root / "docs" / "features" / f"{CONTRACT}.md").write_text(_document(5), encoding="utf-8")
    (root / "docs" / "features" / f"{CONTRACT}.design.md").write_text(
        _document(4), encoding="utf-8")
    write_seat_roster(root, values=("po", "engineer"))
    if git_repo:
        git(root, "init", "-q")
    return root


def start(tmp_path: Path, root: Path, task: str = "green", operator: str = "developer",
          unit: str = UNIT, extra_env: dict | None = None):
    """(exit code, stdout, stderr) of `task.py start`, run from a folder that
    is not the repository and with no git repository above the fixture."""
    argv = [sys.executable, str(TASK_PY), "start", "--unit", unit, "--task", task,
            "--operator", operator, "--root", str(root)]
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1",
           **(extra_env or {})}
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100)
    return done.returncode, done.stdout, done.stderr


def snapshot(root: Path) -> dict:
    """Every path under the repository except its git folder, with the bytes."""
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*") if ".git" not in p.relative_to(root).parts}


def task_file(root: Path) -> Path:
    return root / ".git" / "sdlc-task.json"


def records(root: Path) -> list[dict]:
    path = root / ".sdlc" / "progress" / f"{CONTRACT}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["records"] if path.is_file() else []


def refuses(tmp_path, root, line: str, **kwargs) -> None:
    """The call is refused with `line` on stderr, exit 1, and writes nothing
    (the git folder aside, which holds the task file)."""
    before = snapshot(root)
    held = task_file(root).read_bytes() if task_file(root).is_file() else None
    assert start(tmp_path, root, **kwargs) == (1, "", line)
    assert snapshot(root) == before
    assert (task_file(root).read_bytes() if task_file(root).is_file() else None) == held


def read_test(root: Path):
    spec = importlib.util.find_spec("taskcontract.declaration")
    assert spec is not None, "taskcontract.declaration does not exist"
    from taskcontract.declaration import read_test as reader
    return reader(root)


# --- SC2.3: no declared test command starts no task ----------------------------------

def test_sc2_3_a_repository_with_no_declared_test_command_starts_no_task(tmp_path):
    root = make_repo(tmp_path, config="kit: fixture\n")
    refuses(tmp_path, root, NO_COMMAND.format(task="prove-red"), task="prove-red")
    assert not task_file(root).exists()
    assert records(root) == []
    assert not (root / ".sdlc" / "progress").exists()


@pytest.mark.parametrize("config", [c for _, c in UNUSABLE], ids=UNUSABLE_IDS)
def test_sc2_3_each_unusable_test_command_gives_the_message(tmp_path, config):
    root = make_repo(tmp_path, config=config)
    refuses(tmp_path, root, NO_COMMAND.format(task="green"))
    assert not (root / ".sdlc" / "progress").exists()


# --- done_means: a repository declares test: and wall: ------------------------------

def test_done_means_read_test_returns_the_declared_command_file_and_build(tmp_path):
    root = make_repo(tmp_path)
    got = read_test(root)
    assert got is not None
    assert (got.command, got.file, got.build) == (["test.bat"], ["{file}"], ["build.bat"])
    assert all(isinstance(part, list) for part in (got.command, got.file, got.build))


def test_done_means_an_absent_file_and_build_read_as_empty_lists(tmp_path):
    root = make_repo(tmp_path, config="test:\n  command: [python, -m, pytest]\n")
    got = read_test(root)
    assert got is not None
    assert (got.command, got.file, got.build) == (["python", "-m", "pytest"], [], [])


@pytest.mark.parametrize("config", [c for _, c in UNUSABLE], ids=UNUSABLE_IDS)
def test_sc2_3_read_test_returns_none_for_each_unusable_test_command(tmp_path, config):
    assert read_test(make_repo(tmp_path, config=config)) is None


def test_done_means_the_kit_declares_its_own_test_and_wall_blocks():
    config = yaml.safe_load((ROOT / ".sdlc" / "config.yaml").read_text(encoding="utf-8"))
    test = config.get("test") or {}
    assert test.get("command") == ["python", "-P", "-m", "pytest", "-q", "-n", "auto"]
    assert test.get("file") == ["python", "-P", "-m", "pytest", "{file}", "-q"]
    assert "build" not in test
    assert (config.get("wall") or {}).get("functional") == ["tests/"]
    got = read_test(ROOT)
    assert got is not None and got.build == []
    assert got.command == test["command"] and got.file == test["file"]


# --- reading (a): the options -------------------------------------------------------

@pytest.mark.parametrize("options", [("--task", "bogus"), ("--operator", "bogus")],
                         ids=["task", "operator"])
def test_reading_a_a_value_outside_the_lists_is_a_usage_error_and_writes_nothing(
        tmp_path, options):
    root = make_repo(tmp_path)
    before = snapshot(root)
    argv = [sys.executable, str(TASK_PY), "start", "--unit", UNIT, "--task", "green",
            "--operator", "developer", "--root", str(root)]
    argv[argv.index(options[0]) + 1] = options[1]
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1"}
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100)
    assert done.returncode == 2 and done.stdout == ""
    assert "usage:" in done.stderr and options[0] in done.stderr and "bogus" in done.stderr
    assert snapshot(root) == before and not task_file(root).exists()


@pytest.mark.parametrize("task", TASKS)
def test_reading_a_each_of_the_seven_tasks_starts(tmp_path, task):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, task=task) == (
        0, STARTED.format(task=task, operator="Developer"), "")
    assert json.loads(task_file(root).read_text(encoding="utf-8"))["task"] == task
    assert [(r["item"], r["state"]) for r in records(root)] == [(f"{UNIT}/{task}", "doing")]


@pytest.mark.parametrize("operator, printed", OPERATORS, ids=[o for o, _ in OPERATORS])
def test_reading_a_each_operator_prints_as_its_name_and_the_file_keeps_its_id(
        tmp_path, operator, printed):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, operator=operator) == (
        0, STARTED.format(task="green", operator=printed), "")
    assert json.loads(task_file(root).read_text(encoding="utf-8")) == {
        "task": "green", "operator": operator, "round": 1}


# --- reading (b): the start ---------------------------------------------------------

def test_reading_b_a_start_writes_the_task_file_prints_its_line_and_records_doing(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, task="prove-red", operator="qa") == (
        0, "Task prove-red: QA, round 1\n", "")
    assert task_file(root) == root / ".git" / "sdlc-task.json" and task_file(root).is_file()
    assert json.loads(task_file(root).read_text(encoding="utf-8")) == {
        "task": "prove-red", "operator": "qa", "round": 1}
    got = records(root)
    assert len(got) == 1
    assert got[0]["item"] == f"{UNIT}/prove-red" and got[0]["state"] == "doing"


def test_reading_b_the_declaration_is_checked_before_the_git_repository(tmp_path):
    root = make_repo(tmp_path, config="kit: fixture\n", git_repo=False)
    refuses(tmp_path, root, NO_COMMAND.format(task="green"))


def test_reading_b_no_git_repository_refuses_and_names_the_root_as_given(tmp_path):
    root = make_repo(tmp_path, git_repo=False)
    refuses(tmp_path, root, NO_GIT.format(task="green", root=root))
    assert not (root / ".sdlc" / "progress").exists()
    assert not any(p.name == "sdlc-task.json" for p in tmp_path.rglob("*"))


def test_reading_b_a_running_task_refuses_and_leaves_the_file_as_it_was(tmp_path):
    root = make_repo(tmp_path)
    held = json.dumps({"task": "prove-red", "operator": "qa", "round": 1}, indent=2).encode()
    task_file(root).write_bytes(held)
    refuses(tmp_path, root, RUNNING.format(task="green", running="prove-red"))
    assert task_file(root).read_bytes() == held
    assert not (root / ".sdlc" / "progress").exists()


def test_reading_b_a_second_start_while_the_first_stands_is_refused(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, task="green")[0] == 0
    held, first = task_file(root).read_bytes(), records(root)
    refuses(tmp_path, root, RUNNING.format(task="two-key", running="green"),
            task="two-key", operator="dev-verifier")
    assert task_file(root).read_bytes() == held and records(root) == first


def test_reading_b_the_declaration_is_checked_before_a_running_task(tmp_path):
    root = make_repo(tmp_path, config="kit: fixture\n")
    held = json.dumps({"task": "prove-red", "operator": "qa", "round": 1}).encode()
    task_file(root).write_bytes(held)
    refuses(tmp_path, root, NO_COMMAND.format(task="green"))
    assert task_file(root).read_bytes() == held


def test_reading_b_a_running_task_is_checked_before_progress_start_refuses(tmp_path):
    root = make_repo(tmp_path, g1=True)
    task_file(root).write_text('{"task": "prove-red"}', encoding="utf-8")
    refuses(tmp_path, root, RUNNING.format(task="green", running="prove-red"))


def test_reading_b_progress_starts_refusal_prints_verbatim_and_writes_nothing(tmp_path):
    root = make_repo(tmp_path, g1=True)
    refuses(tmp_path, root, G1_LINE)
    assert not task_file(root).exists() and not (root / ".sdlc" / "progress").exists()


def test_reading_b_an_unknown_unit_prints_progress_starts_line_and_exits_1(tmp_path):
    root = make_repo(tmp_path)
    refuses(tmp_path, root,
            "no node 'exec-fix/u9-none/green' - print the tree to list every node id\n",
            unit=f"{CONTRACT}/u9-none")
    assert not task_file(root).exists()


# --- reading (d): the task file -----------------------------------------------------

@pytest.mark.parametrize("text", [
    "", "not json", "[]", "[\"green\"]", "{}", "{\"operator\": \"qa\"}",
    "{\"task\": \"\"}", "{\"task\": 3}", "{\"task\": null}", "\"green\""],
    ids=["empty", "not-json", "empty-list", "list", "empty-object", "no-task", "empty-task",
         "number-task", "null-task", "string"])
def test_reading_d_a_file_that_names_no_task_is_no_running_task_and_start_replaces_it(
        tmp_path, text):
    root = make_repo(tmp_path)
    task_file(root).write_text(text, encoding="utf-8")
    assert start(tmp_path, root, operator="receipts") == (
        0, STARTED.format(task="green", operator="receipts"), "")
    assert json.loads(task_file(root).read_text(encoding="utf-8")) == {
        "task": "green", "operator": "receipts", "round": 1}


def test_reading_d_in_a_linked_worktree_the_file_is_in_the_worktrees_own_git_folder(tmp_path):
    root = make_repo(tmp_path)
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@example.com", "-c", "user.name=t",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=no-hooks",
        "commit", "-q", "-m", "seed")
    wt = tmp_path / "wt"
    git(root, "worktree", "add", "-q", "--detach", str(wt))
    wt_git = Path(git(wt, "rev-parse", "--absolute-git-dir").strip())
    assert wt_git != root / ".git" and (wt / ".git").is_file()
    assert start(tmp_path, wt, operator="dev-verifier") == (
        0, STARTED.format(task="green", operator="Dev verifier"), "")
    assert json.loads((wt_git / "sdlc-task.json").read_text(encoding="utf-8")) == {
        "task": "green", "operator": "dev-verifier", "round": 1}
    assert not task_file(root).exists()
    assert not (wt / ".git" / "sdlc-task.json").exists()


# --- reading (e): the round ---------------------------------------------------------

def test_reading_e_the_round_is_always_1(tmp_path):
    root = make_repo(tmp_path)
    for _ in range(2):
        assert start(tmp_path, root) == (0, STARTED.format(task="green", operator="Developer"), "")
        assert json.loads(task_file(root).read_text(encoding="utf-8"))["round"] == 1
        task_file(root).unlink()


# --- reading (f): the package beside the script -------------------------------------

def test_reading_f_task_py_imports_the_taskcontract_that_sits_beside_it(tmp_path):
    decoy = tmp_path / "decoy" / "taskcontract"
    decoy.mkdir(parents=True)
    (decoy / "__init__.py").write_text('raise ImportError("the decoy package")\n',
                                       encoding="utf-8")
    root = make_repo(tmp_path)
    assert start(tmp_path, root, extra_env={"PYTHONPATH": str(decoy.parent)}) == (
        0, STARTED.format(task="green", operator="Developer"), "")
