"""Loop files suite (contract: session-loop, unit l1-loop-files, checks SC1.2, SC2.1,
SC5.1 and SC5.2).

`workflows/tools/loop.py` keeps the session loop's files under
`{git folder}/sdlc-loop/` (`loop.json`, `waiting.json`, `sentinel.json`) and files and
closes `needs-ruling` issues. The module is loaded by path and driven in process:

* every git and `gh` call goes through the module's `run(argv)` seam, which the tests
  replace with a fake runner (a test that reached the real `gh` would file a real issue);
* the stop's time comes from the module's `now()` seam, which the tests set;
* the git folder is a temporary folder the fake `git rev-parse --absolute-git-dir` names.

A few tests run the script as a subprocess in a real, throwaway `git init` folder; they
use only `on`, `off` and `due`, which never call `gh`.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LOOP_PY = ROOT / "workflows" / "tools" / "loop.py"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

NOW = dt.datetime(2026, 11, 22, 17, 41, 44)
BRANCH = "feat/session-loop-l1"
HEAD = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
OTHER = "0f" * 20
PICK = "Pick the next deliverable"
ANSWER = "answered in the session"
NO_LABEL = "session-loop: the needs-ruling label is missing; run: gh label create needs-ruling"
NOT_PUSHED = "session-loop: the wrap's commit is not on the remote; push first"
ON_LINE = "session loop on; a launcher may now restart this repo's sessions"
OFF_LINE = "session loop off"
GIT_WRITES = {"add", "commit", "push", "checkout", "switch", "reset", "merge", "rebase",
              "restore", "stash", "apply", "mv", "rm", "tag", "cherry-pick", "revert",
              "pull", "fetch", "clean", "config"}


def flag(argv, name):
    """The value after the flag in an argument list; None when the flag is absent."""
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def iso(when: dt.datetime) -> str:
    return when.isoformat(timespec="seconds")


def snapshot(base: Path, skip: Path | None = None) -> dict:
    """Every file and folder under base (bytes for files), skipping the folder `skip`."""
    seen = {}
    for p in sorted(base.rglob("*")):
        if skip is not None and (p == skip or skip in p.parents):
            continue
        rel = p.relative_to(base).as_posix()
        seen[rel] = None if p.is_dir() else p.read_bytes()
    return seen


class Env:
    """A fixture repository, a fake `git`/`gh` behind the run seam, and a settable clock."""

    def __init__(self, tmp_path: Path, monkeypatch, capsys):
        self.tmp = tmp_path
        self.mp = monkeypatch
        self.capsys = capsys
        self.repo = tmp_path / "repo"
        (self.repo / "docs").mkdir(parents=True)
        (self.repo / "docs" / "backlog.md").write_text("## Next\n\n(none)\n", encoding="utf-8")
        self.git = tmp_path / "gitdir"
        self.git.mkdir()
        self.dir = self.git / "sdlc-loop"
        monkeypatch.chdir(self.repo)
        self.now = NOW
        self.labels = ["needs-ruling"]
        self.open_issues: list[dict] = []
        self.next_number = 172
        self.branch = BRANCH
        self.head = HEAD
        self.remote = {BRANCH: HEAD}
        self.create_rc = 0
        self.close_rc = 0
        self.calls: list[list[str]] = []
        self.bad: list[str] = []
        self.created: list[dict] = []
        self.closed: list[dict] = []
        self.sentinel_at_call: list[tuple[list[str], bool]] = []
        self.waiting_at_call: list[tuple[list[str], bool]] = []
        self.removed_after_sentinel: list[str] = []
        self.module = None
        self._spy_removals()

    # -- the fake runner -------------------------------------------------------------

    def _spy_removals(self):
        real_remove, real_unlink = os.remove, os.unlink
        sentinel = self.dir / "sentinel.json"

        def watch(real):
            def spy(path, *a, **k):
                if Path(path).name in ("loop.json", "waiting.json") and sentinel.exists():
                    self.removed_after_sentinel.append(Path(path).name)
                return real(path, *a, **k)
            return spy

        self.mp.setattr(os, "remove", watch(real_remove))
        self.mp.setattr(os, "unlink", watch(real_unlink))

    def fake_run(self, argv):
        if not (isinstance(argv, list) and all(isinstance(a, str) for a in argv)):
            self.bad.append(f"not an argument list of strings: {argv!r}")
            raise AssertionError(self.bad[-1])
        self.calls.append(list(argv))
        self.sentinel_at_call.append((list(argv), (self.dir / "sentinel.json").exists()))
        self.waiting_at_call.append((list(argv), (self.dir / "waiting.json").exists()))
        out = self._answer(argv)
        if out is None:
            self.bad.append(f"unexpected call: {argv!r}")
            raise AssertionError(self.bad[-1])
        rc, stdout, stderr = out
        return subprocess.CompletedProcess(argv, rc, stdout, stderr)

    def _answer(self, argv):
        if argv[0] == "git":
            rest = argv[1:]
            if rest == ["rev-parse", "--absolute-git-dir"]:
                return 0, f"{self.git}\n", ""
            if rest == ["rev-parse", "HEAD"]:
                return 0, f"{self.head}\n", ""
            if rest == ["branch", "--show-current"]:
                return 0, f"{self.branch}\n", ""
            if len(rest) == 3 and rest[:2] == ["ls-remote", "origin"]:
                ref = rest[2]
                for name, sha in self.remote.items():
                    if ref == f"refs/heads/{name}":
                        return 0, f"{sha}\t{ref}\n", ""
                return 0, "", ""
            return None
        if argv[0] != "gh":
            return None
        rest = argv[1:]
        if rest[:2] == ["label", "list"]:
            if flag(argv, "--search") != "needs-ruling" or flag(argv, "--json") != "name":
                return None
            found = [n for n in self.labels if "needs-ruling" in n]
            return 0, json.dumps([{"name": n} for n in found]), ""
        if rest[:2] == ["issue", "list"]:
            json_fields = (flag(argv, "--json") or "").split(",")
            if (flag(argv, "--state") != "open" or flag(argv, "--label") != "needs-ruling"
                    or "title" not in json_fields or "number" not in json_fields):
                return None
            return 0, json.dumps(self.open_issues, ensure_ascii=False), ""
        if rest[:2] == ["issue", "create"]:
            title, body, label = flag(argv, "--title"), flag(argv, "--body"), flag(argv, "--label")
            if label != "needs-ruling" or not title or not body:
                return None
            if self.create_rc:
                return self.create_rc, "", "gh: could not create the issue\n"
            number = self.next_number
            self.next_number += 1
            self.open_issues.append({"number": number, "title": title})
            self.created.append({"number": number, "title": title, "body": body, "label": label})
            return 0, f"https://github.com/JJandDjango/sdlc-kit/issues/{number}\n", ""
        if rest[:2] == ["issue", "close"]:
            if len(rest) < 3 or flag(argv, "--comment") is None:
                return None
            if self.close_rc:
                return self.close_rc, "", "gh: could not close the issue\n"
            self.closed.append({"number": rest[2], "comment": flag(argv, "--comment")})
            return 0, "", ""
        return None

    # -- driving the module ----------------------------------------------------------

    def load(self):
        assert LOOP_PY.is_file(), "workflows/tools/loop.py is missing"
        spec = importlib.util.spec_from_file_location("sdlc_loop_under_test", LOOP_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def loop(self):
        if self.module is None:
            module = self.load()
            self.mp.setattr(module, "run", self.fake_run)
            self.mp.setattr(module, "now", lambda: self.now)
            self.module = module
        return self.module

    def main(self, *args):
        """Run `loop.py ARGS` in process: (exit code, stdout, stderr)."""
        module = self.loop()
        self.capsys.readouterr()
        rc = module.main(list(args))
        out, err = self.capsys.readouterr()
        return rc, out, err

    def clean(self):
        """The fake saw only the calls the interface names, each an argument list."""
        assert self.bad == []
        written = [c for c in self.calls if c[0] == "git" and c[1] in GIT_WRITES]
        assert written == []

    def file(self, name):
        return json.loads((self.dir / name).read_text(encoding="utf-8"))

    def has(self, name):
        return (self.dir / name).exists()

    def put(self, name, doc):
        self.dir.mkdir(exist_ok=True)
        (self.dir / name).write_text(json.dumps(doc), encoding="utf-8")

    def gh_calls(self, *words):
        return [c for c in self.calls if c[0] == "gh" and c[1:1 + len(words)] == list(words)]

    def wrap(self, next_text="Next 31: session-loop-sidebar", *extra, step="4", task="none"):
        return self.main("wrap", "--plan-step", step, "--task", task, "--next", next_text, *extra)


@pytest.fixture
def env(tmp_path, monkeypatch, capsys):
    return Env(tmp_path, monkeypatch, capsys)


# -- on and off ----------------------------------------------------------------------


def test_on_writes_loop_json_with_the_time_and_prints_the_line(env):
    rc, out, err = env.main("on")
    assert (rc, out, err) == (0, ON_LINE + "\n", "")
    assert env.file("loop.json") == {"on": "2026-11-22T17:41:44"}
    env.clean()


def test_on_when_on_rewrites_the_time_and_prints_the_same_line(env):
    env.main("on")
    env.now = NOW + dt.timedelta(hours=2, seconds=3)
    rc, out, _ = env.main("on")
    assert (rc, out) == (0, ON_LINE + "\n")
    assert env.file("loop.json") == {"on": "2026-11-22T19:41:47"}


def test_off_removes_loop_json_and_prints_the_line(env):
    env.main("on")
    rc, out, err = env.main("off")
    assert (rc, out, err) == (0, OFF_LINE + "\n", "")
    assert not env.has("loop.json")


def test_off_when_off_prints_the_same_line_and_exits_0(env):
    rc, out, err = env.main("off")
    assert (rc, out, err) == (0, OFF_LINE + "\n", "")
    assert not env.has("loop.json")


# -- SC2.1: the stop files its issue first; the reply closes it ----------------------


def test_sc2_1_stop_files_the_issue_before_it_writes_the_waiting_file(env):
    question = "Which database does the loop keep its state in?\nOne file or three?"
    rc, out, err = env.main("stop", "--question", question)
    assert rc == 0 and err == ""
    assert env.created == [{"number": 172, "title": "Which database does the loop keep its state in?",
                            "body": question, "label": "needs-ruling"}]
    at_create = [seen for argv, seen in env.waiting_at_call if argv[:3] == ["gh", "issue", "create"]]
    assert at_create == [False], "waiting.json existed before the issue was filed"
    assert env.has("waiting.json")
    env.clean()


def test_sc2_1_stop_checks_the_label_before_it_files(env):
    env.main("stop", "--question", "Which one?")
    heads = [c[:3] for c in env.calls if c[0] == "gh"]
    assert heads.index(["gh", "label", "list"]) < heads.index(["gh", "issue", "create"])


def test_sc2_1_stop_writes_the_waiting_file_and_prints_the_same_three_keys(env):
    rc, out, err = env.main("stop", "--question", "Which one?")
    assert rc == 0 and err == ""
    printed = json.loads(out)
    assert printed == {"issue": 172, "due": "2026-11-22T18:36:00", "cron": "36 18 22 11 *"}
    assert out.count("\n") == 1 and out.endswith("\n")
    waiting = env.file("waiting.json")
    assert waiting == {"issue": 172, "at": "2026-11-22T17:41:44", "due": "2026-11-22T18:36:00",
                       "cron": "36 18 22 11 *"}
    assert env.has("loop.json") is False  # stop never turns the loop on or off
    assert env.has("sentinel.json") is False
    env.clean()


@pytest.mark.parametrize("question, title", [
    ("x" * 100, "x" * 70),
    ("y" * 70, "y" * 70),
    ("short?\nsecond line\nthird", "short?"),
    ("é" * 90 + "\nrest", "é" * 70),
], ids=["long-line", "exactly-70", "first-line-only", "non-ascii-characters"])
def test_sc2_1_stop_title_is_the_first_line_cut_to_70_characters(env, question, title):
    rc, _, _ = env.main("stop", "--question", question)
    assert rc == 0
    assert [(c["title"], c["body"], c["label"]) for c in env.created] == [(title, question, "needs-ruling")]
    assert len(env.created[0]["title"]) <= 70


def test_sc2_1_stop_keeps_non_ascii_question_text_whole(env):
    question = "Soll die Größe «café» gelten? ✓ 日本語\nZweite Zeile: ñ ü"
    rc, out, _ = env.main("stop", "--question", question)
    assert rc == 0
    assert env.created[0]["title"] == "Soll die Größe «café» gelten? ✓ 日本語"
    assert env.created[0]["body"] == question
    assert json.loads(out)["issue"] == 172


@pytest.mark.parametrize("labels", [[], ["needs-ruling-old", "needs", "ruling"]],
                         ids=["no-labels", "near-misses-only"])
def test_sc2_1_stop_without_the_label_prints_its_line_to_stderr_and_writes_nothing(env, labels):
    env.labels = labels
    before = snapshot(env.tmp)
    rc, out, err = env.main("stop", "--question", "Which one?")
    assert rc == 1
    assert err == NO_LABEL + "\n"
    assert out == ""
    assert env.created == []
    assert env.gh_calls("issue", "create") == []
    assert snapshot(env.tmp) == before
    assert not env.has("waiting.json")


def test_sc2_1_stop_writes_nothing_when_the_issue_cannot_be_filed(env):
    env.create_rc = 1
    before = snapshot(env.tmp)
    rc, out, err = env.main("stop", "--question", "Which one?")
    assert rc == 1
    assert err == "session-loop: could not file the needs-ruling issue\n"
    assert out == ""
    assert snapshot(env.tmp) == before


def test_sc2_1_reply_closes_the_waiting_issue_and_removes_the_waiting_file(env):
    env.main("stop", "--question", "Which one?")
    env.now = NOW + dt.timedelta(minutes=20)
    rc, out, err = env.main("reply")
    assert (rc, out, err) == (0, "closed issue #172\n", "")
    assert env.closed == [{"number": "172", "comment": ANSWER}]
    assert not env.has("waiting.json")
    env.clean()


def test_sc2_1_reply_closes_the_issue_the_waiting_file_names(env):
    env.put("waiting.json", {"issue": 9041, "at": "2026-11-22T17:41:44",
                             "due": "2026-11-22T18:36:00", "cron": "36 18 22 11 *"})
    rc, out, _ = env.main("reply")
    assert rc == 0 and out == "closed issue #9041\n"
    assert env.closed == [{"number": "9041", "comment": ANSWER}]


def test_sc2_1_reply_with_no_stop_waiting_prints_its_line_and_calls_no_gh(env):
    before = snapshot(env.tmp)
    rc, out, err = env.main("reply")
    assert (rc, out, err) == (0, "no stop waiting\n", "")
    assert [c for c in env.calls if c[0] == "gh"] == []
    assert snapshot(env.tmp) == before


def test_sc2_1_reply_keeps_the_waiting_file_when_the_close_fails(env):
    env.main("stop", "--question", "Which one?")
    env.close_rc = 1
    rc, out, err = env.main("reply")
    assert rc == 1
    assert err == "session-loop: could not close issue #172\n"
    assert out == ""
    assert env.file("waiting.json")["issue"] == 172


def test_sc2_1_due_exits_3_with_no_stop_and_0_while_one_waits(env):
    assert env.main("due") == (3, "", "")
    env.main("stop", "--question", "Which one?")
    assert env.main("due") == (0, "", "")
    env.main("reply")
    assert env.main("due") == (3, "", "")


# -- SC1.2: the sentinel follows the push --------------------------------------------


def test_sc1_2_wrap_writes_the_continue_sentinel_after_the_push_check(env):
    env.put("loop.json", {"on": "2026-11-22T16:00:00"})
    rc, out, err = env.wrap("Next 31: session-loop-sidebar", step="4", task="none")
    assert (rc, out, err) == (0, "sentinel written: continue\n", "")
    assert env.file("sentinel.json") == {
        "kind": "continue", "position": "plan step 4, task none",
        "next": "Next 31: session-loop-sidebar", "head": HEAD, "at": "2026-11-22T17:41:44"}
    assert env.has("loop.json"), "a continue wrap leaves the loop on"
    remote_checks = [c for c in env.calls if c[0] == "git" and c[1] == "ls-remote"]
    assert remote_checks == [["git", "ls-remote", "origin", f"refs/heads/{BRANCH}"]]
    assert [seen for _, seen in env.sentinel_at_call] == [False] * len(env.calls)
    env.clean()


def test_sc1_2_wrap_position_names_the_plan_step_and_the_task(env):
    env.wrap("Next 7: x", step="12", task="t3")
    assert env.file("sentinel.json")["position"] == "plan step 12, task t3"


@pytest.mark.parametrize("state", ["no-remote-branch", "stale-remote-head", "detached-head"])
def test_sc1_2_wrap_refuses_when_its_commit_is_not_on_the_remote(env, state):
    if state == "no-remote-branch":
        env.remote = {}
    elif state == "stale-remote-head":
        env.remote = {BRANCH: OTHER}
    else:
        env.branch = ""
    for next_text in ("Next 31: x", "(none)"):
        before = snapshot(env.tmp)
        rc, out, err = env.wrap(next_text)
        assert rc == 1
        assert err == NOT_PUSHED + "\n"
        assert out == ""
        assert not env.has("sentinel.json")
        assert env.created == [], "a wrap that is refused files nothing"
        assert snapshot(env.tmp) == before
    env.clean()


def test_sc1_2_wrap_reads_only_its_own_branch_on_the_remote(env):
    env.remote = {BRANCH: HEAD, "other": OTHER}
    rc, _, _ = env.wrap()
    assert rc == 0
    assert env.file("sentinel.json")["head"] == HEAD


def test_sc1_2_sentinel_is_the_last_write_of_a_self_wrap(env):
    env.put("loop.json", {"on": "2026-11-22T16:00:00"})
    env.main("stop", "--question", "Which one?")
    rc, out, _ = env.wrap("Next 31: x", "--self", step="5", task="none")
    assert (rc, out) == (0, "sentinel written: self-wrap\n")
    assert env.removed_after_sentinel == []
    assert [seen for argv, seen in env.sentinel_at_call] == [False] * len(env.calls)
    assert sorted(p.name for p in env.dir.iterdir()) == ["sentinel.json"]
    assert env.file("sentinel.json")["kind"] == "self-wrap"


def test_sc1_2_self_wrap_leaves_the_waiting_issue_open(env):
    env.put("loop.json", {"on": "2026-11-22T16:00:00"})
    env.main("stop", "--question", "Which one?")
    env.wrap("Next 31: x", "--self")
    assert env.closed == []
    assert env.gh_calls("issue", "close") == []
    assert [i["number"] for i in env.open_issues] == [172]
    assert not env.has("waiting.json")
    assert not env.has("loop.json")
    env.clean()


def test_sc1_2_self_wrap_writes_the_position_next_and_head_it_was_given(env):
    env.wrap("Next 31: Läuft «schön» ✓", "--self", step="9", task="t2")
    assert env.file("sentinel.json") == {
        "kind": "self-wrap", "position": "plan step 9, task t2",
        "next": "Next 31: Läuft «schön» ✓", "head": HEAD, "at": "2026-11-22T17:41:44"}


# -- SC5.1: an empty Next files one pick issue ---------------------------------------


def test_sc5_1_empty_next_files_one_pick_issue_and_the_pick_sentinel(env):
    env.put("loop.json", {"on": "2026-11-22T16:00:00"})
    rc, out, err = env.wrap("(none)", step="6", task="none")
    assert (rc, out, err) == (0, "sentinel written: pick\n", "")
    assert [(c["title"], c["label"]) for c in env.created] == [(PICK, "needs-ruling")]
    assert env.created[0]["body"].strip() != ""
    assert env.file("sentinel.json") == {
        "kind": "pick", "position": "plan step 6, task none", "next": "(none)",
        "head": HEAD, "at": "2026-11-22T17:41:44"}
    assert not env.has("loop.json"), "a pick wrap ends the loop"
    assert env.removed_after_sentinel == []
    assert sorted(p.name for p in env.dir.iterdir()) == ["sentinel.json"]
    assert [seen for _, seen in env.sentinel_at_call] == [False] * len(env.calls)
    heads = [c[:3] for c in env.calls if c[0] == "gh"]
    assert heads.index(["gh", "issue", "list"]) < heads.index(["gh", "issue", "create"])
    env.clean()


def test_sc5_1_an_open_pick_issue_means_no_second_one(env):
    env.open_issues = [{"number": 40, "title": "Fix the Größe check ✓"}, {"number": 41, "title": PICK}]
    rc, out, _ = env.wrap("(none)")
    assert (rc, out) == (0, "sentinel written: pick\n")
    assert env.created == []
    assert env.gh_calls("issue", "create") == []
    assert env.file("sentinel.json")["kind"] == "pick"
    assert not env.has("loop.json")


def test_sc5_1_the_title_must_match_exactly_to_count_as_open(env):
    env.open_issues = [{"number": 40, "title": PICK + " now"}, {"number": 41, "title": "pick the next deliverable"}]
    env.wrap("(none)")
    assert [c["title"] for c in env.created] == [PICK]


def test_sc5_1_self_wrap_with_an_empty_next_files_the_one_pick_issue_and_stays_a_self_wrap(env):
    env.put("loop.json", {"on": "2026-11-22T16:00:00"})
    env.main("stop", "--question", "Which one?")
    rc, out, err = env.wrap("(none)", "--self", step="6", task="none")
    assert (rc, out, err) == (0, "sentinel written: self-wrap\n", "")
    assert [(c["title"], c["label"]) for c in env.created if c["number"] != 172] == [(PICK, "needs-ruling")]
    assert env.file("sentinel.json") == {
        "kind": "self-wrap", "position": "plan step 6, task none", "next": "(none)",
        "head": HEAD, "at": "2026-11-22T17:41:44"}
    assert env.closed == [] and env.gh_calls("issue", "close") == [], "no issue is closed"
    assert sorted(i["number"] for i in env.open_issues) == [172, 173]
    assert sorted(p.name for p in env.dir.iterdir()) == ["sentinel.json"]
    assert env.removed_after_sentinel == []
    assert [seen for _, seen in env.sentinel_at_call] == [False] * len(env.calls)
    # a second such wrap, with the pick issue now open, files no second one (SC5.1)
    (env.dir / "sentinel.json").unlink()
    rc, out, _ = env.wrap("(none)", "--self", step="6", task="none")
    assert (rc, out) == (0, "sentinel written: self-wrap\n")
    assert len([c for c in env.created if c["title"] == PICK]) == 1
    assert env.closed == []
    env.clean()


def test_sc5_1_a_wrap_with_a_next_files_no_pick_issue_and_keeps_the_loop_on(env):
    env.put("loop.json", {"on": "2026-11-22T16:00:00"})
    rc, _, _ = env.wrap("Next 30: l1-loop-files")
    assert rc == 0
    assert env.gh_calls("issue", "create") == [] and env.gh_calls("issue", "list") == []
    assert env.file("sentinel.json")["kind"] == "continue"
    assert env.has("loop.json")


# -- SC5.2: nothing outside the loop's folder, and Next stays as it was --------------


def test_sc5_2_an_empty_next_stays_empty_after_the_wrap(env):
    backlog = env.repo / "docs" / "backlog.md"
    before = backlog.read_bytes()
    env.wrap("(none)")
    assert backlog.read_bytes() == before
    assert env.file("sentinel.json")["next"] == "(none)"
    env.clean()


def test_sc5_2_every_command_writes_only_inside_the_loop_folder(env):
    before = snapshot(env.tmp, skip=env.dir)
    assert env.main("on")[0] == 0
    assert env.main("stop", "--question", "Which one?")[0] == 0
    assert env.main("due")[0] == 0
    assert env.main("reply")[0] == 0
    assert env.wrap("Next 31: x")[0] == 0
    assert env.main("stop", "--question", "Again?")[0] == 0
    assert env.wrap("(none)", "--self")[0] == 0
    assert env.main("off")[0] == 0
    assert env.dir.is_dir() and env.has("sentinel.json")
    assert snapshot(env.tmp, skip=env.dir) == before
    env.clean()


def test_sc5_2_the_loop_runs_no_git_command_that_writes(env):
    env.main("on")
    env.main("stop", "--question", "Which one?")
    env.wrap("(none)", "--self")
    env.main("reply")
    git_calls = {tuple(c[:2]) for c in env.calls if c[0] == "git"}
    assert git_calls  # it did read git
    assert git_calls <= {("git", "rev-parse"), ("git", "branch"), ("git", "ls-remote")}


# -- the timer's minute --------------------------------------------------------------


def test_timer_due_examples(env):
    timer_due = env.loop().timer_due
    assert timer_due(dt.datetime(2026, 11, 22, 17, 41, 44)) == dt.datetime(2026, 11, 22, 18, 36)
    assert timer_due(dt.datetime(2026, 11, 22, 12, 4, 59)) == dt.datetime(2026, 11, 22, 12, 59)
    assert timer_due(dt.datetime(2026, 11, 22, 12, 5, 0)) == dt.datetime(2026, 11, 22, 13, 1)
    assert timer_due(dt.datetime(2026, 11, 22, 12, 5, 30)) == dt.datetime(2026, 11, 22, 13, 1)
    assert timer_due(dt.datetime(2026, 11, 22, 12, 35, 10)) == dt.datetime(2026, 11, 22, 13, 31)
    assert timer_due(dt.datetime(2026, 12, 31, 23, 5, 0)) == dt.datetime(2027, 1, 1, 0, 1)


def seconds(start: dt.datetime, count: int, step: int = 1):
    return (start + dt.timedelta(seconds=n) for n in range(0, count, step))


def check_due(stop: dt.datetime, due: dt.datetime):
    gap = (due - stop).total_seconds()
    assert 54 * 60 <= gap <= 56 * 60, f"{stop}: due {due} is {gap} s away"
    assert due.minute not in (0, 30), f"{stop}: due {due} lands on :00 or :30"
    assert due.second == 0 and due.microsecond == 0, f"{stop}: due {due} is not cut to the minute"


# one ordinary day, the last hour of a month's last day, the last hour of a year's
# last day, and the last hour of a leap February's last day
DAY = dt.datetime(2026, 11, 22)
EDGES = [dt.datetime(2026, 11, 30, 23), dt.datetime(2026, 12, 31, 23), dt.datetime(2028, 2, 29, 23)]


def test_timer_property_every_second_of_an_ordinary_day(env):
    timer_due = env.loop().timer_due
    for stop in seconds(DAY, 86400):
        check_due(stop, timer_due(stop))


def test_timer_property_last_hour_of_a_month_and_of_a_year(env):
    timer_due = env.loop().timer_due
    for edge in EDGES:
        for stop in seconds(edge, 3600):
            check_due(stop, timer_due(stop))


def test_timer_property_the_printed_cron_names_the_due_minute_hour_day_and_month(env):
    stops = list(seconds(DAY, 86400, 61))
    stops += list(seconds(dt.datetime(2026, 11, 22, 12, 5), 60))   # due lands on :00
    stops += list(seconds(dt.datetime(2026, 11, 22, 12, 35), 60))  # due lands on :30
    for edge in EDGES:
        stops += list(seconds(edge, 3600, 13))
    stops += [dt.datetime(2026, 11, 30, 23, 59, 59), dt.datetime(2026, 12, 31, 23, 59, 59),
              dt.datetime(2028, 2, 29, 23, 5, 0), dt.datetime(2028, 2, 29, 23, 35, 0)]
    for stop in stops:
        env.now = stop
        waiting = env.dir / "waiting.json"
        if waiting.exists():
            waiting.unlink()
        rc, out, _ = env.main("stop", "--question", "Which one?")
        assert rc == 0, stop
        printed = json.loads(out)
        due = dt.datetime.fromisoformat(printed["due"])
        check_due(stop, due)
        assert printed["cron"] == f"{due.minute} {due.hour} {due.day} {due.month} *", stop
        assert env.file("waiting.json")["due"] == printed["due"]
        assert env.file("waiting.json")["cron"] == printed["cron"]
        assert env.file("waiting.json")["at"] == iso(stop)
    env.clean()


# -- the run seam --------------------------------------------------------------------


def test_run_seam_decodes_utf8_and_replaces_bad_bytes(env):
    run = env.load().run  # the real run, not the fake
    code = ("import sys; sys.stdout.buffer.write('café Größe ✓'.encode('utf-8') + b'\\xff!');"
            " sys.stderr.buffer.write('ñ'.encode('utf-8') + b'\\xfe'); sys.exit(3)")
    done = run([sys.executable, "-c", code])
    assert done.returncode == 3
    assert done.stdout == "café Größe ✓�!"
    assert done.stderr == "ñ�"


def test_run_seam_passes_each_argument_whole_with_no_shell(env):
    run = env.load().run
    tricky = ["a b", "c;d", "e|f", "g&&h", ">out", "/clear", "$HOME", "é ✓"]
    code = "import json, sys; sys.stdout.buffer.write(json.dumps(sys.argv[1:]).encode('ascii'))"
    done = run([sys.executable, "-c", code, *tricky])
    assert done.returncode == 0
    assert json.loads(done.stdout) == tricky


def test_run_seam_is_how_every_git_and_gh_call_runs(env):
    env.main("stop", "--question", "Which one?")
    env.wrap("(none)")
    env.main("reply")
    assert env.calls, "no call went through the run seam"
    assert {c[0] for c in env.calls} == {"git", "gh"}
    env.clean()


# -- the script as a subprocess: exit codes and lines through a real git folder ------


@pytest.fixture
def real_repo(tmp_path):
    repo = tmp_path / "real"
    repo.mkdir()
    done = subprocess.run(["git", "init", "-q", str(repo)], capture_output=True,
                          creationflags=NO_WINDOW)
    assert done.returncode == 0, "git init failed in the fixture"
    return repo


def script(repo, *args):
    done = subprocess.run([sys.executable, str(LOOP_PY), *args], cwd=repo, capture_output=True,
                          encoding="utf-8", errors="replace", creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


def test_script_on_off_and_due_through_a_real_git_folder(real_repo):
    folder = real_repo / ".git" / "sdlc-loop"
    assert script(real_repo, "due") == (3, "", "")
    assert script(real_repo, "on") == (0, ON_LINE + "\n", "")
    assert set(json.loads((folder / "loop.json").read_text(encoding="utf-8"))) == {"on"}
    (folder / "waiting.json").write_text(json.dumps({"issue": 5, "at": "x", "due": "y", "cron": "z"}),
                                         encoding="utf-8")
    assert script(real_repo, "due") == (0, "", "")
    assert script(real_repo, "off") == (0, OFF_LINE + "\n", "")
    assert not (folder / "loop.json").exists()
    assert script(real_repo, "off") == (0, OFF_LINE + "\n", "")
    outside = [p.name for p in real_repo.rglob("*") if p.relative_to(real_repo).parts[0] != ".git"]
    assert outside == [], "the script wrote outside the git folder"
