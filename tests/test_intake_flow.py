"""Intake-flow structural suite (contract: playbook-guardrails, unit
u7-intake-questions; contract: g0-declaration, unit d4-intake-flow). The
flow is a prompt, so the specification is the behavior: the suite holds the
words the engineer seat is asked, the feature-document rule, the roster
stop and the entities declaration, the PromptLang shape, and the
token-budget proxy.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
FLOW = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token
NO_ROSTER = ("No ratified seat roster. Author and ratify specs/vocabulary/intake-seat.yaml "
             "(`/sdlc vocab add intake-seat` drafts it), then run intake again.")


def _step(text: str, label: str) -> str:
    start = re.search(rf"^{label}\. ", text, re.MULTILINE).start()
    end = text.find("\n\nI", start + 1)
    return text[start:end if end > 0 else None]


def test_i4_asks_the_three_plan_questions_in_the_playbook_words():
    i4 = _step(FLOW.read_text(encoding="utf-8"), "I4")
    assert "which files change (`scope`)" in i4
    assert "in what order (`depends_on`)" in i4
    assert "which tests prove it (`acceptance_sketch`)" in i4
    assert "engineer seat" in i4


def test_i4_and_i5_take_the_answers_from_an_implementation_section():
    text = FLOW.read_text(encoding="utf-8")
    i4, i5 = _step(text, "I4"), _step(text, "I5")
    assert "Implementation section" in i4 and "READ the three from it" in i4
    assert "never as a contract field" in i4  # the schema is unchanged
    assert "files as `scope`, order as `depends_on`, tests as `acceptance_sketch`" in i5
    assert "keep or change them" in i5
    assert "never ask afresh what the document already answers" in i5


def test_i1_stops_before_any_contract_without_a_ratified_roster():
    # SC3.2: the roster check runs before the scaffold writes a file, and
    # the stop line is the request's, verbatim.
    text = FLOW.read_text(encoding="utf-8")
    i1 = _step(text, "I1")
    assert "vocab-list" in i1 and "`intake-seat`" in i1
    assert NO_ROSTER in i1
    assert text.index(NO_ROSTER) < text.index("python -m taskcontract new")


def test_entities_is_always_declared_and_the_empty_list_waits_for_the_po_seat():
    # SC3.1: every contract carries entities, and [] is written only on the
    # PO seat's confirmed answer, never by default (ADR 0030).
    text = FLOW.read_text(encoding="utf-8")
    i4, i5, i6, i7 = (_step(text, step) for step in ("I4", "I5", "I6", "I7"))
    assert "omit the field" not in text
    assert "ALWAYS declare `entities:`" in i4
    assert "never write the empty list by default" in i4
    assert "`entities: []`" in i5 and "PO seat" in i5
    assert "`entities: []` only when the PO seat confirmed it" in i6
    assert "A drop that leaves `entities` empty returns to I5" in i7  # no side door


def test_flow_keeps_the_promptlang_shape_and_budget():
    text = FLOW.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    opened = set(re.findall(r"<([a-z][a-z0-9-]*)>", text))
    assert opened == {"purpose", "instructions"}
    for tag in opened:
        assert f"</{tag}>" in text
    assert len(text) < CHAR_CEILING
