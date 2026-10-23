"""Kit 0.20.0 ships G1 (contract: g1-requirements-spec, unit s6-release).

The unit changes no code of the package. The text is the behavior: the two
version numbers, the changelog entry, USAGE read green, the kit's own
`.sdlc/config.yaml` with its `g1` key, `.spectral.yaml`, `specs/components.yaml`
and the pages that name G1 as shipped. What those files make the kit do is
read through the CLI, run with the root as its working directory: the kit's
own tree shows G1 as an active gate, and SC4.3, that a contract's G0
verdict still reads as the validator reports it, holds on a fixture with one
contract in each state and on the kit's own contracts.

A sentence is matched with each whitespace run folded to one space and a
page's quote marks dropped, so a file may wrap its lines; a section is cut by
its heading, never by a line number. A sentence of a docs page that holds a
code span is matched with its backticks dropped from both sides, so the page
may code-span a word or leave it plain.

Two receipts stay manual and no test runs a tool or installs a package: the
install from the tag reads 0.20.0, and Spectral lints the kit's schemas under
`.spectral.yaml`.
"""

from __future__ import annotations

import datetime
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from conftest import usage_text, write_seat_roster

_HERE = Path(__file__).resolve().parent.parent
# Beside a tree that holds the skill, read that tree; a copy run from any
# other folder reads the tree pytest was started in.
ROOT = _HERE if (_HERE / "skills" / "sdlc").is_dir() else Path.cwd()
USAGE = ROOT / "USAGE.md"
CHANGELOG = ROOT / "CHANGELOG.md"
SDLC = ROOT / "SDLC.md"
SDLC_TEMPLATE = ROOT / "skills" / "sdlc" / "templates" / "SDLC.md.template"
CONFIG_TEMPLATE = ROOT / "skills" / "sdlc" / "templates" / "config.yaml.template"
WORKFLOW_TEMPLATE = ROOT / "skills" / "sdlc" / "templates" / "workflow.yml.template"
CI = ROOT / ".github" / "workflows" / "ci.yml"
CONFIG = ROOT / ".sdlc" / "config.yaml"
SPECTRAL = ROOT / ".spectral.yaml"
COMPONENTS = ROOT / "specs" / "components.yaml"
COMPONENT_SCHEMA = ROOT / "taskcontract" / "schemas" / "component-declaration.schema.json"
SCHEMAS = ROOT / "taskcontract" / "schemas"
GATES_PAGE = ROOT / "docs" / "gates.md"
G1_PAGE = ROOT / "docs" / "gates" / "G1-requirements-spec.md"
OPERATORS = ROOT / "docs" / "operators.md"
COMPONENT_ROWS = ROOT / "docs" / "components.md"
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "skills" / "sdlc" / "init.py"

GREEN = chr(0x1F7E2)
RED = chr(0x1F534)
WHITE = chr(0x26AA)

ADR_0038 = "decisions/0038-a-gate-refuses-a-task-and-g1-records-and-declarations-have-homes.md"

EXEMPT = (
    "controlled-language", "distribution-reconciliation", "document-split",
    "dotnet-profile-g0", "dotnet-profile-g3", "dotnet-profile-g4", "feature-document",
    "g0-declaration", "g1-requirements-spec", "intake-seats", "operator-layer",
    "pane-view", "playbook-guardrails", "project-tree", "spec-interview",
    "tree-first-level", "tree-view", "unit-dag", "vocabulary-layer",
)
NOT_EXEMPT = "glossary-alias-disjointness"
G1_TITLE = "Requirements / Spec"

# --- the changelog ---------------------------------------------------------------

RELEASE_HEADING = re.compile(r"^## 0\.20\.0 - (\d{4}-\d{2}-\d{2}) \(tag `v0\.20\.0`\)$")
BULLETS = (
    ("G1.1 reads the linter's record",
     "(`g1-requirements-spec`, ADR 0038, unit `s1-lint`)", "s1-lint",
     ("`python -m taskcontract g1-record lint <id>`", "`g1.schemas`", "`g1-check <id>`",
      "G1.1 reads `done` when the record shows each schema clean under its pin, and "
      "`to do` where the contract's scope cannot be read.",
      "Delta note: the kit ships no linter; install one and commit its pin.")),
    ("G1.2 reads the model checker's record",
     "(`g1-requirements-spec`, unit `s2-model`)", "s2-model",
     ("`g1-record model <id>`", "`specs/components.yaml`",
      "`taskcontract/schemas/component-declaration.schema.json` at version 1.0.0",
      "Delta note: the kit ships no checker; install TLC or P, and a person writes "
      "`specs/components.yaml`.")),
    ("A person signs G1.3 at the venue",
     "(`g1-requirements-spec`, unit `s3-review`)", "s3-review",
     ("`/sdlc g1 <id>`", "`g1-record review`", "each of G1.3's 11 items, one at a time",
      "Delta note: an agent never answers an item.")),
    ("The tree shows G1",
     "(`g1-requirements-spec`, unit `s4-tree`)", "s4-tree",
     ("`.sdlc/g1`", "`g1.exempt`",
      "Delta note: a feature the `g1.exempt` list names, and a repository with `G1` absent "
      "from `active_gates`, print as 0.19.0 prints them.")),
    ("No task starts before G1 passes",
     "(`g1-requirements-spec`, ADR 0038, unit `s5-start`)", "s5-start",
     ("`Next step: G1. Run /sdlc g1 {id}.`",
      "`progress start` and `progress done` refuse while G1 does not read `done`, with "
      "exit 2 and one line on stderr; `block` and `run` stay open.",
      "Delta note: ADR 0038 amends ADR 0031's \"shown and never enforced\" for this "
      "refusal.")),
    ("G1 is on at the kit and written down",
     "(`g1-requirements-spec`, unit `s6-release`)", "s6-release",
     ("`.sdlc/config.yaml` lists `G1` and holds the `g1` key",
      "`taskcontract/schemas/*.json` lint under `.spectral.yaml`.",
      "`specs/components.yaml` declares no component.",
      "`USAGE.md` reads green throughout.",
      "Kit `0.19.0` -> `0.20.0`; the contract schema stays at `1.5.0`.",
      "Delta note: a repository born from `/sdlc init` keeps G0 alone; to turn G1 on, list "
      "`G1` under `active_gates`, write the `g1` key and `specs/components.yaml`, and pin "
      "the install ref to the tag.")),
)

