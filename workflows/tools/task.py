"""The execution team's task command: `start` opens one task step, `end`
closes it, `fail` counts a failed round and `stop` ends the run on a question,
an error or a refusal.

    python workflows/tools/task.py start --unit {contract}/{unit} --task {task}
        --operator {operator} [--root DIR]
    python workflows/tools/task.py end --unit {contract}/{unit} --task {task}
        [--by SEAT] [--root DIR]
    python workflows/tools/task.py end --run --unit {contract}/{unit} [--root DIR]
    python workflows/tools/task.py fail --unit {contract}/{unit} --task {task}
        [--reason TEXT] [--operator {operator}] [--root DIR]
    python workflows/tools/task.py stop --unit {contract}/{unit} --task {task}
        --operator {operator} --kind question|error|refusal --question TEXT
        [--root DIR]
    python workflows/tools/task.py keep --unit {contract}/{unit}
        --key draft|draft-file|receipts|commit (--file PATH | --value TEXT)
        [--root DIR]
    python workflows/tools/task.py restart --unit {contract}/{unit}
        [--go [--fresh] --scratch DIR] [--root DIR]

`start` checks, in this order, that the repository declares a test command,
that the root is a git repository and that no task is running, then runs
`taskcontract progress start` for the task. Each refusal prints one line on
stderr, writes nothing and exits 1; `progress start`'s own line prints as it
gave it. On acceptance `start` writes `sdlc-task.json` into the git folder,
the running task, its operator, its round and its unit, and prints `Task
{task}: {Operator}, round {n}`: n is one more than the failed rounds of the task's
channel (write-tests or green) in the unit's rounds file, which holds the
failed reasons a task; the task's own, when higher.

A unit's records stand in its run folder, `sdlc-run/{contract}/{unit}/` in the
git folder, made on the first write: `run.json`, `rounds.json` and
`stop.json`, each written whole, so a killed session leaves the old file or
the new one, and `draft/`, QA's kept draft test file. A file that does not
parse reads as absent, except to `restart`, which reports it. `run.json` holds
the unit, the branch and HEAD at the unit's first start, the task in hand and
the values `keep` holds for later tasks; `start` writes it, and `stop` when
none stands. `stop.json` holds the latest stop only: a question, an error or
a refusal with its text, or a third failed round with each round's reason.
Nothing removes another unit's folder.

`end` runs `taskcontract progress done` for the task and removes the task
file; when `progress done` refuses, its line prints as it gave it and the
task file stays. `end --run` removes the task file and the unit's run folder.
`fail` records a failed round and removes the task file; the third failed
round of a task also writes the stop record and exits 1 with the failures.
`stop` removes the task file, writes the stop record and exits 1; a question
or an error prints the operator's words, a refusal prints nothing. Both keep
the rounds file. Each command exits 2 on a usage error, a `--unit` that is
not two names joined by one `/` included, and one name holding a colon.

`keep` sets one key of `run.json`'s `kept`, replacing its old value: `draft`
and `receipts` hold the JSON given, parsed; `commit` the text given;
`draft-file` copies the file into `draft/`. `restart` is read-only: it prints
one JSON line, the run's state (`none`, `stopped` or `abandoned`) with the
task, operator, round, stop kind and text, the kept values and `progress`, one
line for each task before the one in hand whose progress record is not done
(the run record wins); it refuses on
one line when the session is on another branch than the run or a record does
not parse. With `--go` it also removes the stop record and the task file, the
task file only when it names this unit, and
writes the kept draft under the scratch folder; `--fresh` with it also clears
the failed rounds of the stopped task's channel, so its next three rounds
count from one.

The script imports the `taskcontract` that sits beside it, whichever package
of that name the environment holds.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

# The plugin root goes first, so the taskcontract beside this script wins.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import yaml  # noqa: E402

from taskcontract.declaration import read_test  # noqa: E402
from taskcontract.progress import read_progress, record_state  # noqa: E402
from taskcontract.tree import TASKS_PATH  # noqa: E402

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
TASK_FILE = "sdlc-task.json"
RUN_DIR = "sdlc-run"
RUN_FILE = "run.json"
ROUNDS_FILE = "rounds.json"
STOP_FILE = "stop.json"
MAX_ROUNDS = 3
STOP_KINDS = ["question", "error", "refusal"]
# The tasks in the order a unit runs them; the tree lists them in another.
RESTART_ORDER = ["write-tests", "approve-tests", "prove-red", "green",
                 "approve-commit", "commit", "two-key"]
KEEP_KEYS =["draft", "draft-file", "receipts", "commit"]
ROOT_HELP = "repo root that holds specs/ and .sdlc/ (default: cwd)"
# Each operator id, and the name the start line prints for it.
OPERATORS = {
    "qa": "QA",
    "qa-verifier": "QA verifier",
    "developer": "Developer",
    "dev-verifier": "Dev verifier",
    "receipts": "receipts",
    "orchestrator": "Orchestrator",
}
# The task whose failed rounds a task shares: a QA-channel check returns to
# write-tests, a Developer-channel check to green.
CHANNELS = {
    "approve-tests": "write-tests",
    "prove-red": "write-tests",
    "approve-commit": "green",
    "commit": "green",
    "two-key": "green",
}


def task_ids() -> list[str]:
    """The task ids, in order, from the one list the tree shows."""
    doc = yaml.safe_load(TASKS_PATH.read_text(encoding="utf-8"))
    return [task["id"] for task in doc["tasks"]]


def unit_arg(text: str) -> str:
    """The unit when it is two names joined by one `/`; each name is a folder
    name, so neither is empty, `.` or `..`, and neither holds a separator or a
    colon."""
    halves = text.split("/")
    if len(halves) != 2 or any(not half or half in (".", "..") or "\\" in half
                               or ":" in half for half in halves):
        raise argparse.ArgumentTypeError(
            f"invalid unit {text!r}: expected {{contract}}/{{unit}}")
    return text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task.py", description="open one task step of the execution team")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser(
        "start", help="record a task step doing and write the running task's file")
    start.add_argument("--unit", required=True, type=unit_arg, metavar="CONTRACT/UNIT",
                       help="the unit, as {contract}/{unit}")
    start.add_argument("--task", required=True, choices=task_ids(),
                       help="the task step to open")
    start.add_argument("--operator", required=True, choices=list(OPERATORS),
                       help="the operator that does the task")
    start.add_argument("--root", default=".", help=ROOT_HELP)
    end = sub.add_parser(
        "end", help="record a task step done and remove the task file")
    end.add_argument("--unit", type=unit_arg, metavar="CONTRACT/UNIT",
                     help="the unit, as {contract}/{unit}; required")
    end.add_argument("--task", choices=task_ids(),
                     help="the task step to close; required without --run")
    end.add_argument("--by", metavar="SEAT",
                     help="the seat that holds an approval")
    end.add_argument("--run", action="store_true",
                     help="end the run: remove the task file and the unit's run folder")
    end.add_argument("--root", default=".", help=ROOT_HELP)
    fail = sub.add_parser(
        "fail", help="count one failed round of a task and remove the task file")
    fail.add_argument("--unit", required=True, type=unit_arg, metavar="CONTRACT/UNIT",
                      help="the unit, as {contract}/{unit}")
    fail.add_argument("--task", required=True, choices=task_ids(),
                      help="the task whose round failed")
    fail.add_argument("--reason", help="why the round failed")
    fail.add_argument("--operator", choices=list(OPERATORS),
                      help="the operator whose round failed")
    fail.add_argument("--root", default=".", help=ROOT_HELP)
    stop = sub.add_parser(
        "stop", help="end the run on an operator's question, error or refusal")
    stop.add_argument("--unit", required=True, type=unit_arg, metavar="CONTRACT/UNIT",
                      help="the unit, as {contract}/{unit}")
    stop.add_argument("--task", required=True, choices=task_ids(),
                      help="the task that stopped")
    stop.add_argument("--operator", required=True, choices=list(OPERATORS),
                      help="the operator that stopped")
    stop.add_argument("--kind", required=True, choices=STOP_KINDS,
                      help="why the run stops")
    stop.add_argument("--question", required=True, help="the operator's words")
    stop.add_argument("--root", default=".", help=ROOT_HELP)
    keep = sub.add_parser(
        "keep", help="keep one value of the run for the tasks that follow")
    keep.add_argument("--unit", required=True, type=unit_arg, metavar="CONTRACT/UNIT",
                      help="the unit, as {contract}/{unit}")
    keep.add_argument("--key", required=True, choices=KEEP_KEYS,
                      help="the value to keep")
    source = keep.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", metavar="PATH",
                        help="the file that holds the value (a JSON file; any file for draft-file)")
    source.add_argument("--value", metavar="TEXT", help="the value (JSON for draft and receipts)")
    keep.add_argument("--root", default=".", help=ROOT_HELP)
    restart = sub.add_parser(
        "restart", help="print the state of the unit's run; with --go, restart it")
    restart.add_argument("--unit", required=True, type=unit_arg, metavar="CONTRACT/UNIT",
                         help="the unit, as {contract}/{unit}")
    restart.add_argument("--go", action="store_true",
                         help="remove the stop record and the task file (only when it names this unit), write the kept draft")
    restart.add_argument("--fresh", action="store_true",
                         help="with --go, also clear the failed rounds of the stopped task's channel")
    restart.add_argument("--scratch", metavar="DIR",
                         help="the session's scratch folder; required with --go")
    restart.add_argument("--root", default=".", help=ROOT_HELP)
    return parser


def git_folder(root: str) -> Path | None:
    """The folder `git rev-parse --absolute-git-dir` names at the root, or None
    when the root is no git repository or git cannot start."""
    try:
        result = subprocess.run(
            ["git", "-C", root, "rev-parse", "--absolute-git-dir"],
            capture_output=True, encoding="utf-8", errors="replace",
            creationflags=NO_WINDOW)
    except OSError:
        return None
    folder = (result.stdout or "").strip()
    return Path(folder) if result.returncode == 0 and folder else None


def git_line(root: str, *argv: str) -> str | None:
    """The first line `git -C root argv` prints; None when git fails or cannot
    start, or prints nothing."""
    try:
        result = subprocess.run(
            ["git", "-C", root, *argv], capture_output=True, encoding="utf-8",
            errors="replace", creationflags=NO_WINDOW)
    except OSError:
        return None
    line = (result.stdout or "").strip()
    return line if result.returncode == 0 and line else None


def running_task(path: Path) -> str | None:
    """The task the file names; None when the file is absent or is not a JSON
    object with a non-empty string `task`."""
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    task = doc.get("task") if isinstance(doc, dict) else None
    return task if isinstance(task, str) and task else None


def refuse(line: str) -> int:
    print(line, file=sys.stderr)
    return 1


def read_rounds(path: Path) -> tuple[str | None, dict[str, list]]:
    """The unit the rounds file holds and its failed reasons a task; (None, {})
    when the file is absent or is not an object of that shape."""
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, {}
    unit = doc.get("unit") if isinstance(doc, dict) else None
    rounds = doc.get("rounds") if isinstance(doc, dict) else None
    if not isinstance(unit, str) or not isinstance(rounds, dict):
        return None, {}
    return unit, {task: reasons for task, reasons in rounds.items()
                  if isinstance(reasons, list)
                  and all(r is None or isinstance(r, str) for r in reasons)}


def failed_reasons(path: Path, unit: str, task: str) -> list:
    """The reasons of the task's failed rounds for the unit, in order."""
    held, rounds = read_rounds(path)
    return rounds.get(task, []) if held == unit else []


