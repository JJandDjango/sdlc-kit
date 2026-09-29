"""The features-before-intake suite (contract tree-first-level, unit t2-before-intake).

Each regular `*.md` file directly under docs/features/ that has no
specs/<id>/contract.yaml shows as a feature at the first level: a feature
before intake, from a table holding only its r1 row, and also from a table
holding no revision or no table at all. Its id is the file's name without
`.md`; its plain name is the words of the document's first `# ` line after
the first ` - `, ends stripped, and `(no title)` when there is no such line,
no words after the ` - `, or the file cannot be read as text. Its whole-tree
line opens on its id, its plain name and `[to do]`, and ends on `doc:
docs/features/<id>.md`; it carries no summary, and the tree prints none of
the document's other words (SC2.1).

It shows its verdicts as a feature with a contract does: one at each active
gate, then its inactive next gate, each opening into its gate's conditions,
each reading `to do` with no evidence and no diagnostic, since no validator
runs for it. Its G0 verdict counts in gates/G0's roll-up, which names it
`<id> holds G0 at to do`, and each condition `<id> holds G0.<n> at to do`.
A feature with a contract still reads its G0 verdict from the validator
(SC2.2). The first level lists the gate items, then `gates/none`, then the
features: one order by id over both kinds, Python's str order (SC2.3).

Once specs/<id>/contract.yaml exists the feature shows once, as a feature
with a contract: its verdicts, units and drift mark, and no `<id>/request`
or `<id>/solution` item and no `no contract:` mark (SC4.1). Every line
printed today for a feature with a contract stays byte for byte.

`taskcontract tree <id>` on a feature before intake prints its line cut
after the evidence, then `doc: docs/features/<id>.md:1`, and no `file:` or
`summary:` line; each of its verdicts prints its `page:` and no `file:`. The
pane's cursor line on it shows `docs/features/<id>.md:1 | <plain name>`.

Each test drives the CLI in process against a fixture repo under tmp_path
and runs the real validator. The fixture repos sit outside any git
repository, so a verdict's evidence reads `at no commit`.
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import re
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract import checker
from taskcontract.__main__ import main
from taskcontract.tree import build

G0_PAGE = "docs/gates/G0-planning-intake.md"
G1_PAGE = "docs/gates/G1-requirements-spec.md"
INTENT = ("A fixture contract for the before-intake suite; its one unit carries "
          "one sketch line.")
STATEMENT = "A fixture finding for the before-intake suite."
NAME = "Apply one discount code per order"
HIDDEN = "Words of the statement the tree never prints."

ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
DIAGNOSTIC = re.compile(r"^(?P<indent>(?:  )*)- (?P<text>.*)$")

# Each gate's conditions, as the kit's list names them.
CONDITIONS = {
    "G0": [("G0.1", "Definition-of-ready"), ("G0.2", "Vocabulary coverage"),
           ("G0.3", "Unit confirmation")],
    "G1": [("G1.1", "Spec/schema linting"), ("G1.2", "Model checking"),
           ("G1.3", "Criteria completeness + ambiguity review")],
    "G2": [("G2.1", "Design-level model checking"), ("G2.2", "Breaking-change baseline lock"),
           ("G2.3", "ADR review"), ("G2.4", "Threat-model existence"),
           ("G2.5", "Spec-suite red run")],
}
GATE_NAMES = {"G0": "Planning / Intake", "G1": "Requirements / Spec",
              "G2": "Design / Architecture"}


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

def _unit():
    return {"unit": "work for u1-work", "id": "u1-work", "confirmed_by": ["user"],
            "done_means": "the work for u1-work is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}


def _contract(cid, **fields):
    """A contract that reads ready-green, but for the fields given."""
    doc = {"id": cid, "intent": INTENT, "scope": ["src/"], "non_goals": ["No other work"],
           "decomposition": [_unit()], "dependencies": [], "entities": [],
           "provenance": {"origin": "human-request"}}
    doc.update(fields)
    return doc


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _config(root, gates):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates)})


def _finding(root, slug, gate):
    doc = {"finding": slug, "date": "2026-09-28", "kit_pinned": "v0.16.0",
           "diagnostic": "none", "kind": "gap", "count": 1,
           "statement": STATEMENT, "proposal": "none"}
    if gate is not None:
        doc["gate"] = gate
    _dump(root / ".sdlc" / "findings" / f"{slug}.yaml", doc)


# Each fixture contract by its id, and what its G0 verdict reads.
CONTRACTS = {
    # draft-green, one draft entity (TC011 at ready): to do; G0.2 to do
    "drafted": lambda: _contract("drafted", entities=["discount-code"]),
    # draft-green with a blocked dependency (TC003 at ready): blocked
    "parked": lambda: _contract("parked", dependencies=[
        {"ref": "vendor-feed", "status": "blocked", "blocked_by": "the vendor feed"}]),
    # ready-green: done
    "ready": lambda: _contract("ready"),
    # draft-red, a short intent (TC007 at draft): failed
    "short": lambda: _contract("short", intent="Too short."),
}


def _repo(tmp_path, cids=(), gates=("G0",), name="repo"):
    """A repo with the given gates active and the named fixture contracts."""
    root = tmp_path / name
    _config(root, gates)
    write_seat_roster(root)
    _dump(root / "specs" / "vocabulary" / "discount-code.yaml", {
        "term": "discount-code", "name": "Discount code",
        "definition": "A fixture term for the before-intake suite.",
        "kind": "entity", "status": "draft", "since": "2026-01-01"})
    for cid in cids:
        _write_contract(root, cid)
    return root


def _write_contract(root, cid, **fields):
    doc = CONTRACTS[cid]() if cid in CONTRACTS else _contract(cid)
    doc.update(fields)
    _dump(root / "specs" / cid / "contract.yaml", doc)


def _doc_text(fid, title=NAME, rows=("r1: First draft of the request half",)):
    """A feature document: its title line, its revision table, then words
    the tree never prints."""
    head = f"# {fid} - {title}\n\n" if title is not None else ""
    table = ("| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
             + "".join(f"| 2026-09-28 | user | {row} |\n" for row in rows))
    return head + table + f"\n## Statement\n\n{HIDDEN}\n"


def _doc(root, fid, text=None, **kwargs):
    path = root / "docs" / "features" / f"{fid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(_doc_text(fid, **kwargs) if text is None else text, encoding="utf-8")
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


def _tree(root, capsys):
    return _print(root, capsys)[0]


def _row(rows, rid):
    for row in rows:
        if row["id"] == rid:
            return row
    raise AssertionError(f"{rid} not printed")


def _reads(rows, rid):
    row = _row(rows, rid)
    return row["tag"], row["diagnostics"]


def _block(out, rid):
    """The whole tree's lines from the top-level item `rid` to the next
    top-level item, as one text."""
    lines = out.splitlines()
    start = next((i for i, text in enumerate(lines) if text.startswith(rid + " ")), None)
    assert start is not None, f"{rid} not printed at the first level"
    end = next((i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
               len(lines))
    return "\n".join(lines[start:end]) + "\n"


def _first_level(rows):
    return [row["id"] for row in rows if row["depth"] == 0]


def _features(rows):
    return [rid for rid in _first_level(rows) if not rid.startswith("gates/")]


def _assert_before_intake(rows, fid, name=NAME):
    """A feature before intake's line, by its parts: at the first level, its
    id, its plain name and `[to do]` first, its `doc:` reference last."""
    row = _row(rows, fid)
    assert row["depth"] == 0, row["line"]
    assert row["line"].startswith(f"{fid} {name} [to do]"), row["line"]
    assert row["line"].endswith(f" doc: docs/features/{fid}.md"), row["line"]
    assert " | " not in row["line"], row["line"]  # no summary


def _verdict_lines(fid, active, upcoming):
    """A feature before intake's verdicts as the whole tree prints them: one
    at each active gate, then the inactive next gate, each with its
    conditions, all `to do`, no evidence and no diagnostic."""
    lines = []
    for gate, mark in [(g, "") for g in active] + ([(upcoming, " inactive")] if upcoming else []):
        lines.append(f"  {fid}/{gate} {GATE_NAMES[gate]} [to do]{mark}")
        lines += [f"    {fid}/{gate}/{cid} {cname} [to do]" for cid, cname in CONDITIONS[gate]]
    return lines


# --- SC2.1: a document with no contract shows as a feature ---------------------

def test_sc2_1_a_document_with_no_contract_shows_as_a_feature_from_its_r1_row(
        tmp_path, capsys):
    root = _repo(tmp_path, ["ready"])
    _doc(root, "apply-discount")
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _features(rows) == ["apply-discount", "ready"]
    _assert_before_intake(rows, "apply-discount")
    # The tree reads the title line and the table, and prints no other word.
    assert HIDDEN not in out
    assert "Statement" not in out


TITLES = {
    # the words after the first ` - `, however many dashes follow
    "after-the-first-dash": ("# x - Apply one code - per order\n", "Apply one code - per order"),
    # the ends stripped
    "ends-stripped": ("#   x -    Apply one code   \n", "Apply one code"),
    # the first `# ` line, wherever it stands; a `## ` line is not one
    "first-hash-line": ("Some preamble - not a title\n## x - A subheading\n\n"
                        "# x - The real title\n\n# x - A second title\n", "The real title"),
    # the id in the title line is never read: the file name gives the id
    "other-id-in-title": ("# some-other-id - Named by the file\n", "Named by the file"),
}


@pytest.mark.parametrize("case", list(TITLES))
def test_sc2_1_the_plain_name_is_the_title_lines_words_after_the_first_dash(
        tmp_path, capsys, case):
    title, name = TITLES[case]
    root = _repo(tmp_path)
    _doc(root, "x", title + "\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                            "| 2026-09-28 | user | r1: First draft |\n")
    rows, _, err = _print(root, capsys)
    assert err == ""
    _assert_before_intake(rows, "x", name)


NO_TITLES = {
    "no-title-line": "| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                     "| 2026-09-28 | user | r1: First draft |\n",
    "nothing-after-the-dash": "# x - \n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                              "| 2026-09-28 | user | r1: First draft |\n",
    "blanks-after-the-dash": "# x -    \n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                             "| 2026-09-28 | user | r1: First draft |\n",
    "no-dash": "# x\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
               "| 2026-09-28 | user | r1: First draft |\n",
    "not-text": ("# x - Caf\xe9 au lait\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                 "| 2026-09-28 | user | r1: First draft |\n").encode("latin-1"),
}


@pytest.mark.parametrize("case", list(NO_TITLES))
def test_sc2_1_a_document_with_no_usable_title_reads_no_title(tmp_path, capsys, case):
    root = _repo(tmp_path)
    _doc(root, "x", NO_TITLES[case])
    rows, _, err = _print(root, capsys)
    assert err == ""  # an unreadable document prints no problem line
    _assert_before_intake(rows, "x", "(no title)")


NO_REVISIONS = {
    "header-only-table": "# x - A title\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n",
    "rows-without-revision": "# x - A title\n\n| Date | Revised By | Change |\n| :-- | :-- | :-- |\n"
                             "| 2026-09-28 | user | First draft, no revision |\n",
    "no-table": "# x - A title\n\nOnly words, no table.\n",
}


@pytest.mark.parametrize("case", list(NO_REVISIONS))
def test_sc2_1_a_document_with_no_revision_or_no_table_still_shows(tmp_path, capsys, case):
    root = _repo(tmp_path)
    _doc(root, "x", NO_REVISIONS[case])
    rows, _, err = _print(root, capsys)
    assert err == ""
    _assert_before_intake(rows, "x", "A title")


def test_sc2_1_an_empty_document_shows_with_no_title(tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "x", "")
    rows, _, err = _print(root, capsys)
    assert err == ""
    _assert_before_intake(rows, "x", "(no title)")


def test_sc2_1_only_md_files_directly_under_docs_features_count(tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "counted")
    features = root / "docs" / "features"
    (features / "nested").mkdir()
    (features / "nested" / "deeper.md").write_text(_doc_text("deeper"), encoding="utf-8")
    (features / "notes.txt").write_text(_doc_text("notes"), encoding="utf-8")
    (features / "folder.md").mkdir()  # a directory named like a document
    # A specs folder with no contract.yaml leaves its document before intake.
    _doc(root, "pending")
    (root / "specs" / "pending").mkdir()
    (root / "specs" / "pending" / "notes.txt").write_text("not a contract\n", encoding="utf-8")
    rows, _, err = _print(root, capsys)
    assert err == ""
    assert _features(rows) == ["counted", "pending"]
    _assert_before_intake(rows, "counted")
    _assert_before_intake(rows, "pending")
    assert _row(rows, "pending/G0")["line"] == "  pending/G0 Planning / Intake [to do]"


def test_sc2_1_the_query_prints_a_feature_before_intake_with_its_doc_line(tmp_path, capsys):
    root = _repo(tmp_path, ["ready"])
    _doc(root, "x")
    code, out, err = _call(["tree", "x", "--root", str(root)], capsys)
    assert (code, err) == (0, "")
    lines = out.splitlines()
    assert len(lines) == 2, out
    assert lines[0].startswith(f"x {NAME} [to do]"), lines[0]
    assert "doc:" not in lines[0]  # the line is cut after the evidence
    assert lines[1] == "doc: docs/features/x.md:1"
    assert "file:" not in out and "summary:" not in out


def test_sc2_1_the_query_prints_its_verdicts_with_their_page_and_no_file(tmp_path, capsys):
    root = _repo(tmp_path, ["ready"])
    _doc(root, "x")
    assert _call(["tree", "x/G0", "--root", str(root)], capsys) == (
        0, f"x/G0 Planning / Intake [to do]\npage: {G0_PAGE}\n", "")
    assert _call(["tree", "x/G1", "--root", str(root)], capsys) == (
        0, f"x/G1 Requirements / Spec [to do] inactive\npage: {G1_PAGE}\n", "")
    assert _call(["tree", "x/G0/G0.2", "--root", str(root)], capsys) == (
        0, f"x/G0/G0.2 Vocabulary coverage [to do]\npage: {G0_PAGE}\n", "")


# --- the pane: the cursor line on a feature before intake -----------------------

async def _settle(pilot):
    for _ in range(3):
        await pilot.pause()
        await pilot.wait_for_scheduled_animations()
    await pilot.pause()


def _cursor_lines(root, rids, size=(240, 60)):
    """The pane's cursor line with the cursor on each item id in `rids`."""
    assert importlib.util.find_spec("taskcontract.pane") is not None
    pane = importlib.import_module("taskcontract.pane")

    def node_of(tree, rid):
        for top in tree.root.children:
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
            tree = app.query_one("#outline")
            for rid in rids:
                node = node_of(tree, rid)
                up = node.parent
                while up is not None and up.parent is not None:
                    up.expand()
                    up = up.parent
                await _settle(pilot)
                tree.move_cursor(node)
                await _settle(pilot)
                rendered = app.query_one("#cursor").render()
                shown.append(rendered.plain if hasattr(rendered, "plain") else str(rendered))
        return shown

    return asyncio.run(go())


