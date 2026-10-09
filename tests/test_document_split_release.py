"""Kit 0.19.0 ships the pair (contract: document-split, unit d6-release).

The unit ships prompt text and pages, so the text is the behavior. SC4.3:
intake reads at I2, before any other read of the document, whether the
file is a combined document, one that holds a `## Proposed solution`
heading. On one with no `Ready:` row it stops with its message; on one
with a `Ready:` row it stops with a second message; either way it writes
nothing. The rest is the release as the pages tell it: USAGE reads green
under the 0.19.0 banners, the changelog entry, three rows of the map, the
G0 page's title row, the sentences that name a design run's opening, the
stale message's two letters glossed in each flow that words it, one
sentence of the tree's docstring, and the two version numbers.

Nothing here reads G1's documents or USAGE's drawing of G1.

A sentence is matched with each whitespace run folded to one space, and a
page's quote marks dropped, so a file may wrap its lines; a section is cut
by its heading, never by a line number. A size cap is read against the
file's own text, line breaks included. No test runs a model; `python -m
prompt_lang` stays the form receipt.
"""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path

_HERE = Path(__file__).resolve().parent.parent
# Beside a tree that holds the skill, read that tree; a copy run from any
# other folder reads the tree pytest was started in.
ROOT = _HERE if (_HERE / "skills" / "sdlc").is_dir() else Path.cwd()
USAGE = ROOT / "USAGE.md"
CHANGELOG = ROOT / "CHANGELOG.md"
MAP = ROOT / "MAP.md"
G0_PAGE = ROOT / "docs" / "gates" / "G0-planning-intake.md"
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "skills" / "sdlc" / "init.py"
TREE = ROOT / "taskcontract" / "tree.py"
FLOW = ROOT / "skills" / "sdlc" / "flows" / "intake.md"
INTERVIEW = ROOT / "skills" / "product-specification-interview"
OPENING = INTERVIEW / "flows" / "opening.md"
SIGNING = INTERVIEW / "flows" / "signing.md"
INTERVIEW_SKILL = INTERVIEW / "SKILL.md"

GREEN = "\U0001F7E2"
RED = "\U0001F534"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token
PROMPTLANG_TAGS = {"purpose", "instructions", "variables", "context", "constraints",
                   "examples", "output", "criteria", "routing", "directives"}

# --- intake's read of a combined document ----------------------------------------

COMBINED_RULE = "a document that holds a `## Proposed solution` heading is a combined document"
NO_READY_ROW = "`{path} is a combined document with no Ready: row. Intake reads a pair.`"
THROUGH_INTAKE = "`{path} is a combined document through intake. Its contract stands.`"
READY_ROW = "whose changes cell opens `r{n}: Ready:`"
PATH_GLOSS = "{path} the path intake was given"
NOTHING_UNDER_SPECS = ("A pair that stops or parks here gets no contract: nothing under "
                       "`specs/` is created or changed.")
FOUR_PARTS = ("When the request is a feature document at `docs/features/{id}.md`, READ it "
              "here, before the scaffold, in four parts, in this order.")
PARTS = ("DESIGN - ", "REFUSALS - ", "PARK - ", "STOPS - ")
FIND_DESIGN = ("DESIGN - it is the requirements document of a pair: FIND the design document "
               "beside it, at `docs/features/{id}.design.md`.")
NO_DESIGN = "`No design document for {id}. Run the design interview first.`"
NO_ROSTER = ("No ratified seat roster. Author and ratify specs/vocabulary/intake-seat.yaml "
             "(`/sdlc vocab add intake-seat` drafts it), then run intake again.")
SCAFFOLD = "python -m taskcontract new"
COMMANDS = {"vocab-list", "new", "graph", "validate"}

