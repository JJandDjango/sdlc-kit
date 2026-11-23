"""Spec tests for herdr_loop.py, unit l2 of the session-loop contract.

Each test calls main(argv, run, sleep, clock) with fakes. The fake `run` answers
herdr, git and gh calls; the fake `sleep` moves a fake clock and fires scheduled
events (a sentinel appearing, the loop turned off), so a watch ends on its own.
The files (loop.json, sentinel.json, ...) are real files in a temp git folder.
No real process starts and nothing is typed into a real pane.

Unit l3's parts (strikes, the exit check, the hang check, the stop issue, the
toast, exit 1) are not pinned here, and no absence of them is pinned either.
"""
import json
from collections import namedtuple

import pytest

PANE = "w9:p1"
CWD = r"E:\sdlc_development_kit"
T0 = 1000.0
POSITION = "plan step 4, task none"
TYPING_SUBCOMMANDS = ("send-text", "send-keys", "run")

Call = namedtuple("Call", "time argv sentinel_present restart_printed status")


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


OFF = "herdr-loop: the session loop is off"


class Harness:
    """The fakes for main(argv, run, sleep, clock), one event log, one fake clock.

    `timeline` is a list of (seconds after T0, agent_status): the status `herdr
    pane get` reports at a fake time is the last entry at or before it.
    `at(seconds, fn)` schedules fn to run when the fake clock passes T0+seconds,
    inside a sleep call.
    """

    def __init__(self, tmp_path, capsys, pane=PANE, cwd=CWD, loop=True,
                 timeline=((0, "idle"),)):
        self.git_dir = tmp_path / "gitdir"
        self.git_dir.mkdir()
        self.folder = self.git_dir / "sdlc-loop"
        self.capsys = capsys
        self.pane = pane
        self.cwd = cwd
        self.timeline = sorted(timeline)
        self.now = T0
        self.calls = []
        self.sleeps = []
        self.schedule = []
        self.clock_reads = 0
        self._out = ""
        if loop:
            self.write("loop.json", {"on": "2026-11-22T17:44:02"})

    # files
    def write(self, name, record):
        self.folder.mkdir(exist_ok=True)
        (self.folder / name).write_text(json.dumps(record), encoding="utf-8")

    def write_raw(self, name, text):
        self.folder.mkdir(exist_ok=True)
        (self.folder / name).write_text(text, encoding="utf-8")

    def remove(self, name):
        (self.folder / name).unlink()

    def read(self, name):
        return json.loads((self.folder / name).read_text(encoding="utf-8"))

    def exists(self, name):
        return (self.folder / name).exists()

    def turn_loop_off(self):
        self.remove("loop.json")

    # events
    def at(self, seconds, fn):
        self.schedule.append((T0 + seconds, fn))

    def status_at(self, moment):
        status = self.timeline[0][1]
        for seconds, value in self.timeline:
            if T0 + seconds <= moment:
                status = value
        return status

    def printed(self):
        self._out += self.capsys.readouterr().out
        return self._out

    def lines(self):
        return [line for line in self.printed().splitlines() if line.strip()]

    # the seams
    def run(self, argv):
        assert isinstance(argv, list) and argv and all(isinstance(a, str) for a in argv), \
            f"run must get an argument list of strings, got {argv!r}"
        status = None
        out = (0, "")
        if argv[0] == "git":
            if argv[1:] == ["-C", self.cwd, "rev-parse", "--absolute-git-dir"]:
                out = (0, str(self.git_dir) + "\n")
            else:
                out = (128, "")
        elif argv[0] == "gh":
            out = (0, "[]")
        elif argv[1:3] == ["pane", "get"]:
            status = self.status_at(self.now)
            pane = {"agent": "claude",
                    "agent_session": {"agent": "claude", "kind": "id",
                                      "source": "herdr:claude", "value": "0f8c1d2e"},
                    "agent_status": status, "cwd": self.cwd,
                    "pane_id": argv[3] if len(argv) > 3 else self.pane,
                    "tab_id": "w9:t1", "workspace_id": "w9"}
            out = (0, json.dumps({"id": "cli:pane:get",
                                  "result": {"pane": pane, "type": "pane_info"}}))
        self.calls.append(Call(self.now, list(argv), self.exists("sentinel.json"),
                               "restarted pane" in self.printed(), status))
        return out

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        if len(self.sleeps) > 5000 or self.now > T0 + 4 * 3600:
            raise AssertionError("the watch never ended")
        self.now += seconds
        due = sorted((s for s in self.schedule if s[0] <= self.now), key=lambda s: s[0])
        self.schedule = [s for s in self.schedule if s[0] > self.now]
        for _, fn in due:
            fn()

    def clock(self):
        self.clock_reads += 1
        if self.clock_reads > 200000:
            raise AssertionError("the launcher spins on the clock")
        return self.now

    def run_main(self):
        module = load()
        return module.main([self.pane], self.run, self.sleep, self.clock)

    # views of the log
    def herdr_calls(self):
        return [c for c in self.calls if c.argv[0] not in ("git", "gh")]

    def gh_calls(self):
        return [c for c in self.calls if c.argv[0] == "gh"]

    def git_calls(self):
        return [c for c in self.calls if c.argv[0] == "git"]

    def typed(self):
        return [c for c in self.herdr_calls()
                if c.argv[1] == "pane" and c.argv[2] in TYPING_SUBCOMMANDS]

    def reports(self):
        return [c for c in self.herdr_calls()
                if c.argv[1:3] in (["pane", "report-agent"], ["pane", "release-agent"])]


