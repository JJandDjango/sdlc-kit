"""The work as one derived tree (ADR 0031).

The tree is computed at every print and never stored: ADR 0024's rule for
the unit graph, carried to the whole work. `build` reads the contracts under
specs/, `active_gates` from .sdlc/config.yaml, the findings under
.sdlc/findings/, and the two name lists the package ships (data/gates.yaml,
data/tasks.yaml). It reads no document and writes no file.

The gates stand first, at the repository level. A finding names a gate and
never a contract (ADR 0023's form bans identifiers), so each finding stands
once, under the gate its `gate:` field names: a condition such as G3.1 files
under its gate, and a gate a finding names shows even when it is not active.
Then each contract, with its verdict at every active gate, its units, each
unit's seven tasks and its checks.

Every item but a finding carries one of six statuses; a finding records
none, so it shows its kind. Nothing here reads progress or runs the
validator yet, so every status reads `to do`, the reading of an item that
nothing has started.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .graph import units as unit_rows

DATA_DIR = Path(__file__).resolve().parent / "data"
GATES_PATH = DATA_DIR / "gates.yaml"
TASKS_PATH = DATA_DIR / "tasks.yaml"

STATUSES = ("to do", "doing", "done", "failed", "blocked", "waiting on a seat")
TO_DO = STATUSES[0]
NO_GATE = "none"
FORM = "TEMPLATE.yaml"  # the findings form, never a finding
INACTIVE = "inactive"

# A check's id is the ids in its sketch's trailing parentheses, where intake
# writes them, joined with "+"; parentheses that hold words name no id.
_TRAILING = re.compile(r"\(([^()]*)\)\s*$")
_CHECK_ID = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")


@dataclass
class Item:
    """One entry of the tree; `level` is gate, none, finding, contract,
    verdict, unit, task or check."""

    id: str
    level: str
    status: str | None = TO_DO
    kind: str | None = None  # a finding's kind, shown where others show a status
    marks: list[str] = field(default_factory=list)
    children: list[Item] = field(default_factory=list)


def gate_list() -> list[dict]:
    """The kit's gates in registry order, each an id, a name and a page."""
    return yaml.safe_load(GATES_PATH.read_text(encoding="utf-8"))["gates"]


def task_list() -> list[dict]:
    """The seven tasks in order, each an id, a name and a page."""
    return yaml.safe_load(TASKS_PATH.read_text(encoding="utf-8"))["tasks"]


def build(root: Path) -> tuple[list[Item], list[str]]:
    """The tree in print order, and one line per source that could not be read."""
    problems: list[str] = []
    order = [gate["id"] for gate in gate_list()]
    tasks = [task["id"] for task in task_list()]
    active = _in_order(active_gates(root, problems), order)
    findings = read_findings(root, problems)
    items = _gate_items(order, active, findings)
    for cid, instance in read_contracts(root, problems):
        items.append(_contract_item(cid, instance, active, tasks))
    return items, problems


def active_gates(root: Path, problems: list[str]) -> list[str]:
    """`active_gates` from .sdlc/config.yaml; none when there is no config."""
    path = root / ".sdlc" / "config.yaml"
    if not path.is_file():
        return []
    doc = _load(path, root, problems, "config")
    gates = doc.get("active_gates") if doc is not None else None
    return [g for g in gates if isinstance(g, str)] if isinstance(gates, list) else []


def read_findings(root: Path, problems: list[str]) -> list[tuple[str, str, str]]:
    """(gate, finding, kind) per file under .sdlc/findings/, in file-name order."""
    folder = root / ".sdlc" / "findings"
    if not folder.is_dir():
        return []
    found: list[tuple[str, str, str]] = []
    for path in sorted(folder.glob("*.yaml"), key=lambda p: p.name):
        if path.name == FORM:
            continue
        doc = _load(path, root, problems, "finding")
        if doc is not None:
            kind = doc.get("kind")
            found.append((gate_of(doc.get("gate")), path.stem,
                          "none" if kind is None else str(kind)))
    return found


def gate_of(value) -> str:
    """The gate a finding's `gate:` field names; a condition files under its gate."""
    text = value.strip() if isinstance(value, str) else ""
    if not text or text == NO_GATE:
        return NO_GATE
    return text.split(".", 1)[0]


