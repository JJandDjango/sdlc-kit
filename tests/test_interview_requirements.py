"""A requirements run writes the requirements document, for the PO seat alone
(contract: document-split, unit d1-requirements).

The skill is prompt-only, so this suite pins the text of its files, as
tests/test_interview_format.py does. SC1.1: the requirements template holds
the request half's sections in the ratified order, each heading and tag as
kit 0.18.0 wrote them, a bug fix's four among them; then Decisions and open
questions and Notes, each for the PO seat; then the Appendix with Gherkin
and Terms. It holds no Proposed solution, no Risks and cost, no
Traceability, no Contract block and no `---` line. SC2.1: the run asks for
a PO seat and for no engineer seat, asks only the request half's steps, the
Terms and the Gherkin, runs the checks before the PO seat signs, and ends
at that signature by naming the design run as the next command; a later run
goes on at the step its state file names.

Nothing here pins the design run, the design document or its template: a
sentence that names an intake command is left free when it speaks of the
design run.

Text is matched after collapsing each whitespace run to one space, so a
line wrap inside a prompt file never fails a test. No test runs a model;
`python -m prompt_lang` stays the form receipt.
"""

from __future__ import annotations

import re
from pathlib import Path

_HERE = Path(__file__).resolve().parent.parent
# Beside a tree that holds the skill, read that tree; a copy run from any
# other folder reads the tree pytest was started in.
ROOT = _HERE if (_HERE / "skills" / "product-specification-interview").is_dir() else Path.cwd()
SKILL_DIR = ROOT / "skills" / "product-specification-interview"
FLOWS = SKILL_DIR / "flows"
TEMPLATE = SKILL_DIR / "templates" / "requirements-document.md.template"
COMBINED_TEMPLATE = SKILL_DIR / "templates" / "feature-document.md.template"

PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
CHAIN_CHARS = ";|&>"
CHAR_CEILING = 12_000  # tests/test_skill_interview.py CHAR_CEILING

FLOW_FILES = {"opening.md", "request.md", "solution.md", "signing.md", "output.md"}
SKILL_FILES = ({"SKILL.md", "templates/requirements-document.md.template"}
               | {f"flows/{name}" for name in FLOW_FILES})

DESIGN_COMMAND = "/sdlc:product-specification-interview {id} design"
INTAKE_COMMAND = re.compile(r"`/sdlc intake [^`]+`")  # an intake command with its argument
KEPT_MESSAGE = "A document already exists at {path}. Name another path."
DRAFT_COMMAND = "python -m taskcontract lang-check --draft docs/features/{id}.state.yaml"
STATE_KEYS = ("`id`, `phase`, `next`, `origin`, `title`, `seats`, `answers`, `open`,"
              " `history`")
BUG_OPEN, BUG_CLOSE = "{bug fix only}", "{end bug fix only}"

# The requirements document's first lines (Interfaces), in the template's
# placeholders: r1 and the status line name the PO seat alone.
FIRST_LINES = (
    "| Revision Date | Revised By | Changes Made |",
    "| :-: | :-: | :-- |",
    "| {date} | {po} | r1: Created through /sdlc:product-specification-interview."
    " The request half, in progress. PO seat: {po} |",
    "",
    "# {id} - {title}",
    "",
    "`{repo}` · seat: PO {po} · contract: `{id}`, draft · PR: none · merge SHA: none",
)
R1_CHANGES = ("r1: Created through /sdlc:product-specification-interview. The request"
              " half, in progress. PO seat: {po}")

# The request half as kit 0.18.0's template wrote it, byte for byte, from its
# first heading to the close of its last bug-fix-only block.
REQUEST_HALF = """\
## Statement

`[PO seat · authored]`

{statement}

## Description

`[PO seat · authored]`

{description}

{bug fix only}
### Findings at a glance

Incident: {incident_ref}

{findings_at_a_glance}
{end bug fix only}

## Background

`[PO seat · authored]`

{background}

### Existing behavior touched

{existing_behavior}

{bug fix only}
## Findings

`[PO seat · authored]`

{findings}

## Why this happened

`[PO seat · authored]`

{why_this_happened}
{end bug fix only}

## Success criteria

`[PO seat · authored]`

{success_criteria}

## Non-goals

`[PO seat · authored]`

{non_goals}

## Prerequisites

`[PO seat · authored]`

{prerequisites}

## Acceptance criteria

`[PO seat · authored]`

### Checks

{checks}

### Error messages, verbatim

{error_messages}

{bug fix only}
### Regression check

Regression: {regression}
{end bug fix only}
"""

