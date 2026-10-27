"""Wall suite (contract: execution-team, unit e3-wall, checks SC3.1 and SC3.2).

The unit builds the wall between the Developer and QA: a PreToolUse hook
(`hooks/wall.py`, registered in `hooks/hooks.json`) that, while the task file
`.git/sdlc-task.json` names a walled operator, refuses each tool call that
names a path across the wall (exit 2, one line on stderr), and
`python -m taskcontract interface {file}`, which gives QA a Python file's
signatures and docstrings with no body. `taskcontract.declaration.read_wall`
reads the `wall:` block of `.sdlc/config.yaml`.

The plugin's files are found beside the imported package, as
tests/test_declared_command.py finds its scripts, so a run against a prototype
runs the prototype's hook. The hook runs as a subprocess the way Claude Code
runs a PreToolUse hook: the event on stdin (`hook_event_name`, `cwd`,
`tool_name`, `tool_input`). Every test builds its own git repository under
tmp_path, with its own `.sdlc/config.yaml` and its own task file: the kit's
repository, config and git folder are never touched.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

import taskcontract

PLUGIN = Path(taskcontract.__file__).resolve().parents[1]
WALL = PLUGIN / "hooks" / "wall.py"
HOOKS_JSON = PLUGIN / "hooks" / "hooks.json"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
NT = os.name == "nt"

# The design's wall, drawn.
DESIGN = """\
wall:
  functional: [tests/run_*.bat]
  unit: [tests/*.cpp]
  code: [src/]
  interface: [src/*.h]
"""
# A Python case: folders, and one interface file.
PY = """\
wall:
  functional: [tests/functional/]
  unit: [tests/unit/]
  code: [engine/]
  interface: [engine/types.py]
"""
# A path that both a unit entry and a code entry hold.
OVERLAP = """\
wall:
  functional: [tests/functional/]
  unit: [src/*_test.cpp]
  code: [src/]
  interface: [src/*.h]
"""
# The kit's own wall: one folder, no other key.
KIT = """\
wall:
  functional: [tests/]
"""

DEV_LINE = "Task green: Developer reads no functional test: {}"
QA_UNIT_LINE = "Task write-tests: QA reads no unit test: {}"
QA_BODY_LINE = "Task write-tests: QA reads no implementation body: {}"
COMMAND = 'python "${CLAUDE_PLUGIN_ROOT}/hooks/wall.py"'
SEVEN = ["Read", "Edit", "Write", "NotebookEdit", "Grep", "Glob", "Bash"]

PASS = (0, "", "")


def refusal(line: str) -> tuple[int, str, str]:
    """What a refused call gives: exit 2, nothing on stdout, the line on stderr."""
    return (2, "", line + "\n")


# --- the scratch repository and the hook runner -------------------------------------

def run_hook(stdin: str, tmp_path: Path, env: dict | None = None):
    """(exit code, stdout, stderr) of the hook fed `stdin`, run from a folder that is
    not the repository and with no git repository above the fixtures."""
    work = tmp_path / "cwd"
    work.mkdir(exist_ok=True)
    full = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1",
            **(env or {})}
    done = subprocess.run([sys.executable, str(WALL)], input=stdin, cwd=work, env=full,
                          capture_output=True, encoding="utf-8", errors="replace",
                          timeout=100, creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


def event(cwd, tool: str, tool_input: dict) -> str:
    return json.dumps({"session_id": "s", "cwd": str(cwd), "permission_mode": "auto",
                       "hook_event_name": "PreToolUse", "tool_name": tool,
                       "tool_input": tool_input, "tool_use_id": "toolu_1"})


class Fx:
    """<tmp>/repo: a git repository, a config, and a task file naming an operator."""

    def __init__(self, tmp_path: Path, operator: str | None = "developer",
                 task: str = "green", config: str | None = DESIGN):
        self.tmp_path = tmp_path
        self.root = tmp_path / "repo"
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

    def call(self, tool: str, tool_input: dict, cwd=None, env: dict | None = None):
        return run_hook(event(cwd or self.root, tool, tool_input), self.tmp_path, env)


def qa(tmp_path: Path, config: str = DESIGN) -> Fx:
    return Fx(tmp_path, operator="qa", task="write-tests", config=config)


# --- SC3.1: the Developer reads no functional test -----------------------------------

def test_sc3_1_a_read_of_a_functional_test_is_refused_with_the_designs_line(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"file_path": "tests/run_command_line.bat"}) == refusal(
        "Task green: Developer reads no functional test: tests/run_command_line.bat")


DEV_REFUSED = [
    ("edit", DESIGN, "Edit", {"file_path": "tests/run_a.bat", "old_string": "a",
                              "new_string": "b"}, "tests/run_a.bat"),
    ("write", DESIGN, "Write", {"file_path": "tests/run_a.bat", "content": "x"},
     "tests/run_a.bat"),
    ("notebook", PY, "NotebookEdit", {"notebook_path": "tests/functional/n.ipynb",
                                      "new_source": "x"}, "tests/functional/n.ipynb"),
    ("grep-path", DESIGN, "Grep", {"pattern": "main", "path": "tests/run_a.bat"},
     "tests/run_a.bat"),
    ("grep-glob", DESIGN, "Grep", {"pattern": "main", "glob": "tests/run_*.bat"},
     "tests/run_*.bat"),
    ("grep-folder-itself", PY, "Grep", {"pattern": "main", "path": "tests/functional"},
     "tests/functional"),
    ("glob-pattern", DESIGN, "Glob", {"pattern": "tests/run_*.bat"}, "tests/run_*.bat"),
    ("glob-wider-pattern", DESIGN, "Glob", {"pattern": "**/*.bat"}, "**/*.bat"),
    ("glob-path", PY, "Glob", {"pattern": "*.py", "path": "tests/functional"},
     "tests/functional"),
    ("bash-cat", DESIGN, "Bash", {"command": "cat tests/run_a.bat", "description": "d"},
     "tests/run_a.bat"),
    ("bash-in-a-chain", DESIGN, "Bash",
     {"command": "python -m pytest tests/run_a.bat -q && echo done | tail -n 1"},
     "tests/run_a.bat"),
    ("bash-quoted-word", DESIGN, "Bash", {"command": 'cat "tests/run_a.bat"'},
     "tests/run_a.bat"),
    ("bash-option-value", DESIGN, "Bash", {"command": "cp --target=tests/run_a.bat x"},
     "tests/run_a.bat"),
    ("bash-unclosed-quote", DESIGN, "Bash", {"command": 'echo "oops tests/run_a.bat'},
     "tests/run_a.bat"),
    ("bash-glob-word", DESIGN, "Bash", {"command": "ls tests/*"}, "tests/*"),
    ("bash-folder-word", PY, "Bash", {"command": "ls tests/functional/"},
     "tests/functional/"),
]


@pytest.mark.parametrize("config, tool, tool_input, named",
                         [c[1:] for c in DEV_REFUSED], ids=[c[0] for c in DEV_REFUSED])
def test_sc3_1_each_tool_call_naming_a_functional_test_is_refused(
        tmp_path, config, tool, tool_input, named):
    fx = Fx(tmp_path, config=config)
    assert fx.call(tool, tool_input) == refusal(DEV_LINE.format(named))


DEV_PASSES = [
    ("read-a-unit-test", "Read", {"file_path": "tests/engine.cpp"}),
    ("read-the-code", "Read", {"file_path": "src/engine.cpp"}),
    ("edit-the-code", "Edit", {"file_path": "src/engine.cpp", "old_string": "a",
                               "new_string": "b"}),
    ("write-a-unit-test", "Write", {"file_path": "tests/engine.cpp", "content": "x"}),
    ("read-a-file-no-glob-holds", "Read", {"file_path": "tests/run_a.txt"}),
    ("grep-the-code", "Grep", {"pattern": "main", "path": "src", "glob": "*.cpp"}),
    ("glob-the-code", "Glob", {"pattern": "src/*"}),
    ("bash-both-allowed", "Bash", {"command": "cat src/engine.cpp tests/engine.cpp"}),
    ("bash-glob-word-over-the-code", "Bash", {"command": "ls src/*"}),
    ("bash-no-path", "Bash", {"command": "git status"}),
]


@pytest.mark.parametrize("tool, tool_input", [c[1:] for c in DEV_PASSES],
                         ids=[c[0] for c in DEV_PASSES])
def test_sc3_1_the_developer_may_read_code_and_unit_tests(tmp_path, tool, tool_input):
    fx = Fx(tmp_path)
    assert fx.call(tool, tool_input) == PASS


def test_sc3_1_the_refusal_names_the_first_path_in_the_calls_own_order(tmp_path):
    fx = Fx(tmp_path)
    command = "cat src/a.cpp tests/engine.cpp tests/run_b.bat tests/run_a.bat"
    assert fx.call("Bash", {"command": command}) == refusal(DEV_LINE.format("tests/run_b.bat"))
    command = "cat tests/run_a.bat tests/run_b.bat"
    assert fx.call("Bash", {"command": command}) == refusal(DEV_LINE.format("tests/run_a.bat"))


def test_sc3_1_the_kits_own_wall_shuts_the_developer_out_of_its_tests_folder(tmp_path):
    fx = Fx(tmp_path, config=KIT)
    assert fx.call("Read", {"file_path": "tests/test_wall.py"}) == refusal(
        DEV_LINE.format("tests/test_wall.py"))
    assert fx.call("Read", {"file_path": "taskcontract/declaration.py"}) == PASS
    assert fx.call("Read", {"file_path": "testsuite/a.py"}) == PASS


# --- SC3.2: QA reads no implementation body and no unit test -------------------------

def test_sc3_2_a_read_of_a_unit_test_is_refused(tmp_path):
    fx = qa(tmp_path)
    assert fx.call("Read", {"file_path": "tests/test_command_line.cpp"}) == refusal(
        "Task write-tests: QA reads no unit test: tests/test_command_line.cpp")


def test_sc3_2_a_read_of_an_implementation_body_is_refused(tmp_path):
    fx = qa(tmp_path)
    assert fx.call("Read", {"file_path": "src/command_line.cpp"}) == refusal(
        "Task write-tests: QA reads no implementation body: src/command_line.cpp")


QA_REFUSED = [
    ("unit-edit", QA_UNIT_LINE, "Edit", {"file_path": "tests/engine.cpp", "old_string": "a",
                                         "new_string": "b"}, "tests/engine.cpp"),
    ("unit-write", QA_UNIT_LINE, "Write", {"file_path": "tests/engine.cpp", "content": "x"},
     "tests/engine.cpp"),
    ("unit-grep-path", QA_UNIT_LINE, "Grep", {"pattern": "x", "path": "tests/engine.cpp"},
     "tests/engine.cpp"),
    ("unit-grep-glob", QA_UNIT_LINE, "Grep", {"pattern": "x", "glob": "tests/*.cpp"},
     "tests/*.cpp"),
    ("unit-glob", QA_UNIT_LINE, "Glob", {"pattern": "tests/*.cpp"}, "tests/*.cpp"),
    ("unit-bash", QA_UNIT_LINE, "Bash", {"command": "cat tests/engine.cpp"},
     "tests/engine.cpp"),
    ("body-edit", QA_BODY_LINE, "Edit", {"file_path": "src/engine.cpp", "old_string": "a",
                                         "new_string": "b"}, "src/engine.cpp"),
    ("body-write", QA_BODY_LINE, "Write", {"file_path": "src/engine.cpp", "content": "x"},
     "src/engine.cpp"),
    ("body-grep-path", QA_BODY_LINE, "Grep", {"pattern": "x", "path": "src/engine.cpp"},
     "src/engine.cpp"),
    ("body-grep-folder-itself", QA_BODY_LINE, "Grep", {"pattern": "x", "path": "src"}, "src"),
    ("body-grep-glob", QA_BODY_LINE, "Grep", {"pattern": "x", "glob": "src/*.cpp"},
     "src/*.cpp"),
    ("body-glob", QA_BODY_LINE, "Glob", {"pattern": "src/**"}, "src/**"),
    ("body-bash", QA_BODY_LINE, "Bash", {"command": "cat src/engine.cpp"}, "src/engine.cpp"),
    ("body-bash-glob-word-wider-than-the-interface", QA_BODY_LINE, "Bash",
     {"command": "ls src/*"}, "src/*"),
]


@pytest.mark.parametrize("line, tool, tool_input, named",
                         [c[1:] for c in QA_REFUSED], ids=[c[0] for c in QA_REFUSED])
def test_sc3_2_each_tool_call_across_qas_wall_is_refused_with_its_line(
        tmp_path, line, tool, tool_input, named):
    fx = qa(tmp_path)
    assert fx.call(tool, tool_input) == refusal(line.format(named))


QA_PASSES = [
    ("read-an-interface-file", "Read", {"file_path": "src/engine.h"}),
    ("edit-an-interface-file", "Edit", {"file_path": "src/engine.h", "old_string": "a",
                                       "new_string": "b"}),
    ("grep-an-interface-file", "Grep", {"pattern": "x", "path": "src/engine.h"}),
    ("grep-an-interface-glob", "Grep", {"pattern": "x", "glob": "src/*.h"}),
    ("glob-the-interface-files", "Glob", {"pattern": "src/*.h"}),
    ("bash-an-interface-file", "Bash", {"command": "cat src/engine.h"}),
    ("read-a-functional-test", "Read", {"file_path": "tests/run_a.bat"}),
    ("write-a-functional-test", "Write", {"file_path": "tests/run_a.bat", "content": "x"}),
    ("bash-a-functional-test", "Bash", {"command": "cat tests/run_a.bat"}),
    ("read-a-file-outside-every-entry", "Read", {"file_path": "docs/notes.md"}),
    ("bash-no-path", "Bash", {"command": "git status"}),
]


@pytest.mark.parametrize("tool, tool_input", [c[1:] for c in QA_PASSES],
                         ids=[c[0] for c in QA_PASSES])
def test_sc3_2_qa_may_read_an_interface_file_and_a_functional_test(tmp_path, tool, tool_input):
    fx = qa(tmp_path)
    assert fx.call(tool, tool_input) == PASS


def test_sc3_2_a_path_held_by_both_a_unit_and_a_code_entry_is_a_unit_test(tmp_path):
    fx = qa(tmp_path, config=OVERLAP)
    assert fx.call("Read", {"file_path": "src/engine_test.cpp"}) == refusal(
        QA_UNIT_LINE.format("src/engine_test.cpp"))
    assert fx.call("Read", {"file_path": "src/engine.cpp"}) == refusal(
        QA_BODY_LINE.format("src/engine.cpp"))


def test_sc3_2_the_refusal_names_the_first_crossing_path_and_its_own_kind(tmp_path):
    fx = qa(tmp_path)
    command = "cat src/engine.h src/engine.cpp tests/engine.cpp"
    assert fx.call("Bash", {"command": command}) == refusal(QA_BODY_LINE.format("src/engine.cpp"))
    command = "cat tests/engine.cpp src/engine.cpp"
    assert fx.call("Bash", {"command": command}) == refusal(QA_UNIT_LINE.format("tests/engine.cpp"))


def test_sc3_2_the_kits_own_wall_leaves_qa_every_path_it_does_not_list(tmp_path):
    fx = qa(tmp_path, config=KIT)
    assert fx.call("Read", {"file_path": "tests/test_wall.py"}) == PASS
    assert fx.call("Read", {"file_path": "taskcontract/declaration.py"}) == PASS


# --- reading (d): QA's one code-path call, `python -m taskcontract interface FILE` ----

@pytest.mark.parametrize("command", [
    "python -m taskcontract interface engine/core.py",
    'python -m taskcontract interface "engine/core.py"',
    "python -m taskcontract interface ./engine/core.py",
], ids=["plain", "quoted", "dot-slash"])
def test_reading_d_qa_may_ask_for_a_code_files_interface(tmp_path, command):
    fx = qa(tmp_path, config=PY)
    assert fx.call("Bash", {"command": command}) == PASS


def test_reading_d_the_interface_call_passes_the_code_wall_never_the_unit_wall(tmp_path):
    fx = qa(tmp_path, config=PY)
    assert fx.call("Bash", {"command": "python -m taskcontract interface tests/unit/test_core.py"}
                   ) == refusal(QA_UNIT_LINE.format("tests/unit/test_core.py"))


def test_reading_d_only_the_interface_calls_own_file_passes_the_code_wall(tmp_path):
    fx = qa(tmp_path, config=PY)
    assert fx.call("Bash", {"command": "python -m taskcontract interface engine/a.py"
                                       " && cat engine/b.py"}
                   ) == refusal(QA_BODY_LINE.format("engine/b.py"))
    assert fx.call("Bash", {"command": "cat engine/a.py && python -m taskcontract interface"
                                       " engine/b.py"}
                   ) == refusal(QA_BODY_LINE.format("engine/a.py"))
    assert fx.call("Bash", {"command": "python -m taskcontract tree engine/core.py"}
                   ) == refusal(QA_BODY_LINE.format("engine/core.py"))


def test_reading_d_a_plain_read_of_the_same_file_is_still_refused(tmp_path):
    fx = qa(tmp_path, config=PY)
    assert fx.call("Read", {"file_path": "engine/core.py"}) == refusal(
        QA_BODY_LINE.format("engine/core.py"))
    assert fx.call("Read", {"file_path": "engine/types.py"}) == PASS


# --- reading (a): who is walled ------------------------------------------------------

@pytest.mark.parametrize("operator",
                         ["qa-verifier", "dev-verifier", "receipts", "orchestrator"])
def test_reading_a_the_verifiers_receipts_and_orchestrator_are_not_walled(tmp_path, operator):
    fx = Fx(tmp_path, operator=operator, task="two-key")
    for tool, tool_input in [("Read", {"file_path": "tests/run_a.bat"}),
                             ("Read", {"file_path": "tests/engine.cpp"}),
                             ("Read", {"file_path": "src/engine.cpp"}),
                             ("Bash", {"command": "cat tests/run_a.bat src/engine.cpp"})]:
        assert fx.call(tool, tool_input) == PASS


def test_reading_a_the_developer_and_qa_each_stand_behind_a_wall_the_other_may_cross(tmp_path):
    dev = Fx(tmp_path)
    assert dev.call("Read", {"file_path": "tests/engine.cpp"}) == PASS
    assert dev.call("Read", {"file_path": "tests/run_a.bat"}) == refusal(
        DEV_LINE.format("tests/run_a.bat"))
    other = tmp_path / "second"
    other.mkdir()
    helper = qa(other)
    assert helper.call("Read", {"file_path": "tests/run_a.bat"}) == PASS
    assert helper.call("Read", {"file_path": "tests/engine.cpp"}) == refusal(
        QA_UNIT_LINE.format("tests/engine.cpp"))


# --- reading (b): which calls, and how a path resolves --------------------------------

def test_reading_b_a_grep_pattern_is_a_regex_and_never_a_path(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Grep", {"pattern": "tests/run_a.bat"}) == PASS
    assert fx.call("Grep", {"pattern": "tests/run_.*\\.bat", "path": "src", "glob": "*.cpp"}
                   ) == PASS
    assert fx.call("Grep", {"pattern": "tests/run_a.bat", "path": "tests/run_a.bat"}
                   ) == refusal(DEV_LINE.format("tests/run_a.bat"))


@pytest.mark.parametrize("tool, tool_input", [
    ("WebFetch", {"url": "tests/run_a.bat", "file_path": "tests/run_a.bat"}),
    ("mcp__fs__read", {"file_path": "tests/run_a.bat", "path": "tests/run_a.bat"}),
    ("TodoWrite", {"todos": [{"content": "tests/run_a.bat"}]}),
    ("Agent", {"prompt": "read tests/run_a.bat", "file_path": "tests/run_a.bat"}),
], ids=["webfetch", "mcp-tool", "todowrite", "agent"])
def test_reading_b_any_other_tool_passes(tmp_path, tool, tool_input):
    fx = Fx(tmp_path)
    assert fx.call(tool, tool_input) == PASS


def test_reading_b_the_wrong_key_names_no_path(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"path": "tests/run_a.bat"}) == PASS
    assert fx.call("NotebookEdit", {"file_path": "tests/run_a.bat"}) == PASS


@pytest.mark.parametrize("named", ["./tests/run_a.bat", "src/../tests/run_a.bat",
                                   "tests/./run_a.bat"],
                         ids=["dot-slash", "dot-dot", "dot-inside"])
def test_reading_b_a_path_is_resolved_before_it_is_matched(tmp_path, named):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"file_path": named}) == refusal(DEV_LINE.format(named))


def test_reading_b_an_absolute_path_inside_the_root_is_read_relative_to_it(tmp_path):
    fx = Fx(tmp_path)
    inside = str(fx.root / "tests" / "run_a.bat")
    assert fx.call("Read", {"file_path": inside}) == refusal(DEV_LINE.format(inside))
    code = str(fx.root / "src" / "engine.cpp")
    assert fx.call("Read", {"file_path": code}) == PASS
    other = tmp_path / "second"
    other.mkdir()
    helper = qa(other)
    body = str(helper.root / "src" / "engine.cpp")
    assert helper.call("Read", {"file_path": body}) == refusal(QA_BODY_LINE.format(body))
    iface = str(helper.root / "src" / "engine.h")
    assert helper.call("Read", {"file_path": iface}) == PASS


def test_reading_b_a_relative_path_resolves_against_the_root_not_the_cwd(tmp_path):
    fx = Fx(tmp_path)
    (fx.root / "sub").mkdir()
    assert fx.call("Read", {"file_path": "tests/run_a.bat"}, cwd=fx.root / "sub") == refusal(
        DEV_LINE.format("tests/run_a.bat"))
    (fx.root / "tests").mkdir()
    assert fx.call("Read", {"file_path": "run_a.bat"}, cwd=fx.root / "tests") == PASS


def test_reading_b_a_path_outside_the_root_passes(tmp_path):
    fx = Fx(tmp_path)
    elsewhere = tmp_path / "elsewhere" / "tests" / "run_a.bat"
    assert fx.call("Read", {"file_path": str(elsewhere)}) == PASS
    assert fx.call("Read", {"file_path": "../tests/run_a.bat"}) == PASS
    assert fx.call("Bash", {"command": f"cat {elsewhere.as_posix()}"}) == PASS
    assert fx.call("Glob", {"pattern": "*.txt", "path": str(elsewhere.parent)}) == PASS


@pytest.mark.skipif(not NT, reason="paths compare case-insensitively only on Windows")
def test_reading_b_on_windows_paths_compare_without_case(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"file_path": "TESTS/Run_A.BAT"}) == refusal(
        DEV_LINE.format("TESTS/Run_A.BAT"))
    inside = str(fx.root / "TESTS" / "RUN_A.BAT").upper()
    assert fx.call("Read", {"file_path": inside}) == refusal(DEV_LINE.format(inside))


@pytest.mark.skipif(not NT, reason="backslashes are separators only on Windows")
def test_reading_b_on_windows_a_backslash_is_a_separator(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"file_path": "tests\\run_a.bat"}) == refusal(
        DEV_LINE.format("tests\\run_a.bat"))
    assert fx.call("Bash", {"command": "type tests\\run_a.bat"}) == refusal(
        DEV_LINE.format("tests/run_a.bat"))
    assert fx.call("Bash", {"command": "type src\\engine.cpp"}) == PASS


# --- reading (c): what crosses -------------------------------------------------------

def test_reading_c_a_folder_entry_holds_the_folder_itself_and_all_under_it(tmp_path):
    fx = qa(tmp_path)
    for named in ["src", "src/", "src/engine.cpp", "src/deep/er/engine.cpp"]:
        assert fx.call("Read", {"file_path": named}) == refusal(QA_BODY_LINE.format(named))
    for named in ["srcs/engine.cpp", "src2", "mysrc/engine.cpp", "docs/src/engine.cpp"]:
        assert fx.call("Read", {"file_path": named}) == PASS


def test_reading_c_a_glob_entry_holds_what_matches_and_nothing_else(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Read", {"file_path": "tests/run_x.bat"}) == refusal(
        DEV_LINE.format("tests/run_x.bat"))
    for named in ["tests/run_.bat.txt", "tests/other.bat", "run_x.bat", "tests/run_x.cmd"]:
        assert fx.call("Read", {"file_path": named}) == PASS


def test_reading_c_a_glob_word_crosses_when_it_matches_an_entry_or_an_entry_matches_it(tmp_path):
    fx = Fx(tmp_path)
    for tool, tool_input, named in [
        ("Glob", {"pattern": "**/*.bat"}, "**/*.bat"),
        ("Glob", {"pattern": "tests/*"}, "tests/*"),
        ("Glob", {"pattern": "tests/run_*.bat"}, "tests/run_*.bat"),
        ("Bash", {"command": "ls tests/*"}, "tests/*"),
        ("Bash", {"command": "ls **/*.bat"}, "**/*.bat"),
        ("Grep", {"pattern": "x", "glob": "tests/run_?.bat"}, "tests/run_?.bat"),
    ]:
        assert fx.call(tool, tool_input) == refusal(DEV_LINE.format(named))
    for tool, tool_input in [
        ("Glob", {"pattern": "**/*.cpp"}),
        ("Glob", {"pattern": "src/*"}),
        ("Bash", {"command": "ls tests/*.cpp"}),
        ("Grep", {"pattern": "x", "glob": "*.h"}),
    ]:
        assert fx.call(tool, tool_input) == PASS