def one_line(text: str) -> str:
    """The text with each whitespace run collapsed to one space, trimmed."""
    return " ".join(text.split())


def remove(*paths: Path) -> None:
    for path in paths:
        path.unlink(missing_ok=True)


def run_folder(folder: Path, unit: str) -> Path:
    """The unit's run folder under the git folder; it may not exist yet."""
    return folder.joinpath(RUN_DIR, *unit.split("/"))


def write_whole(path: Path, doc: dict) -> None:
    """Write the JSON to a temporary file beside the path, then replace the
    path with it: a killed session leaves the old file or the new one."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as out:
            json.dump(doc, out)
        os.replace(name, path)
    except BaseException:
        remove(Path(name))
        raise


def failed_counts(path: Path, unit: str) -> dict[str, int]:
    """The failed rounds the rounds file holds for write-tests and green."""
    return {name: len(failed_reasons(path, unit, name))
            for name in ("write-tests", "green")}


def round_number(path: Path, unit: str, task: str) -> int:
    """One more than the most failed rounds of the task or its channel."""
    return 1 + max(len(failed_reasons(path, unit, name))
                   for name in (task, CHANNELS.get(task, task)))


def write_stop(folder: Path, args: argparse.Namespace, kind: str, extra: dict) -> None:
    """Write the unit's stop record whole, replacing the one before."""
    run = run_folder(folder, args.unit)
    rounds_path = run / ROUNDS_FILE
    write_whole(run / STOP_FILE, {
        "unit": args.unit, "task": args.task,
        "operator": getattr(args, "operator", None), "kind": kind,
        "round": round_number(rounds_path, args.unit, args.task),
        "failed": failed_counts(rounds_path, args.unit), **extra,
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})


