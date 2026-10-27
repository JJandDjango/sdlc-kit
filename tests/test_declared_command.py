"""Declared-command suite (contract: execution-team, unit e2-scripts, check SC2.1).

`workflows/tools/prove.py` and `receipts.py` run the test command the repository
declares in `.sdlc/config.yaml` (`test.command`, `test.file`, `test.build`), and
pytest only where it is declared. prove.py exports REV into SCRATCH/export/,
places the draft, runs the declared command, and leaves no prototype.

Each script runs as a subprocess beside the package the tests import, so a run
against a prototype runs the prototype's script. Every test builds its own git
repository under tmp_path and passes prove.py a --scratch under tmp_path: the kit
repository is never touched. Two fixture kinds: a pytest toy package, and a batch
file (test.bat on Windows, an executable test.sh elsewhere) whose exit code
depends on a file's text: BAD in it exits 1, ERR exits 2, anything else exits 0.
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

SCRIPTS = Path(taskcontract.__file__).resolve().parents[1] / "workflows" / "tools"
PROVE, RECEIPTS = SCRIPTS / "prove.py", SCRIPTS / "receipts.py"

EXT = "bat" if os.name == "nt" else "sh"
RUN, BUILD = f"test.{EXT}", f"build.{EXT}"
CHECK, NEW = "tests/check_one.txt", "tests/new_check.txt"
CHECK_BYTES = b"fine\n\xff\xfe\n"
PY = sys.executable

SCRIPT_TEXT = {
    "test.sh": '#!/bin/sh\necho "args: $*"\necho test >> trace.txt\nf="${1:-suite.txt}"\n'
               'if grep -q BAD "$f"; then\n  echo "test: FAILED"\n  exit 1\nfi\n'
               'if grep -q ERR "$f"; then\n  echo "test: ERROR"\n  exit 2\nfi\necho "test: ok"\n',
    "test.bat": "@echo off\necho args: %*\necho test>>trace.txt\nset F=%1\n"
                'if "%F%"=="" set F=suite.txt\nset F=%F:/=\\%\n'
                'findstr /c:BAD "%F%" >nul && (\n  echo test: FAILED\n  exit /b 1\n)\n'
                'findstr /c:ERR "%F%" >nul && (\n  echo test: ERROR\n  exit /b 2\n)\necho test: ok\n',
    "build.sh": '#!/bin/sh\necho build >> trace.txt\necho building\n',
    "build.bat": "@echo off\necho build>>trace.txt\necho building\n",
    "fail.sh": '#!/bin/sh\necho build >> trace.txt\necho boom\nexit 3\n',
    "fail.bat": "@echo off\necho build>>trace.txt\necho boom\nexit /b 3\n",
    "decoy.sh": "#!/bin/sh\necho decoy\nexit 5\n",
    "decoy.bat": "@echo off\necho decoy\nexit /b 5\n",
}
CALC = ("def add(a, b):\n    return a + b\n\n\ndef double(x):\n    return add(x, x) * 1\n\n\n"
        "def unused():\n    return 1\n")
CALC_TESTS = ("from toy import calc\n\n\ndef test_add():\n    assert calc.add(1, 2) == 3\n\n\n"
              "def test_double():\n    assert calc.double(2) == 4\n")
DRAFT_RED = ("from toy import calc\n\n\ndef test_new_one():\n    assert calc.add(2, 2) == 5\n\n\n"
             "def test_new_two():\n    assert calc.double(3) == 7\n")


# --- fixtures -----------------------------------------------------------------------

def git(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "-c", "core.autocrlf=false",
         "-c", "commit.gpgsign=false", *args],
        cwd=root, capture_output=True, encoding="utf-8", errors="replace", timeout=60)
    assert done.returncode == 0, done.stderr
    return done.stdout.strip()


def put(root: Path, rel: str, data) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = data if isinstance(data, bytes) else data.encode("utf-8")
    path.write_bytes(raw.replace(b"\n", b"\r\n") if rel.endswith(".bat") else raw)
    if rel.endswith(".sh"):
        path.chmod(0o755)


def commit(root: Path) -> None:
    git(root, "add", "-A")
    git(root, "commit", "-q", "--no-verify", "-m", "c")


def make_repo(tmp_path: Path, files: dict, test: dict | None) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    put(root, ".gitattributes", "* -text\n")
    if test is not None:
        put(root, ".sdlc/config.yaml", yaml.safe_dump({"test": test}))
    for rel, data in files.items():
        put(root, rel, data)
    commit(root)
    return root


def batch_repo(tmp_path, *, build=None, file=True, suite="fine\n", check=CHECK_BYTES, extra=None):
    files = {RUN: SCRIPT_TEXT[RUN], "suite.txt": suite, CHECK: check, "notes.txt": "plain\n"}
    test = {"command": [RUN]}
    if file:
        test["file"] = [RUN, "{file}"]
    if build:
        files[BUILD] = SCRIPT_TEXT[f"fail.{EXT}" if build == "fail" else BUILD]
        test["build"] = [BUILD]
    return make_repo(tmp_path, {**files, **(extra or {})}, test)


def pytest_repo(tmp_path, test=None, extra=None):
    test = test or {"command": [PY, "-m", "pytest", "tests", "-q"],
                    "file": [PY, "-m", "pytest", "{file}", "-q"]}
    files = {"toy/__init__.py": "", "toy/calc.py": CALC, "tests/test_calc.py": CALC_TESTS}
    return make_repo(tmp_path, {**files, **(extra or {})}, test)


def draft(scratch: Path, rel: str, text: str) -> None:
    put(scratch / "draft", rel, text)


def mutations(tmp_path: Path, *items: tuple) -> str:
    path = tmp_path / "mutations.json"
    path.write_text(json.dumps([dict(zip(("name", "file", "old", "new"), item)) for item in items]),
                    encoding="utf-8")
    return str(path)


class Run:
    def __init__(self, done):
        self.code, self.text, self.err = done.returncode, done.stdout, done.stderr

    @property
    def out(self) -> dict:
        assert self.text.strip(), f"no JSON on stdout (exit {self.code}): {self.err}"
        return json.loads(self.text)


def run_script(script: Path, args, cwd: Path, env=None) -> Run:
    done = subprocess.run([PY, str(script), *map(str, args)], cwd=cwd, env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=300)
    return Run(done)


def prove(root: Path, scratch: Path, *args, path: str = CHECK, env=None) -> Run:
    return run_script(PROVE, ["--scratch", scratch, "--test", path, *args], root, env)


def receipts(root: Path, tmp_path: Path, *argvs, env=None) -> Run:
    (tmp_path / "receipts.json").write_text(json.dumps(list(argvs)), encoding="utf-8")
    return run_script(RECEIPTS, ["--repo", root, "--receipts", tmp_path / "receipts.json",
                                 "--out", tmp_path / "out"], tmp_path, env)


def keys_of(node):
    if isinstance(node, dict):
        for key, value in node.items():
            yield key
            yield from keys_of(value)
    elif isinstance(node, list):
        for value in node:
            yield from keys_of(value)


def assert_no_prototype(out: dict, scratch: Path) -> None:
    assert set(keys_of(out)).isdisjoint({"green", "proto_imported", "package"})
    assert not (scratch / "proto").exists()


def arg_line(log: Path) -> str:
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("args:"):
            return line[5:].strip()
    raise AssertionError(f"no args line in {log}")


def trace(scratch: Path) -> list[str]:
    return (scratch / "export" / "trace.txt").read_text(encoding="utf-8").split()


# --- prove-red, batch file ------------------------------------------------------------

def test_sc2_1_prove_red_batch_runs_the_file_command_with_path(tmp_path):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    draft(scratch, NEW, "BAD\n")
    run = prove(root, scratch, path=NEW)
    out = run.out
    assert run.code == 0, run.err
    assert set(out) == {"ok", "scratch", "red"} and out["ok"] is True
    assert Path(out["scratch"]).resolve() == scratch.resolve()
    assert out["red"]["red_ok"] is True and out["red"]["summary"] == "test: FAILED"
    assert out["red"]["log"] == "logs/red.log"
    assert arg_line(scratch / "logs" / "red.log") == NEW
    assert_no_prototype(out, scratch)


def test_sc2_1_prove_red_batch_runs_the_build_before_the_file_command(tmp_path):
    root, scratch = batch_repo(tmp_path, build="ok"), tmp_path / "scratch"
    draft(scratch, NEW, "BAD\n")
    run = prove(root, scratch, path=NEW)
    assert run.out["red"]["red_ok"] is True, run.err
    assert trace(scratch) == ["build", "test"]
    assert "building" in (scratch / "logs" / "build.log").read_text(encoding="utf-8")


def test_sc2_1_prove_red_a_failed_build_is_not_red_and_names_the_build(tmp_path):
    root, scratch = batch_repo(tmp_path, build="fail"), tmp_path / "scratch"
    draft(scratch, NEW, "BAD\n")
    run = prove(root, scratch, path=NEW)
    assert run.out["red"]["summary"] == "build: exit 3: boom"
    assert run.out["red"]["red_ok"] is False and run.out["ok"] is False and run.code == 1
    assert trace(scratch) == ["build"]
    assert "boom" in (scratch / "logs" / "build.log").read_text(encoding="utf-8")


def test_sc2_1_prove_red_batch_without_a_file_runs_the_command(tmp_path):
    root, scratch = batch_repo(tmp_path, file=False, suite="BAD\n"), tmp_path / "scratch"
    run = prove(root, scratch)
    assert run.out["red"]["red_ok"] is True and run.out["red"]["summary"] == "test: FAILED", run.err
    assert arg_line(scratch / "logs" / "red.log") == ""
    assert trace(scratch) == ["test"]


@pytest.mark.parametrize("text, red_ok, last", [
    ("BAD\n", True, "test: FAILED"), ("fine\n", False, "test: ok"), ("ERR\n", False, "test: ERROR")],
    ids=["exit-1-is-red", "exit-0-is-not-red", "exit-2-is-not-red"])
def test_sc2_1_prove_red_batch_is_red_only_on_exit_1(tmp_path, text, red_ok, last):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    draft(scratch, NEW, text)
    run = prove(root, scratch, path=NEW)
    assert run.out["red"]["summary"] == last, run.err
    assert run.out["red"]["red_ok"] is red_ok and run.out["ok"] is red_ok
    assert run.code == (0 if red_ok else 1)


# --- prove-red, pytest ----------------------------------------------------------------

def test_sc2_1_prove_red_pytest_runs_the_file_command_and_reads_each_test(tmp_path):
    root, scratch = pytest_repo(tmp_path), tmp_path / "scratch"
    draft(scratch, "tests/test_new.py", DRAFT_RED)
    run = prove(root, scratch, path="tests/test_new.py")
    red = run.out["red"]
    assert run.code == 0, run.err
    assert red["red_ok"] is True and re.fullmatch(r"2 failed in [\d.]+s", red["summary"])
    assert red["log"] == "logs/red.log" and "passed" not in red
    assert_no_prototype(run.out, scratch)


def test_sc2_1_prove_red_pytest_without_a_file_runs_the_command(tmp_path):
    test = {"command": [PY, "-m", "pytest", "tests/test_new.py", "-q"]}
    root, scratch = pytest_repo(tmp_path, test), tmp_path / "scratch"
    draft(scratch, "tests/test_new.py", DRAFT_RED)
    run = prove(root, scratch, path="tests/test_new.py")
    assert run.out["red"]["red_ok"] is True, run.err
    assert re.fullmatch(r"2 failed in [\d.]+s", run.out["red"]["summary"])


@pytest.mark.parametrize("text, red_ok, passed", [
    (DRAFT_RED, True, None),
    (DRAFT_RED + "\n\ndef test_passes():\n    assert calc.add(1, 1) == 2\n", False, ["test_passes"]),
    (DRAFT_RED + "\n\ndef test_raises():\n    calc.nope()\n", False, None)],
    ids=["every-test-fails-on-an-assertion", "a-test-passes", "a-test-fails-on-an-exception"])
def test_sc2_1_prove_red_pytest_is_red_only_when_every_test_fails_on_an_assertion(
        tmp_path, text, red_ok, passed):
    root, scratch = pytest_repo(tmp_path), tmp_path / "scratch"
    draft(scratch, "tests/test_new.py", text)
    run = prove(root, scratch, path="tests/test_new.py")
    assert run.out["red"]["red_ok"] is red_ok, run.err
    assert run.out["red"].get("passed") == passed
    assert run.code == (0 if red_ok else 1)


def test_sc2_1_prove_red_exits_254_when_the_declared_command_never_starts(tmp_path):
    test = {"command": [RUN], "file": ["no-such-program-xyz", "{file}"]}
    root, scratch = make_repo(tmp_path, {RUN: SCRIPT_TEXT[RUN], CHECK: "x\n"}, test), tmp_path / "scratch"
    run = prove(root, scratch)
    assert run.code == 254 and run.text.strip() == ""
    message = run.err.strip().splitlines()[-1]
    assert message.startswith("prove.py: the test command did not start")
    assert "no-such-program-xyz" in message


# --- prove.py: root, REV, draft, export -----------------------------------------------

@pytest.mark.parametrize("test", [None, {"file": ["{file}"]}], ids=["no-config", "no-command"])
def test_sc2_1_prove_with_no_declared_command_exits_2(tmp_path, test):
    root, scratch = make_repo(tmp_path, {CHECK: "x\n"}, test), tmp_path / "scratch"
    run = prove(root, scratch)
    assert run.err.strip() == "prove.py: the repository declares no test command"
    assert run.code == 2 and run.text.strip() == ""


def test_sc2_1_prove_a_rev_that_is_not_a_commit_exits_2(tmp_path):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    run = prove(root, scratch, "--at", "no-such-rev")
    head, _, tail = run.err.strip().partition(" is not a commit in ")
    assert head == "prove.py: no-such-rev" and Path(tail).resolve() == root.resolve(), run.err
    assert run.code == 2 and run.text.strip() == ""


def test_sc2_1_prove_a_root_that_is_no_git_repository_exits_2(tmp_path):
    plain, scratch = tmp_path / "plain", tmp_path / "scratch"
    put(plain, ".sdlc/config.yaml", yaml.safe_dump({"test": {"command": [RUN]}}))
    draft(scratch, CHECK, "BAD\n")
    run = prove(plain, scratch)
    head, _, tail = run.err.strip().partition(" ")
    assert head == "prove.py:" and tail.endswith(" is not a git repository"), run.err
    assert Path(tail[:-len(" is not a git repository")]).resolve() == plain.resolve()
    assert run.code == 2 and run.text.strip() == ""


def test_sc2_1_prove_exports_rev_afresh_each_run(tmp_path):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    draft(scratch, NEW, "BAD\n")
    assert prove(root, scratch, path=NEW).out["red"]["red_ok"] is True
    (scratch / "export" / "stale.txt").write_text("left by the first run", encoding="utf-8")
    run = prove(root, scratch, path=NEW)
    assert run.out["red"]["red_ok"] is True, run.err
    assert not (scratch / "export" / "stale.txt").exists()
    assert trace(scratch) == ["test"]


def test_sc2_1_prove_at_rev_runs_that_commit_not_the_working_tree(tmp_path):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    put(root, CHECK, "BAD\n")
    commit(root)
    put(root, CHECK, "fine\n")
    assert prove(root, scratch).out["red"]["summary"] == "test: FAILED"
    older = prove(root, scratch, "--at", "HEAD~1")
    assert older.out["red"]["summary"] == "test: ok" and older.out["red"]["red_ok"] is False


def test_sc2_1_prove_places_the_draft_over_the_committed_file_and_leaves_the_tree_alone(tmp_path):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    draft(scratch, CHECK, "BAD\n")
    run = prove(root, scratch)
    assert run.out["red"]["red_ok"] is True, run.err
    assert (scratch / "export" / CHECK).read_bytes() == b"BAD\n"
    assert (root / CHECK).read_bytes() == CHECK_BYTES
    assert git(root, "status", "--porcelain", "--untracked-files=all") == ""


def test_sc2_1_prove_runs_the_committed_file_when_there_is_no_draft(tmp_path):
    root, scratch = batch_repo(tmp_path, check="BAD\n"), tmp_path / "scratch"
    run = prove(root, scratch)
    assert run.out["red"]["red_ok"] is True, run.err
    assert arg_line(scratch / "logs" / "red.log") == CHECK


def test_sc2_1_prove_with_no_draft_and_no_committed_file_exits_2(tmp_path):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    run = prove(root, scratch, path="tests/none.txt")
    head, _, tail = run.err.strip().partition("prove.py: no draft at ")
    where, _, after = tail.partition(" and no ")
    assert head == "" and after == "tests/none.txt at HEAD", run.err
    assert Path(where) == scratch.resolve() / "draft" / "tests" / "none.txt"
    assert run.code == 2 and run.text.strip() == ""


@pytest.mark.parametrize("bad", ["ABS", "../x.txt", "tests/../../x.txt"], ids=["absolute", "up", "inner-up"])
def test_sc2_1_prove_a_path_outside_the_repository_is_a_usage_error(tmp_path, bad):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    bad = str(tmp_path / "x.txt") if bad == "ABS" else bad
    run = prove(root, scratch, path=bad)
    assert run.err.strip() == f"prove.py: --test {bad} is not a path inside the repository"
    assert run.code == 2 and run.text.strip() == ""


# --- two-key: mutations through the declared command ----------------------------------

CALC_FILE = "toy/calc.py"
ADD = ("add subtracts", CALC_FILE, "return a + b", "return a - b")
DOUBLE = ("double triples", CALC_FILE, "return add(x, x) * 1", "return add(x, x) * 3")
UNUSED = ("unused returns 2", CALC_FILE, "return 1\n", "return 2\n")


def test_sc2_1_two_key_pytest_caught_by_lists_the_failing_test_ids(tmp_path):
    root, scratch = pytest_repo(tmp_path), tmp_path / "scratch"
    run = prove(root, scratch, "--mutations", mutations(tmp_path, ADD, DOUBLE),
                path="tests/test_calc.py")
    out = run.out
    assert run.code == 0, run.err
    assert set(out) == {"ok", "scratch", "mutations"} and out["ok"] is True
    first, second = out["mutations"]
    assert set(first["caught_by"]) == {"test_add", "test_double"} and first["caught_count"] == 2
    assert {k: first[k] for k in ("name", "applied", "log")} == {
        "name": "add subtracts", "applied": True, "log": "logs/mutation-1.log"}
    assert second == {"name": "double triples", "applied": True, "caught_by": ["test_double"],
                      "caught_count": 1, "log": "logs/mutation-2.log"}
    assert (scratch / "logs" / "baseline.log").is_file()
    assert (scratch / "export" / CALC_FILE).read_bytes() == (root / CALC_FILE).read_bytes()
    assert_no_prototype(out, scratch)


def test_sc2_1_two_key_pytest_an_uncaught_mutation_reads_not_caught_and_exits_1(tmp_path):
    root, scratch = pytest_repo(tmp_path), tmp_path / "scratch"
    run = prove(root, scratch, "--mutations", mutations(tmp_path, ADD, UNUSED),
                path="tests/test_calc.py")
    assert run.code == 1 and run.out["ok"] is False, run.err
    assert run.out["mutations"][1] == {"name": "unused returns 2", "applied": True,
                                       "caught_by": "not caught", "log": "logs/mutation-2.log"}
    assert "test_add" in run.out["mutations"][0]["caught_by"]


@pytest.mark.parametrize("old, count", [("return z", 0), ("return", 3)], ids=["no-place", "three-places"])
def test_sc2_1_two_key_an_old_text_that_does_not_match_one_place_is_not_applied(tmp_path, old, count):
    root, scratch = pytest_repo(tmp_path), tmp_path / "scratch"
    run = prove(root, scratch, "--mutations", mutations(tmp_path, ("bad old", CALC_FILE, old, "x")),
                path="tests/test_calc.py")
    assert run.out["mutations"] == [{"name": "bad old", "applied": False,
                                     "error": f"old matches {count} places, not 1"}], run.err
    assert run.code == 1 and run.out["ok"] is False


def test_sc2_1_two_key_batch_caught_by_lists_path_and_each_file_is_restored(tmp_path):
    root, scratch = batch_repo(tmp_path, build="ok"), tmp_path / "scratch"
    run = prove(root, scratch, "--mutations", mutations(
        tmp_path, ("check fails", CHECK, "fine", "BAD"), ("check errors", CHECK, "fine", "ERR")))
    out = run.out
    assert run.code == 0, run.err
    assert set(out) == {"ok", "scratch", "mutations"} and out["ok"] is True
    assert out["mutations"] == [
        {"name": "check fails", "applied": True, "caught_by": [CHECK], "caught_count": 1,
         "log": "logs/mutation-1.log"},
        {"name": "check errors", "applied": True, "caught_by": [CHECK], "caught_count": 1,
         "log": "logs/mutation-2.log"}]
    assert (scratch / "export" / CHECK).read_bytes() == CHECK_BYTES
    assert trace(scratch) == ["build", "test"] * 3
    assert (scratch / "logs" / "baseline.log").is_file()
    assert_no_prototype(out, scratch)


def test_sc2_1_two_key_batch_an_uncaught_mutation_reads_not_caught_and_exits_1(tmp_path):
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    run = prove(root, scratch, "--mutations", mutations(tmp_path, ("notes change", "notes.txt", "plain", "mixed")))
    assert run.out["mutations"] == [{"name": "notes change", "applied": True,
                                     "caught_by": "not caught", "log": "logs/mutation-1.log"}], run.err
    assert run.code == 1 and run.out["ok"] is False


def test_sc2_1_two_key_skips_the_mutations_when_the_tests_fail_at_rev(tmp_path):
    root, scratch = batch_repo(tmp_path, check="BAD\n"), tmp_path / "scratch"
    sha = git(root, "rev-parse", "--short", "HEAD")
    run = prove(root, scratch, "--at", sha, "--mutations",
                mutations(tmp_path, ("notes change", "notes.txt", "plain", "mixed")))
    assert run.out == {"ok": False, "scratch": run.out["scratch"],
                       "mutations": f"skipped: the tests do not pass at {sha}"}, run.err
    assert run.code == 1


# --- receipts.py: the declared command as a receipt -----------------------------------

@pytest.mark.parametrize("suite, code, key", [("fine\n", 0, "test: ok"), ("BAD\n", 1, "test: FAILED")],
                         ids=["green", "red"])
def test_sc2_1_receipts_runs_the_declared_command_from_the_repository(tmp_path, suite, code, key):
    root = batch_repo(tmp_path, suite=suite)
    run = receipts(root, tmp_path, [RUN])
    record = run.out["commands"][0]
    assert (record["exit_code"], record["key_output"], record["command"]) == (code, key, RUN), run.err
    assert run.code == code and run.out["ok"] is (code == 0)


def test_sc2_1_receipts_keeps_the_pytest_summary_beside_a_batch_command(tmp_path):
    root = pytest_repo(tmp_path, extra={RUN: SCRIPT_TEXT[RUN], "suite.txt": "fine\n"})
    run = receipts(root, tmp_path, [RUN], [PY, "-m", "pytest", "tests", "-q"])
    batch, pytest_record = run.out["commands"]
    assert batch["key_output"] == "test: ok", run.err
    assert re.fullmatch(r"2 passed in [\d.]+s", pytest_record["key_output"])
    assert run.code == 0


# --- pytest only where it is declared, and the repository's file before PATH ----------

def test_sc2_1_a_batch_repository_never_collects_its_pytest_file(tmp_path):
    marker = tmp_path / "marker.txt"
    collected = f"from pathlib import Path\nPath({str(marker)!r}).write_text('collected')\n\n\ndef test_m():\n    assert True\n"
    root = batch_repo(tmp_path, extra={"tests/test_marker.py": collected})
    scratch = tmp_path / "scratch"
    draft(scratch, NEW, "BAD\n")
    assert prove(root, scratch, path=NEW).out["red"]["red_ok"] is True
    caught = prove(root, scratch, "--mutations", mutations(tmp_path, ("check fails", CHECK, "fine", "BAD")))
    assert caught.out["mutations"][0]["caught_by"] == [CHECK]
    assert receipts(root, tmp_path, [RUN]).out["commands"][0]["key_output"] == "test: ok"
    assert not marker.exists()


@pytest.mark.parametrize("tool", ["prove", "receipts"])
def test_sc2_1_an_argv0_naming_a_repository_file_resolves_there_before_path(tmp_path, tool):
    decoy = tmp_path / "decoy"
    put(decoy, RUN, SCRIPT_TEXT[f"decoy.{EXT}"])
    env = dict(os.environ, PATH=str(decoy) + os.pathsep + os.environ.get("PATH", ""))
    root, scratch = batch_repo(tmp_path), tmp_path / "scratch"
    if tool == "prove":
        draft(scratch, NEW, "BAD\n")
        assert prove(root, scratch, path=NEW, env=env).out["red"]["summary"] == "test: FAILED"
    else:
        assert receipts(root, tmp_path, [RUN], env=env).out["commands"][0]["key_output"] == "test: ok"