def assert_well_formed(h):
    """Every herdr pane call names the pane the launcher was given, and no other.

    `pane process-info` takes the pane by flag (`--pane P`, l3); every other pane
    call takes it as its third argument.
    """
    for call in h.herdr_calls():
        if call.argv[1] == "pane" and call.argv[2] == "process-info":
            assert call.argv[3:5] == ["--pane", h.pane], f"a call names another pane: {call.argv}"
        elif call.argv[1] == "pane":
            assert call.argv[3] == h.pane, f"a call names another pane: {call.argv}"
    for seconds in h.sleeps:
        assert 0 <= seconds <= 5, f"a sleep of {seconds} seconds leaves the folder unread"
    assert not h.reports(), "the launcher must not report or release an agent"


def the_four(pane, first_text="/clear"):
    return [["pane", "send-text", pane, first_text], ["pane", "send-keys", pane, "Enter"],
            ["pane", "send-text", pane, "/resume-session"], ["pane", "send-keys", pane, "Enter"]]


# Start: the pane, its git folder, the first line.

@pytest.mark.parametrize("cwd", [CWD, "C:/work/another repo"])
def test_start_reads_the_pane_then_the_git_folder_of_its_cwd(tmp_path, capsys, cwd):
    h = Harness(tmp_path, capsys, cwd=cwd)
    h.at(10, h.turn_loop_off)
    assert h.run_main() == 0
    assert h.calls[0].argv[1:] == ["pane", "get", PANE]
    git = h.git_calls()
    assert git, "the launcher must ask git for the pane's git folder"
    assert all(c.argv == ["git", "-C", cwd, "rev-parse", "--absolute-git-dir"] for c in git)
    assert h.calls.index(git[0]) > 0
    assert h.lines()[0] == watching(PANE, cwd)


def test_loop_turned_off_prints_one_line_and_exits_0_typing_nothing(tmp_path, capsys):
    h = Harness(tmp_path, capsys)
    h.at(42, h.turn_loop_off)
    assert h.run_main() == 0
    assert h.lines() == [watching(), OFF]
    assert h.typed() == []
    assert_well_formed(h)


@pytest.mark.parametrize("folder_exists", [True, False])
def test_no_loop_on_at_the_start_prints_one_line_and_exits_2(tmp_path, capsys, folder_exists):
    h = Harness(tmp_path, capsys, pane="w3:p7", loop=False)
    if folder_exists:
        h.folder.mkdir()
    assert h.run_main() == 2
    assert h.lines() == ["herdr-loop: no session loop is on in pane w3:p7; "
                         "run /sdlc loop on there"]
    assert h.typed() == []
    assert not h.reports()


# SC1.3: with no sentinel the launcher types nothing and never touches the tree pane's flag.