def read_object(path: Path) -> dict | None:
    """The JSON object the file holds; None when the file is absent or is not
    one."""
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return doc if isinstance(doc, dict) else None


def new_run(root: str, unit: str, task: str) -> dict:
    """A unit's first run record: the branch and HEAD at the root, JSON null for
    HEAD in a repository with no commit."""
    return {"unit": unit, "branch": git_line(root, "branch", "--show-current") or "",
            "base": git_line(root, "rev-parse", "HEAD"), "task": task, "kept": {}}


def start(args: argparse.Namespace) -> int:
    """Open the task: 0 when started, 1 when refused."""
    task = args.task
    if read_test(Path(args.root)) is None:
        return refuse(f"Task {task} did not start: the repository declares no test command.")
    folder = git_folder(args.root)
    if folder is None:
        return refuse(f"Task {task} did not start: no git repository at {args.root}.")
    path = folder / TASK_FILE
    running = running_task(path)
    if running is not None:
        return refuse(f"Task {task} did not start: task {running} is running.")
    # progress start's own "doing" line is not this command's output.
    with contextlib.redirect_stdout(io.StringIO()):
        code = record_state(Path(args.root), "start", f"{args.unit}/{task}")
    if code != 0:
        return 1
    run = run_folder(folder, args.unit)
    number = round_number(run / ROUNDS_FILE, args.unit, task)
    held = read_object(run / RUN_FILE)
    write_whole(run / RUN_FILE, {**held, "task": task} if held is not None
                else new_run(args.root, args.unit, task))
    path.write_text(json.dumps({"task": task, "operator": args.operator, "round": number,
                                "unit": args.unit}), encoding="utf-8")
    print(f"Task {task}: {OPERATORS[args.operator]}, round {number}")
    return 0


