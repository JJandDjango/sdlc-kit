"""The progress format, its reader and its writer (ADR 0031).

Execution state lives at `.sdlc/progress/<contract>.yaml`, one local file per
contract, the place ADR 0024 ruled for it. ADR 0031 gives it its writers
(`taskcontract progress`); this module fixes the format they write, reads it
for the tree, and holds the four writers: `progress run` for a check, and
`progress start`, `done` and `block` for a task step, where a `done` on a
unit or a contract is a close. No gate, check, audit or hook reads it. The
folder holds a `.gitignore` of `*`, so none of it is committed.

A file holds `records`, a list applied in file order. Each record names an
`item` by the full id the tree prints and carries its time in `at`, plus
exactly one of `state` (a task step, or a close of a unit or contract) and
`run` (a check run, judged beside its `expect`). The other keys are display
evidence: `head` (the short `HEAD` id, or `no commit`), `by` (the seat an
approval names), `reason` (why a step is blocked), `command` (a run's argv,
joined) and `dirty` (a tracked file differed from `HEAD`; absent outside
git). The reader carries them all for the tree and checks none of them: a
record without them still reads.

A malformed file is dropped whole, its good records too, with one line
naming it: its contract then reads as having no progress. A writer never
touches a malformed file: it refuses before it writes, and before `run`
starts the command. Every check a writer makes comes first, so a refused
call writes nothing.
"""

from __future__ import annotations

import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

PROGRESS_DIR = Path(".sdlc") / "progress"
STATES = ("doing", "done", "blocked")
RUNS = ("red", "green")
NO_COMMIT = "no commit"
IGNORE_ALL = b"*\n"  # the folder's .gitignore, LF on every platform
PROG = "taskcontract progress"
# The kind a writer names for an item it refuses; the no-gate item is a gate.
KINDS = {"none": "gate"}
# The state each task writer records.
ACTIONS = {"start": "doing", "done": "done", "block": "blocked"}
CLOSES = ("unit", "contract")  # the levels a `done` closes

# A time of day must follow the date: a bare date is no instant.
_TIMED = re.compile(r"^\d{4}-\d{2}-\d{2}[Tt ]\d")


@dataclass(frozen=True)
class Record:
    """One usable record: its item, its kind's value, its instant in UTC, and
    the evidence the tree prints (None where the record has none)."""

    item: str
    at: datetime
    state: str | None = None
    run: str | None = None
    expect: str | None = None
    command: str | None = None
    head: str | None = None
    dirty: bool | None = None
    by: str | None = None
    reason: str | None = None


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
    command, head, dirty = raw.get("command"), raw.get("head"), raw.get("dirty")
    by, reason = raw.get("by"), raw.get("reason")
    return Record(item=item, at=at, state=state, run=run, expect=expect,
                  command=command if isinstance(command, str) else None,
                  head=head if isinstance(head, str) else None,
                  dirty=dirty if isinstance(dirty, bool) else None,
                  by=by if isinstance(by, str) else None,
                  reason=reason if isinstance(reason, str) else None)


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


def main_progress(args) -> int:
    """`taskcontract progress`: `run` for a check, `start`, `done` and
    `block` for a task step."""
    if args.action == "run":
        return run_check(Path(args.root), args.check, args.expect, args.argv)
    return record_state(Path(args.root), args.action, args.item,
                        by=getattr(args, "by", None), reason=getattr(args, "reason", None))


def run_check(root: Path, check: str, expect: str, argv: list[str]) -> int:
    """Run a check's command and append its record: exit 0 when the result
    met `expect`, 1 when it missed, 2 when the command never ran.

    The id, the check's progress file and the command's start are each
    settled before anything is written, so a refused call writes nothing.
    """
    target = _target(root, check)
    if target is None:
        return _refuse(_no_node(check))
    if target.level != "check":
        return _refuse(f"{PROG}: '{check}' is a {_kind(target)}, not a check - "
                       "run takes a check id")
    path = _path(root, check)
    try:
        doc = _existing(path)
    except Malformed as exc:
        return _refuse(_unreadable(path, root, exc))
    head, dirty = head_id(root), dirty_mark(root)
    command = shlex.join(argv)
    try:
        code = subprocess.run(argv, cwd=root).returncode
    except OSError as exc:
        return _refuse(f"{PROG}: cannot start {command} ({exc.strerror or exc})")
    ended = _now()
    result = "green" if code == 0 else "red"
    record = {"item": check, "run": result, "expect": expect,
              "command": command, "head": head}
    if dirty is not None:
        record["dirty"] = dirty
    record["at"] = ended
    doc["records"].append(record)
    _write(path, doc)
    print(f"{check}: {result}, expected {expect}")
    return 0 if result == expect else 1


