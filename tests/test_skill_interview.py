"""Specification-interview structural suite (contract: spec-interview).

The skill is prompt-only, so its regression suite holds the shape the
contract names (ADR 0028): the file set, the frontmatter, the PromptLang
tag set, dispatch coverage, the template's section order, the write
surface, and chain-free command lines. `python -m prompt_lang` is the
form receipt; this suite is the CI-side proxy that needs no validator.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "skills" / "product-specification-interview"
FLOWS = SKILL_DIR / "flows"
TEMPLATE = SKILL_DIR / "templates" / "feature-document.md.template"

FLOW_FILES = {"opening.md", "sections.md", "readiness.md", "output.md"}
FLOW_FIRST_STEP = {"opening.md": "O1.", "sections.md": "Q1.",
                   "readiness.md": "R1.", "output.md": "W1."}
PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
SKILL_TAGS = ("purpose", "variables", "context", "instructions",
              "constraints", "criteria")
CHAIN_CHARS = ";|&>"
TEMPLATE_SECTIONS = (
    "## Feature statement", "## Description", "## Background Information",
    "## Success Criteria", "## Requirements", "## Previously Defined",
    "## Prerequisites", "## Business Requirements", "## Implementation",
    "## Misc.", "## Acceptance Criteria", "## Additional Notes",
)
SECTION_STEPS = (
    "Q1. FEATURE STATEMENT", "Q2. DESCRIPTION", "Q3. BACKGROUND",
    "Q4. SUCCESS CRITERIA", "Q5. REQUIREMENTS", "Q6. PREVIOUSLY DEFINED",
    "Q7. PREREQUISITES", "Q8. BUSINESS REQUIREMENTS", "Q9. IMPLEMENTATION",
    "Q10. MISC", "Q11. ACCEPTANCE CRITERIA", "Q12. ADDITIONAL NOTES",
)
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

def test_skill_file_set_is_exactly_the_ratified_set():
    assert (SKILL_DIR / "SKILL.md").is_file()
    assert {p.name for p in FLOWS.glob("*.md")} == FLOW_FILES
    assert TEMPLATE.is_file()
    assert not (SKILL_DIR / "modules").exists()  # deferred, ADR 0028


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


def test_dispatch_names_every_flow_and_phase():
    text = _text(SKILL_DIR / "SKILL.md")
    for name in FLOW_FILES:
        assert f"flows/{name}" in text, name
    for phase in ("`opening`", "`sections`", "`readiness`", "`output`", "`complete`"):
        assert phase in text, phase
    assert "none starts a new run" in text  # no state file -> the first question
    assert "Exactly one file resumes" in text  # a state file -> the recorded step


def test_every_prompt_file_stays_under_the_budget_proxy():
    for path in _prompt_files():
        assert len(_text(path)) < CHAR_CEILING, path.name


# --- unit: s3-interview-flows ---

def test_each_flow_opens_on_its_first_step():
    for name, first in FLOW_FIRST_STEP.items():
        assert first in _text(FLOWS / name), name


def test_sections_follow_the_template_order_with_a_state_write():
    text = _text(FLOWS / "sections.md")
    positions = [text.index(step) for step in SECTION_STEPS]
    assert positions == sorted(positions)
    assert "WRITE the state file with the section's answers" in text
    assert "Six criteria is two features" in text  # the split guard
    assert "left for intake (no engineer seat)" in text


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


def test_output_writes_from_the_template_and_names_intake():
    text = _text(FLOWS / "output.md")
    assert "templates/feature-document.md.template" in text
    assert "A document already exists at {path}. Name another path." in text
    assert "`/sdlc intake {path}`" in text
    assert "Google Docs form" in text


def test_template_carries_every_section_in_order():
    text = _text(TEMPLATE)
    positions = [text.index(heading) for heading in TEMPLATE_SECTIONS]
    assert positions == sorted(positions)
    assert "| Revision Date | Revised By | Changes Made |" in text
    assert "**Seats:**" in text
    assert "**Not in scope:**" in text
    assert "Reserved for intake" in text


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
    assert len(lines) >= 3  # dispatch, O5, W2
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
