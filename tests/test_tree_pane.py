"""The pane suite for ADR 0031 (contract tree-view, unit t7-pane-face).

`taskcontract tree --follow` keeps a terminal pane on the current task. The
pane reads down to the current task, its last line: at each level of the
path (the top level, the contract, the unit) the other items fold into one
line with their counts by status, above the item on the path, and the items
on the path print in the whole tree's line format (SC2.1). With five
contracts of seven units each, the pane prints at most fifteen lines
(SC2.2). The pane scans its sources at most a second apart, renders at the
first scan after a change and renders nothing while nothing changes (SC2.3).

The pane watches the files under specs/, .sdlc/config.yaml, the files under
.sdlc/findings/, .sdlc/progress/ and docs/features/, and the kit's two name
lists; a file counts as changed when its modification time or its size
differs, and git is not watched. It keeps each contract's G0 verdict in
memory and recomputes it only when that contract's file or a file under
specs/vocabulary/ changes. In the pane only, a line longer than the width is
cut to the width, ending in `...`. Every `git status` the kit runs carries
`--no-optional-locks`, since the pane redraws while the user runs git.

The loop runs in-process: `follow(root, out, sleep=...)` takes an injected
sleep, which changes source files between scans and raises
KeyboardInterrupt to end the loop, as Ctrl-C does. No test waits on a real
second. A test that changes a file changes its size or moves its
modification time forward, since some file systems keep coarse times.
"""

from __future__ import annotations

import _thread
import importlib
import io
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
import yaml

from conftest import ROW, cut_lines, short_line, write_seat_roster
from taskcontract.__main__ import main

tree_module = importlib.import_module("taskcontract.tree")
tree_view = importlib.import_module("taskcontract.tree_view")
progress_module = importlib.import_module("taskcontract.progress")

CLEAR = "\x1b[H\x1b[2J"  # cursor home, then clear the screen: every render opens on it
HEAD = "1a2b3c4"
TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]
INTENT = ("A fixture contract for the pane suite; its units carry the "
          "sketch shapes that check ids come from.")
UNREADABLE = re.compile(
    r"^taskcontract tree: unreadable progress: \.sdlc/progress/beta\.yaml \(.+\)$")


@pytest.fixture(autouse=True)
def _wide_and_outside_git(tmp_path, monkeypatch):
    """A wide pane unless a test sets its own width, and no repo above the fixture."""
    monkeypatch.setenv("COLUMNS", "500")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))


# --- the fixture repository -----------------------------------------------------

def _unit(uid, sketches, depends_on=None):
    unit = {
        "unit": "work for " + uid,
        "id": uid,
        "confirmed_by": ["user"],
        "done_means": "the work for " + uid + " is done",
        "acceptance_sketch": list(sketches),
    }
    if depends_on is not None:
        unit["depends_on"] = depends_on
    return unit


# alpha/a1-core checks SC1.1 and SC5.1+SC5.2; alpha/a2-edges checks sketch-1,
# SC2.1 and sketch-3; beta/b1-solo checks sketch-1.
ALPHA = [
    _unit("a1-core", ["verify the core prints (SC1.1)",
                      "verify both links print (SC5.1, SC5.2)"]),
    _unit("a2-edges", ["verify an edge holds",
                       "verify it again (SC2.1)",
                       "verify it once more (SC2.1)"], depends_on=["a1-core"]),
]
BETA = [_unit("b1-solo", ["verify the price rounds (by the house rule)"])]
LONE = [_unit("l1-lone", ["verify it holds"])]


def _contract(cid, units, **fields):
    """A contract that reads ready-green; a field given as None is dropped."""
    doc = {
        "id": cid,
        "intent": INTENT,
        "scope": ["src/"],
        "non_goals": ["No other work"],
        "decomposition": units,
        "dependencies": [],
        "entities": [],
        "provenance": {"origin": "human-request"},
    }
    for key, value in fields.items():
        if value is None:
            doc.pop(key)
        else:
            doc[key] = value
    return doc


def _finding(slug, gate, kind):
    return {
        "finding": slug, "date": "2026-09-22", "kit_pinned": "v0.14.0",
        "diagnostic": "none", "gate": gate, "kind": kind, "count": 1,
        "statement": "A fixture finding for the pane suite.", "proposal": "none",
    }


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _config(root, gates, **more):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates), **more})


def _repo(tmp_path, gates=("G0",)):
    """alpha and beta, both ready-green, with the given gates active and no progress."""
    root = tmp_path / "repo"
    _config(root, gates)
    _dump(root / "specs" / "alpha" / "contract.yaml", _contract("alpha", ALPHA))
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA))
    write_seat_roster(root)
    return root


def _at(clock):
    return f"2026-09-22T{clock}:00Z"


def _step(item, state, clock, **more):
    """A task-step record; on a unit or a contract id with `done`, a close."""
    return {"item": item, "state": state, "at": _at(clock), "head": HEAD, **more}


def _ran(item, run, expect, clock):
    return {"item": item, "run": run, "expect": expect,
            "command": "python -m pytest tests/", "dirty": False,
            "at": _at(clock), "head": HEAD}


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


