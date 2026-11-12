"""A plain request reaches G1 (contract: g1-requirements-spec, unit
s7-plain-request: checks SC1.2 and SC4.1, and done_means).

Where G1 is an active gate for a feature, `new` refuses a feature that has
no feature document: it prints message 8 on stderr, exits 1 and writes
nothing (SC4.1). G1.3 reads a contract with no feature document first: it
reads `failed` with one finding, RS302, message 9, whatever its records hold,
and it reads `failed` until a later revision's review passes (SC1.2). Kit
0.22.1 ships the fix (done_means).

A temporary repository per test, with a `.sdlc/config.yaml` that turns G1 on,
a ratified `intake-seat` term, and a `g1` declaration whose schema pattern
matches no file and whose component declaration holds no hard core, so G1.1
and G1.2 read `done` in every summary line here. No test needs a tool on the
machine. Every test that pins the new behavior first asserts it, so none
passes on today's code.

The hand-off tests take each path into intake past `new`, a plain request and
a pair, on to `g1-record review` (ADR 0041, rule 3).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from taskcontract.__main__ import main
from taskcontract.scaffold import scaffold

ROOT = Path(__file__).resolve().parent.parent
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
INTAKE = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
G1_FLOW = ROOT / "skills" / "sdlc" / "flows" / "g1.md"
PACKAGE = ROOT / "taskcontract"
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "skills" / "sdlc" / "init.py"
CHANGELOG = ROOT / "CHANGELOG.md"

ID = "apply-discount"
OTHER = "refund-order"
RECORD = f".sdlc/g1/{ID}.yaml"
REQUIREMENTS = f"docs/features/{ID}.md"
DESIGN = f"docs/features/{ID}.design.md"
ROSTER = "specs/vocabulary/intake-seat.yaml"
GREEN = f"g1-green: {ID}"
PASSED = "G1.3: the review checks all 11 items"
RECORDED = f"recorded: {RECORD}"
G1_3_ROW = "Criteria completeness + ambiguity review"

NAMES = ["Testable", "Unambiguous", "Traceable", "Complete over units",
         "Covers the sketch", "Consistent", "Respects non-goals",
         "Boundary + error paths", "Property-spec applicability",
         "Schema presence", "Oracle designation answered"]
ALL = "1,2,3,4,5,6,7,8,9,10,11"

CONTRACT = """id: {id}
title: A fixture feature
intent: >
  A contract with a scope of its own, enough words to pass the door as a
  fixture for the s7 suite.
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

SPECTRAL = {"paths": ["api/*.yaml"], "linter": "spectral", "pin": ".spectral.yaml"}
API = {"id": "api", "paths": ["src/api/"], "hard_core": False, "oracle": "none",
       "oracle_reason": "read-only pass-through, covered by its acceptance tests"}
ACTIVE = {"active_gates": ["G0", "G1"],
          "g1": {"exempt": ["controlled-language"], "schemas": [SPECTRAL]}}

TITLE = "# {id} - A fixture feature\n\n"
HEAD = "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"


def message_8(feature: str) -> str:
    return (f"taskcontract new: no feature document for {feature}, and G1 is active for "
            f"it; write docs/features/{feature}.md, or add {feature} to g1.exempt")


def message_9(feature: str = ID) -> str:
    return (f"G1.3: no feature document at docs/features/{feature}.md; write it and run "
            f"intake again, or add {feature} to g1.exempt")


def rs301(n: int, section: str) -> str:
    return f"G1.3: item {n} {NAMES[n - 1]} is unchecked in {section}"


def row(text: str, by: str = "Ann Lee") -> str:
    return f"| 2026-10-07 | {by} | {text} |\n"


def document(revision: int, feature: str = ID) -> str:
    """A feature document with text rows r1 to r<revision>, then the `Ready:`
    row that names r<revision> as the one the contract is derived from."""
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


