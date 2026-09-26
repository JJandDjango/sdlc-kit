"""The conditions suite (contract project-tree, unit o1-conditions).

Each gate opens into its conditions, the named parts its kit page lists,
in the page's order. `taskcontract/data/gates.yaml` gives each gate a
`conditions:` list, each an `id` and a `name`, 57 in all, and G0's three
conditions a `rules:` list of the validator codes each owns. A name is the
page's heading without its date note and without a last word "check" or
"join". Under each contract the tree shows each gate in `active_gates`,
then the first gate after the last active one in the kit's order, marked
`inactive`; an inactive gate and its conditions read `to do` and never
count toward the contract's status (SC2.1).

Each G0 condition reads its status from its own rules, as the G0 verdict
is read: `failed` when one of its rules reports an error at the draft
profile, else `done` when none reports one at the ready profile, else
`blocked` when `TC003` is among them, else `to do`. A warning never
counts and never shows. A condition that is not done lists its
diagnostics in the whole tree's print, one line each, indented one level
under it: `- ` and the validator's message without its code, each line
break read as one space, each message once, in the validator's order; a
failed condition lists the draft profile's messages, any other the ready
profile's. At the repository level each gate that shows opens into its
conditions too, which read `to do`, and a finding whose `gate:` names a
condition its gate lists stands once under that condition, never under a
feature (SC2.2). The G0 verdict still reads from the validator, with its
evidence unchanged, and agrees with its conditions (SC2.3).

Each test drives the CLI in process against a fixture repo under
tmp_path and runs the real validator. The fixture repos sit outside any
git repository, so a verdict's evidence reads `at no commit`.
"""

from __future__ import annotations

import ast
import io
import re
from collections import Counter
from pathlib import Path

import pytest
import yaml

import taskcontract
from conftest import write_seat_roster
from taskcontract import checker, graph, tree_view, vocabulary
from taskcontract.__main__ import main

# The kit whose package runs: its gate list and the gate pages it names.
KIT = Path(taskcontract.__file__).resolve().parent.parent
GATES = KIT / "taskcontract" / "data" / "gates.yaml"
USAGE = KIT / "USAGE.md"

RED = "\U0001F534"
CLEAR = "\x1b[H\x1b[2J"
TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]
G0_CONDITIONS = ["G0.1", "G0.2", "G0.3"]
G0_NAMES = ["Definition-of-ready", "Vocabulary coverage", "Unit confirmation"]
G0_PAGE = "docs/gates/G0-planning-intake.md"
G0_RULES = {
    "G0.1": ["TC000", "TC001", "TC002", "TC003", "TC004", "TC005", "TC006", "TC007",
             "TC008", "TC009", "TC013", "TC014", "TC015"],
    "G0.2": ["TC010", "TC011", "TC012", "TC017", "W001"],
    "G0.3": ["TC016", "TC018"],
}
G1_LINES = [("G1.1", "Spec/schema linting"), ("G1.2", "Model checking"),
            ("G1.3", "Criteria completeness + ambiguity review")]

INTENT = ("A fixture contract for the conditions suite; its one unit carries "
          "one sketch line.")
STATEMENT = "A fixture finding for the conditions suite."

# The validator's messages the fixtures below provoke, as the tree prints them.
MSG_BLOCKED = "dependency 'vendor-feed' unresolved (blocked-by: the vendor feed)"
MSG_DRAFT_TERM = ("entity 'discount-code' is not ratified (status: draft) - draft does "
                  "not resolve; ratify the term or fork the vocabulary task")
MSG_UNCONFIRMED = ("unit 'u1-work' has no confirmed_by - the seat term 'intake-seat' is "
                   "ratified here (seats: user); take the intake answer for this unit")
MSG_SHORT = "intent must be 40-1200 chars (got 10)"
MSG_GHOST = "depends_on 'ghost' names no unit in this contract"
MSG_ZZ = ("entity 'zz-draft' is not ratified (status: draft) - draft does not "
          "resolve; ratify the term or fork the vocabulary task")
MSG_AA = ("entity 'aa-missing' names no vocabulary term - fork a vocabulary task "
          "(specs/vocabulary/aa-missing.yaml)")

# An item line: its indent, its id, its plain name when it has one
# (project-tree o2), its status (a finding: its kind) in brackets, then the
# rest. A diagnostic line: its indent, `- `, its text.
ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
DIAGNOSTIC = re.compile(r"^(?P<indent>(?:  )*)- (?P<text>.*)$")
CODE = re.compile(r"\b(?:TC\d{3}|W\d{3})\b")


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, find no git repo above the
    fixture, and give the pane a wide terminal."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


# --- the fixture repositories -------------------------------------------------

def _unit(uid="u1-work", confirmed=True, depends_on=None):
    unit = {"unit": "work for " + uid, "id": uid,
            "done_means": "the work for " + uid + " is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}
    if confirmed:
        unit["confirmed_by"] = ["user"]
    if depends_on is not None:
        unit["depends_on"] = list(depends_on)
    return unit


def _contract(cid, units=None, **fields):
    """A contract that reads ready-green; a field given as None is dropped."""
    doc = {"id": cid, "intent": INTENT, "scope": ["src/"], "non_goals": ["No other work"],
           "decomposition": units if units is not None else [_unit()],
           "dependencies": [], "entities": [],
           "provenance": {"origin": "human-request"}}
    for key, value in fields.items():
        if value is None:
            doc.pop(key)
        else:
            doc[key] = value
    return doc


BLOCKED_DEPENDENCY = [{"ref": "vendor-feed", "status": "blocked",
                       "blocked_by": "the vendor\nfeed"}]  # a line break inside


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _config(root, gates, **more):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates), **more})


