"""Intake takes the pair, and a stale design stops it
(contract: document-split, unit d5-intake).

The flows are prompts, so this suite pins the text of three files:
skills/sdlc/flows/intake.md, skills/sdlc/SKILL.md and the interview's
flows/signing.md. SC3.2: a design is stale when the requirements document
holds a text revision newer than the one the design names; the checks
before the engineer seat signs report it at E4, the seat's word to sign
still stands, and intake on that pair stops with the same message. SC4.2:
intake reads three stops only when nothing stands, writes no row and no
contract, and reports each case that holds, in a fixed order. SC4.1: intake
finds the design document beside the requirements document, reads its
refusals on both, parks the pair with one `Parked:` row in each table,
takes each contract field from one document, and on ready-green writes one
`Ready:` row in each table.

Nothing here pins what intake does with a combined document.

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
ROOT = _HERE if (_HERE / "skills" / "sdlc").is_dir() else Path.cwd()
FLOW = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
SKILL = ROOT / "skills" / "sdlc" / "SKILL.md"
SIGNING = ROOT / "skills" / "product-specification-interview" / "flows" / "signing.md"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token

REQUIREMENTS_PATH = "`docs/features/{id}.md`"
DESIGN_PATH = "`docs/features/{id}.design.md`"
NO_ROSTER = ("No ratified seat roster. Author and ratify specs/vocabulary/intake-seat.yaml "
             "(`/sdlc vocab add intake-seat` drafts it), then run intake again.")
SCAFFOLD = "python -m taskcontract new"
COMMANDS = {"vocab-list", "new", "graph", "validate"}
SIGNING_COMMANDS = [
    "python -m taskcontract lang-check --draft docs/features/{id}.state.yaml",
    "python -m taskcontract lang-check --draft docs/features/{id}.design.state.yaml",
]

# The messages, each as the feature document and USAGE give it.
NO_DESIGN = "`No design document for {id}. Run the design interview first.`"
NO_PO = "`The requirements document has no PO signature on r{n}.`"
NO_ENGINEER = "`The design document has no engineer signature on r{n}.`"
STALE = "`The design names requirements r{n}; the requirements stand at r{m}. Stale.`"
NO_UNIT = "`Check {id} is assigned to no unit.`"
TWO_UNITS = "`Check {id} is assigned to units {a} and {b}.`"
NO_CHECK = "`Unit {id} delivers no check.`"
GAP = "`Ready check {n}: {gap}. Marked OPEN.`"
STALE_BLOCK = "`{block} is stamped r{n}; the newest revision is r{m}. Stale.`"

# One rule, shared word for word by E4 and by intake.
STALE_RULE = ("A design is stale when the requirements document holds a text revision "
              "newer than the one the design names")
WORD_STANDS = "The seat's word to sign still stands."

# The rows intake writes.
PARKED = "`r{n}: Parked: {what stands}`"
NOT_TEXT = "opens on none of `Ready:`, `Measured:`, `Signed:` or `Parked:`"
READY_OPENS = "r{n}: Ready: contract `{id}` validates ready-green, derived from r{m}"
READY_REQUIREMENTS = "; the PO seat ({name}) signed the request half at r{m} (r{b})"
READY_DESIGN = (", against requirements r{k}; the engineer seat ({name}) signed the "
                "solution half at r{m} (r{b})")
# The two rows as the feature document draws them, on a feature `x`.
DRAWN_REQUIREMENTS = ("r5: Ready: contract `x` validates ready-green, derived from r3; "
                      "the PO seat (ann) signed the request half at r3 (r4)")
DRAWN_DESIGN = ("r5: Ready: contract `x` validates ready-green, derived from r3, against "
                "requirements r3; the engineer seat (raj) signed the solution half at r3 (r4)")

# The parts of I2, in the order intake reads them.
PARTS = ("DESIGN - ", "REFUSALS - ", "PARK - ", "STOPS - ")

# Wording the unit retires.
RETIRED = ("seat boundary", "the newest revision both seats signed",
           "the higher of the two revisions signed", "intake's only write",
           "REPORT the half that has no signature", "11 to 14")


def _flat(text: str) -> str:
    """The text with each whitespace run collapsed to one space."""
    return " ".join(text.split())


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _step(text: str, label: str) -> str:
    """One step of a flow, up to the next blank line, its whitespace folded."""
    match = re.search(rf"^{label}\. ", text, re.MULTILINE)
    assert match, f"the flow has no step {label}"
    end = text.find("\n\n", match.start())
    return _flat(text[match.start():end if end > 0 else None])


def _line(text: str, opening: str) -> str:
    """The one line of a prompt file that opens on these words."""
    lines = [line for line in text.splitlines() if line.startswith(opening)]
    assert len(lines) == 1, f"{len(lines)} lines open on: {opening}"
    return _flat(lines[0])


def _part(i2: str, name: str) -> str:
    """One part of I2: from its name to the next part's name."""
    assert name in i2, f"I2 has no part {name}"
    start = i2.index(name)
    later = [i2.index(other) for other in PARTS if other in i2 and i2.index(other) > start]
    return i2[start:min(later) if later else None]


