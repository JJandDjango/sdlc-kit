"""G1.1's lint record, G1.2's model record, G1.3's review record, their
writers and the G1 verdict (ADR 0038).

Contract: g1-requirements-spec. G1's rules read records, in their own
command, and no G1 rule reports through `validate`. This module holds the
writers of a lint record, of a model record and of a review record,
`g1-record lint`, `g1-record model` and `g1-record review`, and the
reader, `g1-check`.

G1 is active for a feature when .sdlc/config.yaml lists `G1` under
`active_gates` and its `g1.exempt` list does not name the feature. The
`g1.schemas` entries of that file declare the boundary schemas, each
pattern with its linter and its pin. A schema is in scope when its path
from the root matches one pattern of an entry and one entry of `scope` in
specs/<id>/contract.yaml, each read as `scope_check.matches` reads a scope
entry. A declaration that cannot be read counts as absent for `g1-check`,
and `g1-record lint` refuses it.

`g1-record lint <id>` starts the entry's linter once for each schema in
scope and appends one record to .sdlc/g1/<id>.yaml, a committed file: the
tool, its version, the pin's hash, and each file's hash beside the number
of errors and warnings the tool reported. Every check it makes comes
first, so a refused call writes nothing and starts no tool. Exit 0 when
the record reads clean or no schema is in scope, 1 when a file does not
lint clean or the tool is not installed, 2 on a call it cannot use and
when the tool ends on an error of its own.

specs/components.yaml is the component declaration record, read under
schemas/component-declaration.schema.json: one entry the schema refuses
makes the whole declaration unreadable. A hard core is in scope when one
of its `paths` and one entry of the contract's `scope` overlap, read from
the two texts alone and never from the files on disk. It is out of scope
only when no path could fall under both entries of each such pair: the
texts cannot tell a file from a folder, and a wildcard crosses a slash,
so each doubt counts the hard core in. Letter case is ignored, and an
entry the kit cannot read plainly counts as overlapping: one with a
doubled slash, a `.` or `..` segment, white space at a segment's end, or
a drive. A link from one folder to another is not seen, since nothing is
read from disk. It has no model when its entry
holds no `model` or the model's file is absent.

`g1-record model <id>` starts the declared checker on the model of each
hard core in scope and appends one record: for each hard core that has a
model, the tool, the model's and the configuration's hashes, and `pass`
or `fail`. `tlc` runs once, inside the model's folder, with a working
folder of its own outside the repository that the call removes; `p`
reads the words of the configuration's file, compiles the project and
then checks it with those words. The exit code is the result: 0 passes,
and a code by which the checker says its search found a violation fails.
Every check comes first here too, and nothing is printed or written
before every tool has run. A contract whose scope cannot be read is
refused. Exit 0 when each hard core in scope has a model that passes or
no hard core is in scope, 1 when one has no model, one does not pass or
a checker is not installed, 2 on a call it cannot use, when a tool ends
on an error of its own, and when a configuration cannot be read or
`tlc`'s working folder cannot be made.

G1.3's 11 items, each a number and a name, stand in data/g1-items.yaml.
The revision a contract was derived from is read from the first table of
docs/features/<id>.md, the requirements document, and of
docs/features/<id>.design.md, the design document, when that file is
there: the `Ready:` row with the highest N that names a `derived from
rM` gives it, the lower row winning a tie.

`g1-record review <id>` appends one record of a named person's answers:
the signer's name and seat, the revision each document's `Ready:` row
names, and each of the 11 items as checked, or as unchecked with the
section it concerns. `--by` and `--seat` are each given once, the seat a
value of the ratified `intake-seat` term, and `--checked` and
`--unchecked` name each item once between them. Every check comes first,
so a refused call writes nothing. Exit 0 when the review checks all 11
items, 1 when it leaves one unchecked, 2 on a call it cannot use: a
contract whose scope cannot be read, a name that names no person, a seat
the term does not hold, an item named twice or not at all, or a document
that names no revision.

`g1-check <id>` reads the declarations, the last G1.1 record, the last
G1.2 record, the last G1.3 record and the files on disk; it runs no tool
and writes nothing. The files on disk win: a record whose hashes no
longer match counts as absent, and so does a review that names other
revisions than the documents' `Ready:` rows name now. It reports:

  RS101  the record found the linter not installed
  RS102  a schema in scope is recorded with one error or warning, or more
  RS201  a hard core in scope has no model
  RS202  the record found the checker not installed
  RS203  the model of a hard core in scope is recorded as not passing
  RS301  the last review leaves an item unchecked

A condition reads `failed` when one of its rules reports, else `done` when
everything it needs is present and current, else `to do`. Exit 0 when the
three conditions read `done`, 1 when they do not, 2 when the id has no
contract or G1 is not active for the feature. `--json` emits the
note+findings envelope.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from .progress import head_id
from .scope_check import contract_scope, in_any, matches

G1_DIR = Path(".sdlc") / "g1"
COMPONENTS = Path("specs") / "components.yaml"
COMPONENT_SCHEMA = (Path(__file__).resolve().parent / "schemas"
                    / "component-declaration.schema.json")
ITEMS_PATH = Path(__file__).resolve().parent / "data" / "g1-items.yaml"
FEATURES = Path("docs") / "features"
SEAT_TERM = Path("specs") / "vocabulary" / "intake-seat.yaml"
GATE = "G1"
LINT = "G1.1"
MODEL = "G1.2"
REVIEW = "G1.3"
LINTERS = ("spectral", "buf")
TO_DO, DONE, FAILED = "to do", "done", "failed"
PASS, FAIL = "pass", "fail"
PROG = "taskcontract g1-record"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
COUNTED = (0, 1)  # Spectral's severities for an error and a warning
# the exit codes by which a checker says its search found a violation
VIOLATION = {"tlc": (10, 11, 12, 13, 14), "p": (1,)}

NO_SCHEMA = "G1.1: no boundary schema in scope"
NOT_INSTALLED = "G1.1: {tool} is not installed; install it and pin it in the repository"
NOT_CLEAN = "G1.1: {file} does not lint clean: {tool} reports {n}"
CLEAN = "G1.1: {file} lints clean under {tool}"

NO_HARD_CORE = "G1.2: no hard core in scope"
NO_MODEL = "G1.2: hard core {component} has no model"
NO_CHECKER = "G1.2: {tool} is not installed; install it and pin it in the repository"
NOT_PASSING = "G1.2: the model of {component} does not pass {tool}"
PASSING = "G1.2: the model of {component} passes {tool}"

UNCHECKED = "G1.3: item {n} {item} is unchecked in {section}"
ALL_CHECKED = "G1.3: the review checks all {count} items"

# A feature document's revision table, read as `tree.drift` reads it: a
# pipe after a backslash never splits a cell; a counted row's last cell
# opens on `r<N>:`, and a `Ready:` row names its `rM` by the first
# `derived from rM`, the digits ending at a non-word.
_PIPE = re.compile(r"(?<!\\)\|")
_REVISION = re.compile(r"r([0-9]+):\s*")
_DERIVED = re.compile(r"derived from r([0-9]+)(?!\w)")


@dataclass(frozen=True)
class Schema:
    """One schema in scope: its path from the root, and the linter, the pin
    and the position of the `g1.schemas` entry that declares it."""

    path: str
    linter: str
    pin: str
    entry: int


@dataclass(frozen=True)
class Finding:
    feature: str
    condition: str
    rule: str
    message: str

    @property
    def line(self) -> str:
        return f"{self.feature}: {self.rule} {self.message}"


class Unreadable(ValueError):
    """A record file or a declaration the writer refuses, with the reason
    it prints."""


def read_config(root: Path) -> dict:
    """.sdlc/config.yaml as a mapping; a missing or unreadable file is empty."""
    try:
        doc = yaml.safe_load((root / ".sdlc" / "config.yaml").read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError):  # a date no calendar holds is a ValueError
        return {}
    return doc if isinstance(doc, dict) else {}


def is_active(config: dict, feature_id: str) -> bool:
    """Whether G1 is active for the feature: listed under `active_gates`,
    and the feature not named by `g1.exempt`."""
    gates = config.get("active_gates")
    if not isinstance(gates, list) or GATE not in gates:
        return False
    section = config.get("g1")
    exempt = section.get("exempt") if isinstance(section, dict) else None
    return not (isinstance(exempt, list) and feature_id in [str(e) for e in exempt])


def schema_entries(config: dict) -> list[dict] | None:
    """The `g1.schemas` entries; None when the key is absent, which is not
    the empty list. Unreadable with the reason when the key holds no list,
    or one entry is no mapping that holds `paths`, a list of strings,
    `linter`, a string, and `pin`, a string that is not empty: one such
    entry makes the whole declaration unreadable."""
    section = config.get("g1")
    if not isinstance(section, dict) or "schemas" not in section:
        return None
    entries = section["schemas"]
    if not isinstance(entries, list):
        raise Unreadable("it is no list")
    for n, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise Unreadable(f"entry {n} is no mapping")
        paths = entry.get("paths")
        if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
            raise Unreadable(f"entry {n} holds no list of paths")
        if not isinstance(entry.get("linter"), str):
            raise Unreadable(f"entry {n} names no linter")
        if not isinstance(entry.get("pin"), str) or not entry["pin"]:
            raise Unreadable(f"entry {n} names no pin")
    return entries


def schemas_in_scope(root: Path, scope: list[str], entries: list[dict]) -> list[Schema]:
    """The files on disk that match a pattern of an entry and the contract's
    scope, ordered by path; a file two entries match belongs to the first."""
    found: dict[str, Schema] = {}
    for n, entry in enumerate(entries):
        pin = entry.get("pin")
        for pattern in entry["paths"]:
            for path in _files(root, str(pattern)):
                if path not in found and in_any(path, scope):
                    found[path] = Schema(path, str(entry.get("linter")),
                                         pin if isinstance(pin, str) else "", n)
    return [found[path] for path in sorted(found)]


def _files(root: Path, pattern: str) -> list[str]:
    """The files under the root that the pattern matches, each as its path
    from the root. The walk starts at the folder the pattern names before
    its first wildcard; `matches` decides. A pattern whose path the system
    refuses matches no file."""
    entry = pattern.strip().replace("\\", "/")
    if not entry:
        return []
    if entry.endswith("/"):
        base = entry.rstrip("/")
    else:
        cut = min((entry.index(c) for c in "*?[" if c in entry), default=None)
        if cut is None:
            return [entry] if _inside(entry) and _is_file(root / entry) else []
        base = entry[:cut].rpartition("/")[0]
    if not _inside(base):
        return []
    start = root / base if base else root
    try:
        walked = list(os.walk(start))
    except (OSError, ValueError):  # a folder that holds a NUL names none
        return []
    paths = []
    for folder, _, names in walked:
        under = Path(folder).relative_to(start).as_posix()
        parts = [part for part in (base, "" if under == "." else under) if part]
        for name in names:
            path = "/".join([*parts, name])
            if matches(path, entry):
                paths.append(path)
    return paths


def _inside(path: str) -> bool:
    """Whether a path from the root stays under the root."""
    return not Path(path).is_absolute() and not path.startswith("/") \
        and ".." not in path.split("/")


def _is_file(path: Path) -> bool:
    """Whether the path names a file on disk; a path the system refuses
    names none."""
    try:
        return path.is_file()
    except (OSError, ValueError):  # a name too long, or one that holds a NUL
        return False


def sha256_of(path: Path) -> str | None:
    """The whole SHA-256 of the file's bytes on disk; None when it cannot be read."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except (OSError, ValueError):  # a path that holds a NUL names no file
        return None