@pytest.mark.parametrize("extra", ["none", "seen", "waiting", "both"])
def test_sc1_3_a_stopped_team_run_with_no_sentinel_gets_no_keystroke(tmp_path, capsys, extra):
    h = Harness(tmp_path, capsys,
                timeline=[(0, "idle"), (120, "working"), (300, "idle"), (420, "blocked"),
                          (480, "idle")])
    if extra in ("seen", "both"):
        h.write("sentinel.seen.json", sentinel())
    if extra in ("waiting", "both"):
        h.write("waiting.json", {"issue": 172, "at": "2026-11-22T17:44:02",
                                 "due": "2026-11-22T18:39:00", "cron": "39 18 22 11 *"})
    h.at(900, h.turn_loop_off)
    assert h.run_main() == 0
    assert h.typed() == []
    assert h.lines() == [watching(), OFF]
    assert_well_formed(h)
    assert h.now >= T0 + 900


# SC1.1: the restart.

@pytest.mark.parametrize("pane", [PANE, "w3:p7"])
def test_sc1_1_a_continue_sentinel_types_clear_then_resume_session_into_the_same_pane(
        tmp_path, capsys, pane):
    h = Harness(tmp_path, capsys, pane=pane)
    h.at(30, lambda: h.write("sentinel.json", sentinel()))
    h.at(200, h.turn_loop_off)
    assert h.run_main() == 0
    assert [c.argv[1:] for c in h.typed()] == the_four(pane)
    assert_well_formed(h)
    assert not any(c.restart_printed for c in h.typed()), \
        "the restarted line must follow the typing, not precede it"
    assert h.lines() == [watching(pane), restarted(pane, POSITION), OFF]


def test_sc1_1_the_restart_line_names_the_sentinels_position(tmp_path, capsys):
    h = Harness(tmp_path, capsys)
    h.at(30, lambda: h.write("sentinel.json", sentinel(position="plan step 9, task t3-wrap")))
    h.at(200, h.turn_loop_off)
    assert h.run_main() == 0
    assert restarted(PANE, "plan step 9, task t3-wrap") in h.lines()


def test_sc1_1_types_exactly_resume_session_and_never_the_next(tmp_path, capsys):
    h = Harness(tmp_path, capsys)
    h.at(30, lambda: h.write("sentinel.json", sentinel(next_="Next 31: session-loop-sidebar")))
    h.at(200, h.turn_loop_off)
    assert h.run_main() == 0
    texts = [c.argv[4] for c in h.typed() if c.argv[2] == "send-text"]
    assert texts == ["/clear", "/resume-session"]


@pytest.mark.parametrize("idle_after, latest", [(0, 10), (20, 60), (45, 60)])
def test_sc1_1_types_within_60_seconds_of_the_sentinel_once_the_pane_reads_idle(
        tmp_path, capsys, idle_after, latest):
    wrote = 30
    h = Harness(tmp_path, capsys,
                timeline=[(0, "working"), (wrote + idle_after, "idle")])
    h.at(wrote, lambda: h.write("sentinel.json", sentinel()))
    h.at(wrote + 300, h.turn_loop_off)
    assert h.run_main() == 0
    typed = h.typed()
    assert [c.argv[1:] for c in typed] == the_four(PANE)
    assert typed[0].time >= T0 + wrote + idle_after, "typed while the pane did not read idle"
    gets = [c for c in h.herdr_calls() if c.argv[1:3] == ["pane", "get"]
            and c.time <= typed[0].time]
    assert gets[-1].status == "idle", "the pane must read idle just before the first keystroke"
    assert typed[2].time <= T0 + wrote + latest, "/resume-session came too late"
    assert typed[3].time <= T0 + wrote + latest
    assert_well_formed(h)


def test_sc1_1_waits_for_idle_however_long_and_types_nothing_meanwhile(tmp_path, capsys):
    wrote = 30
    h = Harness(tmp_path, capsys,
                timeline=[(0, "working"), (wrote + 40, "blocked"), (wrote + 90, "working"),
                          (wrote + 150, "idle")])
    h.at(wrote, lambda: h.write("sentinel.json", sentinel()))
    h.at(wrote + 400, h.turn_loop_off)
    assert h.run_main() == 0
    typed = h.typed()
    assert [c.argv[1:] for c in typed] == the_four(PANE)
    assert typed[0].time >= T0 + wrote + 150
    assert h.lines() == [watching(), restarted(), OFF]