def test_sc2_1_the_cursor_line_on_a_feature_before_intake_shows_its_doc_reference(tmp_path):
    pytest.importorskip("textual")
    root = _repo(tmp_path, ["ready"])
    _doc(root, "x")
    assert _cursor_lines(root, ["x", "x/G0"]) == [
        f"docs/features/x.md:1 | {NAME}", f"{G0_PAGE} | Planning / Intake"]


# --- SC2.2: its G0 verdict reads `to do` and counts at gates/G0 -----------------

GATE_SETS = {
    "g0-active": (("G0",), "G1"),
    "g0-and-g1-active": (("G0", "G1"), "G2"),
    "none-active": ((), "G0"),
}


@pytest.mark.parametrize("case", list(GATE_SETS))
def test_sc2_2_a_feature_before_intake_shows_its_verdicts_by_the_gate_rule(
        tmp_path, capsys, case):
    active, upcoming = GATE_SETS[case]
    root = _repo(tmp_path, ["ready"], gates=active)
    _doc(root, "x")
    rows, out, err = _print(root, capsys)
    assert err == ""
    _assert_before_intake(rows, "x")
    expected = _verdict_lines("x", active, upcoming)
    # Its verdicts come first under it, in this order, each `to do`, with no
    # validator evidence and no diagnostic.
    assert _block(out, "x").splitlines()[1:1 + len(expected)] == expected
    # The contract beside it keeps the same gates.
    for gate in active:
        assert _row(rows, f"ready/{gate}")["depth"] == 1
    assert "inactive" in _row(rows, f"ready/{upcoming}")["line"]


