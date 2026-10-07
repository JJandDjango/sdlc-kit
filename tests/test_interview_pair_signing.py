"""Each seat signs in its own document, and a design follows its requirements
(contract: document-split, unit d3-signing).

The skill is prompt-only, so this suite pins the text of its files, as
tests/test_interview_design.py does. SC2.3: each seat's checks run on that
seat's own document and state file and land there as a `Measured:` row; each
seat's `Signed:` row lands in its own document, right after the row it signs;
a design run changes no line of the requirements document. SC3.1: a design
names one requirements revision; every dispatch of a design run reads the
requirements document's newest text revision, and on a newer one shows the
revisions between and asks the engineer seat to confirm the design against
them; on yes the design document takes one text row that names the newer
revision, and a signed design is asked for its signature again; on no nothing
is written. SC5.2: ready check 15 reports a case with no answer, and a yes
that names no one asked or no decision, as an OPEN under Consult cases, and
the seat's word to sign still stands.

Nothing here pins the report of a stale design before the engineer seat
signs, the tree, or intake.

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

PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
CHAIN_CHARS = ";|&>"
CHAR_CEILING = 12_000  # tests/test_skill_interview.py CHAR_CEILING
FLOW_FILES = ["opening.md", "output.md", "request.md", "signing.md", "solution.md"]

REQUIREMENTS_PATH = "`docs/features/{id}.md`"
DESIGN_PATH = "`docs/features/{id}.design.md`"
REQUIREMENTS_COMMAND = "`/sdlc:product-specification-interview {id}`"
INTAKE_COMMAND = "`/sdlc intake docs/features/{id}.md`"

# The two Bash calls of the signing flow: each seat's draft check reads that
# seat's own state file.
REQUIREMENTS_DRAFT = "python -m taskcontract lang-check --draft docs/features/{id}.state.yaml"
DESIGN_DRAFT = "python -m taskcontract lang-check --draft docs/features/{id}.design.state.yaml"

# The rows the signing flow writes, each as its step holds it.
MEASURED_REQUEST = ("r{n}: Measured: the checks before signing, on the request half:"
                    " {findings}; ready checks 1 to 8: {count} OPEN")
FINISHED_REQUEST = ("r{n}: The request half finished: {sections} sections written,"
                    " {open} OPEN")
SIGNED_REQUEST = "r{n}: Signed: request half. The PO seat signs r{m}"
MEASURED_SOLUTION = ("r{n}: Measured: the checks before signing, on the solution half:"
                     " {findings}; Scope against the release unit's paths: {scope};"
                     " ready checks 11 to 15: {count} OPEN")
FINISHED_SOLUTION = ("r{n}: The solution half finished: {sections} sections written,"
                     " {open} OPEN")
SIGNED_SOLUTION = "r{n}: Signed: solution half. The engineer seat signs r{m}"

# A design run's confirmation against a newer requirements revision.
BEHIND = "The design names requirements r{n}; the requirements stand at r{m}."
CONFIRMED_ROW = "r{n}: Confirmed against requirements r{m}"
QUESTION = "Confirm the design against"
QUESTION_ONE = '"Confirm the design against r4?"'
QUESTION_TWO = '"Confirm the design against r4 and r5?"'
QUESTION_MORE = '"Confirm the design against r4, r5 and r6?"'
NAMED_REVISION = ("The design names one requirements revision: the `requirements r{m}` of the"
                  " design table's newest text row that names one")

# Ready check 15, its three gaps, and the two shapes a gap is marked and
# reported in.
CHECK_15 = ("15. Does each of the four cases have an answer, and does each yes name who was"
            " asked and what was decided?")
GAPS = ("`case {k} has no answer`",
        "`case {k} reads yes and names no one asked`",
        "`case {k} reads yes and names no decision`")
OPEN_15 = "`OPEN: Ready check 15: {gap}.`"
OPEN_MARK = "`OPEN: Ready check {n}: {gap}.`"
OPEN_REPORT = "`Ready check {n}: {gap}. Marked OPEN.`"

# Sentences the unit writes, each as the prompt files hold it.
NO_LINE = "changes no line of the requirements document"
NO_LINE_CHANGED = ("A design run changes no line of the requirements document or of the"
                   " requirements run's state file.")
OWN_DOCUMENT_PO = ("P1 to P7 read and write the requirements document, " + REQUIREMENTS_PATH
                   + ", and the requirements run's state file")
OWN_DOCUMENT_ENGINEER = ("E1 to E7 the design document, " + DESIGN_PATH
                         + ", and the design run's state file")
NO_STAMP = "A design run moves no stamp: a design document holds no Gherkin block."
SIGNED_DOCUMENT = "a write into a document after its seat signed adds a text row"
DECLINES = ("a seat that declines keeps its older signature, and the interview names the"
            " revision it covers")

# Wording the unit retires.
RETIRED_SPAN = "11 to 14"
RETIRED_HALF = "a write into a half after its seat signed"
RETIRED_REQUEST_HALF = "signed request half"
RETIRED_ONE_PATH = "its one path"


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


def _signing_step(step: str) -> str:
    steps = _steps("signing.md", "[PE]")
    assert step in steps, f"flows/signing.md has no step {step}"
    return steps[step]


def _signing_context() -> str:
    return _block(_flow("signing.md"), "context")


def _skill_block(tag: str) -> str:
    return _block(_text(SKILL_DIR / "SKILL.md"), tag)


def _skill_step(number: int) -> str:
    """One numbered step of SKILL.md's instructions, whitespace collapsed."""
    parts = re.split(r"^(\d)\. ", _instructions(_text(SKILL_DIR / "SKILL.md")), flags=re.M)
    steps = {parts[i]: _flat(parts[i + 1]) for i in range(1, len(parts), 2)}
    assert str(number) in steps, f"SKILL.md has no step {number}"
    return steps[str(number)]


