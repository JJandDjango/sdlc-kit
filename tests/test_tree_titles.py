"""The titles suite (contract project-tree, unit o2-titles).

Each item line opens on its id and its plain name, the words that say what
the item is, then the parts `tree: pane: parts:` selects, in their fixed
order (SC1.1). The plain name is a gate's and a verdict's gate name in
`taskcontract/data/gates.yaml`, a condition's name there, a task's name in
`taskcontract/data/tasks.yaml`, a feature's contract `title` (else the
literal `(no title)`), a unit's `done_means`, a check's sketch line and a
finding's `statement`, each by the text rule: its ends stripped, each line
break one space. An item whose source gives no text shows no plain name and
reads as before but for that; only a feature shows `(no title)` in its
place. The `summary` part, after ` | `, holds only a feature's intent, and
`taskcontract tree <id>` prints its `summary:` line only for a feature.
`parts:` never leaves out the plain name, as it never leaves out the id.
The pane's item lines open the same way, the last segment of the id under
another item; its waiting line, where-am-I line and fold lines keep ids
alone.

The contract schema (1.5.0) takes an optional top-level `title`: a string
of one line that holds more than blanks. A blank title or one holding a
line break fails the draft profile with TC002. The tree reads the title
from the contract only, never from the feature document, and the intake
flow copies it from the feature document's title line.

Each test drives the CLI in process against a fixture repo under tmp_path,
outside any git repository, so a verdict's evidence reads `at no commit`;
the kit test prints the kit's own tree.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import pytest
import yaml

import taskcontract
from conftest import write_seat_roster
from taskcontract import checker, tree_view
from taskcontract.__main__ import main

# The kit whose package runs: its specs, its lists, its flows.
KIT = Path(taskcontract.__file__).resolve().parent.parent
DATA = KIT / "taskcontract" / "data"
FLOW = KIT / "skills" / "sdlc" / "flows" / "intake.md"

CLEAR = "\x1b[H\x1b[2J"
NO_TITLE = "(no title)"
TITLE = "Apply one discount code per order"
INTENT = ("A fixture contract for the titles suite; each of its items opens on "
          "its id and its plain name.")
BETA_INTENT = "A second fixture contract, which carries no title."
PIN = "The stale-pin finding, in its own words."
LOOP = "The slow-loop finding, in its own words."
IDEA = "The idea finding, in its own words."
TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]
TASK_NAMES = ["Approve the test list", "Write the tests", "Prove red", "Green",
              "Approve the commit", "Commit", "Two-Key PASS"]
EVIDENCE = ("via python -m taskcontract validate specs/alpha/contract.yaml "
            "--profile ready at no commit")
PARTS_IGNORED = ("taskcontract tree: pane parts ignored: shade - give a list from "
                 "id, status, marks, evidence, links, doc, summary")

# The schema's `title` pattern, as the TC002 message quotes it: one line
# (no CR, no LF, anywhere, a trailing one too) holding a non-blank character.
TITLE_PATTERN = r"^[^\r\n]*\S[^\r\n]*(?![\s\S])"

# The flow's words for the title (step I4 of skills/sdlc/flows/intake.md).
TITLE_RULE = ("When the request is a feature document, WRITE `title:` from its title "
              "line `# {id} - {title}`: the words after `{id} - `, or the whole "
              "heading text when the heading opens on anything else.")
CHAR_CEILING = 12_000  # the flow's PromptLang budget, as tests/test_intake_flow.py holds it

ALPHA = f"""\
# alpha: the titles suite's fixture contract, written by hand so that each
# unit and each sketch starts on a line the tests can name.
id: alpha
title: {TITLE}
intent: >
  A fixture contract for the titles suite; each of its items opens on
  its id and its plain name.
scope: [src/]
non_goals: [No other work]
dependencies: []
entities: []
provenance: {{origin: human-request}}
decomposition:
  - unit: work for a1-core
    id: a1-core
    confirmed_by: [user]
    done_means: the work for a1-core is done
    acceptance_sketch:
      - verify the core prints (SC1.1)
  - unit: work for a2-edges
    id: a2-edges
    depends_on: [a1-core]
    confirmed_by: [user]
    done_means: >
      the work for a2-edges
      is done
    acceptance_sketch:
      - verify an edge holds
