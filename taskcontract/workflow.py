"""The workflow file, `.sdlc/workflow.md`: its diagram and settings table.

The mermaid flowchart holds the nodes in order, and each edge's label names
the file it hands to the next node. The settings table holds each node's
agent model, effort, and operator or seat, and is the one place for them.

The reader refuses a file with a structural fault: a node with no row, a
row with no node, or an edge with no label. Every call raises those,
whichever node it asks for. A row
that lacks a value is not structural: it stops only `settings` for that
node, and reads elsewhere as "".

Standard library only (the design's constraint 6): the file is markdown,
parsed by line, never through a markdown or mermaid library.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

WORKFLOW_FILE = ".sdlc/workflow.md"
HEADER = ["Node", "Agent model", "Effort", "Operator or seat"]
FENCE = "```"

# An id may hold a hyphen, but never the one that opens an arrow, so
# `a-->b` reads as two nodes.
_NODE = re.compile(r"\s*((?:[A-Za-z0-9_]|-(?!->))+)(\[[^\]]*\])?")
_ARROW = re.compile(r"\s*-->\s*(?:\|([^|]*)\|)?")
# Mermaid statements the reader does not read; `end` would parse as a node.
_KEYWORDS = {"subgraph", "end", "style", "classDef", "class", "linkStyle",
             "click", "direction"}


class WorkflowError(Exception):
    """The reader's refusal; `lines` holds one line a fault, in order."""

    def __init__(self, lines: list[str]):
        self.lines = list(lines)
        super().__init__("\n".join(self.lines))

    def __str__(self) -> str:
        return "\n".join(self.lines)


class Edge(NamedTuple):
    source: str
    target: str
    label: str


class Row(NamedTuple):
    agent_model: str
    effort: str
    operator: str


class Settings(NamedTuple):
    agent_model: str
    effort: str


class Workflow(NamedTuple):
    nodes: list[str]
    edges: list[Edge]
    rows: dict[str, Row]


def _flowchart(lines: list[str]) -> list[str]:
    """The body of the first mermaid block that is a flowchart, else []."""
    i = 0
    while i < len(lines):
        if not lines[i].strip().startswith(FENCE + "mermaid"):
            i += 1
            continue
        body: list[str] = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith(FENCE):
            body.append(lines[i])
            i += 1
        i += 1
        head = next((line.strip() for line in body
                     if line.strip() and not line.strip().startswith("%%")), "")
        if head.startswith("flowchart"):
            return body
    return []


def _statement(line: str) -> list[tuple] | None:
    """One diagram line as steps, left to right, or None if not read.

    A step is ("node", id) or ("edge", source, target, label); a chain
    `a -->|x| b -->|y| c` gives a node, an edge, a node, an edge, a node.
    """
    match = _NODE.match(line)
    if not match:
        return None
    steps: list[tuple] = [("node", match.group(1))]
    pos = match.end()
    while True:
        arrow = _ARROW.match(line, pos)
        if not arrow:
            break
        target = _NODE.match(line, arrow.end())
        if not target:
            return None
        label = (arrow.group(1) or "").strip()
        steps.append(("edge", steps[-1][1] if steps[-1][0] == "node"
                      else steps[-1][2], target.group(1), label))
        steps.append(("node", target.group(1)))
        pos = target.end()
    if line[pos:].strip():
        return None
    return steps


def _diagram(lines: list[str]) -> tuple[list[str], list[Edge], list[tuple]]:
    """Nodes in order of first appearance, edges, and the walk's steps.

    The steps keep each node's first appearance and every edge in the order
    the diagram is read, which is the order its faults are reported in.
    """
    nodes: list[str] = []
    edges: list[Edge] = []
    walk: list[tuple] = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("%%") or text.startswith("flowchart"):
            continue
        if text.split()[0] in _KEYWORDS:
            continue
        steps = _statement(text)
        if steps is None:
            continue
        for step in steps:
            if step[0] == "node":
                if step[1] not in nodes:
                    nodes.append(step[1])
                    walk.append(step)
            else:
                edges.append(Edge(*step[1:]))
                walk.append(step)
    return nodes, edges, walk


def _cells(line: str) -> list[str]:
    """A table line's cells, outer pipes removed, each stripped."""
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def _table(lines: list[str]) -> dict[str, Row]:
    """Node id -> row, in table order; a later row for the same id is ignored."""
    rows: dict[str, Row] = {}
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and _cells(line) == HEADER:
            break
    else:
        return rows
    for line in lines[i + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = _cells(line) + ["", "", ""]
        rows.setdefault(cells[0], Row(cells[1], cells[2], cells[3]))
    return rows


def _parse(root: Path) -> tuple[Workflow, list[tuple]]:
    lines = (Path(root) / WORKFLOW_FILE).read_text(encoding="utf-8").splitlines()
    nodes, edges, walk = _diagram(_flowchart(lines))
    return Workflow(nodes, edges, _table(lines)), walk


def _missing(node_id: str, row: Row) -> list[str]:
    """The SC2.3 lines for one node's row: agent model first, then effort."""
    out: list[str] = []
    if not row.agent_model:
        out.append(f"Node {node_id} did not start: its row in the workflow "
                   "file has no agent model.")
    if not row.effort:
        out.append(f"Node {node_id} did not start: its row in the workflow "
                   "file has no effort.")
    return out


def _faults(workflow: Workflow, walk: list[tuple],
            asked: str | None = None) -> list[str]:
    """Every refusal line, in order.

    Diagram faults come first, in the order the diagram is read; then table
    faults in row order, with the asked node's SC2.3 lines at its row.
    """
    lines: list[str] = []
    for step in walk:
        if step[0] == "node" and step[1] not in workflow.rows:
            lines.append(f"Node {step[1]} has no row in the settings table "
                         f"of {WORKFLOW_FILE}.")
        elif step[0] == "edge" and not step[3]:
            lines.append(f"The edge from {step[1]} to {step[2]} in "
                         f"{WORKFLOW_FILE} names no file.")
    for row_id, row in workflow.rows.items():
        if row_id not in workflow.nodes:
            lines.append(f"Row {row_id} in the settings table of "
                         f"{WORKFLOW_FILE} has no node in the diagram.")
        elif row_id == asked:
            lines.extend(_missing(row_id, row))
    return lines


def read(root: Path) -> Workflow:
    """The workflow file's nodes, edges and rows; raises on a structural fault."""
    workflow, walk = _parse(root)
    lines = _faults(workflow, walk)
    if lines:
        raise WorkflowError(lines)
    return workflow


def settings(root: Path, node_id: str) -> Settings:
    """One node's agent model and effort, read from the settings table.

    Raises on any structural fault in the file, on a row of this node that
    lacks a value, and on an id that is no node.
    """
    workflow, walk = _parse(root)
    lines = _faults(workflow, walk, node_id)
    if lines:
        raise WorkflowError(lines)
    if node_id not in workflow.nodes:
        raise WorkflowError([f"No node {node_id} in {WORKFLOW_FILE}. "
                             f"Nodes: {', '.join(workflow.nodes)}."])
    row = workflow.rows[node_id]
    return Settings(row.agent_model, row.effort)
