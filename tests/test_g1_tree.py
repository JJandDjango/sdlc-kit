"""G1 in the tree (contract: g1-requirements-spec, unit s4-tree).

A temporary repository per test, built by hand: one contract under specs/
that reads ready-green, `apply-discount`, its pair under docs/features/ (a
requirements document whose newest `Ready:` row names r5 and a design
document whose row names r4), a ratified `intake-seat` term, and a
.sdlc/config.yaml each test writes. Every record under .sdlc/g1/ is
written by hand, so no test needs a linter or a checker on the machine.

What the unit pins: a feature G1 is active for shows its G1 verdict with
no `inactive` mark, each of G1.1, G1.2 and G1.3 with the status `g1-check`
reads and, where it is not done, the messages of `g1-check`'s findings as
its diagnostics, each whole (SC5.1); a feature `g1.exempt` names prints as
it prints under `active_gates: [G0]`, byte for byte, and counts in no
roll-up at gates/G1 (SC5.2); the G1 verdict is the ratified roll-up of its
three conditions, and G1.3 names its review's seat and revisions as its
evidence (SC5.3). The tree prints one problem line for each G1 source it
cannot read, reads no G1 source while `G1` is off, stores nothing and
starts no tool.

A test whose last word is that nothing shows first proves, on the same
repository, that the tree reads G1 at all: no test here passes on a tree
that reads every G1 condition `to do`.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract import g1, tree, tree_view
from taskcontract.__main__ import main

ID = "apply-discount"
OTHER = "refund-order"
OLD = "old-feature"      # a contract the exempt list names
IDEA = "new-idea"        # a feature before intake
CONFIG = ".sdlc/config.yaml"
COMPONENTS = "specs/components.yaml"
PAGE = "docs/gates/G1-requirements-spec.md"
TO_DO, DOING, DONE, FAILED = "to do", "doing", "done", "failed"
CONDITIONS = {"G1.1": "Spec/schema linting", "G1.2": "Model checking",
              "G1.3": "Criteria completeness + ambiguity review"}
ABSENT = object()  # a key a hand-written record leaves out

# G1.3's 11 items as its page ratified them (docs/gates/G1-requirements-spec.md).
NAMES = ["Testable", "Unambiguous", "Traceable", "Complete over units",
         "Covers the sketch", "Consistent", "Respects non-goals",
         "Boundary + error paths", "Property-spec applicability",
         "Schema presence", "Oracle designation answered"]

CONTRACT = """id: {id}
title: A fixture feature
intent: >
  A contract with a scope of its own, enough words to pass the door as a
  fixture for the G1 tree suite.
scope:
  - api/
  - src/
non_goals:
  - nothing beyond the scope
decomposition:
  - unit: the unit
    id: the-unit
    confirmed_by: [po]
    done_means: the unit is done
    acceptance_sketch:
      - verify the unit is done
dependencies: []
entities: []
provenance:
  origin: human-request
