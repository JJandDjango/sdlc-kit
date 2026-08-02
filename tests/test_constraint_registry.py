"""The constraint registry (ADR 0017 V6): schema, VC diagnostics, census.

Born non-empty in this repo: the four pre-existing pipeline joins
enumerated retroactively plus the live coverage join. Reference
integrity binds subjects to term files; the class-E marking is
machine-readable in the file itself.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from taskcontract.__main__ import main
from taskcontract.vocabulary import registry_size, validate_constraints, validate_vocab_root

REPO = Path(__file__).resolve().parent.parent

GATE = """\
term: gate
name: Gate
definition: A checkpoint in the delivery pipeline that enforces conditions before work proceeds.
kind: entity
status: ratified
since: 2026-07-28
"""

MINIMAL = """\
class: E
constraints:
  - id: sample-join
    kind: reference-integrity
    subjects:
      - gate
    check: sample check pointer
    status: specified
"""


def _tree(tmp_path, registry, with_gate=True):
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir(parents=True)
    if with_gate:
        (vocab / "gate.yaml").write_text(GATE, encoding="utf-8")
    (vocab / "constraints.yaml").write_text(registry, encoding="utf-8")
    return tmp_path


def test_kit_registry_is_born_non_empty():
    violations, _count = validate_vocab_root(REPO)
    assert violations == []
    assert registry_size(REPO) == 6

    doc = yaml.safe_load(
        (REPO / "specs" / "vocabulary" / "constraints.yaml").read_text(encoding="utf-8"))
    assert doc["class"] == "E"
    by_id = {c["id"]: c for c in doc["constraints"]}
    assert {"entities-coverage", "g4-3-criterion-traceability", "g4-6-write-surface",
            "fixes-resolution", "g10-1-coherence"} <= set(by_id)
    assert by_id["entities-coverage"]["status"] == "enforced"


def test_minimal_registry_green(tmp_path):
    root = _tree(tmp_path, MINIMAL)
    assert validate_constraints(root) == []


def test_unknown_subject_vc002(tmp_path):
    root = _tree(tmp_path, MINIMAL.replace("- gate", "- unheard-of"))
    violations = validate_constraints(root)
    assert {v.rule for v in violations} == {"VC002"}
    assert "unheard-of" in violations[0].message


def test_duplicate_id_vc003(tmp_path):
    doubled = MINIMAL + MINIMAL[MINIMAL.index("  - id:"):]
    root = _tree(tmp_path, doubled)
    violations = validate_constraints(root)
    assert "VC003" in {v.rule for v in violations}


def test_schema_violations_vc001(tmp_path):
    root = _tree(tmp_path, MINIMAL.replace("class: E", "class: S"))
    rules = {v.rule for v in validate_constraints(root)}
    assert rules == {"VC001"}

    root2 = _tree(tmp_path / "second", MINIMAL.replace("    kind: reference-integrity\n", ""))
    rules2 = {v.rule for v in validate_constraints(root2)}
    assert "VC001" in rules2


def test_unreadable_registry_vc000(tmp_path):
    root = _tree(tmp_path, "{[")
    violations = validate_constraints(root)
    assert [v.rule for v in violations] == ["VC000"]


def test_registry_without_terms_fails_reference_integrity(tmp_path):
    root = _tree(tmp_path, MINIMAL, with_gate=False)
    violations, count = validate_vocab_root(root)
    assert count == 0
    assert "VC002" in {v.rule for v in violations}


def test_cli_reports_registry_in_the_green_line(capsys):
    assert main(["vocab-check", "--root", str(REPO)]) == 0
    assert "registry 6 constraints" in capsys.readouterr().out


def test_audit_reports_registry_errors_as_vocab_invalid(tmp_path, skill_audit):
    (tmp_path / ".sdlc").mkdir()
    _tree(tmp_path, MINIMAL.replace("- gate", "- unheard-of"))
    findings, _ = skill_audit.audit(tmp_path)
    vocab_findings = [f for f in findings if f.code == "VOCAB-INVALID"]
    assert vocab_findings
    assert "VC002" in vocab_findings[0].message