# --- USAGE -----------------------------------------------------------------------

G1_VENUE = "`/sdlc g1`: the G1 venue"
G1_GATE = "G1 as an active gate"
VENUE_BANNER = (
    f"{GREEN} **Shipped** (kit 0.20.0, contract `specs/g1-requirements-spec/`, "
    f"[ADR 0038](../../{ADR_0038})). A kit before 0.20.0 has no G1: it has no `g1-check`, no "
    "`g1-record` and no `/sdlc g1`.")
GATE_BANNER = (
    f"{GREEN} **Shipped** (kit 0.20.0, contract `specs/g1-requirements-spec/`, "
    f"[ADR 0038](../../{ADR_0038})). A repository that does not list `G1` under `active_gates` "
    "reads the subsections above as they read.")
VENUE_LEADS = 22   # the paragraphs of the venue subsection that opened on a red mark
GATE_LEADS = 12    # the same for the active-gate subsection

DONE_TAKES = ("taskcontract progress: '{id}' is a {kind}, not a task, unit or contract - done "
              "takes a task, unit or contract id")
G1_REFUSED = "{unit} cannot start: G1 has not passed for {feature}"
G1_LINE_PARAGRAPH = (
    f"{GREEN} The G1 line stands for `start` on a task and `done` on a task, a unit or a "
    "contract, while G1 is an active gate for the feature and does not read `done` "
    "(§9, \"G1 as an active gate\"). On a contract's close `{unit}` is the feature's id.")

BEFORE_INTAKE_PARAGRAPH = (
    f"{GREEN} A feature before intake rolls up its verdicts, but not the inactive one, and "
    "its halves: it reads `to do` until a seat signs a half, then `doing`. A feature before "
    "intake with its request half signed and its design document at r1 "
    "(\"A pair of documents\"):")
DRAWING = [
    "apply-discount Apply one discount code per order [doing] no contract: document r3 "
    "design r1 doc: docs/features/apply-discount.md",
    "  apply-discount/G0 Planning / Intake [to do]",
    "    apply-discount/G0/G0.1 Definition-of-ready [to do]",
    "    apply-discount/G0/G0.2 Vocabulary coverage [to do]",
    "    apply-discount/G0/G0.3 Unit confirmation [to do]",
    "  apply-discount/G1 Requirements / Spec [to do] inactive",
    "    apply-discount/G1/G1.1 Spec/schema linting [to do]",
    "    apply-discount/G1/G1.2 Model checking [to do]",
    "    apply-discount/G1/G1.3 Criteria completeness + ambiguity review [to do]",
    "  apply-discount/request Request half [done] by user at r3",
    "  apply-discount/solution Solution half [to do]",
]
HALF_DRAWING = [
    "apply-discount/request Request half [done] by user at r3",
    "file: docs/features/apply-discount.md:6",
]
RECORD_SENTENCE = ("The Record reads \"(none: intake writes the record)\" and keeps that line: "
                   "kit 0.20.0 has no step that writes the Record.")

# --- the pages -------------------------------------------------------------------

SDLC_G0 = (f"| G0 planning/intake | contract exists and validates `ready` | {GREEN} CI backstop "
           "live; venue live once `/sdlc intake` is in use |")
SDLC_G1 = ("| G1 requirements/spec | boundary schemas lint clean, hard cores model-check, a "
           f"named person signs the review | {GREEN} live here since kit 0.20.0: `/sdlc g1` is "
           "the venue, and `progress` refuses a task until G1 passes |")
SDLC_G1_OFF = ("| G1 requirements/spec | boundary schemas lint clean, hard cores model-check, a "
               f"named person signs the review | {RED} not live here - kit 0.20.0 ships it; "
               "list `G1` under `active_gates` in `.sdlc/config.yaml` to turn it on |")
SDLC_REST = (f"| G2-G10 + PL-DOC + PL-PIPE | see the kit registry | {RED} aspirational - "
             "enforcement lands via the kit's activation program |")