def _in_order(haystack: str, *needles: str) -> None:
    """Each needle stands in the haystack, and they stand in this order."""
    at = -1
    for needle in needles:
        assert needle in haystack, f"missing: {needle}"
        here = haystack.index(needle)
        assert here > at, f"out of order: {needle}"
        at = here


def _fill(template: str, **values: str) -> str:
    """A row's wording with each `{key}` replaced by its value."""
    for key, value in values.items():
        template = template.replace("{" + key + "}", value)
    return template


# SC3.2: one rule and one message for a stale design, in E4 and in intake.

def test_sc3_2_a_design_is_stale_when_the_requirements_hold_a_newer_text_revision():
    e4 = _step(_read(SIGNING), "E4")
    stops = _part(_step(_read(FLOW), "I2"), "STOPS - ")
    # One rule, in the same words in both flows.
    assert STALE_RULE in e4
    assert STALE_RULE in stops
    # Intake names what each side of the rule is read from.
    assert ("The design names the `requirements r{m}` of its table's newest text row that "
            "names one.") in stops
    assert ("A document's newest text revision is the highest row of its own table that "
            f"{NOT_TEXT}.") in stops


def test_sc3_2_e4_reports_a_stale_design_and_the_seats_word_to_sign_still_stands():
    text = _read(SIGNING)
    e4 = _step(text, "E4")
    assert f"{STALE_RULE}: REPORT {STALE}" in e4
    assert e4.endswith(f"REPORT {STALE} {WORD_STANDS}")
    # The stale blocks are still read: a design document holds a derived Contract block.
    _in_order(e4, "READ each derived block's stamp against the newest revision.",
              "REPORT each stale block with its message.", STALE_RULE)
    assert STALE_BLOCK in _flat(text)
    # The flow keeps its seven E steps, its two Bash calls, its tags and its ceiling.
    assert re.findall(r"^(E\d+)\. ", text, re.MULTILINE) == [f"E{n}" for n in range(1, 8)]
    assert re.findall(r"`(python -m [^`]*)`", text) == SIGNING_COMMANDS
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "context",
                                                             "instructions"}
    assert len(text) < CHAR_CEILING


def test_sc3_2_intake_stops_on_a_stale_design_with_the_message_e4_reports():
    signing, flow = _read(SIGNING), _read(FLOW)
    stops = _part(_step(flow, "I2"), "STOPS - ")
    assert STALE in _step(signing, "E4")
    assert STALE in stops
    # One message: each flow holds it once, and intake words no other.
    assert _flat(signing).count(STALE) == 1
    assert _flat(flow).count(STALE) == 1
    assert _flat(flow).count("Stale.") == 1
    assert f"then {STALE}, with r{{m}} the requirements document's newest text revision" in stops
    # A stale design stops intake; it parks nothing.
    _in_order(stops, STALE, "STOP before any contract exists: write no row and no contract")


# SC4.2: the three stops.

