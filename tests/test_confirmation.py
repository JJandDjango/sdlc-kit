"""Unit-confirmation suite for ADR 0025 (G0.3, TC016).

The schema admits `confirmed_by` (1.3.0, optional); the checker decides
whether it is demanded. The rule is armed only by a *ratified*
`intake-seat` term in the sibling vocabulary, runs at the ready profile
only, and never sees a loose file - the coverage join's three habits,
inherited on purpose.
"""

from __future__ import annotations

import yaml

from taskcontract.__main__ import main
from taskcontract.checker import validate_path

INTENT = ("Every unit records the seats that answered for it at intake, "
          "and the ready door checks the record against the seat term.")


def _unit(uid, confirmed_by=None):
    unit = {
        "unit": "work for " + uid,
        "id": uid,
        "done_means": "the work for " + uid + " is done",
        "acceptance_sketch": ["verify " + uid + " behaves"],
    }
    if confirmed_by is not None:
        unit["confirmed_by"] = confirmed_by
    return unit


def _doc(units):
    return {
        "id": "seat-case",
        "intent": INTENT,
        "scope": ["taskcontract/"],
        "non_goals": ["No author check"],
        "decomposition": units,
        "dependencies": [],
        "provenance": {"origin": "human-request"},
    }


def _tree(tmp_path, units, term_status=None, values=("po", "engineer")):
    """specs/seat-case/contract.yaml plus, when term_status is given, the seat term."""
    contract = tmp_path / "specs" / "seat-case" / "contract.yaml"
    contract.parent.mkdir(parents=True)
    contract.write_text(yaml.safe_dump(_doc(units), sort_keys=False), encoding="utf-8")
    if term_status is not None:
        vocab = tmp_path / "specs" / "vocabulary"
        vocab.mkdir()
        (vocab / "intake-seat.yaml").write_text(yaml.safe_dump({
            "term": "intake-seat",
            "name": "Intake seat",
            "definition": "A human position that answers for a decomposition unit at intake.",
            "kind": "value-set",
            "values": list(values),
            "status": term_status,
            "since": "2026-08-26",
        }, sort_keys=False), encoding="utf-8")
    return contract


def _findings(path, profile="ready"):
    return [v for v in validate_path(path, profile=profile) if v.rule == "TC016"]


# --- armed: the ratified term demands an answer per unit --------------------

def test_unit_without_confirmed_by_is_tc016_naming_the_unit(tmp_path):
    path = _tree(tmp_path, [_unit("alpha", ["po"]), _unit("beta")], term_status="ratified")
    found = _findings(path)
    assert [v.path for v in found] == ["$.decomposition[1]"]
    assert "'beta'" in found[0].message
    assert "intake-seat" in found[0].message


def test_seat_the_term_lacks_is_tc016_naming_the_seat(tmp_path):
    path = _tree(tmp_path, [_unit("alpha", ["po", "qa"])], term_status="ratified")
    found = _findings(path)
    assert [v.path for v in found] == ["$.decomposition[0].confirmed_by[1]"]
    assert "'qa'" in found[0].message
    assert "po" in found[0].message  # the roster rides the diagnostic


def test_every_unit_confirmed_by_listed_seats_is_green(tmp_path):
    path = _tree(tmp_path, [_unit("alpha", ["po", "engineer"]), _unit("beta", ["engineer"])],
                 term_status="ratified")
    assert validate_path(path, profile="ready") == []


# --- inactive: no term, draft term, draft profile, loose file ---------------

def test_tree_with_no_seat_term_is_green(tmp_path):
    path = _tree(tmp_path, [_unit("alpha")])
    assert validate_path(path, profile="ready") == []


def test_draft_seat_term_leaves_the_check_inactive(tmp_path):
    path = _tree(tmp_path, [_unit("alpha")], term_status="draft")
    assert validate_path(path, profile="ready") == []


def test_draft_profile_never_runs_the_rule(tmp_path):
    path = _tree(tmp_path, [_unit("alpha")], term_status="ratified")
    assert _findings(path, profile="draft") == []
    assert _findings(path, profile="ready")  # the same tree is red at ready


def test_loose_file_never_enters_the_join(tmp_path):
    _tree(tmp_path, [_unit("alpha")], term_status="ratified")
    loose = tmp_path / "contract.yaml"
    loose.write_text(yaml.safe_dump(_doc([_unit("alpha")]), sort_keys=False), encoding="utf-8")
    assert validate_path(loose, profile="ready") == []


# --- the CLI speaks the verdict contract ------------------------------------

def test_cli_exit_is_red_when_armed_and_unanswered(tmp_path, capsys):
    path = _tree(tmp_path, [_unit("alpha")], term_status="ratified")
    assert main(["validate", str(path), "--profile", "ready"]) == 1
    assert "TC016" in capsys.readouterr().out
