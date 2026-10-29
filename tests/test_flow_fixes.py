"""Fix round for unit e5-rounds of contract execution-team (reasons 14.1, 14.2,
14.3, 14.6, 15.2 and 15.5 of the last round; checks SC4.1, SC4.2, SC4.3, SC5.1
and SC5.2).

What moves: the Orchestrator's flow `skills/sdlc/flows/execute.md` (its
quoting, two held values, the join of the reasons and one close call),
`workflows/qa-verifier.js` (the argument `at` of prove-red) and
`workflows/dev-verifier.js` (two sections read only where the document has
them). `workflows/tools/task.py` keeps its commands and options (Design
Interfaces 10); `prove.py` keeps `--at REV` (Interfaces 7).

The flow is prose, so a test reads its text: the spans it shows in backticks,
and the sentences round them. Where a span can run, a test renders it (a
placeholder replaced, the line split as a POSIX shell splits it) and runs it
against a repository built under tmp_path, so the quoting is proved by what
reaches `task.py`, not by a pattern. The members run under node with a mock
`agent`, as tests/test_team.py runs them.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract

ROOT = Path(taskcontract.__file__).resolve().parents[1]
TASK_PY = ROOT / "workflows" / "tools" / "task.py"
PROVE_PY = ROOT / "workflows" / "tools" / "prove.py"
WORKFLOWS = ROOT / "workflows"
FLOW = ROOT / "skills" / "sdlc" / "flows" / "execute.md"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="node is not on PATH")

TASKPY = "python {skill-dir}/../../workflows/tools/task.py"
FAIL_SPAN = (f"{TASKPY} fail --unit {{contract}}/{{unit}} --task {{channel}} "
             "--reason '{reasons}'")
STOP_SPAN = (f"{TASKPY} stop --task {{task}} --operator {{operator}} "
             "--question '{question}'")
CLOSE_SPAN = "python -m taskcontract progress done {contract}/{unit}"
END_TWO_KEY = f"{TASKPY} end --unit {{contract}}/{{unit}} --task two-key"
QUOTE_FORM = "'\\''"  # the four characters ' \ ' ' the flow writes for one single quote
DEV_LINE = "Task two-key: Dev verifier, round 1: {verdict}"
# What a reason or a question may hold that a shell reads as more than text.
NASTY = "it's a \"quoted\" `echo x` $HOME $(id) \\n; done"

CONTRACT, U = "exec-fix", "u1-work"
UNIT = f"{CONTRACT}/{U}"
INTENT = ("A fixture contract for the flow fixes suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")
DESIGN_STOP = (
    "Task green failed 3 rounds. The run stops here; the failures follow.\n"
    "  Round 1: 2 sketches failed: SC5.1 (src/command_line.cpp:41), SC5.2 (src/command_line.cpp:58)\n"
    "  Round 2: 1 sketch failed: SC5.2 (src/command_line.cpp:58)\n"
    "  Round 3: 1 sketch failed: SC5.2 (src/command_line.cpp:60)\n")
DESIGN_QUESTION = ("Task green stopped on a question from Developer: "
                   "Which exit code does --frames 0 take?\n")


# --- the flow as text ---------------------------------------------------------------

def flow() -> str:
    assert FLOW.is_file(), "skills/sdlc/flows/execute.md is not written"
    return FLOW.read_text(encoding="utf-8")


def steps_of(text: str) -> dict[str, str]:
    """The flow's steps by label (E1 .. E9), each with its text."""
    block = re.search(r"<instructions>\n(.*?)</instructions>", text, re.DOTALL)
    assert block, "the flow's steps stand inside one instructions block"
    steps = {}
    for part in re.split(r"^(?=E\d+\. )", block[1], flags=re.MULTILINE):
        label = re.match(r"(E\d+)\. ", part)
        if label:
            steps[label[1]] = part
    return steps


def spans(text: str) -> list[tuple[int, str]]:
    """(offset, text) of each command the flow shows in backticks, in order."""
    return [(m.start(), m[1]) for m in re.finditer(r"`([^`\n]+)`", text)
            if m[1].startswith(("python ", "git ", "rm ", "gh "))]