def fail(args: argparse.Namespace) -> int:
    """Count one failed round: 0 on the first or second, 1 on the third."""
    folder = git_folder(args.root)
    if folder is None:
        return refuse(f"No git repository at {args.root}.")
    rounds_path = run_folder(folder, args.unit) / ROUNDS_FILE
    held, rounds = read_rounds(rounds_path)
    if held != args.unit:
        rounds = {}
    rounds[args.task] = [*rounds.get(args.task, []), args.reason]
    write_whole(rounds_path, {"unit": args.unit, "rounds": rounds})
    remove(folder / TASK_FILE)
    if len(rounds[args.task]) < MAX_ROUNDS:
        return 0
    write_stop(folder, args, "fail",
               {"round": MAX_ROUNDS,
                "reasons": [reason or "" for reason in rounds[args.task]]})
    print(f"Task {args.task} failed {MAX_ROUNDS} rounds. The run stops here; the failures follow.")
    for number, reason in enumerate(rounds[args.task], 1):
        print(f"  Round {number}: {one_line(reason or '') or 'no reason given'}")
    return 1


def stop(args: argparse.Namespace) -> int:
    """End the run on an operator's question, error or refusal: always 1."""
    folder = git_folder(args.root)
    if folder is not None:
        remove(folder / TASK_FILE)
        run_path = run_folder(folder, args.unit) / RUN_FILE
        if not run_path.exists():
            write_whole(run_path, new_run(args.root, args.unit, args.task))
        write_stop(folder, args, args.kind, {"text": args.question})
    if args.kind != "refusal":
        print(f"Task {args.task} stopped on a question from {OPERATORS[args.operator]}: "
              f"{one_line(args.question)}")
    return 1