"""

BETA = {
    "id": "beta", "intent": BETA_INTENT, "scope": ["src/"], "non_goals": ["No other work"],
    "decomposition": [{"unit": "work for b1-solo", "id": "b1-solo", "confirmed_by": ["user"],
                       "done_means": "the work for b1-solo is done",
                       "acceptance_sketch": ["verify the price rounds (by the house rule)"]}],
    "dependencies": [], "entities": [], "provenance": {"origin": "human-request"},
}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, find no git repo above the
    fixture, and give the pane a wide terminal."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


# --- the fixture repository ---------------------------------------------------------

def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _config(root, gates=("G0",), **more):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates), **more})


def _finding(root, slug, gate, kind, statement):
    doc = {"finding": slug, "date": "2026-09-25", "kit_pinned": "v0.15.0",
           "diagnostic": "none", "kind": kind, "count": 1, "proposal": "none"}
    if gate is not None:
        doc["gate"] = gate
    if statement is not None:
        doc["statement"] = statement
    _dump(root / ".sdlc" / "findings" / f"{slug}.yaml", doc)


def _repo(tmp_path, alpha=ALPHA):
    """G0 active; alpha (titled, ready-green, with a feature doc) and beta
    (no title); a finding under G0, one under G3.1 (G3 not active) and one
    under gates/none."""
    root = tmp_path / "repo"
    _config(root)
    write_seat_roster(root)
    _write(root / "specs" / "alpha" / "contract.yaml", alpha)
    _dump(root / "specs" / "beta" / "contract.yaml", BETA)
    _write(root / "docs" / "features" / "alpha.md", "# alpha - Apply one discount code per order\n")
    _finding(root, "stale-pin", "G0", "gap", PIN)
    _finding(root, "slow-loop", "G3.1", "friction", LOOP)
    _finding(root, "idea", "none", "proposal", IDEA)
    return root


def _progress(root, cid, *records):
    _dump(root / ".sdlc" / "progress" / f"{cid}.yaml", {"records": list(records)})


def _doing(item):
    return {"item": item, "state": "doing", "at": "2026-09-25T10:00:00Z", "head": "1a2b3c4"}


def _line_of(text, entry):
    """The 1-based line of `text` that is exactly `entry`, found once."""
    lines = text.splitlines()
    assert lines.count(entry) == 1, entry
    return lines.index(entry) + 1


def _pages(name):
    doc = yaml.safe_load((DATA / f"{name}.yaml").read_text(encoding="utf-8"))
    return {entry["id"]: entry["page"] for entry in doc[name]}


def _text(value):
    """The text rule: ends stripped, each line break one space; None when
    the value is not text or is blank."""
    if not isinstance(value, str):
        return None
    return " ".join(value.strip().splitlines()) or None


# --- driving the CLI ------------------------------------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _lines(root, capsys):
    """The whole tree's stdout lines; the print exits 0."""
    code, out, _ = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    return out.splitlines()


def _query(root, capsys, node):
    return _call(["tree", node, "--root", str(root)], capsys)


def _starting(lines, opening):
    """The one line that opens on `opening`."""
    found = [text for text in lines if text.startswith(opening)]
    assert len(found) == 1, (opening, found)
    return found[0]


class _Interrupt:
    """The pane's injected sleep: it ends the loop at its first call."""

    def __call__(self, seconds):
        raise KeyboardInterrupt


def _pane(root, capsys):
    """(lines, stderr) of one pane render."""
    out = io.StringIO()
    assert tree_view.follow(Path(root), out, sleep=_Interrupt()) == 0
    text = out.getvalue()
    assert text.startswith(CLEAR)
    return text[len(CLEAR):].splitlines(), capsys.readouterr().err


def _prove_red(root):
    """The current task alpha/a2-edges/prove-red, doing, not an approval."""
    _progress(root, "alpha", _doing("alpha/a2-edges/prove-red"))


