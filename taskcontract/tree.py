"""The work as one derived tree (ADR 0031).

The tree is computed at every print and never stored: ADR 0024's rule for
the unit graph, carried to the whole work. `build` reads the contracts under
specs/, `active_gates` from .sdlc/config.yaml, the findings under
.sdlc/findings/, each contract's progress file under .sdlc/progress/, and
the two name lists the package ships (data/gates.yaml, data/tasks.yaml).
When an active `G0` verdict shows, it also runs the validator on that
contract and runs git twice: once for `HEAD`, once for the contract files
that differ from it. A caller that passes a verdict cache (the `--follow`
pane) keeps the validator's reading per contract, the verdict's and its
conditions', between prints, and the validator runs only for a contract
the cache lacks; git still runs at every print. It opens each contract's
docs/features/<id>.md for its revision table only, prints none of its
words, reads no other document and writes no file.

The gates stand first, at the repository level, each opening first into
its conditions, the named parts gates.yaml lists in its page's order. A
finding names a gate and never a contract (ADR 0023's form bans
identifiers), so each finding stands once: under the condition its `gate:`
field names when its gate lists that condition, such as G3.1, else under
the gate, after its conditions. A gate a finding names shows even when it
is not active. Then each contract, with its verdict at every active gate,
then its inactive next gate (the first gate in the kit's order after the
last active one, `G0` when none is active, none after the last), each
verdict opening into its gate's conditions; then its units, each unit's
seven tasks and its checks.

Every item but a finding carries one of six statuses; a finding records
none, so it shows its kind. A task step reads its last record in the
contract's progress file, a check its last run judged by what the run
expected, and a close of a unit or contract reads every task and check
under it done, never a verdict or a condition. A check whose last run was
green as expected names that run's command and `HEAD`, and `dirty` when the
run recorded it. A task that reads done by its own done record names that
record's `HEAD`, the seat it gives an approval, and `dirty`; a task that
reads blocked by its own record names its reason. A unit or contract that
reads done names its latest close's `HEAD` and `dirty`. A close neither
adds evidence to the items under it nor hides theirs. An active `G0`
verdict reads the validator at the draft and ready profiles and names the
command and the `HEAD` it read, and `dirty` when its contract file differs
from `HEAD`; each of its conditions reads the same rule over the codes it
owns, and one that is not done carries its rules' messages as its
diagnostics, the draft profile's when it failed, else the ready profile's.
A contract the tree cannot read as a mapping reads only its `G0.1` so,
since the joins behind the other two never ran on it. Warnings never count.
A verdict at any other gate, the inactive verdict, their conditions and
every gate item and its conditions read `to do`. A unit or contract rolls
up its children but the inactive verdict, so it reads `done` only when
every other child does; a closed contract's verdicts never count either,
so it reads `done` once its units do, or at once when it shows none, while
each verdict keeps its reading.

The current task is derived from the task states, never stored: the task
whose `doing` record is latest, else the first `to do` task in the contract
with the latest record. An approval that holds it reads `waiting on a seat`
and names its unit's `confirmed_by` seats as its evidence, `seat: <seats>`:
in order, each once, by the text rule, joined by `, `; none when the field
is not a list or gives no seat. No other item names a seat.

Each item carries its plain name from one source field, unchanged but for
its whitespace: a contract's `title`, a unit's `done_means`, a check's
sketch line, a finding's `statement`, and the name gates.yaml or tasks.yaml
gives a gate, a verdict's gate, a condition or a task. The field's ends are
stripped and each line break reads as one space; a field that is absent,
not text or blank gives no plain name, save that a contract then reads
`(no title)`, as does one the tree cannot read as a mapping. The tree reads
the title from the contract, never from its feature doc. A contract alone
carries a summary, its `intent` by the same rule. Links come from two
fields only: a unit's `depends_on` entries, as the unit graph reads them,
each linked once in the order of its first appearance, and a finding's
`gate:` value as written. A contract with a file at docs/features/<id>.md
carries that path as its feature doc reference. A line prints its plain
name after its id, then its links, the reference and the summary after the
marks and evidence.

A contract carries at most one drift mark, read afresh at every print from
its feature doc's revision table, the first table in the file. A row counts
when its last cell opens on `r<N>:`; the document's revision is the highest
N of a counted row that is neither a `Ready:` nor a `Measured:` row, and
the contract's is the `rM` that the first `derived from rM` in the newest
`Ready:` row naming one gives, the lower row winning a tie. The mark reads
`no feature document` when no file is at docs/features/<id>.md, `no
"Ready:" row` when no `Ready:` row names an `rM` or the file cannot be read
as text, and `stale: document rD, contract from rM` when the document's
revision is higher; else there is none, and the contract matches its
document. A contract the tree cannot read as a mapping carries it too.

Each item but a gate, a condition, a task and the no-gate item names the
file it is read from, and a unit or check the keys to its entry there;
`reference` turns that into the entry's line, parsing the file afresh, so
only the query calls it. A gate, a verdict, a condition and a task carry
the kit page their list gives, a condition its gate's.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import checker
from .graph import units as unit_rows
from .progress import Record, head_id, read_progress, run_git

DATA_DIR = Path(__file__).resolve().parent / "data"
GATES_PATH = DATA_DIR / "gates.yaml"
TASKS_PATH = DATA_DIR / "tasks.yaml"

STATUSES = ("to do", "doing", "done", "failed", "blocked", "waiting on a seat")
TO_DO, DOING, DONE, FAILED, BLOCKED, WAITING = STATUSES
# A parent takes the first of these that any child reads.
ROLL_UP = (FAILED, WAITING, BLOCKED, DOING)
NO_GATE = "none"
FORM = "TEMPLATE.yaml"  # the findings form, never a finding
INACTIVE = "inactive"
NO_TITLE = "(no title)"  # a contract's plain name when it gives no title
# The one G0 condition an unreadable contract still reads: the schema's; the
# joins behind the others never run on a file that is not a mapping.
SCHEMA_CONDITION = "G0.1"
CURRENT = "current"
APPROVALS = ("approve-tests", "approve-commit")
DIRTY = "dirty"
# The names `tree: pane: parts:` takes, in the order a line prints them.
PARTS = ("id", "status", "marks", "evidence", "links", "doc", "summary")
# The values `tree: pane: fold:` takes: name the folded items, or count them.
FOLDS = ("names", "counts")

# A check's id is the ids in its sketch's trailing parentheses, where intake
# writes them, joined with "+"; parentheses that hold words name no id.
_TRAILING = re.compile(r"\(([^()]*)\)\s*$")
_CHECK_ID = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")

# A contract's drift marks when it has no stale one.
NO_DOCUMENT = "no feature document"
NO_READY = 'no "Ready:" row'
# A feature doc's revision table: a pipe after a backslash never splits a
# cell; a counted row's last cell opens on `r<N>:`, and a `Ready:` row names
# its `rM` by the first `derived from rM`, the digits ending at a non-word.
_PIPE = re.compile(r"(?<!\\)\|")
_REVISION = re.compile(r"r([0-9]+):\s*")
_DERIVED = re.compile(r"derived from r([0-9]+)(?!\w)")


@dataclass
class Item:
    """One entry of the tree; `level` is gate, condition, none, finding,
    contract, verdict, unit, task or check."""

    id: str
    level: str
    status: str | None = TO_DO
    kind: str | None = None  # a finding's kind, shown where others show a status
    marks: list[str] = field(default_factory=list)
    children: list[Item] = field(default_factory=list)
    evidence: str | None = None  # what the status was read from
    links: list[str] = field(default_factory=list)  # each `<kind>: <target>`
    doc: str | None = None  # a contract's feature doc path
    name: str | None = None  # the plain name, by the text rule
    summary: str | None = None  # a contract's intent, by the text rule
    source: str | None = None  # the repo path of the file the item is read from
    place: tuple = ()  # the keys from that file's top to the item's entry
    # The kit page that defines a gate or a task; a verdict's or a condition's
    # is its gate's.
    page: str | None = None
    # A condition's messages from its rules, each on one line; never an item.
    diagnostics: list[str] = field(default_factory=list)
    # An approval's seats, its unit's `confirmed_by`; named only while it waits.
    seats: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class G0Reading:
    """The validator's reading of one contract: the verdict's status, the
    errors at the draft and ready profiles as (rule, message) pairs in the
    validator's order, and whether the tree reads the file as a mapping."""

    status: str
    draft: tuple[tuple[str, str], ...]
    ready: tuple[tuple[str, str], ...]
    mapping: bool


