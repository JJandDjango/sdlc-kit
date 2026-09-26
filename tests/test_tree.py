"""The tree suite for ADR 0031 (contract tree-view).

`taskcontract tree` prints the work as one tree, computed from the repo's
files at every run: the gates with their findings, then each contract with
a verdict per active gate, its units, each unit's seven tasks and its
checks. Unit t1-tree-shape fixes that shape (SC1.1), the one place each
finding prints (SC1.2), and a print that is derived, never stored (SC1.3).
Statuses are asserted only as members of the six values: t3 derives them.

Unit t2-summaries-and-links ends each line with what its sources say: a
unit's `depends_on` links, a finding's `gate` link, a contract's feature
document as a file reference only, then, after ` | `, the item's summary,
its source field's own text (SC4.1, SC4.2, SC5.1, SC5.2).

Since project-tree's o2-titles, the source text of every item but a
contract is its plain name, right after its id, before its status; the
summary after ` | ` holds only a contract's intent. The tests below read
the plain name as the row's `name`. Since project-tree's o3-stale the tree
opens a feature document for its revision table alone, and a contract's
marks hold its drift mark (`no feature document`, `no "Ready:" row`).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

from taskcontract.__main__ import main

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "taskcontract" / "data"

STATUSES = {"to do", "doing", "done", "failed", "blocked", "waiting on a seat"}
TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]
TASK_NAMES = ["Approve the test list", "Write the tests", "Prove red", "Green",
              "Approve the commit", "Commit", "Two-Key PASS"]

INTENT = ("A fixture contract for the tree suite; its units carry the sketch "
          "shapes that check ids come from.")

# One item per line: its full id, then its plain name when it has one
# (project-tree o2), then its status (a finding: its kind) in brackets, then
# anything later units add.
ROW = re.compile(r"^(?P<indent> *)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                 r"(?P<rest>.*)$")


class _Row(tuple):
    """(depth, id, tag, rest), carrying the plain name as `name` (None
    when the line shows none)."""

    name = None


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


def _contract(cid, units):
    return {
        "id": cid,
        "intent": INTENT,
        "scope": ["src/"],
        "non_goals": ["No other work"],
        "decomposition": units,
        "dependencies": [],
        "entities": [],
        "provenance": {"origin": "human-request"},
    }


def _finding(slug, gate, kind):
    doc = {
        "finding": slug,
        "date": "2026-09-22",
        "kit_pinned": "v0.14.0",
        "diagnostic": "none",
        "kind": kind,
        "count": 1,
        "statement": "A fixture finding for the tree suite.",
        "proposal": "none",
    }
    if gate is not None:
        doc["gate"] = gate
    return doc


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _config(root, gates):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates)})


def _repo(tmp_path):
    """Two contracts, G0 active, four findings beside the form, a folder with no contract."""
    root = tmp_path / "repo"
    _config(root, ["G0"])
    _dump(root / "specs" / "alpha" / "contract.yaml", _contract("alpha", ALPHA))
    _dump(root / "specs" / "beta" / "contract.yaml", _contract("beta", BETA))
    _dump(root / "specs" / "vocabulary" / "intake-seat.yaml", {
        "term": "intake-seat", "kind": "value-set", "values": ["user"],
        "status": "ratified"})
    findings = root / ".sdlc" / "findings"
    _dump(findings / "TEMPLATE.yaml", _finding("TODO", "TODO", "TODO"))
    _dump(findings / "stale-pin.yaml", _finding("stale-pin", "G0", "gap"))
    _dump(findings / "slow-loop.yaml", _finding("slow-loop", "G3.1", "friction"))
    _dump(findings / "idea.yaml", _finding("idea", "none", "proposal"))
    _dump(findings / "loose-end.yaml", _finding("loose-end", None, "escape"))
    return root


def _run(root, capsys):
    code = main(["tree", "--root", str(root)])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _rows(out):
    """[(depth, id, tag, rest)] for every item line, in print order, each
    with its plain name as `name`."""
    rows = []
    for line in out.splitlines():
        match = ROW.match(line)
        if match:
            row = _Row((len(match["indent"]) // 2, match["id"], match["tag"],
                        match["rest"]))
            row.name = match["name"]
            rows.append(row)
    return rows


def _tree(root, capsys):
    code, out, _ = _run(root, capsys)
    assert code == 0
    return _rows(out)


def _ids(rows):
    return [row[1] for row in rows]


def _row(rows, rid):
    for row in rows:
        if row[1] == rid:
            return row
    raise AssertionError(f"{rid} not printed")


def _children(rows, parent):
    """Ids one level under `parent`, in print order."""
    for i, (depth, rid, _, _) in enumerate(rows):
        if rid == parent:
            found = []
            for child_depth, cid, _, _ in rows[i + 1:]:
                if child_depth <= depth:
                    break
                if child_depth == depth + 1:
                    found.append(cid)
            return found
    raise AssertionError(f"{parent} not printed")


def _checks(rows, unit):
    """The last id segment of a unit's checks: its children after the seven tasks."""
    return [cid.rsplit("/", 1)[1] for cid in _children(rows, unit)][len(TASK_KEYS):]


