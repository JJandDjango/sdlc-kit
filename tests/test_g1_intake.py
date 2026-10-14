"""Intake's report and G1 (contract: g1-requirements-spec, unit s5-start,
the prompt half: check SC4.1 and the first clause of done_means). The flow
is a prompt, so the specification is the behavior: the suite holds the one
line step I9 gains, word for word, its place after the four parts of the
report that stand today, its condition (a ready-green contract whose
feature has G1 as an active gate), the two ways out and the parked case
that end the report as today, the one file the step reads the fact from
with no fifth command (the design's Sources row and its constraint 11), and
the form and budget the flow file keeps.
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
CONFIG = "`.sdlc/config.yaml`"
READS = "READ " + CONFIG
NOT_LISTED = "`G1` absent from `active_gates`"
EXEMPT = "{id} under `g1.exempt`"
NEEDS = "the feature needs G1"
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
    assert READS in added, "I9 does not learn whether the feature needs G1"
    _in_order(added, "For a ready-green contract", READS, NEEDS, ENDS_ON)
    # The line's own clause holds no second condition: needing G1 is enough,
    # passed or not, for the venue to be the next step.
    assert "else " + NEEDS + ", and " + ENDS_ON in added


def test_sc4_1_the_report_closes_as_today_where_g1_is_not_listed_or_the_feature_is_exempt():
    added = _added(_step(_read(FLOW), "I9"))
    assert NOT_LISTED in added, "I9 does not name the case that G1 is not listed"
    # Both ways out are named, in the design's words, before the close.
    _in_order(added, READS, NOT_LISTED, ", or " + EXEMPT, AS_TODAY, NEEDS)
    assert "STOP" not in added  # no way out stops the report: it ends as it ended


def test_sc4_1_a_parked_contracts_report_closes_as_today():
    added = _added(_step(_read(FLOW), "I9"))
    assert LINE in added
    assert AS_TODAY + ", as a parked contract's report does" in added
    assert added.count("ends as today") == 1
    # The file is read for a ready-green contract alone.
    _in_order(added, "ready-green", READS, "parked")


def test_design_i9_gains_one_sentence_that_closes_on_the_g1_line():
    added = _added(_step(_read(FLOW), "I9"))
    assert LINE in added
    # The design's Scope reads "one sentence at I9": outside the texts in
    # backticks the new words hold no full stop, and they close on the line.
    assert "." not in re.sub(r"`[^`]*`", "", added), added
    assert added.endswith(f"`{LINE}`")


# --- the fact's one source (the design's Sources row) -----------------------

def test_design_sources_i9_reads_the_fact_from_the_config_file_and_names_it_once():
    text = _read(FLOW)
    i9 = _step(text, "I9")
    assert READS in _added(i9), "I9 does not name the file the fact is read from"
    # The design's Sources row: `G1` under `active_gates`, and the `g1.exempt`
    # list. Each is named once in the flow, in I9 alone.
    for source in (".sdlc/config.yaml", "active_gates", "g1.exempt"):
        assert text.count(source) == 1 and source in i9, source


# --- no fifth command (the design's constraint 11) --------------------------

def test_design_constraint_11_i9_runs_no_command_and_intake_keeps_its_four():
    text = _read(FLOW)
    added = _added(_step(text, "I9"))
    assert LINE in added
    # No fifth command in letter: no `python -m` in the new words, and the
    # flow's four stand as they stood.
    assert "python -m" not in added
    assert set(re.findall(r"python -m taskcontract ([a-z-]+)", text)) == COMMANDS
    commands = re.findall(r"`(python -m [^`]*)`", text)
    commands += re.findall(r"^\s+(python -m .*)$", text, re.MULTILINE)
    assert len(commands) == 4
    # And none in substance: the new words run nothing, by any name.
    for word in ("RUN", "Bash", "taskcontract", "g1-check", "g1-record", "tree", "exit "):
        assert word not in added, f"I9's new words hold {word!r}: the step runs no command"
    assert "g1-check" not in text and "g1-record" not in text


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