BUG_FIX_ONLY = {"### Findings at a glance", "## Findings", "## Why this happened",
                "### Regression check"}
# The request half in the ratified order, then the document's own record and
# the Appendix's two blocks the PO seat owns.
BUG_FIX_OUTLINE = (
    "## Statement",
    "## Description", "### Findings at a glance",
    "## Background", "### Existing behavior touched",
    "## Findings",
    "## Why this happened",
    "## Success criteria",
    "## Non-goals",
    "## Prerequisites",
    "## Acceptance criteria", "### Checks", "### Error messages, verbatim",
    "### Regression check",
    "## Decisions and open questions",
    "## Notes",
    "## Appendix", "### Gherkin", "### Terms",
)
FEATURE_OUTLINE = tuple(h for h in BUG_FIX_OUTLINE if h not in BUG_FIX_ONLY)
# What a combined document held and a requirements document does not.
ABSENT_HEADINGS = ("## Proposed solution", "### Scope", "### Out of scope",
                   "### Interfaces", "### Sources", "### Constraints", "### Units",
                   "### Order", "## Risks and cost", "## Traceability", "### Links out",
                   "### Record", "### Contract")

PO = "`[PO seat · authored]`"
GHERKIN_TAG = "`[PO seat · derived from r{n}]`"
TAGS = {
    "## Statement": PO, "## Description": PO, "## Background": PO,
    "## Findings": PO, "## Why this happened": PO, "## Success criteria": PO,
    "## Non-goals": PO, "## Prerequisites": PO, "## Acceptance criteria": PO,
    "## Decisions and open questions": PO, "## Notes": PO,
    "### Gherkin": GHERKIN_TAG, "### Terms": PO,
}
# Every `{name}` the template holds: the first lines' five, one per section
# of the request half, then the record's two and the Appendix's.
PLACEHOLDERS = {
    "date", "po", "id", "title", "repo",
    "statement", "description", "incident_ref", "findings_at_a_glance", "background",
    "existing_behavior", "findings", "why_this_happened", "success_criteria",
    "non_goals", "prerequisites", "checks", "error_messages", "regression",
    "decisions", "notes", "n", "gherkin", "terms",
}

REQUEST_STEPS = (
    ("Q1", "STATEMENT"), ("Q2", "DESCRIPTION"), ("Q3", "FINDINGS AT A GLANCE"),
    ("Q4", "BACKGROUND"), ("Q5", "EXISTING BEHAVIOR TOUCHED"), ("Q6", "FINDINGS"),
    ("Q7", "WHY THIS HAPPENED"), ("Q8", "SUCCESS CRITERIA"), ("Q9", "NON-GOALS"),
    ("Q10", "PREREQUISITES"), ("Q11", "CHECKS"), ("Q12", "ERROR MESSAGES"),
    ("Q13", "REGRESSION CHECK"), ("Q14", "TERMS"), ("Q15", "GHERKIN"),
)
PO_STEPS = (("P1", "DRAFT CHECK"), ("P2", "EXISTING BEHAVIOR"), ("P3", "READY CHECKS"),
            ("P4", "STALE BLOCKS"), ("P5", "MEASURED ROW"), ("P6", "SIGN OR GO BACK"),
            ("P7", "SIGNATURE"))

MEASURED_REQUEST = ("r{n}: Measured: the checks before signing, on the request half:"
                    " {findings}; ready checks 1 to 8: {count} OPEN")
FINISHED_REQUEST = "r{n}: The request half finished: {sections} sections written, {open} OPEN"
SIGNED_REQUEST = "r{n}: Signed: request half. The PO seat signs r{m}"

# Wording the unit retires.
RETIRED_COUNT = "fifteen of the eighteen sections"
RETIRED_OPEN = "no engineer seat is named"
RETIRED_SEAT_QUESTION = "then who holds the engineer seat"
RETIRED_EMPTY_SEAT = "The engineer seat can be empty"
RETIRED_SEATS_RECORD = "{po, engineer}"

