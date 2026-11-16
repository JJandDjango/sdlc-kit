"""The words and the folds of G1 (contract: g1-requirements-spec, unit
s10-words-and-folds: check SC1.1, and done_means).

What this file pins, each red on today's code:

- R5's ask says that `checked` covers an item that does not apply to the
  feature (SC1.1);
- one reader reads a `Ready:` row, for `g1.py` and for `tree.drift`: no copy of
  the reader stands in a second module, and both entry points still give the one
  reading (done_means);
- kit 0.22.2 ships the three units, `s8-honest-reads`, `s9-one-line-refusals` and
  `s10-words-and-folds`: the version in both places, and the changelog's entry
  with the delta notes that the design's risks 12 and 13 name (done_means).

The refusal lines and the green lines of `g1-record`, word for word, are built
and read right today: the suite pins them elsewhere, and a test of them cannot
be red here.

A temporary repository per test. No test needs a linter or a checker.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

import taskcontract
from taskcontract import g1, tree
from taskcontract.__main__ import main

ROOT = Path(__file__).resolve().parent.parent
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
PACKAGE = Path(taskcontract.__file__).resolve().parent
FLOW = ROOT / "skills" / "sdlc" / "flows" / "g1.md"
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "skills" / "sdlc" / "init.py"
CHANGELOG = ROOT / "CHANGELOG.md"

ID = "apply-discount"
RECORD = f".sdlc/g1/{ID}.yaml"
RECORDED = f"recorded: {RECORD}"
PASSED = "G1.3: the review checks all 11 items"
ALL = "1,2,3,4,5,6,7,8,9,10,11"

SEAT_TERM = {"term": "intake-seat", "name": "Intake seat",
             "definition": "A human position that answers for a unit at intake.",
             "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
             "since": "2026-08-26"}
INTENT = ("A contract with a scope of its own, enough words to pass the door "
          "as a fixture for the suite of the words and the folds.")
TITLE = "# {id} - A fixture feature\n\n"
HEAD = "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"


def row(text: str, by: str = "Ann Lee") -> str:
    return f"| 2026-10-07 | {by} | {text} |\n"


def document(revision: int, feature: str = ID) -> str:
    """A feature document with text rows r1 to r<revision>, then the `Ready:`
    row that names r<revision> as the one the contract is derived from."""
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{feature}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return TITLE.format(id=feature) + HEAD + rows + ready + "\n## Statement\n\nWords.\n"


def contract_text(feature: str = ID) -> str:
    unit = {"unit": "the unit", "id": "the-unit", "confirmed_by": ["po"],
            "done_means": "the unit is done",
            "acceptance_sketch": ["verify the unit is done (SC1.1)"]}
    return yaml.safe_dump({
        "id": feature, "title": "A fixture feature", "intent": INTENT,
        "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
        "decomposition": [unit], "dependencies": [], "entities": [],
        "provenance": {"origin": "human-request"}}, sort_keys=False)


class Repo:
    """One fixture repository at <tmp>/repo, the working directory: a ratified
    seat roster, the contract of `apply-discount`, its pair at r5 and r4, and a
    config that turns G0 and G1 on with no schema and no component to check."""

    def __init__(self, tmp: Path, monkeypatch):
        self.root = tmp / "repo"
        self.root.mkdir()
        self.write("specs/vocabulary/intake-seat.yaml", yaml.safe_dump(SEAT_TERM, sort_keys=False))
        self.write(f"specs/{ID}/contract.yaml", contract_text())
        self.write(f"docs/features/{ID}.md", document(5))
        self.write(f"docs/features/{ID}.design.md", document(4))
        self.write(".sdlc/config.yaml", yaml.safe_dump(
            {"active_gates": ["G0", "G1"], "g1": {"exempt": [], "schemas": []}}, sort_keys=False))
        self.write("specs/components.yaml", yaml.safe_dump(
            {"version": 1, "components": []}, sort_keys=False))
        monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp))
        monkeypatch.chdir(self.root)

    def write(self, rel: str, text) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def records(self) -> list[dict]:
        return yaml.safe_load((self.root / RECORD).read_text(encoding="utf-8"))["records"]


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Repo:
    return Repo(tmp_path, monkeypatch)


def passing(capsys):
    """`g1-record review` that checks all 11 items: (exit code, stdout, stderr)."""
    words = ["g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po", "--checked", ALL]
    capsys.readouterr()
    try:
        code = main(words)
    except SystemExit:
        code = None
    out, err = capsys.readouterr()
    assert code is not None, f"taskcontract does not take the review call: {err.strip()}"
    return code, out, err


def step(text: str, label: str) -> str:
    """One step of the flow: from its label at a line's start to the next step's
    label or the close of the instructions block."""
    found = re.search(rf"^{label}\. ", text, re.MULTILINE)
    assert found, f"the flow holds no {label}"
    rest = text[found.start():]
    end = re.search(r"\n\n[A-Z]+\d+\. |\n</instructions>", rest)
    return rest[:end.start()] if end else rest


# --- SC1.1: R5's ask -------------------------------------------------------------------

APPLIES = "`checked` covers an item that does not apply to the feature"


def test_sc1_1_r5_asks_checked_or_unchecked_and_says_checked_covers_an_item_that_does_not_apply():
    text = FLOW.read_text(encoding="utf-8")
    r5 = step(text, "R5")
    assert r5.count(APPLIES) == 1 and text.count(APPLIES) == 1
    ask = r5.index("ASK one question: checked or unchecked")
    take = r5.index("Take one answer")
    assert ask < r5.index(APPLIES) < take, "the sentence stands inside R5's ask, not after it"
    assert APPLIES not in step(text, "R6")
    # the venue still asks the 11 items one at a time, and holds its cap
    assert "one at a time" in r5 and "11 items" in r5
    assert len(text) < 12_000


# --- done_means: one reader reads a `Ready:` row ---------------------------------------

def ready_row_modules() -> list[str]:
    """The modules under the package whose code (a docstring left out) holds a
    string constant that names a `Ready:` row: where a reader of that row stands."""
    found = []
    for path in sorted(PACKAGE.rglob("*.py")):
        module = ast.parse(path.read_text(encoding="utf-8"))
        docstrings = set()
        for node in ast.walk(module):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                first = node.body[0] if node.body else None
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstrings.add(id(first.value))
        if any(isinstance(node, ast.Constant) and isinstance(node.value, str)
               and id(node) not in docstrings and "Ready" in node.value
               for node in ast.walk(module)):
            found.append(path.relative_to(PACKAGE).as_posix())
    return found


READY_5 = row("r6: Ready: contract validates ready-green, derived from r5", by="intake")
TEXT_5 = row("r5: the text")
LATER = row("r99: a later text")  # the document moved on; the contract did not

# A document's first table, and the revision its newest `Ready:` row names; None
# when no row names one.
TABLES = [
    pytest.param(TITLE + HEAD + TEXT_5 + READY_5, "r5", id="one-ready-row"),
    pytest.param(TITLE + HEAD + TEXT_5 + READY_5 + row("r7: more text")
                 + row("r8: Ready: validates again, derived from r7"), "r7",
                 id="the-newest-ready-row-wins"),
    pytest.param(TITLE + HEAD + row("r8: Ready: validates again, derived from r7")
                 + TEXT_5 + READY_5, "r7", id="the-newest-by-its-number-not-its-place"),
    pytest.param(TITLE + HEAD + row("r6: Ready: derived from r05"), "r5",
                 id="a-leading-zero-in-the-table"),
    pytest.param("﻿" + TITLE + HEAD + TEXT_5 + READY_5, "r5", id="a-byte-order-mark"),
    pytest.param((TITLE + HEAD + TEXT_5 + READY_5).replace("\n", "\r\n"), "r5", id="crlf"),
    pytest.param(TITLE + HEAD + TEXT_5, None, id="no-ready-row"),
    pytest.param(TITLE + HEAD + row("r6: Ready: derived from r5x"), None,
                 id="a-word-after-the-digits"),
    pytest.param(TITLE + HEAD + row("r6: ready: derived from r5"), None,
                 id="ready-in-another-case"),
    pytest.param(TITLE + HEAD + TEXT_5 + "\nWords.\n\n" + HEAD + READY_5, None,
                 id="a-ready-row-in-a-second-table"),
]


@pytest.mark.parametrize("text, revision", TABLES)
def test_done_means_one_reader_reads_a_ready_row_for_g1_and_for_the_trees_drift(
        repo, capsys, text, revision):
    # one module holds the reader of a `Ready:` row: neither g1.py nor tree.py keeps a copy
    assert len(ready_row_modules()) == 1, ready_row_modules()
    # and both entry points give the one reading
    later = LATER.replace("\n", "\r\n" if "\r\n" in text else "\n")
    path = repo.write(f"docs/features/{ID}.md", text + later)
    if revision is None:
        assert tree.drift(path) == tree.NO_READY
        with pytest.raises(g1.Unreadable, match=re.escape('"Ready:" row that names a revision')):
            g1.derived_from(repo.root, ID)
        assert passing(capsys)[0] == 2
    else:
        assert tree.drift(path) == f"stale: document r99, contract from {revision}"
        assert g1.derived_from(repo.root, ID) == {"requirements": revision, "design": "r4"}
        assert passing(capsys) == (0, f"{PASSED}\n{RECORDED}\n", "")
        assert repo.records()[-1]["requirements"] == revision


# --- done_means: kit 0.22.2 ships the three units --------------------------------------

def version_of(path: Path, pattern: str) -> tuple[int, ...]:
    found = re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE)
    assert found, f"no version in {path.name}"
    return tuple(int(part) for part in found.group(1).split("."))


def test_done_means_the_kit_version_reads_0_22_2_or_later_and_both_places_agree():
    # a floor, never the literal: the next release moves both numbers
    project = version_of(PYPROJECT, r'^version\s*=\s*"(\d+\.\d+\.\d+)"')
    kit = version_of(INIT, r'^KIT_VERSION\s*=\s*"(\d+\.\d+\.\d+)"')
    assert project >= (0, 22, 2)
    assert kit == project


def entry_of_0_22_2() -> str:
    """The changelog's 0.22.2 entry: its heading to the next `## ` heading, its
    whitespace collapsed."""
    text = CHANGELOG.read_text(encoding="utf-8")
    headings = [line.rstrip() for line in text.splitlines() if line.startswith("## ")]
    mine = [h for h in headings if h.startswith("## 0.22.2 - ")]
    assert len(mine) == 1, "no entry heads 0.22.2, or two do"
    assert re.fullmatch(r"## 0\.22\.2 - \d{4}-\d{2}-\d{2} \(tag `v0\.22\.2`\)", mine[0]), mine[0]
    after = text.split(mine[0], 1)[1]
    return " ".join(after.split("\n## ", 1)[0].split())


def test_done_means_the_changelog_holds_a_dated_0_22_2_entry_above_0_22_1():
    entry_of_0_22_2()
    headings = [line.rstrip() for line in CHANGELOG.read_text(encoding="utf-8").splitlines()
                if line.startswith("## ")]
    new = [n for n, h in enumerate(headings) if h.startswith("## 0.22.2 - ")]
    old = [n for n, h in enumerate(headings) if h.startswith("## 0.22.1 - ")]
    assert new and old and new[0] < old[0]


def test_done_means_the_changelog_entry_names_the_three_units_and_the_schema_version():
    entry = entry_of_0_22_2()
    for unit in ("s8-honest-reads", "s9-one-line-refusals", "s10-words-and-folds"):
        assert f"`{unit}`" in entry, unit
    assert "`g1-requirements-spec`" in entry
    assert "`0.22.1` -> `0.22.2`" in entry
    assert "`1.5.0`" in entry


def test_done_means_the_changelog_entry_carries_the_two_delta_notes_of_risks_12_and_13():
    entry = entry_of_0_22_2()
    assert entry.count("Delta note") >= 1
    # risk 12: a G1.2 record of the two-file form counts as absent
    assert "G1.2" in entry and "`g1-record model`" in entry
    # risk 13: G1.1 read `done` on a pattern that matches no file, or with no `g1.schemas` key
    assert "G1.1" in entry and "`g1.schemas`" in entry
    assert "matches no file" in entry
    assert entry.count("`to do`") >= 2