def task_spans(text: str, verb: str) -> list[tuple[int, str]]:
    return [(at, c) for at, c in spans(text) if c.startswith(f"{TASKPY} {verb} ")
            or c == f"{TASKPY} {verb}"]


def reading(text: str, at: int, command: str) -> str:
    """What the flow says after a command: the text up to the next command span or
    the next blank line."""
    later = [o for o, _ in spans(text) if o > at]
    tail = text[at + len(command) + 2:(later[0] if later else len(text))]
    return tail.split("\n\n")[0]


def sentence_around(text: str, index: int) -> str:
    """The sentence of `text` that holds `index`: from the previous '. ' or line start
    to the next '. ' or line end."""
    start = max(text.rfind(". ", 0, index) + 2, text.rfind("\n", 0, index) + 1)
    ends = [e for e in (text.find(". ", index), text.find("\n", index)) if e != -1]
    return text[start:min(ends) if ends else len(text)]


def member_starts(step: str) -> list[tuple[str, str]]:
    """The members a step starts, in order: (plugin-name, text up to the next one)."""
    found = list(re.finditer(r"\{plugin\}:([a-z][a-z-]*)", step))
    return [(m[1], step[m.start():(found[i + 1].start() if i + 1 < len(found) else len(step))])
            for i, m in enumerate(found)]


def args_of(segment: str) -> str:
    found = re.search(r"args `([^`]*)`", segment)
    assert found, f"no args span after {segment[:40]!r}"
    return found[1]


# --- the scratch repository and task.py ------------------------------------------------

