"""G1's document stands as a pair (contract: document-split, unit
d6-release, SC4.3).

`docs/features/g1-requirements-spec.md` holds no solution half, so it
stands unchanged as a requirements document, its request half's text and
signature as they were. A design run opens its design document beside it,
at r1 against requirements r3, with no signature yet. The kit's own tree
then prints G1 as one feature: a second mark, `design r1`, and a solution
half read from the design document's table. USAGE draws that feature as
the tree prints it.

The design document's own words are a seat's: no test here reads its
seat's name, its date or a section of it.

The tests read the kit's own tree and run no model.
"""

from __future__ import annotations

import asyncio
import hashlib
import importlib
import importlib.util
import re
from pathlib import Path

import pytest

from taskcontract.__main__ import main

_HERE = Path(__file__).resolve().parent.parent
# Beside a tree that holds the skill, read that tree; a copy run from any
# other folder reads the tree pytest was started in.
ROOT = _HERE if (_HERE / "skills" / "sdlc").is_dir() else Path.cwd()
USAGE = ROOT / "USAGE.md"

G1 = "g1-requirements-spec"
NAME = "Failure points found before development starts"
REQUIREMENTS = f"docs/features/{G1}.md"
DESIGN = f"docs/features/{G1}.design.md"
# sha256 of the requirements document's text, read as UTF-8 text: the build
# changes no byte of it.
REQUIREMENTS_TEXT = "eb81d41780bae6fde7a37dfcc45f922540f450370d520623c10d00434f0399f3"
STATUS_ROWS = ("Ready:", "Measured:", "Signed:", "Parked:")

FEATURE_LINE = (f"{G1} {NAME} [doing] no contract: document r3 design r1 "
                f"doc: {REQUIREMENTS}")
REQUEST_HALF = f"  {G1}/request Request half [done] by user at r3"
SOLUTION_HALF = f"  {G1}/solution Solution half [to do]"
DRAWING_LEAD = ("G1's feature before intake, with its request half signed and its design "
                "document at r1 (\"A pair of documents\"):")

ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
DIAGNOSTIC = re.compile(r"^(?P<indent>(?:  )*)- (?P<text>.*)$")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """The text with each whitespace run folded to one space."""
    return " ".join(text.split())


