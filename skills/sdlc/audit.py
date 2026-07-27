"""Audit an SDLC gate spine - report-only health check for /sdlc audit.

Deterministic, REPORT-ONLY: audit never writes, creates, or modifies
anything. Detection is automated; fixes stay with the user (or the
contract flow). Stdlib-only at import; PyYAML and the taskcontract
package are probed at run time - absence is a *finding* with the install
hint, never a crash.

Invoked two ways:
  1. By the /sdlc skill (`/sdlc audit`), or
  2. Directly:  python audit.py [--cwd DIR] [--format text|json]

Exit codes:
  0 - clean (INFO findings allowed)
  1 - at least one WARN or ERROR finding
  2 - no gate spine here (no .sdlc/ and no SDLC.md), or bad usage

Finding codes:
  SPINE-MISSING     a payload surface is absent (.sdlc/*, SDLC.md,
                    specs/README.md, the CI workflow)
  KIT-MISSING       PyYAML / taskcontract unavailable - parse and contract
                    checks skipped (install: pip install "git+https://github.com/JJandDjango/sdlc-kit.git")
  CONFIG-PARSE      .sdlc/config.yaml is not valid YAML          (ERROR)
  CONFIG-KEYS       config lacks kit / material / stack / active_gates
  CLOCKS-PARSE      .sdlc/clocks.yaml is not valid YAML          (ERROR)
  REDS-PARSE        .sdlc/reds.yaml is not valid YAML            (ERROR)
  REDS-SCHEMA       a reds entry lacks the ledger fields
                    {id, condition, class, clock_origin, window, status}
  CONTRACT-INVALID  a specs/*/contract.yaml fails the ready profile (ERROR)
  CONTRACT-PARKED   a contract fails ready ONLY on unresolved
                    dependencies (TC003) - a legal parked draft   (INFO)
  CONTRACT-ORPHAN   a specs/<dir>/ carries no contract.yaml
  ID-MISMATCH       a contract's id differs from its directory name
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import namedtuple
from pathlib import Path

SEVERITY_RANK = {"ERROR": 0, "WARN": 1, "INFO": 2}

PIP_HINT = 'pip install "git+https://github.com/JJandDjango/sdlc-kit.git"'

SURFACES = (
    "SDLC.md",
    ".sdlc/config.yaml",
    ".sdlc/clocks.yaml",
    ".sdlc/reds.yaml",
    "specs/README.md",
    ".github/workflows/sdlc.yml",
)

CONFIG_KEYS = ("kit", "material", "stack", "active_gates")
REDS_ENTRY_KEYS = ("id", "condition", "class", "clock_origin", "window", "status")

Finding = namedtuple("Finding", ["severity", "code", "message", "path"])


def _yaml_module():
    try:
        import yaml
        return yaml
    except ImportError:
        return None


def _taskcontract():
    try:
        from taskcontract.checker import load_schema, validate_path
        return load_schema, validate_path
    except ImportError:
        return None


def _check_surfaces(cwd: Path, findings: list[Finding]) -> None:
    for rel in SURFACES:
        if not (cwd / rel).is_file():
            findings.append(Finding("WARN", "SPINE-MISSING", f"{rel} is absent", rel))


def _load_yaml(cwd: Path, rel: str, code: str, yaml, findings: list[Finding]):
    path = cwd / rel
    if not path.is_file():
        return None  # SPINE-MISSING already covers absence
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # yaml.YAMLError or OSError
        findings.append(Finding("ERROR", code, f"{rel} does not parse: {exc}", rel))
        return None


def _check_yaml_surfaces(cwd: Path, findings: list[Finding]) -> None:
    yaml = _yaml_module()
    if yaml is None:
        findings.append(Finding("WARN", "KIT-MISSING",
                                f"PyYAML unavailable - parse checks skipped ({PIP_HINT})", ""))
        return

    config = _load_yaml(cwd, ".sdlc/config.yaml", "CONFIG-PARSE", yaml, findings)
    if isinstance(config, dict):
        missing = [k for k in CONFIG_KEYS if k not in config]
        if missing:
            findings.append(Finding("WARN", "CONFIG-KEYS",
                                    f"config lacks {missing}", ".sdlc/config.yaml"))

    _load_yaml(cwd, ".sdlc/clocks.yaml", "CLOCKS-PARSE", yaml, findings)

    reds = _load_yaml(cwd, ".sdlc/reds.yaml", "REDS-PARSE", yaml, findings)
    if reds is not None:
        entries = reds.get("reds") if isinstance(reds, dict) else None
        if not isinstance(entries, list):
            findings.append(Finding("WARN", "REDS-SCHEMA",
                                    "reds.yaml must carry a top-level `reds:` list",
                                    ".sdlc/reds.yaml"))
        else:
            for i, entry in enumerate(entries):
                missing = ([k for k in REDS_ENTRY_KEYS if k not in entry]
                           if isinstance(entry, dict) else list(REDS_ENTRY_KEYS))
                if missing:
                    findings.append(Finding("WARN", "REDS-SCHEMA",
                                            f"reds[{i}] lacks {missing}", ".sdlc/reds.yaml"))


def _check_contracts(cwd: Path, findings: list[Finding]) -> None:
    specs = cwd / "specs"
    if not specs.is_dir():
        return

    task_dirs = sorted(d for d in specs.iterdir() if d.is_dir())
    contracts = [d / "contract.yaml" for d in task_dirs]
    for d, contract in zip(task_dirs, contracts):
        if not contract.is_file():
            findings.append(Finding("WARN", "CONTRACT-ORPHAN",
                                    f"specs/{d.name}/ carries no contract.yaml",
                                    f"specs/{d.name}"))

    present = [c for c in contracts if c.is_file()]
    if not present:
        return

    tc = _taskcontract()
    if tc is None:
        findings.append(Finding("WARN", "KIT-MISSING",
                                f"taskcontract unavailable - contract checks skipped ({PIP_HINT})", ""))
        return
    load_schema, validate_path = tc
    schema_doc = load_schema()
    yaml = _yaml_module()

    for contract in present:
        rel = contract.relative_to(cwd).as_posix()
        violations = validate_path(contract, profile="ready", schema_doc=schema_doc)
        rules = {v.rule for v in violations}
        if violations and rules == {"TC003"}:
            blockers = "; ".join(v.message for v in violations)
            findings.append(Finding("INFO", "CONTRACT-PARKED",
                                    f"legal draft parked on {blockers}", rel))
        elif violations:
            head = "; ".join(f"{v.rule} {v.message}" for v in violations[:3])
            more = f" (+{len(violations) - 3} more)" if len(violations) > 3 else ""
            findings.append(Finding("ERROR", "CONTRACT-INVALID", head + more, rel))

        if yaml is not None:
            try:
                doc = yaml.safe_load(contract.read_text(encoding="utf-8"))
            except Exception:
                doc = None  # TC000 already reported by validate_path
            if isinstance(doc, dict) and doc.get("id") not in (None, contract.parent.name):
                findings.append(Finding("WARN", "ID-MISMATCH",
                                        f"contract id {doc.get('id')!r} != directory "
                                        f"{contract.parent.name!r}", rel))


def audit(cwd: Path) -> tuple[list[Finding], bool]:
    """Run every check. Returns (findings, is_spine)."""
    is_spine = (cwd / ".sdlc").is_dir() or (cwd / "SDLC.md").is_file()
    if not is_spine:
        return [], False

    findings: list[Finding] = []
    _check_surfaces(cwd, findings)
    _check_yaml_surfaces(cwd, findings)
    _check_contracts(cwd, findings)
    findings.sort(key=lambda f: (SEVERITY_RANK[f.severity], f.code, f.path))
    return findings, True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit an SDLC gate spine (report-only)."
    )
    parser.add_argument("--cwd", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    cwd = Path(args.cwd).resolve()
    findings, is_spine = audit(cwd)

    if not is_spine:
        print("No SDLC gate spine here (no .sdlc/ and no SDLC.md) - run /sdlc to initialize.",
              file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        for f in findings:
            location = f" [{f.path}]" if f.path else ""
            print(f"{f.severity:5}  {f.code:16} {f.message}{location}")
        worst = [f for f in findings if f.severity in ("ERROR", "WARN")]
        if not findings:
            print("clean - no findings")
        elif not worst:
            print(f"clean - {len(findings)} informational finding(s)")
        else:
            print(f"{len(worst)} finding(s) need attention")

    return 1 if any(f.severity in ("ERROR", "WARN") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
