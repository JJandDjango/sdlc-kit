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

from .checker import Violation

TC_DUPLICATE_ID = "TC013"
TC_DANGLING_REF = "TC014"
TC_CYCLE = "TC015"


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
        trail = " -> ".join(ring + [ring[0]])
        violations.append(Violation(
            name, f"$.decomposition[{first[ring[0]]}]", TC_CYCLE,
            f"dependency cycle: {trail}"))

    return violations
