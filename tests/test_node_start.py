"""Node-start suite (contract: small-session-flow, unit w3-node-start).

The unit adds `python -m taskcontract node <id> [--print] [--root DIR]`, the
command the design draws in Interfaces. It reads the node's agent model and
effort from `<root>/.sdlc/workflow.md` through w2's reader, prints
`Node {id}: claude --model {M} --effort {E}` on stdout, then starts `claude`
in the same terminal and exits with its exit code; `--print` prints the line
and starts nothing. Every refusal goes to stderr, exits 1 and starts nothing.

The command runs in-process through `taskcontract.__main__.main(argv)`, so a
run against a prototype imports the prototype's package. SC2.1 and SC2.2 run
through `--print` on a scratch root that holds only a copy of the real
workflow file, found through the `taskcontract` package, with one cell of
one row changed. The start path runs against a stand-in `claude` on a PATH
the test sets to a folder holding only the stand-in, so no test can start
the real `claude`; the stand-in records its arguments and exits with a code
the test chooses. A spy on `subprocess.Popen` records the argument list the
command starts and the options it starts it with.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest

import taskcontract
from taskcontract.__main__ import main

ROOT = Path(taskcontract.__file__).resolve().parents[1]
WORKFLOW = ROOT / ".sdlc" / "workflow.md"

MODEL, EFFORT = 1, 2  # the cells of a settings row, after the node's id
FULL_ID = "claude-opus-4-1-20250805"

# Windows creation flags that would take the session out of this terminal.
NEW_CONSOLE, DETACHED, NO_WINDOW = 0x00000010, 0x00000008, 0x08000000

STAND_IN = '''\
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
calls = here / "calls.json"
record = json.loads(calls.read_text(encoding="utf-8")) if calls.is_file() else []
record.append({"program": sys.argv[1], "args": sys.argv[2:]})
calls.write_text(json.dumps(record), encoding="utf-8")
sys.exit(int((here / "exit_code.txt").read_text(encoding="utf-8")))
'''


# --- the design's lines, word for word ---

def node_line(node: str, model: str, effort: str) -> str:
    return f"Node {node}: claude --model {model} --effort {effort}"


def no_file(node: str) -> str:
    return f"Node {node} did not start: no workflow file at .sdlc/workflow.md."


def no_claude(node: str) -> str:
    return f"Node {node} did not start: no claude command on the path."


def no_model(node: str) -> str:
    return f"Node {node} did not start: its row in the workflow file has no agent model."


def no_effort(node: str) -> str:
    return f"Node {node} did not start: its row in the workflow file has no effort."


def no_such_node(node: str) -> str:
    return (f"No node {node} in .sdlc/workflow.md. "
            "Nodes: feature, design, execution, review.")


def no_row(node: str) -> str:
    return f"Node {node} has no row in the settings table of .sdlc/workflow.md."


def row_no_node(row: str) -> str:
    return f"Row {row} in the settings table of .sdlc/workflow.md has no node in the diagram."


def no_label(a: str, b: str) -> str:
    return f"The edge from {a} to {b} in .sdlc/workflow.md names no file."


# --- the workflow file and its scratch copies ---

def real_text() -> str:
    assert WORKFLOW.is_file(), f"no workflow file at {WORKFLOW}"
    return WORKFLOW.read_text(encoding="utf-8")


def _row_cells(raw: str) -> list[str] | None:
    text = raw.strip()
    if not text.startswith("|"):
        return None
    return [cell.strip() for cell in text.strip("|").split("|")]


def with_cell(text: str, node: str, column: int, value: str) -> str:
    """`text` with one cell of one node's row changed, and nothing else."""
    out, hits = [], 0
    for raw in text.splitlines():
        cells = _row_cells(raw)
        if cells and cells[0] == node:
            cells[column] = value
            raw = "| " + " | ".join(cells) + " |"
            hits += 1
        out.append(raw)
    assert hits == 1, f"the workflow file has {hits} rows for {node}"
    changed = "\n".join(out) + "\n"
    before = text.splitlines()
    after = changed.splitlines()
    assert len(before) == len(after)
    assert sum(1 for a, b in zip(before, after) if a != b) == 1
    return changed


