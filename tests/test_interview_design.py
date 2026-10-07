"""A design run writes the design document, for one engineer seat
(contract: document-split, unit d2-design).

The skill is prompt-only, so this suite pins the text of its files, as
tests/test_interview_requirements.py does. SC1.2: the design template names
the requirements revision the design stands against, then holds the Proposed
solution's seven sections as kit 0.18.0 wrote them, Risks and cost, Consult
cases, its own Decisions and open questions, Traceability, Notes and the
Appendix's Contract block, with no section tagged for the PO seat; the Google
Docs form shows the run's own document alone. SC2.2: a design run starts only
on a requirements document the PO seat has signed at its newest text
revision, and otherwise stops with its message and writes nothing; it asks
for an engineer seat and for no PO seat, shows that seat each place the PO
seat refused at Non-goals, asks only the solution half's steps and the four
cases, and a later run goes on at the step its own state file names. SC5.1:
the four cases are asked one at a time, each answer is written as yes or no,
and a yes takes who was asked and what was decided.

Nothing here pins the checks before the engineer seat signs, its signature,
the `Measured:` and `Signed:` rows of a design document, a design behind its
requirements, the tree or intake.

Text is matched after collapsing each whitespace run to one space, so a
line wrap inside a prompt file never fails a test. A sentence the sources
give no file for is looked for in SKILL.md and in every flow file. No test
runs a model; `python -m prompt_lang` stays the form receipt.
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
TEMPLATES = SKILL_DIR / "templates"
REQUIREMENTS_TEMPLATE = TEMPLATES / "requirements-document.md.template"
DESIGN_TEMPLATE = TEMPLATES / "design-document.md.template"

PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
CHAIN_CHARS = ";|&>"
CHAR_CEILING = 12_000  # tests/test_skill_interview.py CHAR_CEILING

DESIGN_COMMAND = "/sdlc:product-specification-interview {id} design"
INTAKE_COMMAND = "`/sdlc intake docs/features/{id}.md`"
REQUIREMENTS_PATH = "`docs/features/{id}.md`"
REQUIREMENTS_STATE = "`docs/features/{id}.state.yaml`"
DESIGN_PATH = "`docs/features/{id}.design.md`"
DESIGN_STATE = "`docs/features/{id}.design.state.yaml`"
STATE_KEYS = ("`id`, `phase`, `next`, `origin`, `title`, `seats`, `answers`, `open`,"
              " `history`")
KEPT_MESSAGE = "A document already exists at {path}. Name another path."

# The stops of a design run's start, verbatim.
NO_DOCUMENT = "No requirements document for {id}. Run the requirements interview first."
UNSIGNED = ("The requirements document is unsigned at r{n}. The PO seat signs before the"
            " design starts.")
COMBINED = "{path} is a combined document. Split it by hand, then run the design interview."

# The design document's first lines (Interfaces), in the template's
# placeholders: r1 names the requirements revision and the engineer seat, and
# the status line names that seat and the requirements document's path.
FIRST_LINES = (
    "| Revision Date | Revised By | Changes Made |",
    "| :-: | :-: | :-- |",
    "| {date} | {engineer} | r1: Created through /sdlc:product-specification-interview."
    " The design, in progress, against requirements r{m}. Engineer seat: {engineer} |",
    "",
    "# {id} - {title}",
    "",
    "`{repo}` · seat: engineer {engineer} · requirements: `docs/features/{id}.md`"
    " · contract: `{id}`, draft · PR: none · merge SHA: none",
)
R1_CHANGES = ("r1: Created through /sdlc:product-specification-interview. The design,"
              " in progress, against requirements r{m}. Engineer seat: {engineer}")

# The Proposed solution as kit 0.18.0's template wrote it, byte for byte, from
# its heading to its seventh section.
PROPOSED_SOLUTION = """\
## Proposed solution

`[Engineer seat · authored]`

### Scope

{scope}

### Out of scope

{out_of_scope}

### Interfaces

{interfaces}

### Sources

{sources}

### Constraints

{constraints}

### Units

{units}

### Order