def _term(root, slug, status, **more):
    _dump(root / "specs" / "vocabulary" / f"{slug}.yaml", {
        "term": slug, "name": slug.replace("-", " ").capitalize(),
        "definition": "A fixture term for the conditions suite.",
        "kind": "entity", "status": status, "since": "2026-01-01", **more})


def _finding(root, slug, gate):
    doc = {"finding": slug, "date": "2026-09-25", "kit_pinned": "v0.15.0",
           "diagnostic": "none", "kind": "gap", "count": 1,
           "statement": STATEMENT, "proposal": "none"}
    if gate is not None:
        doc["gate"] = gate
    _dump(root / ".sdlc" / "findings" / f"{slug}.yaml", doc)


def _put(root, cid, doc):
    _dump(root / "specs" / cid / "contract.yaml", doc)


def _repo(tmp_path, gates=("G0",)):
    """The contract `ready`, ready-green, with the given gates active."""
    root = tmp_path / "repo"
    _config(root, gates)
    write_seat_roster(root)
    _put(root, "ready", _contract("ready"))
    return root


# Each contract of the verdict repo: its G0 verdict and its conditions' statuses.
READINGS = {
    "drafted": ("to do", ["done", "to do", "done"]),        # draft-green, a G0.2 error
    "parked": ("blocked", ["blocked", "done", "done"]),     # draft-green with TC003
    "ready": ("done", ["done", "done", "done"]),            # ready-green
    "short": ("failed", ["failed", "done", "done"]),        # draft-red
    "unconfirmed": ("to do", ["done", "done", "to do"]),    # draft-green, a G0.3 error
}
# The diagnostics each condition that is not done lists.
DIAGNOSTICS = {
    "drafted/G0/G0.2": [MSG_DRAFT_TERM],
    "parked/G0/G0.1": [MSG_BLOCKED],
    "short/G0/G0.1": [MSG_SHORT],
    "unconfirmed/G0/G0.3": [MSG_UNCONFIRMED],
}


def _verdict_repo(tmp_path, gates=("G0",)):
    """One contract per G0 reading, in folder order: drafted (a draft
    entity: TC011 at ready), parked (a blocked dependency: TC003 at ready),
    ready (ready-green), short (a short intent: TC007 at draft) and
    unconfirmed (a unit with no confirmed_by: TC016 at ready)."""
    root = _repo(tmp_path, gates)
    _term(root, "discount-code", "draft")
    _put(root, "drafted", _contract("drafted", entities=["discount-code"]))
    _put(root, "parked", _contract("parked", dependencies=BLOCKED_DEPENDENCY))
    _put(root, "short", _contract("short", intent="Too short."))
    _put(root, "unconfirmed", _contract("unconfirmed", [_unit(confirmed=False)]))
    return root


# --- driving the CLI and reading its print --------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _print(root, capsys):
    """(rows, stdout, stderr) of the whole tree, which exits 0. Each row is
    a dict of depth, id, tag, plain name, rest and the diagnostics printed under it;
    every line printed is an item line or a diagnostic line one level under
    the item line above it."""
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    rows = []
    for text in out.splitlines():
        diagnostic = DIAGNOSTIC.match(text)
        if diagnostic:
            assert rows, f"a diagnostic line opens the print: {text!r}"
            assert len(diagnostic["indent"]) // 2 == rows[-1]["depth"] + 1, text
            rows[-1]["diagnostics"].append(diagnostic["text"])
            continue
        item = ITEM.match(text)
        assert item, f"neither an item line nor a diagnostic line: {text!r}"
        rows.append({"depth": len(item["indent"]) // 2, "id": item["id"], "tag": item["tag"],
                     "name": item["name"], "rest": item["rest"], "line": text,
                     "diagnostics": []})
    return rows, out, err


def _tree(root, capsys):
    return _print(root, capsys)[0]


def _ids(rows):
    return [row["id"] for row in rows]


def _row(rows, rid):
    for row in rows:
        if row["id"] == rid:
            return row
    raise AssertionError(f"{rid} not printed")


def _tag(rows, rid):
    return _row(rows, rid)["tag"]


def _children(rows, parent):
    """Ids one level under `parent`, in print order."""
    for i, row in enumerate(rows):
        if row["id"] == parent:
            found = []
            for child in rows[i + 1:]:
                if child["depth"] <= row["depth"]:
                    break
                if child["depth"] == row["depth"] + 1:
                    found.append(child["id"])
            return found
    raise AssertionError(f"{parent} not printed")


def _query(root, capsys, node):
    return _call(["tree", node, "--root", str(root)], capsys)


def _gate_list():
    return yaml.safe_load(GATES.read_text(encoding="utf-8"))["gates"]


# The conditions of each gate page, read from the page itself: each "###"
# heading under "## Conditions" that opens on a condition id, the first
# heading per id, named by the heading without its date note and without a
# last word "check" or "join".
_HEADING = re.compile(r"^### ((?:G\d+|PL-[A-Z]+)\.\d+) (.+)$")


