"""G1-flow structural suite (contract: g1-requirements-spec, unit s3-review,
the prompt half). The flow is a prompt, so the specification is the
behavior: the suite holds the seven steps and their order, the four
commands, the 11 items of G1.3 word for word, the sentences that keep an
agent from answering an item or signing, the two closing lines, the four
lines SKILL.md gains, and the places ready checks 1 to 15 are asked.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
FLOW = ROOT / "skills" / "sdlc" / "flows" / "g1.md"
SKILL = ROOT / "skills" / "sdlc" / "SKILL.md"
INTAKE = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
SIGNING = ROOT / "skills" / "product-specification-interview" / "flows" / "signing.md"
GATE_PAGE = ROOT / "docs" / "gates" / "G1-requirements-spec.md"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token

STEPS = ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]
VALIDATE = "`python -m taskcontract validate specs/{id}/contract.yaml --profile ready`"
CHECK = "`python -m taskcontract g1-check {id}`"
LINT = "`python -m taskcontract g1-record lint {id}`"
MODEL = "`python -m taskcontract g1-record model {id}`"
REVIEW = ('python -m taskcontract g1-record review {id} --by "{name}" --seat {seat} '
          '--checked {checked} --unchecked {n}="{section}"')
NO_AGENT = "An agent may draft a reading of an item; it never answers one and never signs."
ONLY_AFTER = "only after the person has given a name, a seat and the word to sign"
PASSED = "G1 has passed for {id}. Next step: the first unit's approve-tests."
NOT_PASSED = "G1 has not passed for {id}. Fix each line above, then run /sdlc g1 {id} again."
NONE_AGAIN = "The review asks none of ready checks 1 to 15 again"

SKILL_DISPATCH_BEFORE = [
    "   - `audit` - LOAD {skill-dir}/flows/audit.md and EXECUTE the Audit flow (A1-A2).",
    "   - `update` - LOAD {skill-dir}/flows/update.md and EXECUTE the Update flow (U1-U3).",
    "   - `new` - LOAD {skill-dir}/flows/new.md and EXECUTE the New flow (N1-N2); the second argument is the task id.",
    "   - `intake` - LOAD {skill-dir}/flows/intake.md and EXECUTE the Intake flow (I1-I9); remaining text is the raw request, when given.",
    "   - `vocab` - LOAD {skill-dir}/flows/vocab.md and sub-dispatch on the next argument: none - the List flow (L1); `add` - the Add flow (VA1-VA2), third argument is the term slug; `extract` - the Extract flow (X1-X4), remaining text names the surfaces, when given.",
    "   - `lang` - LOAD {skill-dir}/flows/lang.md and sub-dispatch on the next argument: none - the Lang Check flow (LC1); `extract` - the Lang Extract flow (LX1).",
    "   Otherwise (no args, or a scaffold / `init` intent) LOAD {skill-dir}/flows/init.md and EXECUTE the Init interview, steps 1-6.",
]

# The question sentences of ready checks 1 to 8 (signing.md, P3) and 11 to 15
# (signing.md, E3), as they stand today. Check 3's carries a second sentence.
P3_QUESTIONS = [
    "1. Does the statement's outcome clause name a state of the world?",
    "2. Are there three to five success criteria, one line each, each an outcome a test can decide?",
    "3. Does every criterion hold two or three checks, each with an id, none marked thin? A thin check, and a check with no confirmed scenario, carries its OPEN from Q15.",
    "4. Does Non-goals hold the standing line and at least one line specific to this feature?",
    "5. Is every prerequisite marked exists or missing, and does a missing one name its ticket or owner?",
    "6. Is Existing behavior touched listed, or does it say \"none\", and does every entry name the file or step it was measured from and have a regression check? An OPEN from P2 counts here.",
    "7. Is every error message a check rejects with written verbatim?",
    "8. Is the PO seat named, and for a bug fix does a `Measured:` row for the findings fall inside the consumer's window?",
]
E3_QUESTIONS = [
    "11. Does every fact a check names have a Sources row, and does every pair of sources that can disagree name its winner?",
    "12. Does every output kind have a drawn example, with its edges?",
    "13. Does every unit name its retirements or \"none\", and list its tests by check id and kind?",
    "14. Do the checks run before signing read green, or does each finding stand answered in the document?",
    "15. Does each of the four cases have an answer, and does each yes name who was asked and what was decided?",
]
INTAKE_I2_READS = ("READ the requirements document against ready checks 1 to 8 and the design "
                   "document against 11 to 15, each a question: asked, never parsed")
INTAKE_I2_POINTS = ("`{skill-dir}/../product-specification-interview/flows/signing.md` holds "
                    "the questions at P3 and E3")


def _read(path: Path) -> str:
    """The file's text, or the empty text when the file does not stand yet."""
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _step(text: str, label: str) -> str:
    """One step of a flow: from its label at a line's start to the next
    step's label, or to the close of the instructions block. Empty when the
    flow holds no such step."""
    found = re.search(rf"^{label}\. ", text, re.MULTILINE)
    if not found:
        return ""
    rest = text[found.start():]
    end = re.search(r"\n\n[A-Z]+\d+\. |\n</instructions>", rest)
    return rest[:end.start()] if end else rest