def _confirm() -> str:
    """The DESIGN CONFIRM step of the opening flow, whitespace collapsed: the
    paragraph that opens a line as `DESIGN CONFIRM - `, up to step O1."""
    lead = re.split(r"^O1\. ", _instructions(_flow("opening.md")), flags=re.M)[0]
    parts = re.split(r"^DESIGN CONFIRM - ", lead, flags=re.M)
    assert len(parts) == 2, "flows/opening.md has no one DESIGN CONFIRM step above O1"
    return _flat("DESIGN CONFIRM - " + parts[1])


def _finished_design() -> str:
    """What SKILL.md's route says of a design run, whitespace collapsed."""
    route = _skill_step(1)
    assert "A design run takes the same routes" in route
    return route.split("A design run takes the same routes", 1)[1]


def _in_order(text: str, *fragments: str) -> None:
    """Each fragment stands in the text, each after the one before it."""
    at = 0
    for fragment in fragments:
        found = text.find(fragment, at)
        assert found != -1, f"missing, or out of order: {fragment!r}"
        at = found + len(fragment)


# --- SC2.3: each seat's checks run on its own document ---

def test_sc2_3_each_seats_checks_and_rows_stand_in_that_seats_own_document():
    context = _signing_context()
    assert "Each seat's checks and rows stand in that seat's own document." in context
    assert OWN_DOCUMENT_PO in context
    assert OWN_DOCUMENT_ENGINEER in context
    assert context.index(OWN_DOCUMENT_PO) < context.index(OWN_DOCUMENT_ENGINEER)
    criteria = _skill_block("criteria")
    assert "each run landed as a `Measured:` row in that seat's own document" in criteria


def test_sc2_3_draft_check_before_the_engineer_seat_signs_reads_the_design_runs_state_file():
    check = _signing_step("E1")
    assert check.startswith("E1. DRAFT CHECK - ")
    assert f"RUN one Bash call `{DESIGN_DRAFT}` at the repo root" in check
    assert "docs/features/{id}.state.yaml" not in check  # the requirements run's file
    assert "each unit's `done_means`, from `answers.units`" in check
    assert "reports the copied terms' findings again" in check
    # The PO seat's draft check keeps the requirements run's state file.
    first = _signing_step("P1")
    assert f"RUN one Bash call `{REQUIREMENTS_DRAFT}` at the repo root" in first
    assert ".design." not in first


