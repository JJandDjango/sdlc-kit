"""G1.3 suite, the code half (contract: g1-requirements-spec, unit s3-review).

A temporary repository per test: one contract under specs/, a
.sdlc/config.yaml that turns G1 on, a ratified `intake-seat` term whose
values are `po` and `engineer`, and the feature's pair under
docs/features/: a requirements document whose newest `Ready:` row names
r5, and a design document whose newest `Ready:` row names r4. The
fixture's `g1.schemas` pattern matches no file and its component
declaration holds no hard core, so G1.1 and G1.2 read `done` in every
summary line here. No test needs a tool on the machine.

What the unit pins: `g1-record review` appends one G1.3 record to
.sdlc/g1/<id>.yaml, with the signer's name, the seat, the revision of each
document the contract was derived from, and each of the 11 items once
(SC1.1); each item a review leaves unchecked is RS301's diagnostic under
G1.3, with the item's name and the section the person named, and G1.3
reads `failed` until a later review passes (SC1.2); the review holds
G1.3's 11 items and no ready check (SC1.3); and G1.3 reads `done` only
from a review with a signature over all 11 items, on the revisions the
contract was derived from (done_means). Each rule that sorts free text
has one table of hostile inputs, and each case the rule cannot tell lands
on the closed side: the call is refused, or G1.3 does not read `done`.

A reader's test first shows `g1-green` from a record that reads well, and
only then changes it, so no test here passes on a reader that reads every
record as absent.
"""

from __future__ import annotations

import copy
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract
from conftest import write_seat_roster
from taskcontract import tree
from taskcontract.__main__ import main
from taskcontract.progress import head_id

KIT = Path(__file__).resolve().parent.parent
PAGE = KIT / "docs" / "gates" / "G1-requirements-spec.md"
PACKAGE = Path(taskcontract.__file__).resolve().parent
ITEMS_FILE = PACKAGE / "data" / "g1-items.yaml"

ID = "apply-discount"
OTHER = "refund-order"
RECORD = f".sdlc/g1/{ID}.yaml"
RECORDED = f"recorded: {RECORD}"
REQUIREMENTS = f"docs/features/{ID}.md"
DESIGN = f"docs/features/{ID}.design.md"
ROSTER = "specs/vocabulary/intake-seat.yaml"
GREEN = f"g1-green: {ID}"
PASSED = "G1.3: the review checks all 11 items"

# G1.3's 11 items as its page ratified them (docs/gates/G1-requirements-spec.md).
NAMES = ["Testable", "Unambiguous", "Traceable", "Complete over units",
         "Covers the sketch", "Consistent", "Respects non-goals",
         "Boundary + error paths", "Property-spec applicability",
         "Schema presence", "Oracle designation answered"]
ALL = "1,2,3,4,5,6,7,8,9,10,11"
BUT_6 = "1,2,3,4,5,7,8,9,10,11"
ABSENT = object()  # a key a hand-written record leaves out

CONTRACT = """id: {id}
title: A fixture feature
intent: >
  A contract with a scope of its own, enough words to pass the door as a
  fixture for the G1.3 suite.
scope:
  - api/
  - src/
non_goals:
  - nothing beyond the scope
decomposition:
  - unit: the unit
    id: the-unit
    confirmed_by: [po]
    done_means: the unit is done
    acceptance_sketch:
      - verify the unit is done
dependencies: []
entities: []
provenance:
  origin: human-request
"""

SPECTRAL = {"paths": ["api/*.yaml"], "linter": "spectral", "pin": ".spectral.yaml"}
API = {"id": "api", "paths": ["src/api/"], "hard_core": False, "oracle": "none",
       "oracle_reason": "read-only pass-through, covered by its acceptance tests"}

TITLE = "# {id} - A fixture feature\n\n"
HEAD = "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"


def row(text: str, by: str = "Ann Lee") -> str:
    """One row of a revision table, its last cell the given words."""
    return f"| 2026-10-07 | {by} | {text} |\n"


def document(revision: int, feature: str = ID) -> str:
    """A feature document with text rows r1 to r<revision>, then the
    `Ready:` row that names r<revision> as the one the contract is derived
    from."""
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{feature}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return TITLE.format(id=feature) + HEAD + rows + ready + "\n## Statement\n\nWords.\n"


def items(unchecked: dict | None = None) -> list[dict]:
    """The `items` of a G1.3 record: the 11, each checked but the ones
    `unchecked` maps to a section."""
    unchecked = unchecked or {}
    held = []
    for n, name in enumerate(NAMES, start=1):
        entry = {"n": n, "name": name, "checked": n not in unchecked}
        if n in unchecked:
            entry["section"] = unchecked[n]
        held.append(entry)
    return held


def written(unchecked: dict | None = None, **keys) -> dict:
    """A G1.3 record as `g1-record review` writes it for the fixture's
    pair, with each given key changed, or left out when it is ABSENT."""
    record = {"condition": "G1.3", "at": "2026-10-07T14:20:40Z", "head": "8635064",
              "by": "Ann Lee", "seat": "po", "requirements": "r5", "design": "r4",
              "items": items(unchecked)}
    for key, value in keys.items():
        if value is ABSENT:
            record.pop(key, None)
        else:
            record[key] = value
    return record


class Repo:
    """One fixture repository at <tmp>/repo: the working directory."""

    def __init__(self, tmp: Path, monkeypatch):
        self.root = tmp / "repo"
        self.root.mkdir()
        write_seat_roster(self.root, values=("po", "engineer"))
        self.contract(ID)
        self.write(".sdlc/config.yaml", yaml.safe_dump({
            "active_gates": ["G0", "G1"],
            "g1": {"exempt": ["controlled-language"], "schemas": [SPECTRAL]}},
            sort_keys=False))
        self.write("specs/components.yaml", yaml.safe_dump(
            {"version": 1, "components": [API]}, sort_keys=False))
        self.requirements(5)
        self.design(4)
        monkeypatch.chdir(self.root)

    def write(self, rel: str, text) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def remove(self, rel: str) -> None:
        (self.root / rel).unlink()

    def contract(self, contract_id: str) -> None:
        self.write(f"specs/{contract_id}/contract.yaml", CONTRACT.format(id=contract_id))

    def requirements(self, revision: int, feature: str = ID) -> None:
        self.write(f"docs/features/{feature}.md", document(revision, feature))

    def design(self, revision: int, feature: str = ID) -> None:
        self.write(f"docs/features/{feature}.design.md", document(revision, feature))

    def put(self, *records, feature: str = ID) -> None:
        """Write the record file by hand: these records and no other."""
        self.write(f".sdlc/g1/{feature}.yaml", yaml.safe_dump(
            {"records": list(records)}, sort_keys=False, allow_unicode=True))

    def records(self) -> list[dict]:
        return yaml.safe_load((self.root / RECORD).read_text(encoding="utf-8"))["records"]

    def last(self) -> dict:
        return self.records()[-1]

    def files(self) -> dict[str, bytes]:
        """Every file under the root with its bytes: what a call wrote shows
        as a difference."""
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in sorted(self.root.rglob("*")) if path.is_file()}


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Repo:
    return Repo(tmp_path, monkeypatch)


def cli(capsys, *argv):
    """Run one taskcontract command in this process: (exit code, stdout,
    stderr). A command the parser does not hold fails here, by name."""
    words = [str(arg) for arg in argv]
    capsys.readouterr()
    try:
        code = main(words)
    except SystemExit:  # argparse refused the words themselves
        code = None
    out, err = capsys.readouterr()
    assert code is not None, (
        f"taskcontract does not take `{' '.join(words[:3])}`: "
        f"{(err.strip().splitlines() or ['no line'])[-1]}")
    return code, out, err


def review(capsys, *args, feature: str = ID):
    """`g1-record review <id>` with these words, run at the repository's root."""
    return cli(capsys, "g1-record", "review", feature, *args)