GATES_OLD = ("G1.2's designation criteria ratified in "
             "[0007](../decisions/0007-hard-core-designation-criteria.md).")
GATES_NEW = (f"Enforcement shipped in kit 0.20.0 ([0038](../{ADR_0038})): the venue is "
             "/sdlc g1, and enforced flips per target at first live use, here with the "
             "0.20.0 release.")

G1_PAGE_LIFECYCLES = (
    ("### G1.1 Spec/schema linting",
     "**Lifecycle:** specified (strictness ratified 2026-07-23); enforced here since kit "
     "0.20.0."),
    ("### G1.2 Model checking",
     "**Lifecycle:** specified (designation criteria ratified 2026-07-23, "
     "[0007](../../decisions/0007-hard-core-designation-criteria.md)); enforced here since "
     "kit 0.20.0."),
    ("### G1.3 Criteria completeness + ambiguity review",
     "**Lifecycle:** specified (checklist ratified 2026-07-23); enforced here since kit "
     "0.20.0."),
)
G12_PARAMETERS = (
    "Procedure-bound like G1.1's pinned rulesets; the per-component set is decided at spec "
    "time and recorded in specs/components.yaml "
    f"([0038](../../{ADR_0038})).")
G13_TOOLING = (
    "**Tooling:** the review checklist (specified below); the operational artifact is the "
    "signed review in .sdlc/g1/<id>.yaml, written by g1-record review at the venue /sdlc g1 "
    f"([0038](../../{ADR_0038})).")

SPEC_AGENT_STATUS = (f"| {WHITE} registered - ships at the first bound G2 authoring surface; "
                     "/sdlc intake and /sdlc g1 are the live flows today |")
VENUE_MAP_G1 = ("| G1 requirements | sdlc-spec authors; G1.3 human | conversation flow + human "
                f"sign-off | {GREEN} venue live (/sdlc g1, kit 0.20.0, [0038](../{ADR_0038})); "
                "def registered |")
DEFERRED = ("**sdlc-spec def** - trigger: first bound G2 authoring surface (/sdlc intake "
            "carries G0 live and /sdlc g1 carries G1: a person signs each, so neither is an "
            "agent's authoring surface).")
COMPONENT_ROW = (
    "| G1 gate | The requirements and spec gate, active by feature: three conditions, each "
    "read from a committed record (`g1-record lint`, `model` and `review` write them; "
    "`g1-check` and the tree read them), two declarations a person writes (`g1.schemas` and "
    "`g1.exempt` in `.sdlc/config.yaml`, and `specs/components.yaml`), the venue `/sdlc g1`, "
    "and the `progress` refusal while G1 is active and has not passed | implemented (v1) | "
    f"[decisions/0038](../{ADR_0038}), "
    "[docs/gates/G1-requirements-spec.md](gates/G1-requirements-spec.md) |")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """The text with each whitespace run folded to one space."""
    return " ".join(text.split())


def _unquoted(text: str) -> str:
    """A page's text on one line: its quote marks dropped, whitespace folded."""
    return _flat(re.sub(r"^>", "", text, flags=re.MULTILINE))


def _plain(text: str) -> str:
    """A docs page's text on one line, its quote marks and its backticks dropped."""
    return _unquoted(text).replace("`", "")


def _cut(text: str, opening: str, stop: str) -> str:
    """The part of a page from the heading that opens on `opening` up to
    the next line that matches `stop`, or to the end of the page."""
    start = re.search(rf"^{re.escape(opening)}", text, re.MULTILINE)
    assert start, f"the page has no heading that opens {opening!r}"
    end = re.compile(stop, re.MULTILINE).search(text, start.end())
    return text[start.start():end.start() if end else len(text)]


def _section(number: int) -> str:
    """One numbered section of USAGE, up to the next numbered section."""
    return _cut(usage_text(USAGE), f"## {number}. ", r"^## \d+\. ")


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


def _prose(text: str) -> list[str]:
    """The paragraphs of running prose: no code block, banner, heading, table
    or list."""
    bare = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    blocks = [block.strip() for block in re.split(r"\n[ \t]*\n", bare) if block.strip()]
    return [_unquoted(block) for block in blocks if block[0] not in ">#|-"]


def _fences(text: str) -> list[list[str]]:
    """The lines of each fenced code block of the text."""
    return [body.splitlines() for body in re.findall(r"```[^\n]*\n(.*?)```", text,
                                                      flags=re.DOTALL)]


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


def _yaml(path: Path):
    assert path.is_file(), f"{path.relative_to(ROOT)} is not there"
    return yaml.safe_load(_read(path))


def _env(**more) -> dict:
    env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    env.update(COLUMNS="500", PYTHONIOENCODING="utf-8", PYTHONUTF8="1", **more)
    return env


def _cli(*argv, env: dict | None = None) -> subprocess.CompletedProcess:
    """`python -m taskcontract` run with the root as its working directory, so
    the code that runs is the root's."""
    return subprocess.run([sys.executable, "-m", "taskcontract", *map(str, argv)],
                          cwd=ROOT, env=env or _env(), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=500)


def _g1_is_on() -> None:
    """The release's own precondition: the kit's config lists G1."""
    config = _yaml(CONFIG)
    assert "G1" in (config.get("active_gates") or []), "G1 is not an active gate of the kit"


