"""Intake's report and G1 (contract: g1-requirements-spec, unit s5-start,
the prompt half: check SC4.1 and the first clause of done_means). The flow
is a prompt, so the specification is the behavior: the suite holds the one
line step I9 gains, word for word, its place after the four parts of the
report that stand today, its condition (a ready-green contract whose
feature has G1 as an active gate), the two ways out and the parked case
that end the report as today, the kit's own reading the step learns the
fact from, and the form and budget the flow file keeps.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
FLOW = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token

# Step I9 as it stood before this unit: every word stays, in order.
TODAY = ("I9. REPORT the contract path, its state (ready-green, or parked-draft + blocker), "
         "the seats recorded, and a one-line scope summary. Development starts only from green.")
PARTS = ["the contract path", "its state", "the seats recorded", "a one-line scope summary"]
LINE = "Next step: G1. Run /sdlc g1 {id}."
ENDS_ON = "the report ends on this line, verbatim: `" + LINE + "`"
CHECK = "`g1-check {id}`"
HOW = CHECK + " as I1 runs `vocab-list`"
NOT_ACTIVE = "`{id}: G1 is not active`"
AS_TODAY = "the report ends as today"
COMMANDS = {"vocab-list", "new", "graph", "validate"}


def _read(path: Path) -> str:
    """The file's text, or the empty text when the file does not stand."""
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _step(text: str, label: str) -> str:
    """One step of the flow: from its label at a line's start to the next
    step's label, or to the close of the instructions block."""
    found = re.search(rf"^{label}\. ", text, re.MULTILINE)
    if not found:
        return ""
    rest = text[found.start():]
    end = re.search(r"\n\n[A-Z]+\d+\. |\n</instructions>", rest)
    return rest[:end.start()] if end else rest


def _added(i9: str) -> str:
    """What I9 holds after the words that stand today; empty when the step
    does not open on them."""
    return i9[len(TODAY):] if i9.startswith(TODAY) else ""


def _in_order(text: str, *parts: str) -> None:
    at = 0
    for part in parts:
        found = text.find(part, at)
        assert found >= 0, f"{part!r} is absent, or stands before the part ahead of it"
        at = found + len(part)


# --- the line's words (ruling 1, SC4.1, done_means) -------------------------

def test_sc4_1_i9_holds_the_g1_line_word_for_word_with_the_flows_own_placeholder():
    text = _read(FLOW)
    i9 = _step(text, "I9")
    assert f"`{LINE}`" in i9, "I9 holds no G1 line in backticks"
    # One line, in I9 alone, and no second wording of it anywhere in the flow.
    assert text.count(LINE) == 1
    assert text.count("Next step") == 1
    assert text.count("/sdlc g1") == 1
    # The id is the flow's own placeholder, `{id}`: never the guide's example
    # id, and never a form in angle brackets, which the form rules read as a tag.
    assert "apply-discount" not in text
    assert "<id>" not in text and "{feature}" not in i9 and "{contract}" not in i9


def test_done_means_the_report_names_g1_as_the_next_step_and_ends_on_that_line():
    i9 = _step(_read(FLOW), "I9")
    added = _added(i9)
    assert ENDS_ON in added, "I9 does not end the report on the G1 line"
    # The line names the gate and the venue's command, in that order.
    _in_order(LINE, "Next step: ", "G1", "Run ", "/sdlc g1 {id}")
    assert LINE.endswith(".")


# --- the line's place (ruling 1, SC4.1) -------------------------------------

def test_sc4_1_the_g1_line_stands_after_the_path_the_state_the_seats_and_the_scope_line():
    i9 = _step(_read(FLOW), "I9")
    assert LINE in i9
    _in_order(i9, "REPORT ", *PARTS, "Development starts only from green.", LINE)
    for part in PARTS:
        assert i9.count(part) == 1, f"I9 names {part!r} more than once"
    # Nothing is reported between the four parts and the line but the line's condition.
    assert "REPORT" not in _added(i9)


# --- the words that stand today (ruling 2) ----------------------------------

def test_ruling_2_every_word_i9_holds_today_stays_in_order_and_i9_stays_the_last_step():
    text = _read(FLOW)
    i9 = _step(text, "I9")
    assert LINE in i9
    assert i9.startswith(TODAY), "I9 no longer opens on the words it held"
    assert text.count(TODAY) == 1
    assert _added(i9).startswith(" "), "the new words join the old on the same line"
    # The steps keep their ids and their order, and I9 closes the flow.
    assert re.findall(r"^(I\d+)\. ", text, re.MULTILINE) == [f"I{n}" for n in range(1, 10)]
    assert text[text.index(i9) + len(i9):].strip() == "</instructions>"
    # The step before it stands as it stood: G1 is named in I9 alone.
    for step in (f"I{n}" for n in range(1, 9)):
        assert "G1" not in _step(text, step), step
    assert "G1" not in text.split("<instructions>", 1)[0]