# The words that show the unit's text stands in each prompt file it touches.
TOUCHED = {
    "SKILL.md": "templates/requirements-document.md.template",
    "flows/opening.md": "templates/requirements-document.md.template",
    "flows/request.md": "for the design run",
    "flows/signing.md": "Is the PO seat named",
    "flows/output.md": f"`{DESIGN_COMMAND}`",
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """The text with each whitespace run collapsed to one space."""
    return " ".join(text.split())


def _prompt_files() -> list[Path]:
    return [SKILL_DIR / "SKILL.md"] + sorted(FLOWS.glob("*.md"))


def _flow(name: str) -> str:
    path = FLOWS / name
    assert path.is_file(), f"flows/{name} is not written"
    return _text(path)


def _instructions(text: str) -> str:
    assert "<instructions>" in text and "</instructions>" in text
    return text.split("<instructions>", 1)[1].split("</instructions>", 1)[0]


def _raw_steps(text: str, letter: str) -> dict[str, str]:
    """Each numbered step of the instructions block, in order: its id mapped
    to its text as written. A step opens a line as `{letter}{n}. `."""
    parts = re.split(rf"^({letter}\d+)\. ", _instructions(text), flags=re.M)
    assert len(parts[1::2]) == len(set(parts[1::2])), "a step id opens two steps"
    return {parts[i]: f"{parts[i]}. {parts[i + 1]}" for i in range(1, len(parts), 2)}


def _steps(name: str, letter: str) -> dict[str, str]:
    """As `_raw_steps` for one flow, each step's whitespace collapsed."""
    return {step: _flat(body) for step, body in _raw_steps(_flow(name), letter).items()}


def _step(name: str, letter: str, step: str) -> str:
    steps = _steps(name, letter)
    assert step in steps, f"flows/{name} has no step {step}"
    return steps[step]


def _po_steps() -> dict[str, str]:
    """The signing flow's steps before the PO seat signs, P1 on, each step's
    whitespace collapsed. The flow's other steps are another seat's."""
    steps = _raw_steps(_flow("signing.md"), "[A-Z]")
    return {step: _flat(body) for step, body in steps.items() if step.startswith("P")}


def _skill_step(number: int) -> str:
    """One numbered step of SKILL.md's instructions, whitespace collapsed."""
    parts = re.split(r"^(\d)\. ", _instructions(_text(SKILL_DIR / "SKILL.md")), flags=re.M)
    steps = {parts[i]: _flat(parts[i + 1]) for i in range(1, len(parts), 2)}
    assert str(number) in steps, f"SKILL.md has no step {number}"
    return steps[str(number)]


def _finished_state_clause() -> str:
    """What SKILL.md's dispatch does for a state file whose phase is
    `complete`: the words of step 1 after that phase's name."""
    route = _skill_step(1)
    assert "`complete` - " in route, "the dispatch has no `complete` phase"
    return route.split("`complete` - ", 1)[1]


def _sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.?!]) ", _flat(text))


def _intake_commands_outside_a_design_run(text: str) -> list[str]:
    """Each sentence that names an intake command with its argument and does
    not speak of the design run, or that names it beside the design run's own
    command."""
    return [sentence for sentence in _sentences(text)
            if INTAKE_COMMAND.search(sentence)
            and ("design run" not in sentence or DESIGN_COMMAND in sentence)]


def _ready_checks() -> dict[int, str]:
    """The ready checks P3 asks: each stands on its own line inside the step,
    as its number, a full stop, then its question."""
    steps = _raw_steps(_flow("signing.md"), "[A-Z]")
    assert "P3" in steps, "flows/signing.md has no step P3"
    return {int(n): line.strip()
            for n, line in re.findall(r"^ +(\d+)\. (.+)$", steps["P3"], flags=re.M)}


def _template() -> str:
    assert TEMPLATE.is_file(), "templates/requirements-document.md.template is not written"
    return _text(TEMPLATE)


def _render(origin: str) -> list[str]:
    """The template's lines as the opening writes them for `origin`: a
    feature drops each bug-fix-only block, markers included; a bug fix keeps
    the block and drops only the two marker lines."""
    out, inside = [], False
    for line in _template().splitlines():
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