def last_record(root: Path, feature_id: str, condition: str) -> dict | None:
    """The last record of the condition in the feature's record file; a file
    that is absent or cannot be read counts as no record."""
    try:
        doc = yaml.safe_load((root / G1_DIR / f"{feature_id}.yaml").read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError):  # a date no calendar holds is a ValueError
        return None
    records = doc.get("records") if isinstance(doc, dict) else None
    if not isinstance(records, list):
        return None
    return next((r for r in reversed(records)
                 if isinstance(r, dict) and r.get("condition") == condition), None)


def read_lint(root: Path, feature_id: str, scope: list[str],
              config: dict) -> tuple[str, list[Finding]]:
    """G1.1's status and its findings, in path order.

    `to do` when `g1.schemas` is absent or cannot be read, `done` when no
    schema is in scope. Else each schema in scope is held against the last
    G1.1 record: it is matched when the record holds its path with the
    file's hash as it stands now, the entry's linter, and the entry's pin
    with the pin's hash as it stands now. A file entry whose path is no
    text is no recorded file. A pin's file that is absent
    reads as null on both sides, and null equals null. A matched schema
    reports RS101 when the record found the tool not installed, once for
    the tool, and RS102 when it reported above 0; a result whose pin's
    hash is null is no pinned result, so its schema is unmatched. With no
    report, one unmatched schema reads `to do`.
    """
    try:
        entries = schema_entries(config)
    except Unreadable:
        entries = None
    if entries is None:
        return TO_DO, []
    schemas = schemas_in_scope(root, scope, entries)
    if not schemas:
        return DONE, []
    record = last_record(root, feature_id, LINT) or {}
    pin = record.get("pin") if isinstance(record.get("pin"), dict) else {}
    files = record.get("files") if isinstance(record.get("files"), list) else []
    recorded = {f["path"]: f for f in files
                if isinstance(f, dict) and isinstance(f.get("path"), str)}
    findings: list[Finding] = []
    missing: set[str] = set()  # the tools RS101 has named
    unmatched = False
    for schema in schemas:
        held = recorded.get(schema.path)
        pin_hash = sha256_of(root / schema.pin) if schema.pin else None
        if (held is None or held.get("sha256") != sha256_of(root / schema.path)
                or record.get("tool") != schema.linter or pin.get("path") != schema.pin
                or pin.get("sha256") != pin_hash):
            unmatched = True
            continue
        count = held.get("reported")
        if record.get("installed") is False:
            if schema.linter not in missing:
                missing.add(schema.linter)
                findings.append(Finding(feature_id, LINT, "RS101",
                                        NOT_INSTALLED.format(tool=schema.linter)))
        elif pin_hash is None or not isinstance(count, int) or isinstance(count, bool):
            unmatched = True
        elif count > 0:
            findings.append(Finding(feature_id, LINT, "RS102", NOT_CLEAN.format(
                file=schema.path, tool=schema.linter, n=count)))
    if findings:
        return FAILED, findings
    return (TO_DO if unmatched else DONE), []


