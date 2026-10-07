"""The interview runs the checks before each signature, marks each gap OPEN
and writes the `Signed:` row (contract: feature-document, unit f3-signing).

The skill is prompt-only, so this suite pins the text of its files, as
tests/test_interview_sections.py does. One flow, `flows/signing.md`, holds
the checks before each seat signs its half and the signature: steps P1 to
P7 for the PO seat and the request half, E1 to E7 for the engineer seat
and the solution half. It replaces the readiness flow.

SC1.3: a signature is a row that opens `rN: Signed: request half` or `rN:
Signed: solution half`, written right after the text row it signs; how the
tree reads those rows is held by tests/test_tree_halves.py. SC2.1: the draft check runs as one command
before each signature and lands as a `Measured:` row; nothing is written
under `specs/`. SC2.2: each ready check is a question (1 to 8 before the PO
seat signs, 11 to 14 before the engineer seat signs), a gap is marked OPEN,
a stale block gets its message, and the checks never block. SC2.3: each
entry of Existing behavior touched is read against the file or step it
names.

Text is matched after collapsing each whitespace run to one space, so a
line wrap inside a prompt file never fails a test. No test runs a model,
and `python -m prompt_lang` stays the form receipt.
"""

from __future__ import annotations

import re
from pathlib import Path

# The kit's root. In tests/ it is the folder above this file; a copy that
# stands outside the kit reads the folder pytest runs from.
_ABOVE = Path(__file__).resolve().parent.parent
ROOT = _ABOVE if (_ABOVE / "skills").is_dir() else Path.cwd()
SKILL_DIR = ROOT / "skills" / "product-specification-interview"
FLOWS = SKILL_DIR / "flows"
TEMPLATE = SKILL_DIR / "templates" / "requirements-document.md.template"

PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context",
                   "constraints", "examples", "output", "criteria",
                   "routing", "directives"}
CHAIN_CHARS = ";|&>"
CHAR_CEILING = 12_000  # tests/test_skill_interview.py CHAR_CEILING

# The signing flow replaces the readiness flow.
FLOW_FILES = {"opening.md", "request.md", "solution.md", "signing.md", "output.md"}
PO_STEPS = (("P1", "DRAFT CHECK"), ("P2", "EXISTING BEHAVIOR"), ("P3", "READY CHECKS"),
            ("P4", "STALE BLOCKS"), ("P5", "MEASURED ROW"), ("P6", "SIGN OR GO BACK"),
            ("P7", "SIGNATURE"))
ENGINEER_STEPS = (("E1", "DRAFT CHECK"), ("E2", "SCOPE"), ("E3", "READY CHECKS"),
                  ("E4", "STALE BLOCKS"), ("E5", "MEASURED ROW"), ("E6", "SIGN OR GO BACK"),
                  ("E7", "SIGNATURE"))

DRAFT_COMMAND = "python -m taskcontract lang-check --draft docs/features/{id}.state.yaml"
FINDINGS_EXAMPLE = "4 findings (CL003 1, CL008 1, CL012 1, CL014 1)"

# The six revision rows the flow writes, as it draws them.
MEASURED_REQUEST = ("r{n}: Measured: the checks before signing, on the request half:"
                    " {findings}; ready checks 1 to 8: {count} OPEN")
FINISHED_REQUEST = "r{n}: The request half finished: {sections} sections written, {open} OPEN"
SIGNED_REQUEST = "r{n}: Signed: request half. The PO seat signs r{m}"
MEASURED_SOLUTION = ("r{n}: Measured: the checks before signing, on the solution half:"
                     " {findings}; Scope against the release unit's paths: {scope};"
                     " ready checks 11 to 14: {count} OPEN")
FINISHED_SOLUTION = "r{n}: The solution half finished: {sections} sections written, {open} OPEN"
SIGNED_SOLUTION = "r{n}: Signed: solution half. The engineer seat signs r{m}"
ROW_FORMS = {MEASURED_REQUEST, FINISHED_REQUEST, SIGNED_REQUEST,
             MEASURED_SOLUTION, FINISHED_SOLUTION, SIGNED_SOLUTION}