"""

SCHEMA = "api/openapi.yaml"
PIN = ".spectral.yaml"
SPECTRAL = {"paths": ["api/*.yaml"], "linter": "spectral", "pin": PIN}
MODEL = "specs/models/ledger.tla"
MODEL_CONFIG = "specs/models/ledger.cfg"
# The design's hard core; its model's file is absent until a test writes it.
LEDGER = {"id": "ledger", "paths": ["src/ledger/"], "hard_core": True,
          "oracle": "concurrency", "model": MODEL, "model_config": MODEL_CONFIG,
          "checker": "tlc"}

NO_MODEL = "G1.2: hard core ledger has no model"
NOT_CLEAN = "G1.1: api/openapi.yaml does not lint clean: spectral reports 2"
UNCHECKED_6 = "G1.3: item 6 Consistent is unchecked in Statement"

# The design's first drawing (docs/features/g1-requirements-spec.design.md,
# "The tree"), line for line, and the repository's line under it.
DRAWING = [
    "  apply-discount/G1 Requirements / Spec [failed]",
    "    apply-discount/G1/G1.1 Spec/schema linting [done]",
    "    apply-discount/G1/G1.2 Model checking [failed]",
    "      - G1.2: hard core ledger has no model",
    "    apply-discount/G1/G1.3 Criteria completeness + ambiguity review [done]"
    " by po at r5, design r4",
    "  apply-discount/G2 Design / Architecture [to do] inactive",
]
GATE_DRAWING = [
    "gates/G1 Requirements / Spec [failed]",
    "  - apply-discount holds G1 at failed",
]

TITLE = "# {id} - A fixture feature\n\n"
HEAD = "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"

ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
DIAGNOSTIC = re.compile(r"^(?P<indent>(?:  )*)- (?P<text>.*)$")
PROBLEM = "taskcontract tree: "

# Each tool's stand-in leaves a mark when it starts; no print may start one.
STAND_IN = """import pathlib, sys
pathlib.Path(__file__).with_name(sys.argv[1] + ".started").write_text("started")
"""


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, and find no git repository
    above the fixture."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


# --- the fixture repository -------------------------------------------------------

def row(text: str, by: str = "Ann Lee") -> str:
    return f"| 2026-10-07 | {by} | {text} |\n"


def document(revision: int, feature: str = ID) -> str:
    """A feature document with text rows r1 to r<revision>, then the
    `Ready:` row that names r<revision> as the one the contract is derived
    from."""
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{feature}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return TITLE.format(id=feature) + HEAD + rows + ready + "\n## Statement\n\nWords.\n"


def items(unchecked: dict | None = None) -> list[dict]:
    unchecked = unchecked or {}
    held = []
    for n, name in enumerate(NAMES, start=1):
        entry = {"n": n, "name": name, "checked": n not in unchecked}
        if n in unchecked:
            entry["section"] = unchecked[n]
        held.append(entry)
    return held


def review(unchecked: dict | None = None, **keys) -> dict:
    """A G1.3 record as `g1-record review` writes it for the fixture's pair,
    with each given key changed, or left out when it is ABSENT."""
    record = {"condition": "G1.3", "at": "2026-10-07T14:20:40Z", "head": "8635064",
              "by": "Ann Lee", "seat": "po", "requirements": "r5", "design": "r4",
              "items": items(unchecked)}
    for key, value in keys.items():
        if value is ABSENT:
            record.pop(key, None)
        else:
            record[key] = value
    return record


class Repo:
    """One fixture repository at <tmp>/repo; never the working directory."""

    def __init__(self, tmp: Path):
        self.tmp = tmp
        self.root = tmp / "repo"
        self.root.mkdir()
        write_seat_roster(self.root, values=("po", "engineer"))
        self.contract(ID)
        self.pair(ID)
        self.config()

    def write(self, rel: str, text) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def dump(self, rel: str, doc) -> Path:
        return self.write(rel, yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

    def remove(self, rel: str) -> None:
        path = self.root / rel
        if path.is_file():
            path.unlink()

    def sha(self, rel: str) -> str:
        return hashlib.sha256((self.root / rel).read_bytes()).hexdigest()

    def contract(self, cid: str) -> None:
        self.write(f"specs/{cid}/contract.yaml", CONTRACT.format(id=cid))

    def pair(self, cid: str, requirements: int = 5, design: int | None = 4) -> None:
        self.write(f"docs/features/{cid}.md", document(requirements, cid))
        if design is None:
            self.remove(f"docs/features/{cid}.design.md")
        else:
            self.write(f"docs/features/{cid}.design.md", document(design, cid))

    def feature(self, cid: str = OTHER) -> None:
        """One more contract with its pair, as `apply-discount` has them."""
        self.contract(cid)
        self.pair(cid)

    def idea(self, fid: str = IDEA) -> None:
        """A feature before intake: a requirements document and no contract."""
        self.write(f"docs/features/{fid}.md", TITLE.format(id=fid) + HEAD
                   + row("r1: the first text") + "\n## Statement\n\nWords.\n")

    def close(self, cid: str) -> None:
        """Close the contract: one `done` record on its own id."""
        self.dump(f".sdlc/progress/{cid}.yaml", {"records": [
            {"item": cid, "state": "done", "at": "2026-09-25T10:00:00Z", "head": "1a2b3c4"}]})

    def config(self, active=("G0", "G1"), **g1_keys) -> None:
        """.sdlc/config.yaml as a person writes it: the `g1` key holds the
        given keys as given, and is left out when none is given."""
        doc = {"kit": "fixture", "active_gates": list(active)}
        if g1_keys:
            doc["g1"] = g1_keys
        self.dump(CONFIG, doc)

    def components(self, *entries: dict) -> None:
        self.dump(COMPONENTS, {"version": 1, "components": list(entries)})

    def records(self, *records: dict, cid: str = ID) -> None:
        self.dump(f".sdlc/g1/{cid}.yaml", {"records": list(records)})

    def schema_files(self) -> None:
        self.write(SCHEMA, "openapi: 3.1.0\n")
        self.write(PIN, "rules: {}\n")

    def lint(self, reported: int | None = 2, installed: bool = True) -> dict:
        """A G1.1 record that matches the schema and the pin as they stand."""
        return {"condition": "G1.1", "at": "2026-10-07T14:02:11Z", "head": "8635064",
                "tool": "spectral", "tool_version": "6.17.0" if installed else None,
                "installed": installed,
                "pin": {"path": PIN, "sha256": self.sha(PIN)},
                "files": [{"path": SCHEMA, "sha256": self.sha(SCHEMA),
                           "reported": reported if installed else None}]}

    def model_files(self) -> None:
        self.write(MODEL, "---- MODULE ledger ----\n====\n")
        self.write(MODEL_CONFIG, "SPECIFICATION Spec\n")

    def model(self, result: str | None = "fail", installed: bool = True) -> dict:
        """A G1.2 record that matches the ledger's model as it stands."""
        return {"condition": "G1.2", "at": "2026-10-07T14:10:00Z", "head": "8635064",
                "cores": [{"component": "ledger", "tool": "tlc", "installed": installed,
                           "model": {"path": MODEL, "sha256": self.sha(MODEL)},
                           "config": {"path": MODEL_CONFIG, "sha256": self.sha(MODEL_CONFIG)},
                           "result": result}]}

    def state(self, lint: str = TO_DO, model: str = TO_DO, rev: str = TO_DO,
              active=("G0", "G1"), **g1_keys) -> None:
        """Put `apply-discount` where each condition reads the given status:
        `to do` by an absent declaration or record, `done` by a declaration
        that says none (and a review that checks all 11 items on r5 and r4),
        `failed` by one rule's report."""
        held = []
        if lint != TO_DO:
            g1_keys["schemas"] = [SPECTRAL] if lint == FAILED else []
        if lint == FAILED:
            self.schema_files()
            held.append(self.lint(reported=2))
        self.config(active, **g1_keys)
        if model == TO_DO:
            self.remove(COMPONENTS)
        else:
            self.components(*([LEDGER] if model == FAILED else []))
        if rev != TO_DO:
            held.append(review({6: "Statement"} if rev == FAILED else None))
        if held:
            self.records(*held)
        else:
            self.remove(f".sdlc/g1/{ID}.yaml")

    def drawing(self) -> None:
        """The design's drawing: G1.1 done, G1.2 failed on a hard core with
        no model, G1.3 done by a review on r5 and r4."""
        self.state(DONE, FAILED, DONE)

    def files(self) -> dict[str, bytes]:
        return {path.relative_to(self.tmp).as_posix(): path.read_bytes()
                for path in sorted(self.tmp.rglob("*")) if path.is_file()}


@pytest.fixture
def repo(tmp_path) -> Repo:
    return Repo(tmp_path)


# --- driving the CLI and reading its print ------------------------------------------

def cli(capsys, *argv):
    capsys.readouterr()
    try:
        code = main([str(arg) for arg in argv])
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


class Print:
    """One whole print: its stdout, its stderr's lines, and each item line
    as a row with the diagnostics printed under it."""

    def __init__(self, out: str, err: str):
        self.out, self.err = out, err
        self.lines = out.splitlines()
        self.problems = err.splitlines()
        self.rows: list[dict] = []
        for text in self.lines:
            diagnostic = DIAGNOSTIC.match(text)
            if diagnostic:
                assert self.rows, f"a diagnostic line opens the print: {text!r}"
                assert len(diagnostic["indent"]) // 2 == self.rows[-1]["depth"] + 1, text
                self.rows[-1]["diagnostics"].append(diagnostic["text"])
                continue
            item = ITEM.match(text)
            assert item, f"neither an item line nor a diagnostic line: {text!r}"
            self.rows.append({"depth": len(item["indent"]) // 2, "id": item["id"],
                              "tag": item["tag"], "name": item["name"],
                              "rest": item["rest"], "line": text, "diagnostics": []})

    def row(self, rid: str) -> dict:
        for held in self.rows:
            if held["id"] == rid:
                return held
        raise AssertionError(f"{rid} not printed")

    def tag(self, rid: str) -> str:
        return self.row(rid)["tag"]

    def conditions(self, fid: str = ID) -> list[str]:
        return [self.tag(f"{fid}/G1/{key}") for key in CONDITIONS]

    def block(self, fid: str) -> list[str]:
        """The feature's own lines: its line, then every line under it."""
        start = next(n for n, text in enumerate(self.lines) if text.startswith(f"{fid} "))
        size = next((n for n, text in enumerate(self.lines[start + 1:])
                     if not text.startswith(" ")), len(self.lines) - start - 1)
        return self.lines[start:start + 1 + size]

    def verdicts(self, fid: str) -> list[str]:
        """The feature's verdict lines, in print order."""
        return [held["line"] for held in self.rows
                if held["depth"] == 1 and re.fullmatch(rf"{re.escape(fid)}/G\d+", held["id"])]

    def after(self, line: str, count: int) -> list[str]:
        """`count` lines of the print from the given line on."""
        assert line in self.lines, f"not printed: {line!r}"
        at = self.lines.index(line)
        return self.lines[at:at + count]