# --- SC1.1 the whole tree (unit t1-tree-shape) -----------------------------

def test_gates_print_first_then_each_contract_in_folder_order(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    top = [rid for depth, rid, _, _ in rows if depth == 0]
    assert top == ["gates/G0", "gates/G3", "gates/none", "alpha", "beta"]
    assert not any(rid.startswith("vocabulary") for rid in _ids(rows))


def test_a_contract_prints_a_verdict_per_active_gate_before_its_units(tmp_path, capsys):
    root = _repo(tmp_path)
    # after the active gates, the next gate in the kit's order, inactive (project-tree o1)
    assert _children(_tree(root, capsys), "alpha") == [
        "alpha/G0", "alpha/G1", "alpha/a1-core", "alpha/a2-edges"]
    _config(root, ["G0", "G4"])
    assert _children(_tree(root, capsys), "alpha") == [
        "alpha/G0", "alpha/G4", "alpha/G5", "alpha/a1-core", "alpha/a2-edges"]


def test_a_unit_prints_its_seven_tasks_then_its_checks(tmp_path, capsys):
    listed = yaml.safe_load((DATA / "tasks.yaml").read_text(encoding="utf-8"))["tasks"]
    rows = _tree(_repo(tmp_path), capsys)
    assert _children(rows, "alpha/a1-core") == (
        [f"alpha/a1-core/{task['id']}" for task in listed]
        + ["alpha/a1-core/SC1.1", "alpha/a1-core/SC5.1+SC5.2"])


def test_check_ids_come_from_the_trailing_parentheses(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _checks(rows, "alpha/a1-core") == ["SC1.1", "SC5.1+SC5.2"]
    # no parentheses, then a repeated id: each falls back to its position
    assert _checks(rows, "alpha/a2-edges") == ["sketch-1", "SC2.1", "sketch-3"]
    # parentheses that hold words, not ids
    assert _checks(rows, "beta/b1-solo") == ["sketch-1"]


def test_every_item_but_a_finding_shows_one_of_six_statuses(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    # 13 gate items (each gate with its conditions), 30 under alpha, 18 under
    # beta: each contract's G0 and its next gate, G1, open into their conditions
    assert len(rows) == 61
    slugs = {"stale-pin", "slow-loop", "idea", "loose-end"}
    findings = [row for row in rows
                if row[1].startswith("gates/") and row[1].rsplit("/", 1)[1] in slugs]
    others = [row for row in rows if row not in findings]
    assert len(findings) == 4
    assert all(tag in STATUSES for _, _, tag, _ in others)


def test_a_finding_shows_its_kind_in_place_of_a_status(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _row(rows, "gates/G0/stale-pin")[2] == "kind: gap"
    assert _row(rows, "gates/G3/G3.1/slow-loop")[2] == "kind: friction"
    assert _row(rows, "gates/none/idea")[2] == "kind: proposal"
    assert _row(rows, "gates/none/loose-end")[2] == "kind: escape"


# --- SC1.2 every finding once -----------------------------------------------

def test_each_finding_prints_once_under_the_gate_it_names(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    # a gate opens into its conditions; a finding naming a condition stands under it
    assert _children(rows, "gates/G0") == [
        "gates/G0/G0.1", "gates/G0/G0.2", "gates/G0/G0.3", "gates/G0/stale-pin"]
    assert _children(rows, "gates/G3") == ["gates/G3/G3.1", "gates/G3/G3.2", "gates/G3/G3.3"]
    assert _children(rows, "gates/G3/G3.1") == ["gates/G3/G3.1/slow-loop"]
    for slug in ("stale-pin", "slow-loop", "idea", "loose-end"):
        assert sum(rid.endswith("/" + slug) for rid in _ids(rows)) == 1, slug


def test_a_named_gate_outside_active_gates_prints_inactive(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _row(rows, "gates/G3")[3].split()[:1] == ["inactive"]
    assert "inactive" not in _row(rows, "gates/G0")[3].split()
    gate_items = [rid for rid in _ids(rows)
                  if rid.startswith("gates/") and rid.count("/") == 1]
    assert gate_items == ["gates/G0", "gates/G3", "gates/none"]  # no gate neither active nor named


def test_gate_none_and_a_missing_gate_print_under_the_none_item(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _children(rows, "gates/none") == ["gates/none/idea", "gates/none/loose-end"]


def test_the_finding_form_prints_nothing(tmp_path, capsys):
    code, out, _ = _run(_repo(tmp_path), capsys)
    assert code == 0
    assert "TEMPLATE" not in out


# --- SC1.3 derived, never stored --------------------------------------------

def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


def test_the_tree_writes_no_file(tmp_path, capsys):
    root = _repo(tmp_path)
    before = _snapshot(root)
    _tree(root, capsys)
    assert _snapshot(root) == before


def test_a_new_unit_shows_at_the_next_run(tmp_path, capsys):
    root = _repo(tmp_path)
    assert "alpha/a3-new" not in _ids(_tree(root, capsys))
    _dump(root / "specs" / "alpha" / "contract.yaml",
          _contract("alpha", ALPHA + [_unit("a3-new", ["verify the new unit prints"])]))
    rows = _tree(root, capsys)
    assert _children(rows, "alpha")[-1] == "alpha/a3-new"
    assert len(_children(rows, "alpha/a3-new")) == len(TASK_KEYS) + 1


def test_a_removed_finding_is_gone_at_the_next_run(tmp_path, capsys):
    root = _repo(tmp_path)
    assert "gates/G0/stale-pin" in _ids(_tree(root, capsys))
    (root / ".sdlc" / "findings" / "stale-pin.yaml").unlink()
    rows = _tree(root, capsys)
    assert "gates/G0/stale-pin" not in _ids(rows)
    assert _children(rows, "gates/G0") == [  # an active gate prints with no findings
        "gates/G0/G0.1", "gates/G0/G0.2", "gates/G0/G0.3"]


def test_a_gate_added_to_active_gates_shows_at_the_next_run(tmp_path, capsys):
    root = _repo(tmp_path)
    assert "alpha/G3" not in _ids(_tree(root, capsys))
    _config(root, ["G0", "G3"])
    rows = _tree(root, capsys)
    assert "inactive" not in _row(rows, "gates/G3")[3].split()
    assert {"alpha/G3", "beta/G3"} <= set(_ids(rows))


# --- the name lists and the command -----------------------------------------

def _registry():
    """{id: name} from the Overview table of docs/gates.md, in table order."""
    table = re.compile(r"^\| (G\d+|PL-[A-Z]+) \| ([^|]+?) \|")
    text = (ROOT / "docs" / "gates.md").read_text(encoding="utf-8")
    return dict(m.groups() for m in map(table.match, text.splitlines()) if m)


def test_the_gate_list_holds_the_thirteen_registry_gates():
    gates = yaml.safe_load((DATA / "gates.yaml").read_text(encoding="utf-8"))["gates"]
    registry = _registry()
    assert len(registry) == 13
    assert [(gate["id"], gate["name"]) for gate in gates] == list(registry.items())
    for gate in gates:
        assert gate["page"].startswith(f"docs/gates/{gate['id']}-"), gate["page"]
        assert (ROOT / gate["page"]).is_file(), gate["page"]


def test_the_task_list_is_the_seven_tasks_in_order():
    tasks = yaml.safe_load((DATA / "tasks.yaml").read_text(encoding="utf-8"))["tasks"]
    assert [task["id"] for task in tasks] == TASK_KEYS
    assert [task["name"] for task in tasks] == TASK_NAMES
    for task in tasks:
        assert (ROOT / task["page"].split("#")[0]).is_file(), task["page"]


def test_the_kit_tree_prints_every_contract(capsys):
    code, out, _ = _run(ROOT, capsys)
    assert code == 0
    top = [rid for depth, rid, _, _ in _rows(out) if depth == 0]
    contracts = sorted(p.parent.name for p in (ROOT / "specs").glob("*/contract.yaml"))
    assert contracts
    assert [rid for rid in top if not rid.startswith("gates/")] == contracts
    assert "gates/G0" in top


def test_an_unreadable_source_never_stops_the_print(tmp_path, capsys):
    root = _repo(tmp_path)
    broken = root / "specs" / "broken" / "contract.yaml"
    broken.parent.mkdir(parents=True)
    broken.write_text("id: [unclosed\n", encoding="utf-8")
    (root / ".sdlc" / "findings" / "garbled.yaml").write_text(
        "gate: [unclosed\n", encoding="utf-8")
    code, out, err = _run(root, capsys)
    assert code == 0
    assert "specs/broken/contract.yaml" in err
    assert ".sdlc/findings/garbled.yaml" in err
    assert len(err.strip().splitlines()) == 2  # one line each
    ids = _ids(_rows(out))
    assert "alpha/a2-edges/sketch-3" in ids
    assert "gates/none/loose-end" in ids


# --- t2-summaries-and-links ---------------------------------------------------
# After its tag, its marks and its evidence, a line carries its links, then its
# file reference, then " | " and its summary: the source field's own text, last
# because it is free text. A line with no summary prints no bar. The tests split
# the summary off at the first " | " after the tag.

BAR = " | "
BETA_INTENT = ("A second fixture contract, so that each contract's line shows "
               "its own intent.")


def _gate_names():
    """{id: name} from the kit's gate list, the source of a gate's summary."""
    gates = yaml.safe_load((DATA / "gates.yaml").read_text(encoding="utf-8"))["gates"]
    return {gate["id"]: gate["name"] for gate in gates}


def _task_names():
    """The seven names from the kit's task list, in order."""
    tasks = yaml.safe_load((DATA / "tasks.yaml").read_text(encoding="utf-8"))["tasks"]
    return [task["name"] for task in tasks]


def _printed(root, capsys):
    """(rows, stdout) of one print, which exits 0."""
    code, out, _ = _run(root, capsys)
    assert code == 0
    return _rows(out), out


def _parts(rows, rid):
    """(head, summary) of an item's line: the text after its tag, split at the
    first " | ". The head holds the marks, the evidence, the links and the file
    reference; the summary is None when no bar prints."""
    head, bar, summary = _row(rows, rid)[3].partition(BAR)
    return head, (summary if bar else None)


def _head(rows, rid):
    return _parts(rows, rid)[0]


def _summary(rows, rid):
    return _parts(rows, rid)[1]


def _name(rows, rid):
    """An item's plain name, between its id and its tag; None when it shows none."""
    return _row(rows, rid).name


def _one_line_each(out):
    """Whether every line printed is one item's line."""
    return len(out.splitlines()) == len(_rows(out))


def _contract_path(root, cid):
    return root / "specs" / cid / "contract.yaml"


def _finding_path(root, slug):
    return root / ".sdlc" / "findings" / f"{slug}.yaml"


def _edit(path, **fields):
    """Rewrite the YAML mapping at `path` with `fields` set; None drops a field."""
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    for key, value in fields.items():
        if value is None:
            doc.pop(key, None)
        else:
            doc[key] = value
    _dump(path, doc)


# --- SC4.1 each item's summary is its source's text (unit t2) -----------------

def test_a_contract_shows_its_intent(tmp_path, capsys):
    root = _repo(tmp_path)
    _edit(_contract_path(root, "beta"), intent=BETA_INTENT)
    rows = _tree(root, capsys)
    assert _summary(rows, "alpha") == INTENT
    assert _summary(rows, "beta") == BETA_INTENT


def test_a_unit_shows_its_done_means(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    for rid in ("alpha/a1-core", "alpha/a2-edges", "beta/b1-solo"):
        assert _name(rows, rid) == f"the work for {rid.split('/')[1]} is done", rid
        assert _summary(rows, rid) is None, rid  # its plain name now, never after a bar


def test_a_check_shows_its_sketch_line(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    for cid, units in (("alpha", ALPHA), ("beta", BETA)):
        for unit in units:
            base = f"{cid}/{unit['id']}"
            # a check whose id falls back to its position still shows its own line
            shown = [_name(rows, f"{base}/{check}") for check in _checks(rows, base)]
            assert shown == unit["acceptance_sketch"], base


def test_a_finding_shows_its_statement(tmp_path, capsys):
    root = _repo(tmp_path)
    findings = ["gates/G0/stale-pin", "gates/G3/G3.1/slow-loop", "gates/none/idea",
                "gates/none/loose-end"]
    for rid in findings:
        slug = rid.rsplit("/", 1)[1]
        _edit(_finding_path(root, slug), statement=f"The {slug} finding, in its own words.")
    rows = _tree(root, capsys)
    for rid in findings:
        assert _name(rows, rid) == f"The {rid.rsplit('/', 1)[1]} finding, in its own words."


def test_a_gate_shows_its_name_from_the_gate_list(tmp_path, capsys):
    names = _gate_names()
    rows = _tree(_repo(tmp_path), capsys)
    assert _name(rows, "gates/G0") == names["G0"]  # active
    assert _name(rows, "gates/G3") == names["G3"]  # inactive, named by a finding's G3.1


def test_a_task_step_shows_its_name_from_the_task_list(tmp_path, capsys):
    names = _task_names()
    rows = _tree(_repo(tmp_path), capsys)
    for unit in ("alpha/a1-core", "alpha/a2-edges", "beta/b1-solo"):
        assert [_name(rows, f"{unit}/{task}") for task in TASK_KEYS] == names, unit


def test_a_verdict_shows_the_name_of_its_gate(tmp_path, capsys):
    root = _repo(tmp_path)
    _config(root, ["G0", "G4"])
    names = _gate_names()
    rows = _tree(root, capsys)
    for cid in ("alpha", "beta"):
        assert _name(rows, f"{cid}/G0") == names["G0"], cid  # before its status and evidence
        assert _name(rows, f"{cid}/G4") == names["G4"], cid


def test_the_no_gate_item_shows_no_summary(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _name(rows, "gates/G0") == _gate_names()["G0"]  # the gate beside it shows its name
    assert (_name(rows, "gates/none"), _row(rows, "gates/none")[3]) == (None, "")  # nothing


def test_a_gate_the_gate_list_lacks_shows_no_summary(tmp_path, capsys):
    root = _repo(tmp_path)
    _config(root, ["G0", "X1"])  # X1: an id the kit's gate list does not hold
    names = _gate_names()
    assert "X1" not in names
    rows = _tree(root, capsys)
    assert [_name(rows, rid) for rid in ("gates/G0", "alpha/G0")] == [names["G0"]] * 2
    assert [(_name(rows, rid), _row(rows, rid)[3]) for rid in ("gates/X1", "alpha/X1")] == [
        (None, ""), (None, "")]


def test_a_field_absent_blank_or_not_a_string_gives_no_summary(tmp_path, capsys):
    root = _repo(tmp_path)
    alpha = _contract("alpha", [
        {**_unit("a1-core", ["verify the core prints (SC1.1)", {"verify": "a mapping"}]),
         "done_means": 42},
        {**_unit("a2-edges", ["verify an edge holds"]), "done_means": " \n"},
        _unit("a3-plain", ["verify it holds"]),
    ])
    del alpha["intent"]
    _dump(_contract_path(root, "alpha"), alpha)
    _edit(_finding_path(root, "stale-pin"), statement=None)
    rows = _tree(root, capsys)
    assert _name(rows, "alpha/a3-plain") == "the work for a3-plain is done"  # a string shows
    assert _name(rows, "alpha/a1-core/SC1.1") == "verify the core prints (SC1.1)"
    assert _summary(rows, "alpha") is None  # no intent
    for rid in ("alpha/a1-core",           # done_means a number
                "alpha/a2-edges",          # done_means blank
                "alpha/a1-core/sketch-2",  # a sketch line that is a mapping
                "gates/G0/stale-pin"):     # no statement
        assert (_name(rows, rid), _summary(rows, rid)) == (None, None), rid


# --- SC4.1 the text unchanged: stripped, on one line, whole -------------------

# A finding as the form writes it: `statement: >` folds its lines into one and
# keeps a line break at the end.
FORM_SHAPED = """\
finding: slow-loop
date: 2026-09-22
kit_pinned: v0.14.0
gate: G3.1
diagnostic: none
kind: friction
count: 1
statement: >
  The loop runs slow on each save.
  It costs a minute each run.
proposal: >
  none
"""


def test_a_summary_drops_the_whitespace_around_its_text(tmp_path, capsys):
    root = _repo(tmp_path)
    assert yaml.safe_load(FORM_SHAPED)["statement"].endswith("run.\n")  # the form's `>`
    _finding_path(root, "slow-loop").write_text(FORM_SHAPED, encoding="utf-8")
    _dump(_contract_path(root, "beta"), _contract("beta", [
        {**BETA[0], "done_means": " \tthe work for b1-solo is done  \n"}]))
    rows, out = _printed(root, capsys)
    assert _name(rows, "gates/G3/G3.1/slow-loop") == (
        "The loop runs slow on each save. It costs a minute each run.")
    assert _name(rows, "beta/b1-solo") == "the work for b1-solo is done"
    assert _one_line_each(out)


def test_each_line_break_inside_a_summary_prints_as_one_space(tmp_path, capsys):
    root = _repo(tmp_path)
    _dump(_contract_path(root, "beta"), _contract("beta", [
        {**BETA[0],
         "done_means": "first line\nsecond line\r\nthird line\n\nafter a blank line\n"}]))
    rows, out = _printed(root, capsys)
    # \r\n is one line break; a blank line is two, so two spaces
    assert _name(rows, "beta/b1-solo") == (
        "first line second line third line  after a blank line")
    assert _one_line_each(out)


LONG_INTENT = (
    "A contract whose intent runs long on purpose: it holds 'single quotes', "
    '"double quotes", a bar | inside it, [brackets], a hash # and `backticks`, '
    "two  spaces kept as two, and it runs on well past the width of any "
    "terminal, so a tree that cut, wrapped or quoted its summary would print "
    "something other than this text, which the line must carry whole.")


def test_a_summary_prints_its_text_whole(tmp_path, capsys):
    root = _repo(tmp_path)
    _edit(_contract_path(root, "alpha"), intent=LONG_INTENT)
    rows, out = _printed(root, capsys)
    assert _summary(rows, "alpha") == LONG_INTENT  # no cut, no wrap, no quotes, its bar kept
    assert _one_line_each(out)


# --- the line: marks, evidence, links, the reference, then the summary --------

FEATURE_DOC = ("# A feature\n\nFEATURE-DOC-ONLY: these words live in the feature "
               "document and in no source field.\n")


def _feature_doc(root, cid):
    """docs/features/<cid>.md, holding words no source field holds."""
    path = root / "docs" / "features" / f"{cid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FEATURE_DOC, encoding="utf-8")


def test_the_summary_comes_last_after_one_bar(tmp_path, capsys):
    root = _repo(tmp_path)
    _feature_doc(root, "alpha")
    names = _gate_names()
    statement = "A fixture finding for the tree suite."
    rows = _tree(root, capsys)
    # only a contract keeps a bar: every other item's source text is its plain name
    assert (_name(rows, "gates/G3"), _row(rows, "gates/G3")[3]) == (names["G3"], " inactive")
    assert (_name(rows, "gates/G3/G3.1/slow-loop"),
            _row(rows, "gates/G3/G3.1/slow-loop")[3]) == (statement, " gate: G3.1")
    # the feature doc holds no revision table: its mark (project-tree o3), then the reference
    assert _row(rows, "alpha")[3] == f' no "Ready:" row doc: docs/features/alpha.md | {INTENT}'
    assert _row(rows, "alpha/a1-core")[3] == ""
    assert _row(rows, "alpha/a2-edges")[3] == " depends_on: alpha/a1-core"
    head, summary = _parts(rows, "alpha/G0")
    assert (head.split()[:1], summary) == (["via"], None)  # t3's evidence, no bar
    assert _name(rows, "alpha/G0") == names["G0"]


# --- SC5.1, SC5.2 links, typed and read from source fields --------------------

def test_a_unit_shows_one_depends_on_link_per_entry_in_its_order(tmp_path, capsys):
    root = _repo(tmp_path)
    _dump(_contract_path(root, "alpha"), _contract("alpha", ALPHA + [
        _unit("a3-join", ["verify the join holds"], depends_on=["a2-edges", "a1-core"])]))
    rows = _tree(root, capsys)
    assert _head(rows, "alpha/a2-edges") == " depends_on: alpha/a1-core"
    assert _head(rows, "alpha/a3-join") == (
        " depends_on: alpha/a2-edges depends_on: alpha/a1-core")  # the field's order, full ids


def test_a_finding_links_to_the_gate_its_field_names_as_written(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _head(rows, "gates/G0/stale-pin") == " gate: G0"
    assert _head(rows, "gates/G3/G3.1/slow-loop") == " gate: G3.1"  # the condition, kept, under it


def test_a_link_prints_only_from_depends_on_or_a_finding_gate(tmp_path, capsys):
    root = _repo(tmp_path)
    beta = _contract("beta", [{**BETA[0], "depends_on": []}])
    beta["dependencies"] = [{"ref": "vendor-feed", "status": "blocked",
                             "blocked_by": "the vendor feed"}]  # names other work, links nothing
    _dump(_contract_path(root, "beta"), beta)
    rows = _tree(root, capsys)
    assert _head(rows, "alpha/a2-edges") == " depends_on: alpha/a1-core"  # a source field
    assert [_head(rows, rid) for rid in (
        "alpha/a1-core",         # no depends_on
        "beta/b1-solo",          # depends_on: []
        "gates/none/idea",       # gate: none
        "gates/none/loose-end",  # no gate field
    )] == [""] * 4
    linked = [rid for _, rid, _, rest in rows
              if {"depends_on:", "gate:"} & set(rest.partition(BAR)[0].split())]
    assert linked == ["gates/G0/stale-pin", "gates/G3/G3.1/slow-loop", "alpha/a2-edges"]


# --- SC4.2 no document read but a feature doc's revision table (project-tree o3)

_WATCHES: list[list[str]] = []  # while a list is here, it collects each path opened
_HOOKED: list = []


def _on_audit(event, args):
    if event == "open" and _WATCHES and args and isinstance(args[0], (str, bytes, os.PathLike)):
        for seen in _WATCHES:
            seen.append(os.fsdecode(os.fspath(args[0])))


def _opened_while(action):
    """(each path the process opened while `action` ran, what it returned).
    An audit hook (PEP 578) sees every open; it is added once and does
    nothing while no test watches. Checking that a file exists opens nothing."""
    if not _HOOKED:
        sys.addaudithook(_on_audit)
        _HOOKED.append(_on_audit)
    seen: list[str] = []
    _WATCHES.append(seen)
    try:
        result = action()
    finally:
        _WATCHES.remove(seen)
    return seen, result


def _under(path, place):
    """Whether `path` is `place` or lies below it, compared as the OS compares paths."""
    path, place = (os.path.normcase(os.path.realpath(p)) for p in (path, place))
    return path == place or path.startswith(place.rstrip(os.sep) + os.sep)


def test_a_feature_doc_is_opened_for_its_revision_table_alone_and_no_other_document(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _feature_doc(root, "alpha")
    (root / "docs" / "gates").mkdir()
    (root / "docs" / "gates" / "G0-planning-intake.md").write_text("# G0\n", encoding="utf-8")
    documents = [root / name for name in ("REQUEST_alpha_2026-09-22.md", "STATE.md", "plan.md")]
    for path in documents:
        path.write_text("# A document, never a source\n", encoding="utf-8")
    opened, (code, out, _) = _opened_while(lambda: _run(root, capsys))
    assert code == 0
    rows = _rows(out)
    # project-tree o3: the feature doc is read for its revision table only, which
    # this one lacks; its words never print
    assert _head(rows, "alpha") == ' no "Ready:" row doc: docs/features/alpha.md'
    assert _head(rows, "beta") == " no feature document"  # no feature doc, no reference
    assert "FEATURE-DOC-ONLY" not in out
    assert any(_under(path, _contract_path(root, "alpha")) for path in opened)  # the watch works
    read = {os.path.normcase(os.path.realpath(path)) for path in opened
            if _under(path, root / "docs") or any(_under(path, doc) for doc in documents)}
    assert read == {os.path.normcase(os.path.realpath(root / "docs" / "features" / "alpha.md"))}


def test_with_docs_gone_every_line_prints_the_same_but_its_reference_and_its_mark(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _feature_doc(root, "alpha")
    _feature_doc(root, "beta")
    rows, first = _printed(root, capsys)
    references = [' no "Ready:" row doc: docs/features/alpha.md',
                  ' no "Ready:" row doc: docs/features/beta.md']
    assert [_head(rows, "alpha"), _head(rows, "beta")] == references
    assert _summary(rows, "alpha") == INTENT  # the print holds summaries to compare
    (root / "docs").rename(tmp_path / "docs-aside")
    _, second = _printed(root, capsys)
    # the reference goes, and the mark reads the missing file (project-tree o3)
    assert second == first.replace(references[0], " no feature document").replace(
        references[1], " no feature document")