SIGNED_AGAIN_TEXT_ROW = "r{n}: {what changed}"
NO_RELEASE_UNIT = "no release unit, check skipped"

OPEN_MARK = "`OPEN: Ready check {n}: {gap}.`"
OPEN_REPORT = "`Ready check {n}: {gap}. Marked OPEN.`"
STALE_MESSAGE = "`{block} is stamped r{n}; the newest revision is r{m}. Stale.`"
NEWEST_REVISION = ("the highest `rN` of a row that opens on none of `Ready:`, `Measured:`,"
                   " `Signed:` or `Parked:`")
FALSE_ENTRY_OPEN = ("`OPEN: Ready check 6: {entry} no longer holds:"
                    " {what the source says}.`")
UNCONFIRMED_OPEN = "`OPEN: Ready check 3: {id} has no confirmed scenario.`"
UNCONFIRMED_PLACE = "`(from the PO seat, not confirmed)`"
SIGN_REQUEST_QUESTION = '"Sign the request half now, or go back to a section?"'
SIGN_SOLUTION_QUESTION = '"Sign the solution half now, or go back to a section?"'
NEVER_BLOCKS = ("The checks advise and never block: the seat's word to sign, or to write,"
                " stands whatever the count of findings and OPEN marks")
STAMP_MOVES = ("Each text row the interview writes moves the Gherkin block's stamp to that"
               " row, once every check changed since the last stamp has a confirmed"
               " scenario again.")
HAND_ROW = ("A row written by hand moves no stamp, so the checks before signing report the"
            " block stale.")

# Each ready check the interview asks, with the words its question holds.
# Ready checks 9 and 10 are intake's.
READY_CHECKS = {
    1: ("statement", "state of the world"),
    2: ("three to five success criteria", "a test can decide"),
    3: ("two or three checks", "an id", "thin"),
    4: ("standing line", "specific to this feature"),
    5: ("prerequisite", "exists or missing", "ticket or owner"),
    6: ("Existing behavior touched", '"none"', "file or step it was measured from",
        "regression check"),
    7: ("error message", "verbatim"),
    8: ("Is the PO seat named", "bug fix", "`Measured:` row"),
    11: ("Sources row", "winner"),
    12: ("output kind", "drawn example", "edges"),
    13: ("retirements", '"none"', "by check id and kind"),
    14: ("read green", "answered in the document"),
}
REQUEST_CHECKS = list(range(1, 9))
SOLUTION_CHECKS = list(range(11, 15))


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
    """One tagged block of a prompt file, whitespace collapsed."""
    assert f"<{tag}>" in text and f"</{tag}>" in text, f"no <{tag}> block"
    return _flat(text.split(f"<{tag}>", 1)[1].split(f"</{tag}>", 1)[0])


def _raw_steps(text: str, letter: str) -> dict[str, str]:
    """Each numbered step of the instructions block, in order: its id mapped
    to its text as written. A step opens a line as `{letter}{n}. NAME - `,
    its name in capitals."""
    assert "<instructions>" in text and "</instructions>" in text
    body = text.split("<instructions>", 1)[1].split("</instructions>", 1)[0]
    parts = re.split(rf"^({letter}\d+)\. (?=[A-Z][A-Z -]* - )", body, flags=re.M)
    assert len(parts[1::2]) == len(set(parts[1::2])), "a step id opens two steps"
    return {parts[i]: f"{parts[i]}. {parts[i + 1]}" for i in range(1, len(parts), 2)}


def _steps(text: str, letter: str) -> dict[str, str]:
    """As `_raw_steps`, each step's whitespace collapsed."""
    return {step: _flat(body) for step, body in _raw_steps(text, letter).items()}


