"""The herdr launcher for the SDLC kit's session loop.

Run it in a second pane, once, with the pane that holds the session ({kit} is
the kit's folder: a clone, or the plugin's install):

    python {kit}/herdr/herdr_loop.py <pane>

While `/sdlc loop on` is in force, the kit writes a sentinel at each wrap. On
a `continue` sentinel this launcher waits until the pane reads idle or done,
then types `/clear` and `/resume-session` into it. On a `self-wrap` or `pick`
sentinel it stops and types nothing. A sentinel of any other kind is left in
place and ends at the hang check. The files are in `<git folder>/sdlc-loop/`.

The launcher also stops the loop, typing nothing, when two sessions in a row
end at the same position, when Claude has left the pane with no sentinel, or
when the session shows no change for 60 minutes. A stop files one
`needs-ruling` issue, shows a toast, removes `loop.json` and exits 1.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

POLL = 2
GAP = 3
HANG = 3600


def run_command(argv, cwd=None):
    """Run one command, in `cwd` when given; return (exit code, stdout).

    The exit code is 127 when the command cannot start.
    """
    try:
        done = subprocess.run(argv, stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, encoding="utf-8",
                              errors="replace", cwd=cwd)
    except OSError:
        return 127, ""
    return done.returncode, done.stdout or ""


def say(line):
    """Print one line to stdout."""
    print(line, flush=True)


def pane_info(run, herdr, pane):
    """Return the pane object from `herdr pane get`, or None."""
    code, output = run([herdr, "pane", "get", pane])
    if code != 0:
        return None
    try:
        info = json.loads(output)["result"]["pane"]
    except (ValueError, KeyError, TypeError):
        return None
    return info if isinstance(info, dict) else None


def read_json(path):
    """Return the object in the file, or None when absent or not yet whole."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


READY = ("idle", "done")


def wait_idle(run, sleep, herdr, pane):
    """Poll the pane until its agent status reads `idle` or `done`.

    Both are herdr's ready states: a turn that ends in a pane nobody has
    looked at reads `done`, not `idle`. `working`, `blocked` and `unknown`
    are not ready.
    """
    while True:
        info = pane_info(run, herdr, pane)
        if info is not None and info.get("agent_status") in READY:
            return
        sleep(POLL)


def restart(run, sleep, herdr, pane):
    """Type `/clear`, then `/resume-session`, each followed by Enter."""
    run([herdr, "pane", "send-text", pane, "/clear"])
    run([herdr, "pane", "send-keys", pane, "Enter"])
    sleep(GAP)
    run([herdr, "pane", "send-text", pane, "/resume-session"])
    run([herdr, "pane", "send-keys", pane, "Enter"])


def claude_gone(run, herdr, pane):
    """True when `herdr pane process-info` lists no `claude` in the foreground.

    A failed call, or output that is empty or not JSON, is not gone.
    """
    code, output = run([herdr, "pane", "process-info", "--pane", pane])
    if code != 0:
        return False
    try:
        info = json.loads(output)["result"]["process_info"]["foreground_processes"]
        return not any(isinstance(entry, dict)
                       and entry.get("name") in ("claude.exe", "claude")
                       for entry in info)
    except (ValueError, KeyError, TypeError):
        return False


def transcript_time(run, herdr, pane):
    """Return the mtime of the pane's session transcript, or None.

    The transcript is `~/.claude/projects/*/<id>.jsonl`, found by the id alone.
    The id and the home folder are read again at each call.
    """
    info = pane_info(run, herdr, pane)
    agent = info.get("agent_session") if info else None
    session = agent.get("value") if isinstance(agent, dict) else None
    if not isinstance(session, str) or not session or session != Path(session).name:
        return None
    times = []
    try:
        for project in (Path.home() / ".claude" / "projects").iterdir():
            try:
                times.append((project / f"{session}.jsonl").stat().st_mtime)
            except OSError:
                pass
    except OSError:
        pass
    return max(times) if times else None


def stop(run, herdr, pane, cwd, loop, message, position, sentinel):
    """Stop the loop: file one issue, show a toast, remove `loop.json`; return 1.

    Nothing is typed into the pane.
    """
    body = f"pane {pane}; last position {position}; last sentinel {sentinel}"
    run(["gh", "issue", "create", "--title", message, "--body", body,
         "--label", "needs-ruling"], cwd=cwd)
    run([herdr, "notification", "show", "session-loop stopped",
         "--body", message, "--sound", "request"])
    try:
        loop.unlink()
    except OSError:
        pass
    say(f"herdr-loop: {message}")
    return 1


def main(argv, run, sleep, clock):
    """Watch the pane's loop folder and restart the pane; return the exit code."""
    if len(argv) != 1:
        print("usage: herdr_loop.py <pane>", file=sys.stderr)
        return 2
    pane = argv[0]
    herdr = os.environ.get("HERDR_BIN_PATH") or "herdr"
    no_loop = f"herdr-loop: no session loop is on in pane {pane}; run /sdlc loop on there"

    info = pane_info(run, herdr, pane)
    if info is None or not isinstance(info.get("cwd"), str):
        print(f"herdr-loop: cannot read pane {pane}", file=sys.stderr)
        return 2
    cwd = info["cwd"]
    code, output = run(["git", "-C", cwd, "rev-parse", "--absolute-git-dir"])
    if code != 0 or not output.strip():
        say(no_loop)
        return 2
    folder = Path(output.strip()) / "sdlc-loop"
    loop = folder / "loop.json"
    sentinel = folder / "sentinel.json"
    seen = folder / "sentinel.seen.json"

    if not loop.exists():
        say(no_loop)
        return 2
    say(f"herdr-loop: watching pane {pane} ({cwd})")

    previous = None
    strikes = 0
    last = None
    filed = False
    began = clock()

    def halt(message):
        return stop(run, herdr, pane, cwd, loop, message,
                    "none" if last is None else last,
                    str(seen) if filed else "none")

    while True:
        if sentinel.exists():
            data = read_json(sentinel)
            kind = data.get("kind") if data else None
            if kind == "continue":
                position = str(data.get("position", ""))
                try:
                    os.replace(sentinel, seen)
                except OSError:
                    sleep(POLL)
                    continue
                strikes = strikes + 1 if position == previous else 0
                previous = last = position
                filed = True
                if strikes == 2:
                    return halt("session-loop stopped: two sessions in a row "
                                f"ended at {position}")
                wait_idle(run, sleep, herdr, pane)
                restart(run, sleep, herdr, pane)
                began = clock()
                say(f"herdr-loop: restarted pane {pane} at {position}")
                continue
            if kind in ("self-wrap", "pick"):
                say(f"herdr-loop: the loop stopped: {kind}")
                return 0
        if not loop.exists():
            say("herdr-loop: the session loop is off")
            return 0
        where = "none" if last is None else last
        if claude_gone(run, herdr, pane):
            return halt(f"session-loop stopped: the session in pane {pane} "
                        f"exited without a wrap; last position {where}")
        written = transcript_time(run, herdr, pane)
        if clock() - max(began, written or began) >= HANG:
            return halt(f"session-loop stopped: the session in pane {pane} "
                        f"showed no change for 60 minutes; last position {where}")
        sleep(POLL)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], run_command, time.sleep, time.time))
