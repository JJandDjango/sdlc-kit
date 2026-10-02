"""The 0.18.0 release, structurally (contract: feature-document, unit
f5-release). The unit ships documents and prompt text, so the pages are
the behavior: the suite holds USAGE's interview section green under its
`Shipped` banner, what the section says of the format, the Gherkin step,
the checks before signing, the signatures and intake's refusals, the
green paragraphs of sections 8 and 9, the page's two legend lines, the
changelog entry, the map row, and the two skills' sentences on what
intake writes and on the count of sections.

Every sentence is searched with its whitespace folded and its quote marks
dropped, so a page may wrap its lines. A section is cut by its heading,
never by a line number. SC5.1 is a manual receipt taken after the tag and
has no test here.
"""

from __future__ import annotations

import re
from pathlib import Path

_HERE = Path(__file__).resolve().parent.parent
# Beside a tree that holds the skill, read that tree; a copy run from any
# other folder reads the tree pytest was started in.
ROOT = _HERE if (_HERE / "skills" / "sdlc").is_dir() else Path.cwd()
USAGE = ROOT / "USAGE.md"
CHANGELOG = ROOT / "CHANGELOG.md"
MAP = ROOT / "MAP.md"
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "skills" / "sdlc" / "init.py"
SDLC_SKILL = ROOT / "skills" / "sdlc" / "SKILL.md"
INTERVIEW_SKILL = ROOT / "skills" / "product-specification-interview" / "SKILL.md"
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token

GREEN = "\U0001F7E2"
RED = "\U0001F534"
DOT = "·"

INTERVIEW_HEADING = "### `/sdlc:product-specification-interview`"
BANNER = (f"{GREEN} **Shipped** (kit 0.18.0, "
          "[ADR 0029](decisions/0029-feature-document-format-and-done.md) "
          "as ADRs 0033 to 0036 amend it, contract `specs/feature-document/`).")
COUNT = ("The table, the title line and the status line are the first three of "
         "ADR 0029's eighteen sections. The other fifteen follow in order, each "
         "heading followed by its tag")
REFUSALS = ("Check {id} is assigned to no unit.",
            "Check {id} is assigned to units {a} and {b}.",
            "Unit {id} delivers no check.",
            "r{n}: Parked: {what stands}",
            "Ready check {n}: {gap}. Marked OPEN.")
PARKS = ("A refusal parks the document: intake writes one row, "
         "`r{n}: Parked: {what stands}`, that names every thing that stands, "
         "and no contract.")
SIGNATURE_STOP = ("Intake reads the signatures only when nothing stands. A half with "
                  "no `Signed:` row, or a text row newer than the newest revision both "
                  "seats signed, stops intake before any contract and writes no row: "
                  "the seat signs through the interview, and intake runs again.")
SECTION_8 = (f"{GREEN} When the raw request is a feature document, intake reads the "
             "three from its Scope, Order and Units sections and asks the engineer "
             "seat to keep or change them.")
RELEASE_HEADING = "## 0.18.0 - 2026-10-02 (tag `v0.18.0`)"
STRATA_EXCEPTION = ("One exception: intake adds its `Ready:` or `Parked:` row to a "
                    "feature document's revision table at `docs/features/{id}.md`.")
INTAKE_WRITES = ("- intake writes ONLY `specs/{id}/contract.yaml` and, for a feature "
                 "document, one `Ready:` or `Parked:` row in its revision table; a "
                 "parked document gets no contract, and a red contract never hands "
                 "off to development.")
INTAKE_CRITERION = ("handoff refused while red; a feature document read before the "
                    "scaffold: parked with one `Parked:` row and no contract while a "
                    "refusal stands, stopped with no row and no contract while a "
                    "signature is missing, and given its `Ready:` row only once the "
                    "contract validates ready-green; nothing else written.")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """The text on one line: quote marks dropped, whitespace folded."""
    return " ".join(re.sub(r"^>", "", text, flags=re.MULTILINE).split())


def _cut(text: str, opening: str, stop: str) -> str:
    """The part of a page from the heading that opens on `opening` up to
    the next line that matches `stop`, or to the end of the page."""
    start = re.search(rf"^{re.escape(opening)}", text, re.MULTILINE)
    assert start, f"the page has no heading that opens {opening!r}"
    end = re.compile(stop, re.MULTILINE).search(text, start.end())
    return text[start.start():end.start() if end else len(text)]


def _interview() -> str:
    """USAGE's interview section: its heading up to the next `###` heading."""
    return _cut(_read(USAGE), INTERVIEW_HEADING, r"^### ")


