"""Four-vector suppression audit - G4.10's diff-scoped subject check.

The candidate diff may introduce no new weakening of any gating
constraint. Four ecosystem-free vectors, bound here for the dotnet
profile (construct lists are binding material - they grow per real
defect data, never silently):

  V1  in-source suppression constructs (.cs)
  V2  severity downgrades in analysis config (.editorconfig/.globalconfig)
  V3  strictness-flag weakening in build config (.props/.csproj/.targets)
  V4  exclusion-scope widening (generated-code globs, coverage
      exclusions, quarantine-list additions)

V2 trips on a removed->added pair that lowers a rule's severity, and on
an unpaired added severity at none/silent/suggestion; an unpaired added
warning/error passes (tightening is never a finding). Every diagnostic
names the construct, the location, and the legitimate channel - the
routing line is the anti-gaming instrument, not just "no".

Base resolution when --base is absent reads the Actions event
(GITHUB_EVENT_PATH): pull_request.base.sha, merge_group.base_sha, or
push `before`. Exit codes follow the house audit convention:
0 clean, 1 findings, 2 environment/usage error.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import PurePosixPath

SEVERITY_ORDER = {"error": 4, "warning": 3, "suggestion": 2, "silent": 1,
                  "refactoring": 1, "none": 0}
WEAK_SEVERITIES = {"none", "silent", "refactoring", "suggestion"}

ROUTE = {
    1: ("remove the suppression, or route a permanent exception through "
        "the committed class-E suppression config (PL-PIPE.1)"),
    2: "severity policy is enforcement-layer config - PL-PIPE.1 second channel",
    3: "strictness flags are enforcement-layer config - PL-PIPE.1 second channel",
    4: "exclusion scope is enforcement-layer config - PL-PIPE.1 second channel",
}

# V1 - in-source suppression constructs (C# sources).
V1_PATTERNS = (
    (re.compile(r"#pragma\s+warning\s+disable"), "#pragma warning disable"),
    (re.compile(r"\[(?:assembly:\s*)?SuppressMessage"), "[SuppressMessage]"),
    (re.compile(r"//\s*Stryker\s+disable", re.IGNORECASE), "Stryker disable comment"),
    (re.compile(r"\bSkip\s*=\s*\""), "test Skip="),
    (re.compile(r"\[Ignore[\](]"), "[Ignore] test attribute"),
)

# V2 - severity assignment in analysis config.
V2_SEVERITY = re.compile(
    r"^\s*(?P<key>dotnet_(?:analyzer_)?diagnostic\.[\w.-]+\.severity|"
    r"dotnet_analyzer_diagnostic\.severity)\s*=\s*(?P<value>\w+)")

# V3 - strictness-flag weakening in MSBuild config (flag -> weak values).
V3_WEAK_FLAGS = {
    "TreatWarningsAsErrors": {"false"},
    "Nullable": {"disable", "annotations", "warnings"},
    "CheckForOverflowUnderflow": {"false"},
    "AllowUnsafeBlocks": {"true"},
    "EnforceCodeStyleInBuild": {"false"},
    "RunAnalyzersDuringBuild": {"false"},
    "RunAnalyzers": {"false"},
    "NuGetAudit": {"false"},
    "RestorePackagesWithLockFile": {"false"},
    "AnalysisLevel": {"none", "latest-minimum", "latest-recommended",
                      "minimum", "recommended"},
}
V3_ELEMENT = re.compile(r"<(?P<flag>\w+)>\s*(?P<value>[\w.-]+)\s*</")
V3_NOWARN = re.compile(r"<NoWarn>")

# V4 - exclusion-scope widening.
V4_PATTERNS = (
    (re.compile(r"^\s*generated_code\s*=\s*true"), "generated_code = true"),
    (re.compile(r"\[ExcludeFromCodeCoverage"), "[ExcludeFromCodeCoverage]"),
)

CS_SUFFIXES = {".cs"}
# .editorconfig at any depth is a bare dotfile (no suffix in pathlib's
# model); named variants like rules.globalconfig arrive as suffixes.
ANALYSIS_CONFIG_NAMES = {".editorconfig", ".globalconfig"}
BUILD_CONFIG_SUFFIXES = {".props", ".csproj", ".targets"}


@dataclass(frozen=True)
class Finding:
    file: str
    line_no: int
    vector: int
    construct: str
    detail: str = ""

    @property
    def line(self) -> str:
        detail = f" {self.detail}" if self.detail else ""
        return (f"G410-V{self.vector} {self.file}:{self.line_no}: "
                f"{self.construct}{detail} - route: {ROUTE[self.vector]}")


@dataclass(frozen=True)
class DiffLine:
    path: str
    line_no: int
    text: str


def parse_diff(diff_text: str):
    """Split a unified diff into (added, removed) DiffLine lists.

    Added lines carry new-file line numbers from the hunk headers;
    removed lines carry the old numbers. Binary files contribute
    nothing; deletions land under /dev/null and are dropped.
    """
    added: list[DiffLine] = []
    removed: list[DiffLine] = []
    path = None
    new_no = old_no = 0
    for raw in diff_text.splitlines():
        if raw.startswith("+++ "):
            target = raw[4:].strip()
            path = None if target == "/dev/null" else target.partition("b/")[2] or target
            continue
        if raw.startswith("@@"):
            match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
            if match:
                old_no, new_no = int(match.group(1)), int(match.group(2))
            continue
        if path is None:
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            added.append(DiffLine(path, new_no, raw[1:]))
            new_no += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            removed.append(DiffLine(path, old_no, raw[1:]))
            old_no += 1
        elif not raw.startswith("\\"):
            new_no += 1
            old_no += 1
    return added, removed


def _suffix(path: str) -> str:
    return PurePosixPath(path).suffix.lower()


def _name(path: str) -> str:
    return PurePosixPath(path).name.lower()


def _is_analysis_config(path: str) -> bool:
    return _name(path) in ANALYSIS_CONFIG_NAMES or \
        _suffix(path) in ANALYSIS_CONFIG_NAMES


def _severities(lines) -> dict[tuple[str, str], str]:
    out: dict[tuple[str, str], str] = {}
    for entry in lines:
        if not _is_analysis_config(entry.path):
            continue
        match = V2_SEVERITY.match(entry.text)
        if match:
            out[(entry.path, match.group("key"))] = match.group("value").lower()
    return out


def audit_diff_text(diff_text: str) -> list[Finding]:
    """The four vectors over one unified diff. Pure - no git, no env."""
    added, removed = parse_diff(diff_text)
    findings: list[Finding] = []
    removed_severities = _severities(removed)

    for entry in added:
        suffix, name = _suffix(entry.path), _name(entry.path)

        if suffix in CS_SUFFIXES:
            if name == "globalsuppressions.cs":
                findings.append(Finding(entry.path, entry.line_no, 1,
                                        "GlobalSuppressions.cs addition"))
            else:
                for pattern, construct in V1_PATTERNS:
                    if pattern.search(entry.text):
                        findings.append(Finding(entry.path, entry.line_no, 1,
                                                construct))
            for pattern, construct in V4_PATTERNS:
                if pattern.search(entry.text) and construct.startswith("[Exclude"):
                    findings.append(Finding(entry.path, entry.line_no, 4,
                                            construct))

        elif _is_analysis_config(entry.path):
            match = V2_SEVERITY.match(entry.text)
            if match:
                key, value = match.group("key"), match.group("value").lower()
                prior = removed_severities.get((entry.path, key))
                if prior is not None and SEVERITY_ORDER.get(value, 0) < \
                        SEVERITY_ORDER.get(prior, 0):
                    findings.append(Finding(
                        entry.path, entry.line_no, 2, key,
                        f"downgraded {prior} -> {value}"))
                elif prior is None and value in WEAK_SEVERITIES:
                    findings.append(Finding(
                        entry.path, entry.line_no, 2, key,
                        f"introduced at {value}"))
            for pattern, construct in V4_PATTERNS:
                if pattern.search(entry.text) and construct.startswith("generated"):
                    findings.append(Finding(entry.path, entry.line_no, 4,
                                            construct))

        elif suffix in BUILD_CONFIG_SUFFIXES:
            if V3_NOWARN.search(entry.text):
                findings.append(Finding(entry.path, entry.line_no, 3,
                                        "<NoWarn> addition"))
            match = V3_ELEMENT.search(entry.text)
            if match:
                flag, value = match.group("flag"), match.group("value").lower()
                if value in V3_WEAK_FLAGS.get(flag, ()):
                    findings.append(Finding(
                        entry.path, entry.line_no, 3,
                        f"<{flag}>{match.group('value')}"))

        if "quarantine" in name:
            findings.append(Finding(entry.path, entry.line_no, 4,
                                    "quarantine-list addition"))

    return findings


def resolve_base(environ=os.environ) -> str:
    """The diff base from the Actions event when no --base is given."""
    event_path = environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        raise ValueError(
            "no --base given and no Actions event to read "
            "(GITHUB_EVENT_PATH unset) - pass --base <sha>")
    with open(event_path, encoding="utf-8") as fh:
        event = json.load(fh)
    base = (event.get("pull_request", {}).get("base", {}).get("sha")
            or event.get("merge_group", {}).get("base_sha")
            or event.get("before"))
    if not base or set(base) == {"0"}:
        raise ValueError(
            "the Actions event carries no diffable base - pass --base <sha>")
    return base


def run_git_diff(repo: str, base: str, head: str) -> str:
    result = subprocess.run(
        ["git", "-C", repo, "diff", "--no-color", "--unified=0",
         f"{base}..{head}"],
        capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"git diff failed: {result.stderr.strip()}")
    return result.stdout


def main_audit(args) -> int:
    try:
        base = args.base or resolve_base()
        diff_text = run_git_diff(args.repo, base, args.head)
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"taskcontract suppression-audit: {exc}")
        return 2

    findings = audit_diff_text(diff_text)
    if args.as_json:
        print(json.dumps([vars(f) for f in findings], indent=2))
    else:
        for finding in findings:
            print(finding.line)
        if not findings:
            print(f"suppression-green: {base[:12]}..{args.head} "
                  "(no new weakening on any vector)")
    return 1 if findings else 0