def _append(path, text="\n# a note\n"):
    """Grow a file, so its size differs whatever its time reads."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


# --- driving the pane -----------------------------------------------------------

class Sleeper:
    """The injected sleep: each call notes its argument and the renders so
    far, then runs the next step; with no step left it raises
    KeyboardInterrupt, as Ctrl-C does."""

    def __init__(self, out, steps):
        self.out = out
        self.steps = list(steps)
        self.args = []
        self.renders = []  # renders written before each call
        self.texts = []    # the stream's text at each call

    def __call__(self, seconds):
        self.args.append(seconds)
        text = self.out.getvalue()
        self.renders.append(text.count(CLEAR))
        self.texts.append(text)
        if not self.steps:
            raise KeyboardInterrupt
        step = self.steps.pop(0)
        if step is not None:
            step()


def _follow():
    follow = getattr(tree_view, "follow", None)
    assert callable(follow), "taskcontract.tree_view has no follow(root, out, sleep=...)"
    return follow


def _pane(root, *steps, out=None):
    """(sleeper, renders) of one pane run: each step runs in one sleep, and
    the call after the last step ends the loop. Each render is its lines."""
    out = io.StringIO() if out is None else out
    sleeper = Sleeper(out, steps)
    code = _follow()(Path(root), out, sleep=sleeper)
    assert code == 0, f"the pane ended with {code!r}, not 0"
    return sleeper, _renders(out.getvalue())


def _renders(text):
    assert text.startswith(CLEAR), f"the pane output opens on {text[:20]!r}"
    return [chunk.splitlines() for chunk in text.split(CLEAR)[1:]]


def _whole(root, capsys):
    """The whole tree's lines by id, as `taskcontract tree` prints them."""
    code = main(["tree", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 0
    lines = {}
    for line in out.splitlines():
        match = ROW.match(line)
        if match:
            lines[match["id"]] = line
    return lines


# --- the SC2.1 fixture ----------------------------------------------------------

def _path_repo(tmp_path):
    """alpha, beta closed, two findings under the no-gate item; the current
    task is alpha/a2-edges/prove-red, the only task doing."""
    root = _repo(tmp_path)
    _dump(root / ".sdlc" / "findings" / "idea.yaml", _finding("idea", "none", "proposal"))
    _dump(root / ".sdlc" / "findings" / "other.yaml", _finding("other", "none", "friction"))
    _progress(root, "beta", _step("beta", "done", "09:00"))
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "10:00", by="user"),
              _step("alpha/a1-core/write-tests", "blocked", "10:01", reason="the runner is down"),
              _step("alpha/a2-edges/approve-tests", "done", "10:02", by="user"),
              _step("alpha/a2-edges/write-tests", "done", "10:03"),
              _step("alpha/a2-edges/prove-red", "doing", "10:04"),
              _ran("alpha/a2-edges/sketch-1", "green", "red", "10:05"))
    return root


# --- SC2.1 the path to the current task ------------------------------------------

def test_sc2_1_the_pane_shows_the_path_and_folds_each_levels_other_items_into_one_line(
        tmp_path, capsys):
    root = _path_repo(tmp_path)
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert renders == [[
        "specs/alpha/contract.yaml > alpha > a2-edges > prove-red",  # the where-am-I line
        "3 more: 2 to do, 1 done",                    # gates/G0, gates/none, beta
        whole["alpha"],
        "  2 more: 1 done, 1 blocked",                # alpha/G0, alpha/a1-core
        short_line(whole["alpha/a2-edges"]),
        "    9 more: 6 to do, 2 done, 1 failed",      # the other tasks and the checks
        short_line(whole["alpha/a2-edges/prove-red"]),
    ]]
    assert whole["alpha/a2-edges/prove-red"].split()[1:4] == ["[doing]", "current", "|"]


def test_sc2_1_a_level_with_no_other_item_prints_no_fold_line(tmp_path, capsys):
    root = tmp_path / "repo"
    _config(root, [])  # no gate item, no verdict
    _dump(root / "specs" / "lone" / "contract.yaml", _contract("lone", LONE))
    write_seat_roster(root)
    _progress(root, "lone", _step("lone/l1-lone/approve-tests", "doing", "10:00"))
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert renders == [[
        "waiting on a seat: approve-tests for lone/l1-lone",  # the current task is an approval
        "specs/lone/contract.yaml > lone > l1-lone > approve-tests",  # the where-am-I line
        whole["lone"],
        short_line(whole["lone/l1-lone"]),
        "    7 more: 7 to do",  # six tasks and one check
        short_line(whole["lone/l1-lone/approve-tests"]),
    ]]
    assert "waiting on a seat" in whole["lone/l1-lone/approve-tests"]


def test_sc2_1_with_no_current_task_the_pane_shows_the_root_folded(tmp_path, capsys):
    root = _repo(tmp_path)
    _dump(root / ".sdlc" / "findings" / "idea.yaml", _finding("idea", "none", "proposal"))
    _dump(root / "specs" / "delta" / "contract.yaml",
          _contract("delta", LONE, intent="Too short."))  # draft-red: failed
    # the second render: beta closed, the latest contract, with no task to do
    _, renders = _pane(root, lambda: _progress(root, "beta", _step("beta", "done", "09:00")))
    assert renders == [
        ["no current task", "5 items: 4 to do, 1 failed"],
        ["no current task", "5 items: 3 to do, 1 done, 1 failed"],
    ]


# --- SC2.2 fifteen lines ------------------------------------------------------------

def test_sc2_2_five_contracts_of_seven_units_print_at_most_fifteen_lines(tmp_path, capsys):
    root = tmp_path / "repo"
    _config(root, ["G0"])
    write_seat_roster(root)
    _dump(root / ".sdlc" / "findings" / "idea.yaml", _finding("idea", "none", "proposal"))
    for c in range(1, 6):
        units = [_unit(f"u{u}", [f"verify part {u} holds (SC{c}.{u})"],
                       depends_on=[f"u{u - 1}"] if u > 1 else None)
                 for u in range(1, 8)]
        _dump(root / "specs" / f"work-{c}" / "contract.yaml", _contract(f"work-{c}", units))
    _progress(root, "work-5",
              _step("work-5/u6", "done", "09:00"),
              _step("work-5/u7/approve-tests", "done", "10:00", by="user"),
              _step("work-5/u7/write-tests", "doing", "10:01"))
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert len(renders) == 1
    lines = renders[0]
    assert len(lines) <= 15, lines
    assert whole["work-5"] in lines
    for rid in ("work-5/u7", "work-5/u7/write-tests"):
        assert short_line(whole[rid]) in lines, rid
    assert lines[-1] == short_line(whole["work-5/u7/write-tests"])
    assert "current" in lines[-1].split()


