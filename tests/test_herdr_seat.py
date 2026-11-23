"""Spec tests for herdr_seat.py, pinned to herdr/README.md, section Interface.

Each test calls main(environ, run, sleep, clock) with fakes, except the two
script tests, which run the module file under sys.executable.
"""
import os
import subprocess
import sys

import pytest

import herdr_seat

NODE = "tree-view/t6-query-face/approve-tests"
SEAT = "approve-tests for tree-view/t6-query-face"
WAITING = "waiting on a seat: " + SEAT
PANE = "7"
T0 = 1000.0
SEQ0 = "1000000"


def env(**over):
    """A herdr pane's environment with SDLC_NODE; a None value removes the key."""
    e = {"HERDR_ENV": "1", "HERDR_PANE_ID": PANE, "SDLC_NODE": NODE}
    for key, value in over.items():
        if value is None:
            e.pop(key, None)
        else:
            e[key] = value
    return e


def key_of(argv):
    """The herdr subcommand of an argv: 'pane report-agent', 'notification show', ..."""
    return " ".join(argv[1:3])


class Hook:
    """Fakes for main(environ, run, sleep, clock), sharing one event log.

    run answers from a script of (exit_code, stdout) replies keyed by the herdr
    subcommand; an exhausted script answers (0, ""), which a read takes as no
    seat. sleep records its argument, can raise KeyboardInterrupt at a chosen
    call, and moves the clock by its argument unless the clock stands still.
    """

    def __init__(self, reads=(), report=(0, ""), toast=(0, ""), release=(0, ""),
                 interrupt_at_sleep=None, interrupt_on=None, clock_moves=True):
        self.replies = {
            "pane report-agent": [report],
            "notification show": [toast],
            "pane read": [(0, r) if isinstance(r, str) else r for r in reads],
            "pane release-agent": [release],
        }
        self.interrupt_at_sleep = interrupt_at_sleep
        self.interrupt_on = interrupt_on
        self.clock_moves = clock_moves
        self.events = []
        self.sleeps = 0
        self.now = T0

    def run(self, argv):
        argv = list(argv)
        self.events.append(("run", argv))
        if key_of(argv) == self.interrupt_on:
            raise KeyboardInterrupt
        queue = self.replies.get(key_of(argv), [])
        return queue.pop(0) if queue else (0, "")

    def sleep(self, seconds):
        self.events.append(("sleep", seconds))
        self.sleeps += 1
        if self.sleeps == self.interrupt_at_sleep:
            raise KeyboardInterrupt
        if self.sleeps > 100:
            raise AssertionError("the watch never ended")
        if self.clock_moves:
            self.now += seconds

    def clock(self):
        return self.now

    def main(self, environ=None):
        return herdr_seat.main(env() if environ is None else environ,
                               self.run, self.sleep, self.clock)

    @property
    def argvs(self):
        return [e[1] for e in self.events if e[0] == "run"]

    def calls(self, key):
        return [a for a in self.argvs if key_of(a) == key]


def seq_of(argv):
    return int(argv[argv.index("--seq") + 1])


# Guards: the hook calls nothing and exits 0.

@pytest.mark.parametrize("value", [None, "", "0", "true"])
def test_outside_herdr_calls_nothing(value):
    hook = Hook()
    assert hook.main(env(HERDR_ENV=value)) == 0
    assert hook.events == []


@pytest.mark.parametrize("value", [None, ""])
def test_missing_or_empty_pane_id_calls_nothing(value):
    hook = Hook()
    assert hook.main(env(HERDR_PANE_ID=value)) == 0
    assert hook.events == []


@pytest.mark.parametrize("value", [None, ""])
def test_missing_or_empty_sdlc_node_calls_nothing(value):
    hook = Hook()
    assert hook.main(env(SDLC_NODE=value)) == 0
    assert hook.events == []


# The seat.

def test_seat_splits_node_at_last_slash():
    hook = Hook()
    hook.main(env(SDLC_NODE="a/b/c/approve-code"))
    report = hook.calls("pane report-agent")[0]
    toast = hook.calls("notification show")[0]
    assert report[report.index("--message") + 1] == "approve-code for a/b/c"
    assert toast[toast.index("--body") + 1] == "approve-code for a/b/c"


# Call 1: the report.

def test_report_argv_exact():
    hook = Hook()
    hook.main()
    assert hook.argvs[0] == [
        "herdr", "pane", "report-agent", PANE, "--source", "sdlc:tree",
        "--agent", "sdlc", "--state", "blocked", "--message", SEAT,
        "--seq", SEQ0,
    ]


def test_report_failure_exits_with_its_code_before_any_other_call():
    hook = Hook(report=(3, ""))
    assert hook.main() == 3
    assert [key_of(a) for a in hook.argvs] == ["pane report-agent"]
    assert hook.sleeps == 0


# Call 2: the toast.

def test_toast_argv_exact():
    hook = Hook()
    hook.main()
    assert hook.argvs[1] == [
        "herdr", "notification", "show", "waiting on a seat",
        "--body", SEAT, "--sound", "request",
    ]


def test_toast_failure_exits_1_but_watch_still_runs():
    hook = Hook(toast=(2, ""), reads=["", ""])
    assert hook.main() == 1
    assert len(hook.calls("pane read")) == 2
    assert len(hook.calls("pane release-agent")) == 1


# Call 3: the watch.

def test_read_argv_exact():
    hook = Hook(reads=["", ""])
    hook.main()
    assert hook.calls("pane read")[0] == [
        "herdr", "pane", "read", PANE, "--source", "visible",
    ]