# The rows intake writes, kept byte for byte.
PARKED = "`r{n}: Parked: {what stands}`"
NOT_TEXT = "opens on none of `Ready:`, `Measured:`, `Signed:` or `Parked:`"
READY_OPENS = "``r{n}: Ready: contract `{id}` validates ready-green, derived from r{m}``"
READY_REQUIREMENTS = "``; the PO seat ({name}) signed the request half at r{m} (r{b})``"
READY_DESIGN = ("``, against requirements r{k}; the engineer seat ({name}) signed the "
                "solution half at r{m} (r{b})``")
ROWS_INTAKE_WRITES = "Intake writes `Ready:` and `Parked:` rows, and never a `Signed:` row."
I8_PARKED = ("A feature document gets no `Parked:` row here: a parked document has no "
             "contract, and this contract stands at draft.")

# --- the stale message, its two letters glossed ----------------------------------

STALE = "`The design names requirements r{n}; the requirements stand at r{m}. Stale.`"
WORD_STANDS = "The seat's word to sign still stands."
INTAKE_NAMES = ("The design names the `requirements r{n}` of its table's newest text row "
                "that names one.")
INTAKE_GLOSS = (", with r{n} there the revision the design names and r{m} the requirements "
                "document's newest text revision.")
E4_GLOSS = (", with r{n} the revision the design names and r{m} the requirements document's "
            "newest text revision.")
CONFIRM_NAMES = ("the `requirements r{n}` of the design table's newest text row that names "
                 "one")
OLD_LETTER = "`requirements r{m}`"

# --- a design run's opening, named in two places ---------------------------------

PURPOSE_CLOSE = "and the document written as r1 at the close."
PURPOSE_DESIGN = ("A design run opens on DESIGN READ, the requirements document read before "
                  "anything is written, and at every later dispatch on DESIGN CONFIRM, the "
                  "design confirmed against a newer requirements revision.")
OPENING_LINE = ("{skill-dir}/flows/opening.md DESIGN READ, DESIGN CONFIRM, O1-O6: a design "
                "run's read of the requirements document and its confirmation; id, origin, "
                "title, seats, materials; the state file from O1 on, the document as r1 at O6")

# --- the tree's docstring --------------------------------------------------------

BESIDE = "stands beside it."
NO_DOT = ("A contract's id holds no dot, by the schema's pattern, so no valid contract's "
          "document ends `.design.md`; a contract folder named `x.design` would still read "
          "docs/features/x.design.md as its own.")
# sha256 of tree.py below its module docstring: the release changes that docstring alone.
TREE_CODE = "ebb9ab815be239505d5f9a272eefe6e6f4d9bc52967229fd027fcbac10e85cb7"

# --- USAGE -----------------------------------------------------------------------

INTERVIEW_HEADING = ("### `/sdlc:product-specification-interview` — writing the feature "
                     f"document {GREEN}")
INTERVIEW_BANNER = (
    f"{GREEN} **Shipped** (kit 0.19.0, "
    "[ADR 0029](decisions/0029-feature-document-format-and-done.md) as ADRs 0033 to 0037 "
    "amend it, contract `specs/document-split/`). Kit 0.18.0's interview wrote one combined "
    "document, both halves in one file at `docs/features/<id>.md`: this page at tag "
    "`v0.18.0` is its guide.")
USAGE_STOPS = [
    "docs/features/x.md is a combined document with no Ready: row. Intake reads a pair.",
    "docs/features/x.md is a combined document through intake. Its contract stands.",
    "No design document for x. Run the design interview first.",
]
USAGE_TAKES_THE_PAIR = (
    f"{GREEN} **Intake takes the pair.** `/sdlc intake docs/features/<id>.md` takes the "
    "requirements document's path and finds the design document beside it. It stops, with "
    "nothing written, on a combined document and on a missing design document:")
USAGE_COMBINED = (
    f"{GREEN} A combined document is one that holds a `## Proposed solution` heading. The "
    "first message is for one with no `Ready:` row. The second is for one with a `Ready:` "
    "row: it stays unchanged, and its contract validates as before.")