def signed(capsys, *args, by: str = "Ann Lee", seat: str = "po", feature: str = ID):
    """A review signed by Ann Lee at the `po` seat, unless a test says other."""
    return review(capsys, "--by", by, "--seat", seat, *args, feature=feature)


def passing(capsys, feature: str = ID):
    """A review that checks all 11 items."""
    return signed(capsys, "--checked", ALL, feature=feature)


def drawn(capsys):
    """The design's drawn call, word for word."""
    return review(capsys, "--by", "Ann Lee", "--seat", "po",
                  "--checked", BUT_6, "--unchecked", "6=Statement")


def check(repo: Repo, capsys, *extra: str, feature: str = ID):
    return cli(capsys, "g1-check", feature, "--root", repo.root, *extra)


def summary(g1_3: str, feature: str = ID) -> str:
    return f"{feature}: G1.1 done, G1.2 done, G1.3 {g1_3}"


def rs301(n: int, section: str) -> str:
    return f"G1.3: item {n} {NAMES[n - 1]} is unchecked in {section}"


def is_green(repo: Repo, capsys) -> None:
    """G1 reads `done`: `g1-check` prints its one line and exits 0."""
    assert check(repo, capsys) == (0, GREEN + "\n", "")


def reads(repo: Repo, capsys, g1_3: str, *findings: str) -> None:
    """G1.3 reads the status, under these RS301 messages and no other line;
    `g1-check` exits 1."""
    code, out, err = check(repo, capsys)
    assert out.splitlines() == [*(f"{ID}: RS301 {message}" for message in findings),
                                summary(g1_3)]
    assert (code, err) == (1, "")


def refused(repo: Repo, capsys, *args, names: tuple[str, ...] = ()) -> str:
    """The call is one the writer cannot use: exit 2, nothing on stdout, one
    line on stderr that holds the feature's id and each given text, and
    every file under the root keeps every byte. Returns the line."""
    before = repo.files()
    code, out, err = review(capsys, *args)
    assert code == 2, f"exit {code}, stdout {out!r}, stderr {err!r}"
    assert out == ""
    lines = err.splitlines()
    assert len(lines) == 1, f"not one line on stderr: {err!r}"
    assert ID in lines[0]
    for name in names:
        assert name in lines[0], f"{lines[0]!r} does not name {name!r}"
    assert repo.files() == before, "a refused call wrote under the root"
    return lines[0]


def g1_rules() -> dict[str, list[str]]:
    """G1's conditions with the codes each owns, from the packaged list."""
    gates = yaml.safe_load((PACKAGE / "data" / "gates.yaml").read_text(encoding="utf-8"))
    gate = next(g for g in gates["gates"] if g["id"] == "G1")
    return {c["id"]: c.get("rules") for c in gate["conditions"]}


# --- SC1.1: the 11 items, a named person's signature, each revision ---


def test_sc1_1_a_review_that_checks_all_11_items_prints_its_line_and_exits_0(repo, capsys):
    assert passing(capsys) == (0, f"{PASSED}\n{RECORDED}\n", "")
    assert [r["condition"] for r in repo.records()] == ["G1.3"]


def test_sc1_1_the_record_holds_the_drawings_keys_in_the_drawings_order(repo, capsys):
    assert passing(capsys)[0] == 0
    record = repo.last()
    assert list(record) == ["condition", "at", "head", "by", "seat", "requirements",
                            "design", "items"]
    assert record["condition"] == "G1.3"
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", record["at"])
    assert record["head"] == head_id(repo.root)
    assert (record["by"], record["seat"]) == ("Ann Lee", "po")
    assert (record["requirements"], record["design"]) == ("r5", "r4")


def test_sc1_1_the_record_holds_each_of_the_11_items_once_with_its_ratified_name(
        repo, capsys):
    assert passing(capsys)[0] == 0
    held = repo.last()["items"]
    assert held == [{"n": n, "name": name, "checked": True}
                    for n, name in enumerate(NAMES, start=1)]
    assert all(list(entry) == ["n", "name", "checked"] for entry in held)


def test_sc1_1_the_items_file_holds_the_11_items_equal_to_the_gates_page():
    """The page wins (the design's Sources): the bold names under its G1.3
    checklist heading, in their order, are the file's names."""
    assert PAGE.is_file(), f"no page at {PAGE}"
    assert ITEMS_FILE.is_file(), "the package holds no data/g1-items.yaml"
    page = PAGE.read_text(encoding="utf-8")
    section = page.split("### G1.3 review checklist", 1)[1].split("\n## ", 1)[0]
    ratified = [(int(n), name) for n, name in
                re.findall(r"^\s*(\d+)\. \*\*(.+?)\*\*", section, flags=re.MULTILINE)]
    assert [n for n, _ in ratified] == list(range(1, 12))
    assert [name for _, name in ratified] == NAMES
    assert yaml.safe_load(ITEMS_FILE.read_text(encoding="utf-8")) == {
        "items": [{"n": n, "name": name} for n, name in ratified]}


