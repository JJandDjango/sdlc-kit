"""Wall passes suite (contract: execution-team, unit e3-wall; backlog Next actions 13 and 15).

tests/test_wall.py pins the wall's refusals and stays as it is. This file pins the
two passes that file never drew:

* Next actions 13: a Bash call whose words equal the repository's declared
  `test.command`, or its declared `test.build`, passes for the Developer and for QA,
  though the command names a walled folder. Any other word list is held as before.
* Next actions 15: the hook holds only a call whose input carries an `agent_id` (a
  workflow member's call does; the session's own call carries neither `agent_id` nor
  `agent_type`, as a probe in session 133 measured).
  A call with no `agent_id` key, or a null one, passes; any other value is held.

The hook runs as a subprocess the way Claude Code runs a PreToolUse hook: one JSON event
on stdin. Every test builds its own git repository under tmp_path, with its own
`.sdlc/config.yaml` and its own task file. Every event that should be held carries an
`agent_id`, so each old refusal still proves the wall holds members.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import taskcontract

PLUGIN = Path(taskcontract.__file__).resolve().parents[1]
WALL = PLUGIN / "hooks" / "wall.py"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
NT = os.name == "nt"

MEMBER = {"agent_id": "a28a6f45e23166402", "agent_type": "workflow-subagent"}

# The Developer's repository: the kit's own shape, a command that names the walled folder.
DEV_CONFIG = """\
test:
  command: [python, -P, -m, pytest, tests, -q, -n, auto]
  file: [python, -P, -m, pytest, "{file}", -q]
  build: [python, tools/build.py, tests/]
wall:
  functional: [tests/]
"""
DEV_COMMAND = "python -P -m pytest tests -q -n auto"
DEV_BUILD = "python tools/build.py tests/"

# QA's repository: a unit folder and a code folder that the declared commands name.
QA_CONFIG = """\
test:
  command: [python, -m, pytest, tests/unit, engine/core.py, -q]
  build: [python, tools/build.py, engine/]
wall:
  functional: [tests/functional/]
  unit: [tests/unit/]
  code: [engine/]
  interface: [engine/types.py]
"""
QA_COMMAND = "python -m pytest tests/unit engine/core.py -q"
QA_BUILD = "python tools/build.py engine/"

DEV_LINE = "Task green: Developer reads no functional test: {}"
QA_UNIT_LINE = "Task write-tests: QA reads no unit test: {}"
QA_BODY_LINE = "Task write-tests: QA reads no implementation body: {}"

PASS = (0, "", "")


def refusal(line: str) -> tuple[int, str, str]:
    """What a held call gives: exit 2, nothing on stdout, the line on stderr."""
    return (2, "", line + "\n")


def run_hook(stdin: str, tmp_path: Path):
    """(exit code, stdout, stderr) of the hook fed `stdin`, run from a folder that is
    not the repository and with no git repository above the fixtures."""
    work = tmp_path / "cwd"
    work.mkdir(exist_ok=True)
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1"}
    done = subprocess.run([sys.executable, str(WALL)], input=stdin, cwd=work, env=env,
                          capture_output=True, encoding="utf-8", errors="replace",
                          timeout=100, creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


class Fx:
    """<tmp>/<name>: a git repository, a config, and a task file naming an operator."""

    def __init__(self, tmp_path: Path, config: str | None = DEV_CONFIG,
                 operator: str | None = "developer", task: str = "green",
                 name: str = "repo"):
        self.tmp_path = tmp_path
        self.root = tmp_path / name
        self.root.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True, capture_output=True,
                       creationflags=NO_WINDOW)
        if config is not None:
            (self.root / ".sdlc").mkdir()
            (self.root / ".sdlc" / "config.yaml").write_text(config, encoding="utf-8")
        if operator is not None:
            self.task_file.write_text(
                json.dumps({"task": task, "operator": operator, "round": 1}), encoding="utf-8")

    @property
    def task_file(self) -> Path:
        return self.root / ".git" / "sdlc-task.json"

    def call(self, tool: str, tool_input, **extra):
        """One PreToolUse event; `extra` are the top-level keys a member's call adds."""
        event = {"session_id": "s", "cwd": str(self.root), "permission_mode": "auto",
                 "hook_event_name": "PreToolUse", "tool_name": tool,
                 "tool_input": tool_input, "tool_use_id": "toolu_1", **extra}
        return run_hook(json.dumps(event), self.tmp_path)

    def member(self, tool: str, tool_input):
        """The call of a workflow member: `agent_id` and `agent_type` ride in the event."""
        return self.call(tool, tool_input, **MEMBER)

    def own(self, tool: str, tool_input):
        """The session's own call: neither `agent_id` nor `agent_type`."""
        return self.call(tool, tool_input)