def _page_conditions(page):
    found, inside = [], False
    for text in (KIT / page).read_text(encoding="utf-8").splitlines():
        if text.startswith("## "):
            inside = text.rstrip() == "## Conditions"
            continue
        match = _HEADING.match(text) if inside else None
        if match is None or match[1] in dict(found):
            continue
        name = re.sub(r" - added .*$", "", match[2].rstrip())
        name = re.sub(r" (?:check|join)$", "", name)
        found.append((match[1], name))
    return found


def _pages():
    """[(gate id, gate page)] in the kit's order, from the gate list."""
    return [(gate["id"], gate["page"]) for gate in _gate_list()]


# --- done_means: the gate list holds the 57 conditions ---------------------------

def test_the_gate_list_gives_each_gate_its_conditions_in_its_pages_order():
    total = 0
    for gate in _gate_list():
        listed = gate.get("conditions")
        assert isinstance(listed, list), f"{gate['id']} lists no conditions"
        assert [(c["id"], c["name"]) for c in listed] == _page_conditions(gate["page"]), gate["id"]
        for condition in listed:
            keys = {"id", "name", "rules"} if gate["id"] == "G0" else {"id", "name"}
            assert set(condition) == keys, condition
        total += len(listed)
    assert total == 57
    names = {c["id"]: c["name"] for gate in _gate_list() for c in gate["conditions"]}
    assert [names[cid] for cid in G0_CONDITIONS] == G0_NAMES
    assert names["G4.12"] == "Scope"
    assert names["G1.3"] == "Criteria completeness + ambiguity review"


def test_the_gate_list_gives_each_g0_condition_the_rules_it_owns():
    g0 = next(gate for gate in _gate_list() if gate["id"] == "G0")
    assert {c["id"]: c.get("rules") for c in g0.get("conditions", [])} == G0_RULES


def _named():
    """Every code the validator's sources name: TCnnn and Wnnn."""
    codes = set()
    for module in (checker, graph, vocabulary):
        codes |= set(CODE.findall(Path(module.__file__).read_text(encoding="utf-8")))
    return codes


def _literal(expr, constants):
    """The text a rule expression spells in the source: a string literal, or
    a name the module binds to one at its top level; None otherwise."""
    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        return expr.value
    if isinstance(expr, ast.Name):
        return constants.get(expr.id)
    return None


def _built_with(module):
    """(the codes each `Violation(...)` in the module is built with, the
    places whose code the source does not spell). A rule argument counts when
    it is a string literal, a module constant bound to one, or a name the
    same function assigns from a literal or unpacks from a call to a function
    of the module whose every return gives a literal at that place; a code
    built at runtime (an f-string, a join, a lookup) counts as unspelled."""
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    constants = {target.id: node.value.value for node in tree.body
                 if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                 and isinstance(node.value.value, str)
                 for target in node.targets if isinstance(target, ast.Name)}
    functions = {node.name: node for node in ast.walk(tree)
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Name) and node.func.id == "Violation"]
    codes, unspelled = set(), []
    for func in functions.values():
        for call in ast.walk(func):
            if call not in calls:
                continue
            rule = call.args[2] if len(call.args) > 2 else next(
                (word.value for word in call.keywords if word.arg == "rule"), None)
            spelled = [_literal(rule, constants)]
            if spelled[0] is None:
                spelled = _assigned(func, rule, constants, functions)
            if not spelled or None in spelled:
                unspelled.append(f"{Path(module.__file__).name}:{call.lineno}")
            else:
                codes |= set(spelled)
    placed = {call.lineno for func in functions.values() for call in ast.walk(func)
              if call in calls}
    unspelled += [f"{Path(module.__file__).name}:{call.lineno} (outside a function)"
                  for call in calls if call.lineno not in placed]
    return codes, unspelled


def _assigned(func, rule, constants, functions):
    """The literals a function's assignments give the name `rule`, one per
    source; None for a source that gives no literal; [] when none assigns it."""
    if not isinstance(rule, ast.Name):
        return []
    found = []
    for node in ast.walk(func):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == rule.id:
                found.append(_literal(node.value, constants))
                continue
            places = [i for i, element in enumerate(getattr(target, "elts", []))
                      if isinstance(element, ast.Name) and element.id == rule.id]
            for i in places:
                value = node.value
                callee = (functions.get(value.func.id) if isinstance(value, ast.Call)
                          and isinstance(value.func, ast.Name) else None)
                if callee is None:
                    found.append(None)
                    continue
                found += [_literal(ret.value.elts[i], constants)
                          if isinstance(ret.value, ast.Tuple) and len(ret.value.elts) > i
                          else None
                          for ret in ast.walk(callee) if isinstance(ret, ast.Return)]
    return found


def _emitted():
    """Every TCnnn and Wnnn code a Violation of the validator is built with,
    read from the source; a code the source does not spell fails here."""
    codes, unspelled = set(), []
    for module in (checker, graph, vocabulary):
        built, missed = _built_with(module)
        codes |= built
        unspelled += missed
    assert unspelled == [], f"a Violation's code built at runtime: {unspelled}"
    assert all(re.fullmatch(r"(?:TC|W|VT|VC)\d{3}", code) for code in codes), codes
    return {code for code in codes if CODE.fullmatch(code)}