def test_sc1_1_the_items_file_is_found_beside_gates_yaml_and_ships_with_the_package(
        tmp_path):
    """`g1.ITEMS_PATH` names the file beside gates.yaml, pyproject's package
    data holds it, and reading g1 does not load the tree: `tree` will read
    g1 from s4-tree on, so g1 reads a `Ready:` row by itself."""
    probe = ("import sys\nfrom taskcontract import g1\n"
             "print(getattr(g1, 'ITEMS_PATH', None))\n"
             "print('taskcontract.tree' in sys.modules)\n")
    result = subprocess.run(
        [sys.executable, "-c", probe], cwd=tmp_path, capture_output=True,
        encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONPATH": str(PACKAGE.parent)},
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    assert result.returncode == 0, result.stderr
    named, tree_loaded = result.stdout.splitlines()
    assert named != "None", "taskcontract.g1 holds no ITEMS_PATH"
    assert Path(named) == ITEMS_FILE
    assert ITEMS_FILE.is_file()
    assert tree_loaded == "False", "taskcontract.g1 loads taskcontract.tree"
    project = (KIT / "pyproject.toml").read_text(encoding="utf-8")
    table = project.split("[tool.setuptools.package-data]", 1)[1].split("\n[", 1)[0]
    patterns = re.findall(r'"([^"]+)"', table)
    assert any(fnmatch.fnmatchcase("data/g1-items.yaml", p) for p in patterns)


# How the item numbers are read. `--checked` is one comma-separated list;
# an element, with its outer spaces cut, is one of the texts 1 to 11.
CHECKED_TAKEN = [
    pytest.param(ALL, id="in-order"),
    pytest.param("11,10,9,8,7,6,5,4,3,2,1", id="any-order"),
    pytest.param(" 1, 2 ,3,4,5,6,7,8,9,10 , 11 ", id="outer-spaces-cut"),
]


@pytest.mark.parametrize("value", CHECKED_TAKEN)
def test_sc1_1_checked_is_one_list_of_item_numbers_with_outer_spaces_cut(
        repo, capsys, value):
    assert signed(capsys, "--checked", value) == (0, f"{PASSED}\n{RECORDED}\n", "")
    assert repo.last()["items"] == items()
    is_green(repo, capsys)


def but(*left_out: int) -> str:
    return ",".join(str(n) for n in range(1, 12) if n not in left_out)


EVERY_UNCHECKED = [word for n in range(1, 12) for word in ("--unchecked", f"{n}=Statement")]

# Each call fails to name each of the 11 items once: (the words after the
# signature, the texts the refusal names).
ITEMS_REFUSED = [
    pytest.param([], (), id="no-item-named"),
    pytest.param(["--checked", BUT_6], ("6",), id="item-6-in-neither-flag"),
    pytest.param(["--checked", ALL, "--unchecked", "6=Statement"], ("6",),
                 id="item-6-in-both-flags"),
    pytest.param(["--checked", "1," + ALL], ("1",), id="a-repeat-in-checked"),
    pytest.param(["--checked", BUT_6, "--unchecked", "6=Statement",
                  "--unchecked", "6=Statement"], ("6",), id="a-repeat-in-unchecked"),
    pytest.param(["--checked", BUT_6, "--unchecked", "6=Statement",
                  "--unchecked", "6=Checks"], ("6",),
                 id="a-repeat-in-unchecked-with-two-sections"),
    pytest.param(["--checked", "", *EVERY_UNCHECKED], (), id="empty-list"),
    pytest.param(["--checked", "   ", *EVERY_UNCHECKED], (), id="blank-list"),
    pytest.param(["--checked", ALL + ","], (), id="empty-element-at-the-end"),
    pytest.param(["--checked", "1,,2,3,4,5,6,7,8,9,10,11"], (), id="empty-element-inside"),
    pytest.param(["--checked", "1-11"], ("1-11",), id="a-range"),
    pytest.param(["--checked", "1-5,6,7,8,9,10,11"], ("1-5",), id="a-range-element"),
    pytest.param(["--checked", "01," + but(1)], ("01",), id="leading-zero"),
    pytest.param(["--checked", "+1," + but(1)], ("+1",), id="plus-sign"),
    pytest.param(["--checked=-1," + but(1)], ("-1",), id="minus-sign"),
    pytest.param(["--checked", "0," + ALL], ("0",), id="item-0"),
    pytest.param(["--checked", ALL + ",12"], ("12",), id="item-12"),
    pytest.param(["--checked", "\uff11," + but(1)], (), id="fullwidth-digit"),
    pytest.param(["--checked", "1,\u00b2,3,4,5,6,7,8,9,10,11"], (), id="superscript-digit"),
    pytest.param(["--checked", "one," + but(1)], ("one",), id="a-word"),
    pytest.param(["--checked", "ALL"], ("ALL",), id="the-word-all-in-capitals"),
    pytest.param(["--checked", "all"], ("all",), id="the-word-all"),
    pytest.param(["--checked", "*"], ("*",), id="a-star"),
    pytest.param(["--checked", "1.0," + but(1)], ("1.0",), id="a-decimal"),
    pytest.param(["--checked", "0x1," + but(1)], ("0x1",), id="a-hex-number"),
    pytest.param(["--checked", "1 0," + but(10)], ("1 0",), id="a-space-inside-a-number"),
    pytest.param(["--checked", ALL.replace(",", " ")], (), id="spaces-for-commas"),
    pytest.param(["--checked", ALL.replace(",", ";")], (), id="semicolons-for-commas"),
    pytest.param(["--checked", "6=Statement," + but(6)], (), id="an-equals-sign-inside"),
    pytest.param(["--checked", "1\n," + but(1)], (), id="a-line-break-inside"),
    pytest.param(["--checked", ALL + "\n"], (), id="a-line-break-at-the-end"),
    pytest.param(["--checked", "1,2,3,4,5\n6,7,8,9,10,11"], (),
                 id="a-line-break-for-a-comma"),
]


@pytest.mark.parametrize("words, names", ITEMS_REFUSED)
def test_sc1_1_a_review_that_does_not_name_each_of_the_11_items_once_is_refused(
        repo, capsys, words, names):
    assert drawn(capsys)[0] == 1
    refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", *words, names=names)
    reads(repo, capsys, "failed", rs301(6, "Statement"))


def test_sc1_1_a_refused_first_review_leaves_no_record_file(repo, capsys):
    repo.contract(OTHER)
    repo.requirements(3, OTHER)
    assert passing(capsys, feature=OTHER)[0] == 0
    refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", BUT_6)
    assert [path.name for path in (repo.root / ".sdlc" / "g1").iterdir()] == [
        f"{OTHER}.yaml"]


# The signer's name: kept as the person wrote it, with its outer whitespace cut.
BY_KEPT = [
    pytest.param("Ann Lee", "Ann Lee", id="plain"),
    pytest.param("  Ann Lee  ", "Ann Lee", id="outer-spaces-cut"),
    pytest.param("\tAnn Lee\t", "Ann Lee", id="outer-tabs-cut"),
    pytest.param("ann lee", "ann lee", id="lower-case-kept"),
    pytest.param("ANN LEE", "ANN LEE", id="capitals-kept"),
    pytest.param("Lee, Ann", "Lee, Ann", id="a-comma-inside"),
    pytest.param("Ann=Lee", "Ann=Lee", id="an-equals-sign-inside"),
    pytest.param("Ann  Lee", "Ann  Lee", id="inner-spaces-kept"),
    pytest.param("Zo\u00eb \u00d3 N\u00e9ill", "Zo\u00eb \u00d3 N\u00e9ill", id="not-ascii"),
    pytest.param("123", "123", id="digits-stay-text"),
    pytest.param("null", "null", id="yamls-null-stays-text"),
    pytest.param("true", "true", id="yamls-true-stays-text"),
    pytest.param("# Ann", "# Ann", id="a-hash"),
    pytest.param("Ann: Lee", "Ann: Lee", id="a-colon"),
    pytest.param("po", "po", id="a-seats-name"),
]


@pytest.mark.parametrize("given, kept", BY_KEPT)
def test_sc1_1_a_named_person_signs_and_the_name_is_kept_as_written(
        repo, capsys, given, kept):
    assert signed(capsys, "--checked", ALL, by=given) == (0, f"{PASSED}\n{RECORDED}\n", "")
    assert repo.last()["by"] == kept
    assert isinstance(repo.last()["by"], str)
    is_green(repo, capsys)


BY_REFUSED = [
    pytest.param("", id="empty"),
    pytest.param("   ", id="spaces-alone"),
    pytest.param("\t", id="a-tab-alone"),
    pytest.param("\u00a0", id="a-no-break-space-alone"),
    pytest.param("\u3000", id="an-ideographic-space-alone"),
    pytest.param("\n", id="a-line-break-alone"),
    pytest.param("Ann\nLee", id="a-line-break-inside"),
    pytest.param("Ann Lee\n", id="a-line-break-at-the-end"),
    pytest.param("\nAnn Lee", id="a-line-break-at-the-start"),
    pytest.param("Ann\rLee", id="a-carriage-return-inside"),
    pytest.param("Ann\r\nLee", id="a-crlf-inside"),
    pytest.param("Ann\u2028Lee", id="a-line-separator-inside"),
    pytest.param("Ann\u2029Lee", id="a-paragraph-separator-inside"),
    pytest.param("Ann\x85Lee", id="a-next-line-inside"),
    pytest.param("Ann\x0bLee", id="a-vertical-tab-inside"),
    pytest.param("Ann\x0cLee", id="a-form-feed-inside"),
    # a text with no letter and no digit names no person
    pytest.param("​", id="a-zero-width-space-alone"),
    pytest.param("-", id="a-dash-alone"),
    pytest.param("...", id="dots-alone"),
]


@pytest.mark.parametrize("given", BY_REFUSED)
def test_sc1_1_a_by_that_names_no_person_or_holds_a_line_break_is_refused(
        repo, capsys, given):
    assert drawn(capsys)[0] == 1
    refused(repo, capsys, "--by", given, "--seat", "po", "--checked", ALL)
    reads(repo, capsys, "failed", rs301(6, "Statement"))


OPTION_LEFT_OUT = [
    pytest.param(["--seat", "po", "--checked", ALL], id="no-by"),
    pytest.param(["--by", "Ann Lee", "--checked", ALL], id="no-seat"),
    pytest.param(["--checked", ALL], id="neither"),
]


@pytest.mark.parametrize("words", OPTION_LEFT_OUT)
def test_sc1_1_a_review_with_no_signer_or_no_seat_exits_2_and_writes_nothing(
        repo, capsys, words):
    """The parser's own refusal counts here, so only the exit code, the
    empty stdout and the files are held."""
    assert drawn(capsys)[0] == 1
    before = repo.files()
    capsys.readouterr()
    try:
        code = main(["g1-record", "review", ID, *words])
    except SystemExit as stop:
        code = stop.code
    out, err = capsys.readouterr()
    assert code == 2
    assert out == ""
    assert err.strip()
    assert repo.files() == before
    reads(repo, capsys, "failed", rs301(6, "Statement"))


# An option given twice names two signers, two seats or two lists: refused.
REPEATED = [
    pytest.param(["--by", "Ann Lee", "--by", "Ann Lee", "--seat", "po", "--checked", ALL],
                 id="by-twice-the-same"),
    pytest.param(["--by", "Ann Lee", "--by", "Bo Chen", "--seat", "po", "--checked", ALL],
                 id="by-twice-two-names"),
    pytest.param(["--by", "Ann Lee", "--seat", "po", "--seat", "po", "--checked", ALL],
                 id="seat-twice-the-same"),
    pytest.param(["--by", "Ann Lee", "--seat", "po", "--seat", "engineer", "--checked", ALL],
                 id="seat-twice-two-seats"),
    pytest.param(["--by", "Ann Lee", "--seat", "po", "--checked", ALL, "--checked", ALL],
                 id="checked-twice-the-same"),
    pytest.param(["--by", "Ann Lee", "--seat", "po", "--checked", "1,2,3,4,5",
                  "--checked", "6,7,8,9,10,11"], id="checked-in-two-lists"),
]


@pytest.mark.parametrize("words", REPEATED)
def test_sc1_1_an_option_given_twice_is_refused(repo, capsys, words):
    assert drawn(capsys)[0] == 1
    refused(repo, capsys, *words)
    reads(repo, capsys, "failed", rs301(6, "Statement"))


@pytest.mark.parametrize("seat", ["po", "engineer"])
def test_sc1_1_the_seat_is_a_value_of_the_ratified_intake_seat_term(repo, capsys, seat):
    assert signed(capsys, "--checked", ALL, seat=seat) == (
        0, f"{PASSED}\n{RECORDED}\n", "")
    assert repo.last()["seat"] == seat
    is_green(repo, capsys)


# The seat against a roster whose values are `po` and `engineer`: matched
# exactly, letter case and outer spaces included.
SEAT_REFUSED = [
    pytest.param("", (), id="empty"),
    pytest.param(" ", (), id="a-space-alone"),
    pytest.param("PO", ("PO",), id="capitals"),
    pytest.param("Po", ("Po",), id="one-capital"),
    pytest.param(" po", ("po",), id="a-space-before"),
    pytest.param("po ", ("po",), id="a-space-after"),
    pytest.param("po\n", (), id="a-line-break-at-the-end"),
    pytest.param("\npo", (), id="a-line-break-at-the-start"),
    pytest.param("po\nengineer", (), id="a-line-break-inside"),
    pytest.param("po,engineer", ("po,engineer",), id="a-comma-inside"),
    pytest.param("po=engineer", ("po=engineer",), id="an-equals-sign-inside"),
    pytest.param("po engineer", ("po engineer",), id="two-seats"),
    pytest.param("user", ("user",), id="a-seat-of-another-roster"),
    pytest.param("seat", ("seat",), id="the-terms-alias"),
    pytest.param("intake-seat", ("intake-seat",), id="the-terms-slug"),
    pytest.param("p", ("p",), id="a-prefix"),
    pytest.param("poo", ("poo",), id="a-longer-word"),
    pytest.param("\uff50\uff4f", (), id="fullwidth-letters"),
    pytest.param("ratified", ("ratified",), id="the-terms-status"),
]


@pytest.mark.parametrize("seat, names", SEAT_REFUSED)
def test_sc1_1_a_seat_that_is_no_value_of_the_term_is_refused(repo, capsys, seat, names):
    assert drawn(capsys)[0] == 1
    refused(repo, capsys, "--by", "Ann Lee", "--seat", seat, "--checked", ALL, names=names)
    reads(repo, capsys, "failed", rs301(6, "Statement"))


def term(**keys) -> str:
    doc = {"term": "intake-seat", "name": "Intake seat",
           "definition": "A human position that answers for a unit at intake.",
           "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
           "since": "2026-08-26"}
    for key, value in keys.items():
        if value is ABSENT:
            doc.pop(key)
        else:
            doc[key] = value
    return yaml.safe_dump(doc, sort_keys=False)


# A roster that gives no seat: (the term's file or None for no file, the seat tried).
ROSTER_REFUSED = [
    pytest.param(None, "po", id="no-term"),
    pytest.param(term(status="draft"), "po", id="a-draft-term"),
    pytest.param(term(status="deprecated"), "po", id="a-deprecated-term"),
    pytest.param(term(status="Ratified"), "po", id="status-in-another-case"),
    pytest.param(term(status=ABSENT), "po", id="no-status"),
    pytest.param(term(values=ABSENT), "po", id="no-values"),
    pytest.param(term(values="po"), "po", id="values-is-the-seats-text"),
    pytest.param(term(values="engineer po"), "po", id="values-is-a-text-that-holds-the-seat"),
    pytest.param(term(values={"po": "the PO seat"}), "po", id="values-is-a-mapping"),
    pytest.param(term(values=[["po"]]), "po", id="values-holds-a-list"),
    pytest.param(term(values=[1]), "1", id="values-holds-a-number"),
    pytest.param(term(values=[True]), "True", id="values-holds-a-boolean"),
    pytest.param(term(values=[None]), "None", id="values-holds-null"),
    pytest.param(term(values=["po", ""]), "", id="values-holds-the-empty-text"),
    pytest.param("values: [po\n", "po", id="no-yaml"),
    pytest.param("- po\n- engineer\n", "po", id="a-yaml-list"),
    pytest.param(b"\xff\xfe values: [po]\n", "po", id="not-utf8"),
]


@pytest.mark.parametrize("text, seat", ROSTER_REFUSED)
def test_sc1_1_a_roster_that_is_absent_or_not_ratified_gives_no_seat(
        repo, capsys, text, seat):
    assert drawn(capsys)[0] == 1
    if text is None:
        repo.remove(ROSTER)
    else:
        repo.write(ROSTER, text)
    refused(repo, capsys, "--by", "Ann Lee", "--seat", seat, "--checked", ALL)
    reads(repo, capsys, "failed", rs301(6, "Statement"))


@pytest.mark.parametrize("requirements, design", [(5, 4), (7, 2), (12, 12)])
def test_sc1_1_the_signature_names_the_revision_of_each_document_of_a_pair(
        repo, capsys, requirements, design):
    repo.requirements(requirements)
    repo.design(design)
    assert passing(capsys)[0] == 0
    record = repo.last()
    assert record["requirements"] == f"r{requirements}"
    assert record["design"] == f"r{design}"
    is_green(repo, capsys)


def test_sc1_1_a_feature_with_one_document_records_requirements_alone(repo, capsys):
    repo.remove(DESIGN)
    assert passing(capsys) == (0, f"{PASSED}\n{RECORDED}\n", "")
    record = repo.last()
    assert list(record) == ["condition", "at", "head", "by", "seat", "requirements",
                            "items"]
    assert record["requirements"] == "r5"
    is_green(repo, capsys)


READY_5 = row("r6: Ready: contract validates ready-green, derived from r5", by="intake")
TEXT_5 = row("r5: the text")
LATER = row("r99: a later text")  # the document moved on; the contract did not

# A document's first table, and the revision its newest `Ready:` row names
# as the one the contract is derived from; None when no row names one.
# `tree.drift` reads the same table today, and each case holds the two
# readings equal.
TABLES = [
    pytest.param(TITLE + HEAD + TEXT_5 + READY_5, "r5", id="one-ready-row"),
    pytest.param(TITLE + HEAD + TEXT_5 + READY_5 + row("r7: more text")
                 + row("r8: Ready: validates again, derived from r7"), "r7",
                 id="the-newest-ready-row-wins"),
    pytest.param(TITLE + HEAD + row("r8: Ready: validates again, derived from r7")
                 + TEXT_5 + READY_5, "r7", id="the-newest-by-its-number-not-its-place"),
    pytest.param(TITLE + HEAD + row("r6: Ready: derived from r3") + READY_5, "r5",
                 id="the-lower-row-wins-a-tie"),
    pytest.param(TITLE + HEAD + TEXT_5 + READY_5 + row("r8: Ready: validates again"), "r5",
                 id="the-newest-ready-row-that-names-one"),
    pytest.param(TITLE + HEAD + row("r6: Ready: derived from r5, its design derived from r4"),
                 "r5", id="the-first-revision-a-row-names"),
    pytest.param(TITLE + HEAD + row("r6: Ready: derived from r05"), "r5",
                 id="a-leading-zero-in-the-table"),
    pytest.param(TITLE + HEAD + row("r6:    Ready: derived from r5"), "r5",
                 id="blanks-after-the-rows-number"),
    pytest.param(TITLE + HEAD + row("r6: Ready: a \\| b, derived from r5"), "r5",
                 id="a-pipe-after-a-backslash"),
    pytest.param(TITLE + HEAD + "| 2026-10-07 | intake | r6: Ready: derived from r5\n", "r5",
                 id="a-row-with-no-closing-pipe"),
    pytest.param("\ufeff" + TITLE + HEAD + TEXT_5 + READY_5, "r5", id="a-byte-order-mark"),
    pytest.param((TITLE + HEAD + TEXT_5 + READY_5).replace("\n", "\r\n"), "r5", id="crlf"),
    pytest.param(TITLE + HEAD + TEXT_5, None, id="no-ready-row"),
    pytest.param(TITLE + HEAD + TEXT_5 + row("r6: Ready: validates ready-green"), None,
                 id="a-ready-row-that-names-no-revision"),
    pytest.param(TITLE + HEAD + row("r6: Ready: derived from r5x"), None,
                 id="a-word-after-the-digits"),
    pytest.param(TITLE + HEAD + row("r6: Ready: Derived From r5"), None,
                 id="derived-from-in-another-case"),
    pytest.param(TITLE + HEAD + row("r6: ready: derived from r5"), None,
                 id="ready-in-another-case"),
    pytest.param(TITLE + HEAD + row("r6: now Ready: derived from r5"), None,
                 id="ready-not-at-the-rows-start"),
    pytest.param(TITLE + HEAD + row("Ready: derived from r5"), None,
                 id="a-ready-row-with-no-number"),
    pytest.param(TITLE + HEAD + TEXT_5 + "\nWords.\n\n" + HEAD + READY_5, None,
                 id="a-ready-row-in-a-second-table"),
    pytest.param(TITLE + "Words: Ready: derived from r5\n", None, id="no-table"),
    pytest.param("", None, id="an-empty-file"),
    pytest.param((TITLE + HEAD + TEXT_5 + READY_5).encode("utf-8") + b"\xff\xfe\n", None,
                 id="not-utf8"),
]


def moved_on(text):
    """The table with a later text row at its end: `tree.drift` then names
    the contract's revision in its stale mark."""
    if isinstance(text, bytes):
        return text
    return text + LATER.replace("\n", "\r\n" if "\r\n" in text else "\n")


@pytest.mark.parametrize("text, revision", TABLES)
@pytest.mark.parametrize("doc", [REQUIREMENTS, DESIGN])
def test_sc1_1_the_revision_is_the_one_the_newest_ready_row_names(
        repo, capsys, doc, text, revision):
    assert drawn(capsys)[0] == 1
    path = repo.write(doc, moved_on(text))
    key, other = ("requirements", "design") if doc == REQUIREMENTS else ("design", "requirements")
    mark = tree.drift(path)
    if revision is None:
        assert mark == tree.NO_READY
        refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", ALL,
                names=(doc,))
        reads(repo, capsys, "failed", rs301(6, "Statement"))
    else:
        assert mark == f"stale: document r99, contract from {revision}"
        assert passing(capsys) == (0, f"{PASSED}\n{RECORDED}\n", "")
        record = repo.last()
        assert record[key] == revision
        assert record[other] == ("r4" if key == "requirements" else "r5")
        is_green(repo, capsys)


