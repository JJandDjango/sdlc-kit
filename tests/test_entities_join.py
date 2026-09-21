"""The G0 coverage join (ADR 0017 V3): entities resolve ratified-only.

Join semantics live on tmp specs trees - a contract at
specs/<id>/contract.yaml with a sibling specs/vocabulary/. Ratified
resolves silently; missing forks (TC010); draft does not resolve
(TC011); deprecated warns inside its sunset window (W001, non-gating)
and errors past it (TC012). Loose files - the golden fixtures - never
enter the join. At ready the field itself is required (ADR 0030): a
contract with none fails TC017, in a specs tree or out of it, and the
empty list is a declaration that joins against nothing.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taskcontract.__main__ import main
from taskcontract.checker import TC017_MESSAGE, validate_path

RATIFIED = """\
term: gate
name: Gate
definition: A checkpoint in the delivery pipeline that enforces conditions before work proceeds.
kind: entity
status: ratified
since: 2026-07-28
"""

DRAFT = """\
term: draft-term
name: Draft term
definition: A term still awaiting its one cheap human ratification action.
kind: entity
status: draft
since: 2026-07-28
"""

DEPRECATED_IN_WINDOW = """\
term: fading-term
name: Fading term
definition: A deprecated term whose sunset window is still open for migration.
kind: entity
status: deprecated
since: 2026-07-28
sunset: 2999-01-01
"""

DEPRECATED_PAST = """\
term: dead-term
name: Dead term
definition: A deprecated term whose sunset date is long past and must not resolve.
kind: entity
status: deprecated
since: 2000-01-01
sunset: 2000-06-01
"""

CONTRACT = """\
id: join-case
intent: >-
  Exercise the coverage join against the vocabulary sitting beside this
  contract in its tmp specs tree, resolving every declared entity.
scope:
  - taskcontract/
non_goals:
  - Anything beyond the join
decomposition:
  - unit: join
    id: join
    done_means: the declared entities resolve per ADR 0017 V3
    acceptance_sketch:
      - resolution behaves per term status
dependencies: []
provenance:
  origin: human-request
entities:
{entities}
"""


def _tree(tmp_path, entities, terms):
    contract_dir = tmp_path / "specs" / "join-case"
    contract_dir.mkdir(parents=True)
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir()
    for stem, text in terms.items():
        (vocab / f"{stem}.yaml").write_text(text, encoding="utf-8")
    lines = "\n".join(f"  - {e}" for e in entities)
    contract = contract_dir / "contract.yaml"
    contract.write_text(CONTRACT.format(entities=lines), encoding="utf-8")
    return contract


def test_ratified_refs_resolve_green(tmp_path):
    contract = _tree(tmp_path, ["gate"], {"gate": RATIFIED})
    assert validate_path(contract, profile="ready") == []


def test_missing_term_forks_tc010(tmp_path):
    contract = _tree(tmp_path, ["gate", "unheard-of"], {"gate": RATIFIED})
    violations = validate_path(contract, profile="ready")
    rules = {v.rule for v in violations}
    assert rules == {"TC010"}
    assert "unheard-of" in violations[0].message
    assert "fork a vocabulary task" in violations[0].message


def test_draft_does_not_resolve_tc011(tmp_path):
    contract = _tree(tmp_path, ["draft-term"], {"draft-term": DRAFT})
    violations = validate_path(contract, profile="ready")
    assert {v.rule for v in violations} == {"TC011"}
    assert "draft-term" in violations[0].message


def test_deprecated_in_window_warns_not_gates(tmp_path, capsys):
    contract = _tree(tmp_path, ["fading-term"],
                     {"fading-term": DEPRECATED_IN_WINDOW})
    violations = validate_path(contract, profile="ready")
    assert [v.rule for v in violations] == ["W001"]
    assert violations[0].severity == "warning"
    assert main(["validate", str(contract), "--profile", "ready"]) == 0
    out = capsys.readouterr().out
    assert "W001" in out
    assert "ready-green" in out


def test_deprecated_past_sunset_errors_tc012(tmp_path):
    contract = _tree(tmp_path, ["dead-term"], {"dead-term": DEPRECATED_PAST})
    violations = validate_path(contract, profile="ready")
    assert {v.rule for v in violations} == {"TC012"}


def test_no_vocabulary_directory_means_every_ref_forks(tmp_path):
    contract_dir = tmp_path / "specs" / "join-case"
    contract_dir.mkdir(parents=True)
    contract = contract_dir / "contract.yaml"
    contract.write_text(
        CONTRACT.format(entities="  - gate"), encoding="utf-8")
    violations = validate_path(contract, profile="ready")
    assert {v.rule for v in violations} == {"TC010"}


def test_draft_profile_skips_the_join(tmp_path):
    contract = _tree(tmp_path, ["unheard-of"], {"gate": RATIFIED})
    assert validate_path(contract, profile="draft") == []


NO_ENTITIES = CONTRACT.replace("entities:\n{entities}\n", "")
EMPTY_ENTITIES = CONTRACT.replace("entities:\n{entities}\n", "entities: []\n")


def test_contract_without_entities_fails_tc017(tmp_path):
    """ADR 0030, SC1.1: at ready the declaration is required; silence is a miss."""
    contract_dir = tmp_path / "specs" / "join-case"
    contract_dir.mkdir(parents=True)
    contract = contract_dir / "contract.yaml"
    contract.write_text(NO_ENTITIES, encoding="utf-8")
    (tmp_path / "specs" / "vocabulary").mkdir()
    (tmp_path / "specs" / "vocabulary" / "gate.yaml").write_text(RATIFIED, encoding="utf-8")
    violations = validate_path(contract, profile="ready")
    assert [v.rule for v in violations] == ["TC017"]
    assert violations[0].path == "$"
    assert violations[0].message == TC017_MESSAGE  # the request's words, verbatim
    assert "entities" in violations[0].message
    assert "`entities: []`" in violations[0].message  # names the empty-list option
    # The draft profile is unchanged: a parked contract may carry no field.
    assert validate_path(contract, profile="draft") == []


def test_empty_entities_is_a_declaration(tmp_path):
    """ADR 0030, SC1.2: `entities: []` validates ready and joins against nothing."""
    contract_dir = tmp_path / "specs" / "join-case"
    contract_dir.mkdir(parents=True)
    contract = contract_dir / "contract.yaml"
    contract.write_text(EMPTY_ENTITIES, encoding="utf-8")
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir()
    (vocab / "gate.yaml").write_text(RATIFIED, encoding="utf-8")
    (vocab / "draft-term.yaml").write_text(DRAFT, encoding="utf-8")
    assert validate_path(contract, profile="ready") == []
    assert validate_path(contract, profile="draft") == []


def test_loose_file_without_entities_fails_tc017(tmp_path):
    """The requirement lives in the schema, so a contract outside a specs tree cannot skip it."""
    loose = tmp_path / "contract.yaml"
    loose.write_text(NO_ENTITIES, encoding="utf-8")
    assert [v.rule for v in validate_path(loose, profile="ready")] == ["TC017"]


def test_loose_files_never_join():
    fixture = Path(__file__).parent / "fixtures" / "valid" / "entities-declared.yaml"
    assert validate_path(fixture, profile="ready") == []