def written(unchecked: dict | None = None, **keys) -> dict:
    """A G1.3 record as `g1-record review` writes it for the fixture's pair."""
    record = {"condition": "G1.3", "at": "2026-10-07T14:20:40Z", "head": "8635064",
              "by": "Ann Lee", "seat": "po", "requirements": "r5", "design": "r4",
              "items": items(unchecked)}
    record.update(keys)
    return record


SEAT_TERM = {"term": "intake-seat", "name": "Intake seat",
             "definition": "A human position that answers for a unit at intake.",
             "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
             "since": "2026-08-26"}


class Repo:
    """One fixture repository at <tmp>/repo, the working directory. It holds
    a roster and a config that turns G1 on, and the pair of documents of
    `apply-discount` unless the test leaves them out."""

    def __init__(self, tmp: Path, monkeypatch, contract: bool = True, docs: bool = True):
        self.root = tmp / "repo"
        self.root.mkdir()
        self.write(ROSTER, yaml.safe_dump(SEAT_TERM, sort_keys=False))
        self.config(ACTIVE)
        self.write("specs/components.yaml", yaml.safe_dump(
            {"version": 1, "components": [API]}, sort_keys=False))
        # another feature's documents: no document for ID
        self.write(f"docs/features/{OTHER}.md", document(2, OTHER))
        self.write(f"docs/features/{OTHER}.design.md", document(2, OTHER))
        if contract:
            self.write(f"specs/{ID}/contract.yaml", CONTRACT.format(id=ID))
        if docs:
            self.requirements(5)
            self.design(4)
        monkeypatch.chdir(self.root)

    def write(self, rel: str, text) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def remove(self, rel: str) -> None:
        path = self.root / rel
        if path.is_file():
            path.unlink()

    def config(self, doc) -> None:
        if doc is None:
            self.remove(".sdlc/config.yaml")
        else:
            self.write(".sdlc/config.yaml", yaml.safe_dump(doc, sort_keys=False))

    def requirements(self, revision: int, feature: str = ID) -> None:
        self.write(f"docs/features/{feature}.md", document(revision, feature))

    def design(self, revision: int, feature: str = ID) -> None:
        self.write(f"docs/features/{feature}.design.md", document(revision, feature))

    def put(self, *records, feature: str = ID) -> None:
        self.write(f".sdlc/g1/{feature}.yaml", yaml.safe_dump(
            {"records": list(records)}, sort_keys=False, allow_unicode=True))

    def records(self) -> list[dict]:
        return yaml.safe_load((self.root / RECORD).read_text(encoding="utf-8"))["records"]

    def snapshot(self) -> dict:
        """Every path under the root, a folder as None: a refused call leaves
        no file, and no empty folder either."""
        return {path.relative_to(self.root).as_posix():
                (path.read_bytes() if path.is_file() else None)
                for path in sorted(self.root.rglob("*"))}


