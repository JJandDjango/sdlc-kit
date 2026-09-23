"""The progress format and its reader (ADR 0031).

Execution state lives at `.sdlc/progress/<contract>.yaml`, one local file per
contract, the place ADR 0024 ruled for it. ADR 0031 gives it its writers
(`taskcontract progress`, later units); this module fixes the format they
write and reads it for the tree. No gate, check, audit or hook reads it.

A file holds `records`, a list applied in file order. Each record names an
`item` by the full id the tree prints and carries its time in `at`, plus
exactly one of `state` (a task step, or a close of a unit or contract) and
`run` (a check run, judged beside its `expect`). Other keys are display
evidence for later units and go unchecked here.

A malformed file is dropped whole, its good records too, with one line
naming it: its contract then reads as having no progress.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

PROGRESS_DIR = Path(".sdlc") / "progress"
STATES = ("doing", "done", "blocked")
RUNS = ("red", "green")

# A time of day must follow the date: a bare date is no instant.
_TIMED = re.compile(r"^\d{4}-\d{2}-\d{2}[Tt ]\d")


@dataclass(frozen=True)
class Record:
    """One usable record: its item, its kind's value, and its instant in UTC."""

    item: str
    at: datetime
    state: str | None = None
    run: str | None = None
    expect: str | None = None


class Malformed(ValueError):
    """A progress file the reader drops, with the reason it prints."""


def read_progress(root: Path, problems: list[str]) -> dict[str, list[Record]]:
    """Records per contract id (the file's stem), in file order; a malformed
    file adds one line to `problems` and gives its contract no records."""
    folder = root / PROGRESS_DIR
    if not folder.is_dir():
        return {}
    progress: dict[str, list[Record]] = {}
    for path in sorted(folder.glob("*.yaml"), key=lambda p: p.name):
        if not path.is_file():
            continue
        try:
            progress[path.stem] = parse(path.read_text(encoding="utf-8"))
        except Malformed as exc:
            problems.append(f"unreadable progress: {_rel(path, root)} ({exc})")
        except (OSError, UnicodeDecodeError) as exc:
            reason = getattr(exc, "strerror", None) or "cannot be read"
            problems.append(f"unreadable progress: {_rel(path, root)} ({reason})")
    return progress


def parse(text: str) -> list[Record]:
    """The records in one file's text, or Malformed naming the first fault."""
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        raise Malformed(f"YAML error at line {mark.line + 1}" if mark is not None
                        else "YAML error") from None
    if not isinstance(doc, dict):
        raise Malformed("not a mapping")
    records = doc.get("records")
    if not isinstance(records, list):
        raise Malformed("records is not a list")
    return [_record(n, raw) for n, raw in enumerate(records, start=1)]


def _record(n: int, raw) -> Record:
    """Record `n` (counted from 1) checked against the format."""
    if not isinstance(raw, dict):
        raise Malformed(f"record {n} is not a mapping")
    item = raw.get("item")
    if not isinstance(item, str) or not item.strip():
        raise Malformed(f"record {n} has no usable item")
    if ("state" in raw) == ("run" in raw):
        raise Malformed(f"record {n} needs one of state and run")
    state = run = expect = None
    if "state" in raw:
        state = raw["state"]
        if state not in STATES:
            raise Malformed(f"record {n} has no usable state")
    else:
        run, expect = raw["run"], raw.get("expect")
        if run not in RUNS:
            raise Malformed(f"record {n} has no usable run")
        if expect not in RUNS:
            raise Malformed(f"record {n} has no usable expect")
    at = instant(raw.get("at"))
    if at is None:
        raise Malformed(f"record {n} has no usable at")
    return Record(item=item, at=at, state=state, run=run, expect=expect)


def instant(value) -> datetime | None:
    """`at` as a UTC instant: a YAML timestamp or an ISO 8601 string, where
    no offset reads as UTC; None for a bare date or any other value."""
    if isinstance(value, datetime):
        moment = value
    elif isinstance(value, str) and _TIMED.match(value.strip()):
        text = value.strip()
        if text[-1] in "Zz":  # fromisoformat takes a trailing Z only from 3.11
            text = text[:-1] + "+00:00"
        try:
            moment = datetime.fromisoformat(text)
        except ValueError:
            return None
    else:
        return None
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