def test_sc1_1_waits_3_seconds_between_clear_and_resume_session(tmp_path, capsys):
    h = Harness(tmp_path, capsys)
    h.at(30, lambda: h.write("sentinel.json", sentinel()))
    h.at(200, h.turn_loop_off)
    assert h.run_main() == 0
    typed = h.typed()
    gap = typed[2].time - typed[1].time
    assert 3 <= gap <= 5, f"{gap} seconds between /clear and /resume-session"
    assert typed[1].time - typed[0].time <= 1, "Enter follows /clear at once"
    assert typed[3].time - typed[2].time <= 1, "Enter follows /resume-session at once"


def test_sc1_1_renames_the_sentinel_before_typing_and_replaces_a_leftover(tmp_path, capsys):
    h = Harness(tmp_path, capsys, timeline=[(0, "working"), (50, "idle")])
    h.write("sentinel.seen.json", sentinel(position="an older position"))
    new = sentinel(position="plan step 5, task none", next_="Next 40: the next one")
    h.at(30, lambda: h.write("sentinel.json", new))
    h.at(300, h.turn_loop_off)
    assert h.run_main() == 0
    assert h.typed(), "the launcher must restart the pane"
    assert h.typed()[0].sentinel_present is False, "sentinel.json must be renamed before typing"
    assert not h.exists("sentinel.json")
    assert h.read("sentinel.seen.json") == new
    assert len([c for c in h.typed() if c.argv[2] == "send-text"]) == 2, "one restart only"


def test_sc1_1_each_sentinel_restarts_the_pane_once_it_reads_idle_again(tmp_path, capsys):
    h = Harness(tmp_path, capsys,
                timeline=[(0, "idle"), (40, "working"), (335, "idle")])
    h.at(20, lambda: h.write("sentinel.json", sentinel(position="plan step 2, task none")))
    h.at(320, lambda: h.write("sentinel.json", sentinel(position="plan step 3, task none")))
    h.at(520, h.turn_loop_off)
    assert h.run_main() == 0
    typed = h.typed()
    assert [c.argv[1:] for c in typed] == the_four(PANE) + the_four(PANE)
    assert typed[4].time >= T0 + 335, "the second restart typed while the pane worked"
    assert typed[7].time <= T0 + 320 + 60
    assert h.lines() == [watching(), restarted(PANE, "plan step 2, task none"),
                         restarted(PANE, "plan step 3, task none"), OFF]
    assert_well_formed(h)


# herdr reads `done`, not `idle`, when a turn ends in a pane nobody has looked at.

@pytest.mark.parametrize("pane", [PANE, "w3:p7"])
def test_sc1_1_a_continue_sentinel_restarts_a_pane_that_reads_done(tmp_path, capsys, pane):
    h = Harness(tmp_path, capsys, pane=pane, timeline=[(0, "done")])
    h.at(30, lambda: h.write("sentinel.json", sentinel()))
    h.at(200, h.turn_loop_off)
    assert h.run_main() == 0
    assert [c.argv[1:] for c in h.typed()] == the_four(pane)
    assert_well_formed(h)
    assert h.lines() == [watching(pane), restarted(pane, POSITION), OFF]


def test_sc1_1_a_pane_moving_from_working_to_done_is_restarted_once_it_reads_done(
        tmp_path, capsys):
    wrote = 30
    h = Harness(tmp_path, capsys, timeline=[(0, "working"), (wrote + 45, "done")])
    h.at(wrote, lambda: h.write("sentinel.json", sentinel()))
    h.at(wrote + 300, h.turn_loop_off)
    assert h.run_main() == 0
    typed = h.typed()
    assert [c.argv[1:] for c in typed] == the_four(PANE)
    assert typed[0].time >= T0 + wrote + 45, "typed while the pane read working"
    gets = [c for c in h.herdr_calls() if c.argv[1:3] == ["pane", "get"]
            and c.time <= typed[0].time]
    assert gets[-1].status == "done", "the pane must read done just before the first keystroke"
    assert typed[3].time <= T0 + wrote + 60, "/resume-session came too late"
    assert h.lines() == [watching(), restarted(), OFF]
    assert_well_formed(h)


