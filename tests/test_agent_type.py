"""Agent-type suite (contract: execution-team, unit e7-agent-type, checks SC1.1 and SC1.3).

The unit makes each team member start as the plugin's agent type `sdlc-team`:
`agents/sdlc-team.md` holds only Read, Grep, Glob, Edit, Write and Bash, and
names no model and no effort, so the execution row stays the one source of both.
The Orchestrator's flow `skills/sdlc/flows/execute.md` passes
`"agentType": "{plugin}:sdlc-team"` in the args of every member it starts, and
each workflow under `workflows/` takes `agentType` as a required argument and
passes it on to `agent()` beside `model` and `effort`. A workflow given no type
starts no agent and logs its missing argument.

The plugin's files are found beside the imported package, as tests/test_team.py
finds them, so a run against a prototype reads the prototype's files. The
definition, the flow and the workflow files are read as text; where `node` is
on PATH each member also runs under a small harness with a mock `agent`, so the
tests check what a member returns, what it logs and what its agent is called
with. Every test reads only the plugin's files and builds its own scratch under
tmp_path.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

import taskcontract

PLUGIN = Path(taskcontract.__file__).resolve().parents[1]
WORKFLOWS = PLUGIN / "workflows"
AGENTS = PLUGIN / "agents"
DEFINITION = AGENTS / "sdlc-team.md"
FLOW = PLUGIN / "skills" / "sdlc" / "flows" / "execute.md"
OPERATORS_PAGE = PLUGIN / "docs" / "operators.md"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="node is not on PATH")

MEMBERS = ("qa", "qa-verifier", "developer", "dev-verifier", "test-retirer")
TOOLS = {"Read", "Grep", "Glob", "Edit", "Write", "Bash"}
SHIPPED = {"sdlc-developer.md", "sdlc-team.md", "sdlc-verifier.md"}
TYPE_ARG = '"agentType": "{plugin}:sdlc-team"'
MISSING = "missing required argument(s): agentType"
CHAR_CEILING = 12_000  # the flow's PromptLang budget (tests/test_team.py)
# The six member starts of the flow, in order: (step, member).
STARTS = [("E3", "qa"), ("E4", "qa-verifier"), ("E5", "qa-verifier"),
          ("E6", "developer"), ("E9", "dev-verifier"), ("E9", "qa-verifier")]


# --- readers ----------------------------------------------------------------

def read(path: Path) -> str:
    """The file's text; an assertion, not an error, when the unit has not written it."""
    assert path.is_file(), f"{path.relative_to(PLUGIN).as_posix()} is not written"
    return path.read_text(encoding="utf-8")


def member_text(name: str) -> str:
    return read(WORKFLOWS / f"{name}.js")


def definition() -> tuple[dict[str, str], str]:
    """The agent definition's frontmatter fields and its body."""
    text = read(DEFINITION)
    assert text.startswith("---\n"), "agents/sdlc-team.md opens with frontmatter"
    head, sep, body = text[4:].partition("\n---")
    assert sep, "agents/sdlc-team.md closes its frontmatter"
    fields = {}
    for line in head.splitlines():
        found = re.match(r"([A-Za-z_-]+):\s*(.*)$", line)
        if found:
            fields[found[1]] = found[2].strip()
    return fields, body


def flow_text() -> str:
    return read(FLOW)


def flow_steps() -> dict[str, str]:
    """The flow's instruction steps by label (E1, E2, ...), each with its text."""
    block = re.search(r"<instructions>\n(.*?)</instructions>", flow_text(), re.DOTALL)
    assert block, "the flow's steps stand inside one instructions block"
    steps = {}
    for part in re.split(r"^(?=E\d+\. )", block[1], flags=re.MULTILINE):
        label = re.match(r"(E\d+)\. ", part)
        if label:
            steps[label[1]] = part
    return steps


def member_starts(step: str) -> list[tuple[str, str]]:
    """The members a step starts, in order, each with its text up to the next:
    (plugin-name, segment). The agent type's own name, which a start's args now
    carry, is no member."""
    found = list(re.finditer(r"\{plugin\}:((?!sdlc-team)[a-z][a-z-]*)", step))
    return [(m[1], step[m.start():(found[i + 1].start() if i + 1 < len(found) else len(step))])
            for i, m in enumerate(found)]


def args_of(segment: str) -> str:
    """The text of the args span that follows a member's name in a flow step."""
    found = re.search(r"args `([^`]*)`", segment)
    assert found, f"no args span after {segment[:40]!r}"
    return found[1]


def start_args() -> list[tuple[str, str, str]]:
    """Each member start of the flow: (step, member, its args span)."""
    out = []
    for label, step in flow_steps().items():
        for name, segment in member_starts(step):
            out.append((label, name, args_of(segment)))
    return out