def test_sc2_2_its_g0_verdict_counts_in_gates_g0s_roll_up(tmp_path, capsys):
    root = _repo(tmp_path, ["ready"])
    _doc(root, "x")
    rows = _tree(root, capsys)
    assert _reads(rows, "gates/G0") == ("doing", ["x holds G0 at to do"])
    for condition, _ in CONDITIONS["G0"]:
        assert _reads(rows, f"gates/G0/{condition}") == (
            "doing", [f"x holds {condition} at to do"])
    # Alone, it holds gates/G0 at `to do`.
    alone = _repo(tmp_path, name="alone")
    _doc(alone, "x")
    rows = _tree(alone, capsys)
    assert _reads(rows, "gates/G0") == ("to do", ["x holds G0 at to do"])


def test_sc2_2_the_gate_block_prints_as_the_feature_document_shows_it(tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "g1-requirements-spec", title="Failure points found before development starts")
    _doc(root, "tree-first-level",
         title="The tree's first level shows where each gate and feature stands")
    _, out, err = _print(root, capsys)
    assert err == ""
    assert _block(out, "gates/G0") == (
        "gates/G0 Planning / Intake [to do]\n"
        "  - g1-requirements-spec holds G0 at to do\n"
        "  - tree-first-level holds G0 at to do\n"
        "  gates/G0/G0.1 Definition-of-ready [to do]\n"
        "    - g1-requirements-spec holds G0.1 at to do\n"
        "    - tree-first-level holds G0.1 at to do\n"
        "  gates/G0/G0.2 Vocabulary coverage [to do]\n"
        "    - g1-requirements-spec holds G0.2 at to do\n"
        "    - tree-first-level holds G0.2 at to do\n"
        "  gates/G0/G0.3 Unit confirmation [to do]\n"
        "    - g1-requirements-spec holds G0.3 at to do\n"
        "    - tree-first-level holds G0.3 at to do\n")