# --- the line's condition (ruling 1, SC4.1) ---------------------------------

def test_sc4_1_i9_names_g1_only_for_a_ready_green_contract_whose_feature_has_g1_active():
    added = _added(_step(_read(FLOW), "I9"))
    assert CHECK in added, "I9 does not learn whether G1 is active"
    _in_order(added, "For a ready-green contract", CHECK, "G1 is active", ENDS_ON)
    # Both results of the verdict mean the gate is active: passed or not, the
    # venue is the next step.
    before = added[:added.index(ENDS_ON)]
    assert re.search(r"exit 0 or (exit )?1 means G1 is active", before), before


def test_sc4_1_the_report_closes_as_today_where_g1_is_not_listed_or_the_feature_is_exempt():
    added = _added(_step(_read(FLOW), "I9"))
    assert NOT_ACTIVE in added, "I9 does not name the reading that G1 is not active"
    _in_order(added, CHECK, "exit 2", NOT_ACTIVE, AS_TODAY)
    out = added[added.index(NOT_ACTIVE):]
    out = out[:out.index(AS_TODAY)]
    # Both ways out are named, between the kit's line and the close.
    assert "not listed" in out and "exempt" in out, out
    assert "STOP" not in added  # no way out stops the report: it ends as it ended


def test_sc4_1_a_parked_contracts_report_closes_as_today():
    added = _added(_step(_read(FLOW), "I9"))
    assert LINE in added
    assert AS_TODAY + ", as a parked contract's report does" in added
    assert added.count("ends as today") == 1
    # The kit's reading is asked for a ready-green contract alone.
    _in_order(added, "ready-green", CHECK, "parked")


def test_design_i9_gains_one_sentence_that_closes_on_the_g1_line():
    added = _added(_step(_read(FLOW), "I9"))
    assert LINE in added
    # The design's Scope reads "one sentence at I9": outside the texts in
    # backticks the new words hold no full stop, and they close on the line.
    assert "." not in re.sub(r"`[^`]*`", "", added), added
    assert added.endswith(f"`{LINE}`")


# --- the kit's own reading (ruling 3, reading 7) ----------------------------

def test_reading_7_i9_learns_the_fact_from_the_kits_g1_check_in_one_bash_call():
    text = _read(FLOW)
    added = _added(_step(text, "I9"))
    assert HOW in added, "I9 does not say how the kit's reading is run"
    assert "RUN the kit's " + HOW + ", one Bash call" in added
    # One reading, asked once, and in I9 alone.
    assert text.count("g1-check") == 1
    assert "tree" not in added and "g1-record" not in text


def test_reading_7_intake_never_reads_the_config_for_whether_g1_is_active():
    text = _read(FLOW)
    assert CHECK in _step(text, "I9")
    for source in (".sdlc/", "config.yaml", "active_gates", "g1.exempt", "g1:"):
        assert source not in text, f"the flow names {source!r}: the kit reads it, never intake"


def test_reading_7_the_g1_check_is_named_bare_so_intake_keeps_its_four_commands():
    text = _read(FLOW)
    added = _added(_step(text, "I9"))
    assert CHECK in added
    assert "python -m" not in added
    assert set(re.findall(r"python -m taskcontract ([a-z-]+)", text)) == COMMANDS
    commands = re.findall(r"`(python -m [^`]*)`", text)
    commands += re.findall(r"^\s+(python -m .*)$", text, re.MULTILINE)
    assert len(commands) == 4
    # The call is one segment as the step words it.
    for held in re.findall(r"`([^`]*)`", added):
        assert not re.search(r"[|;&<>]", held), held


# --- form and size (ruling 4) -----------------------------------------------

def test_ruling_4_intake_keeps_the_promptlang_shape_and_budget_with_the_g1_line():
    text = _read(FLOW)
    assert LINE in text
    assert text.startswith("---\nname: sdlc-flow-intake\ndescription: ")
    assert text.split("\n")[3] == "---"
    opened = set(re.findall(r"<([a-z][a-z0-9-]*)>", text))
    assert opened == {"purpose", "instructions"}
    for tag in opened:
        assert text.count(f"<{tag}>") == 1 and text.count(f"</{tag}>") == 1
    assert text.index("</purpose>") < text.index("<instructions>")
    assert len(text) < CHAR_CEILING, len(text)
    # I9 stays one line, as I1, I3 to I6 and I8 are, and the file ends on its close.
    assert "\n" not in _step(text, "I9")
    assert text.endswith("</instructions>\n")
