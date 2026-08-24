"""Unit-graph suite for ADR 0024.

The schema declares the fields (`id` required, `depends_on` optional);
the checker decides the graph. Graph validity - duplicate ids,
reference resolution, acyclicity - is a Python-side ready check, the
same category as 0017's entities join, and it fires in both profiles
because a cycle is malformed at draft too.
"""

from __future__ import annotations

import yaml

from taskcontract.__main__ import main
from taskcontract.checker import load_schema, validate_path
from taskcontract.graph import render_mermaid

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
    assert hits[0].message.endswith("solo depends on solo")


def test_two_cycle_yields_tc015(tmp_path):
    units = [_unit("alpha", ["beta"]), _unit("beta", ["alpha"])]
    hits = [v for v in _violations(tmp_path, units) if v.rule == "TC015"]
    assert len(hits) == 1
    assert "alpha depends on beta depends on alpha" in hits[0].message


def test_three_cycle_message_names_the_ring(tmp_path):
    units = [_unit("a-one", ["c-three"]), _unit("b-two", ["a-one"]),
             _unit("c-three", ["b-two"])]
    hits = [v for v in _violations(tmp_path, units) if v.rule == "TC015"]
    assert len(hits) == 1
    assert ("a-one depends on c-three depends on b-two depends on a-one"
            in hits[0].message)


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


# --- render (unit g0-graph-render) -----------------------------------------

DIAMOND = [_unit("root"), _unit("left", ["root"]), _unit("right", ["root"]),
           _unit("join", ["left", "right"])]


def test_render_opens_a_flowchart():
    assert render_mermaid(_doc(DIAMOND)).splitlines()[0] == "flowchart TD"


def test_diamond_renders_four_units_and_four_links():
    lines = render_mermaid(_doc(DIAMOND)).splitlines()[1:]
    nodes = [ln for ln in lines if "-->" not in ln]
    links = [ln for ln in lines if "-->" in ln]
    assert len(nodes) == 4
    assert len(links) == 4


def test_edges_run_dependency_to_dependent():
    """Execution order, not depends_on order: root comes first, so root --> left."""
    lines = render_mermaid(_doc(DIAMOND))
    assert "    root --> left" in lines
    assert "    left --> join" in lines
    assert "left --> root" not in lines


def test_unit_with_no_links_renders_as_a_shape():
    out = render_mermaid(_doc([_unit("lonely")]))
    assert '    lonely["work for lonely"]' in out
    assert "-->" not in out


def test_render_is_byte_identical_across_runs():
    assert render_mermaid(_doc(DIAMOND)) == render_mermaid(_doc(DIAMOND))


def test_label_quotes_are_neutralised():
    unit = _unit("quoted")
    unit["unit"] = 'ship the "graph" command'
    assert '#quot;graph#quot;' in render_mermaid(_doc([unit]))


def test_label_newlines_collapse():
    unit = _unit("wrapped")
    unit["unit"] = "render the graph\n  across two lines"
    assert '    wrapped["render the graph across two lines"]' in render_mermaid(
        _doc([unit]))


def test_duplicate_id_draws_one_node():
    out = render_mermaid(_doc([_unit("twin"), _unit("twin")]))
    assert out.count('twin["') == 1


def test_cli_graph_writes_mermaid_and_exits_zero(tmp_path, capsys):
    path = _write(tmp_path, _doc(DIAMOND))
    assert main(["graph", str(path)]) == 0
    assert capsys.readouterr().out == render_mermaid(_doc(DIAMOND))


def test_cli_graph_reports_a_cycle_on_stderr_but_still_renders(tmp_path, capsys):
    units = [_unit("alpha", ["beta"]), _unit("beta", ["alpha"])]
    path = _write(tmp_path, _doc(units))
    assert main(["graph", str(path)]) == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("flowchart TD")
    assert "TC015" in captured.err


def test_cli_graph_rejects_an_unreadable_contract(tmp_path, capsys):
    missing = tmp_path / "absent.yaml"
    assert main(["graph", str(missing)]) == 1
    assert "unreadable contract" in capsys.readouterr().err