def _section(number: int) -> str:
    """One numbered section of USAGE, up to the next numbered section."""
    return _cut(_read(USAGE), f"## {number}. ", r"^## \d+\. ")


def _subsection(section: str, name: str) -> str:
    return _cut(section, f"### {name}", r"^### ")


def _paragraphs(text: str) -> list[str]:
    """The blocks a blank line parts, each with its whitespace folded."""
    return [_flat(block) for block in re.split(r"\n[ \t]*\n", text) if block.strip()]


def _paragraph(text: str, needle: str) -> str:
    """The first paragraph of the text that holds the needle."""
    found = [block for block in _paragraphs(text) if needle in block]
    assert found, f"no paragraph holds {needle!r}"
    return found[0]


def _opens_green(text: str, needle: str) -> None:
    """The paragraph that holds the needle opens on the green mark."""
    paragraph = _paragraph(text, needle)
    assert paragraph.startswith(GREEN + " "), (
        f"the paragraph that holds {needle!r} opens {paragraph[:40]!r}, not on the green mark")


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
    return _flat("\n".join(quote))


def _item(text: str, opening: str) -> str:
    """One list item of a prompt file, whitespace folded: from its opening
    to the next line that opens an item or a tag."""
    start = text.find("\n" + opening)
    assert start >= 0, f"no item opens {opening!r}"
    end = re.compile(r"^(- |<)", re.MULTILINE).search(text, start + 1 + len(opening))
    return _flat(text[start:end.start() if end else len(text)])


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


# --- done_means: kit 0.18.0 ships the interview ----------------------------------

def test_done_means_the_kit_version_is_0_18_0_or_later():
    # a floor, never the literal: the next release moves both numbers
    assert _version(PYPROJECT, r'^version\s*=\s*"(\d+\.\d+\.\d+)"') >= (0, 18, 0)
    assert _version(INIT, r'^KIT_VERSION\s*=\s*"(\d+\.\d+\.\d+)"') >= (0, 18, 0)


# --- SC5.2: USAGE's interview section --------------------------------------------

def test_sc5_2_the_interview_section_is_green_under_its_shipped_banner():
    section = _interview()
    assert section.splitlines()[0].rstrip().endswith(" " + GREEN)
    assert RED not in section
    assert _banner(section) == BANNER
    flat = _flat(section)
    assert "Ratified, not shipped" not in flat
    assert "Until then" not in flat


def test_sc5_2_the_section_covers_the_format_and_counts_fifteen_sections_after_three():
    section = _interview()
    flat = _flat(section)
    for name in ("`docs/features/<id>.md`", "`docs/features/<id>.state.yaml`",
                 "`# <id> - <title>`", "seat boundary", f"`[PO seat {DOT} authored]`"):
        assert name in flat
    assert COUNT in flat
    assert "The eighteen sections of ADR 0029 follow in order" not in flat
    _opens_green(section, "The other fifteen follow in order")
    _opens_green(section, "`docs/features/<id>.state.yaml`")


def test_sc5_2_the_section_covers_the_gherkin_step_the_po_seat_accepts_changes_or_drops():
    section = _interview()
    flat = _flat(section)
    assert "one scenario per check" in flat
    assert "the PO seat accepts, changes or drops each" in flat
    assert "edits or drops" not in flat
    _opens_green(section, "accepts, changes or drops each")


def test_sc5_2_the_section_covers_the_checks_before_signing_and_both_signatures():
    section = _interview()
    flat = _flat(section)
    assert "lang-check --draft" in flat
    for name in ("`CL014`", "1 to 8 for the request half and 11 to 14 for the solution half",
                 "`Measured:` row"):
        assert name in flat
        _opens_green(section, name)
    for half in ("`rN: Signed: request half`", "`rN: Signed: solution half`"):
        assert half in flat
        _opens_green(section, half)


def test_sc5_2_the_section_covers_each_error_intake_rejects_with_and_the_park():
    section = _interview()
    flat = _flat(section)
    for message in REFUSALS:
        assert message in flat
    # the refusal paragraph: one row that names every thing that stands
    refusal = _paragraph(section, "A refusal parks the document:")
    assert refusal.startswith(f"{GREEN} {PARKS}")
    # the signature stop: after the three messages, never after "On ready"
    _in_order(flat, "Unit {id} delivers no check.", SIGNATURE_STOP)
    stop = _paragraph(section, SIGNATURE_STOP)
    assert stop.startswith(GREEN + " ")
    before, _, after = stop.partition(SIGNATURE_STOP)
    assert "On ready" not in before
    assert "A refusal parks the document:" not in after
    _opens_green(section, "`Ready check {n}: {gap}. Marked OPEN.`")


