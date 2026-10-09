"""G1.1's lint record, its writer and the G1 verdict (ADR 0038).

Contract: g1-requirements-spec. G1's rules read records, in their own
command, and no G1 rule reports through `validate`. This module holds the
writer of a lint record, `g1-record lint`, and the reader, `g1-check`.

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

`g1-check <id>` reads the declarations, the last G1.1 record and the files
on disk; it runs no tool and writes nothing. The files on disk win: a
record whose hashes no longer match counts as absent. Under G1.1 it
reports:

  RS101  the record found the linter not installed
  RS102  a schema in scope is recorded with one error or warning, or more

G1.2's and G1.3's rules are not built in this module yet, so each of the
two reads `to do`.

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
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .progress import head_id
from .scope_check import contract_scope, in_any, matches

G1_DIR = Path(".sdlc") / "g1"
GATE = "G1"
LINT = "G1.1"
LINTERS = ("spectral", "buf")
TO_DO, DONE, FAILED = "to do", "done", "failed"
PROG = "taskcontract g1-record"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
COUNTED = (0, 1)  # Spectral's severities for an error and a warning

NO_SCHEMA = "G1.1: no boundary schema in scope"
NOT_INSTALLED = "G1.1: {tool} is not installed; install it and pin it in the repository"
NOT_CLEAN = "G1.1: {file} does not lint clean: {tool} reports {n}"
CLEAN = "G1.1: {file} lints clean under {tool}"


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
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
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
    its first wildcard; `matches` decides."""
    entry = pattern.strip().replace("\\", "/")
    if not entry:
        return []
    if entry.endswith("/"):
        base = entry.rstrip("/")
    else:
        cut = min((entry.index(c) for c in "*?[" if c in entry), default=None)
        if cut is None:
            return [entry] if _inside(entry) and (root / entry).is_file() else []
        base = entry[:cut].rpartition("/")[0]
    if not _inside(base):
        return []
    start = root / base if base else root
    paths = []
    for folder, _, names in os.walk(start):
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


def sha256_of(path: Path) -> str | None:
    """The whole SHA-256 of the file's bytes on disk; None when it cannot be read."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def last_record(root: Path, feature_id: str, condition: str) -> dict | None:
    """The last record of the condition in the feature's record file; a file
    that is absent or cannot be read counts as no record."""
    try:
        doc = yaml.safe_load((root / G1_DIR / f"{feature_id}.yaml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
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
    with the pin's hash as it stands now. A pin's file that is absent
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
    recorded = {f.get("path"): f for f in files if isinstance(f, dict)}
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


def main_g1_check(args) -> int:
    """`taskcontract g1-check`: the three conditions' statuses and G1.1's
    findings. Exit 0 when all three read `done`, 1 when they do not, 2 when
    the id has no contract or G1 is not active for the feature."""
    root, feature_id = Path(args.root), args.id
    scope = contract_scope(root, feature_id)
    if scope is None:
        return _refuse(_no_contract(feature_id))
    config = read_config(root)
    if not is_active(config, feature_id):
        return _refuse(_not_active(feature_id))
    lint, findings = read_lint(root, feature_id, scope, config)
    # G1.2's and G1.3's rules are not built yet, so each of the two reads `to do`
    statuses = {LINT: lint, "G1.2": TO_DO, "G1.3": TO_DO}
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
    """`taskcontract g1-record`: `lint` for G1.1. The working directory is
    the repository."""
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


def _start(argv: list[str], root: Path) -> subprocess.CompletedProcess | None:
    """One tool call at the root, its output captured, with no window and no
    time limit; None when the tool cannot start."""
    try:
        return subprocess.run(argv, cwd=root, capture_output=True, encoding="utf-8",
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


def _existing(path: Path) -> dict:
    """The record file's mapping as read, every record kept; an absent file
    is empty; Unreadable with the reason for one that cannot be used."""
    if not path.exists():
        return {"records": []}
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        raise Unreadable(getattr(exc, "strerror", None) or "cannot be read") from None
    except yaml.YAMLError as exc:
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