def _dump(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _unit(uid: str) -> dict:
    return {"unit": "work for " + uid, "id": uid, "confirmed_by": ["po"],
            "done_means": "the work for " + uid + " is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}


def _document(revision: int) -> str:
    def row(text, by="Ann Lee"):
        return f"| 2026-10-07 | {by} | {text} |\n"
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{CONTRACT}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return (f"# {CONTRACT} - A fixture feature\n\n"
            "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"
            + rows + ready + "\n## Statement\n\nWords.\n")


def make_repo(tmp_path: Path) -> Path:
    """<tmp>/repo: a declared test command, a ready contract with two units, a
    ratified seat roster, and a git repository."""
    root = tmp_path / "repo"
    root.mkdir()
    (tmp_path / "cwd").mkdir()
    (root / ".sdlc").mkdir()
    (root / ".sdlc" / "config.yaml").write_text(
        "kit: fixture\ntest:\n  command: [test.bat]\n", encoding="utf-8")
    _dump(root / "specs" / CONTRACT / "contract.yaml", {
        "id": CONTRACT, "title": "A fixture feature", "intent": INTENT,
        "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
        "decomposition": [_unit(U), _unit("u2-more")], "dependencies": [], "entities": [],
        "provenance": {"origin": "human-request"}})
    (root / "docs" / "features").mkdir(parents=True)
    (root / "docs" / "features" / f"{CONTRACT}.md").write_text(_document(5), encoding="utf-8")
    (root / "docs" / "features" / f"{CONTRACT}.design.md").write_text(
        _document(4), encoding="utf-8")
    vocab = root / "specs" / "vocabulary"
    vocab.mkdir(parents=True, exist_ok=True)
    (vocab / "intake-seat.yaml").write_text(yaml.safe_dump({
        "term": "intake-seat", "name": "Intake seat",
        "definition": "A human position that answers for a decomposition unit at intake.",
        "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
        "since": "2026-08-26"}, sort_keys=False), encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True)
    return root


def env_for(tmp_path: Path) -> dict:
    return {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1"}


def call(tmp_path: Path, root: Path, *args: str):
    """(exit code, stdout, stderr) of `task.py ARGS --root ROOT`."""
    argv = [sys.executable, str(TASK_PY), *args, "--root", str(root)]
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env_for(tmp_path), capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100,
                          creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


def run_span(tmp_path: Path, root: Path, span: str, **values: str):
    """Run a task.py span of the flow as the Orchestrator would: each placeholder of
    `values` replaced, the line split as a POSIX shell splits it, the program resolved
    to this checkout's task.py. Returns (exit code, stdout, stderr)."""
    text = span
    for name, value in values.items():
        text = text.replace("{" + name + "}", value)
    tokens = shlex.split(text)
    assert tokens[0] == "python" and tokens[1].endswith("workflows/tools/task.py"), tokens[:2]
    return call(tmp_path, root, *tokens[2:])


def started(tmp_path, root, task, operator):
    assert call(tmp_path, root, "start", "--unit", UNIT, "--task", task,
                "--operator", operator)[0] == 0


def tree(tmp_path: Path, root: Path) -> str:
    done = subprocess.run([sys.executable, "-m", "taskcontract", "tree", "--root", str(root)],
                          cwd=tmp_path / "cwd", env=env_for(tmp_path), capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100,
                          creationflags=NO_WINDOW)
    assert done.returncode == 0, done.stderr
    return done.stdout


def tree_line(text: str, node: str) -> str:
    found = [line for line in text.split("\n") if line.strip().startswith(node + " ")]
    assert len(found) == 1, (node, found)
    return found[0]


# --- the members under node ------------------------------------------------------------

HARNESS = r"""
const fs = require('fs')
const [file, cfg] = process.argv.slice(2)
const { args, responses } = JSON.parse(fs.readFileSync(cfg, 'utf8'))
const src = fs.readFileSync(file, 'utf8').replace(/^export const meta/m, 'const meta')
const calls = []
const logs = []
let next = 0
const agent = async (prompt, opts) => {
  calls.push({ prompt, opts })
  return next < responses.length ? responses[next++] : null
}
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const run = new AsyncFunction('args', 'agent', 'log', 'phase', src)
run(args, agent, m => logs.push(String(m)), () => {})
  .then(result => console.log(JSON.stringify({ result: result === undefined ? null : result, calls, logs })))
  .catch(err => console.log(JSON.stringify({ thrown: String((err && err.stack) || err) })))
"""

BASE = {"model": "m-from-args", "effort": "e-from-args", "unit": "u1", "contract": "contract-1",
        "repo": "/r"}
TEST_FILE = "tests/run_x.bat"
VERIFIER = {**BASE, "scratch": "/s", "pluginRoot": "/p", "testFile": TEST_FILE}
PROVE_RED_REPLY = {"command": "prove", "exit_code": 0, "output": "{}", "red_summary": "2 failed"}
MUTANTS = [{"name": f"m{i}", "behavior": f"behavior {i}", "applied": True, "caught": True}
           for i in range(1, 5)]
TWO_KEY_REPLY = {"command": "prove", "exit_code": 0, "output": "{}", "mutations": MUTANTS}
RECEIPTS_OK = {"ok": True, "commands": [{"command": ["run-all.bat"], "exit_code": 0}]}
GRADE_OK = {
    "commit_checked": "abc1234", "files_in_commit": ["src/a.cpp"],
    "trailers": {"contract_trailer": "Contract: contract-1", "theory_trailer_present": True},
    "every_path_inside_scope_or_free": True,
    "sketches": [{"sketch": "s1", "verdict": "PASS", "evidence": "src/a.cpp:1"}],
    "done_means_held": True, "defects": [], "summary": "ok",
}


def run_member(tmp_path: Path, name: str, args: dict, responses=()) -> dict:
    """Run workflows/NAME.js under node with a mock agent; the harness's JSON:
    result, calls (prompt, opts) and logs."""
    file = WORKFLOWS / f"{name}.js"
    assert file.is_file(), f"workflows/{name}.js is not written"
    (tmp_path / "harness.js").write_text(HARNESS, encoding="utf-8")
    (tmp_path / "cfg.json").write_text(json.dumps({"args": args, "responses": list(responses)}),
                                       encoding="utf-8")
    done = subprocess.run([NODE, str(tmp_path / "harness.js"), str(file), str(tmp_path / "cfg.json")],
                          capture_output=True, encoding="utf-8", errors="replace", timeout=60,
                          creationflags=NO_WINDOW)
    assert done.returncode == 0, f"node failed: {done.stderr.strip()}"
    out = json.loads(done.stdout.strip().splitlines()[-1])
    assert "thrown" not in out, out["thrown"]
    return out


def prompt_of(tmp_path: Path, name: str, args: dict, reply: dict) -> str:
    return run_member(tmp_path, name, args, responses=[reply])["calls"][0]["prompt"]


# === 14.1: verifier text goes to the shell in single quotes ===============================

def test_14_1_the_flow_passes_the_reasons_and_the_question_in_single_quotes():
    text = flow()
    assert [c for _, c in task_spans(text, "fail")] == [FAIL_SPAN]
    assert [c for _, c in task_spans(text, "stop")] == [STOP_SPAN]
    assert '"{reasons}"' not in text and '"{question}"' not in text
    # One sentence of the rounds rule says how a single quote inside the value is written;
    # it comes before the fail command, so the stop command after it follows it too.
    e2 = steps_of(text)["E2"]
    assert f"`{QUOTE_FORM}`" in e2, "the rounds rule never shows the form of a single quote"
    at = e2.index(f"`{QUOTE_FORM}`")
    assert "single quote" in sentence_around(e2, at).lower()
    assert at < e2.index("`" + FAIL_SPAN + "`") < e2.index("`" + STOP_SPAN + "`")


def test_14_1_task_py_commands_and_options_stay_as_drawn():
    text = flow()
    drawn = {"start": {"--unit", "--task", "--operator"},
             "fail": {"--unit", "--task", "--reason"},
             "stop": {"--task", "--operator", "--question"},
             "end": {"--unit", "--task", "--by", "--run"}}
    used = {}
    for _, command in spans(text):
        if command.startswith(TASKPY + " "):
            verb = command[len(TASKPY) + 1:].split()[0]
            options = set(re.findall(r"(?<=\s)--[a-z-]+", command))
            assert options <= drawn[verb], (verb, options - drawn[verb])
            used.setdefault(verb, set()).update(options)
    assert set(used) == set(drawn)
    assert used["fail"] == drawn["fail"] and used["stop"] == drawn["stop"]
    # The drawn options still stand in the script itself.
    helped = subprocess.run([sys.executable, str(TASK_PY), "fail", "--help"], capture_output=True,
                            encoding="utf-8", errors="replace", timeout=60,
                            creationflags=NO_WINDOW).stdout
    assert all(option in helped for option in drawn["fail"])
    # The two values reach the script through single quotes, whatever they hold.
    assert [c for _, c in task_spans(text, "fail")][0].endswith("--reason '{reasons}'")
    assert [c for _, c in task_spans(text, "stop")][0].endswith("--question '{question}'")


def test_14_1_a_reason_with_shell_characters_reaches_the_stop_line_whole(tmp_path):
    text = flow()
    found = [c for _, c in task_spans(text, "fail")]
    assert found == [FAIL_SPAN], found
    form = re.search(r"`('\\'')`", steps_of(text)["E2"])
    assert form and form[1] == QUOTE_FORM
    value = NASTY.replace("'", form[1])
    root = make_repo(tmp_path)
    tokens = shlex.split(found[0].replace("{reasons}", value))
    assert tokens[-1] == NASTY, tokens
    codes = []
    for n in range(3):
        codes.append(run_span(tmp_path, root, found[0], contract=CONTRACT, unit=U,
                              channel="green", reasons=value))
    assert [c[0] for c in codes] == [0, 0, 1]
    assert codes[0][1] == "" and codes[1][1] == ""
    assert codes[2][1] == ("Task green failed 3 rounds. The run stops here; the failures follow.\n"
                           + (f"  Round 1: {NASTY}\n  Round 2: {NASTY}\n  Round 3: {NASTY}\n"))
    assert codes[2][2] == ""


def test_14_1_a_question_with_shell_characters_reaches_the_stop_line_whole(tmp_path):
    text = flow()
    found = [c for _, c in task_spans(text, "stop")]
    assert found == [STOP_SPAN], found
    form = re.search(r"`('\\'')`", steps_of(text)["E2"])
    assert form and form[1] == QUOTE_FORM
    value = NASTY.replace("'", form[1])
    root = make_repo(tmp_path)
    assert shlex.split(found[0].replace("{question}", value))[-1] == NASTY
    code, out, err = run_span(tmp_path, root, found[0], task="green", operator="developer",
                              question=value)
    assert (code, err) == (1, "")
    assert out == f"Task green stopped on a question from Developer: {NASTY}\n"


# === 14.2: prove-red runs at the base commit ==============================================

def test_14_2_the_flow_holds_the_base_commit_at_e2_and_passes_it_to_prove_red():
    text = flow()
    steps = steps_of(text)
    e2 = steps["E2"]
    hold = "`git rev-parse HEAD` as {base}"
    assert hold in e2, "E2 never holds {base}"
    assert [c for _, c in spans(text) if c == "git rev-parse HEAD"] == ["git rev-parse HEAD"]
    sentence = sentence_around(e2, e2.index(hold))
    for part in ("{repo}", "{gitdir}", "{branch}", "one Bash call"):
        assert part in sentence, (part, sentence)
    # Held before any task opens: no task.py start precedes it.
    assert text.index(hold) < min(at for at, _ in task_spans(text, "start"))
    # Only prove-red gets it, from the qa-verifier start of E5.
    starts = member_starts(steps["E5"])
    assert [n for n, _ in starts] == ["qa-verifier"]
    args = args_of(starts[0][1])
    assert '"at": "{base}"' in args and '"task": "prove-red"' in args, args


@needs_node
def test_14_2_prove_red_runs_prove_py_at_the_given_revision_and_at_no_other_when_none(tmp_path):
    given = prompt_of(tmp_path, "qa-verifier", {**VERIFIER, "task": "prove-red", "at": "9f8e7d6"},
                      PROVE_RED_REPLY)
    command = "python /p/workflows/tools/prove.py --scratch /s --test tests/run_x.bat --at 9f8e7d6"
    assert command in given
    assert given.count("--at") == 1
    assert "exports 9f8e7d6" in given and "exports HEAD" not in given
    none = prompt_of(tmp_path, "qa-verifier", {**VERIFIER, "task": "prove-red"}, PROVE_RED_REPLY)
    assert "python /p/workflows/tools/prove.py --scratch /s --test tests/run_x.bat" in none
    assert "--at" not in none and "exports HEAD" in none
    # prove.py keeps its option as drawn: --at REV exports REV, HEAD by default.
    helped = subprocess.run([sys.executable, str(PROVE_PY), "--help"], capture_output=True,
                            encoding="utf-8", errors="replace", timeout=60,
                            creationflags=NO_WINDOW).stdout
    assert "--at" in helped and "(default HEAD)" in helped
    # The argument changes nothing at two-key, which names its own commit, once.
    two = prompt_of(tmp_path, "qa-verifier",
                    {**VERIFIER, "task": "two-key", "commit": "abc1234", "at": "9f8e7d6",
                     "contractPath": "c.yaml", "requestPath": "r.md"}, TWO_KEY_REPLY)
    assert two.count("--at") == 1 and "--at abc1234 --mutations /s/mutations.json" in two


@needs_node
def test_14_2_prove_red_with_at_given_still_returns_the_verdict_of_the_exit_code(tmp_path):
    args = {**VERIFIER, "task": "prove-red", "at": "9f8e7d6"}
    out = run_member(tmp_path, "qa-verifier", args, responses=[PROVE_RED_REPLY])
    assert "--at 9f8e7d6" in out["calls"][0]["prompt"]
    assert out["result"]["verdict"] == "PASS" and out["result"]["reasons"] == []
    failing = {**PROVE_RED_REPLY, "exit_code": 1}
    result = run_member(tmp_path, "qa-verifier", args, responses=[failing])["result"]
    assert result["verdict"] == "FAIL" and result["reasons"]


@needs_node
def test_14_2_the_command_the_verifier_runs_proves_red_at_the_base_after_the_code_is_committed(
        tmp_path):
    repo = tmp_path / "proj"
    repo.mkdir()
    (repo / ".sdlc").mkdir()
    (repo / ".sdlc" / "config.yaml").write_text(yaml.safe_dump(
        {"kit": "fixture", "test": {"command": [sys.executable, "-m", "pytest", "-q"]}}),
        encoding="utf-8")
    (repo / "mod.py").write_text("def f():\n    return 0\n", encoding="utf-8")
    ident = ["-c", "user.name=t", "-c", "user.email=t@example.com"]

    def git(*args: str) -> str:
        return subprocess.run(["git", *ident, *args], cwd=repo, check=True, capture_output=True,
                              encoding="utf-8", errors="replace").stdout.strip()
    git("init", "-q")
    git("add", "-A")
    git("commit", "-q", "-m", "base")
    base = git("rev-parse", "HEAD")
    (repo / "mod.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "-m", "the code, committed and green")
    draft = tmp_path / "scratch" / "draft" / "tests"
    draft.mkdir(parents=True)
    (draft / "test_x.py").write_text("import mod\n\n\ndef test_f():\n    assert mod.f() == 1\n",
                                     encoding="utf-8")
    args = {**BASE, "repo": repo.as_posix(), "scratch": (tmp_path / "scratch").as_posix(),
            "pluginRoot": ROOT.as_posix(), "task": "prove-red", "testFile": "tests/test_x.py",
            "at": base}
    prompt = prompt_of(tmp_path, "qa-verifier", args, PROVE_RED_REPLY)
    line = re.search(r"^python \S*prove\.py .*$", prompt, re.MULTILINE)
    assert line and f"--at {base}" in line[0], prompt
    tokens = shlex.split(line[0])
    done = subprocess.run([sys.executable, *tokens[1:]], cwd=repo, env=env_for(tmp_path),
                          capture_output=True, encoding="utf-8", errors="replace", timeout=300,
                          creationflags=NO_WINDOW)
    assert done.returncode == 0, done.stdout + done.stderr
    result = json.loads(done.stdout.strip().splitlines()[-1])
    assert result["red"]["red_ok"] is True, result
    # The same command with no revision exports HEAD, where the code is green: no red.
    plain = [t for i, t in enumerate(tokens) if t != "--at" and tokens[i - 1] != "--at"]
    again = subprocess.run([sys.executable, *plain[1:]], cwd=repo, env=env_for(tmp_path),
                           capture_output=True, encoding="utf-8", errors="replace", timeout=300,
                           creationflags=NO_WINDOW)
    assert again.returncode != 0
    assert json.loads(again.stdout.strip().splitlines()[-1])["red"]["red_ok"] is False


# === 14.3: a QA verifier's question names the QA verifier =================================

def held_operator(e9: str) -> str:
    found = re.findall(r"HOLD \{operator\} as `([\w-]+)`", e9)
    assert found, "E9 never holds {operator} for the QA verifier"
    assert len(found) == 1, found
    return found[0]


def test_14_3_the_flow_holds_the_operator_as_qa_verifier_after_the_dev_verifier_line():
    text = flow()
    e9 = steps_of(text)["E9"]
    assert held_operator(e9) == "qa-verifier"
    hold = e9.index("HOLD {operator} as `qa-verifier`")
    # After the Dev verifier's line, so a Dev verifier's own question still reads Dev verifier;
    # before the QA verifier starts, so the stop rule finds the new operator.
    assert e9.index(DEV_LINE) < hold < e9.index("{plugin}:qa-verifier")
    assert "--task two-key --operator dev-verifier" in e9
    assert text.count("HOLD {operator} as") == 1
    # E2's rule still holds both from the `task.py start` just run.
    assert re.search(r"HOLD[^\n]*\{task\}[^\n]*\{operator\}", steps_of(text)["E2"])


def test_14_3_a_question_from_the_qa_verifier_at_two_key_stops_with_its_name(tmp_path):
    text = flow()
    operator = held_operator(steps_of(text)["E9"])
    found = [c for _, c in task_spans(text, "stop")]
    assert found == [STOP_SPAN], found
    root = make_repo(tmp_path)
    started(tmp_path, root, "two-key", "dev-verifier")
    question = "Which mutation may touch the exit code?"
    code, out, err = run_span(tmp_path, root, found[0], task="two-key", operator=operator,
                              question=question)
    assert (code, err) == (1, "")
    assert out == f"Task two-key stopped on a question from QA verifier: {question}\n"
    assert "Dev verifier" not in out


# === 14.6: the reasons are built as the design's stop sample prints them ==================

def reasons_line() -> str:
    found = [line for line in flow().split("\n") if "`failedSketches`" in line]
    assert len(found) == 1, "one line of the rounds rule names the result's detail"
    return found[0]


def check_reasons_rule(line: str) -> None:
    """The line says: the verifier's reasons joined by `; `, then, when the result keeps any
    detail, `: ` and the detail entries joined by `, `; the old all-by-`; ` join is gone."""
    hold = line.index("HOLD the `reasons`")
    semi = [m.start() for m in re.finditer(r"`; `", line)]
    colon = [m.start() for m in re.finditer(r"`: `", line)]
    comma = [m.start() for m in re.finditer(r"`, `", line)]
    assert len(semi) == 1 and len(colon) == 1 and comma, (semi, colon, comma, line)
    assert hold < semi[0] < colon[0] < comma[0], line
    assert re.search(r"when[^.`]*detail[^.`]*,\s*`: `", line), line
    assert "all joined by" not in line, line
    assert "`{sketch} ({evidence})`" in line and "`{description} ({file}:{line})`" in line


def build_reasons(reasons: list[str], detail: list[str]) -> str:
    """The rule check_reasons_rule pins, applied."""
    joined = "; ".join(reasons)
    return joined + (": " + ", ".join(detail) if detail else "")


def test_14_6_the_reasons_rule_joins_the_reasons_by_semicolon_then_the_detail_by_comma():
    check_reasons_rule(reasons_line())
    text = flow()
    # The verdict line's parentheses keep their `; ` join.
    verdict = [line for line in text.split("\n") if "{verdict} is `PASS`" in line]
    assert len(verdict) == 1 and "joined by `; `" in verdict[0], verdict
    # The detail still comes from the same two result fields, and the receipts case stays.
    assert "each `failedSketches` entry as `{sketch} ({evidence})`" in reasons_line()
    assert "each `blocking` entry as `{description} ({file}:{line})`" in reasons_line()
    assert "(for receipts, its key output)" in reasons_line()


def test_14_6_the_stop_sample_prints_the_design_lines_when_the_rule_builds_the_reasons(tmp_path):
    check_reasons_rule(reasons_line())
    rounds = [
        (["2 sketches failed"], ["SC5.1 (src/command_line.cpp:41)", "SC5.2 (src/command_line.cpp:58)"]),
        (["1 sketch failed"], ["SC5.2 (src/command_line.cpp:58)"]),
        (["1 sketch failed"], ["SC5.2 (src/command_line.cpp:60)"]),
    ]
    assert build_reasons(["1 sketch failed"], []) == "1 sketch failed"
    text = flow()
    fail = [c for _, c in task_spans(text, "fail")]
    stop = [c for _, c in task_spans(text, "stop")]
    assert fail == [FAIL_SPAN] and stop == [STOP_SPAN]
    root = make_repo(tmp_path)
    outs = [run_span(tmp_path, root, fail[0], contract=CONTRACT, unit=U, channel="green",
                     reasons=build_reasons(*one)) for one in rounds]
    assert [o[0] for o in outs] == [0, 0, 1] and outs[0][1] == "" and outs[1][1] == ""
    assert outs[2] == (1, DESIGN_STOP, "")
    # On a question, the other sample line of the design.
    (tmp_path / "second").mkdir()
    again = make_repo(tmp_path / "second")
    code, out, err = run_span(tmp_path / "second", again, stop[0], task="green",
                              operator="developer", question="Which exit code does --frames 0 take?")
    assert (code, out, err) == (1, DESIGN_QUESTION, "")


# === 15.2: a green run closes the unit ====================================================

def test_15_2_the_flow_closes_the_unit_after_both_verifiers_pass_and_before_the_push():
    text = flow()
    found = [(at, c) for at, c in spans(text) if c.startswith("python -m taskcontract progress done")]
    assert [c for _, c in found] == [CLOSE_SPAN], found
    at = found[0][0]
    ends = [o for o, c in task_spans(text, "end") if c == END_TWO_KEY]
    assert len(ends) == 1, "the flow ends two-key through task.py end, once"
    push = [o for o, c in spans(text) if c.startswith("git push")]
    pr = text.index("`gh pr create --draft")
    assert len(push) == 1 and ends[0] < at < push[0] < pr
    # Nothing but the close stands between the end of two-key and the push.
    assert [c for o, c in spans(text) if ends[0] < o < push[0]] == [CLOSE_SPAN]
    assert "one Bash call" in reading(text, at, CLOSE_SPAN)
    # It sits on the pass path alone: after both verifiers pass, before the failure branch.
    e9 = steps_of(text)["E9"]
    assert e9.index("When both verifiers are PASS") < e9.index("`" + CLOSE_SPAN + "`")
    assert e9.index("`" + CLOSE_SPAN + "`") < e9.index("When either exits non-zero")
    # The close is no PR command: the run still opens one draft PR and marks nothing ready.
    assert [c for _, c in spans(text) if c.startswith("gh ")][0].startswith("gh pr create --draft")
    assert not re.search(r"gh pr (ready|merge)", text)


def test_15_2_the_flow_ends_every_task_through_task_py_end_and_closes_only_the_unit():
    text = flow()
    close = [c for _, c in spans(text) if c.startswith("python -m taskcontract progress done")]
    assert close == [CLOSE_SPAN]
    # No other `progress done` anywhere: no task id, no approval, no contract.
    assert [c for _, c in spans(text) if "progress done" in c] == [CLOSE_SPAN]
    ends = [c for _, c in task_spans(text, "end") if " --run" not in c]
    for task in ("write-tests", "approve-tests", "prove-red", "green", "approve-commit", "commit",
                 "two-key"):
        assert any(c.startswith(f"{TASKPY} end --unit {{contract}}/{{unit}} --task {task}")
                   for c in ends), task


def test_15_2_the_close_the_flow_runs_reads_every_task_and_check_done_on_the_tree(tmp_path):
    text = flow()
    found = [c for _, c in spans(text) if c.startswith("python -m taskcontract progress done")]
    assert found == [CLOSE_SPAN], found
    root = make_repo(tmp_path)
    for task, operator in (("write-tests", "qa"), ("green", "developer")):
        started(tmp_path, root, task, operator)
        assert call(tmp_path, root, "end", "--unit", UNIT, "--task", task)[0] == 0
    before = tree(tmp_path, root)
    # The tasks the run recorded read done; the unit and its check do not.
    assert "[done]" in tree_line(before, f"{UNIT}/green")
    assert "[done]" not in tree_line(before, UNIT)
    assert "[to do]" in tree_line(before, f"{UNIT}/SC1.1")
    tokens = shlex.split(found[0].replace("{contract}", CONTRACT).replace("{unit}", U))
    assert tokens[:4] == ["python", "-m", "taskcontract", "progress"]
    done = subprocess.run([sys.executable, *tokens[1:], "--root", str(root)], cwd=tmp_path / "cwd",
                          env=env_for(tmp_path), capture_output=True, encoding="utf-8",
                          errors="replace", timeout=100, creationflags=NO_WINDOW)
    assert (done.returncode, done.stderr) == (0, "")
    after = tree(tmp_path, root)
    for node in (UNIT, *(f"{UNIT}/{t}" for t in (
            "approve-tests", "write-tests", "prove-red", "green", "approve-commit", "commit",
            "two-key", "SC1.1"))):
        assert "[done]" in tree_line(after, node), node
    # Only the closed unit: the other unit of the contract is not closed.
    assert "[done]" not in tree_line(after, f"{CONTRACT}/u2-more/green")
    assert "[done]" not in tree_line(after, f"{CONTRACT}/u2-more/SC1.1")


# === 15.5: the grader reads two sections only where the document has them ================

@needs_node
def test_15_5_the_dev_verifier_reads_the_error_messages_and_constraints_where_the_document_has_them(
        tmp_path):
    args = {**BASE, "branch": "b1", "commit": "abc1234", "contractPath": "specs/c1/contract.yaml",
            "requestPath": "docs/features/c1.md", "receiptsResult": RECEIPTS_OK}
    prompt = prompt_of(tmp_path, "dev-verifier", args, GRADE_OK)
    lines = [line for line in prompt.split("\n") if "Error messages, verbatim" in line]
    assert len(lines) == 1, lines
    line = lines[0]
    errors, constraints = '"Error messages, verbatim"', '"Constraints"'
    assert errors in line and constraints in line, line
    first = min(line.index(errors), line.index(constraints))
    last = max(line.index(errors) + len(errors), line.index(constraints) + len(constraints))
    near = line[max(0, first - 90):last + 90].lower()
    assert "where the document has them" in near, line
    # The checks under "Acceptance criteria" are still read, unconditionally.
    assert '"Acceptance criteria"' in line and "read those checks" in line
    assert line.index('"Acceptance criteria"') < first