@pytest.fixture(autouse=True)
def _no_git_above(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Repo:
    return Repo(tmp_path, monkeypatch)


@pytest.fixture
def bare(tmp_path, monkeypatch) -> Repo:
    """G1 on, no contract and no document for `apply-discount`: a plain request."""
    return Repo(tmp_path, monkeypatch, contract=False, docs=False)


def cli(capsys, *argv):
    """Run one taskcontract command in this process: (exit code, stdout, stderr)."""
    words = [str(arg) for arg in argv]
    capsys.readouterr()
    try:
        code = main(words)
    except SystemExit:  # argparse refused the words themselves
        code = None
    out, err = capsys.readouterr()
    assert code is not None, f"taskcontract does not take `{' '.join(words[:3])}`: {err!r}"
    return code, out, err


def new(capsys, repo: Repo, feature: str = ID, *extra: str):
    return cli(capsys, "new", feature, "--root", repo.root, *extra)


def check(repo: Repo, capsys, *extra: str, feature: str = ID):
    return cli(capsys, "g1-check", feature, "--root", repo.root, *extra)


def summary(g1_3: str, feature: str = ID) -> str:
    return f"{feature}: G1.1 done, G1.2 done, G1.3 {g1_3}"


def rs302(feature: str = ID) -> str:
    return f"{feature}: RS302 {message_9(feature)}"


def reads(repo: Repo, capsys, g1_3: str, *lines: str) -> None:
    """`g1-check` prints exactly these lines (finding lines, then the summary
    line) on stdout, nothing on stderr, and exits 1."""
    code, out, err = check(repo, capsys)
    assert out.splitlines() == [*lines, summary(g1_3)]
    assert (code, err) == (1, "")


def is_green(repo: Repo, capsys) -> None:
    assert check(repo, capsys) == (0, GREEN + "\n", "")


def refused_8(repo: Repo, capsys, feature: str = ID, *extra: str) -> None:
    """`new` refuses: message 8 alone on stderr, nothing on stdout, exit 1, and
    nothing under the root changes."""
    before = repo.snapshot()
    assert new(capsys, repo, feature, *extra) == (1, "", message_8(feature) + "\n")
    assert repo.snapshot() == before, "a refused `new` wrote under the root"
    assert not (repo.root / "specs" / feature).exists()


def normal(path: Path, root: Path) -> str:
    """A contract's text with its root's name (the header comment holds the
    path) replaced, so two roots compare."""
    text = path.read_text(encoding="utf-8")
    return text.replace(root.as_posix(), "<ROOT>").replace(str(root), "<ROOT>")


def reference_contract(tmp_path: Path, feature: str = ID) -> str:
    """The contract `new` writes where G1 is no active gate: a root with no config."""
    other = tmp_path / "reference"
    other.mkdir(exist_ok=True)
    return normal(scaffold(feature, root=other), other)


# --- SC4.1: `new` refuses a feature with no feature document where G1 is active ---------

@pytest.mark.parametrize("feature", [ID, "csv-export", "x-1"])
def test_sc4_1_new_rejects_a_feature_with_no_feature_document_where_g1_is_active(
        bare, capsys, feature):
    refused_8(bare, capsys, feature)


def test_sc4_1_new_takes_its_root_from_the_working_directory_when_none_is_given(
        bare, capsys, tmp_path, monkeypatch):
    before = bare.snapshot()
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    assert cli(capsys, "new", ID, "--root", bare.root) == (1, "", message_8(ID) + "\n")
    monkeypatch.chdir(bare.root)
    assert cli(capsys, "new", ID) == (1, "", message_8(ID) + "\n")
    assert bare.snapshot() == before
    assert not (bare.root / "specs" / ID).exists()


def test_sc4_1_a_design_document_alone_is_no_feature_document(bare, capsys):
    bare.design(4)
    refused_8(bare, capsys)


def test_sc4_1_a_folder_at_the_documents_path_is_no_feature_document(bare, capsys):
    (bare.root / REQUIREMENTS).mkdir(parents=True)
    before = bare.snapshot()
    assert new(capsys, bare) == (1, "", message_8(ID) + "\n")
    assert bare.snapshot() == before
    assert not (bare.root / "specs" / ID).exists()


def test_sc4_1_another_features_document_is_no_document_for_this_feature(bare, capsys):
    assert (bare.root / f"docs/features/{OTHER}.md").is_file()
    refused_8(bare, capsys)
    refused_8(bare, capsys, "csv-export")


@pytest.mark.parametrize("with_design", [False, True], ids=["requirements-alone", "a-pair"])
def test_sc4_1_new_writes_the_contract_as_today_where_a_feature_document_stands(
        bare, capsys, tmp_path, with_design):
    refused_8(bare, capsys)
    bare.requirements(2)
    if with_design:
        bare.design(2)
    code, out, err = new(capsys, bare)
    assert (code, err) == (0, "")
    contract = bare.root / "specs" / ID / "contract.yaml"
    assert out.startswith(f"created {contract}\n")
    assert normal(contract, bare.root) == reference_contract(tmp_path)


@pytest.mark.parametrize("config", [
    pytest.param(None, id="no-config-file"),
    pytest.param({"kit": "fixture"}, id="no-active-gates-key"),
    pytest.param({"active_gates": ["G0"], "g1": {"schemas": [SPECTRAL]}},
                 id="g1-is-no-active-gate"),
    pytest.param({"active_gates": ["G0", "G1"], "g1": {"exempt": [ID]}},
                 id="the-feature-is-exempt"),
])
def test_sc4_1_new_writes_the_contract_as_today_where_g1_is_no_active_gate(
        bare, capsys, tmp_path, config):
    refused_8(bare, capsys)  # the same repository, G1 on and no document
    bare.config(config)
    code, out, err = new(capsys, bare)
    assert (code, err) == (0, "")
    contract = bare.root / "specs" / ID / "contract.yaml"
    assert out.startswith(f"created {contract}\n")
    assert normal(contract, bare.root) == reference_contract(tmp_path)
    assert "no feature document" not in out


def test_sc4_1_new_keeps_its_two_older_refusals_ahead_of_the_new_one(bare, capsys):
    refused_8(bare, capsys)
    # a bad id: today's words, not message 8
    before = bare.snapshot()
    assert new(capsys, bare, "Bad_Id") == (
        1, "", "taskcontract new: id 'Bad_Id' must match ^[a-z][a-z0-9-]{2,63}$\n")
    assert bare.snapshot() == before
    # a contract that exists: today's words, the file as it stood
    contract = bare.write(f"specs/{OTHER}x/contract.yaml", "id: kept\n")
    before = bare.snapshot()
    code, out, err = new(capsys, bare, f"{OTHER}x")
    assert (code, out) == (1, "")
    assert err == (f"taskcontract new: {contract} already exists "
                   f"(contracts are never overwritten)\n")
    assert "no feature document" not in err
    assert bare.snapshot() == before
    assert contract.read_text(encoding="utf-8") == "id: kept\n"


def test_sc4_1_scaffold_refuses_with_a_value_error_that_holds_message_8_less_its_prefix(
        bare):
    prefix = "taskcontract new: "
    assert message_8(ID).startswith(prefix)
    before = bare.snapshot()
    with pytest.raises(ValueError) as caught:
        scaffold(ID, root=bare.root)
    assert str(caught.value) == message_8(ID)[len(prefix):]
    assert bare.snapshot() == before


# The hand-off (ADR 0041, rule 3): each path into intake, taken on to the step `new`
# hands to. A plain request first meets message 8; a document written, `new` scaffolds,
# the contract is filled as intake's I6 fills it, and `g1-record review` records.

@pytest.mark.parametrize("with_design", [False, True], ids=["a-plain-request", "a-pair"])
def test_sc4_1_each_path_into_intake_reaches_g1_record_review_past_new(
        bare, capsys, with_design):
    refused_8(bare, capsys)
    if with_design:
        bare.design(1)  # a design document alone is still no feature document
        refused_8(bare, capsys)
    bare.requirements(1)
    code, out, err = new(capsys, bare)
    assert (code, err) == (0, "")
    contract = bare.root / "specs" / ID / "contract.yaml"
    doc = yaml.safe_load(contract.read_text(encoding="utf-8"))
    doc["scope"] = ["api/", "src/"]
    contract.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    reads(bare, capsys, "to do")
    assert cli(capsys, "g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po",
               "--checked", ALL) == (0, f"{PASSED}\n{RECORDED}\n", "")
    record = bare.records()[-1]
    assert record["requirements"] == "r1"
    assert record.get("design") == ("r1" if with_design else None)
    is_green(bare, capsys)


# --- SC1.2: G1.3 names the missing feature document ----------------------------------------

def test_sc1_2_a_feature_with_no_feature_document_makes_g1_3_read_failed_with_message_9(
        repo, capsys):
    repo.remove(REQUIREMENTS)
    repo.remove(DESIGN)
    before = repo.snapshot()
    reads(repo, capsys, "failed", rs302())
    assert repo.snapshot() == before, "g1-check wrote under the root"


def test_sc1_2_the_json_envelope_holds_one_rs302_finding(repo, capsys):
    repo.remove(REQUIREMENTS)
    code, out, err = check(repo, capsys, "--json")
    assert (code, err) == (1, "")
    assert json.loads(out) == {
        "note": "G1.1 done, G1.2 done, G1.3 failed",
        "findings": [{"feature": ID, "condition": "G1.3", "rule": "RS302",
                      "message": message_9()}]}


def test_sc1_2_message_9_names_the_features_own_id(repo, capsys):
    repo.write(f"specs/{OTHER}/contract.yaml", CONTRACT.format(id=OTHER))
    repo.remove(f"docs/features/{OTHER}.md")
    code, out, err = check(repo, capsys, feature=OTHER)
    assert out.splitlines() == [rs302(OTHER), summary("failed", OTHER)]
    assert (code, err) == (1, "")


def test_sc1_2_a_design_document_alone_is_no_feature_document_for_g1_3(repo, capsys):
    repo.remove(REQUIREMENTS)
    assert (repo.root / DESIGN).is_file()
    reads(repo, capsys, "failed", rs302())


def test_sc1_2_a_folder_at_the_documents_path_is_no_feature_document_for_g1_3(repo, capsys):
    repo.remove(REQUIREMENTS)
    repo.remove(DESIGN)
    (repo.root / REQUIREMENTS).mkdir()
    reads(repo, capsys, "failed", rs302())


@pytest.mark.parametrize("held", [
    pytest.param([], id="no-record"),
    pytest.param([written()], id="a-passing-review"),
    pytest.param([written({6: "Statement"})], id="a-review-with-an-item-unchecked"),
    pytest.param([written({2: "Statement", 8: "Checks"})], id="a-review-with-two-unchecked"),
    pytest.param([written({6: "Statement"}), written()], id="a-later-passing-review"),
])
def test_sc1_2_one_finding_whatever_the_records_hold(repo, capsys, held):
    if held:
        repo.put(*held)
    repo.remove(REQUIREMENTS)
    reads(repo, capsys, "failed", rs302())


def test_sc1_2_each_unchecked_item_is_a_diagnostic_naming_the_item_and_the_section(
        repo, capsys):
    repo.put(written({2: "Statement", 6: "Acceptance criteria, Checks"}))
    reads(repo, capsys, "failed",
          f"{ID}: RS301 {rs301(2, 'Statement')}",
          f"{ID}: RS301 {rs301(6, 'Acceptance criteria, Checks')}")
    # the document goes: one finding, and the item lines go with it
    repo.remove(REQUIREMENTS)
    reads(repo, capsys, "failed", rs302())
    # the document comes back: the review stands, and the item lines with it
    repo.requirements(5)
    reads(repo, capsys, "failed",
          f"{ID}: RS301 {rs301(2, 'Statement')}",
          f"{ID}: RS301 {rs301(6, 'Acceptance criteria, Checks')}")


def test_sc1_2_g1_3_reads_failed_until_the_review_of_a_later_revision_passes(
        repo, capsys):
    repo.remove(REQUIREMENTS)
    repo.remove(DESIGN)
    reads(repo, capsys, "failed", rs302())  # no document: failed, never `to do`
    # the person writes the documents: nothing is reviewed yet
    repo.requirements(5)
    repo.design(4)
    assert check(repo, capsys) == (1, summary("to do") + "\n", "")
    # a review that leaves an item unchecked
    assert cli(capsys, "g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po",
               "--checked", "1,2,3,4,5,7,8,9,10,11", "--unchecked", "6=Statement") == (
        1, f"{rs301(6, 'Statement')}\n{RECORDED}\n", "")
    reads(repo, capsys, "failed", f"{ID}: RS301 {rs301(6, 'Statement')}")
    # the document is gone again: the missing document is the finding
    repo.remove(REQUIREMENTS)
    reads(repo, capsys, "failed", rs302())
    # a later revision, and a review of it that passes
    repo.requirements(6)
    repo.design(5)
    reads(repo, capsys, "failed", f"{ID}: RS301 {rs301(6, 'Statement')}")
    assert cli(capsys, "g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po",
               "--checked", ALL) == (0, f"{PASSED}\n{RECORDED}\n", "")
    assert (repo.records()[-1]["requirements"], repo.records()[-1]["design"]) == ("r6", "r5")
    is_green(repo, capsys)
    # a passing review does not outlive its document
    repo.remove(REQUIREMENTS)
    reads(repo, capsys, "failed", rs302())


def test_sc1_2_the_review_writer_keeps_its_refusal_and_g1_check_names_the_way_out(
        repo, capsys):
    repo.remove(REQUIREMENTS)
    repo.remove(DESIGN)
    before = repo.snapshot()
    code, out, err = cli(capsys, "g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po",
                         "--checked", ALL)
    assert (code, out) == (2, "")
    assert len(err.splitlines()) == 1 and REQUIREMENTS in err
    assert repo.snapshot() == before
    reads(repo, capsys, "failed", rs302())  # the line names the way out


def test_sc1_2_g1_check_reads_g1_off_as_it_did_with_no_document(repo, capsys):
    repo.remove(REQUIREMENTS)
    reads(repo, capsys, "failed", rs302())
    repo.config({"active_gates": ["G0"]})
    assert check(repo, capsys) == (2, "", f"{ID}: G1 is not active\n")
    repo.config({"active_gates": ["G0", "G1"], "g1": {"exempt": [ID]}})
    assert check(repo, capsys) == (2, "", f"{ID}: G1 is not active\n")


def test_sc1_2_gates_yaml_lists_both_rules_g1_3_owns():
    gates = yaml.safe_load((PACKAGE / "data" / "gates.yaml").read_text(encoding="utf-8"))
    gate = next(g for g in gates["gates"] if g["id"] == "G1")
    rules = {c["id"]: c.get("rules") for c in gate["conditions"]}
    assert rules["G1.3"] == ["RS301", "RS302"]
    assert rules["G1.1"] == ["RS101", "RS102"]
    assert rules["G1.2"] == ["RS201", "RS202", "RS203"]


def test_sc1_2_the_kits_own_feature_with_no_document_reads_g1_3_failed(capsys):
    """Risk 11: `glossary-alias-disjointness` is parked, G1 is active for it and no
    document stands. RS302 reports where a document is absent, and only there."""
    feature = "glossary-alias-disjointness"
    assert (ROOT / "specs" / feature / "contract.yaml").is_file()
    held = (ROOT / "docs" / "features" / f"{feature}.md").is_file()
    code, out, err = cli(capsys, "g1-check", feature, "--root", ROOT)
    lines = out.splitlines()
    assert (rs302(feature) in lines) == (not held), lines
    if not held:
        assert (code, err) == (1, "")
        assert lines[-1].endswith("G1.3 failed"), lines[-1]


# --- SC1.2: the tree shows what g1-check shows --------------------------------------------

def tree_lines(repo: Repo, capsys) -> list[str]:
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0, err
    return out.splitlines()


@pytest.mark.parametrize("held", [
    pytest.param([], id="no-record"),
    pytest.param([written()], id="a-passing-review"),
    pytest.param([written({6: "Statement"})], id="a-review-with-an-item-unchecked"),
])
def test_sc1_2_the_tree_shows_g1_3_failed_with_message_9_as_its_one_diagnostic(
        repo, capsys, held):
    if held:
        repo.put(*held)
    repo.remove(REQUIREMENTS)
    repo.remove(DESIGN)
    lines = tree_lines(repo, capsys)
    wanted = f"    {ID}/G1/G1.3 {G1_3_ROW} [failed]"
    at = [n for n, line in enumerate(lines) if line.startswith(wanted)]
    assert len(at) == 1, f"no G1.3 row [failed] for {ID}"
    assert lines[at[0] + 1] == f"      - {message_9()}"
    assert not lines[at[0] + 2].startswith("      - "), "a second diagnostic under G1.3"
    # the roll-up: G1.1 and G1.2 done, G1.3 failed
    assert f"  {ID}/G1 Requirements / Spec [failed]" in lines
    if not held:
        assert lines[at[0]] == wanted


def test_sc1_2_the_tree_reads_g1_3_as_g1_check_reads_it_once_the_document_stands(
        repo, capsys):
    repo.remove(REQUIREMENTS)
    lines = tree_lines(repo, capsys)
    assert f"      - {message_9()}" in lines
    repo.requirements(5)
    lines = tree_lines(repo, capsys)
    assert f"    {ID}/G1/G1.3 {G1_3_ROW} [to do]" in lines
    assert f"      - {message_9()}" not in lines


# --- the two flows: intake's I3 and the venue's R5 ------------------------------------------

def step(text: str, label: str) -> str:
    """One step of a flow: from its label at a line's start to the next step's
    label, or to the close of the instructions block."""
    found = re.search(rf"^{label}\. ", text, re.MULTILINE)
    if not found:
        return ""
    rest = text[found.start():]
    end = re.search(r"\n\n[A-Z]+\d+\. |\n</instructions>", rest)
    return rest[:end.start()] if end else rest


I3_TODAY = ("I3. SCAFFOLD - one Bash call: `python -m taskcontract new {id}`. If it fails "
            "because the contract already exists, ASK before touching anything - existing "
            "contracts are never silently edited.")
I3_CLAUSE = " On any other failure, REPORT its line verbatim, write nothing, and return to the conversation."


def test_sc4_1_intake_i3_reports_any_other_failure_of_new_and_returns_to_the_conversation():
    text = INTAKE.read_text(encoding="utf-8")
    i3 = step(text, "I3")
    assert i3 == I3_TODAY + I3_CLAUSE
    # the clause names no G1 word, no config file and no command: I9's tests stand
    clause = i3[len(I3_TODAY):]
    assert "G1" not in clause and ".sdlc" not in clause and "python" not in clause
    assert text.count("python -m taskcontract new") == 1
    assert len(text) < 12_000


R5_SENTENCE = ("Where `docs/features/{id}.md` is no file, ASK no item and go on to R7, "
               "which names the way out.")


def test_sc1_2_g1_flow_r5_asks_no_item_where_the_feature_has_no_feature_document():
    text = G1_FLOW.read_text(encoding="utf-8")
    r5 = step(text, "R5")
    assert R5_SENTENCE in r5
    assert text.count(R5_SENTENCE) == 1
    # the venue still asks the 11 items, one at a time, and R7 still reads the verdict
    assert "one at a time" in r5 and "11 items" in r5
    assert "g1-check" in step(text, "R7")
    assert len(text) < 12_000


# --- done_means: kit 0.22.1 ships the fix ---------------------------------------------------

def version_of(path: Path, pattern: str) -> tuple[int, ...]:
    found = re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE)
    assert found, f"no version in {path.name}"
    return tuple(int(part) for part in found.group(1).split("."))


def test_done_means_the_kit_version_reads_0_22_1_or_later_and_both_places_agree():
    # a floor, never the literal: the next release moves both numbers
    project = version_of(PYPROJECT, r'^version\s*=\s*"(\d+\.\d+\.\d+)"')
    kit = version_of(INIT, r'^KIT_VERSION\s*=\s*"(\d+\.\d+\.\d+)"')
    assert project >= (0, 22, 1)
    assert kit == project


def test_done_means_the_changelog_holds_a_dated_0_22_1_entry_above_0_22_0():
    headings = [line.rstrip() for line in CHANGELOG.read_text(encoding="utf-8").splitlines()
                if line.startswith("## ")]
    fixed = [n for n, h in enumerate(headings)
             if re.match(r"## 0\.22\.1 - \d{4}-\d{2}-\d{2}\b", h)]
    old = [n for n, h in enumerate(headings) if h.startswith("## 0.22.0 - ")]
    assert len(fixed) == 1, "no entry heads 0.22.1"
    assert old and fixed[0] < old[0]