@pytest.mark.parametrize("status", ["blocked", "unknown"])
def test_sc1_1_a_pane_reading_blocked_or_unknown_gets_no_keystroke(tmp_path, capsys, status):
    wrote = 30
    h = Harness(tmp_path, capsys, timeline=[(0, status), (wrote + 600, "idle")])
    h.at(wrote, lambda: h.write("sentinel.json", sentinel()))
    h.at(wrote + 900, h.turn_loop_off)
    assert h.run_main() == 0
    typed = h.typed()
    assert [c.argv[1:] for c in typed] == the_four(PANE)
    assert typed[0].time >= T0 + wrote + 600, f"typed while the pane read {status}"
    assert h.lines() == [watching(), restarted(), OFF]
    assert_well_formed(h)


@pytest.mark.parametrize("partial", ["", '{"kind": "continue", "position": "plan st'],
                         ids=["empty", "cut-mid-object"])
def test_a_sentinel_that_does_not_parse_is_left_and_read_again_at_the_next_poll(
        tmp_path, capsys, partial):
    h = Harness(tmp_path, capsys)
    seen_while_partial = {}

    def look():
        seen_while_partial["exists"] = h.exists("sentinel.json")
        seen_while_partial["text"] = (h.folder / "sentinel.json").read_text(encoding="utf-8") \
            if h.exists("sentinel.json") else None
        seen_while_partial["renamed"] = h.exists("sentinel.seen.json")
        seen_while_partial["typed"] = list(h.typed())

    good = sentinel(position="plan step 6, task none")
    h.at(30, lambda: h.write_raw("sentinel.json", partial))
    h.at(40, look)
    h.at(50, lambda: h.write("sentinel.json", good))
    h.at(300, h.turn_loop_off)
    assert h.run_main() == 0, "a half-written sentinel must not crash the launcher"
    assert seen_while_partial["exists"], "an unparseable sentinel.json must be left in place"
    assert seen_while_partial["text"] == partial
    assert not seen_while_partial["renamed"], "an unparseable sentinel must not be renamed"
    assert seen_while_partial["typed"] == [], "an unparseable sentinel must type nothing"
    assert [c.argv[1:] for c in h.typed()] == the_four(PANE)
    assert h.typed()[0].time >= T0 + 50, "typed before a parseable sentinel was there"
    assert h.read("sentinel.seen.json") == good
    assert not h.exists("sentinel.json")
    assert h.lines() == [watching(), restarted(PANE, "plan step 6, task none"), OFF]
    assert_well_formed(h)


# SC3.2 and the other quiet ends: types nothing, files nothing.

@pytest.mark.parametrize("loop_removed", [True, False])
def test_sc3_2_after_a_self_wrap_the_launcher_types_nothing_and_leaves_the_issue_open(
        tmp_path, capsys, loop_removed):
    h = Harness(tmp_path, capsys)
    waiting = {"issue": 172, "at": "2026-11-22T17:44:02",
               "due": "2026-11-22T18:39:00", "cron": "39 18 22 11 *"}
    h.write("waiting.json", waiting)

    def self_wrap():
        if loop_removed:
            h.turn_loop_off()
        h.write("sentinel.json", sentinel(kind="self-wrap"))

    h.at(12, self_wrap)
    assert h.run_main() == 0
    assert h.lines() == [watching(), "herdr-loop: the loop stopped: self-wrap"]
    assert h.typed() == []
    assert h.gh_calls() == [], "no gh call: the needs-ruling issue stays open"
    assert h.read("waiting.json") == waiting
    assert not h.reports()


@pytest.mark.parametrize("loop_removed", [True, False])
def test_a_pick_sentinel_stops_quietly_and_types_nothing(tmp_path, capsys, loop_removed):
    h = Harness(tmp_path, capsys)

    def pick():
        if loop_removed:
            h.turn_loop_off()
        h.write("sentinel.json", sentinel(kind="pick", next_="(none)"))

    h.at(12, pick)
    assert h.run_main() == 0
    assert h.lines() == [watching(), "herdr-loop: the loop stopped: pick"]
    assert h.typed() == []
    assert h.gh_calls() == [], "the wrap filed the pick issue; the launcher files none"
    assert not h.reports()