def _step(name: str, letter: str, step: str) -> str:
    steps = _steps(_flow(name), letter)
    assert step in steps, f"flows/{name} has no step {step}"
    return steps[step]


def _signing() -> str:
    """The signing flow, whitespace collapsed."""
    return _flat(_flow("signing.md"))


def _signing_step(step: str) -> str:
    return _step("signing.md", "[PE]", step)


def _ready_checks(step: str) -> dict[int, str]:
    """The ready checks one step asks: each stands on its own line inside the
    step, as its number, a full stop, then its question."""
    steps = _raw_steps(_flow("signing.md"), "[PE]")
    assert step in steps, f"flows/signing.md has no step {step}"
    found = re.findall(r"^ +(\d+)\. (.+)$", steps[step], flags=re.M)
    assert len(found) == len({n for n, _ in found}), "a ready check stands twice"
    return {int(n): line.strip() for n, line in found}


def _row_forms() -> list[str]:
    """Each revision-row form the signing flow holds: a code span that opens
    on `r{n}: `."""
    return re.findall(r"`(r\{n\}: [^`]+)`", _signing())


# --- SC1.3: the flow, its steps, and the dispatch that routes to it ---

def test_sc1_3_signing_flow_holds_the_steps_of_each_half_in_order():
    text = _flow("signing.md")
    assert "name: spec-interview-flow-signing\n" in text.split("---", 2)[1]
    steps = _steps(text, "[PE]")
    assert list(steps) == [step for step, _ in PO_STEPS + ENGINEER_STEPS]
    for step, name in PO_STEPS + ENGINEER_STEPS:
        assert steps[step].startswith(f"{step}. {name} - "), (step, steps[step][:40])
    purpose = _block(text, "purpose")
    assert "P1 to P7" in purpose and "E1 to E7" in purpose
    assert "the PO seat" in purpose and "the engineer seat" in purpose


def test_sc1_3_dispatch_sends_a_signing_step_to_the_signing_flow():
    skill = _flat(_text(SKILL_DIR / "SKILL.md"))
    assert ("`request` - LOAD {skill-dir}/flows/request.md, or {skill-dir}/flows/signing.md"
            " when `next` names a P step") in skill
    assert ("`solution` - LOAD {skill-dir}/flows/solution.md, or"
            " {skill-dir}/flows/signing.md when `next` names an E step") in skill
    assert "P1-P7, E1-E7" in skill  # the flow's steps, in the file list
    for name in FLOW_FILES:
        assert f"{{skill-dir}}/flows/{name}" in skill, name
    for phase in ("opening", "request", "solution", "output", "complete"):
        assert f"`{phase}`" in skill, phase  # no new phase: a half's checks run in its phase


def test_sc1_3_each_half_hands_over_to_its_checks_and_each_signature_hands_on():
    gherkin = _step("request.md", "Q", "Q15")
    assert "`phase: request`" in gherkin and "`next: P1`" in gherkin
    assert "`next: S1`" not in gherkin  # the PO seat signs before the solution half opens
    notes = _step("solution.md", "S", "S11")
    assert "`phase: solution`" in notes and "`next: E1`" in notes
    signed = _signing_step("P7")
    assert "`phase: output`" in signed and "`next: W1`" in signed
    signed = _signing_step("E7")
    assert "`phase: output`" in signed and "`next: W1`" in signed
    assert re.search(r"^W1\. ", _flow("output.md"), flags=re.M)  # the output flow's first step


# --- SC1.3: the `Signed:` row ---

def test_sc1_3_a_signature_is_a_row_that_opens_signed_and_names_its_half():
    request, solution = _signing_step("P7"), _signing_step("E7")
    assert f"`{SIGNED_REQUEST}`" in request
    assert f"`{SIGNED_SOLUTION}`" in solution
    assert "Signed: solution half" not in request  # each seat signs its own half
    assert "Signed: request half" not in solution
    for step, _ in PO_STEPS[:-1] + ENGINEER_STEPS[:-1]:
        assert "`r{n}: Signed:" not in _signing_step(step), step  # only the signature step signs


