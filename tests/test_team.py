"""Team suite (contract: execution-team, unit e4-team, checks SC1.1, SC1.2 and SC1.3).

The unit ships the execution team in the plugin: five workflow files at the
plugin root (`workflows/qa.js`, `qa-verifier.js`, `developer.js`,
`dev-verifier.js` and `test-retirer.js`, the first four named by the operator
ids `workflows/tools/task.py` takes), and the Orchestrator's flow
`skills/sdlc/flows/execute.md`, dispatched by one line of `skills/sdlc/SKILL.md`.
A consumer session starts a member by its plugin name, `{plugin}:{operator}`,
with nothing copied (the session's workflow probe, reading b), and every
member runs at the model and effort its caller passes from the execution row.

The plugin's files are found beside the imported package, as tests/test_wall.py
finds its hook, so a run against a prototype reads the prototype's files. The
workflow files and the flow are read as text; where `node` is on PATH the
members also run under a small harness with a mock `agent`, so the tests
check what a member returns and what its agent is called with. Every test
reads only the plugin's files and builds its own scratch under tmp_path.
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

import taskcontract

PLUGIN = Path(taskcontract.__file__).resolve().parents[1]
WORKFLOWS = PLUGIN / "workflows"
TOOLS = WORKFLOWS / "tools"
SKILL = PLUGIN / "skills" / "sdlc" / "SKILL.md"
FLOW = PLUGIN / "skills" / "sdlc" / "flows" / "execute.md"
MARKETPLACE = PLUGIN / ".claude-plugin" / "marketplace.json"
OPERATORS_PAGE = PLUGIN / "docs" / "operators.md"
AGENTS = PLUGIN / "agents"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="node is not on PATH")

# The members that run as agents, each named by an operator id of task.py;
# the retirer is the kit's own tool, not a run member.
RUN_MEMBERS = ("qa", "qa-verifier", "developer", "dev-verifier")
MEMBERS = RUN_MEMBERS + ("test-retirer",)
CHAR_CEILING = 12_000  # PromptLang fails at 4000 tokens; ~3.5 chars per token

# The seven tasks, in the order a run takes them: the step that holds each, its
# operator, and the task's line (a template, {verdict} and {code} stand for the
# value the run printed). QA's list is approved after QA writes it, as the
# design's run shows (Interfaces 5), so write-tests comes before approve-tests.
TASKS = [
    ("E3", "write-tests", "qa"),
    ("E4", "approve-tests", "qa-verifier"),
    ("E5", "prove-red", "qa-verifier"),
    ("E6", "green", "developer"),
    ("E7", "approve-commit", "receipts"),
    ("E8", "commit", "orchestrator"),
    ("E9", "two-key", "dev-verifier"),
]
START = ("python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} "
         "--task %s --operator %s")
DONE = "python -m taskcontract progress done {contract}/{unit}/%s"
DONE_BY = {"approve-tests": "qa-verifier", "approve-commit": "receipts"}
LINES = {
    "E3": ["Task write-tests: QA, round 1: done"],
    "E4": ["Task approve-tests: QA verifier, round 1: {verdict}"],
    "E5": ["Task prove-red: QA verifier, round 1: {verdict}"],
    "E6": ["Task green: Developer, round 1: done"],
    "E7": ["Task approve-commit: receipts, round 1: exit {code}"],
    "E8": ["Task commit: Orchestrator: {sha}"],
    "E9": ["Task two-key: Dev verifier, round 1: {verdict}",
           "Task two-key: QA verifier, round 1: {verdict}"],
}
MUTATIONS_TAIL = " (mutations: {caught} of {total} caught)"
# The design's run (Interfaces 5), the lines a one-round run prints.
DESIGN_LINES = [
    "Execution: execution-team unit u1, sonnet at high, test command: test.bat",
    "Task write-tests: QA, round 1: done",
    "Task approve-tests: QA verifier, round 1: PASS",
    "Task prove-red: QA verifier, round 1: PASS",
    "Task green: Developer, round 1: done",
    "Task approve-commit: receipts, round 1: exit 0",
    "Task commit: Orchestrator: 3f2a1bc",
    "Task two-key: Dev verifier, round 1: FAIL (2 sketches failed)",
    "Task two-key: QA verifier, round 1: PASS (mutations: 4 of 4 caught)",
]
HEADER = "Execution: {contract} unit {unit}, {model} at {effort}, test command: {argv0}"
REFUSAL_NO_UNIT = "Execution did not start: no unit {unit} in specs/{contract}/contract.yaml."
REFUSAL_NOT_READY = "Execution did not start: specs/{contract}/contract.yaml is not ready-green."
NODE_LINE = "Node execution: claude --model {model} --effort {effort}"
REMOVE_TASK_FILE = "rm -f {gitdir}/sdlc-task.json"

# The arguments the flow must pass each member start (the step, the member),
# and what each member reads as `a.name`. Optional arguments a member also
# reads (pins, notes, open, focus, sweep, freePaths) are not required here.
COMMON = {"model", "effort", "unit", "contract", "repo"}
FLOW_KEYS = {
    ("E3", "qa"): COMMON | {"scratch", "pluginRoot", "test", "wall", "sources"},
    ("E4", "qa-verifier"): COMMON | {"scratch", "pluginRoot", "task", "testFile",
                                     "contractPath", "requestPath", "draft"},
    ("E5", "qa-verifier"): COMMON | {"scratch", "pluginRoot", "task", "testFile"},
    ("E6", "developer"): COMMON | {"branch", "testFile", "scratchRoot", "files", "sources",
                                   "interface", "test", "wall"},
    ("E9", "dev-verifier"): COMMON | {"branch", "commit", "contractPath", "requestPath",
                                      "receiptsResult"},
    ("E9", "qa-verifier"): COMMON | {"scratch", "pluginRoot", "task", "testFile", "commit",
                                     "contractPath", "requestPath"},
}
TASK_OF = {("E4", "qa-verifier"): "approve-tests", ("E5", "qa-verifier"): "prove-red",
           ("E9", "qa-verifier"): "two-key"}

# The dispatch block of SKILL.md as the g1 unit left it (tests/test_g1_flow.py).
DISPATCH_KEPT = [
    "   - `audit` - LOAD {skill-dir}/flows/audit.md and EXECUTE the Audit flow (A1-A2).",
    "   - `update` - LOAD {skill-dir}/flows/update.md and EXECUTE the Update flow (U1-U3).",
    "   - `new` - LOAD {skill-dir}/flows/new.md and EXECUTE the New flow (N1-N2); the second argument is the task id.",
    "   - `intake` - LOAD {skill-dir}/flows/intake.md and EXECUTE the Intake flow (I1-I9); remaining text is the raw request, when given.",
    "   Otherwise (no args, or a scaffold / `init` intent) LOAD {skill-dir}/flows/init.md and EXECUTE the Init interview, steps 1-6.",
]
G1_DISPATCH = "   - `g1` - LOAD {skill-dir}/flows/g1.md and EXECUTE the G1 flow (R1-R7)"
DISPATCH_HEAD = ("0. DISPATCH. If this skill was invoked with a first argument naming a "
                 "subcommand, do NOT run the interview:")


# --- readers ----------------------------------------------------------------

def read(path: Path) -> str:
    """The file's text; an assertion, not an error, when the unit has not written it."""
    assert path.is_file(), f"{path.relative_to(PLUGIN).as_posix()} is not written"
    return path.read_text(encoding="utf-8")


