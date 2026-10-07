"""Intake's refusals, structurally (contract: feature-document, unit
f4-intake). The flow is a prompt, so the specification is the behavior:
the suite holds how a check's unit is read, the ready-check gap and its
message, the place of the refusals between the roster stop and the
scaffold, the word-for-word `done_means` that intake never rewords, the
sketch entry of two checks as the tree reads it, and what the flow keeps.
The pair of documents, its `Parked:` and `Ready:` rows and its stops are
held by tests/test_intake_pair.py.

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

def test_sc4_2_a_ready_check_gap_parks_with_its_message_and_counts_once():
    i2 = _step(_flow(), "I2")
    assert "A ready check with a gap." in i2
    assert ("READ the requirements document against ready checks 1 to 8 and the design "
            "document against 11 to 15, each a question") in i2
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