def test_reading_c_a_glob_word_over_a_folder_crosses_by_the_same_test(tmp_path):
    fx = qa(tmp_path)
    for named in ["src/*", "src/**", "s*/*"]:
        assert fx.call("Glob", {"pattern": named}) == refusal(QA_BODY_LINE.format(named))
    assert fx.call("Glob", {"pattern": "src/*.h"}) == PASS
    assert fx.call("Bash", {"command": "ls src/*.h"}) == PASS


# --- reading (e): the refusal names the first path that crosses ----------------------

def test_reading_e_the_first_crossing_path_wins_over_an_earlier_path_that_passes(tmp_path):
    fx = Fx(tmp_path)
    assert fx.call("Grep", {"pattern": "x", "path": "src", "glob": "tests/run_*.bat"}
                   ) == refusal(DEV_LINE.format("tests/run_*.bat"))
    assert fx.call("Bash", {"command": "diff src/a.cpp tests/run_b.bat tests/run_a.bat"}
                   ) == refusal(DEV_LINE.format("tests/run_b.bat"))


# --- reading (f): when the hook refuses nothing --------------------------------------

READ_WALLED = ("Read", {"file_path": "tests/run_a.bat"})


def test_reading_f_with_no_task_file_nothing_is_refused(tmp_path):
    fx = Fx(tmp_path, operator=None)
    assert not fx.task_file.exists()
    assert fx.call(*READ_WALLED) == PASS
    assert fx.call("Bash", {"command": "cat tests/run_a.bat src/engine.cpp"}) == PASS