# --- the fixture repositories ----------------------------------------------------

INTENT = ("A fixture contract for the G1 release suite; its one unit carries one "
          "sketch line.")
BLOCKED_DEPENDENCY = [{"ref": "vendor-feed", "status": "blocked", "blocked_by": "the vendor feed"}]


def _unit(uid="u1-work", confirmed=True):
    unit = {"unit": "work for " + uid, "id": uid,
            "done_means": "the work for " + uid + " is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}
    if confirmed:
        unit["confirmed_by"] = ["user"]
    return unit


def _contract(cid, **fields):
    """A contract that reads ready-green, with each given field changed."""
    doc = {"id": cid, "intent": INTENT, "scope": ["src/"], "non_goals": ["No other work"],
           "decomposition": [_unit()], "dependencies": [], "entities": [],
           "provenance": {"origin": "human-request"}}
    doc.update(fields)
    return doc


def _dump(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _fixture(root: Path, gates) -> Path:
    """One contract in each G0 state under `root`, with the given gates active."""
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates)})
    write_seat_roster(root)
    _dump(root / "specs" / "vocabulary" / "discount-code.yaml", {
        "term": "discount-code", "name": "Discount code",
        "definition": "A fixture term for the G1 release suite.", "kind": "entity",
        "status": "draft", "since": "2026-01-01"})
    contracts = {
        "ready": _contract("ready"),                                                 # ready-green
        "parked": _contract("parked", dependencies=BLOCKED_DEPENDENCY),              # TC003
        "drafted": _contract("drafted", entities=["discount-code"]),                 # TC011
        "short": _contract("short", intent="Too short."),                            # draft-red
        "mixed": _contract("mixed", intent="Too short.", dependencies=BLOCKED_DEPENDENCY),
    }
    for cid, doc in contracts.items():
        _dump(root / "specs" / cid / "contract.yaml", doc)
    return root


STATES = {"ready": "done", "parked": "blocked", "drafted": "to do", "short": "failed",
          "mixed": "failed"}


def _g0_verdict(root: Path, cid: str) -> str:
    """The verdict the validator's report gives: done at ready-green, else
    failed when draft-red, else blocked when TC003 is among the ready errors,
    else to do."""
    path = root / "specs" / cid / "contract.yaml"
    ready = _validate(path, "ready")
    if not ready:
        return "done"
    if _validate(path, "draft"):
        return "failed"
    return "blocked" if "TC003" in ready else "to do"


def _validate(path: Path, profile: str) -> list[str]:
    """The rule codes of the errors `validate <path> --profile <profile>` reports."""
    done = _cli("validate", path, "--profile", profile, "--json")
    found = json.loads(done.stdout)
    errors = [item["rule"] for item in found if item.get("severity", "error") == "error"]
    assert (done.returncode == 0) == (not errors), (path, profile, done.returncode, errors)
    return errors


def _tree(root: Path, **env) -> list[str]:
    done = _cli("tree", "--root", root, env=_env(**env))
    assert done.returncode == 0, done.stderr
    return done.stdout.splitlines()


def _tag(lines: list[str], item: str, name: str) -> str:
    """The status of the item line `<item> <name> [status]`, its indent dropped."""
    found = [line for line in lines
             if re.match(rf"^ *{re.escape(item)} {re.escape(name)} \[", line)]
    assert len(found) == 1, (item, found)
    return re.match(r"^ *\S+ .*?\[([^\]]*)\]", found[0]).group(1)


def _g0_block(lines: list[str], cid: str) -> list[str]:
    """A contract's G0 verdict line and its three conditions' lines."""
    at = next(n for n, line in enumerate(lines) if line.startswith(f"  {cid}/G0 "))
    return lines[at:at + 4]


@pytest.fixture(scope="module")
def verdict_repo(tmp_path_factory):
    base = tmp_path_factory.mktemp("g1-release")
    env = {"GIT_CEILING_DIRECTORIES": str(base)}
    on = _fixture(base / "on", ("G0", "G1"))
    off = _fixture(base / "off", ("G0",))
    return {"on": on, "off": off, "lines_on": _tree(on, **env), "lines_off": _tree(off, **env)}


@pytest.fixture(scope="module")
def kit_tree():
    """The kit's own tree, printed once: about 200 KB."""
    done = _cli("tree", "--root", ROOT)
    assert done.returncode == 0, done.stderr
    return {"lines": done.stdout.splitlines(), "problems": done.stderr.splitlines()}


# --- done_means: kit 0.20.0, the version ---------------------------------------------

def test_done_means_the_kit_version_reads_0_20_0_or_later_and_both_places_agree():
    # a floor, never the literal: the next release moves both numbers
    project = _version(PYPROJECT, r'^version\s*=\s*"(\d+\.\d+\.\d+)"')
    kit = _version(INIT, r'^KIT_VERSION\s*=\s*"(\d+\.\d+\.\d+)"')
    assert project >= (0, 20, 0)
    assert kit == project


# --- done_means: kit 0.20.0, the changelog -----------------------------------------------