def without_row(text: str, node: str) -> str:
    kept = [raw for raw in text.splitlines()
            if not ((_row_cells(raw) or [None])[0] == node)]
    assert len(kept) == len(text.splitlines()) - 1
    return "\n".join(kept) + "\n"


def with_extra_row(text: str, row: str) -> str:
    out = []
    for raw in text.splitlines():
        out.append(raw)
        if (_row_cells(raw) or [None])[0] == "review":
            out.append(f"| {row} | opus | high | engineer seat |")
    return "\n".join(out) + "\n"


def scratch(tmp_path: Path, text: str | None, name: str = "root") -> Path:
    """A root that holds only `.sdlc/workflow.md` with `text`, or nothing."""
    root = tmp_path / name
    root.mkdir()
    if text is not None:
        (root / ".sdlc").mkdir()
        (root / ".sdlc" / "workflow.md").write_bytes(text.encode("utf-8"))
    return root


def files_under(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def node(capsys, *args: str) -> tuple[object, str, str]:
    """Run `taskcontract node ARGS` in-process: (exit code, stdout, stderr)."""
    try:
        code = main(["node", *args])
    except SystemExit as exc:
        code = exc.code
    out, err = capsys.readouterr()
    return code, out, err


# --- the PATH each test sets, and the stand-in claude ---

class Path_:
    """A PATH holding one folder this test built, a spy on subprocess.Popen,
    and the stand-in `claude` once `install` puts it there."""

    def __init__(self, tmp_path: Path, monkeypatch):
        self.bin = tmp_path / "bin"
        self.bin.mkdir()
        cwd = tmp_path / "cwd"
        cwd.mkdir()
        monkeypatch.setenv("PATH", str(self.bin))
        if os.name == "nt":
            monkeypatch.setenv("PATHEXT", ".COM;.EXE;.BAT;.CMD")
        monkeypatch.chdir(cwd)
        self.popens: list[dict] = []
        self.on_start = None
        real = subprocess.Popen
        spy = self

        class Spy(real):
            def __init__(self, args, *rest, **kwargs):
                spy.popens.append({"args": args, "rest": rest, "kwargs": kwargs})
                if spy.on_start is not None:
                    spy.on_start()
                super().__init__(args, *rest, **kwargs)

        monkeypatch.setattr(subprocess, "Popen", Spy)

    def install(self, exit_code: int = 0) -> None:
        script = self.bin / "stand_in.py"
        script.write_text(STAND_IN, encoding="utf-8")
        (self.bin / "exit_code.txt").write_text(str(exit_code), encoding="utf-8")
        if os.name == "nt":
            (self.bin / "claude.cmd").write_text(
                f'@echo off\r\n"{sys.executable}" "{script}" "%~f0" %*\r\n'
                "exit /b %ERRORLEVEL%\r\n", encoding="utf-8", newline="")
        else:
            shim = self.bin / "claude"
            shim.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" "$0" "$@"\n',
                            encoding="utf-8", newline="")
            shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def calls(self) -> list[dict]:
        calls = self.bin / "calls.json"
        return json.loads(calls.read_text(encoding="utf-8")) if calls.is_file() else []

    def started(self) -> list[list[str]]:
        """Each argument list given to subprocess.Popen, as strings."""
        out = []
        for popen in self.popens:
            args = popen["args"]
            out.append([os.fspath(a) for a in args] if not isinstance(args, (str, bytes))
                       else [args])
        return out


@pytest.fixture
def bare(tmp_path, monkeypatch) -> Path_:
    """PATH holds one empty folder: no claude anywhere."""
    return Path_(tmp_path, monkeypatch)


@pytest.fixture
def stand_in(tmp_path, monkeypatch) -> Path_:
    """PATH holds one folder with the stand-in claude, which exits 0."""
    path = Path_(tmp_path, monkeypatch)
    path.install(0)
    return path


def assert_refused(code, out, err, lines, path: Path_) -> None:
    assert err.splitlines() == lines, f"stderr was {err!r}"
    assert out == "", f"stdout was {out!r}"
    assert code == 1
    assert path.popens == [], "node started a process"
    assert path.calls() == [], "node started claude"


# --- SC2.1 and SC2.2 through --print, on the real file with one cell changed ---

