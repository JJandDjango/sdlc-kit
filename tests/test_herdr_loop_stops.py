"""Spec tests for herdr_loop.py, unit l3 of the session-loop contract: the stops.

Two strikes (SC4.1, SC4.2), an exit and a 60-minute hang (SC4.3) stop the loop
with one `needs-ruling` issue, a toast and exit 1, and the launcher types nothing.

Each test calls main(argv, run, sleep, clock) with fakes. The fake `run` answers
herdr, git and gh calls in the shapes herdr 0.9.5 and gh print; `run(argv)` returns
(exit code, stdout), and the one `gh issue create` call also gets `cwd=` (the pane's
working directory). The fake `sleep` moves a fake clock and fires scheduled events,
so a watch that never stops fails on an assertion (the harness gives up after 2.5
fake hours and main's result reads None). The loop files are real files in a temp git
folder; the home folder holding `.claude/projects` is a temp folder named by HOME and
USERPROFILE; transcript mtimes are set with os.utime against the fake clock. No real
process starts and nothing is typed into a real pane.

l2's tests (tests/test_herdr_loop.py) pin the restart; these pin the stops.
"""
import json
import os
from collections import namedtuple

import pytest

PANE = "w9:p1"
CWD = r"E:\sdlc_development_kit"
OTHER_CWD = "C:/work/another repo"
T0 = 1000.0
POSITION = "plan step 4, task none"
POSITION_2 = "plan step 5, task t2-code"
POSITION_3 = "plan step 6, task none"
TYPING_SUBCOMMANDS = ("send-text", "send-keys", "run")
SESSION_A = "4e40fb9b-9c8d-4106-b4f4-bc32d7a71559"
SESSION_B = "0f8c1d2e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"
PROJECT = "E--sdlc-development-kit"
HUNG = 3600
SLACK = 10          # seconds past the exact moment within which a stop must land
GIVE_UP = 9000      # fake seconds after which the harness ends a watch that never stops

Call = namedtuple("Call", "time argv cwd")


class Runaway(Exception):
    """The fake clock passed GIVE_UP: the launcher never stopped."""


def load():
    """Import the launcher; a missing module fails the test, it does not error it."""
    try:
        import herdr_loop
    except ImportError:
        pytest.fail("herdr_loop.py does not exist in herdr/")
    return herdr_loop


def sentinel(kind="continue", position=POSITION, next_="Next 31: session-loop-sidebar"):
    return {"kind": kind, "position": position, "next": next_,
            "head": "0123456789abcdef0123456789abcdef01234567",
            "at": "2026-11-22T18:00:00"}


def watching(pane=PANE, cwd=CWD):
    return f"herdr-loop: watching pane {pane} ({cwd})"


def restarted(pane=PANE, position=POSITION):
    return f"herdr-loop: restarted pane {pane} at {position}"


def strike_message(position):
    return f"session-loop stopped: two sessions in a row ended at {position}"


def exit_message(pane, position):
    return (f"session-loop stopped: the session in pane {pane} exited without a wrap; "
            f"last position {position}")


def hung_message(pane, position):
    return (f"session-loop stopped: the session in pane {pane} showed no change for "
            f"60 minutes; last position {position}")


def stop_line(message):
    return "herdr-loop: " + message


def the_four(pane):
    return [["pane", "send-text", pane, "/clear"], ["pane", "send-keys", pane, "Enter"],
            ["pane", "send-text", pane, "/resume-session"], ["pane", "send-keys", pane, "Enter"]]


def process_info_json(pane, names):
    procs = [{"argv": [f"C:\\Users\\hyden\\.local\\bin\\{name}", "--model", "x"],
              "argv0": f"C:\\Users\\hyden\\.local\\bin\\{name}", "cmdline": "...",
              "cwd": "E:\\sdlc_development_kit\\", "name": name, "pid": 23648 + i}
             for i, name in enumerate(names)]
    return json.dumps({"id": "cli:pane:process_info",
                       "result": {"process_info": {"foreground_process_group_id": 23648,
                                                   "foreground_processes": procs,
                                                   "pane_id": pane, "shell_pid": 6764},
                                  "type": "pane_process_info"}})