SECTION_9_BANNER_END = (
    "\"Revisions and halves\"; kit 0.18.0, "
    "[ADR 0036](decisions/0036-the-appendix-names-the-contract-and-a-unit-row-holds-done.md), "
    "contract `specs/feature-document/`, \"A parked document\"; kit 0.19.0, "
    "[ADR 0037](decisions/0037-a-feature-document-is-a-pair-and-each-document-has-one-seat.md), "
    "contract `specs/document-split/`, \"A pair of documents\").")
PAIR_PARAGRAPHS = (
    f"{GREEN} The tree shows a pair before intake as one feature.",
    f"{GREEN} With no design document, a feature prints as kit 0.18.0 prints it:",
    f"{GREEN} For a pair through intake, the drift mark reads each table against that "
    "table's `Ready:` row.",
)
BEFORE_INTAKE = (
    f"{GREEN} Each `.md` file directly under `docs/features/` that has no "
    "`specs/<id>/contract.yaml` shows as a feature at the first level: a **feature before "
    "intake**, from its first revision on. A design document, `<id>.design.md`, is the one "
    "exception (\"A pair of documents\"). A document whose table holds no revision shows "
    "too. Its id is the file's name without `.md`. The features with a contract keep the "
    "order of `specs/`, and a feature before intake stands among them by its id.")
READY_ROW_PARAGRAPH = (
    f"{GREEN} When the request is a feature document at `docs/features/<id>.md`, intake "
    "adds one row to each document's revision table once the contract validates "
    "ready-green: the date, `intake`, and a changes cell that opens ``rN: Ready: contract "
    "`<id>` validates ready-green, derived from rM``, with `rN` the next revision in that "
    "table and `rM` that table's signed text revision.")
PARKED_PARAGRAPH = (
    f"{GREEN} A `Parked:` row is no text row either: intake writes one in each table when "
    "it parks a pair, and it never moves `rN`.")

# --- the changelog, the map and the G0 page --------------------------------------

RELEASE_HEADING = "## 0.19.0 - 2026-10-07 (tag `v0.19.0`)"
UNITS = ("d1-requirements", "d2-design", "d3-signing", "d4-tree", "d5-intake", "d6-release")
ADR_0037 = ("[0037](decisions/0037-a-feature-document-is-a-pair-and-each-document-has-one-"
            "seat.md)")
MAP_INTAKE = (
    "| raw-request intake | The consumer's feature document is the raw request: a pair, the "
    "requirements document and the design document of one feature. Intake takes the "
    "requirements document's path and produces one contract from the pair (section-to-field "
    "mapping, each field from one document; a `Ready:` or `Parked:` row in each revision "
    "table as the linkage record), and stops on a combined document | implemented (v1) | "
    f"[decisions/0026](decisions/0026-feature-document-as-raw-request.md), {ADR_0037} |")
MAP_INTERVIEW = (
    "| specification interview | `/sdlc:product-specification-interview`, the feature "
    "document's writer, upstream of G0: a pair in ADR 0029's format, each document written "
    "in its own run from r1, one question at a time, resumable state beside it. A "
    "requirements run writes `docs/features/<id>.md` for the PO seat, with one Gherkin "
    "scenario per check; a design run writes `docs/features/<id>.design.md` for one engineer "
    "seat, names the requirements revision it stands against and records the four consult "
    "cases. The checks before each seat signs (`lang-check --draft` and the ready checks, "
    "advisory), then a `Signed:` row in that seat's document; intake refuses ready on an "
    "OPEN mark, a ready-check gap or a check without one unit, with a `Parked:` row in each "
    "table and no contract, and stops on a missing signature or a stale design; domain "
    "modules deferred | implemented (v1) | "
    "[decisions/0028](decisions/0028-specification-interview-skill.md), "
    "[0029](decisions/0029-feature-document-format-and-done.md), "
    "[0033](decisions/0033-the-solution-half-names-sources-examples-and-retirements.md), "
    "[0036](decisions/0036-the-appendix-names-the-contract-and-a-unit-row-holds-done.md), "
    f"{ADR_0037} |")
