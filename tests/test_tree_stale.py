"""The drift suite (contract project-tree, unit o3-stale).

The tree opens each feature's document at docs/features/<id>.md for its
revision table only: the first table in the file, a run of lines that open
on `|`. A row counts when its last cell, the changes made, opens on
`r<N>:`; the tree skips every other row. The document's revision is the
highest rN of a counted row that is neither a `Ready:` row (its cell opens
`rN: Ready:`) nor a `Measured:` row (`rN: Measured:`). The contract's
revision is the rM that the newest `Ready:` row names: the one with the
highest rN among those whose cell holds `derived from rM` (SC5.1).

The feature's line names what the tree finds as a mark after its status:
`stale: document rN, contract from rM` when the document's revision is
higher than the contract's; `no feature document` when there is no file at
docs/features/<id>.md; `no "Ready:" row` when the file holds no `Ready:` row
that names its rM, or cannot be read as text. With none of the three, the
contract matches its document and its line carries no mark; neither missing
piece ever reads as a match (SC5.2). The `doc:` part still shows whenever
the file exists. The mark shows on the whole print, on the query's first
line and on the pane's feature line. The unit adds no stderr line, and the
tree writes no file. Intake writes the `Ready:` row in its fixed shape.

Each test drives the CLI in process against a fixture repo under tmp_path,
outside any git repository, with no gate active, so no validator runs; the
fixtures never read the kit's own feature documents.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import pytest
import yaml

import taskcontract
from taskcontract import tree_view
from taskcontract.__main__ import main

# The kit whose package runs: its intake flow.
KIT = Path(taskcontract.__file__).resolve().parent.parent
FLOW = KIT / "skills" / "sdlc" / "flows" / "intake.md"
CHAR_CEILING = 12_000  # the flow's PromptLang budget, as tests/test_intake_flow.py holds it

CLEAR = "\x1b[H\x1b[2J"
CID = "apply-discount"
TITLE = "Apply one discount code per order"
INTENT = "Checkout applies one discount code per order."
HEAD = f"{CID} {TITLE}"
DOC = f" doc: docs/features/{CID}.md"
TAIL = f"{DOC} | {INTENT}"
NO_DOCUMENT = "no feature document"
NO_READY = 'no "Ready:" row'

# The USAGE example, "Drift from the feature document", verbatim.
EXAMPLE = ("apply-discount Apply one discount code per order [doing] stale: document r4, "
           "contract from r2 doc: docs/features/apply-discount.md | Checkout applies one "
           "discount code per order.")

# The intake flow's words for the Ready row (step I7 of skills/sdlc/flows/intake.md).
READY_RULE = ("When the loop ends ready-green and the request is a feature document at "
              "`docs/features/{id}.md`, ADD one row to its revision table: the date, "
              "`intake`, and a changes cell that opens ``r{n}: Ready: contract `{id}` "
              "validates ready-green, derived from r{m}``, with r{n} the next revision "
              "and r{m} the signed revision intake read.")
READY_CELL = "r{n}: Ready: contract `{id}` validates ready-green, derived from r{m}"

HEADER = "| Revision Date | Revised By | Changes Made |\n| :-: | :-: | :-- |\n"


def _stale(document, contract):
    return f"stale: document r{document}, contract from r{contract}"


def _ready(n, m):
    """Intake's Ready row cell, in its fixed shape."""
    return READY_CELL.format(n=n, m=m, id=CID) + " in kit session 51; both seats signed"


def _row(cell):
    return f"| 2026-09-24 | user | {cell} |\n"


def _table(*cells):
    return HEADER + "".join(_row(cell) for cell in cells)


def _document(*cells, before="# apply-discount - Apply one discount code per order\n\n",
              after="\n## Statement\n\nCheckout applies one discount code per order.\n"):
    """A feature document: a preamble, the revision table, then the body."""
    return before + _table(*cells) + after


BASE = ("r1: Created through an interview", "r2: The request half finished")


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, find no git repo above the
    fixture, and give the pane a wide terminal."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


# --- the fixture repository -----------------------------------------------------------