class Harness:
    """The fakes for main(argv, run, sleep, clock), one event log, one fake clock.

    `timeline`: (seconds after T0, agent_status) entries for `herdr pane get`.
    `sessions`: (seconds after T0, session id) entries for its agent_session value;
    None means a pane with no agent (no `agent`, no `agent_session` key).
    `processes`: (seconds after T0, spec) entries for `herdr pane process-info --pane P`;
    a spec is a list of foreground process names, or ("raw", exit code, stdout).
    `at(seconds, fn)` runs fn when the fake clock passes T0+seconds, inside a sleep.
    """

    def __init__(self, tmp_path, monkeypatch, capsys, pane=PANE, cwd=CWD,
                 timeline=((0, "idle"),), sessions=((0, SESSION_A),),
                 processes=((0, ["claude.exe"]),)):
        self.git_dir = tmp_path / "gitdir"
        self.git_dir.mkdir()
        self.folder = self.git_dir / "sdlc-loop"
        self.home = tmp_path / "home"
        (self.home / ".claude" / "projects").mkdir(parents=True)
        for name in ("HOME", "USERPROFILE"):
            monkeypatch.setenv(name, str(self.home))
        monkeypatch.delenv("HOMEDRIVE", raising=False)
        monkeypatch.delenv("HOMEPATH", raising=False)
        self.capsys = capsys
        self.pane = pane
        self.cwd = cwd
        self.timeline = sorted(timeline)
        self.sessions = None if sessions is None else sorted(sessions)
        self.processes = sorted(processes, key=lambda p: p[0])
        self.now = T0
        self.calls = []
        self.sleeps = []
        self.schedule = []
        self.clock_reads = 0
        self.runaway = False
        self.write("loop.json", {"on": "2026-11-22T17:44:02"})

    # files
    def write(self, name, record):
        self.folder.mkdir(exist_ok=True)
        (self.folder / name).write_text(json.dumps(record), encoding="utf-8")

    def read(self, name):
        return json.loads((self.folder / name).read_text(encoding="utf-8"))

    def exists(self, name):
        return (self.folder / name).exists()

    def turn_loop_off(self):
        (self.folder / "loop.json").unlink()

    def transcript(self, session_id, mtime, project=PROJECT):
        folder = self.home / ".claude" / "projects" / project
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{session_id}.jsonl"
        path.write_text('{"type":"user"}\n', encoding="utf-8")
        os.utime(path, (mtime, mtime))
        return path

    def touch_at(self, seconds, session_id, project=PROJECT):
        self.at(seconds, lambda: self.transcript(session_id, T0 + seconds, project))

    # events
    def at(self, seconds, fn):
        self.schedule.append((T0 + seconds, fn))

    def lines(self):
        out = self.capsys.readouterr().out
        self._out = getattr(self, "_out", "") + out
        return [line for line in self._out.splitlines() if line.strip()]

    @staticmethod
    def _last_at(entries, moment, default=None):
        value = default
        for seconds, item in entries:
            if T0 + seconds <= moment:
                value = item
        return value

    # the seams
    def run(self, argv, cwd=None):
        assert isinstance(argv, list) and argv and all(isinstance(a, str) for a in argv), \
            f"run must get an argument list of strings, got {argv!r}"
        self.calls.append(Call(self.now, list(argv), cwd))
        head = argv[0]
        if head == "git":
            if argv[1:] == ["-C", self.cwd, "rev-parse", "--absolute-git-dir"]:
                return (0, str(self.git_dir) + "\n")
            return (128, "")
        if head == "gh":
            if argv[1:3] == ["issue", "create"]:
                return (0, "https://github.com/JJandDjango/sdlc_development_kit/issues/190\n")
            return (0, "[]")
        if argv[1:3] == ["pane", "get"]:
            if argv[3:] != [self.pane]:
                return (1, "")
            pane = {"agent_status": self._last_at(self.timeline, self.now),
                    "cwd": self.cwd, "pane_id": self.pane, "tab_id": "w9:t1",
                    "workspace_id": "w9"}
            if self.sessions is not None:
                pane["agent"] = "claude"
                pane["agent_session"] = {"agent": "claude", "kind": "id",
                                         "source": "herdr:claude",
                                         "value": self._last_at(self.sessions, self.now)}
            return (0, json.dumps({"id": "cli:pane:get",
                                   "result": {"pane": pane, "type": "pane_info"}}))
        if argv[1:3] == ["pane", "process-info"]:
            if argv[3:] != ["--pane", self.pane]:
                return (1, f"unknown option: {argv[3] if len(argv) > 3 else ''}")
            spec = self._last_at(self.processes, self.now, [])
            if isinstance(spec, tuple):
                return (spec[1], spec[2])
            return (0, process_info_json(self.pane, spec))
        return (0, "")

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        if self.now > T0 + GIVE_UP or len(self.sleeps) > 20000:
            raise Runaway()
        self.now += seconds
        due = sorted((s for s in self.schedule if s[0] <= self.now), key=lambda s: s[0])
        self.schedule = [s for s in self.schedule if s[0] > self.now]
        for _, fn in due:
            fn()

    def clock(self):
        self.clock_reads += 1
        if self.clock_reads > 400000:
            raise Runaway()
        return self.now

    def run_main(self):
        module = load()
        try:
            return module.main([self.pane], self.run, self.sleep, self.clock)
        except Runaway:
            self.runaway = True
            return None

    # views of the log
    def herdr_calls(self):
        return [c for c in self.calls if c.argv[0] not in ("git", "gh")]

    def typed(self):
        return [c for c in self.herdr_calls()
                if c.argv[1] == "pane" and c.argv[2] in TYPING_SUBCOMMANDS]

    def creates(self):
        return [c for c in self.calls if c.argv[0] == "gh" and c.argv[1:3] == ["issue", "create"]]

    def toasts(self):
        return [c for c in self.herdr_calls() if c.argv[1:3] == ["notification", "show"]]

    def process_calls(self):
        return [c for c in self.herdr_calls() if c.argv[1:3] == ["pane", "process-info"]]

    def reports(self):
        return [c for c in self.herdr_calls()
                if c.argv[1:3] in (["pane", "report-agent"], ["pane", "release-agent"])]