def test_sc1_1_a_feature_with_no_feature_document_cannot_be_reviewed(repo, capsys):
    """The design document alone is no feature document."""
    assert passing(capsys)[0] == 0
    is_green(repo, capsys)
    repo.remove(REQUIREMENTS)
    refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", ALL,
            names=(REQUIREMENTS,))
    reads(repo, capsys, "to do")
    repo.remove(DESIGN)
    refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", ALL,
            names=(REQUIREMENTS,))
    reads(repo, capsys, "to do")


@pytest.mark.parametrize("doc", [REQUIREMENTS, DESIGN])
def test_sc1_1_a_passing_review_reads_to_do_once_a_document_names_no_revision(
        repo, capsys, doc):
    assert passing(capsys)[0] == 0
    is_green(repo, capsys)
    repo.write(doc, TITLE + HEAD + TEXT_5)
    reads(repo, capsys, "to do")
    refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", ALL, names=(doc,))
    reads(repo, capsys, "to do")


# --- the calls the writer cannot use, in the words the kit prints today ---


def test_sc1_1_an_id_with_no_contract_is_refused_in_todays_words(repo, capsys):
    assert passing(capsys)[0] == 0
    repo.requirements(3, OTHER)
    before = repo.files()
    assert passing(capsys, feature=OTHER) == (
        2, "", f"{OTHER}: no contract at specs/{OTHER}/contract.yaml\n")
    assert repo.files() == before