def test_reading_f_with_no_task_file_a_broken_config_is_never_read(tmp_path):
    fx = Fx(tmp_path, operator=None, config="wall: [unclosed\n")
    assert fx.call(*READ_WALLED) == PASS
    (fx.root / ".sdlc" / "config.yaml").unlink()
    (fx.root / ".sdlc" / "config.yaml").mkdir()
    assert fx.call(*READ_WALLED) == PASS


@pytest.mark.parametrize("text", ["", "not json", "{", "[]", "{}", '"developer"',
                                  '{"task": "green"}', '{"operator": null, "task": "green"}'],
                         ids=["empty", "not-json", "open-brace", "list", "empty-object",
                              "string", "no-operator", "null-operator"])
def test_reading_f_a_task_file_that_names_no_walled_operator_refuses_nothing(tmp_path, text):
    fx = Fx(tmp_path, operator=None)
    fx.task_file.write_text(text, encoding="utf-8")
    assert fx.call(*READ_WALLED) == PASS


@pytest.mark.parametrize("config", [None, "kit: fixture\n", "test:\n  command: [x]\n",
                                    "wall:\n", "wall: tests/\n", "test: [unclosed\n"],
                         ids=["no-file", "no-wall-key", "test-only", "null-wall",
                              "wall-is-a-string", "does-not-parse"])