def record_state(root: Path, action: str, item_id: str,
                 by: str | None = None, reason: str | None = None) -> int:
    """Append one record for `start`, `done` or `block`: exit 0 when written,
    2 when refused.

    `start` and `block` take a task; `done` takes a task, or closes a unit
    or a contract with one record naming it. An approval's `done` names its
    seat in `by`, and a `block` its `reason`. The id, its kind, the options
    and the contract's progress file are checked in that order before
    anything is written, so a refused call writes nothing.
    """
    from .tree import APPROVALS  # tree imports this module

    target = _target(root, item_id)
    if target is None:
        return _refuse(_no_node(item_id))
    if action == "done" and target.level not in ("task", *CLOSES):
        return _refuse(f"{PROG}: '{item_id}' is a {_kind(target)}, not a task, unit or "
                       "contract - done takes a task, unit or contract id")
    if action != "done" and target.level != "task":
        return _refuse(f"{PROG}: '{item_id}' is a {_kind(target)}, not a task - "
                       f"{action} takes a task id")
    approval = target.level == "task" and item_id.rsplit("/", 1)[-1] in APPROVALS
    if action == "done" and approval and not (by or "").strip():
        return _refuse(f"{PROG}: '{item_id}' is an approval - done needs --by <seat>")
    if action == "done" and not approval and by is not None:
        return _refuse(f"{PROG}: '{item_id}' is not an approval - "
                       "only approve-tests and approve-commit take --by")
    if action == "block" and not (reason or "").strip():
        return _refuse(f"{PROG}: block needs --reason <text> - say why '{item_id}' is blocked")
    path = _path(root, item_id)
    try:
        doc = _existing(path)
    except Malformed as exc:
        return _refuse(_unreadable(path, root, exc))
    record = {"item": item_id, "state": ACTIONS[action]}
    if action == "done" and approval:
        record["by"] = by
    if action == "block":
        record["reason"] = reason
    record["head"] = head_id(root)
    dirty = dirty_mark(root)
    if dirty is not None:
        record["dirty"] = dirty
    record["at"] = _now()
    doc["records"].append(record)
    _write(path, doc)
    print(f"{item_id}: {ACTIONS[action]}" + (f" by {by}" if "by" in record else ""))
    return 0


def _target(root: Path, item_id: str):
    """The tree's item with this id, or None; the tree is read quietly, so
    its own lines stay unprinted."""
    from .tree import build  # tree imports this module

    items, _ = build(root)
    return next((item for item in _every(items) if item.id == item_id), None)


def _kind(item) -> str:
    """The kind a refusal names for an item."""
    return KINDS.get(item.level, item.level)


def _no_node(item_id: str) -> str:
    return f"no node '{item_id}' - print the tree to list every node id"


def _path(root: Path, item_id: str) -> Path:
    """The progress file of the contract the id opens on."""
    return root / PROGRESS_DIR / f"{item_id.split('/', 1)[0]}.yaml"


def _unreadable(path: Path, root: Path, exc: Malformed) -> str:
    return f"{PROG}: unreadable progress: {_rel(path, root)} ({exc})"


def _now() -> str:
    """The time now in UTC, as every writer records it."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _every(items):
    """Each item and everything under it, in print order."""
    for item in items:
        yield item
        yield from _every(item.children)


def _refuse(line: str) -> int:
    print(line, file=sys.stderr)
    return 2


def _existing(path: Path) -> dict:
    """The file's mapping as read, every record kept; an absent file is empty;
    Malformed by the reader's own reason."""
    if not path.exists():
        return {"records": []}
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Malformed(getattr(exc, "strerror", None) or "cannot be read") from None
    parse(text)
    return yaml.safe_load(text)


def _write(path: Path, doc: dict) -> None:
    """The file, its folder, and the folder's `.gitignore` if it has none."""
    path.parent.mkdir(parents=True, exist_ok=True)
    ignore = path.parent / ".gitignore"
    if not ignore.exists():
        ignore.write_bytes(IGNORE_ALL)
    with path.open("w", encoding="utf-8", newline="\n") as out:
        yaml.safe_dump(doc, out, sort_keys=False, allow_unicode=True)


def head_id(root: Path) -> str:
    """`git rev-parse --short HEAD` at the root, or `no commit`."""
    result = run_git(root, "rev-parse", "--short", "HEAD")
    head = (result.stdout or "").strip() if result is not None else ""
    return head if result is not None and result.returncode == 0 and head else NO_COMMIT


def dirty_mark(root: Path) -> bool | None:
    """Whether a tracked file differs from `HEAD`, staged or not; untracked
    files never count. None outside git."""
    result = run_git(root, "status", "--porcelain", "--untracked-files=no")
    if result is None or result.returncode != 0:
        return None
    return bool(result.stdout.strip())


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess | None:
    """One git call at the root, its output captured; None when git cannot start."""
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True,
                              encoding="utf-8", errors="replace")
    except OSError:
        return None


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