# --- SC5.2: the rest of USAGE ----------------------------------------------------

def test_sc5_2_section_8_asks_the_engineer_seat_to_keep_or_change_the_three():
    paragraph = _paragraph(_section(8), "When the raw request is a feature document")
    assert paragraph == SECTION_8
    assert "asks the seats to keep or change them" not in _flat(_read(USAGE))


def test_sc5_2_section_9_shows_a_parked_document_green_and_counts_no_parked_row():
    nine = _section(9)
    banner = _banner(nine)
    for name in ("kit 0.18.0", "ADR 0036", "contract `specs/feature-document/`"):
        assert name in banner
    assert f"### A parked document {GREEN}" in [line.rstrip() for line in nine.splitlines()]
    assert _paragraphs(_subsection(nine, "A parked document"))[1].startswith(GREEN + " ")
    # the drift mark's document revision leaves out the four kinds of row
    drift = _flat(_subsection(nine, "Drift from the feature document"))
    assert "The **document's revision**" in drift and "The **contract's revision**" in drift
    bullet = drift[drift.index("The **document's revision**"):
                   drift.index("The **contract's revision**")]
    _in_order(bullet, "is the highest `rN` of a row that is none of a `Ready:` row",
              "a `Measured:` row", "a `Signed:` row", "or a `Parked:` row (`rN: Parked:`)")
    assert "or a `Signed:` row" not in bullet
    halves = _flat(_subsection(nine, "Revisions and halves"))
    assert "opens on none of `Ready:`, `Measured:`, `Signed:` or `Parked:`" in halves
    assert "opens on none of `Ready:`, `Measured:` or `Signed:`" not in halves


def test_sc5_2_usage_holds_the_red_mark_only_in_its_two_legend_lines():
    reds = [line for line in _read(USAGE).splitlines() if RED in line]
    assert len(reds) == 2, f"{len(reds)} lines hold the red mark"
    assert "Sections marked" in reds[0]
    assert reds[1].startswith("SDLC.md")


# --- SC5.2: the changelog, the map and the skills --------------------------------

def test_sc5_2_the_changelog_names_release_0_18_0_above_0_17_0_with_its_five_units():
    text = _read(CHANGELOG)
    headings = [line.rstrip() for line in text.splitlines() if line.startswith("## ")]
    assert RELEASE_HEADING in headings
    below = headings[headings.index(RELEASE_HEADING) + 1:]
    assert below and below[0].startswith("## 0.17.0 ")
    # the entry's own body, up to the next release's heading
    entry = _flat(_cut(text, RELEASE_HEADING, r"^## "))
    for name in ("`feature-document`", "f1-format", "f2-sections", "f3-signing",
                 "f4-intake", "f5-release", "lang-check --draft", "`CL014`",
                 "`Parked:` row",
                 "Kit `0.17.0` -> `0.18.0`; the contract schema stays at `1.5.0`."):
        assert name in entry


def test_sc5_2_the_map_row_names_the_document_its_signed_and_parked_rows_and_four_adrs():
    rows = [line for line in _read(MAP).splitlines()
            if line.startswith("| specification interview |")]
    assert len(rows) == 1
    row = rows[0]
    for name in ("`docs/features/<id>.md`", "`Signed:` row", "`Parked:` row"):
        assert name in row
    for adr in ("0028", "0029", "0033", "0036"):
        assert re.search(rf"\]\(decisions/{adr}-[a-z0-9-]+\.md\)", row), (
            f"the row links no decisions/{adr}")
    assert "an advisory readiness check" not in row


def test_sc5_2_the_sdlc_skill_says_intake_writes_its_row_into_the_feature_document():
    text = _read(SDLC_SKILL)
    assert _item(text, "- Do NOT touch Cairn strata").endswith(
        "never write on its behalf. " + STRATA_EXCEPTION)
    assert _item(text, "- intake writes ONLY") == INTAKE_WRITES
    assert _item(text, "- [ ] Intake flow:").endswith(INTAKE_CRITERION)
    assert len(text) < CHAR_CEILING


def test_sc5_2_the_interview_skill_counts_the_other_fifteen_of_the_eighteen_sections():
    flat = _flat(_read(INTERVIEW_SKILL))
    assert "the status line; then the other fifteen of the eighteen sections" in flat
    assert "then eighteen sections" not in flat