def test_sc2_1_print_follows_a_changed_agent_model_with_no_other_file(tmp_path, capsys, bare):
    before = real_text()
    text = with_cell(before, "design", MODEL, "sonnet")
    root = scratch(tmp_path, text)
    code, out, err = node(capsys, "design", "--print", "--root", str(root))
    assert out.splitlines() == [node_line("design", "sonnet", "xhigh")], f"stderr: {err!r}"
    assert err == ""
    assert code == 0
    assert files_under(root) == {".sdlc/workflow.md": text.encode("utf-8")}
    assert real_text() == before


def test_sc2_1_print_follows_a_full_model_id_in_the_row(tmp_path, capsys, bare):
    text = with_cell(real_text(), "execution", MODEL, FULL_ID)
    root = scratch(tmp_path, text)
    code, out, err = node(capsys, "execution", "--print", "--root", str(root))
    assert out.splitlines() == [node_line("execution", FULL_ID, "high")], f"stderr: {err!r}"
    assert code == 0
    assert files_under(root) == {".sdlc/workflow.md": text.encode("utf-8")}


def test_sc2_2_print_follows_a_changed_effort_with_no_other_file(tmp_path, capsys, bare):
    before = real_text()
    text = with_cell(before, "review", EFFORT, "low")
    root = scratch(tmp_path, text)
    code, out, err = node(capsys, "review", "--print", "--root", str(root))
    assert out.splitlines() == [node_line("review", "opus", "low")], f"stderr: {err!r}"
    assert err == ""
    assert code == 0
    assert files_under(root) == {".sdlc/workflow.md": text.encode("utf-8")}
    assert real_text() == before


# --- SC2.1 and SC2.2 on the start path: claude gets the changed row ---

def test_sc2_1_start_passes_a_changed_agent_model_to_claude(tmp_path, capsys, stand_in):
    text = with_cell(real_text(), "feature", MODEL, "haiku")
    root = scratch(tmp_path, text)
    code, out, err = node(capsys, "feature", "--root", str(root))
    assert [c["args"] for c in stand_in.calls()] == [["--model", "haiku", "--effort", "xhigh"]], \
        f"stderr: {err!r}"
    assert out.splitlines() == [node_line("feature", "haiku", "xhigh")]
    assert code == 0
    assert files_under(root) == {".sdlc/workflow.md": text.encode("utf-8")}


def test_sc2_2_start_passes_a_changed_effort_to_claude(tmp_path, capsys, stand_in):
    text = with_cell(real_text(), "execution", EFFORT, "medium")
    root = scratch(tmp_path, text)
    code, out, err = node(capsys, "execution", "--root", str(root))
    assert [c["args"] for c in stand_in.calls()] == [["--model", "sonnet", "--effort", "medium"]], \
        f"stderr: {err!r}"
    assert out.splitlines() == [node_line("execution", "sonnet", "medium")]
    assert code == 0
    assert files_under(root) == {".sdlc/workflow.md": text.encode("utf-8")}


# --- done_means: the real file's lines, and --root ---

def test_done_means_real_file_prints_the_designs_line_for_design(capsys, bare):
    code, out, err = node(capsys, "design", "--print", "--root", str(ROOT))
    assert out == "Node design: claude --model opus --effort xhigh\n", f"stderr: {err!r}"
    assert err == ""
    assert code == 0


def test_done_means_real_file_prints_each_nodes_row(capsys, bare):
    rows = {"feature": ("opus", "xhigh"), "design": ("opus", "xhigh"),
            "execution": ("sonnet", "high"), "review": ("opus", "high")}
    for name, (model, effort) in rows.items():
        code, out, err = node(capsys, name, "--print", "--root", str(ROOT))
        assert out.splitlines() == [node_line(name, model, effort)], f"stderr: {err!r}"
        assert code == 0


def test_reading_e_root_defaults_to_the_current_folder(tmp_path, capsys, bare, monkeypatch):
    root = scratch(tmp_path, with_cell(real_text(), "design", EFFORT, "max"))
    monkeypatch.chdir(root)
    code, out, err = node(capsys, "design", "--print")
    assert out.splitlines() == [node_line("design", "opus", "max")], f"stderr: {err!r}"
    assert code == 0