def test_sc2_3_ready_checks_of_each_seat_are_read_on_that_seats_document():
    ready = _signing_step("E3")
    assert ready.startswith("E3. READY CHECKS - ")
    assert "READ the document against ready checks 11 to 15, each a question" in ready
    assert "READ the document against ready checks 1 to 8, each a question" in _signing_step("P3")
    # "The document" of an E step is the design document.
    assert OWN_DOCUMENT_ENGINEER in _signing_context()


def test_sc2_3_each_seats_measured_row_lands_in_that_seats_own_document():
    row = _signing_step("E5")
    assert row.startswith("E5. MEASURED ROW - ")
    assert f"WRITE into the design document the row `{MEASURED_SOLUTION}`" in row
    assert "the count under ready checks 11 to 15" in row
    assert "Each run of the checks writes one row." in row
    assert "requirements document" not in row
    po = _signing_step("P5")
    assert f"`{MEASURED_REQUEST}`" in po
    assert "design document" not in po and ".design." not in po
    for path in _prompt_files():
        assert RETIRED_SPAN not in _flat(_text(path)), path.name


def test_sc2_3_each_seats_signed_row_lands_in_its_own_document_right_after_the_row_it_signs():
    signed = _signing_step("E7")
    assert signed.startswith("E7. SIGNATURE - ")
    assert f"WRITE into the design document the text row `{FINISHED_SOLUTION}`" in signed
    assert ("Then WRITE into the design document, right after the first, with no row between,"
            f" the row `{SIGNED_SOLUTION}`, where r{{m}} is that text row") in signed
    assert signed.index(f"`{FINISHED_SOLUTION}`") < signed.index(f"`{SIGNED_SOLUTION}`")
    assert "Both rows carry `seats.engineer` in Revised By" in signed
    assert "Signed: request half" not in signed and "`seats.po`" not in signed
    # The PO seat's rows stay in the requirements run's document.
    po = _signing_step("P7")
    assert f"`{FINISHED_REQUEST}`" in po
    assert f"right after the first, with no row between, the row `{SIGNED_REQUEST}`" in po
    assert "Signed: solution half" not in po and "design document" not in po
    assert OWN_DOCUMENT_PO in _signing_context()


# --- SC2.3: a design run changes no line of the requirements document ---

def test_sc2_3_a_design_run_changes_no_line_of_the_requirements_document_at_any_signing_step():
    assert NO_LINE_CHANGED in _skill_block("constraints")
    assert ("No E step changes a line of the requirements document or of the requirements"
            " run's state file.") in _signing_context()
    assert "a design run " + NO_LINE in _signing_step("E6")
    assert "E7 " + NO_LINE in _signing_step("E7")
    assert "the step " + NO_LINE in _confirm()


def test_sc2_3_e6_offers_the_way_back_to_a_section_of_the_design_document_only():
    back = _signing_step("E6")
    assert back.startswith("E6. SIGN OR GO BACK - ")
    assert ("To go back, the seat names a section of the design document: EXECUTE that"
            " section's step from {skill-dir}/flows/solution.md, WRITE the state file with"
            " `next: E1`, and go to E1") in back
    # A section of the requirements document is the requirements run's to write.
    assert ("When the seat names a section of the requirements document, REPORT the"
            f" requirements run's command, {REQUIREMENTS_COMMAND}, WRITE nothing") in back
    assert "request half" not in back
    assert "PO seat" not in back
    for step, body in _steps("signing.md", "E").items():
        assert "{skill-dir}/flows/request.md" not in body, step
    assert RETIRED_REQUEST_HALF not in _flat(_flow("signing.md"))


def test_sc2_3_e7_moves_no_gherkin_stamp():
    signed = _signing_step("E7")
    assert "Gherkin" not in signed and "stamp" not in signed
    assert ("where `{sections}` counts the design document's sections written and `{open}`"
            " the OPEN marks that stand in it") in signed
    assert NO_STAMP in _skill_block("constraints")
    # The PO seat's signature keeps its sentence on the stamp.
    assert "the Gherkin block's stamp moves to this row" in _signing_step("P7")


# --- SC3.1: the revision a design names ---

