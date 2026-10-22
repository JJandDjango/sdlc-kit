"""Session-size suite (contract: small-session-flow, unit w1-session-size).

SC3.1 reads `CONTRIBUTING.md` and `docs/conventions/standing-practice.md`.
SC3.2 and SC3.3 run the plugin hook `hooks/context_size.py` as a child
process, the way Claude Code runs it: the event on stdin, a fixture
transcript in tmp_path, and TMP, TEMP and TMPDIR pointed at a tmp_path
folder, so the hook's once-a-session markers never touch the real temp
directory and each test starts with none.

The repository root is found through the `taskcontract` package, never
through this file's own location, so a run against a prototype reads the
prototype's pages and hook.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

import taskcontract

ROOT = Path(taskcontract.__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "context_size.py"
HOOKS_JSON = ROOT / "hooks" / "hooks.json"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
STANDING_PRACTICE = ROOT / "docs" / "conventions" / "standing-practice.md"

TARGET_MESSAGE = ("This session has passed 200K tokens, the target. "
                  "Finish the deliverable and close.")
LIMIT_MESSAGE = ("This session has passed 400K tokens, the limit. "
                 "Save the notes and close now.")
SESSION_SENTENCE = ("A session ships one deliverable. "
                    "Its context targets 200K tokens and stops at 400K.")
COMMAND = 'python "${CLAUDE_PLUGIN_ROOT}/hooks/context_size.py"'


# --- fixture transcripts, in the line shapes Claude Code writes ---

def assistant(input_tokens=0, cache_write=0, cache_read=0, *, sidechain=False,
              usage=None, sidechain_key=True) -> dict:
    """One assistant line; `usage` replaces the three counts when given."""
    if usage is None:
        usage = {"input_tokens": input_tokens,
                 "cache_creation_input_tokens": cache_write,
                 "cache_read_input_tokens": cache_read,
                 "output_tokens": 244}
    line = {"type": "assistant", "uuid": "a-1", "sessionId": "s",
            "message": {"role": "assistant", "model": "claude-haiku-5-5",
                        "content": [{"type": "text", "text": "ok"}],
                        "usage": usage}}
    if sidechain_key:
        line["isSidechain"] = sidechain
    return line


def sized(total: int, **kwargs) -> dict:
    """An assistant line whose three counts sum to `total`, spread over all three."""
    write = total // 3
    return assistant(7, write, total - 7 - write, **kwargs)


def user(text="go") -> dict:
    return {"type": "user", "isSidechain": False,
            "message": {"role": "user", "content": text}}


TRAILING = [
    {"type": "last-prompt", "lastPrompt": "go", "sessionId": "s"},
    {"type": "cost-state", "costUSD": 0, "sessionId": "s"},
    {"type": "attachment", "isSidechain": False,
     "attachment": {"type": "hook_system_message", "content": "earlier",
                    "hookEvent": "PostToolUse"}},
    {"type": "atis-latch", "sessionId": "s"},
    {"type": "api-request-blob", "message": {"role": "user", "content": "go"}},
]


def write_transcript(path: Path, lines: list) -> Path:
    """Write dicts as JSON lines and bytes as given, as utf-8 bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = b""
    for line in lines:
        data += line if isinstance(line, bytes) else json.dumps(line).encode("utf-8") + b"\n"
    path.write_bytes(data)
    return path