def member_text(name: str) -> str:
    return read(WORKFLOWS / f"{name}.js")


def flow_text() -> str:
    return read(FLOW)


def flow_steps() -> dict[str, str]:
    """The flow's instruction steps by label (E1, E2, ...), each with its text."""
    text = flow_text()
    block = re.search(r"<instructions>\n(.*?)</instructions>", text, re.DOTALL)
    assert block, "the flow's steps stand inside one instructions block"
    parts = re.split(r"^(?=E\d+\. )", block[1], flags=re.MULTILINE)
    steps = {}
    for part in parts:
        label = re.match(r"(E\d+)\. ", part)
        if label:
            steps[label[1]] = part
    return steps


def member_starts(step: str) -> list[tuple[str, str]]:
    """The members a step starts, in order, each with its text up to the next:
    (plugin-name, segment)."""
    found = list(re.finditer(r"\{plugin\}:([a-z][a-z-]*)", step))
    return [(m[1], step[m.start():(found[i + 1].start() if i + 1 < len(found) else len(step))])
            for i, m in enumerate(found)]


def args_of(segment: str) -> str:
    """The text of the args span that follows a member's name in a flow step."""
    found = re.search(r"args `([^`]*)`", segment)
    assert found, f"no args span after {segment[:40]!r}"
    return found[1]


