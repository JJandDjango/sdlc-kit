"""Run Two-Key's receipts in the session, with no agent, and print the minimum.

usage: receipts.py --repo DIR --receipts FILE --out DIR [--timeout SECONDS]

FILE is a JSON list of argv lists, e.g. the whole suite on workers:
[["python", "-P", "-m", "pytest", "tests", "-q", "-n", "auto"]].
No shell runs, so a pipe, a redirect or a chain cannot enter a receipt, and a
glob is not expanded: name the folder. The commands run one at a time from DIR
(the repository root), each hidden, with PYTHONUTF8 set and stdin closed.
Before the first one the script reads the repository's state from git.

stdout is one compact JSON object, also written to OUT/result.json:
  ok, out, head, branch, working_tree_clean_of_tracked_changes,
  commands: [{command, exit_code, key_output, log, seconds}], notes?
That is the shape two-key-unit-verifier.js reads as its receipts result.
exit_code is the process's own. 254 means the command never started; 124 means
it passed --timeout and was killed with its children. key_output is, for a
pytest command, the summary line and each failing id with its first assertion
line (the first 10, then a count); for any other command, its last non-empty
output line. Each command's full output, stderr merged, is OUT/logs/<n>.log.

OUT/alive holds the pid and start time, written before the first command.
OUT/progress.json is rewritten before and after each command so the session can
follow a long run with a Monitor: total, done, running, finished, commands.

exit: 0 every command exited 0; 1 a command did not; 2 usage (a bad receipts
file, or a folder that is no git repository); 254 git never started.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SPAWN_FAILED = 254
TIMED_OUT = 124
LINE_CAP = 200
IDS_CAP = 10
GIT_TIMEOUT = 60
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
SUMMARY_HEADER = "short test summary info"


class SpawnFailed(Exception):
    """git could not be started at all."""


class Usage(Exception):
    """The command line or a file it names is wrong."""


def clip(line: str) -> str:
    return line if len(line) <= LINE_CAP else line[:LINE_CAP - 3] + "..."


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_receipts(path: str) -> list[list[str]]:
    """The receipts file's argv lists; anything else is a usage error."""
    try:
        items = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        raise Usage(f"cannot read the receipts file {path}: {err}") from err
    if not isinstance(items, list) or not items:
        raise Usage(f"{path} must be a non-empty JSON list of argv lists")
    for n, item in enumerate(items, 1):
        if isinstance(item, str):
            raise Usage(f"entry {n} is a string: write it as an argv list "
                        f"(['python', '-m', 'pytest']), since no shell runs")
        if not (isinstance(item, list) and item
                and all(isinstance(word, str) and word for word in item)):
            raise Usage(f"entry {n} must be a non-empty argv list of non-empty strings")
    return items


def git(repo: Path, *args: str) -> tuple[int, str]:
    try:
        done = subprocess.run(["git", *args], cwd=repo, capture_output=True,
                              timeout=GIT_TIMEOUT, creationflags=NO_WINDOW)
    except OSError as err:
        raise SpawnFailed(f"git did not start: {err}") from err
    return done.returncode, done.stdout.decode("utf-8", "replace").strip()


def git_state(repo: Path) -> dict:
    """HEAD, branch and whether a tracked file is modified, read before any command."""
    if not repo.is_dir():
        raise Usage(f"{repo} is not a folder")
    code, head = git(repo, "rev-parse", "--short", "HEAD")
    if code != 0:
        raise Usage(f"{repo} is not a git repository with a commit")
    _, branch = git(repo, "branch", "--show-current")
    _, changed = git(repo, "status", "--porcelain", "--untracked-files=no")
    return {"head": head, "branch": branch or "(detached)",
            "working_tree_clean_of_tracked_changes": not changed}


def write_atomic(path: Path, text: str) -> None:
    """Replace `path` whole; a reader never sees half a file. Never raises."""
    tmp = path.with_name(path.name + ".tmp")
    for _ in range(3):
        try:
            tmp.write_text(text, encoding="utf-8")
            os.replace(tmp, path)
            return
        except OSError:
            time.sleep(0.05)