{order}
"""

DESIGN_OUTLINE = (
    "## Proposed solution", "### Scope", "### Out of scope", "### Interfaces",
    "### Sources", "### Constraints", "### Units", "### Order",
    "## Risks and cost",
    "## Consult cases",
    "## Decisions and open questions",
    "## Traceability", "### Links out", "### Record",
    "## Notes",
    "## Appendix", "### Contract",
)
# What a requirements document holds and a design document does not.
ABSENT_HEADINGS = ("## Statement", "## Description", "### Findings at a glance",
                   "## Background", "### Existing behavior touched", "## Findings",
                   "## Why this happened", "## Success criteria", "## Non-goals",
                   "## Prerequisites", "## Acceptance criteria", "### Checks",
                   "### Error messages, verbatim", "### Regression check", "### Gherkin",
                   "### Terms")

ENGINEER = "`[Engineer seat · authored]`"
RECORD_TAG = "`[Intake · derived from r{n}]`"  # stamped, for the step that writes the block
CONTRACT_TAG = "`[Intake · derived]`"
CONTRACT_BODY = "(none: intake writes `specs/{id}/contract.yaml`)"
TAGS = {
    "## Proposed solution": ENGINEER, "## Risks and cost": ENGINEER,
    "## Consult cases": ENGINEER, "## Decisions and open questions": ENGINEER,
    "### Links out": ENGINEER, "### Record": RECORD_TAG, "## Notes": ENGINEER,
    "### Contract": CONTRACT_TAG,
}
# Every `{name}` the template holds: the first lines' six, one per section of
# the Proposed solution, then Risks and cost, the cases and the record's.
PLACEHOLDERS = {
    "date", "engineer", "m", "id", "title", "repo",
    "scope", "out_of_scope", "interfaces", "sources", "constraints", "units", "order",
    "risks_and_cost", "cases", "decisions", "links_out", "n", "record", "notes",
}
RECORD_CLAUSE = ('the Record block gets the tag `[Intake · derived]` and the body'
                 ' "(none: intake writes the record)"')

SOLUTION_STEPS = (
    ("S1", "SCOPE"), ("S2", "OUT OF SCOPE"), ("S3", "INTERFACES"), ("S4", "SOURCES"),
    ("S5", "CONSTRAINTS"), ("S6", "UNITS"), ("S7", "ORDER"), ("S8", "RISKS AND COST"),
    ("S9", "CONSULT CASES"), ("S10", "DECISIONS AND OPEN QUESTIONS"),
    ("S11", "LINKS OUT"), ("S12", "NOTES"),
)

# The four consult cases, each as the Consult cases table names it.
CASES = (
    "1. An ambiguity in the requirements",
    "2. More than one solution",
    "3. A solution unconventional to the codebase",
    "4. A change to a public contract: routes, a gateway definition, events, a schema",
)
CASES_HEADER = "| Case | Answer | Who was asked | What was decided |"
CASES_RULE = "| :-- | :-: | :-- | :-- |"
CASES_STATE = "`answers.cases: [{case, answer, asked, decided}]`"
OPEN_NON_GOAL = "`OPEN: a non-goal for the PO seat: {thing}`"

# Sentences the unit writes, each as the prompt files hold it.
OWN_FILES = "A run writes only its own document and its own state file."
NO_LINE_CHANGED = ("A design run changes no line of the requirements document or of the"
                   " requirements run's state file.")
READ_NEVER_WRITTEN = ("A design run reads, and never writes, the requirements document and"
                      " the requirements run's state file.")
ONE_DERIVED_BLOCK = "A requirements document holds one derived block, `Gherkin`"
OWN_FORM = "The form shows the run's own document, and that one alone"

# Wording the unit retires.
RETIRED_NULL_SEAT = "`seats.engineer` is null"
RETIRED_SKIP = "skips the solution half"
RETIRED_UNCONFIRMED = "(from the PO seat, not confirmed)"
RETIRED_HAND_OVER = "with no engineer seat `phase: output`"
RETIRED_BOTH_SEATS = "both seats answer"
RETIRED_SPAN = "S1-S11"
RETIRED_BLOCKS = "one of `Gherkin`, `Contract`, `Record`"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """The text with each whitespace run collapsed to one space."""
    return " ".join(text.split())


def _prompt_files() -> list[Path]:
    return [SKILL_DIR / "SKILL.md"] + sorted(FLOWS.glob("*.md"))


def _skill() -> str:
    return _flat(_text(SKILL_DIR / "SKILL.md"))


def _flow(name: str) -> str:
    path = FLOWS / name
    assert path.is_file(), f"flows/{name} is not written"
    return _text(path)


def _block(text: str, tag: str) -> str:
    """One PromptLang block of a prompt file, whitespace collapsed."""
    assert f"<{tag}>" in text and f"</{tag}>" in text, f"no <{tag}> block"
    return _flat(text.split(f"<{tag}>", 1)[1].split(f"</{tag}>", 1)[0])


def _instructions(text: str) -> str:
    assert "<instructions>" in text and "</instructions>" in text
    return text.split("<instructions>", 1)[1].split("</instructions>", 1)[0]


def _steps(name: str, letter: str) -> dict[str, str]:
    """Each numbered step of a flow's instructions block, in order: its id
    mapped to its text, whitespace collapsed. A step opens a line as
    `{letter}{n}. `."""
    parts = re.split(rf"^({letter}\d+)\. ", _instructions(_flow(name)), flags=re.M)
    assert len(parts[1::2]) == len(set(parts[1::2])), "a step id opens two steps"
    return {parts[i]: _flat(f"{parts[i]}. {parts[i + 1]}") for i in range(1, len(parts), 2)}


def _step(name: str, letter: str, step: str) -> str:
    steps = _steps(name, letter)
    assert step in steps, f"flows/{name} has no step {step}"
    return steps[step]


def _skill_step(number: int) -> str:
    """One numbered step of SKILL.md's instructions, whitespace collapsed."""
    parts = re.split(r"^(\d)\. ", _instructions(_text(SKILL_DIR / "SKILL.md")), flags=re.M)
    steps = {parts[i]: _flat(parts[i + 1]) for i in range(1, len(parts), 2)}
    assert str(number) in steps, f"SKILL.md has no step {number}"
    return steps[str(number)]