def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _contract(cid=CID, title=TITLE, intent=INTENT):
    doc = {"id": cid, "intent": intent, "scope": ["src/"], "non_goals": ["No other work"],
           "decomposition": [{"unit": "the code field", "id": "u1-code-field",
                              "confirmed_by": ["user"],
                              "done_means": "The checkout form validates a discount code.",
                              "acceptance_sketch": ["verify a code validates (SC1.1)"]}],
           "dependencies": [], "entities": [], "provenance": {"origin": "human-request"}}
    if title is not None:
        doc["title"] = title
    return doc


def _repo(tmp_path, document=None, doing=True):
    """No gate active; the contract apply-discount, doing when `doing`, with
    `document` (text, or bytes written as they are) at its feature document's
    path, or no file there when it is None."""
    root = tmp_path / "repo"
    _dump(root / ".sdlc" / "config.yaml", {"kit": "fixture", "adoption": "greenfield",
                                            "stack": "python", "active_gates": []})
    _dump(root / "specs" / CID / "contract.yaml", _contract())
    if document is not None:
        _put_document(root, CID, document)
    if doing:
        _dump(root / ".sdlc" / "progress" / f"{CID}.yaml", {"records": [
            {"item": f"{CID}/u1-code-field/write-tests", "state": "doing",
             "at": "2026-09-25T10:00:00Z", "head": "1a2b3c4"}]})
    return root


def _put_document(root, cid, document):
    path = root / "docs" / "features" / f"{cid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(document, bytes):
        path.write_bytes(document)
    else:
        path.write_text(document, encoding="utf-8")


def _append_after_table(root, *cells):
    """Rewrite the document with rows added at the end of its table, above its body."""
    path = root / "docs" / "features" / f"{CID}.md"
    text = path.read_text(encoding="utf-8")
    at = text.index("\n## Statement")
    path.write_text(text[:at].rstrip("\n") + "\n" + "".join(_row(c) for c in cells)
                    + text[at:], encoding="utf-8")


# --- driving the CLI --------------------------------------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _print(root, capsys):
    """(stdout lines, stderr) of the whole tree, which exits 0."""
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    return out.splitlines(), err


def _feature(root, capsys, cid=CID):
    """The feature's line in the whole print; the print writes nothing on stderr."""
    lines, err = _print(root, capsys)
    found = [text for text in lines if text.startswith(f"{cid} ")]
    assert len(found) == 1, found
    assert err == ""
    return found[0]


def _query(root, capsys, cid=CID):
    """The query's stdout lines for the feature; it exits 0 with nothing on stderr."""
    code, out, err = _call(["tree", cid, "--root", str(root)], capsys)
    assert (code, err) == (0, "")
    return out.splitlines()


class _Interrupt:
    """The pane's injected sleep: it ends the loop at its first call."""

    def __call__(self, seconds):
        raise KeyboardInterrupt


def _pane_line(root, capsys, cid=CID):
    """The feature's line in one render of the 0.15.0 pane (`--follow`)."""
    out = io.StringIO()
    assert tree_view.follow(Path(root), out, sleep=_Interrupt()) == 0
    text = out.getvalue()
    assert text.startswith(CLEAR)
    assert capsys.readouterr().err == ""
    found = [line for line in text[len(CLEAR):].splitlines() if line.startswith(f"{cid} ")]
    assert len(found) == 1, found
    return found[0]


def _mark(root, capsys):
    """The text between the feature's status and its `doc:` part."""
    line = _feature(root, capsys)
    head = f"{HEAD} [doing]"
    assert line.startswith(head) and line.endswith(TAIL), line
    return line[len(head):len(line) - len(TAIL)].strip() or None


# --- SC5.1 a newer document revision reads stale, naming both ----------------------------

def test_sc5_1_the_usage_example_reads_stale_naming_both_revisions_on_the_whole_print(
        tmp_path, capsys):
    root = _repo(tmp_path, _document(*BASE, _ready(3, 2), "r4: The solution half"))
    assert _feature(root, capsys) == EXAMPLE


def test_sc5_1_a_stale_feature_names_both_revisions_on_the_query_and_the_pane(
        tmp_path, capsys):
    root = _repo(tmp_path, _document(*BASE, _ready(3, 2), "r4: The solution half"))
    assert _query(root, capsys) == [
        f"{HEAD} [doing] {_stale(4, 2)}",
        f"summary: {INTENT}",
        f"doc: docs/features/{CID}.md:1",
        f"file: specs/{CID}/contract.yaml:1"]
    assert _pane_line(root, capsys) == EXAMPLE