def _outline(lines: list[str]) -> list[str]:
    return [line.rstrip() for line in lines
            if line.startswith(("## ", "### ")) or set(line.strip()) == {"-"}]


# --- SC1.1: the requirements template, and the combined one it replaces ---

def test_sc1_1_skill_folder_holds_the_requirements_template_and_no_combined_template():
    assert TEMPLATE.is_file(), "templates/requirements-document.md.template is not written"
    assert not COMBINED_TEMPLATE.exists(), "templates/feature-document.md.template still stands"
    held = {p.relative_to(SKILL_DIR).as_posix() for p in SKILL_DIR.rglob("*") if p.is_file()}
    assert held == SKILL_FILES  # SKILL.md, its five flows, one template, no code
    for path in _prompt_files():
        assert "feature-document.md.template" not in _text(path), path.name
    assert "{skill-dir}/templates/requirements-document.md.template" in _text(
        SKILL_DIR / "SKILL.md")


def test_sc1_1_requirements_document_opens_on_r1_the_title_line_and_a_status_line_for_the_po_seat():
    text = _template()
    lines = text.splitlines()
    assert tuple(lines[:len(FIRST_LINES)]) == FIRST_LINES
    rows = lines[2:lines.index("")]
    assert len(rows) == 1, rows  # r1 alone
    cells = [cell.strip() for cell in rows[0].strip("|").split("|")]
    assert cells == ["{date}", "{po}", R1_CHANGES]
    assert [line for line in lines if line.startswith("# ")] == ["# {id} - {title}"]
    assert "{engineer}" not in text and "engineer" not in text.lower()
    assert "seats:" not in text  # the status line names one seat


def test_sc1_1_request_half_stands_byte_for_byte_as_kit_0_18_0_wrote_it():
    text = _template()
    opening = "\n".join(FIRST_LINES) + "\n\n"
    assert text.startswith(opening + REQUEST_HALF)  # right under the status line
    assert text.count(REQUEST_HALF) == 1
    after = text[len(opening + REQUEST_HALF):]
    assert after.startswith("\n## Decisions and open questions\n"), after[:60]


def test_sc1_1_requirements_document_holds_the_request_half_then_its_record_then_the_appendix():
    assert _outline(_render("feature")) == list(FEATURE_OUTLINE)
    feature = "\n".join(_render("feature"))
    assert "{incident_ref}" not in feature and "{regression}" not in feature
    assert BUG_OPEN not in feature and BUG_CLOSE not in feature


def test_sc1_1_a_bug_fixs_requirements_document_holds_its_four_sections_in_place():
    assert _outline(_render("bug-fix")) == list(BUG_FIX_OUTLINE)
    text = _template()
    blocks = re.findall(re.escape(BUG_OPEN) + r"\n(.*?)" + re.escape(BUG_CLOSE), text,
                        flags=re.S)
    assert len(blocks) == 3, len(blocks)  # 0.18.0's three marked blocks, markers kept
    for heading in BUG_FIX_ONLY:
        assert any(heading in block.splitlines() for block in blocks), heading
    outside = re.sub(re.escape(BUG_OPEN) + r"\n.*?" + re.escape(BUG_CLOSE), "", text,
                     flags=re.S)
    for heading in BUG_FIX_ONLY:
        assert heading not in outside.splitlines(), heading
    assert any("Incident: {incident_ref}" in block for block in blocks)
    assert any("Regression: {regression}" in block for block in blocks)


def test_sc1_1_every_section_carries_its_tag_and_every_tag_names_the_po_seat():
    lines = _render("bug-fix")
    for heading, tag in TAGS.items():
        assert heading in lines, heading
        at = lines.index(heading)
        following = next(line for line in lines[at + 1:] if line.strip())
        assert following == tag, (heading, following)
    tags = [line for line in lines if re.fullmatch(r"`\[[^\]]+\]`", line.strip())]
    assert tags == [PO] * 11 + [GHERKIN_TAG, PO]  # no tag for another seat, none for intake