# --- SC2.3 redraw on change, and only on change ---------------------------------------

def test_sc2_3_the_first_scan_after_a_change_renders_and_scans_are_at_most_a_second_apart(
        tmp_path, capsys):
    root = _repo(tmp_path)
    start = _step("alpha/a2-edges/write-tests", "doing", "10:00")
    _progress(root, "alpha", start)
    sleeper, renders = _pane(
        root,
        lambda: _progress(root, "alpha", start,
                          _step("alpha/a2-edges/prove-red", "doing", "10:05")),
        None, None)
    whole = _whole(root, capsys)
    assert sleeper.args and all(0 < seconds <= 1 for seconds in sleeper.args), sleeper.args
    # one render at start, then one at the scan right after the change, then none
    assert sleeper.renders == [1, 2, 2, 2]
    assert len(renders) == 2
    assert renders[0][-1].split()[0] == "write-tests"
    assert renders[1][-1] == short_line(whole["alpha/a2-edges/prove-red"])


def test_sc2_3_while_no_source_changes_the_pane_renders_nothing_new_and_writes_no_file(
        tmp_path):
    root = _path_repo(tmp_path)
    before = _snapshot(root)
    sleeper, renders = _pane(root, None, None, None)
    assert len(renders) == 1
    assert sleeper.renders == [1, 1, 1, 1]
    assert len(set(sleeper.texts)) == 1  # not a byte more after the first render
    assert _snapshot(root) == before


def test_sc2_3_the_command_takes_follow_and_ctrl_c_exits_0_with_no_traceback(
        tmp_path, capsys, monkeypatch):
    root = _path_repo(tmp_path)
    slept = []

    def interrupt(seconds):
        slept.append(seconds)
        raise KeyboardInterrupt

    monkeypatch.setattr(time, "sleep", interrupt)
    # a pane that kept a real sleep would never end: interrupt it after 10 seconds
    watchdog = threading.Timer(10, _thread.interrupt_main)
    watchdog.start()
    exited = None
    try:
        code = main(["tree", "--follow", "--root", str(root)])
    except SystemExit as exc:  # argparse refuses an unknown option
        exited, code = exc.code, None
    finally:
        watchdog.cancel()
    captured = capsys.readouterr()
    assert exited is None, f"`tree --follow` exited {exited}: {captured.err}"
    assert slept, "the pane slept through the real time.sleep, not the one time holds"
    assert code == 0
    assert captured.err == ""
    renders = _renders(captured.out)
    assert len(renders) == 1
    assert renders[0][-1].split()[:3] == ["prove-red", "[doing]", "current"]


class _InterruptedOut(io.StringIO):
    """A stream that takes the first render, then meets Ctrl-C at the second."""

    def write(self, text):
        if CLEAR in text and CLEAR in self.getvalue():
            raise KeyboardInterrupt
        return super().write(text)


def test_ctrl_c_during_a_render_ends_the_pane_with_0(tmp_path):
    root = _path_repo(tmp_path)
    out = _InterruptedOut()
    sleeper = Sleeper(out, [lambda: _append(root / ".sdlc" / "config.yaml"), None])
    code = _follow()(root, out, sleep=sleeper)
    assert code == 0
    assert out.getvalue().count(CLEAR) == 1


# --- what the pane watches ---------------------------------------------------------------

def _kit_lists(tmp_path, monkeypatch):
    """Copies of the kit's two name lists, which the pane reads and watches."""
    kit = tmp_path / "kit"
    kit.mkdir()
    gates, tasks = kit / "gates.yaml", kit / "tasks.yaml"
    shutil.copyfile(tree_module.GATES_PATH, gates)
    shutil.copyfile(tree_module.TASKS_PATH, tasks)
    monkeypatch.setattr(tree_module, "GATES_PATH", gates)
    monkeypatch.setattr(tree_module, "TASKS_PATH", tasks)
    return kit


def _watch_repo(tmp_path, monkeypatch):
    """No active gate, so no render runs the validator or git."""
    root = _repo(tmp_path, gates=())
    _dump(root / ".sdlc" / "findings" / "idea.yaml", _finding("idea", "none", "proposal"))
    _progress(root, "alpha", _step("alpha/a1-core/write-tests", "doing", "10:00"))
    _append(root / "docs" / "features" / "beta.md", "# Beta\n")
    _append(root / "docs" / "guide.md", "# Guide\n")
    _append(root / "README.md", "# Repo\n")
    _append(root / ".sdlc" / "notes.txt", "notes\n")
    return root, _kit_lists(tmp_path, monkeypatch)