def test_each_code_the_validator_emits_belongs_to_exactly_one_condition():
    emitted = _emitted()
    assert {"TC000", "TC003", "TC018", "W001"} <= emitted  # the reading works
    assert emitted == _named()  # each code the sources name is one a Violation carries
    owners = Counter(code for gate in _gate_list() for condition in gate.get("conditions", [])
                     for code in condition.get("rules", []))
    assert set(owners) == emitted  # a new code with no condition fails here
    assert all(count == 1 for count in owners.values()), owners
    carriers = [c["id"] for gate in _gate_list() for c in gate.get("conditions", [])
                if "rules" in c]
    assert carriers == G0_CONDITIONS


# --- SC2.1 the gates under a feature, and each gate's conditions ------------------

def test_sc2_1_a_contract_shows_its_active_gates_then_the_next_gate_inactive(tmp_path, capsys):
    root = _repo(tmp_path)
    rows = _tree(root, capsys)
    assert _children(rows, "ready") == ["ready/G0", "ready/G1", "ready/u1-work"]
    assert _row(rows, "ready/G1")["line"] == "  ready/G1 Requirements / Spec [to do] inactive"
    assert _row(rows, "ready/G0")["rest"].startswith(" via ")  # active: no inactive mark
    assert [row["id"] for row in rows if row["depth"] == 0] == ["gates/G0", "ready"]
    _config(root, ["G4", "G0"])
    rows = _tree(root, capsys)
    assert _children(rows, "ready") == ["ready/G0", "ready/G4", "ready/G5", "ready/u1-work"]
    assert _row(rows, "ready/G4")["line"] == "  ready/G4 Pre-merge CI [to do]"
    assert _row(rows, "ready/G5")["line"] == "  ready/G5 Integration / System [to do] inactive"
    # the repository level shows the gates it showed before: the active ones
    assert [row["id"] for row in rows if row["depth"] == 0] == ["gates/G0", "gates/G4", "ready"]


def test_sc2_1_with_no_active_gate_a_contract_shows_g0_inactive(tmp_path, capsys):
    root = _verdict_repo(tmp_path, gates=())
    rows = _tree(root, capsys)
    for cid in READINGS:
        assert _children(rows, cid) == [f"{cid}/G0", f"{cid}/u1-work"], cid
        # inactive: to do, no validator run, and its conditions to do with nothing listed
        assert _row(rows, f"{cid}/G0")["line"] == (
            f"  {cid}/G0 Planning / Intake [to do] inactive"), cid
        for condition, name in zip(G0_CONDITIONS, G0_NAMES):
            row = _row(rows, f"{cid}/G0/{condition}")
            assert (row["line"], row["diagnostics"]) == (
                f"    {cid}/G0/{condition} {name} [to do]", []), cid
    assert not any(row["id"].startswith("gates/") for row in rows)


def test_sc2_1_with_the_last_gate_active_no_inactive_gate_shows(tmp_path, capsys):
    root = _repo(tmp_path, gates=("G0", "PL-PIPE"))
    rows = _tree(root, capsys)
    assert _children(rows, "ready") == ["ready/G0", "ready/PL-PIPE", "ready/u1-work"]
    assert _children(rows, "ready/PL-PIPE") == [
        "ready/PL-PIPE/PL-PIPE.1", "ready/PL-PIPE/PL-PIPE.2", "ready/PL-PIPE/PL-PIPE.3"]
    assert not any("inactive" in row["rest"].split() for row in rows)


def test_sc2_1_every_gate_opens_into_its_conditions_in_the_kit_order(tmp_path, capsys):
    pages = _pages()
    root = _repo(tmp_path, gates=[gate for gate, _ in pages])  # every gate active
    rows = _tree(root, capsys)
    total = 0
    for gate, page in pages:
        conditions = _page_conditions(page)
        total += len(conditions)
        for base in (f"gates/{gate}", f"ready/{gate}"):
            assert _children(rows, base) == [f"{base}/{cid}" for cid, _ in conditions], base
            for cid, name in conditions:
                row = _row(rows, f"{base}/{cid}")
                # a condition line carries its name and its status, no evidence
                assert (row["name"], row["rest"]) == (name, ""), row["line"]
                assert row["tag"] in ("done", "to do"), row["line"]
    assert total == 57


def test_sc2_1_each_g0_condition_reads_its_status_from_its_own_rules(tmp_path, capsys):
    rows = _tree(_verdict_repo(tmp_path), capsys)
    for cid, (_, statuses) in READINGS.items():
        assert _children(rows, f"{cid}/G0") == [f"{cid}/G0/{c}" for c in G0_CONDITIONS], cid
        assert [_tag(rows, f"{cid}/G0/{c}") for c in G0_CONDITIONS] == statuses, cid


def test_sc2_1_a_warning_never_changes_a_status_and_never_shows(tmp_path, capsys):
    root = _repo(tmp_path)
    _term(root, "old-term", "deprecated", sunset="2099-01-01")  # W001: inside its window
    _put(root, "warned", _contract("warned", entities=["old-term"]))
    assert [v.rule for v in checker.validate_path(root / "specs" / "warned" / "contract.yaml")
            ] == ["W001"]  # the fixture provokes the warning alone
    rows, out, _ = _print(root, capsys)
    assert [_tag(rows, f"warned/G0/{c}") for c in G0_CONDITIONS] == ["done"] * 3
    assert _tag(rows, "warned/G0") == "done"
    assert _row(rows, "warned/G0/G0.2")["diagnostics"] == []
    assert "deprecated" not in out