def listed(path: str) -> bool:
    """Whether git lists the file at the plugin root: tracked, or new and not
    ignored, which is how a file reads before the commit task adds it."""
    done = subprocess.run(["git", "-C", str(PLUGIN), "ls-files", "--cached", "--others",
                           "--exclude-standard", "--", path],
                          capture_output=True, encoding="utf-8", errors="replace",
                          creationflags=NO_WINDOW)
    assert done.returncode == 0, f"git ls-files failed at {PLUGIN}: {done.stderr.strip()}"
    return path in done.stdout.split()


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
TYPE = "plug-x:sdlc-team"
BASE = {"model": "m-from-args", "effort": "e-from-args", "agentType": TYPE, "unit": "u1",
        "contract": "contract-1", "repo": "/r"}
TEST_FILE = "tests/run_x.bat"
RECEIPTS_OK = {"ok": True, "commands": [{"command": ["run-all.bat"], "exit_code": 0}]}
DRAFT = {
    "test_file": TEST_FILE, "interface": "NOTE-TEXT",
    "tests": [{"name": "t1", "proves": "SC1.1", "intent": "pins x"}],
    "red_proof": {"command": "prove", "summary": "red", "every_failure_on_the_missing_behavior": True},
    "details_fixed": ["d1"], "questions": [],
}


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
ERROR_CASES = ["qa", "developer", "test-retirer"]  # a missing type is an error
VERDICT_CASES = [c for c in CASES if c not in ERROR_CASES]  # a missing type is INCOMPLETE


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


def without_type(case: str, how: str) -> dict:
    """The case's args with the type absent (`absent`) or empty (`empty`)."""
    if how == "empty":
        return {**ARGS[case], "agentType": ""}
    return {k: v for k, v in ARGS[case].items() if k != "agentType"}


# --- SC1.1: the type ships, each member starts as it -------------------------

def test_sc1_1_the_definition_stands_in_the_plugins_agents_folder_and_git_lists_it():
    assert DEFINITION.is_file(), "agents/sdlc-team.md is not written"
    assert listed("agents/sdlc-team.md"), "git does not list agents/sdlc-team.md"


def test_sc1_1_the_definition_is_named_sdlc_team_and_is_described():
    fields, _ = definition()
    assert fields.get("name") == "sdlc-team", fields
    assert fields.get("description"), "the definition has no description"


def test_sc1_1_the_definition_holds_only_read_grep_glob_edit_write_and_bash():
    fields, _ = definition()
    assert "tools" in fields, "the definition has no tools line"
    tools = [t.strip() for t in fields["tools"].strip("[]").split(",") if t.strip()]
    assert len(tools) == len(set(tools)), tools
    assert set(tools) == TOOLS, tools


def test_sc1_1_the_definition_body_is_a_short_promptlang_body_about_the_brief_and_the_schema():
    _, body = definition()
    assert body.strip(), "the definition has no body"
    assert len(body) < 4000, len(body)
    for tag in ("purpose", "instructions"):
        assert body.count(f"<{tag}>") == 1 and body.count(f"</{tag}>") == 1, tag
    assert body.index("</purpose>") < body.index("<instructions>")
    lowered = body.lower()
    assert "brief" in lowered and "schema" in lowered


def test_sc1_1_the_agents_folder_ships_the_two_operators_and_the_type_and_neither_registered_one():
    assert DEFINITION.is_file(), "agents/sdlc-team.md is not written"
    assert {p.name for p in AGENTS.glob("*.md")} == SHIPPED
    assert not any(p.name.startswith(("sdlc-spec", "sdlc-qa")) for p in AGENTS.iterdir())
    assert not any(p.name.startswith(("sdlc-spec", "sdlc-qa")) for p in WORKFLOWS.glob("*"))


def test_sc1_1_the_operators_page_gains_the_type_and_keeps_spec_and_qa_registered():
    page = read(OPERATORS_PAGE).splitlines()
    rows = {name: line for line in page for name in ("sdlc-team", "sdlc-spec", "sdlc-qa")
            if line.startswith(f"| `{name}` |")}
    assert sorted(rows) == ["sdlc-qa", "sdlc-spec", "sdlc-team"], sorted(rows)
    for name in ("sdlc-spec", "sdlc-qa"):
        assert "registered" in rows[name], name
    assert "registered" not in rows["sdlc-team"]


def test_sc1_1_the_flow_passes_the_type_in_the_args_of_each_of_its_six_member_starts():
    starts = start_args()
    assert [(label, name) for label, name, _ in starts] == STARTS
    for label, name, args in starts:
        assert TYPE_ARG in args, (label, name, args)
    # The type's name is the flow's to build from {plugin}: no start spells the plugin out.
    text = flow_text()
    assert "sdlc:sdlc-team" not in text
    assert text.count(TYPE_ARG) == len(STARTS)


