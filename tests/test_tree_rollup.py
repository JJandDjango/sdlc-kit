"""The gate roll-up suite (contract tree-first-level, unit t1-gate-rollup).

A gate item at the first level reads the roll-up of the features' verdicts
at its gate, and each of its conditions reads the roll-up of that condition
across the same verdicts: each feature's own reading of the condition. A
verdict marked `inactive` never counts; a closed feature's verdicts count as
they read, since a close governs only its own feature's roll-up. The roll-up
takes the first of `failed`, `waiting on a seat`, `blocked` and `doing` that
any counted verdict reads; otherwise `done` when every one reads `done`, `to
do` when every one reads `to do`, and `doing` when some read `done` and some
`to do`. A gate or condition in which no verdict counts reads `to do`, with
no diagnostic (SC1.1).

A gate item or condition that is not `done` names each feature holding it
back, one diagnostic per feature, in the tree's order of features:
`{feature} holds {id} at {status}`, printed in the whole tree's text as `- `
and the message, one level under the item, right after its line and before
its conditions and findings (SC1.2). A finding still stands once under the
condition or gate its `gate:` field names, shows its kind and never a
status, and counts in no roll-up (SC1.3). Every line printed today for a
feature with a contract, and every finding line, stays byte for byte.

Each test drives the CLI in process against a fixture repo under tmp_path
and runs the real validator. The fixture repos sit outside any git
repository, so a verdict's evidence reads `at no commit`.
"""

from __future__ import annotations

import re

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

G0_PAGE = "docs/gates/G0-planning-intake.md"
INTENT = ("A fixture contract for the roll-up suite; its one unit carries "
          "one sketch line.")
STATEMENT = "A fixture finding for the roll-up suite."

# An item line: its indent, its id, its plain name when it has one, its
# status (a finding: its kind) in brackets, then the rest. A diagnostic line:
# its indent, `- `, its text.
ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
DIAGNOSTIC = re.compile(r"^(?P<indent>(?:  )*)- (?P<text>.*)$")


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