def bash(command: str) -> dict:
    return {"command": command, "description": "d"}


def qa(tmp_path: Path, config: str = QA_CONFIG, name: str = "repo") -> Fx:
    return Fx(tmp_path, config=config, operator="qa", task="write-tests", name=name)


# --- Next actions 13: the declared commands pass, word for word --------------------

def test_nextaction13_the_developer_may_run_the_declared_test_command(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash(DEV_COMMAND)) == PASS
    # the same word is still a refused path to any other tool and to any other call
    assert fx.member("Read", {"file_path": "tests"}) == refusal(DEV_LINE.format("tests"))
    assert fx.member("Bash", bash("cat tests")) == refusal(DEV_LINE.format("tests"))


def test_nextaction13_the_developer_may_run_the_declared_test_build(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash(DEV_BUILD)) == PASS
    assert fx.member("Bash", bash(DEV_BUILD + " extra")) == refusal(DEV_LINE.format("tests/"))


def test_nextaction13_qa_may_run_the_declared_commands_too(tmp_path):
    fx = qa(tmp_path)
    assert fx.member("Bash", bash(QA_COMMAND)) == PASS
    assert fx.member("Bash", bash(QA_BUILD)) == PASS
    assert fx.member("Bash", bash(QA_COMMAND + " -x")) == refusal(
        QA_UNIT_LINE.format("tests/unit"))
    assert fx.member("Bash", bash(QA_BUILD + " engine/core.py")) == refusal(
        QA_BODY_LINE.format("engine/"))


def test_nextaction13_one_more_word_holds_the_command(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash(DEV_COMMAND)) == PASS
    for command in [DEV_COMMAND + " -x", DEV_COMMAND + " tests", "-x " + DEV_COMMAND,
                    "python -P -m pytest tests -q -n auto -n auto"]:
        assert fx.member("Bash", bash(command)) == refusal(DEV_LINE.format("tests")), command


def test_nextaction13_one_fewer_word_holds_the_command(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash(DEV_COMMAND)) == PASS
    for command in ["python -P -m pytest tests -q -n", "python -P -m pytest tests -q",
                    "-P -m pytest tests -q -n auto", "python -P -m pytest tests"]:
        assert fx.member("Bash", bash(command)) == refusal(DEV_LINE.format("tests")), command


def test_nextaction13_a_walled_word_glued_to_a_shell_operator_is_still_held(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash(DEV_COMMAND)) == PASS
    # a chain whose second part reads a walled file
    assert fx.member("Bash", bash(DEV_COMMAND + " && cat tests/test_a.py")) == refusal(
        DEV_LINE.format("tests"))
    assert fx.member("Bash", bash(DEV_COMMAND + " | cat tests/test_a.py")) == refusal(
        DEV_LINE.format("tests"))
    # the operator is glued to the last word, to the first word, or to the walled word
    assert fx.member("Bash", bash(DEV_COMMAND + ";")) == refusal(DEV_LINE.format("tests"))
    assert fx.member("Bash", bash("echo hi;" + DEV_COMMAND)) == refusal(
        DEV_LINE.format("tests"))
    assert fx.member("Bash", bash("echo a&&" + DEV_COMMAND)) == refusal(
        DEV_LINE.format("tests"))
    assert fx.member("Bash", bash("python -P -m pytest tests/;cat -q -n auto")) == refusal(
        DEV_LINE.format("tests/;cat"))


def test_nextaction13_words_compare_exactly_with_no_case_folding(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash(DEV_COMMAND)) == PASS
    assert fx.member("Bash", bash("PYTHON -P -m pytest tests -q -n auto")) == refusal(
        DEV_LINE.format("tests"))
    assert fx.member("Bash", bash("python -P -m pytest tests -Q -n auto")) == refusal(
        DEV_LINE.format("tests"))
    assert fx.member("Bash", bash("python -p -m pytest tests -q -n auto")) == refusal(
        DEV_LINE.format("tests"))


def test_nextaction13_the_words_are_the_commands_own_so_quotes_and_spaces_do_not_matter(tmp_path):
    fx = Fx(tmp_path)
    for command in ['python -P -m pytest "tests" -q -n auto',
                    "python -P -m pytest 'tests' -q -n auto",
                    "python   -P -m  pytest tests -q -n auto",
                    "python\t-P -m pytest tests -q -n auto  "]:
        assert fx.member("Bash", bash(command)) == PASS, command