WATCHED = [
    pytest.param(lambda root, kit: _append(root / "specs" / "alpha" / "contract.yaml"),
                 id="a-contract-edited"),
    pytest.param(lambda root, kit: _dump(root / "specs" / "gamma" / "contract.yaml",
                                         _contract("gamma", LONE)),
                 id="a-new-contract"),
    pytest.param(lambda root, kit: (root / "specs" / "beta" / "contract.yaml").unlink(),
                 id="a-contract-deleted"),
    pytest.param(lambda root, kit: _append(root / "specs" / "alpha" / "notes" / "n.md", "n\n"),
                 id="a-new-file-deep-under-specs"),
    pytest.param(lambda root, kit: _append(root / "specs" / "vocabulary" / "intake-seat.yaml"),
                 id="a-vocabulary-term-edited"),
    pytest.param(lambda root, kit: _config(root, [], stack="rust"),
                 id="the-config-edited"),
    pytest.param(lambda root, kit: _dump(root / ".sdlc" / "findings" / "new.yaml",
                                         _finding("new", "none", "friction")),
                 id="a-new-finding"),
    pytest.param(lambda root, kit: (root / ".sdlc" / "findings" / "idea.yaml").unlink(),
                 id="a-finding-deleted"),
    pytest.param(lambda root, kit: _progress(root, "beta",
                                             _step("beta/b1-solo/write-tests", "doing", "09:00")),
                 id="a-new-progress-file"),
    pytest.param(lambda root, kit: _append(root / ".sdlc" / "progress" / "alpha.yaml"),
                 id="a-progress-file-edited"),
    pytest.param(lambda root, kit: _append(root / "docs" / "features" / "alpha.md", "# A\n"),
                 id="a-new-feature-doc"),
    pytest.param(lambda root, kit: _append(root / "docs" / "features" / "beta.md"),
                 id="a-feature-doc-edited"),
    pytest.param(lambda root, kit: _append(kit / "gates.yaml"), id="the-kits-gate-list"),
    pytest.param(lambda root, kit: _append(kit / "tasks.yaml"), id="the-kits-task-list"),
]

UNWATCHED = [
    pytest.param(lambda root, kit: _append(root / "README.md"), id="a-readme-edited"),
    pytest.param(lambda root, kit: _append(root / "docs" / "guide.md"),
                 id="a-doc-outside-features"),
    pytest.param(lambda root, kit: _append(root / "docs" / "other" / "alpha.md", "# A\n"),
                 id="a-new-doc-outside-features"),
    pytest.param(lambda root, kit: _append(root / ".sdlc" / "notes.txt"),
                 id="another-file-under-sdlc"),
    pytest.param(lambda root, kit: _append(root / "src" / "app.py", "x = 1\n"),
                 id="a-new-source-file"),
    pytest.param(lambda root, kit: _append(root / "specs-old" / "alpha.yaml", "a: 1\n"),
                 id="a-folder-named-like-specs"),
    pytest.param(lambda root, kit: _append(kit / "other.yaml", "a: 1\n"),
                 id="another-file-beside-the-kit-lists"),
]


@pytest.mark.parametrize("change", WATCHED)
def test_the_pane_renders_again_when_a_watched_source_changes(tmp_path, monkeypatch, change):
    root, kit = _watch_repo(tmp_path, monkeypatch)
    sleeper, _ = _pane(root, None, lambda: change(root, kit), None)
    assert sleeper.renders == [1, 1, 2, 2]


@pytest.mark.parametrize("change", UNWATCHED)
def test_the_pane_never_renders_again_when_any_other_file_changes(
        tmp_path, monkeypatch, change):
    root, kit = _watch_repo(tmp_path, monkeypatch)
    # the last step changes a watched file, so a pane that never renders again fails too
    sleeper, _ = _pane(root, None, lambda: change(root, kit), None,
                       lambda: _append(root / ".sdlc" / "progress" / "alpha.yaml"))
    assert sleeper.renders == [1, 1, 1, 1, 2]


def test_a_file_counts_as_changed_when_its_size_or_its_modification_time_differs(
        tmp_path, monkeypatch):
    root, _ = _watch_repo(tmp_path, monkeypatch)
    path = root / ".sdlc" / "progress" / "alpha.yaml"
    original = path.read_bytes()
    stat = path.stat()
    later = stat.st_mtime_ns + 5_000_000_000

    def same_size_later_time():
        path.write_bytes(original.replace(b"10:00", b"10:01"))
        os.utime(path, ns=(stat.st_atime_ns, later))

    def larger_same_time():
        path.write_bytes(original.replace(b"10:00", b"10:01") + b"# a note\n")
        os.utime(path, ns=(stat.st_atime_ns, later))

    def rewritten_as_it_was():
        path.write_bytes(original.replace(b"10:00", b"10:01") + b"# a note\n")
        os.utime(path, ns=(stat.st_atime_ns, later))

    sleeper, _ = _pane(root, same_size_later_time, larger_same_time, rewritten_as_it_was)
    assert path.stat().st_mtime_ns == later
    assert sleeper.renders == [1, 2, 3, 3]


@pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
def test_a_git_commit_alone_never_renders_the_pane_again(tmp_path, monkeypatch):
    root, _ = _watch_repo(tmp_path, monkeypatch)

    def git(*args):
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                       encoding="utf-8", errors="replace")

    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    git("config", "commit.gpgsign", "false")

    def commit():
        git("add", "-A")
        git("-c", "core.hooksPath=no-hooks", "commit", "-q", "-m", "seed")

    # the last step changes a watched file, so a pane that never renders again fails too
    sleeper, _ = _pane(root, commit, None,
                       lambda: _append(root / ".sdlc" / "progress" / "alpha.yaml"))
    assert sleeper.renders == [1, 1, 1, 2]


# --- the width ----------------------------------------------------------------------------