def _entry() -> tuple[str, str]:
    text = _read(CHANGELOG)
    headings = [line.rstrip() for line in text.splitlines() if line.startswith("## ")]
    assert headings, "the changelog holds no release"
    match = RELEASE_HEADING.match(headings[0])
    assert match, f"the newest entry heads {headings[0]!r}"
    assert headings[1].startswith("## 0.19.0 "), headings[1]
    return match.group(1), _cut(text, headings[0], r"^## ")


def test_done_means_the_changelogs_newest_entry_heads_0_20_0_with_an_iso_date_above_0_19_0():
    date, entry = _entry()
    datetime.date.fromisoformat(date)
    text = _read(CHANGELOG)
    assert text.index("## 0.20.0 - ") < text.index("## 0.19.0 - ")
    assert text.count("## 0.20.0 - ") == 1


def test_done_means_the_changelog_entry_holds_six_bullets_in_the_order_of_the_units():
    _, entry = _entry()
    bullets = [_flat(chunk) for chunk in re.split(r"(?m)^- ", entry)[1:]]
    assert len(bullets) == 6
    for chunk, (lead, where, unit, _) in zip(bullets, BULLETS):
        assert chunk.startswith(f"**{lead}** {where}"), (lead, chunk[:120])
        assert f"unit `{unit}`" in chunk, unit
    units = re.findall(r"unit `(s\d-[a-z]+)`", _flat(entry))
    assert units == [unit for _, _, unit, _ in BULLETS]


@pytest.mark.parametrize("lead, facts", [(lead, facts) for lead, _, _, facts in BULLETS],
                         ids=[unit for _, _, unit, _ in BULLETS])
def test_done_means_the_changelog_bullet_names_its_commands_files_and_delta_note(lead, facts):
    _, entry = _entry()
    bullets = {chunk.split("**")[1]: _flat(chunk) for chunk in re.split(r"(?m)^- ", entry)[1:]
               if chunk.startswith("**")}
    assert lead in bullets, lead
    for fact in facts:
        assert fact in bullets[lead], fact


# --- done_means: USAGE reads green -------------------------------------------------------

def test_done_means_usage_section_4_shows_the_g1_venue_green_under_the_shipped_banner():
    four = _section(4)
    assert f"### {G1_VENUE} {GREEN}" in [line.rstrip() for line in four.splitlines()]
    venue = _subsection(four, G1_VENUE)
    assert _banner(venue) == VENUE_BANNER
    assert RED not in venue
    leads = _prose(venue)
    assert len(leads) == VENUE_LEADS
    assert all(block.startswith(f"{GREEN} ") for block in leads), [
        block[:50] for block in leads if not block.startswith(f"{GREEN} ")]


def test_done_means_usage_section_9_shows_g1_as_an_active_gate_green_under_the_shipped_banner():
    nine = _section(9)
    assert f"### {G1_GATE} {GREEN}" in [line.rstrip() for line in nine.splitlines()]
    gate = _subsection(nine, G1_GATE)
    assert _banner(gate) == GATE_BANNER
    assert RED not in gate
    leads = _prose(gate)
    assert len(leads) == GATE_LEADS
    assert all(block.startswith(f"{GREEN} ") for block in leads), [
        block[:50] for block in leads if not block.startswith(f"{GREEN} ")]


def test_done_means_usage_keeps_a_red_mark_on_its_two_legend_lines_and_nowhere_else():
    marked = [line for line in usage_text(USAGE).splitlines() if RED in line]
    assert len(marked) == 2, marked
    # The page's own legend, and the line of the file listing that explains the marks.
    assert f"Sections marked {RED} are ratified but not" in marked[0]
    assert "gate status page" in marked[1] and f"({GREEN}/{RED})" in marked[1]


def test_done_means_usage_refused_progress_lines_hold_the_g1_line_after_the_done_line():
    recording = _subsection(_section(9), "Recording progress")
    blocks = [lines for lines in _fences(recording) if "no node '{id}'" in " ".join(lines)]
    assert len(blocks) == 1
    lines = blocks[0]
    at = lines.index(DONE_TAKES)
    assert lines[at + 1] == G1_REFUSED
    assert "is an approval" in lines[at + 2]
    # the nine lines of 0.19.0, and this one
    assert lines.count(G1_REFUSED) == 1 and len(lines) == 10


def test_done_means_usage_says_when_the_g1_refused_line_stands_in_the_paragraph_after_the_block():
    recording = _subsection(_section(9), "Recording progress")
    assert G1_REFUSED in recording, "the refused lines hold no G1 line"
    after = recording[recording.index(G1_REFUSED):]
    paragraphs = _paragraphs(after[after.index("```") + 3:])
    assert paragraphs[0] == G1_LINE_PARAGRAPH
    assert paragraphs[1].startswith(f"{GREEN} A malformed progress file prints one line")


def test_done_means_usage_draws_a_feature_before_intake_on_the_invented_feature_apply_discount():
    halves = _subsection(_section(9), "Revisions and halves")
    assert _paragraph(halves, "A feature before intake rolls up its verdicts") == (
        BEFORE_INTAKE_PARAGRAPH)
    drawings = _fences(halves)
    assert DRAWING in drawings
    assert HALF_DRAWING in drawings
    assert "g1-requirements-spec" not in halves


