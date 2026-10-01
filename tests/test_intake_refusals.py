"""Intake's refusals, structurally (contract: feature-document, unit
f4-intake). The flow is a prompt, so the specification is the behavior:
the suite holds the three refusal messages, the `Parked:` row and what it
names, the readings that park a document or stop intake before any
contract exists (the park first, the signature stop only when nothing
stands), the word-for-word `done_means` that intake never rewords, the
pair form the tree reads, the `Ready:` row that names both seats, and
what the flow keeps.

Every sentence is searched with its whitespace folded, so the flow may
wrap its lines.
"""

from __future__ import annotations

import re
from pathlib import Path

_HERE = Path(__file__).resolve().parent.parent
# Beside a tree that holds the skill, read that tree; a copy run from any
# other folder reads the tree pytest was started in.
ROOT = _HERE if (_HERE / "skills" / "sdlc").is_dir() else Path.cwd()
FLOW = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token

NO_ROSTER = ("No ratified seat roster. Author and ratify specs/vocabulary/intake-seat.yaml "
             "(`/sdlc vocab add intake-seat` drafts it), then run intake again.")
SCAFFOLD = "python -m taskcontract new"
NO_UNIT = "`Check {id} is assigned to no unit.`"
TWO_UNITS = "`Check {id} is assigned to units {a} and {b}.`"
NO_CHECK = "`Unit {id} delivers no check.`"
GAP = "`Ready check {n}: {gap}. Marked OPEN.`"
PARKED = "`r{n}: Parked: {what stands}`"
NOT_TEXT = "opens on none of `Ready:`, `Measured:`, `Signed:` or `Parked:`"
READY = ("``r{n}: Ready: contract `{id}` validates ready-green, derived from r{m}; "
         "the PO seat ({name}) signed the request half at r{a} (r{b}), "
         "the engineer seat ({name}) the solution half at r{c} (r{d})``")
TITLE = ("WRITE `title:` from its title line `# {id} - {title}`: the words after "
         "`{id} - `, or the whole heading text when the heading opens on anything else")
COMMANDS = {"vocab-list", "new", "graph", "validate"}


def _flat(text: str) -> str:
    return " ".join(text.split())


def _flow() -> str:
    return FLOW.read_text(encoding="utf-8")


def _step(text: str, label: str) -> str:
    """One step of the flow, its whitespace folded."""
    match = re.search(rf"^{label}\. ", text, re.MULTILINE)
    assert match, f"the flow has no step {label}"
    end = text.find("\n\nI", match.start() + 1)
    return _flat(text[match.start():end if end > 0 else None])


def _in_order(haystack: str, *needles: str) -> None:
    """Each needle stands in the haystack, and they stand in this order."""
    at = -1
    for needle in needles:
        assert needle in haystack, f"missing: {needle}"
        here = haystack.index(needle)
        assert here > at, f"out of order: {needle}"
        at = here


# SC4.1: a check without one unit, or a unit without a check.

def test_sc4_1_the_three_refusal_messages_stand_verbatim_each_naming_its_id():
    i2 = _step(_flow(), "I2")
    assert "A check assigned to no unit or to two, or a unit that delivers no check." in i2
    assert "Each message names its id, verbatim:" in i2
    _in_order(i2, NO_UNIT, TWO_UNITS, NO_CHECK)


def test_sc4_1_a_checks_unit_is_read_from_the_checks_cell_where_plus_joins_two():
    i2 = _step(_flow(), "I2")
    assert ("A check's unit is read from the Checks cell of its row under Units, "
            "where `+` joins two checks that share one sketch entry.") in i2


def test_sc4_1_the_refusals_run_after_the_roster_stop_and_before_the_scaffold():
    text = _flow()
    flat = _flat(text)
    for message in (NO_UNIT, TWO_UNITS, NO_CHECK):
        _in_order(flat, NO_ROSTER, message, SCAFFOLD)
    # The nine steps keep their ids and their order (SKILL.md cites I1-I9).
    assert re.findall(r"^(I\d+)\. ", text, re.MULTILINE) == [f"I{n}" for n in range(1, 10)]
    assert SCAFFOLD in _step(text, "I3")


def test_sc4_1_a_units_refusal_parks_the_document():
    i2 = _step(_flow(), "I2")
    assert "REFUSALS - intake refuses ready while any of these stands:" in i2
    _in_order(i2, NO_CHECK, "PARK - a refusal parks the document.", PARKED)
    assert "then the Units messages, by check and then by unit, in the document's order" in i2


def test_sc4_1_a_unit_of_more_than_three_checks_pairs_two_in_one_entry():
    i4 = _step(_flow(), "I4")
    assert ("WRITE each check into the `acceptance_sketch` of the unit its Checks cell "
            "names, the check's id last in its entry, inside `( )`.") in i4
    assert ("A unit holds at most three entries: a unit of more than three checks pairs "
            "two in one entry that ends in both ids, the two its Checks cell joins "
            "with `+`.") in i4
    assert "1-3 acceptance_sketch criteria" in i4  # the schema's cap stands


