"""Unit dependency graph over a task contract's decomposition (ADR 0024).

The schema declares the fields - `id` required, `depends_on` optional - but
JSON Schema cannot express reference resolution or acyclicity, so graph
validity is a Python-side check, the same category as ADR 0017's entities
coverage join. The checks fire in both profiles: a cycle is malformed at
draft too, not only at the ready gate.

Isolated units are valid. Parallel work is the point, so there is no
connectivity check - a decomposition with no edges is a legitimate graph
of N roots.

One model, two consumers: `graph_checks` decides validity and
`render_mermaid` draws it, both over `units()`, so the picture can never
disagree with the gate.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from .checker import Violation

TC_DUPLICATE_ID = "TC013"
TC_DANGLING_REF = "TC014"
TC_CYCLE = "TC015"

HEADER = "flowchart TD"
INDENT = "    "


def units(instance) -> list[tuple[int, str, list[str]]]:
    """[(index, id, depends_on)] for every unit carrying a usable string id.

    Units with a missing or non-string id are skipped, not guessed at: the
    schema already reports them (TC001), and inventing an identity here
    would make the graph disagree with the contract.
    """
    out: list[tuple[int, str, list[str]]] = []
    if not isinstance(instance, dict):
        return out
    decomposition = instance.get("decomposition")
    if not isinstance(decomposition, list):
        return out
    for i, unit in enumerate(decomposition):
        if not isinstance(unit, dict):
            continue
        uid = unit.get("id")
        if not isinstance(uid, str) or not uid:
            continue
        raw = unit.get("depends_on")
        deps = [d for d in raw if isinstance(d, str)] if isinstance(raw, list) else []
        out.append((i, uid, deps))
    return out


def _first_index(rows) -> dict[str, int]:
    """id -> index of its first occurrence; later duplicates never win."""
    first: dict[str, int] = {}
    for index, uid, _ in rows:
        first.setdefault(uid, index)
    return first


def _cycles(rows, known: dict[str, int]) -> list[list[str]]:
    """Every distinct cycle reachable by depth-first search, deterministic.

    Nodes and edges are walked in document order, and each ring is
    canonicalised by rotating its smallest id to the front, so the same
    contract always yields the same list in the same order.
    """
    edges = {uid: [d for d in deps if d in known] for _, uid, deps in rows}
    order = [uid for _, uid, _ in rows]
    done: set[str] = set()
    on_stack: list[str] = []
    stacked: set[str] = set()
    found: list[list[str]] = []
    seen_rings: set[tuple[str, ...]] = set()

    def canonical(ring: list[str]) -> tuple[str, ...]:
        pivot = ring.index(min(ring))
        return tuple(ring[pivot:] + ring[:pivot])

    def walk(node: str) -> None:
        on_stack.append(node)
        stacked.add(node)
        for nxt in edges.get(node, []):
            if nxt in stacked:
                ring = on_stack[on_stack.index(nxt):]
                key = canonical(ring)
                if key not in seen_rings:
                    seen_rings.add(key)
                    found.append(list(key))
            elif nxt not in done:
                walk(nxt)
        stacked.discard(node)
        on_stack.pop()
        done.add(node)

    for uid in order:
        if uid not in done:
            walk(uid)
    return found


def graph_checks(name: str, instance) -> list[Violation]:
    """TC013 duplicate id, TC014 unresolvable depends_on, TC015 cycle."""
    rows = units(instance)
    violations: list[Violation] = []

    first = _first_index(rows)
    for index, uid, _ in rows:
        if first[uid] != index:
            violations.append(Violation(
                name, f"$.decomposition[{index}]", TC_DUPLICATE_ID,
                f"duplicate unit id '{uid}' (already used at "
                f"$.decomposition[{first[uid]}])"))

    for index, _, deps in rows:
        for j, dep in enumerate(deps):
            if dep not in first:
                violations.append(Violation(
                    name, f"$.decomposition[{index}].depends_on[{j}]",
                    TC_DANGLING_REF,
                    f"depends_on '{dep}' names no unit in this contract"))

    for ring in _cycles(rows, first):
        # Spelled out, never an arrow: the render draws edges in execution
        # order (dependency --> dependent), so reusing "->" here would point
        # the opposite way in the same feature's other output.
        trail = " depends on ".join(ring + [ring[0]])
        violations.append(Violation(
            name, f"$.decomposition[{first[ring[0]]}]", TC_CYCLE,
            f"dependency cycle: {trail}"))

    return violations


# --- rendering (ADR 0008's second layer: the graph is shape, Mermaid draws it)

def _labels(instance) -> dict[str, str]:
    """id -> display label, taken from the unit's own `unit` field."""
    out: dict[str, str] = {}
    decomposition = instance.get("decomposition") if isinstance(instance, dict) else None
    if not isinstance(decomposition, list):
        return out
    for unit in decomposition:
        if not isinstance(unit, dict):
            continue
        uid = unit.get("id")
        if isinstance(uid, str) and uid and uid not in out:
            text = unit.get("unit")
            out[uid] = _label(text) if isinstance(text, str) else uid
    return out


def _label(text: str) -> str:
    """Collapse to one line and neutralise the quote that ends a Mermaid label."""
    return " ".join(text.split()).replace('"', "#quot;")


def render_mermaid(instance) -> str:
    """One contract's unit graph as Mermaid, byte-identical across runs.

    Every unit is declared as a node before any edge, so a unit with no
    links still draws - isolated units are valid (ADR 0024). Edges run
    dependency --> dependent, which is execution order: the arrow points
    the way the work flows, not the way `depends_on` is written.
    """
    rows = units(instance)
    labels = _labels(instance)
    known = {uid for _, uid, _ in rows}

    lines = [HEADER]
    drawn: set[str] = set()
    for _, uid, _ in rows:
        if uid in drawn:
            continue  # duplicate ids are TC013; draw the first, once
        drawn.add(uid)
        lines.append(f'{INDENT}{uid}["{labels.get(uid, uid)}"]')
    for _, uid, deps in rows:
        for dep in deps:
            if dep in known:
                lines.append(f"{INDENT}{dep} --> {uid}")
    return "\n".join(lines) + "\n"


def main_graph(args) -> int:
    """`taskcontract graph <file>` - Mermaid on stdout, advisories on stderr.

    Rendering never gates: stdout stays the product so a non-interactive
    caller can consume it, and graph violations are reported on stderr
    because seeing a cycle drawn is exactly how an author fixes it.
    `validate` remains the door.
    """
    path = Path(args.file)
    try:
        instance = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"taskcontract graph: unreadable contract: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(render_mermaid(instance))
    for violation in graph_checks(str(path), instance):
        print(violation.line, file=sys.stderr)
    return 0