def test_sc2_2_holds_lines_name_both_kinds_in_the_trees_feature_order(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "short"])
    _doc(root, "e-doc")  # between drafted and short by its id
    rows = _tree(root, capsys)
    assert _features(rows) == ["drafted", "e-doc", "short"]
    assert _reads(rows, "gates/G0") == ("failed", [
        "drafted holds G0 at to do", "e-doc holds G0 at to do", "short holds G0 at failed"])
    assert _reads(rows, "gates/G0/G0.1") == ("failed", [
        "e-doc holds G0.1 at to do", "short holds G0.1 at failed"])


def test_sc2_2_a_feature_with_a_contract_still_reads_g0_from_the_validator(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "parked", "ready", "short"])
    _doc(root, "m-doc")
    rows, _, _ = _print(root, capsys)
    _assert_before_intake(rows, "m-doc")
    assert {cid: _row(rows, f"{cid}/G0")["tag"]
            for cid in ("drafted", "parked", "ready", "short", "m-doc")} == {
        "drafted": "to do", "parked": "blocked", "ready": "done", "short": "failed",
        "m-doc": "to do"}
    for cid in ("drafted", "parked", "ready", "short"):
        assert _row(rows, f"{cid}/G0")["line"].endswith(
            f" via python -m taskcontract validate specs/{cid}/contract.yaml"
            " --profile ready at no commit")
    assert _row(rows, "m-doc/G0")["line"] == "  m-doc/G0 Planning / Intake [to do]"