def show(repo: Repo, capsys) -> Print:
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0, err
    return Print(out, err)


def g1_lines(fid: str, verdict: str, conditions=(TO_DO, TO_DO, TO_DO), mark: str = "") -> list[str]:
    """A G1 verdict's line and its three conditions', with no evidence."""
    return [f"  {fid}/G1 Requirements / Spec [{verdict}]{mark}"] + [
        f"    {fid}/G1/{key} {name} [{status}]"
        for (key, name), status in zip(CONDITIONS.items(), conditions)]


def check(repo: Repo, capsys, cid: str = ID) -> tuple[dict[str, str], dict[str, list[str]]]:
    """`g1-check <id> --json`: each condition's status from its note, and
    each condition's messages from its findings, in its order."""
    code, out, err = cli(capsys, "g1-check", cid, "--root", repo.root, "--json")
    assert code in (0, 1), err
    answer = json.loads(out)
    statuses = dict(part.split(" ", 1) for part in answer["note"].split(", "))
    messages = {key: [f["message"] for f in answer["findings"] if f["condition"] == key]
                for key in CONDITIONS}
    return statuses, messages


def agree(repo: Repo, capsys, printed: Print, cid: str = ID) -> dict[str, str]:
    """One source: each G1 condition's status in the tree is `g1-check`'s,
    and its diagnostics are the messages of `g1-check`'s findings for it,
    in its order. A condition that reads `to do` or `done` lists nothing."""
    statuses, messages = check(repo, capsys, cid)
    for key in CONDITIONS:
        held = printed.row(f"{cid}/G1/{key}")
        assert held["tag"] == statuses[key], (key, held["line"], statuses)
        assert held["diagnostics"] == messages[key], (key, held["diagnostics"])
        if held["tag"] in (TO_DO, DONE):
            assert held["diagnostics"] == []
    return statuses


# --- SC5.1: G1 active, each condition from its own rules, its diagnostics listed ------

def test_sc5_1_a_feature_past_g0_prints_the_designs_drawing_line_for_line(repo, capsys):
    repo.drawing()
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G0")["line"].startswith(f"  {ID}/G0 Planning / Intake [done] via ")
    assert printed.after(DRAWING[0], len(DRAWING)) == DRAWING
    assert printed.problems == []
    agree(repo, capsys, printed)


def test_sc5_1_the_repositorys_line_names_the_feature_that_holds_g1(repo, capsys):
    repo.drawing()
    printed = show(repo, capsys)
    assert printed.after(GATE_DRAWING[0], len(GATE_DRAWING)) == GATE_DRAWING
    assert printed.row("gates/G1/G1.1")["line"] == "  gates/G1/G1.1 Spec/schema linting [done]"
    held = printed.row("gates/G1/G1.2")
    assert held["line"] == "  gates/G1/G1.2 Model checking [failed]"
    assert held["diagnostics"] == [f"{ID} holds G1.2 at failed"]


def test_sc5_1_a_condition_that_is_not_done_lists_each_diagnostic_whole(repo, capsys):
    # two schemas that do not lint clean, two hard cores with no model, two items unchecked
    repo.config(schemas=[SPECTRAL])
    repo.schema_files()
    repo.write("api/orders.yaml", "openapi: 3.1.0\n")
    lint = repo.lint(reported=2)
    lint["files"].append({"path": "api/orders.yaml", "sha256": repo.sha("api/orders.yaml"),
                          "reported": 1})
    repo.components(LEDGER, {**LEDGER, "id": "pricing", "paths": ["src/pricing/"]})
    repo.records(lint, review({6: "Statement", 9: "Success criteria"}))
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G1/G1.1")["diagnostics"] == [
        NOT_CLEAN, "G1.1: api/orders.yaml does not lint clean: spectral reports 1"]
    assert printed.row(f"{ID}/G1/G1.2")["diagnostics"] == [
        NO_MODEL, "G1.2: hard core pricing has no model"]
    assert printed.row(f"{ID}/G1/G1.3")["diagnostics"] == [
        UNCHECKED_6, "G1.3: item 9 Property-spec applicability is unchecked in Success criteria"]
    assert printed.conditions() == [FAILED, FAILED, FAILED]
    # the verdict lists nothing of its own
    assert printed.row(f"{ID}/G1")["diagnostics"] == []
    agree(repo, capsys, printed)


def test_sc5_1_a_diagnostic_prints_on_one_line(repo, capsys):
    # a component's id is a person's text: a line break inside it reads as one space
    repo.config(schemas=[])
    repo.components({**LEDGER, "id": "ledger\ncore"})
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G1/G1.2")["diagnostics"] == ["G1.2: hard core ledger core has no model"]
    _, messages = check(repo, capsys)
    assert messages["G1.2"] == ["G1.2: hard core ledger\ncore has no model"]


def _linter_missing(repo: Repo) -> None:
    repo.config(schemas=[SPECTRAL])
    repo.schema_files()
    repo.components(LEDGER)
    repo.model_files()
    repo.records(repo.lint(installed=False), repo.model("fail"),
                 review({2: "Statement", 11: "Terms"}))


def _stale(repo: Repo) -> None:
    # a lint record of the file as it was, a passing model, a review of older revisions
    repo.config(schemas=[SPECTRAL])
    repo.schema_files()
    repo.components(LEDGER)
    repo.model_files()
    lint = repo.lint(reported=0)
    repo.write(SCHEMA, "openapi: 3.1.1\n")
    repo.records(lint, repo.model("pass"), review(requirements="r4", design="r3"))


