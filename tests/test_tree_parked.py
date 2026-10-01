"""The parked-row suite (contract feature-document, unit f4-intake).

When intake refuses a feature document it parks it: it adds one row to the
document's revision table whose last cell opens `r<N>: Parked:`, then what
stands, and it writes no contract. The row changes no text (SC4.2), and the
tree reads it so. A counted row that opens, after `r<N>:` and its blanks,
on `Parked:` is no text row, like a `Ready:`, a `Measured:` or a `Signed:`
row:

- it never ages a contract's drift mark: the document's revision is still
  the highest rN of a text row;
- it never moves the revision a feature before intake names, `no contract:
  document rN`, and a table whose counted rows are all such rows reads `no
  revision table`;
- it is never the row a `Signed:` row signs: a signature signs the text row
  above it with the highest rN, whatever `Parked:` rows stand between;
- it is no signature itself, whatever words follow, and its `Revised By`
  cell gives no half a signer.

The match is the prefix the other three words use: a row that only holds
the word later in its cell, or opens on `Parking:` or on `Parked` with no
colon, is a text row still. Apart from this the tree prints what it
printed: a parked document gets no mark, line or status of its own, and
none of the row's words print (the feature document's Constraints, 6).

Each test drives the CLI in process against a fixture repo under tmp_path,
outside any git repository, with G0 active; the fixtures never read the
kit's own feature documents.
"""

from __future__ import annotations

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

NAME = "Apply one discount code per order"
# No fixture id, name or intent holds the row's word, so a print that holds it
# took it from the row.
INTENT = ("A fixture contract for this suite; its one unit carries one "
          "sketch line.")
HIDDEN = "Words of the statement the tree never prints."
# What stands, as intake writes it after `Parked:`.
WHAT = "Check SC2.3 is assigned to no unit."
READY = "r2: Ready: contract validates ready-green, derived from r1"


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


def _repo(tmp_path, name="repo"):
    root = tmp_path / name
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": ["G0"]})
    write_seat_roster(root)
    return root


def _write_contract(root, cid):
    """A contract with no title, so its feature's plain name is `(no title)`."""
    _dump(root / "specs" / cid / "contract.yaml", {
        "id": cid, "intent": INTENT, "scope": ["src/"], "non_goals": ["No other work"],
        "decomposition": [{"unit": "work for u1-work", "id": "u1-work",
                           "confirmed_by": ["user"],
                           "done_means": "the work for u1-work is done",
                           "acceptance_sketch": ["verify the work holds (SC1.1)"]}],
        "dependencies": [], "entities": [], "provenance": {"origin": "human-request"}})


def _parked(n, what=WHAT, blanks=" "):
    """Intake's row for a document it refuses: its seat cell and its changes."""
    return ("intake", f"r{n}:{blanks}Parked: {what}")


def _doc(root, fid, rows):
    """docs/features/<fid>.md: its title line, a blank line, its revision
    table, then words the tree never prints. A row is a (signer, changes)
    pair, or a changes cell alone, signed off by `user`."""
    path = root / "docs" / "features" / f"{fid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for row in rows:
        by, changes = row if isinstance(row, tuple) else ("user", row)
        lines.append(f"| 2026-10-03 | {by} | {changes} |\n")
    path.write_text(
        f"# {fid} - {NAME}\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
        + "".join(lines) + f"\n## Statement\n\n{HIDDEN}\n", encoding="utf-8")
    return path


# --- driving the CLI and reading its print --------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _print(root, capsys):
    """The whole tree's stdout; it exits 0 and writes nothing on stderr."""
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert (code, err) == (0, "")
    return out


def _query(root, capsys, item):
    """The query's stdout for `item`; it exits 0 with nothing on stderr."""
    code, out, err = _call(["tree", item, "--root", str(root)], capsys)
    assert (code, err) == (0, "")
    return out