def test_done_means_usages_drawing_of_a_feature_before_intake_is_what_the_tree_prints(tmp_path):
    halves = _subsection(_section(9), "Revisions and halves")
    drawn = next((lines for lines in _fences(halves)
                  if lines and lines[0].startswith("apply-discount ")), None)
    assert drawn is not None, "USAGE draws no apply-discount before intake"
    root = tmp_path / "scratch"
    _dump(root / ".sdlc" / "config.yaml", {"kit": "fixture", "active_gates": ["G0"]})
    head = "| Revision Date | Revised By | Changes Made |\n| :-: | :-: | :-- |\n"
    title = "# apply-discount - Apply one discount code per order\n\n"
    rows = "".join(f"| 2026-10-01 | user | {text} |\n" for text in (
        "r1: Created through an interview", "r2: Measured: the checks before signing",
        "r3: The request half finished", "r4: Signed: request half. The PO seat signs r3"))
    feature = root / "docs" / "features"
    feature.mkdir(parents=True)
    # The revision table opens the document, as the interview writes it: r4 stands on line 6.
    (feature / "apply-discount.md").write_text(head + rows + "\n" + title, encoding="utf-8")
    (feature / "apply-discount.design.md").write_text(
        head + "| 2026-10-02 | raj | r1: Created through an interview |\n\n" + title,
        encoding="utf-8")
    env = _env(GIT_CEILING_DIRECTORIES=str(tmp_path))
    lines = _tree(root, GIT_CEILING_DIRECTORIES=str(tmp_path))
    start = next(n for n, line in enumerate(lines) if line.startswith("apply-discount "))
    size = next((n for n, line in enumerate(lines[start + 1:]) if not line.startswith(" ")),
                len(lines) - start - 1)
    assert lines[start:start + 1 + size] == drawn
    half = _cli("tree", "apply-discount/request", "--root", root, env=env)
    assert half.stdout.splitlines()[:2] == next(
        lines for lines in _fences(halves) if lines[0].startswith("apply-discount/request"))


def test_done_means_usage_line_that_says_intake_writes_the_record_reads_kit_0_20_0():
    interview = _subsection(_section(4), "`/sdlc:product-specification-interview`")
    assert RECORD_SENTENCE in _paragraph(interview, "The Record reads")
    assert "kit 0.19.0 has no step that writes the Record" not in _flat(usage_text(USAGE))


def test_done_means_usage_says_the_kit_computes_no_condition_from_g2_on_and_reads_g1s_from_its_records():
    sentence = _paragraph(_subsection(_section(9), "Gates and their conditions"),
                          "the kit computes none of them yet")
    assert "conditions at every other gate" not in sentence
    assert ("A feature's conditions at G2 to G10 read `to do`: the kit computes none of them "
            "yet.") in sentence
    assert ("G1's conditions read from its records where G1 is active for the feature (\"G1 as "
            "an active gate\", below) and `to do` where it is inactive.") in sentence


# --- done_means: the kit's own declarations -----------------------------------------------

def test_done_means_the_kits_config_lists_g1_under_active_gates_beside_g0():
    gates = _yaml(CONFIG).get("active_gates")
    assert gates == ["G0", "G1"], gates


def test_done_means_the_kits_g1_exempt_list_holds_the_19_features_and_not_the_glossary_one():
    section = _yaml(CONFIG).get("g1")
    assert isinstance(section, dict), "the config holds no g1 key"
    exempt = section.get("exempt")
    assert isinstance(exempt, list) and len(exempt) == len(set(exempt)) == 19
    assert set(exempt) == set(EXEMPT)
    assert NOT_EXEMPT not in exempt
    for feature in exempt:
        assert (ROOT / "specs" / feature / "contract.yaml").is_file(), feature


def test_done_means_the_kits_g1_schemas_holds_one_spectral_entry_over_each_boundary_schema():
    section = _yaml(CONFIG).get("g1")
    assert isinstance(section, dict), "the config holds no g1 key"
    assert set(section) == {"exempt", "schemas"}
    entries = section["schemas"]
    assert isinstance(entries, list) and len(entries) == 1
    entry = entries[0]
    assert set(entry) == {"paths", "linter", "pin"}
    assert entry["linter"] == "spectral" and entry["pin"] == ".spectral.yaml"
    assert (ROOT / entry["pin"]).is_file()
    files = sorted(path.relative_to(ROOT).as_posix() for path in SCHEMAS.rglob("*.json"))
    assert files, "the kit holds no schema"
    for file in files:
        assert any(fnmatch.fnmatchcase(file, pattern) for pattern in entry["paths"]), file


def test_done_means_the_spectral_pin_holds_the_two_rules_with_their_severities_and_fields():
    rules = _yaml(SPECTRAL)["rules"]
    assert set(rules) == {"schema-names-its-dialect", "schema-has-a-title"}
    dialect, title = rules["schema-names-its-dialect"], rules["schema-has-a-title"]
    assert dialect["given"] == "$" and title["given"] == "$"
    assert dialect["severity"] == "error" and title["severity"] == "warn"
    assert dialect["then"] == {"field": "$schema", "function": "truthy"}
    assert title["then"] == {"field": "title", "function": "truthy"}
    assert dialect["description"] and title["description"]