def _sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.?!]) ", _flat(text))


def _naming_intake(text: str) -> list[str]:
    """Each sentence that names the intake command with the requirements
    document's path."""
    return [sentence for sentence in _sentences(text) if INTAKE_COMMAND in sentence]


def _holding(words: str) -> list[str]:
    """The text of each prompt file, SKILL.md or a flow, that holds the
    words, whitespace collapsed."""
    return [_flat(_text(path)) for path in _prompt_files() if words in _flat(_text(path))]


def _design_start() -> str:
    """The prompt file that opens a design run: the one that holds the stop
    for a missing requirements document, whitespace collapsed."""
    held = _holding(NO_DOCUMENT)
    assert held, "no prompt file holds the stop for a missing requirements document"
    assert len(held) == 1, "two prompt files hold the stop for a missing requirements document"
    return held[0]


def _template() -> str:
    assert DESIGN_TEMPLATE.is_file(), "templates/design-document.md.template is not written"
    return _text(DESIGN_TEMPLATE)


def _outline(lines: list[str]) -> list[str]:
    return [line.rstrip() for line in lines
            if line.startswith(("## ", "### ")) or set(line.strip()) == {"-"}]


def _cases_step() -> str:
    steps = _steps("solution.md", "S")
    assert "S9" in steps and steps["S9"].startswith("S9. CONSULT CASES - "), (
        "flows/solution.md has no step S9 for the consult cases")
    return steps["S9"]


# --- SC1.2: the design template ---

def test_sc1_2_skill_folder_holds_markdown_and_exactly_two_templates_and_no_code():
    held = {p.relative_to(SKILL_DIR).as_posix() for p in SKILL_DIR.rglob("*") if p.is_file()}
    templates = {name for name in held if name.startswith("templates/")}
    assert templates == {"templates/requirements-document.md.template",
                         "templates/design-document.md.template"}
    for name in held - templates:
        assert name.endswith(".md"), f"{name} is not Markdown"
        assert name == "SKILL.md" or name.startswith("flows/"), name
    skill = _text(SKILL_DIR / "SKILL.md")
    assert "{skill-dir}/templates/requirements-document.md.template" in skill
    assert "{skill-dir}/templates/design-document.md.template" in skill
    for path in _prompt_files():
        assert "feature-document.md.template" not in _text(path), path.name


