"""The session loop's files and issues, for the session and the launcher.

usage: loop.py on | off | due
       loop.py stop --question TEXT
       loop.py reply
       loop.py wrap --plan-step N --task T --next TEXT [--self]

The files live under {git folder}/sdlc-loop/, untracked, as UTF-8 JSON, and the
folder is made only when a file is first written. Times are local, no zone.
  loop.json      {"on": TIME}
  waiting.json   {"issue": N, "at": TIME, "due": TIME, "cron": "M H D Mo *"}
  sentinel.json  {"kind", "position", "next", "head", "at"}; kind is
                 continue, self-wrap or pick

Every git and gh call goes through run(), the one seam; the commands write
nothing outside the git folder and run no git command that writes.

on writes loop.json. off removes it. due exits 0 when waiting.json exists, else
3. stop files a needs-ruling issue holding TEXT, then writes waiting.json and
prints the issue, the due time and the cron that names it. reply closes the
waiting issue and removes waiting.json. wrap checks that its commit is on the
remote, files one "Pick the next deliverable" issue when Next is "(none)", and
writes sentinel.json last.

exit: 0 done; 1 a refusal or a failed gh call, with a line on stderr; 3 only
`due`, with no stop waiting; 2 usage (argparse's).
"""

from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
LABEL = "needs-ruling"
PICK_TITLE = "Pick the next deliverable"
NONE_NEXT = "(none)"
TITLE_CAP = 70
TIMER_MINUTES = 55
NOT_DUE = 3


def run(argv: list[str]) -> subprocess.CompletedProcess:
    """Run argv with no shell; a non-zero exit is returned, not raised."""
    extra = {"creationflags": NO_WINDOW} if NO_WINDOW else {}
    return subprocess.run(argv, capture_output=True, encoding="utf-8",
                          errors="replace", **extra)


def now() -> datetime.datetime:
    return datetime.datetime.now()


def timer_due(stop: datetime.datetime) -> datetime.datetime:
    """The stop plus 55 minutes, cut to the minute, never at :00 or :30.

    A one-shot cron landing on :00 or :30 may fire up to 90 seconds early.
    """
    due = (stop + datetime.timedelta(minutes=TIMER_MINUTES)).replace(
        second=0, microsecond=0)
    if due.minute in (0, 30):
        due += datetime.timedelta(minutes=1)
    return due


def stamp(moment: datetime.datetime) -> str:
    return moment.isoformat(timespec="seconds")


def refuse(line: str) -> int:
    print(f"session-loop: {line}", file=sys.stderr)
    return 1


def state_dir() -> Path | None:
    done = run(["git", "rev-parse", "--absolute-git-dir"])
    folder = done.stdout.strip()
    if done.returncode != 0 or not folder:
        return None
    return Path(folder) / "sdlc-loop"


def write(folder: Path, name: str, record: dict) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(json.dumps(record, ensure_ascii=False),
                               encoding="utf-8")


def remove(folder: Path, name: str) -> None:
    (folder / name).unlink(missing_ok=True)


def read(folder: Path, name: str) -> dict:
    return json.loads((folder / name).read_text(encoding="utf-8"))


def issue_number(url: str) -> int | None:
    last = url.strip().rstrip("/").rsplit("/", 1)[-1]
    return int(last) if last.isdigit() else None


def gh_json(argv: list[str]) -> list | None:
    done = run(argv)
    if done.returncode != 0:
        return None
    try:
        found = json.loads(done.stdout)
    except ValueError:
        return None
    return found if isinstance(found, list) else None


def file_issue(title: str, body: str) -> int | None:
    done = run(["gh", "issue", "create", "--title", title, "--label", LABEL,
                "--body", body])
    if done.returncode != 0:
        return None
    return issue_number(done.stdout)


def cmd_on(folder: Path, args: argparse.Namespace) -> int:
    write(folder, "loop.json", {"on": stamp(now())})
    print("session loop on; a launcher may now restart this repo's sessions")
    return 0


def cmd_off(folder: Path, args: argparse.Namespace) -> int:
    remove(folder, "loop.json")
    print("session loop off")
    return 0


