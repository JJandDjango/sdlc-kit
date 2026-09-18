"""G4.12 scope check: the diff stays within its contract's scope.

Contract: playbook-guardrails (ADR 0027 gap 2). Every commit binds itself
to a contract with a `Contract:` git trailer, parsed like the `Theory:`
trailer. Over a range (base..head) the check reads each commit's
trailers, resolves each named contract's `scope`, and reports:

  SC001  a changed path outside the scope of the named contract(s)
  SC002  a commit with no `Contract:` trailer touching a bound path
  SC003  a `Contract:` trailer naming an id with no contract file

A path is free when it matches `scope_check.free_paths` in
.sdlc/config.yaml (default: the docs spine, the plan, the changelog,
the readme, the inbox). Free paths pass with or without a trailer.
Paths under specs/ are the spec channel: governed by the write-surface
rule and the session hook, never by this check.

Exit 0 clean, 1 findings, 2 when no base can be resolved or git fails.
`--json` emits the note+findings envelope (form checked, meaning not).
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict, dataclass
from fnmatch import fnmatch
from pathlib import Path

import yaml

from .suppression_audit import resolve_base

DEFAULT_FREE_PATHS = (
    "THEORY.md", "MAP.md", "STATE.md", "CONVENTIONS.md", "DOCS-SYSTEM.md",
    "decisions/", "docs/", "plan.md", "plan.workflow.json", "CHANGELOG.md",
    "README.md", "REQUEST_*.md", ".sdlc/",
)
SPEC_CHANNEL = "specs/"
NOTE = "form checked; meaning not checked"


@dataclass
class ScopeFinding:
    commit: str
    code: str
    path: str
    contract: str
    message: str

    @property
    def line(self) -> str:
        return f"{self.commit[:7]}: {self.code} {self.message}"


def _git(repo: str, *args: str) -> str:
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                            encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"git {args[0]} failed: {result.stderr.strip()}")
    return result.stdout


def commits_in_range(repo: str, base: str, head: str) -> list[str]:
    return [sha for sha in _git(repo, "rev-list", "--reverse",
                                f"{base}..{head}").split() if sha]


def trailers_of(repo: str, sha: str) -> list[str]:
    out = _git(repo, "show", "-s", "--format=%(trailers:key=Contract,valueonly)", sha)
    return [line.strip() for line in out.splitlines() if line.strip()]


def paths_of(repo: str, sha: str) -> list[str]:
    out = _git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", sha)
    return [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]


def free_paths(root: Path) -> list[str]:
    """`scope_check.free_paths` from .sdlc/config.yaml, else the default seed."""
    config = root / ".sdlc" / "config.yaml"
    try:
        doc = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return list(DEFAULT_FREE_PATHS)
    section = doc.get("scope_check") if isinstance(doc, dict) else None
    entries = section.get("free_paths") if isinstance(section, dict) else None
    if isinstance(entries, list) and all(isinstance(e, str) for e in entries):
        return entries
    return list(DEFAULT_FREE_PATHS)


def contract_scope(root: Path, contract_id: str) -> list[str] | None:
    """The contract's scope entries; None when no contract of that id exists."""
    path = root / "specs" / contract_id / "contract.yaml"
    if not path.is_file():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return []
    scope = doc.get("scope") if isinstance(doc, dict) else None
    return [str(entry) for entry in scope] if isinstance(scope, list) else []


def matches(path: str, entry: str) -> bool:
    entry = entry.strip().replace("\\", "/")
    if not entry:
        return False
    if entry.endswith("/"):
        return path == entry.rstrip("/") or path.startswith(entry)
    return path == entry or fnmatch(path, entry)


def in_any(path: str, entries: list[str]) -> bool:
    return any(matches(path, entry) for entry in entries)


def check_range(root: Path, base: str, head: str = "HEAD") -> list[ScopeFinding]:
    repo = str(root)
    free = free_paths(root)
    findings: list[ScopeFinding] = []
    scopes: dict[str, list[str] | None] = {}
    for sha in commits_in_range(repo, base, head):
        ids = trailers_of(repo, sha)
        paths = [p for p in paths_of(repo, sha) if not p.startswith(SPEC_CHANNEL)]
        bound: list[str] = []
        for contract_id in ids:
            if contract_id not in scopes:
                scopes[contract_id] = contract_scope(root, contract_id)
            if scopes[contract_id] is None:
                findings.append(ScopeFinding(
                    sha, "SC003", "", contract_id,
                    f"Contract trailer names {contract_id}, which has no contract"))
            else:
                bound.append(contract_id)
        for path in paths:
            if in_any(path, free):
                continue
            if not ids:
                findings.append(ScopeFinding(
                    sha, "SC002", path, "",
                    f"commit {sha[:7]} carries no Contract trailer and touches {path}"))
            elif not any(in_any(path, scopes[c] or []) for c in bound):
                named = ", ".join(ids)
                findings.append(ScopeFinding(
                    sha, "SC001", path, named,
                    f"{path} is outside the scope of {named}"))
    return findings


def main_scope_check(args) -> int:
    root = Path(args.root)
    try:
        base = args.base or resolve_base()
        findings = check_range(root, base, args.head)
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"taskcontract scope-check: {exc}")
        return 2
    if args.as_json:
        print(json.dumps({"note": NOTE, "base": base, "head": args.head,
                          "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        for finding in findings:
            print(finding.line)
        if not findings:
            print(f"scope-green: {base[:12]}..{args.head} "
                  "(every changed path inside its contract's scope or free)")
    return 1 if findings else 0