@dataclass(frozen=True)
class Finding:
    """One finding file: the gate it files under, its slug and kind, the
    `gate:` value it links to (None under the no-gate item) and its statement."""

    gate: str
    slug: str
    kind: str
    link: str | None
    statement: str | None


@dataclass(frozen=True)
class _Reading:
    """A task's or check's status by its last counted record, and that
    record's key: (at, the contract's folder position, the record's position)."""

    status: str
    key: tuple


def gate_list() -> list[dict]:
    """The kit's gates in registry order, each an id, a name, a page and its
    conditions in the page's order, each an id and a name (G0's with rules)."""
    return yaml.safe_load(GATES_PATH.read_text(encoding="utf-8"))["gates"]


def task_list() -> list[dict]:
    """The seven tasks in order, each an id, a name and a page."""
    return yaml.safe_load(TASKS_PATH.read_text(encoding="utf-8"))["tasks"]


def build(root: Path, cache: dict[str, G0Reading] | None = None
          ) -> tuple[list[Item], list[str]]:
    """The tree in print order, and one line per source that could not be read.

    `cache` maps a contract id to its `G0` reading, the verdict's and its
    conditions', kept by the caller between prints; without one, every
    verdict is read afresh.
    """
    problems: list[str] = []
    gates = {gate["id"]: gate for gate in gate_list()}
    tasks = {task["id"]: task for task in task_list()}
    order = list(gates)
    active = _in_order(active_gates(root, problems), order)
    upcoming = next_gate(active, order)
    findings = read_findings(root, problems)
    items = _gate_items(order, active, findings, gates)
    contracts = [_contract_item(root, cid, instance, active, upcoming, gates, tasks)
                 for cid, instance in read_contracts(root, problems)]
    items += contracts
    derive(root, contracts, read_progress(root, problems), cache)
    return items, problems