def cmd_due(folder: Path, args: argparse.Namespace) -> int:
    return 0 if (folder / "waiting.json").exists() else NOT_DUE


def cmd_stop(folder: Path, args: argparse.Namespace) -> int:
    labels = gh_json(["gh", "label", "list", "--search", LABEL, "--json",
                      "name"])
    if labels is None or not any(
            isinstance(one, dict) and one.get("name") == LABEL
            for one in labels):
        return refuse(f"the {LABEL} label is missing; "
                      f"run: gh label create {LABEL}")
    number = file_issue(args.question.split("\n")[0][:TITLE_CAP], args.question)
    if number is None:
        return refuse(f"could not file the {LABEL} issue")
    at = now()
    due = timer_due(at)
    cron = f"{due.minute} {due.hour} {due.day} {due.month} *"
    write(folder, "waiting.json",
          {"issue": number, "at": stamp(at), "due": stamp(due), "cron": cron})
    print(json.dumps({"issue": number, "due": stamp(due), "cron": cron}))
    return 0


def cmd_reply(folder: Path, args: argparse.Namespace) -> int:
    if not (folder / "waiting.json").exists():
        print("no stop waiting")
        return 0
    number = read(folder, "waiting.json")["issue"]
    done = run(["gh", "issue", "close", str(number), "--comment",
                "answered in the session"])
    if done.returncode != 0:
        return refuse(f"could not close issue #{number}")
    remove(folder, "waiting.json")
    print(f"closed issue #{number}")
    return 0


def pick_issue_open() -> bool | None:
    issues = gh_json(["gh", "issue", "list", "--state", "open", "--label",
                      LABEL, "--json", "number,title"])
    if issues is None:
        return None
    return any(isinstance(one, dict) and one.get("title") == PICK_TITLE
               for one in issues)


def cmd_wrap(folder: Path, args: argparse.Namespace) -> int:
    branch = run(["git", "branch", "--show-current"]).stdout.strip()
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    on_remote = ""
    if branch:
        listed = run(["git", "ls-remote", "origin", f"refs/heads/{branch}"])
        tokens = listed.stdout.split()
        on_remote = tokens[0] if tokens else ""
    if not branch or not head or on_remote != head:
        return refuse("the wrap's commit is not on the remote; push first")
    kind = ("self-wrap" if args.self_wrap
            else "pick" if args.next == NONE_NEXT else "continue")
    if args.next == NONE_NEXT:
        is_open = pick_issue_open()
        if is_open is None:
            return refuse(f"could not file the {LABEL} issue")
        if not is_open and file_issue(
                PICK_TITLE, "The wrap found Next empty. Name the next "
                "deliverable.") is None:
            return refuse(f"could not file the {LABEL} issue")
    if kind in ("pick", "self-wrap"):
        remove(folder, "loop.json")
    if kind == "self-wrap":
        remove(folder, "waiting.json")
    write(folder, "sentinel.json",
          {"kind": kind,
           "position": f"plan step {args.plan_step}, task {args.task}",
           "next": args.next, "head": head, "at": stamp(now())})
    print(f"sentinel written: {kind}")
    return 0


def parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(prog="loop.py", description=__doc__.split("\n")[0])
    sub = top.add_subparsers(dest="command", required=True)
    for name in ("on", "off", "due", "reply"):
        sub.add_parser(name)
    stop = sub.add_parser("stop")
    stop.add_argument("--question", required=True)
    wrap = sub.add_parser("wrap")
    wrap.add_argument("--plan-step", required=True)
    wrap.add_argument("--task", required=True)
    wrap.add_argument("--next", required=True)
    wrap.add_argument("--self", dest="self_wrap", action="store_true")
    return top


COMMANDS = {"on": cmd_on, "off": cmd_off, "due": cmd_due, "stop": cmd_stop,
            "reply": cmd_reply, "wrap": cmd_wrap}


def main(argv: list[str]) -> int:
    try:
        args = parser().parse_args(argv)
    except SystemExit as stop:
        return stop.code if isinstance(stop.code, int) else 1
    folder = state_dir()
    if folder is None:
        return refuse("not inside a git repository")
    return COMMANDS[args.command](folder, args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