@pytest.mark.parametrize("operator, task", [("developer", "green"), ("qa", "write-tests")])
def test_reading_f_a_config_with_no_wall_block_refuses_nothing(tmp_path, config, operator, task):
    fx = Fx(tmp_path, operator=operator, task=task, config=config)
    assert fx.call(*READ_WALLED) == PASS
    assert fx.call("Read", {"file_path": "src/engine.cpp"}) == PASS


def test_reading_f_a_wall_block_with_keys_missing_reads_them_as_empty(tmp_path):
    fx = Fx(tmp_path, operator="qa", task="write-tests", config=KIT)
    assert fx.call("Read", {"file_path": "src/engine.cpp"}) == PASS
    assert fx.call("Read", {"file_path": "tests/engine.cpp"}) == PASS


def test_reading_f_a_cwd_that_is_no_git_repository_refuses_nothing(tmp_path):
    plain = tmp_path / "plain"
    (plain / ".sdlc").mkdir(parents=True)
    (plain / ".sdlc" / "config.yaml").write_text(DESIGN, encoding="utf-8")
    (plain / ".git").mkdir()  # not a repository: no HEAD
    (plain / ".git" / "sdlc-task.json").write_text(
        json.dumps({"task": "green", "operator": "developer", "round": 1}), encoding="utf-8")
    assert run_hook(event(plain, *READ_WALLED), tmp_path) == PASS
    assert run_hook(event(tmp_path / "nowhere", *READ_WALLED), tmp_path) == PASS