def test_sc1_3_the_signed_row_stands_right_after_the_text_row_it_signs():
    for step, finished, signed in (("P7", FINISHED_REQUEST, SIGNED_REQUEST),
                                   ("E7", FINISHED_SOLUTION, SIGNED_SOLUTION)):
        body = _signing_step(step)
        assert f"`{finished}`" in body, step  # the text row the signature covers
        assert body.index(f"`{finished}`") < body.index(f"`{signed}`"), step
        assert "right after the first" in body and "no row between" in body, step
        assert "where r{m} is that text row" in body, step
        assert "Measured:" not in body, step  # the `Measured:` row is an earlier step's


def test_sc1_3_revised_by_names_the_seat_that_signs_the_half():
    request, solution = _signing_step("P7"), _signing_step("E7")
    assert "Revised By" in request and "`seats.po`" in request
    assert "`seats.engineer`" not in request
    assert "Revised By" in solution and "`seats.engineer`" in solution
    assert "`seats.po`" not in solution
    # Every row of a half, its `Measured:` row too, carries that half's seat.
    assert ("`seats.po` for the request half, `seats.engineer` for the solution half"
            in _signing())


def test_sc1_3_the_flow_writes_six_row_forms_and_never_a_ready_or_parked_row():
    assert set(_row_forms()) == ROW_FORMS
    assert "never writes a `Ready:` or `Parked:` row" in _signing()
    for path in _prompt_files():
        for form in re.findall(r"`(r\{n\}: [^`]*)`", _flat(_text(path))):
            assert not form.startswith(("r{n}: Ready:", "r{n}: Parked:")), (path.name, form)


# --- SC1.3: a write into a signed half, and a seat that declines ---

def test_sc1_3_a_write_into_a_signed_half_adds_a_text_row_and_the_seat_is_asked_to_sign_again():
    constraints = _block(_text(SKILL_DIR / "SKILL.md"), "constraints")
    assert "a write into a half after its seat signed adds a text row" in constraints
    assert f"`{SIGNED_AGAIN_TEXT_ROW}`" in constraints
    assert "the interview asks that seat to sign again" in constraints
    assert "a new `Signed:` row right after it" in constraints
    assert f"`{SIGNED_REQUEST}`" in constraints and f"`{SIGNED_SOLUTION}`" in constraints
    # The rule that a step adds no row keeps its one exception, in each half's flow.
    for name in ("request.md", "solution.md"):
        context = _block(_flow(name), "context")
        assert "A step adds no revision row" in context, name
        assert "a write into a half after its seat signed" in context, name
        assert "adds a text row" in context and "sign again" in context, name
    # The case that raised it: Out of scope sends a thing we will not build to Non-goals.
    out_of_scope = _step("solution.md", "S", "S2")
    assert "adds a text row" in out_of_scope
    assert "asks the PO seat to sign again" in out_of_scope


def test_sc1_3_a_seat_that_declines_keeps_its_older_signature_and_gets_no_new_signed_row():
    constraints = _block(_text(SKILL_DIR / "SKILL.md"), "constraints")
    assert "a seat that declines keeps its older signature" in constraints
    assert "the interview names the revision it covers" in constraints
    for step in ("P6", "E6"):
        body = _signing_step(step)
        assert "A seat that declines to sign gets no `Signed:` row" in body, step
        assert f"`next: {step}`" in body, step  # the run stays at the question
        assert "REPORT the step to resume at" in body, step


def test_sc1_3_solution_flows_purpose_agrees_with_the_step_both_seats_answer():
    purpose = _block(_flow("solution.md"), "purpose")
    assert "The engineer seat answers S1 to S7, and both seats answer S8" in purpose
    assert "answers S1 to S8" not in purpose
    assert "Both seats answer" in _step("solution.md", "S", "S8")


# --- SC1.3: Constraints 1 and 3 of the feature document ---