def _block(out, rid):
    """The whole tree's lines from the top-level item `rid` to the next
    top-level item."""
    lines = out.splitlines()
    start = next((i for i, text in enumerate(lines) if text.startswith(rid + " ")), None)
    assert start is not None, f"{rid} not printed at the first level"
    end = next((i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
               len(lines))
    return lines[start:end]


def _before(fid, status, mark):
    """A feature before intake's line, whole."""
    return f"{fid} {NAME} [{status}] {mark} doc: docs/features/{fid}.md"


def _with_contract(cid, mark=""):
    """The line of a feature with a contract, whole; `mark` opens on a blank."""
    return f"{cid} (no title) [to do]{mark} doc: docs/features/{cid}.md | {INTENT}"


def _halves(fid, request="[to do]", solution="[to do]"):
    return [f"  {fid}/request Request half {request}",
            f"  {fid}/solution Solution half {solution}"]


def _no_word_of_the_row(out):
    """A parked document gets no mark, line or status of its own."""
    return "Parked" not in out and "parked" not in out and WHAT not in out


# --- SC4.2: a `Parked:` row changes no content, as the tree reads it ------------

def test_sc4_2_a_parked_row_never_ages_a_contracts_drift_mark(tmp_path, capsys):
    root = _repo(tmp_path)
    docs = {
        # a `Parked:` row above the newest `Ready:` row's rM, however high its rN
        "a-one-row": ["r1: First draft", READY, _parked(3)],
        "b-high-rows": ["r1: First draft", READY, _parked(9), _parked(12)],
        # blanks after `rN:` read as the tree already reads them
        "c-blanks": ["r1: First draft", READY, _parked(3, blanks=""),
                     _parked(4, blanks="   ")],
        # a text row still ages it, and the mark names that row, never the `Parked:` one
        "d-stale": ["r1: First draft", READY, "r3: A later edit", _parked(4)],
        # no new mark: a parked document without a `Ready:` row reads as before
        "e-no-ready": ["r1: First draft", _parked(2)],
    }
    marks = {"a-one-row": "", "b-high-rows": "", "c-blanks": "",
             "d-stale": " stale: document r3, contract from r1",
             "e-no-ready": ' no "Ready:" row'}
    for cid, rows in docs.items():
        _write_contract(root, cid)
        _doc(root, cid, rows)
    out = _print(root, capsys)
    for cid, mark in marks.items():
        assert _block(out, cid)[0] == _with_contract(cid, mark)
        first = _query(root, capsys, cid).splitlines()[0]
        assert first == f"{cid} (no title) [to do]{mark}"
    assert _no_word_of_the_row(out)


MOVES_NOTHING = {
    "parked-last": (["r1: First draft", "r2: The request half", _parked(3)], "r2"),
    # the highest rN of a text row, wherever the `Parked:` row stands
    "parked-highest-not-last": (["r1: First draft", _parked(9), "r2: An edit"], "r2"),
    "two-parked": (["r1: First draft", _parked(2), "r3: An edit", _parked(4)], "r3"),
    # blanks after `rN:` read as the tree already reads them
    "no-blank-after-the-colon": (["r1: First draft", _parked(2, blanks="")], "r1"),
    "blanks-after-the-colon": (["r1: First draft", _parked(2, blanks="   ")], "r1"),
}


@pytest.mark.parametrize("case", list(MOVES_NOTHING))
def test_sc4_2_a_parked_row_never_moves_the_revision_a_feature_before_intake_names(
        tmp_path, capsys, case):
    rows, revision = MOVES_NOTHING[case]
    root = _repo(tmp_path)
    _doc(root, "x", rows)
    out = _print(root, capsys)
    block = _block(out, "x")
    assert block[0] == _before("x", "to do", f"no contract: document {revision}")
    assert block[-2:] == _halves("x")
    assert _query(root, capsys, "x").splitlines()[0] == (
        f"x {NAME} [to do] no contract: document {revision}")
    assert _no_word_of_the_row(out)


def test_sc4_2_a_signed_row_below_a_parked_row_signs_the_text_row_above_it(tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "x", ["r1: First draft", "r2: The request half", _parked(3),
                     ("ana", "r4: Signed: request half. The PO seat signs r2"),
                     "r5: The solution half", _parked(6), _parked(7, "OPEN in Decisions."),
                     ("ben", "r8: Signed: solution half. The engineer seat signs r5")])
    out = _print(root, capsys)
    block = _block(out, "x")
    assert block[-2:] == _halves("x", "[done] by ana at r2", "[done] by ben at r5")
    assert block[0] == _before("x", "doing", "no contract: document r5")
    assert _query(root, capsys, "x/request").splitlines()[0] == (
        "x/request Request half [done] by ana at r2")
    assert _no_word_of_the_row(out)


def test_sc4_2_a_parked_row_is_no_signature_and_gives_no_half_a_signer(tmp_path, capsys):
    root = _repo(tmp_path)
    # Its `Revised By` cell is not blank, a text row stands above it, and the
    # fixed words of a signature stand in its cell: still it signs no half.
    _doc(root, "x", ["r1: First draft",
                     ("intake", "r2: Parked: Signed: request half is missing"),
                     ("intake", "r3: Parked: Signed: solution half is missing")])
    out = _print(root, capsys)
    block = _block(out, "x")
    assert block[-2:] == _halves("x")
    # No half is signed, so the feature still reads `to do`, at its text row.
    assert block[0] == _before("x", "to do", "no contract: document r1")
    assert "intake" not in out
    assert "Parked" not in out and "is missing" not in out


NEAR_MISSES = {
    # the word stands later in the cell
    "word-later": "r{n}: SC2.3 goes to unit u2, which answers r8: Parked: {what}",
    # another word opens the cell
    "another-word": "r{n}: Parking: the document waits on a seat",
    # the word with no colon
    "no-colon": "r{n}: Parked the document until a seat answers",
}


@pytest.mark.parametrize("case", list(NEAR_MISSES))
def test_sc4_2_only_a_row_that_opens_on_parked_and_its_colon_is_a_parked_row(
        tmp_path, capsys, case):
    near = NEAR_MISSES[case]
    root = _repo(tmp_path)
    # Before intake: the near miss is the newest text row, the `Parked:` row is not.
    _doc(root, "x", ["r1: First draft", near.format(n=2, what=WHAT), _parked(3),
                     ("ana", "r4: Signed: request half")])
    # With a contract: the near miss ages the drift mark, the `Parked:` row does not.
    _write_contract(root, "c-near")
    _doc(root, "c-near", ["r1: First draft", READY, near.format(n=3, what=WHAT), _parked(4)])
    out = _print(root, capsys)
    block = _block(out, "x")
    assert block[0] == _before("x", "doing", "no contract: document r2")
    assert block[-2:] == _halves("x", "[done] by ana at r2")
    assert _block(out, "c-near")[0] == _with_contract(
        "c-near", " stale: document r3, contract from r1")


def test_sc4_2_a_table_with_parked_rows_prints_the_same_tree_as_the_table_without_them(
        tmp_path, capsys):
    tables = {
        # before intake, one half signed
        "x": (["r1: First draft", "r2: The request half",
               ("ana", "r3: Signed: request half")], [_parked(4)]),
        # before intake, no half signed
        "y": (["r1: First draft"], [_parked(2), _parked(3, "OPEN in Decisions.")]),
        # with a contract that matches its document
        "c-match": (["r1: First draft", READY], [_parked(3)]),
        # with a contract a text row aged
        "d-stale": (["r1: First draft", READY, "r3: A later edit"], [_parked(4)]),
    }
    prints = {}
    for name in ("without", "with"):
        root = _repo(tmp_path, name)
        for fid, (rows, parked) in tables.items():
            if fid in ("c-match", "d-stale"):
                _write_contract(root, fid)
            _doc(root, fid, rows + (parked if name == "with" else []))
        prints[name] = [_print(root, capsys)] + [
            _query(root, capsys, item)
            for item in ("x", "x/request", "x/solution", "y", "c-match", "d-stale")]
    # What the table without the rows prints, so the two never agree on nothing.
    whole = prints["without"][0]
    assert _block(whole, "x")[0] == _before("x", "doing", "no contract: document r2")
    assert _block(whole, "x")[-2:] == _halves("x", "[done] by ana at r2")
    assert _block(whole, "y")[0] == _before("y", "to do", "no contract: document r1")
    assert _block(whole, "c-match")[0] == _with_contract("c-match")
    assert _block(whole, "d-stale")[0] == _with_contract(
        "d-stale", " stale: document r3, contract from r1")
    # Byte for byte the same: no new mark, no new line and no new status.
    assert prints["with"] == prints["without"]


def test_sc4_2_a_table_whose_counted_rows_are_all_parked_rows_reads_no_revision_table(
        tmp_path, capsys):
    root = _repo(tmp_path)
    # No text row stands above the `Signed:` row, so it signs nothing.
    _doc(root, "x", [_parked(1), _parked(2, "OPEN in Decisions."),
                     ("ana", "r3: Signed: request half")])
    out = _print(root, capsys)
    block = _block(out, "x")
    assert block[0] == _before("x", "to do", "no revision table")
    assert block[-2:] == _halves("x")
    assert "no contract:" not in "\n".join(block)
    assert _no_word_of_the_row(out)


# The rows the interview and intake write, in one table's order, as the feature
# document shows them (r2 to r11), under a first row; the contract's id is the
# fixture's.
FID = "apply-discount"
EXAMPLE = [
    ("ann", "r1: Created through the interview"),
    ("ann", "r2: Measured: the checks before signing, on the request half: 4 findings "
            "(CL003 1, CL008 1, CL012 1, CL014 1); ready checks 1 to 8: 1 OPEN"),
    ("ann", "r3: The request half finished: ..."),
    ("ann", "r4: Signed: request half. The PO seat signs r3"),
    ("raj", "r5: Measured: the checks before signing, on the solution half: ..."),
    ("raj", "r6: The solution half finished: ..."),
    ("raj", "r7: Signed: solution half. The engineer seat signs r6"),
    ("intake", "r8: Parked: Check SC2.3 is assigned to no unit."),
    ("raj", "r9: SC2.3 goes to unit u2"),
    ("raj", "r10: Signed: solution half. The engineer seat signs r9"),
    ("intake", f"r11: Ready: contract `{FID}` validates ready-green, derived from r9; the PO "
               "seat (ann) signed the request half at r3 (r4), the engineer seat (raj) the "
               "solution half at r9 (r10)"),
]


def test_sc4_2_the_example_rows_read_unaged_from_the_parked_row_to_the_ready_row(
        tmp_path, capsys):
    root = _repo(tmp_path)
    # Parked at r8: the document still stands at r6, both halves signed.
    _doc(root, FID, EXAMPLE[:8])
    block = _block(_print(root, capsys), FID)
    assert block[0] == _before(FID, "doing", "no contract: document r6")
    assert block[-2:] == _halves(FID, "[done] by ann at r3", "[done] by raj at r6")
    # The seat answers at r9 and signs again at r10.
    _doc(root, FID, EXAMPLE[:10])
    block = _block(_print(root, capsys), FID)
    assert block[0] == _before(FID, "doing", "no contract: document r9")
    assert block[-2:] == _halves(FID, "[done] by ann at r3", "[done] by raj at r9")
    # Ready at r11, derived from r9: the contract matches its document.
    _doc(root, FID, EXAMPLE)
    _write_contract(root, FID)
    out = _print(root, capsys)
    assert _block(out, FID)[0] == _with_contract(FID)
    assert _query(root, capsys, FID).splitlines()[0] == f"{FID} (no title) [to do]"
    assert _no_word_of_the_row(out)