# --- SC1.1 on the kit's own print: every contract a feature, every line id first -----

def _depth(text):
    return (len(text) - len(text.lstrip(" "))) // 2


def _under(lines, at):
    """The indexes of the lines one level under the line at `at`."""
    depth, found = _depth(lines[at]), []
    for n in range(at + 1, len(lines)):
        if _depth(lines[n]) <= depth:
            break
        if _depth(lines[n]) == depth + 1:
            found.append(n)
    return found


def test_sc1_1_every_kit_contract_stands_as_a_feature_and_each_line_opens_on_its_id_and_plain_name(
        capsys):
    lines = _lines(KIT, capsys)
    contracts = sorted(KIT.glob("specs/*/contract.yaml"), key=lambda p: p.parent.name)
    assert contracts
    tops = [text for text in lines if not text.startswith(" ")]
    assert [text.split(" ", 1)[0] for text in tops if not text.startswith("gates/")] == [
        path.parent.name for path in contracts]
    assert _starting(tops, "gates/G0 ").startswith("gates/G0 Planning / Intake [")
    for path in contracts:
        cid = path.parent.name
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        doc = doc if isinstance(doc, dict) else {}
        at = lines.index(_starting(tops, f"{cid} "))
        assert lines[at].startswith(f"{cid} {_text(doc.get('title')) or NO_TITLE} ["), lines[at]
        units = {unit["id"]: unit for unit in reversed(doc.get("decomposition") or [])
                 if isinstance(unit, dict) and isinstance(unit.get("id"), str)}
        for n in _under(lines, at):
            rid = lines[n].strip().split(" ", 1)[0]
            uid = rid.split("/", 1)[1]
            if uid in units and not re.fullmatch(r"(?:G\d+|PL-[A-Z]+)", uid):
                unit = units[uid]
                name = _text(unit.get("done_means"))
                assert lines[n].strip().startswith(f"{rid} {name} [" if name else f"{rid} ["), \
                    lines[n]
                children = _under(lines, n)
                for task, key, title in zip(children, TASK_KEYS, TASK_NAMES):
                    assert lines[task].strip().startswith(f"{rid}/{key} {title} ["), lines[task]
                sketches = unit.get("acceptance_sketch") or []
                for check, sketch in zip(children[len(TASK_KEYS):], sketches):
                    head, _, rest = lines[check].strip().partition(" ")
                    assert head.startswith(f"{rid}/"), lines[check]
                    assert rest.startswith(f"{_text(sketch)} ["), lines[check]


# --- SC1.1 each item kind, on a fixture print -------------------------------------------

def test_sc1_1_a_gate_a_condition_and_a_finding_open_on_their_id_and_plain_name(
        tmp_path, capsys):
    lines = _lines(_repo(tmp_path), capsys)
    for text in (
            "gates/G0 Planning / Intake [to do]",
            "  gates/G0/G0.1 Definition-of-ready [to do]",
            "  gates/G0/G0.2 Vocabulary coverage [to do]",
            "  gates/G0/G0.3 Unit confirmation [to do]",
            f"  gates/G0/stale-pin {PIN} [kind: gap] gate: G0",
            # a gate a finding names, not active: its gate name, then its mark
            "gates/G3 Implementation [to do] inactive",
            "  gates/G3/G3.1 Formatter [to do]",
            f"    gates/G3/G3.1/slow-loop {LOOP} [kind: friction] gate: G3.1",
            f"  gates/none/idea {IDEA} [kind: proposal]"):
        assert text in lines, text
    assert not any(" | " in text for text in lines if text.lstrip().startswith("gates/"))