def test_sc1_3_skill_folder_holds_the_signing_flow_markdown_and_the_template_and_no_code():
    assert {p.name for p in FLOWS.glob("*.md")} == FLOW_FILES
    held = {p.relative_to(SKILL_DIR).as_posix() for p in SKILL_DIR.rglob("*") if p.is_file()}
    assert held == ({"SKILL.md", "templates/requirements-document.md.template"}
                    | {f"flows/{name}" for name in FLOW_FILES})
    for path in SKILL_DIR.rglob("*"):
        if path.is_file():
            assert path.suffix == ".md" or path == TEMPLATE, path


def test_sc1_3_touched_prompt_files_keep_the_promptlang_tags_and_the_ceiling():
    touched = {SKILL_DIR / "SKILL.md": "{skill-dir}/flows/signing.md",
               FLOWS / "request.md": "`next: P1`",
               FLOWS / "solution.md": "`next: E1`",
               FLOWS / "signing.md": "P7. SIGNATURE"}
    for path, marker in touched.items():
        assert path.is_file(), f"{path.name} is not written"
        text = _text(path)
        assert marker in _flat(text), (path.name, "the unit's text is missing")
        assert text.startswith("---\n") and "name:" in text.split("---", 2)[1], path.name
        description = next(line for line in text.split("---", 2)[1].splitlines()
                           if line.startswith("description:"))
        value = description[len("description:"):].strip()
        assert value and not value.startswith(('"', "'", ">", "|")), path.name
        assert ": " not in value and " #" not in value, path.name
        opened = re.findall(r"<([a-z][a-z0-9-]*)>", text)
        assert {"purpose", "instructions"} <= set(opened), path.name
        assert set(opened) <= PROMPTLANG_TAGS, (path.name, set(opened) - PROMPTLANG_TAGS)
        for tag in opened:
            assert f"</{tag}>" in text, (path.name, tag)
    for path in _prompt_files():
        assert len(_text(path)) < CHAR_CEILING, (path.name, len(_text(path)))


# --- SC2.1: the draft check, run as one command before each signature ---

def test_sc2_1_the_draft_check_runs_as_one_shell_segment_before_the_po_seat_signs():
    check = _signing_step("P1")
    assert f"one Bash call `{DRAFT_COMMAND}`" in check
    assert "SHOW its lines" in check
    assert "reads the state file, never the document, and writes nothing" in check
    # What the run covers for the request half.
    assert "the new terms of `answers.terms` as drafts" in check
    assert "vocabulary check" in check and "CL003" in check
    assert "a draft contract of the statement, the non-goals and the checks" in check
    assert "language check" in check
    order = list(_steps(_flow("signing.md"), "[PE]"))
    assert order.index("P1") < order.index("P6") < order.index("P7")


def test_sc2_1_the_same_command_runs_before_the_engineer_seat_signs_and_reads_each_done_means():
    check = _signing_step("E1")
    assert f"one Bash call `{DRAFT_COMMAND}`" in check
    assert "SHOW its lines" in check
    assert "each unit's `done_means`" in check and "`answers.units`" in check
    order = list(_steps(_flow("signing.md"), "[PE]"))
    assert order.index("E1") < order.index("E6") < order.index("E7")


def test_sc2_1_every_shell_command_the_signing_flow_authors_is_one_segment():
    lines = [line for line in _flow("signing.md").splitlines() if "Bash" in line]
    assert len(lines) == 2, lines  # the draft check, once per half
    for line in lines:
        assert "one Bash call" in line, line
        commands = re.findall(r"`([^`]+)`", line)
        assert DRAFT_COMMAND in commands, line
        for command in commands:
            assert not any(ch in command for ch in CHAIN_CHARS), command
    # The flows name the command in one form only.
    for path in _prompt_files():
        for span in re.findall(r"`([^`]+)`", _flat(_text(path))):
            if "lang-check" in span:
                assert span == DRAFT_COMMAND, (path.name, span)