def test_sc1_2_design_document_opens_on_an_r1_that_names_the_requirements_revision_and_the_engineer_seat():
    text = _template()
    lines = text.splitlines()
    assert tuple(lines[:len(FIRST_LINES)]) == FIRST_LINES
    rows = lines[2:lines.index("")]
    assert len(rows) == 1, rows  # r1 alone
    cells = [cell.strip() for cell in rows[0].strip("|").split("|")]
    assert cells == ["{date}", "{engineer}", R1_CHANGES]
    assert "against requirements r{m}" in cells[2]
    assert [line for line in lines if line.startswith("# ")] == ["# {id} - {title}"]
    assert "seats:" not in text  # the status line names one seat
    assert "{po}" not in text


def test_sc1_2_proposed_solution_stands_byte_for_byte_as_kit_0_18_0_wrote_it():
    text = _template()
    opening = "\n".join(FIRST_LINES) + "\n\n"
    assert text.startswith(opening + PROPOSED_SOLUTION)  # right under the status line
    assert text.count(PROPOSED_SOLUTION) == 1
    after = text[len(opening + PROPOSED_SOLUTION):]
    assert after.startswith("\n## Risks and cost\n"), after[:60]  # heading and place kept


def test_sc1_2_design_document_holds_the_solution_half_then_the_cases_its_record_and_the_contract_block():
    lines = _template().splitlines()
    assert _outline(lines) == list(DESIGN_OUTLINE)  # and no `---` line
    stripped = [line.strip() for line in lines]
    for heading in ABSENT_HEADINGS:
        assert heading not in stripped, heading
    assert "{bug fix only}" not in stripped  # the sections are the same for a bug fix
    tail = lines[lines.index("## Risks and cost"):]
    assert [line for line in tail if line.strip()] == [
        "## Risks and cost", ENGINEER, "{risks_and_cost}",
        "## Consult cases", ENGINEER, "{cases}",
        "## Decisions and open questions", ENGINEER, "{decisions}",
        "## Traceability",
        "### Links out", ENGINEER, "{links_out}",
        "### Record", RECORD_TAG, "{record}",
        "## Notes", ENGINEER, "{notes}",
        "## Appendix",
        "### Contract", CONTRACT_TAG, CONTRACT_BODY,
    ]
    assert set(re.findall(r"\{([a-z_]+)\}", _template())) == PLACEHOLDERS


def test_sc1_2_every_authored_section_is_tagged_for_the_engineer_seat_and_none_for_the_po_seat():
    text = _template()
    lines = text.splitlines()
    for heading, tag in TAGS.items():
        assert heading in lines, heading
        at = lines.index(heading)
        following = next(line for line in lines[at + 1:] if line.strip())
        assert following == tag, (heading, following)
    tags = [line for line in lines if re.fullmatch(r"`\[[^\]]+\]`", line.strip())]
    assert tags == [ENGINEER] * 5 + [RECORD_TAG, ENGINEER, CONTRACT_TAG]
    for words in ("PO seat", "Both seats"):
        assert words not in text, words


def test_sc1_2_opening_writes_r1_from_the_design_template_and_fills_the_record_block():
    close = _step("opening.md", "O", "O6")
    assert "{skill-dir}/templates/requirements-document.md.template" in close
    assert "{skill-dir}/templates/design-document.md.template" in close
    design = close.split("{skill-dir}/templates/design-document.md.template", 1)[1]
    written = close.split("{skill-dir}/templates/design-document.md.template", 1)[0]
    assert DESIGN_PATH in written and "r1" in written
    assert "`{engineer}`" in design
    # The Record block is a design document's: filled as kit 0.18.0 filled it.
    assert RECORD_CLAUSE in design
    assert RECORD_CLAUSE not in written  # a requirements run fills no Record block
    assert "the template keeps its stamped tag" in design
    assert "`phase: solution`" in design and "`next: S1`" in design


