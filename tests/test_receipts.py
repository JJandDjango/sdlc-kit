"""Self-test for receipts.py, on a toy git repository.

run: python -m pytest tests/test_receipts.py -q --tb=line

Each test builds a toy repo under tmp_path and runs receipts.py with another
folder as the working directory, so only --repo can place the commands. The
environment lacks PYTHONUTF8 on purpose: receipts.py sets it for its commands.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

RECEIPTS = Path(__file__).resolve().parents[1] / "workflows" / "tools" / "receipts.py"

CHILD = ("import sys, time\n"
         "for _ in range(150):\n"
         "    open(sys.argv[1], 'w').write(str(time.time()))\n"
         "    time.sleep(0.2)\n")
PARENT = ("import subprocess, sys, time; "
          f"subprocess.Popen([sys.executable, '-c', {CHILD!r}, sys.argv[1]]); "
          "time.sleep(60)")
STAMP = ("import sys, time\n"
         "with open(sys.argv[1], 'a') as f:\n"
         "    f.write(sys.argv[2] + '-start\\n'); f.flush()\n"
         "    time.sleep(0.4)\n"
         "    f.write(sys.argv[2] + '-end\\n')\n")
TOY_TESTS = '''def test_a_ok():
    assert 1 == 1


def test_b_bad():
    assert "ab" == "ac", "b differs"


def test_c_bad():
    assert 1 + 1 == 3
'''
MANY_TESTS = '''import pytest


@pytest.mark.parametrize("n", range(12))
def test_f(n):
    assert n < 0
'''


def py(code: str, *args: str) -> list[str]:
    return [sys.executable, "-c", code, *args]


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=repo, capture_output=True, timeout=60)
    assert done.returncode == 0, done.stderr.decode("utf-8", "replace")
    return done.stdout.decode("utf-8", "replace").strip()


@pytest.fixture
def world(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "toy@example.com")
    git(repo, "config", "user.name", "Toy")
    git(repo, "config", "commit.gpgsign", "false")
    (repo / "tracked.txt").write_text("one\n", encoding="utf-8")
    git(repo, "add", "tracked.txt")
    git(repo, "commit", "-q", "--no-verify", "-m", "toy")
    return SimpleNamespace(repo=repo, out=tmp_path / "out", tmp=tmp_path)


def receipts(world, *commands, extra=(), raw=None, repo=None):
    """Run receipts.py on a list of argv lists (or the raw text of the file)."""
    assert RECEIPTS.is_file(), "receipts.py is missing"
    path = world.tmp / "receipts.json"
    path.write_text(raw if raw is not None else json.dumps(list(commands)), encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k != "PYTHONUTF8"}
    began = time.monotonic()
    done = subprocess.run(
        [sys.executable, str(RECEIPTS), "--repo", str(repo or world.repo),
         "--receipts", str(path), "--out", str(world.out), *extra],
        cwd=world.tmp, env=env, capture_output=True, timeout=300)
    text = done.stdout.decode("utf-8")
    return SimpleNamespace(code=done.returncode, text=text, seconds=time.monotonic() - began,
                           out=json.loads(text) if text.strip() else None,
                           err=done.stderr.decode("utf-8", "replace"))


def test_all_pass_prints_the_state_and_each_exit_code_and_exits_zero(world):
    run = receipts(world, py("print('first')"), py("print('second')"))
    assert run.code == 0
    assert run.out["head"] == git(world.repo, "rev-parse", "--short", "HEAD")
    assert run.out["branch"] == git(world.repo, "branch", "--show-current")
    assert run.out["working_tree_clean_of_tracked_changes"] is True
    assert [(c["exit_code"], c["key_output"]) for c in run.out["commands"]] == [
        (0, "first"), (0, "second")]
    assert "first" in run.out["commands"][0]["command"]


def test_the_json_on_stdout_is_also_written_to_result_json(world):
    run = receipts(world, py("print('first')"))
    assert (world.out / "result.json").read_text(encoding="utf-8").strip() == run.text.strip()


def test_a_nonzero_exit_is_read_not_inferred_and_later_commands_still_run(world):
    run = receipts(world, py("import sys; print('1 passed in 0.01s'); sys.exit(4)"),
                   py("print('after')"))
    assert [c["exit_code"] for c in run.out["commands"]] == [4, 0]
    assert run.out["commands"][0]["key_output"] == "1 passed in 0.01s"
    assert run.out["commands"][1]["key_output"] == "after"
    assert run.code == 1


def test_a_command_past_its_timeout_is_killed_and_reads_124(world):
    run = receipts(world, py("import time; time.sleep(60)"), extra=("--timeout", "2"))
    command = run.out["commands"][0]
    assert command["exit_code"] == 124
    assert "timeout" in command["key_output"]
    assert run.seconds < 40
    assert run.code == 1


def test_a_timeout_kills_the_commands_children_too(world):
    beat = world.tmp / "beat.txt"
    run = receipts(world, py(PARENT, str(beat)), extra=("--timeout", "3"))
    assert run.out["commands"][0]["exit_code"] == 124
    assert beat.is_file()
    before = beat.read_text(encoding="utf-8")
    time.sleep(1.5)
    assert beat.read_text(encoding="utf-8") == before


def test_a_command_that_never_starts_reads_254_and_the_rest_still_run(world):
    run = receipts(world, ["no-such-tool-xyz-receipts", "--version"], py("print('after')"))
    first, second = run.out["commands"]
    assert first["exit_code"] == 254
    assert "not found" in first["key_output"]
    assert second["exit_code"] == 0
    assert run.code == 1


def test_a_pytest_command_gives_the_summary_and_each_failing_id_with_its_first_line(world):
    folder = world.repo / "toy_tests"
    folder.mkdir()
    (folder / "test_toy.py").write_text(TOY_TESTS, encoding="utf-8")
    run = receipts(world, [sys.executable, "-m", "pytest", "toy_tests", "-q",
                           "-p", "no:cacheprovider"])
    command = run.out["commands"][0]
    key = command["key_output"]
    assert command["exit_code"] == 1
    assert "2 failed, 1 passed" in key
    assert any("test_b_bad" in line and "b differs" in line for line in key.splitlines())
    assert any("test_c_bad" in line and "assert" in line for line in key.splitlines())
    assert "def test_" not in key
    assert len(key.splitlines()) <= 4
    assert "def test_b_bad" in (world.out / command["log"]).read_text(encoding="utf-8")
    assert run.code == 1


def test_a_pytest_command_on_xdist_workers_gives_the_same_summary_and_failing_ids(world):
    pytest.importorskip("xdist")
    folder = world.repo / "toy_tests"
    folder.mkdir()
    (folder / "test_toy.py").write_text(TOY_TESTS, encoding="utf-8")
    run = receipts(world, [sys.executable, "-m", "pytest", "toy_tests", "-q", "-n", "2",
                           "-p", "no:cacheprovider"])
    key = run.out["commands"][0]["key_output"]
    assert run.out["commands"][0]["exit_code"] == 1
    assert "2 failed, 1 passed" in key
    assert any("test_b_bad" in line and "b differs" in line for line in key.splitlines())
    assert any("test_c_bad" in line and "assert" in line for line in key.splitlines())
    assert len(key.splitlines()) <= 4


def test_many_failing_ids_are_capped_with_a_count_of_the_rest(world):
    folder = world.repo / "toy_tests"
    folder.mkdir()
    (folder / "test_many.py").write_text(MANY_TESTS, encoding="utf-8")
    run = receipts(world, [sys.executable, "-m", "pytest", "toy_tests", "-q",
                           "-p", "no:cacheprovider"])
    key = run.out["commands"][0]["key_output"]
    assert "12 failed" in key
    assert sum(1 for line in key.splitlines() if line.startswith("FAILED")) == 10
    assert "+2 more in the log" in key


def test_a_modified_tracked_file_reads_not_clean(world):
    (world.repo / "tracked.txt").write_text("two\n", encoding="utf-8")
    run = receipts(world, py("print('ok')"))
    assert run.out["working_tree_clean_of_tracked_changes"] is False
    assert run.code == 0


def test_an_untracked_file_is_ignored(world):
    (world.repo / "scratch.txt").write_text("loose\n", encoding="utf-8")
    run = receipts(world, py("print('ok')"))
    assert run.out["working_tree_clean_of_tracked_changes"] is True


def test_the_state_is_taken_before_the_first_command_runs(world):
    run = receipts(world, py("open('tracked.txt', 'a').write('x')"))
    assert run.out["working_tree_clean_of_tracked_changes"] is True
    assert (world.repo / "tracked.txt").read_text(encoding="utf-8") == "one\nx"


@pytest.mark.parametrize("raw", [
    json.dumps(["python -c print(1)"]),
    json.dumps([]),
    json.dumps([[]]),
    json.dumps([[1]]),
    json.dumps({"cmd": ["python"]}),
    "not json",
])
def test_anything_but_a_list_of_argv_lists_is_refused_and_nothing_runs(world, raw):
    run = receipts(world, raw=raw)
    assert run.code == 2
    assert "receipts.py:" in run.err
    assert not (world.out / "logs").exists()


def test_a_string_entry_is_refused_naming_the_argv_list(world):
    run = receipts(world, raw=json.dumps(["python -c print(1) | more"]))
    assert run.code == 2
    assert "argv" in run.err


def test_a_folder_that_is_no_git_repo_is_refused(world):
    plain = world.tmp / "plain"
    plain.mkdir()
    run = receipts(world, py("print('ok')"), repo=plain)
    assert run.code == 2
    assert not (world.out / "logs").exists()


def test_commands_run_in_order_one_at_a_time_from_the_repo_root(world):
    mark = world.tmp / "marks.txt"
    run = receipts(world, py(STAMP, str(mark), "a"), py(STAMP, str(mark), "b"),
                   py("import os; print(os.getcwd())"))
    assert mark.read_text(encoding="utf-8").split() == ["a-start", "a-end", "b-start", "b-end"]
    assert Path(run.out["commands"][2]["key_output"]).resolve() == world.repo.resolve()


def test_the_alive_marker_exists_while_the_first_command_runs(world):
    alive = world.out / "alive"
    check = "import sys, pathlib; sys.exit(0 if pathlib.Path(sys.argv[1]).is_file() else 6)"
    run = receipts(world, py(check, str(alive)))
    assert run.out["commands"][0]["exit_code"] == 0
    assert isinstance(json.loads(alive.read_text(encoding="utf-8"))["pid"], int)


def test_progress_json_is_updated_after_each_command(world):
    progress = world.out / "progress.json"
    check = ("import json, sys\n"
             "d = json.load(open(sys.argv[1], encoding='utf-8'))\n"
             "sys.exit(0 if d['done'] == 1 and d['total'] == 2 else 5)")
    run = receipts(world, py("print('one')"), py(check, str(progress)))
    assert [c["exit_code"] for c in run.out["commands"]] == [0, 0]
    final = json.loads(progress.read_text(encoding="utf-8"))
    assert (final["done"], final["total"], final["finished"]) == (2, 2, True)


def test_each_commands_full_output_goes_to_its_own_log_and_stderr_is_in_it(world):
    run = receipts(world, py("import sys; sys.stderr.write('warn line\\n')"),
                   py("print('plain')"))
    first, second = run.out["commands"]
    assert first["log"] == "logs/1.log" and second["log"] == "logs/2.log"
    assert first["key_output"] == "warn line"
    assert "warn line" in (world.out / first["log"]).read_text(encoding="utf-8")


def test_utf8_output_survives_a_console_code_page_and_bad_bytes_do_not_crash(world):
    run = receipts(world, py("print(chr(0x2713) + ' done')"),
                   py("import sys; sys.stdout.buffer.write(b'caf' + bytes([0xe9]) + b' bad\\n')"))
    first, second = run.out["commands"]
    assert (first["exit_code"], first["key_output"]) == (0, chr(0x2713) + " done")
    assert second["exit_code"] == 0
    assert second["key_output"].startswith("caf") and second["key_output"].endswith(" bad")