MAP_TREE = ("feature documents before intake, with their revision and each half's signature, "
            "a pair shown as one feature with its design document's revision as a second "
            "mark")
TITLE_SOURCE = "which intake copies from the requirements document's title line"
OLD_TITLE_SOURCE = "which intake copies from the feature document's title line"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """The text with each whitespace run folded to one space."""
    return " ".join(text.split())


def _unquoted(text: str) -> str:
    """A page's text on one line: its quote marks dropped, whitespace folded."""
    return _flat(re.sub(r"^>", "", text, flags=re.MULTILINE))


def _cut(text: str, opening: str, stop: str) -> str:
    """The part of a page from the heading that opens on `opening` up to
    the next line that matches `stop`, or to the end of the page."""
    start = re.search(rf"^{re.escape(opening)}", text, re.MULTILINE)
    assert start, f"the page has no heading that opens {opening!r}"
    end = re.compile(stop, re.MULTILINE).search(text, start.end())
    return text[start.start():end.start() if end else len(text)]


def _section(number: int) -> str:
    """One numbered section of USAGE, up to the next numbered section."""
    return _cut(_read(USAGE), f"## {number}. ", r"^## \d+\. ")


def _subsection(section: str, name: str) -> str:
    return _cut(section, f"### {name}", r"^### ")


def _paragraphs(text: str) -> list[str]:
    """The blocks a blank line parts, each on one line without quote marks."""
    return [_unquoted(block) for block in re.split(r"\n[ \t]*\n", text) if block.strip()]


def _paragraph(text: str, needle: str) -> str:
    """The first paragraph of the text that holds the needle."""
    found = [block for block in _paragraphs(text) if needle in block]
    assert found, f"no paragraph holds {needle!r}"
    return found[0]


def _banner(section: str) -> str:
    """The first block quote of a section, on one line without its quote marks."""
    lines = section.splitlines()
    first = next((at for at, line in enumerate(lines) if line.startswith(">")), None)
    assert first is not None, "the section has no banner"
    quote = []
    for line in lines[first:]:
        if not line.startswith(">"):
            break
        quote.append(line)
    return _unquoted("\n".join(quote))


def _in_order(haystack: str, *needles: str) -> None:
    """Each needle stands in the haystack, and they stand in this order."""
    at = 0
    for needle in needles:
        found = haystack.find(needle, at)
        assert found >= 0, f"{needle!r} does not stand after position {at}"
        at = found + len(needle)


def _version(path: Path, pattern: str) -> tuple[int, ...]:
    match = re.search(pattern, _read(path), re.MULTILINE)
    assert match, f"{path.name} names no version"
    return tuple(int(part) for part in match.group(1).split("."))


def _step(text: str, label: str) -> str:
    """One step of a flow, up to the next blank line, its whitespace folded."""
    match = re.search(rf"^{re.escape(label)}(?:\.| -) ", text, re.MULTILINE)
    assert match, f"the flow has no step {label}"
    end = text.find("\n\n", match.start())
    return _flat(text[match.start():end if end > 0 else None])


def _part(i2: str, name: str) -> str:
    """One part of I2: from its name to the next part's name."""
    assert name in i2, f"I2 has no part {name}"
    start = i2.index(name)
    later = [i2.index(other) for other in PARTS if other in i2 and i2.index(other) > start]
    return i2[start:min(later) if later else None]


def _combined_read(i2: str) -> str:
    """I2's read of a combined document: from the sentence that says what
    makes a document combined up to the first of the four parts."""
    assert COMBINED_RULE in i2, "I2 does not say what makes a document combined"
    start = i2.index(COMBINED_RULE)
    assert "DESIGN - " in i2 and i2.index("DESIGN - ") > start, (
        "the combined-document read does not stand before the DESIGN part")
    return i2[start:i2.index("DESIGN - ")]