def test_sc1_2_google_docs_form_shows_only_the_document_the_run_wrote():
    form = _step("output.md", "W", "W1")
    assert "Google Docs form" in form
    assert OWN_FORM in form
    own = form.split(OWN_FORM, 1)[1].split(".", 1)[0]
    assert "the requirements document after a requirements run" in own
    assert "the design document after a design run" in own
    assert "Nothing is written" in form  # the form is written nowhere


# --- SC2.2: the dispatch ---

def test_sc2_2_second_argument_design_routes_to_the_design_run():
    skill = _text(SKILL_DIR / "SKILL.md")
    hint = next(line for line in skill.split("---", 2)[1].splitlines()
                if line.startswith("argument-hint:"))
    assert "design" in hint
    assert "<variables>" in skill and "</variables>" in skill
    variables = skill.split("<variables>", 1)[1].split("</variables>", 1)[0]
    rows = [line for line in variables.splitlines() if line.startswith("| `$")]
    assert [row.split("|")[1].strip() for row in rows] == ["`$1`", "`$2`"]
    assert "`design`" in rows[1] and "design run" in rows[1]
    dispatch = _skill_step(0)
    assert "PARSE `$1` as the feature id" in dispatch
    assert "PARSE `$2`" in dispatch
    assert "`design` asks for the design run" in dispatch
    assert "no second argument for the requirements run" in dispatch
    assert "the run is never guessed from the files" in dispatch


def test_sc2_2_design_run_reads_and_writes_its_own_document_and_its_own_state_file():
    skill = _skill()
    for path in (REQUIREMENTS_PATH, REQUIREMENTS_STATE, DESIGN_PATH, DESIGN_STATE):
        assert path in skill, path
    assert "`schema: spec-interview-state/2`" in skill and STATE_KEYS in skill
    assert "with the same schema and keys plus `requirements_revision`" in skill
    for path in _prompt_files():
        assert "spec-interview-state/3" not in _text(path), path.name
    first = _step("opening.md", "O", "O1")
    assert KEPT_MESSAGE in first
    assert "one Bash call `ls docs/features/{id}.design.md`" in first
    assert DESIGN_STATE in first and "`requirements_revision`" in first
    # The draft check reads each done_means beside the requirements' new terms.
    assert "under `answers.terms` a copy of the requirements document's new terms" in first


def test_sc2_2_a_later_design_run_goes_on_at_the_step_its_own_state_file_names():
    dispatch = _skill_step(0)
    assert "one Bash call `ls docs/features/{id}.state.yaml`" in dispatch
    assert "one Bash call `ls docs/features/{id}.design.state.yaml`" in dispatch
    assert "A design run LOADs its own state file" in dispatch
    assert "a hit resumes at the step that file's `next` names" in dispatch
    skill = _skill()
    assert "EXECUTE the flow from the step `next` names" in skill
    assert "`solution` - LOAD {skill-dir}/flows/solution.md" in skill
    assert "writes the state file with `next` unchanged" in _flat(_flow("solution.md"))
    # Each flow of the run leaves `next` at the first step of the flow after it.
    design = _step("opening.md", "O", "O6").split(DESIGN_PATH, 1)[-1]
    assert "`phase: solution`" in design and "`next: S1`" in design
    last = _step("solution.md", "S", "S12")
    assert "`phase: solution`" in last and "`next: E1`" in last


# --- SC2.2: the start, and its stops ---

def test_sc2_2_design_run_reads_the_requirements_document_before_it_writes_anything():
    start = _design_start()
    assert f"READs the requirements document {REQUIREMENTS_PATH} before it writes anything" in start
    assert "stops with nothing written" in start
    assert f'REPORT "{NO_DOCUMENT}"' in start
    assert "No file at the path" in start
    # The read and its stops stand above the run's first write, its state file.
    assert DESIGN_STATE in start
    assert start.index(NO_DOCUMENT) < start.index(DESIGN_STATE)
    assert start.index(UNSIGNED) < start.index(DESIGN_STATE)
    assert READ_NEVER_WRITTEN in start


