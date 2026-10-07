"""The pair suite (contract document-split): the tree shows a pair as one feature.

A pair is a requirements document at docs/features/<id>.md and a design
document at docs/features/<id>.design.md. A file whose name ends in
`.design.md` is never a feature of its own, before intake and through it,
and one with no requirements document beside it prints nothing: no feature,
no half, no problem line. A file named exactly `design.md` is a feature with
the id `design`.

Before intake the feature's line carries a second mark after `no contract:
document rN`: `design rN`, the design table's newest text revision, or
`design: no revision table` when that table holds no text row or the file
cannot be read as text. Once a design document stands, its table alone gives
the solution half, and the requirements document's table alone gives the
request half; the solution half's `file:` reference names the design
document, at its counting signature's row, else line 1. The plain name comes
from the requirements document's title line only. A stale design shows no
mark before intake (SC1.3).

Through intake, a contract with a pair reads each table against that table's
own `Ready:` row. The design's mark stands after the requirements document's:
`stale: design rD, contract from rM`. A design at or behind its own row gets
no mark, and neither does one whose table names no `rM` or whose file cannot
be read as text: the design document adds no other drift mark.

A feature with no design document, before intake and through it, prints byte
for byte as it did, a combined document through intake among them. Each
document is opened once per print.

Each test drives the CLI in process against a fixture repo under tmp_path,
outside any git repository, with G0 active, so a contract's verdict reads
`at no commit`. A document here is a revision table and a title line, in the
order the interview writes them.
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

TITLE = "The outcome, in a few words"
OTHER_TITLE = "A title the tree never prints"
INTENT = ("A fixture contract for the pair suite; its one unit carries one "
          "sketch line.")
FREE = "Free words of a row the tree never prints."

ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
DIAGNOSTIC = re.compile(r"^(?P<indent>(?:  )*)- (?P<text>.*)$")

HEADER = "| Revision Date | Revised By | Changes Made |\n| :-: | :-: | :-- |\n"

# The requirements document's rows as the interview writes them: the PO seat
# ann signs r3 with the row on line 6.
REQUIREMENTS = (
    ("ann", "r1: Created through /sdlc:product-specification-interview. The request half, "
            "in progress. PO seat: ann"),
    ("ann", "r2: Measured: the checks before signing, on the request half: 0 findings; "
            "ready checks 1 to 8: 0 OPEN"),
    ("ann", "r3: The request half finished: 7 sections written, 0 OPEN"),
    ("ann", "r4: Signed: request half. The PO seat signs r3"),
)
# The design document's rows: the engineer seat raj signs r3 with the row on line 6.
DESIGN = (
    ("raj", "r1: Created through /sdlc:product-specification-interview. The design, in "
            "progress, against requirements r3. Engineer seat: raj"),
    ("raj", "r2: Measured: the checks before signing, on the solution half: 0 findings; "
            "Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN"),
    ("raj", "r3: The solution half finished: 12 sections written, 0 OPEN"),
    ("raj", "r4: Signed: solution half. The engineer seat signs r3"),
)


def _requirements_ready(cid, n=5, m=3):
    """Intake's `Ready:` row in a requirements document's table."""
    return ("intake", f"r{n}: Ready: contract `{cid}` validates ready-green, derived from "
                      f"r{m}; the PO seat (ann) signed the request half at r{m} (r{m + 1})")


def _design_ready(cid, n=5, m=3):
    """Intake's `Ready:` row in a design document's table."""
    return ("intake", f"r{n}: Ready: contract `{cid}` validates ready-green, derived from "
                      f"r{m}, against requirements r3; the engineer seat (raj) signed the "
                      f"solution half at r{m} (r{m + 1})")


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

# A feature through intake, whole, with G0 active and its contract ready-green.
CONTRACT_LINES = """\
{cid} {name} [to do]{marks} doc: docs/features/{cid}.md | {intent}
  {cid}/G0 Planning / Intake [done] via python -m taskcontract validate specs/{cid}/contract.yaml --profile ready at no commit
    {cid}/G0/G0.1 Definition-of-ready [done]
    {cid}/G0/G0.2 Vocabulary coverage [done]
    {cid}/G0/G0.3 Unit confirmation [done]
  {cid}/G1 Requirements / Spec [to do] inactive
    {cid}/G1/G1.1 Spec/schema linting [to do]
    {cid}/G1/G1.2 Model checking [to do]
    {cid}/G1/G1.3 Criteria completeness + ambiguity review [to do]
  {cid}/u1-work the work for u1-work is done [to do]
    {cid}/u1-work/approve-tests Approve the test list [to do]
    {cid}/u1-work/write-tests Write the tests [to do]
    {cid}/u1-work/prove-red Prove red [to do]
    {cid}/u1-work/green Green [to do]
    {cid}/u1-work/approve-commit Approve the commit [to do]
    {cid}/u1-work/commit Commit [to do]
    {cid}/u1-work/two-key Two-Key PASS [to do]
    {cid}/u1-work/SC1.1 verify the work holds (SC1.1) [to do]