def _map_row(name: str) -> str:
    rows = [line for line in _read(MAP).splitlines() if line.startswith(f"| {name} |")]
    assert len(rows) == 1, f"{len(rows)} rows of the map open on {name!r}"
    return rows[0].rstrip()


def _prompt_shape(path: Path) -> str:
    """A prompt file's text, after its PromptLang tags and its ceiling are
    read: the size counts the file's own text, line breaks included."""
    text = _read(path)
    assert text.startswith("---\n"), path.name
    opened = re.findall(r"<([a-z][a-z0-9-]*)>", text)
    assert set(opened) <= PROMPTLANG_TAGS, (path.name, set(opened) - PROMPTLANG_TAGS)
    for tag in opened:
        assert f"</{tag}>" in text, (path.name, tag)
    assert "<purpose>" in text and "<instructions>" in text, path.name
    assert len(text) < CHAR_CEILING, (path.name, len(text))
    return text


# --- SC4.3: a combined document with no `Ready:` row -----------------------------

def test_sc4_3_intake_reads_whether_the_document_is_combined_before_the_design_read():
    text = _read(FLOW)
    i2 = _step(text, "I2")
    # The heading makes a document combined, and I2 says so once, before its four parts.
    _in_order(i2, FOUR_PARTS, NOTHING_UNDER_SPECS, COMBINED_RULE, FIND_DESIGN, "REFUSALS - ")
    assert _flat(text).count("`## Proposed solution`") == 1
    # The four parts keep their count and their order: the read adds no fifth.
    _in_order(i2, "in four parts, in this order.", *PARTS)
    assert not re.search(r"\b[A-Z]{4,} - ", _combined_read(i2))


def test_sc4_3_intake_stops_on_a_combined_document_with_no_ready_row_with_its_message():
    text = _read(FLOW)
    combined = _combined_read(_step(text, "I2"))
    assert NO_READY_ROW in combined
    assert "STOP" in combined and "REPORT" in combined
    assert "return to the conversation" in combined
    # The message stands once, and `{path}` is glossed once.
    assert _flat(text).count(NO_READY_ROW) == 1
    assert combined.count(PATH_GLOSS) == 1
    # The stop stands after the roster stop and before every other read and the scaffold.
    _in_order(_flat(text), NO_ROSTER, NO_READY_ROW, NO_DESIGN, "REFUSALS - ", SCAFFOLD)


def test_sc4_3_a_stop_on_a_combined_document_writes_no_row_no_contract_and_nothing_under_specs():
    text = _read(FLOW)
    i2 = _step(text, "I2")
    combined = _combined_read(i2)
    assert "write nothing" in combined
    # No row and no command: the read holds neither a write nor a Bash call.
    assert "WRITE" not in combined and "ADD" not in combined
    assert "Parked:" not in combined and "python -m" not in combined
    # No contract and nothing under specs/: I2 says so above the read, and the
    # scaffold, the first write under specs/, stands a step later.
    _in_order(i2, NOTHING_UNDER_SPECS, COMBINED_RULE)
    assert SCAFFOLD not in i2 and SCAFFOLD in _step(text, "I3")


# --- SC4.3: a combined document that holds a `Ready:` row ------------------------

def test_sc4_3_a_combined_document_with_a_ready_row_stops_with_its_contract_stands_message():
    text = _read(FLOW)
    combined = _combined_read(_step(text, "I2"))
    assert THROUGH_INTAKE in combined
    assert _flat(text).count(THROUGH_INTAKE) == 1
    # A `Ready:` row is read from the revision table, in these words, once.
    assert READY_ROW in combined
    assert _flat(text).count("`r{n}: Ready:`") == 1
    # The document stays unchanged: the one stop covers both messages, and it writes nothing.
    assert "write nothing" in combined and "WRITE" not in combined
    # Its contract validates as before: the read runs no command on it, and
    # the flow keeps its four.
    assert "python -m" not in combined
    assert set(re.findall(r"python -m taskcontract ([a-z-]+)", text)) == COMMANDS