def test_sc2_2_design_run_stops_on_a_requirements_document_the_po_seat_has_not_signed():
    start = _design_start()
    assert f'REPORT "{UNSIGNED}"' in start
    cause = start.split(f'REPORT "{UNSIGNED}"', 1)[0].rsplit('" ', 1)[-1]
    assert "No `Signed: request half` row" in cause
    assert "the newest text revision r{n}" in cause
    assert ("The newest text revision is the highest `rN` of a row that opens on none of"
            " `Ready:`, `Measured:`, `Signed:` or `Parked:`") in start
    assert start.index(NO_DOCUMENT) < start.index(UNSIGNED)


def test_a_design_run_on_a_combined_document_stops_with_nothing_written():
    start = _design_start()
    assert f'REPORT "{COMBINED}"' in start
    cause = start.split(f'REPORT "{COMBINED}"', 1)[0].rsplit('" ', 1)[-1]
    assert "`## Proposed solution` heading" in cause
    assert start.index(NO_DOCUMENT) < start.index(COMBINED) < start.index(DESIGN_STATE)


# --- SC2.2: one seat ---

def test_sc2_2_design_run_asks_for_an_engineer_seat_and_for_no_po_seat():
    seats = _step("opening.md", "O", "O4")
    assert "A design run ASKs who holds the engineer seat, and asks for no PO seat." in seats
    assert "Record `seats: {engineer}`" in seats
    assert "Record `seats: {po}`" in seats  # a requirements run's answer stands
    opening = _flat(_flow("opening.md"))
    assert "A design run asks O1, O4, O5 and O6" in opening
    assert ("It asks no origin and no title: it reads both from the requirements"
            " document.") in opening
    first = _step("opening.md", "O", "O1")
    assert "`next: O2`" in first and "`next: O4`" in first
    assert first.index("`next: O2`") < first.index(DESIGN_STATE) < first.index("`next: O4`")


def test_sc2_2_design_run_shows_the_engineer_seat_each_place_the_po_seat_refused_at_non_goals():
    places = _step("solution.md", "S", "S2")
    assert places.startswith("S2. OUT OF SCOPE - ")
    assert f"READ the requirements run's state file, {REQUIREMENTS_STATE}" in places
    assert ("SHOW the engineer seat each place the PO seat refused at Non-goals, its"
            " `answers.out_of_scope`") in places
    assert "With no such state file, show no refused places and say so." in places
    assert "Record `answers.out_of_scope` (list)" in places
    kept = _step("request.md", "Q", "Q9")  # where a requirements run keeps them
    assert "`answers.out_of_scope`" in kept


def test_sc2_2_a_thing_the_engineer_seat_will_not_build_is_an_open_mark_in_the_design_document():
    places = _step("solution.md", "S", "S2")
    assert "a thing we will not build, or a place we will not touch?" in places
    assert OPEN_NON_GOAL in places
    assert "under the design document's Decisions and open questions" in places
    assert "write nothing in the requirements document" in places
    # What retires: the write into Non-goals, and the PO seat's signature for it.
    for retired in ("`answers.non_goals`", "under Non-goals", "sign again", "text row"):
        assert retired not in places, retired


# --- SC2.2: the steps a design run asks ---

def test_sc2_2_design_run_asks_only_the_solution_halfs_steps_and_the_four_cases():
    steps = _steps("solution.md", "S")
    assert list(steps) == [step for step, _ in SOLUTION_STEPS]
    for step, name in SOLUTION_STEPS:
        assert steps[step].startswith(f"{step}. {name} - "), (step, steps[step][:40])
    lead = _flat(_instructions(_flow("solution.md")).split("S1. ", 1)[0])
    assert lead.startswith("Each step S1-S12 ends the same way")
    assert steps["S1"].startswith("S1. SCOPE - ASK the engineer seat ")
    assert steps["S8"].startswith("S8. RISKS AND COST - ASK the engineer seat ")
    # The check ids are the requirements document's: a design run's state holds none.
    assert "by their ids in the requirements document's Checks" in steps["S6"]
    assert "`answers.checks`" not in steps["S6"]
    # From S1 to S12 no step hands the run to a step or a phase of the other half.
    for step, body in steps.items():
        assert "ASK the PO seat" not in body, step
        for following in re.findall(r"`next: ([A-Za-z0-9]+)`", body):
            assert re.fullmatch(r"S\d+|E1", following), (step, following)
        for phase in re.findall(r"`phase: ([a-z]+)`", body):
            assert phase == "solution", (step, phase)