def test_sc5_1_a_matching_feature_carries_no_mark_until_a_newer_revision_lands(
        tmp_path, capsys):
    root = _repo(tmp_path, _document(*BASE, _ready(3, 2)))
    bare = f"{HEAD} [doing]{TAIL}"
    assert _feature(root, capsys) == bare
    assert _query(root, capsys)[0] == f"{HEAD} [doing]"
    assert _pane_line(root, capsys) == bare
    _append_after_table(root, "r4: The solution half")
    assert _feature(root, capsys) == EXAMPLE
    assert _query(root, capsys)[0] == f"{HEAD} [doing] {_stale(4, 2)}"
    assert _pane_line(root, capsys) == EXAMPLE


def test_sc5_1_a_measured_row_never_counts_as_the_documents_revision(tmp_path, capsys):
    root = _repo(tmp_path, _document(
        *BASE, _ready(3, 2), "r4: Measured: the pilot ran two weeks, derived from r9"))
    assert _mark(root, capsys) is None
    _append_after_table(root, "r5: The solution half")
    assert _mark(root, capsys) == _stale(5, 2)


def test_sc5_1_a_ready_row_never_counts_as_the_documents_revision(tmp_path, capsys):
    root = _repo(tmp_path, _document("r1: Created", _ready(2, 1), _ready(3, 1)))
    assert _mark(root, capsys) is None
    _append_after_table(root, "r4: The request half finished")
    assert _mark(root, capsys) == _stale(4, 1)


def test_sc5_1_the_newest_ready_row_names_the_contracts_revision(tmp_path, capsys):
    root = _repo(tmp_path, _document("r1: Created", _ready(2, 1), "r3: Revised",
                                     _ready(4, 3)))
    assert _mark(root, capsys) is None  # the older Ready row alone would read r3 after r1
    _append_after_table(root, "r5: Revised again")
    assert _mark(root, capsys) == _stale(5, 3)


def test_sc5_1_a_newer_ready_row_without_derived_from_names_no_revision_so_the_older_one_stands(
        tmp_path, capsys):
    root = _repo(tmp_path, _document("r1: Created", _ready(2, 1), "r3: Revised",
                                     "r4: Ready: contract `apply-discount` re-read by hand"))
    assert _mark(root, capsys) == _stale(3, 1)


def test_sc5_1_revisions_compare_as_numbers_so_r10_stands_after_r9(tmp_path, capsys):
    cells = ["r1: Created", _ready(2, 1), *(f"r{n}: Revision {n}" for n in range(3, 10)),
             _ready(10, 9), "r11: Revision 11"]
    root = _repo(tmp_path, _document(*cells))
    assert _mark(root, capsys) == _stale(11, 9)


def test_sc5_1_a_ready_row_naming_a_revision_above_the_documents_reads_as_a_match(
        tmp_path, capsys):
    root = _repo(tmp_path, _document("r1: Created", _ready(2, 5)))
    assert _mark(root, capsys) is None
    _append_after_table(root, "r6: Revised")
    assert _mark(root, capsys) == _stale(6, 5)


def test_sc5_1_of_two_ready_rows_with_one_revision_the_lower_row_names_the_contracts(
        tmp_path, capsys):
    root = _repo(tmp_path, _document(*BASE, _ready(3, 1), _ready(3, 2)))
    assert _mark(root, capsys) is None
    _append_after_table(root, "r4: The solution half")
    assert _mark(root, capsys) == _stale(4, 2)


def test_sc5_1_rows_the_tree_cannot_read_and_a_later_table_are_skipped(tmp_path, capsys):
    later = ("\nA later table, which the tree never reads:\n\n"
             + _table("r12: A row of a later table", "r13: Ready: derived from r4"))
    root = _repo(tmp_path, _document(
        *BASE, _ready(3, 2), "r4: The solution half",
        "R7: a capital R", "Revised as r8: the cell opens on other words",
        "r 9: a blank inside the revision", "(r10): the revision in parentheses",
        "r11 without its colon", after=later))
    assert _mark(root, capsys) == _stale(4, 2)