def test_sc4_3_the_three_messages_stand_in_one_order_in_the_flow_and_on_the_usage_page():
    i2 = _step(_read(FLOW), "I2")
    _in_order(i2, NO_READY_ROW, THROUGH_INTAKE, NO_DESIGN)
    interview = _subsection(_section(4), "`/sdlc:product-specification-interview`")
    blocks = [block.strip() for block in re.split(r"\n[ \t]*\n", interview) if block.strip()]
    lead = [at for at, block in enumerate(blocks) if "**Intake takes the pair.**" in block]
    assert len(lead) == 1
    assert _flat(blocks[lead[0]]) == USAGE_TAKES_THE_PAIR
    # The fenced block right after it lists the three, one a line.
    assert blocks[lead[0] + 1].splitlines() == ["```", *USAGE_STOPS, "```"]
    assert _paragraph(interview, "A combined document is one that holds") == USAGE_COMBINED
    # The flow's two messages are the page's, with the path as a placeholder.
    for message, line in zip((NO_READY_ROW, THROUGH_INTAKE), USAGE_STOPS):
        assert message.strip("`").replace("{path}", "docs/features/x.md") == line


# --- the constraints that bind the unit's prompt files ---------------------------

def test_sc4_3_intake_with_the_two_stops_keeps_its_steps_commands_rows_tags_and_ceiling():
    text = _prompt_shape(FLOW)
    i2 = _step(text, "I2")
    _combined_read(i2)
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    # The nine steps keep their ids and their order: the roster stop, the read, the scaffold.
    assert re.findall(r"^(I\d+)\. ", text, re.MULTILINE) == [f"I{n}" for n in range(1, 10)]
    assert NO_ROSTER in _step(text, "I1") and SCAFFOLD in _step(text, "I3")
    # The word `Signed:` stands in I2 and I7 alone, and intake never writes one.
    assert ROWS_INTAKE_WRITES in i2
    for step in ("I1", "I3", "I4", "I5", "I6", "I8", "I9"):
        assert "Signed:" not in _step(text, step), step
    # Four commands and no fifth, each one segment.
    assert set(re.findall(r"python -m taskcontract ([a-z-]+)", text)) == COMMANDS
    commands = re.findall(r"`(python -m [^`]*)`", text)
    commands += re.findall(r"^\s+(python -m .*)$", text, re.MULTILINE)
    assert len(commands) == 4
    for command in commands:
        assert not re.search(r"[|;&<>]", command), command
    # The row words stay byte for byte.
    flat = _flat(text)
    for words in (PARKED, NOT_TEXT, READY_OPENS, READY_REQUIREMENTS, READY_DESIGN):
        assert words in flat, words
    assert I8_PARKED in _step(text, "I8")


# --- done_means: the stale message's two letters ---------------------------------

def test_done_means_intake_names_the_designs_revision_by_the_stale_messages_letter():
    text = _read(FLOW)
    stops = _part(_step(text, "I2"), "STOPS - ")
    assert INTAKE_NAMES in stops
    assert f"then {STALE}{INTAKE_GLOSS} When a case holds, STOP" in stops
    # The message keeps its words and its letters, and stands once.
    assert _flat(text).count(STALE) == 1 and _flat(text).count("Stale.") == 1
    assert OLD_LETTER not in _flat(text)


def test_done_means_e4_glosses_the_stale_messages_letters_and_the_seats_word_stays_last():
    text = _prompt_shape(SIGNING)
    e4 = _step(text, "E4")
    assert e4.endswith(f"REPORT {STALE}{E4_GLOSS} {WORD_STANDS}")
    assert _flat(text).count(STALE) == 1
    assert re.findall(r"^(E\d+)\. ", text, re.MULTILINE) == [f"E{n}" for n in range(1, 8)]
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "context",
                                                             "instructions"}