def components(root: Path) -> list[dict] | None:
    """The entries of specs/components.yaml; None when the file is absent,
    which is not the empty list. Unreadable with the reason when the file
    is no YAML or the declaration's schema refuses it: one such entry makes
    the whole declaration unreadable."""
    path = root / COMPONENTS
    if not path.exists():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        schema = json.loads(COMPONENT_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        raise Unreadable(getattr(exc, "strerror", None) or "cannot be read") from None
    except (yaml.YAMLError, ValueError) as exc:  # a date no calendar holds is a ValueError
        mark = getattr(exc, "problem_mark", None)
        raise Unreadable(f"YAML error at line {mark.line + 1}" if mark is not None
                         else "YAML error") from None
    error = next(iter(Draft202012Validator(schema).iter_errors(doc)), None)
    if error is not None:
        where = "/".join(str(part) for part in error.absolute_path)
        raise Unreadable(f"{where}: {error.message}" if where else error.message)
    return doc["components"]


def hard_cores_in_scope(scope: list[str], entries: list[dict]) -> list[dict]:
    """The hard cores one of whose paths overlaps one entry of the
    contract's scope, in the declaration's order. A hard core is left out
    only when no path could fall under both entries, for each such pair.
    Letter case is ignored, and an entry the kit cannot read plainly
    counts as overlapping. A link from one folder to another is not seen,
    since nothing is read from disk."""
    return [entry for entry in entries if entry["hard_core"]
            and any(_overlap(path, held) for path in entry["paths"] for held in scope)]


def _overlap(one: str, other: str) -> bool:
    """Whether two path entries overlap, read from the two texts alone:
    they do not only when no path could fall under both. The texts cannot
    tell a file from a folder, and a wildcard crosses a slash, so each
    doubt counts as an overlap. An entry the kit cannot read plainly
    overlaps every entry, the root among them. Letter case is ignored:
    the two texts are compared casefolded. Two entries with no wildcard
    overlap when they are equal or one is a folder that holds the other;
    an entry with none and one with a wildcard when the first starts with
    the second's text before its first wildcard, or is a folder that
    holds that text; two with a wildcard when that text of one starts
    with the other's. A link from one folder to another is not seen,
    since nothing is read from disk."""
    one, other = _path(one), _path(other)
    if not (_plain(one) and _plain(other)):
        return True
    one, other = one.casefold(), other.casefold()
    a, b = _literal(one), _literal(other)
    if _wild(one) and _wild(other):
        return a.startswith(b) or b.startswith(a)
    if _wild(one):
        return other.startswith(a) or a.startswith(other + "/")
    if _wild(other):
        return one.startswith(b) or b.startswith(one + "/")
    return one == other or one.startswith(other + "/") or other.startswith(one + "/")


def _entry(text: str) -> str:
    return text.strip().replace("\\", "/")


def _path(text: str) -> str:
    """The entry as the overlap rule reads it: with no leading `./` or
    `/` and no trailing `/`, and empty when it names the root."""
    entry = _entry(text)
    while entry.startswith(("./", "/")):
        entry = entry[2:] if entry.startswith("./") else entry[1:]
    entry = entry.rstrip("/")
    return "" if entry == "." else entry


def _plain(entry: str) -> bool:
    """Whether the overlap rule can read the entry from its text: it holds
    no `:`, so no drive, and split on `/` no segment is empty, `.` or
    `..`, or has white space at either end. The root is not plain."""
    return ":" not in entry and all(
        segment not in ("", ".", "..") and segment == segment.strip()
        for segment in entry.split("/"))


def _wild(entry: str) -> bool:
    return any(c in entry for c in "*?[")


def _literal(entry: str) -> str:
    """The entry's text before its first wildcard; the whole text when it
    has none."""
    return entry[:min((entry.index(c) for c in "*?[" if c in entry), default=len(entry))]


def _has_model(root: Path, core: dict) -> bool:
    """Whether the hard core's entry holds a `model` whose file is on disk;
    a path the system refuses reads as a file that is absent."""
    return "model" in core and _is_file(root / _entry(core["model"]))


def _pins(root: Path, core: dict) -> dict:
    """What a G1.2 record holds of a hard core that has a model, but for the
    result: the component, the tool, and the model and its configuration,
    each with its path and its file's hash as it stands now."""
    model, config = _entry(core["model"]), core["model_config"]
    return {
        "component": core["id"],
        "tool": core["checker"],
        "model": {"path": model, "sha256": sha256_of(root / model)},
        "config": {"path": config, "sha256": sha256_of(root / config)},
    }


def read_model(root: Path, feature_id: str,
               scope: list[str]) -> tuple[str, list[Finding]]:
    """G1.2's status and its findings, in the declaration's order.

    `to do` when specs/components.yaml is absent or cannot be read, or the
    contract holds no scope entry to read a hard core against; `done` when
    no hard core is in scope. Else each hard core in scope reports RS201
    when it has no model, whatever a record holds, and is else held
    against the last G1.2 record: it is matched when the record holds its
    component with the declared checker, and the declared model and
    configuration, each with its file's hash as it stands now. A
    configuration's file that is absent reads as null on both sides, and
    null equals null; a model whose file cannot be read is unmatched. A
    matched hard core reports RS202 when the record found the tool not
    installed, once for the tool, and RS203 when its result is `fail`; a
    result whose configuration's hash is null is no pinned result, and a
    result that is neither `pass` nor `fail` is none, so its hard core is
    unmatched. With no report, one unmatched hard core reads `to do`.
    """
    try:
        entries = components(root)
    except Unreadable:
        entries = None
    if entries is None or not scope:
        return TO_DO, []
    cores = hard_cores_in_scope(scope, entries)
    if not cores:
        return DONE, []
    record = last_record(root, feature_id, MODEL) or {}
    held = record.get("cores") if isinstance(record.get("cores"), list) else []
    findings: list[Finding] = []
    missing: set[str] = set()  # the tools RS202 has named
    unmatched = False
    for core in cores:
        if not _has_model(root, core):
            findings.append(Finding(feature_id, MODEL, "RS201",
                                    NO_MODEL.format(component=core["id"])))
            continue
        pins = _pins(root, core)
        tool = pins["tool"]
        entry = next((e for e in held if isinstance(e, dict)
                      and all(e.get(key) == value for key, value in pins.items())), None)
        if entry is None or pins["model"]["sha256"] is None:
            unmatched = True
        elif entry.get("installed") is False:
            if tool not in missing:
                missing.add(tool)
                findings.append(Finding(feature_id, MODEL, "RS202",
                                        NO_CHECKER.format(tool=tool)))
        elif entry.get("installed") is not True or pins["config"]["sha256"] is None:
            unmatched = True
        elif entry.get("result") == FAIL:
            findings.append(Finding(feature_id, MODEL, "RS203", NOT_PASSING.format(
                component=core["id"], tool=tool)))
        elif entry.get("result") != PASS:
            unmatched = True
    if findings:
        return FAILED, findings
    return (TO_DO if unmatched else DONE), []


def items() -> dict[int, str]:
    """G1.3's items from data/g1-items.yaml: each number with its name, in
    the file's order."""
    doc = yaml.safe_load(ITEMS_PATH.read_text(encoding="utf-8"))
    return {entry["n"]: entry["name"] for entry in doc["items"]}


def _one_line(value: str) -> bool:
    """Whether the text holds no line break, at any place, its ends
    included: `str.splitlines` decides what a line break is."""
    return not value or value.splitlines() == [value]


def _names(value) -> bool:
    """Whether the value is a text on one line that holds a letter or a
    digit: blanks, a dash or a zero-width space name no person and no
    section."""
    return (isinstance(value, str) and _one_line(value)
            and any(ch.isalnum() for ch in value))


def _ready_revision(path: Path) -> int | None:
    """The revision the document's contract was derived from, as
    `tree.drift` reads it: of the first table's `Ready:` rows that name a
    `derived from rM`, the one with the highest N gives M, the lower row
    winning a tie. None when the file cannot be read as text, holds no
    table or holds no such row."""
    try:
        lines = path.read_bytes().decode("utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    revision, newest, started = None, -1, False
    for line in lines:
        row = line.strip()
        if not row.startswith("|"):
            if started:  # only the first table is read
                break
            continue
        started = True
        if row.endswith("|") and not row.endswith("\\|"):
            row = row[:-1]
        cells = [cell.strip() for cell in _PIPE.split(row)[1:]]
        cell = cells[-1] if cells else ""
        match = _REVISION.match(cell)
        if match is None or not cell.startswith("Ready:", match.end()):
            continue
        derived = _DERIVED.search(cell, match.end())
        if derived is not None and int(match.group(1)) >= newest:
            newest, revision = int(match.group(1)), int(derived.group(1))
    return revision


def derived_from(root: Path, feature_id: str) -> dict[str, str]:
    """The revisions the contract was derived from, each as `r<M>`:
    `requirements` from docs/features/<id>.md and `design` from
    docs/features/<id>.design.md, a key the mapping holds only when that
    file is there. Unreadable with the reason when the requirements
    document is no file, or a document names no revision."""
    found: dict[str, str] = {}
    for key, name in (("requirements", f"{feature_id}.md"),
                      ("design", f"{feature_id}.design.md")):
        shown = (FEATURES / name).as_posix()
        if not (root / FEATURES / name).is_file():
            if key == "design":
                continue
            raise Unreadable(f"no feature document at {shown}")
        revision = _ready_revision(root / FEATURES / name)
        if revision is None:
            raise Unreadable(f'{shown} holds no "Ready:" row that names a revision')
        found[key] = f"r{revision}"
    return found


def _unchecked(record: dict, names: dict[int, str]) -> list[tuple[int, str]] | None:
    """The unchecked items of a well-formed review record, each number
    with its section, ends stripped, by number; None when the record is
    not well formed. A well-formed record holds `by`, a text that names a
    person, and `seat`, a text on one line that is not blank; its `items`
    is a list of one mapping for each item, in any order, whose `n` is an
    int and no bool, whose `name` is the items file's name for that
    number and whose `checked` is a bool; each unchecked entry holds
    `section`, a text that names a section."""
    seat, entries = record.get("seat"), record.get("items")
    if not _names(record.get("by")):
        return None
    if not (isinstance(seat, str) and seat.strip() and _one_line(seat)):
        return None
    if not isinstance(entries, list) or len(entries) != len(names):
        return None
    seen: set[int] = set()
    unchecked: dict[int, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            return None
        n, checked = entry.get("n"), entry.get("checked")
        if type(n) is not int or n not in names or n in seen:
            return None
        seen.add(n)
        if entry.get("name") != names[n] or type(checked) is not bool:
            return None
        if not checked:
            if not _names(entry.get("section")):
                return None
            unchecked[n] = entry["section"].strip()
    return sorted(unchecked.items())


def read_review(root: Path, feature_id: str) -> tuple[str, list[Finding]]:
    """G1.3's status and its findings, by item number.

    Only the last G1.3 record counts, with no falling back to an earlier
    one. `to do` when there is none or it is not well formed. A
    well-formed record that leaves an item unchecked reports RS301 for
    each, whatever the documents say now. One that checks every item
    reads `done` only when its `requirements` and its `design` equal, as
    text, the revisions the documents' `Ready:` rows name now, the
    `design` key absent on both sides when the feature holds no design
    document; a document that names no revision reads `to do`. The seat
    is held against the roster at the call alone.
    """
    names = items()
    record = last_record(root, feature_id, REVIEW)
    unchecked = _unchecked(record, names) if record is not None else None
    if unchecked is None:
        return TO_DO, []
    if unchecked:
        return FAILED, [Finding(feature_id, REVIEW, "RS301", UNCHECKED.format(
            n=n, item=names[n], section=section)) for n, section in unchecked]
    try:
        current = derived_from(root, feature_id)
    except Unreadable:
        return TO_DO, []
    held = {key: record[key] for key in ("requirements", "design") if key in record}
    return (DONE if held == current else TO_DO), []


def main_g1_check(args) -> int:
    """`taskcontract g1-check`: the three conditions' statuses, G1.1's
    findings, then G1.2's and then G1.3's. Exit 0 when all three read
    `done`, 1 when they do not, 2 when the id has no contract or G1 is not
    active for the feature."""
    root, feature_id = Path(args.root), args.id
    scope = contract_scope(root, feature_id)
    if scope is None:
        return _refuse(_no_contract(feature_id))
    config = read_config(root)
    if not is_active(config, feature_id):
        return _refuse(_not_active(feature_id))
    lint, findings = read_lint(root, feature_id, scope, config)
    model, reported = read_model(root, feature_id, scope)
    review, unchecked = read_review(root, feature_id)
    findings = findings + reported + unchecked
    statuses = {LINT: lint, MODEL: model, REVIEW: review}
    note = ", ".join(f"{condition} {status}" for condition, status in statuses.items())
    green = all(status == DONE for status in statuses.values())
    if args.as_json:
        print(json.dumps({"note": note, "findings": [asdict(f) for f in findings]}))
    elif green:
        print(f"g1-green: {feature_id}")
    else:
        for finding in findings:
            print(finding.line)
        print(f"{feature_id}: {note}")
    return 0 if green else 1


def main_g1_record(args) -> int:
    """`taskcontract g1-record`: `lint` for G1.1, `model` for G1.2 and
    `review` for G1.3. The working directory is the repository."""
    if args.kind == "model":
        return record_model(Path("."), args.id)
    if args.kind == "review":
        return record_review(Path("."), args.id, args.by, args.seat,
                             args.checked, args.unchecked)
    return record_lint(Path("."), args.id)


def record_lint(root: Path, feature_id: str) -> int:
    """Lint each schema in scope and append one G1.1 record: exit 0 when
    every file lints clean or no schema is in scope, 1 when a file does not
    or the tool is not installed, 2 when the call is refused or the tool
    ends on an error of its own.

    The contract, the gate, the declaration, the schemas, the linter's name
    and the record file are checked in that order before a tool starts,
    not even for its version, and nothing is
    written before every file has run, so a call that exits 2 writes
    nothing. A tool that did not start is recorded as not installed; one
    that started and ended on its own error gives no result.
    """
    scope = contract_scope(root, feature_id)
    if scope is None:
        return _refuse(_no_contract(feature_id))
    config = read_config(root)
    if not is_active(config, feature_id):
        return _refuse(_not_active(feature_id))
    try:
        entries = schema_entries(config)
    except Unreadable as exc:
        return _refuse(f"{feature_id}: g1.schemas cannot be read: {exc}")
    schemas = schemas_in_scope(root, scope, entries or [])
    if not schemas:
        print(NO_SCHEMA)
        return 0
    if len({schema.entry for schema in schemas}) > 1:
        return _refuse(f"{feature_id}: more than one g1.schemas entry is in scope; "
                       "a record holds one linter and one pin")
    tool, pin = schemas[0].linter, schemas[0].pin
    if tool not in LINTERS:
        return _refuse(f"{feature_id}: g1.schemas names a linter the kit does not know: {tool}")
    path = root / G1_DIR / f"{feature_id}.yaml"
    try:
        doc = _existing(path)
    except Unreadable as exc:
        return _refuse(f"{PROG}: unreadable record: "
                       f"{(G1_DIR / path.name).as_posix()} ({exc})")
    version, counts = None, None
    program = shutil.which(tool)
    started = _start([program, "--version"], root) if program is not None else None
    if started is not None:
        version, counts = started.stdout.strip(), []
        for schema in schemas:
            result = _start(_argv(program, tool, schema.path, pin), root)
            if result is None:  # the tool did not start: recorded as not installed
                version, counts = None, None
                break
            count = COUNTS[tool](result)
            if count is None:
                for text in (result.stderr, result.stdout):
                    if text and text.strip():
                        print(text.rstrip("\n"), file=sys.stderr)
                return 2
            counts.append(count)
    installed = counts is not None
    doc["records"].append({
        "condition": LINT,
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "head": head_id(root),
        "tool": tool,
        "tool_version": version,
        "installed": installed,
        "pin": {"path": pin, "sha256": sha256_of(root / pin) if pin else None},
        "files": [{"path": schema.path, "sha256": sha256_of(root / schema.path),
                   "reported": counts[n] if installed else None}
                  for n, schema in enumerate(schemas)],
    })
    _write(path, doc)
    if not installed:
        print(NOT_INSTALLED.format(tool=tool))
    else:
        for schema, count in zip(schemas, counts):
            line = CLEAN if count == 0 else NOT_CLEAN
            print(line.format(file=schema.path, tool=tool, n=count))
    print(f"recorded: {(G1_DIR / path.name).as_posix()}")
    return 0 if installed and not any(counts) else 1


def _argv(program: str, tool: str, file: str, pin: str) -> list[str]:
    """The linter's call for one file, started by the path `shutil.which`
    returned. Spectral is quiet, so a clean run prints a JSON array alone,
    and fails from a warning up."""
    if tool == "buf":
        return [program, "lint", "--config", pin, "--path", file, "--error-format", "json"]
    return [program, "lint", file, "--ruleset", pin, "--format", "json", "--quiet",
            "--fail-severity", "warn"]


def _start(argv: list[str], folder: Path) -> subprocess.CompletedProcess | None:
    """One tool call inside the folder, its output captured, with no window
    and no time limit; None when the tool cannot start."""
    try:
        return subprocess.run(argv, cwd=folder, capture_output=True, encoding="utf-8",
                              errors="replace", creationflags=NO_WINDOW)
    except OSError:
        return None


def _spectral_count(result: subprocess.CompletedProcess) -> int | None:
    """The rows that are an error or a warning; None when Spectral ended on
    an error of its own, printed no JSON array, or exited 1 with no such
    row: a file is clean only on exit 0."""
    if result.returncode not in (0, 1):
        return None
    try:
        rows = json.loads(result.stdout)
    except ValueError:
        return None
    if not isinstance(rows, list):
        return None
    count = sum(1 for row in rows if isinstance(row, dict) and row.get("severity") in COUNTED)
    return None if result.returncode == 1 and count == 0 else count


def _buf_count(result: subprocess.CompletedProcess) -> int | None:
    """The stdout lines that are a JSON object; None when buf ended on an
    error with no such line."""
    count = 0
    for line in (result.stdout or "").splitlines():
        try:
            count += isinstance(json.loads(line), dict)
        except ValueError:
            continue
    return None if result.returncode != 0 and count == 0 else count


COUNTS = {"spectral": _spectral_count, "buf": _buf_count}


class NoResult(Exception):
    """A checker that started and gave no result, with the lines the writer
    prints to stderr."""


def record_model(root: Path, feature_id: str) -> int:
    """Check the model of each hard core in scope and append one G1.2
    record: exit 0 when every hard core in scope has a model that passes
    or none is in scope, 1 when one has no model, one does not pass or a
    checker is not installed, 2 when the call is refused or a tool ends
    on an error of its own.

    The contract, the gate, the contract's scope, the declaration, the
    hard cores and the record file are checked in that order before a
    tool starts, and nothing is printed or written before every tool has
    run, so a call that exits 2 writes nothing. A contract whose scope
    cannot be read, or holds no entry, is refused. A hard core with no
    model gets its line and no entry: the rule reads the declaration. A
    checker is found by its bare name, with no version call; one that is
    not found or did not start is recorded as not installed, and one that
    started and ended on its own error gives no result, as does a hard
    core whose configuration P cannot read or whose working folder TLC
    cannot get. Each file is hashed before its tool starts.
    """
    scope = contract_scope(root, feature_id)
    if scope is None:
        return _refuse(_no_contract(feature_id))
    if not is_active(read_config(root), feature_id):
        return _refuse(_not_active(feature_id))
    if not scope:
        return _refuse(f"{feature_id}: the contract's scope cannot be read at "
                       f"specs/{feature_id}/contract.yaml")
    try:
        entries = components(root)
    except Unreadable as exc:
        return _refuse(f"{feature_id}: {COMPONENTS.as_posix()} cannot be read: {exc}")
    if entries is None:
        return _refuse(f"{feature_id}: no component declaration at {COMPONENTS.as_posix()}")
    cores = hard_cores_in_scope(scope, entries)
    if not cores:
        print(NO_HARD_CORE)
        return 0
    path = root / G1_DIR / f"{feature_id}.yaml"
    try:
        doc = _existing(path)
    except Unreadable as exc:
        return _refuse(f"{PROG}: unreadable record: "
                       f"{(G1_DIR / path.name).as_posix()} ({exc})")
    programs: dict[str, str | None] = {}  # each tool's path; None when not installed
    named: set[str] = set()  # the tools the not-installed line has named
    lines, held, green = [], [], True
    for core in cores:
        if not _has_model(root, core):
            lines.append(NO_MODEL.format(component=core["id"]))
            green = False
            continue
        pins = _pins(root, core)
        component, tool = pins["component"], pins["tool"]
        if tool not in programs:
            programs[tool] = shutil.which(tool)
        result = None
        if programs[tool] is not None:
            try:
                result = CHECKS[tool](programs[tool], root, core, feature_id)
            except NoResult as exc:
                for text in exc.args:
                    print(text, file=sys.stderr)
                return 2
            if result is None:  # the tool did not start: recorded as not installed
                programs[tool] = None
        held.append({**pins, "installed": result is not None, "result": result})
        if result is None and tool not in named:
            named.add(tool)
            lines.append(NO_CHECKER.format(tool=tool))
        elif result is not None:
            line = PASSING if result == PASS else NOT_PASSING
            lines.append(line.format(component=component, tool=tool))
        green = green and result == PASS
    if held:
        doc["records"].append({
            "condition": MODEL,
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "head": head_id(root),
            "cores": [{key: entry[key] for key in ("component", "tool", "installed",
                                                   "model", "config", "result")}
                      for entry in held],
        })
        _write(path, doc)
    for line in lines:
        print(line)
    if held:
        print(f"recorded: {(G1_DIR / path.name).as_posix()}")
    return 0 if green else 1


def _tlc(program: str, root: Path, core: dict, feature_id: str) -> str | None:
    """One TLC run inside the model's folder, the model by its file name and
    the configuration by its absolute path. TLC names its working folder
    from the clock, so each run gets a fresh `-metadir` outside the
    repository, removed on every path. A folder that cannot be made gives
    no result, and TLC does not start. None when TLC cannot start."""
    model = root / _entry(core["model"])
    try:
        metadir = tempfile.mkdtemp(prefix="taskcontract-g1-")
    except OSError as exc:
        raise NoResult(f"{feature_id}: no working folder for the model of {core['id']}: "
                       f"{exc.strerror or 'it cannot be made'}") from None
    try:
        result = _start([program, "-metadir", metadir, "-config",
                         os.path.abspath(root / core["model_config"]), model.name],
                        model.parent)
    finally:
        shutil.rmtree(metadir, ignore_errors=True)
    return None if result is None else _verdict("tlc", result)


def _p(program: str, root: Path, core: dict, feature_id: str) -> str | None:
    """P's two calls inside the model's folder: the project compiled, then
    checked with the words of the configuration's file, which are read
    before P starts. A configuration that cannot be read gives no result
    with no call made; a compile that does not exit 0 gives no result,
    and no check follows. None when P cannot start."""
    model = root / _entry(core["model"])
    try:
        words = (root / core["model_config"]).read_text(encoding="utf-8").split()
    except (OSError, UnicodeDecodeError):
        raise NoResult(f"{feature_id}: the configuration of {core['id']} cannot be "
                       f"read: {core['model_config']}") from None
    built = _start([program, "compile", "--pproj", model.name], model.parent)
    if built is None:
        return None
    if built.returncode != 0:
        raise NoResult(*_tool_lines(built))
    result = _start([program, "check", *words], model.parent)
    return None if result is None else _verdict("p", result)


def _verdict(tool: str, result: subprocess.CompletedProcess) -> str:
    """The result by the exit code: 0 passes, and a code by which the
    checker says its search found a violation fails. NoResult with the
    tool's lines for any other code: an error of the tool's own."""
    if result.returncode == 0:
        return PASS
    if result.returncode in VIOLATION[tool]:
        return FAIL
    raise NoResult(*_tool_lines(result))


def _tool_lines(result: subprocess.CompletedProcess) -> list[str]:
    """What the tool printed, its stderr first, each stream that is not blank."""
    return [text.rstrip("\n") for text in (result.stderr, result.stdout)
            if text and text.strip()]


CHECKS = {"tlc": _tlc, "p": _p}


class Refused(Exception):
    """A review call the writer cannot use, with the words its one line
    prints after the feature's id."""


def record_review(root: Path, feature_id: str, by: list[str], seat: list[str],
                  checked: list[str], unchecked: list[str]) -> int:
    """Append one G1.3 record of a named person's answers: exit 0 when the
    review checks every item, 1 when it leaves one unchecked, 2 when the
    call is refused.

    Each option comes as the list of its values, so a repeat is seen. The
    contract, the gate, the contract's scope, the signer, the seat, the
    items, the documents' revisions and the record file are checked in
    that order, and nothing is written before every check has passed, so
    a call that exits 2 writes nothing. The record holds the revision
    each document's `Ready:` row names at the call, and no `design` when
    the feature holds no design document.
    """
    try:
        scope = contract_scope(root, feature_id)
    except UnicodeDecodeError:  # a contract that is not UTF-8 has no scope to read
        scope = []
    if scope is None:
        return _refuse(_no_contract(feature_id))
    if not is_active(read_config(root), feature_id):
        return _refuse(_not_active(feature_id))
    if not scope:
        return _refuse(f"{feature_id}: the contract's scope cannot be read at "
                       f"specs/{feature_id}/contract.yaml")
    names = items()
    try:
        signer = _signer(by)
        sat = _seat(root, seat)
        sections = _answers(checked, unchecked, names)
        revisions = derived_from(root, feature_id)
    except (Refused, Unreadable) as exc:
        return _refuse(f"{feature_id}: {exc}")
    path = root / G1_DIR / f"{feature_id}.yaml"
    try:
        doc = _existing(path)
    except Unreadable as exc:
        return _refuse(f"{PROG}: unreadable record: "
                       f"{(G1_DIR / path.name).as_posix()} ({exc})")
    doc["records"].append({
        "condition": REVIEW,
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "head": head_id(root),
        "by": signer,
        "seat": sat,
        **revisions,
        "items": [{"n": n, "name": name, "checked": n not in sections,
                   **({"section": sections[n]} if n in sections else {})}
                  for n, name in names.items()],
    })
    _write(path, doc)
    for n in sorted(sections):
        print(UNCHECKED.format(n=n, item=names[n], section=sections[n]))
    if not sections:
        print(ALL_CHECKED.format(count=len(names)))
    print(f"recorded: {(G1_DIR / path.name).as_posix()}")
    return 1 if sections else 0


def _once(option: str, values: list[str]) -> str:
    """The option's one value; Refused when it is absent or repeated, even
    twice with the same value."""
    if len(values) != 1:
        raise Refused(f"{option} is given {len(values)} times; a review takes it once")
    return values[0]


def _signer(by: list[str]) -> str:
    """The signer's name, outer blanks cut; Refused for a name that holds
    a line break, or no letter and no digit."""
    name = _once("--by", by)
    if not _names(name):
        raise Refused(f"--by {ascii(name)} names no person")
    return name.strip()


def _seat(root: Path, seat: list[str]) -> str:
    """The signer's seat as given; Refused when it does not equal, to the
    letter, one value of the ratified `intake-seat` term. A term's file
    that is absent, not UTF-8, no YAML mapping or not ratified gives no
    term. `values` that is no list holds no seat, and neither does a
    value that is no text; an empty seat is never one."""
    given = _once("--seat", seat)
    try:
        term = yaml.safe_load((root / SEAT_TERM).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        term = None
    if not isinstance(term, dict) or term.get("status") != "ratified":
        raise Refused(f"no ratified intake-seat term at {SEAT_TERM.as_posix()}")
    values = term.get("values")
    seats = [v for v in values if isinstance(v, str)] if isinstance(values, list) else []
    if not given or not _one_line(given) or given not in seats:
        raise Refused(f"--seat {ascii(given)} is no value of the ratified "
                      "intake-seat term")
    return given


def _answers(checked: list[str], unchecked: list[str],
             names: dict[int, str]) -> dict[int, str]:
    """Each unchecked item's section by its number, ends stripped; an item
    the mapping does not hold is checked. Refused unless the two options
    name every item once between them. `--checked` is one list, cut at
    each comma, and `--unchecked` one `<n>=<section>` pair, cut at its
    first `=` alone. An item number is one of the items file's numbers as
    plain digits, blanks around it aside: no number is parsed, so `01`,
    `+1` and a fullwidth digit name none. No section is held against a
    document's headings."""
    numbers = {str(n): n for n in names}
    last = max(names)
    if len(checked) > 1:
        raise Refused(f"--checked is given {len(checked)} times; a review takes one list")
    named: list[int] = []
    sections: dict[int, str] = {}
    for value in checked:
        if not _one_line(value):
            raise Refused(f"--checked {ascii(value)} holds a line break")
        for element in value.split(","):
            if element.strip() not in numbers:
                raise Refused(f"--checked holds {ascii(element)}, which is no item "
                              f"number from 1 to {last}")
            named.append(numbers[element.strip()])
    for pair in unchecked:
        left, cut, right = pair.partition("=")
        if not _one_line(pair) or not cut or left.strip() not in numbers:
            raise Refused(f"--unchecked {ascii(pair)} is no <n>=<section> pair on one "
                          f"line with an item number from 1 to {last}")
        if not _names(right):
            raise Refused(f"--unchecked {ascii(pair)} names no section")
        named.append(numbers[left.strip()])
        sections[numbers[left.strip()]] = right.strip()
    twice = [n for n in names if named.count(n) > 1]
    absent = [n for n in names if n not in named]
    if twice or absent:
        problem = (f"item {twice[0]} is named more than once" if twice
                   else f"item {absent[0]} is not named")
        raise Refused(f"{problem}; a review names each of the {len(names)} items once")
    return sections


def _existing(path: Path) -> dict:
    """The record file's mapping as read, every record kept; an absent file
    is empty; Unreadable with the reason for one that cannot be used."""
    if not path.exists():
        return {"records": []}
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        raise Unreadable(getattr(exc, "strerror", None) or "cannot be read") from None
    except (yaml.YAMLError, ValueError) as exc:  # a date no calendar holds is a ValueError
        mark = getattr(exc, "problem_mark", None)
        raise Unreadable(f"YAML error at line {mark.line + 1}" if mark is not None
                         else "YAML error") from None
    if not isinstance(doc, dict):
        raise Unreadable("not a mapping")
    if not isinstance(doc.get("records"), list):
        raise Unreadable("records is not a list")
    return doc


def _write(path: Path, doc: dict) -> None:
    """The record file and its folder, UTF-8 with LF on every platform. The
    folder is committed, so it gets no `.gitignore`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as out:
        yaml.safe_dump(doc, out, sort_keys=False, allow_unicode=True)


def _no_contract(feature_id: str) -> str:
    return f"{feature_id}: no contract at specs/{feature_id}/contract.yaml"


def _not_active(feature_id: str) -> str:
    return f"{feature_id}: G1 is not active"


def _refuse(line: str) -> int:
    print(line, file=sys.stderr)
    return 2