def test_sc2_2_the_validator_runs_only_for_a_feature_with_a_contract(
        tmp_path, capsys, monkeypatch):
    root = _repo(tmp_path, ["ready"])
    _doc(root, "x")
    validated = []
    real = checker.validate_path

    def spy(path, *args, **kwargs):
        validated.append(Path(path))
        return real(path, *args, **kwargs)

    monkeypatch.setattr(checker, "validate_path", spy)
    cache = {}
    items, problems = build(root, cache)
    assert problems == []
    assert [item.id for item in items if not item.id.startswith("gates/")] == ["ready", "x"]
    # The pane's verdict cache stays keyed by contract id.
    assert set(cache) == {"ready"}
    assert validated and all(path.name == "contract.yaml" and path.is_file()
                             for path in validated)
    assert all(path.parent.name == "ready" for path in validated)


def test_progress_refuses_a_feature_before_intake(tmp_path, capsys):
    """A feature before intake is level `feature`, never `contract`: no
    progress record is written for it, so no done record waits for intake."""
    root = _repo(tmp_path, ["ready"])
    _doc(root, "x")
    code, out, err = _call(["progress", "done", "x", "--root", str(root)], capsys)
    assert err.splitlines() == [
        "taskcontract progress: 'x' is a feature, not a task, unit or contract - "
        "done takes a task, unit or contract id"]
    assert (code, out) == (2, "")
    code, out, err = _call(["progress", "start", "x", "--root", str(root)], capsys)
    assert err.splitlines() == [
        "taskcontract progress: 'x' is a feature, not a task - start takes a task id"]
    assert (code, out) == (2, "")
    assert not (root / ".sdlc" / "progress" / "x.yaml").exists()