def test_sc2_1_an_inactive_gate_never_counts_toward_its_contracts_status(tmp_path, capsys):
    root = _repo(tmp_path)
    _dump(root / ".sdlc" / "progress" / "ready.yaml", {"records": [
        {"item": "ready", "state": "done", "at": "2026-09-25T10:00:00Z", "head": "1a2b3c4"}]})
    rows = _tree(root, capsys)
    assert _tag(rows, "ready/G0") == "done"
    assert _row(rows, "ready/G1")["line"] == "  ready/G1 Requirements / Spec [to do] inactive"
    assert [_tag(rows, f"ready/G1/{c}") for c, _ in G1_LINES] == ["to do"] * 3
    # a closed contract; its drift mark (project-tree o3) before its evidence
    assert _row(rows, "ready")["line"].startswith(
        "ready (no title) [done] no feature document at 1a2b3c4 | ")


def test_sc2_1_the_conditions_of_every_gate_but_g0_read_to_do(tmp_path, capsys):
    root = _repo(tmp_path, gates=("G0", "G3"))
    _dump(root / ".sdlc" / "progress" / "ready.yaml", {"records": [
        {"item": "ready", "state": "done", "at": "2026-09-25T10:00:00Z", "head": "1a2b3c4"}]})
    rows = _tree(root, capsys)
    assert [_tag(rows, f"ready/G0/{c}") for c in G0_CONDITIONS] == ["done"] * 3
    for base, gate in (("ready/G3", "G3"), ("ready/G4", "G4"), ("gates/G3", "G3")):
        under = _children(rows, base)
        assert under and all(cid.startswith(f"{base}/{gate}.") for cid in under), base
        assert {_tag(rows, cid) for cid in under} == {"to do"}, base
    # the repository level reads no validator: G0's conditions there read to do
    assert [_tag(rows, f"gates/G0/{c}") for c in G0_CONDITIONS] == ["to do"] * 3


# --- SC2.2 what the rules report, and the findings under a condition --------------

def test_sc2_2_a_condition_not_done_lists_each_diagnostic_on_its_own_line_without_its_code(
        tmp_path, capsys):
    rows, out, _ = _print(_verdict_repo(tmp_path), capsys)
    lines = out.splitlines()
    for rid, messages in DIAGNOSTICS.items():
        row = _row(rows, rid)
        assert row["diagnostics"] == messages, rid
        at = lines.index(row["line"])
        assert lines[at + 1:at + 1 + len(messages)] == [f"      - {m}" for m in messages], rid
    assert CODE.findall(out) == []  # no code on any line


def test_sc2_2_a_done_condition_lists_no_diagnostic(tmp_path, capsys):
    rows, out, _ = _print(_verdict_repo(tmp_path), capsys)
    lines = out.splitlines()
    at = lines.index(_row(rows, "ready/G0")["line"])
    assert lines[at + 1:at + 5] == [
        "    ready/G0/G0.1 Definition-of-ready [done]",
        "    ready/G0/G0.2 Vocabulary coverage [done]",
        "    ready/G0/G0.3 Unit confirmation [done]",
        "  ready/G1 Requirements / Spec [to do] inactive"]
    done = [row for row in rows if "/G0/G0." in row["id"] and row["tag"] == "done"]
    assert len(done) == 11 and all(row["diagnostics"] == [] for row in done)