def _clean(repo: Repo) -> None:
    repo.config(schemas=[SPECTRAL])
    repo.schema_files()
    repo.components(LEDGER)
    repo.model_files()
    repo.records(repo.lint(reported=0), repo.model("pass"), review())


def _checker_missing(repo: Repo) -> None:
    repo.config(schemas=[])
    repo.components(LEDGER)
    repo.model_files()
    repo.records(repo.model(None, installed=False))


def _broken_contract(repo: Repo) -> None:
    # a contract that is no YAML: its scope reads as `g1-check` reads it
    repo.config(schemas=[SPECTRAL])
    repo.schema_files()
    repo.components(LEDGER)
    repo.records(repo.lint(reported=2), review())
    repo.write(f"specs/{ID}/contract.yaml", "id: [\n")


def _one_document(repo: Repo) -> None:
    repo.pair(ID, 5, None)
    repo.config(schemas=[])
    repo.records(review(design=ABSENT))


SCENARIOS = {
    "the-drawing": Repo.drawing,
    "a-linter-not-installed-a-failing-model-two-items-unchecked": _linter_missing,
    "a-stale-lint-record-a-passing-model-a-review-of-older-revisions": _stale,
    "every-record-clean": _clean,
    "a-checker-not-installed": _checker_missing,
    "a-contract-that-is-no-yaml": _broken_contract,
    "one-document": _one_document,
}


@pytest.mark.parametrize("scenario", list(SCENARIOS))
def test_sc5_1_one_source_each_condition_reads_as_g1_check_reads_it(repo, capsys, scenario):
    SCENARIOS[scenario](repo)
    printed = show(repo, capsys)
    statuses = agree(repo, capsys, printed)
    # a guard on the fixture: `g1-check` reads something a tree with no G1 would not
    assert set(statuses.values()) != {TO_DO}, statuses


# --- SC5.2: an exempt feature prints as today ------------------------------------

def test_sc5_2_an_exempt_feature_prints_byte_for_byte_as_under_g0_alone(repo, capsys):
    repo.feature(OLD)
    repo.close(OLD)
    repo.idea("old-idea")
    repo.state(DONE, DONE, FAILED, exempt=[OLD, "old-idea"])
    # each exempt feature holds a record file the tree has no cause to read
    repo.write(f".sdlc/g1/{OLD}.yaml", "- no mapping\n")
    repo.write(".sdlc/g1/old-idea.yaml", "- no mapping\n")
    printed = show(repo, capsys)
    for fid in (OLD, "old-idea"):
        assert printed.after(f"  {fid}/G1 Requirements / Spec [to do] inactive", 4) == g1_lines(
            fid, TO_DO, mark=" inactive")
    assert printed.verdicts(OLD) == [printed.row(f"{OLD}/G0")["line"],
                                     f"  {OLD}/G1 Requirements / Spec [to do] inactive"]
    assert printed.tag(OLD) == DONE
    assert printed.verdicts("old-idea")[-1] == "  old-idea/G1 Requirements / Spec [to do] inactive"
    # G1 counts the one feature that needs it, at the gate and at each condition
    assert printed.row("gates/G1")["diagnostics"] == [f"{ID} holds G1 at failed"]
    assert printed.row("gates/G1/G1.1")["diagnostics"] == []
    assert printed.row("gates/G1/G1.3")["diagnostics"] == [f"{ID} holds G1.3 at failed"]
    assert printed.problems == []
    repo.config(active=("G0",))
    today = show(repo, capsys)
    for fid in (OLD, "old-idea"):
        assert printed.block(fid) == today.block(fid)


def test_sc5_2_exempt_features_alone_hold_nothing_at_gates_g1(repo, capsys):
    repo.feature(OLD)
    repo.config(exempt=[ID, OLD])
    printed = show(repo, capsys)
    assert printed.after("gates/G1 Requirements / Spec [to do]", 4) == [
        "gates/G1 Requirements / Spec [to do]",
        "  gates/G1/G1.1 Spec/schema linting [to do]",
        "  gates/G1/G1.2 Model checking [to do]",
        "  gates/G1/G1.3 Criteria completeness + ambiguity review [to do]"]


def test_sc5_2_the_next_gate_after_a_features_last_active_gate_is_marked_inactive(repo, capsys):
    repo.feature(OLD)
    repo.config(exempt=[OLD])
    printed = show(repo, capsys)
    g0 = "{}/G0 Planning / Intake [done] via "
    exempt, needs = printed.verdicts(OLD), printed.verdicts(ID)
    # an exempt feature's last active gate is G0, so its next gate is G1
    assert exempt[0].startswith("  " + g0.format(OLD))
    assert exempt[1:] == [f"  {OLD}/G1 Requirements / Spec [to do] inactive"]
    # a feature that needs G1 shows it with no mark, then G2 as its next gate
    assert needs[0].startswith("  " + g0.format(ID))
    assert needs[1:] == [f"  {ID}/G1 Requirements / Spec [to do]",
                         f"  {ID}/G2 Design / Architecture [to do] inactive"]


def test_done_means_an_exempt_feature_keeps_its_g1_line_while_g2_is_active(repo, capsys):
    repo.config(active=("G0", "G1", "G2"), exempt=[ID])
    printed = show(repo, capsys)
    assert printed.after(f"  {ID}/G1 Requirements / Spec [to do] inactive", 4) == g1_lines(
        ID, TO_DO, mark=" inactive")
    # G2 stays active for it, and the next gate after its last active gate is G3
    assert printed.verdicts(ID)[1:] == [
        f"  {ID}/G1 Requirements / Spec [to do] inactive",
        f"  {ID}/G2 Design / Architecture [to do]",
        f"  {ID}/G3 Implementation [to do] inactive"]
    assert printed.row("gates/G1")["diagnostics"] == []


# --- SC5.3: the roll-up, and the review's seat and revisions -------------------------

@pytest.mark.parametrize("lint, model, rev, verdict, feature", [
    (DONE, TO_DO, TO_DO, DOING, DOING),
    (TO_DO, DONE, TO_DO, DOING, DOING),
    (TO_DO, TO_DO, DONE, DOING, DOING),
    (DONE, DONE, TO_DO, DOING, DOING),   # `schemas: []`, `components: []`, no review
    (DONE, DONE, DONE, DONE, TO_DO),     # a verdict done alone never starts its contract
    (FAILED, DONE, DONE, FAILED, FAILED),
    (DONE, FAILED, DONE, FAILED, FAILED),
    (DONE, DONE, FAILED, FAILED, FAILED),
    (TO_DO, TO_DO, FAILED, FAILED, FAILED),
], ids=["one-done-lint", "one-done-model", "one-done-review", "no-schema-no-hard-core-no-review",
        "all-done", "lint-failed", "model-failed", "review-failed", "review-failed-rest-to-do"])