def test_sc2_1_a_finding_that_is_an_error_never_stops_the_run():
    check = _signing_step("P1")
    assert "It exits 1 when a finding is an error" in check
    assert "never a failed step" in check
    assert "the interview reads the lines either way" in check
    assert "as at P1" in _signing_step("E1")


def test_sc2_1_scope_is_checked_against_the_paths_of_the_release_unit():
    scope = _signing_step("E2")
    assert "Scope against the paths of the release unit's row under Units" in scope
    assert "`answers.scope`" in scope
    assert ("A document with no release unit skips this check and says so in its"
            " `Measured:` row") in scope
    assert f"`{NO_RELEASE_UNIT}`" in _signing_step("E5")  # the words that row holds
    assert "release unit" not in "".join(_signing_step(step) for step, _ in PO_STEPS)


def test_sc2_1_each_run_is_recorded_as_a_measured_row_that_copies_the_findings():
    for check, row, form in (("P1", "P5", MEASURED_REQUEST), ("E1", "E5", MEASURED_SOLUTION)):
        assert "the findings part of the command's last line" in _signing_step(check), check
        body = _signing_step(row)
        assert f"`{form}`" in body, row
        assert "Each run of the checks writes one row" in body, row
    measured = _signing_step("P5")
    assert "`{findings}` copies the findings part of the command's last line" in measured
    assert f"`{FINDINGS_EXAMPLE}`" in measured
    assert "`{count}` is the number of OPEN marks that stand" in measured
    # One row per run, written once the command has run and the ready checks are read.
    order = list(_steps(_flow("signing.md"), "[PE]"))
    assert order.index("P3") < order.index("P5") and order.index("E3") < order.index("E5")


def test_sc2_1_the_signing_flow_writes_the_document_and_its_state_file_and_nothing_under_specs():
    flat = _signing()
    assert "nothing under `specs/`" in flat
    targets = re.findall(r"\bWRITE\b([^.;:]*)", flat)
    assert any("document" in target for target in targets)
    assert any("state file" in target for target in targets)
    for target in targets:
        assert "state file" in target or "document" in target, target
    for span in re.findall(r"`([^`]+)`", flat):
        assert not span.startswith("specs/") or span == "specs/", span


def test_sc2_1_the_checks_before_the_po_seat_signs_read_the_terms_the_request_flow_records():
    assert "the checks before signing read the terms" in _block(_flow("request.md"), "purpose")
    assert "Record `answers.terms" in _step("request.md", "Q", "Q14")
    assert "`next: P1`" in _step("request.md", "Q", "Q15")  # the checks follow the Gherkin step
    assert "`answers.terms`" in _signing_step("P1")


# --- SC2.2: the ready checks, each a question; a gap is marked OPEN ---

def _assert_ready_checks(step: str, numbers: list[int], span: str) -> None:
    checks = _ready_checks(step)
    assert list(checks) == numbers, (step, list(checks))
    for number, line in checks.items():
        assert "?" in line, (number, line)
        question = line.split("?", 1)[0]
        for words in READY_CHECKS[number]:
            assert words in question, (number, words)
    body = _signing_step(step)
    assert f"READ the document against ready checks {span}, each a question" in body, step
    assert "mark each gap" in body, step


def test_sc2_2_ready_checks_1_to_8_stand_as_questions_before_the_po_seat_signs():
    _assert_ready_checks("P3", REQUEST_CHECKS, "1 to 8")
    order = list(_steps(_flow("signing.md"), "[PE]"))
    assert order.index("P3") < order.index("P6")


def test_sc2_2_ready_checks_11_to_14_stand_as_questions_before_the_engineer_seat_signs():
    _assert_ready_checks("E3", SOLUTION_CHECKS, "11 to 14")
    order = list(_steps(_flow("signing.md"), "[PE]"))
    assert order.index("E3") < order.index("E6")