def end(args: argparse.Namespace) -> int:
    """Close the task: 0 when recorded done, 1 when `progress done` refuses."""
    folder = git_folder(args.root)
    if args.run:
        if folder is not None:
            remove(folder / TASK_FILE)
            shutil.rmtree(run_folder(folder, args.unit), ignore_errors=True)
        return 0
    with contextlib.redirect_stdout(io.StringIO()):
        code = record_state(Path(args.root), "done", f"{args.unit}/{args.task}",
                            by=args.by)
    if code != 0:
        return 1
    if folder is not None:
        remove(folder / TASK_FILE)
    return 0


def keep_value(args: argparse.Namespace) -> object:
    """The value `keep` stores for the key: the JSON parsed for `draft` and
    `receipts`, the text for `commit`, the file's name in `draft/` for
    `draft-file`. Raises ValueError, with the usage message, when the key and
    the source do not fit."""
    if args.key == "draft-file":
        if args.file is None or not Path(args.file).is_file():
            raise ValueError("--key draft-file takes --file, the path of a file")
        return f"draft/{Path(args.file).name}"
    if args.key == "commit":
        if args.value is None:
            raise ValueError("--key commit takes --value, not --file")
        return args.value
    source, text = ("--file", None) if args.value is None else ("--value", args.value)
    try:
        if text is None:
            text = Path(args.file).read_text(encoding="utf-8")
        return json.loads(text)
    except (OSError, ValueError) as error:
        raise ValueError(f"{source} for --key {args.key} is not JSON: {error}") from None


def keep(args: argparse.Namespace) -> int:
    """Set one kept value of the unit's run: 0 when kept, 1 when no run stands."""
    folder = git_folder(args.root)
    if folder is None:
        return refuse(f"Nothing kept: no git repository at {args.root}.")
    run = run_folder(folder, args.unit)
    doc = read_object(run / RUN_FILE)
    if doc is None:
        return refuse(f"Nothing kept: unit {args.unit} has no run.json.")
    if args.key == "draft-file":
        (run / "draft").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.file, run / args.parsed)
    kept = doc.get("kept") if isinstance(doc.get("kept"), dict) else {}
    write_whole(run / RUN_FILE, {**doc, "kept": {**kept, args.key: args.parsed}})
    return 0


def run_state(args: argparse.Namespace, folder: Path) -> tuple[dict | None, str | None]:
    """The unit's state for `restart`: the line to print, or the refusal's line
    when a record does not parse or the run stopped on another branch."""
    contract, unit = args.unit.split("/")
    run_path = run_folder(folder, args.unit)
    run, stop = read_object(run_path / RUN_FILE), read_object(run_path / STOP_FILE)
    has_run, has_stop = (run_path / RUN_FILE).exists(), (run_path / STOP_FILE).exists()

    def refusal(record: str, why: str = "does not parse") -> str:
        return f"Execution did not restart: {record} of {contract} unit {unit} {why}."

    if has_run and run is None:
        return None, refusal(RUN_FILE)
    if has_stop and stop is None:
        return None, refusal(STOP_FILE)
    if has_stop and not has_run:
        return None, refusal(STOP_FILE, "has no run.json")
    state = {"state": "none", "task": None, "operator": None, "round": None,
             "kind": None, "text": None, "kept": {}, "progress": []}
    if run is None:
        return state, None
    branch = git_line(args.root, "branch", "--show-current") or ""
    if run.get("branch") != branch:
        return None, (f"Execution did not restart: the run stopped on branch "
                      f"{run.get('branch')}; this session is on {branch}.")
    state["kept"] = run["kept"] if isinstance(run.get("kept"), dict) else {}
    if stop is not None:
        reasons = stop.get("reasons")
        text = ("; ".join(r if isinstance(r, str) else "" for r in reasons)
                if stop.get("kind") == "fail" and isinstance(reasons, list)
                else stop.get("text"))
        return {**state, "state": "stopped", "task": stop.get("task"),
                "operator": stop.get("operator"), "round": stop.get("round"),
                "kind": stop.get("kind"), "text": text,
                "progress": disagreements(args, stop.get("task"))}, None
    running = read_object(folder / TASK_FILE)
    held = running is not None and running.get("unit") == args.unit \
        and isinstance(running.get("task"), str)
    task = running["task"] if held else run.get("task")
    return {**state, "state": "abandoned", "task": task,
            "operator": running.get("operator") if held else None,
            "round": round_number(run_path / ROUNDS_FILE, args.unit, task),
            "progress": disagreements(args, task)}, None