def test_reading_e_root_option_wins_over_the_current_folder(tmp_path, capsys, bare, monkeypatch):
    here = scratch(tmp_path, with_cell(real_text(), "design", MODEL, "sonnet"), "here")
    there = scratch(tmp_path, with_cell(real_text(), "design", MODEL, "haiku"), "there")
    monkeypatch.chdir(here)
    code, out, err = node(capsys, "design", "--print", "--root", str(there))
    assert out.splitlines() == [node_line("design", "haiku", "xhigh")], f"stderr: {err!r}"
    assert code == 0


# --- reading (a): --print neither looks for claude nor starts it ---

def test_reading_a_print_needs_no_claude_on_the_path(tmp_path, capsys, bare, monkeypatch):
    looked: list[str] = []
    real_which = shutil.which
    monkeypatch.setattr(shutil, "which", lambda cmd, *a, **k: looked.append(cmd) or real_which(cmd, *a, **k))
    root = scratch(tmp_path, real_text())
    code, out, err = node(capsys, "design", "--print", "--root", str(root))
    assert out == node_line("design", "opus", "xhigh") + "\n", f"stderr: {err!r}"
    assert err == ""
    assert code == 0
    assert "claude" not in looked, "--print looked for claude"
    assert bare.popens == []


def test_reading_a_print_starts_nothing_with_claude_on_the_path(tmp_path, capsys, stand_in):
    root = scratch(tmp_path, real_text())
    code, out, err = node(capsys, "design", "--print", "--root", str(root))
    assert out == node_line("design", "opus", "xhigh") + "\n", f"stderr: {err!r}"
    assert code == 0
    assert stand_in.calls() == [], "--print started claude"
    assert stand_in.popens == [], "--print started a process"


# --- readings (b), (c), (d): the start ---

def test_reading_b_start_runs_the_which_path_with_model_and_effort(tmp_path, capsys, stand_in):
    root = scratch(tmp_path, real_text())
    found = shutil.which("claude")
    assert found, "the test's stand-in is not on its PATH"
    code, out, err = node(capsys, "design", "--root", str(root))
    assert stand_in.started() == [[found, "--model", "opus", "--effort", "xhigh"]], \
        f"stderr: {err!r}"
    calls = stand_in.calls()
    assert [c["args"] for c in calls] == [["--model", "opus", "--effort", "xhigh"]]
    assert os.path.normcase(os.path.abspath(calls[0]["program"])) == \
        os.path.normcase(os.path.abspath(found))
    assert out == "Node design: claude --model opus --effort xhigh\n"
    assert err == ""


def test_reading_b_start_prints_the_line_before_claude_starts(tmp_path, capsys, stand_in):
    root = scratch(tmp_path, real_text())
    seen: list[str] = []
    stand_in.on_start = lambda: seen.append(capsys.readouterr().out)
    code, out, err = node(capsys, "design", "--root", str(root))
    assert seen == ["Node design: claude --model opus --effort xhigh\n"], f"stderr: {err!r}"
    assert out == ""
    assert code == 0


def test_constraint_4_start_uses_an_argument_list_no_shell_same_terminal(tmp_path, capsys, stand_in):
    root = scratch(tmp_path, real_text())
    code, out, err = node(capsys, "review", "--root", str(root))
    assert len(stand_in.popens) == 1, f"stderr: {err!r}"
    popen = stand_in.popens[0]
    kwargs = popen["kwargs"]
    assert isinstance(popen["args"], (list, tuple)), "the start is not an argument list"
    assert not kwargs.get("shell"), "the start goes through a shell"
    assert not popen["rest"], "the start passes Popen options by position"
    flags = kwargs.get("creationflags") or 0
    assert flags & (NEW_CONSOLE | DETACHED | NO_WINDOW) == 0, "the start leaves this terminal"
    assert not kwargs.get("start_new_session"), "the start leaves this terminal's session"
    for stream in ("stdin", "stdout", "stderr"):
        assert kwargs.get(stream) is None, f"the start redirects {stream}"
    assert code == 0


@pytest.mark.parametrize("exit_code", [0, 3, 7])
def test_reading_d_node_exits_with_claudes_exit_code(tmp_path, capsys, stand_in, exit_code):
    stand_in.install(exit_code)
    root = scratch(tmp_path, real_text())
    code, out, err = node(capsys, "design", "--root", str(root))
    assert len(stand_in.calls()) == 1, f"stderr: {err!r}"
    assert out == node_line("design", "opus", "xhigh") + "\n"
    assert code == exit_code