@pytest.mark.parametrize("stdin", ["", "not json", "{", "[]", "null", '"Read"', "{}",
                                   '{"cwd": 3, "tool_name": "Read"}'],
                         ids=["empty", "not-json", "open-brace", "list", "null", "string",
                              "empty-object", "cwd-is-a-number"])
def test_reading_f_input_that_cannot_be_read_refuses_nothing(tmp_path, stdin):
    Fx(tmp_path)
    assert run_hook(stdin, tmp_path) == PASS


def test_reading_f_a_tool_input_that_is_not_an_object_refuses_nothing(tmp_path):
    fx = Fx(tmp_path)
    for odd in [None, "tests/run_a.bat", ["tests/run_a.bat"], 3]:
        assert run_hook(event(fx.root, "Read", odd), tmp_path) == PASS
    assert fx.call("Read", {"file_path": None}) == PASS
    assert fx.call("Read", {"file_path": 7}) == PASS
    assert fx.call("Bash", {"command": None}) == PASS
    assert fx.call("Grep", {"pattern": "x", "path": ["tests/run_a.bat"]}) == PASS
    assert fx.call("Read", {"file_path": "tests/run_a.bat"}) == refusal(
        DEV_LINE.format("tests/run_a.bat"))


def test_reading_f_the_hook_finds_the_repository_from_a_folder_below_its_root(tmp_path):
    fx = Fx(tmp_path)
    (fx.root / "deep" / "er").mkdir(parents=True)
    assert fx.call("Read", {"file_path": "tests/run_a.bat"}, cwd=fx.root / "deep" / "er"
                   ) == refusal(DEV_LINE.format("tests/run_a.bat"))