def test_sc2_2_ready_checks_9_and_10_are_intakes_and_appear_in_no_flow():
    asked = [number for step in _raw_steps(_flow("signing.md"), "[PE]")
             for number in _ready_checks(step)]
    assert asked == REQUEST_CHECKS + SOLUTION_CHECKS
    for path in _prompt_files():
        for first, last in re.findall(r"[Rr]eady checks? (\d+)(?: (?:to|and) (\d+))?",
                                      _flat(_text(path))):
            named = (int(first), int(last)) if last else int(first)
            assert named in [(1, 8), (11, 14)] + REQUEST_CHECKS + SOLUTION_CHECKS, (
                path.name, named)


def test_sc2_2_each_gap_is_written_inline_added_to_open_and_reported():
    context = _block(_flow("signing.md"), "context")
    assert "asked, never parsed" in context
    assert "inline in its section" in context
    assert OPEN_MARK in context and OPEN_REPORT in context
    assert "the state file's `open`" in context
    assert context.index(OPEN_MARK) < context.index("the state file's `open`") < context.index(
        OPEN_REPORT)
    # A gap already marked is counted once: the mark a thin check carries from Q15.
    assert "never marked twice" in context


def test_sc2_2_a_check_with_no_confirmed_scenario_carries_its_open_into_the_request_halfs_checks():
    gherkin = _step("request.md", "Q", "Q15")
    assert UNCONFIRMED_OPEN in gherkin and "`next: P1`" in gherkin
    assert gherkin.index(UNCONFIRMED_OPEN) < gherkin.index("`next: P1`")
    third = _ready_checks("P3")[3]
    assert "a check with no confirmed scenario" in third and "Q15" in third


# --- SC2.2: the stale message ---

def test_sc2_2_a_block_stamped_below_the_newest_revision_gets_the_stale_message():
    context = _block(_flow("signing.md"), "context")
    assert STALE_MESSAGE in context
    assert "`derived from r{n}`" in context
    assert "below the newest revision" in context
    assert "The newest revision is " + NEWEST_REVISION in context
    for block in ("`Gherkin`", "`Contract`", "`Record`"):
        assert block in context, block
    assert ("Before intake the Contract and the Record carry no stamp and are never stale"
            in context)
    for step in ("P4", "E4"):  # reported in each half's checks, before its row
        body = _signing_step(step)
        assert "REPORT each stale block with its message" in body, step
        assert "the newest revision" in body, step


def test_sc2_2_each_text_row_the_interview_writes_moves_the_gherkin_stamp():
    constraints = _block(_text(SKILL_DIR / "SKILL.md"), "constraints")
    assert STAMP_MOVES in constraints
    assert HAND_ROW in constraints
    for step in ("P7", "E7"):
        assert "the Gherkin block's stamp moves to this row" in _signing_step(step), step


# --- SC2.2: the checks advise ---

def test_sc2_2_the_checks_advise_and_the_seats_word_to_sign_stands_at_any_count():
    assert NEVER_BLOCKS in _block(_flow("signing.md"), "context")
    for step, seat, question in (("P6", "the PO seat", SIGN_REQUEST_QUESTION),
                                 ("E6", "the engineer seat", SIGN_SOLUTION_QUESTION)):
        body = _signing_step(step)
        assert f"ASK {seat} {question}" in body, step
        assert "The seat's word to sign stands, whatever the count" in body, step
    constraints = _block(_text(SKILL_DIR / "SKILL.md"), "constraints")
    assert "The checks before signing advise and never block" in constraints
    assert "the seat's word to sign, or to write, stands whatever the count" in constraints


def test_sc2_2_going_back_to_a_section_runs_the_checks_again_from_their_first_step():
    for step, first, flow in (("P6", "P1", "request.md"), ("E6", "E1", "solution.md")):
        body = _signing_step(step)
        assert f"EXECUTE that section's step from {{skill-dir}}/flows/{flow}" in body, step
        assert f"WRITE the state file with `next: {first}`" in body, step
        assert f"go to {first}, so the command and the ready checks run again" in body, step
    # No step only says to return to a step: `next` is written, so a pause keeps the place.
    for step, body in _steps(_flow("signing.md"), "[PE]").items():
        assert not re.search(r"\breturn to [A-Z]\d", body), step
    context = _block(_flow("signing.md"), "context")
    assert "until the `Measured:` row is written" in context
    assert "a pause inside a run resumes at that first step" in context
    assert "writes the state file with `next` unchanged" in context