def test_sc3_1_every_dispatch_of_a_design_run_reads_the_requirements_newest_text_revision():
    dispatch = _skill_step(0)
    assert ("A design run that resumes first EXECUTEs the DESIGN CONFIRM of"
            " {skill-dir}/flows/opening.md, at every dispatch and at any phase") in dispatch
    assert "a hit resumes at the step that file's `next` names" in dispatch
    confirm = _confirm()
    assert confirm.startswith("DESIGN CONFIRM - A design run with a state file of its own"
                              " EXECUTEs this step at every dispatch, at any phase, before the"
                              " step `next` names.")
    assert "READ the requirements document's newest text revision." in confirm
    # The step stands under the read that opens a design run, above O1.
    lead = re.split(r"^O1\. ", _instructions(_flow("opening.md")), flags=re.M)[0]
    assert lead.index("DESIGN READ - ") < lead.index("DESIGN CONFIRM - ")


def test_sc3_1_a_design_names_one_requirements_revision_the_one_its_newest_text_row_names():
    confirm = _confirm()
    assert NAMED_REVISION in confirm
    assert "the design's table wins over its state file's `requirements_revision`" in confirm
    assert "When it is no newer, go on at `next`." in confirm
    _in_order(confirm, NAMED_REVISION, "READ the requirements document's newest text revision.",
              "When it is no newer", "On a newer one")


def test_sc3_1_on_a_newer_revision_the_run_names_each_text_revision_between():
    confirm = _confirm()
    assert f'On a newer one SHOW "{BEHIND}"' in confirm  # the message, and no word after it
    assert "the requirements table's text rows above the named revision" in confirm
    _in_order(confirm, f'SHOW "{BEHIND}"', "then the revisions between",
              "each on its own line", "that row's Changes Made text", QUESTION)


def test_sc3_1_the_engineer_seat_is_asked_whether_the_design_still_stands_against_each():
    confirm = _confirm()
    assert "ASK the engineer seat whether the design still stands against each" in confirm
    for question in (QUESTION_ONE, QUESTION_TWO, QUESTION_MORE):
        assert question in confirm, question
    assert f"One revision between reads {QUESTION_ONE}" in confirm
    assert f"three or more {QUESTION_MORE}" in confirm
    # The question is asked in one place.
    held = [path.name for path in _prompt_files() if QUESTION in _flat(_text(path))]
    assert held == ["opening.md"], held


def test_sc3_1_on_yes_the_design_document_takes_one_text_row_that_names_the_newer_revision():
    confirm = _confirm()
    assert f"On yes WRITE into the design document one text row, `{CONFIRMED_ROW}`" in confirm
    yes = confirm.split("On yes ", 1)[1].split("On no,", 1)[0]
    assert "`seats.engineer` in Revised By" in yes
    assert "WRITE the state file with `requirements_revision` moved to r{m}" in yes
    assert "under `answers.terms`, a new copy of the requirements document's new terms" in yes
    assert "Measured:" not in yes and "Bash" not in confirm  # no run of the checks, no command
    forms = [form for path in _prompt_files()
             for form in re.findall(r"`(r\{n\}: Confirmed[^`]*)`", _flat(_text(path)))]
    assert forms == [CONFIRMED_ROW], forms


def test_sc3_1_a_signed_design_is_asked_for_its_signature_again_right_after_the_text_row():
    confirm = _confirm()
    assert "On yes " in confirm and "On no," in confirm
    yes = confirm.split("On yes ", 1)[1].split("On no,", 1)[0]
    assert ("A design that carries a `Signed: solution half` row is then asked for its"
            " signature again, at once, with no run of the checks between") in yes
    assert ("on the seat's word WRITE, right after that text row, with no row between,"
            f" `{SIGNED_SOLUTION}`, where r{{m}} is that text row") in yes
    assert yes.index(f"`{CONFIRMED_ROW}`") < yes.index(f"`{SIGNED_SOLUTION}`")
    assert DECLINES in yes
    assert "Signed: request half" not in confirm


def test_sc3_1_a_design_with_no_signature_takes_the_text_row_alone():
    confirm = _confirm()
    assert "A design with no signature takes the text row alone." in confirm
    _in_order(confirm, f"`{CONFIRMED_ROW}`", "A design that carries a `Signed: solution half` row",
              "A design with no signature takes the text row alone.", "On no,")


