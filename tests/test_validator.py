"""Golden-fixture regression suite for the taskcontract validator (ADR 0006).

Every invalid fixture is named for the TCnnn rule it must trigger; the
enforcement layer carries its own regression suite (THEORY; PL-PIPE.2).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taskcontract.__main__ import main
from taskcontract.checker import load_schema, validate_path

FIXTURES = Path(__file__).parent / "fixtures"
VALID = sorted((FIXTURES / "valid").glob("*.yaml"))
INVALID = sorted((FIXTURES / "invalid").glob("*.yaml"))
SCHEMA = load_schema()


@pytest.mark.parametrize("fixture", VALID, ids=lambda p: p.stem)
def test_valid_fixtures_pass_ready(fixture):
    assert validate_path(fixture, profile="ready", schema_doc=SCHEMA) == []


@pytest.mark.parametrize("fixture", INVALID, ids=lambda p: p.stem)
def test_invalid_fixtures_fail_with_named_rule(fixture):
    expected = fixture.stem[:5].upper()
    violations = validate_path(fixture, profile="ready", schema_doc=SCHEMA)
    assert violations, f"{fixture.stem} unexpectedly clean"
    assert expected in {v.rule for v in violations}


def test_tc003_names_dependency_and_blocker():
    fixture = FIXTURES / "invalid" / "tc003-blocked-dependency.yaml"
    violations = validate_path(fixture, profile="ready", schema_doc=SCHEMA)
    tc003 = [v for v in violations if v.rule == "TC003"]
    assert tc003
    assert "schema-migration" in tc003[0].message
    assert "auth-rework" in tc003[0].message


def test_blocked_dependency_is_draft_legal():
    fixture = FIXTURES / "invalid" / "tc003-blocked-dependency.yaml"
    assert validate_path(fixture, profile="draft", schema_doc=SCHEMA) == []


def test_cli_exit_codes(capsys):
    assert main(["validate", str(VALID[0])]) == 0
    assert f"ready-green: {VALID[0]}" in capsys.readouterr().out
    assert main(["validate", str(INVALID[-1])]) == 1
    assert capsys.readouterr().out.strip()