def test_sc1_1_decisions_and_notes_stand_for_the_po_seat_above_an_appendix_of_gherkin_and_terms():
    lines = _render("feature")
    tail = lines[lines.index("## Decisions and open questions"):]
    assert [line for line in tail if line.strip()] == [
        "## Decisions and open questions", PO, "{decisions}",
        "## Notes", PO, "{notes}",
        "## Appendix",
        "### Gherkin", GHERKIN_TAG, "{gherkin}",
        "### Terms", PO, "{terms}",
    ]
    assert set(re.findall(r"\{([a-z_]+)\}", _template())) == PLACEHOLDERS


def test_sc1_1_requirements_document_holds_no_solution_no_risks_no_traceability_no_contract_and_no_line_between_halves():
    text = _template()
    lines = [line.strip() for line in text.splitlines()]
    for heading in ABSENT_HEADINGS:
        assert heading not in lines, heading
    assert not [line for line in lines if line and set(line) == {"-"}], "a `---` line stands"
    assert "contract.yaml" not in text  # the Contract block's one line
    for words in ("Intake", "Engineer seat", "Both seats"):
        assert words not in text, words
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert "seat boundary" not in skill  # no document of a pair holds the line


def test_sc1_1_the_count_of_a_combined_documents_sections_is_gone_from_every_prompt_file():
    for path in _prompt_files():
        assert RETIRED_COUNT not in _flat(_text(path)), path.name


# --- SC1.1: the opening writes the document from the template ---

def test_sc1_1_opening_refuses_a_standing_document_with_the_kept_message_and_writes_r1_from_the_requirements_template():
    steps = _steps("opening.md", "O")
    assert list(steps) == ["O1", "O2", "O3", "O4", "O5", "O6"]
    assert KEPT_MESSAGE in steps["O1"]  # kept byte for byte
    assert "one Bash call `ls docs/features/{id}.md`" in steps["O1"]
    close = steps["O6"]
    assert "`docs/features/{id}.md`" in close and "r1" in close
    assert "`phase: request`" in close and "`next: Q1`" in close
    assert f"`{BUG_OPEN}`" in close and f"`{BUG_CLOSE}`" in close
    assert "{skill-dir}/templates/requirements-document.md.template" in close
    assert '"none" when empty' not in _flat(_flow("opening.md"))  # no empty seat to fill


def test_sc1_1_no_step_asks_decisions_or_notes_and_each_holds_the_openings_material_else_none():
    asked = {**_steps("opening.md", "O"), **_steps("request.md", "Q"),
             **_po_steps(), **_steps("output.md", "W")}
    for step, body in asked.items():
        name = body.split(" - ", 1)[0]
        assert "DECISIONS" not in name and "NOTES" not in name, step
    materials = _step("opening.md", "O", "O5")
    assert "decisions and open questions, notes" in materials  # O5 still extracts both
    close = _step("opening.md", "O", "O6")
    assert "Decisions and open questions and Notes" in close
    assert 'the material O5 confirmed, else "(none)"' in close
    assert 'reads "(not yet asked)"' in close  # every other section no step has written


# --- SC2.1: one seat ---

def test_sc2_1_opening_asks_for_a_po_seat_and_for_no_engineer_seat():
    seats = _step("opening.md", "O", "O4")
    assert seats.startswith("O4. SEATS - ")
    assert "ASK who holds the PO seat" in seats
    assert RETIRED_SEAT_QUESTION not in seats
    assert RETIRED_EMPTY_SEAT not in seats
    assert "solution.md" not in seats  # no seat decides whether a half is asked
    assert "no engineer seat" in seats
    assert "Record `seats: {po}`" in seats


def test_state_file_keeps_schema_2_and_its_nine_keys_and_a_requirements_run_records_the_po_seat_alone():
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert "`docs/features/{id}.state.yaml`" in skill
    assert "`schema: spec-interview-state/2`" in skill
    assert STATE_KEYS in skill  # the nine keys, none added and none dropped
    first = _step("opening.md", "O", "O1")
    assert "`schema: spec-interview-state/2`" in first
    for path in _prompt_files():
        assert "spec-interview-state/3" not in _text(path), path.name
    opening = _flat(_flow("opening.md"))
    assert RETIRED_SEATS_RECORD not in opening
    assert "Record `seats: {po}`" in opening


