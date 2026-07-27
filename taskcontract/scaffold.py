"""Scaffold a task-contract skeleton - the F11 `new <id>` subcommand (ADR 0016).

The skeleton is deliberately red: `intent: TODO` trips TC007 until a real
intent is authored, so a freshly scaffolded contract can never pass the
G0.1 gate vacuously. The id pattern comes from the schema - single source
of truth, never duplicated here.
"""

from __future__ import annotations

import re
from pathlib import Path

from .checker import load_schema

TEMPLATE = """\
# Task contract - G0 definition-of-ready (ADR 0005 fields, ADR 0006 encoding).
# Fill every TODO, then loop to green:
#   python -m taskcontract validate {path} --profile ready
# Contracts are immutable to implementers once ready (write-surface rule, ADR 0010).

id: {task_id}

# 40-1200 chars, outcome terms: what is true after this task that is not true now.
intent: TODO

# Paths / modules this task may touch (>=1).
scope:
  - TODO

# What this task deliberately does not do (>=1).
non_goals:
  - TODO

# Smallest separately-verifiable pieces; 1-3 sketch criteria each.
decomposition:
  - unit: TODO
    done_means: TODO
    acceptance_sketch:
      - TODO

# [] when none; else {{ref: <task-id>, status: resolved}} or
# {{ref: <task-id>, status: blocked, blocked_by: <blocker>}} - blocked parks the
# contract as draft; ready requires every dependency resolved.
dependencies: []

# origin: human-request | g8-escape | g9-maintenance; g8-escape requires ref
# (the incident the escape converges from).
provenance:
  origin: human-request
"""


def scaffold(task_id: str, root: Path | str = ".", schema_doc: dict | None = None) -> Path:
    """Write specs/<id>/contract.yaml under root; refuse bad ids and clobbers."""
    doc = schema_doc or load_schema()
    pattern = doc["properties"]["id"]["pattern"]
    if not re.fullmatch(pattern, task_id):
        raise ValueError(f"id {task_id!r} must match {pattern}")
    path = Path(root) / "specs" / task_id / "contract.yaml"
    if path.exists():
        raise FileExistsError(f"{path} already exists (contracts are never overwritten)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(task_id=task_id, path=path.as_posix()), encoding="utf-8")
    return path
