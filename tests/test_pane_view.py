"""The pane-view suite (contract pane-view, units p1-where-line, p2-short-ids,
p3-line-parts and p4-fold-names).

The 0.15.0 `taskcontract tree --follow` loop, its where-am-I line, its fold
lines and their tests retired with project-tree's o6-pane-keys; the
interactive pane's tests are in tests/test_pane.py, tests/test_pane_keys.py
and tests/test_pane_renders.py. What stays here pins the whole print:
`taskcontract tree` prints the same bytes, every id full (SC3.2), and the
same stdout and stderr with `tree: pane: parts:` set (SC2.2) or `tree:
pane: fold:` set (SC4.2), valid or not.
"""

from __future__ import annotations

import re

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main


HEAD = "1a2b3c4"
INTENT = ("A fixture contract for the pane-view suite; its units carry the "
          "sketch shapes that check ids come from.")
# A feature's mark after its status (project-tree o3): a contract with no file
# at docs/features/<id>.md, and one whose document holds no Ready row.
NO_DOCUMENT = " no feature document"


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


def _at(clock):
    return f"2026-09-22T{clock}:00Z"


def _step(item, state, clock, **more):
    """A task-step record; on a unit or a contract id with `done`, a close."""
    return {"item": item, "state": state, "at": _at(clock), "head": HEAD, **more}


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


def _append(path, text="\n# a note\n"):
    """Grow a file, so its size differs whatever its time reads."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


# --- SC3.2 full ids everywhere else -------------------------------------------------------

SOLO_TREE = f"""\
solo-2 (no title) [waiting on a seat]{NO_DOCUMENT} | {INTENT}
  solo-2/G0 Planning / Intake [to do] inactive
    solo-2/G0/G0.1 Definition-of-ready [to do]
    solo-2/G0/G0.2 Vocabulary coverage [to do]
    solo-2/G0/G0.3 Unit confirmation [to do]
  solo-2/s1-base the work for s1-base is done [done] at {HEAD}
    solo-2/s1-base/approve-tests Approve the test list [done]
    solo-2/s1-base/write-tests Write the tests [done]
    solo-2/s1-base/prove-red Prove red [done]
    solo-2/s1-base/green Green [done]
    solo-2/s1-base/approve-commit Approve the commit [done]
    solo-2/s1-base/commit Commit [done]
    solo-2/s1-base/two-key Two-Key PASS [done]
    solo-2/s1-base/SC3.1 verify it holds (SC3.1) [done]
  solo-2/s2-top the work for s2-top is done [waiting on a seat] depends_on: solo-2/s1-base
    solo-2/s2-top/approve-tests Approve the test list [waiting on a seat] current seat: user
    solo-2/s2-top/write-tests Write the tests [to do]
    solo-2/s2-top/prove-red Prove red [to do]
    solo-2/s2-top/green Green [to do]
    solo-2/s2-top/approve-commit Approve the commit [to do]
    solo-2/s2-top/commit Commit [to do]
    solo-2/s2-top/two-key Two-Key PASS [to do]
    solo-2/s2-top/SC3.2 verify it stays (SC3.2) [to do]
