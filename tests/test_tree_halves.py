"""The revisions-and-halves suite (contract tree-first-level, unit t3-halves).

A feature before intake names its document's revision as a mark after its
status, `no contract: document rN`: rN is the highest revision of a text
row, a row of the document's first table whose last cell opens on `r<N>:`
and then on none of `Ready:`, `Measured:` or `Signed:`. A document with no
text row, or that cannot be read as text, shows `no revision table` there
instead (SC3.1, SC3.2).

After its verdicts come its two halves, the items `<id>/request` (plain
name `Request half`) and `<id>/solution` (`Solution half`), in that order.
A seat signs a half with a row whose last cell opens `rN:`, then (blanks
there as the tree already reads them) the fixed words `Signed: request
half` or `Signed: solution half`: case as shown, one space between them,
the half's name ending at a word's end; free words may follow (ADR 0034).
Such a row signs the text row above it with the highest revision, a tie
going to the lower row. It is no signature when no text row stands above
it, or its `Revised By` cell (the cell before the last) is blank or
missing. A half's latest signature counts: the highest rN, a tie going to
the lower row. A signed half reads `[done] by <signer> at rN`, the signer
its `Revised By` cell and rN the text row it signs; an unsigned half reads
`[to do]` with no evidence (SC3.1, SC3.2).

The feature rolls up its verdicts but the inactive one, and its halves: it
reads `to do` until a half is signed, then `doing`. `taskcontract tree
<id>/request` prints the half's line, then `file: docs/features/<id>.md:<L>`,
L the line of the row whose signature counts, else 1; the pane's cursor
line shows the same reference. `taskcontract progress` refuses a half's id.

Every row that opens `Signed:`, a signature or not, stays out of the
document's revision, both in this mark and in the drift mark of a feature
with a contract; a feature with a contract shows no halves, and its roll-up
still reads its units and verdicts but the inactive one (SC3.3, SC4.3).

The fixture repos sit under tmp_path, outside any git repository; two
tests read the kit's own tree.
"""

from __future__ import annotations

import asyncio
import builtins
import importlib
import importlib.util
import io
import os
import re
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

NAME = "Apply one discount code per order"
INTENT = ("A fixture contract for the halves suite; its one unit carries one "
          "sketch line.")
HIDDEN = "Words of the statement the tree never prints."
FREE = "Free words after the signature the tree never prints."

ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
DIAGNOSTIC = re.compile(r"^(?P<indent>(?:  )*)- (?P<text>.*)$")

VERDICT_LINES = [
    "  {fid}/G0 Planning / Intake [to do]",
    "    {fid}/G0/G0.1 Definition-of-ready [to do]",
    "    {fid}/G0/G0.2 Vocabulary coverage [to do]",
    "    {fid}/G0/G0.3 Unit confirmation [to do]",
    "  {fid}/G1 Requirements / Spec [to do] inactive",
    "    {fid}/G1/G1.1 Spec/schema linting [to do]",
    "    {fid}/G1/G1.2 Model checking [to do]",
    "    {fid}/G1/G1.3 Criteria completeness + ambiguity review [to do]",
]


KIT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, and find no git repo above
    the fixture."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


# --- the fixture repositories -------------------------------------------------

def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _contract(cid, **fields):
    """A contract that reads ready-green, but for the fields given."""
    doc = {"id": cid, "intent": INTENT, "scope": ["src/"], "non_goals": ["No other work"],
           "decomposition": [{"unit": "work for u1-work", "id": "u1-work",
                              "confirmed_by": ["user"],
                              "done_means": "the work for u1-work is done",
                              "acceptance_sketch": ["verify the work holds (SC1.1)"]}],
           "dependencies": [], "entities": [], "provenance": {"origin": "human-request"}}
    doc.update(fields)
    return doc


def _repo(tmp_path, gates=("G0",), name="repo"):
    root = tmp_path / name
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates)})
    write_seat_roster(root)
    return root


