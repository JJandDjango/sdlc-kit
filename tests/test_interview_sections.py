"""The interview asks each half's sections in order and derives the Gherkin
(contract: feature-document, unit f2-sections).

The skill is prompt-only, so this suite pins the text of its files, as
tests/test_interview_format.py does: one flow per half replaces the
sections flow, the request flow asks its sections in the template's order
and the solution flow in kit 0.18.0's order of its headings, with Consult
cases after Risks and cost, one question at a time, and each writes the
state file after every step (SC1.2);
the request half closes on the Gherkin step, which derives one scenario
per check, joined by the check's id, and marks a thin check OPEN (SC3.1,
SC3.2, SC3.3). Text is matched after collapsing each whitespace run to one
space, so a line wrap inside a prompt file never fails a test. No test
runs a model; `python -m prompt_lang` stays the form receipt.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "skills" / "product-specification-interview"
FLOWS = SKILL_DIR / "flows"
TEMPLATE = SKILL_DIR / "templates" / "requirements-document.md.template"

PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
CHAIN_CHARS = ";|&>"
CHAR_CEILING = 12_000  # tests/test_skill_interview.py CHAR_CEILING

# One flow per half; signing.md holds the checks before each seat signs, and
# output.md stands until its own unit.
FLOW_FILES = {"opening.md", "request.md", "solution.md", "signing.md", "output.md"}
HALVES = (("request.md", "Q", "Q1-Q15"), ("solution.md", "S", "S1-S12"))

# One step per section: its id, its name, and its key under `answers` (the
# template's placeholder). The Regression check reads O2's `regression`.
REQUEST_STEPS = (
    ("Q1", "STATEMENT", "statement"),
    ("Q2", "DESCRIPTION", "description"),
    ("Q3", "FINDINGS AT A GLANCE", "findings_at_a_glance"),
    ("Q4", "BACKGROUND", "background"),
    ("Q5", "EXISTING BEHAVIOR TOUCHED", "existing_behavior"),
    ("Q6", "FINDINGS", "findings"),
    ("Q7", "WHY THIS HAPPENED", "why_this_happened"),
    ("Q8", "SUCCESS CRITERIA", "success_criteria"),
    ("Q9", "NON-GOALS", "non_goals"),
    ("Q10", "PREREQUISITES", "prerequisites"),
    ("Q11", "CHECKS", "checks"),
    ("Q12", "ERROR MESSAGES", "error_messages"),
    ("Q13", "REGRESSION CHECK", "regression"),
    ("Q14", "TERMS", "terms"),
    ("Q15", "GHERKIN", "gherkin"),
)
SOLUTION_STEPS = (
    ("S1", "SCOPE", "scope"),
    ("S2", "OUT OF SCOPE", "out_of_scope"),
    ("S3", "INTERFACES", "interfaces"),
    ("S4", "SOURCES", "sources"),
    ("S5", "CONSTRAINTS", "constraints"),
    ("S6", "UNITS", "units"),
    ("S7", "ORDER", "order"),
    ("S8", "RISKS AND COST", "risks_and_cost"),
    ("S9", "CONSULT CASES", "cases"),
    ("S10", "DECISIONS AND OPEN QUESTIONS", "decisions"),
    ("S11", "LINKS OUT", "links_out"),
    ("S12", "NOTES", "notes"),
)
# A bug-fix step, and the step a feature's run goes to in its place.
BUG_FIX_STEPS = {"Q3": "Q4", "Q6": "Q7", "Q7": "Q8", "Q13": "Q14"}
# The request half's template placeholder no step asks: O2's incident
# reference.
NOT_A_STEP = {"incident_ref"}
# The solution half's headings a step asks, in kit 0.18.0's order, with
# Consult cases after Risks and cost. The requirements template holds none
# of them; each step is named for its heading.
SOLUTION_HEADINGS = (
    "### Scope", "### Out of scope", "### Interfaces", "### Sources",
    "### Constraints", "### Units", "### Order",
    "## Risks and cost",
    "## Consult cases",
    "## Decisions and open questions",
    "### Links out",
    "## Notes",
)

SORTING_QUESTION = "a thing we will not build, or a place we will not touch?"
SPLIT_MESSAGE = "Six criteria is two features. Which criteria form the second document?"
CONFLICT_QUESTION = "The material says X; you said Y. Which stands?"
MATERIAL_RULE = ("When O5 recorded material for the section, SHOW it and ASK to confirm"
                 " or change instead of asking afresh")
STATE_WRITE = ("WRITE the state file with the section's answers and `next` set to the"
               " following step")
SECTION_WRITE = "WRITE the section into the document under its heading and tag"

GHERKIN_UNWRITTEN = "(none: the Gherkin step writes one scenario per check)"
THIN_OPEN = "`OPEN: Ready check 3: {id} is thin: {reason}.`"
UNCONFIRMED_OPEN = "`OPEN: Ready check 3: {id} has no confirmed scenario.`"
OPEN_REPORT = "`Ready check 3: {gap}. Marked OPEN.`"
NEWEST_REVISION = ("the highest `rN` of a row that opens on none of `Ready:`, `Measured:`,"
                   " `Signed:` or `Parked:`")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """The text with each whitespace run collapsed to one space."""
    return " ".join(text.split())


def _flow(name: str) -> str:
    path = FLOWS / name
    assert path.is_file(), f"flows/{name} is not written"
    return _text(path)


def _instructions(text: str) -> str:
    assert "<instructions>" in text and "</instructions>" in text
    return text.split("<instructions>", 1)[1].split("</instructions>", 1)[0]


def _steps(text: str, letter: str) -> dict[str, str]:
    """Each numbered step of the instructions block, in order: its id mapped
    to its whole text, whitespace collapsed. A step opens a line as
    `{letter}{n}. NAME - `, its name in capitals."""
    parts = re.split(rf"^({letter}\d+)\. (?=[A-Z][A-Z -]* - )", _instructions(text),
                     flags=re.M)
    assert len(parts[1::2]) == len(set(parts[1::2])), "a step id opens two steps"
    return {parts[i]: _flat(f"{parts[i]}. {parts[i + 1]}") for i in range(1, len(parts), 2)}


def _step(name: str, letter: str, step: str) -> str:
    steps = _steps(_flow(name), letter)
    assert step in steps, f"flows/{name} has no step {step}"
    return steps[step]


def _opening_step(step: str) -> str:
    return _step("opening.md", "O", step)


def _template_keys() -> list[str]:
    """The template's section placeholders in order, from Statement down to
    the last section a step of the request half asks."""
    body = _text(TEMPLATE).split("## Statement", 1)[1]
    above = body.split("\n## Decisions and open questions\n", 1)[0]
    return [key for key in re.findall(r"\{([a-z_]+)\}", above)
            if key not in NOT_A_STEP]


# --- SC1.2: one flow per half, and the dispatch that routes to it ---

def test_sc1_2_skill_holds_one_flow_per_half_and_no_sections_flow():
    assert {p.name for p in FLOWS.glob("*.md")} == FLOW_FILES
    held = {p.relative_to(SKILL_DIR).as_posix() for p in SKILL_DIR.rglob("*") if p.is_file()}
    assert held == ({"SKILL.md", "templates/requirements-document.md.template",
                     "templates/design-document.md.template"}
                    | {f"flows/{name}" for name in FLOW_FILES})  # Markdown and the templates


def test_sc1_2_no_prompt_file_points_at_the_retired_sections_flow():
    for path in [SKILL_DIR / "SKILL.md"] + sorted(FLOWS.glob("*.md")):
        assert "sections.md" not in _text(path), path.name
    signing = _flat(_text(FLOWS / "signing.md"))  # its pointer names both halves
    assert "{skill-dir}/flows/request.md" in signing
    assert "{skill-dir}/flows/solution.md" in signing


def test_sc1_2_dispatch_routes_each_half_to_its_own_flow():
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert "`request` - LOAD {skill-dir}/flows/request.md" in skill
    assert "`solution` - LOAD {skill-dir}/flows/solution.md" in skill
    assert "`sections`" not in skill  # the old phase retires
    for name in FLOW_FILES:
        assert f"{{skill-dir}}/flows/{name}" in skill, name
    assert "Q1-Q15" in skill and "S1-S12" in skill  # each half's steps, in the file list
    for phase in ("opening", "request", "solution", "output", "complete"):
        assert f"`{phase}`" in skill, phase
    assert "none starts a new run" in skill  # no state file -> the first question
    assert "Exactly one file resumes" in skill  # a state file -> the recorded step


def test_sc1_2_opening_hands_over_to_the_first_step_of_the_request_half():
    close = _opening_step("O6")
    assert "`phase: request`" in close and "`next: Q1`" in close
    assert "`phase: sections`" not in _text(FLOWS / "opening.md")
    assert "Q1" in _steps(_flow("request.md"), "Q")


# --- SC1.2: what r1 holds for a section no step has written ---

def test_sc1_2_a_section_no_step_has_written_reads_not_yet_asked():
    close = _opening_step("O6")
    assert 'reads "(not yet asked)"' in close
    assert 'reads "(none)"' not in close  # the words of an asked section, never r1's
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert 'a section with nothing to say reads "(none)"' in skill
    assert '"(not yet asked)"' in skill


def test_sc1_2_a_derived_block_not_yet_written_carries_no_stamp():
    close = _opening_step("O6")
    assert "`[PO seat · derived]`" in close and GHERKIN_UNWRITTEN in close
    assert close.index("`[PO seat · derived]`") < close.index(GHERKIN_UNWRITTEN)


# --- SC1.2: the sections in the ratified order, one step each ---

def test_sc1_2_request_half_asks_its_sections_in_the_template_order_one_step_each():
    steps = _steps(_flow("request.md"), "Q")
    assert list(steps) == [step for step, _, _ in REQUEST_STEPS]
    for step, name, key in REQUEST_STEPS:
        assert steps[step].startswith(f"{step}. {name} - "), (step, steps[step][:40])
        record = "`regression`" if key == "regression" else f"Record `answers.{key}"
        assert record in steps[step], (step, record)
    above = _template_keys()  # then the Appendix's two the PO seat owns
    assert [key for _, _, key in REQUEST_STEPS] == above + ["terms", "gherkin"]


def test_sc1_2_solution_half_asks_its_sections_in_the_template_order_one_step_each():
    steps = _steps(_flow("solution.md"), "S")
    assert list(steps) == [step for step, _, _ in SOLUTION_STEPS]
    for step, name, key in SOLUTION_STEPS:
        assert steps[step].startswith(f"{step}. {name} - "), (step, steps[step][:40])
        assert f"Record `answers.{key}" in steps[step], (step, key)
    assert [name for _, name, _ in SOLUTION_STEPS] == [
        heading.lstrip("# ").upper() for heading in SOLUTION_HEADINGS]


def test_sc1_2_each_half_asks_one_question_at_a_time():
    for name, letter, _ in HALVES:
        text = _flow(name)
        assert "Ask one question; wait for the answer." in _flat(text), name
        steps = _steps(text, letter)
        assert steps, f"flows/{name} has no {letter} steps"
        for step, body in steps.items():
            assert "ASK" in body, (name, step)


# --- SC1.2: the state file after every step, and the step `next` names ---

def test_sc1_2_each_step_writes_its_section_then_the_state_file_with_next_moved():
    for name, _, span in HALVES:
        flat = _flat(_flow(name))
        assert f"Each step {span} ends the same way" in flat, name
        assert SECTION_WRITE in flat, name
        assert STATE_WRITE in flat, name
        assert flat.index(SECTION_WRITE) < flat.index(STATE_WRITE), name


def test_sc1_2_a_section_step_adds_no_revision_row():
    for name, _, _ in HALVES:
        assert "A step adds no revision row" in _flat(_flow(name)), name
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert "the interview adds a row when it writes the document" not in skill


def test_sc1_2_a_pause_keeps_next_and_a_later_run_goes_on_at_that_step():
    for name, _, _ in HALVES:
        flat = _flat(_flow(name))
        assert "A pause" in flat, name
        assert "writes the state file with `next` unchanged" in flat, name
        assert "at the step `next` names" in flat, name
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert "EXECUTE the flow from the step `next` names" in skill


def test_sc1_2_each_half_hands_over_when_its_last_step_closes():
    last = _step("request.md", "Q", "Q15")
    assert "`phase: request`" in last and "`next: P1`" in last
    assert "S1" in _steps(_flow("solution.md"), "S")
    last = _step("solution.md", "S", "S12")
    assert "`phase: solution`" in last and "`next: E1`" in last


def test_sc1_2_bug_fix_sections_are_asked_only_for_a_bug_fix():
    steps = _steps(_flow("request.md"), "Q")
    for step, following in BUG_FIX_STEPS.items():
        assert step in steps, f"flows/request.md has no step {step}"
        assert "Only when `origin` is `bug-fix`" in steps[step], step
        assert f"`next: {following}`" in steps[step], step  # a feature's run moves on
    for step, body in steps.items():
        if step not in BUG_FIX_STEPS:
            assert "`bug-fix`" not in body, step
    for body in _steps(_flow("solution.md"), "S").values():
        assert "`bug-fix`" not in body


# --- SC1.2: the two kept questions ---

def test_sc1_2_sorting_question_is_asked_at_non_goals_and_at_out_of_scope():
    non_goals = _step("request.md", "Q", "Q9")
    out_of_scope = _step("solution.md", "S", "S2")
    for step in (non_goals, out_of_scope):
        assert SORTING_QUESTION in step, step[:40]
        assert "`answers.out_of_scope`" in step, step[:40]
    assert "`answers.non_goals`" in non_goals  # a thing we will not build goes to its list


def test_sc1_2_a_sixth_success_criterion_draws_the_split_message():
    criteria = _step("request.md", "Q", "Q8")
    assert "sixth" in criteria
    assert SPLIT_MESSAGE in criteria
    assert "`answers.split`" in criteria


# --- SC1.2: material from the opening, read back per section ---

def test_sc1_2_material_from_the_opening_is_read_back_at_each_section_step():
    materials = _opening_step("O5")
    assert "`source: material`" in materials
    assert "the section's own step" in materials
    for name, _, _ in HALVES:
        assert MATERIAL_RULE in _flat(_flow(name)), name


def test_sc1_2_an_answer_that_differs_from_the_material_is_asked_never_settled_silently():
    assert CONFLICT_QUESTION in _opening_step("O5")
    for name, _, _ in HALVES:
        flat = _flat(_flow(name))
        assert CONFLICT_QUESTION in flat, name
        assert "never settled silently" in flat, name


# --- SC1.2: the modules seam, the answers' shapes ---

def test_sc1_2_modules_seam_names_the_solution_flow():
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert "the seam is the solution flow, solution.md" in skill
    assert "modules are deferred (ADR 0028)" in _flat(_flow("solution.md"))


def test_sc1_2_answers_keep_the_shapes_the_draft_check_reads():
    statement = _step("request.md", "Q", "Q1")
    assert "Record `answers.statement`" in statement  # one text, not three parts
    assert "{role, capability, outcome}" not in statement
    assert "Record `answers.non_goals` (list" in _step("request.md", "Q", "Q9")
    checks = _step("request.md", "Q", "Q11")
    assert "Record `answers.checks: [{id, text}]`" in checks
    assert "`- SC{n}.{m}: verify ...`" in checks  # a check's line in Checks
    terms = _step("request.md", "Q", "Q14")
    assert "Record `answers.terms: [{name, definition}]`" in terms
    assert "`amends`" in terms
    units = _step("solution.md", "S", "S6")
    assert "Record `answers.units: [{id, checks, done_means}]`" in units


# --- SC3.1: one scenario per check, joined by its id, confirmed by the PO seat ---

def test_sc3_1_gherkin_step_closes_the_request_half_once_the_checks_stand():
    order = list(_steps(_flow("request.md"), "Q"))
    assert order[-1:] == ["Q15"], "the Gherkin step is the request half's last step"
    assert "Q11" in order[:-1]  # the checks are asked first
    gherkin = _step("request.md", "Q", "Q15")
    assert gherkin.startswith("Q15. GHERKIN - ")
    assert "once the checks stand" in gherkin
    assert "one scenario per check" in gherkin
    assert "`answers.checks`" in gherkin


def test_sc3_1_each_scenario_joins_its_check_by_the_checks_id():
    gherkin = _step("request.md", "Q", "Q15")
    assert "by the check's id" in gherkin
    assert "`Scenario: {id} {name}`" in gherkin
    assert "Given, When and Then lines" in gherkin
    assert ("Record `answers.gherkin: [{check, name, given, when, then, status}]`"
            in gherkin)


def test_sc3_1_po_seat_accepts_changes_or_drops_each_scenario_one_at_a_time():
    gherkin = _step("request.md", "Q", "Q15")
    assert "one at a time" in gherkin
    assert "the PO seat" in gherkin
    assert "accept, change or drop" in gherkin
    assert "`accepted`, `changed` or `dropped`" in gherkin
    assert "WRITE the state file after each scenario" in gherkin


def test_sc3_1_gherkin_step_writes_the_block_with_its_stamp():
    gherkin = _step("request.md", "Q", "Q15")
    assert "`[PO seat · derived from r{n}]`" in gherkin
    assert "the newest revision" in gherkin
    assert NEWEST_REVISION in gherkin


# --- SC3.2: a thin check ---

def test_sc3_2_a_scenario_whose_then_needs_a_missing_fact_is_never_shown():
    gherkin = _step("request.md", "Q", "Q15")
    assert "whose Then needs a fact its check lacks is never shown" in gherkin
    assert "the check is a thin check instead" in gherkin
    assert "`its Then needs {fact}`" in gherkin  # the reason its OPEN carries


def test_sc3_2_ready_check_3_reads_a_thin_check_as_an_inline_open():
    gherkin = _step("request.md", "Q", "Q15")
    assert THIN_OPEN in gherkin
    assert "under its line in Checks" in gherkin
    assert "`thin: {reason}`" in gherkin  # on the check's entry in the state file
    assert "`open`" in gherkin
    assert OPEN_REPORT in gherkin


# --- SC3.3: a dropped scenario, and a check with no accepted scenario ---

def test_sc3_3_a_dropped_scenario_makes_its_check_a_thin_check():
    gherkin = _step("request.md", "Q", "Q15")
    assert re.search(r"drops makes its check a thin check[^.]*`scenario dropped`", gherkin)
    assert THIN_OPEN in gherkin  # the mark a thin check carries


def test_sc3_3_a_check_with_no_accepted_scenario_gets_an_open_where_the_request_half_closes():
    gherkin = _step("request.md", "Q", "Q15")
    assert "At the signature of the request half" in gherkin
    assert UNCONFIRMED_OPEN in gherkin
    assert gherkin.index(UNCONFIRMED_OPEN) < gherkin.index("`phase: request`")


# --- Constraints 1, 2 and 5 of the feature document ---

def test_c1_flows_of_both_halves_keep_the_promptlang_form_and_the_ceiling():
    touched = {SKILL_DIR / "SKILL.md": "{skill-dir}/flows/request.md",
               FLOWS / "opening.md": "`phase: request`",
               FLOWS / "signing.md": "{skill-dir}/flows/request.md",
               FLOWS / "request.md": "Q15. GHERKIN",
               FLOWS / "solution.md": "S12. NOTES"}
    for path, marker in touched.items():
        assert path.is_file(), f"{path.name} is not written"
        text = _text(path)
        assert marker in _flat(text), (path.name, "the unit's text is missing")
        assert text.startswith("---\n") and "name:" in text.split("---", 2)[1], path.name
        opened = re.findall(r"<([a-z][a-z0-9-]*)>", text)
        assert set(opened) <= PROMPTLANG_TAGS, (path.name, set(opened) - PROMPTLANG_TAGS)
        for tag in opened:
            assert f"</{tag}>" in text, (path.name, tag)
        assert len(text) < CHAR_CEILING, (path.name, len(text))
    for name, _, _ in HALVES:
        text = _flow(name)
        assert f"name: spec-interview-flow-{name[:-3]}\n" in text.split("---", 2)[1], name
        opened = set(re.findall(r"<([a-z][a-z0-9-]*)>", text))
        assert {"purpose", "instructions"} <= opened, name


def test_c2_a_bash_call_in_either_half_is_named_and_one_segment():
    for name, _, _ in HALVES:
        for line in _flow(name).splitlines():
            if "Bash" in line:
                assert "one Bash call" in line, (name, line)
                for command in re.findall(r"`([^`]+)`", line):
                    assert not any(ch in command for ch in CHAIN_CHARS), (name, command)


def test_c5_each_half_writes_only_the_document_and_its_state_file():
    for name, _, _ in HALVES:
        flat = _flat(_flow(name))
        targets = re.findall(r"\bWRITE\b([^.;:]*)", flat)
        assert any("document" in target for target in targets), name
        assert any("state file" in target for target in targets), name
        for target in targets:
            assert "state file" in target or "document" in target, (name, target)