def read_contracts(root: Path, problems: list[str]) -> list[tuple[str, dict | None]]:
    """(id, contract) per specs/<id>/contract.yaml in folder order; None if unreadable."""
    specs = root / "specs"
    if not specs.is_dir():
        return []
    paths = sorted(specs.glob("*/contract.yaml"), key=lambda p: p.parent.name)
    return [(path.parent.name, _load(path, root, problems, "contract")) for path in paths]


def check_ids(sketches: list) -> list[str]:
    """One id per sketch line by the trailing-parentheses rule; a line that
    names none, or repeats an id, is `sketch-<n>` by its position from 1."""
    ids: list[str] = []
    for n, sketch in enumerate(sketches, start=1):
        named = _named(sketch)
        ids.append(named if named and named not in ids else f"sketch-{n}")
    return ids


def _named(sketch) -> str | None:
    match = _TRAILING.search(sketch) if isinstance(sketch, str) else None
    if match is None:
        return None
    parts = [part.strip() for part in match.group(1).split(",")]
    return "+".join(parts) if all(_CHECK_ID.match(part) for part in parts) else None


def _gate_items(order: list[str], active: list[str],
                findings: list[tuple[str, str, str]]) -> list[Item]:
    """Each active gate and each gate a finding names, then the no-gate item."""
    named = [gate for gate, _, _ in findings]
    items = [Item(f"gates/{gate}", "gate",
                  marks=[] if gate in active else [INACTIVE],
                  children=_finding_items(gate, findings))
             for gate in _in_order(active + named, order)]
    if NO_GATE in named:
        items.append(Item(f"gates/{NO_GATE}", "none",
                          children=_finding_items(NO_GATE, findings)))
    return items


def _finding_items(gate: str, findings: list[tuple[str, str, str]]) -> list[Item]:
    return [Item(f"gates/{gate}/{slug}", "finding", status=None, kind=kind)
            for named, slug, kind in findings if named == gate]


def _contract_item(cid: str, instance: dict | None, active: list[str],
                   tasks: list[str]) -> Item:
    """A contract: its verdict at each active gate, then its units. An
    unreadable contract keeps its verdicts and shows no unit."""
    item = Item(cid, "contract",
                children=[Item(f"{cid}/{gate}", "verdict") for gate in active])
    for uid, unit in _units(instance):
        base = f"{cid}/{uid}"
        sketches = unit.get("acceptance_sketch")
        unit_item = Item(base, "unit",
                         children=[Item(f"{base}/{task}", "task") for task in tasks])
        unit_item.children += [
            Item(f"{base}/{check}", "check")
            for check in check_ids(sketches if isinstance(sketches, list) else [])]
        item.children.append(unit_item)
    return item


def _units(instance: dict | None) -> list[tuple[str, dict]]:
    """(id, unit) per unit with a usable id; of a duplicate id (TC013), the
    first only, as the unit graph draws it (ADR 0024)."""
    if instance is None:
        return []
    decomposition = instance.get("decomposition")
    seen: set[str] = set()
    out: list[tuple[str, dict]] = []
    for index, uid, _ in unit_rows(instance):
        if uid not in seen:
            seen.add(uid)
            out.append((uid, decomposition[index]))
    return out


def _in_order(ids: list[str], order: list[str]) -> list[str]:
    """`ids` once each: the kit's gates in registry order, then any other id."""
    wanted = [gate for gate in dict.fromkeys(ids) if gate != NO_GATE]
    return [gate for gate in order if gate in wanted] + [
        gate for gate in wanted if gate not in order]


def _load(path: Path, root: Path, problems: list[str], what: str) -> dict | None:
    """The YAML mapping at `path`, or None with one line added to `problems`."""
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        reason = f"YAML error at line {mark.line + 1}" if mark is not None else "YAML error"
    except (OSError, UnicodeDecodeError) as exc:
        reason = getattr(exc, "strerror", None) or "cannot be read"
    else:
        if isinstance(doc, dict):
            return doc
        reason = "not a mapping"
    problems.append(f"unreadable {what}: {_rel(path, root)} ({reason})")
    return None


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