def assert_well_formed(h):
    """Every herdr pane call names the pane the launcher was given and no other."""
    for call in h.herdr_calls():
        if call.argv[1:3] == ["pane", "process-info"]:
            assert call.argv[3:] == ["--pane", h.pane], f"process-info takes --pane P: {call.argv}"
        elif call.argv[1] == "pane":
            assert call.argv[3] == h.pane, f"a call names another pane: {call.argv}"
    for seconds in h.sleeps:
        assert 0 <= seconds <= 5, f"a sleep of {seconds} seconds leaves the folder unread"
    assert not h.reports(), "the launcher must not report or release an agent"


def flag(argv, name):
    assert name in argv, f"{name} missing from {argv}"
    assert argv.index(name) + 1 < len(argv), f"{name} has no value in {argv}"
    return argv[argv.index(name) + 1]


def norm(path):
    return os.path.normcase(os.path.normpath(path))


def assert_one_stop(h, code, message, position, seen):
    """The launcher stopped: one issue, one toast, loop.json removed, one printed line, exit 1.

    `position` is the last continue sentinel's position or "none"; `seen` says whether a
    continue sentinel was seen (then `last sentinel` is the path of sentinel.seen.json).
    """
    assert code == 1, f"the launcher must stop the loop and exit 1, main returned {code!r}"
    creates = h.creates()
    assert len(creates) == 1, f"one issue per stop, got {len(creates)}"
    argv = creates[0].argv
    assert argv[:3] == ["gh", "issue", "create"]
    assert flag(argv, "--title") == message
    assert flag(argv, "--label") == "needs-ruling"
    assert creates[0].cwd == h.cwd, \
        f"gh must run in the pane's folder {h.cwd!r}, ran in {creates[0].cwd!r}"
    prefix = f"pane {h.pane}; last position {position}; last sentinel "
    body = flag(argv, "--body")
    assert body.startswith(prefix), f"issue body {body!r} does not start {prefix!r}"
    tail = body[len(prefix):]
    if seen:
        assert norm(tail) == norm(str(h.folder / "sentinel.seen.json")), tail
    else:
        assert tail == "none", tail
    toasts = h.toasts()
    assert len(toasts) == 1, f"one toast per stop, got {len(toasts)}"
    assert toasts[0].argv[1:] == ["notification", "show", "session-loop stopped", "--body",
                                  message, "--sound", "request"]
    assert toasts[0].argv[0] == h.calls[0].argv[0], "the toast goes through the same herdr"
    assert not h.exists("loop.json"), "a stop removes loop.json"
    assert h.lines()[-1] == stop_line(message)
    assert_well_formed(h)