def test_done_means_design_confirm_names_the_requirements_revision_by_the_messages_letter():
    text = _prompt_shape(OPENING)
    confirm = _step(text, "DESIGN CONFIRM")
    assert f"The design names one requirements revision: {CONFIRM_NAMES};" in confirm
    assert OLD_LETTER not in _flat(text)
    # The SHOW and the row the step writes keep their words.
    assert ('SHOW "The design names requirements r{n}; the requirements stand at r{m}.", '
            "then the revisions between") in confirm
    assert "`r{n}: Confirmed against requirements r{m}`" in confirm


# --- done_means: a design run's opening, named in two places ---------------------

def test_done_means_the_openings_purpose_says_where_a_design_run_opens():
    text = _prompt_shape(OPENING)
    purpose = _flat(text[text.index("<purpose>"):text.index("</purpose>")])
    _in_order(purpose, f"{PURPOSE_CLOSE} {PURPOSE_DESIGN} Dispatched by")
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    # The steps the sentence names stand in the flow, in its order.
    labels = re.findall(r"^(DESIGN READ|DESIGN CONFIRM|O\d)(?:\.| -) ", text, re.MULTILINE)
    assert labels == ["DESIGN READ", "DESIGN CONFIRM"] + [f"O{n}" for n in range(1, 7)]


def test_done_means_the_interviews_file_list_names_design_read_and_design_confirm():
    text = _prompt_shape(INTERVIEW_SKILL)
    lines = [_flat(line) for line in text.splitlines()
             if line.strip().startswith("{skill-dir}/flows/opening.md")]
    assert lines == [OPENING_LINE]
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {
        "purpose", "variables", "context", "instructions", "constraints", "criteria"}


# --- done_means: the tree's docstring --------------------------------------------

def test_done_means_the_trees_docstring_says_no_valid_contracts_document_ends_design_md():
    text = _read(TREE)
    first = ast.parse(text).body[0]
    docstring = _flat(ast.get_docstring(ast.parse(text), clean=False) or "")
    _in_order(docstring, f"{BESIDE} {NO_DOT} The tree prints none of their other words")
    # One sentence of the docstring and no code: every line below it stands as it stood.
    code = "\n".join(text.split("\n")[first.end_lineno:])
    assert hashlib.sha256(code.encode("utf-8")).hexdigest() == TREE_CODE


# --- done_means: kit 0.19.0 ------------------------------------------------------

def test_done_means_the_kit_version_reads_0_19_0_or_later_and_both_places_agree():
    # a floor, never the literal: the next release moves both numbers
    project = _version(PYPROJECT, r'^version\s*=\s*"(\d+\.\d+\.\d+)"')
    kit = _version(INIT, r'^KIT_VERSION\s*=\s*"(\d+\.\d+\.\d+)"')
    assert project >= (0, 19, 0)
    assert kit == project


# --- done_means: USAGE reads green -----------------------------------------------

def test_done_means_usage_shows_the_interview_shipped_under_the_kit_0_19_0_banner():
    four = _section(4)
    assert INTERVIEW_HEADING in [line.rstrip() for line in four.splitlines()]
    interview = _subsection(four, "`/sdlc:product-specification-interview`")
    assert _banner(interview) == INTERVIEW_BANNER
    # Its paragraphs read green, each lead as it stood.
    for lead in ("**What it writes.**", "**Intake takes the pair.**",
                 "**Intake's refusals**", "**Next step:**"):
        assert _paragraph(interview, lead).startswith(f"{GREEN} {lead}"), lead
    assert RED not in interview