"""


def _solo_repo(tmp_path):
    """solo-2: s1-base closed, s2-top at approve-tests; no active gate."""
    root = tmp_path / "repo"
    _config(root, [])
    _dump(root / "specs" / "solo-2" / "contract.yaml", _contract("solo-2", [
        _unit("s1-base", ["verify it holds (SC3.1)"]),
        _unit("s2-top", ["verify it stays (SC3.2)"], depends_on=["s1-base"]),
    ]))
    write_seat_roster(root)
    _progress(root, "solo-2", _step("solo-2/s1-base", "done", "09:00"),
              _step("solo-2/s2-top/approve-tests", "doing", "10:00"))
    return root


def test_sc3_2_taskcontract_tree_prints_the_same_bytes_with_every_id_full(tmp_path, capsys):
    root = _solo_repo(tmp_path)
    code = main(["tree", "--root", str(root)])
    printed = capsys.readouterr()
    assert code == 0
    assert printed.out == SOLO_TREE
    assert printed.err == ""


# --- SC2 the parts of an item line ----------------------------------------------------
#
# `tree: pane: parts:` in .sdlc/config.yaml lists the fields each item line
# of the pane shows after its id. On the fixture's path every field but
# evidence shows on some line: the contract's status, doc reference and
# summary, the unit's status, depends_on link and summary, the task's status,
# `current` mark and summary. The path never carries evidence: the current
# task is doing, to do or waiting on a seat, never done or blocked by its own
# record, and its unit and contract read done only when every child does. So
# evidence's place in the order shows only as nothing where it stands.

UNREADABLE_BETA = re.compile(
    r"^taskcontract tree: unreadable progress: \.sdlc/progress/beta\.yaml \(.+\)$")


def _doc_repo(tmp_path):
    """alpha and beta, no active gate, alpha's feature doc on disk; the
    current task is alpha/a2-edges/prove-red, doing, not an approval."""
    root = _repo(tmp_path, gates=())
    _append(root / "docs" / "features" / "alpha.md", "# Alpha\n")
    _progress(root, "alpha",
              _step("alpha/a1-core/approve-tests", "done", "10:00", by="user"),
              _step("alpha/a2-edges/prove-red", "doing", "10:04"))
    return root


def _parts(root, parts, gates=(), **tree):
    """The config with `tree: pane: parts:` set to `parts`, beside any other
    `tree:` key given."""
    _config(root, gates, tree={**tree, "pane": {"parts": parts}})


# --- SC2.2 what the setting leaves unchanged ----------------------------------------------

WHOLE_TREE = [
    pytest.param(["status"], id="a-valid-parts"),
    pytest.param(["status", "colour"], id="a-bad-parts"),
]


@pytest.mark.parametrize("parts", WHOLE_TREE)
def test_sc2_2_taskcontract_tree_prints_the_same_stdout_and_stderr_with_parts_set(
        tmp_path, capsys, parts):
    root = _doc_repo(tmp_path)
    (root / ".sdlc" / "progress" / "beta.yaml").write_text("records: [unclosed\n",
                                                           encoding="utf-8")
    _parts(root, parts)
    code = main(["tree", "--root", str(root)])
    with_key = capsys.readouterr()
    assert code == 0
    _config(root, [])
    code = main(["tree", "--root", str(root)])
    without_key = capsys.readouterr()
    assert code == 0
    assert with_key.out == without_key.out
    assert with_key.err == without_key.err
    assert "pane parts ignored" not in with_key.err
    assert UNREADABLE_BETA.match(with_key.err.splitlines()[0])


# --- SC4 the fold lines ------------------------------------------------------------------
#
# `tree: pane: fold:` in .sdlc/config.yaml chooses what each fold line holds:
# the counts by status (`counts`, or no key), or each folded item by its id and
# status (`names`). Each fold line keeps its place and its indent; only the
# text after `<n> more: ` (or `<n> items`) changes.


def _fold(root, fold, gates=(), **pane):
    """The config with `tree: pane: fold:` set to `fold`, beside any other
    `tree: pane:` key given."""
    _config(root, gates, tree={"pane": {**pane, "fold": fold}})


# --- SC4.2 counts, and a bad fold setting -------------------------------------------------------

FOLD_WHOLE_TREE = [
    pytest.param("names", id="fold-names"),
    pytest.param("sideways", id="a-bad-fold"),
]


@pytest.mark.parametrize("fold", FOLD_WHOLE_TREE)
def test_sc4_2_taskcontract_tree_prints_the_same_stdout_and_stderr_with_fold_set(
        tmp_path, capsys, fold):
    root = _doc_repo(tmp_path)
    (root / ".sdlc" / "progress" / "beta.yaml").write_text("records: [unclosed\n",
                                                           encoding="utf-8")
    _fold(root, fold)
    code = main(["tree", "--root", str(root)])
    with_key = capsys.readouterr()
    assert code == 0
    _config(root, [])
    code = main(["tree", "--root", str(root)])
    without_key = capsys.readouterr()
    assert code == 0
    assert with_key.out == without_key.out
    assert with_key.err == without_key.err
    assert "pane fold ignored" not in with_key.err
    assert UNREADABLE_BETA.match(with_key.err.splitlines()[0])