@pytest.mark.parametrize("row", [
    pytest.param("|   2026-09-24   |  user  |     r4:   blanks around the cell     |\n",
                 id="blanks-around-the-cell"),
    pytest.param("| 2026-09-24 | user | r4: a row without its closing pipe\n",
                 id="no-closing-pipe"),
    pytest.param("| 2026-09-24 | user | r4: a cell holding an escaped \\| pipe |\n",
                 id="escaped-pipe"),
    pytest.param("| 2026-09-24 | user | r4: ready: lower case is not intake's row |\n",
                 id="lower-case-ready"),
    pytest.param("| 2026-09-24 | user | r4: measured: lower case is not a Measured row |\n",
                 id="lower-case-measured"),
    pytest.param("| 2026-09-24 | user | r4: a row with blanks after its closing pipe |   \n",
                 id="blanks-after-the-row"),
])
def test_sc5_1_a_row_counts_when_its_last_cell_opens_on_its_revision(tmp_path, capsys, row):
    root = _repo(tmp_path, _document(*BASE, _ready(3, 2), after=row))
    assert _mark(root, capsys) == _stale(4, 2)


@pytest.mark.parametrize("cell", [
    pytest.param("r3: Ready: contract validates ready-green, derived from r2, in session 51",
                 id="comma"),
    pytest.param("r3: Ready: contract validates ready-green, derived from r2.", id="full-stop"),
    pytest.param("r3:   Ready:   derived from r2", id="blanks"),
    pytest.param("r3:Ready: derived from r2", id="no-blank"),
    pytest.param("r3: Ready: derived from r1, then derived from r2", id="first-named"),
])
def test_sc5_1_a_ready_row_names_its_revision_by_derived_from(tmp_path, capsys, cell):
    expected = 1 if cell.endswith("then derived from r2") else 2
    root = _repo(tmp_path, _document(*BASE, cell, "r4: The solution half"))
    assert _mark(root, capsys) == _stale(4, expected)


# --- SC5.2 a missing document or Ready row says so, never a match ------------------------

def _surfaces(root, capsys):
    return _feature(root, capsys), _query(root, capsys), _pane_line(root, capsys)


def test_sc5_2_a_feature_with_no_feature_document_reads_no_feature_document(tmp_path, capsys):
    root = _repo(tmp_path)
    line, query, pane = _surfaces(root, capsys)
    assert line == f"{HEAD} [doing] {NO_DOCUMENT} | {INTENT}"
    assert query == [f"{HEAD} [doing] {NO_DOCUMENT}", f"summary: {INTENT}",
                     f"file: specs/{CID}/contract.yaml:1"]
    assert pane == line


def test_sc5_2_a_folder_at_the_documents_path_reads_no_feature_document(tmp_path, capsys):
    root = _repo(tmp_path)
    folder = root / "docs" / "features" / f"{CID}.md"
    folder.mkdir(parents=True)
    (folder / "notes.md").write_text(_document(*BASE, _ready(3, 2)), encoding="utf-8")
    assert _feature(root, capsys) == f"{HEAD} [doing] {NO_DOCUMENT} | {INTENT}"


@pytest.mark.parametrize("document", [
    pytest.param("# apply-discount - Apply one discount code per order\n", id="no-table"),
    pytest.param("", id="empty-file"),
    pytest.param(_document(*BASE), id="no-ready-row"),
    pytest.param(_document(*BASE, "r3: Ready: contract `apply-discount` validates ready-green"),
                 id="ready-row-without-derived-from"),
    pytest.param(_document(*BASE, "Ready: derived from r2"), id="ready-row-without-its-revision"),
    pytest.param(_document(*BASE, after="\n" + _table(_ready(3, 2))),
                 id="ready-row-in-a-later-table"),
    pytest.param(_document(*BASE, "r3: ready: derived from r2"), id="lower-case-ready"),
    pytest.param(_document(*BASE, "r3: Ready: Derived from r2"), id="capital-derived"),
    pytest.param(_document(*BASE, "r3: derived from r2"), id="derived-from-outside-ready"),
    pytest.param(_document(*BASE, "r3: Measured: derived from r2"), id="measured-row"),
])
def test_sc5_2_a_document_with_no_readable_ready_row_reads_no_ready_row(
        tmp_path, capsys, document):
    root = _repo(tmp_path, document)
    line, query, pane = _surfaces(root, capsys)
    assert line == f"{HEAD} [doing] {NO_READY}{TAIL}"  # the doc: part still shows
    assert query == [f"{HEAD} [doing] {NO_READY}", f"summary: {INTENT}",
                     f"doc: docs/features/{CID}.md:1", f"file: specs/{CID}/contract.yaml:1"]
    assert pane == line