def test_sc1_1_the_flow_stays_inside_its_promptlang_budget_with_the_type_added():
    text = flow_text()
    assert TYPE_ARG in text, "the flow does not pass the type yet"
    assert len(text) < CHAR_CEILING, len(text)


def test_sc1_1_the_flow_copies_nothing_into_the_consumers_agents():
    text = flow_text()
    assert TYPE_ARG in text, "the flow does not pass the type yet"
    assert ".claude/agents" not in text and "~/.claude" not in text
    assert not re.search(r"(?:^|`)\s*(?:cp|copy|xcopy|robocopy|Copy-Item|mv)\s", text, re.MULTILINE)


@pytest.mark.parametrize("member", MEMBERS)
def test_sc1_1_each_workflow_reads_the_type_as_an_argument_and_names_it_nowhere(member):
    text = member_text(member)
    assert "a.agentType" in text, f"workflows/{member}.js never reads agentType"
    assert "sdlc-team" not in text and "sdlc:" not in text, member
    assert not re.search(r"agentType\s*:\s*['\"`]", text), member


@pytest.mark.parametrize("member", MEMBERS)
def test_sc1_1_each_workflow_checks_the_type_before_its_first_agent_call(member):
    text = member_text(member)
    guard, first = text.find("a.agentType"), text.find("await agent(")
    assert 0 <= guard < first, f"workflows/{member}.js starts an agent before it checks agentType"


@needs_node
@pytest.mark.parametrize("how", ["absent", "empty"])
@pytest.mark.parametrize("case", CASES)
def test_sc1_1_a_member_given_no_type_starts_no_agent_and_logs_its_missing_argument(
        tmp_path, case, how):
    out = run_member(tmp_path, case, without_type(case, how))
    assert out["calls"] == [], out["calls"]
    assert f"u1: {MISSING}" in out["logs"], out["logs"]


@needs_node
@pytest.mark.parametrize("how", ["absent", "empty"])
@pytest.mark.parametrize("case", ERROR_CASES)
def test_sc1_1_qa_the_developer_and_the_retirer_return_the_missing_type_as_an_error(
        tmp_path, case, how):
    result = run_member(tmp_path, case, without_type(case, how))["result"]
    assert result["error"] == MISSING, result
    assert result["unit"] == "u1"
    assert result.get("questions", []) == []


@needs_node
@pytest.mark.parametrize("how", ["absent", "empty"])
@pytest.mark.parametrize("case", VERDICT_CASES)
def test_sc1_1_the_verifiers_return_the_missing_type_as_an_incomplete_verdict(
        tmp_path, case, how):
    result = run_member(tmp_path, case, without_type(case, how))["result"]
    assert result["verdict"] == "INCOMPLETE", result
    assert result["reasons"] == [MISSING], result
    assert result["questions"] == []
    assert result["unit"] == "u1"
    if case.startswith("qa-verifier:"):
        assert result["task"] == case.split(":")[1]


# --- SC1.3: each agent call carries model, effort and the type ---------------

def test_sc1_3_the_type_names_no_model_and_no_effort_so_the_execution_row_stays_the_one_source():
    fields, body = definition()
    assert fields.get("model") == "inherit", fields
    assert "effort" not in fields, fields
    text = read(DEFINITION)
    assert not re.search(r"\b(sonnet|opus|haiku)\b", text, re.IGNORECASE)


def test_sc1_3_the_flow_passes_the_type_beside_model_and_effort_in_each_start():
    starts = start_args()
    assert len(starts) == len(STARTS)
    for label, name, args in starts:
        assert '"model": "{model}"' in args and '"effort": "{effort}"' in args, (label, name)
        assert TYPE_ARG in args, (label, name)
    assert not re.search(r"\b(sonnet|opus|haiku)\b", flow_text(), re.IGNORECASE)


@pytest.mark.parametrize("member", MEMBERS)
def test_sc1_3_each_agent_call_passes_model_effort_and_the_type_from_the_arguments(member):
    calls = [line for line in member_text(member).splitlines() if "await agent(" in line]
    assert calls, f"workflows/{member}.js makes no agent call"
    for line in calls:
        assert "model: a.model" in line and "effort: a.effort" in line, (member, line.strip())
        assert re.search(r"agentType:\s*a\.agentType", line), (member, line.strip())


@needs_node
@pytest.mark.parametrize("case", CASES)
def test_sc1_3_each_member_calls_its_agent_with_the_type_model_and_effort_it_was_given(
        tmp_path, case):
    out = run_member(tmp_path, case, ARGS[case])
    assert len(out["calls"]) == 1
    options = out["calls"][0]["opts"]
    assert options.get("agentType") == TYPE, options
    assert options.get("model") == "m-from-args" and options.get("effort") == "e-from-args", options
    assert f"u1: {MISSING}" not in out["logs"]