def test_sc3_1_on_no_nothing_is_written_and_the_run_asks_again_at_the_next_dispatch():
    confirm = _confirm()
    assert "On no, WRITE nothing" in confirm
    no = confirm.split("On no,", 1)[1]
    assert "the run asks again at the next dispatch" in no
    assert "Either way the run then goes on at the step `next` names" in no
    assert "`r{n}: " not in no  # no row


# --- SC5.2: ready check 15 ---

def test_sc5_2_ready_check_15_asks_whether_each_case_has_an_answer_and_each_yes_names_both():
    ready = _signing_step("E3")
    assert CHECK_15 in ready
    numbers = re.findall(r"(?<= )(\d\d)\. (?=[A-Z])", ready)
    assert numbers == ["11", "12", "13", "14", "15"], numbers
    assert ready.index("14. ") < ready.index(CHECK_15)


def test_sc5_2_each_gap_of_ready_check_15_is_an_open_under_consult_cases_with_its_message():
    ready = _signing_step("E3")
    assert CHECK_15 in ready
    gaps = ready.split(CHECK_15, 1)[1]
    assert f"each marked under Consult cases as {OPEN_15}" in gaps
    _in_order(gaps, *GAPS)
    assert len(re.findall(r"`case \{k\} [^`]+`", ready)) == len(GAPS)  # three, no fourth
    # The kept shapes: how a gap is marked, and how it is reported.
    context = _signing_context()
    assert OPEN_MARK in context
    assert OPEN_REPORT in context


def test_sc5_2_the_seats_word_to_sign_still_stands_whatever_ready_check_15_reports():
    steps = _steps("signing.md", "E")
    order = list(steps)
    assert CHECK_15 in steps["E3"]
    assert "the count under ready checks 11 to 15" in steps["E5"]
    assert order.index("E3") < order.index("E5") < order.index("E6")
    assert "The seat's word to sign stands, whatever the count" in steps["E6"]
    assert "The checks advise and never block" in _signing_context()
    after = steps["E3"].split(CHECK_15, 1)[1]
    assert "block" not in after.replace("never block", "") and "stop" not in after


# --- the design run's own text, corrected for a pair ---

def test_s9_keeps_a_row_with_an_empty_answer_cell_for_a_case_not_yet_answered():
    cases = _steps("solution.md", "S")["S9"]
    assert ("A case not yet answered keeps its row, with an empty Answer cell, so ready check"
            " 15 has a row to read.") in cases
    assert "A `no` row leaves its last two cells empty." in cases


def test_solution_flows_description_names_consult_cases():
    description = next(line for line in _flow("solution.md").split("---", 2)[1].splitlines()
                       if line.startswith("description:"))
    _in_order(description, "the solution half's sections in order", "Consult cases",
              "the record's authored sections")


def test_skill_criteria_speak_for_each_runs_own_state_file_and_document():
    criteria = _skill_block("criteria")
    assert "the run's own state file found at its path" in criteria
    assert RETIRED_ONE_PATH not in criteria
    assert (f"A requirements run's document lands at {REQUIREMENTS_PATH} and a design run's at"
            f" {DESIGN_PATH}, each as r1 in its template's format") in criteria
    assert "The document lands at" not in criteria


def test_a_write_into_a_document_after_its_seat_signed_adds_a_text_row():
    constraints = _skill_block("constraints")
    assert SIGNED_DOCUMENT in constraints
    assert "the interview asks that seat to sign again" in constraints
    assert f"`{SIGNED_REQUEST}`" in constraints and f"`{SIGNED_SOLUTION}`" in constraints
    for name in ("request.md", "solution.md"):
        assert "a write into a document after its seat signed" in _block(_flow(name), "context"), name
    for path in _prompt_files():
        assert RETIRED_HALF not in _flat(_text(path)), path.name


def test_a_finished_design_run_offers_the_way_back_to_a_section_of_the_design_document():
    finished = _finished_design()
    _in_order(finished, "at `complete` it REPORTs the design document path", INTAKE_COMMAND,
              "then OFFERs the way back to a section of the design document",
              "EXECUTE its step from {skill-dir}/flows/solution.md", "writes a text row",
              "WRITE the state file with `phase: solution`, `next: E1`",
              "so the checks run again from E1 and the engineer seat signs again")
    assert "request.md" not in finished and "PO seat" not in finished
    # A requirements run's way back stands as it was.
    route = _skill_step(1)
    assert "`phase: request`, `next: P1`, so the checks run again and the PO seat signs again" in route