"""


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
    """A repo with G0 active and the seat roster, and no feature yet."""
    root = tmp_path / name
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": ["G0"]})
    write_seat_roster(root)
    return root


def _contract(root, cid, title=TITLE):
    """specs/<cid>/contract.yaml, a contract that reads ready-green."""
    _dump(root / "specs" / cid / "contract.yaml", {
        "id": cid, "title": title, "intent": INTENT, "scope": ["src/"],
        "non_goals": ["No other work"],
        "decomposition": [{"unit": "work for u1-work", "id": "u1-work",
                           "confirmed_by": ["user"],
                           "done_means": "the work for u1-work is done",
                           "acceptance_sketch": ["verify the work holds (SC1.1)"]}],
        "dependencies": [], "entities": [], "provenance": {"origin": "human-request"}})


def _text(fid, rows, title=TITLE):
    """A document: its revision table, rows from line 3 on, a blank line,
    then its title line, or no title line when `title` is None."""
    table = HEADER + "".join(f"| 2026-10-07 | {by} | {changes} |\n" for by, changes in rows)
    return table + (f"\n# {fid} - {title}\n" if title is not None else "")


def _put(path, fid, rows, title, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(_text(fid, rows, title) if text is None else text, encoding="utf-8")
    return path


def _requirements(root, fid, rows=REQUIREMENTS, title=TITLE, text=None):
    """docs/features/<fid>.md, the requirements document."""
    return _put(root / "docs" / "features" / f"{fid}.md", fid, rows, title, text)


def _design(root, fid, rows=DESIGN, title=TITLE, text=None):
    """docs/features/<fid>.design.md, the design document."""
    return _put(root / "docs" / "features" / f"{fid}.design.md", fid, rows, title, text)


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
                     "line": text, "diagnostics": []})
    return rows, out, err


def _row(rows, rid):
    for row in rows:
        if row["id"] == rid:
            return row
    raise AssertionError(f"{rid} not printed")


def _line(rows, rid):
    return _row(rows, rid)["line"]


def _features(rows):
    return [row["id"] for row in rows if row["depth"] == 0 and not row["id"].startswith("gates/")]


def _block(out, rid):
    """The whole tree's lines from the top-level item `rid` to the next
    top-level item."""
    lines = out.splitlines()
    start = next((i for i, text in enumerate(lines) if text.startswith(rid + " ")), None)
    assert start is not None, f"{rid} not printed at the first level"
    end = next((i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
               len(lines))
    return lines[start:end]


def _before_intake(fid, status, marks, request="[to do]", solution="[to do]", name=TITLE):
    """A feature before intake, whole: its line, its verdicts, its halves."""
    return ([f"{fid} {name} [{status}] {marks} doc: docs/features/{fid}.md"]
            + [line.format(fid=fid) for line in VERDICT_LINES]
            + [f"  {fid}/request Request half {request}",
               f"  {fid}/solution Solution half {solution}"])


def _through_intake(cid, marks=""):
    """A feature through intake's first line."""
    return f"{cid} {TITLE} [to do]{marks} doc: docs/features/{cid}.md | {INTENT}"


def _query(root, capsys, rid):
    return _call(["tree", rid, "--root", str(root)], capsys)


# --- SC1.3: a pair before intake is one feature --------------------------------