def _plain(text: str) -> str:
    """Text for a word-for-word comparison: bold marks dropped, a Markdown
    link cut to its words, wrapped lines joined, whitespace collapsed."""
    text = text.replace("**", "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return " ".join(text.split())


def _question(numbered: str) -> str:
    """A ready check's question with its number cut off, lower case, for the
    search that must not find it."""
    return _plain(numbered.split(". ", 1)[1].split("? ")[0]).rstrip("?").lower()


def _page_items() -> dict[int, str]:
    """G1.3's items as G1's page ratified them: number -> plain text."""
    page = GATE_PAGE.read_text(encoding="utf-8")
    block = page.split("### G1.3 review checklist", 1)[1].split("\n## ", 1)[0]
    items: dict[int, str] = {}
    number = None
    for line in block.splitlines()[1:]:
        opened = re.match(r"^(\d+)\. (.*)$", line)
        if opened:
            number = int(opened[1])
            items[number] = opened[2]
        elif number is not None and line.startswith(" ") and line.strip():
            items[number] += " " + line.strip()
        else:
            number = None
    return {n: _plain(words) for n, words in items.items()}


def _flow_items(r5: str) -> dict[int, list[str]]:
    """The items as step R5 holds them: one indented line an item, opening
    on the item's number and a full stop."""
    items: dict[int, list[str]] = {}
    for found in re.finditer(r"^[ \t]+(\d+)\. (.+)$", r5, re.MULTILINE):
        items.setdefault(int(found[1]), []).append(_plain(found[2]))
    return items


def _section(text: str, tag: str) -> list[str]:
    body = re.search(rf"<{tag}>\n(.*?)</{tag}>", text, re.DOTALL)
    return body[1].splitlines() if body else []


def _skill_additions(text: str) -> dict[str, list[str]]:
    """The lines of SKILL.md this unit adds, by kind."""
    return {
        "dispatch": [line for line in _section(text, "instructions")
                     if line.startswith("   - `g1` - ")],
        "flow list": [line for line in _section(text, "context") if "g1.md" in line],
        "constraint": [line for line in _section(text, "constraints") if "G1.3" in line],
        "criterion": [line for line in _section(text, "criteria")
                      if line.startswith("- [ ] G1 flow:")],
    }


def _commands(text: str) -> list[str]:
    """Each command the flow authors: a `python -m` call inside backticks,
    or standing alone on its own indented line."""
    inline = re.findall(r"`(python -m [^`]*)`", text)
    alone = re.findall(r"^[ \t]+(python -m .*)$", text, re.MULTILINE)
    return inline + alone


# --- the seven steps (ruling 1, done_means) --------------------------------

def test_done_means_the_flow_holds_seven_steps_r1_to_r7_in_order():
    text = _read(FLOW)
    labels = re.findall(r"^(R\d+)\. ", text, re.MULTILINE)
    assert labels == STEPS
    block = re.search(r"<instructions>\n(.*?)</instructions>", text, re.DOTALL)
    assert block, "the steps stand inside one instructions block"
    assert re.findall(r"^(R\d+)\. ", block[1], re.MULTILINE) == STEPS
    assert "`/sdlc g1 {id}`" in text
    assert "after intake and before a unit's first task" in _plain(text)


def test_done_means_r1_stops_when_the_contract_is_not_ready_green_or_g1_is_not_active():
    r1 = _step(_read(FLOW), "R1")
    assert "specs/{id}/contract.yaml" in r1
    assert VALIDATE in r1 and CHECK in r1
    assert r1.index(VALIDATE) < r1.index(CHECK)
    assert "not ready-green" in r1
    assert "`{id}: G1 is not active`" in r1
    assert r1.count("STOP") >= 2
    # R1 records nothing: no writer runs before the two readings pass.
    assert "g1-record" not in r1


def test_done_means_r2_shows_a_declarations_form_and_stops_since_a_person_writes_it():
    text = _read(FLOW)
    r2 = _step(text, "R2")
    assert "`.sdlc/config.yaml`" in r2 and "`specs/components.yaml`" in r2
    assert "a person writes a declaration, never the flow" in r2
    assert "SHOW" in r2 and "STOP" in r2
    assert r2.index("SHOW") < r2.index("STOP")
    for part in ("g1:", "schemas:", "linter:", "pin:",
                 "version: 1", "components:", "hard_core:", "oracle:"):
        assert part in r2, f"the form shown at R2 lacks {part!r}"
    # The stop comes before either writer runs.
    assert text.index("a person writes a declaration, never the flow") < text.index(LINT)


def test_done_means_r3_and_r4_run_the_lint_and_model_writers_and_show_their_lines():
    text = _read(FLOW)
    r3, r4 = _step(text, "R3"), _step(text, "R4")
    assert LINT in r3 and MODEL not in r3
    assert MODEL in r4 and LINT not in r4
    for step in (r3, r4):
        assert "SHOW its lines" in step
    # A failed condition is a result the flow carries to R7, never a halt.
    assert "a result, never a failed step" in r3


def test_done_means_r7_runs_g1_check_shows_its_lines_and_names_the_next_step():
    text = _read(FLOW)
    r7 = _step(text, "R7")
    assert CHECK in r7
    assert "SHOW its lines" in r7
    assert "next step" in r7.lower()
    assert "g1-record" not in r7
    # R7 is the last step: nothing runs after the verdict.
    assert text[text.index(r7) + len(r7):].strip() == "</instructions>"


def test_done_means_r7s_report_ends_on_one_of_the_two_lines_word_for_word():
    r7 = _step(_read(FLOW), "R7")
    lines = [line.strip() for line in r7.splitlines()]
    assert PASSED in lines
    assert NOT_PASSED in lines
    assert lines.index(PASSED) < lines.index(NOT_PASSED)
    assert r7.rstrip().endswith(NOT_PASSED)
    assert "exit 0" in r7[:r7.index(PASSED)]


# --- the commands (rulings 2 and 3, constraint 14) --------------------------

def test_done_means_every_command_the_flow_authors_is_one_segment():
    text = _read(FLOW)
    commands = _commands(text)
    assert len(commands) >= 6, "validate, g1-check twice, lint, model, review"
    for command in commands:
        for mark in ("|", "&&", ";", ">", "<", "$(", "\n"):
            assert mark not in command, f"{mark!r} in {command!r}"
    assert {command.split()[2] for command in commands} == {"taskcontract"}
    assert {command.split()[3] for command in commands} == {"validate", "g1-record", "g1-check"}
    kinds = {command.split()[4] for command in commands if command.split()[3] == "g1-record"}
    assert kinds == {"lint", "model", "review"}
    # No `python -m` call hides outside the two forms read above.
    assert text.count("python -m ") == len(commands)


def test_sc1_2_the_review_command_takes_one_checked_list_and_one_unchecked_flag_an_item():
    r6 = _step(_read(FLOW), "R6")
    lines = [line.strip() for line in r6.splitlines()]
    assert REVIEW in lines, "the review command stands alone on one line of R6"
    plain = _plain(r6)
    assert "one comma-separated list" in plain
    assert '`--unchecked {n}="{section}"` is given once for each unchecked item' in plain
    assert "the section in quotes" in plain
    assert "with no item unchecked the flag is absent" in plain.lower()
    assert "with no item checked `--checked` is absent" in plain.lower()
    assert "SHOW its lines" in r6[r6.index(REVIEW):]


# --- the 11 items (ruling 4, SC1.1, SC1.2) ----------------------------------

def test_sc1_1_r5_holds_the_11_items_word_for_word_as_g1s_page_ratified_them():
    page = _page_items()
    assert sorted(page) == list(range(1, 12))  # the page still holds 11
    held = _flow_items(_step(_read(FLOW), "R5"))
    assert sorted(held) == list(range(1, 12))
    for number in range(1, 12):
        assert held[number] == [page[number]], f"item {number} differs from G1's page"


def test_sc1_1_r5_asks_a_person_each_item_one_at_a_time_in_its_own_words():
    text = _read(FLOW)
    r5 = _step(text, "R5")
    assert "ASK" in r5
    assert "11 items" in r5
    assert "one at a time" in r5
    assert "in the item's own words" in r5
    assert "checked or unchecked" in r5
    assert "`docs/features/{id}.md`" in r5 and "`docs/features/{id}.design.md`" in r5
    assert "An item with no answer from the person is asked again, never filled in." in r5
    # The items are asked before the signature is, and nowhere but R5.
    for step in STEPS:
        if step != "R5":
            assert not _flow_items(_step(text, step)).get(11), f"{step} holds items too"


def test_sc1_1_r5_shows_intakes_ready_rows_as_the_evidence_for_items_3_and_4():
    r5 = _step(_read(FLOW), "R5")
    found = re.search(r"[^.\n]*items 3 and 4[^.\n]*\.", r5)
    assert found, "R5 names items 3 and 4"
    assert "`Ready:` rows" in found[0]
    assert "SHOW" in found[0] and "evidence" in found[0]


def test_sc1_2_r5_asks_which_section_an_unchecked_item_concerns():
    r5 = _step(_read(FLOW), "R5")
    found = re.search(r"[^.\n]*item left unchecked[^.\n]*\.", r5)
    assert found, "R5 names an item left unchecked"
    assert "ASK which section" in found[0]
    assert "concerns" in found[0]


# --- the signature (ruling 5, constraint 13, the second non-goal) -----------

def test_sc1_1_r6_keeps_the_rule_that_an_agent_never_answers_an_item_and_never_signs():
    text = _read(FLOW)
    r6 = _step(text, "R6")
    assert NO_AGENT in r6
    assert text.count(NO_AGENT) == 1
    # No sentence of the flow lets an agent answer or sign.
    lowered = _plain(text).lower()
    for opening in ("an agent may answer", "an agent may sign", "the agent answers",
                    "the agent signs", "sign for the person", "answer for the person"):
        assert opening not in lowered


def test_sc1_1_r6_runs_the_review_writer_only_after_a_name_a_seat_and_the_word_to_sign():
    text = _read(FLOW)
    r6 = _step(text, "R6")
    assert "ASK the signer's name and seat" in r6
    assert "the word to sign" in r6
    assert "RUN the writer " + ONLY_AFTER in r6
    assert "`intake-seat`" in r6
    command = r6.index("python -m taskcontract g1-record review")
    for said_first in ("ASK the signer's name and seat", NO_AGENT, ONLY_AFTER):
        assert r6.index(said_first) < command, f"{said_first!r} stands after the command"
    assert "A person who declines to sign gets no review record" in r6
    # The review writer is named in R6 alone: no other step can run it.
    assert text.count("g1-record review") == r6.count("g1-record review") == 1


def test_sc1_1_r6_shows_the_revisions_the_signature_names_one_for_each_document_of_a_pair():
    r6 = _step(_read(FLOW), "R6")
    assert "revisions the signature names" in r6
    assert "`Ready:` rows" in r6
    assert "one for each document of a pair" in r6
    assert r6.index("one for each document of a pair") < r6.index("ASK for the word to sign")


# --- ready checks 1 to 15 (ruling 7, SC1.3, constraint 12) ------------------

def test_sc1_3_the_g1_flow_and_skill_md_hold_no_ready_check_question():
    flow, skill = _read(FLOW), _read(SKILL)
    assert NONE_AGAIN in _plain(flow)
    assert _skill_additions(skill)["dispatch"], "SKILL.md dispatches no `g1` yet"
    for name, text in (("flows/g1.md", flow), ("SKILL.md", skill)):
        lowered = _plain(text).lower()
        for numbered in P3_QUESTIONS + E3_QUESTIONS:
            assert _question(numbered) not in lowered, f"{name} asks: {numbered}"
        assert not re.search(r"ready check \d", lowered), f"{name} names one ready check"


def test_sc1_3_the_interview_and_intake_still_ask_ready_checks_1_to_15_as_today():
    assert len(P3_QUESTIONS) + len(E3_QUESTIONS) == 13
    # The flow says where they are asked, in the user guide's words.
    assert (NONE_AGAIN + ": the interview and intake ask them, as today.") in _plain(_read(FLOW))
    signing = SIGNING.read_text(encoding="utf-8")
    p3, e3 = _step(signing, "P3"), _step(signing, "E3")
    assert p3.startswith("P3. READY CHECKS - READ the document against ready checks 1 to 8, "
                         "each a question")
    assert e3.startswith("E3. READY CHECKS - READ the document against ready checks 11 to 15, "
                         "each a question")
    assert "\n".join("   " + line for line in P3_QUESTIONS) in p3
    assert "\n".join("   " + line for line in E3_QUESTIONS) in e3
    for numbered in P3_QUESTIONS + E3_QUESTIONS:
        assert signing.count(numbered) == 1
    i2 = _step(INTAKE.read_text(encoding="utf-8"), "I2")
    assert INTAKE_I2_READS in i2
    assert INTAKE_I2_POINTS in i2
    assert "`Ready check {n}: {gap}. Marked OPEN.`" in i2


# --- SKILL.md (ruling 8) ----------------------------------------------------

def test_done_means_skill_md_dispatches_g1_to_its_flow_file():
    skill = _read(SKILL)
    added = _skill_additions(skill)["dispatch"]
    assert len(added) == 1
    assert added[0].startswith(
        "   - `g1` - LOAD {skill-dir}/flows/g1.md and EXECUTE the G1 flow (R1-R7)")
    assert "id" in added[0]
    lines = _section(skill, "instructions")
    place = lines.index(added[0])
    assert lines.index("0. DISPATCH. If this skill was invoked with a first argument naming "
                       "a subcommand, do NOT run the interview:") < place
    assert place < lines.index(SKILL_DISPATCH_BEFORE[-1])
    assert FLOW.is_file(), "the dispatch line names a flow file that does not stand"


def test_done_means_skill_md_names_g1_md_in_its_flow_list():
    skill = _read(SKILL)
    added = _skill_additions(skill)["flow list"]
    assert len(added) == 1
    context = _plain("\n".join(_section(skill, "context")))
    listed = context.split("one PromptLang file per subcommand (ADR 0025): ", 1)[1]
    listed = listed.split(" This file dispatches", 1)[0]
    names = [name.strip(" .") for name in listed.split(",")]
    assert sorted(names) == sorted(["init.md", "new.md", "intake.md", "vocab.md", "lang.md",
                                    "audit.md", "update.md", "g1.md", "execute.md"])
    assert listed.endswith(".")


def test_sc1_1_skill_md_holds_the_constraint_that_no_agent_signs_a_g1_3_review():
    added = _skill_additions(_read(SKILL))["constraint"]
    assert len(added) == 1
    assert added[0].startswith("- No agent signs a G1.3 review")
    assert "`g1-record review` only on the person's word" in added[0]
    assert "never answers one" in added[0]


def test_done_means_skill_md_holds_one_criterion_for_the_g1_flow():
    added = _skill_additions(_read(SKILL))["criterion"]
    assert len(added) == 1
    assert "11 items" in added[0]
    assert "person" in added[0]
    assert "word to sign" in added[0]
    assert "`g1-check`" in added[0]


def test_done_means_skill_md_gains_four_lines_and_loses_nothing():
    skill = _read(SKILL)
    additions = _skill_additions(skill)
    for kind, lines in additions.items():
        assert len(lines) == 1, f"SKILL.md holds {len(lines)} {kind} lines for G1"
    added = [lines[0] for lines in additions.values()]
    kept = skill.splitlines()
    for line in added:
        assert kept.count(line) == 1
        kept.remove(line)
    # What stands without the four lines holds the dispatch block and the
    # flow list as they stood; the file's size is not pinned.
    for line in SKILL_DISPATCH_BEFORE:
        assert line in kept
    assert "0025): init.md, new.md, intake.md, vocab.md, lang.md, audit.md," in kept
    assert "update.md. This file dispatches; the flow file executes. The" in kept


# --- form and size (ruling 9, constraint 10) --------------------------------

def test_done_means_the_g1_flow_keeps_the_promptlang_shape_and_budget():
    text = _read(FLOW)
    assert text.startswith("---\nname: sdlc-flow-g1\ndescription: ")
    assert text.split("\n")[3] == "---"
    opened = set(re.findall(r"<([a-z][a-z0-9-]*)>", text))
    assert opened == {"purpose", "instructions"}
    for tag in opened:
        assert text.count(f"<{tag}>") == 1 and text.count(f"</{tag}>") == 1
    assert text.index("</purpose>") < text.index("<instructions>")
    assert len(text) < CHAR_CEILING


def test_done_means_skill_md_keeps_its_tag_set_and_budget_with_the_g1_lines():
    skill = _read(SKILL)
    assert all(_skill_additions(skill).values()), "SKILL.md lacks a G1 line"
    opened = re.findall(r"<([a-z][a-z0-9-]*)>", skill)
    assert opened == ["purpose", "context", "instructions", "constraints", "criteria"]
    for tag in opened:
        assert skill.count(f"</{tag}>") == 1
    assert len(skill) < CHAR_CEILING