def test_in_follow_a_line_longer_than_the_width_is_cut_to_the_width_ending_in_dots(
        tmp_path, capsys, monkeypatch):
    root = _path_repo(tmp_path)
    _, (full,) = _pane(root)  # at 500 columns, every line whole
    assert full[0] == "specs/alpha/contract.yaml > alpha > a2-edges > prove-red"
    exact = len(full[2])      # the contract line, exactly as wide as the pane
    monkeypatch.setenv("COLUMNS", str(exact))

    def narrower():
        monkeypatch.setenv("COLUMNS", "40")
        _append(root / ".sdlc" / "config.yaml")  # a change that moves no line

    _, renders = _pane(root, narrower)
    assert renders[0] == cut_lines(full, exact)
    assert renders[0][2] == full[2]            # a line exactly the width stays whole
    assert renders[1] == cut_lines(full, 40)    # the width is read at each render
    assert any(line.endswith("...") and len(line) == 40 for line in renders[1])
    assert all(len(line) <= 40 for line in renders[1])
    # the whole tree, without --follow, prints every line whole at any width
    code = main(["tree", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 0 and full[2] in out.splitlines()


def test_in_follow_a_width_below_ten_columns_cuts_as_ten(tmp_path, monkeypatch):
    root = _path_repo(tmp_path)
    _, (full,) = _pane(root)
    monkeypatch.setenv("COLUMNS", "4")
    _, (narrow,) = _pane(root)
    assert narrow == cut_lines(full, 10)
    assert all(len(line) == 10 for line in narrow)


# --- the verdict cache -----------------------------------------------------------------------

def test_the_pane_recomputes_a_verdict_only_when_its_contract_or_the_vocabulary_changes(
        tmp_path, monkeypatch):
    root = _repo(tmp_path)
    _dump(root / "specs" / "gamma" / "contract.yaml", _contract("gamma", LONE))
    records = [_step("alpha/a1-core/write-tests", "doing", "10:00")]
    _progress(root, "alpha", *records)
    real = tree_module.g0_status
    calls = []

    def counted(path, schema):
        calls.append(Path(path).parent.name)
        return real(path, schema)

    monkeypatch.setattr(tree_module, "g0_status", counted)
    seen = []

    def noting(step):
        def run():
            seen.append(list(calls))
            calls.clear()
            if step is not None:
                step()
        return run

    sleeper, renders = _pane(
        root,
        noting(None),
        noting(lambda: _progress(root, "alpha", *records,
                                 _step("alpha/a1-core/approve-tests", "done", "10:05",
                                       by="user"))),
        noting(lambda: _append(root / "specs" / "alpha" / "notes.md", "n\n")),
        noting(lambda: _dump(root / "specs" / "alpha" / "contract.yaml",
                             _contract("alpha", ALPHA, intent="Too short."))),
        noting(lambda: _append(root / "specs" / "vocabulary" / "intake-seat.yaml")),
        noting(lambda: _append(root / "specs" / "beta" / "contract.yaml")),
        noting(None),
    )
    seen.append(list(calls))
    # the calls of: the first render, a scan with no change, then the renders
    # after a progress file, a file beside a contract, alpha's contract, a
    # vocabulary term and beta's contract changed, then a scan with no change
    assert [sorted(tick) for tick in seen] == [
        ["alpha", "beta", "gamma"], [], [], [], ["alpha"],
        ["alpha", "beta", "gamma"], ["beta"], []]
    assert sleeper.renders == [1, 1, 2, 3, 4, 5, 6, 6]
    assert all(render[0] == "specs/alpha/contract.yaml > alpha > a1-core > write-tests"
               for render in renders)
    # the recomputed verdict reads: alpha is draft-red from the fourth render on
    assert [render[2].split()[:2] for render in renders] == [
        ["alpha", "[doing]"], ["alpha", "[doing]"], ["alpha", "[doing]"],
        ["alpha", "[failed]"], ["alpha", "[failed]"], ["alpha", "[failed]"]]


# --- unreadable sources ---------------------------------------------------------------------------

def test_the_pane_prints_each_unreadable_source_on_stderr_at_each_render(tmp_path, capsys):
    root = _path_repo(tmp_path)
    (root / ".sdlc" / "progress" / "beta.yaml").write_text("records: [unclosed\n",
                                                           encoding="utf-8")
    _, renders = _pane(root, lambda: _append(root / ".sdlc" / "config.yaml"))
    err = capsys.readouterr().err.splitlines()
    assert len(renders) == 2
    assert len(err) == 2 and all(UNREADABLE.match(line) for line in err), err
    assert not any(line.startswith("taskcontract tree:") for render in renders
                   for line in render)
    assert renders[0][-1].split()[:3] == ["prove-red", "[doing]", "current"]


# --- git status takes no optional lock --------------------------------------------------------------

def _git_spy(monkeypatch):
    """Every argv the kit hands subprocess.run, as the progress module sees it."""
    calls = []
    real = progress_module.subprocess.run

    def spy(*args, **kwargs):
        argv = args[0] if args else kwargs.get("args")
        calls.append([str(part) for part in argv])
        return real(*args, **kwargs)

    monkeypatch.setattr(progress_module.subprocess, "run", spy)
    return calls


def _status_calls(calls):
    """The git calls whose subcommand is status."""
    return [argv for argv in calls
            if Path(argv[0]).name.lower() in ("git", "git.exe") and "status" in argv]


def _takes_no_lock(argv):
    return "--no-optional-locks" in argv and (
        argv.index("--no-optional-locks") < argv.index("status"))


def test_every_git_status_of_the_tree_and_progress_takes_no_optional_locks(
        tmp_path, capsys, monkeypatch):
    root = _repo(tmp_path)
    calls = _git_spy(monkeypatch)
    assert main(["tree", "--root", str(root)]) == 0
    assert main(["progress", "run", "alpha/a1-core/SC1.1", "--root", str(root),
                 "--", sys.executable, "-c", "pass"]) == 0
    assert main(["progress", "done", "alpha/a1-core/write-tests", "--root", str(root)]) == 0
    capsys.readouterr()
    status = _status_calls(calls)
    assert len(status) >= 3, calls  # the tree's, the run's and the done's
    assert all(_takes_no_lock(argv) for argv in status), status


def test_every_git_status_of_the_pane_takes_no_optional_locks(tmp_path, monkeypatch):
    root = _path_repo(tmp_path)
    calls = _git_spy(monkeypatch)
    _pane(root, lambda: _append(root / ".sdlc" / "progress" / "alpha.yaml"))
    status = _status_calls(calls)
    assert len(status) >= 2, calls  # each render reads the G0 verdict's dirty mark
    assert all(_takes_no_lock(argv) for argv in status), status


# --- the waiting line and the notify command ------------------------------------------------------
#
# When the current task is approve-tests or approve-commit, the pane's first
# line reads `waiting on a seat: {approval} for {unit}`, with the approval's
# task key and the unit's id, above the path and cut to the width like every
# line of the render, in the render's one write (SC8.1). The command at
# `tree: notify:` in .sdlc/config.yaml starts through the shell, as
# subprocess.Popen(command, shell=True, ...), once at each arrival: a render
# whose current task is an approval and differs from the previous render's,
# the first render included. It runs at the repo root with the pane's
# environment plus the approval's id in SDLC_NODE, its streams on DEVNULL
# (SC8.2). The pane never waits on it: at each tick it checks each command it
# started, and one that ended with a nonzero exit prints
# `notify failed, exit {code}: {command}` once, whole, on stderr (SC8.3). A
# start that raises OSError prints the line at once with code 127. A notify
# value that is not a string holding a non-blank command counts as unset.
#
# The tests spy on subprocess.Popen, where a call with shell=True is a notify
# start. A test that needs a command's effect waits for the process itself, a
# bounded real wait inside one injected sleep.

LIMIT = 10  # seconds: the bound on every real wait for a notify command
WAIT_LONE = "waiting on a seat: approve-tests for lone/l1-lone"

# Appends SDLC_NODE, the working folder and NOTIFY_TEST_MARK to <script>.log,
# writes to both streams, then exits with the given code.
LOG_SCRIPT = """\
import os
import sys
from pathlib import Path

fields = [os.environ.get("SDLC_NODE", "-"), os.getcwd(), os.environ.get("NOTIFY_TEST_MARK", "-")]
with Path(__file__).with_suffix(".log").open("a", encoding="utf-8") as log:
    log.write("\\t".join(fields) + "\\n")
print("notify-out-marker")
print("notify-err-marker", file=sys.stderr)
sys.exit({code})
"""

# Holds until <script>.release exists, at most five seconds, then writes
# <script>.ended with how it stopped.
HOLD_SCRIPT = """\
import time
from pathlib import Path

here = Path(__file__)
deadline = time.monotonic() + 5
while not here.with_suffix(".release").exists() and time.monotonic() < deadline:
    time.sleep(0.01)
released = here.with_suffix(".release").exists()
here.with_suffix(".ended").write_text("released" if released else "timed out", encoding="utf-8")
"""


def _script(tmp_path, name, text):
    """A script under tmp_path, and the command that runs it through either
    shell (cmd.exe or /bin/sh): the interpreter's path, then the script's."""
    path = tmp_path / "scripts" / f"{name}.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path, f'"{sys.executable}" "{path}"'


def _logger(tmp_path, code=0):
    """(the log path, the command) of a notify script that exits with `code`."""
    path, command = _script(tmp_path, "notify", LOG_SCRIPT.format(code=code))
    return path.with_suffix(".log"), command


def _log(path):
    """One (SDLC_NODE, working folder, mark) per run the log holds."""
    if not path.is_file():
        return []
    return [tuple(line.split("\t")) for line in path.read_text(encoding="utf-8").splitlines()]


def _notify(command):
    return {"tree": {"notify": command}}


def _approve_tests(clock="10:00"):
    return _step("lone/l1-lone/approve-tests", "doing", clock)


def _lone_repo(tmp_path, *records, **config):
    """lone, one unit, with no active gate, so no render runs the validator or
    git; `config` joins .sdlc/config.yaml."""
    root = tmp_path / "repo"
    _config(root, [], **config)
    _dump(root / "specs" / "lone" / "contract.yaml", _contract("lone", LONE))
    write_seat_roster(root)
    _progress(root, "lone", *records)
    return root


class ShellRuns:
    """The spy on subprocess.Popen: each start through the shell as (the
    command, the keyword arguments, the process); every other call passes
    through. With `refuse` set, a start through the shell raises OSError, as
    a missing shell would."""

    def __init__(self, real):
        self.real = real
        self.runs = []
        self.refuse = False

    def __call__(self, args, *more, **kwargs):
        if not kwargs.get("shell"):
            return self.real(args, *more, **kwargs)
        if self.refuse:
            self.runs.append((args, kwargs, None))
            raise OSError("the shell cannot start")
        process = self.real(args, *more, **kwargs)
        self.runs.append((args, kwargs, process))
        return process

    def wait(self):
        """Each started command's end: a bounded real wait."""
        for _, _, process in self.runs:
            if process is not None:
                process.wait(timeout=LIMIT)


@pytest.fixture
def shell_runs(monkeypatch):
    runs = ShellRuns(subprocess.Popen)
    monkeypatch.setattr(subprocess, "Popen", runs)
    yield runs
    for _, _, process in runs.runs:
        if process is not None and process.poll() is None:
            try:
                process.wait(timeout=LIMIT)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


class Noting(Sleeper):
    """A Sleeper that also notes `note()` at each call, before its step."""

    def __init__(self, out, steps, note):
        super().__init__(out, steps)
        self.note = note
        self.notes = []

    def __call__(self, seconds):
        self.notes.append(self.note())
        return super().__call__(seconds)


def _noting(root, note, *steps, out=None):
    """(sleeper, renders) of one pane run, as _pane, noting `note()` at each tick."""
    out = io.StringIO() if out is None else out
    sleeper = Noting(out, steps, note)
    code = _follow()(Path(root), out, sleep=sleeper)
    assert code == 0, f"the pane ended with {code!r}, not 0"
    return sleeper, _renders(out.getvalue())


class _Writes(io.StringIO):
    """A stream that keeps each write."""

    def __init__(self):
        super().__init__()
        self.writes = []

    def write(self, text):
        self.writes.append(text)
        return super().write(text)


# --- SC8.1 the waiting line ------------------------------------------------------------------------

def test_sc8_1_on_approve_tests_the_first_line_is_the_waiting_line_cut_like_the_rest_in_one_write(
        tmp_path, capsys, monkeypatch):
    root = _lone_repo(tmp_path, _approve_tests())
    _, (full,) = _pane(root)
    whole = _whole(root, capsys)
    assert full[0] == WAIT_LONE
    assert full == [WAIT_LONE, "specs/lone/contract.yaml > lone > l1-lone > approve-tests",
                    whole["lone"], short_line(whole["lone/l1-lone"]), "    7 more: 7 to do",
                    short_line(whole["lone/l1-lone/approve-tests"])]
    monkeypatch.setenv("COLUMNS", "40")
    out = _Writes()
    _, (narrow,) = _pane(root, out=out)
    assert narrow == cut_lines(full, 40)
    assert narrow[0] == WAIT_LONE[:37] + "..."
    writes = [text for text in out.writes if text]
    assert len(writes) == 1 and writes[0].startswith(CLEAR + narrow[0] + "\n"), writes


def test_sc8_1_on_approve_commit_the_waiting_line_names_the_approval_and_its_unit(
        tmp_path, capsys):
    root = _repo(tmp_path, gates=())
    _progress(root, "alpha", _step("alpha/a2-edges/green", "done", "10:00"),
              _step("alpha/a2-edges/approve-commit", "doing", "10:01"))
    _, renders = _pane(root)
    whole = _whole(root, capsys)
    assert renders[0][0] == "waiting on a seat: approve-commit for alpha/a2-edges"
    assert renders == [[
        "waiting on a seat: approve-commit for alpha/a2-edges",
        "specs/alpha/contract.yaml > alpha > a2-edges > approve-commit",  # the where-am-I line
        "1 more: 1 to do",                   # beta
        whole["alpha"],
        "  1 more: 1 to do",                 # alpha/a1-core
        short_line(whole["alpha/a2-edges"]),
        "    9 more: 8 to do, 1 done",       # the other tasks and the checks
        short_line(whole["alpha/a2-edges/approve-commit"]),
    ]]


def test_sc8_1_the_waiting_line_leaves_when_the_current_task_moves_off_the_approval(
        tmp_path, capsys):
    root = _repo(tmp_path, gates=())
    first = _step("alpha/a2-edges/approve-commit", "doing", "10:00")
    _progress(root, "alpha", first)
    _, renders = _pane(root, lambda: _progress(
        root, "alpha", first, _step("alpha/a2-edges/commit", "doing", "10:01")))
    whole = _whole(root, capsys)
    assert [render[0] for render in renders] == [
        "waiting on a seat: approve-commit for alpha/a2-edges",
        "specs/alpha/contract.yaml > alpha > a2-edges > commit"]
    assert renders[1][-1] == short_line(whole["alpha/a2-edges/commit"])
    assert not any(line.startswith("waiting on a seat") for line in renders[1])


# --- SC8.2 notify once per arrival ------------------------------------------------------------------

def test_sc8_2_a_pane_that_starts_on_an_approval_runs_notify_once_with_the_item_id_in_sdlc_node(
        tmp_path, capsys, shell_runs):
    log, command = _logger(tmp_path)
    root = _lone_repo(tmp_path, _approve_tests(), **_notify(command))
    sleeper, renders = _noting(
        root, lambda: len(shell_runs.runs),
        shell_runs.wait,                                              # the command ends
        lambda: _append(root / ".sdlc" / "config.yaml"),              # a redraw, the same task
        lambda: _append(root / ".sdlc" / "progress" / "lone.yaml"),   # another
        None)
    assert sleeper.notes == [1, 1, 1, 1, 1]  # started by the first render, never again
    assert [run[0] for run in shell_runs.runs] == [command]
    assert len(renders) == 3 and all(render[0] == WAIT_LONE for render in renders)
    assert [node for node, _, _ in _log(log)] == ["lone/l1-lone/approve-tests"]
    assert capsys.readouterr().err == ""  # a zero exit prints nothing


def test_sc8_2_notify_runs_at_each_arrival_at_an_approval_and_never_on_a_redraw_of_the_same_task(
        tmp_path, shell_runs):
    log, command = _logger(tmp_path)
    root = _repo(tmp_path, gates=())
    _config(root, [], **_notify(command))
    records = [_step("alpha/a2-edges/write-tests", "doing", "10:00")]
    _progress(root, "alpha", *records)

    def then(item, clock):
        def step():
            records.append(_step(item, "doing", clock))
            _progress(root, "alpha", *records)
        return step

    sleeper, renders = _noting(
        root, lambda: len(shell_runs.runs),
        then("alpha/a2-edges/approve-commit", "10:01"),    # arrives
        lambda: _append(root / ".sdlc" / "config.yaml"),   # a redraw, the same task
        None,                                              # no change
        then("alpha/a2-edges/commit", "10:02"),            # leaves
        then("alpha/a2-edges/approve-commit", "10:03"),    # comes back: a new arrival
        then("alpha/a1-core/approve-tests", "10:04"))      # another approval: a new arrival
    shell_runs.wait()
    assert sleeper.renders == [1, 2, 3, 3, 4, 5, 6]
    assert sleeper.notes == [0, 1, 1, 1, 1, 2, 3]
    assert [render[0].startswith("waiting on a seat:") for render in renders] == [
        False, True, True, False, True, True]
    assert sorted(node for node, _, _ in _log(log)) == [
        "alpha/a1-core/approve-tests",
        "alpha/a2-edges/approve-commit", "alpha/a2-edges/approve-commit"]


def test_the_notify_command_runs_at_the_repo_root_with_the_panes_environment_and_prints_nowhere(
        tmp_path, capfd, monkeypatch, shell_runs):
    monkeypatch.setenv("NOTIFY_TEST_MARK", "kept")
    monkeypatch.delenv("SDLC_NODE", raising=False)
    log, command = _logger(tmp_path)
    root = _lone_repo(tmp_path, _approve_tests(), **_notify(command))
    _, renders = _noting(root, lambda: None, shell_runs.wait, None)
    captured = capfd.readouterr()
    runs = _log(log)
    assert len(runs) == 1, runs
    node, cwd, mark = runs[0]
    assert node == "lone/l1-lone/approve-tests"
    assert os.path.samefile(cwd, root)
    assert mark == "kept"
    assert "SDLC_NODE" not in os.environ  # the pane's own environment stays as it was
    assert "marker" not in captured.out + captured.err
    assert not any("marker" in line for render in renders for line in render)


def test_the_pane_never_waits_on_the_notify_command(tmp_path, capsys, shell_runs):
    script, command = _script(tmp_path, "hold", HOLD_SCRIPT)
    root = _lone_repo(tmp_path, _approve_tests(), **_notify(command))
    running = []

    def first_tick():
        running.append([process.poll() is None for _, _, process in shell_runs.runs])
        script.with_suffix(".release").write_text("go", encoding="utf-8")

    sleeper, _ = _noting(root, lambda: len(shell_runs.runs), first_tick, shell_runs.wait, None)
    # started at the first render, and still holding when the pane reached its first tick
    assert sleeper.notes[0] == 1
    assert running == [[True]]
    assert script.with_suffix(".ended").read_text(encoding="utf-8") == "released"
    assert capsys.readouterr().err == ""


# --- SC8.3 a notify failure ----------------------------------------------------------------------

def test_sc8_3_a_failing_notify_prints_one_failure_line_on_stderr_and_the_pane_keeps_running(
        tmp_path, capsys, monkeypatch, shell_runs):
    monkeypatch.setenv("COLUMNS", "40")
    _, command = _logger(tmp_path, code=3)
    root = _lone_repo(tmp_path, _approve_tests(), **_notify(command))
    sleeper, renders = _noting(
        root, lambda: capsys.readouterr().err,
        shell_runs.wait,                                              # the command ends, exit 3
        None,                                                         # no change
        lambda: _append(root / ".sdlc" / "progress" / "lone.yaml"),   # a redraw, the same task
        None)
    line = f"notify failed, exit 3: {command}"
    assert len(line) > 40  # printed whole: stderr lines are not cut
    # found at the tick after the command ended, with no render, and printed once
    assert sleeper.notes == ["", line + "\n", "", "", ""]
    assert len(shell_runs.runs) == 1
    assert len(renders) == 2 and all(render[0] == WAIT_LONE[:37] + "..." for render in renders)
    assert not any("notify failed" in text for render in renders for text in render)


def test_sc8_3_with_no_notify_set_the_pane_shows_the_waiting_line_starts_nothing_and_keeps_running(
        tmp_path, capsys, shell_runs):
    root = _lone_repo(tmp_path, _approve_tests())
    _, renders = _pane(root, lambda: _append(root / ".sdlc" / "progress" / "lone.yaml"), None)
    assert [render[0] for render in renders] == [WAIT_LONE, WAIT_LONE]
    assert shell_runs.runs == []
    assert capsys.readouterr().err == ""


NO_COMMAND = [
    pytest.param({"tree": {}}, id="a-tree-key-without-notify"),
    pytest.param({"tree": {"notify": None}}, id="notify-null"),
    pytest.param({"tree": {"notify": 5}}, id="notify-a-number"),
    pytest.param({"tree": {"notify": ""}}, id="notify-empty"),
    pytest.param({"tree": {"notify": "   "}}, id="notify-blank"),
    pytest.param({"tree": {"notify": ["echo", "hi"]}}, id="notify-a-list"),
    pytest.param({"tree": "echo hi"}, id="tree-not-a-mapping"),
]


@pytest.mark.parametrize("config", NO_COMMAND)
def test_a_notify_value_that_is_not_a_command_counts_as_unset(
        tmp_path, capsys, shell_runs, config):
    root = _lone_repo(tmp_path, _approve_tests(), **config)
    _, renders = _pane(root, lambda: _append(root / ".sdlc" / "progress" / "lone.yaml"), None)
    assert [render[0] for render in renders] == [WAIT_LONE, WAIT_LONE]
    assert shell_runs.runs == []
    assert capsys.readouterr().err == ""


def test_a_notify_command_that_cannot_start_prints_the_failure_line_with_exit_127_and_keeps_running(
        tmp_path, capsys, shell_runs):
    shell_runs.refuse = True
    command = "notify-that-cannot-start --now"
    root = _lone_repo(tmp_path, _approve_tests(), **_notify(command))
    sleeper, renders = _noting(
        root, lambda: capsys.readouterr().err,
        lambda: _append(root / ".sdlc" / "progress" / "lone.yaml"),   # a redraw, the same task
        None)
    # printed at the arrival itself, once
    assert sleeper.notes == [f"notify failed, exit 127: {command}\n", "", ""]
    assert len(shell_runs.runs) == 1
    assert len(renders) == 2 and all(render[0] == WAIT_LONE for render in renders)