def operators() -> dict[str, str]:
    """task.py's OPERATORS (id -> the name its start line prints), read without importing it."""
    tree = ast.parse(read(TOOLS / "task.py"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "OPERATORS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError("task.py holds no OPERATORS table")


def listed(path: str, strict: bool) -> bool:
    """Whether git lists the file at the plugin root. Strict: tracked. Otherwise:
    tracked, or new and not ignored, which is how a file reads before the commit
    task adds it (the Developer's green and approve-commit run before that)."""
    flags = [] if strict else ["--cached", "--others", "--exclude-standard"]
    done = subprocess.run(["git", "-C", str(PLUGIN), "ls-files", *flags, "--", path],
                          capture_output=True, encoding="utf-8", errors="replace",
                          creationflags=NO_WINDOW)
    assert done.returncode == 0, f"git ls-files failed at {PLUGIN}: {done.stderr.strip()}"
    return path in done.stdout.split()


def used_keys(text: str) -> set[str]:
    """The arguments a member reads, each as `a.name`."""
    return set(re.findall(r"\ba\.([A-Za-z_]\w*)", text))


# --- running a member under node --------------------------------------------

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

TEST = {"command": ["run-all.bat"], "file": ["run-one.bat", "{file}"], "build": ["build.bat"]}
WALL = {"functional": ["tests/run_*.bat"], "unit": ["tests/*.cpp"], "code": ["src/"],
        "interface": ["src/*.h"]}
BASE = {"model": "m-from-args", "effort": "e-from-args", "unit": "u1", "contract": "contract-1",
        "repo": "/r"}
TEST_FILE = "tests/run_x.bat"
RECEIPTS_OK = {"ok": True, "commands": [{"command": ["run-all.bat"], "exit_code": 0}]}
GRADE_OK = {
    "commit_checked": "abc1234", "files_in_commit": ["src/a.cpp"],
    "trailers": {"contract_trailer": "Contract: contract-1", "theory_trailer_present": True},
    "every_path_inside_scope_or_free": True,
    "sketches": [{"sketch": "s1", "verdict": "PASS", "evidence": "src/a.cpp:1"}],
    "done_means_held": True, "defects": [], "summary": "ok",
}
DRAFT = {
    "test_file": TEST_FILE, "interface": "NOTE-TEXT",
    "tests": [{"name": "t1", "proves": "SC1.1", "intent": "pins x"}],
    "red_proof": {"command": "prove", "summary": "red", "every_failure_on_the_missing_behavior": True},
    "details_fixed": ["d1"], "questions": ["Which exit code?"],
}
DEV = {"files_changed": ["src/a.cpp"], "summary": "s", "unit_tests": "1 passed", "suite": "9 passed",
       "deviations": [], "questions": ["Which flag?"]}


def verifier_args(task: str) -> dict:
    extra = {
        "approve-tests": {"contractPath": "specs/c1/contract.yaml",
                          "requestPath": "docs/features/c1.md", "draft": DRAFT},
        "prove-red": {},
        "two-key": {"commit": "abc1234", "contractPath": "specs/c1/contract.yaml",
                    "requestPath": "docs/features/c1.md"},
    }[task]
    return {**BASE, "scratch": "/s", "pluginRoot": "/p", "task": task, "testFile": TEST_FILE, **extra}


ARGS = {
    "qa": {**BASE, "scratch": "/s", "pluginRoot": "/p", "test": TEST, "wall": WALL,
           "sources": ["specs/c1/contract.yaml"]},
    "qa-verifier:approve-tests": verifier_args("approve-tests"),
    "qa-verifier:prove-red": verifier_args("prove-red"),
    "qa-verifier:two-key": verifier_args("two-key"),
    "developer": {**BASE, "branch": "b1", "testFile": TEST_FILE, "scratchRoot": "/s",
                  "files": ["src/a.cpp"], "sources": ["s1"], "interface": "NOTE-TEXT",
                  "test": TEST, "wall": WALL},
    "dev-verifier": {**BASE, "branch": "b1", "commit": "abc1234",
                     "contractPath": "specs/c1/contract.yaml",
                     "requestPath": "docs/features/c1.md", "receiptsResult": RECEIPTS_OK},
    "test-retirer": {**BASE, "scratch": "/s", "test": TEST, "deletions": ["a.py:b"], "keep": "k",
                     "retiredMeans": "r", "context": ["c"]},
}
CASES = list(ARGS)


def run_member(tmp_path: Path, case: str, args: dict, responses=()) -> dict:
    """Run the member's file under node with a mock agent; the harness's JSON:
    result, calls (prompt, opts) and logs."""
    file = WORKFLOWS / f"{case.split(':')[0]}.js"
    assert file.is_file(), f"{file.relative_to(PLUGIN).as_posix()} is not written"
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


def stopped(result: dict) -> bool:
    """A member's result that stops the run: an error, or a verdict that is not PASS."""
    return bool(result.get("error")) or result.get("verdict") not in (None, "PASS")


# --- SC1.1: a consumer session starts each team member ----------------------

def test_sc1_1_five_workflow_files_stand_at_the_plugin_root_and_no_other():
    names = sorted(p.name for p in WORKFLOWS.glob("*.js"))
    assert names == sorted(f"{m}.js" for m in MEMBERS), names
    for member in MEMBERS:
        assert member_text(member).strip(), f"workflows/{member}.js is empty"


def test_sc1_1_each_workflow_file_names_itself_by_its_file_name():
    # A plugin's workflow is served as {plugin}:{meta.name}; the file name and the
    # name agree so the served name is the same whichever Claude Code takes.
    for member in MEMBERS:
        found = re.search(r"export const meta = \{\s*name: '([^']+)'", member_text(member))
        assert found, f"workflows/{member}.js has no meta name"
        assert found[1] == member, f"workflows/{member}.js is named {found[1]!r}"


def test_sc1_1_the_four_run_members_are_operators_of_task_py_and_the_retirer_is_not():
    table = operators()
    for member in RUN_MEMBERS:
        assert (WORKFLOWS / f"{member}.js").is_file(), f"workflows/{member}.js is not written"
        assert member in table, f"{member} is no operator id of task.py"
    assert "test-retirer" not in table
    # receipts and the Orchestrator run in the session and start no agent.
    assert not (WORKFLOWS / "receipts.js").exists()
    assert not (WORKFLOWS / "orchestrator.js").exists()


def test_sc1_1_the_flow_starts_each_member_by_its_plugin_name_with_the_workflow_tool():
    text, steps = flow_text(), flow_steps()
    assert "Workflow tool" in text
    started = [(label, name) for label, step in steps.items() for name, _ in member_starts(step)]
    assert started == [("E3", "qa"), ("E4", "qa-verifier"), ("E5", "qa-verifier"),
                       ("E6", "developer"), ("E9", "dev-verifier"), ("E9", "qa-verifier")]
    # {plugin} is the plugin the skill runs from (the probe's answer): `sdlc` when
    # installed, the folder's name under `--plugin-dir`.
    assert "`sdlc`" in text and "`--plugin-dir`" in text
    # A bare name is not served, and a path is not what the session starts by.
    for old in ("spec-channel-drafter", "unit-developer", "two-key-unit-verifier"):
        assert old not in text, old
    assert "scriptPath" not in text


def test_sc1_1_the_flow_runs_task_py_and_receipts_py_from_the_plugin_root():
    text, steps = flow_text(), flow_steps()
    for label, task, operator in TASKS:
        assert (START % (task, operator)) in steps[label], f"{label} does not start {task}"
    assert text.count("workflows/tools/task.py start") == len(TASKS)
    assert ("python {skill-dir}/../../workflows/tools/receipts.py --repo {repo} "
            "--receipts {scratch}/receipts.json --out {scratch}/receipts") in steps["E7"]
    # The plugin root is two folders above the skill's own directory.
    assert "{skill-dir}/../.." in text
    # No script path that is not under the plugin root.
    for found in re.findall(r"python (\S+\.py)", text):
        assert found.startswith("{skill-dir}/../../workflows/tools/"), found


def test_sc1_1_nothing_is_copied_into_the_consumer():
    # Every file the team runs stands under the plugin root and none names the
    # untracked folder; the flow starts members by name and runs scripts in place.
    texts = {f"workflows/{m}.js": member_text(m) for m in MEMBERS}
    texts["flows/execute.md"] = flow_text()
    for tool in ("task.py", "prove.py", "receipts.py"):
        texts[f"workflows/tools/{tool}"] = read(TOOLS / tool)
    for name, text in texts.items():
        assert ".claude/workflows" not in text, f"{name} names the untracked folder"
    flow = texts["flows/execute.md"]
    assert not re.search(r"(?:^|`)\s*(?:cp|copy|xcopy|robocopy|Copy-Item|mv)\s", flow, re.MULTILINE)


def test_sc1_1_skill_md_dispatches_execute_in_the_shape_of_the_other_lines():
    skill = read(SKILL)
    steps = flow_steps()
    last = sorted(steps, key=lambda s: int(s[1:]))[-1]
    block = re.search(r"<instructions>\n(.*?)</instructions>", skill, re.DOTALL)
    lines = block[1].splitlines()
    added = [line for line in lines if line.startswith("   - `execute` - ")]
    assert len(added) == 1, f"SKILL.md holds {len(added)} execute dispatch lines"
    assert added[0].startswith("   - `execute` - LOAD {skill-dir}/flows/execute.md and EXECUTE "
                               f"the Execute flow (E1-{last})")
    assert "contract" in added[0] and "unit" in added[0]
    assert lines.index(DISPATCH_HEAD) < lines.index(added[0]) < lines.index(DISPATCH_KEPT[-1])
    # It loses nothing: the other dispatch lines and the g1 line stand as they did.
    for kept in DISPATCH_KEPT:
        assert kept in lines, kept
    assert sum(1 for line in lines if line.startswith(G1_DISPATCH)) == 1
    assert [t for t in re.findall(r"<([a-z][a-z0-9-]*)>", skill)] == [
        "purpose", "context", "instructions", "constraints", "criteria"]
    assert len(skill) < CHAR_CEILING


def test_sc1_1_skill_md_lists_execute_md_among_its_flow_files():
    skill = read(SKILL)
    context = re.search(r"<context>\n(.*?)</context>", skill, re.DOTALL)[1].splitlines()
    named = [line for line in context if "execute.md" in line]
    assert named == ["execute.md,"], named
    assert context.index("g1.md,") < context.index("execute.md,") < context.index(
        "update.md. This file dispatches; the flow file executes. The")
    assert "0025): init.md, new.md, intake.md, vocab.md, lang.md, audit.md," in context


def test_sc1_1_sdlc_spec_and_sdlc_qa_stay_registered_and_unshipped():
    # The unit adds QA and the QA verifier as workflows, not as agents: the two
    # registered operators stay registered (docs/operators.md rows) and unshipped.
    assert FLOW.is_file(), "the team's flow is not written"
    shipped = sorted(p.name for p in AGENTS.iterdir())
    assert "sdlc-spec.md" not in shipped and "sdlc-qa.md" not in shipped, shipped
    page = read(OPERATORS_PAGE).splitlines()
    rows = {name: line for line in page for name in ("sdlc-spec", "sdlc-qa")
            if line.startswith(f"| `{name}` |")}
    assert sorted(rows) == ["sdlc-qa", "sdlc-spec"]
    for line in rows.values():
        assert "registered" in line
    assert not any(p.name.startswith(("sdlc-qa", "sdlc-spec")) for p in WORKFLOWS.glob("*"))


# --- SC1.2: git holds each file the team runs, and the plugin ships it -------

def test_sc1_2_git_holds_each_file_the_team_runs():
    # The scripts are tracked today; the new files read as listed once git
    # lists them (tracked, or new and not ignored: the commit task adds them).
    for member in MEMBERS:
        assert listed(f"workflows/{member}.js", strict=False), f"workflows/{member}.js"
    assert listed("skills/sdlc/flows/execute.md", strict=False)
    for tool in ("task.py", "prove.py", "receipts.py"):
        assert listed(f"workflows/tools/{tool}", strict=True), f"workflows/tools/{tool}"
    assert listed("skills/sdlc/SKILL.md", strict=True)


def test_sc1_2_the_plugin_ships_the_tracked_tree_that_holds_them():
    market = json.loads(read(MARKETPLACE))
    entry = [p for p in market["plugins"] if p["name"] == "sdlc"]
    assert len(entry) == 1 and entry[0]["source"] == "./"
    for member in MEMBERS:
        assert (WORKFLOWS / f"{member}.js").is_file(), f"workflows/{member}.js is not written"
    assert FLOW.is_file()


def test_sc1_2_every_script_the_team_names_stands_under_workflows_tools_and_is_tracked():
    named = set()
    for text in [flow_text(), *(member_text(m) for m in MEMBERS)]:
        named |= set(re.findall(r"workflows/tools/([A-Za-z_]+\.py)", text))
    assert {"task.py", "prove.py", "receipts.py"} <= named, named
    for script in sorted(named):
        assert (TOOLS / script).is_file(), f"workflows/tools/{script} is not written"
        assert listed(f"workflows/tools/{script}", strict=True), script


def test_sc1_2_no_file_the_team_runs_stands_only_under_dot_claude_workflows():
    for member in MEMBERS:
        path = WORKFLOWS / f"{member}.js"
        assert path.is_file(), f"workflows/{member}.js is not written"
        assert ".claude" not in path.relative_to(PLUGIN).parts
    steps = flow_steps()
    for text in (flow_text(), *steps.values()):
        assert ".claude/" not in text


# --- SC1.3: each member runs at the execution row's model and effort ---------

def test_sc1_3_the_flow_reads_the_row_with_node_execution_print_and_passes_both_to_each_member():
    text, steps = flow_text(), flow_steps()
    assert "python -m taskcontract node execution --print" in steps["E2"]
    assert NODE_LINE in steps["E2"]
    for (label, name), keys in FLOW_KEYS.items():
        segments = [seg for n, seg in member_starts(steps[label]) if n == name]
        assert segments, f"{label} starts no {name}"
        for segment in segments:
            args = args_of(segment)
            assert '"model": "{model}"' in args and '"effort": "{effort}"' in args, (label, name)
    # The flow names no model and no effort of its own.
    assert not re.search(r"\b(sonnet|opus|haiku)\b", text, re.IGNORECASE)
    assert not re.search(r"--(?:model|effort) (?!\{)\S", text)


def test_sc1_3_each_member_refuses_to_start_without_model_and_effort_in_its_source():
    for member in MEMBERS:
        text = member_text(member)
        guard = text.find("!a.model || !a.effort")
        first = text.find("await agent(")
        assert 0 <= guard < first, f"workflows/{member}.js starts an agent before its guard"
        assert "model and effort are required arguments" in text, member


def test_sc1_3_each_agent_call_passes_the_arguments_model_and_effort():
    for member in MEMBERS:
        calls = [line for line in member_text(member).splitlines() if "await agent(" in line]
        assert calls, f"workflows/{member}.js makes no agent call"
        for line in calls:
            assert "model: a.model" in line and "effort: a.effort" in line, (member, line.strip())


def test_sc1_3_no_workflow_file_names_a_model_or_an_effort_as_a_literal_setting():
    for member in MEMBERS:
        text = member_text(member)
        assert not re.search(r"\b(sonnet|opus|haiku)\b", text, re.IGNORECASE), member
        assert not re.search(r"\b(?:model|effort)\s*:\s*['\"`]", text), member
        assert not re.search(r"--(?:model|effort)\b", text), member
        assert "a.model" in text and "a.effort" in text, member


@needs_node
@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("missing", ["model", "effort"])
def test_sc1_3_a_member_given_no_model_or_no_effort_starts_no_agent(tmp_path, case, missing):
    args = {k: v for k, v in ARGS[case].items() if k != missing}
    out = run_member(tmp_path, case, args)
    assert out["calls"] == []
    assert stopped(out["result"]), out["result"]
    assert "model and effort" in json.dumps(out["result"])


@needs_node
@pytest.mark.parametrize("case", CASES)
def test_sc1_3_each_member_calls_its_agent_with_the_arguments_model_and_effort(tmp_path, case):
    out = run_member(tmp_path, case, ARGS[case])
    assert len(out["calls"]) == 1
    options = out["calls"][0]["opts"]
    assert options["model"] == "m-from-args" and options["effort"] == "e-from-args"


@needs_node
@pytest.mark.parametrize("case", CASES)
def test_sc1_3_a_member_whose_agent_returns_nothing_reports_it_and_stops_the_run(tmp_path, case):
    out = run_member(tmp_path, case, ARGS[case], responses=[None])
    assert stopped(out["result"]), out["result"]
    assert out["result"].get("questions", []) == []


# --- reading 4: the declared test command, never pytest ----------------------

def test_reading4_no_workflow_file_names_pytest_and_three_take_the_declared_commands():
    for member in MEMBERS:
        assert "pytest" not in member_text(member), member
    for member in ("qa", "developer", "test-retirer"):
        assert "a.test.command" in member_text(member), member
    for member in ("qa", "developer"):
        assert "a.test.build" in member_text(member), member
    # test.file is prove-red's (design, the declaration): QA proves its draft with it,
    # and the Developer, walled from the functional tests, runs the whole command only.
    assert "a.test.file" in member_text("qa")
    assert "a.test.file" not in member_text("developer")


@needs_node
def test_reading4_qa_developer_and_retirer_name_the_declared_commands_in_their_prompts(tmp_path):
    for case in ("qa", "developer", "test-retirer"):
        prompt = run_member(tmp_path, case, ARGS[case])["calls"][0]["prompt"]
        assert "run-all.bat" in prompt, case
        assert "pytest" not in prompt, case
    qa = run_member(tmp_path, "qa", ARGS["qa"])["calls"][0]["prompt"]
    assert "run-one.bat {file}" in qa and "build.bat" in qa
    developer = run_member(tmp_path, "developer", ARGS["developer"])["calls"][0]["prompt"]
    assert "build.bat" in developer
    assert "run-one.bat" not in developer
    assert "{file}" not in developer


@needs_node
def test_reading4_a_member_given_no_test_command_starts_no_agent(tmp_path):
    for case in ("qa", "developer", "test-retirer"):
        args = {k: v for k, v in ARGS[case].items() if k != "test"}
        out = run_member(tmp_path, case, args)
        assert out["calls"] == [], case
        assert "test.command" in out["result"]["error"], case


# --- the wall and the draft (reading f; design Interfaces 4 and 7) -----------

@needs_node
def test_reading_f_qa_writes_its_draft_under_scratch_and_proves_it_with_prove_py(tmp_path):
    prompt = run_member(tmp_path, "qa", ARGS["qa"])["calls"][0]["prompt"]
    assert "/s/draft/" in prompt
    assert "python /p/workflows/tools/prove.py --scratch /s --test" in prompt
    assert "python -m taskcontract interface" in prompt
    assert "src/*.h" in prompt and "tests/*.cpp" in prompt and "tests/run_*.bat" in prompt
    assert "single command" in prompt and "foreground" in prompt and "no git state" in prompt
    # QA writes no prototype and no mutation.
    assert "prototype" not in prompt.lower() and "proto/" not in prompt


def test_reading_f_qa_has_no_prototype_in_its_source_and_draft_schema():
    text = member_text("qa")
    assert "prototype" not in text.lower() and "proto/" not in text
    assert "draft/" in text and "test_file" in text and "--mutations" not in text
    assert re.search(r"\$\{a\.pluginRoot\}/workflows/tools/prove\.py", text)


@needs_node
def test_reading_f_the_developer_reads_no_functional_test_and_no_scratch(tmp_path):
    prompt = run_member(tmp_path, "developer", ARGS["developer"])["calls"][0]["prompt"]
    assert "tests/run_*.bat" in prompt
    assert "/s" in prompt and "NOTE-TEXT" in prompt
    assert "under tests/" not in prompt
    for rule in ("single command", "foreground", "no git state", "No new dependency"):
        assert rule in prompt, rule


def test_reading_f_each_member_keeps_the_prompt_rules_of_the_file_it_comes_from():
    for member in MEMBERS:
        assert "Every shell call is a single command" in member_text(member), member
    for member in ("qa", "developer", "qa-verifier", "test-retirer"):
        text = member_text(member)
        assert "foreground" in text and "timeout" in text, member
        assert "no git state" in text, member
    assert "No new dependency" in member_text("developer")
    assert "read-only" in member_text("dev-verifier")


@needs_node
def test_reading_f_qa_and_developer_results_carry_the_draft_the_note_and_the_questions(tmp_path):
    qa = run_member(tmp_path, "qa", ARGS["qa"], responses=[DRAFT])["result"]
    assert qa["draft"] == DRAFT and qa["questions"] == ["Which exit code?"]
    dev = run_member(tmp_path, "developer", ARGS["developer"], responses=[DEV])["result"]
    assert dev["dev"] == DEV and dev["questions"] == ["Which flag?"]
    assert not stopped(qa) and not stopped(dev)


# --- the QA verifier's three tasks -------------------------------------------

def test_reading8_qa_verifier_holds_three_tasks_and_runs_prove_py_on_its_exit_code():
    text = member_text("qa-verifier")
    for task in ("approve-tests", "prove-red", "two-key"):
        assert f"'{task}'" in text, task
    assert re.search(r"\$\{a\.pluginRoot\}/workflows/tools/prove\.py", text)
    assert "--at" in text and "--mutations" in text and "mutations.json" in text
    assert "exit_code" in text and "a.task" in text


@needs_node
@pytest.mark.parametrize("code,verdict", [(0, "PASS"), (1, "FAIL"), (2, "FAIL"), (254, "INCOMPLETE")])
def test_reading8_prove_red_verdict_is_computed_from_prove_pys_exit_code(tmp_path, code, verdict):
    case = "qa-verifier:prove-red"
    # The agent's own claim of a verdict is never read.
    reply = {"command": "prove", "exit_code": code, "output": "{}", "red_summary": "2 passed",
             "verdict": "PASS", "ok": True}
    out = run_member(tmp_path, case, ARGS[case], responses=[reply])
    prompt = out["calls"][0]["prompt"]
    assert "python /p/workflows/tools/prove.py --scratch /s --test tests/run_x.bat" in prompt
    result = out["result"]
    assert result["verdict"] == verdict and result["task"] == "prove-red"
    assert result["questions"] == []
    assert bool(result["reasons"]) == (verdict != "PASS")


MUTANTS = [{"name": f"m{i}", "behavior": f"behavior {i}", "applied": True, "caught": True}
           for i in range(1, 5)]


def mutate_reply(code=0, mutations=MUTANTS) -> dict:
    return {"command": "prove", "exit_code": code, "mutations": mutations,
            "output": '{"old":"if frames > 0"}'}


@needs_node
def test_reading8_two_key_passes_when_four_mutations_are_all_caught_and_prove_py_exits_0(tmp_path):
    case = "qa-verifier:two-key"
    out = run_member(tmp_path, case, ARGS[case], responses=[mutate_reply()])
    prompt = out["calls"][0]["prompt"]
    assert "python /p/workflows/tools/prove.py --scratch /s --test tests/run_x.bat" in prompt
    assert "--at abc1234" in prompt and "--mutations /s/mutations.json" in prompt
    result = out["result"]
    assert result["verdict"] == "PASS" and result["reasons"] == []
    assert result["mutations"] == {"caught": 4, "total": 4}
    assert result["task"] == "two-key" and result["questions"] == []


@needs_node
def test_reading8_two_key_fails_an_uncaught_mutation_naming_the_behavior_never_the_code(tmp_path):
    case = "qa-verifier:two-key"
    mutants = [*MUTANTS[:3], {"name": "m4", "behavior": "frames accepts 0", "applied": True,
                              "caught": False}]
    result = run_member(tmp_path, case, ARGS[case], responses=[mutate_reply(1, mutants)])["result"]
    assert result["verdict"] == "FAIL"
    assert result["mutations"] == {"caught": 3, "total": 4}
    assert any("frames accepts 0" in reason for reason in result["reasons"])
    assert "if frames > 0" not in json.dumps(result)


@needs_node
def test_reading8_two_key_fails_a_non_zero_exit_and_fewer_than_four_mutations(tmp_path):
    case = "qa-verifier:two-key"
    exit_one = run_member(tmp_path, case, ARGS[case], responses=[mutate_reply(1)])["result"]
    assert exit_one["verdict"] == "FAIL" and exit_one["reasons"]
    three = run_member(tmp_path, case, ARGS[case], responses=[mutate_reply(0, MUTANTS[:3])])["result"]
    assert three["verdict"] == "FAIL" and three["mutations"] == {"caught": 3, "total": 3}
    unapplied = [*MUTANTS[:3], {**MUTANTS[3], "applied": False}]
    result = run_member(tmp_path, case, ARGS[case], responses=[mutate_reply(0, unapplied)])["result"]
    assert result["verdict"] == "FAIL" and result["mutations"] == {"caught": 3, "total": 4}


def sketch(text: str, pinned: bool) -> dict:
    return {"sketch": text, "pinned": pinned, "tests": ["t"] if pinned else []}


def approve_reply(sketches, done_means_held=True, defects=(), questions=()) -> dict:
    return {"sketches": sketches, "done_means_held": done_means_held, "defects": list(defects),
            "summary": "s", "questions": list(questions)}


@needs_node
def test_reading8_approve_tests_passes_a_list_that_pins_every_sketch_and_done_means(tmp_path):
    case = "qa-verifier:approve-tests"
    reply = approve_reply([sketch("S1", True), sketch("S2", True)],
                          defects=[{"severity": "advisory", "description": "wording"}])
    out = run_member(tmp_path, case, ARGS[case], responses=[reply])
    prompt = out["calls"][0]["prompt"]
    assert "NOTE-TEXT" in prompt and "/s/draft/tests/run_x.bat" in prompt
    assert "specs/c1/contract.yaml" in prompt and "docs/features/c1.md" in prompt
    result = out["result"]
    assert result["verdict"] == "PASS" and result["reasons"] == []
    assert result["task"] == "approve-tests" and result["questions"] == []


@needs_node
def test_reading8_approve_tests_fails_an_unpinned_sketch_done_means_or_a_blocking_defect(tmp_path):
    case = "qa-verifier:approve-tests"
    unpinned = approve_reply([sketch("S1", True), sketch("S2 is not pinned", False)])
    result = run_member(tmp_path, case, ARGS[case], responses=[unpinned])["result"]
    assert result["verdict"] == "FAIL"
    assert any("S2 is not pinned" in reason for reason in result["reasons"])
    done = approve_reply([sketch("S1", True)], done_means_held=False)
    assert run_member(tmp_path, case, ARGS[case], responses=[done])["result"]["verdict"] == "FAIL"
    blocking = approve_reply([sketch("S1", True)],
                             defects=[{"severity": "blocking", "description": "no exit code in note"}])
    result = run_member(tmp_path, case, ARGS[case], responses=[blocking])["result"]
    assert result["verdict"] == "FAIL"
    assert any("no exit code in note" in reason for reason in result["reasons"])


@needs_node
def test_reading8_a_verifier_question_reaches_the_result(tmp_path):
    case = "qa-verifier:approve-tests"
    reply = approve_reply([sketch("S1", True)], questions=["Is S1 retired?"])
    result = run_member(tmp_path, case, ARGS[case], responses=[reply])["result"]
    assert result["questions"] == ["Is S1 retired?"]


@needs_node
@pytest.mark.parametrize("case,drop", [("qa-verifier:approve-tests", "draft"),
                                       ("qa-verifier:two-key", "commit"),
                                       ("qa-verifier:prove-red", "pluginRoot")])
def test_reading8_qa_verifier_without_a_required_argument_starts_no_agent(tmp_path, case, drop):
    args = {k: v for k, v in ARGS[case].items() if k != drop}
    out = run_member(tmp_path, case, args)
    assert out["calls"] == []
    assert out["result"]["verdict"] == "INCOMPLETE"
    assert drop in " ".join(out["result"]["reasons"])


@needs_node
def test_reading8_qa_verifier_given_an_unknown_task_starts_no_agent(tmp_path):
    args = {**ARGS["qa-verifier:prove-red"], "task": "green"}
    out = run_member(tmp_path, "qa-verifier", args)
    assert out["calls"] == []
    assert out["result"]["verdict"] == "INCOMPLETE" and out["result"]["reasons"]


# --- the Dev verifier: the verdict reads the exit codes ----------------------

@needs_node
def test_reading_the_dev_verdict_reads_receipts_exit_codes_and_never_the_ok_field(tmp_path):
    args = ARGS["dev-verifier"]
    failing = {"ok": True, "commands": [{"command": ["run-all.bat"], "exit_code": 1}]}
    result = run_member(tmp_path, "dev-verifier", {**args, "receiptsResult": failing},
                        responses=[GRADE_OK])["result"]
    assert result["verdict"] == "FAIL" and result["reasons"]
    passing = {"ok": False, "commands": [{"command": ["run-all.bat"], "exit_code": 0}]}
    result = run_member(tmp_path, "dev-verifier", {**args, "receiptsResult": passing},
                        responses=[GRADE_OK])["result"]
    assert result["verdict"] == "PASS" and result["reasons"] == []
    assert result["questions"] == []
    none = {k: v for k, v in args.items() if k != "receiptsResult"}
    result = run_member(tmp_path, "dev-verifier", none, responses=[GRADE_OK])["result"]
    assert result["verdict"] == "INCOMPLETE"


@needs_node
def test_reading_the_dev_verifier_words_its_failed_sketches_as_the_design_prints_them(tmp_path):
    def graded(failed: int) -> dict:
        sketches = [{"sketch": f"s{i}", "verdict": "FAIL", "evidence": "f:1"} for i in range(failed)]
        return {**GRADE_OK, "sketches": sketches or GRADE_OK["sketches"]}
    two = run_member(tmp_path, "dev-verifier", ARGS["dev-verifier"], responses=[graded(2)])["result"]
    assert two["verdict"] == "FAIL" and "2 sketches failed" in two["reasons"]
    one = run_member(tmp_path, "dev-verifier", ARGS["dev-verifier"], responses=[graded(1)])["result"]
    assert one["verdict"] == "FAIL" and "1 sketch failed" in one["reasons"]


@needs_node
def test_reading_a_dev_verifier_question_reaches_the_result_beside_a_passing_verdict(tmp_path):
    grade = {**GRADE_OK, "questions": ["Is the ADR needed?"]}
    result = run_member(tmp_path, "dev-verifier", ARGS["dev-verifier"], responses=[grade])["result"]
    assert result["verdict"] == "PASS" and result["questions"] == ["Is the ADR needed?"]


# --- the flow (done_means: each member starts at the row's settings) ---------

def test_flow_keeps_the_promptlang_shape_and_budget():
    text = flow_text()
    assert text.startswith("---\nname: sdlc-flow-execute\ndescription: ")
    assert text.split("\n")[3] == "---"
    opened = set(re.findall(r"<([a-z][a-z0-9-]*)>", text))
    assert opened == {"purpose", "instructions"}
    for tag in opened:
        assert text.count(f"<{tag}>") == 1 and text.count(f"</{tag}>") == 1
    assert text.index("</purpose>") < text.index("<instructions>")
    assert len(text) < CHAR_CEILING
    assert "`/sdlc execute {contract} {unit}`" in text


def test_flow_holds_steps_e1_to_e9_in_order():
    steps = flow_steps()
    assert list(steps) == [f"E{n}" for n in range(1, 10)]
    text = flow_text()
    assert re.findall(r"^(E\d+)\. ", text, re.MULTILINE) == list(steps)


def test_reading5_the_two_refusals_come_first_and_the_header_follows_the_settings():
    steps = flow_steps()
    e1, e2 = steps["E1"], steps["E2"]
    assert REFUSAL_NO_UNIT in e1 and REFUSAL_NOT_READY in e1
    assert e1.index(REFUSAL_NO_UNIT) < e1.index(REFUSAL_NOT_READY)
    assert "python -m taskcontract validate specs/{contract}/contract.yaml --profile ready" in e1
    assert HEADER in e2
    assert e2.index(NODE_LINE) < e2.index(HEADER)
    assert ".sdlc/config.yaml" in e2 and "test:" in e2 and "wall:" in e2
    assert "test.command" in e2 and "{argv0}" in e2
    # The refusals are not repeated and the header is shown once.
    text = flow_text()
    assert text.count(HEADER) == 1 and text.count(REFUSAL_NO_UNIT) == 1


def test_reading5_each_task_runs_start_then_member_then_line_then_progress_done():
    steps = flow_steps()
    for label, task, operator in TASKS:
        step = steps[label]
        start = START % (task, operator)
        assert step.count(start) == 1 and step.count("task.py start") == 1, label
        done = DONE % task
        if task in DONE_BY:
            done = f"{done} --by {DONE_BY[task]}"
            assert done in step, label
        else:
            assert re.search(re.escape(done) + r"(?! --by)", step), label
            assert " --by " not in step, label
        order = [step.index(start)]
        names = [n for n, _ in member_starts(step)]
        if names:
            order.append(step.index("{plugin}:" + names[0]))
        line = LINES[label][0]
        assert line in step, f"{label} does not show {line!r}"
        order += [step.index(line), step.index(done)]
        assert order == sorted(order), (label, order)
        assert len(set(order)) == len(order), label


def test_reading5_the_seven_tasks_run_in_the_order_the_design_shows():
    text = flow_text()
    starts = [text.index(START % (task, operator)) for _, task, operator in TASKS]
    assert starts == sorted(starts) and len(set(starts)) == 7


def test_reading5_each_tasks_line_names_its_operator_as_task_py_prints_it():
    table, steps = operators(), flow_steps()
    for label, task, operator in TASKS:
        separator = ": " if task == "commit" else ", round 1: "
        assert f"Task {task}: {table[operator]}{separator}" in steps[label], label
    assert "Task two-key: QA verifier, round 1: " in steps["E9"]
    assert table["qa-verifier"] == "QA verifier"


def test_reading5_the_lines_the_flow_shows_are_the_design_lines():
    steps = flow_steps()
    templates = [HEADER] + [line for label in LINES for line in LINES[label]]
    for label, lines in LINES.items():
        for line in lines:
            assert line in steps[label], (label, line)
    assert HEADER in steps["E2"]
    assert MUTATIONS_TAIL in steps["E9"]
    rendered = set()
    for template in templates:
        for verdict in ("PASS", "FAIL (2 sketches failed)"):
            for tail in ("", MUTATIONS_TAIL):
                rendered.add((template + tail)
                             .replace("{verdict}", verdict).replace("{code}", "0")
                             .replace("{sha}", "3f2a1bc").replace("{contract}", "execution-team")
                             .replace("{unit}", "u1").replace("{model}", "sonnet")
                             .replace("{effort}", "high").replace("{argv0}", "test.bat")
                             .replace("{caught}", "4").replace("{total}", "4"))
    for line in DESIGN_LINES:
        assert line in rendered, line


def test_reading5_a_task_that_stops_removes_the_task_file_and_opens_nothing():
    steps, text = flow_steps(), flow_text()
    e2 = steps["E2"]
    assert e2.index("task.py start") < e2.index("progress done") < e2.index(REMOVE_TASK_FILE)
    # The task file sits where git names its folder: a linked worktree's .git is a file.
    assert "`git rev-parse --absolute-git-dir` as {gitdir}" in e2
    assert ".git/sdlc-task.json" not in text
    for word in ("`error`", "`questions`", "`PASS`", "STOP", "exits 1"):
        assert word in e2, word
    assert e2.count(REMOVE_TASK_FILE) >= 2
    # A failed approve-commit stops before the task is recorded done, task file removed.
    e7 = steps["E7"]
    between = e7[e7.index(LINES["E7"][0]):e7.index(DONE % "approve-commit")]
    assert "STOP" in between and REMOVE_TASK_FILE in between
    # e5's, not this flow's: no rounds, no stop messages, no pull request.
    for absent in ("gh pr", "Draft PR", "failed 3 rounds", "stopped on a question",
                   "task.py fail", "task.py stop", "task.py end"):
        assert absent not in text, absent


def test_reading5_the_flow_chains_no_shell_segments():
    text = flow_text()
    commands = [c for c in re.findall(r"`([^`\n]+)`", text)
                if c.startswith(("python ", "git ", "rm "))]
    assert len(commands) >= 20, len(commands)
    for command in commands:
        assert not re.search(r"\|| && |;|>|<", command), command


def test_reading6_the_orchestrator_places_the_draft_after_prove_red_and_commits_once():
    steps, text = flow_steps(), flow_text()
    e5, draft = steps["E5"], "{scratch}/draft/{testFile}"
    assert e5.index(LINES["E5"][0]) < e5.index(draft) < e5.index(DONE % "prove-red")
    assert "{testFile}" in e5[e5.index(draft) + len(draft):], "the draft is placed at {testFile}"
    assert text.count("git commit") == 1 and "git commit" in steps["E8"]
    assert text.count("git add") == 1 and "git add" in steps["E8"]
    e8 = steps["E8"]
    assert "Contract: {contract}" in e8 and "Theory:" in e8
    assert e8.index("git add") < e8.index("git commit") < e8.index(LINES["E8"][0])
    # QA's draft is where the write-tests step says it is.
    assert "`{scratch}/draft/{testFile}`" in steps["E3"]
    assert "draft.test_file" in steps["E3"] and "draft.interface" in steps["E3"]


def test_reading7_two_key_names_the_dev_verifier_and_runs_the_qa_verifier_in_the_same_step():
    e9 = flow_steps()["E9"]
    assert "--task two-key --operator dev-verifier" in e9
    assert [n for n, _ in member_starts(e9)] == ["dev-verifier", "qa-verifier"]
    assert e9.index(LINES["E9"][0]) < e9.index("{plugin}:qa-verifier") < e9.index(LINES["E9"][1])
    assert e9.index(LINES["E9"][1]) < e9.index(DONE % "two-key")
    # The grade reads receipts.py's result from approve-commit.
    assert '"receiptsResult": {receipts}' in e9
    assert "{receipts}" in flow_steps()["E7"]


def test_reading_b_each_member_start_passes_the_arguments_its_file_reads():
    steps = flow_steps()
    for (label, name), required in FLOW_KEYS.items():
        text = member_text(name)
        reads = used_keys(text)
        for _, segment in [s for s in member_starts(steps[label]) if s[0] == name]:
            args = args_of(segment)
            keys = set(re.findall(r'"(\w+)":', args))
            assert required <= keys, (label, name, sorted(required - keys))
            assert keys <= reads, (label, name, sorted(keys - reads))
            if name == "qa-verifier":
                assert f'"task": "{TASK_OF[(label, name)]}"' in args, (label, name)
            assert '"unit": "{unit}"' in args and '"contract": "{contract}"' in args
            if "pluginRoot" in keys:
                assert '"pluginRoot": "{skill-dir}/../.."' in args
        assert required <= reads, (name, sorted(required - reads))


def test_reading_b_the_arguments_the_flow_builds_come_from_the_declarations():
    steps = flow_steps()
    e2, e3, e6 = steps["E2"], steps["E3"], steps["E6"]
    assert "{test}" in e2 and "{wall}" in e2 and "{repo}" in e2 and "{branch}" in e2
    assert "{scratch}" in e2
    assert '"test": {test}' in e3 and '"wall": {wall}' in e3
    assert '"files": {scope}' in e6 and '"interface": {note}' in e6
    assert '"scratchRoot": "{scratch}"' in e6 and '"branch": "{branch}"' in e6
    assert "{scope}" in steps["E1"]