def test_sc4_1_a_pair_stands_in_one_parenthesis_with_a_comma_as_the_tree_reads_it():
    i4 = _step(_flow(), "I4")
    assert ("The two ids stand inside one `( )` at the end of the entry with a comma "
            "between, as `(SC2.2, SC2.3)`; the tree reads that pair as the check "
            "`SC2.2+SC2.3`.") in i4
    assert ("The `+` belongs to the Units table's Checks cell and to the tree's id, "
            "never to the sketch entry.") in i4
    # The example agrees with itself: the ids split on the comma, joined with `+`.
    pair, named = re.search(r"as `\(([^()`]*)\)`; the tree reads that pair as the "
                            r"check `([^`]*)`", i4).groups()
    assert "+" not in pair
    assert "+".join(part.strip() for part in pair.split(",")) == named


# SC4.2: an OPEN mark or a ready-check gap parks the document.

def test_sc4_2_an_open_mark_parks_above_the_seat_boundary_in_decisions_and_below():
    i2 = _step(_flow(), "I2")
    assert "An OPEN mark above the seat boundary or in Decisions and open questions." in i2
    assert ("Below the seat boundary an OPEN mark is its ready check failing, "
            "and parks too.") in i2


def test_sc4_2_a_ready_check_gap_parks_with_its_message_and_counts_once():
    i2 = _step(_flow(), "I2")
    assert "A ready check with a gap." in i2
    assert "READ the document against ready checks 1 to 8 and 11 to 14, each a question" in i2
    assert f"A gap reads {GAP}" in i2
    assert "A gap that already carries its OPEN mark counts once, as that mark." in i2


def test_sc4_2_a_ready_check_stays_a_question_and_every_command_is_one_segment():
    text = _flow()
    assert "each a question: asked, never parsed" in _step(text, "I2")
    # No command reads a section: the flow runs the four commands it ran before.
    assert set(re.findall(r"python -m taskcontract ([a-z-]+)", text)) == COMMANDS
    commands = re.findall(r"`(python -m [^`]*)`", text)
    commands += re.findall(r"^\s+(python -m .*)$", text, re.MULTILINE)
    assert len(commands) >= 4
    for command in commands:
        assert not re.search(r"[|;&<>]", command), command
    # The shape and the ceiling stand with the new text in.
    assert text.startswith("---\n")
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    assert len(text) < CHAR_CEILING


def test_sc4_2_the_parked_row_carries_the_date_intake_and_the_next_revision():
    i2 = _step(_flow(), "I2")
    assert ("WRITE one row into its revision table: the date, `intake` in the Revised By "
            f"cell, and the changes cell {PARKED}, with r{{n}} one past the table's last "
            "row.") in i2


def test_sc4_2_one_parked_row_names_every_thing_that_stands_in_a_fixed_order():
    i2 = _step(_flow(), "I2")
    assert ("`{what stands}` names every thing that stands, each in its own words, one "
            "after another on one line, in this order:") in i2
    _in_order(i2, "in this order:", "the OPEN marks in document order",
              "then the ready-check gaps by check number", "then the Units messages")
    assert "REPORT the same list and return to the conversation" in i2


def test_sc4_2_a_refusal_writes_no_contract_and_changes_no_section():
    text = _flow()
    i2 = _step(text, "I2")
    assert "READ it here, before the scaffold" in i2
    assert ("A document that stops or parks here gets no contract: nothing under "
            "`specs/` is created or changed.") in i2
    assert ("That row is intake's only write: it changes no section and writes no "
            "contract.") in i2
    _in_order(_flat(text), NO_ROSTER, "PARK - a refusal parks the document.", SCAFFOLD)


def test_sc4_2_a_parked_row_changes_no_text_and_a_later_run_reads_afresh():
    i2 = _step(_flow(), "I2")
    assert ("A `Parked:` row changes no text: a later run reads the document afresh, "
            "and an earlier `Parked:` row parks nothing.") in i2
    assert NOT_TEXT in i2  # never the row a `Signed:` row signs
    assert "the seats fix the document through the interview, sign again, and run intake again" in i2


def test_sc4_2_a_document_with_something_standing_parks_even_when_a_half_is_unsigned():
    i2 = _step(_flow(), "I2")
    assert ("Intake reads the refusals on the document as it stands, signed or not: a "
            "document with something standing parks even when a half is unsigned.") in i2
    # The refusals and the park stand before the signature stop.
    _in_order(i2, "in three parts, in this order.",
              "REFUSALS - intake refuses ready while any of these stands:",
              "PARK - a refusal parks the document.", PARKED,
              "SIGNATURES - read only when nothing stands.",
              "When a half has no `Signed:` row")


def test_sc4_2_a_missing_signature_gets_no_parked_row():
    i2 = _step(_flow(), "I2")
    assert ("A missing signature gets no `Parked:` row: the three refusals are all "
            "that parks a document.") in i2
    _in_order(i2, "STOP before any contract exists:", "A missing signature gets no "
              "`Parked:` row", "The seat signs through the interview")