def _write_contract(root, cid, **fields):
    _dump(root / "specs" / cid / "contract.yaml", _contract(cid, **fields))


def _row_text(row):
    """One revision row: a raw line that opens on `|` as given; a (signer,
    changes) pair; or a changes cell alone, signed off by `user`."""
    if isinstance(row, str) and row.startswith("|"):
        return row
    by, changes = row if isinstance(row, tuple) else ("user", row)
    return f"| 2026-09-28 | {by} | {changes} |"


def _doc(root, fid, rows=("r1: First draft",), title=NAME, text=None):
    """docs/features/<fid>.md: its title line, a blank line, its revision
    table (rows from line 5 on), then words the tree never prints."""
    path = root / "docs" / "features" / f"{fid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    elif text is not None:
        path.write_text(text, encoding="utf-8")
    else:
        path.write_text(
            f"# {fid} - {title}\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
            + "".join(_row_text(row) + "\n" for row in rows)
            + f"\n## Statement\n\n{HIDDEN}\n", encoding="utf-8")
    return path


def _line_of(path, text):
    """The 1-based line of the only line in the file that holds `text`."""
    found = [n for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
             if text in line]
    assert len(found) == 1, (text, found)
    return found[0]


# --- driving the CLI and reading its print --------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _print(root, capsys):
    """(rows, stdout, stderr) of the whole tree, which exits 0."""
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    rows = []
    for text in out.splitlines():
        diagnostic = DIAGNOSTIC.match(text)
        if diagnostic:
            assert rows, f"a diagnostic line opens the print: {text!r}"
            rows[-1]["diagnostics"].append(diagnostic["text"])
            continue
        item = ITEM.match(text)
        assert item, f"neither an item line nor a diagnostic line: {text!r}"
        rows.append({"depth": len(item["indent"]) // 2, "id": item["id"], "tag": item["tag"],
                     "name": item["name"], "rest": item["rest"], "line": text,
                     "diagnostics": []})
    return rows, out, err


def _row(rows, rid):
    for row in rows:
        if row["id"] == rid:
            return row
    raise AssertionError(f"{rid} not printed")


