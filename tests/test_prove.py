"""Self-test for prove.py, on a toy `taskcontract` package.

run: python -m pytest tests/test_prove.py -q --tb=line

Each test builds a toy git repository (the toy package and a .sdlc/config.yaml
declaring the pytest test command) and a scratch folder under tmp_path, and runs
prove.py with the toy repository as the working directory, as the drafter does.
The draft sits at scratch/draft/tests/test_toy.py.
The environment lacks PYTHONUTF8 on purpose: prove.py sets it itself.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

PROVE = Path(__file__).resolve().parents[1] / "workflows" / "tools" / "prove.py"

TEST = "tests/test_toy.py"
CONFIG = {"test": {"command": [sys.executable, "-m", "pytest", "tests", "-q"],
                   "file": [sys.executable, "-m", "pytest", "{file}", "-q"]}}

OLD = 'def greet(name):\n    return "hello"\n'
NEW = 'def greet(name):\n    return "hello " + name\n'
UNUSED = "\n\ndef unused():\n    return 1\n"

DRAFT = '''import taskcontract


def test_sc1_1_greets_by_name():
    assert taskcontract.greet("ana") == "hello ana"


def test_sc1_2_greets_an_empty_name_with_a_space():
    assert taskcontract.greet("") == "hello "


def test_sc1_3_keeps_accents():
    assert taskcontract.greet("zoé") == "hello zoé"
'''


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "-c", "core.autocrlf=false",
         "-c", "commit.gpgsign=false", *args],
        cwd=repo, capture_output=True, encoding="utf-8", errors="replace", timeout=60)
    assert done.returncode == 0, done.stderr
    return done.stdout.strip()


def commit(repo: Path) -> None:
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--no-verify", "-m", "c")


@pytest.fixture
def world(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    put(repo / ".gitattributes", "* -text\n")
    put(repo / ".sdlc" / "config.yaml", yaml.safe_dump(CONFIG))
    package = repo / "taskcontract" / "__init__.py"
    put(package, OLD + UNUSED)
    commit(repo)
    scratch = tmp_path / "scratch"
    draft = scratch / "draft" / "tests" / "test_toy.py"
    put(draft, DRAFT)
    return SimpleNamespace(repo=repo, scratch=scratch, draft=draft, package=package,
                           exported=scratch / "export" / "taskcontract" / "__init__.py")


def prove(world, *args, test=TEST):
    env = {k: v for k, v in os.environ.items() if k != "PYTHONUTF8"}
    done = subprocess.run(
        [sys.executable, str(PROVE), "--scratch", str(world.scratch), "--test", test, *args],
        cwd=world.repo, env=env, capture_output=True, timeout=300)
    text = done.stdout.decode("utf-8")
    return SimpleNamespace(code=done.returncode, text=text,
                           out=json.loads(text) if text.strip() else None,
                           err=done.stderr.decode("utf-8", "replace"))


def mutations(world, *items):
    path = world.scratch / "mutations.json"
    put(path, json.dumps(list(items)))
    return ["--mutations", str(path)]


def fixed(world):
    """Do what the drafter does: commit the new code, so the draft passes at HEAD."""
    put(world.package, NEW + UNUSED)
    commit(world.repo)


@pytest.fixture
def prove_mod():
    spec = importlib.util.spec_from_file_location("prove_under_test", PROVE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_caught_mutations_exit_zero_and_leave_the_export_byte_for_byte(world):
    fixed(world)
    run = prove(world, *mutations(
        world,
        {"name": "drop-space", "file": "taskcontract/__init__.py",
         "old": '"hello " + name', "new": '"hello" + name'},
        {"name": "same-size", "file": "taskcontract/__init__.py",
         "old": '"hello " + name', "new": '"hellO " + name'}))
    caught = run.out["mutations"]
    assert [m["name"] for m in caught] == ["drop-space", "same-size"]
    assert "test_sc1_1_greets_by_name" in caught[0]["caught_by"]
    assert "test_sc1_1_greets_by_name" in caught[1]["caught_by"]
    assert digest(world.exported) == digest(world.package)
    assert run.code == 0


def test_a_mutation_path_outside_the_export_is_refused(world):
    fixed(world)
    before = digest(world.draft)
    run = prove(world, *mutations(
        world, {"name": "escape", "file": "../draft/tests/test_toy.py", "old": "import", "new": "mport"}))
    assert run.out["mutations"][0]["applied"] is False
    assert digest(world.draft) == before
    assert run.code == 1


def test_red_is_not_ok_on_a_collection_error(world):
    put(world.draft, "import taskcontract.nope\n\n\ndef test_sc1_1_x():\n    assert True\n")
    run = prove(world)
    assert run.out["red"]["red_ok"] is False
    assert run.out["red"]["not_assertion"][0]["kind"] == "error"
    assert run.code == 1


def test_red_is_not_ok_when_a_test_fails_on_an_exception_not_an_assertion(world):
    put(world.draft, "import taskcontract\n\n\ndef test_sc1_1_x():\n    taskcontract.nope()\n")
    run = prove(world)
    assert run.out["red"]["red_ok"] is False
    bad = run.out["red"]["not_assertion"]
    assert [(b["id"], b["kind"]) for b in bad] == [("test_sc1_1_x", "AttributeError")]
    assert "nope" in bad[0]["line"]


def test_red_lists_a_failing_line_decoded_as_utf8(world):
    put(world.draft, DRAFT + '\n\ndef test_sc1_4_raises():\n    raise ValueError("zoé")\n')
    run = prove(world)
    bad = run.out["red"]["not_assertion"]
    assert [(b["id"], b["kind"]) for b in bad] == [("test_sc1_4_raises", "ValueError")]
    assert "zoé" in bad[0]["line"]
    assert run.out["red"]["summary"].startswith("4 failed")


def test_stdout_is_one_compact_json_line_and_logs_hold_the_full_output(world):
    red = prove(world)
    assert red.text.count("\n") <= 1
    assert json.dumps(red.out, separators=(",", ":"), ensure_ascii=False) == red.text.strip()
    assert red.out["scratch"] == str(world.scratch.resolve())
    assert red.out["red"]["log"] == "logs/red.log"
    assert "3 failed" in (world.scratch / red.out["red"]["log"]).read_text(encoding="utf-8")
    fixed(world)
    run = prove(world, *mutations(
        world, {"name": "drop-space", "file": "taskcontract/__init__.py",
                "old": '"hello " + name', "new": '"hello" + name'}))
    assert run.text.count("\n") <= 1
    assert json.dumps(run.out, separators=(",", ":"), ensure_ascii=False) == run.text.strip()
    assert "3 passed" in (world.scratch / "logs" / "baseline.log").read_text(encoding="utf-8")
    log = run.out["mutations"][0]["log"]
    assert log == "logs/mutation-1.log"
    assert "failed" in (world.scratch / log).read_text(encoding="utf-8")


def test_a_run_leaves_the_repo_tree_as_it_found_it(world):
    fixed(world)

    def tree():
        return sorted(p.relative_to(world.repo).as_posix() for p in world.repo.rglob("*")
                      if ".git" not in p.relative_to(world.repo).parts)

    before = tree()
    prove(world)
    prove(world, *mutations(
        world, {"name": "drop-space", "file": "taskcontract/__init__.py",
                "old": '"hello " + name', "new": '"hello" + name'}))
    assert tree() == before
    assert git(world.repo, "status", "--porcelain", "--untracked-files=all") == ""


def test_a_hung_test_is_killed_at_the_timeout_and_exits_one(world):
    put(world.draft, "import time\n\n\ndef test_sc9_1_hangs():\n    time.sleep(60)\n")
    start = time.monotonic()
    run = prove(world, "--timeout", "3")
    assert time.monotonic() - start < 40
    assert run.out["red"]["red_ok"] is False
    assert run.out["red"]["summary"] == "timeout after 3s"
    assert run.code == 1


def test_usage_errors_exit_two(world):
    put(world.scratch / "bad.json", "{not json")
    bad = prove(world, "--mutations", str(world.scratch / "bad.json"))
    assert bad.code == 2
    assert "cannot read the mutations file" in bad.err


def test_a_crash_mid_mutation_still_restores_the_file(world, prove_mod, monkeypatch):
    fixed(world)
    before = digest(world.package)
    monkeypatch.chdir(world.repo)
    real = subprocess.run
    calls = []

    def crashing(argv, *args, **kwargs):
        if argv[0] == "git":
            return real(argv, *args, **kwargs)
        calls.append(1)
        if len(calls) == 2:
            assert digest(world.exported) != before
            raise RuntimeError("boom")
        return real(argv, *args, **kwargs)

    monkeypatch.setattr(prove_mod.subprocess, "run", crashing)
    argv = ["--scratch", str(world.scratch), "--test", TEST,
            *mutations(world, {"name": "drop-space", "file": "taskcontract/__init__.py",
                               "old": '"hello " + name', "new": '"hello" + name'})]
    with pytest.raises(RuntimeError):
        prove_mod.main(argv)
    assert len(calls) == 2
    assert digest(world.exported) == before


def test_a_pytest_that_never_starts_exits_254(world, prove_mod, monkeypatch):
    monkeypatch.chdir(world.repo)
    real = subprocess.run

    def no_python(argv, *args, **kwargs):
        if argv[0] == "git":
            return real(argv, *args, **kwargs)
        raise FileNotFoundError("no interpreter")

    monkeypatch.setattr(prove_mod.subprocess, "run", no_python)
    code = prove_mod.main(["--scratch", str(world.scratch), "--test", TEST])
    assert code == 254