def test_sc5_3_g1_reads_the_roll_up_of_its_three_conditions(repo, capsys, lint, model, rev,
                                                             verdict, feature):
    repo.state(lint, model, rev)
    printed = show(repo, capsys)
    assert printed.conditions() == [lint, model, rev]
    held = printed.row(f"{ID}/G1")
    # the verdict's line carries its status alone, and no diagnostic of its own
    assert held["line"] == f"  {ID}/G1 Requirements / Spec [{verdict}]"
    assert held["diagnostics"] == []
    # the feature's own line takes it by the roll-up an open contract already has
    assert printed.tag(f"{ID}/G0") == DONE
    assert printed.tag(ID) == feature
    gate = printed.row("gates/G1")
    assert gate["line"] == f"gates/G1 Requirements / Spec [{verdict}]"
    assert gate["diagnostics"] == ([] if verdict == DONE else [f"{ID} holds G1 at {verdict}"])
    agree(repo, capsys, printed)


def test_sc5_3_a_closed_contract_still_reads_done_and_still_counts_at_gates_g1(repo, capsys):
    repo.state(DONE, FAILED, DONE)
    repo.close(ID)
    printed = show(repo, capsys)
    assert printed.tag(ID) == DONE
    assert printed.row(f"{ID}/G1")["line"] == f"  {ID}/G1 Requirements / Spec [failed]"
    assert printed.after(GATE_DRAWING[0], len(GATE_DRAWING)) == GATE_DRAWING


def test_sc5_3_a_signed_review_shows_its_seat_and_each_revision_it_names(repo, capsys):
    line = f"    {ID}/G1/G1.3 Criteria completeness + ambiguity review [done]"
    repo.config(schemas=[])
    repo.records(review(seat="engineer"))
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G1/G1.3")["line"] == line + " by engineer at r5, design r4"
    agree(repo, capsys, printed)
    # a feature with one document: its review names one revision
    repo.pair(ID, 5, None)
    repo.records(review(design=ABSENT))
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G1/G1.3")["line"] == line + " by po at r5"
    agree(repo, capsys, printed)


# --- the evidence, the problem lines, G1 off, the query and the pane ------------

def test_done_means_g1_3_prints_its_evidence_when_done_or_failed_and_at_no_other_status(
        repo, capsys):
    line = f"    {ID}/G1/G1.3 Criteria completeness + ambiguity review "

    def shown(*records) -> str:
        if records:
            repo.records(*records)
        else:
            repo.remove(f".sdlc/g1/{ID}.yaml")
        printed = show(repo, capsys)
        agree(repo, capsys, printed)
        return printed.row(f"{ID}/G1/G1.3")["line"]

    assert shown(review()) == line + "[done] by po at r5, design r4"
    assert shown(review({6: "Statement"})) == line + "[failed] by po at r5, design r4"
    # the last record counts alone: an earlier review that passed shows nothing
    assert shown(review(), review({6: "Statement"}, seat="engineer")) == (
        line + "[failed] by engineer at r5, design r4")
    # a review that does not count prints none
    assert shown() == line + "[to do]"
    assert shown(review(by=ABSENT)) == line + "[to do]"
    assert shown(review(seat="  ")) == line + "[to do]"
    assert shown(review(requirements="r4", design="r3")) == line + "[to do]"
    repo.pair(ID, 5, None)  # the record names a design revision the feature does not hold
    assert shown(review()) == line + "[to do]"


@pytest.mark.parametrize("requirements, design, evidence", [
    ("r5", "r4", "by po at r5, design r4"),
    ("r5", ABSENT, "by po at r5"),
    ("r5", 4, "by po at r5"),
    ("r5", ["r4"], "by po at r5"),
    ("r5", "r4 ", "by po at r5"),
    ("r5", "r4\n", "by po at r5"),
    ("r5", "design", "by po at r5"),
    (5, "r4", "by po, design r4"),
    ("r5 ", "r4", "by po, design r4"),
    (["r5"], "r4", "by po, design r4"),
    ("R5", "r4", "by po, design r4"),
    ("r５", "r4", "by po, design r4"),
    (ABSENT, ABSENT, "by po"),
    (5, 4, "by po"),
], ids=["both", "no-design", "design-a-number", "design-a-list", "design-a-blank-after",
        "design-a-line-break-after", "design-a-word", "requirements-a-number",
        "requirements-a-blank-after", "requirements-a-list", "requirements-a-capital",
        "requirements-a-fullwidth-digit", "neither", "both-numbers"])
def test_done_means_the_evidence_names_only_a_revision_that_is_r_and_digits(
        repo, capsys, requirements, design, evidence):
    # an unchecked item reads `failed` whatever the revisions hold
    repo.records(review({6: "Statement"}, requirements=requirements, design=design))
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G1/G1.3")["line"] == (
        f"    {ID}/G1/G1.3 Criteria completeness + ambiguity review [failed] {evidence}")
    assert printed.row(f"{ID}/G1/G1.3")["diagnostics"] == [UNCHECKED_6]
    agree(repo, capsys, printed)


def test_done_means_the_evidence_names_the_records_design_where_the_feature_holds_none(
        repo, capsys):
    repo.pair(ID, 5, None)
    repo.records(review({6: "Statement"}))
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G1/G1.3")["line"].endswith(" [failed] by po at r5, design r4")
    agree(repo, capsys, printed)


@pytest.mark.parametrize("seat, shown", [
    ("  po  ", "po"),
    ("p\to", "p\to"),
    ("\x1b[31mpo", "\x1b[31mpo"),
    ("s" * 300, "s" * 300),
], ids=["blanks-at-its-ends", "a-tab", "a-terminal-escape", "300-characters"])
def test_done_means_the_seat_prints_with_its_ends_stripped_and_nothing_else_changed(
        repo, capsys, seat, shown):
    repo.records(review(seat=seat))
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0, err
    assert (f"    {ID}/G1/G1.3 Criteria completeness + ambiguity review [done] "
            f"by {shown} at r5, design r4") in out.split("\n")
    statuses, _ = check(repo, capsys)
    assert statuses["G1.3"] == DONE


@pytest.mark.parametrize("section", ["State\tment", "\x1b[2JStatement", "S" * 300],
                         ids=["a-tab", "a-terminal-escape", "300-characters"])