# --- reading (g): read_wall ----------------------------------------------------------

def read_wall(root: Path):
    spec = importlib.util.find_spec("taskcontract.declaration")
    assert spec is not None, "taskcontract.declaration does not exist"
    module = importlib.import_module("taskcontract.declaration")
    reader = getattr(module, "read_wall", None)
    assert reader is not None, "taskcontract.declaration has no read_wall"
    return reader(root)


def put_config(tmp_path: Path, text: str | None) -> Path:
    root = tmp_path / "cfg"
    root.mkdir()
    if text is not None:
        (root / ".sdlc").mkdir()
        (root / ".sdlc" / "config.yaml").write_text(text, encoding="utf-8")
    return root


def test_reading_g_read_wall_returns_the_four_lists(tmp_path):
    got = read_wall(put_config(tmp_path, DESIGN))
    assert got is not None
    assert got.functional == ["tests/run_*.bat"]
    assert got.unit == ["tests/*.cpp"]
    assert got.code == ["src/"]
    assert got.interface == ["src/*.h"]
    assert all(isinstance(part, list) for part in (got.functional, got.unit, got.code,
                                                   got.interface))


def test_reading_g_an_absent_key_reads_as_an_empty_list(tmp_path):
    got = read_wall(put_config(tmp_path, KIT))
    assert got is not None
    assert (got.functional, got.unit, got.code, got.interface) == (["tests/"], [], [], [])


@pytest.mark.parametrize("text", [None, "kit: fixture\n", "test:\n  command: [x]\n", "wall:\n",
                                  "wall: tests/\n", "wall: [tests/]\n", "- wall\n",
                                  "wall: [unclosed\n"],
                         ids=["no-file", "no-wall-key", "test-only", "null", "string", "list",
                              "config-is-a-list", "does-not-parse"])
def test_reading_g_read_wall_returns_none_when_the_config_has_no_wall_block(tmp_path, text):
    assert read_wall(put_config(tmp_path, text)) is None


def test_reading_g_a_key_that_is_not_a_list_of_strings_reads_as_empty(tmp_path):
    text = "wall:\n  functional: tests/\n  unit: [tests/, 3]\n  code: [src/]\n  interface:\n"
    got = read_wall(put_config(tmp_path, text))
    assert got is not None
    assert (got.functional, got.unit, got.code, got.interface) == ([], [], ["src/"], [])


# --- reading (i): hooks.json ---------------------------------------------------------

POST_TOOL_USE = [{"matcher": "*", "hooks": [{
    "type": "command", "command": 'python "${CLAUDE_PLUGIN_ROOT}/hooks/context_size.py"'}]}]