# --- SC2.3: the first level's order ---------------------------------------------

def test_sc2_3_the_first_level_lists_gates_then_none_then_features_by_id(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "ready", "short"])
    _finding(root, "f-later", "G3")
    _finding(root, "f-loose", None)
    for fid in ("alpha", "m-doc", "zulu", "Upper"):
        _doc(root, fid)
    _doc(root, "ready", title="Ready's own document")  # a contract's document, not a new feature
    rows, _, err = _print(root, capsys)
    assert err == ""
    # One order by id over both kinds, Python's str order: capitals first.
    assert _first_level(rows) == [
        "gates/G0", "gates/G3", "gates/none",
        "Upper", "alpha", "drafted", "m-doc", "ready", "short", "zulu"]
    for fid in ("alpha", "m-doc", "zulu", "Upper"):
        _assert_before_intake(rows, fid)


# --- SC4.1: once the contract exists, the feature is one item -------------------

FEATURE_LINES = """\
{cid} {name} [{status}]{marks} doc: docs/features/{cid}.md | {intent}
  {cid}/G0 Planning / Intake [{verdict}] via python -m taskcontract validate specs/{cid}/contract.yaml --profile ready at no commit
    {cid}/G0/G0.1 Definition-of-ready [done]
    {cid}/G0/G0.2 Vocabulary coverage [{g02}]
{g02_lines}    {cid}/G0/G0.3 Unit confirmation [done]
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
MSG_DRAFT_TERM = ("entity 'discount-code' is not ratified (status: draft) - draft does "
                  "not resolve; ratify the term or fork the vocabulary task")
CONTRACT_TITLE = "The contract's own title for this feature"


def _no_before_intake_parts(out, rows, cid):
    ids = [row["id"] for row in rows]
    assert f"{cid}/request" not in ids and f"{cid}/solution" not in ids
    assert "no contract:" not in _block(out, cid)


def test_sc4_1_once_the_contract_exists_the_feature_shows_once_with_its_contract(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _doc(root, "drafted", rows=("r1: First draft", "r2: Ready: derived from r1",
                                "r3: A later edit"))
    _doc(root, "zulu")  # stays before intake throughout
    rows = _tree(root, capsys)
    _assert_before_intake(rows, "drafted")
    # Intake writes the contract: the feature stays one item.
    _write_contract(root, "drafted", title=CONTRACT_TITLE)
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _features(rows) == ["drafted", "zulu"]
    assert _block(out, "drafted") == FEATURE_LINES.format(
        cid="drafted", name=CONTRACT_TITLE, status="to do",
        marks=" stale: document r3, contract from r1", intent=INTENT, verdict="to do",
        g02="to do", g02_lines=f"      - {MSG_DRAFT_TERM}\n")
    _no_before_intake_parts(out, rows, "drafted")
    _assert_before_intake(rows, "zulu")


DRIFTS = {
    "matches": (("r1: First draft", "r2: Ready: derived from r1"), ""),
    "no-ready-row": (("r1: First draft",), ' no "Ready:" row'),
}


@pytest.mark.parametrize("case", list(DRIFTS))
def test_sc4_1_a_feature_with_a_contract_keeps_its_drift_mark_and_no_revision_or_half(
        tmp_path, capsys, case):
    doc_rows, marks = DRIFTS[case]
    root = _repo(tmp_path)
    _write_contract(root, "ready", title=CONTRACT_TITLE)
    _doc(root, "ready", rows=doc_rows)
    _doc(root, "x")
    rows, out, err = _print(root, capsys)
    assert err == ""
    assert _features(rows) == ["ready", "x"]
    assert _block(out, "ready") == FEATURE_LINES.format(
        cid="ready", name=CONTRACT_TITLE, status="to do", marks=marks, intent=INTENT,
        verdict="done", g02="done", g02_lines="")
    _no_before_intake_parts(out, rows, "ready")
    _assert_before_intake(rows, "x")


def test_sc4_1_an_unreadable_contract_still_makes_its_feature_one_item(tmp_path, capsys):
    root = _repo(tmp_path)
    broken = root / "specs" / "broken" / "contract.yaml"
    broken.parent.mkdir(parents=True)
    broken.write_text("- a list\n", encoding="utf-8")
    _doc(root, "broken")
    _doc(root, "x")
    rows, out, err = _print(root, capsys)
    assert err == "taskcontract tree: unreadable contract: specs/broken/contract.yaml (not a mapping)\n"
    assert _features(rows) == ["broken", "x"]
    assert _row(rows, "broken")["line"] == (
        'broken (no title) [failed] no "Ready:" row doc: docs/features/broken.md')
    assert _row(rows, "broken/G0")["line"].endswith(
        " via python -m taskcontract validate specs/broken/contract.yaml --profile ready at no commit")
    _no_before_intake_parts(out, rows, "broken")
    _assert_before_intake(rows, "x")


# --- Constraint 2: every line for a feature with a contract stays byte for byte --

def test_constraint_2_a_feature_before_intake_changes_no_other_line(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "ready"])
    _finding(root, "f-gate", "G0")
    _finding(root, "f-loose", None)
    before, _, _ = _print(root, capsys)
    _doc(root, "m-doc")
    rows, out, err = _print(root, capsys)
    assert err == ""
    _assert_before_intake(rows, "m-doc")
    assert _block(out, "drafted") == FEATURE_LINES.format(
        cid="drafted", name="(no title)", status="to do", marks=" no feature document",
        intent=INTENT, verdict="to do", g02="to do",
        g02_lines=f"      - {MSG_DRAFT_TERM}\n").replace(" doc: docs/features/drafted.md", "")
    assert _block(out, "ready") == FEATURE_LINES.format(
        cid="ready", name="(no title)", status="to do", marks=" no feature document",
        intent=INTENT, verdict="done", g02="done", g02_lines="").replace(
            " doc: docs/features/ready.md", "")
    # Every item line stays but the new feature's, gates/G0's and its
    # conditions', which now count it.
    rolled = {"gates/G0", "gates/G0/G0.1", "gates/G0/G0.2", "gates/G0/G0.3"}

    def kept(printed):
        return [row["line"] for row in printed
                if row["id"].split("/", 1)[0] != "m-doc" and row["id"] not in rolled]

    assert kept(rows) == kept(before)
    assert _block(out, "gates/none") == f"gates/none [to do]\n  gates/none/f-loose {STATEMENT} [kind: gap]\n"
