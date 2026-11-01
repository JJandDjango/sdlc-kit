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

`start` checks, in this order, that the repository declares a test command,
that the root is a git repository and that no task is running, then runs
`taskcontract progress start` for the task. Each refusal prints one line on
stderr, writes nothing and exits 1; `progress start`'s own line prints as it
gave it. On acceptance `start` writes `sdlc-task.json` into the git folder,
the running task, its operator and its round, and prints `Task {task}:
{Operator}, round {n}`: n is one more than the failed rounds of the task's
channel (write-tests or green) in the unit's rounds file, which holds the
failed reasons a task; the task's own, when higher.

A unit's records stand in its run folder, `sdlc-run/{contract}/{unit}/` in the
git folder, made on the first write: `rounds.json` and `stop.json`, each
written whole, so a killed session leaves the old file or the new one. A file
that does not parse reads as absent. `stop.json` holds the latest stop only:
a question, an error or a refusal with its text, or a third failed round with
each round's reason. Nothing removes another unit's folder.

`end` runs `taskcontract progress done` for the task and removes the task
file; when `progress done` refuses, its line prints as it gave it and the
task file stays. `end --run` removes the task file and the unit's run folder.
`fail` records a failed round and removes the task file; the third failed
round of a task also writes the stop record and exits 1 with the failures.
`stop` removes the task file, writes the stop record and exits 1; a question
or an error prints the operator's words, a refusal prints nothing. Both keep
the rounds file. Each command exits 2 on a usage error, a `--unit` that is
not two names joined by one `/` included.

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
from pathlib import Path

# The plugin root goes first, so the taskcontract beside this script wins.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import yaml  # noqa: E402

from taskcontract.declaration import read_test  # noqa: E402
from taskcontract.progress import record_state  # noqa: E402
from taskcontract.tree import TASKS_PATH  # noqa: E402

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
TASK_FILE = "sdlc-task.json"
RUN_DIR = "sdlc-run"
ROUNDS_FILE = "rounds.json"
STOP_FILE = "stop.json"
MAX_ROUNDS = 3
STOP_KINDS = ["question", "error", "refusal"]
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
    name, so neither is empty, `.` or `..`, and neither holds a separator."""
    halves = text.split("/")
    if len(halves) != 2 or any(not half or half in (".", "..") or "\\" in half
                               for half in halves):
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
    number = round_number(run_folder(folder, args.unit) / ROUNDS_FILE, args.unit, task)
    path.write_text(json.dumps({"task": task, "operator": args.operator, "round": number}),
                    encoding="utf-8")
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


COMMANDS = {"start": start, "end": end, "fail": fail, "stop": stop}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "end":
        needed = ("unit",) if args.run else ("unit", "task")
        missing = [f"--{name}" for name in needed if not getattr(args, name)]
        if missing:
            parser.error(f"the following arguments are required: {', '.join(missing)}")
    return COMMANDS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