def _unit(confirmed=True):
    unit = {"unit": "work for u1-work", "id": "u1-work",
            "done_means": "the work for u1-work is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}
    if confirmed:
        unit["confirmed_by"] = ["user"]
    return unit


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
    doc = {"finding": slug, "date": "2026-09-25", "kit_pinned": "v0.15.0",
           "diagnostic": "none", "kind": "gap", "count": 1,
           "statement": STATEMENT, "proposal": "none"}
    if gate is not None:
        doc["gate"] = gate
    _dump(root / ".sdlc" / "findings" / f"{slug}.yaml", doc)


# Each fixture contract by its id, and what it reads at G0: its verdict and
# its conditions G0.1, G0.2, G0.3.
CONTRACTS = {
    # draft-green, one draft entity (TC011 at ready): to do; G0.2 to do
    "drafted": lambda: _contract("drafted", entities=["discount-code"]),
    "apply-discount": lambda: _contract("apply-discount", entities=["discount-code"]),
    # draft-green with a blocked dependency (TC003 at ready): blocked; G0.1 blocked
    "parked": lambda: _contract("parked", dependencies=[
        {"ref": "vendor-feed", "status": "blocked", "blocked_by": "the vendor feed"}]),
    # ready-green: done; every condition done
    "ready": lambda: _contract("ready"),
    "sealed": lambda: _contract("sealed"),
    "ship-rates": lambda: _contract("ship-rates"),
    # draft-red, a short intent (TC007 at draft): failed; G0.1 failed
    "short": lambda: _contract("short", intent="Too short."),
    # draft-green, a unit with no confirmed_by (TC016 at ready): to do; G0.3 to do
    "unconfirmed": lambda: _contract("unconfirmed", decomposition=[_unit(confirmed=False)]),
}


def _repo(tmp_path, cids, gates=("G0",), name="repo"):
    """A repo with the given gates active and the named fixture contracts,
    written in the order given."""
    root = tmp_path / name
    _config(root, gates)
    write_seat_roster(root)
    _dump(root / "specs" / "vocabulary" / "discount-code.yaml", {
        "term": "discount-code", "name": "Discount code",
        "definition": "A fixture term for the roll-up suite.",
        "kind": "entity", "status": "draft", "since": "2026-01-01"})
    for cid in cids:
        _dump(root / "specs" / cid / "contract.yaml", CONTRACTS[cid]())
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
    a dict of depth, id, tag, line and the diagnostics printed under it;
    every diagnostic line sits one level under the item line above it."""
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
    """What an item reads: (its tag, its diagnostics)."""
    row = _row(rows, rid)
    return row["tag"], row["diagnostics"]


def _block(out, rid):
    """The whole tree's lines from the top-level item `rid` to the next
    top-level item, as one text."""
    lines = out.splitlines()
    start = next(i for i, text in enumerate(lines) if text.startswith(rid + " "))
    end = next((i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
               len(lines))
    return "\n".join(lines[start:end]) + "\n"


def _features(rows):
    """The ids at the first level that are not gate items, in print order."""
    return [row["id"] for row in rows if row["depth"] == 0 and not row["id"].startswith("gates/")]


# --- SC1.1: a gate item reads the roll-up of its verdicts -----------------------

# Each case: the contracts in the repo, then what gates/G0 reads and the
# features it names.
GATE_CASES = {
    "every-verdict-done": (("ready", "sealed"), "done", []),
    "every-verdict-to-do": (("drafted", "unconfirmed"), "to do",
                            ["drafted holds G0 at to do", "unconfirmed holds G0 at to do"]),
    "done-and-to-do": (("drafted", "ready"), "doing", ["drafted holds G0 at to do"]),
    "blocked-first": (("drafted", "parked", "ready"), "blocked",
                      ["drafted holds G0 at to do", "parked holds G0 at blocked"]),
    "failed-first": (("parked", "ready", "short"), "failed",
                     ["parked holds G0 at blocked", "short holds G0 at failed"]),
    "every-reading": (("drafted", "parked", "ready", "short", "unconfirmed"), "failed",
                      ["drafted holds G0 at to do", "parked holds G0 at blocked",
                       "short holds G0 at failed", "unconfirmed holds G0 at to do"]),
}


@pytest.mark.parametrize("case", list(GATE_CASES))
def test_sc1_1_a_gate_item_reads_the_roll_up_of_the_verdicts_at_its_gate(tmp_path, capsys, case):
    cids, status, holds = GATE_CASES[case]
    rows = _tree(_repo(tmp_path, cids), capsys)
    # Each verdict still reads as the validator says.
    readings = {"drafted": "to do", "parked": "blocked", "ready": "done", "sealed": "done",
                "short": "failed", "unconfirmed": "to do"}
    assert {cid: _row(rows, f"{cid}/G0")["tag"] for cid in cids} == {
        cid: readings[cid] for cid in cids}
    assert _reads(rows, "gates/G0") == (status, holds)


def test_sc1_1_at_a_gate_a_done_verdict_starts_it_where_a_feature_stays_to_do(tmp_path, capsys):
    rows = _tree(_repo(tmp_path, ["ready"]), capsys)
    # The feature's own roll-up: a done verdict alone never starts it.
    assert _row(rows, "ready")["tag"] == "to do"
    assert _row(rows, "ready/G0")["tag"] == "done"
    assert _reads(rows, "gates/G0") == ("done", [])


def test_sc1_1_a_closed_features_verdict_counts_as_it_reads(tmp_path, capsys):
    root = _repo(tmp_path, ["ready", "short"])
    code, _, _ = _call(["progress", "done", "short", "--root", str(root)], capsys)
    assert code == 0
    rows = _tree(root, capsys)
    # The close governs only its own feature's roll-up.
    assert _row(rows, "short")["tag"] == "done"
    assert _row(rows, "short/G0")["tag"] == "failed"
    assert _reads(rows, "gates/G0") == ("failed", ["short holds G0 at failed"])
    assert _reads(rows, "gates/G0/G0.1") == ("failed", ["short holds G0.1 at failed"])
    assert _reads(rows, "gates/G0/G0.2") == ("done", [])


def test_sc1_1_an_inactive_verdict_at_the_next_gate_never_counts(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "ready"])
    _finding(root, "f-next", "G1")  # shows gates/G1, each feature's inactive next gate
    rows = _tree(root, capsys)
    assert "inactive" in _row(rows, "drafted/G1")["line"]
    assert "inactive" in _row(rows, "gates/G1")["line"]
    assert _reads(rows, "gates/G1") == ("to do", [])
    for condition in ("G1.1", "G1.2", "G1.3"):
        assert _reads(rows, f"gates/G1/{condition}") == ("to do", [])
    # The active gate in the same tree counts the same features.
    assert _reads(rows, "gates/G0") == ("doing", ["drafted holds G0 at to do"])


def test_sc1_1_an_inactive_g0_verdict_leaves_gates_g0_at_to_do(tmp_path, capsys):
    # With no gate active, each feature's G0 verdict is its inactive next gate.
    idle = _repo(tmp_path, ["drafted", "ready"], gates=(), name="idle")
    _finding(idle, "f-intake", "G0")
    rows = _tree(idle, capsys)
    assert "inactive" in _row(rows, "ready/G0")["line"]
    assert "inactive" in _row(rows, "gates/G0")["line"]
    assert _reads(rows, "gates/G0") == ("to do", [])
    for condition in ("G0.1", "G0.2", "G0.3"):
        assert _reads(rows, f"gates/G0/{condition}") == ("to do", [])
    # The same features with G0 active count at gates/G0.
    live = _repo(tmp_path, ["drafted", "ready"], gates=("G0",), name="live")
    _finding(live, "f-intake", "G0")
    rows = _tree(live, capsys)
    assert _reads(rows, "gates/G0") == ("doing", ["drafted holds G0 at to do"])


def test_sc1_1_a_gate_named_only_by_a_finding_reads_to_do(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "ready"])
    _finding(root, "f-later", "G3")  # no feature shows a verdict at G3
    rows = _tree(root, capsys)
    assert not any(row["id"].endswith("/G3") for row in rows if not row["id"].startswith("gates/"))
    assert _reads(rows, "gates/G3") == ("to do", [])
    for condition in ("G3.1", "G3.2", "G3.3"):
        assert _reads(rows, f"gates/G3/{condition}") == ("to do", [])
    assert _reads(rows, "gates/G0") == ("doing", ["drafted holds G0 at to do"])


def test_sc1_1_a_gate_in_a_repo_with_no_contract_reads_to_do(tmp_path, capsys):
    empty = _repo(tmp_path, [], name="empty")
    rows, out, _ = _print(empty, capsys)
    assert _features(rows) == []
    assert _reads(rows, "gates/G0") == ("to do", [])
    for condition in ("G0.1", "G0.2", "G0.3"):
        assert _reads(rows, f"gates/G0/{condition}") == ("to do", [])
    assert not any(DIAGNOSTIC.match(text) for text in out.splitlines())
    # Once a done feature shows, the same gate reads its verdict.
    rows = _tree(_repo(tmp_path, ["ready"], name="one"), capsys)
    assert _reads(rows, "gates/G0") == ("done", [])


def test_sc1_1_every_active_gate_counts_its_verdicts(tmp_path, capsys):
    rows = _tree(_repo(tmp_path, ["drafted", "ready"], gates=("G0", "G1")), capsys)
    assert _reads(rows, "gates/G0") == ("doing", ["drafted holds G0 at to do"])
    # G1's verdicts, active now, read `to do`: the kit computes none yet.
    assert _reads(rows, "gates/G1") == (
        "to do", ["drafted holds G1 at to do", "ready holds G1 at to do"])
    for condition in ("G1.1", "G1.2", "G1.3"):
        assert _reads(rows, f"gates/G1/{condition}") == (
            "to do", [f"drafted holds {condition} at to do",
                      f"ready holds {condition} at to do"])


# --- SC1.2: each condition rolls up, and names what holds it --------------------

# Each case: the contracts in the repo, then what G0.1, G0.2 and G0.3 read,
# each with the features it names.
CONDITION_CASES = {
    "every-verdict-done": (("ready", "sealed"), [
        ("done", []), ("done", []), ("done", [])]),
    "every-reading-to-do": (("drafted",), [
        ("done", []), ("to do", ["drafted holds G0.2 at to do"]), ("done", [])]),
    "done-and-to-do": (("drafted", "unconfirmed"), [
        ("done", []), ("doing", ["drafted holds G0.2 at to do"]),
        ("doing", ["unconfirmed holds G0.3 at to do"])]),
    "blocked-first": (("parked", "ready"), [
        ("blocked", ["parked holds G0.1 at blocked"]), ("done", []), ("done", [])]),
    "every-reading": (("drafted", "parked", "ready", "short", "unconfirmed"), [
        ("failed", ["parked holds G0.1 at blocked", "short holds G0.1 at failed"]),
        ("doing", ["drafted holds G0.2 at to do"]),
        ("doing", ["unconfirmed holds G0.3 at to do"])]),
}


@pytest.mark.parametrize("case", list(CONDITION_CASES))
def test_sc1_2_each_condition_reads_the_roll_up_of_that_condition(tmp_path, capsys, case):
    cids, expected = CONDITION_CASES[case]
    rows = _tree(_repo(tmp_path, cids), capsys)
    assert [_reads(rows, f"gates/G0/{c}") for c in ("G0.1", "G0.2", "G0.3")] == expected


def test_sc1_2_the_gate_block_prints_as_usage_shows_it(tmp_path, capsys):
    _, out, _ = _print(_repo(tmp_path, ["apply-discount", "ship-rates"]), capsys)
    assert _block(out, "gates/G0") == (
        "gates/G0 Planning / Intake [doing]\n"
        "  - apply-discount holds G0 at to do\n"
        "  gates/G0/G0.1 Definition-of-ready [done]\n"
        "  gates/G0/G0.2 Vocabulary coverage [doing]\n"
        "    - apply-discount holds G0.2 at to do\n"
        "  gates/G0/G0.3 Unit confirmation [done]\n")


def test_sc1_2_holds_lines_follow_the_trees_order_of_features(tmp_path, capsys):
    # Written in reverse; the tree lists the features in the order of specs/.
    rows = _tree(_repo(tmp_path, ["unconfirmed", "short", "drafted"]), capsys)
    features = _features(rows)
    assert features == ["drafted", "short", "unconfirmed"]
    assert _reads(rows, "gates/G0") == ("failed", [
        "drafted holds G0 at to do", "short holds G0 at failed",
        "unconfirmed holds G0 at to do"])


def test_sc1_2_the_whole_print_puts_holds_lines_before_conditions(tmp_path, capsys):
    _, out, _ = _print(_repo(tmp_path, ["drafted", "parked", "ready", "short",
                                        "unconfirmed"]), capsys)
    assert _block(out, "gates/G0") == (
        "gates/G0 Planning / Intake [failed]\n"
        "  - drafted holds G0 at to do\n"
        "  - parked holds G0 at blocked\n"
        "  - short holds G0 at failed\n"
        "  - unconfirmed holds G0 at to do\n"
        "  gates/G0/G0.1 Definition-of-ready [failed]\n"
        "    - parked holds G0.1 at blocked\n"
        "    - short holds G0.1 at failed\n"
        "  gates/G0/G0.2 Vocabulary coverage [doing]\n"
        "    - drafted holds G0.2 at to do\n"
        "  gates/G0/G0.3 Unit confirmation [doing]\n"
        "    - unconfirmed holds G0.3 at to do\n")


def test_sc1_2_an_unreadable_contract_holds_by_its_folder_id(tmp_path, capsys):
    root = _repo(tmp_path, ["ready"])
    broken = root / "specs" / "broken" / "contract.yaml"
    broken.parent.mkdir(parents=True)
    broken.write_text("- a list\n", encoding="utf-8")
    rows, _, err = _print(root, capsys)
    assert "taskcontract tree: unreadable contract: specs/broken/contract.yaml (not a mapping)" in err
    assert _reads(rows, "gates/G0") == ("failed", ["broken holds G0 at failed"])
    assert [_reads(rows, f"gates/G0/{c}") for c in ("G0.1", "G0.2", "G0.3")] == [
        ("failed", ["broken holds G0.1 at failed"]),
        ("doing", ["broken holds G0.2 at to do"]),
        ("doing", ["broken holds G0.3 at to do"])]


def test_sc1_2_the_query_prints_a_gates_and_a_conditions_roll_up_without_holds(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "ready"])
    assert _call(["tree", "gates/G0", "--root", str(root)], capsys) == (
        0, f"gates/G0 Planning / Intake [doing]\npage: {G0_PAGE}\n", "")
    assert _call(["tree", "gates/G0/G0.2", "--root", str(root)], capsys) == (
        0, f"gates/G0/G0.2 Vocabulary coverage [doing]\npage: {G0_PAGE}\n", "")
    assert _call(["tree", "gates/G0/G0.1", "--root", str(root)], capsys) == (
        0, f"gates/G0/G0.1 Definition-of-ready [done]\npage: {G0_PAGE}\n", "")


# --- SC1.3: a finding counts in no roll-up ----------------------------------------

def test_sc1_3_a_finding_stands_once_shows_its_kind_and_counts_in_no_roll_up(tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "ready"])
    before = _tree(root, capsys)
    ids = ["gates/G0", "gates/G0/G0.1", "gates/G0/G0.2", "gates/G0/G0.3"]
    _finding(root, "f-done", "G0.1")  # under a condition that reads done
    _finding(root, "f-cond", "G0.2")  # under a condition that does not
    _finding(root, "f-gate", "G0")    # under the gate itself
    rows, out, _ = _print(root, capsys)
    assert [_reads(rows, rid) for rid in ids] == [_reads(before, rid) for rid in ids]
    assert _block(out, "gates/G0") == (
        "gates/G0 Planning / Intake [doing]\n"
        "  - drafted holds G0 at to do\n"
        "  gates/G0/G0.1 Definition-of-ready [done]\n"
        f"    gates/G0/G0.1/f-done {STATEMENT} [kind: gap] gate: G0.1\n"
        "  gates/G0/G0.2 Vocabulary coverage [doing]\n"
        "    - drafted holds G0.2 at to do\n"
        f"    gates/G0/G0.2/f-cond {STATEMENT} [kind: gap] gate: G0.2\n"
        "  gates/G0/G0.3 Unit confirmation [done]\n"
        f"  gates/G0/f-gate {STATEMENT} [kind: gap] gate: G0\n")
    for slug in ("f-done", "f-cond", "f-gate"):
        assert sum(row["id"].endswith("/" + slug) for row in rows) == 1


# --- Constraint 2: every other line stays byte for byte --------------------------

FEATURE_LINES = """\
{cid} (no title) [to do] no feature document | {intent}
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


def test_constraint_only_gate_items_and_their_conditions_change_in_the_whole_print(
        tmp_path, capsys):
    root = _repo(tmp_path, ["drafted", "ready"])
    _finding(root, "f-cond", "G0.2")
    _finding(root, "f-gate", "G0")
    _finding(root, "f-later", "G3")
    _finding(root, "f-loose", None)
    _, out, err = _print(root, capsys)
    assert err == ""
    assert out == (
        "gates/G0 Planning / Intake [doing]\n"
        "  - drafted holds G0 at to do\n"
        "  gates/G0/G0.1 Definition-of-ready [done]\n"
        "  gates/G0/G0.2 Vocabulary coverage [doing]\n"
        "    - drafted holds G0.2 at to do\n"
        f"    gates/G0/G0.2/f-cond {STATEMENT} [kind: gap] gate: G0.2\n"
        "  gates/G0/G0.3 Unit confirmation [done]\n"
        f"  gates/G0/f-gate {STATEMENT} [kind: gap] gate: G0\n"
        "gates/G3 Implementation [to do] inactive\n"
        "  gates/G3/G3.1 Formatter [to do]\n"
        "  gates/G3/G3.2 Analyzer battery [to do]\n"
        "  gates/G3/G3.3 Strict compile [to do]\n"
        f"  gates/G3/f-later {STATEMENT} [kind: gap] gate: G3\n"
        "gates/none [to do]\n"
        f"  gates/none/f-loose {STATEMENT} [kind: gap]\n"
        + FEATURE_LINES.format(cid="drafted", intent=INTENT, verdict="to do", g02="to do",
                               g02_lines=f"      - {MSG_DRAFT_TERM}\n")
        + FEATURE_LINES.format(cid="ready", intent=INTENT, verdict="done", g02="done",
                               g02_lines=""))
