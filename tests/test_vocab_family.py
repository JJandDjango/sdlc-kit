"""The /sdlc vocab family engines (ADR 0017 V5) + audit integration.

vocab-add mirrors `new`: a deliberately red skeleton (VT002 on the TODO
definition) born draft. vocab-list is computed at call time - no stored
index exists to drift. The kit's own specs/vocabulary/ is the brownfield
extraction's first fixture: door-green, core nouns ratified, every term
carrying sources provenance.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from taskcontract.__main__ import main
from taskcontract.vocabulary import (
    list_terms,
    load_glossary_schema,
    scaffold_term,
    validate_term_path,
    validate_vocab_root,
)

REPO = Path(__file__).resolve().parent.parent
SCHEMA = load_glossary_schema()

BROKEN = """\
term: broken
name: Broken
definition: short
kind: entity
status: draft
since: 2026-07-28
"""

WARNED_CONTRACT = """\
id: warned
intent: >-
  Reference a deprecated term inside its sunset window so the audit
  reports the warning as informational, never as invalid.
scope:
  - taskcontract/
non_goals:
  - Gating on warnings
decomposition:
  - unit: warn
    done_means: the join warns without gating
    acceptance_sketch:
      - audit reports CONTRACT-WARNED
dependencies: []
provenance:
  origin: human-request
entities:
  - fading-term
"""

FADING = """\
term: fading-term
name: Fading term
definition: A deprecated term whose sunset window is still open for migration.
kind: entity
status: deprecated
since: 2026-07-28
sunset: 2999-01-01
"""


def test_vocab_add_round_trip_fill_then_green(tmp_path):
    path = scaffold_term("billing-account", root=tmp_path)
    assert path == tmp_path / "specs" / "vocabulary" / "billing-account.yaml"

    rules = {v.rule for v in validate_term_path(path, schema_doc=SCHEMA)}
    assert rules == {"VT002"}, "fresh skeleton must be red on exactly the definition tripwire"

    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    doc["name"] = "Billing account"
    doc["definition"] = ("The payer-facing account that invoices bill against; "
                         "one per customer, never shared across tenants.")
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    assert validate_term_path(path, schema_doc=SCHEMA) == []
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert doc["status"] == "draft", "day-2 terms are born draft, never ratified"


def test_vocab_add_rejects_bad_and_reserved_slugs(tmp_path):
    with pytest.raises(ValueError):
        scaffold_term("Bad_Slug", root=tmp_path)
    with pytest.raises(ValueError):
        scaffold_term("constraints", root=tmp_path)
    assert not (tmp_path / "specs").exists()


def test_vocab_add_refuses_clobber(tmp_path):
    scaffold_term("billing-account", root=tmp_path)
    with pytest.raises(FileExistsError):
        scaffold_term("billing-account", root=tmp_path)


def test_cli_vocab_add_exit_codes(tmp_path, capsys):
    assert main(["vocab-add", "billing-account", "--root", str(tmp_path)]) == 0
    assert "created" in capsys.readouterr().out
    assert main(["vocab-add", "billing-account", "--root", str(tmp_path)]) == 1
    assert "already exists" in capsys.readouterr().err


def test_vocab_list_computes_rows_and_names_unreadables(tmp_path):
    scaffold_term("beta-term", root=tmp_path)
    scaffold_term("alpha-term", root=tmp_path)
    vocab = tmp_path / "specs" / "vocabulary"
    (vocab / "garbage.yaml").write_text("{[", encoding="utf-8")

    rows, unreadable = list_terms(tmp_path)
    assert [r[0] for r in rows] == ["alpha-term", "beta-term"]
    assert all(r[2] == "draft" for r in rows)
    assert [p.name for p in unreadable] == ["garbage.yaml"]


def test_cli_vocab_list_output(tmp_path, capsys):
    assert main(["vocab-list", "--root", str(tmp_path)]) == 0
    assert "terms: 0" in capsys.readouterr().out

    scaffold_term("billing-account", root=tmp_path)
    assert main(["vocab-list", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "billing-account" in out
    assert "terms: 1 (ratified 0, draft 1, deprecated 0)" in out


def test_kit_vocabulary_is_the_extraction_fixture():
    violations, count = validate_vocab_root(REPO)
    assert violations == []
    assert count >= 10

    rows, unreadable = list_terms(REPO)
    assert unreadable == []
    ratified = {r[0] for r in rows if r[2] == "ratified"}
    assert {"task-contract", "gate", "vocabulary-term"} <= ratified

    vocab = REPO / "specs" / "vocabulary"
    for row in rows:
        doc = yaml.safe_load((vocab / f"{row[0]}.yaml").read_text(encoding="utf-8"))
        assert doc.get("sources"), f"{row[0]} lacks extraction provenance"


def test_audit_reports_vocab_invalid(tmp_path, skill_audit):
    (tmp_path / ".sdlc").mkdir()
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir(parents=True)
    (vocab / "broken.yaml").write_text(BROKEN, encoding="utf-8")

    findings, is_spine = skill_audit.audit(tmp_path)
    assert is_spine
    vocab_findings = [f for f in findings if f.code == "VOCAB-INVALID"]
    assert vocab_findings
    assert vocab_findings[0].severity == "ERROR"
    assert "VT002" in vocab_findings[0].message
    assert "CONTRACT-ORPHAN" not in {f.code for f in findings}, \
        "specs/vocabulary/ is the glossary, never an orphaned task dir"


def test_audit_reports_warned_contract_as_info(tmp_path, skill_audit):
    (tmp_path / ".sdlc").mkdir()
    contract_dir = tmp_path / "specs" / "warned"
    contract_dir.mkdir(parents=True)
    (contract_dir / "contract.yaml").write_text(WARNED_CONTRACT, encoding="utf-8")
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir()
    (vocab / "fading-term.yaml").write_text(FADING, encoding="utf-8")

    findings, _ = skill_audit.audit(tmp_path)
    codes = {f.code for f in findings}
    assert "CONTRACT-WARNED" in codes
    assert "CONTRACT-INVALID" not in codes
    warned = next(f for f in findings if f.code == "CONTRACT-WARNED")
    assert warned.severity == "INFO"
    assert "W001" in warned.message
