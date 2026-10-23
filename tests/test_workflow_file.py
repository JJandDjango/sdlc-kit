"""Workflow-file suite (contract: small-session-flow, unit w2-workflow-file).

The unit adds `.sdlc/workflow.md`, the workflow file the design draws in
Interfaces, and `taskcontract/workflow.py`, the reader. The reader is a
library with no command (w3 adds `python -m taskcontract node`), so these
tests call it directly and assert each refusal's text:

- `read(root)` returns the parsed workflow (`nodes`, `edges`, `rows`) or
  raises `WorkflowError` for a structural fault (a node with no row, a row
  with no node, an edge with no label);
- `settings(root, node_id)` returns the node's (agent model, effort) or
  raises `WorkflowError`; SC2.3's "starts no session" is that refusal.

SC1.1, SC1.2 and SC1.3 are pinned on the real file, found through the
`taskcontract` package (never through this file's location), so a run
against a prototype reads the prototype's file. The reader's refusals are
pinned on fixture files under tmp_path, passed to the reader as the root.
"""

from __future__ import annotations

import ast
import importlib
import re
import sys
from pathlib import Path

import pytest

import taskcontract

ROOT = Path(taskcontract.__file__).resolve().parents[1]
WORKFLOW = ROOT / ".sdlc" / "workflow.md"
READER = ROOT / "taskcontract" / "workflow.py"

# The design's Interfaces, word for word.
DIAGRAM = """flowchart LR
  feature[Feature document] -->|docs/features/{id}.md| design[Design document]
  design -->|specs/{id}/contract.yaml| execution[Execution]
  execution -->|.sdlc/progress/{id}.yaml| review[Self PR review]"""

TABLE = """| Node | Agent model | Effort | Operator or seat |
| :-- | :-- | :-- | :-- |
| feature | opus | xhigh | PO seat |
| design | opus | xhigh | engineer seat |
| execution | sonnet | high | Developer, QA, Dev verifier, QA verifier, Orchestrator |
| review | opus | high | engineer seat |"""

HEADER = "| Node | Agent model | Effort | Operator or seat |\n| :-- | :-- | :-- | :-- |"

NODES = ["feature", "design", "execution", "review"]
EDGES = [("feature", "design", "docs/features/{id}.md"),
         ("design", "execution", "specs/{id}/contract.yaml"),
         ("execution", "review", ".sdlc/progress/{id}.yaml")]
ROWS = {"feature": ("opus", "xhigh", "PO seat"),
        "design": ("opus", "xhigh", "engineer seat"),
        "execution": ("sonnet", "high",
                      "Developer, QA, Dev verifier, QA verifier, Orchestrator"),
        "review": ("opus", "high", "engineer seat")}


def no_model(node: str) -> str:
    return f"Node {node} did not start: its row in the workflow file has no agent model."


def no_effort(node: str) -> str:
    return f"Node {node} did not start: its row in the workflow file has no effort."


def no_row(node: str) -> str:
    return f"Node {node} has no row in the settings table of .sdlc/workflow.md."


def no_node(row: str) -> str:
    return f"Row {row} in the settings table of .sdlc/workflow.md has no node in the diagram."


def no_label(a: str, b: str) -> str:
    return f"The edge from {a} to {b} in .sdlc/workflow.md names no file."


def reader():
    """The reader module, or a test failure that names it as missing."""
    try:
        return importlib.import_module("taskcontract.workflow")
    except ModuleNotFoundError as err:
        pytest.fail(f"no reader: taskcontract.workflow does not import ({err})")


def page(diagram: str | None = DIAGRAM, table: str | None = TABLE) -> str:
    """A workflow file: a title, the mermaid block, then the settings table."""
    parts = ["# Workflow", ""]
    if diagram is not None:
        parts += ["```mermaid", diagram, "```", ""]
    if table is not None:
        parts += [table, ""]
    return "\n".join(parts)


def write(root: Path, text: str) -> Path:
    """Write `text` as root/.sdlc/workflow.md; return root."""
    folder = root / ".sdlc"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "workflow.md").write_text(text, encoding="utf-8")
    return root


def refusal(call, *args) -> list[str]:
    """Call the reader; it must raise WorkflowError. Return its lines, checked against str()."""
    wf = reader()
    with pytest.raises(wf.WorkflowError) as caught:
        call(*args)
    lines = list(caught.value.lines)
    assert str(caught.value) == "\n".join(lines)
    return lines


def real_text() -> str:
    assert WORKFLOW.is_file(), f"no workflow file at {WORKFLOW}"
    return WORKFLOW.read_text(encoding="utf-8")