def test_done_means_a_diagnostic_prints_the_section_as_g1_check_gives_it(repo, capsys, section):
    repo.records(review({6: section}))
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0, err
    message = f"G1.3: item 6 Consistent is unchecked in {section}"
    assert f"      - {message}" in out.split("\n")
    assert check(repo, capsys)[1]["G1.3"] == [message]


@pytest.mark.parametrize("held", [
    yaml.safe_dump({"records": [review({6: "Statement"})]}, sort_keys=False).encode("utf-8"),
    b"- no mapping\n",
    b"\xff\xfe\x00",
], ids=["a-review-that-fails", "no-mapping", "not-utf-8"])
def test_done_means_a_feature_before_intake_shows_g1_active_and_to_do_whatever_its_record_holds(
        repo, capsys, held):
    repo.idea(IDEA)
    repo.records(review({6: "Statement"}))
    repo.write(f".sdlc/g1/{IDEA}.yaml", held)
    printed = show(repo, capsys)
    # the contract beside it reads its record
    assert printed.row(f"{ID}/G1")["line"] == f"  {ID}/G1 Requirements / Spec [failed]"
    assert printed.after(f"  {IDEA}/G1 Requirements / Spec [to do]", 5) == g1_lines(
        IDEA, TO_DO) + [f"  {IDEA}/G2 Design / Architecture [to do] inactive"]
    assert printed.row("gates/G1")["diagnostics"] == [
        f"{ID} holds G1 at failed", f"{IDEA} holds G1 at to do"]
    # its record file is no source of the tree, so it has no problem line
    assert printed.problems == []


@pytest.mark.parametrize("held, reason", [
    (b"- no mapping\n", r"not a mapping"),
    (b"", r"not a mapping"),
    (b"note: no records\n", r"records is not a list"),
    (b"records: 5\n", r"records is not a list"),
    (b"\xff\xfe\x00", r"cannot be read"),
    (b"records: [\n", r"YAML error at line \d+"),
], ids=["a-list", "empty", "no-records-key", "records-no-list", "not-utf-8", "no-yaml"])
def test_done_means_a_record_file_that_cannot_be_read_prints_one_problem_line(
        repo, capsys, held, reason):
    repo.config(schemas=[])
    repo.components()
    repo.write(f".sdlc/g1/{ID}.yaml", held)
    printed = show(repo, capsys)
    assert len(printed.problems) == 1, printed.problems
    assert re.fullmatch(re.escape(f"{PROBLEM}unreadable record: .sdlc/g1/{ID}.yaml (")
                        + reason + r"\)", printed.problems[0]), printed.problems[0]
    # the file counts as absent for the statuses, as `g1-check` has it
    assert printed.conditions() == [DONE, DONE, TO_DO]
    assert printed.row(f"{ID}/G1/G1.3")["line"].endswith("[to do]")
    agree(repo, capsys, printed)


@pytest.mark.parametrize("schemas, reason", [
    ("api/*.yaml", "it is no list"),
    (None, "it is no list"),
    (["api/*.yaml"], "entry 1 is no mapping"),
    ([{"paths": "api/*.yaml", "linter": "spectral", "pin": PIN}],
     "entry 1 holds no list of paths"),
    ([SPECTRAL, {"paths": ["api/*.proto"], "pin": "buf.yaml"}], "entry 2 names no linter"),
    ([{"paths": ["api/*.yaml"], "linter": "spectral", "pin": ""}], "entry 1 names no pin"),
], ids=["a-text", "null", "an-entry-no-mapping", "paths-no-list", "no-linter", "an-empty-pin"])
def test_done_means_a_schema_declaration_that_cannot_be_read_prints_one_line_a_print(
        repo, capsys, schemas, reason):
    repo.feature(OTHER)
    repo.schema_files()
    repo.config(schemas=schemas)
    repo.components()
    printed = show(repo, capsys)
    # once a print, never once a feature
    assert printed.problems == [f"{PROBLEM}unreadable g1.schemas: {CONFIG} ({reason})"]
    for cid in (ID, OTHER):
        assert printed.conditions(cid) == [TO_DO, DONE, TO_DO]
        agree(repo, capsys, printed, cid)


@pytest.mark.parametrize("text", [
    b"components: [\n",
    b"\xff\xfe\x00",
    b"version: 1\ncomponents:\n  - {id: ledger, paths: [src/ledger/], hard_core: true}\n",
    b"version: 2\ncomponents: []\n",
    b"- no mapping\n",
], ids=["no-yaml", "not-utf-8", "an-entry-the-schema-refuses", "a-version-the-schema-refuses",
        "no-mapping"])
def test_done_means_a_component_declaration_that_cannot_be_read_prints_one_line_a_print(
        repo, capsys, text):
    repo.feature(OTHER)
    repo.config(schemas=[])
    repo.write(COMPONENTS, text)
    with pytest.raises(g1.Unreadable) as refused:  # the reason `g1-record model` prints
        g1.components(repo.root)
    printed = show(repo, capsys)
    assert printed.problems == [
        f"{PROBLEM}unreadable component declaration: {COMPONENTS} ({refused.value})"]
    for cid in (ID, OTHER):
        assert printed.conditions(cid) == [DONE, TO_DO, TO_DO]
        agree(repo, capsys, printed, cid)


def test_done_means_each_exempt_id_that_names_no_feature_prints_one_problem_line(repo, capsys):
    repo.feature(OLD)
    repo.idea(IDEA)
    # a contract, a feature before intake, two ids of no feature, and the
    # contract's id in another letter case, which names no feature either
    repo.config(exempt=["ghost-b", OLD, IDEA, "ghost-a", "Apply-Discount"])
    printed = show(repo, capsys)
    assert printed.problems == [f"{PROBLEM}g1.exempt names no feature: {name}"
                                for name in ("ghost-b", "ghost-a", "Apply-Discount")]
    # an id is matched as written: `apply-discount` is not exempt
    assert printed.verdicts(ID)[1:] == [f"  {ID}/G1 Requirements / Spec [to do]",
                                        f"  {ID}/G2 Design / Architecture [to do] inactive"]
    for fid in (OLD, IDEA):
        assert printed.verdicts(fid)[-1] == f"  {fid}/G1 Requirements / Spec [to do] inactive"
    assert printed.row("gates/G1")["diagnostics"] == [f"{ID} holds G1 at to do"]


@pytest.mark.parametrize("exempt", [ID, {ID: True}, 5], ids=["a-text", "a-mapping", "a-number"])
def test_done_means_an_exempt_value_that_is_no_list_exempts_nothing_and_prints_one_line(
        repo, capsys, exempt):
    repo.state(DONE, DONE, FAILED, exempt=exempt)
    printed = show(repo, capsys)
    assert printed.problems == [f"{PROBLEM}unreadable g1.exempt: {CONFIG} (it is no list)"]
    assert printed.row(f"{ID}/G1")["line"] == f"  {ID}/G1 Requirements / Spec [failed]"
    agree(repo, capsys, printed)