USER_PROMPT_SUBMIT = [{"hooks": [{
    "type": "command", "command": 'python "${CLAUDE_PLUGIN_ROOT}/hooks/context_size.py"'}]}]


def matches(matcher: str, tool: str) -> bool:
    if matcher in ("", "*"):
        return True
    return re.fullmatch(matcher, tool) is not None


def test_reading_i_hooks_json_gains_one_pretooluse_entry_for_the_seven_tools():
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
    entries = hooks.get("PreToolUse")
    assert isinstance(entries, list) and len(entries) == 1
    entry = entries[0]
    assert entry["hooks"] == [{"type": "command", "command": COMMAND}]
    assert isinstance(entry.get("matcher"), str)
    for tool in SEVEN:
        assert matches(entry["matcher"], tool), tool
    for tool in ["WebFetch", "Agent", "TodoWrite", "ReadMcpResourceTool"]:
        assert not matches(entry["matcher"], tool), tool
    assert hooks["PostToolUse"] == POST_TOOL_USE
    assert hooks["UserPromptSubmit"] == USER_PROMPT_SUBMIT
    assert set(hooks) == {"PreToolUse", "PostToolUse", "UserPromptSubmit"}


def test_reading_i_the_registered_script_is_the_hook_that_refuses(tmp_path):
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
    command = (hooks.get("PreToolUse") or [{"hooks": [{"command": ""}]}])[0]["hooks"][0]["command"]
    assert command == COMMAND
    assert (PLUGIN / "hooks" / "wall.py").is_file()
    fx = Fx(tmp_path)
    assert fx.call(*READ_WALLED) == refusal(DEV_LINE.format("tests/run_a.bat"))


def test_reading_i_the_hook_imports_the_taskcontract_that_sits_beside_it(tmp_path):
    decoy = tmp_path / "decoy" / "taskcontract"
    decoy.mkdir(parents=True)
    (decoy / "__init__.py").write_text('raise ImportError("the decoy package")\n',
                                       encoding="utf-8")
    fx = Fx(tmp_path)
    assert fx.call(*READ_WALLED, env={"PYTHONPATH": str(decoy.parent)}) == refusal(
        DEV_LINE.format("tests/run_a.bat"))


# --- done_means 1 and reading (h): python -m taskcontract interface -------------------

