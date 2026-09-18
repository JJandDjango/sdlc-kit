"""Intake-flow structural suite (contract: playbook-guardrails, unit
u7-intake-questions). The flow is a prompt, so the specification is the
behavior: the suite holds the words the engineer seat is asked, the
feature-document rule, the PromptLang shape, and the token-budget proxy.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
FLOW = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token


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
    assert "`source: document`" in i4
    assert "keep or change them" in i5
    assert "never ask afresh what the document already answers" in i5


def test_flow_keeps_the_promptlang_shape_and_budget():
    text = FLOW.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    opened = set(re.findall(r"<([a-z][a-z0-9-]*)>", text))
    assert opened == {"purpose", "instructions"}
    for tag in opened:
        assert f"</{tag}>" in text
    assert len(text) < CHAR_CEILING