def test_done_means_usage_section_9_shows_a_pair_of_documents_green_under_the_sections_banner():
    nine = _section(9)
    banner = _banner(nine)
    for name in ("kit 0.19.0", "ADR 0037", "contract `specs/document-split/`",
                 '"A pair of documents"'):
        assert name in banner, name
    assert banner.endswith(SECTION_9_BANNER_END)
    assert f"### A pair of documents {GREEN}" in [line.rstrip() for line in nine.splitlines()]
    pair = _subsection(nine, "A pair of documents")
    # The subsection's own banner is gone, and each paragraph reads green.
    assert not [line for line in pair.splitlines() if line.startswith(">")]
    assert "Ratified, not shipped" not in pair
    opened = [block for block in _paragraphs(pair) if block.startswith(GREEN)]
    assert len(opened) == len(PAIR_PARAGRAPHS)
    for block, opening in zip(opened, PAIR_PARAGRAPHS):
        assert block.startswith(opening), opening


def test_done_means_usage_names_a_design_document_as_no_feature_before_intake():
    before = _subsection(_section(9), "Features before intake")
    assert _paragraph(before, "shows as a feature at the first level") == BEFORE_INTAKE


def test_done_means_usage_says_intake_adds_a_ready_row_to_each_documents_table():
    drift = _subsection(_section(9), "Drift from the feature document")
    assert _paragraph(drift, "When the request is a feature document") == READY_ROW_PARAGRAPH
    assert "intake adds one row to its revision table" not in _flat(_read(USAGE))


def test_done_means_usage_says_intake_writes_a_parked_row_in_each_table_of_a_pair():
    parked = _subsection(_section(9), "A parked document")
    assert _paragraphs(parked)[1] == PARKED_PARAGRAPH
    assert "when it parks a document" not in _flat(_read(USAGE))


# --- done_means: the changelog, the map and the G0 page --------------------------

def test_done_means_the_changelog_names_release_0_19_0_above_0_18_0_with_its_six_units():
    text = _read(CHANGELOG)
    headings = [line.rstrip() for line in text.splitlines() if line.startswith("## ")]
    assert RELEASE_HEADING in headings
    below = headings[headings.index(RELEASE_HEADING) + 1:]
    assert below and below[0].startswith("## 0.18.0 ")
    # the entry's own body, up to the next release's heading
    entry = _flat(_cut(text, RELEASE_HEADING, r"^## "))
    for unit in UNITS:
        assert f"unit `{unit}`" in entry, unit
    _in_order(entry, *UNITS)
    for name in ("(`document-split`, ADR 0037, unit `d1-requirements`)",
                 "`requirements-document.md.template` and `design-document.md.template`",
                 "`/sdlc:product-specification-interview <id> design`",
                 "ready check 15 reads the four cases",
                 "a feature with no design document prints as 0.18.0 prints it.",
                 "intake stops with `No design document for {id}. Run the design interview "
                 "first.` where no design document stands.",
                 "Intake stops, with nothing written, on a combined document: one message "
                 "for a document with no `Ready:` row, one for a document through intake, "
                 "whose contract stands.",
                 "`USAGE.md` reads green throughout.",
                 "Kit `0.18.0` -> `0.19.0`; the contract schema stays at `1.5.0`.",
                 "Delta note: a combined document with no `Ready:` row is split by hand "
                 "into a pair before intake; pin the install ref to the tag."):
        assert name in entry, name


def test_done_means_the_maps_intake_row_reads_a_pair_and_stops_on_a_combined_document():
    assert _map_row("raw-request intake") == MAP_INTAKE


def test_done_means_the_maps_interview_row_names_each_run_its_document_and_its_seat():
    assert _map_row("specification interview") == MAP_INTERVIEW


def test_done_means_the_maps_tree_row_shows_a_pair_as_one_feature_with_a_second_mark():
    row = _map_row("work tree")
    assert MAP_TREE in row
    assert row.endswith(f", {ADR_0037} |")
    assert row.count("](decisions/0037-") == 1


def test_done_means_the_g0_pages_title_row_names_the_requirements_documents_title_line():
    rows = [line for line in _read(G0_PAGE).splitlines() if line.startswith("| `title` |")]
    assert len(rows) == 1
    assert TITLE_SOURCE in rows[0]
    assert OLD_TITLE_SOURCE not in _flat(_read(G0_PAGE))
