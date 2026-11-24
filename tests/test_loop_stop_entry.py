"""Stop-entry fix suite (contract: session-loop, unit l4-loop-rules, fix round on design r17).

The design's r17 (revision rows r17 to r20) answers session 177's live failure: at a
question, both loop sessions asked by an AskUserQuestion dialog and ran no `loop.py stop`.
l4's done_means sentence "In a loop, a session files its stop and sets its timer" now rests
on four things, each pinned here and each red on the tree before the fix:

* `hooks/loop_ask.py`, a PreToolUse hook, run as a child process in a throwaway git
  repository: it denies AskUserQuestion (exit 2, the reason on stderr) while
  `{git folder}/sdlc-loop/loop.json` exists, and else prints nothing and exits 0;
* its entry in `hooks/hooks.json`, beside the unchanged SessionStart and wall entries;
* the SessionStart line `hooks/loop_on.py` prints, now carrying the stop rule, the plain
  message ask and the `{plugin}` path of `loop.py`;
* `skills/sdlc/flows/loop.md`: every loop.py call runs as
  `python {plugin}/workflows/tools/loop.py ...`, no `{skill-dir}/../..` is left, the purpose
  says what `{plugin}` is and copies the new line, and L3 makes every question a stop that
  asks in a plain message and outranks a flow step that asks by a dialog (SC2.3);
* the docs that copy the line or list the files: the usage page, the components row, the
  changelog's 0.23.0 entry.

l4's other behavior stays pinned by tests/test_loop_rules.py. The live receipt (a fresh loop
pane, asked to ask a question with no nudge) is manual: no test calls `gh`, `herdr` or Claude.
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
FLOW = ROOT / "skills" / "sdlc" / "flows" / "loop.md"
ASK_HOOK = ROOT / "hooks" / "loop_ask.py"
START_HOOK = ROOT / "hooks" / "loop_on.py"
HOOKS_JSON = ROOT / "hooks" / "hooks.json"
CHANGELOG = ROOT / "CHANGELOG.md"
USAGE_PAGE = ROOT / "docs" / "usage" / "session-loop.md"
COMPONENTS = ROOT / "docs" / "components.md"

LP = "python {plugin}/workflows/tools/loop.py"
REASON = ("A session loop is on in this repo: this question is a stop. Run the stop rule (L3) "
          "in {plugin}/skills/sdlc/flows/loop.md, then ask in a plain message that ends on "
          "the question.")
LINE = ("A session loop is on in this repo, and the user may be away. Every question to the "
        "user is a stop: first run the stop rule (L3) in {plugin}/skills/sdlc/flows/loop.md, "
        "then ask in a plain message, never by AskUserQuestion. Follow the same file at every "
        "wrap. Run loop.py as python {plugin}/workflows/tools/loop.py.")
OLD_LINE = ("A session loop is on in this repo: follow {plugin}/skills/sdlc/flows/loop.md at "
            "every stop and wrap.")
ASK_COMMAND = 'python "${CLAUDE_PLUGIN_ROOT}/hooks/loop_ask.py"'
START_COMMAND = 'python "${CLAUDE_PLUGIN_ROOT}/hooks/loop_on.py"'
WALL_COMMAND = 'python "${CLAUDE_PLUGIN_ROOT}/hooks/wall.py"'


# --- reading the flow -----------------------------------------------------------------

def collapsed(text: str) -> str:
    return " ".join(text.split())


def flow_text() -> str:
    assert FLOW.is_file(), f"no flow file at {FLOW}"
    return FLOW.read_text(encoding="utf-8")


def purpose() -> str:
    text = flow_text()
    assert "<purpose>" in text and "</purpose>" in text, "no purpose block"
    return collapsed(text.split("<purpose>", 1)[1].split("</purpose>", 1)[0])


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


# --- running the hooks ----------------------------------------------------------------

def clean_env() -> dict:
    return {k: v for k, v in os.environ.items()
            if not k.startswith("GIT_") and k != "CLAUDE_PLUGIN_ROOT"}


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


def ask_event(cwd: Path, tool: str = "AskUserQuestion") -> str:
    return json.dumps({
        "session_id": "s-1", "transcript_path": "", "cwd": str(cwd),
        "permission_mode": "default", "hook_event_name": "PreToolUse", "tool_name": tool,
        "tool_input": {"questions": [{
            "question": "Should it be trial-note.md or trial-note.txt?", "header": "File",
            "multiSelect": False,
            "options": [{"label": "trial-note.md", "description": "Markdown"},
                        {"label": "trial-note.txt", "description": "Plain text"}]}]},
        "tool_use_id": "toolu_1"})


def start_event(cwd: Path) -> str:
    return json.dumps({"session_id": "s-1", "transcript_path": "", "cwd": str(cwd),
                       "hook_event_name": "SessionStart", "source": "startup"})


def run_script(script: Path, stdin: str, process_cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script)], input=stdin, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          cwd=str(process_cwd), env=clean_env(), timeout=60)


def run_ask(stdin: str, process_cwd: Path) -> subprocess.CompletedProcess:
    assert ASK_HOOK.is_file(), f"no deny hook at {ASK_HOOK}"
    return run_script(ASK_HOOK, stdin, process_cwd)


def run_start(stdin: str, process_cwd: Path) -> subprocess.CompletedProcess:
    assert START_HOOK.is_file(), f"no plugin hook at {START_HOOK}"
    return run_script(START_HOOK, stdin, process_cwd)


def plugin_of(hook: Path) -> str:
    return hook.resolve().parents[1].as_posix()


def reason() -> str:
    return REASON.replace("{plugin}", plugin_of(ASK_HOOK))


def line() -> str:
    return LINE.replace("{plugin}", plugin_of(START_HOOK))


def denied(done: subprocess.CompletedProcess) -> bool:
    return done.returncode == 2 and done.stdout == "" and done.stderr.splitlines() == [reason()]


def passed(done: subprocess.CompletedProcess) -> bool:
    return done.returncode == 0 and done.stdout == "" and done.stderr == ""


def snapshot(base: Path) -> dict:
    return {p.relative_to(base).as_posix(): (None if p.is_dir() else p.read_bytes())
            for p in sorted(base.rglob("*"))}


# --- the deny hook: while the loop is on ------------------------------------------------

def test_done_means_the_deny_hook_exits_2_with_the_reason_on_stderr_while_the_loop_is_on(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    done = run_ask(ask_event(repo), repo)
    assert done.returncode == 2, (done.returncode, done.stdout, done.stderr)
    assert done.stdout == ""
    assert done.stderr.splitlines() == [reason()]


def test_done_means_the_reason_names_the_kit_folder_in_forward_slashes(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    done = run_ask(ask_event(repo), repo)
    folder = plugin_of(ASK_HOOK)
    assert "\\" not in folder
    assert done.stderr.splitlines() == [reason()]
    assert f"{folder}/skills/sdlc/flows/loop.md" in done.stderr
    assert (Path(folder) / "skills" / "sdlc" / "flows" / "loop.md").is_file()


def test_done_means_the_deny_hook_reads_the_repo_of_the_events_cwd_not_the_process_cwd(tmp_path):
    on = make_repo(tmp_path, "on")
    turn_on(on)
    off = make_repo(tmp_path, "off")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert denied(run_ask(ask_event(on), elsewhere))
    assert denied(run_ask(ask_event(on), off))
    assert passed(run_ask(ask_event(off), on))


def test_done_means_the_deny_hook_finds_the_loop_from_a_folder_below_the_repo_root(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    below = repo / "src" / "pkg"
    below.mkdir(parents=True)
    assert denied(run_ask(ask_event(below), tmp_path))


def test_done_means_the_loop_is_on_while_the_file_exists_whatever_it_holds(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo, "not json at all")
    assert denied(run_ask(ask_event(repo), repo))


# --- the deny hook: every other case passes the call -----------------------------------

def test_done_means_the_deny_hook_prints_nothing_with_no_loop_file(tmp_path):
    repo = make_repo(tmp_path)
    assert passed(run_ask(ask_event(repo), repo))
    (repo / ".git" / "sdlc-loop").mkdir()
    assert passed(run_ask(ask_event(repo), repo))
    waiting = repo / ".git" / "sdlc-loop" / "waiting.json"
    waiting.write_text('{"issue": 172}', encoding="utf-8")
    assert passed(run_ask(ask_event(repo), repo))


def test_done_means_the_deny_hook_prints_nothing_outside_a_git_repository(tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    assert passed(run_ask(ask_event(plain), plain))


def test_done_means_the_deny_hook_lets_the_call_go_on_once_the_loop_file_is_gone(tmp_path):
    repo = make_repo(tmp_path)
    path = turn_on(repo)
    assert denied(run_ask(ask_event(repo), repo))
    path.unlink()
    assert passed(run_ask(ask_event(repo), repo))


def test_done_means_the_deny_hook_prints_nothing_on_an_unreadable_event_even_in_a_loop(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    assert denied(run_ask(ask_event(repo), repo))  # the loop is on, the event readable
    for stdin in ("", "not json", "\x00\x01", "{}", "[1, 2]", "null"):  # A: the user's, session 178
        done = run_ask(stdin, repo)
        assert passed(done), (stdin, done.returncode, done.stdout, done.stderr)


def test_constraint_the_deny_hook_denies_only_askuserquestion(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    assert denied(run_ask(ask_event(repo), repo))
    for tool in ("Bash", "Read", "Edit", "Write", "Grep", "AskUserQuestions"):
        done = run_ask(ask_event(repo, tool), repo)
        assert passed(done), (tool, done.returncode, done.stdout, done.stderr)


def test_done_means_the_deny_hook_writes_nothing(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    before = snapshot(tmp_path)
    assert denied(run_ask(ask_event(repo), repo))
    assert snapshot(tmp_path) == before
    path = repo / ".git" / "sdlc-loop" / "loop.json"
    path.unlink()
    before = snapshot(tmp_path)
    assert passed(run_ask(ask_event(repo), repo))
    assert snapshot(tmp_path) == before


def test_constraint_the_deny_hook_imports_only_the_standard_library():
    assert ASK_HOOK.is_file(), f"no deny hook at {ASK_HOOK}"
    tree = ast.parse(ASK_HOOK.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    assert names <= set(sys.stdlib_module_names), names - set(sys.stdlib_module_names)


# --- hooks.json -------------------------------------------------------------------------

def test_done_means_hooks_json_runs_the_deny_hook_on_askuserquestion_and_keeps_the_others():
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    pre = hooks["hooks"].get("PreToolUse")
    assert isinstance(pre, list) and len(pre) == 2, pre
    assert pre[0]["hooks"] == [{"type": "command", "command": WALL_COMMAND}]  # the wall, first
    assert pre[1] == {"matcher": "AskUserQuestion",
                      "hooks": [{"type": "command", "command": ASK_COMMAND}]}
    assert hooks["hooks"].get("SessionStart") == [
        {"hooks": [{"type": "command", "command": START_COMMAND}]}]
    assert set(hooks["hooks"]) == {"PreToolUse", "PostToolUse", "UserPromptSubmit",
                                   "SessionStart"}
    assert "permissions" not in hooks  # non-goal: the loop adds no `permissions` entry


# --- the SessionStart line --------------------------------------------------------------

def test_done_means_the_sessionstart_line_carries_the_stop_rule_and_the_plugin_path(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    done = run_start(start_event(repo), repo)
    assert done.returncode == 0 and done.stderr == ""
    assert done.stdout.splitlines() == [line()]


def test_done_means_the_sessionstart_line_names_a_loop_py_and_a_flow_that_exist(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    printed = run_start(start_event(repo), repo).stdout
    folder = plugin_of(START_HOOK)
    assert f"python {folder}/workflows/tools/loop.py" in printed, printed
    assert (Path(folder) / "workflows" / "tools" / "loop.py").is_file()
    assert (Path(folder) / "skills" / "sdlc" / "flows" / "loop.md").is_file()


def test_done_means_the_sessionstart_line_no_longer_says_only_follow_the_flow(tmp_path):
    repo = make_repo(tmp_path)
    turn_on(repo)
    printed = run_start(start_event(repo), repo).stdout
    assert printed.splitlines() == [line()]
    assert OLD_LINE.replace("{plugin}", plugin_of(START_HOOK)) not in printed


# --- loop.md: the path ------------------------------------------------------------------

def test_done_means_every_loop_py_call_in_loop_md_runs_from_the_plugin_folder():
    spans = [s for s in code_spans(flow_text()) if s.startswith("python ")]
    assert len(spans) >= 7, spans  # on, off, stop, reply, due, wrap, wrap --self
    for span in spans:
        assert span.startswith(LP + " "), span
    in_steps = re.findall(r"\S*workflows/tools/loop\.py", instructions())
    assert len(in_steps) >= 7, in_steps
    assert set(in_steps) == {"{plugin}/workflows/tools/loop.py"}, set(in_steps)


def test_done_means_loop_md_holds_no_skill_dir_path_to_the_kit():
    text = flow_text()
    assert FLOW.is_file()
    assert "{skill-dir}/../.." not in text
    assert "{plugin}/workflows/tools/loop.py" in text


def test_done_means_the_purpose_says_what_plugin_is():
    text = purpose()
    assert "{plugin} is the kit's folder in forward slashes" in text, text
    assert "names it in full" in text, text
    assert "two folders above the folder holding SKILL.md" in text, text
    assert "/sdlc loop on" in text


def test_done_means_the_purpose_copies_the_sessionstart_line_in_full():
    text = purpose()
    assert collapsed(LINE) in text, text
    assert collapsed(OLD_LINE) not in text


# --- loop.md: L3, the stop rule ---------------------------------------------------------

def test_done_means_l3_says_every_question_to_the_user_while_the_loop_is_on_is_this_stop():
    text = step("L3")
    assert "Every question to the user while the loop is on is this stop." in text, text


def test_done_means_l3_runs_loop_py_stop_before_asking():
    text = step("L3")
    run = f'RUN `{LP} stop --question "{{question}}"` before asking'
    assert run in text, text
    assert text.index(run) < text.index("CronCreate")


def test_sc2_3_l3_asks_in_a_plain_message_never_by_askuserquestion():
    text = step("L3")
    said = ("Ask the question in a plain message, never by AskUserQuestion: a dialog that "
            "waits is no idle session, so the timer's prompt never lands.")
    assert said in text, text
    assert text.index(said) > text.index(f"{LP} stop")
    assert "END the turn on the question" in text  # the stop still ends on its question


def test_done_means_l3_outranks_a_flow_step_that_asks_by_askuserquestion():
    text = step("L3")
    said = "This rule outranks a flow step that asks by AskUserQuestion (`init`, `intake`)."
    assert said in text, text


# --- the docs ---------------------------------------------------------------------------

def test_done_means_the_usage_page_shows_the_new_sessionstart_line():
    plain = collapsed(USAGE_PAGE.read_text(encoding="utf-8"))
    assert collapsed(LINE) in plain
    assert collapsed(OLD_LINE) not in plain


def test_done_means_components_md_names_the_deny_hook_in_the_session_loop_row():
    rows = [r for r in COMPONENTS.read_text(encoding="utf-8").splitlines()
            if r.startswith("| session loop |")]
    assert len(rows) == 1, rows
    for piece in ("`hooks/loop_ask.py`", "`hooks/loop_on.py`"):
        assert piece in rows[0], piece


def entry_of_0_23_0() -> str:
    text = CHANGELOG.read_text(encoding="utf-8")
    headings = [h.rstrip() for h in text.splitlines() if h.startswith("## ")]
    mine = [h for h in headings if h.startswith("## 0.23.0 - ")]
    assert len(mine) == 1, "no entry heads 0.23.0, or two do"
    after = text.split(mine[0], 1)[1]
    return " ".join(after.split("\n## ", 1)[0].split())


def test_done_means_the_changelog_entry_names_the_deny_hook_and_its_entry():
    entry = entry_of_0_23_0()
    assert "`hooks/loop_ask.py`" in entry
    assert "`AskUserQuestion`" in entry
    assert "`PreToolUse`" in entry
    assert "`hooks/loop_on.py`" in entry
    assert "`SessionStart`" in entry