def test_reading_c_no_claude_on_the_path_prints_only_the_refusal(tmp_path, capsys, bare):
    root = scratch(tmp_path, real_text())
    code, out, err = node(capsys, "design", "--root", str(root))
    assert_refused(code, out, err, [no_claude("design")], bare)


# --- ruling 1: no workflow file ---

def test_ruling_1_no_workflow_file_refuses_and_starts_nothing(tmp_path, capsys, stand_in):
    root = scratch(tmp_path, None)
    code, out, err = node(capsys, "design", "--root", str(root))
    assert_refused(code, out, err, [no_file("design")], stand_in)
    assert files_under(root) == {}


def test_ruling_1_no_workflow_file_refuses_under_print(tmp_path, capsys, bare):
    root = scratch(tmp_path, None)
    code, out, err = node(capsys, "execution", "--print", "--root", str(root))
    assert_refused(code, out, err, [no_file("execution")], bare)


# --- reading (f) and the no-node refusal ---

@pytest.mark.parametrize("asked", ["Design", "DESIGN", "de sign", "build", " design"])
def test_reading_f_an_id_that_is_no_node_exactly_refuses(tmp_path, capsys, stand_in, asked):
    root = scratch(tmp_path, real_text())
    code, out, err = node(capsys, asked, "--root", str(root))
    assert_refused(code, out, err, [no_such_node(asked)], stand_in)


def test_reading_f_print_refuses_an_id_in_another_case(tmp_path, capsys, bare):
    root = scratch(tmp_path, real_text())
    code, out, err = node(capsys, "Review", "--print", "--root", str(root))
    assert_refused(code, out, err, [no_such_node("Review")], bare)


# --- SC2.3 and the reader's faults reach the command unchanged ---

@pytest.mark.parametrize("value", ["", "   "])
def test_sc2_3_row_with_no_agent_model_does_not_start(tmp_path, capsys, stand_in, value):
    root = scratch(tmp_path, with_cell(real_text(), "design", MODEL, value))
    code, out, err = node(capsys, "design", "--root", str(root))
    assert_refused(code, out, err, [no_model("design")], stand_in)


@pytest.mark.parametrize("value", ["", "   "])
def test_sc2_3_row_with_no_effort_does_not_start(tmp_path, capsys, stand_in, value):
    root = scratch(tmp_path, with_cell(real_text(), "review", EFFORT, value))
    code, out, err = node(capsys, "review", "--root", str(root))
    assert_refused(code, out, err, [no_effort("review")], stand_in)


def test_sc2_3_row_with_neither_value_gives_both_lines(tmp_path, capsys, stand_in):
    text = with_cell(with_cell(real_text(), "feature", MODEL, ""), "feature", EFFORT, "")
    root = scratch(tmp_path, text)
    code, out, err = node(capsys, "feature", "--root", str(root))
    assert_refused(code, out, err, [no_model("feature"), no_effort("feature")], stand_in)


def test_sc2_3_print_refuses_a_row_with_no_agent_model(tmp_path, capsys, bare):
    root = scratch(tmp_path, with_cell(real_text(), "execution", MODEL, ""))
    code, out, err = node(capsys, "execution", "--print", "--root", str(root))
    assert_refused(code, out, err, [no_model("execution")], bare)


def test_reader_fault_node_with_no_row_starts_nothing(tmp_path, capsys, stand_in):
    root = scratch(tmp_path, without_row(real_text(), "review"))
    code, out, err = node(capsys, "design", "--root", str(root))
    assert_refused(code, out, err, [no_row("review")], stand_in)


def test_reader_faults_reach_node_each_on_its_line_in_the_readers_order(tmp_path, capsys, stand_in):
    text = real_text().replace("-->|docs/features/{id}.md|", "-->")
    root = scratch(tmp_path, with_extra_row(text, "build"))
    code, out, err = node(capsys, "design", "--root", str(root))
    assert_refused(code, out, err, [no_label("feature", "design"), row_no_node("build")],
                   stand_in)


def test_reader_fault_print_refuses_a_row_with_no_node(tmp_path, capsys, bare):
    root = scratch(tmp_path, with_extra_row(real_text(), "build"))
    code, out, err = node(capsys, "design", "--print", "--root", str(root))
    assert_refused(code, out, err, [row_no_node("build")], bare)
