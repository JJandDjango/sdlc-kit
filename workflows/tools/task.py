"""The execution team's task command: `start` opens one task step, `end`
closes it, `fail` counts a failed round and `stop` ends the run on a question.

    python workflows/tools/task.py start --unit {contract}/{unit} --task {task}
        --operator {operator} [--root DIR]
    python workflows/tools/task.py end --unit {contract}/{unit} --task {task}
        [--by SEAT] [--root DIR]
    python workflows/tools/task.py end --run [--root DIR]
    python workflows/tools/task.py fail --unit {contract}/{unit} --task {task}
        [--reason TEXT] [--root DIR]
    python workflows/tools/task.py stop --task {task} --operator {operator}
        --question TEXT [--root DIR]

`start` checks, in this order, that the repository declares a test command,
that the root is a git repository and that no task is running, then runs
`taskcontract progress start` for the task. Each refusal prints one line on
stderr, writes nothing and exits 1; `progress start`'s own line prints as it
gave it. On acceptance `start` writes `sdlc-task.json` into the git folder,
the running task, its operator and its round, and prints `Task {task}:
{Operator}, round {n}`: n is one more than the task's failed rounds in the
rounds file, `sdlc-rounds.json`, which holds one unit's failed reasons a task.

`end` runs `taskcontract progress done` for the task and removes the task
file; when `progress done` refuses, its line prints as it gave it and the
task file stays. `end --run` removes both files. `fail` records a failed
round and removes the task file; the third failed round of a task removes
both files and exits 1 with the failures. `stop` removes both files and
exits 1 with the operator's question. Both files stand in the git folder.
Each command exits 2 on a usage error.

The script imports the `taskcontract` that sits beside it, whichever package
of that name the environment holds.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

# The plugin root goes first, so the taskcontract beside this script wins.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import yaml  # noqa: E402

from taskcontract.declaration import read_test  # noqa: E402
from taskcontract.progress import record_state  # noqa: E402
from taskcontract.tree import TASKS_PATH  # noqa: E402

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
TASK_FILE = "sdlc-task.json"
ROUNDS_FILE = "sdlc-rounds.json"
MAX_ROUNDS = 3
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


def task_ids() -> list[str]:
    """The task ids, in order, from the one list the tree shows."""
    doc = yaml.safe_load(TASKS_PATH.read_text(encoding="utf-8"))
    return [task["id"] for task in doc["tasks"]]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task.py", description="open one task step of the execution team")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser(
        "start", help="record a task step doing and write the running task's file")
    start.add_argument("--unit", required=True, metavar="CONTRACT/UNIT",
                       help="the unit, as {contract}/{unit}")
    start.add_argument("--task", required=True, choices=task_ids(),
                       help="the task step to open")
    start.add_argument("--operator", required=True, choices=list(OPERATORS),
                       help="the operator that does the task")
    start.add_argument("--root", default=".", help=ROOT_HELP)
    end = sub.add_parser(
        "end", help="record a task step done and remove the task file")
    end.add_argument("--unit", metavar="CONTRACT/UNIT",
                     help="the unit, as {contract}/{unit}; required without --run")
    end.add_argument("--task", choices=task_ids(),
                     help="the task step to close; required without --run")
    end.add_argument("--by", metavar="SEAT",
                     help="the seat that holds an approval")
    end.add_argument("--run", action="store_true",
                     help="end the run: remove the task file and the rounds file")
    end.add_argument("--root", default=".", help=ROOT_HELP)
    fail = sub.add_parser(
        "fail", help="count one failed round of a task and remove the task file")
    fail.add_argument("--unit", required=True, metavar="CONTRACT/UNIT",
                      help="the unit, as {contract}/{unit}")
    fail.add_argument("--task", required=True, choices=task_ids(),
                      help="the task whose round failed")
    fail.add_argument("--reason", help="why the round failed")
    fail.add_argument("--root", default=".", help=ROOT_HELP)
    stop = sub.add_parser(
        "stop", help="end the run on an operator's question")
    stop.add_argument("--task", required=True, choices=task_ids(),
                      help="the task that asked")
    stop.add_argument("--operator", required=True, choices=list(OPERATORS),
                      help="the operator that asked")
    stop.add_argument("--question", required=True, help="the operator's question")
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
    rounds_path = folder / ROUNDS_FILE
    held, _ = read_rounds(rounds_path)
    if held is not None and held != args.unit:
        remove(rounds_path)  # another unit's counts end here
    number = len(failed_reasons(rounds_path, args.unit, task)) + 1
    path.write_text(json.dumps({"task": task, "operator": args.operator, "round": number}),
                    encoding="utf-8")
    print(f"Task {task}: {OPERATORS[args.operator]}, round {number}")
    return 0


def fail(args: argparse.Namespace) -> int:
    """Count one failed round: 0 on the first or second, 1 on the third."""
    folder = git_folder(args.root)
    if folder is None:
        return refuse(f"No git repository at {args.root}.")
    rounds_path = folder / ROUNDS_FILE
    held, rounds = read_rounds(rounds_path)
    if held != args.unit:
        rounds = {}
    rounds[args.task] = [*rounds.get(args.task, []), args.reason]
    remove(folder / TASK_FILE)
    if len(rounds[args.task]) < MAX_ROUNDS:
        rounds_path.write_text(json.dumps({"unit": args.unit, "rounds": rounds}),
                               encoding="utf-8")
        return 0
    remove(rounds_path)
    print(f"Task {args.task} failed {MAX_ROUNDS} rounds. The run stops here; the failures follow.")
    for number, reason in enumerate(rounds[args.task], 1):
        print(f"  Round {number}: {one_line(reason or '') or 'no reason given'}")
    return 1


def stop(args: argparse.Namespace) -> int:
    """End the run on an operator's question: always 1."""
    folder = git_folder(args.root)
    if folder is not None:
        remove(folder / TASK_FILE, folder / ROUNDS_FILE)
    print(f"Task {args.task} stopped on a question from {OPERATORS[args.operator]}: "
          f"{one_line(args.question)}")
    return 1


def end(args: argparse.Namespace) -> int:
    """Close the task: 0 when recorded done, 1 when `progress done` refuses."""
    folder = git_folder(args.root)
    if args.run:
        if folder is not None:
            remove(folder / TASK_FILE, folder / ROUNDS_FILE)
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
    if args.command == "end" and not args.run:
        missing = [f"--{name}" for name in ("unit", "task") if not getattr(args, name)]
        if missing:
            parser.error(f"the following arguments are required: {', '.join(missing)}")
    return COMMANDS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