# --- SC2.1: the steps a requirements run asks ---

def test_sc2_1_requirements_run_asks_only_the_request_halfs_steps_the_terms_and_the_gherkin():
    steps = _steps("request.md", "Q")
    assert list(steps) == [step for step, _ in REQUEST_STEPS]
    for step, name in REQUEST_STEPS:
        assert steps[step].startswith(f"{step}. {name} - "), (step, steps[step][:40])
    signing = _po_steps()
    assert list(signing) == [step for step, _ in PO_STEPS]
    # From Q1 to W2 no step hands the run to a step or a phase of the other half.
    run = {**steps, **signing, **_steps("output.md", "W")}
    for step, body in run.items():
        for following in re.findall(r"`next: ([A-Za-z0-9]+)`", body):
            assert re.fullmatch(r"[QPW]\d+|null", following), (step, following)
        for phase in re.findall(r"`phase: ([a-z]+)`", body):
            assert phase in ("request", "output", "complete"), (step, phase)


def test_a_place_the_po_seat_refuses_at_non_goals_is_kept_in_the_state_file_for_the_design_run():
    non_goals = _step("request.md", "Q", "Q9")
    assert "a thing we will not build, or a place we will not touch?" in non_goals
    assert "`answers.non_goals`" in non_goals
    assert re.search(r"a place we will not touch goes to `answers\.out_of_scope`[^.]*"
                     r"for the design run", non_goals), non_goals
    assert "Record `answers.non_goals` (list" in non_goals


# --- SC2.1: the checks before the PO seat signs, and the signature ---

def test_sc2_1_checks_run_before_the_po_seat_signs_and_ready_check_8_names_the_po_seat_alone():
    steps = _po_steps()
    for step, name in PO_STEPS:
        assert step in steps, step
        assert steps[step].startswith(f"{step}. {name} - "), (step, steps[step][:40])
    assert f"one Bash call `{DRAFT_COMMAND}`" in steps["P1"]
    assert "READ the document against ready checks 1 to 8, each a question" in steps["P3"]
    assert f"`{MEASURED_REQUEST}`" in steps["P5"]  # `Measured:`, kept byte for byte
    assert "ASK the PO seat" in steps["P6"]
    checks = _ready_checks()
    assert list(checks) == list(range(1, 9))
    eighth = checks[8]
    assert eighth.endswith("?"), eighth  # the question, and no OPEN line for a seat
    for words in ("bug fix", "`Measured:` row"):
        assert words in eighth, words
    assert "both seats" not in steps["P3"].lower()
    assert "the PO seat named" in eighth
    for path in _prompt_files():
        assert RETIRED_OPEN not in _flat(_text(path)), path.name
    for step, body in steps.items():
        assert "`seats.engineer`" not in body, step


def test_sc2_1_the_po_seats_signature_keeps_its_row_and_hands_the_run_to_the_output_flow():
    signed = _po_steps().get("P7", "")
    assert f"`{FINISHED_REQUEST}`" in signed
    assert f"`{SIGNED_REQUEST}`" in signed  # `Signed: request half`, kept byte for byte
    assert signed.index(f"`{FINISHED_REQUEST}`") < signed.index(f"`{SIGNED_REQUEST}`")
    assert "right after the first" in signed and "no row between" in signed
    assert "`seats.po`" in signed
    assert "event: request half signed" in signed
    assert "`next: S1`" not in signed and "`phase: solution`" not in signed
    assert "`phase: output`" in signed and "`next: W1`" in signed
    assert signed.index(f"`{SIGNED_REQUEST}`") < signed.index("`next: W1`")
    assert re.search(r"^W1\. ", _flow("output.md"), flags=re.M)


def test_sc2_1_the_run_ends_by_naming_the_design_run_as_the_next_command():
    last = _step("output.md", "W", "W2")
    assert "`phase: complete`" in last and "`next: null`" in last
    assert "the document path" in last and "the state file path" in last
    assert f"`{DESIGN_COMMAND}`" in last
    assert "next command" in last
    assert _intake_commands_outside_a_design_run(_flow("output.md")) == []
    skill = _text(SKILL_DIR / "SKILL.md")
    assert f"`{DESIGN_COMMAND}`" in _skill_step(3)  # the report at the end
    assert _intake_commands_outside_a_design_run(skill) == []
    assert "never run `/sdlc intake`" in skill  # the write surface stays