def test_sc4_2_the_three_stops_stand_verbatim_and_are_reported_in_their_order():
    stops = _part(_step(_read(FLOW), "I2"), "STOPS - ")
    assert "REPORT each case that holds, verbatim, in this order:" in stops
    _in_order(stops, "REPORT each case that holds, verbatim, in this order:",
              NO_PO, NO_ENGINEER, STALE)


def test_sc4_2_a_signature_is_missing_when_it_signs_no_revision_or_an_older_one():
    text = _read(FLOW)
    stops = _part(_step(text, "I2"), "STOPS - ")
    assert ("Its signature is its table's latest `Signed:` row: the signer is that row's "
            "Revised By cell, and the revision it signs is the newest text revision above "
            "it, never the `Signed:` row's own number (ADR 0034).") in stops
    assert (f"{NO_PO} and {NO_ENGINEER}, each when that document's signature signs an older "
            "revision than r{n}, its newest text revision, or none;") in stops
    # Each table counts alone: the one revision both seats signed is gone.
    for retired in RETIRED:
        assert retired not in _flat(text), retired


def test_sc4_2_the_stops_are_read_only_when_nothing_stands():
    text = _read(FLOW)
    i2 = _step(text, "I2")
    assert "STOPS - read only when nothing stands." in i2
    _in_order(i2, "REFUSALS - ", "PARK - a refusal parks the pair.", PARKED,
              "STOPS - read only when nothing stands.", NO_PO)
    assert ("Intake reads the refusals on the pair as it stands: a pair with something "
            "standing parks even when a signature is missing or the design is stale.") in i2


def test_sc4_2_a_stop_writes_no_row_and_no_contract():
    text = _read(FLOW)
    i2 = _step(text, "I2")
    stops = _part(i2, "STOPS - ")
    assert ("When a case holds, STOP before any contract exists: write no row and no "
            "contract, and return to the conversation.") in stops
    assert ("A stop gets no `Parked:` row: the three refusals are all that parks a "
            "pair.") in stops
    assert ("A pair that stops or parks here gets no contract: nothing under `specs/` is "
            "created or changed.") in i2
    assert stops.endswith("The seat signs, or confirms the design, through its own run, "
                          "then intake runs again.")
    # Every stop stands before the scaffold writes a file.
    for message in (NO_PO, NO_ENGINEER, STALE):
        _in_order(_flat(text), NO_ROSTER, message, SCAFFOLD)


def test_sc4_2_skill_md_holds_a_stop_for_a_missing_signature_or_a_stale_design():
    criterion = _line(_read(SKILL), "- [ ] Intake flow:")
    assert ("stopped with no row and no contract while a signature is missing or the "
            "design is stale") in criterion
    _in_order(criterion, "a pair read before the scaffold:",
              "parked with one `Parked:` row in each table",
              "stopped with no row and no contract while a signature is missing",
              "given one `Ready:` row in each table")


# SC4.1: one contract from the pair, and a row in each table.

def test_sc4_1_intake_finds_the_design_document_beside_and_stops_without_one():
    text = _read(FLOW)
    i2 = _step(text, "I2")
    design = _part(i2, "DESIGN - ")
    assert ("DESIGN - it is the requirements document of a pair: FIND the design document "
            f"beside it, at {DESIGN_PATH}.") in design
    assert (f"With none, STOP: REPORT {NO_DESIGN}, write nothing, and return to the "
            "conversation.") in design
    assert "Parked:" not in design  # the stop writes no row
    # Intake still takes the requirements document's path.
    assert (f"When the request is a feature document at {REQUIREMENTS_PATH}, READ it here, "
            "before the scaffold, in four parts, in this order.") in i2
    _in_order(_flat(text), NO_ROSTER, NO_DESIGN, "REFUSALS - ", SCAFFOLD)