def _block(out, rid):
    """The whole tree's lines from the top-level item `rid` to the next
    top-level item."""
    lines = out.splitlines()
    start = next((i for i, text in enumerate(lines) if text.startswith(rid + " ")), None)
    assert start is not None, f"{rid} not printed at the first level"
    end = next((i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
               len(lines))
    return lines[start:end]


def _feature(rows, fid, name=NAME, status="to do"):
    """A feature before intake's line, by its parts: at the first level, its
    id, its plain name and status first, its `doc:` reference last; returns
    its marks, the words between the status and the reference."""
    row = _row(rows, fid)
    line = row["line"]
    assert row["depth"] == 0, line
    head = f"{fid} {name} [{status}]"
    tail = f" doc: docs/features/{fid}.md"
    assert line.startswith(head), line
    assert line.endswith(tail), line
    return line[len(head):len(line) - len(tail)]


def _has_mark(marks, mark):
    return re.search(rf"(?:^| ){re.escape(mark)}(?: |$)", marks) is not None


def _halves(fid, request="[to do]", solution="[to do]"):
    return [f"  {fid}/request Request half {request}",
            f"  {fid}/solution Solution half {solution}"]


def _half(rows, rid):
    return _row(rows, rid)["line"]


# --- SC3.1: the document's newest revision ------------------------------------

REVISIONS = {
    # one text row
    "one-row": (("r1: First draft",), "r1", "to do"),
    # the highest revision, not the last row
    "highest-not-last": (("r1: First draft", "r5: A later edit", "r3: An edit"), "r5", "to do"),
    # Ready:, Measured: and Signed: rows stay out, however high their rN
    "status-rows-left-out": (
        ("r1: First draft", "r2: Measured: checks before signing", "r3: The request half",
         "r4: Signed: request half. The PO seat signs r3", "r5: Ready: derived from r3",
         "r6: Measured: later checks", "r7: Signed: solution half"), "r3", "doing"),
    # blanks after `rN:` read as the tree already reads them
    "blanks-after-the-colon": (
        ("r1: First draft", "r2:Signed: request half", "r3:   Measured: checks"), "r1", "doing"),
}


@pytest.mark.parametrize("case", list(REVISIONS))
def test_sc3_1_a_feature_before_intake_names_its_documents_newest_text_revision(
        tmp_path, capsys, case):
    doc_rows, revision, status = REVISIONS[case]
    root = _repo(tmp_path)
    _doc(root, "x", doc_rows)
    rows, _, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x", status=status)
    assert _has_mark(marks, f"no contract: document {revision}"), marks
    assert "no revision table" not in marks


def test_sc3_1_each_half_shows_its_signer_and_the_revision_it_signs(tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "x", ["r1: First draft", "r2: The request half",
                     ("ana", f"r3: Signed: request half. The PO seat signs r2. {FREE}"),
                     "r4: The solution half",
                     ("ben", f"r5: Signed: solution half, {FREE}")])
    files = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
    rows, out, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x", status="doing")
    assert _has_mark(marks, "no contract: document r4"), marks
    # The verdicts first, then the two halves, in that order, each line whole.
    assert _block(out, "x")[1:] == [line.format(fid="x") for line in VERDICT_LINES] + _halves(
        "x", "[done] by ana at r2", "[done] by ben at r4")
    # The tree prints no other words of the document, and writes no file.
    assert FREE not in out and HIDDEN not in out
    assert sorted(p.relative_to(root).as_posix() for p in root.rglob("*")) == files


def test_sc3_1_an_unsigned_half_reads_to_do_with_no_evidence(tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "x", ["r1: First draft", "r2: The request half"])
    rows, out, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x")
    assert _has_mark(marks, "no contract: document r2"), marks
    assert _block(out, "x")[-2:] == _halves("x")
    # The halves never count at a gate: gates/G0 still reads its verdict.
    assert (_row(rows, "gates/G0")["tag"], _row(rows, "gates/G0")["diagnostics"]) == (
        "to do", ["x holds G0 at to do"])


SIGNED = {
    "none": ((), "to do", "[to do]", "[to do]"),
    "request": ((("ana", "r3: Signed: request half"),), "doing",
                "[done] by ana at r2", "[to do]"),
    "solution": ((("ben", "r3: Signed: solution half"),), "doing",
                 "[to do]", "[done] by ben at r2"),
    # still `doing`: its G0 verdict reads `to do`
    "both": ((("ana", "r3: Signed: request half"), ("ben", "r4: Signed: solution half")),
             "doing", "[done] by ana at r2", "[done] by ben at r2"),
}


@pytest.mark.parametrize("case", list(SIGNED))
def test_sc3_1_the_feature_reads_to_do_until_a_half_is_signed_then_doing(
        tmp_path, capsys, case):
    signatures, status, request, solution = SIGNED[case]
    root = _repo(tmp_path)
    _doc(root, "x", ["r1: First draft", "r2: The request half", *signatures])
    rows, out, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x", status=status)
    assert _has_mark(marks, "no contract: document r2"), marks
    assert _block(out, "x")[-2:] == _halves("x", request, solution)
    assert _row(rows, "gates/G0")["tag"] == "to do"


LATEST = {
    # the higher rN, lower in the table
    "higher-revision-later": (
        ["r1: First draft", ("ana", "r2: Signed: request half"), "r3: An edit",
         ("ben", "r4: Signed: request half")], "[done] by ben at r3", "r4: Signed"),
    # the higher rN wins wherever it stands; it signs the text rows above it only
    "higher-revision-earlier": (
        ["r1: First draft", ("ana", "r5: Signed: request half"), "r2: An edit",
         ("ben", "r3: Signed: request half")], "[done] by ana at r1", "r5: Signed"),
    # a tie in rN goes to the lower row
    "tie-to-the-lower-row": (
        ["r1: First draft", ("ana", "r2: Signed: request half, first"),
         ("ben", "r2: Signed: request half, second")], "[done] by ben at r1", "second"),
    # the text row above it with the highest revision, not the nearest
    "highest-text-row-above": (
        ["r1: First draft", "r4: An edit", "r2: An older edit",
         ("ana", "r5: Signed: request half")], "[done] by ana at r4", "r5: Signed"),
    # a text row below the signature is not what it signs
    "text-row-below": (
        ["r1: First draft", ("ana", "r2: Signed: request half"), "r3: A later edit"],
        "[done] by ana at r1", "r2: Signed"),
}


@pytest.mark.parametrize("case", list(LATEST))
def test_sc3_1_a_halfs_latest_signature_counts(tmp_path, capsys, case):
    doc_rows, request, counted = LATEST[case]
    root = _repo(tmp_path)
    path = _doc(root, "x", doc_rows)
    rows, _, err = _print(root, capsys)
    assert err == ""
    _feature(rows, "x", status="doing")
    assert _half(rows, "x/request") == f"  x/request Request half {request}"
    assert _half(rows, "x/solution") == "  x/solution Solution half [to do]"
    # The query's reference names the row whose signature counts.
    assert _call(["tree", "x/request", "--root", str(root)], capsys) == (
        0, f"x/request Request half {request}\n"
           f"file: docs/features/x.md:{_line_of(path, counted)}\n", "")


def test_sc3_1_the_query_prints_a_halfs_line_then_its_file_reference(tmp_path, capsys):
    root = _repo(tmp_path)
    path = _doc(root, "x", ["r1: First draft", "r2: The request half",
                            ("ana", "r3: Signed: request half. The PO seat signs r2"),
                            "r4: An edit"])
    signed = _line_of(path, "r3: Signed")
    assert signed == 7
    assert _call(["tree", "x/request", "--root", str(root)], capsys) == (
        0, "x/request Request half [done] by ana at r2\nfile: docs/features/x.md:7\n", "")
    # An unsigned half: line 1, and no `page:` or `doc:` line.
    assert _call(["tree", "x/solution", "--root", str(root)], capsys) == (
        0, "x/solution Solution half [to do]\nfile: docs/features/x.md:1\n", "")
    # The feature's own query stays as it was: its line cut after the marks,
    # then its `doc:` reference.
    assert _call(["tree", "x", "--root", str(root)], capsys) == (
        0, f"x {NAME} [doing] no contract: document r4\ndoc: docs/features/x.md:1\n", "")


def test_sc3_1_the_cursor_line_on_a_half_shows_its_file_reference(tmp_path):
    pytest.importorskip("textual")
    root = _repo(tmp_path)
    path = _doc(root, "x", ["r1: First draft", ("ana", "r2: Signed: request half")])
    signed = _line_of(path, "r2: Signed")
    shown = _pane(root, ["x", "x/request", "x/solution"])
    assert [cursor for _, cursor in shown] == [
        f"docs/features/x.md:1 | {NAME}",
        f"docs/features/x.md:{signed} | Request half",
        "docs/features/x.md:1 | Solution half"]
    # A half's label: its id's last segment, then the line the tree prints.
    assert [label for label, _ in shown[1:]] == [
        "request Request half [done] by ana at r1", "solution Solution half [to do]"]


def test_constraint_4_a_feature_document_is_read_once_per_print(tmp_path, capsys, monkeypatch):
    root = _repo(tmp_path)
    before = _doc(root, "x", ["r1: First draft", ("ana", "r2: Signed: request half")])
    _write_contract(root, "c")
    after = _doc(root, "c", ["r1: First draft", "r2: Ready: derived from r1",
                             ("ana", "r3: Signed: solution half")])
    opened = []
    original = builtins.open

    def counting(file, *args, **kwargs):
        if isinstance(file, (str, bytes, os.PathLike)):
            opened.append(Path(os.fsdecode(file)).resolve())
        return original(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", counting)
    monkeypatch.setattr(io, "open", counting)
    _print(root, capsys)
    # Each document opens once, a feature before intake's and a contract's.
    assert (opened.count(before.resolve()), opened.count(after.resolve())) == (1, 1)


def test_progress_refuses_a_halfs_id(tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "x", ["r1: First draft", ("ana", "r2: Signed: request half")])
    for half in ("x/request", "x/solution"):
        assert _call(["progress", "done", half, "--root", str(root)], capsys) == (
            2, "", f"taskcontract progress: '{half}' is a half, not a task, unit or "
                   "contract - done takes a task, unit or contract id\n")
        assert _call(["progress", "start", half, "--root", str(root)], capsys) == (
            2, "", f"taskcontract progress: '{half}' is a half, not a task - "
                   "start takes a task id\n")
    assert not (root / ".sdlc" / "progress").exists()


# --- SC3.2: no revision table, and forms that are no signature ------------------

NO_TEXT_ROW = {
    "header-only-table": ("# x - A title\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n",
                          "A title"),
    "rows-without-revision": ("# x - A title\n\n| Date | Revised By | Change |\n"
                              "| :-- | :-- | :-- |\n| 2026-09-28 | user | First draft |\n",
                              "A title"),
    "no-table": ("# x - A title\n\nOnly words, no table.\n", "A title"),
    "empty": ("", "(no title)"),
    # every counted row opens Ready:, Measured: or Signed:
    "status-rows-only": ("# x - A title\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                         "| 2026-09-28 | user | r1: Measured: checks |\n"
                         "| 2026-09-28 | user | r2: Ready: derived from r1 |\n"
                         "| 2026-09-28 | ana | r3: Signed: request half |\n", "A title"),
    "not-text": (("# x - Caf\xe9 au lait\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                  "| 2026-09-28 | user | r1: First draft |\n"
                  "| 2026-09-28 | ana | r2: Signed: request half |\n").encode("latin-1"),
                 "(no title)"),
}


@pytest.mark.parametrize("case", list(NO_TEXT_ROW))
def test_sc3_2_a_document_with_no_text_row_shows_no_revision_table(tmp_path, capsys, case):
    text, name = NO_TEXT_ROW[case]
    root = _repo(tmp_path)
    _doc(root, "x", text=text)
    rows, out, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x", name=name)
    assert _has_mark(marks, "no revision table"), marks
    assert "no contract:" not in marks
    assert _block(out, "x")[-2:] == _halves("x")
    for half, plain in (("request", "Request half"), ("solution", "Solution half")):
        assert _call(["tree", f"x/{half}", "--root", str(root)], capsys) == (
            0, f"x/{half} {plain} [to do]\nfile: docs/features/x.md:1\n", "")


NOT_SIGNATURES = {
    # rows that open `Signed:` stay out of the revision
    "halfway": ("r2: Signed: request halfway", "r1"),
    "capital-request": ("r2: Signed: Request half", "r1"),
    "capital-solution": ("r2: Signed: Solution half", "r1"),
    "two-spaces-between-the-words": ("r2: Signed: request  half", "r1"),
    "two-spaces-after-signed": ("r2: Signed:  solution half", "r1"),
    "neither-half": ("r2: Signed: the whole document", "r1"),
    "solution-half-then-a-digit": ("r2: Signed: solution half2", "r1"),
    # rows that open on none of the three are text rows
    "no-colon": ("r2: Signed request half", "r2"),
    "in-words": ("r2: The request half, signed by the PO seat (user)", "r2"),
    "later-in-the-cell": ("r2: Restated. Signed: request half", "r2"),
}


@pytest.mark.parametrize("case", list(NOT_SIGNATURES))
def test_sc3_2_a_signature_in_any_other_form_is_no_signature(tmp_path, capsys, case):
    form, revision = NOT_SIGNATURES[case]
    root = _repo(tmp_path)
    _doc(root, "x", ["r1: First draft", ("ana", form)])
    rows, out, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x")
    assert _has_mark(marks, f"no contract: document {revision}"), marks
    assert _block(out, "x")[-2:] == _halves("x")


SIGNATURES = {
    "bare": ("r2: Signed: request half", "request"),
    "full-stop-then-words": ("r2: Signed: request half. The PO seat signs r1", "request"),
    "comma-then-words": ("r2: Signed: request half, restated", "request"),
    "no-blank-after-the-colon": ("r2:Signed: request half", "request"),
    "blanks-after-the-colon": ("r2:   Signed: request half", "request"),
    "solution": ("r2: Signed: solution half.", "solution"),
}


@pytest.mark.parametrize("case", list(SIGNATURES))
def test_sc3_2_the_fixed_words_sign_with_free_words_after(tmp_path, capsys, case):
    form, half = SIGNATURES[case]
    root = _repo(tmp_path)
    _doc(root, "x", ["r1: First draft", ("ana", form)])
    rows, out, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x", status="doing")
    assert _has_mark(marks, "no contract: document r1"), marks
    signed = "[done] by ana at r1"
    assert _block(out, "x")[-2:] == _halves(
        "x", signed if half == "request" else "[to do]",
        signed if half == "solution" else "[to do]")


SIGNERS = {
    # no text row above it: no signature
    "no-text-row-above": ([("ben", "r9: Signed: request half"), "r1: First draft"],
                          "[to do]", None),
    # ... and the half reads its next-latest signature
    "no-text-row-above-falls-back": (
        [("ben", "r9: Signed: request half"), "r1: First draft",
         ("ana", "r2: Signed: request half")], "[done] by ana at r1", "r2: Signed"),
    "blank-signer": (["r1: First draft", ("", "r2: Signed: request half")], "[to do]", None),
    "blank-signer-falls-back": (
        ["r1: First draft", ("ana", "r2: Signed: request half"),
         ("   ", "r3: Signed: request half")], "[done] by ana at r1", "r2: Signed"),
    # a row with fewer than three cells has no Revised By cell
    "one-cell-row": (["r1: First draft", "| r2: Signed: request half |"], "[to do]", None),
    "two-cell-row": (["r1: First draft", "| ana | r2: Signed: request half |"],
                     "[to do]", None),
    # the signer is the cell before the changes cell
    "four-cell-row": (["r1: First draft", "| 2026-09-28 | a note | carol | r2: Signed: request half |"],
                      "[done] by carol at r1", "r2: Signed"),
}


@pytest.mark.parametrize("case", list(SIGNERS))
def test_sc3_2_a_signed_row_with_no_text_row_above_or_no_signer_is_no_signature(
        tmp_path, capsys, case):
    doc_rows, request, counted = SIGNERS[case]
    root = _repo(tmp_path)
    path = _doc(root, "x", doc_rows)
    rows, _, err = _print(root, capsys)
    assert err == ""
    marks = _feature(rows, "x", status="to do" if request == "[to do]" else "doing")
    assert _has_mark(marks, "no contract: document r1"), marks
    assert _half(rows, "x/request") == f"  x/request Request half {request}"
    line = 1 if counted is None else _line_of(path, counted)
    assert _call(["tree", "x/request", "--root", str(root)], capsys) == (
        0, f"x/request Request half {request}\nfile: docs/features/x.md:{line}\n", "")


# --- SC3.3 and SC4.3: a feature with a contract ---------------------------------

def test_sc3_3_a_signed_row_never_ages_a_contracts_drift_mark(tmp_path, capsys):
    root = _repo(tmp_path)
    ready = "r2: Ready: contract validates ready-green, derived from r1"
    docs = {
        # a signature after the Ready: row
        "a-signed": ["r1: First draft", ready, ("ana", "r3: Signed: solution half")],
        # a Signed: row that is no signature
        "b-no-signature": ["r1: First draft", ready, ("ana", "r3: Signed: the whole document")],
        # a text row still ages it, the Signed: row above it never
        "c-stale": ["r1: First draft", ready, "r3: A later edit",
                    ("ana", "r4: Signed: request half")],
        "d-no-ready": ["r1: First draft", ("ana", "r2: Signed: request half")],
        "e-no-doc": None,
    }
    marks = {"a-signed": "", "b-no-signature": "",
             "c-stale": " stale: document r3, contract from r1",
             "d-no-ready": ' no "Ready:" row', "e-no-doc": " no feature document"}
    for cid, doc_rows in docs.items():
        _write_contract(root, cid)
        if doc_rows is not None:
            _doc(root, cid, doc_rows)
    _doc(root, "z-doc", ["r1: First draft", ("ana", "r2: Signed: request half")])
    rows, out, err = _print(root, capsys)
    assert err == ""
    ids = [row["id"] for row in rows]
    for cid, mark in marks.items():
        doc = "" if cid == "e-no-doc" else f" doc: docs/features/{cid}.md"
        assert _row(rows, cid)["line"] == f"{cid} (no title) [to do]{mark}{doc} | {INTENT}"
        # A feature with a contract shows no revision and no halves.
        assert f"{cid}/request" not in ids and f"{cid}/solution" not in ids
        assert "no contract:" not in "\n".join(_block(out, cid))
    assert _block(out, "z-doc")[-2:] == _halves("z-doc", "[done] by ana at r1")


ROLL_UPS = {
    # G0 active: the halves count beside the G0 verdict, never the inactive G1
    "g0-active": (("G0",), {"p-none": "to do", "p-request": "doing", "p-both": "doing"}),
    # no gate active: G0 is the inactive verdict and stays out, so the halves
    # decide, and a feature before intake never reads done
    "none-active": ((), {"p-none": "to do", "p-request": "doing", "p-both": "doing"}),
}


@pytest.mark.parametrize("case", list(ROLL_UPS))
def test_sc4_3_a_features_roll_up_counts_its_halves_units_and_verdicts_but_the_inactive_one(
        tmp_path, capsys, case):
    gates, before = ROLL_UPS[case]
    root = _repo(tmp_path, gates=gates)
    for cid in ("a-open", "b-started", "c-closed"):
        _write_contract(root, cid)
    _write_contract(root, "d-closed-red", intent="Too short.")  # G0 reads failed at draft
    assert _call(["progress", "done", "b-started/u1-work/write-tests", "--root", str(root)],
                 capsys)[0] == 0
    for cid in ("c-closed", "d-closed-red"):
        assert _call(["progress", "done", cid, "--root", str(root)], capsys)[0] == 0
    _doc(root, "p-none", ["r1: First draft"])
    _doc(root, "p-request", ["r1: First draft", ("ana", "r2: Signed: request half")])
    _doc(root, "p-both", ["r1: First draft", ("ana", "r2: Signed: request half"),
                          ("ben", "r3: Signed: solution half")])
    rows, _, err = _print(root, capsys)
    assert err == ""
    for fid, status in before.items():
        marks = _feature(rows, fid, status=status)
        assert _has_mark(marks, "no contract: document r1"), marks
    assert _half(rows, "p-both/solution") == "  p-both/solution Solution half [done] by ben at r1"
    # A feature with a contract still rolls up its units and verdicts but the
    # inactive one, and a closed one reads done once its units do.
    g0 = "done" if "G0" in gates else "to do"
    assert {cid: _row(rows, cid)["tag"] for cid in
            ("a-open", "b-started", "c-closed", "d-closed-red")} == {
        "a-open": "to do", "b-started": "doing", "c-closed": "done", "d-closed-red": "done"}
    assert _row(rows, "c-closed/G0")["tag"] == g0
    if "G0" in gates:
        assert _row(rows, "d-closed-red/G0")["tag"] == "failed"


# --- the kit's own tree -------------------------------------------------------

def test_sc3_1_the_kits_tree_shows_g1s_halves_and_tree_first_level_unaged(capsys):
    rows, _, _ = _print(KIT, capsys)
    marks = _feature(rows, "g1-requirements-spec",
                     name="Failure points found before development starts", status="doing")
    assert _has_mark(marks, "no contract: document r3"), marks
    assert _half(rows, "g1-requirements-spec/request") == (
        "  g1-requirements-spec/request Request half [done] by user at r3")
    assert _half(rows, "g1-requirements-spec/solution") == (
        "  g1-requirements-spec/solution Solution half [to do]")
    assert _row(rows, "gates/G0")["tag"] == "doing"
    assert "g1-requirements-spec holds G0 at to do" in _row(rows, "gates/G0")["diagnostics"]
    # Its r7 is a Signed: row, so its contract matches its document.
    assert "stale:" not in _row(rows, "tree-first-level")["line"]
    code, out, _ = _call(["tree", "g1-requirements-spec/request", "--root", str(KIT)], capsys)
    assert (code, out) == (0, "g1-requirements-spec/request Request half [done] by user at r3\n"
                              "file: docs/features/g1-requirements-spec.md:6\n")


def test_sc3_1_the_pane_on_the_kit_shows_g1s_halves_and_gates_g0_doing():
    pytest.importorskip("textual")
    shown = _pane(KIT, ["gates/G0", "g1-requirements-spec/request",
                        "g1-requirements-spec/solution"])
    assert shown[0][0].startswith("gates/G0 Planning / Intake [doing]"), shown[0]
    assert shown[1] == ("request Request half [done] by user at r3",
                        "docs/features/g1-requirements-spec.md:6 | Request half")
    assert shown[2] == ("solution Solution half [to do]",
                        "docs/features/g1-requirements-spec.md:1 | Solution half")


# --- the pane -------------------------------------------------------------------

async def _settle(pilot):
    for _ in range(3):
        await pilot.pause()
        await pilot.wait_for_scheduled_animations()
    await pilot.pause()


def _pane(root, rids, size=(240, 60)):
    """(label, cursor line) with the cursor on each item id in `rids`, the
    label read before the cursor moves onto it."""
    assert importlib.util.find_spec("taskcontract.pane") is not None
    pane = importlib.import_module("taskcontract.pane")

    def node_of(outline, rid):
        for top in outline.root.children:
            head = top.label.plain.split(" ", 1)[0]
            if rid == head or rid.startswith(head + "/"):
                node = top
                rest = rid[len(head) + 1:]
                for segment in rest.split("/") if rest else []:
                    found = [c for c in node.children
                             if c.label.plain.split(" ", 1)[0] == segment]
                    assert len(found) == 1, (rid, segment)
                    node = found[0]
                return node
        raise AssertionError(f"no top-level line opens {rid!r}")

    async def go():
        app = pane.PaneApp(Path(root))
        shown = []
        async with app.run_test(size=size) as pilot:
            await _settle(pilot)
            outline = app.query_one("#outline")
            for rid in rids:
                node = node_of(outline, rid)
                up = node.parent
                while up is not None and up.parent is not None:
                    up.expand()
                    up = up.parent
                await _settle(pilot)
                label = node.label.plain
                outline.move_cursor(node)
                await _settle(pilot)
                rendered = app.query_one("#cursor").render()
                shown.append((label, rendered.plain if hasattr(rendered, "plain")
                              else str(rendered)))
        return shown

    return asyncio.run(go())