def stop_time(h):
    creates = h.creates()
    assert creates, "no issue was filed"
    return creates[0].time


def send_continues(h, positions, start=30, gap=60):
    for i, position in enumerate(positions):
        h.at(start + gap * i, lambda p=position: h.write("sentinel.json", sentinel(position=p)))


def strike_run(tmp_path, monkeypatch, capsys, positions, pane=PANE, cwd=CWD, leftover=None):
    h = Harness(tmp_path, monkeypatch, capsys, pane=pane, cwd=cwd)
    if leftover:
        h.write("sentinel.seen.json", sentinel(position=leftover))
    send_continues(h, positions)
    return h, h.run_main()


# SC4.1: two strikes in a row.

@pytest.mark.parametrize("pane, cwd", [(PANE, CWD), ("w3:p7", OTHER_CWD)])
@pytest.mark.parametrize("position", [POSITION, "plan step 9, task t3-wrap"])
def test_sc4_1_the_second_strike_types_nothing_and_files_one_issue_naming_the_position(
        tmp_path, monkeypatch, capsys, pane, cwd, position):
    h, code = strike_run(tmp_path, monkeypatch, capsys, [position] * 3, pane=pane, cwd=cwd)
    assert_one_stop(h, code, strike_message(position), position, seen=True)
    assert [c.argv[1:] for c in h.typed()] == the_four(pane) * 2, \
        "two restarts only: the sentinel that is the second strike types nothing"
    assert h.lines() == [watching(pane, cwd), restarted(pane, position),
                         restarted(pane, position), stop_line(strike_message(position))]


def test_sc4_1_the_first_strike_restarts_and_files_nothing(tmp_path, monkeypatch, capsys):
    h, code = strike_run(tmp_path, monkeypatch, capsys, [POSITION] * 3)
    assert code == 1
    assert h.creates() and h.creates()[0].time >= T0 + 30 + 60 + 60, \
        "no issue before the third sentinel (the second strike)"
    second = [c for c in h.typed() if c.argv[2] == "send-text" and c.argv[4] == "/resume-session"]
    assert len(second) == 2 and second[-1].time < h.creates()[0].time, \
        "the first strike still restarts the pane"
    assert h.lines()[-3:-1] == [restarted(PANE, POSITION)] * 2


def test_sc4_1_a_leftover_seen_file_is_not_a_previous_position(tmp_path, monkeypatch, capsys):
    # strikes live in the launcher's memory: the first continue sentinel after the start
    # counts no strike, whatever an older sentinel.seen.json holds.
    h, code = strike_run(tmp_path, monkeypatch, capsys, [POSITION] * 3, leftover=POSITION)
    assert_one_stop(h, code, strike_message(POSITION), POSITION, seen=True)
    assert [c.argv[1:] for c in h.typed()] == the_four(PANE) * 2
    assert h.lines() == [watching(), restarted(), restarted(), stop_line(strike_message(POSITION))]