def test_done_means_g1s_problem_lines_follow_todays_in_one_order(repo, capsys):
    repo.feature(OTHER)
    repo.config(exempt=["ghost-b", "ghost-a"], schemas="api/*.yaml")
    repo.write(COMPONENTS, "- no mapping\n")
    with pytest.raises(g1.Unreadable) as refused:
        g1.components(repo.root)
    repo.write(f".sdlc/g1/{OTHER}.yaml", "note: no records\n")
    repo.write(f".sdlc/g1/{ID}.yaml", "- no mapping\n")
    repo.write(".sdlc/findings/bad-finding.yaml", "- no mapping\n")
    printed = show(repo, capsys)
    assert printed.problems == [PROBLEM + line for line in (
        "unreadable finding: .sdlc/findings/bad-finding.yaml (not a mapping)",
        "g1.exempt names no feature: ghost-b",
        "g1.exempt names no feature: ghost-a",
        f"unreadable g1.schemas: {CONFIG} (it is no list)",
        f"unreadable component declaration: {COMPONENTS} ({refused.value})",
        f"unreadable record: .sdlc/g1/{ID}.yaml (not a mapping)",
        f"unreadable record: .sdlc/g1/{OTHER}.yaml (records is not a list)")]


def test_done_means_a_contract_that_is_not_utf_8_never_stops_the_print(repo, capsys):
    # G0 is off here: its validator is no part of this unit, and G1's reading
    # of the contract's scope is what must not stop the print
    repo.feature(OTHER)
    repo.state(DONE, DONE, FAILED, active=("G1",))
    repo.write(f"specs/{OTHER}/contract.yaml", b"id: \xff\xfe\n")
    printed = show(repo, capsys)
    assert printed.row(f"{ID}/G1")["line"] == f"  {ID}/G1 Requirements / Spec [failed]"
    assert printed.row(f"{OTHER}/G1")["line"].startswith(f"  {OTHER}/G1 Requirements / Spec [")
    assert printed.problems == [
        f"{PROBLEM}unreadable contract: specs/{OTHER}/contract.yaml (cannot be read)"]


@pytest.mark.parametrize("condition", ["G1.1", "G1.2"], ids=["a-pin", "a-model-configuration"])
def test_done_means_a_declared_path_that_holds_a_nul_never_stops_the_print(
        repo, capsys, condition):
    # a control first: the tree reads G1 on this repository
    repo.state(DONE, DONE, DONE)
    assert show(repo, capsys).conditions() == [DONE, DONE, DONE]
    # then one declared path no system call takes: its file reads as absent,
    # for the tree and for `g1-check` alike
    if condition == "G1.1":
        repo.schema_files()
        repo.config(schemas=[{**SPECTRAL, "pin": "a\x00b"}])
    else:
        repo.model_files()
        repo.components({**LEDGER, "model_config": "specs/models/a\x00b.cfg"})
    printed = show(repo, capsys)
    assert printed.tag(f"{ID}/G1/{condition}") == TO_DO
    assert printed.problems == []
    agree(repo, capsys, printed)


def test_done_means_absent_declarations_and_records_read_to_do_and_print_no_problem_line(
        repo, capsys):
    # G0 and G1 active, no `g1` key, no specs/components.yaml: first with a record
    repo.records(review({6: "Statement"}))
    printed = show(repo, capsys)
    assert printed.after(f"  {ID}/G1 Requirements / Spec [failed]", 4)[:3] == g1_lines(
        ID, FAILED, (TO_DO, TO_DO, FAILED))[:3]
    assert printed.problems == []
    # then with none: every condition reads `to do`, and nothing is named
    repo.remove(f".sdlc/g1/{ID}.yaml")
    printed = show(repo, capsys)
    assert printed.after(f"  {ID}/G1 Requirements / Spec [to do]", 5) == g1_lines(ID, TO_DO) + [
        f"  {ID}/G2 Design / Architecture [to do] inactive"]
    assert printed.row("gates/G1")["diagnostics"] == [f"{ID} holds G1 at to do"]
    assert printed.problems == []
    agree(repo, capsys, printed)


def _unreadable_sources(repo: Repo, active) -> None:
    """Every G1 source in a state the tree names when it reads it."""
    repo.config(active, exempt=["ghost"], schemas="api/*.yaml")
    repo.write(COMPONENTS, "components: [\n")
    repo.write(f".sdlc/g1/{ID}.yaml", "- no mapping\n")


def test_done_means_with_g1_off_the_tree_reads_no_g1_source(repo, capsys):
    _unreadable_sources(repo, ("G0", "G1"))
    assert len(show(repo, capsys).problems) == 4
    # the same sources with G1 off: not one is read
    _unreadable_sources(repo, ("G0",))
    off = show(repo, capsys)
    repo.config(("G0",))
    repo.remove(COMPONENTS)
    repo.remove(f".sdlc/g1/{ID}.yaml")
    (repo.root / ".sdlc" / "g1").rmdir()
    without = show(repo, capsys)
    assert (off.out, off.err) == (without.out, without.err)
    assert off.err == ""
    assert off.verdicts(ID)[1:] == [f"  {ID}/G1 Requirements / Spec [to do] inactive"]


def test_done_means_an_unreadable_config_prints_its_one_line_and_no_second(repo, capsys):
    _unreadable_sources(repo, ("G0", "G1"))
    assert len(show(repo, capsys).problems) == 4
    repo.write(CONFIG, "active_gates: [G0, G1\ng1: {exempt: 5}\n")
    printed = show(repo, capsys)
    assert len(printed.problems) == 1, printed.problems
    assert re.fullmatch(re.escape(f"{PROBLEM}unreadable config: {CONFIG} (")
                        + r"YAML error at line \d+\)", printed.problems[0])


def test_done_means_the_query_prints_a_g1_condition_with_its_evidence_and_no_diagnostic(
        repo, capsys):
    repo.drawing()
    code, out, err = cli(capsys, "tree", f"{ID}/G1/G1.3", "--root", repo.root)
    assert (code, err) == (0, "")
    assert out == (f"{ID}/G1/G1.3 Criteria completeness + ambiguity review [done] "
                   f"by po at r5, design r4\npage: {PAGE}\n")
    code, out, err = cli(capsys, "tree", f"{ID}/G1/G1.2", "--root", repo.root)
    assert (code, err) == (0, "")
    assert out == f"{ID}/G1/G1.2 Model checking [failed]\npage: {PAGE}\n"