@pytest.mark.parametrize("config", [
    {"active_gates": ["G0"]},
    {"active_gates": ["G0", "G1"], "g1": {"exempt": [ID]}},
], ids=["g1-is-no-active-gate", "the-feature-is-exempt"])
def test_sc1_1_a_feature_g1_is_not_active_for_is_refused_in_todays_words(
        repo, capsys, config):
    assert passing(capsys)[0] == 0
    repo.write(".sdlc/config.yaml", yaml.safe_dump(config))
    before = repo.files()
    assert passing(capsys) == (2, "", f"{ID}: G1 is not active\n")
    assert repo.files() == before


# Reading 4: a contract the writer cannot read, as `g1-record model` refuses it.
CONTRACT_REFUSED = [
    pytest.param("id: [apply-discount\n", id="no-yaml"),
    pytest.param("- api/\n- src/\n", id="a-yaml-list"),
    pytest.param(CONTRACT.format(id=ID).replace("scope:\n  - api/\n  - src/\n", ""),
                 id="no-scope"),
    pytest.param(CONTRACT.format(id=ID).replace("scope:\n  - api/\n  - src/\n",
                                                "scope: api/\n"), id="scope-is-a-text"),
    pytest.param(CONTRACT.format(id=ID).replace("scope:\n  - api/\n  - src/\n",
                                                "scope: []\n"), id="scope-holds-no-entry"),
]


@pytest.mark.parametrize("text", CONTRACT_REFUSED)
def test_sc1_1_a_contract_that_cannot_be_read_is_refused_as_model_refuses_it(
        repo, capsys, text):
    assert passing(capsys)[0] == 0
    repo.write(f"specs/{ID}/contract.yaml", text)
    line = refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", ALL,
                   names=(f"specs/{ID}/contract.yaml",))
    assert line.startswith(f"{ID}: ")
    code, _, err = cli(capsys, "g1-record", "model", ID)
    assert (code, err.splitlines()) == (2, [line])


RECORD_REFUSED = [
    pytest.param("- condition: G1.3\n", "not a mapping", id="a-yaml-list"),
    pytest.param("records: none\n", "records is not a list", id="records-is-no-list"),
    pytest.param("records:\n  - condition: [G1.3\n", None, id="no-yaml"),
]


