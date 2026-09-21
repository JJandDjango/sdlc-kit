"""Shared loaders for the /sdlc skill engines (skills/sdlc is not a package).

Also the seat-roster writer: since ADR 0030 the ready profile needs a
ratified `intake-seat` term, so every tmp specs tree that validates a
contract at ready has to carry one. One writer, so the roster a test
seeds is the roster every other test seeds.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

SKILL_DIR = Path(__file__).parent.parent / "skills" / "sdlc"


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