def test_sc2_2_a_failed_condition_lists_the_draft_profiles_messages_and_any_other_the_ready(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _term(root, "discount-code", "draft")
    # draft: TC007; ready: TC003 and TC007 (G0.1), TC011 (G0.2)
    _put(root, "mixed", _contract("mixed", intent="Too short.",
                                  dependencies=BLOCKED_DEPENDENCY,
                                  entities=["discount-code"]))
    rows = _tree(root, capsys)
    assert _tag(rows, "mixed/G0") == "failed"
    assert [(_tag(rows, f"mixed/G0/{c}"), _row(rows, f"mixed/G0/{c}")["diagnostics"])
            for c in G0_CONDITIONS] == [
        ("failed", [MSG_SHORT]),        # the draft profile's messages: no TC003
        ("to do", [MSG_DRAFT_TERM]),    # the ready profile's
        ("done", [])]


def test_sc2_2_a_message_holding_a_line_break_prints_on_one_line(tmp_path, capsys):
    root = _verdict_repo(tmp_path)
    raw = [v.message for v in checker.validate_path(root / "specs" / "parked" / "contract.yaml")]
    assert raw == ["dependency 'vendor-feed' unresolved (blocked-by: the vendor\nfeed)"]
    rows, out, _ = _print(root, capsys)
    assert _row(rows, "parked/G0/G0.1")["diagnostics"] == [MSG_BLOCKED]
    assert f"      - {MSG_BLOCKED}" in out.splitlines()


def test_sc2_2_diagnostics_keep_the_validators_order_and_a_repeated_message_prints_once(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _term(root, "zz-draft", "draft")
    # two units name the same missing unit: TC014 twice, in the same words
    _put(root, "ordered", _contract(
        "ordered", [_unit("u1-work", depends_on=["ghost"]), _unit("u2-more", depends_on=["ghost"])],
        entities=["zz-draft", "aa-missing"]))
    draft = checker.validate_path(root / "specs" / "ordered" / "contract.yaml", profile="draft")
    assert [v.message for v in draft] == [MSG_GHOST, MSG_GHOST]
    rows = _tree(root, capsys)
    assert _row(rows, "ordered/G0/G0.1")["diagnostics"] == [MSG_GHOST]
    # the validator's order: by the entry, not by the code or the words
    assert _row(rows, "ordered/G0/G0.2")["diagnostics"] == [MSG_ZZ, MSG_AA]


def test_sc2_2_a_finding_that_names_a_condition_stands_once_under_it_for_the_repository(
        tmp_path, capsys):
    root = _verdict_repo(tmp_path)
    _finding(root, "slow-loop", "G3.1")   # a condition of G3, a gate not active
    _finding(root, "tidy-terms", "G0.2")  # a condition of G0, the active gate
    rows = _tree(root, capsys)
    assert _row(rows, "gates/G3")["line"] == "gates/G3 Implementation [to do] inactive"
    assert _children(rows, "gates/G3") == ["gates/G3/G3.1", "gates/G3/G3.2", "gates/G3/G3.3"]
    assert _children(rows, "gates/G3/G3.1") == ["gates/G3/G3.1/slow-loop"]
    assert _children(rows, "gates/G0/G0.2") == ["gates/G0/G0.2/tidy-terms"]
    assert _row(rows, "gates/G3/G3.1")["line"] == "  gates/G3/G3.1 Formatter [to do]"
    assert _row(rows, "gates/G0/G0.2")["line"] == "  gates/G0/G0.2 Vocabulary coverage [to do]"
    assert _row(rows, "gates/G3/G3.1/slow-loop")["line"] == (
        f"    gates/G3/G3.1/slow-loop {STATEMENT} [kind: gap] gate: G3.1")
    for slug in ("slow-loop", "tidy-terms"):
        printed = [rid for rid in _ids(rows) if rid.endswith("/" + slug)]
        assert len(printed) == 1, printed  # once, and never under a feature
        assert printed[0].startswith("gates/")


def test_sc2_2_a_finding_that_names_its_gate_or_an_unlisted_condition_stands_after_the_conditions(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _finding(root, "stale-pin", "G0")    # the gate itself
    _finding(root, "odd-one", "G3.9")    # a condition G3 does not list
    _finding(root, "strange", "X1.1")    # a gate the kit's list lacks
    _finding(root, "idea", "none")
    rows = _tree(root, capsys)
    assert _children(rows, "gates/G0") == [
        "gates/G0/G0.1", "gates/G0/G0.2", "gates/G0/G0.3", "gates/G0/stale-pin"]
    assert _children(rows, "gates/G3") == [
        "gates/G3/G3.1", "gates/G3/G3.2", "gates/G3/G3.3", "gates/G3/odd-one"]
    assert _children(rows, "gates/X1") == ["gates/X1/strange"]
    assert _children(rows, "gates/none") == ["gates/none/idea"]
    assert _row(rows, "gates/G3/odd-one")["line"] == (
        f"  gates/G3/odd-one {STATEMENT} [kind: gap] gate: G3.9")


def test_sc2_2_the_query_prints_a_condition_as_it_prints_a_gate_without_diagnostics(
        tmp_path, capsys):
    root = _verdict_repo(tmp_path)
    _finding(root, "slow-loop", "G3.1")
    expected = {
        # the name on the first line, after the id; no summary line (project-tree o2)
        "drafted/G0/G0.2": ("drafted/G0/G0.2 Vocabulary coverage [to do]\n"
                            f"page: {G0_PAGE}\n"),
        "short/G0/G0.1": ("short/G0/G0.1 Definition-of-ready [failed]\n"
                          f"page: {G0_PAGE}\n"),
        "ready/G1/G1.1": ("ready/G1/G1.1 Spec/schema linting [to do]\n"
                          "page: docs/gates/G1-requirements-spec.md\n"),
        "gates/G3/G3.1": ("gates/G3/G3.1 Formatter [to do]\n"
                          "page: docs/gates/G3-implementation.md\n"),
        "ready/G1": ("ready/G1 Requirements / Spec [to do] inactive\n"
                     "file: specs/ready/contract.yaml:1\n"
                     "page: docs/gates/G1-requirements-spec.md\n"),
        "gates/G3/G3.1/slow-loop": (f"gates/G3/G3.1/slow-loop {STATEMENT} [kind: gap]\n"
                                    "gate: G3.1\n"
                                    "file: .sdlc/findings/slow-loop.yaml:1\n"),
    }
    for node, block in expected.items():
        assert _query(root, capsys, node) == (0, block, ""), node


# --- SC2.3 the G0 verdict still reads from the validator ---------------------------

def _verdict_line(cid, status):
    return (f"  {cid}/G0 Planning / Intake [{status}] via python -m taskcontract validate "
            f"specs/{cid}/contract.yaml --profile ready at no commit")


def test_sc2_3_the_g0_verdict_still_reads_from_the_validator_above_its_conditions(
        tmp_path, capsys):
    rows = _tree(_verdict_repo(tmp_path), capsys)
    for cid, (verdict, _) in READINGS.items():
        assert _row(rows, f"{cid}/G0")["line"] == _verdict_line(cid, verdict), cid
        assert _row(rows, f"{cid}/G0")["diagnostics"] == []  # the verdict lists none itself
        assert _children(rows, f"{cid}/G0") == [f"{cid}/G0/{c}" for c in G0_CONDITIONS], cid


def _agreement(statuses):
    """The verdict its conditions give."""
    if "failed" in statuses:
        return "failed"
    if "blocked" in statuses:
        return "blocked"
    return "done" if all(status == "done" for status in statuses) else "to do"


def test_sc2_3_the_g0_verdict_agrees_with_its_conditions(tmp_path, capsys):
    root = _verdict_repo(tmp_path)
    _put(root, "mixed", _contract("mixed", intent="Too short.",
                                  dependencies=BLOCKED_DEPENDENCY,
                                  entities=["discount-code"]))
    _put(root, "undeclared", _contract("undeclared", entities=None))  # TC017 at ready
    rows = _tree(root, capsys)
    seen = set()
    for cid in [*READINGS, "mixed", "undeclared"]:
        statuses = [_tag(rows, f"{cid}/G0/{c}") for c in G0_CONDITIONS]
        verdict = _tag(rows, f"{cid}/G0")
        assert verdict == _agreement(statuses), (cid, verdict, statuses)
        seen.add(verdict)
    assert seen == {"done", "blocked", "to do", "failed"}
    assert _tag(rows, "undeclared/G0/G0.2") == "to do"


# --- the USAGE section -------------------------------------------------------------

def _section_nine():
    text = USAGE.read_text(encoding="utf-8")
    start = text.index("\n## 9. ")
    return text[start:text.index("\n## 10. ", start)]


def test_usage_marks_its_project_tree_subsections_red_and_its_example_is_the_tree(
        tmp_path, capsys):
    section = _section_nine()
    headings = [text for text in section.splitlines() if text.startswith("### ")]
    assert headings[-5:] == [
        f"### {name} {RED}" for name in (
            "Gates and their conditions", "Plain names and titles",
            "Drift from the feature document", "Blocked and waiting, named",
            "The interactive pane")]
    part = section[section.index(f"### Gates and their conditions {RED}"):]
    example = part.split("```\n", 2)[1].splitlines()
    # the contract line opens on its id and its title, then its status (project-tree
    # o2), then its drift mark before intake writes the Ready row (project-tree o3)
    assert example[0] == (
        'apply-discount Apply one discount code per order [to do] no "Ready:" row '
        "doc: docs/features/apply-discount.md | Checkout applies one discount code per order.")
    root = _repo(tmp_path)
    _term(root, "discount-code", "draft")
    _put(root, "apply-discount", _contract(
        "apply-discount", title="Apply one discount code per order",
        intent="Checkout applies one discount code per order.",
        entities=["discount-code"]))
    # the feature document, its revision table signed but not yet read by intake
    document = root / "docs" / "features" / "apply-discount.md"
    document.parent.mkdir(parents=True)
    document.write_text(
        "| Revision Date | Revised By | Changes Made |\n| :-: | :-: | :-- |\n"
        "| 2026-09-24 | user | r1: Created through an interview |\n"
        "| 2026-09-24 | user | r2: The request half finished; signed by the PO seat |\n"
        "\n# apply-discount - Apply one discount code per order\n", encoding="utf-8")
    _, out, _ = _print(root, capsys)
    lines = out.splitlines()
    tops = [text for text in lines if text.startswith("apply-discount ")]
    assert len(tops) == 1, tops
    at = lines.index(tops[0])
    # the whole example, the contract line included, line for line
    wanted = [re.sub(r" at 1a2b3c4$", " at no commit", text) for text in example]
    assert lines[at:at + len(example)] == wanted


# --- ruling: progress refuses a condition ----------------------------------------------

def _snapshot(root):
    return {str(p.relative_to(root)): (p.is_dir(), p.stat().st_size, p.stat().st_mtime_ns)
            for p in root.rglob("*")}


def test_progress_refuses_a_condition_id_naming_its_kind_and_writes_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    before = _snapshot(root)
    for node in ("ready/G0/G0.1", "ready/G1/G1.2", "gates/G0/G0.3"):
        calls = [
            (["progress", "done", node, "--root", str(root)],
             f"taskcontract progress: '{node}' is a condition, not a task, unit or contract"
             " - done takes a task, unit or contract id\n"),
            (["progress", "start", node, "--root", str(root)],
             f"taskcontract progress: '{node}' is a condition, not a task - start takes a task id\n"),
            (["progress", "block", node, "--reason", "waiting", "--root", str(root)],
             f"taskcontract progress: '{node}' is a condition, not a task - block takes a task id\n"),
            (["progress", "run", node, "--root", str(root), "--", "python", "-c", "pass"],
             f"taskcontract progress: '{node}' is a condition, not a check - run takes a check id\n"),
        ]
        for argv, refusal in calls:
            assert _call(argv, capsys) == (2, "", refusal), argv
    assert _snapshot(root) == before


# --- existing behavior holds with the new items ----------------------------------------

def test_the_whole_tree_prints_every_item_and_exits_0_beside_an_unreadable_source(
        tmp_path, capsys):
    root = _verdict_repo(tmp_path)
    broken = root / "specs" / "broken" / "contract.yaml"
    broken.parent.mkdir(parents=True)
    broken.write_text("id: [unclosed\n", encoding="utf-8")
    listed = root / "specs" / "listed" / "contract.yaml"
    listed.parent.mkdir(parents=True)
    listed.write_text("- one\n- two\n", encoding="utf-8")  # parses, but not a mapping
    (root / ".sdlc" / "findings").mkdir(parents=True)
    (root / ".sdlc" / "findings" / "garbled.yaml").write_text("gate: [unclosed\n", encoding="utf-8")
    rows, out, err = _print(root, capsys)  # every line an item or a diagnostic line
    assert err.splitlines() == [  # one line per source, as before
        "taskcontract tree: unreadable finding: .sdlc/findings/garbled.yaml (YAML error at line 2)",
        "taskcontract tree: unreadable contract: specs/broken/contract.yaml (YAML error at line 2)",
        "taskcontract tree: unreadable contract: specs/listed/contract.yaml (not a mapping)"]
    # G0.1 fails from the validator; the joins behind G0.2 and G0.3 never ran on
    # a contract the tree cannot read as a mapping, so those read to do, never done
    for cid in ("broken", "listed"):
        assert [_tag(rows, f"{cid}/G0/{c}") for c in G0_CONDITIONS] == [
            "failed", "to do", "to do"], cid
        assert _tag(rows, f"{cid}/G0") == "failed", cid
        assert [_row(rows, f"{cid}/G0/{c}")["diagnostics"] for c in ("G0.2", "G0.3")] == [[], []]
    # the validator's multi-line YAML message prints on one line
    (message,) = _row(rows, "broken/G0/G0.1")["diagnostics"]
    assert message.startswith("unreadable contract: ")
    for cid in READINGS:
        assert f"{cid}/u1-work/SC1.1" in _ids(rows), cid


_LINKED = re.compile(r" (?:depends_on|gate|doc): \S+")


def _first(row):
    """The query's first line for a row of the whole tree: its line cut
    after the evidence, so its id, its plain name, its tag, its marks and its
    evidence, without its links, doc and summary."""
    return (row["id"] + (f" {row['name']}" if row["name"] else "") + f" [{row['tag']}]"
            + _LINKED.sub("", row["rest"].partition(" | ")[0]))


def test_every_id_the_tree_prints_answers_as_a_query_in_at_most_seven_lines(tmp_path, capsys):
    root = _repo(tmp_path)
    _term(root, "discount-code", "draft")
    _put(root, "drafted", _contract("drafted", entities=["discount-code"]))
    _put(root, "short", _contract("short", intent="Too short."))
    _finding(root, "slow-loop", "G3.1")
    _finding(root, "stale-pin", "G0")
    rows, _, _ = _print(root, capsys)
    ids = _ids(rows)
    assert len(ids) == len(set(ids))
    for rid in ("gates/G0/G0.1", "gates/G3/G3.1/slow-loop", "gates/G0/stale-pin",
                "drafted/G0/G0.2", "short/G1/G1.3"):
        assert rid in ids, rid
    for row in rows:
        code, out, err = _query(root, capsys, row["id"])
        assert (code, err) == (0, ""), row["id"]
        lines = out.splitlines()
        assert lines[0] == _first(row), row["id"]
        assert len(lines) <= 7, out
        assert not any(DIAGNOSTIC.match(text) for text in lines), out


class _Interrupt:
    """The pane's injected sleep: it ends the loop at its first call."""

    def __call__(self, seconds):
        raise KeyboardInterrupt


def _pane(root):
    out = io.StringIO()
    assert tree_view.follow(root, out, sleep=_Interrupt()) == 0
    text = out.getvalue()
    assert text.startswith(CLEAR)
    return text[len(CLEAR):].splitlines()


def test_the_follow_pane_folds_the_new_items_and_shows_no_diagnostic(tmp_path, capsys):
    root = _repo(tmp_path)
    _term(root, "discount-code", "draft")
    _put(root, "drafted", _contract("drafted", entities=["discount-code"]))
    _dump(root / ".sdlc" / "progress" / "ready.yaml", {"records": [
        {"item": "ready/u1-work/write-tests", "state": "doing",
         "at": "2026-09-25T10:00:00Z", "head": "1a2b3c4"}]})
    rows = _tree(root, capsys)
    whole = {row["id"]: row["line"] for row in rows}
    task = whole["ready/u1-work/write-tests"]
    assert _pane(root) == [
        "specs/ready/contract.yaml > ready > u1-work > write-tests",
        "2 more: 2 to do",                   # gates/G0, drafted
        whole["ready"],
        "  2 more: 1 to do, 1 done",         # ready/G0 done, ready/G1 inactive
        "  u1-work" + whole["ready/u1-work"][len("  ready/u1-work"):],
        "    7 more: 7 to do",               # the other six tasks and the check
        "    write-tests" + task[len("    ready/u1-work/write-tests"):],
    ]
    _config(root, ["G0"], tree={"pane": {"fold": "names"}})
    lines = _pane(root)
    assert lines[1] == "2 more: gates/G0 [to do], drafted [to do]"
    assert lines[3] == "  2 more: G0 [done], G1 [to do]"
    assert not any(DIAGNOSTIC.match(text) for text in lines)