# --- Constraints 1, 2, 3 and 7 of the feature document ---

def test_c3_signing_flow_keeps_exactly_two_bash_calls_one_for_each_seats_draft_check():
    signing = _flat(_flow("signing.md"))
    assert re.findall(r"one Bash call `([^`]+)`", signing) == [REQUIREMENTS_DRAFT, DESIGN_DRAFT]
    assert signing.count("Bash") == 2
    steps = _steps("signing.md", "[PE]")
    assert [step for step, body in steps.items() if "Bash" in body] == ["P1", "E1"]
    # The build adds no taskcontract command.
    for path in _prompt_files():
        for command in re.findall(r"python -m taskcontract (\S+)", _text(path)):
            assert command == "lang-check", (path.name, command)


def test_c7_row_words_signed_and_measured_stay_byte_for_byte():
    forms = re.findall(r"`(r\{n\}: [^`]*)`", _flat(_flow("signing.md")))
    assert forms == [MEASURED_REQUEST, FINISHED_REQUEST, SIGNED_REQUEST,
                     MEASURED_SOLUTION, FINISHED_SOLUTION, SIGNED_SOLUTION]
    for form in (MEASURED_REQUEST, MEASURED_SOLUTION):
        assert form.startswith("r{n}: Measured: the checks before signing, on the ")
    assert SIGNED_REQUEST.startswith("r{n}: Signed: request half")
    assert SIGNED_SOLUTION.startswith("r{n}: Signed: solution half")
    # A design run's confirmation signs in the same words.
    assert f"`{SIGNED_SOLUTION}`" in _confirm()
    for path in _prompt_files():
        for form in re.findall(r"`(r\{n\}: [^`]*)`", _flat(_text(path))):
            assert not form.startswith(("r{n}: Ready:", "r{n}: Parked:")), (path.name, form)


def test_c1_c2_c3_every_prompt_file_keeps_the_promptlang_form_the_ceiling_and_one_segment_commands():
    touched = {
        "SKILL.md": "EXECUTEs the DESIGN CONFIRM of {skill-dir}/flows/opening.md",
        "flows/opening.md": f"`{CONFIRMED_ROW}`",
        "flows/signing.md": CHECK_15,
        "flows/solution.md": "A case not yet answered keeps its row",
        "flows/request.md": "a write into a document after its seat signed",
    }
    for name, marker in touched.items():
        path = SKILL_DIR / name
        assert path.is_file(), f"{name} is not written"
        assert marker in _flat(_text(path)), (name, "the unit's text is missing")
    assert sorted(path.name for path in FLOWS.glob("*")) == FLOW_FILES  # no flow file added
    held = {p.relative_to(SKILL_DIR).as_posix() for p in SKILL_DIR.rglob("*") if p.is_file()}
    assert held == ({"SKILL.md", "templates/requirements-document.md.template",
                     "templates/design-document.md.template"}
                    | {f"flows/{name}" for name in FLOW_FILES}), held  # Markdown, no code
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
                commands = re.findall(r"one Bash call `([^`]+)`", line)
                assert commands, (name, line)
                for command in commands:
                    assert not any(ch in command for ch in CHAIN_CHARS), (name, command)


# --- the unit's done_means ---

def test_done_means_design_run_writes_its_checks_each_text_revision_and_its_signature_into_the_design_document():
    assert f"WRITE into the design document the row `{MEASURED_SOLUTION}`" in _signing_step("E5")
    signed = _signing_step("E7")
    assert f"WRITE into the design document the text row `{FINISHED_SOLUTION}`" in signed
    assert f"`{SIGNED_SOLUTION}`" in signed
    assert f"WRITE into the design document one text row, `{CONFIRMED_ROW}`" in _confirm()


def test_done_means_a_consult_case_with_no_answer_is_marked_open():
    ready = _signing_step("E3")
    assert GAPS[0] in ready
    assert f"each marked under Consult cases as {OPEN_15}" in ready
    assert OPEN_REPORT in _signing_context()
