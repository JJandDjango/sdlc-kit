"""Session-hook suite (contract: playbook-guardrails, unit u1-hook-script).

The hook is rendered from skills/sdlc/templates/hooks-protect-specs.py.template
and run as a subprocess the way Claude Code runs a PreToolUse hook: the
event on stdin, exit 0 to allow, exit 2 to deny with the rationale on
stderr, a systemMessage on stdout to warn. Each rule of the unit's
done_means has a case here.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import write_seat_roster

ROOT = Path(__file__).parent.parent
TEMPLATE = ROOT / "skills" / "sdlc" / "templates" / "hooks-protect-specs.py.template"
READY_CONTRACT = ROOT / "tests" / "fixtures" / "valid" / "minimal.yaml"

RATIFIED_TERM = """term: checkout
name: Checkout
definition: The step that turns a cart into an order.
kind: entity
status: ratified
since: 2026-07-01
"""
DRAFT_TERM = RATIFIED_TERM.replace("status: ratified", "status: draft")


@pytest.fixture(scope="module")
def hook_source(skill_init) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    return skill_init.substitute(text, skill_init.build_var_dict(
        {"project_name": "demo", "adoption": "greenfield", "stack": "python"},
        "2026-09-18"))


@pytest.fixture
def repo(tmp_path, hook_source) -> Path:
    """A consumer tree: a ready contract, a draft contract, two terms, the hook."""
    hook = tmp_path / ".sdlc" / "hooks" / "protect_specs.py"
    hook.parent.mkdir(parents=True)
    hook.write_text(hook_source, encoding="utf-8")
    ready = tmp_path / "specs" / "ready-task" / "contract.yaml"
    ready.parent.mkdir(parents=True)
    # Inside a specs tree a ready contract now needs the seat answer too
    # (ADR 0030 makes the roster below required, which arms TC016).
    ready.write_text(READY_CONTRACT.read_text(encoding="utf-8").replace(
        "    id: guard-empty-cart\n",
        "    id: guard-empty-cart\n    confirmed_by: [user]\n"),
        encoding="utf-8")
    draft = tmp_path / "specs" / "parked-task" / "contract.yaml"
    draft.parent.mkdir(parents=True)
    draft.write_text(READY_CONTRACT.read_text(encoding="utf-8").replace(
        "dependencies: []",
        "dependencies:\n  - ref: other-task\n    status: blocked\n    blocked_by: the other task\n"),
        encoding="utf-8")
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir()
    (vocab / "checkout.yaml").write_text(RATIFIED_TERM, encoding="utf-8")
    (vocab / "cart.yaml").write_text(DRAFT_TERM, encoding="utf-8")
    (vocab / "dictionary.yaml").write_text("class: E\nwords: []\n", encoding="utf-8")
    write_seat_roster(tmp_path)  # the ready profile needs it (ADR 0030)
    (tmp_path / "specs" / "README.md").write_text("# specs\n", encoding="utf-8")
    return tmp_path


def _run(repo: Path, rel: str, tool: str = "Edit", *, kit: bool = True,
         env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "SDLC_CONTRACT"}
    if kit:
        env["PYTHONPATH"] = str(ROOT)  # the checkout's validator, not a stale install
    else:
        # A fake package first on sys.path whose checker raises ImportError:
        # an empty package is not enough, because an editable install's
        # finder still resolves taskcontract.checker from the checkout.
        fake = repo / "fake-site" / "taskcontract"
        fake.mkdir(parents=True, exist_ok=True)
        (fake / "__init__.py").write_text("", encoding="utf-8")
        (fake / "checker.py").write_text(
            'raise ImportError("no kit present")\n', encoding="utf-8")
        env["PYTHONPATH"] = str(repo / "fake-site")
    env.update(env_extra or {})
    key = "notebook_path" if tool == "NotebookEdit" else "file_path"
    event = {"tool_name": tool, "cwd": str(repo),
             "tool_input": {key: str(repo / rel)}}
    return subprocess.run(
        [sys.executable, str(repo / ".sdlc" / "hooks" / "protect_specs.py")],
        input=json.dumps(event), capture_output=True, encoding="utf-8",
        errors="replace", cwd=repo, env=env, timeout=60)


# --- the spec channel: denials ---

def test_ready_contract_is_denied_with_the_reintake_rationale(repo):
    result = _run(repo, "specs/ready-task/contract.yaml")
    assert result.returncode == 2
    assert "validates ready" in result.stderr and "re-intakes" in result.stderr


@pytest.mark.parametrize("tool", ["Edit", "Write", "MultiEdit", "NotebookEdit"])
def test_every_covered_tool_is_denied_on_a_ready_contract(repo, tool):
    assert _run(repo, "specs/ready-task/contract.yaml", tool).returncode == 2


def test_ratified_term_is_denied_as_a_class_s_edit(repo):
    result = _run(repo, "specs/vocabulary/checkout.yaml")
    assert result.returncode == 2
    assert "is ratified" in result.stderr and "class-S" in result.stderr


@pytest.mark.parametrize("rel", ["specs/README.md", "specs/vocabulary/dictionary.yaml",
                                 "specs/new-task/notes.md"])
def test_every_other_file_under_specs_is_the_spec_channel(repo, rel):
    result = _run(repo, rel)
    assert result.returncode == 2
    assert "spec channel" in result.stderr


def test_without_the_kit_every_write_under_specs_is_denied(repo):
    for rel in ("specs/parked-task/contract.yaml", "specs/vocabulary/cart.yaml"):
        result = _run(repo, rel, kit=False)
        assert result.returncode == 2, rel
        assert "not installed" in result.stderr


# --- drafts pass ---

def test_draft_contract_and_draft_term_pass(repo):
    for rel in ("specs/parked-task/contract.yaml", "specs/vocabulary/cart.yaml"):
        result = _run(repo, rel)
        assert result.returncode == 0, (rel, result.stderr)
        assert result.stdout.strip() == ""


def test_a_new_contract_file_is_a_draft(repo):
    result = _run(repo, "specs/brand-new/contract.yaml", "Write")
    assert result.returncode == 0


# --- outside specs/: warn or stay silent ---

def test_bound_by_environment_warns_outside_scope_and_allows(repo):
    result = _run(repo, "docs/guide.md", env_extra={"SDLC_CONTRACT": "ready-task"})
    assert result.returncode == 0
    message = json.loads(result.stdout)["systemMessage"]
    assert message == "Warning: docs/guide.md is outside the scope of ready-task."


def test_bound_and_inside_scope_is_silent(repo):
    result = _run(repo, "checkout/cart.py", env_extra={"SDLC_CONTRACT": "ready-task"})
    assert result.returncode == 0 and result.stdout.strip() == ""


def test_scope_match_is_exact_or_glob_never_right_anchored(repo):
    contract = repo / "specs" / "ready-task" / "contract.yaml"
    text = contract.read_text(encoding="utf-8").replace(
        "scope:\n  - checkout/\n", "scope: [checkout/, USAGE.md, 'docs/*.md']\n")
    contract.write_text(text, encoding="utf-8")  # flow-style list parses too
    env = {"SDLC_CONTRACT": "ready-task"}
    assert _run(repo, "USAGE.md", env_extra=env).stdout.strip() == ""
    assert _run(repo, "docs/guide.md", env_extra=env).stdout.strip() == ""
    assert "outside the scope" in _run(repo, "sub/USAGE.md", env_extra=env).stdout


def test_unbound_session_is_silent(repo):
    result = _run(repo, "docs/guide.md")
    assert result.returncode == 0 and result.stdout.strip() == ""


def test_a_binding_that_names_no_contract_is_ignored(repo):
    result = _run(repo, "docs/guide.md", env_extra={"SDLC_CONTRACT": "nope"})
    assert result.returncode == 0 and result.stdout.strip() == ""


@pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
def test_branch_name_binds_the_session(repo):
    def git(*args):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
    git("init", "-q")
    git("checkout", "-q", "-b", "ready-task")
    result = _run(repo, "docs/guide.md")
    assert result.returncode == 0
    assert "outside the scope of ready-task" in json.loads(result.stdout)["systemMessage"]


# --- shape ---

def test_uncovered_tools_and_paths_outside_the_repo_pass(repo):
    assert _run(repo, "specs/ready-task/contract.yaml", "Bash").returncode == 0
    event = {"tool_name": "Edit", "cwd": str(repo),
             "tool_input": {"file_path": str(repo.parent / "elsewhere.txt")}}
    result = subprocess.run(
        [sys.executable, str(repo / ".sdlc" / "hooks" / "protect_specs.py")],
        input=json.dumps(event), capture_output=True, encoding="utf-8",
        cwd=repo, env={**os.environ, "PYTHONPATH": str(ROOT)}, timeout=60)
    assert result.returncode == 0


def test_managed_profile_command_runs_the_hook_only_where_it_exists(repo):
    """Unit u3-managed-settings: the org profile's guarded command."""
    profile = json.loads((ROOT / "skills" / "sdlc" / "templates" / "reference"
                          / "managed-settings.json").read_text(encoding="utf-8"))
    entry = profile["hooks"]["PreToolUse"][0]
    assert entry["matcher"] == "Edit|Write|MultiEdit|NotebookEdit"
    command = entry["hooks"][0]["command"]
    assert "protect_specs.py" in command
    assert not any(ch in command for ch in ";|&>")  # no shell chain
    event = {"tool_name": "Edit", "cwd": str(repo),
             "tool_input": {"file_path": str(repo / "specs/ready-task/contract.yaml")}}
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    denied = subprocess.run(command, shell=True, input=json.dumps(event),
                            capture_output=True, encoding="utf-8", cwd=repo,
                            env=env, timeout=60)
    assert denied.returncode == 2 and "validates ready" in denied.stderr
    bare = repo.parent / "no-kit-repo"
    bare.mkdir(exist_ok=True)
    allowed = subprocess.run(command, shell=True, input=json.dumps(event),
                             capture_output=True, encoding="utf-8", cwd=bare,
                             env=env, timeout=60)
    assert allowed.returncode == 0 and allowed.stderr.strip() == ""


def test_template_is_stdlib_only_and_substituted(hook_source):
    assert "{{" not in hook_source
    compile(hook_source, "protect_specs.py", "exec")  # a rendered hook that parses
    imports = [line for line in hook_source.splitlines()
               if line.startswith(("import ", "from "))]
    assert all("taskcontract" not in line for line in imports)  # imported lazily
    assert "from taskcontract.checker import validate_path" in hook_source