def test_sc4_1_the_pair_is_read_in_four_parts_and_intake_keeps_its_steps_and_commands():
    text = _read(FLOW)
    i2 = _step(text, "I2")
    _in_order(i2, "in four parts, in this order.", *PARTS)
    # The nine steps keep their ids and their order: the roster stop, the read, the scaffold.
    assert re.findall(r"^(I\d+)\. ", text, re.MULTILINE) == [f"I{n}" for n in range(1, 10)]
    assert NO_ROSTER in _step(text, "I1") and SCAFFOLD in _step(text, "I3")
    # The word `Signed:` stands in I2 and I7 alone, and intake never writes one.
    assert "Intake writes `Ready:` and `Parked:` rows, and never a `Signed:` row." in i2
    for step in ("I1", "I3", "I4", "I5", "I6", "I8", "I9"):
        assert "Signed:" not in _step(text, step), step
    # Four commands and no fifth, each one segment.
    assert set(re.findall(r"python -m taskcontract ([a-z-]+)", text)) == COMMANDS
    commands = re.findall(r"`(python -m [^`]*)`", text)
    commands += re.findall(r"^\s+(python -m .*)$", text, re.MULTILINE)
    assert len(commands) == 4
    for command in commands:
        assert not re.search(r"[|;&<>]", command), command
    assert text.startswith("---\n")
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    assert len(text) < CHAR_CEILING


def test_sc4_1_the_refusals_are_read_on_both_documents():
    i2 = _step(_read(FLOW), "I2")
    refusals = _part(i2, "REFUSALS - ")
    assert ("REFUSALS - read on both documents. Intake refuses ready while any of these "
            "stands:") in refusals
    assert "1. An OPEN mark in either document. 2." in refusals
    assert ("READ the requirements document against ready checks 1 to 8 and the design "
            "document against 11 to 15, each a question: asked, never parsed") in refusals
    assert "signing.md` holds the questions at P3 and E3" in refusals
    assert f"A gap reads {GAP}" in refusals
    assert ("3. A check of the requirements document assigned to no unit, or to two, of "
            "the design document's Units, or a unit that delivers no check.") in refusals
    _in_order(refusals, "Each message names its id, verbatim:", NO_UNIT, TWO_UNITS, NO_CHECK)


def test_sc4_1_a_refusal_parks_the_pair_with_one_parked_row_in_each_table():
    park = _part(_step(_read(FLOW), "I2"), "PARK - ")
    assert "PARK - a refusal parks the pair." in park
    assert ("WRITE one row into each document's revision table: the date, `intake` in the "
            f"Revised By cell, and the changes cell {PARKED}, with r{{n}} one past that "
            "table's last row.") in park
    assert "Both rows hold the same list." in park
    assert "Intake writes nothing else: it changes no section and writes no contract." in park
    assert ("REPORT the same list and return to the conversation; each seat fixes its "
            "document through its own run, signs again, and intake runs again.") in park
    assert ("A `Parked:` row changes no text: a later run reads the pair afresh, and an "
            "earlier `Parked:` row parks nothing.") in park


def test_sc4_1_the_parked_list_names_the_requirements_documents_things_first():
    park = _part(_step(_read(FLOW), "I2"), "PARK - ")
    assert ("`{what stands}` names every thing that stands, each in its own words, one "
            "after another on one line, the requirements document's things first, then "
            "the design document's, each in this order:") in park
    _in_order(park, "the requirements document's things first", "then the design document's",
              "each in this order:", "the OPEN marks in document order",
              "then the ready-check gaps by check number",
              "then the Units messages, by check and then by unit, in the document's order")


def test_sc4_1_each_contract_field_has_one_source():
    text = _read(FLOW)
    i4, i5 = _step(text, "I4"), _step(text, "I5")
    assert ("For a pair, each contract field has one source: "
            "the title, the statement, the non-goals, the checks and the terms from the "
            "requirements document; the scope, the units, each `done_means` word for "
            "word, the order and the tests from the design document.") in i4
    # The copies the flow already held stand after it.
    _in_order(i4, "each contract field has one source:", "WRITE `title:` from its title line",
              "COPY each unit's `done_means` word for word from its row's Done means cell "
              "under Units", "Intake never rewords a copied `done_means`")
    assert ("READ the three from its own sections (files from Scope, order from Order, "
            "tests from the Tests cell of each row under Units)") in i4
    # I5 stands: each unit takes a human answer, and intake asks which seats answered.
    assert "Every unit needs a human answer before the contract is final" in i5
    assert "ASK which seats answered for each unit" in i5


