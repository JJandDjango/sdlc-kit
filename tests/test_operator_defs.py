"""Operator-layer structural suite (contract: operator-layer).

The defs are class-E artifacts (PL-PIPE scopes agent prompts), and the
enforcement layer carries its own regression suite (THEORY): the
shipped pair, the profile command bindings, and the venue map hold
their shape here.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
OPERATORS_DOC = ROOT / "docs" / "operators.md"
DOTNET_DIR = ROOT / "skills" / "sdlc" / "templates" / "profiles" / "dotnet"

SHIPPED = {"sdlc-developer.md", "sdlc-verifier.md"}
PROMPTLANG_TAGS = ("purpose", "context", "instructions", "constraints",
                   "output", "criteria")
CHAIN_CHARS = ";|&>"
GATE_IDS = ("G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9",
            "G10", "PL-DOC", "PL-PIPE")
HUMAN_CONDITIONS = ("G1.3", "G6.1", "G6.2", "G8.3", "PL-PIPE.1")


def _def_text(name: str) -> str:
    return (AGENTS / name).read_text(encoding="utf-8")


def _doc_text() -> str:
    return OPERATORS_DOC.read_text(encoding="utf-8")


# --- unit: operator-defs ---

def test_shipped_pair_is_exactly_the_ratified_set():
    files = {p.name for p in AGENTS.glob("*.md")}
    assert files == SHIPPED  # sdlc-spec / sdlc-qa register, no files ship


def test_defs_carry_frontmatter_and_promptlang_structure():
    for name in SHIPPED:
        text = _def_text(name)
        assert text.startswith("---\n"), name
        frontmatter = text.split("---", 2)[1]
        for field in ("name:", "description:", "tools:", "model:"):
            assert field in frontmatter, (name, field)
        for tag in PROMPTLANG_TAGS:
            assert f"<{tag}>" in text and f"</{tag}>" in text, (name, tag)
        assert "class E" in text, name  # enforcement-layer standing named


def test_developer_manifest_forbids_acceptance_test_source():
    text = _def_text("sdlc-developer.md")
    assert "MUST NOT READ: acceptance-test source" in text
    assert "implementation and unit tests" in text  # the write surface


def test_verifier_writes_nothing_mechanically():
    text = _def_text("sdlc-verifier.md")
    frontmatter = text.split("---", 2)[1]
    tools_line = next(line for line in frontmatter.splitlines()
                      if line.startswith("tools:"))
    assert "Edit" not in tools_line and "Write" not in tools_line
    assert "Write nothing" in text


# --- unit: loop-protocol ---

def test_loop_protocol_names_cap_segment_and_readonly():
    doc = " ".join(_doc_text().split())  # wrap-proof
    assert "Cap 5" in doc
    assert "single chain-free segment" in doc
    assert "read-only to the looping agent" in doc


def test_each_shipped_def_carries_the_loop_with_the_same_cap():
    for name in SHIPPED:
        text = _def_text(name)
        assert "Loop protocol (docs/operators.md)" in text, name
        assert "Cap 5" in text, name
        assert "single chain-free" in text, name
        assert "retry-to-green" in text, name


# --- unit: verdict-contract ---

def test_verdict_conformance_table_covers_all_five_surfaces():
    doc = _doc_text()
    for surface in ("taskcontract validate", "taskcontract vocab-check",
                    "taskcontract suppression-audit", "audit.py",
                    "update.py"):
        assert surface in doc, surface
    assert "argparse usage only" in doc  # the exit-2 delta, named as fact


# --- unit: venue-map ---

def test_venue_map_covers_every_gate_and_rules_hold():
    doc = _doc_text()
    section = doc.split("Venue map")[1].split("\n## ")[0]
    for gate in GATE_IDS:
        assert f"| {gate} " in section, gate
    assert "local preflight" in section
    assert "authoritative, agentless" in section
    assert "sdlc-developer" in section  # the shipped pair appears bound
    for condition in HUMAN_CONDITIONS:
        assert condition in doc, condition


# --- unit: profile-commands ---

def test_dotnet_commands_block_shape_and_chain_free():
    manifest = json.loads((DOTNET_DIR / "profile.json").read_text(
        encoding="utf-8"))
    commands = manifest["commands"]
    assert set(commands) == {"g3", "g4-preflight"}
    for binding, entries in commands.items():
        assert entries, binding
        for command in entries:
            assert isinstance(command, str) and command.strip(), binding
            assert not any(ch in command for ch in CHAIN_CHARS), command


def test_preflight_echoes_the_merge_gate_core():
    manifest = json.loads((DOTNET_DIR / "profile.json").read_text(
        encoding="utf-8"))
    workflow = (DOTNET_DIR / "dotnet-workflow.yml.template").read_text(
        encoding="utf-8")
    preflight = manifest["commands"]["g4-preflight"]
    for needle in ("dotnet restore --locked-mode",
                   "dotnet build --no-restore",
                   "dotnet test --no-build "
                   "-- RunConfiguration.TreatNoTestsAsError=true"):
        assert needle in preflight, needle       # bound for the operator
        assert needle in workflow, needle        # and identical in CI


# --- unit: def-test-suite (self-referential glue) ---

def test_def_command_lines_are_chain_free():
    for name in SHIPPED:
        lines = [line for line in _def_text(name).splitlines()
                 if "python -m taskcontract" in line or "audit.py" in line]
        assert lines, name
        for line in lines:
            assert not any(ch in line for ch in CHAIN_CHARS), (name, line)


def test_def_subcommands_resolve_against_the_cli():
    cli_source = (ROOT / "taskcontract" / "__main__.py").read_text(
        encoding="utf-8")
    available = set(re.findall(r'add_parser\(\s*"([a-z-]+)"', cli_source))
    for name in SHIPPED:
        referenced = set(re.findall(r"python -m taskcontract ([a-z][a-z-]*)",
                                    _def_text(name)))
        assert referenced, name
        assert referenced <= available, (name, referenced - available)