class Kit:
    """A project with the workflow file, a transcript folder and a private temp folder."""

    def __init__(self, base: Path):
        self.base = base
        self.project = base / "project"
        (self.project / ".sdlc").mkdir(parents=True)
        (self.project / ".sdlc" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
        self.bare = base / "bare"
        self.bare.mkdir()
        self.temp = base / "temp"
        self.temp.mkdir()
        self.transcripts = base / "transcripts"
        self.transcripts.mkdir()
        self._count = 0

    def transcript(self, lines: list) -> Path:
        self._count += 1
        return write_transcript(self.transcripts / f"t{self._count}.jsonl", lines)

    def at(self, total: int) -> Path:
        """A transcript whose newest assistant line sums to `total`."""
        return self.transcript([user(), sized(1000), user(), sized(total), *TRAILING])

    def event(self, transcript, session_id="session-1", name="PostToolUse",
              cwd=None) -> dict:
        common = {"session_id": session_id, "transcript_path": str(transcript),
                  "cwd": str(cwd or self.project), "prompt_id": "p-1",
                  "permission_mode": "default"}
        if name == "UserPromptSubmit":
            return {**common, "hook_event_name": name, "prompt": "go on"}
        return {**common, "effort": {"level": "medium"}, "hook_event_name": name,
                "tool_name": "Bash", "tool_input": {"command": "ls"},
                "tool_response": {"stdout": "", "stderr": ""},
                "tool_use_id": "toolu_1", "duration_ms": 12}

    def run(self, transcript=None, session_id="session-1", name="PostToolUse",
            cwd=None, stdin=None, process_cwd=None) -> subprocess.CompletedProcess:
        assert HOOK.is_file(), f"no plugin hook at {HOOK}"
        if stdin is None:
            stdin = json.dumps(self.event(transcript, session_id, name, cwd))
        env = dict(os.environ)
        for key in ("TMP", "TEMP", "TMPDIR"):
            env[key] = str(self.temp)
        return subprocess.run(
            [sys.executable, str(HOOK)], input=stdin, capture_output=True,
            encoding="utf-8", errors="replace", cwd=process_cwd or self.project,
            env=env, timeout=60)


@pytest.fixture
def kit(tmp_path) -> Kit:
    return Kit(tmp_path)


def assert_message(result, text, event="PostToolUse"):
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip(), f"expected a message, got nothing; stderr: {result.stderr}"
    assert json.loads(result.stdout) == {
        "systemMessage": text,
        "hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def assert_silent(result):
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "", f"expected nothing, got {result.stdout!r}"


def files_under(folder: Path) -> dict:
    return {p.relative_to(folder).as_posix(): p.read_bytes()
            for p in folder.rglob("*") if p.is_file()}


def load_hook_module():
    assert HOOK.is_file(), f"no plugin hook at {HOOK}"
    spec = importlib.util.spec_from_file_location("context_size_under_test", HOOK)
    module = importlib.util.module_from_spec(spec)
    before = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # leave no __pycache__ beside the hook
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = before
    return module


# --- SC3.1: the session size is stated, and the 40% boundary stands ---

def test_sc3_1_contributing_states_one_deliverable_200k_target_and_400k_limit():
    assert SESSION_SENTENCE in CONTRIBUTING.read_text(encoding="utf-8")
    standing = " ".join(STANDING_PRACTICE.read_text(encoding="utf-8").split())
    assert "session boundary before 40% of the context" in standing


def test_sc3_1_contributing_numbers_match_the_hook_constants():
    module = load_hook_module()
    for name in ("TARGET", "LIMIT"):
        value = getattr(module, name, None)
        assert isinstance(value, int) and not isinstance(value, bool), name
    found = re.search(r"Its context targets (\d+)K tokens and stops at (\d+)K\.",
                      CONTRIBUTING.read_text(encoding="utf-8"))
    assert found, "CONTRIBUTING.md names no target and limit"
    assert int(found.group(1)) * 1000 == module.TARGET
    assert int(found.group(2)) * 1000 == module.LIMIT


# --- SC3.2: a warning past 200K ---

def test_sc3_2_past_200k_shows_the_target_warning_to_user_and_agent(kit):
    assert_message(kit.run(kit.at(250_000)), TARGET_MESSAGE)


def test_sc3_2_exactly_200k_shows_nothing_and_one_more_token_warns(kit):
    # output tokens are not context: a large count must not tip it over
    exact_line = assistant(usage={"input_tokens": 0, "cache_creation_input_tokens": 150_000,
                                  "cache_read_input_tokens": 50_000, "output_tokens": 9_000})
    exact = kit.transcript([user(), exact_line, *TRAILING])
    assert_silent(kit.run(exact, session_id="exact"))
    assert_message(kit.run(kit.at(200_001), session_id="one-more"), TARGET_MESSAGE)


@pytest.mark.parametrize("usage", [
    {"input_tokens": 200_001, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0},
    {"input_tokens": 0, "cache_creation_input_tokens": 200_001, "cache_read_input_tokens": 0},
    {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 200_001},
    {"input_tokens": 1, "cache_creation_input_tokens": 100_000, "cache_read_input_tokens": 100_000},
], ids=["input", "cache-write", "cache-read", "sum-of-three"])
def test_sc3_2_context_is_input_plus_cache_write_plus_cache_read(kit, usage):
    transcript = kit.transcript([user(), assistant(usage={**usage, "output_tokens": 5}),
                                 *TRAILING])
    assert_message(kit.run(transcript), TARGET_MESSAGE)


def test_sc3_2_a_missing_usage_field_counts_as_zero(kit):
    transcript = kit.transcript([user(), assistant(usage={"cache_read_input_tokens": 250_000}),
                                 *TRAILING])
    assert_message(kit.run(transcript), TARGET_MESSAGE)


def test_sc3_2_warning_shows_once_a_session_across_both_events(kit):
    assert_message(kit.run(kit.at(250_000), session_id="one"), TARGET_MESSAGE)
    assert_silent(kit.run(kit.at(260_000), session_id="one", name="UserPromptSubmit"))
    assert_silent(kit.run(kit.at(270_000), session_id="one"))
    assert_message(kit.run(kit.at(250_000), session_id="two", name="UserPromptSubmit"),
                   TARGET_MESSAGE, event="UserPromptSubmit")


def test_sc3_2_reads_the_newest_assistant_line_and_skips_the_lines_after_it(kit):
    transcript = kit.transcript([user(), sized(450_000), user(), sized(250_000),
                                 *TRAILING, user("next"), b"\n"])
    assert_message(kit.run(transcript), TARGET_MESSAGE)


def test_sc3_2_a_subagent_line_after_the_newest_main_line_is_skipped(kit):
    transcript = kit.transcript([user(), sized(250_000, sidechain_key=False),
                                 sized(450_000, sidechain=True), *TRAILING])
    assert_message(kit.run(transcript), TARGET_MESSAGE)


def test_sc3_2_an_unknown_hook_event_name_is_echoed(kit):
    assert_message(kit.run(kit.at(250_000), name="FutureEvent"), TARGET_MESSAGE,
                   event="FutureEvent")


# --- SC3.3: a notice to close past 400K ---

def test_sc3_3_past_400k_shows_the_close_notice(kit):
    assert_message(kit.run(kit.at(400_001), session_id="over"), LIMIT_MESSAGE)
    assert_message(kit.run(kit.at(400_000), session_id="at"), TARGET_MESSAGE)


def test_sc3_3_a_step_past_both_thresholds_shows_only_the_400k_notice(kit):
    assert_message(kit.run(kit.at(450_000), session_id="jump"), LIMIT_MESSAGE)
    assert_silent(kit.run(kit.at(250_000), session_id="jump"))
    assert_silent(kit.run(kit.at(450_000), session_id="jump", name="UserPromptSubmit"))


def test_sc3_3_after_the_200k_warning_the_400k_notice_still_shows_once(kit):
    assert_message(kit.run(kit.at(250_000), session_id="climb"), TARGET_MESSAGE)
    assert_message(kit.run(kit.at(450_000), session_id="climb", name="UserPromptSubmit"),
                   LIMIT_MESSAGE, event="UserPromptSubmit")
    assert_silent(kit.run(kit.at(460_000), session_id="climb"))
    assert_silent(kit.run(kit.at(250_000), session_id="climb"))


# --- constraint 8: silent where the repo holds no .sdlc/workflow.md ---

def test_constraint_8_silent_without_a_workflow_file_at_any_size(kit):
    (kit.bare / ".sdlc").mkdir()
    for total in (250_000, 450_000):
        # the stdin cwd decides, even when the process runs in a repo with the file
        assert_silent(kit.run(kit.at(total), session_id="quiet", cwd=kit.bare,
                              process_cwd=kit.project))
    # silence wrote no marker: the same session speaks once the stdin cwd has the file
    assert_message(kit.run(kit.at(450_000), session_id="quiet", cwd=kit.project,
                           process_cwd=kit.bare), LIMIT_MESSAGE)


# --- constraint 1: never blocks; on an error, prints nothing ---

@pytest.mark.parametrize("stdin", ["not json", "", "[1, 2]", '{"session_id": '],
                         ids=["text", "empty", "array", "truncated"])
def test_constraint_1_stdin_that_is_not_a_json_object_prints_nothing(kit, stdin):
    assert_silent(kit.run(stdin=stdin))
    assert_message(kit.run(kit.at(250_000), session_id="control"), TARGET_MESSAGE)


def test_constraint_1_a_missing_or_unreadable_transcript_prints_nothing(kit):
    assert_silent(kit.run(kit.transcripts / "absent.jsonl", session_id="t"))
    assert_silent(kit.run(kit.transcripts, session_id="t"))  # a folder, not a file
    event = kit.event(kit.at(250_000), session_id="t")
    del event["transcript_path"]
    assert_silent(kit.run(stdin=json.dumps(event)))
    assert_message(kit.run(kit.at(250_000), session_id="t"), TARGET_MESSAGE)


def test_constraint_1_a_transcript_with_no_main_assistant_line_prints_nothing(kit):
    assert_silent(kit.run(kit.transcript([]), session_id="t"))
    assert_silent(kit.run(kit.transcript([user(), *TRAILING]), session_id="t"))
    assert_silent(kit.run(kit.transcript([user(), sized(450_000, sidechain=True), *TRAILING]),
                          session_id="t"))
    assert_message(kit.run(kit.at(450_000), session_id="t"), LIMIT_MESSAGE)


def test_constraint_1_a_malformed_line_after_the_newest_assistant_line_prints_nothing(kit):
    lines = [user(), sized(250_000), *TRAILING]
    assert_silent(kit.run(kit.transcript([*lines, b'{"type": "last-prompt", "lastPro']),
                          session_id="t"))
    assert_message(kit.run(kit.transcript(lines), session_id="t"), TARGET_MESSAGE)


@pytest.mark.parametrize("bad", ["250000", None, [250_000]], ids=["string", "null", "list"])
def test_constraint_1_a_usage_value_that_is_not_an_integer_prints_nothing(kit, bad):
    line = assistant(usage={"input_tokens": 3, "cache_creation_input_tokens": bad,
                            "cache_read_input_tokens": 250_000})
    assert_silent(kit.run(kit.transcript([user(), line, *TRAILING]), session_id="t"))
    assert_message(kit.run(kit.at(250_000), session_id="t"), TARGET_MESSAGE)


# --- constraint 2: reading stops at the newest assistant line ---

def test_constraint_2_lines_before_the_newest_assistant_line_are_never_parsed(kit):
    transcript = kit.transcript([
        b"{not json at all\n",
        b"\xff\xfe\x80 not utf-8 \xc3\x28\n",
        sized(450_000),
        b'{"type": "assistant", "message": {"usage": \n',
        user(), sized(250_000), *TRAILING])
    assert_message(kit.run(transcript), TARGET_MESSAGE)


# --- constraint 3: nothing written but the markers in the temp directory ---

def test_constraint_3_writes_only_its_markers_in_the_temp_directory(kit):
    first, second = kit.at(450_000), kit.at(250_000)
    outside = {k: v for k, v in files_under(kit.base).items() if not k.startswith("temp/")}
    assert_message(kit.run(first, session_id="one"), LIMIT_MESSAGE)
    assert len(files_under(kit.temp)) == 2  # a marker for each threshold
    assert_message(kit.run(second, session_id="two", process_cwd=kit.bare), TARGET_MESSAGE)
    assert len(files_under(kit.temp)) == 3
    after = {k: v for k, v in files_under(kit.base).items() if not k.startswith("temp/")}
    assert after == outside


@pytest.mark.parametrize("session_id", ["../escape", "nested/id", "..\\escape", "a\\b"])
def test_constraint_3_a_session_id_with_path_characters_writes_no_file_outside_the_temp_directory(
        kit, session_id):
    transcript = kit.at(250_000)
    outside = {k: v for k, v in files_under(kit.base).items() if not k.startswith("temp/")}
    assert_message(kit.run(transcript, session_id=session_id), TARGET_MESSAGE)
    assert_silent(kit.run(transcript, session_id=session_id))
    after = {k: v for k, v in files_under(kit.base).items() if not k.startswith("temp/")}
    assert after == outside
    assert files_under(kit.temp)


# --- the plugin runs the hook on both events ---

def test_hooks_json_runs_the_hook_on_post_tool_use_and_user_prompt_submit():
    assert HOOKS_JSON.is_file(), f"no plugin hook file at {HOOKS_JSON}"
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]

    def commands(entry):
        return [(h.get("type"), h.get("command")) for h in entry.get("hooks", [])]

    post = [e for e in hooks.get("PostToolUse", []) if ("command", COMMAND) in commands(e)]
    assert [e.get("matcher") for e in post] == ["*"]
    prompt = [e for e in hooks.get("UserPromptSubmit", [])
              if ("command", COMMAND) in commands(e)]
    assert len(prompt) == 1 and "matcher" not in prompt[0]