def test_design_run_ends_by_naming_the_intake_command_on_the_requirements_documents_path():
    last = _step("output.md", "W", "W2")
    assert f"`{DESIGN_COMMAND}`" in last  # a requirements run's next command stands
    named = _naming_intake(last)
    assert len(named) == 1, named
    assert named[0].startswith("After a design run the next command is " + INTAKE_COMMAND)
    assert DESIGN_COMMAND not in named[0]
    route = _naming_intake(_skill_step(1))
    assert len(route) == 1, route
    assert "A design run" in route[0] and "at `complete` it REPORTs" in route[0]
    assert "the design document path" in route[0] and "its state file path" in route[0]
    report = _naming_intake(_skill_step(3))
    assert len(report) == 1, report
    assert report[0].startswith("After a design run's output the report names " + INTAKE_COMMAND)
    assert "never run `/sdlc intake`" in _skill()  # the write surface stays


def test_r1_of_a_design_document_and_its_state_file_name_the_revision_the_opening_read():
    assert "against requirements r{m}" in _template()
    start = _design_start()
    assert "Else HOLD for O1 that revision" in start
    first = _step("opening.md", "O", "O1")
    assert "`requirements_revision` (the revision the read held)" in first
    close = _step("opening.md", "O", "O6")
    assert "`{m}`, the state file's `requirements_revision`" in close
    assert "so r1 reads `against requirements r{m}`" in close


# --- SC5.1: the four cases ---

def test_sc5_1_design_run_asks_the_four_cases_one_at_a_time_after_risks_and_cost():
    steps = _steps("solution.md", "S")
    order = list(steps)
    cases = _cases_step()
    assert order.index("S8") + 1 == order.index("S9") == order.index("S10") - 1
    assert steps["S8"].startswith("S8. RISKS AND COST - ")
    assert steps["S10"].startswith("S10. DECISIONS AND OPEN QUESTIONS - ")
    assert "ASK the engineer seat the four cases, one case per question, in this order" in cases
    at = [cases.find(f"| {case} |") for case in CASES]
    assert -1 not in at, [case for case, found in zip(CASES, at) if found == -1]
    assert at == sorted(at)
    assert len(re.findall(r"\| \d\. ", cases)) == len(CASES)  # four, no fifth
    assert "so a pause resumes at the first case with no entry" in cases


def test_sc5_1_each_answer_is_written_into_the_design_document_as_yes_or_no():
    cases = _cases_step()
    assert "Record each answer as `yes` or `no`." in cases
    assert f"Record {CASES_STATE}" in cases
    assert "The document shows one row per case" in cases
    assert f"{CASES_HEADER} {CASES_RULE} | {CASES[0]} |" in cases
    for case in CASES:
        assert f"| {case} | {{answer}} | {{asked}} | {{decided}} |" in cases, case
    lines = _template().splitlines()
    at = lines.index("## Consult cases")
    assert [line for line in lines[at + 1:] if line.strip()][:2] == [ENGINEER, "{cases}"]


def test_sc5_1_a_yes_takes_who_was_asked_and_what_was_decided_and_the_document_shows_both():
    cases = _cases_step()
    assert "A `yes` takes two more questions, one at a time" in cases
    assert '"Who was asked?"' in cases and '"What was decided?"' in cases
    assert (cases.index("A `yes` takes two more questions") < cases.index('"Who was asked?"')
            < cases.index('"What was decided?"'))
    assert "a `yes` row shows who was asked and what was decided" in cases


# --- what the unit retires, and the two sentences it corrects ---

def test_no_engineer_seat_branch_and_its_hand_over_are_gone_from_every_prompt_file():
    for path in _prompt_files():
        text = _flat(_text(path))
        for retired in (RETIRED_NULL_SEAT, RETIRED_SKIP, RETIRED_UNCONFIRMED,
                        RETIRED_HAND_OVER):
            assert retired not in text, (path.name, retired)
    for step, body in _steps("solution.md", "S").items():
        assert "`phase: output`" not in body and "`next: W1`" not in body, step