def test_sc5_2_a_document_that_is_not_valid_utf8_reads_no_ready_row_and_prints_nothing_on_stderr(
        tmp_path, capsys):
    document = _document(*BASE, _ready(3, 2)).encode("utf-8") + b"| 2026 | user | r4: \xff\xfe |\n"
    root = _repo(tmp_path, document)
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert (code, err) == (0, "")
    assert f"{HEAD} [doing] {NO_READY}{TAIL}" in out.splitlines()
    assert _query(root, capsys)[0] == f"{HEAD} [doing] {NO_READY}"


def test_sc5_2_neither_missing_piece_reads_as_a_match(tmp_path, capsys):
    root = _repo(tmp_path, _document(*BASE, _ready(3, 2)))
    # beta: no document, and closed, so it reads done with its close's evidence
    _dump(root / "specs" / "beta" / "contract.yaml",
          _contract("beta", title=None, intent="A second feature, which has no document."))
    _dump(root / ".sdlc" / "progress" / "beta.yaml", {"records": [
        {"item": "beta", "state": "done", "at": "2026-09-25T09:00:00Z", "head": "9f8e7d6"}]})
    # gamma: a document whose table holds no revision at all
    _dump(root / "specs" / "gamma" / "contract.yaml",
          _contract("gamma", title="A third feature", intent="A third feature."))
    _put_document(root, "gamma", HEADER)
    lines, err = _print(root, capsys)
    assert err == ""
    tops = [text for text in lines if not text.startswith(" ")]
    assert tops == [
        f"{HEAD} [doing]{TAIL}",
        f"beta (no title) [done] {NO_DOCUMENT} at 9f8e7d6 | A second feature, which has no document.",
        f"gamma A third feature [to do] {NO_READY} doc: docs/features/gamma.md | A third feature."]


# --- done_means: the tree only reads; intake writes the Ready row ------------------------

def test_an_unreadable_document_adds_no_stderr_line_and_an_unreadable_source_still_one(
        tmp_path, capsys):
    root = _repo(tmp_path, b"\xff\xfe not text")
    broken = root / "specs" / "broken" / "contract.yaml"
    broken.parent.mkdir(parents=True)
    broken.write_text("id: [unclosed\n", encoding="utf-8")
    lines, err = _print(root, capsys)
    assert err.splitlines() == [
        "taskcontract tree: unreadable contract: specs/broken/contract.yaml (YAML error at line 2)"]
    assert f"broken (no title) [to do] {NO_DOCUMENT}" in lines
    assert f"{HEAD} [doing] {NO_READY}{TAIL}" in lines


def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns,
                                        p.read_bytes() if p.is_file() else None)
            for p in root.rglob("*")}


def test_the_tree_reads_each_feature_document_and_writes_no_file(tmp_path, capsys):
    root = _repo(tmp_path, _document(*BASE, _ready(3, 2), "r4: The solution half"))
    before = _snapshot(root)
    assert _feature(root, capsys) == EXAMPLE
    assert _query(root, capsys)[0] == f"{HEAD} [doing] {_stale(4, 2)}"
    assert _pane_line(root, capsys) == EXAMPLE
    assert _snapshot(root) == before  # no file written, the contract untouched


def _step(text, label):
    start = re.search(rf"^{label}\. ", text, re.MULTILINE).start()
    end = text.find("\n\nI", start + 1)
    return text[start:end if end > 0 else None]


def test_intake_writes_the_ready_row_in_the_shape_the_tree_reads(tmp_path, capsys):
    text = FLOW.read_text(encoding="utf-8")
    assert READY_RULE in _step(text, "I7")
    assert text.count("Ready:") == 1  # one place says it
    # the flow stays a PromptLang prompt under its ceiling
    assert text.startswith("---\n")
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    assert all(f"</{tag}>" in text for tag in ("purpose", "instructions"))
    assert len(text) < CHAR_CEILING
    # the row, filled in as intake writes it, is the one the tree reads
    cell = READY_CELL.format(n=3, m=2, id=CID)
    root = _repo(tmp_path, _document(*BASE, cell))
    assert _mark(root, capsys) is None
    _append_after_table(root, "r4: The solution half")
    assert _mark(root, capsys) == _stale(4, 2)