def disagreements(args: argparse.Namespace, in_hand: object) -> list[str]:
    """One line for each task before the one in hand whose last progress record
    is not `done`, in task order; nothing when the task in hand is not one of
    the tasks. The run record wins, so these lines only report."""
    if in_hand not in RESTART_ORDER:
        return []
    contract = args.unit.split("/")[0]
    problems: list[str] = []
    records = read_progress(Path(args.root), problems).get(contract, [])
    lines = []
    for task in RESTART_ORDER[:RESTART_ORDER.index(in_hand)]:
        states = [r.state for r in records
                  if r.item == f"{args.unit}/{task}" and r.state is not None]
        if states[-1:] != ["done"]:
            lines.append(f"Progress record disagrees: {task} reads "
                         f"{states[-1] if states else 'no record'}, "
                         f"but the run is at {in_hand}.")
    return lines


def place_draft(run_path: Path, kept: dict, scratch: Path) -> None:
    """Copy the kept draft file to `draft/{test_file}` under the scratch folder;
    nothing when no draft file is kept."""
    draft, name = kept.get("draft"), kept.get("draft-file")
    test_file = draft.get("test_file") if isinstance(draft, dict) else None
    if not isinstance(name, str) or not isinstance(test_file, str) or not test_file:
        return
    relative = PurePosixPath(test_file)
    source = run_path.joinpath(*PurePosixPath(name).parts)
    if relative.is_absolute() or ".." in relative.parts or not source.is_file():
        return
    target = scratch.joinpath("draft", *relative.parts)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def clear_channel(path: Path, task: object) -> None:
    """Remove the failed reasons of the task's channel from the rounds file,
    keeping its unit and the other channel's reasons; nothing is written when
    the file holds no reasons for the channel."""
    held, rounds = read_rounds(path)
    channel = CHANNELS.get(task, task)
    if held is None or channel not in rounds:
        return
    del rounds[channel]
    write_whole(path, {"unit": held, "rounds": rounds})


def restart(args: argparse.Namespace) -> int:
    """Print the unit's state as one JSON line: 0 when it reads, 1 when a record
    does not parse or the run stopped on another branch. With `--go`, a stopped
    or abandoned run also loses its stop record and, when it names this unit,
    its task file, and the kept draft is written under the scratch folder;
    with `--fresh` as well, the failed rounds of the stopped task's channel
    are cleared."""
    folder = git_folder(args.root)
    if folder is None:
        return refuse(f"Execution did not restart: no git repository at {args.root}.")
    state, line = run_state(args, folder)
    if line is not None:
        return refuse(line)
    if args.go and state["state"] != "none":
        run_path = run_folder(folder, args.unit)
        place_draft(run_path, state["kept"], Path(args.scratch))
        if args.fresh:
            clear_channel(run_path / ROUNDS_FILE, state["task"])
        running = read_object(folder / TASK_FILE)
        if running is not None and running.get("unit") == args.unit:
            remove(folder / TASK_FILE)
        remove(run_path / STOP_FILE)
    print(json.dumps(state, separators=(",", ":")))
    return 0


COMMANDS = {"start": start, "end": end, "fail": fail, "stop": stop,
            "keep": keep, "restart": restart}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "end":
        needed = ("unit",) if args.run else ("unit", "task")
        missing = [f"--{name}" for name in needed if not getattr(args, name)]
        if missing:
            parser.error(f"the following arguments are required: {', '.join(missing)}")
    if args.command == "keep":
        try:
            args.parsed = keep_value(args)
        except ValueError as error:
            parser.error(str(error))
    if args.command == "restart" and args.go and not args.scratch:
        parser.error("--go requires --scratch")
    if args.command == "restart" and args.fresh and not args.go:
        parser.error("--fresh requires --go")
    return COMMANDS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
