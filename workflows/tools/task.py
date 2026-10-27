"""The execution team's task command: one `start` opens one task step.

    python workflows/tools/task.py start --unit {contract}/{unit} --task {task}
        --operator {operator} [--root DIR]

`start` checks, in this order, that the repository declares a test command,
that the root is a git repository and that no task is running, then runs
`taskcontract progress start` for the task. Each refusal prints one line on
stderr, writes nothing and exits 1; `progress start`'s own line prints as it
gave it. On acceptance `start` writes `sdlc-task.json` into the git folder,
the running task, its operator and its round, and prints `Task {task}:
{Operator}, round 1`. It exits 2 on a usage error. The round is always 1
here: no command counts failed rounds yet.

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
    start.add_argument("--root", default=".",
                       help="repo root that holds specs/ and .sdlc/ (default: cwd)")
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
    path.write_text(json.dumps({"task": task, "operator": args.operator, "round": 1}),
                    encoding="utf-8")
    print(f"Task {task}: {OPERATORS[args.operator]}, round 1")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return start(args)


if __name__ == "__main__":
    sys.exit(main())