@pytest.mark.parametrize("text, reason", RECORD_REFUSED)
def test_sc1_1_a_record_file_that_cannot_be_read_is_refused_in_todays_words(
        repo, capsys, text, reason):
    assert passing(capsys)[0] == 0
    repo.write(RECORD, text)
    if reason is None:  # the line YAML's own error names, from 1
        with pytest.raises(yaml.YAMLError) as caught:
            yaml.safe_load(text)
        reason = f"YAML error at line {caught.value.problem_mark.line + 1}"
    before = repo.files()
    assert passing(capsys) == (
        2, "", f"taskcontract g1-record: unreadable record: {RECORD} ({reason})\n")
    assert repo.files() == before


def test_sc1_1_each_review_appends_one_record_and_keeps_the_ones_before(repo, capsys):
    lint = {"condition": "G1.1", "at": "2026-10-07T14:02:11Z", "head": "8635064",
            "tool": "spectral", "tool_version": "6.11.0", "installed": True,
            "pin": {"path": ".spectral.yaml", "sha256": "9f2c"},
            "files": [{"path": "api/openapi.yaml", "sha256": "41d0", "reported": 0}]}
    repo.put(lint)
    assert drawn(capsys)[0] == 1
    assert passing(capsys)[0] == 0
    records = repo.records()
    assert records[0] == lint
    assert [r["condition"] for r in records] == ["G1.1", "G1.3", "G1.3"]
    assert [[e["checked"] for e in r["items"]].count(False) for r in records[1:]] == [1, 0]
    text = (repo.root / RECORD).read_bytes()
    assert b"\r" not in text and text.endswith(b"\n")


# --- SC1.2: each unchecked item is a diagnostic under G1.3 ---


def test_sc1_2_the_designs_drawn_call_prints_its_two_lines_and_exits_1(repo, capsys):
    assert drawn(capsys) == (
        1, f"G1.3: item 6 Consistent is unchecked in Statement\n{RECORDED}\n", "")
    held = repo.last()["items"]
    assert held == items({6: "Statement"})
    assert list(held[5]) == ["n", "name", "checked", "section"]
    assert (repo.last()["by"], repo.last()["seat"]) == ("Ann Lee", "po")


def test_sc1_2_each_unchecked_item_is_an_rs301_line_under_g1_3_by_item_number(
        repo, capsys):
    code, out, err = signed(capsys, "--unchecked", "9=Checks", "--checked",
                            but(2, 8, 9), "--unchecked", "2=Statement",
                            "--unchecked", "8=Error messages")
    messages = [rs301(2, "Statement"), rs301(8, "Error messages"), rs301(9, "Checks")]
    assert messages[1] == "G1.3: item 8 Boundary + error paths is unchecked in Error messages"
    assert (code, out.splitlines(), err) == (1, [*messages, RECORDED], "")
    assert repo.last()["items"] == items({2: "Statement", 8: "Error messages", 9: "Checks"})
    before = repo.files()
    reads(repo, capsys, "failed", *messages)
    assert "RS301" in g1_rules()["G1.3"]
    assert repo.files() == before, "g1-check wrote under the root"


def test_sc1_2_the_json_envelope_holds_one_finding_for_each_unchecked_item(repo, capsys):
    assert signed(capsys, "--checked", but(2, 9), "--unchecked", "9=Checks",
                  "--unchecked", "2=Statement")[0] == 1
    code, out, err = check(repo, capsys, "--json")
    assert (code, err) == (1, "")
    assert json.loads(out) == {
        "note": "G1.1 done, G1.2 done, G1.3 failed",
        "findings": [
            {"feature": ID, "condition": "G1.3", "rule": "RS301",
             "message": rs301(2, "Statement")},
            {"feature": ID, "condition": "G1.3", "rule": "RS301",
             "message": rs301(9, "Checks")}]}


def test_sc1_2_a_review_with_every_item_unchecked_takes_no_checked_flag(repo, capsys):
    code, out, err = signed(capsys, *EVERY_UNCHECKED)
    messages = [rs301(n, "Statement") for n in range(1, 12)]
    assert (code, out.splitlines(), err) == (1, [*messages, RECORDED], "")
    reads(repo, capsys, "failed", *messages)


# The `<n>=<section>` pair: cut at its first `=`; the number is read as an
# element of `--checked` is, and the section is kept as the person wrote
# it, with its outer whitespace cut. No section is held against a heading.
PAIR_KEPT = [
    pytest.param("6=Statement", "Statement", id="plain"),
    pytest.param("6= Statement ", "Statement", id="outer-spaces-cut"),
    pytest.param("6=\tStatement\t", "Statement", id="outer-tabs-cut"),
    pytest.param(" 6 =Statement", "Statement", id="spaces-around-the-number"),
    pytest.param("6=Acceptance criteria, Checks", "Acceptance criteria, Checks",
                 id="a-comma-inside"),
    pytest.param("6=a=b", "a=b", id="an-equals-sign-inside"),
    pytest.param("6=7=Statement", "7=Statement", id="a-second-pair-inside"),
    pytest.param("6=statement", "statement", id="lower-case-kept"),
    pytest.param("6=STATEMENT", "STATEMENT", id="capitals-kept"),
    pytest.param("6=Risks  and   cost", "Risks  and   cost", id="inner-spaces-kept"),
    pytest.param("6=No such heading anywhere", "No such heading anywhere",
                 id="no-heading-of-that-name"),
    pytest.param("6=6", "6", id="digits-stay-text"),
    pytest.param("6=null", "null", id="yamls-null-stays-text"),
    pytest.param("6=true", "true", id="yamls-true-stays-text"),
    pytest.param("6=# Statement", "# Statement", id="a-hash"),
    pytest.param("6=key: value", "key: value", id="a-colon"),
    pytest.param("6='quoted'", "'quoted'", id="quotes"),
    pytest.param("6=- a dash", "- a dash", id="a-dash"),
    pytest.param("6=[x] {y} |z >w", "[x] {y} |z >w", id="yamls-marks"),
    pytest.param("6=Crit\u00e8res \u00ab \u00e9 \u00bb", "Crit\u00e8res \u00ab \u00e9 \u00bb",
                 id="not-ascii"),
]


@pytest.mark.parametrize("pair, section", PAIR_KEPT)
def test_sc1_2_the_diagnostic_names_the_item_and_the_section_as_the_person_named_it(
        repo, capsys, pair, section):
    message = f"G1.3: item 6 Consistent is unchecked in {section}"
    assert signed(capsys, "--checked", BUT_6, "--unchecked", pair) == (
        1, f"{message}\n{RECORDED}\n", "")
    entry = repo.last()["items"][5]
    assert entry == {"n": 6, "name": "Consistent", "checked": False, "section": section}
    assert isinstance(entry["section"], str)
    reads(repo, capsys, "failed", message)