@pytest.mark.skipif(not NT, reason="backslashes are separators only on Windows")
def test_nextaction13_on_windows_a_backslash_path_equals_the_declared_slash_path(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash("python tools\\build.py tests\\")) == PASS
    assert fx.member("Bash", bash("python tools\\build.py tests\\x")) == refusal(
        DEV_LINE.format("tests/x"))


def test_nextaction13_the_file_command_is_not_the_test_command(tmp_path):
    fx = Fx(tmp_path)
    assert fx.member("Bash", bash(DEV_COMMAND)) == PASS
    # `test.file` is not passed: a run of one functional file stays a read of it
    assert fx.member("Bash", bash("python -P -m pytest tests/test_wall.py -q")) == refusal(
        DEV_LINE.format("tests/test_wall.py"))


def test_nextaction13_a_repository_with_no_declared_build_passes_only_its_command(tmp_path):
    config = """\
test:
  command: [python, -P, -m, pytest, tests, -q, -n, auto]
wall:
  functional: [tests/]
"""
    fx = Fx(tmp_path, config=config)
    assert fx.member("Bash", bash(DEV_COMMAND)) == PASS
    assert fx.member("Bash", bash(DEV_BUILD)) == refusal(DEV_LINE.format("tests/"))


def test_nextaction13_a_repository_with_no_test_block_holds_the_same_words(tmp_path):
    with_block = Fx(tmp_path, name="with")
    assert with_block.member("Bash", bash(DEV_COMMAND)) == PASS
    without = Fx(tmp_path, config="wall:\n  functional: [tests/]\n", name="without")
    assert without.member("Bash", bash(DEV_COMMAND)) == refusal(DEV_LINE.format("tests"))


def test_nextaction13_a_test_command_that_is_no_list_declares_nothing(tmp_path):
    good = Fx(tmp_path, name="good")
    assert good.member("Bash", bash(DEV_COMMAND)) == PASS
    bad = "test:\n  command: 3\nwall:\n  functional: [tests/]\n"
    fx = Fx(tmp_path, config=bad, name="bad")
    assert fx.member("Bash", bash(DEV_COMMAND)) == refusal(DEV_LINE.format("tests"))


def test_nextaction13_the_declared_pass_prints_nothing_and_exits_0(tmp_path):
    fx = Fx(tmp_path)
    code, out, err = fx.member("Bash", bash(DEV_COMMAND))
    assert (code, out, err) == PASS
    assert fx.member("Bash", bash(DEV_COMMAND + " -x"))[0] == 2


# --- Next actions 15: the hook holds only a call that carries an agent_id ---------------

def test_nextaction15_the_sessions_own_call_during_a_task_passes(tmp_path):
    fx = Fx(tmp_path)
    for tool, tool_input in [("Read", {"file_path": "tests/run_a.bat"}),
                             ("Glob", {"pattern": "**/*"}),
                             ("Grep", {"pattern": "x", "path": "tests"}),
                             ("Write", {"file_path": "tests/a.py", "content": "x"}),
                             ("Bash", bash("cat tests/a.py"))]:
        assert fx.own(tool, tool_input) == PASS, tool
    # the same calls, as a member, are held
    assert fx.member("Read", {"file_path": "tests/run_a.bat"}) == refusal(
        DEV_LINE.format("tests/run_a.bat"))
    assert fx.member("Glob", {"pattern": "**/*"}) == refusal(DEV_LINE.format("**/*"))
    assert fx.member("Bash", bash("cat tests/a.py")) == refusal(DEV_LINE.format("tests/a.py"))


def test_nextaction15_the_orchestrators_glob_during_write_tests_passes(tmp_path):
    fx = qa(tmp_path)
    assert fx.own("Glob", {"pattern": "**/*"}) == PASS
    assert fx.own("Read", {"file_path": "engine/core.py"}) == PASS
    assert fx.own("Read", {"file_path": "tests/unit/test_a.py"}) == PASS
    assert fx.own("Bash", bash("cat engine/core.py tests/unit/test_a.py")) == PASS
    assert fx.member("Glob", {"pattern": "**/*"}) == refusal(QA_UNIT_LINE.format("**/*"))
    assert fx.member("Read", {"file_path": "engine/core.py"}) == refusal(
        QA_BODY_LINE.format("engine/core.py"))
    assert fx.member("Read", {"file_path": "tests/unit/test_a.py"}) == refusal(
        QA_UNIT_LINE.format("tests/unit/test_a.py"))


def test_nextaction15_a_null_agent_id_passes(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"file_path": "tests/run_a.bat"}, agent_id=None) == PASS
    assert fx.call("Bash", bash("cat tests/run_a.bat"), agent_id=None,
                   agent_type="workflow-subagent") == PASS
    assert fx.call("Read", {"file_path": "tests/run_a.bat"}, agent_id="a1") == refusal(
        DEV_LINE.format("tests/run_a.bat"))