# --- SC2.2: what retires, and the seat that is not named ---

def test_sc2_2_readiness_flow_retires_with_every_line_that_names_it():
    assert not (FLOWS / "readiness.md").exists()
    assert (FLOWS / "signing.md").is_file()
    for path in _prompt_files():
        assert "readiness" not in _text(path).lower(), path.name
        assert "R1" not in re.findall(r"\b[A-Z]\d+\b", _text(path)), path.name
    skill = _text(SKILL_DIR / "SKILL.md")
    description = next(line for line in skill.split("---", 2)[1].splitlines()
                       if line.startswith("description:"))
    assert "advisory checks before each seat signs its half" in description
    assert "the checks before each seat signs its half" in _block(skill, "purpose")


def test_sc2_2_probe_mark_is_probed_true_so_thin_marks_only_a_thin_check():
    for name in ("request.md", "solution.md"):
        assert "record it with `probed: true`" in _block(_flow(name), "context"), name
    for path in _prompt_files():
        assert "thin: true" not in _text(path), path.name
    assert "`thin: {reason}`" in _step("request.md", "Q", "Q15")  # a thin check's mark stays


def test_sc2_2_no_engineer_seat_skips_the_solution_halfs_steps_checks_and_signature():
    scope = _step("solution.md", "S", "S1")
    assert "When `seats.engineer` is null" in scope
    assert "skips the solution half's steps S1 to S8, its checks and its signature" in scope
    assert "`next: S9`" in scope
    # Out of scope lists the places the PO seat named at Non-goals, each marked.
    assert "under Out of scope" in scope and "`answers.out_of_scope`" in scope
    assert UNCONFIRMED_PLACE in scope
    # The run goes from the record's sections straight to the output flow.
    notes = _step("solution.md", "S", "S11")
    assert re.search(r"with no engineer seat `phase: output`, `next: W1`", notes)
    assert "ready check 8 has marked the missing seat OPEN" in scope


# --- SC2.3: each entry of Existing behavior touched, read against its source ---

def test_sc2_3_each_entry_of_existing_behavior_touched_names_the_file_or_step_of_its_source():
    asked = _step("request.md", "Q", "Q5")
    assert "the file or step it was read from" in asked
    assert "Record `answers.existing_behavior: [{text, source}]`" in asked
    read = _signing_step("P2")
    assert "An entry with no `source` cannot be read" in read
    assert "a gap under ready check 6" in read
    assert "does every entry name the file or step it was measured from" in _ready_checks("P3")[6]


def test_sc2_3_the_checks_before_the_po_seat_signs_read_each_entry_against_its_source():
    read = _signing_step("P2")
    assert ("READ each entry of `answers.existing_behavior` against the file or step its"
            " `source` names") in read
    assert "The source wins" in read
    order = list(_steps(_flow("signing.md"), "[PE]"))
    assert order.index("P2") < order.index("P3") < order.index("P6")
    for step, _ in ENGINEER_STEPS:  # the PO seat's checks only
        assert "`answers.existing_behavior`" not in _signing_step(step), step


def test_sc2_3_an_entry_that_no_longer_holds_gets_an_open_under_ready_check_6():
    read = _signing_step("P2")
    assert "An entry that no longer holds gets an OPEN under ready check 6" in read
    assert FALSE_ENTRY_OPEN in read
    assert "under the entry in Existing behavior touched" in read
    assert "add the line to `open`" in read and "REPORT it" in read
    assert "An OPEN from P2 counts here" in _ready_checks("P3")[6]
