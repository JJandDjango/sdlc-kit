"""Specification-interview structural suite (contract: spec-interview).

The skill is prompt-only, so its regression suite holds the shape the
contract names (ADR 0028): the frontmatter, the PromptLang tag set, the
write surface, and chain-free command lines. The template's sections and
the document's path are tests/test_interview_format.py's; the file set,
the dispatch and each half's steps are tests/test_interview_sections.py's
(contract: feature-document).
`python -m prompt_lang` is the form receipt; this suite is the CI-side
proxy that needs no validator.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "skills" / "product-specification-interview"
FLOWS = SKILL_DIR / "flows"

FLOW_FIRST_STEP = {"opening.md": "O1.", "request.md": "Q1.", "solution.md": "S1.",
                   "readiness.md": "R1.", "output.md": "W1."}
PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
SKILL_TAGS = ("purpose", "variables", "context", "instructions",
              "constraints", "criteria")
CHAIN_CHARS = ";|&>"
# Coarse token-budget proxy: PromptLang fails a file at 4000 cl100k
# tokens; kit prose runs about 3.5 characters per token.
CHAR_CEILING = 12_000


def _prompt_files() -> list[Path]:
    return [SKILL_DIR / "SKILL.md"] + sorted(FLOWS.glob("*.md"))


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    assert text.startswith("---\n")
    return text.split("---", 2)[1]


# --- unit: s2-skill-entry ---

def test_skill_name_is_the_command():
    frontmatter = _frontmatter(_text(SKILL_DIR / "SKILL.md"))
    assert "name: product-specification-interview\n" in frontmatter
    assert "argument-hint:" in frontmatter


def test_every_prompt_file_carries_plain_safe_frontmatter():
    for path in _prompt_files():
        frontmatter = _frontmatter(_text(path))
        assert "name:" in frontmatter, path.name
        description = next(line for line in frontmatter.splitlines()
                           if line.startswith("description:"))
        value = description[len("description:"):].strip()
        assert value and not value.startswith(('"', "'", ">", "|")), path.name
        assert ": " not in value and " #" not in value, path.name


def test_only_promptlang_tags_appear_and_every_tag_closes():
    for path in _prompt_files():
        text = _text(path)
        opened = re.findall(r"<([a-z][a-z0-9-]*)>", text)
        assert opened, path.name
        assert set(opened) <= PROMPTLANG_TAGS, (path.name, set(opened) - PROMPTLANG_TAGS)
        for tag in opened:
            assert f"</{tag}>" in text, (path.name, tag)
        assert "<purpose>" in text and "<instructions>" in text, path.name


def test_skill_entry_carries_every_block():
    text = _text(SKILL_DIR / "SKILL.md")
    for tag in SKILL_TAGS:
        assert f"<{tag}>" in text and f"</{tag}>" in text, tag


def test_every_prompt_file_stays_under_the_budget_proxy():
    for path in _prompt_files():
        assert len(_text(path)) < CHAR_CEILING, path.name


# --- unit: s3-interview-flows ---

def test_each_flow_opens_on_its_first_step():
    for name, first in FLOW_FIRST_STEP.items():
        assert first in _text(FLOWS / name), name


def test_opening_writes_the_state_file_and_never_overwrites():
    text = _text(FLOWS / "opening.md")
    assert "WRITE the state file" in text
    assert "A document already exists at {path}. Name another path." in text


# --- unit: s4-document-flows ---

def test_readiness_advises_and_never_blocks():
    text = _text(FLOWS / "readiness.md")
    assert "never blocks" in text
    assert "OPEN" in text
    assert "the user's word to write is final" in text


# --- unit: s5-shape-and-docs ---

def test_write_surface_is_the_document_and_its_state_file():
    text = _text(SKILL_DIR / "SKILL.md")
    assert "Write ONLY the document and its state file" in text
    assert "never run `/sdlc intake`" in text
    assert "Never overwrite" in text
    assert "single segment" in text


def test_bash_call_commands_are_chain_free():
    lines = [line for path in _prompt_files()
             for line in _text(path).splitlines() if "one Bash call" in line]
    assert len(lines) >= 2  # dispatch, O1
    for line in lines:
        commands = re.findall(r"`([^`]+)`", line)
        assert commands, line  # the authored command is always a code span
        for command in commands:
            assert not any(ch in command for ch in CHAIN_CHARS), command


def test_usage_and_changelog_name_the_skill():
    usage = _text(ROOT / "USAGE.md")
    assert "/sdlc:product-specification-interview" in usage
    assert usage.index("/sdlc:product-specification-interview") < usage.index(
        "### `/sdlc intake`")
    assert "product-specification-interview" in _text(ROOT / "CHANGELOG.md")