def next_gate(active: list[str], order: list[str]) -> str | None:
    """The gate a contract's work reaches next: the first in the kit's order
    after the last active gate the kit lists; the first gate when none is
    active; None after the last."""
    known = [gate for gate in active if gate in order]
    if not known:
        return order[0] if order else None
    after = order.index(known[-1]) + 1
    return order[after] if after < len(order) else None


def text(value) -> str | None:
    """A source field as a plain name or a summary: ends stripped, each line
    break one space; None when the field is not text or is blank."""
    if not isinstance(value, str):
        return None
    return " ".join(value.strip().splitlines()) or None


def drift(path: Path) -> str | None:
    """A contract's drift mark from the feature doc at `path`: `no feature
    document` when no file is there, `no "Ready:" row` when no `Ready:` row
    names an `rM` or the file cannot be read as text, `stale: document rD,
    contract from rM` when the document's revision passed the contract's,
    else None. Only the first table is read, and none of its words print."""
    if not path.is_file():
        return NO_DOCUMENT
    try:
        lines = path.read_bytes().decode("utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError):
        return NO_READY
    document = contract = None
    newest = -1  # the N of the `Ready:` row that gave `contract`
    for cell in _last_cells(lines):
        match = _REVISION.match(cell)
        if match is None:
            continue
        n, rest = int(match.group(1)), cell[match.end():]
        if rest.startswith("Ready:"):
            derived = _DERIVED.search(rest)
            if derived is not None and n >= newest:  # a tie: the lower row wins
                newest, contract = n, int(derived.group(1))
        elif not rest.startswith("Measured:"):
            document = n if document is None else max(document, n)
    if contract is None:
        return NO_READY
    if document is not None and document > contract:
        return f"stale: document r{document}, contract from r{contract}"
    return None


def _last_cells(lines: list[str]):
    """The last cell of each row of the first table, the first run of lines
    that open on `|`, blanks stripped; a row's one closing pipe is dropped
    first, and a row without it still counts."""
    started = False
    for line in lines:
        row = line.strip()
        if not row.startswith("|"):
            if started:
                return
            continue
        started = True
        if row.endswith("|") and not row.endswith("\\|"):
            row = row[:-1]
        yield _PIPE.split(row)[-1].strip()


def derive(root: Path, contracts: list[Item], progress: dict[str, list[Record]],
           cache: dict[str, G0Reading] | None = None) -> None:
    """Set every status under the contracts, the verdicts' evidence, the G0
    conditions' diagnostics and the current mark; the gate items and their
    conditions keep `to do`."""
    readings: dict[str, _Reading] = {}
    # Each check's last run and each task's own last record, whatever closed
    # it after, and each unit's and contract's latest close.
    own: dict[str, Record] = {}
    latest: tuple[tuple, Item] | None = None  # the greatest counted key, its contract
    for position, contract in enumerate(contracts):
        key = _apply(contract, position, progress.get(contract.id, []), readings, own)
        if key is not None and (latest is None or key > latest[0]):
            latest = (key, contract)
    for contract in contracts:
        for item in _walk(contract):
            if item.level in ("task", "check") and item.id in readings:
                item.status = readings[item.id].status
            record = own.get(item.id)
            if record is None:
                continue
            if item.level == "check" and record.run == record.expect == "green":
                item.evidence = run_evidence(record)
            elif item.level == "task" and record.state == item.status == DONE:
                item.evidence = state_evidence(record)
            elif item.level == "task" and record.state == item.status == BLOCKED:
                item.evidence = f"because {record.reason}" if record.reason else None
    current = _current(contracts, readings, latest[1] if latest else None)
    if current is not None:
        if current.id.rsplit("/", 1)[-1] in APPROVALS:
            current.status = WAITING
            # Never blocked or done, so it has no evidence of its own.
            current.evidence = f"seat: {', '.join(current.seats)}" if current.seats else None
        current.marks.append(CURRENT)
    _verdicts(root, contracts, {} if cache is None else cache)
    for contract in contracts:
        _roll_up(contract, contract.id in own)
        for item in _walk(contract):
            if item.level in ("unit", "contract") and item.status == DONE and item.id in own:
                item.evidence = state_evidence(own[item.id])


def _apply(contract: Item, position: int, records: list[Record],
           readings: dict[str, _Reading], own: dict[str, Record]) -> tuple | None:
    """Apply one contract's records in file order, noting each item's own
    last record that fits it; the greatest key counted."""
    index = {item.id: item for item in _walk(contract)}
    latest = None
    for n, record in enumerate(records):
        key = (record.at, position, n)
        placed = _place(record, index.get(record.item))
        if placed is None:
            continue
        own[record.item] = record
        for item, status in placed:
            readings[item.id] = _Reading(status, key)
        latest = key if latest is None or key > latest else latest
    return latest


def _place(record: Record, target: Item | None) -> list[tuple[Item, str]] | None:
    """What a record sets, or None where its kind does not fit its item."""
    if target is None:
        return None
    if record.run is not None:
        return [(target, _judge(record.run, record.expect))] if target.level == "check" else None
    if target.level == "task":
        return [(target, record.state)]
    if target.level in ("unit", "contract") and record.state == DONE:
        # A close: a done record for every task and check under it, never a verdict.
        return [(item, DONE) for item in _walk(target) if item.level in ("task", "check")]
    return None


def _judge(run: str, expect: str) -> str:
    """A check run judged by its expectation: an expected red is under way."""
    if run != expect:
        return FAILED
    return DOING if run == "red" else DONE


def _current(contracts: list[Item], readings: dict[str, _Reading],
             latest: Item | None) -> Item | None:
    """The task whose `doing` record is latest; else the first `to do` task
    in the contract with the latest counted record; else none."""
    doing = [(readings[item.id].key, item) for contract in contracts
             for item in _walk(contract)
             if item.level == "task" and item.id in readings
             and readings[item.id].status == DOING]
    if doing:
        return max(doing, key=lambda pair: pair[0])[1]
    if latest is None:
        return None
    return next((item for item in _walk(latest)
                 if item.level == "task" and item.status == TO_DO), None)


def _verdicts(root: Path, contracts: list[Item], cache: dict[str, G0Reading]) -> None:
    """Each active `G0` verdict from the validator, with its command and
    `HEAD`, and `dirty` when its contract file differs from `HEAD`, and each
    of its conditions from the same reading over its own rules; git runs
    twice per print, and only when an active `G0` shows. A reading in
    `cache` stands in for the validator, and each new reading joins it; the
    schema loads only when the validator runs. A contract the tree cannot
    read as a mapping reads only its schema condition; the others keep `to
    do` and list nothing."""
    verdicts = [(contract.id, item) for contract in contracts
                for item in contract.children
                if item.level == "verdict" and item.id == f"{contract.id}/G0"
                and INACTIVE not in item.marks]
    if not verdicts:
        return
    rules = condition_rules()
    schema = None
    head = head_id(root)
    dirty = dirty_contracts(root)
    for cid, verdict in verdicts:
        path = f"specs/{cid}/contract.yaml"
        if cid not in cache:
            schema = checker.load_schema() if schema is None else schema
            cache[cid] = g0_status(root / path, schema)
        reading = cache[cid]
        verdict.status = reading.status
        verdict.evidence = (f"via python -m taskcontract validate {path} "
                            f"--profile ready at {head}"
                            + (f" {DIRTY}" if cid in dirty else ""))
        for condition in verdict.children:
            key = condition.id.rsplit("/", 1)[-1]
            if reading.mapping or key == SCHEMA_CONDITION:
                condition.status, condition.diagnostics = condition_reading(
                    reading, rules.get(key, []))


def run_evidence(record: Record) -> str | None:
    """A green run's evidence: its command, the `HEAD` it ran at, and `dirty`
    when a tracked file differed; each part only when the record has it."""
    parts = []
    if record.command is not None:
        parts.append(f"via {record.command}")
    if record.head is not None:
        parts.append(f"at {record.head}")
    if record.dirty:
        parts.append(DIRTY)
    return " ".join(parts) or None


def state_evidence(record: Record) -> str | None:
    """A done record's evidence: the seat it names, the `HEAD` it was
    written at, and `dirty` when a tracked file differed; each part only when
    the record has it."""
    parts = []
    if record.by is not None:
        parts.append(f"by {record.by}")
    if record.head is not None:
        parts.append(f"at {record.head}")
    if record.dirty:
        parts.append(DIRTY)
    return " ".join(parts) or None


def g0_status(path: Path, schema: dict) -> G0Reading:
    """The validator's reading: the errors at both profiles, the verdict
    they give (draft-red `failed`, ready-green `done`, `TC003` at ready
    `blocked`, else `to do`), and whether the file reads as a mapping, which
    decides whether the joins' conditions can read it. Warnings never count."""
    def errors(profile: str) -> tuple[tuple[str, str], ...]:
        return tuple((v.rule, v.message)
                     for v in checker.validate_path(path, profile=profile, schema_doc=schema)
                     if v.severity == "error")

    draft, ready = errors("draft"), errors("ready")
    return G0Reading(_g0(draft, ready), draft, ready,
                     _load(path, path.parent, [], "contract") is not None)


def condition_reading(reading: G0Reading, rules: list[str]) -> tuple[str, list[str]]:
    """A G0 condition's status by the verdict's rule over its own rules'
    errors, and its diagnostics: none when done, else the messages of the
    profile that decided it (draft when failed, ready otherwise), in the
    validator's order, each on one line and each text once."""
    draft = tuple(pair for pair in reading.draft if pair[0] in rules)
    ready = tuple(pair for pair in reading.ready if pair[0] in rules)
    status = _g0(draft, ready)
    if status == DONE:
        return status, []
    messages = draft if status == FAILED else ready
    return status, list(dict.fromkeys(" ".join(message.splitlines())
                                      for _, message in messages))


def _g0(draft: tuple, ready: tuple) -> str:
    """The rule over (rule, message) errors: draft-red `failed`, ready-green
    `done`, `TC003` at ready `blocked`, else `to do`."""
    if draft:
        return FAILED
    if not ready:
        return DONE
    return BLOCKED if any(rule == "TC003" for rule, _ in ready) else TO_DO


def condition_rules() -> dict[str, list[str]]:
    """The validator codes each G0 condition owns, by the condition's id."""
    g0 = next((gate for gate in gate_list() if gate.get("id") == "G0"), None)
    return {condition["id"]: list(condition.get("rules") or [])
            for condition in _conditions(g0)}


def dirty_contracts(root: Path) -> set[str]:
    """The ids whose specs/<id>/contract.yaml differs from `HEAD`: modified,
    staged or not, or not in `HEAD` at all. One git call for every contract;
    none outside git."""
    result = run_git(root, "--no-optional-locks", "status", "--porcelain", "-z",
                     "--untracked-files=all",
                     "--", ":(glob)specs/*/contract.yaml")
    if result is None or result.returncode != 0:
        return set()
    dirty: set[str] = set()
    entries = iter(result.stdout.split("\0"))
    for entry in entries:
        if len(entry) < 4:
            continue
        if entry[0] in "RC":
            next(entries, None)  # a rename's or copy's source path follows
        # The path runs from the repo's top; its last three parts are ours.
        parts = entry[3:].split("/")
        if len(parts) >= 3:
            dirty.add(parts[-2])
    return dirty


def _roll_up(item: Item, closed: bool = False) -> None:
    """A unit's or contract's status from its children's but the inactive
    verdict's, and a closed contract's from its units' alone, `done` when it
    has none; a verdict done alone never starts its contract."""
    for child in item.children:
        if child.level == "unit":
            _roll_up(child)
    children = [child for child in item.children if INACTIVE not in child.marks
                and not (closed and child.level == "verdict")]
    statuses = [child.status for child in children]
    first = next((status for status in ROLL_UP if status in statuses), None)
    if first is not None:
        item.status = first
    elif (statuses or closed) and all(status == DONE for status in statuses):
        item.status = DONE
    elif any(child.status == DONE for child in children if child.level != "verdict"):
        item.status = DOING
    else:
        item.status = TO_DO


def _walk(item: Item):
    """The item and everything under it, in print order."""
    yield item
    for child in item.children:
        yield from _walk(child)


def active_gates(root: Path, problems: list[str]) -> list[str]:
    """`active_gates` from .sdlc/config.yaml; none when there is no config."""
    path = root / ".sdlc" / "config.yaml"
    if not path.is_file():
        return []
    doc = _load(path, root, problems, "config")
    gates = doc.get("active_gates") if doc is not None else None
    return [g for g in gates if isinstance(g, str)] if isinstance(gates, list) else []


def notify_command(root: Path) -> str | None:
    """`tree.notify` from .sdlc/config.yaml, as written; None when it is not
    set to text that holds more than blanks, or the config is missing or
    unreadable (the tree itself names an unreadable config)."""
    path = root / ".sdlc" / "config.yaml"
    if not path.is_file():
        return None
    doc = _load(path, root, [], "config")
    section = doc.get("tree") if doc is not None else None
    command = section.get("notify") if isinstance(section, dict) else None
    return command if isinstance(command, str) and command.strip() else None


def pane_settings(root: Path, problems: list[str]) -> dict[str, object]:
    """`tree.pane` from .sdlc/config.yaml: each key set to a usable value.
    `parts` is a list of names from PARTS, `fold` one of FOLDS; any other
    value of a present key is left out, with one line added to `problems`
    that names it, the parts line before the fold line. Nothing is added
    for a missing or unreadable config (the tree itself names an unreadable
    one) or an absent key."""
    path = root / ".sdlc" / "config.yaml"
    if not path.is_file():
        return {}
    doc = _load(path, root, [], "config")
    section = doc.get("tree") if doc is not None else None
    pane = section.get("pane") if isinstance(section, dict) else None
    if not isinstance(pane, dict):
        return {}
    settings: dict[str, object] = {}
    if "parts" in pane:
        parts = pane["parts"]
        # The value named: the first entry outside the names, or the whole value.
        bad = [parts] if not isinstance(parts, list) else [
            entry for entry in parts if not (isinstance(entry, str) and entry in PARTS)]
        if bad:
            problems.append(f"pane parts ignored: {bad[0]} - give a list from {', '.join(PARTS)}")
        else:
            settings["parts"] = parts
    if "fold" in pane:
        fold = pane["fold"]
        if isinstance(fold, str) and fold in FOLDS:
            settings["fold"] = fold
        else:
            problems.append(f"pane fold ignored: {fold} - give {' or '.join(FOLDS)}")
    return settings


def read_findings(root: Path, problems: list[str]) -> list[Finding]:
    """One finding per file under .sdlc/findings/, in file-name order."""
    folder = root / ".sdlc" / "findings"
    if not folder.is_dir():
        return []
    found: list[Finding] = []
    for path in sorted(folder.glob("*.yaml"), key=lambda p: p.name):
        if path.name == FORM:
            continue
        doc = _load(path, root, problems, "finding")
        if doc is not None:
            kind = doc.get("kind")
            gate = gate_of(doc.get("gate"))
            found.append(Finding(gate, path.stem, "none" if kind is None else str(kind),
                                 None if gate == NO_GATE else doc["gate"].strip(),
                                 text(doc.get("statement"))))
    return found


def gate_of(value) -> str:
    """The gate a finding's `gate:` field names; a condition names its gate
    by the part before its dot."""
    text = value.strip() if isinstance(value, str) else ""
    if not text or text == NO_GATE:
        return NO_GATE
    return text.split(".", 1)[0]


def read_contracts(root: Path, problems: list[str]) -> list[tuple[str, dict | None]]:
    """(id, contract) per specs/<id>/contract.yaml in folder order; None if unreadable."""
    specs = root / "specs"
    if not specs.is_dir():
        return []
    paths = sorted(specs.glob("*/contract.yaml"), key=lambda p: p.parent.name)
    return [(path.parent.name, _load(path, root, problems, "contract")) for path in paths]


def check_ids(sketches: list) -> list[str]:
    """One id per sketch line by the trailing-parentheses rule; a line that
    names none, or repeats an id, is `sketch-<n>` by its position from 1."""
    ids: list[str] = []
    for n, sketch in enumerate(sketches, start=1):
        named = _named(sketch)
        ids.append(named if named and named not in ids else f"sketch-{n}")
    return ids


def _named(sketch) -> str | None:
    match = _TRAILING.search(sketch) if isinstance(sketch, str) else None
    if match is None:
        return None
    parts = [part.strip() for part in match.group(1).split(",")]
    return "+".join(parts) if all(_CHECK_ID.match(part) for part in parts) else None


def _gate_items(order: list[str], active: list[str], findings: list[Finding],
                gates: dict[str, dict]) -> list[Item]:
    """Each active gate and each gate a finding names, then the no-gate item.
    A gate opens into its conditions, each holding the findings that name
    it, then the gate's other findings."""
    named = [finding.gate for finding in findings]
    items = []
    for gate in _in_order(active + named, order):
        base = f"gates/{gate}"
        conditions = _condition_items(base, gates.get(gate))
        for condition in conditions:
            condition.children = _finding_items(
                condition.id, gate, condition.id.rsplit("/", 1)[-1], findings, gates)
        items.append(Item(base, "gate", marks=[] if gate in active else [INACTIVE],
                          children=conditions + _finding_items(base, gate, None,
                                                               findings, gates),
                          name=_name(gates.get(gate)), page=_page(gates.get(gate))))
    if NO_GATE in named:
        items.append(Item(f"gates/{NO_GATE}", "none",
                          children=_finding_items(f"gates/{NO_GATE}", NO_GATE, None,
                                                  findings, gates)))
    return items


def _finding_items(base: str, gate: str, condition: str | None,
                   findings: list[Finding], gates: dict[str, dict]) -> list[Item]:
    """The findings under `base`: those of `gate` whose `gate:` value is
    `condition` when its gate lists it, or with `condition` None, the rest."""
    return [Item(f"{base}/{finding.slug}", "finding", status=None,
                 kind=finding.kind, name=finding.statement,
                 links=[f"gate: {finding.link}"] if finding.link else [],
                 source=f".sdlc/findings/{finding.slug}.yaml")
            for finding in findings
            if finding.gate == gate and _condition_of(finding, gates) == condition]


def _condition_of(finding: Finding, gates: dict[str, dict]) -> str | None:
    """The condition a finding stands under: its `gate:` value when its gate
    lists that condition, else None."""
    listed = [condition.get("id") for condition in _conditions(gates.get(finding.gate))]
    return finding.link if finding.link in listed else None


def _condition_items(base: str, entry: dict | None) -> list[Item]:
    """A gate's conditions under `base`, in its page's order, each reading
    `to do`, with its name as its plain name and its gate's page."""
    return [Item(f"{base}/{condition.get('id')}", "condition",
                 name=text(condition.get("name")), page=_page(entry))
            for condition in _conditions(entry)]


def _conditions(entry: dict | None) -> list[dict]:
    """The conditions a gate's entry in the kit's list gives, in order."""
    conditions = entry.get("conditions") if entry is not None else None
    return [c for c in conditions if isinstance(c, dict)] if isinstance(conditions, list) else []


def _contract_item(root: Path, cid: str, instance: dict | None, active: list[str],
                   upcoming: str | None, gates: dict[str, dict],
                   tasks: dict[str, dict]) -> Item:
    """A contract with its drift mark: its verdict at each active gate, then
    the upcoming gate's verdict marked `inactive`, each opening into its
    gate's conditions; then its units. An unreadable contract keeps its
    verdicts and its mark, and shows no unit."""
    doc = f"docs/features/{cid}.md"
    source = f"specs/{cid}/contract.yaml"
    verdicts = [(gate, []) for gate in active]
    if upcoming is not None:
        verdicts.append((upcoming, [INACTIVE]))
    mark = drift(root / doc)
    item = Item(cid, "contract", marks=[mark] if mark else [],
                children=[Item(f"{cid}/{gate}", "verdict", marks=marks,
                               children=_condition_items(f"{cid}/{gate}", gates.get(gate)),
                               name=_name(gates.get(gate)),
                               source=source, page=_page(gates.get(gate)))
                          for gate, marks in verdicts],
                doc=doc if (root / doc).is_file() else None,
                name=(text(instance.get("title")) if instance is not None else None) or NO_TITLE,
                summary=text(instance.get("intent")) if instance is not None else None,
                source=source)
    for index, uid, unit, deps in _units(instance):
        base = f"{cid}/{uid}"
        place = ("decomposition", index)
        sketches = unit.get("acceptance_sketch")
        sketches = sketches if isinstance(sketches, list) else []
        seats = _seats(unit.get("confirmed_by"))
        unit_item = Item(base, "unit",
                         children=[Item(f"{base}/{task}", "task", name=_name(entry),
                                        page=_page(entry),
                                        seats=seats if task in APPROVALS else [])
                                   for task, entry in tasks.items()],
                         links=[f"depends_on: {cid}/{dep}" for dep in dict.fromkeys(deps)],
                         name=text(unit.get("done_means")), source=source, place=place)
        unit_item.children += [
            Item(f"{base}/{check}", "check", name=text(sketch),
                 source=source, place=place + ("acceptance_sketch", n))
            for n, (check, sketch) in enumerate(zip(check_ids(sketches), sketches))]
        item.children.append(unit_item)
    return item


def _seats(value) -> list[str]:
    """A unit's `confirmed_by` seats in order, each once, by the text rule;
    none when it is not a list, and no entry that gives no text."""
    if not isinstance(value, list):
        return []
    return list(dict.fromkeys(seat for seat in map(text, value) if seat))


def _name(entry: dict | None) -> str | None:
    """A gate's or task's name from its entry in the kit's list, by the text rule."""
    return text(entry.get("name")) if entry is not None else None


def _page(entry: dict | None) -> str | None:
    """A gate's or task's kit page from its entry in the kit's list, as written."""
    page = entry.get("page") if entry is not None else None
    return page if isinstance(page, str) else None


def _units(instance: dict | None) -> list[tuple[int, str, dict, list[str]]]:
    """(index, id, unit, depends_on) per unit with a usable id; of a
    duplicate id (TC013), the first only, as the unit graph draws it
    (ADR 0024)."""
    if instance is None:
        return []
    decomposition = instance.get("decomposition")
    seen: set[str] = set()
    out: list[tuple[int, str, dict, list[str]]] = []
    for index, uid, deps in unit_rows(instance):
        if uid not in seen:
            seen.add(uid)
            out.append((index, uid, decomposition[index], deps))
    return out


def reference(root: Path, item: Item) -> str | None:
    """`<path>:<line>` for the item's source file, or None when it has none:
    the line its entry starts at, else 1. It parses the file afresh, so only
    the query calls it, and only for the items it prints."""
    if item.source is None:
        return None
    node = _node(root / item.source, item.place) if item.place else None
    return f"{item.source}:{node.start_mark.line + 1 if node is not None else 1}"


def _node(path: Path, place: tuple):
    """The YAML node the keys in `place` lead to, or None where the file no
    longer holds it; a repeated key gives its last value, as the loader does."""
    try:
        node = yaml.compose(path.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        return None
    for key in place:
        if isinstance(key, int):
            if not isinstance(node, yaml.SequenceNode) or key >= len(node.value):
                return None
            node = node.value[key]
        elif isinstance(node, yaml.MappingNode):
            node = next((value for name, value in reversed(node.value)
                         if isinstance(name, yaml.ScalarNode) and name.value == key), None)
            if node is None:
                return None
        else:
            return None
    return node


def _in_order(ids: list[str], order: list[str]) -> list[str]:
    """`ids` once each: the kit's gates in registry order, then any other id."""
    wanted = [gate for gate in dict.fromkeys(ids) if gate != NO_GATE]
    return [gate for gate in order if gate in wanted] + [
        gate for gate in wanted if gate not in order]


def _load(path: Path, root: Path, problems: list[str], what: str) -> dict | None:
    """The YAML mapping at `path`, or None with one line added to `problems`."""
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        reason = f"YAML error at line {mark.line + 1}" if mark is not None else "YAML error"
    except (OSError, UnicodeDecodeError) as exc:
        reason = getattr(exc, "strerror", None) or "cannot be read"
    else:
        if isinstance(doc, dict):
            return doc
        reason = "not a mapping"
    problems.append(f"unreadable {what}: {_rel(path, root)} ({reason})")
    return None


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