def test_sc1_1_a_verdict_its_conditions_units_tasks_and_checks_open_on_their_id_and_plain_name(
        tmp_path, capsys):
    lines = _lines(_repo(tmp_path), capsys)
    for text in (
            f"  alpha/G0 Planning / Intake [done] {EVIDENCE}",
            "    alpha/G0/G0.1 Definition-of-ready [done]",
            "    alpha/G0/G0.2 Vocabulary coverage [done]",
            "    alpha/G0/G0.3 Unit confirmation [done]",
            "  alpha/G1 Requirements / Spec [to do] inactive",
            "    alpha/G1/G1.1 Spec/schema linting [to do]",
            "  alpha/a1-core the work for a1-core is done [to do]",
            # a folded done_means, by the text rule, before the links
            "  alpha/a2-edges the work for a2-edges is done [to do] depends_on: alpha/a1-core",
            *(f"    alpha/a1-core/{key} {name} [to do]" for key, name in zip(TASK_KEYS, TASK_NAMES)),
            "    alpha/a1-core/SC1.1 verify the core prints (SC1.1) [to do]",
            "    alpha/a2-edges/sketch-1 verify an edge holds [to do]",
            "  beta/b1-solo the work for b1-solo is done [to do]",
            "    beta/b1-solo/sketch-1 verify the price rounds (by the house rule) [to do]"):
        assert text in lines, text
    # the ` | ` part now belongs to a feature alone
    assert [text.split(" ", 1)[0] for text in lines if " | " in text] == ["alpha", "beta"]


def test_sc1_1_a_feature_opens_on_its_id_and_its_title_and_keeps_its_intent_last(
        tmp_path, capsys):
    lines = _lines(_repo(tmp_path), capsys)
    alpha = _starting(lines, "alpha ")
    assert alpha.startswith(f"alpha {TITLE} [to do]"), alpha
    assert alpha.endswith(f" doc: docs/features/alpha.md | {INTENT}"), alpha


def test_sc1_1_a_feature_without_a_title_shows_no_title_in_its_place(tmp_path, capsys):
    root = _repo(tmp_path)
    blank = {**BETA, "id": "gamma", "title": "   "}  # a blank title gives no text
    _dump(root / "specs" / "gamma" / "contract.yaml", blank)
    _dump(root / "specs" / "delta" / "contract.yaml", {**BETA, "id": "delta", "title": 42})
    _write(root / "specs" / "broken" / "contract.yaml", "id: [unclosed\n")
    lines = _lines(root, capsys)
    beta = _starting(lines, "beta ")
    assert beta.startswith(f"beta {NO_TITLE} [to do]"), beta
    assert beta.endswith(f" | {BETA_INTENT}"), beta
    for cid in ("gamma", "delta"):  # the schema fails them; the tree still names them
        assert _starting(lines, f"{cid} ").startswith(f"{cid} {NO_TITLE} [failed]"), cid
    # a contract the tree cannot read is still a feature, with no title
    assert _starting(lines, "broken ").startswith(f"broken {NO_TITLE} [failed]")


def test_sc1_1_a_title_prints_by_the_text_rule(tmp_path, capsys):
    root = _repo(tmp_path, alpha=ALPHA.replace(
        f"title: {TITLE}\n", '"title": "  Apply one discount code\\nper order  "\n'))
    alpha = _starting(_lines(root, capsys), "alpha ")
    assert alpha.startswith("alpha Apply one discount code per order [failed]"), alpha