def test_the_engineer_seat_alone_answers_risks_and_cost():
    solution = _flat(_flow("solution.md"))
    assert "both seats" not in solution.lower()
    for path in _prompt_files():
        assert RETIRED_BOTH_SEATS not in _flat(_text(path)).lower(), path.name
    assert "the engineer seat answers each of them alone" in _block(_flow("solution.md"),
                                                                    "purpose")


def test_the_solution_flows_span_reads_s1_to_s12_wherever_it_is_named():
    for path in _prompt_files():
        assert RETIRED_SPAN not in _text(path), path.name
    assert "{skill-dir}/flows/solution.md S1-S12: " in _skill()
    assert "S1-S12" in _flat(_flow("solution.md"))


def test_stale_block_report_names_gherkin_as_a_requirements_documents_one_derived_block():
    for path in _prompt_files():
        assert RETIRED_BLOCKS not in _flat(_text(path)), path.name
    held = _holding(ONE_DERIVED_BLOCK)
    assert held, "no prompt file says which derived block a requirements document holds"
    for text in held:
        assert "`Contract` and `Record` stand in a design document" in text


def test_solution_flow_says_nothing_of_ready_check_8_or_of_a_missing_seat():
    solution = _flat(_flow("solution.md")).lower()
    assert "ready check 8" not in solution
    assert "missing seat" not in solution
    assert "s1. scope - ask the engineer seat" in solution  # the step asks, with no branch


# --- Constraints 1, 2 and 5 of the feature document ---

def test_c5_a_design_run_writes_only_its_own_document_and_its_own_state_file():
    constraints = _block(_text(SKILL_DIR / "SKILL.md"), "constraints")
    assert OWN_FILES in constraints
    assert NO_LINE_CHANGED in constraints
    assert "never write a `Ready:` or `Parked:` row" in constraints
    context = _block(_flow("solution.md"), "context")
    assert ("The requirements document and the requirements run's state file are read and"
            " never written.") in context
    assert DESIGN_PATH in context and DESIGN_STATE in context
    assert _holding(READ_NEVER_WRITTEN), "the design run's start does not say what it reads"


def test_c1_c2_every_prompt_file_keeps_the_promptlang_form_the_ceiling_and_one_segment_commands():
    touched = {
        "SKILL.md": "{skill-dir}/templates/design-document.md.template",
        "flows/opening.md": "{skill-dir}/templates/design-document.md.template",
        "flows/solution.md": "S9. CONSULT CASES - ",
        "flows/output.md": INTAKE_COMMAND,
    }
    for name, marker in touched.items():
        path = SKILL_DIR / name
        assert path.is_file(), f"{name} is not written"
        assert marker in _flat(_text(path)), (name, "the unit's text is missing")
    assert _holding(ONE_DERIVED_BLOCK), "the unit's text is missing from the signing flow"
    for path in _prompt_files():
        text = _text(path)
        name = path.name
        assert len(text) < CHAR_CEILING, (name, len(text))
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
        for line in text.splitlines():
            if "one Bash call" in line:
                commands = re.findall(r"`([^`]+)`", line)
                assert commands, (name, line)
                for command in commands:
                    assert not any(ch in command for ch in CHAIN_CHARS), (name, command)
    calls = re.findall(r"one Bash call `([^`]+)`", " ".join(_text(p) for p in _prompt_files()))
    assert "ls docs/features/{id}.design.md" in calls
    assert "ls docs/features/{id}.design.state.yaml" in calls


# --- the unit's done_means ---

def test_done_means_design_run_needs_signed_requirements_names_their_revision_and_records_each_case():
    start = _design_start()
    assert NO_DOCUMENT in start and UNSIGNED in start
    rows = [line for line in _template().splitlines() if line.startswith("| {date} |")]
    assert len(rows) == 1 and "against requirements r{m}" in rows[0]
    cases = _cases_step()
    assert f"Record {CASES_STATE}" in cases
    for case in CASES:
        assert f"| {case} |" in cases, case