def test_done_means_the_kits_component_declaration_validates_and_declares_no_component():
    doc = _yaml(COMPONENTS)
    schema = json.loads(_read(COMPONENT_SCHEMA))
    assert list(Draft202012Validator(schema).iter_errors(doc)) == []
    assert doc == {"version": 1, "components": []}


# --- done_means: the kit's own tree shows G1 as an active gate -----------------------------

def test_done_means_the_kits_tree_marks_g1_inactive_for_each_exempt_feature(kit_tree):
    _g1_is_on()
    lines = kit_tree["lines"]
    for feature in EXEMPT:
        assert f"  {feature}/G1 {G1_TITLE} [to do] inactive" in lines, feature
        for condition, name in (("G1.1", "Spec/schema linting"), ("G1.2", "Model checking"),
                                ("G1.3", "Criteria completeness + ambiguity review")):
            assert f"    {feature}/G1/{condition} {name} [to do]" in lines, (feature, condition)


def test_done_means_the_kits_tree_shows_g1_active_for_the_feature_the_exempt_list_leaves_out(
        kit_tree):
    _g1_is_on()
    lines = kit_tree["lines"]
    own = f"  {NOT_EXEMPT}/G1 {G1_TITLE} ["
    at = next((n for n, line in enumerate(lines) if line.startswith(own)), None)
    assert at is not None, "the tree prints no G1 line for the feature"
    assert not lines[at].endswith(" inactive")
    # G1.1 and G1.2 read their declarations, which hold none for this feature.
    assert _tag(lines, f"{NOT_EXEMPT}/G1/G1.1", "Spec/schema linting") == "done"
    assert _tag(lines, f"{NOT_EXEMPT}/G1/G1.2", "Model checking") == "done"
    assert _tag(lines, f"{NOT_EXEMPT}/G1/G1.3", "Criteria completeness + ambiguity review") in (
        "to do", "failed", "done")
    # The next gate after the active one is marked inactive, as today.
    assert any(line.startswith(f"  {NOT_EXEMPT}/G2 ") and line.endswith("[to do] inactive")
               for line in lines)


def test_done_means_the_kits_repository_line_holds_the_feature_the_exempt_list_leaves_out_and_no_exempt_one(
        kit_tree):
    _g1_is_on()
    lines = kit_tree["lines"]
    at = next((n for n, line in enumerate(lines) if line.startswith(f"gates/G1 {G1_TITLE} [")),
              None)
    assert at is not None, "the tree prints no gates/G1 line"
    # Every feature the kit adds later joins this list, so name the two sides, not the count.
    held = []
    for line in lines[at + 1:]:
        found = re.match(r"^  - (\S+) holds G1 at ", line)
        if not found:
            break
        held.append(found.group(1))
    assert NOT_EXEMPT in held
    assert not set(held) & set(EXEMPT), sorted(set(held) & set(EXEMPT))


def test_done_means_the_kits_tree_prints_no_g1_problem_line(kit_tree):
    _g1_is_on()
    assert not [line for line in kit_tree["problems"] if "g1" in line.lower()]
    assert not [line for line in kit_tree["problems"] if "component declaration" in line]


def test_done_means_g1_check_reads_the_kits_two_declarations_for_a_feature_each_side_of_exempt():
    done = _cli("g1-check", NOT_EXEMPT)
    # Exit 0 or 1 is a reading of the declarations; exit 2 says one is absent or unreadable.
    # G1.3 changes once the feature's review is recorded, so its word is not pinned.
    assert done.returncode in (0, 1) and done.stderr == "", (done.returncode, done.stderr)
    first = done.stdout.splitlines()[0]
    assert first == f"g1-green: {NOT_EXEMPT}" or first.startswith(f"{NOT_EXEMPT}: G1.1 done, G1.2 done"), first
    for feature in ("g1-requirements-spec", "tree-view"):
        done = _cli("g1-check", feature)
        assert (done.returncode, done.stdout) == (2, "")
        assert done.stderr.splitlines() == [f"{feature}: G1 is not active"]


# --- SC4.3: a contract's G0 verdict reads as the validator says --------------------------

def test_sc4_3_each_contract_of_a_fixture_reads_done_blocked_to_do_or_failed_as_the_validator_says(
        verdict_repo):
    lines = verdict_repo["lines_on"]
    for cid, expected in STATES.items():
        assert _g0_verdict(verdict_repo["on"], cid) == expected, cid
        assert _tag(lines, f"{cid}/G0", "Planning / Intake") == expected, cid
    assert {_tag(lines, f"{cid}/G0", "Planning / Intake") for cid in STATES} == {
        "done", "blocked", "to do", "failed"}


def test_sc4_3_a_fixture_with_g1_active_reads_g1_on_each_contract_and_leaves_g0_as_it_was(
        verdict_repo):
    on, off = verdict_repo["lines_on"], verdict_repo["lines_off"]
    for cid in STATES:
        assert _g0_block(on, cid) == _g0_block(off, cid), cid
        assert not _g1_line(on, cid).endswith(" inactive"), cid
        assert _g1_line(off, cid).endswith("[to do] inactive"), cid
        assert any(line.startswith(f"  {cid}/G2 ") and line.endswith("[to do] inactive")
                   for line in on), cid