def test_sleep_1_before_each_read():
    hook = Hook(reads=["", ""])
    hook.main()
    shape = [key_of(e[1]) if e[0] == "run" else ("sleep", e[1]) for e in hook.events]
    assert shape == [
        "pane report-agent", "notification show",
        ("sleep", 1), "pane read", ("sleep", 1), "pane read",
        "pane release-agent",
    ]


def test_first_nonblank_line_stripped_is_the_pane_line():
    hook = Hook(reads=["\n   \n\t  " + WAITING + "  \nidle\n", "", ""])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 3


def test_only_the_first_nonblank_line_counts():
    hook = Hook(reads=["idle\n" + WAITING, "idle\n" + WAITING])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 2
    assert len(hook.calls("pane release-agent")) == 1


def test_this_seat_line_equal_keeps_watching():
    hook = Hook(reads=[WAITING, "", ""])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 3
    assert len(hook.calls("pane release-agent")) == 1


def test_this_seat_line_cut_with_dots_keeps_watching():
    hook = Hook(reads=[WAITING[:30] + "...", "", ""])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 3
    assert len(hook.calls("pane release-agent")) == 1


def test_cut_line_without_seat_prefix_is_no_seat():
    hook = Hook(reads=["waiting on...", "waiting on..."])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 2
    assert len(hook.calls("pane release-agent")) == 1


def test_another_seat_line_exits_without_release():
    hook = Hook(reads=["waiting on a seat: approve-code for tree-view/t9-other"])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 1
    assert hook.calls("pane release-agent") == []


def test_cut_line_of_another_seat_exits_without_release():
    hook = Hook(reads=["waiting on a seat: approve-code for tr..."])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 1
    assert hook.calls("pane release-agent") == []


def test_longer_seat_line_is_another_seat():
    hook = Hook(reads=[WAITING + "-b"])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 1
    assert hook.calls("pane release-agent") == []


def test_one_no_seat_alone_does_not_release():
    hook = Hook(reads=["idle", "waiting on a seat: approve-code for tree-view/t9-other"])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 2
    assert hook.calls("pane release-agent") == []


def test_seat_line_resets_no_seat_count():
    hook = Hook(reads=["idle", WAITING, "idle", "idle"])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 4
    assert len(hook.calls("pane release-agent")) == 1


def test_failed_read_counts_as_no_seat():
    hook = Hook(reads=[(1, WAITING), (1, WAITING)])
    assert hook.main() == 0
    assert len(hook.calls("pane read")) == 2
    assert len(hook.calls("pane release-agent")) == 1


# Call 4: the release.

def test_release_argv_exact():
    hook = Hook(reads=["", ""])
    hook.main()
    assert hook.argvs[-1] == [
        "herdr", "pane", "release-agent", PANE, "--source", "sdlc:tree",
        "--agent", "sdlc", "--seq", "1002000",
    ]


def test_failed_release_exits_1():
    hook = Hook(reads=["", ""], release=(5, ""))
    assert hook.main() == 1


# --seq.

def test_seq_strictly_increases_when_clock_stands_still():
    hook = Hook(reads=["", ""], clock_moves=False)
    hook.main()
    report = hook.calls("pane report-agent")[0]
    release = hook.calls("pane release-agent")[0]
    assert seq_of(report) == int(SEQ0)
    assert seq_of(release) > seq_of(report)


# The binary.

def test_bin_path_used_as_argv0_when_set():
    hook = Hook(reads=["", ""])
    hook.main(env(HERDR_BIN_PATH="C:/tools/herdr.exe"))
    assert len(hook.argvs) == 5
    assert {a[0] for a in hook.argvs} == {"C:/tools/herdr.exe"}


@pytest.mark.parametrize("value", [None, ""])
def test_bin_path_unset_or_empty_uses_herdr(value):
    hook = Hook(reads=["", ""])
    hook.main(env(HERDR_BIN_PATH=value))
    assert len(hook.argvs) == 5
    assert {a[0] for a in hook.argvs} == {"herdr"}


# Ctrl-C.

def test_ctrl_c_during_sleep_releases_and_exits_0():
    hook = Hook(reads=[WAITING], interrupt_at_sleep=2)
    assert hook.main() == 0
    assert hook.calls("pane release-agent") == [[
        "herdr", "pane", "release-agent", PANE, "--source", "sdlc:tree",
        "--agent", "sdlc", "--seq", "1001000",
    ]]


def test_ctrl_c_during_read_releases_and_exits_0():
    hook = Hook(interrupt_on="pane read")
    assert hook.main() == 0
    assert len(hook.calls("pane release-agent")) == 1
    assert key_of(hook.argvs[-1]) == "pane release-agent"


def test_ctrl_c_during_toast_releases_and_exits_0():
    hook = Hook(interrupt_on="notification show")
    assert hook.main() == 0
    assert [key_of(a) for a in hook.argvs] == [
        "pane report-agent", "notification show", "pane release-agent",
    ]


# Run as a script.

def _script_env(**over):
    e = dict(os.environ)
    e.pop("HERDR_ENV", None)
    e.update(over)
    return e


def test_script_outside_herdr_exits_0():
    proc = subprocess.run([sys.executable, herdr_seat.__file__],
                          env=_script_env(), capture_output=True, timeout=60)
    assert proc.returncode == 0


def test_script_unstartable_binary_exits_127(tmp_path):
    missing = str(tmp_path / "no-such-herdr.exe")
    proc = subprocess.run(
        [sys.executable, herdr_seat.__file__],
        env=_script_env(HERDR_ENV="1", HERDR_PANE_ID=PANE, SDLC_NODE=NODE,
                        HERDR_BIN_PATH=missing),
        capture_output=True, timeout=60,
    )
    assert proc.returncode == 127