def test_sc4_1_the_stopping_sentinel_is_renamed_to_seen_and_nothing_else_is_filed(
        tmp_path, monkeypatch, capsys):
    h, code = strike_run(tmp_path, monkeypatch, capsys, [POSITION] * 3)
    assert code == 1
    assert not h.exists("sentinel.json"), "the sentinel is renamed before the strike is counted"
    assert h.read("sentinel.seen.json")["position"] == POSITION
    assert len(h.creates()) == 1
    assert [c for c in h.calls if c.argv[0] == "gh" and c not in h.creates()] == [], \
        "the stop runs no other gh command"


# SC4.2: a changed position sets the strike count back to zero.

@pytest.mark.parametrize("positions, restarts", [
    ([POSITION, POSITION_2, POSITION, POSITION, POSITION], 4),
    ([POSITION, POSITION, POSITION_2, POSITION_2, POSITION_2], 4),
    ([POSITION, POSITION_2, POSITION_2, POSITION, POSITION, POSITION], 5),
    ([POSITION, POSITION_2, POSITION_3, POSITION_3, POSITION_3], 4),
], ids=["moves-then-repeats", "one-strike-then-moves", "reset-after-one-strike", "three-moves"])
def test_sc4_2_a_changed_position_sets_the_strike_count_to_zero(
        tmp_path, monkeypatch, capsys, positions, restarts):
    h, code = strike_run(tmp_path, monkeypatch, capsys, positions)
    last = positions[-1]
    assert_one_stop(h, code, strike_message(last), last, seen=True)
    assert [c.argv[1:] for c in h.typed()] == the_four(PANE) * restarts, \
        f"{restarts} sentinels restart the pane, the next one is the second strike"
    assert h.lines() == ([watching()] + [restarted(PANE, p) for p in positions[:restarts]]
                         + [stop_line(strike_message(last))])


# SC4.3: the Claude process exits with no sentinel.

GONE = {"empty": [], "pwsh": ["pwsh.exe"], "shells": ["pwsh.exe", "conhost.exe"]}
STILL_THERE = {"exe": ["claude.exe"], "bare": ["claude"], "beside-a-shell": ["pwsh.exe", "claude.exe"]}


@pytest.mark.parametrize("pane, cwd", [(PANE, CWD), ("w3:p7", OTHER_CWD)])
@pytest.mark.parametrize("names", list(GONE.values()), ids=list(GONE))
def test_sc4_3_an_exited_claude_stops_the_loop_naming_the_pane_and_no_position(
        tmp_path, monkeypatch, capsys, pane, cwd, names):
    h = Harness(tmp_path, monkeypatch, capsys, pane=pane, cwd=cwd, processes=[(0, names)])
    code = h.run_main()
    assert_one_stop(h, code, exit_message(pane, "none"), "none", seen=False)
    assert h.typed() == []
    assert stop_time(h) <= T0 + SLACK, "the exit is read at the first polls, not after a wait"
    assert h.lines() == [watching(pane, cwd), stop_line(exit_message(pane, "none"))]


def test_sc4_3_an_exit_later_stops_at_the_next_poll(tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys, processes=[(0, ["claude.exe"]), (400, ["pwsh.exe"])])
    code = h.run_main()
    assert_one_stop(h, code, exit_message(PANE, "none"), "none", seen=False)
    assert T0 + 400 <= stop_time(h) <= T0 + 400 + SLACK
    assert h.typed() == []


def test_sc4_3_an_exit_after_restarts_names_the_last_continue_sentinels_position(
        tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys, processes=[(0, ["claude.exe"]), (300, ["pwsh.exe"])])
    send_continues(h, [POSITION, POSITION_2], start=30, gap=70)
    code = h.run_main()
    assert_one_stop(h, code, exit_message(PANE, POSITION_2), POSITION_2, seen=True)
    assert [c.argv[1:] for c in h.typed()] == the_four(PANE) * 2, "the stop types nothing more"
    assert h.lines() == [watching(), restarted(PANE, POSITION), restarted(PANE, POSITION_2),
                         stop_line(exit_message(PANE, POSITION_2))]


