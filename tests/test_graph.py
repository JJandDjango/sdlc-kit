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


# --- graph door (unit tc013-tc015-door) ------------------------------------

def _violations(tmp_path, units, profile="ready"):
    return validate_path(_write(tmp_path, _doc(units)), profile=profile)


def test_duplicate_id_yields_tc013_naming_both_units(tmp_path):
    units = [_unit("twin"), _unit("twin")]
    hits = [v for v in _violations(tmp_path, units) if v.rule == "TC013"]
    assert len(hits) == 1
    assert "twin" in hits[0].message
    assert "$.decomposition[0]" in hits[0].message  # the first occurrence
    assert hits[0].path == "$.decomposition[1]"     # and the duplicate


def test_dangling_depends_on_yields_tc014(tmp_path):
    units = [_unit("real"), _unit("second", ["ghost"])]
    hits = [v for v in _violations(tmp_path, units) if v.rule == "TC014"]
    assert len(hits) == 1
    assert "ghost" in hits[0].message
    assert hits[0].path == "$.decomposition[1].depends_on[0]"


def test_self_loop_yields_tc015(tmp_path):
    hits = [v for v in _violations(tmp_path, [_unit("solo", ["solo"])])
            if v.rule == "TC015"]
    assert len(hits) == 1
    assert hits[0].message.endswith("solo -> solo")


def test_two_cycle_yields_tc015(tmp_path):
    units = [_unit("alpha", ["beta"]), _unit("beta", ["alpha"])]
    hits = [v for v in _violations(tmp_path, units) if v.rule == "TC015"]
    assert len(hits) == 1
    assert "alpha -> beta -> alpha" in hits[0].message


def test_three_cycle_message_names_the_ring(tmp_path):
    units = [_unit("a-one", ["c-three"]), _unit("b-two", ["a-one"]),
             _unit("c-three", ["b-two"])]
    hits = [v for v in _violations(tmp_path, units) if v.rule == "TC015"]
    assert len(hits) == 1
    assert "a-one -> c-three -> b-two -> a-one" in hits[0].message


def test_cycle_is_red_in_draft_too(tmp_path):
    """A cycle is malformed, not merely unready (ADR 0024)."""
    units = [_unit("alpha", ["beta"]), _unit("beta", ["alpha"])]
    assert "TC015" in _rules(tmp_path, units, profile="draft")


def test_diamond_is_valid(tmp_path):
    units = [_unit("root"), _unit("left", ["root"]), _unit("right", ["root"]),
             _unit("join", ["left", "right"])]
    assert _rules(tmp_path, units) == set()


def test_cycle_reporting_is_deterministic(tmp_path):
    units = [_unit("alpha", ["beta"]), _unit("beta", ["alpha"])]
    first = [v.line for v in _violations(tmp_path, units)]
    second = [v.line for v in _violations(tmp_path, units)]
    assert first == second
