"""Loop rules suite (contract: session-loop, unit l4-loop-rules, checks SC2.2, SC2.3 and
SC3.1+SC3.3, and the unit's done_means).

`/sdlc loop on` turns the loop on; in a loop a session files its stop and sets its timer;
a reply continues the session; with no reply the session wraps itself; kit 0.23.0 ships.

What this file pins, each red on a tree with no l4 files:

* the flow `skills/sdlc/flows/loop.md`, read as text (the design's test kind for SC2.3): its
  six steps L1 to L6 (on, off, stop, reply, wrap, self-wrap), the commands each runs, the
  order of the stop's acts, the verbatim cron prompt and notice, a reply that deletes the
  timer and runs no wrap and writes no sentinel (SC2.2), a self-wrap that leaves the
  issue open for `/cairn status` (SC3.1, SC3.3), and closing messages (SC2.3);
* the route in `skills/sdlc/SKILL.md`;
* the SessionStart hook `hooks/loop_on.py`, run as a child process in a throwaway git
  repository, and its entry in `hooks/hooks.json`;
* the release: version 0.23.0 in both places, the changelog entry, the usage page's
  markers, one row each in `USAGE.md` and `docs/components.md`.

SC2.2 and SC3.1+SC3.3 are manual receipts in one live sitting (the design's Units table):
no test here can wait 54 or 55 minutes, so the tests above pin the rules the sitting reads.
No test calls `gh`, `herdr` or Claude.
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
FLOW = ROOT / "skills" / "sdlc" / "flows" / "loop.md"
SKILL = ROOT / "skills" / "sdlc" / "SKILL.md"
HOOK = ROOT / "hooks" / "loop_on.py"
HOOKS_JSON = ROOT / "hooks" / "hooks.json"
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "skills" / "sdlc" / "init.py"
CHANGELOG = ROOT / "CHANGELOG.md"
USAGE_PAGE = ROOT / "docs" / "usage" / "session-loop.md"
USAGE = ROOT / "USAGE.md"
COMPONENTS = ROOT / "docs" / "components.md"

LP = "python {skill-dir}/../../workflows/tools/loop.py"
CEILING = 12000  # the flow files' ceiling (design, constraints)
STEPS = [("L1", "ON"), ("L2", "OFF"), ("L3", "STOP"), ("L4", "REPLY"), ("L5", "WRAP"),
         ("L6", "SELF-WRAP")]
CRON_PROMPT = ("session-loop: no reply to issue #{n} in 55 minutes. Run loop.py due: "
               "on exit 0 self-wrap by flows/loop.md; on exit 3 do nothing.")
NOTICE = "Ruling needed (#{n}): {question, cut to 150 characters}"
HOOK_COMMAND = 'python "${CLAUDE_PLUGIN_ROOT}/hooks/loop_on.py"'


# --- reading the flow -----------------------------------------------------------------

def collapsed(text: str) -> str:
    return " ".join(text.split())


def flow_text() -> str:
    assert FLOW.is_file(), f"no flow file at {FLOW}"
    return FLOW.read_text(encoding="utf-8")


def instructions() -> str:
    text = flow_text()
    assert "<instructions>" in text and "</instructions>" in text, "no instructions block"
    return text.split("<instructions>", 1)[1].split("</instructions>", 1)[0]


def step(label: str) -> str:
    """The step `label` (L1 to L6), whitespace collapsed: from its line to the next step."""
    found = re.split(r"(?m)^(?=L\d+\. )", instructions())
    mine = [part for part in found if part.startswith(f"{label}. ")]
    assert len(mine) == 1, f"the flow has {len(mine)} steps labelled {label}"
    return collapsed(mine[0])


def code_spans(text: str) -> list[str]:
    return re.findall(r"`([^`\n]+)`", text)


# --- the flow's shape -----------------------------------------------------------------

def test_done_means_loop_md_is_a_promptlang_flow_file_with_purpose_and_instructions():
    text = flow_text()
    lines = text.split("\n")
    assert lines[0] == "---" and lines[1] == "name: sdlc-flow-loop"
    assert lines[2].startswith("description: ") and lines[3] == "---"
    assert set(re.findall(r"<([a-z][a-z0-9-]*)>", text)) == {"purpose", "instructions"}
    assert text.index("</purpose>") < text.index("<instructions>")


def test_done_means_loop_md_has_the_six_steps_in_order_each_led_by_its_name():
    labels = re.findall(r"(?m)^(L\d+)\. (\S+)", instructions())
    assert labels == STEPS


def test_constraint_loop_md_stays_under_the_flow_ceiling():
    assert len(flow_text()) < CEILING


def test_constraint_every_command_in_loop_md_is_one_segment():
    spans = [s for s in code_spans(flow_text()) if s.startswith("python ")]
    assert len(spans) >= 7, spans  # on, off, stop, reply, due, wrap, wrap --self
    for span in spans:
        assert span.startswith(LP + " "), span
        for bad in ("|", ";", "&&", ">", "<", "$("):
            assert bad not in span, f"{bad!r} in {span!r}"


def test_done_means_the_purpose_names_the_loop_file_and_the_sessionstart_line():
    text = flow_text()
    purpose = collapsed(text.split("<purpose>", 1)[1].split("</purpose>", 1)[0])
    assert "loop.json" in purpose
    assert "A session loop is on in this repo" in purpose
    for name in ("stop", "reply", "wrap", "self-wrap"):
        assert name in purpose, name


def test_loop_md_never_names_a_compact_restart_or_a_permissions_entry():
    text = flow_text().lower()
    assert "/compact" not in text
    assert "permissions" not in text


# --- done_means: `/sdlc loop on` turns the loop on --------------------------------------

def test_done_means_l1_runs_loop_py_on_and_shows_the_line_it_prints():
    text = step("L1")
    assert f"RUN `{LP} on`" in text
    assert re.search(r"SHOW [^.]*\bline\b", text), text
    assert " off`" not in text


def test_done_means_l2_runs_loop_py_off_and_shows_the_line_it_prints():
    text = step("L2")
    assert f"RUN `{LP} off`" in text
    assert re.search(r"SHOW [^.]*\bline\b", text), text
    assert f"{LP} on`" not in text


# --- done_means: in a loop a session files its stop and sets its timer ------------------

def test_done_means_l3_runs_stop_with_the_question_then_the_timer_then_the_notice_then_ends():
    text = step("L3")
    run = f'RUN `{LP} stop --question "{{question}}"`'
    assert run in text, text
    order = [text.index(run), text.index("CronCreate"), text.index("PushNotification"),
             text.index("END the turn on the question")]
    assert order == sorted(order), f"the acts stand out of order: {order}"


def test_done_means_l3_on_exit_1_shows_the_line_and_stops_as_an_ordinary_stop_before_any_timer():
    text = step("L3")
    said = "On exit 1, SHOW its line and STOP as an ordinary stop"
    assert said in text, text
    assert text.index(said) < text.index("CronCreate")
    assert text.index(said) > text.index(f"{LP} stop")


def test_done_means_l3_sets_a_one_shot_timer_at_the_printed_cron():
    text = step("L3")
    at = text.index("CronCreate")
    assert "one-shot" in text[at:at + 80]
    for held in ("{n}", "{due}", "{cron}"):
        assert held in text[:at], f"{held} is held before the timer is set"
    assert "{cron}" in text[at:], "the timer is set at the printed cron"


def test_done_means_l3_gives_the_timer_the_design_prompt_verbatim_with_the_issue_number():
    assert CRON_PROMPT in step("L3")


def test_done_means_l3_holds_the_job_id_the_timer_returns():
    text = step("L3")
    assert "{job}" in text
    assert text.index("{job}") > text.index("CronCreate")


def test_done_means_l3_sends_the_notice_verbatim_cut_to_150_characters():
    text = step("L3")
    assert NOTICE in text
    assert text.index(NOTICE) > text.index("PushNotification")
    assert text.index(NOTICE) < text.index("END the turn on the question")


def test_done_means_l3_runs_no_wrap_and_writes_no_sentinel():
    text = step("L3")
    assert f"{LP} wrap" not in text and f"{LP} reply" not in text
    assert "sentinel" not in text.lower() or "no sentinel" in text.lower()


# --- SC2.3: a stop ends on its question, a wrap's closing message asks nothing ----------

def test_sc2_3_l3_ends_the_turn_on_the_question_with_the_question_as_the_last_message():
    text = step("L3")
    for said in ("END the turn on the question", "the last message is the question",
                 "ends on `?`"):
        assert said in text, said
    assert text.index("END the turn on the question") > text.index(NOTICE)


def test_sc2_3_l5_closing_message_asks_nothing():
    text = step("L5")
    assert "closing message" in text
    assert "asks nothing" in text
    assert "holds no question" in text
    assert text.index(f"{LP} wrap") < text.index("closing message")


def test_sc2_3_l6_closing_message_asks_nothing():
    text = step("L6")
    assert "closing message" in text
    assert "asks nothing" in text
    assert "holds no question" in text


def test_sc2_3_only_l3_ends_on_a_question():
    for label in ("L1", "L2", "L4", "L5", "L6"):
        assert "ends on `?`" not in step(label), label
        assert "END the turn on the question" not in step(label), label


# --- done_means: the wrap's order, and Next --------------------------------------------

def test_done_means_l5_commits_then_pushes_then_reads_next_then_runs_the_wrap():
    text = step("L5").lower()
    wrap = f"{LP} wrap".lower()
    order = [text.index("commit"), text.index("push"), text.index("/cairn status"),
             text.index(wrap), text.index("closing message")]
    assert order == sorted(order) and len(set(order)) == 5, order


def test_done_means_l5_runs_the_wrap_with_the_step_the_task_and_next_and_no_self_flag():
    text = step("L5")
    run = f'RUN `{LP} wrap --plan-step {{step}} --task {{task}} --next "{{next}}"`'
    assert run in text, text
    assert "--self" not in text


def test_done_means_l5_passes_next_as_cairn_status_prints_it_and_names_no_deliverable():
    text = step("L5")
    assert "`(none)`" in text
    assert "/cairn status" in text
    assert "Do NOT name a deliverable" in text


# --- SC2.2: a reply continues the session -----------------------------------------------

def test_sc2_2_l4_reply_deletes_the_timer_then_closes_the_issue_then_goes_on():
    text = step("L4")
    delete = "CronDelete"
    run = f"RUN `{LP} reply`"
    assert delete in text and run in text, text
    assert "{job}" in text
    assert text.index(delete) < text.index(run) < text.index("then go on")


def test_sc2_2_l4_runs_no_wrap_and_writes_no_sentinel():
    text = step("L4")
    assert "Run no wrap and write no sentinel." in text
    assert f"{LP} wrap" not in text and f"{LP} due" not in text
    assert "--self" not in text


def test_sc2_2_l4_reads_the_reply_as_the_users_next_message_in_the_session_never_the_issue():
    text = step("L4")
    assert "next message" in text
    assert "in the session, never on the issue" in text


# --- SC3.1 and SC3.3: with no reply the session wraps itself ----------------------------

def test_sc3_1_l6_runs_due_and_self_wraps_on_exit_0_and_does_nothing_on_exit_3():
    text = step("L6")
    due = f"RUN `{LP} due`"
    assert due in text, text
    at = text.index(due)
    assert "exit 0" in text[at:] and "exit 3" in text[at:]
    assert text.index("exit 0") < text.index("exit 3")
    assert "exit 3 do nothing" in text.replace(":", "").replace(",", "")
    assert text.index("exit 0") < text.index(f"{LP} wrap")


def test_sc3_1_l6_the_self_wrap_is_the_wrap_with_the_self_flag_and_the_same_order():
    text = step("L6")
    run = f'RUN `{LP} wrap --plan-step {{step}} --task {{task}} --next "{{next}}" --self`'
    assert run in text, text
    lowered = text.lower()
    order = [lowered.index("commit"), lowered.index("push"), lowered.index("/cairn status"),
             lowered.index(run.lower())]
    assert order == sorted(order) and len(set(order)) == 4, order


def test_sc3_3_l6_leaves_the_needs_ruling_issue_open_for_cairn_status():
    text = step("L6")
    assert "stays open" in text
    assert "Waiting on you" in text
    assert f"RUN `{LP} reply`" not in text
    assert "CronDelete" not in text


def test_sc3_1_l6_names_the_cron_prompt_as_what_starts_it():
    text = step("L6")
    assert "session-loop: no reply to issue" in text
    assert "the loop stays stopped" in text


# --- SKILL.md routes `/sdlc loop on|off` -----------------------------------------------

def skill_lines() -> list[str]:
    return SKILL.read_text(encoding="utf-8").split("\n")


def test_done_means_skill_md_dispatches_loop_to_its_flow_file_inside_step_0():
    lines = skill_lines()
    start = next(n for n, line in enumerate(lines) if line.startswith("0. DISPATCH."))
    end = next(n for n, line in enumerate(lines) if line.startswith("1. EXECUTE"))
    found = [n for n, line in enumerate(lines)
             if line.startswith("   - `loop` - LOAD {skill-dir}/flows/loop.md and EXECUTE "
                                "the Loop flow (L1-L6)")]
    assert len(found) == 1 and start < found[0] < end, found
    line = lines[found[0]]
    assert "`on`" in line and "`off`" in line


def test_done_means_skill_md_lists_loop_md_among_the_flows_beside_it():
    text = "\n".join(skill_lines())
    context = collapsed(text.split("<context>", 1)[1].split("</context>", 1)[0])
    listed = context.split("one PromptLang file per subcommand (ADR 0025): ", 1)[1]
    listed = collapsed(listed.split(" This file dispatches", 1)[0])
    names = [name.strip(" .") for name in listed.split(",")]
    assert sorted(names) == sorted(["init.md", "new.md", "intake.md", "vocab.md", "lang.md",
                                    "audit.md", "update.md", "g1.md", "execute.md",
                                    "restart.md", "loop.md"])


def test_done_means_skill_md_holds_one_criterion_for_the_loop_flow():
    found = [line for line in skill_lines() if line.startswith("- [ ] Loop flow:")]
    assert len(found) == 1, found
    assert "loop.py" in found[0] and "/sdlc loop" in found[0]


# --- the SessionStart hook --------------------------------------------------------------

def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def make_repo(base: Path, name: str = "repo") -> Path:
    repo = base / name
    done = subprocess.run(["git", "init", "-q", str(repo)], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=clean_env())
    assert done.returncode == 0, done.stderr
    return repo


def turn_on(repo: Path, content: str = '{"on": "2026-11-22T17:44:02"}') -> Path:
    folder = repo / ".git" / "sdlc-loop"
    folder.mkdir(exist_ok=True)
    (folder / "loop.json").write_text(content, encoding="utf-8")
    return folder / "loop.json"


def event(cwd: Path) -> str:
    return json.dumps({"session_id": "s-1", "transcript_path": "", "cwd": str(cwd),
                       "hook_event_name": "SessionStart", "source": "startup"})


def run_hook(stdin: str, process_cwd: Path) -> subprocess.CompletedProcess:
    assert HOOK.is_file(), f"no plugin hook at {HOOK}"
    return subprocess.run([sys.executable, str(HOOK)], input=stdin, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          cwd=str(process_cwd), env=clean_env(), timeout=60)


def hook_line() -> str:
    plugin = HOOK.resolve().parents[1].as_posix()
    return (f"A session loop is on in this repo: follow {plugin}/skills/sdlc/flows/loop.md "
            "at every stop and wrap.")


def snapshot(base: Path) -> dict:
    return {p.relative_to(base).as_posix(): (None if p.is_dir() else p.read_bytes())
            for p in sorted(base.rglob("*"))}


def test_done_means_the_hook_tells_a_fresh_session_the_loop_is_on(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    done = run_hook(event(repo), repo)
    assert done.returncode == 0 and done.stderr == ""
    assert done.stdout.splitlines() == [hook_line()]


def test_done_means_the_hook_reads_the_repo_of_the_events_cwd_not_the_process_cwd(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    done = run_hook(event(repo), elsewhere)
    assert done.returncode == 0 and done.stdout.splitlines() == [hook_line()]


def test_done_means_the_hook_finds_the_loop_from_a_folder_below_the_repo_root(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    below = repo / "src" / "pkg"
    below.mkdir(parents=True)
    done = run_hook(event(below), tmp_path)
    assert done.returncode == 0 and done.stdout.splitlines() == [hook_line()]


def test_done_means_the_loop_is_on_while_the_file_exists_whatever_it_holds(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo, "not json at all")
    done = run_hook(event(repo), repo)
    assert done.returncode == 0 and done.stdout.splitlines() == [hook_line()]


def test_done_means_the_hook_falls_back_to_the_process_cwd_when_the_event_is_unreadable(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    for stdin in ("", "not json", "{}", "[1, 2]"):
        done = run_hook(stdin, repo)
        assert done.returncode == 0 and done.stderr == "", stdin
        assert done.stdout.splitlines() == [hook_line()], stdin


def test_done_means_the_hook_prints_nothing_with_no_loop_file(tmp_path):
    repo = make_repo(tmp_path)
    assert run_hook(event(repo), repo).stdout == ""
    (repo / ".git" / "sdlc-loop").mkdir()
    done = run_hook(event(repo), repo)
    assert done.returncode == 0 and done.stdout == "" and done.stderr == ""


def test_done_means_the_hook_prints_nothing_outside_a_git_repository(tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    done = run_hook(event(plain), plain)
    assert done.returncode == 0 and done.stdout == "" and done.stderr == ""


def test_done_means_the_hook_prints_nothing_once_the_loop_file_is_gone(tmp_path):
    repo = make_repo(tmp_path)
    path = turn_on(repo)
    assert run_hook(event(repo), repo).stdout.splitlines() == [hook_line()]
    path.unlink()
    assert run_hook(event(repo), repo).stdout == ""


def test_done_means_the_hook_writes_nothing(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    before = snapshot(tmp_path)
    run_hook(event(repo), repo)
    assert snapshot(tmp_path) == before


def test_constraint_the_hook_imports_only_the_standard_library():
    assert HOOK.is_file(), f"no plugin hook at {HOOK}"
    tree = ast.parse(HOOK.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    assert names <= set(sys.stdlib_module_names), names - set(sys.stdlib_module_names)


def test_done_means_hooks_json_runs_the_hook_on_session_start_with_no_matcher():
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    assert hooks["hooks"].get("SessionStart") == [
        {"hooks": [{"type": "command", "command": HOOK_COMMAND}]}]
    assert "permissions" not in hooks  # non-goal: the loop adds no `permissions` entry


# --- done_means: kit 0.23.0 ships -------------------------------------------------------

def version_of(path: Path, pattern: str) -> tuple[int, ...]:
    found = re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE)
    assert found, f"no version in {path.name}"
    return tuple(int(part) for part in found.group(1).split("."))


def test_done_means_the_kit_version_reads_0_23_0_or_later_and_both_places_agree():
    # a floor, never the literal: the next release moves both numbers
    project = version_of(PYPROJECT, r'^version\s*=\s*"(\d+\.\d+\.\d+)"')
    kit = version_of(INIT, r'^KIT_VERSION\s*=\s*"(\d+\.\d+\.\d+)"')
    assert project >= (0, 23, 0)
    assert kit == project


def entry_of_0_23_0() -> str:
    text = CHANGELOG.read_text(encoding="utf-8")
    headings = [line.rstrip() for line in text.splitlines() if line.startswith("## ")]
    mine = [h for h in headings if h.startswith("## 0.23.0 - ")]
    assert len(mine) == 1, "no entry heads 0.23.0, or two do"
    assert re.fullmatch(r"## 0\.23\.0 - \d{4}-\d{2}-\d{2} \(tag `v0\.23\.0`\)", mine[0]), mine[0]
    after = text.split(mine[0], 1)[1]
    return " ".join(after.split("\n## ", 1)[0].split())


def test_done_means_the_changelog_holds_a_dated_0_23_0_entry_above_0_22_2():
    entry_of_0_23_0()
    headings = [line.rstrip() for line in CHANGELOG.read_text(encoding="utf-8").splitlines()
                if line.startswith("## ")]
    new = [n for n, h in enumerate(headings) if h.startswith("## 0.23.0 - ")]
    old = [n for n, h in enumerate(headings) if h.startswith("## 0.22.2 - ")]
    assert new and old and new[0] < old[0]


def test_done_means_the_changelog_entry_names_the_contract_the_four_units_and_the_versions():
    entry = entry_of_0_23_0()
    assert "`session-loop`" in entry
    for unit in ("l1-loop-files", "l2-loop-launcher", "l3-loop-stops", "l4-loop-rules"):
        assert f"`{unit}`" in entry, unit
    assert "`0.22.2` -> `0.23.0`" in entry
    assert "`1.5.0`" in entry


def test_done_means_the_changelog_entry_names_the_command_the_hook_the_launcher_and_the_label():
    entry = entry_of_0_23_0()
    assert "`/sdlc loop on`" in entry
    assert "`SessionStart`" in entry
    assert "`herdr/herdr_loop.py`" in entry
    assert "`gh label create needs-ruling`" in entry
    assert entry.count("Delta note") >= 1


# --- the docs ---------------------------------------------------------------------------

def test_done_means_the_usage_page_has_no_not_built_marker_left():
    text = USAGE_PAGE.read_text(encoding="utf-8")
    assert "🔴" not in text
    assert "Not shipped" not in text


def test_done_means_the_usage_page_carries_built_or_shipped_markers_and_keeps_its_lines():
    text = USAGE_PAGE.read_text(encoding="utf-8")
    first = text.split("\n", 1)[0]
    assert first.startswith("### The session loop: `/sdlc loop on`")
    assert first.rstrip().endswith(("🟡", "🟢")), first
    for lead in ("On and off.", "A fresh session knows.", "A stop that needs you.",
                 "Your reply.", "No reply."):
        assert re.search(rf"(🟢|🟡) \*\*{re.escape(lead)}\*\*", text), lead
    # the page still shows the command and the hook's line, word for word
    plain = collapsed(text)
    assert "> /sdlc loop on session loop on; a launcher may now restart this repo's sessions" \
        in plain
    assert ("A session loop is on in this repo: follow {plugin}/skills/sdlc/flows/loop.md "
            "at every stop and wrap.") in plain


def test_done_means_usage_md_links_the_session_loop_page_in_one_row():
    rows = [line for line in USAGE.read_text(encoding="utf-8").splitlines()
            if line.startswith("|") and "(docs/usage/session-loop.md)" in line]
    assert len(rows) == 1, rows
    assert "[The session loop](docs/usage/session-loop.md)" in rows[0]
    assert "/sdlc loop on" in rows[0]


def test_done_means_components_md_holds_one_session_loop_row_with_the_three_files():
    rows = [line for line in COMPONENTS.read_text(encoding="utf-8").splitlines()
            if line.startswith("| session loop |")]
    assert len(rows) == 1, rows
    row = rows[0]
    for piece in ("`workflows/tools/loop.py`", "`hooks/loop_on.py`", "`herdr/herdr_loop.py`",
                  "/sdlc loop on", "implemented (v1)", "[docs/usage/session-loop.md]"
                  "(usage/session-loop.md)"):
        assert piece in row, piece