def test_sc1_3_a_pair_before_intake_prints_as_the_usage_block_draws_it(tmp_path, capsys):
    root = _repo(tmp_path)
    _requirements(root, "x")
    _design(root, "x")
    rows, out, err = _print(root, capsys)
    assert err == ""
    block = _block(out, "x")
    assert block[0] == ("x The outcome, in a few words [doing] no contract: document r3 "
                        "design r3 doc: docs/features/x.md")
    assert block[-2:] == ["  x/request Request half [done] by ann at r3",
                          "  x/solution Solution half [done] by raj at r3"]
    # The verdicts stand between the feature's line and its halves.
    assert block[1:-2] == [line.format(fid="x") for line in VERDICT_LINES]
    assert _features(rows) == ["x"]
    assert _query(root, capsys, "x/solution") == (
        0, "x/solution Solution half [done] by raj at r3\n"
           "file: docs/features/x.design.md:6\n", "")


def test_sc1_3_a_pair_a_feature_with_no_design_document_and_a_combined_document_through_intake_each_show_as_one_feature(
        tmp_path, capsys):
    root = _repo(tmp_path)
    # A pair before intake.
    _requirements(root, "pair")
    _design(root, "pair")
    # A requirements document with no design document yet.
    _requirements(root, "alone")
    # One document that holds both signatures, with no design document.
    both = (("ann", "r1: First draft"), ("ann", "r2: Signed: request half"),
            ("ben", "r3: The solution half"), ("ben", "r4: Signed: solution half"))
    _requirements(root, "both", rows=both)
    # A combined document through intake, and a text row after its `Ready:` row.
    _contract(root, "combined")
    _requirements(root, "combined", rows=both + (
        ("intake", "r5: Ready: contract `combined` validates ready-green, derived from r3"),
        ("ben", "r6: A later edit")))
    # A feature through intake with no design document, matching its contract.
    _contract(root, "matched")
    _requirements(root, "matched", rows=REQUIREMENTS + (_requirements_ready("matched"),))
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _block(out, "pair") == _before_intake(
        "pair", "doing", "no contract: document r3 design r3",
        "[done] by ann at r3", "[done] by raj at r3")
    assert _features(rows) == ["alone", "both", "combined", "matched", "pair"]
    # With no design document each prints as it did: one mark, and the
    # solution half from the document's own row, else `[to do]`.
    assert _block(out, "alone") == _before_intake(
        "alone", "doing", "no contract: document r3", "[done] by ann at r3")
    assert _block(out, "both") == _before_intake(
        "both", "doing", "no contract: document r3",
        "[done] by ann at r1", "[done] by ben at r3")
    assert "\n".join(_block(out, "combined")) + "\n" == CONTRACT_LINES.format(
        cid="combined", name=TITLE, marks=" stale: document r6, contract from r3",
        intent=INTENT)
    assert "\n".join(_block(out, "matched")) + "\n" == CONTRACT_LINES.format(
        cid="matched", name=TITLE, marks="", intent=INTENT)
    assert _query(root, capsys, "both/solution") == (
        0, "both/solution Solution half [done] by ben at r3\nfile: docs/features/both.md:6\n", "")
    assert _query(root, capsys, "alone/solution") == (
        0, "alone/solution Solution half [to do]\nfile: docs/features/alone.md:1\n", "")


def test_sc1_3_the_design_document_is_never_a_feature_of_its_own(tmp_path, capsys):
    root = _repo(tmp_path)
    _requirements(root, "x")
    _design(root, "x")
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _features(rows) == ["x"]
    assert [row["id"] for row in rows if row["id"].startswith("x.design")] == []
    # The pair holds its gate once.
    assert _block(out, "gates/G0") == [
        "gates/G0 Planning / Intake [to do]",
        "  - x holds G0 at to do",
        "  gates/G0/G0.1 Definition-of-ready [to do]",
        "    - x holds G0.1 at to do",
        "  gates/G0/G0.2 Vocabulary coverage [to do]",
        "    - x holds G0.2 at to do",
        "  gates/G0/G0.3 Unit confirmation [to do]",
        "    - x holds G0.3 at to do"]
    for rid in ("x.design", "x.design/solution", "x.design/G0"):
        assert _query(root, capsys, rid) == (
            2, "", f"no node '{rid}' - print the tree to list every node id\n")