def test_nextaction15_the_agent_type_alone_does_not_hold_a_call(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"file_path": "tests/run_a.bat"},
                   agent_type="workflow-subagent") == PASS
    assert fx.call("Read", {"file_path": "tests/run_a.bat"}, agent_type="workflow-subagent",
                   agent_id="a1") == refusal(DEV_LINE.format("tests/run_a.bat"))


@pytest.mark.parametrize("value", ["", "a28a6f45e23166402", " ", "0", 0, 7, False, True, [], {},
                                   ["a1"]],
                         ids=["empty-string", "an-id", "blank", "string-zero", "zero", "number",
                              "false", "true", "empty-list", "empty-object", "list"])
def test_nextaction15_any_agent_id_but_null_holds_the_call(tmp_path, value):
    fx = Fx(tmp_path)
    assert fx.own("Read", {"file_path": "tests/run_a.bat"}) == PASS
    assert fx.call("Read", {"file_path": "tests/run_a.bat"}, agent_id=value) == refusal(
        DEV_LINE.format("tests/run_a.bat"))


def test_nextaction15_a_held_member_keeps_each_refusal_line_on_stderr_with_exit_2(tmp_path):
    fx = Fx(tmp_path)
    assert fx.own("Read", {"file_path": "tests/run_a.bat"}) == PASS
    code, out, err = fx.member("Read", {"file_path": "tests/run_a.bat"})
    assert (code, out) == (2, "")
    assert err == "Task green: Developer reads no functional test: tests/run_a.bat\n"
    helper = qa(tmp_path, name="second")
    assert helper.own("Read", {"file_path": "engine/core.py"}) == PASS
    assert helper.member("Read", {"file_path": "engine/core.py"}) == (
        2, "", "Task write-tests: QA reads no implementation body: engine/core.py\n")
    assert helper.member("Read", {"file_path": "tests/unit/a.py"}) == (
        2, "", "Task write-tests: QA reads no unit test: tests/unit/a.py\n")


def test_nextaction15_a_call_with_no_agent_id_passes_the_declared_commands_too(tmp_path):
    fx = Fx(tmp_path)
    assert fx.own("Bash", bash(DEV_COMMAND + " -x")) == PASS
    assert fx.member("Bash", bash(DEV_COMMAND + " -x")) == refusal(DEV_LINE.format("tests"))


def test_nextaction15_the_hook_still_never_raises(tmp_path):
    # a broken wall, a broken task file and a broken event, each with an agent_id: exit 0
    broken = Fx(tmp_path, config="wall: [unclosed\n", name="a")
    assert broken.own("Read", {"file_path": "tests/run_a.bat"}) == PASS
    assert broken.member("Read", {"file_path": "tests/run_a.bat"}) == PASS
    task = Fx(tmp_path, name="b")
    assert task.own("Read", {"file_path": "tests/run_a.bat"}) == PASS
    task.task_file.write_text("{", encoding="utf-8")
    assert task.member("Read", {"file_path": "tests/run_a.bat"}) == PASS
    fx = Fx(tmp_path, name="c")
    assert fx.own("Read", {"file_path": "tests/run_a.bat"}) == PASS
    for odd in [None, "tests/run_a.bat", ["tests/run_a.bat"], 3]:
        assert fx.call("Read", odd, **MEMBER) == PASS
    assert fx.call("Read", {"file_path": 7}, **MEMBER) == PASS
    assert fx.call("Bash", {"command": None}, **MEMBER) == PASS
    assert run_hook("not json", tmp_path) == PASS
    assert run_hook(json.dumps({"agent_id": "a1"}), tmp_path) == PASS
    assert fx.member("Read", {"file_path": "tests/run_a.bat"}) == refusal(
        DEV_LINE.format("tests/run_a.bat"))


def test_nextaction15_between_tasks_no_task_file_stands_and_nothing_is_held(tmp_path):
    fx = Fx(tmp_path, operator=None)
    assert fx.own("Read", {"file_path": "tests/run_a.bat"}) == PASS
    assert fx.member("Read", {"file_path": "tests/run_a.bat"}) == PASS
    fx.task_file.write_text(
        json.dumps({"task": "green", "operator": "developer", "round": 1}), encoding="utf-8")
    assert fx.own("Read", {"file_path": "tests/run_a.bat"}) == PASS
    assert fx.member("Read", {"file_path": "tests/run_a.bat"}) == refusal(
        DEV_LINE.format("tests/run_a.bat"))
