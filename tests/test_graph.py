"""Unit-graph suite for ADR 0024.

The schema declares the fields (`id` required, `depends_on` optional);
the checker decides the graph. Graph validity - duplicate ids,
reference resolution, acyclicity - is a Python-side ready check, the
same category as 0017's entities join, and it fires in both profiles
because a cycle is malformed at draft too.
"""

from __future__ import annotations

import yaml

from taskcontract.checker import load_schema, validate_path

INTENT = ("Unit order is declared in the contract and checked at the door, "
          "so the decomposition can be read as a shape rather than a list.")


def _doc(units):
    return {
        "id": "graph-case",
        "intent": INTENT,
        "scope": ["taskcontract/"],
        "non_goals": ["No scheduling"],
        "decomposition": units,
        "dependencies": [],
        "provenance": {"origin": "human-request"},
    }


def _unit(uid, depends_on=None):
    unit = {
        "unit": "work for " + uid,
        "id": uid,
        "done_means": "the work for " + uid + " is done",
        "acceptance_sketch": ["verify " + uid + " behaves"],
    }
    if depends_on is not None:
        unit["depends_on"] = depends_on
    return unit


def _write(tmp_path, doc):
    path = tmp_path / "contract.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def _rules(tmp_path, units, profile="ready"):
    return {v.rule for v in validate_path(_write(tmp_path, _doc(units)), profile=profile)}


# --- schema surface (unit schema-1-2-0) ------------------------------------

def test_schema_version_is_1_2_0():
    assert load_schema()["version"] == "1.2.0"


def test_unit_without_id_is_red(tmp_path):
    bare = _unit("orphan")
    del bare["id"]
    assert "TC001" in _rules(tmp_path, [bare])


def test_unit_carrying_depends_on_validates_green(tmp_path):
    units = [_unit("first"), _unit("second", ["first"])]
    assert _rules(tmp_path, units) == set()


def test_isolated_units_are_valid(tmp_path):
    """Parallel work is the point - no connectivity check (ADR 0024)."""
    assert _rules(tmp_path, [_unit("alpha"), _unit("beta")]) == set()