# (the pair, the items `--checked` holds beside it)
PAIR_REFUSED = [
    pytest.param("", BUT_6, id="empty"),
    pytest.param("6", BUT_6, id="no-equals-sign"),
    pytest.param("6=", BUT_6, id="no-section"),
    pytest.param("6=   ", BUT_6, id="a-section-of-spaces"),
    pytest.param("6=\t", BUT_6, id="a-section-of-a-tab"),
    pytest.param("6=\u3000", BUT_6, id="a-section-of-an-ideographic-space"),
    # a text with no letter and no digit names no section
    pytest.param("6==", BUT_6, id="a-section-of-an-equals-sign"),
    pytest.param("6=\u200b", BUT_6, id="a-section-of-a-zero-width-space"),
    pytest.param("6=-", BUT_6, id="a-section-of-a-dash"),
    pytest.param("=Statement", BUT_6, id="no-number"),
    pytest.param(" =Statement", BUT_6, id="a-number-of-a-space"),
    pytest.param("6=\n", BUT_6, id="a-section-of-a-line-break"),
    pytest.param("6=Line\nbreak", BUT_6, id="a-line-break-inside"),
    pytest.param("6=Statement\n", BUT_6, id="a-line-break-at-the-end"),
    pytest.param("6=\nStatement", BUT_6, id="a-line-break-at-the-start"),
    pytest.param("6\n=Statement", BUT_6, id="a-line-break-after-the-number"),
    pytest.param("6=a\rb", BUT_6, id="a-carriage-return-inside"),
    pytest.param("6=a\u2028b", BUT_6, id="a-line-separator-inside"),
    pytest.param("6=a\x85b", BUT_6, id="a-next-line-inside"),
    pytest.param("6=a\x0bb", BUT_6, id="a-vertical-tab-inside"),
    pytest.param("6=a\x0cb", BUT_6, id="a-form-feed-inside"),
    pytest.param("06=Statement", BUT_6, id="leading-zero"),
    pytest.param("+6=Statement", BUT_6, id="plus-sign"),
    pytest.param("six=Statement", BUT_6, id="a-word-for-the-number"),
    pytest.param("Consistent=Statement", BUT_6, id="the-items-name-for-the-number"),
    pytest.param("\uff16=Statement", BUT_6, id="fullwidth-digit"),
    pytest.param("6,7=Statement", but(6, 7), id="two-numbers"),
    pytest.param("6-7=Statement", but(6, 7), id="a-range"),
    pytest.param("0=Statement", ALL, id="item-0"),
    pytest.param("12=Statement", ALL, id="item-12"),
    pytest.param("Statement=6", BUT_6, id="the-pair-turned-round"),
    pytest.param("6:Statement", BUT_6, id="a-colon-for-the-equals-sign"),
    pytest.param("6 Statement", BUT_6, id="a-space-for-the-equals-sign"),
]


@pytest.mark.parametrize("pair, checked", PAIR_REFUSED)
def test_sc1_2_a_pair_that_names_no_item_or_no_section_is_refused(
        repo, capsys, pair, checked):
    assert passing(capsys)[0] == 0
    refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", checked,
            "--unchecked", pair)
    is_green(repo, capsys)


def test_sc1_2_g1_3_reads_failed_until_a_later_review_passes_whatever_revision_follows(
        repo, capsys):
    assert drawn(capsys)[0] == 1
    reads(repo, capsys, "failed", rs301(6, "Statement"))
    repo.requirements(6)
    repo.design(5)
    reads(repo, capsys, "failed", rs301(6, "Statement"))
    assert passing(capsys) == (0, f"{PASSED}\n{RECORDED}\n", "")
    assert (repo.last()["requirements"], repo.last()["design"]) == ("r6", "r5")
    is_green(repo, capsys)


def test_sc1_2_a_later_review_that_leaves_an_item_unchecked_reads_failed_again(
        repo, capsys):
    assert passing(capsys)[0] == 0
    is_green(repo, capsys)
    assert signed(capsys, "--checked", but(3), "--unchecked", "3=Units")[0] == 1
    reads(repo, capsys, "failed", rs301(3, "Units"))


# --- SC1.3: the review holds G1.3's 11 items and no ready check ---


def test_sc1_3_the_review_holds_g1_3s_11_items_and_takes_no_ready_check(repo, capsys):
    """Ready checks run 1 to 15: a review takes no item 12 to 15, checked or
    not, and its record holds the 11 names of the items file and no other."""
    assert passing(capsys)[0] == 0
    listed = yaml.safe_load(ITEMS_FILE.read_text(encoding="utf-8"))["items"]
    assert [(e["n"], e["name"]) for e in repo.last()["items"]] == [
        (e["n"], e["name"]) for e in listed]
    assert len(listed) == 11
    for n in (12, 13, 14, 15):
        refused(repo, capsys, "--by", "Ann Lee", "--seat", "po",
                "--checked", f"{ALL},{n}", names=(str(n),))
        refused(repo, capsys, "--by", "Ann Lee", "--seat", "po", "--checked", ALL,
                "--unchecked", f"{n}=Statement", names=(str(n),))
    assert len(repo.records()) == 1


# --- done_means: G1.3 reads done only from a review with a signature ---


def test_done_means_g1_check_prints_the_summary_line_with_no_review_and_g1_green_after_one(
        repo, capsys):
    """The advisory carried from s1-lint: both lines of `g1-check`."""
    assert check(repo, capsys) == (1, summary("to do") + "\n", "")
    code, out, err = check(repo, capsys, "--json")
    assert (code, json.loads(out), err) == (
        1, {"note": "G1.1 done, G1.2 done, G1.3 to do", "findings": []}, "")
    assert passing(capsys)[0] == 0
    assert check(repo, capsys) == (0, f"g1-green: {ID}\n", "")
    code, out, err = check(repo, capsys, "--json")
    assert (code, json.loads(out), err) == (
        0, {"note": "G1.1 done, G1.2 done, G1.3 done", "findings": []}, "")


def test_done_means_a_record_as_the_writer_writes_it_reads_done_from_any_folder(
        repo, capsys, tmp_path, monkeypatch):
    """`g1-check --root` reads the record and both documents under the root."""
    repo.put(written())
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    before = repo.files()
    is_green(repo, capsys)
    assert repo.files() == before
    assert list(elsewhere.iterdir()) == []


def test_done_means_the_last_review_counts(repo, capsys):
    repo.put(written({6: "Statement"}), written())
    is_green(repo, capsys)
    repo.put(written(), written({6: "Statement"}))
    reads(repo, capsys, "failed", rs301(6, "Statement"))
    repo.put(written(), written(by=""))
    reads(repo, capsys, "to do")
    repo.put(written(), written(items=items()[:10]))
    reads(repo, capsys, "to do")
    repo.put(written(), written({6: "Statement"}, by=ABSENT))
    reads(repo, capsys, "to do")


def test_done_means_a_review_of_another_feature_does_not_count(repo, capsys):
    repo.contract(OTHER)
    repo.requirements(5, OTHER)
    repo.design(4, OTHER)
    assert passing(capsys, feature=OTHER)[0] == 0
    assert check(repo, capsys, feature=OTHER) == (0, f"g1-green: {OTHER}\n", "")
    reads(repo, capsys, "to do")
    assert not (repo.root / RECORD).exists()


def change(**keys):
    return lambda record: record.update(keys)


def drop(key):
    return lambda record: record.pop(key)


def item(place: int, /, **keys):
    """Change the entry of the item at that place; ABSENT leaves a key out."""
    def apply(record):
        entry = record["items"][place - 1]
        for key, value in keys.items():
            if value is ABSENT:
                entry.pop(key)
            else:
                entry[key] = value
    return apply


def entries(edit):
    return lambda record: edit(record["items"])