def _g1_line(lines: list[str], cid: str) -> str:
    return next(line for line in lines if line.startswith(f"  {cid}/G1 "))


def test_sc4_3_each_contract_of_the_kit_reads_in_the_tree_as_the_validator_reports_it(kit_tree):
    _g1_is_on()
    contracts = sorted(path.parent.name for path in (ROOT / "specs").glob("*/contract.yaml"))
    assert len(contracts) >= 20
    seen = set()
    for cid in contracts:
        verdict = _g0_verdict(ROOT, cid)
        assert _tag(kit_tree["lines"], f"{cid}/G0", "Planning / Intake") == verdict, cid
        seen.add(verdict)
    assert "done" in seen


# --- unchanged by the release (the design's Out of scope) ---------------------------------

def test_unchanged_a_new_repository_is_born_with_g0_alone_active():
    text = _read(CONFIG_TEMPLATE)
    assert re.findall(r"^\s+- (\S+)", text, re.MULTILINE) == ["G0"]
    assert "G1" not in text and "g1:" not in text


def test_unchanged_no_scaffolded_or_own_workflow_runs_a_linter_or_a_checker():
    for path in (CI, WORKFLOW_TEMPLATE):
        text = _read(path)
        assert not re.search(r"spectral|\bbuf\b|\btlc\b|g1-check|g1-record|\bg1\b", text,
                             re.IGNORECASE), path.name


# --- done_means: the pages name G1 as shipped ----------------------------------------------

def test_done_means_sdlc_page_reads_g1_live_here_between_g0_and_the_rest_of_the_table():
    rows = _read(SDLC).splitlines()
    at = rows.index(SDLC_G0)
    assert rows[at + 1:at + 3] == [SDLC_G1, SDLC_REST]
    assert "G1-G10" not in _read(SDLC)


def test_done_means_the_sdlc_template_names_g1_shipped_and_not_live_in_a_new_repository():
    rows = _read(SDLC_TEMPLATE).splitlines()
    at = rows.index(SDLC_G0)
    assert rows[at + 1:at + 3] == [SDLC_G1_OFF, SDLC_REST]
    assert "G1-G10" not in _read(SDLC_TEMPLATE)


def test_done_means_the_gates_page_says_enforcement_shipped_after_its_g1_line():
    text = _read(GATES_PAGE)
    paragraph = _paragraph(text, "**Deep page:** [gates/G1-requirements-spec.md]")
    _in_order(_plain(paragraph), GATES_OLD, GATES_NEW)
    assert _plain(paragraph).endswith(GATES_NEW)


@pytest.mark.parametrize("heading, lifecycle", G1_PAGE_LIFECYCLES,
                         ids=["G1.1", "G1.2", "G1.3"])
def test_done_means_the_g1_page_reads_each_condition_enforced_here_since_kit_0_20_0(
        heading, lifecycle):
    section = _plain(_cut(_read(G1_PAGE), heading, r"^### "))
    assert section.endswith(lifecycle), section[-200:]


def test_done_means_the_g1_page_records_the_per_component_set_in_the_components_file():
    section = _plain(_cut(_read(G1_PAGE), "### G1.2 Model checking", r"^### "))
    assert G12_PARAMETERS in section
    _in_order(section, "all three prongs must hold.", G12_PARAMETERS, "**Lifecycle:**")
    assert "recording venue deferred to the enforcement pass" not in section


def test_done_means_the_g1_page_names_the_signed_review_as_g1_3s_operational_artifact():
    section = _plain(_cut(_read(G1_PAGE), "### G1.3 Criteria completeness + ambiguity review",
                          r"^### "))
    assert G13_TOOLING in section
    assert "is enforcement-pass work" not in section
    assert "**Parameters:** the checklist content - PROPOSED." in section


def test_done_means_operators_names_sdlc_spec_as_shipping_at_the_first_bound_g2_surface():
    rows = [line for line in _read(OPERATORS).splitlines()
            if _plain(line).startswith("| sdlc-spec | G0-G2 authoring venues |")]
    assert len(rows) == 1
    assert _plain(rows[0]).endswith(SPEC_AGENT_STATUS)


def test_done_means_operators_venue_map_reads_g1_live_at_kit_0_20_0():
    rows = [_plain(line) for line in _read(OPERATORS).splitlines()
            if line.startswith("| G1 requirements |")]
    assert rows == [VENUE_MAP_G1]


def test_done_means_operators_deferred_list_drops_g1_from_the_sdlc_spec_trigger():
    text = _plain(_read(OPERATORS))
    assert DEFERRED in text
    assert "first bound G1/G2 authoring" not in text


def test_done_means_the_components_page_has_a_g1_gate_row_after_the_work_tree_row():
    rows = [line.rstrip() for line in _read(COMPONENT_ROWS).splitlines()
            if line.startswith("| ")]
    tree = next(n for n, line in enumerate(rows) if line.startswith("| work tree |"))
    assert rows[tree + 1:tree + 2] == [COMPONENT_ROW]
    assert sum(line.startswith("| G1 gate |") for line in rows) == 1
