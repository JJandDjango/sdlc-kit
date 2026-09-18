"""Scope-check suite (contract: playbook-guardrails, unit u4-scope-check).

A temporary git repository per test: contracts under specs/, commits that
carry (or lack) a Contract: trailer, and the check run over base..HEAD.
Each rule of the unit's done_means has a case: SC001, SC002, SC003, the
free paths, the spec channel, several trailers, the envelope, the exit
codes.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from taskcontract import scope_check
from taskcontract.__main__ import main

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")

CONTRACT = """id: {id}
intent: >
  A contract with a scope of its own, enough words to pass the door as a
  fixture for the scope check.
scope:
{scope}
non_goals:
  - nothing beyond the scope
decomposition:
  - unit: the unit
    id: the-unit
    done_means: the unit is done
    acceptance_sketch:
      - verify the unit is done
dependencies: []
provenance:
  origin: human-request
"""


class Repo:
    def __init__(self, root: Path):
        self.root = root
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, encoding="utf-8").stdout

    def contract(self, contract_id: str, *scope: str) -> None:
        path = self.root / "specs" / contract_id / "contract.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        entries = "\n".join(f"  - {s}" for s in scope)
        path.write_text(CONTRACT.format(id=contract_id, scope=entries), encoding="utf-8")

    def commit(self, files: dict[str, str], title: str, *trailers: str) -> str:
        for rel, text in files.items():
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.git("add", "-A")
        args = ["commit", "-q", "-m", title]
        if trailers:  # one final paragraph: git reads trailers from the last block only
            args += ["-m", "\n".join(trailers)]
        self.git(*args)
        return self.git("rev-parse", "HEAD").strip()


@pytest.fixture
def repo(tmp_path) -> Repo:
    r = Repo(tmp_path)
    r.contract("csv-export", "src/export/", "tests/")
    r.contract("billing", "src/billing/")
    r.base = r.commit({"README.md": "# demo\n"}, "seed")  # the contracts land here too
    return r


def _run(repo: Repo, *extra: str, capsys=None) -> int:
    return main(["scope-check", "--base", repo.base, "--root", str(repo.root), *extra])


# --- the rules ---

def test_paths_inside_the_named_scope_are_green(repo, capsys):
    repo.commit({"src/export/csv.py": "x\n", "tests/test_csv.py": "y\n"},
                "export", "Contract: csv-export")
    assert _run(repo) == 0
    assert "scope-green" in capsys.readouterr().out


def test_path_outside_scope_is_sc001_and_exit_1(repo, capsys):
    sha = repo.commit({"src/billing/invoice.py": "x\n"}, "stray", "Contract: csv-export")
    assert _run(repo) == 1
    out = capsys.readouterr().out
    assert f"{sha[:7]}: SC001 src/billing/invoice.py is outside the scope of csv-export" in out


def test_no_trailer_on_a_bound_path_is_sc002(repo, capsys):
    sha = repo.commit({"src/export/csv.py": "x\n"}, "untrailed")
    assert _run(repo) == 1
    out = capsys.readouterr().out
    assert f"SC002 commit {sha[:7]} carries no Contract trailer and touches src/export/csv.py" in out


def test_no_trailer_on_free_paths_only_is_green(repo, capsys):
    repo.commit({"README.md": "# demo 2\n", "CHANGELOG.md": "- note\n",
                 "docs/guide.md": "g\n", "plan.md": "p\n", "REQUEST_x_2026-09-18.md": "r\n"},
                "docs only")
    assert _run(repo) == 0


def test_unknown_contract_id_is_sc003(repo, capsys):
    repo.commit({"src/export/csv.py": "x\n"}, "ghost", "Contract: nope")
    assert _run(repo) == 1
    out = capsys.readouterr().out
    assert "SC003 Contract trailer names nope, which has no contract" in out
    assert "SC001" in out  # the path had no resolvable scope to be inside


def test_spec_channel_paths_are_never_in_remit(repo, capsys):
    repo.commit({"specs/csv-export/contract.yaml": "id: csv-export\n"}, "intake edit")
    assert _run(repo) == 0


def test_free_paths_come_from_config_when_declared(repo, capsys):
    (repo.root / ".sdlc").mkdir()
    (repo.root / ".sdlc" / "config.yaml").write_text(
        "kit: x\nscope_check:\n  free_paths:\n    - notes/\n    - .sdlc/\n", encoding="utf-8")
    repo.commit({"notes/a.md": "n\n"}, "notes")
    assert _run(repo) == 0
    repo.commit({"README.md": "# no longer free\n"}, "readme")
    assert _run(repo) == 1
    assert "SC002" in capsys.readouterr().out


def test_several_trailers_across_and_within_commits(repo, capsys):
    repo.commit({"src/export/csv.py": "x\n"}, "export", "Contract: csv-export")
    repo.commit({"src/billing/invoice.py": "y\n"}, "billing", "Contract: billing")
    repo.commit({"src/billing/tax.py": "z\n", "src/export/xml.py": "w\n"}, "both",
                "Contract: csv-export", "Contract: billing")
    assert _run(repo) == 0


def test_free_path_is_allowed_inside_a_bound_commit(repo, capsys):
    repo.commit({"src/export/csv.py": "x\n", "CHANGELOG.md": "- export\n"},
                "export", "Contract: csv-export")
    assert _run(repo) == 0


# --- shape ---

def test_json_envelope_names_every_finding(repo, capsys):
    repo.commit({"src/billing/invoice.py": "x\n", "lib/util.py": "u\n"},
                "stray", "Contract: csv-export")
    repo.commit({"src/export/a.py": "a\n"}, "untrailed")
    assert _run(repo, "--json") == 1
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["note"] == scope_check.NOTE
    codes = sorted(f["code"] for f in envelope["findings"])
    assert codes == ["SC001", "SC001", "SC002"]
    assert {f["path"] for f in envelope["findings"]} == {
        "src/billing/invoice.py", "lib/util.py", "src/export/a.py"}


def test_missing_base_and_git_failure_exit_2(repo, capsys, monkeypatch):
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    assert main(["scope-check", "--root", str(repo.root)]) == 2
    assert "pass --base" in capsys.readouterr().out
    assert main(["scope-check", "--base", "0000000", "--root", str(repo.root)]) == 2


ROOT = Path(__file__).parent.parent


def test_ci_step_in_the_template_and_the_kit_workflow():
    """Unit u5-ci-and-g4-12: the step rides pull requests at full depth."""
    for rel in ("skills/sdlc/templates/workflow.yml.template", ".github/workflows/sdlc.yml"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "fetch-depth: 0" in text, rel
        step = text.split("scope check (G4.12")[1]
        assert "if: github.event_name == 'pull_request'" in step, rel
        assert "run: python -m taskcontract scope-check" in step, rel


def test_g4_12_named_in_registry_deep_page_constraints_and_conventions():
    """Unit u5-ci-and-g4-12: the class-E delta, the pull merge as the record."""
    registry = (ROOT / "docs" / "gates.md").read_text(encoding="utf-8")
    assert "| G4.12 | Scope check | mechanical |" in registry
    assert "| G4 | Pre-merge CI |" in registry and "| merge to main | 12 |" in registry
    assert "57 conditions total" in registry
    deep = (ROOT / "docs" / "gates" / "G4-pre-merge-ci.md").read_text(encoding="utf-8")
    assert "### G4.12 Scope check" in deep and "SC001" in deep
    constraints = (ROOT / "specs" / "vocabulary" / "constraints.yaml").read_text(encoding="utf-8")
    assert "id: g4-12-scope-check" in constraints
    conventions = (ROOT / "CONVENTIONS.md").read_text(encoding="utf-8")
    assert "**Commits name their contract.**" in conventions


def test_matches_prefix_exact_and_glob():
    assert scope_check.matches("src/export/csv.py", "src/export/")
    assert scope_check.matches("src/export", "src/export/")
    assert not scope_check.matches("src/exporter/x.py", "src/export/")
    assert scope_check.matches("USAGE.md", "USAGE.md")
    assert not scope_check.matches("docs/USAGE.md", "USAGE.md")
    assert scope_check.matches("REQUEST_a_2026.md", "REQUEST_*.md")