# --- SC1.1, SC1.2, SC1.3 on the real file ---

def test_sc1_1_real_file_holds_the_designs_diagram_word_for_word():
    text = real_text()
    assert text.count("```mermaid") == 1, "the workflow file holds more or fewer than one mermaid block"
    assert "```mermaid\n" + DIAGRAM + "\n```" in text


def test_sc1_1_real_file_has_four_nodes_one_per_stage_in_order():
    wf = reader()
    assert wf.read(ROOT).nodes == NODES


def test_sc1_3_real_file_names_the_file_on_each_edge():
    wf = reader()
    assert [tuple(edge) for edge in wf.read(ROOT).edges] == EDGES


def test_sc1_2_real_file_holds_the_designs_table_word_for_word():
    assert TABLE in real_text()


def test_sc1_2_real_file_has_one_row_per_node_with_all_four_values():
    text = real_text()
    for node in NODES:
        rows = re.findall(rf"^\|\s*{node}\s*\|", text, flags=re.MULTILINE)
        assert len(rows) == 1, f"node {node} has {len(rows)} rows in the settings table"
    wf = reader()
    rows = wf.read(ROOT).rows
    assert list(rows) == NODES
    assert {node: tuple(row) for node, row in rows.items()} == ROWS


def test_sc2_3_real_file_gives_each_node_its_agent_model_and_effort():
    wf = reader()
    for node, (model, effort, _seat) in ROWS.items():
        assert tuple(wf.settings(ROOT, node)) == (model, effort)


def test_constraint_6_reader_imports_only_the_standard_library():
    assert READER.is_file(), f"no reader at {READER}"
    tree = ast.parse(READER.read_text(encoding="utf-8"))
    outside = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            names = [node.module or ""]
        else:
            continue
        for name in names:
            top = name.split(".")[0]
            if top not in sys.stdlib_module_names and top not in ("taskcontract", "__future__"):
                outside.append(name)
    assert outside == [], f"the reader imports outside the standard library: {outside}"


# --- the reader on fixtures: a clean file and the forms it reads ---

def test_sc1_1_reader_reads_nodes_edges_and_rows_of_a_clean_file(tmp_path):
    wf = reader()
    got = wf.read(write(tmp_path, page()))
    assert got.nodes == NODES
    assert [tuple(edge) for edge in got.edges] == EDGES
    assert {node: tuple(row) for node, row in got.rows.items()} == ROWS


def test_sc1_1_reader_reads_chains_lone_nodes_and_skips_comments(tmp_path):
    wf = reader()
    diagram = "\n".join([
        "flowchart TD",
        "  %% feature --> ghost",
        "  feature[Feature document]",
        "  feature -->|a.md| design[Design document] -->|b.md| execution",
        "  execution -->|c.md| review",
    ])
    got = wf.read(write(tmp_path, page(diagram=diagram)))
    assert got.nodes == NODES
    assert [tuple(edge) for edge in got.edges] == [
        ("feature", "design", "a.md"), ("design", "execution", "b.md"),
        ("execution", "review", "c.md")]


def test_sc1_1_reader_reads_the_first_mermaid_block_that_opens_with_flowchart(tmp_path):
    wf = reader()
    other = "sequenceDiagram\n  ghost->>feature: hello"
    later = "flowchart LR\n  feature -->|x.md| phantom"
    text = "\n".join(["# Workflow", "", "```mermaid", other, "```", "",
                      "```mermaid", DIAGRAM, "```", "",
                      "```mermaid", later, "```", "", TABLE, ""])
    got = wf.read(write(tmp_path, text))
    assert got.nodes == NODES
    assert [tuple(edge) for edge in got.edges] == EDGES


def test_sc1_2_reader_finds_the_table_by_its_four_column_names(tmp_path):
    wf = reader()
    table = "\n".join([
        "|Node|Agent model|Effort|Operator or seat|",
        "|---|---|---|---|",
        "|feature|opus|xhigh|PO seat|",
        "|design|opus|xhigh|engineer seat|",
        "|execution|sonnet|high|Orchestrator|",
        "|review|opus|high|engineer seat|",
    ])
    root = write(tmp_path, page(table=table))
    assert tuple(wf.settings(root, "execution")) == ("sonnet", "high")
    assert tuple(wf.read(root).rows["review"]) == ("opus", "high", "engineer seat")


def test_sc1_2_first_of_two_rows_for_one_node_counts_without_refusal(tmp_path):
    wf = reader()
    table = TABLE + "\n| design | sonnet | low | engineer seat |"
    root = write(tmp_path, page(table=table))
    assert tuple(wf.settings(root, "design")) == ("opus", "xhigh")
    assert list(wf.read(root).rows) == NODES


