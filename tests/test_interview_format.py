"""The interview writes the ratified format (contract: feature-document, unit f1-format).

The skill is prompt-only, so this suite pins the text of its files, as
tests/test_skill_interview.py does: the prompt files write the document at
`docs/features/{id}.md` from r1, with its state file beside it (SC1.1).
The template is the requirements document's; its rows, sections and tags
are held by tests/test_interview_requirements.py, and here only its title
line and its bug-fix-only blocks are read.
No test runs a model; `python -m prompt_lang` stays the form receipt.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "skills" / "product-specification-interview"
FLOWS = SKILL_DIR / "flows"
TEMPLATE = SKILL_DIR / "templates" / "requirements-document.md.template"
DESIGN_TEMPLATE = SKILL_DIR / "templates" / "design-document.md.template"

PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
CHAIN_CHARS = ";|&>"
CHAR_CEILING = 12_000  # tests/test_skill_interview.py CHAR_CEILING

KEPT_MESSAGE = "A document already exists at {path}. Name another path."
STATE_LS = "ls docs/features/{id}.state.yaml"
DOCUMENT_LS = "ls docs/features/{id}.md"
BUG_OPEN, BUG_CLOSE = "{bug fix only}", "{end bug fix only}"

# The revision table's two heading lines, the document's first.
FIRST_LINES = (
    "| Revision Date | Revised By | Changes Made |",
    "| :-: | :-: | :-- |",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _prompt_files() -> list[Path]:
    return [SKILL_DIR / "SKILL.md"] + sorted(FLOWS.glob("*.md"))


def _render(origin: str) -> list[str]:
    """The template's lines as the opening writes them for `origin`: a
    feature drops each bug-fix-only block, markers included; a bug fix keeps
    the block and drops only the two marker lines."""
    out, inside = [], False
    for line in _text(TEMPLATE).splitlines():
        if line.strip() == BUG_OPEN:
            assert not inside, "nested bug-fix-only block"
            inside = True
            continue
        if line.strip() == BUG_CLOSE:
            assert inside, "bug-fix-only block closed before it opened"
            inside = False
            continue
        if origin == "bug-fix" or not inside:
            out.append(line)
    assert not inside, "bug-fix-only block never closed"
    return out


def _blocks(text: str) -> list[str]:
    """The text of each bug-fix-only block in the template."""
    return re.findall(re.escape(BUG_OPEN) + r"\n(.*?)" + re.escape(BUG_CLOSE),
                      text, flags=re.S)


def _instruction_steps(text: str, letter: str) -> list[str]:
    assert "<instructions>" in text and "</instructions>" in text
    body = text.split("<instructions>", 1)[1].split("</instructions>", 1)[0]
    return [line for line in body.splitlines() if re.match(rf"{letter}\d+\. ", line)]


# --- SC1.1: the path, the state file beside it, the dispatch ---

def test_sc1_1_document_and_state_file_live_under_docs_features():
    skill = _text(SKILL_DIR / "SKILL.md")
    assert "`docs/features/{id}.md`" in skill
    assert "`docs/features/{id}.state.yaml`" in skill
    opening = _text(FLOWS / "opening.md")
    assert "WRITE the state file `docs/features/{id}.state.yaml`" in opening
    for path in _prompt_files() + [TEMPLATE]:
        assert "REQUEST_{slug}_{date}" not in _text(path), path.name
    for path in (SKILL_DIR / "SKILL.md", FLOWS / "opening.md", FLOWS / "output.md"):
        for old in ("Business Requirements", "Previously Defined", "Jira key"):
            assert old not in _text(path), (path.name, old)  # ADR 0026's template retires


def test_sc1_1_state_file_carries_schema_2_and_the_interfaces_keys():
    opening = _text(FLOWS / "opening.md")
    assert "`schema: spec-interview-state/2`" in opening
    for key in ("id", "phase", "next", "origin", "title", "seats", "answers", "open",
                "history"):
        assert re.search(rf"`{key}[`:]", opening), key  # `key` or `key: value`
    for path in _prompt_files():
        assert "spec-interview-state/1" not in _text(path), path.name


def test_sc1_1_an_old_request_state_file_is_never_read_and_the_run_starts_fresh():
    skill = _text(SKILL_DIR / "SKILL.md")
    assert ("A state file at the old `REQUEST_{slug}_*.state.yaml` path is never read:"
            " a run for that id starts fresh.") in skill
    for path in _prompt_files() + [TEMPLATE]:
        for line in _text(path).splitlines():
            if "REQUEST_" in line:
                assert "is never read" in line, (path.name, line)


def test_sc1_1_dispatch_finds_the_state_file_at_its_one_path_in_one_bash_call():
    skill = _text(SKILL_DIR / "SKILL.md")
    lines = [line for line in skill.splitlines() if f"`{STATE_LS}`" in line]
    assert lines, "dispatch never names the state file's one path"
    assert all("one Bash call" in line for line in lines), lines
    assert "ls REQUEST_" not in skill
    assert "`^[a-z][a-z0-9-]{2,63}$`" in skill  # the id pattern stays


# --- SC1.1: the title line, numbered revision rows ---

def test_sc1_1_template_opens_on_the_revision_table_then_the_title_line():
    lines = _text(TEMPLATE).splitlines()
    assert tuple(lines[:len(FIRST_LINES)]) == FIRST_LINES
    titles = [line for line in lines if line.startswith("# ")]
    assert titles == ["# {id} - {title}"]  # the one title line, ADR 0035
    assert "{{" not in _text(TEMPLATE)  # placeholders are {name}, one brace
    opening = _text(FLOWS / "opening.md")
    assert "`# {id} - {title}`" in opening
    assert "ABC-1234" not in opening  # the Jira-key title retires


def test_sc1_1_each_later_revision_row_takes_the_next_number():
    skill = _text(SKILL_DIR / "SKILL.md")
    assert "Every revision row opens `r{n}: `, numbered one past the table's last row" in skill


# --- SC1.1: the bug-fix-only blocks ---

def test_sc1_1_bug_fix_sections_carry_the_incident_reference_and_regression_scenario():
    blocks = _blocks(_text(TEMPLATE))
    glance = [b for b in blocks if "### Findings at a glance" in b.splitlines()]
    regression = [b for b in blocks if "### Regression check" in b.splitlines()]
    assert glance, "no bug-fix-only block holds ### Findings at a glance"
    assert "{incident_ref}" in glance[0]
    assert regression, "no bug-fix-only block holds ### Regression check"
    assert "{regression}" in regression[0]
    feature = "\n".join(_render("feature"))
    assert "{incident_ref}" not in feature and "{regression}" not in feature
    opening = _text(FLOWS / "opening.md")
    assert f"`{BUG_OPEN}`" in opening and f"`{BUG_CLOSE}`" in opening
    assert "never leaves them empty" in opening


# --- SC1.1: when the document is written, and what the interview writes ---

def test_sc1_1_opening_writes_the_document_as_r1_at_its_last_step():
    opening = _text(FLOWS / "opening.md")
    steps = _instruction_steps(opening, "O")
    assert steps, "the opening has no numbered steps"
    last = steps[-1]
    assert "templates/requirements-document.md.template" in last, last
    assert "`docs/features/{id}.md`" in last and "r1" in last, last
    skill = _text(SKILL_DIR / "SKILL.md")
    assert "each section into the document as its step closes" in skill


def test_sc1_1_write_surface_is_the_document_and_its_state_file_never_specs_or_intake():
    skill = _text(SKILL_DIR / "SKILL.md")
    assert "never write a `Ready:` or `Parked:` row" in skill
    assert "never edit an existing document" not in skill  # retired: it writes its own
    assert "Write ONLY the document and its state file" in skill
    assert "Never write under `specs/`" in skill
    assert "never run `/sdlc intake`" in skill


def test_sc1_1_existing_path_is_refused_at_the_opening_with_its_kept_message():
    opening = _text(FLOWS / "opening.md")
    steps = [line for line in _instruction_steps(opening, "O") if f"`{DOCUMENT_LS}`" in line]
    assert len(steps) == 1, "the opening checks the document's path in one step"
    assert "one Bash call" in steps[0]
    assert KEPT_MESSAGE in steps[0]
    assert "Never overwrite" in _text(SKILL_DIR / "SKILL.md")


def test_sc1_1_output_keeps_the_google_docs_form_and_writes_nothing():
    output = _text(FLOWS / "output.md")
    assert "Nothing is written" in output
    assert "Google Docs form" in output
    assert ".md.template" not in output  # W1's render retires
    assert "WRITE the document" not in output  # W3's write retires
    assert "one Bash call" not in output  # W2's path check retires to the opening


# --- Constraints 1 to 3 of the feature document ---

def test_c1_touched_prompt_files_keep_the_promptlang_tags_and_the_ceiling():
    touched = {SKILL_DIR / "SKILL.md": "`docs/features/{id}.state.yaml`",
               FLOWS / "opening.md": "`docs/features/{id}.md`",
               FLOWS / "output.md": "Nothing is written"}
    for path, marker in touched.items():
        text = _text(path)
        assert marker in text, (path.name, "f1's text is missing")
        assert text.startswith("---\n") and "name:" in text.split("---", 2)[1], path.name
        opened = re.findall(r"<([a-z][a-z0-9-]*)>", text)
        assert set(opened) <= PROMPTLANG_TAGS, (path.name, set(opened) - PROMPTLANG_TAGS)
        for tag in opened:
            assert f"</{tag}>" in text, (path.name, tag)
        assert len(text) < CHAR_CEILING, (path.name, len(text))


def test_c2_every_shell_command_a_prompt_file_authors_is_one_segment():
    commands = [(path.name, command) for path in _prompt_files()
                for line in _text(path).splitlines() if "one Bash call" in line
                for command in re.findall(r"`([^`]+)`", line)]
    assert ("SKILL.md", STATE_LS) in commands and ("opening.md", DOCUMENT_LS) in commands
    for name, command in commands:
        assert not any(ch in command for ch in CHAIN_CHARS), (name, command)


def test_c3_skill_stays_prompt_only_with_its_template():
    assert "# {id} - {title}" in _text(TEMPLATE).splitlines()  # f1's template
    for path in SKILL_DIR.rglob("*"):
        if path.is_file():
            assert path.suffix == ".md" or path in (TEMPLATE, DESIGN_TEMPLATE), path