def interface(tmp_path: Path, file: str, source: str | None = None):
    """(exit code, stdout, stderr) of `python -m taskcontract interface FILE`, run from
    tmp_path/work with the plugin's package first on the path; `source` is written to FILE."""
    work = tmp_path / "work"
    work.mkdir(exist_ok=True)
    if source is not None:
        path = work / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    paths = [str(PLUGIN)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(paths), "PYTHONUTF8": "1"}
    done = subprocess.run([sys.executable, "-P", "-m", "taskcontract", "interface", file],
                          cwd=work, env=env, capture_output=True, encoding="utf-8",
                          errors="replace", timeout=100, creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


def lines(*rows: str) -> str:
    return "".join(row + "\n" for row in rows)


FUNCTIONS = '''\
"""Module docstring: never printed."""

import os

VALUE = 3
ANNOTATED: int = 4


def read(root: Path) -> Workflow:
    """The workflow file's nodes, edges and rows; raises on a structural fault."""
    return os.fspath(root)


def settings(root: Path, node_id: str) -> Settings:
    """One node's agent model and effort, read from the settings table.

    Raises when the table has no row.
    """

    def inner():
        """Nested: never printed."""

    VALUE = 5
    return inner


def _private(x):
    """Private: never printed."""


def bare(a, b=2, *args, c=3, **kwargs):
    return a


async def fetch(url: str) -> bytes:
    """Fetch the url."""
    return b""


__all__ = ["read"]
'''


def test_done_means_interface_prints_each_public_signature_and_docstring_and_no_body(tmp_path):
    assert interface(tmp_path, "mod.py", FUNCTIONS) == (0, lines(
        "def read(root: Path) -> Workflow:",
        '    """The workflow file\'s nodes, edges and rows; raises on a structural fault."""',
        "def settings(root: Path, node_id: str) -> Settings:",
        '    """One node\'s agent model and effort, read from the settings table. ..."""',
        "def bare(a, b=2, *args, c=3, **kwargs):",
        "async def fetch(url: str) -> bytes:",
        '    """Fetch the url."""',
    ), "")


def test_reading_h_a_one_line_docstring_gets_no_dots_and_a_longer_one_gets_them(tmp_path):
    source = ('def one():\n    """Only line."""\n\n\n'
              'def two():\n    """First line.\n\n    Second paragraph.\n    """\n\n\n'
              'def three():\n    """First line.\n    Second line, no gap."""\n')
    assert interface(tmp_path, "docs.py", source) == (0, lines(
        "def one():", '    """Only line."""',
        "def two():", '    """First line. ..."""',
        "def three():", '    """First line. ..."""'), "")


def test_reading_h_a_name_without_a_docstring_prints_its_header_line_alone(tmp_path):
    source = "def plain(a, b):\n    return a\n\n\nclass Empty:\n    pass\n\n\ndef after():\n    pass\n"
    assert interface(tmp_path, "plain.py", source) == (0, lines(
        "def plain(a, b):", "class Empty:", "def after():"), "")


CLASSES = '''\
@dataclass
class Settings(Base):
    """Agent settings.

    More text.
    """

    model: str
    effort: str = "high"
    _hidden: int = 0
    LIMIT = 3

    def __init__(self, model: str) -> None:
        """Build one."""
        self.model = model

    def render(self, width=80) -> str:
        """Render it."""

    def _helper(self):
        """Not public."""

    def __repr__(self):
        return ""

    @staticmethod
    def make(name: str) -> Settings:
        return Settings(name)

    async def load(self) -> None:
        pass

    class Inner:
        def f(self): ...


class K(Base, metaclass=Meta):
    count: int
    def run(self):
        pass
'''


def test_reading_h_a_class_prints_its_header_annotated_fields_and_public_methods(tmp_path):
    assert interface(tmp_path, "classes.py", CLASSES) == (0, lines(
        "@dataclass",
        "class Settings(Base):",
        '    """Agent settings. ..."""',
        "    model: str",
        "    effort: str",
        "    def __init__(self, model: str) -> None:",
        '        """Build one."""',
        "    def render(self, width=80) -> str:",
        '        """Render it."""',
        "    @staticmethod",
        "    def make(name: str) -> Settings:",
        "    async def load(self) -> None:",
        "class K(Base, metaclass=Meta):",
        "    count: int",
        "    def run(self):",
    ), "")


def test_reading_h_decorators_print_above_their_header(tmp_path):
    source = ('import functools\n\n\n@functools.lru_cache(maxsize=None)\n@staticmethod\n'
              'def cached(n: int) -> int:\n    """Memo."""\n    return n\n\n\n'
              '@dataclass(frozen=True)\nclass Point:\n    x: int\n')
    assert interface(tmp_path, "deco.py", source) == (0, lines(
        "@functools.lru_cache(maxsize=None)", "@staticmethod",
        "def cached(n: int) -> int:", '    """Memo."""',
        "@dataclass(frozen=True)", "class Point:", "    x: int"), "")


def test_reading_h_a_header_that_spans_lines_prints_as_one_line(tmp_path):
    source = ('def long_one(\n    first: int,\n    second: str,\n    *rest,\n) -> None:\n'
              '    """Spans."""\n\n\n'
              'class Wide(\n    Base,\n    Other,\n):\n    def meth(\n        self,\n'
              '        a: int,\n    ) -> int:\n        """Also spans."""\n')
    assert interface(tmp_path, "wide.py", source) == (0, lines(
        "def long_one(first: int, second: str, *rest) -> None:", '    """Spans."""',
        "class Wide(Base, Other):",
        "    def meth(self, a: int) -> int:", '        """Also spans."""'), "")


def test_reading_h_names_print_in_file_order(tmp_path):
    source = ("def zeta():\n    pass\n\n\nclass Alpha:\n    pass\n\n\n"
              "def middle():\n    pass\n\n\nclass Beta:\n    pass\n\n\ndef alpha():\n    pass\n")
    assert interface(tmp_path, "order.py", source) == (0, lines(
        "def zeta():", "class Alpha:", "def middle():", "class Beta:", "def alpha():"), "")


def test_reading_h_a_file_with_no_public_name_prints_nothing_and_exits_0(tmp_path):
    source = '"""Only private names."""\n\nX = 1\n\n\ndef _a():\n    pass\n\n\nclass _B:\n    pass\n'
    assert interface(tmp_path, "quiet.py", source) == (0, "", "")
    assert interface(tmp_path, "empty.py", "") == (0, "", "")


def test_reading_h_the_file_is_read_as_given_and_the_header_keeps_text_the_body_does_not(tmp_path):
    source = ('def read(path: str, mode: str = "r") -> str:\n    """Read it."""\n'
              '    secret = "never printed"\n    return secret\n')
    code, out, err = interface(tmp_path, "pkg/sub/mod.py", source)
    assert (code, err) == (0, "")
    assert out.splitlines()[0] == "def read(path: str, mode: str='r') -> str:"
    assert out.splitlines()[1] == '    """Read it."""'
    assert len(out.splitlines()) == 2 and "secret" not in out


# --- done_means 1: the three refusals, checked in order ------------------------------

def test_done_means_a_file_that_is_not_python_exits_2_with_the_designs_line(tmp_path):
    assert interface(tmp_path, "notes.txt", "def f(): pass\n") == (
        2, "", "No interface for notes.txt: only a .py file has one.\n")
    assert interface(tmp_path, "src/engine.cpp", "int main() {}\n") == (
        2, "", "No interface for src/engine.cpp: only a .py file has one.\n")


def test_done_means_a_missing_file_exits_2_with_the_designs_line(tmp_path):
    assert interface(tmp_path, "missing.py") == (
        2, "", "No interface for missing.py: no such file.\n")
    assert interface(tmp_path, "pkg/gone.py") == (
        2, "", "No interface for pkg/gone.py: no such file.\n")


def test_done_means_a_py_file_that_does_not_parse_exits_2_with_the_line_and_the_message(tmp_path):
    source = "x = 1\ndef broken(:\n    pass\n"
    with pytest.raises(SyntaxError) as raised:
        ast.parse(source)
    exc = raised.value
    assert exc.lineno == 2
    assert interface(tmp_path, "broken.py", source) == (
        2, "", f"No interface for broken.py: line {exc.lineno} does not parse: {exc.msg}.\n")


def test_done_means_the_checks_run_in_the_designs_order(tmp_path):
    # not .py first: a missing .txt file and an unparseable .txt file are both "only a .py file"
    assert interface(tmp_path, "absent.txt") == (
        2, "", "No interface for absent.txt: only a .py file has one.\n")
    assert interface(tmp_path, "bad.txt", "def broken(:\n") == (
        2, "", "No interface for bad.txt: only a .py file has one.\n")
    # then missing, then unparseable
    assert interface(tmp_path, "absent.py") == (
        2, "", "No interface for absent.py: no such file.\n")
    code, out, err = interface(tmp_path, "bad.py", "def broken(:\n")
    assert (code, out) == (2, "")
    assert err.startswith("No interface for bad.py: line 1 does not parse: ") and err.endswith(".\n")