def test_sc4_3_a_sentinel_is_handled_before_the_exit_check_at_the_same_poll(
        tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys, processes=[(0, ["claude.exe"]), (30, ["pwsh.exe"])])
    send_continues(h, [POSITION], start=30)
    code = h.run_main()
    assert code == 1
    assert [c.argv[1:] for c in h.typed()] == the_four(PANE), \
        "the sentinel that is there when the exit is read is restarted first"
    assert_one_stop(h, code, exit_message(PANE, POSITION), POSITION, seen=True)


def test_sc4_3_process_info_is_asked_by_the_pane_flag_at_each_poll(tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys)
    h.at(100, h.turn_loop_off)
    assert h.run_main() == 0
    calls = h.process_calls()
    assert len(calls) >= 10, f"process-info is read at each poll, got {len(calls)} reads in 100 s"
    assert all(c.argv[1:] == ["pane", "process-info", "--pane", PANE] for c in calls)
    assert_well_formed(h)


@pytest.mark.parametrize("names", list(STILL_THERE.values()), ids=list(STILL_THERE))
def test_sc4_3_a_claude_foreground_process_is_not_gone_so_the_hang_check_stops_it(
        tmp_path, monkeypatch, capsys, names):
    h = Harness(tmp_path, monkeypatch, capsys, processes=[(0, names)])
    code = h.run_main()
    assert_one_stop(h, code, hung_message(PANE, "none"), "none", seen=False)
    assert T0 + HUNG - 0.5 <= stop_time(h) <= T0 + HUNG + SLACK


FAILED_INFO = {
    "not-found": (1, '{"error":{"code":"pane_not_found","message":"pane not found"},'
                     '"id":"cli:pane:process_info"}'),
    "cannot-start": (127, ""),
    "empty-output": (0, ""),
    "not-json": (0, "claude.exe is running"),
}


@pytest.mark.parametrize("spec", list(FAILED_INFO.values()), ids=list(FAILED_INFO))
def test_sc4_3_a_failed_process_info_is_not_read_as_gone_and_the_hang_check_is_the_net(
        tmp_path, monkeypatch, capsys, spec):
    h = Harness(tmp_path, monkeypatch, capsys, processes=[(0, ("raw",) + spec)])
    code = h.run_main()
    assert_one_stop(h, code, hung_message(PANE, "none"), "none", seen=False)
    assert T0 + HUNG - 0.5 <= stop_time(h) <= T0 + HUNG + SLACK
    assert h.typed() == []


# SC4.3: the hung session.

@pytest.mark.parametrize("case", ["no-transcript", "transcript-older-than-the-start",
                                  "pane-has-no-agent-session"])
@pytest.mark.parametrize("pane, cwd", [(PANE, CWD), ("w3:p7", OTHER_CWD)])
def test_sc4_3_a_session_with_no_change_for_60_minutes_from_the_start_stops_the_loop(
        tmp_path, monkeypatch, capsys, case, pane, cwd):
    h = Harness(tmp_path, monkeypatch, capsys, pane=pane, cwd=cwd,
                timeline=[(0, "working")],
                sessions=None if case == "pane-has-no-agent-session" else [(0, SESSION_A)])
    if case == "transcript-older-than-the-start":
        h.transcript(SESSION_A, 100.0)
    code = h.run_main()
    assert_one_stop(h, code, hung_message(pane, "none"), "none", seen=False)
    assert T0 + HUNG - 0.5 <= stop_time(h) <= T0 + HUNG + SLACK, \
        f"stopped at {stop_time(h) - T0} s after the start"
    assert h.typed() == []
    assert h.lines() == [watching(pane, cwd), stop_line(hung_message(pane, "none"))]


