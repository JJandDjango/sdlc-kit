"""The herdr hook for the SDLC kit's tree pane.

When `python -m taskcontract tree --follow` arrives at an approval, the kit
runs its `tree: notify:` command (set in a repo's `.sdlc/config.yaml`; {kit}
is the kit's folder: a clone, or the plugin's install):

    tree:
      notify: python {kit}/herdr/herdr_seat.py

This hook flags the tree pane in herdr's sidebar as agent `sdlc`, state
`blocked`, shows a toast, and releases the flag once the pane's first line
stops reading this seat's waiting line. The contract is README.md's
Interface section.
"""

import os
import subprocess
import sys
import time

SOURCE = "sdlc:tree"
AGENT = "sdlc"
WAITING = "waiting on a seat"


def seat_of(node):
    """Return the seat `<approval> for <unit>` for a full approval task id."""
    unit, _, approval = node.rpartition("/")
    return f"{approval} for {unit}"


def first_line(output):
    """Return the first non-blank line of output, stripped, or ''."""
    for line in output.splitlines():
        if line.strip():
            return line.strip()
    return ""


def is_this_seat(line, waiting_line):
    """Whether the pane line is this seat's waiting line, whole or cut."""
    if line == waiting_line:
        return True
    if line.endswith("..."):
        head = line[:-3]
        return head.startswith(WAITING + ": ") and waiting_line.startswith(head)
    return False


class Seq:
    """Millisecond --seq values, each greater than the one before."""

    def __init__(self, clock):
        self.clock = clock
        self.last = None

    def next(self):
        """Return the next --seq value as a string."""
        value = int(self.clock() * 1000)
        if self.last is not None and value <= self.last:
            value = self.last + 1
        self.last = value
        return str(value)


def main(environ, run, sleep, clock):
    """Flag the seat, toast it, watch the pane, release; return the exit code."""
    pane = environ.get("HERDR_PANE_ID") or ""
    node = environ.get("SDLC_NODE") or ""
    if environ.get("HERDR_ENV") != "1" or not pane or not node:
        return 0
    herdr = environ.get("HERDR_BIN_PATH") or "herdr"
    seat = seat_of(node)
    waiting_line = f"{WAITING}: {seat}"
    seq = Seq(clock)

    code, _ = run([herdr, "pane", "report-agent", pane, "--source", SOURCE,
                   "--agent", AGENT, "--state", "blocked", "--message", seat,
                   "--seq", seq.next()])
    if code != 0:
        return code

    def release():
        code, _ = run([herdr, "pane", "release-agent", pane, "--source", SOURCE,
                       "--agent", AGENT, "--seq", seq.next()])
        return code

    try:
        result = 0
        code, _ = run([herdr, "notification", "show", WAITING, "--body", seat,
                       "--sound", "request"])
        if code != 0:
            result = 1

        no_seat = 0
        while no_seat < 2:
            sleep(1)
            code, output = run([herdr, "pane", "read", pane, "--source", "visible"])
            line = first_line(output) if code == 0 else ""
            if code == 0 and is_this_seat(line, waiting_line):
                no_seat = 0
            elif code == 0 and line.startswith(WAITING + ":"):
                return result
            else:
                no_seat += 1

        if release() != 0:
            result = 1
        return result
    except KeyboardInterrupt:
        try:
            release()
        except KeyboardInterrupt:
            pass
        return 0


def run_command(argv):
    """Run one command; return (exit code, stdout), 127 when it cannot start."""
    try:
        done = subprocess.run(argv, stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, encoding="utf-8",
                              errors="replace")
    except OSError:
        return 127, ""
    return done.returncode, done.stdout or ""


if __name__ == "__main__":
    sys.exit(main(os.environ, run_command, time.sleep, time.time))