def test_reading_f_row_with_no_operator_or_seat_is_no_refusal(tmp_path):
    wf = reader()
    table = TABLE.replace("| review | opus | high | engineer seat |", "| review | opus | high |  |")
    root = write(tmp_path, page(table=table))
    assert tuple(wf.settings(root, "review")) == ("opus", "high")
    assert tuple(wf.read(root).rows["review"]) == ("opus", "high", "")


def test_reading_d_full_model_id_and_any_effort_are_accepted(tmp_path):
    wf = reader()
    table = TABLE.replace("| design | opus | xhigh |", "| design | claude-opus-5-5 | max |")
    root = write(tmp_path, page(table=table))
    assert tuple(wf.settings(root, "design")) == ("claude-opus-5-5", "max")


# --- SC2.3: a row that lacks a value starts no session ---

def test_sc2_3_row_with_empty_agent_model_refuses_with_sc2_3_message(tmp_path):
    wf = reader()
    table = TABLE.replace("| design | opus | xhigh |", "| design |  | xhigh |")
    root = write(tmp_path, page(table=table))
    assert refusal(wf.settings, root, "design") == [no_model("design")]


def test_sc2_3_row_with_whitespace_effort_refuses_with_sc2_3_message(tmp_path):
    wf = reader()
    table = TABLE.replace("| execution | sonnet | high |", "| execution | sonnet | \t   |")
    root = write(tmp_path, page(table=table))
    assert refusal(wf.settings, root, "execution") == [no_effort("execution")]


def test_sc2_3_row_lacking_both_values_gives_two_lines_agent_model_first(tmp_path):
    wf = reader()
    table = TABLE.replace("| review | opus | high |", "| review |   |  |")
    root = write(tmp_path, page(table=table))
    assert refusal(wf.settings, root, "review") == [no_model("review"), no_effort("review")]


def test_sc2_3_missing_value_stops_only_the_node_asked_for(tmp_path):
    wf = reader()
    table = TABLE.replace("| design | opus | xhigh |", "| design |  |  |")
    root = write(tmp_path, page(table=table))
    assert tuple(wf.settings(root, "feature")) == ("opus", "xhigh")
    assert tuple(wf.settings(root, "execution")) == ("sonnet", "high")
    assert tuple(wf.read(root).rows["design"]) == ("", "", "engineer seat")
    assert refusal(wf.settings, root, "design") == [no_model("design"), no_effort("design")]


def test_sc2_3_id_with_no_node_is_refused_naming_the_files_nodes(tmp_path):
    wf = reader()
    root = write(tmp_path, page())
    assert refusal(wf.settings, root, "ghost") == [
        "No node ghost in .sdlc/workflow.md. Nodes: feature, design, execution, review."]
    other = tmp_path / "other"
    diagram = "flowchart LR\n  beta -->|b.md| alpha"
    table = HEADER + "\n| alpha | opus | high | PO seat |\n| beta | opus | high | PO seat |"
    write(other, page(diagram=diagram, table=table))
    assert refusal(wf.settings, other, "design") == [
        "No node design in .sdlc/workflow.md. Nodes: beta, alpha."]


# --- structural faults refuse every node ---

def test_sc1_2_node_with_no_row_refuses_every_node(tmp_path):
    wf = reader()
    diagram = DIAGRAM + "\n  review -->|r.md| ghost[Ghost]"
    root = write(tmp_path, page(diagram=diagram))
    assert refusal(wf.read, root) == [no_row("ghost")]
    for node in NODES:
        assert refusal(wf.settings, root, node) == [no_row("ghost")]


def test_sc1_2_lone_node_with_no_row_is_refused(tmp_path):
    wf = reader()
    diagram = DIAGRAM + "\n  ghost[Ghost]"
    root = write(tmp_path, page(diagram=diagram))
    assert refusal(wf.read, root) == [no_row("ghost")]


def test_sc1_2_row_with_no_node_refuses_every_node(tmp_path):
    wf = reader()
    table = TABLE + "\n| phantom | opus | high | PO seat |"
    root = write(tmp_path, page(table=table))
    assert refusal(wf.read, root) == [no_node("phantom")]
    for node in NODES:
        assert refusal(wf.settings, root, node) == [no_node("phantom")]


