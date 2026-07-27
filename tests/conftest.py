"""Shared loaders for the /sdlc skill engines (skills/sdlc is not a package)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).parent.parent / "skills" / "sdlc"


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
