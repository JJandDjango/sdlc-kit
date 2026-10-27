"""Self-test for prove.py, on a toy `taskcontract` package.

run: python -m pytest tests/test_prove.py -q --tb=line

Each test builds a toy repo and a scratch folder under tmp_path and runs
prove.py with the toy repo as the working directory, as the drafter does.
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

PROVE = Path(__file__).resolve().parents[1] / "workflows" / "tools" / "prove.py"

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


@pytest.fixture
def world(tmp_path):
    repo = tmp_path / "repo"
    (repo / "taskcontract").mkdir(parents=True)
    (repo / "taskcontract" / "__init__.py").write_text(OLD + UNUSED, encoding="utf-8")
    scratch = tmp_path / "scratch"
    (scratch / "red").mkdir(parents=True)
    (scratch / "red" / "test_toy.py").write_text(DRAFT, encoding="utf-8")
    proto = scratch / "proto" / "taskcontract" / "__init__.py"
    return SimpleNamespace(repo=repo, scratch=scratch, proto=proto)


def prove(world, *args, test="test_toy.py"):
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
    path.write_text(json.dumps(list(items)), encoding="utf-8")
    return ["--mutations", str(path)]


def fixed(world):
    """Run once so proto exists, then do what the drafter does: make it pass."""
    prove(world)
    world.proto.write_text(NEW + UNUSED, encoding="utf-8")


@pytest.fixture
def prove_mod():
    spec = importlib.util.spec_from_file_location("prove_under_test", PROVE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_first_run_copies_the_package_and_reports_red_ok_green_not(world):
    run = prove(world, *mutations(
        world, {"name": "drop-space", "file": "taskcontract/__init__.py",
                "old": '"hello"', "new": '"hullo"'}))
    assert world.proto.is_file()
    assert run.out["red"]["red_ok"] is True
    assert run.out["green"]["green_ok"] is False
    assert run.out["mutations"].startswith("skipped")
    assert world.proto.read_text(encoding="utf-8") == OLD + UNUSED
    assert run.code == 1


def test_a_rerun_keeps_the_drafters_proto_edits_and_exits_zero(world):
    fixed(world)
    run = prove(world)
    assert world.proto.read_text(encoding="utf-8") == NEW + UNUSED
    assert run.out["green"]["green_ok"] is True
    assert run.code == 0


def test_green_names_the_proto_package_and_red_the_repo_package(world):
    fixed(world)
    run = prove(world)
    assert run.out["green"]["package"] == "proto/taskcontract/__init__.py"
    assert (world.scratch / run.out["green"]["package"]).resolve() == world.proto.resolve()
    assert run.out["green"]["proto_imported"] is True
    assert (world.scratch / run.out["red"]["package"]).resolve() == (
        world.repo / "taskcontract" / "__init__.py").resolve()


def test_caught_mutations_exit_zero_and_leave_proto_byte_for_byte(world):
    fixed(world)
    before = digest(world.proto)
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
    assert digest(world.proto) == before
    assert run.code == 0


def test_an_uncaught_mutation_reads_not_caught_and_exits_one(world):
    fixed(world)
    before = digest(world.proto)
    run = prove(world, *mutations(
        world, {"name": "unused", "file": "taskcontract/__init__.py",
                "old": "return 1", "new": "return 2"}))
    assert run.out["mutations"][0]["caught_by"] == "not caught"
    assert digest(world.proto) == before
    assert run.code == 1


def test_a_mutation_matching_zero_or_many_places_is_refused_untouched(world):
    fixed(world)
    before = digest(world.proto)
    run = prove(world, *mutations(
        world,
        {"name": "none", "file": "taskcontract/__init__.py", "old": "no such text", "new": "x"},
        {"name": "many", "file": "taskcontract/__init__.py", "old": "return", "new": "yield"}))
    refused = run.out["mutations"]
    assert [m["applied"] for m in refused] == [False, False]
    assert "matches 0" in refused[0]["error"] and "matches 2" in refused[1]["error"]
    assert digest(world.proto) == before
    assert run.code == 1


def test_a_mutation_path_outside_proto_is_refused(world):
    fixed(world)
    draft = world.scratch / "red" / "test_toy.py"
    before = digest(draft)
    run = prove(world, *mutations(
        world, {"name": "escape", "file": "../red/test_toy.py", "old": "import", "new": "mport"}))
    assert run.out["mutations"][0]["applied"] is False
    assert digest(draft) == before
    assert run.code == 1


def test_red_is_not_ok_when_a_test_passes_before_the_code_exists(world):
    (world.scratch / "red" / "test_toy.py").write_text(
        DRAFT + "\n\ndef test_sc1_9_passes_today():\n    assert taskcontract.unused() == 1\n",
        encoding="utf-8")
    run = prove(world)
    assert run.out["red"]["red_ok"] is False
    assert run.out["red"]["passed"] == ["test_sc1_9_passes_today"]
    assert run.code == 1


def test_red_is_not_ok_on_a_collection_error(world):
    (world.scratch / "red" / "test_toy.py").write_text(
        "import taskcontract.nope\n\n\ndef test_sc1_1_x():\n    assert True\n", encoding="utf-8")
    run = prove(world)
    assert run.out["red"]["red_ok"] is False
    assert run.out["red"]["not_assertion"][0]["kind"] == "error"
    assert run.code == 1


def test_red_is_not_ok_when_a_test_fails_on_an_exception_not_an_assertion(world):
    (world.scratch / "red" / "test_toy.py").write_text(
        "import taskcontract\n\n\ndef test_sc1_1_x():\n    taskcontract.nope()\n", encoding="utf-8")
    run = prove(world)
    assert run.out["red"]["red_ok"] is False
    bad = run.out["red"]["not_assertion"]
    assert [(b["id"], b["kind"]) for b in bad] == [("test_sc1_1_x", "AttributeError")]
    assert "nope" in bad[0]["line"]


def test_green_lists_each_failing_id_with_its_first_assertion_line_in_utf8(world):
    run = prove(world)
    failing = {f["id"]: f["line"] for f in run.out["green"]["failing"]}
    assert set(failing) == {"test_sc1_1_greets_by_name",
                            "test_sc1_2_greets_an_empty_name_with_a_space",
                            "test_sc1_3_keeps_accents"}
    assert "zoé" in failing["test_sc1_3_keeps_accents"]
    assert run.out["green"]["summary"].startswith("3 failed")


def test_stdout_is_one_compact_json_line_and_logs_hold_the_full_output(world):
    fixed(world)
    run = prove(world)
    assert run.text.count("\n") <= 1
    assert json.dumps(run.out, separators=(",", ":"), ensure_ascii=False) == run.text.strip()
    assert run.out["scratch"] == str(world.scratch.resolve())
    for key, tail in (("red", "3 failed"), ("green", "3 passed")):
        assert run.out[key]["log"] == f"logs/{key}.log"
        assert tail in (world.scratch / run.out[key]["log"]).read_text(encoding="utf-8")


def test_a_run_leaves_the_repo_tree_as_it_found_it(world):
    fixed(world)
    before = sorted(p.relative_to(world.repo).as_posix() for p in world.repo.rglob("*"))
    prove(world)
    assert sorted(p.relative_to(world.repo).as_posix() for p in world.repo.rglob("*")) == before


def test_a_hung_test_is_killed_at_the_timeout_and_exits_one(world):
    (world.scratch / "red" / "test_toy.py").write_text(
        "import time\n\n\ndef test_sc9_1_hangs():\n    time.sleep(60)\n", encoding="utf-8")
    start = time.monotonic()
    run = prove(world, "--timeout", "3")
    assert time.monotonic() - start < 40
    assert run.out["red"]["timeout"] is True
    assert run.code == 1


def test_usage_errors_exit_two(world):
    missing = prove(world, test="test_absent.py")
    assert missing.code == 2
    assert "test_absent.py" in missing.err
    (world.scratch / "bad.json").write_text("{not json", encoding="utf-8")
    bad = prove(world, "--mutations", str(world.scratch / "bad.json"))
    assert bad.code == 2


def test_a_crash_mid_mutation_still_restores_proto(world, prove_mod, monkeypatch, capsys):
    fixed(world)
    before = digest(world.proto)
    monkeypatch.chdir(world.repo)
    real = prove_mod.run_pytest
    calls = []

    def crashing(*args, **kwargs):
        calls.append(1)
        if len(calls) == 3:
            assert digest(world.proto) != before
            raise RuntimeError("boom")
        return real(*args, **kwargs)

    monkeypatch.setattr(prove_mod, "run_pytest", crashing)
    argv = ["--scratch", str(world.scratch), "--test", "test_toy.py",
            *mutations(world, {"name": "drop-space", "file": "taskcontract/__init__.py",
                               "old": '"hello " + name', "new": '"hello" + name'})]
    with pytest.raises(RuntimeError):
        prove_mod.main(argv)
    assert digest(world.proto) == before
    assert not (world.scratch / "logs" / "journal.json").exists()


def test_a_journal_left_by_a_killed_run_is_restored_before_anything_runs(world):
    fixed(world)
    logs = world.scratch / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "orig.bin").write_bytes((NEW + UNUSED).encode("utf-8"))
    (logs / "journal.json").write_text(json.dumps({"file": "taskcontract/__init__.py"}), encoding="utf-8")
    world.proto.write_text(OLD + UNUSED, encoding="utf-8")
    run = prove(world)
    assert run.out["recovered"] == ["taskcontract/__init__.py"]
    assert world.proto.read_text(encoding="utf-8") == NEW + UNUSED
    assert run.out["green"]["green_ok"] is True
    assert not (logs / "journal.json").exists()


def test_a_pytest_that_never_starts_exits_254(world, prove_mod, monkeypatch):
    monkeypatch.chdir(world.repo)

    def no_python(*args, **kwargs):
        raise FileNotFoundError("no interpreter")

    monkeypatch.setattr(prove_mod.subprocess, "run", no_python)
    code = prove_mod.main(["--scratch", str(world.scratch), "--test", "test_toy.py"])
    assert code == 254
