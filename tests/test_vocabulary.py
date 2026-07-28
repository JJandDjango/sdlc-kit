"""Golden-fixture suite for the vocabulary door (ADR 0017 V1).

Invalid fixtures are named for the VTnnn rule they must trigger - the
contract suite's discipline. Directory-scoped semantics (VT009 relation
resolution, vacuous green, the reserved registry filename) are proven
on tmp trees, and the schemas-inside-the-package property that keeps
non-editable installs working is pinned here.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taskcontract import checker, vocabulary
from taskcontract.__main__ import main
from taskcontract.vocabulary import (
    load_glossary_schema,
    validate_term_path,
    validate_vocab_root,
)

FIXTURES = Path(__file__).parent / "fixtures" / "vocab"
VALID = sorted((FIXTURES / "valid").glob("*.yaml"))
INVALID = sorted((FIXTURES / "invalid").glob("*.yaml"))
SCHEMA = load_glossary_schema()

GATE = """\
term: gate
name: Gate
definition: A checkpoint in the delivery pipeline that enforces conditions before work proceeds.
kind: entity
status: ratified
since: 2026-07-28
"""

ORPHAN = """\
term: orphan
name: Orphan
definition: A term whose relation points at nothing, proving reference integrity bites.
kind: entity
relations:
  is_a:
    - missing-term
status: draft
since: 2026-07-28
"""


def _vocab_tree(tmp_path, **files):
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir(parents=True)
    for stem, text in files.items():
        (vocab / f"{stem}.yaml").write_text(text, encoding="utf-8")
    return vocab


@pytest.mark.parametrize("fixture", VALID, ids=lambda p: p.stem)
def test_valid_terms_pass(fixture):
    assert validate_term_path(fixture, schema_doc=SCHEMA) == []


@pytest.mark.parametrize("fixture", INVALID, ids=lambda p: p.stem)
def test_invalid_terms_fail_with_named_rule(fixture):
    expected = fixture.stem[:5].upper()
    violations = validate_term_path(fixture, schema_doc=SCHEMA)
    assert violations, f"{fixture.stem} unexpectedly clean"
    assert expected in {v.rule for v in violations}


def test_valid_set_is_reference_closed():
    known = {p.stem for p in VALID}
    for fixture in VALID:
        assert validate_term_path(fixture, schema_doc=SCHEMA, known_terms=known) == []


def test_absent_directory_is_vacuously_green(tmp_path):
    assert validate_vocab_root(tmp_path, schema_doc=SCHEMA) == ([], 0)


def test_relation_refs_resolve_across_the_directory(tmp_path):
    _vocab_tree(tmp_path, gate=GATE, orphan=ORPHAN)
    violations, count = validate_vocab_root(tmp_path, schema_doc=SCHEMA)
    assert count == 2
    vt009 = [v for v in violations if v.rule == "VT009"]
    assert vt009
    assert "missing-term" in vt009[0].message


def test_single_file_mode_skips_ref_resolution(tmp_path):
    vocab = _vocab_tree(tmp_path, orphan=ORPHAN)
    assert validate_term_path(vocab / "orphan.yaml", schema_doc=SCHEMA) == []


def test_constraints_yaml_is_reserved_for_the_registry(tmp_path):
    registry = (
        "class: E\n"
        "constraints:\n"
        "  - id: sample-join\n"
        "    kind: reference-integrity\n"
        "    subjects:\n"
        "      - gate\n"
        "    check: sample check pointer\n"
        "    status: specified\n"
    )
    _vocab_tree(tmp_path, gate=GATE, constraints=registry)
    violations, count = validate_vocab_root(tmp_path, schema_doc=SCHEMA)
    assert violations == []
    assert count == 1, "the registry is judged by its own schema, never counted as a term"


def test_schemas_ship_inside_the_package():
    pkg = Path(checker.__file__).resolve().parent
    for schema_path in (checker.SCHEMA_PATH, vocabulary.GLOSSARY_SCHEMA_PATH):
        assert schema_path.is_file()
        assert pkg in schema_path.parents


def test_cli_vocab_check_exit_codes(tmp_path, capsys):
    assert main(["vocab-check", "--root", str(tmp_path)]) == 0
    assert "vocab-green" in capsys.readouterr().out
    _vocab_tree(tmp_path, gate=GATE.replace("kind: entity", "kind: verb"))
    assert main(["vocab-check", "--root", str(tmp_path)]) == 1
    assert "VT002" in capsys.readouterr().out


def test_kit_repo_vocabulary_green():
    root = Path(__file__).resolve().parent.parent
    assert main(["vocab-check", "--root", str(root)]) == 0