def test_sc1_1_the_tree_reads_the_title_from_the_contract_never_the_feature_document(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _write(root / "docs" / "features" / "beta.md", "# beta - A title only the document holds\n")
    code, out, _ = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    beta = _starting(out.splitlines(), "beta ")
    assert beta.startswith(f"beta {NO_TITLE} [to do]"), beta
    assert "A title only the document holds" not in out


def test_sc1_1_an_item_whose_source_gives_no_text_shows_no_plain_name(tmp_path, capsys):
    root = _repo(tmp_path, alpha=ALPHA + (
        "  - unit: work with no done_means\n"
        "    id: a3-bare\n"
        "    confirmed_by: [user]\n"
        "    acceptance_sketch:\n"
        "      - {verify: a mapping, not a line}\n"))
    _config(root, ["G0", "X1"])  # X1: a gate the kit's list lacks
    _finding(root, "stale-pin", "G0", "gap", None)  # a finding without a statement
    lines = _lines(root, capsys)
    for text in (
            "gates/none [to do]",                      # no source names it
            "gates/X1 [to do]",                        # the kit's list lacks it
            "  alpha/X1 [to do]",                      # a verdict at that gate
            "  alpha/a3-bare [to do]",                 # no done_means (the schema fails it)
            "    alpha/a3-bare/sketch-1 [to do]",      # a sketch that is no line
            "  gates/G0/stale-pin [kind: gap] gate: G0"):
        assert text in lines, text
    # beside them, the items whose source gives text show it
    for text in ("gates/G0 Planning / Intake [to do]",
                 "  alpha/G1 Requirements / Spec [to do] inactive",
                 "    alpha/a3-bare/approve-tests Approve the test list [to do]"):
        assert text in lines, text


# --- SC1.1 a condition reads a bad title's TC002 under G0.1 -------------------------------

def test_sc1_1_a_blank_title_fails_g0_1_with_the_schemas_message(tmp_path, capsys):
    root = _repo(tmp_path, alpha=ALPHA.replace(f"title: {TITLE}\n", 'title: "   "\n'))
    lines = _lines(root, capsys)
    assert "    alpha/G0/G0.1 Definition-of-ready [failed]" in lines
    at = lines.index("    alpha/G0/G0.1 Definition-of-ready [failed]")
    assert lines[at + 1] == f"      - {'   '!r} does not match {TITLE_PATTERN!r}"
    assert "    alpha/G0/G0.2 Vocabulary coverage [done]" in lines
    assert _starting(lines, "alpha ").startswith(f"alpha {NO_TITLE} [failed]")


# --- SC1.1 the query: its first line carries the plain name; summary: a feature's only ---

def test_sc1_1_the_querys_first_line_opens_on_the_id_and_the_plain_name(tmp_path, capsys):
    root = _repo(tmp_path)
    gates, tasks = _pages("gates"), _pages("tasks")
    a1 = _line_of(ALPHA, "  - unit: work for a1-core")
    sketch = _line_of(ALPHA, "      - verify the core prints (SC1.1)")
    expected = {
        "alpha/a1-core": ("alpha/a1-core the work for a1-core is done [to do]\n"
                          f"file: specs/alpha/contract.yaml:{a1}\n"),
        "alpha/a1-core/SC1.1": ("alpha/a1-core/SC1.1 verify the core prints (SC1.1) [to do]\n"
                                f"file: specs/alpha/contract.yaml:{sketch}\n"),
        "alpha/a1-core/approve-tests": ("alpha/a1-core/approve-tests Approve the test list [to do]\n"
                                        f"page: {tasks['approve-tests']}\n"),
        "alpha/G0": (f"alpha/G0 Planning / Intake [done] {EVIDENCE}\n"
                     "file: specs/alpha/contract.yaml:1\n"
                     f"page: {gates['G0']}\n"),
        "alpha/G0/G0.2": ("alpha/G0/G0.2 Vocabulary coverage [done]\n"
                          f"page: {gates['G0']}\n"),
        "gates/G3": ("gates/G3 Implementation [to do] inactive\n"
                     f"page: {gates['G3']}\n"),
        "gates/G3/G3.1/slow-loop": (f"gates/G3/G3.1/slow-loop {LOOP} [kind: friction]\n"
                                    "gate: G3.1\n"
                                    "file: .sdlc/findings/slow-loop.yaml:1\n"),
        "gates/none": "gates/none [to do]\n",
    }
    for node, block in expected.items():
        assert _query(root, capsys, node) == (0, block, ""), node


def test_sc1_1_the_query_prints_summary_only_for_a_feature_its_intent(tmp_path, capsys):
    root = _repo(tmp_path)
    code, out, err = _query(root, capsys, "alpha")
    assert (code, err) == (0, "")
    lines = out.splitlines()
    assert lines[0].startswith(f"alpha {TITLE} [to do]"), lines[0]
    assert lines[1:] == [f"summary: {INTENT}", "doc: docs/features/alpha.md:1",
                         "file: specs/alpha/contract.yaml:1"]
    code, out, err = _query(root, capsys, "beta")
    assert (code, err) == (0, "")
    lines = out.splitlines()
    assert lines[0].startswith(f"beta {NO_TITLE} [to do]"), lines[0]
    assert lines[1:] == [f"summary: {BETA_INTENT}", "file: specs/beta/contract.yaml:1"]


# --- SC1.1 the pane: its item lines open on the short id and the plain name --------------

def test_sc1_1_the_panes_item_lines_open_on_the_short_id_then_the_plain_name(tmp_path, capsys):
    root = _repo(tmp_path)
    _prove_red(root)
    lines, err = _pane(root, capsys)
    assert err == ""
    assert lines[0] == "specs/alpha/contract.yaml > alpha > a2-edges > prove-red"
    assert lines[1] == "4 more: 4 to do"         # gates/G0, gates/G3, gates/none, beta
    assert lines[2].startswith(f"alpha {TITLE} [doing]"), lines[2]  # the top level: its full id
    assert lines[2].endswith(f" doc: docs/features/alpha.md | {INTENT}"), lines[2]
    assert lines[3:] == [
        "  3 more: 2 to do, 1 done",              # alpha/G0 done, alpha/G1, a1-core
        "  a2-edges the work for a2-edges is done [doing] depends_on: alpha/a1-core",
        "    7 more: 7 to do",
        "    prove-red Prove red [doing] current"]


def test_sc1_1_the_panes_fold_names_keep_ids_alone(tmp_path, capsys):
    root = _repo(tmp_path)
    _prove_red(root)
    _config(root, tree={"pane": {"fold": "names"}})
    lines, err = _pane(root, capsys)
    assert err == ""
    assert lines[1] == "4 more: gates/G0 [to do], gates/G3 [to do], gates/none [to do], beta [to do]"
    assert lines[3] == "  3 more: G0 [done], G1 [to do], a1-core [to do]"
    assert lines[5] == ("    7 more: approve-tests [to do], write-tests [to do], green [to do], "
                        "approve-commit [to do], commit [to do], two-key [to do], sketch-1 [to do]")
    assert lines[6] == "    prove-red Prove red [doing] current"


def test_sc1_1_at_an_approval_the_waiting_and_where_lines_keep_ids_alone(tmp_path, capsys):
    root = _repo(tmp_path)
    _progress(root, "alpha", _doing("alpha/a1-core/approve-tests"))
    lines, _ = _pane(root, capsys)
    assert lines[:2] == ["waiting on a seat: approve-tests for alpha/a1-core",
                         "specs/alpha/contract.yaml > alpha > a1-core > approve-tests"]
    assert lines[5] == "  a1-core the work for a1-core is done [waiting on a seat]"
    assert lines[-1].startswith(
        "    approve-tests Approve the test list [waiting on a seat] current"), lines[-1]


# --- SC1.1 `parts:` selects after the id and the plain name (existing behavior 8) --------

def test_sc1_1_parts_empty_shows_the_id_and_the_plain_name(tmp_path, capsys):
    root = _repo(tmp_path)
    _prove_red(root)
    _config(root, tree={"pane": {"parts": []}})
    lines, err = _pane(root, capsys)
    assert err == ""
    assert [lines[2], lines[4], lines[6]] == [
        f"alpha {TITLE}",
        "  a2-edges the work for a2-edges is done",
        "    prove-red Prove red"]
    assert lines[1] == "4 more: 4 to do"  # a fold line keeps its counts


@pytest.mark.parametrize("parts, render", [
    pytest.param(["summary", "status"],
                 (f"alpha {TITLE} [doing] | {INTENT}",
                  "  a2-edges the work for a2-edges is done [doing]",
                  "    prove-red Prove red [doing]"), id="summary-status"),
    pytest.param(["links", "id", "marks"],
                 (f"alpha {TITLE}",
                  "  a2-edges the work for a2-edges is done depends_on: alpha/a1-core",
                  "    prove-red Prove red current"), id="links-id-marks"),
    pytest.param(["doc", "evidence", "status"],
                 (f"alpha {TITLE} [doing] doc: docs/features/alpha.md",
                  "  a2-edges the work for a2-edges is done [doing]",
                  "    prove-red Prove red [doing]"), id="doc-evidence-status"),
])
def test_sc1_1_a_parts_list_selects_the_parts_after_the_plain_name_in_the_fixed_order(
        tmp_path, capsys, parts, render):
    root = _repo(tmp_path)
    _prove_red(root)
    _config(root, tree={"pane": {"parts": parts}})
    lines, err = _pane(root, capsys)
    assert err == ""
    assert (lines[2], lines[4], lines[6]) == render


def test_sc1_1_a_bad_parts_prints_its_line_on_stderr_and_each_line_opens_on_id_and_plain_name(
        tmp_path, capsys):
    root = _repo(tmp_path)
    _prove_red(root)
    _config(root, tree={"pane": {"parts": ["status", "shade"]}})
    lines, err = _pane(root, capsys)
    assert err.splitlines() == [PARTS_IGNORED]
    assert lines[4:] == [  # ignored as a whole: every part shows
        "  a2-edges the work for a2-edges is done [doing] depends_on: alpha/a1-core",
        "    7 more: 7 to do",
        "    prove-red Prove red [doing] current"]


# --- the contract schema: an optional one-line title, version 1.5.0 ----------------------

def _contract_file(tmp_path, **fields):
    doc = {**BETA, **fields}
    path = tmp_path / "loose" / "contract.yaml"
    _dump(path, doc)
    return path


def _found(path, profile):
    return [(v.path, v.rule, v.message)
            for v in checker.validate_path(path, profile=profile) if v.severity == "error"]


def test_the_schema_takes_an_optional_one_line_title_at_version_1_5_0(tmp_path):
    schema = checker.load_schema()
    assert schema["version"] == "1.5.0"
    assert schema["properties"]["title"] == {"type": "string", "pattern": TITLE_PATTERN}
    assert "title" not in schema["required"]
    for title in (TITLE, "  A title with blanks around it  ", "x"):
        path = _contract_file(tmp_path, title=title)
        assert (_found(path, "draft"), _found(path, "ready")) == ([], []), title
    path = _contract_file(tmp_path)  # no title: as before, at both profiles
    assert (_found(path, "draft"), _found(path, "ready")) == ([], [])


@pytest.mark.parametrize("title", [
    pytest.param("", id="empty"),
    pytest.param("   ", id="blank"),
    pytest.param("\t \n", id="blank-lines"),
    pytest.param("Apply one discount\ncode per order", id="line-feed"),
    pytest.param("Apply one discount\r\ncode per order", id="crlf"),
    pytest.param("Apply one discount\rcode per order", id="carriage-return"),
    pytest.param("Apply one discount code per order\n", id="trailing-line-feed"),
])
def test_a_blank_title_or_one_holding_a_line_break_fails_the_draft_profile_with_tc002(
        tmp_path, title):
    path = _contract_file(tmp_path, title=title)
    wanted = [("$.title", "TC002", f"{title!r} does not match {TITLE_PATTERN!r}")]
    assert _found(path, "draft") == wanted
    assert _found(path, "ready") == wanted


def test_a_title_that_is_not_a_string_fails_the_draft_profile_with_tc002(tmp_path):
    path = _contract_file(tmp_path, title=42)
    assert _found(path, "draft") == [("$.title", "TC002", "42 is not of type 'string'")]


# --- intake copies the title from the feature document's title line ----------------------

def _step(text, label):
    start = re.search(rf"^{label}\. ", text, re.MULTILINE).start()
    end = text.find("\n\nI", start + 1)
    return text[start:end if end > 0 else None]


def test_intake_copies_the_title_from_the_feature_documents_title_line():
    text = FLOW.read_text(encoding="utf-8")
    assert TITLE_RULE in _step(text, "I4")
    assert text.count("`title:`") == 1  # one place says it
    # the flow stays a PromptLang prompt under its ceiling
    assert text.startswith("---\n")
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    assert all(f"</{tag}>" in text for tag in ("purpose", "instructions"))
    assert len(text) < CHAR_CEILING