def test_sc4_1_ready_green_writes_one_ready_row_in_each_table():
    i7 = _step(_read(FLOW), "I7")
    assert ("When the loop ends ready-green and the request is a feature document at "
            f"{REQUIREMENTS_PATH}, ADD one row to each document's revision table: the date, "
            f"`intake`, and a changes cell that opens ``{READY_OPENS}``, with r{{n}} one "
            "past that table's last row and r{m} that table's signed text revision, as I2 "
            "read it.") in i7
    assert "Each cell then names its own seat and the revision that seat signed." in i7
    assert f"The requirements document's cell goes on ``{READY_REQUIREMENTS}``." in i7
    assert f"The design document's goes on ``{READY_DESIGN}``." in i7
    assert ("r{b} is the `Signed:` row's own number, {name} that row's Revised By cell, "
            "and r{k} the requirements revision the design names.") in i7
    # The row waits for the green loop, which stays as it is.
    _in_order(i7, "Fix exactly what each TCnnn diagnostic names.", "Cap at 5 iterations",
              "When the loop ends ready-green", READY_OPENS)


def test_sc4_1_each_ready_row_fills_to_the_row_the_feature_document_draws():
    i7 = _step(_read(FLOW), "I7")
    # The rows are read from the flow: what opens the cell, then each table's own end.
    opens = re.search(r"a changes cell that opens ``(.*?)``,", i7)
    ends = re.findall(r"goes on ``(.*?)``\.", i7)
    assert opens and len(ends) == 2, "I7 words no row for each table"
    assert opens.group(1) == READY_OPENS  # byte for byte through `derived from r{m}`
    requirements, design = (opens.group(1) + end for end in ends)
    assert _fill(requirements, id="x", n="5", m="3", name="ann", b="4") == DRAWN_REQUIREMENTS
    assert _fill(design, id="x", n="5", m="3", k="3", name="raj", b="4") == DRAWN_DESIGN
    # Each row names one seat, and only the design's names a requirements revision.
    assert "engineer" not in requirements and "requirements r" not in requirements
    assert "PO seat" not in design
    assert _fill(design, id="x", n="6", m="4", k="5", name="raj", b="5") == (
        "r6: Ready: contract `x` validates ready-green, derived from r4, against "
        "requirements r5; the engineer seat (raj) signed the solution half at r4 (r5)")


def test_sc4_1_skill_md_speaks_of_one_row_in_each_table_of_a_pair():
    text = _read(SKILL)
    strata = _line(text, "- Do NOT touch Cairn strata")
    writes = _line(text, "- intake writes ONLY")
    criterion = _line(text, "- [ ] Intake flow:")
    assert (f"One exception: intake adds one `Ready:` or `Parked:` row to each revision "
            f"table of a pair, at {REQUIREMENTS_PATH} and {DESIGN_PATH}.") in strata
    assert ("intake writes ONLY `specs/{id}/contract.yaml` and, for a pair, one `Ready:` or "
            "`Parked:` row in each revision table; a parked pair gets no contract, and a "
            "red contract never hands off to development.") in writes
    assert ("a pair read before the scaffold: stopped with nothing written when no design "
            "document stands, parked with one `Parked:` row in each table and no contract "
            "while a refusal stands in either document,") in criterion
    assert ("and given one `Ready:` row in each table only once the contract validates "
            "ready-green; nothing else written.") in criterion
    # The three one-row sentences are gone.
    flat = _flat(text)
    for retired in ("intake adds its `Ready:` or `Parked:` row",
                    "row in its revision table", "a parked document gets no contract",
                    "given its `Ready:` row"):
        assert retired not in flat, retired
    # The file keeps its tags and its ceiling.
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {
        "purpose", "context", "instructions", "constraints", "criteria"}
    assert len(text) < CHAR_CEILING