def kill_tree(proc: subprocess.Popen) -> None:
    """End a command and every process it started."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                       capture_output=True, timeout=30, creationflags=NO_WINDOW)
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def is_pytest(argv: list[str]) -> bool:
    return "pytest" in argv or Path(argv[0]).stem in ("pytest", "py.test")


def pytest_key(lines: list[str]) -> str:
    """The summary line, then each failing id with its first line, as pytest prints them."""
    summary = lines[-1].strip("= ").strip()
    failing: list[str] = []
    seen = False
    for line in lines:
        if SUMMARY_HEADER in line and line.startswith("="):
            seen = True
        elif seen and line.startswith(("FAILED ", "ERROR ")):
            failing.append(clip(line))
    out = [summary, *failing[:IDS_CAP]]
    if len(failing) > IDS_CAP:
        out.append(f"+{len(failing) - IDS_CAP} more in the log")
    return "\n".join(out)


def key_output(argv: list[str], text: str, code: int, timed_out: bool, timeout: int) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if timed_out:
        tail = f"; last line: {clip(lines[-1])}" if lines else ""
        return clip(f"timeout after {timeout}s{tail}")
    if not lines:
        return f"exit {code}, no output"
    return pytest_key(lines) if is_pytest(argv) else clip(lines[-1])


def run_command(argv: list[str], n: int, repo: Path, logs: Path, timeout: int) -> dict:
    """Run one receipt; return its record. A command that fails to start reads 254."""
    log = logs / f"{n}.log"
    record = {"command": shlex.join(argv), "exit_code": SPAWN_FAILED, "key_output": "",
              "log": f"logs/{n}.log", "seconds": 0.0}
    exe = shutil.which(argv[0])
    if exe is None:
        log.write_text(f"not found on PATH: {argv[0]}\n", encoding="utf-8")
        return {**record, "key_output": clip(f"not found on PATH: {argv[0]}")}
    env = dict(os.environ, PYTHONUTF8="1")
    extra = {"creationflags": NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
    began, timed_out = time.monotonic(), False
    try:
        with log.open("wb") as sink:
            proc = subprocess.Popen([exe, *argv[1:]], cwd=repo, env=env,
                                    stdin=subprocess.DEVNULL, stdout=sink,
                                    stderr=subprocess.STDOUT, **extra)
            try:
                code = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                kill_tree(proc)
                code, timed_out = TIMED_OUT, True
    except OSError as err:
        message = clip(f"did not start: {err}")
        log.write_text(message + "\n", encoding="utf-8")
        return {**record, "key_output": message}
    text = log.read_bytes().decode("utf-8", "replace")
    return {**record, "exit_code": code, "seconds": round(time.monotonic() - began, 1),
            "key_output": key_output(argv, text, code, timed_out, timeout)}


def run_all(args: argparse.Namespace) -> tuple[dict, bool]:
    if args.timeout < 1:
        raise Usage("--timeout must be at least 1 second")
    commands = load_receipts(args.receipts)
    repo = Path(args.repo).resolve()
    state = git_state(repo)
    out = Path(args.out).resolve()
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    write_atomic(out / "alive", json.dumps({"pid": os.getpid(), "started": now(),
                                            "repo": str(repo)}))
    progress = {"total": len(commands), "done": 0, "running": None, "finished": False,
                "commands": []}
    records = []
    for n, argv in enumerate(commands, 1):
        progress["running"] = {"n": n, "command": shlex.join(argv), "since": now()}
        write_atomic(out / "progress.json", json.dumps(progress, separators=(",", ":")))
        record = run_command(argv, n, repo, logs, args.timeout)
        records.append(record)
        progress["commands"].append({"n": n, "exit_code": record["exit_code"],
                                     "seconds": record["seconds"]})
        progress.update(done=n, running=None)
        write_atomic(out / "progress.json", json.dumps(progress, separators=(",", ":")))
    progress["finished"] = True
    write_atomic(out / "progress.json", json.dumps(progress, separators=(",", ":")))
    holds = all(r["exit_code"] == 0 for r in records)
    result = {"ok": holds, "out": str(out), **state, "commands": records}
    if not state["working_tree_clean_of_tracked_changes"]:
        result["notes"] = "tracked files were modified before the first command"
    return result, holds


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="receipts.py", description="Run Two-Key's receipts.")
    parser.add_argument("--repo", required=True, help="the repository root; commands run here")
    parser.add_argument("--receipts", required=True, help="JSON list of argv lists")
    parser.add_argument("--out", required=True, help="folder for alive, progress.json, logs/")
    parser.add_argument("--timeout", type=int, default=1800,
                        help="seconds one command may take (default 1800)")
    args = parser.parse_args(argv)
    try:
        result, holds = run_all(args)
    except Usage as err:
        print(f"receipts.py: {err}", file=sys.stderr)
        return 2
    except SpawnFailed as err:
        print(f"receipts.py: {err}", file=sys.stderr)
        return SPAWN_FAILED
    text = json.dumps(result, separators=(",", ":"), ensure_ascii=False)
    write_atomic(Path(result["out"]) / "result.json", text)
    print(text)
    return 0 if holds else 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
