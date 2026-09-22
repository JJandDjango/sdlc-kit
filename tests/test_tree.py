"""The tree suite for ADR 0031 (contract tree-view).

`taskcontract tree` prints the work as one tree, computed from the repo's
files at every run: the gates with their findings, then each contract with
a verdict per active gate, its units, each unit's seven tasks and its
checks. Unit t1-tree-shape fixes that shape (SC1.1), the one place each
finding prints (SC1.2), and a print that is derived, never stored (SC1.3).
Statuses are asserted only as members of the six values: t3 derives them.
"""

from __future__ import annotations

import re
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

# One item per line: its full id, then its status (a finding: its kind) in
# brackets, then anything later units add.
ROW = re.compile(r"^(?P<indent> *)(?P<id>\S+) \[(?P<tag>[^\]]*)\](?P<rest>.*)$")


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
    """[(depth, id, tag, rest)] for every item line, in print order."""
    rows = []
    for line in out.splitlines():
        match = ROW.match(line)
        if match:
            rows.append((len(match["indent"]) // 2, match["id"], match["tag"],
                         match["rest"]))
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
    assert _children(_tree(root, capsys), "alpha") == [
        "alpha/G0", "alpha/a1-core", "alpha/a2-edges"]
    _config(root, ["G0", "G4"])
    assert _children(_tree(root, capsys), "alpha") == [
        "alpha/G0", "alpha/G4", "alpha/a1-core", "alpha/a2-edges"]


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
    assert len(rows) == 41  # 7 gate items, 23 under alpha, 11 under beta
    findings = [row for row in rows
                if row[1].startswith("gates/") and row[1].count("/") == 2]
    others = [row for row in rows if row not in findings]
    assert len(findings) == 4
    assert all(tag in STATUSES for _, _, tag, _ in others)


def test_a_finding_shows_its_kind_in_place_of_a_status(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _row(rows, "gates/G0/stale-pin")[2] == "kind: gap"
    assert _row(rows, "gates/G3/slow-loop")[2] == "kind: friction"
    assert _row(rows, "gates/none/idea")[2] == "kind: proposal"
    assert _row(rows, "gates/none/loose-end")[2] == "kind: escape"


# --- SC1.2 every finding once -----------------------------------------------

def test_each_finding_prints_once_under_the_gate_it_names(tmp_path, capsys):
    rows = _tree(_repo(tmp_path), capsys)
    assert _children(rows, "gates/G0") == ["gates/G0/stale-pin"]
    assert _children(rows, "gates/G3") == ["gates/G3/slow-loop"]  # G3.1, a condition of G3
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
    assert _children(rows, "gates/G0") == []  # an active gate prints with no findings


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