def test_sc4_2_intake_writes_ready_and_parked_rows_and_never_a_signed_row():
    text = _flow()
    assert "Intake writes `Ready:` and `Parked:` rows, and never a `Signed:` row." in _flat(text)
    for step in ("I1", "I3", "I4", "I5", "I6", "I8", "I9"):
        assert "Signed:" not in _step(text, step), step


# SC4.3: the document's words, the `Ready:` row, and what stays.

def test_sc4_3_done_means_is_copied_word_for_word_beside_the_title_line():
    i4 = _step(_flow(), "I4")
    assert ("COPY each unit's `done_means` word for word from its row's Done means cell "
            "under Units: the document wins over any wording intake would derive.") in i4
    assert TITLE in i4  # still copied into `title`


def test_sc4_3_a_copied_done_means_is_never_reworded_at_i5_or_i7():
    text = _flow()
    i4 = _step(text, "I4")
    # One sentence, right after the copy.
    assert ("the document wins over any wording intake would derive. Intake never "
            "rewords a copied `done_means`, at I5 or at I7: a change the seat names at "
            "I5, or a diagnostic at I7 that names a `done_means`, goes to the "
            "document's Units row through the interview and a new signature, and "
            "intake runs again.") in i4
    assert text.count("never rewords a copied `done_means`") == 1
    # I5's answers and I7's loop otherwise stay as they are.
    assert "keep, change (the answer names the change), or strike" in _step(text, "I5")
    assert "Fix exactly what each TCnnn diagnostic names." in _step(text, "I7")


def test_sc4_3_the_contract_derives_from_the_newest_revision_both_seats_signed():
    i2 = _step(_flow(), "I2")
    assert "a half's signature is its latest `Signed:` row" in i2
    assert "the signer is that row's Revised By cell" in i2
    assert (f"the revision it signs is the newest row above it that {NOT_TEXT}, never "
            "the `Signed:` row's own number") in i2
    assert ("r{m}, the newest revision both seats signed, is the higher of the two "
            "revisions signed; intake derives the contract from the document at r{m}.") in i2


def test_sc4_3_an_unsigned_half_or_revision_stops_intake_with_no_row_and_no_contract():
    text = _flow()
    i2 = _step(text, "I2")
    assert "SIGNATURES - read only when nothing stands." in i2  # the park comes first
    assert ("When a half has no `Signed:` row, or a row that opens on none of the four "
            "words stands above r{m}, STOP before any contract exists:") in i2
    assert "write no row and no contract, and return to the conversation" in i2
    assert "The seat signs through the interview, then intake runs again." in i2
    _in_order(_flat(text), "When a half has no `Signed:` row", SCAFFOLD)


def test_sc4_3_the_ready_row_names_both_seats_and_the_revision_each_signed():
    i7 = _step(_flow(), "I7")
    assert "The cell then names both seats and the revision each signed" in i7
    assert f"the whole cell reads {READY}." in i7
    assert "r{m} is the newest revision both seats signed, as I2 read it" in i7
    assert ("r{a} and r{c} are the revisions the two halves' `Signed:` rows sign, r{b} "
            "and r{d} those rows' own numbers, and each {name} its row's Revised By "
            "cell.") in i7
    assert "When the loop ends ready-green" in i7  # the row waits for the green loop


def test_sc4_3_the_roster_stop_still_stands_before_the_document_is_read():
    text = _flow()
    i1 = _step(text, "I1")
    assert NO_ROSTER in i1 and "STOP before any contract exists" in i1
    assert "write nothing" in i1 and "Parked:" not in i1  # the stop writes no row
    _in_order(_flat(text), NO_ROSTER,
              "When the request is a feature document at `docs/features/{id}.md`, "
              "READ it here, before the scaffold", SCAFFOLD)


def test_sc4_3_the_plan_answers_come_from_scope_order_and_the_units_rows():
    text = _flow()
    i4 = _step(text, "I4")
    assert "Implementation section" not in text  # the ratified format has none
    assert ("When the request is a feature document, READ the three from its own "
            "sections (files from Scope, order from Order, tests from the Tests cell of "
            "each row under Units) and note each as taken from the document, for the I5 "
            "readback only, never as a contract field.") in i4


def test_sc4_3_each_unit_is_still_confirmed_with_its_seats_beside_the_documents_answers():
    text = _flow()
    i5, i6 = _step(text, "I5"), _step(text, "I6")
    assert "Every unit needs a human answer before the contract is final" in i5
    assert "ASK which seats answered for each unit" in i5
    assert "add `confirmed_by: [seats]` to every unit" in i6
    assert ("SHOW the three plan answers (files as `scope`, order as `depends_on`, tests "
            "as `acceptance_sketch`) beside their source (the document's Scope, Order "
            "and Units sections, or the seat's own words)") in i5
    assert "ASK the engineer seat to keep or change them" in i5
    assert "never ask afresh what the document already answers" in i5


def test_sc4_3_a_blocked_dependency_still_holds_the_contract_at_draft_with_no_parked_row():
    i8 = _step(_flow(), "I8")
    assert "VERIFY `--profile draft` passes" in i8
    assert "REFUSE the development handoff" in i8
    assert ("A feature document gets no `Parked:` row here: a parked document has no "
            "contract, and this contract stands at draft.") in i8