def test_done_means_every_id_the_tree_prints_answers_as_a_query_in_at_most_seven_lines(
        repo, capsys):
    repo.idea(IDEA)
    repo.state(FAILED, FAILED, FAILED)
    printed = show(repo, capsys)
    assert printed.conditions() == [FAILED, FAILED, FAILED]
    listed = [text for held in printed.rows for text in held["diagnostics"]]
    assert {NOT_CLEAN, NO_MODEL, UNCHECKED_6} <= set(listed)
    for held in printed.rows:
        code, out, err = cli(capsys, "tree", held["id"], "--root", repo.root)
        assert (code, err) == (0, ""), held["id"]
        lines = out.splitlines()
        assert 1 <= len(lines) <= 7, held["id"]
        assert lines[0].startswith(f"{held['id']} "), held["id"]
        assert f"[{held['tag']}]" in lines[0], held["id"]
        assert not any(text.lstrip().startswith("- ") for text in lines), held["id"]
        assert not any(text in out for text in listed), held["id"]


def test_done_means_the_pane_watches_the_g1_record_folder(repo):
    assert ".sdlc/g1" in tree_view.WATCHED
    before = tree_view.scan(repo.root)
    repo.write(".sdlc/notes.txt", "not a source\n")
    assert tree_view.scan(repo.root) == before
    repo.records(review())
    after = tree_view.scan(repo.root)
    assert set(after) - set(before) == {f".sdlc/g1/{ID}.yaml"}


# --- the design's constraints ------------------------------------------------------

def _install(folder: Path, tool: str) -> None:
    """Put a stand-in named `tool` in the folder: a .cmd on Windows, an
    executable script elsewhere. It leaves `<tool>.started` when it starts."""
    script = folder / "stand_in.py"
    script.write_text(STAND_IN, encoding="utf-8")
    if os.name == "nt":
        (folder / f"{tool}.cmd").write_text(
            f'@echo off\r\n"{sys.executable}" "{script}" {tool} %*\r\n'
            "exit /b %ERRORLEVEL%\r\n", encoding="utf-8", newline="")
    else:
        shim = folder / tool
        shim.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" {tool} "$@"\n',
                        encoding="utf-8", newline="")
        shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def test_constraint_7_a_print_stores_nothing_and_starts_no_tool(repo, capsys, monkeypatch):
    # a schema in scope with no lint record and a hard core whose model has
    # no result: the state in which `g1-record` would start both tools
    repo.config(schemas=[SPECTRAL, {"paths": ["api/*.proto"], "linter": "buf", "pin": "buf.yaml"}])
    repo.schema_files()
    repo.write("api/orders.proto", 'syntax = "proto3";\n')
    repo.components(LEDGER, {**LEDGER, "id": "pricing", "paths": ["src/pricing/"],
                             "checker": "p"})
    repo.model_files()
    repo.records(review({6: "Statement"}))
    bin_dir = repo.tmp / "bin"
    bin_dir.mkdir()
    for tool in ("spectral", "buf", "tlc", "p"):
        _install(bin_dir, tool)
    monkeypatch.setenv("PATH", str(bin_dir))
    if os.name == "nt":
        monkeypatch.setenv("PATHEXT", ".COM;.EXE;.BAT;.CMD")
    before = repo.files()
    printed = show(repo, capsys)
    code, _, err = cli(capsys, "tree", f"{ID}/G1", "--root", repo.root)
    assert (code, err) == (0, "")
    assert printed.conditions() == [TO_DO, TO_DO, FAILED]
    assert printed.row(f"{ID}/G1")["line"] == f"  {ID}/G1 Requirements / Spec [failed]"
    assert sorted(path.name for path in bin_dir.glob("*.started")) == []
    assert repo.files() == before


def _item(items, rid):
    for item in items:
        if item.id == rid:
            return item
        found = _item(item.children, rid)
        if found is not None:
            return found
    return None


def test_constraint_7_a_record_changed_between_two_builds_shows_with_a_cache(repo):
    repo.config(schemas=[])
    repo.components()
    cache: dict = {}
    first, _ = tree.build(repo.root, cache)
    assert [_item(first, f"{ID}/G1/{key}").status for key in CONDITIONS] == [DONE, DONE, TO_DO]
    assert _item(first, f"{ID}/G1").status == DOING
    assert ID in cache  # the pane's cache holds the G0 reading, and no G1 reading follows it
    repo.records(review())
    second, _ = tree.build(repo.root, cache)
    held = _item(second, f"{ID}/G1/G1.3")
    assert (held.status, held.evidence) == (DONE, "by po at r5, design r4")
    assert _item(second, f"{ID}/G1").status == DONE
    repo.components(LEDGER)
    third, _ = tree.build(repo.root, cache)
    held = _item(third, f"{ID}/G1/G1.2")
    assert (held.status, held.diagnostics) == (FAILED, [NO_MODEL])
    assert _item(third, f"{ID}/G1").status == FAILED


# --- done_means ---------------------------------------------------------------------

def test_done_means_g1_is_read_where_g0_is_not_an_active_gate(repo, capsys):
    repo.state(DONE, FAILED, DONE, active=("G1",))
    printed = show(repo, capsys)
    assert printed.after(DRAWING[0], 5) == DRAWING[:5]
    assert printed.after(GATE_DRAWING[0], 2) == GATE_DRAWING
    assert printed.problems == []
    agree(repo, capsys, printed)


def test_done_means_the_trees_docstring_says_what_it_reads_for_g1():
    text = Path(tree.__file__).read_text(encoding="utf-8")
    docstring = " ".join((ast.get_docstring(ast.parse(text), clean=False) or "").split())
    for source in (".sdlc/g1", "specs/components.yaml", "g1.exempt", "g1.schemas"):
        assert source in docstring, f"the docstring names no {source}"
    # G1.3 names a seat now, so the sentence that no other item does is gone
    assert "No other item names a seat." not in docstring
    # the order document-split pinned stays (tests/test_document_split_release.py)
    at = 0
    for sentence in ("stands beside it.",
                     "A contract's id holds no dot, by the schema's pattern, so no valid "
                     "contract's document ends `.design.md`; a contract folder named "
                     "`x.design` would still read docs/features/x.design.md as its own.",
                     "The tree prints none of their other words"):
        found = docstring.find(sentence, at)
        assert found >= 0, f"{sentence!r} does not stand after position {at}"
        at = found + len(sentence)
