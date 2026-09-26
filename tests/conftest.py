"""Shared loaders for the /sdlc skill engines (skills/sdlc is not a package).

Also the seat-roster writer: since ADR 0030 the ready profile needs a
ratified `intake-seat` term, so every tmp specs tree that validates a
contract at ready has to carry one. One writer, so the roster a test
seeds is the roster every other test seeds.

Also the pane suites' two line helpers (tests/test_tree_pane.py and
tests/test_pane_view.py) and the item-line pattern they read: one copy, so
the cut and the short id both suites expect are the same.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest
import yaml

SKILL_DIR = Path(__file__).parent.parent / "skills" / "sdlc"

# An item line of `taskcontract tree`: its indent, its id, then its plain
# name when it has one (project-tree o2), then its status (or a finding's
# kind) in brackets, then the rest of the line.
ROW = re.compile(r"^(?P<indent> *)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                 r"(?P<rest>.*)$")


def write_seat_roster(root, status="ratified", values=("user",)):
    """Write specs/vocabulary/intake-seat.yaml under `root`; return its path."""
    vocab = Path(root) / "specs" / "vocabulary"
    vocab.mkdir(parents=True, exist_ok=True)
    path = vocab / "intake-seat.yaml"
    path.write_text(yaml.safe_dump({
        "term": "intake-seat",
        "name": "Intake seat",
        "definition": ("A human position that answers for a decomposition "
                       "unit at intake."),
        "kind": "value-set",
        "values": list(values),
        "status": status,
        "since": "2026-08-26",
    }, sort_keys=False), encoding="utf-8")
    return path


def cut_lines(lines, width):
    """Each line as the pane cuts it: whole when it fits the width, else its
    prefix ending in `...`, exactly the width long."""
    return [line if len(line) <= width else line[:width - 3] + "..." for line in lines]


def short_line(line):
    """The whole tree's line for an item under another item, as the pane
    prints it since pane-view's p2-short-ids: the leading full id cut to its
    last segment, the indent and the rest of the line kept byte for byte."""
    match = ROW.match(line)
    assert match, f"not an item line: {line!r}"
    indent, full = match["indent"], match["id"]
    return indent + full.rsplit("/", 1)[-1] + line[len(indent) + len(full):]


def _load(stem: str):
    spec = importlib.util.spec_from_file_location(f"sdlc_skill_{stem}", SKILL_DIR / f"{stem}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def skill_init():
    return _load("init")


@pytest.fixture(scope="session")
def skill_audit():
    return _load("audit")


@pytest.fixture(scope="session")
def skill_update():
    return _load("update")