def test_sc4_3_the_hang_clock_runs_from_the_transcripts_last_write(tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys, timeline=[(0, "working")])
    h.transcript(SESSION_A, T0)
    h.touch_at(1500, SESSION_A)
    h.touch_at(3000, SESSION_A)
    code = h.run_main()
    assert_one_stop(h, code, hung_message(PANE, "none"), "none", seen=False)
    assert T0 + 3000 + HUNG - 0.5 <= stop_time(h) <= T0 + 3000 + HUNG + SLACK, \
        f"stopped at {stop_time(h) - T0} s: 60 minutes after the last write at 3000 s"
    assert h.typed() == []


def test_sc4_3_the_hang_clock_runs_from_the_last_restart(tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys, timeline=[(0, "working"), (40, "idle")])
    h.transcript(SESSION_A, 100.0)
    send_continues(h, [POSITION], start=30)
    code = h.run_main()
    assert_one_stop(h, code, hung_message(PANE, POSITION), POSITION, seen=True)
    typed = h.typed()
    assert [c.argv[1:] for c in typed] == the_four(PANE)
    assert T0 + 30 + HUNG - 0.5 <= stop_time(h) <= typed[-1].time + HUNG + SLACK, \
        f"stopped at {stop_time(h) - T0} s; the restart was at about 40 s"
    assert h.lines() == [watching(), restarted(), stop_line(hung_message(PANE, POSITION))]


def test_sc4_3_the_hang_check_reads_the_session_id_again_after_a_clear(
        tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys, timeline=[(0, "working"), (40, "idle")],
                sessions=[(0, SESSION_A), (60, SESSION_B)])
    h.transcript(SESSION_A, T0)
    h.transcript("ffffffff-0000-4000-8000-000000000000", 5000.0, project="E--some-other-repo")
    h.touch_at(2000, SESSION_B, project="E--other-project-folder")
    send_continues(h, [POSITION], start=30)
    code = h.run_main()
    assert_one_stop(h, code, hung_message(PANE, POSITION), POSITION, seen=True)
    assert T0 + 2000 + HUNG - 0.5 <= stop_time(h) <= T0 + 2000 + HUNG + SLACK, \
        f"stopped at {stop_time(h) - T0} s: the new session's transcript, found by its id " \
        "in whatever project folder, was last written at 2000 s"


def test_sc4_3_the_transcript_is_found_by_the_id_alone_in_any_project_folder(
        tmp_path, monkeypatch, capsys):
    h = Harness(tmp_path, monkeypatch, capsys, timeline=[(0, "working")])
    h.transcript("aaaaaaaa-0000-4000-8000-000000000000", T0 + 4000, project=PROJECT)
    h.transcript(SESSION_A, T0 + 1200, project="C--Users-hyden-some-other-repo")
    code = h.run_main()
    assert_one_stop(h, code, hung_message(PANE, "none"), "none", seen=False)
    assert T0 + 1200 + HUNG - 0.5 <= stop_time(h) <= T0 + 1200 + HUNG + SLACK, \
        "another session's newer transcript must not hold the clock back"


@pytest.mark.parametrize("kind", ["mystery", "wrap", ""])
def test_sc4_3_a_sentinel_of_an_unknown_kind_is_left_and_ends_at_the_hang_check(
        tmp_path, monkeypatch, capsys, kind):
    h = Harness(tmp_path, monkeypatch, capsys, timeline=[(0, "working")])
    sent = sentinel(kind=kind)
    h.at(30, lambda: h.write("sentinel.json", sent))
    code = h.run_main()
    assert_one_stop(h, code, hung_message(PANE, "none"), "none", seen=False)
    assert h.typed() == [], "the launcher types nothing for a sentinel of an unknown kind"
    assert h.exists("sentinel.json") and h.read("sentinel.json") == sent, "it is left in place"
    assert not h.exists("sentinel.seen.json")
    assert T0 + HUNG - 0.5 <= stop_time(h) <= T0 + HUNG + SLACK