def _table(text: str) -> list[list[str]]:
    """The rows of a document's first table, each as its cells, the header
    and the rule below it left out."""
    rows = []
    for line in text.splitlines():
        if line.startswith("|"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif rows:
            break
    return rows[2:]


def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _print(capsys):
    """(rows, stdout) of the kit's whole tree, which exits 0."""
    code, out, _ = _call(["tree", "--root", str(ROOT)], capsys)
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
    return rows, out


def _row(rows, rid):
    found = [row for row in rows if row["id"] == rid]
    assert len(found) == 1, f"{rid} is printed {len(found)} times"
    return found[0]


def _block(out, rid):
    """The whole tree's lines from the top-level item `rid` to the next
    top-level item."""
    lines = out.splitlines()
    start = next((i for i, text in enumerate(lines) if text.startswith(rid + " ")), None)
    assert start is not None, f"{rid} not printed at the first level"
    end = next((i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
               len(lines))
    return lines[start:end]


def _drawing(section: str, lead: str) -> list[str]:
    """The lines of the first fenced block after the paragraph that ends on
    `lead`, the paragraph matched with its whitespace folded."""
    blocks = re.split(r"\n[ \t]*\n", section)
    at = next((i for i, block in enumerate(blocks) if _flat(block).endswith(lead)), None)
    assert at is not None, f"no paragraph ends: {lead}"
    fenced = blocks[at + 1].strip().splitlines()
    assert fenced[0] == "```" and fenced[-1] == "```", "no drawing follows the paragraph"
    return fenced[1:-1]


# --- SC4.3: the two documents ----------------------------------------------------

def test_sc4_3_g1s_design_document_stands_at_r1_against_requirements_r3_beside_an_unchanged_request_half():
    assert (ROOT / DESIGN).is_file(), f"no design document at {DESIGN}"
    rows = _table(_read(ROOT / DESIGN))
    assert rows, "the design document opens on no revision table"
    first = rows[0][-1]
    # r1 is a text row, and it names the requirements revision the design stands against.
    assert first.startswith("r1: ")
    assert not first[len("r1: "):].startswith(STATUS_ROWS)
    assert re.search(r"\brequirements r3\b", first), first
    # The requirements document keeps its text, its signature row among it.
    text = _read(ROOT / REQUIREMENTS)
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == REQUIREMENTS_TEXT
    assert "## Proposed solution" not in text


# --- SC4.3: the kit's own tree ---------------------------------------------------

def test_sc4_3_the_kits_tree_prints_g1_as_one_feature_with_the_mark_design_r1(capsys):
    rows, out = _print(capsys)
    feature = _row(rows, G1)
    assert feature["depth"] == 0
    assert feature["line"] == FEATURE_LINE
    # One feature: the design document is no item of its own.
    assert not [row["id"] for row in rows if row["id"].startswith(f"{G1}.design")]
    # The first level holds each contract and each requirements document, by id.
    features = {path.parent.name for path in ROOT.glob("specs/*/contract.yaml")}
    features |= {path.name[:-len(".md")] for path in ROOT.glob("docs/features/*.md")
                 if not path.name.endswith(".design.md")}
    assert [row["id"] for row in rows
            if row["depth"] == 0 and not row["id"].startswith("gates/")] == sorted(features)
    # The request half keeps its signature; the solution half is read from
    # the design document, which holds no signature yet.
    assert _row(rows, f"{G1}/request")["line"] == REQUEST_HALF
    assert _row(rows, f"{G1}/solution")["line"] == SOLUTION_HALF
    assert _block(out, G1)[-2:] == [REQUEST_HALF, SOLUTION_HALF]
    code, printed, _ = _call(["tree", f"{G1}/solution", "--root", str(ROOT)], capsys)
    assert (code, printed) == (0, f"{SOLUTION_HALF.strip()}\nfile: {DESIGN}:1\n")
    code, printed, _ = _call(["tree", f"{G1}/request", "--root", str(ROOT)], capsys)
    assert (code, printed) == (0, f"{REQUEST_HALF.strip()}\nfile: {REQUIREMENTS}:6\n")
    # G0 still waits on G1, and a `Signed:` row ages no contract.
    assert _row(rows, "gates/G0")["tag"] == "doing"
    assert f"{G1} holds G0 at to do" in _row(rows, "gates/G0")["diagnostics"]
    assert "stale:" not in _row(rows, "tree-first-level")["line"]


# --- SC4.3: the pane -------------------------------------------------------------

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


def test_sc4_3_the_pane_on_the_kit_shows_g1s_solution_half_from_its_design_document():
    pytest.importorskip("textual")
    shown = _pane(ROOT, ["gates/G0", f"{G1}/request", f"{G1}/solution"])
    assert shown[0][0].startswith("gates/G0 Planning / Intake [doing]"), shown[0]
    assert shown[1] == ("request Request half [done] by user at r3",
                        f"{REQUIREMENTS}:6 | Request half")
    assert shown[2] == ("solution Solution half [to do]", f"{DESIGN}:1 | Solution half")


# --- SC4.3: USAGE's drawing ------------------------------------------------------

def test_sc4_3_usages_drawing_of_g1_reads_what_the_kits_tree_prints(capsys):
    _, out = _print(capsys)
    text = _read(USAGE)
    start = re.search(r"^### Revisions and halves", text, re.MULTILINE)
    assert start, "USAGE has no subsection Revisions and halves"
    end = re.compile(r"^### ", re.MULTILINE).search(text, start.end())
    halves = text[start.start():end.start() if end else len(text)]
    drawn = _drawing(halves, DRAWING_LEAD)
    assert drawn == _block(out, G1)
    assert drawn[0] == FEATURE_LINE
