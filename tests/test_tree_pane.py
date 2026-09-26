"""The pane suite for ADR 0031 (contract tree-view, unit t7-pane-face).

The 0.15.0 `taskcontract tree --follow` loop and its tests retired with
project-tree's o6-pane-keys; the interactive pane's tests are in
tests/test_pane.py, tests/test_pane_keys.py and tests/test_pane_renders.py.
One rule of this suite still holds and stays here: every `git status` the
kit runs carries `--no-optional-locks`, since the pane renders while the
user runs git.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

progress_module = importlib.import_module("taskcontract.progress")

TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]
INTENT = ("A fixture contract for the pane suite; its units carry the "
          "sketch shapes that check ids come from.")


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