def test_sc1_3_a_design_document_with_no_requirements_document_prints_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    _design(root, "lone")
    _design(root, "broken", text=b"\xff\xfe not text")
    _requirements(root, "other")
    rows, out, err = _print(root, capsys)
    assert err == ""  # no problem line
    assert _features(rows) == ["other"]
    assert "lone" not in out and "broken" not in out
    assert _row(rows, "gates/G0")["diagnostics"] == ["other holds G0 at to do"]
    assert _block(out, "other") == _before_intake(
        "other", "doing", "no contract: document r3", "[done] by ann at r3")
    assert _query(root, capsys, "lone/solution") == (
        2, "", "no node 'lone/solution' - print the tree to list every node id\n")


def test_sc1_3_a_design_document_beside_a_contract_with_no_requirements_document_prints_nothing(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _contract(root, "cut")
    _design(root, "cut", rows=DESIGN + (("raj", "r5: A later edit"),))
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _features(rows) == ["cut"]
    assert _line(rows, "cut") == f"cut {TITLE} [to do] no feature document | {INTENT}"
    assert "cut.design" not in out and "design" not in _line(rows, "cut")


def test_sc1_3_a_file_named_design_md_is_a_feature_with_the_id_design(tmp_path, capsys):
    root = _repo(tmp_path)
    _requirements(root, "design", rows=(("ann", "r1: First draft"),))
    _design(root, "design", rows=(("raj", "r1: First draft"), ("raj", "r2: An edit")))
    rows, out, err = _print(root, capsys)
    assert err == ""
    # Only the suffix `.design.md` makes a design document.
    assert _features(rows) == ["design"]
    assert _block(out, "design") == _before_intake(
        "design", "to do", "no contract: document r1 design r2")


# --- SC1.3: each document's newest text revision ---------------------------------

REVISIONS = {
    # the design ahead of the requirements document
    "design-ahead": (REQUIREMENTS, DESIGN + (("raj", "r5: Confirmed against requirements r3"),),
                     "no contract: document r3 design r5"),
    # the highest revision of a text row, not the last row
    "highest-not-last": (REQUIREMENTS, (("raj", "r1: First draft"), ("raj", "r6: A later edit"),
                                        ("raj", "r2: An edit")),
                         "no contract: document r3 design r6"),
    # Measured:, Signed:, Parked: and Ready: rows never count, however high
    "status-rows-left-out": (REQUIREMENTS, DESIGN + (
        ("intake", "r5: Parked: Check SC2.3 is assigned to no unit."),
        ("raj", "r6: Measured: later checks"), ("raj", "r7: Signed: solution half"),
        ("intake", "r8: Ready: derived from r3")), "no contract: document r3 design r3"),
    # each table counts alone
    "requirements-ahead": (REQUIREMENTS + (("ann", "r5: A non-goal added"),),
                           (("raj", "r1: First draft"),), "no contract: document r5 design r1"),
}


@pytest.mark.parametrize("case", list(REVISIONS))
def test_sc1_3_the_features_line_names_each_documents_newest_text_revision(
        tmp_path, capsys, case):
    requirements, design, marks = REVISIONS[case]
    root = _repo(tmp_path)
    _requirements(root, "x", rows=requirements)
    _design(root, "x", rows=design)
    rows, _, err = _print(root, capsys)
    assert err == ""
    assert _line(rows, "x") == f"x {TITLE} [doing] {marks} doc: docs/features/x.md"
    assert _features(rows) == ["x"]


def test_sc1_3_before_intake_a_stale_design_shows_no_mark(tmp_path, capsys):
    root = _repo(tmp_path)
    # The design names requirements r3; the requirements stand at r6.
    _requirements(root, "x", rows=REQUIREMENTS + (
        ("ann", "r5: A non-goal added: no export to CSV"), ("ann", "r6: SC2.1 reworded")))
    _design(root, "x")
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _block(out, "x") == _before_intake(
        "x", "doing", "no contract: document r6 design r3",
        "[done] by ann at r3", "[done] by raj at r3")
    assert "stale" not in out


NO_TEXT_ROW = {
    "header-only-table": HEADER + "\n# x - A design title\n",
    "rows-without-revision": HEADER + "| 2026-10-07 | raj | First draft |\n",
    "no-table": "# x - A design title\n\nOnly words, no table.\n",
    "empty": "",
    # every counted row opens Ready:, Measured:, Signed: or Parked:
    "status-rows-only": HEADER + ("| 2026-10-07 | raj | r1: Measured: checks |\n"
                                  "| 2026-10-07 | raj | r2: Signed: solution half |\n"
                                  "| 2026-10-07 | intake | r3: Parked: one thing |\n"
                                  "| 2026-10-07 | intake | r4: Ready: derived from r1 |\n"),
    "not-text": (HEADER + "| 2026-10-07 | raj | r1: Caf\xe9 au lait |\n"
                 "| 2026-10-07 | raj | r2: Signed: solution half |\n").encode("latin-1"),
}


@pytest.mark.parametrize("case", list(NO_TEXT_ROW))
def test_sc1_3_a_design_document_with_no_text_row_shows_design_no_revision_table(
        tmp_path, capsys, case):
    root = _repo(tmp_path)
    _requirements(root, "x")
    _design(root, "x", text=NO_TEXT_ROW[case])
    rows, out, err = _print(root, capsys)
    assert err == ""  # a design document the tree cannot read prints no problem line
    assert _block(out, "x") == _before_intake(
        "x", "doing", "no contract: document r3 design: no revision table",
        "[done] by ann at r3")
    assert _features(rows) == ["x"]
    assert _query(root, capsys, "x/solution") == (
        0, "x/solution Solution half [to do]\nfile: docs/features/x.design.md:1\n", "")


NO_REQUIREMENTS_ROW = {
    "design-with-a-text-row": (DESIGN, "no revision table design r3", "doing",
                               "[done] by raj at r3"),
    "neither-with-a-text-row": ((), "no revision table design: no revision table", "to do",
                                "[to do]"),
}


@pytest.mark.parametrize("case", list(NO_REQUIREMENTS_ROW))
def test_sc1_3_a_requirements_document_with_no_text_row_keeps_its_mark_before_the_designs(
        tmp_path, capsys, case):
    design, marks, status, solution = NO_REQUIREMENTS_ROW[case]
    root = _repo(tmp_path)
    _requirements(root, "x", rows=())
    _design(root, "x", rows=design)
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _block(out, "x") == _before_intake("x", status, marks, solution=solution)
    assert _features(rows) == ["x"]


# --- SC1.3: each document's signature --------------------------------------------

# One document's own `Signed: solution half` row, signed by ben on line 6.
OWN_SOLUTION = (("ann", "r1: First draft"), ("ann", "r2: The request half"),
                ("ann", "r3: Signed: request half"), ("ben", "r4: Signed: solution half"))

SIGNATURES = {
    # the requirements table's own solution signature no longer counts
    "requirements-table-signs-the-solution-half": (
        OWN_SOLUTION, (("raj", "r1: First draft"),),
        "no contract: document r2 design r1", "[done] by ann at r2", "[to do]", 5, 1),
    # ... nor does it beside a signed design: the design's signer and revision show
    "both-tables-sign-the-solution-half": (
        OWN_SOLUTION, DESIGN,
        "no contract: document r2 design r3", "[done] by ann at r2", "[done] by raj at r3", 5, 6),
    # a `Signed: request half` row in the design table signs nothing
    "design-table-signs-the-request-half": (
        (("ann", "r1: First draft"),),
        (("raj", "r1: First draft"), ("raj", "r2: Signed: request half")),
        "no contract: document r1 design r1", "[to do]", "[to do]", 1, 1),
    # of the design's signatures the highest revision counts, and signs the
    # text row above it
    "the-designs-latest-signature": (
        REQUIREMENTS, DESIGN + (("raj", "r5: Confirmed against requirements r5"),
                                ("lee", "r6: Signed: solution half. The engineer seat signs r5")),
        "no contract: document r3 design r5", "[done] by ann at r3", "[done] by lee at r5", 6, 8),
    # a design signature with no text row above it, or no signer, signs nothing
    "no-design-signature-counts": (
        REQUIREMENTS, (("raj", "r9: Signed: solution half"), ("raj", "r1: First draft"),
                       ("", "r2: Signed: solution half")),
        "no contract: document r3 design r1", "[done] by ann at r3", "[to do]", 6, 1),
}


@pytest.mark.parametrize("case", list(SIGNATURES))
def test_sc1_3_once_a_design_document_stands_its_table_alone_gives_the_solution_half(
        tmp_path, capsys, case):
    requirements, design, marks, request, solution, request_line, solution_line = SIGNATURES[case]
    root = _repo(tmp_path)
    _requirements(root, "x", rows=requirements)
    _design(root, "x", rows=design)
    # The same document with no design document beside it reads its own row.
    _requirements(root, "own", rows=OWN_SOLUTION)
    rows, out, err = _print(root, capsys)
    assert err == ""
    status = "to do" if (request, solution) == ("[to do]", "[to do]") else "doing"
    assert _block(out, "x") == _before_intake("x", status, marks, request, solution)
    assert _block(out, "own") == _before_intake(
        "own", "doing", "no contract: document r2", "[done] by ann at r2", "[done] by ben at r2")
    assert _features(rows) == ["own", "x"]
    # The request half's reference stays in the requirements document; the
    # solution half's names the design document.
    assert _query(root, capsys, "x/request") == (
        0, f"x/request Request half {request}\nfile: docs/features/x.md:{request_line}\n", "")
    assert _query(root, capsys, "x/solution") == (
        0, f"x/solution Solution half {solution}\n"
           f"file: docs/features/x.design.md:{solution_line}\n", "")
    assert _query(root, capsys, "own/solution") == (
        0, "own/solution Solution half [done] by ben at r2\nfile: docs/features/own.md:6\n", "")


def test_sc1_3_the_halves_keep_their_ids_plain_names_and_level(tmp_path, capsys):
    root = _repo(tmp_path)
    _requirements(root, "x")
    _design(root, "x")
    rows, out, err = _print(root, capsys)
    assert err == ""
    # Two halves and no third: the design document adds no item.
    assert [(row["id"], row["depth"]) for row in rows if row["id"].startswith("x")
            and row["id"].rsplit("/", 1)[-1] in ("request", "solution")] == [
        ("x/request", 1), ("x/solution", 1)]
    assert _block(out, "x")[-2:] == ["  x/request Request half [done] by ann at r3",
                                     "  x/solution Solution half [done] by raj at r3"]
    # Each is still a half: the progress file refuses its id as before.
    for half in ("x/request", "x/solution"):
        assert _call(["progress", "done", half, "--root", str(root)], capsys) == (
            2, "", f"taskcontract progress: '{half}' is a half, not a task, unit or "
                   "contract - done takes a task, unit or contract id\n")
    assert not (root / ".sdlc" / "progress").exists()


def test_sc1_3_the_query_prints_a_pair_with_both_marks_and_its_requirements_document(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _requirements(root, "x")
    _design(root, "x")
    assert _query(root, capsys, "x") == (
        0, "x The outcome, in a few words [doing] no contract: document r3 design r3\n"
           "doc: docs/features/x.md:1\n", "")
    assert _query(root, capsys, "x/request") == (
        0, "x/request Request half [done] by ann at r3\nfile: docs/features/x.md:6\n", "")


# --- Constraint 4: what the tree reads of a pair ---------------------------------

def test_sc1_3_the_design_documents_title_line_never_names_the_feature(tmp_path, capsys):
    root = _repo(tmp_path)
    # No title line in the requirements document, one in the design document.
    _requirements(root, "bare", title=None)
    _design(root, "bare", title=OTHER_TITLE)
    # A title line in each, with other words.
    _requirements(root, "x")
    _design(root, "x", title=OTHER_TITLE, rows=DESIGN[:3] + (
        ("raj", f"r4: Signed: solution half. {FREE}"),))
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _line(rows, "bare") == ("bare (no title) [doing] no contract: document r3 design r3 "
                                   "doc: docs/features/bare.md")
    assert _line(rows, "x") == (f"x {TITLE} [doing] no contract: document r3 design r3 "
                                "doc: docs/features/x.md")
    assert _line(rows, "x/solution") == "  x/solution Solution half [done] by raj at r3"
    # No word of the design document prints but its signer.
    assert OTHER_TITLE not in out and FREE not in out
    assert "requirements r3" not in out


def test_sc1_3_each_document_of_a_pair_is_read_once_per_print(tmp_path, capsys, monkeypatch):
    root = _repo(tmp_path)
    before = [_requirements(root, "x"), _design(root, "x")]
    _contract(root, "two")
    through = [_requirements(root, "two", rows=REQUIREMENTS + (_requirements_ready("two"),)),
               _design(root, "two", rows=DESIGN + (_design_ready("two"), ("raj", "r6: An edit")))]
    opened = []
    original = builtins.open

    def counting(file, *args, **kwargs):
        if isinstance(file, (str, bytes, os.PathLike)):
            opened.append(Path(os.fsdecode(file)).resolve())
        return original(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", counting)
    monkeypatch.setattr(io, "open", counting)
    rows, _, err = _print(root, capsys)
    assert err == ""
    # Both documents were read: each pair's line carries its design's mark.
    assert _line(rows, "x") == (f"x {TITLE} [doing] no contract: document r3 design r3 "
                                "doc: docs/features/x.md")
    assert _line(rows, "two") == _through_intake("two", " stale: design r6, contract from r3")
    assert [opened.count(path.resolve()) for path in before + through] == [1, 1, 1, 1]


# --- the pane -------------------------------------------------------------------

async def _settle(pilot):
    for _ in range(3):
        await pilot.pause()
        await pilot.wait_for_scheduled_animations()
    await pilot.pause()


def _pane(root, rids, size=(240, 60)):
    """(top-level ids, the cursor line with the cursor on each id in `rids`)."""
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
            tops = [top.label.plain.split(" ", 1)[0] for top in outline.root.children]
            for rid in rids:
                node = node_of(outline, rid)
                up = node.parent
                while up is not None and up.parent is not None:
                    up.expand()
                    up = up.parent
                await _settle(pilot)
                outline.move_cursor(node)
                await _settle(pilot)
                rendered = app.query_one("#cursor").render()
                shown.append(rendered.plain if hasattr(rendered, "plain") else str(rendered))
        return tops, shown

    return asyncio.run(go())


def test_sc1_3_the_cursor_line_on_a_pairs_solution_half_names_the_design_document(tmp_path):
    pytest.importorskip("textual")
    root = _repo(tmp_path)
    _requirements(root, "x")
    _design(root, "x")
    tops, shown = _pane(root, ["x", "x/request", "x/solution"])
    assert shown == [f"docs/features/x.md:1 | {TITLE}",
                     "docs/features/x.md:6 | Request half",
                     "docs/features/x.design.md:6 | Solution half"]
    assert [top for top in tops if not top.startswith("gates/")] == ["x"]


# --- done_means: a pair through intake, each table against its own Ready row ------

# A design table past its own `Ready:` row: r5 is a text row, the contract from r3.
PAST = DESIGN[:3] + (_design_ready("one", n=4), ("raj", "r5: Confirmed against requirements r5"),
                     ("raj", "r6: Signed: solution half. The engineer seat signs r5"))
CURRENT = REQUIREMENTS + (_requirements_ready("one"),)


def test_done_means_a_design_past_its_own_ready_row_reads_stale_after_the_requirements_mark(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _contract(root, "one")
    _requirements(root, "one", rows=CURRENT + (("ann", "r6: SC2.1 reworded"),))
    _design(root, "one", rows=PAST)
    rows, out, err = _print(root, capsys)
    assert err == ""
    marks = " stale: document r6, contract from r3 stale: design r5, contract from r3"
    assert "\n".join(_block(out, "one")) + "\n" == CONTRACT_LINES.format(
        cid="one", name=TITLE, marks=marks, intent=INTENT)
    assert _features(rows) == ["one"]
    # A feature through intake shows no half, pair or not.
    assert [row["id"] for row in rows if row["id"].endswith(("/request", "/solution"))] == []
    assert _query(root, capsys, "one") == (
        0, f"one {TITLE} [to do]{marks}\nsummary: {INTENT}\ndoc: docs/features/one.md:1\n"
           "file: specs/one/contract.yaml:1\n", "")


def test_done_means_a_current_requirements_table_beside_a_stale_design_shows_the_designs_mark_alone(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _contract(root, "one")
    _requirements(root, "one", rows=CURRENT)
    _design(root, "one", rows=PAST)
    rows, _, err = _print(root, capsys)
    assert err == ""
    assert _line(rows, "one") == _through_intake("one", " stale: design r5, contract from r3")
    assert _features(rows) == ["one"]


AT_OR_BEHIND = {
    "at-its-row": DESIGN + (_design_ready("one"),),
    # a contract's revision above the design's matches too
    "behind-its-row": DESIGN + (_design_ready("one", m=9),),
    # Signed:, Measured: and Parked: rows after the row never age the design
    "status-rows-after": DESIGN + (
        _design_ready("one"), ("raj", "r6: Measured: later checks"),
        ("raj", "r7: Signed: solution half"), ("intake", "r8: Parked: one thing")),
    # the newest `Ready:` row that names a revision gives the contract's
    "newest-ready-row": DESIGN + (_design_ready("one"), ("raj", "r6: An edit"),
                                  _design_ready("one", n=7, m=6)),
}


@pytest.mark.parametrize("case", list(AT_OR_BEHIND))
def test_done_means_a_design_at_or_behind_its_own_ready_row_gets_no_mark(tmp_path, capsys, case):
    root = _repo(tmp_path)
    _contract(root, "one")
    _requirements(root, "one", rows=CURRENT)
    _design(root, "one", rows=AT_OR_BEHIND[case])
    # The same table one text row later, in a second pair.
    _contract(root, "two")
    _requirements(root, "two", rows=CURRENT)
    _design(root, "two", rows=AT_OR_BEHIND[case] + (("raj", "r12: A later edit"),))
    rows, _, err = _print(root, capsys)
    assert err == ""
    contract = {"at-its-row": 3, "behind-its-row": 9, "status-rows-after": 3,
                "newest-ready-row": 6}[case]
    assert _line(rows, "two") == _through_intake(
        "two", f" stale: design r12, contract from r{contract}")
    assert _line(rows, "one") == _through_intake("one")
    assert _features(rows) == ["one", "two"]


def test_done_means_each_table_is_read_against_its_own_ready_row(tmp_path, capsys):
    root = _repo(tmp_path)
    # The requirements row names r3 and the design's r2: only the design is past its own.
    _contract(root, "one")
    _requirements(root, "one", rows=CURRENT)
    _design(root, "one", rows=DESIGN + (_design_ready("one", m=2),))
    # The requirements row names r2 and the design's r3: only the requirements document is.
    _contract(root, "two")
    _requirements(root, "two", rows=REQUIREMENTS + (_requirements_ready("two", m=2),))
    _design(root, "two", rows=DESIGN + (_design_ready("two"),))
    rows, _, err = _print(root, capsys)
    assert err == ""
    assert _line(rows, "one") == _through_intake("one", " stale: design r3, contract from r2")
    assert _line(rows, "two") == _through_intake("two", " stale: document r3, contract from r2")
    assert _features(rows) == ["one", "two"]


NO_READY_ROW = {
    "no-ready-row": _text("one", DESIGN),
    "ready-row-without-derived-from": _text("one", DESIGN + (
        ("intake", "r5: Ready: contract `x` validates ready-green, against requirements r3"),)),
    "no-table": "# one - A design title\n",
    "empty": "",
    "not-text": _text("one", DESIGN + (_design_ready("one"),)).encode("utf-8") + b"\xff\xfe\n",
}


@pytest.mark.parametrize("case", list(NO_READY_ROW))
def test_done_means_a_design_table_with_no_ready_row_adds_no_mark(tmp_path, capsys, case):
    root = _repo(tmp_path)
    _contract(root, "one")
    _requirements(root, "one", rows=CURRENT)
    _design(root, "one", text=NO_READY_ROW[case])
    # Neither table holds a row: the requirements document's mark stands alone.
    _contract(root, "two")
    _requirements(root, "two")
    _design(root, "two", text=NO_READY_ROW[case])
    rows, _, err = _print(root, capsys)
    assert err == ""  # a design document the tree cannot read prints no problem line
    assert _line(rows, "one") == _through_intake("one")
    assert _line(rows, "two") == _through_intake("two", ' no "Ready:" row')
    assert _features(rows) == ["one", "two"]