@pytest.mark.parametrize("arrow", ["-->", "-->| |"], ids=["bare", "blank-label"])
def test_sc1_3_edge_with_no_label_refuses_every_node(tmp_path, arrow):
    wf = reader()
    diagram = DIAGRAM.replace("design -->|specs/{id}/contract.yaml| execution",
                              f"design {arrow} execution")
    root = write(tmp_path, page(diagram=diagram))
    assert refusal(wf.read, root) == [no_label("design", "execution")]
    for node in NODES:
        assert refusal(wf.settings, root, node) == [no_label("design", "execution")]


def test_sc1_3_comment_line_with_an_unlabelled_edge_is_no_fault(tmp_path):
    wf = reader()
    diagram = DIAGRAM + "\n  %% review --> feature"
    root = write(tmp_path, page(diagram=diagram))
    assert [tuple(edge) for edge in wf.read(root).edges] == EDGES


def test_sc1_1_file_with_no_mermaid_block_refuses_each_row(tmp_path):
    wf = reader()
    root = write(tmp_path, page(diagram=None))
    assert refusal(wf.read, root) == [no_node(node) for node in NODES]


def test_sc1_2_file_with_no_settings_table_refuses_each_node(tmp_path):
    wf = reader()
    root = write(tmp_path, page(table=None))
    assert refusal(wf.read, root) == [no_row(node) for node in NODES]
    assert refusal(wf.settings, root, "design") == [no_row(node) for node in NODES]


# --- several faults at once: diagram faults first, then table faults, in file order ---

def test_faults_two_nodes_with_no_row_in_diagram_order(tmp_path):
    wf = reader()
    diagram = DIAGRAM + "\n  spook[Spook]\n  review -->|r.md| ghost"
    root = write(tmp_path, page(diagram=diagram))
    assert refusal(wf.read, root) == [no_row("spook"), no_row("ghost")]


def test_faults_two_rows_with_no_node_in_table_order(tmp_path):
    wf = reader()
    table = TABLE.replace("| design |", "| wraith | opus | high | PO seat |\n| design |") \
        + "\n| phantom | opus | high | PO seat |"
    root = write(tmp_path, page(table=table))
    assert refusal(wf.read, root) == [no_node("wraith"), no_node("phantom")]


def test_faults_two_unlabelled_edges_in_diagram_order(tmp_path):
    wf = reader()
    diagram = "\n".join([
        "flowchart LR",
        "  feature -->|a.md| design",
        "  execution --> review",
        "  design -->| | execution",
    ])
    root = write(tmp_path, page(diagram=diagram))
    assert refusal(wf.read, root) == [no_label("execution", "review"),
                                      no_label("design", "execution")]


def test_faults_diagram_faults_first_then_table_faults_each_in_file_order(tmp_path):
    wf = reader()
    diagram = "\n".join([
        "flowchart LR",
        "  feature -->|f.md| design",
        "  design --> execution",
        "  execution -->|e.md| ghost",
        "  ghost --> review",
        "  review -->|r.md| spook",
    ])
    table = TABLE.replace("| execution |", "| phantom | opus | high | PO seat |\n| execution |") \
        + "\n| wraith | opus | high | PO seat |"
    expected = [no_label("design", "execution"), no_row("ghost"),
                no_label("ghost", "review"), no_row("spook"),
                no_node("phantom"), no_node("wraith")]
    root = write(tmp_path, page(diagram=diagram, table=table))
    assert refusal(wf.read, root) == expected
    assert refusal(wf.settings, root, "feature") == expected


def test_faults_diagram_first_even_when_the_table_comes_first_in_the_file(tmp_path):
    wf = reader()
    diagram = DIAGRAM + "\n  review -->|r.md| ghost"
    table = TABLE + "\n| phantom | opus | high | PO seat |"
    text = "\n".join(["# Workflow", "", table, "", "```mermaid", diagram, "```", ""])
    root = write(tmp_path, text)
    assert refusal(wf.read, root) == [no_row("ghost"), no_node("phantom")]


def test_faults_missing_values_of_the_asked_node_are_table_faults_in_row_order(tmp_path):
    wf = reader()
    diagram = DIAGRAM.replace("design -->|specs/{id}/contract.yaml|", "design -->")
    table = TABLE.replace("| feature |", "| wraith | opus | high | PO seat |\n| feature |") \
        .replace("| design | opus | xhigh |", "| design |  |  |") \
        .replace("| execution |", "| phantom | opus | high | PO seat |\n| execution |")
    root = write(tmp_path, page(diagram=diagram, table=table))
    assert refusal(wf.settings, root, "design") == [
        no_label("design", "execution"), no_node("wraith"),
        no_model("design"), no_effort("design"), no_node("phantom")]
    assert refusal(wf.settings, root, "review") == [
        no_label("design", "execution"), no_node("wraith"), no_node("phantom")]