# --- SC2.1: a later run ---

def test_sc2_1_a_later_run_goes_on_at_the_step_its_state_file_names():
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert "a later run resumes at the exact step `next` names" in skill
    assert "EXECUTE the flow from the step `next` names" in skill
    assert "Exactly one file resumes" in skill and "none starts a new run" in skill
    for name in ("request.md", "signing.md"):
        assert "writes the state file with `next` unchanged" in _flat(_flow(name)), name
    # Each flow of the run leaves `next` at the first step of the flow after it.
    hand_overs = (("opening.md", "O", "O6", "request", "Q1"),
                  ("request.md", "Q", "Q15", "request", "P1"),
                  ("signing.md", "[A-Z]", "P7", "output", "W1"),
                  ("output.md", "W", "W2", "complete", "null"))
    for name, letter, step, phase, following in hand_overs:
        body = _step(name, letter, step)
        assert f"`phase: {phase}`" in body, (step, phase)
        assert f"`next: {following}`" in body, (step, following)
    assert ("`request` - LOAD {skill-dir}/flows/request.md, or {skill-dir}/flows/signing.md"
            " when `next` names a P step") in skill
    assert "`output` - LOAD {skill-dir}/flows/output.md" in skill


def test_a_run_on_a_finished_state_reports_its_paths_and_the_design_runs_command_then_offers_the_way_back():
    clause = _finished_state_clause()
    assert clause.startswith("REPORT"), clause[:40]
    assert "the document path" in clause
    assert f"`{DESIGN_COMMAND}`" in clause
    assert "the state file path" in clause
    assert "back to a section" in clause
    assert clause.index(f"`{DESIGN_COMMAND}`") < clause.index("back to a section")
    # The way back runs that section's step, then the checks and the signature again.
    assert "{skill-dir}/flows/request.md" in clause
    assert "`next: P1`" in clause


# --- the unit's done_means ---

def test_done_means_requirements_document_names_the_po_seat_only_and_the_design_run_is_named_after_its_signature():
    seat_lines = [line for line in _template().splitlines() if "seat" in line.lower()]
    assert seat_lines, "the template names no seat"
    for line in seat_lines:
        assert "PO seat" in line or "seat: PO {po}" in line, line
        assert "ngineer" not in line and "Both seats" not in line, line
    signed = _po_steps().get("P7", "")
    assert f"`{SIGNED_REQUEST}`" in signed and "`next: W1`" in signed
    steps = _steps("output.md", "W")
    assert list(steps) == ["W1", "W2"]
    assert f"`{DESIGN_COMMAND}`" in steps["W2"]


# --- Constraints 1 and 2 of the feature document ---

def test_c1_c2_every_prompt_file_the_unit_touches_keeps_the_promptlang_form_the_ceiling_and_one_segment_commands():
    for name, marker in TOUCHED.items():
        path = SKILL_DIR / name
        assert path.is_file(), f"{name} is not written"
        text = _text(path)
        assert marker in _flat(text), (name, "the unit's text is missing")
        assert text.startswith("---\n") and "name:" in text.split("---", 2)[1], name
        description = next(line for line in text.split("---", 2)[1].splitlines()
                           if line.startswith("description:"))
        value = description[len("description:"):].strip()
        assert value and not value.startswith(('"', "'", ">", "|")), name
        assert ": " not in value and " #" not in value, name
        opened = re.findall(r"<([a-z][a-z0-9-]*)>", text)
        assert {"purpose", "instructions"} <= set(opened), name
        assert set(opened) <= PROMPTLANG_TAGS, (name, set(opened) - PROMPTLANG_TAGS)
        for tag in opened:
            assert f"</{tag}>" in text, (name, tag)
    for path in _prompt_files():
        text = _text(path)
        assert len(text) < CHAR_CEILING, (path.name, len(text))
        for line in text.splitlines():
            if "one Bash call" in line:
                commands = re.findall(r"`([^`]+)`", line)
                assert commands, (path.name, line)
                for command in commands:
                    assert not any(ch in command for ch in CHAIN_CHARS), (path.name, command)