# A G1.3 record changed by hand so that it holds no signature over each of
# the 11 items once: it counts as absent, so G1.3 reads `to do`.
RECORD_AS_ABSENT = [
    pytest.param(drop("by"), id="no-by"),
    pytest.param(change(by=""), id="by-empty"),
    pytest.param(change(by="   "), id="by-of-spaces"),
    pytest.param(change(by="Ann\nLee"), id="by-with-a-line-break"),
    pytest.param(change(by=None), id="by-null"),
    pytest.param(change(by=7), id="by-a-number"),
    pytest.param(change(by=True), id="by-a-boolean"),
    pytest.param(change(by=["Ann Lee"]), id="by-a-list"),
    pytest.param(change(by={"name": "Ann Lee"}), id="by-a-mapping"),
    pytest.param(change(by="​"), id="by-of-a-zero-width-space"),
    pytest.param(change(by="-"), id="by-of-a-dash"),
    pytest.param(drop("seat"), id="no-seat"),
    pytest.param(change(seat=""), id="seat-empty"),
    pytest.param(change(seat=" "), id="seat-of-a-space"),
    pytest.param(change(seat="po\nengineer"), id="seat-with-a-line-break"),
    pytest.param(change(seat=None), id="seat-null"),
    pytest.param(change(seat=7), id="seat-a-number"),
    pytest.param(change(seat=["po"]), id="seat-a-list"),
    pytest.param(change(condition="g1.3"), id="condition-in-another-case"),
    pytest.param(change(condition="G1.3 "), id="condition-with-a-space-after"),
    pytest.param(drop("items"), id="no-items"),
    pytest.param(change(items=None), id="items-null"),
    pytest.param(change(items={}), id="items-a-mapping"),
    pytest.param(change(items=[]), id="items-empty"),
    pytest.param(change(items="1,2,3,4,5,6,7,8,9,10,11"), id="items-a-text"),
    pytest.param(change(items=list(range(1, 12))), id="items-a-list-of-numbers"),
    pytest.param(entries(lambda held: held.pop()), id="ten-items"),
    pytest.param(entries(lambda held: held.pop(0)), id="no-item-1"),
    pytest.param(entries(lambda held: held.append(dict(held[2]))), id="item-3-twice"),
    pytest.param(entries(lambda held: held.append(
        {"n": 12, "name": "Signed", "checked": True})), id="an-item-12"),
    pytest.param(item(4, n=3, name="Traceable"), id="item-3-in-the-place-of-item-4"),
    pytest.param(item(11, n=0), id="an-item-0-for-item-11"),
    pytest.param(item(1, n="1"), id="a-number-as-a-text"),
    pytest.param(item(1, n=True), id="a-boolean-for-item-1"),
    pytest.param(item(1, n=1.0), id="a-decimal-for-item-1"),
    pytest.param(item(1, n=None), id="a-null-number"),
    pytest.param(item(1, n=ABSENT), id="no-number"),
    pytest.param(entries(lambda held: held.__setitem__(0, "1")), id="an-entry-that-is-a-text"),
    pytest.param(entries(lambda held: held.__setitem__(0, None)), id="an-entry-that-is-null"),
    pytest.param(item(6, checked=ABSENT), id="no-checked"),
    pytest.param(item(6, checked=None), id="checked-null"),
    pytest.param(item(6, checked="true"), id="checked-a-text"),
    pytest.param(item(6, checked="yes"), id="checked-the-word-yes"),
    pytest.param(item(6, checked=1), id="checked-a-number"),
    pytest.param(item(6, checked=[True]), id="checked-a-list"),
    pytest.param(item(6, name=ABSENT), id="no-name"),
    pytest.param(item(6, name="Testable"), id="another-items-name"),
    pytest.param(item(6, name="consistent"), id="the-name-in-another-case"),
    pytest.param(item(6, name="Consistent "), id="the-name-with-a-space-after"),
    pytest.param(item(6, checked=False), id="unchecked-with-no-section"),
    pytest.param(item(6, checked=False, section=""), id="unchecked-in-an-empty-section"),
    pytest.param(item(6, checked=False, section="  "), id="unchecked-in-a-section-of-spaces"),
    pytest.param(item(6, checked=False, section="a\nb"),
                 id="unchecked-in-a-section-with-a-line-break"),
    pytest.param(item(6, checked=False, section="​"),
                 id="unchecked-in-a-section-of-a-zero-width-space"),
    pytest.param(item(6, checked=False, section=7), id="unchecked-in-a-number"),
    pytest.param(item(6, checked=False, section=None), id="unchecked-in-null"),
    pytest.param(item(6, checked=False, section=["Statement"]), id="unchecked-in-a-list"),
]


@pytest.mark.parametrize("edit", RECORD_AS_ABSENT)
def test_done_means_a_record_with_no_signature_over_each_item_once_counts_as_absent(
        repo, capsys, edit):
    record = written()
    repo.put(record)
    is_green(repo, capsys)
    changed = copy.deepcopy(record)
    edit(changed)
    repo.put(changed)
    reads(repo, capsys, "to do")
    code, out, _ = check(repo, capsys, "--json")
    assert (code, json.loads(out)) == (
        1, {"note": "G1.1 done, G1.2 done, G1.3 to do", "findings": []})


def test_done_means_the_items_of_a_record_count_in_any_order(repo, capsys):
    """A record holds each item once; the diagnostics come by item number."""
    held = items({2: "Statement", 9: "Checks"})
    repo.put(written(items=held[::-1]))
    reads(repo, capsys, "failed", rs301(2, "Statement"), rs301(9, "Checks"))
    repo.put(written(items=items()[::-1]))
    is_green(repo, capsys)


# The revision a record names, held against a document whose `Ready:` row
# names r5: only the text `r5` counts.
REVISION_NOT_R5 = [
    pytest.param(ABSENT, id="absent"),
    pytest.param(None, id="null"),
    pytest.param("", id="empty"),
    pytest.param("r5\n", id="a-line-break-after"),
    pytest.param("r5,r4", id="a-comma-inside"),
    pytest.param("r5=r5", id="an-equals-sign-inside"),
    pytest.param("r5 r5", id="a-repeat"),
    pytest.param(["r5"], id="a-list"),
    pytest.param(["r5", "r5"], id="a-list-with-a-repeat"),
    pytest.param("R5", id="a-capital"),
    pytest.param(" r5", id="a-space-before"),
    pytest.param("r5 ", id="a-space-after"),
    pytest.param("r05", id="a-leading-zero"),
    pytest.param("5", id="the-digits-alone"),
    pytest.param(5, id="a-number"),
    pytest.param(True, id="a-boolean"),
    pytest.param("r4", id="an-older-revision"),
    pytest.param("r6", id="a-later-revision"),
    pytest.param("r", id="no-digits"),
    pytest.param("r5.0", id="a-decimal"),
    pytest.param("\uff525", id="a-fullwidth-letter"),
]


@pytest.mark.parametrize("named", REVISION_NOT_R5)
@pytest.mark.parametrize("key", ["requirements", "design"])
def test_done_means_a_passing_review_on_other_revisions_reads_to_do(
        repo, capsys, key, named):
    repo.requirements(5)
    repo.design(5)
    repo.put(written(design="r5"))
    is_green(repo, capsys)
    repo.put(written(**{"design": "r5", key: named}))
    reads(repo, capsys, "to do")


@pytest.mark.parametrize("doc", ["requirements", "design"])
def test_done_means_a_passing_review_reads_to_do_once_the_contract_is_derived_again(
        repo, capsys, doc):
    assert passing(capsys)[0] == 0
    is_green(repo, capsys)
    getattr(repo, doc)(8)
    reads(repo, capsys, "to do")
    assert passing(capsys)[0] == 0
    assert repo.last()[doc] == "r8"
    is_green(repo, capsys)


def test_done_means_a_review_that_names_a_design_revision_does_not_count_for_one_document(
        repo, capsys):
    assert passing(capsys)[0] == 0
    is_green(repo, capsys)
    repo.remove(DESIGN)
    reads(repo, capsys, "to do")
    assert passing(capsys)[0] == 0
    assert "design" not in repo.last()
    is_green(repo, capsys)


def test_done_means_a_review_of_one_document_does_not_count_for_a_pair(repo, capsys):
    repo.remove(DESIGN)
    assert passing(capsys)[0] == 0
    is_green(repo, capsys)
    repo.design(4)
    reads(repo, capsys, "to do")
    repo.put(written(design=ABSENT))
    reads(repo, capsys, "to do")
    repo.put(written())
    is_green(repo, capsys)


@pytest.mark.parametrize("text", [
    "- condition: G1.3\n", "records: none\n", "records:\n  - condition: [G1.3\n", "",
], ids=["a-yaml-list", "records-is-no-list", "no-yaml", "an-empty-file"])
def test_done_means_a_record_file_that_cannot_be_read_counts_as_absent(repo, capsys, text):
    assert passing(capsys)[0] == 0
    is_green(repo, capsys)
    repo.write(RECORD, text)
    reads(repo, capsys, "to do")
