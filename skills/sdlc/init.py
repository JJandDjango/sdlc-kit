"""Render the SDLC gate spine into a target repository.

The /sdlc skill's engine (ADR 0016): after the interview it lays down the
contract-flow payload - the gate status page, `.sdlc/` config + ledgers,
the protected `specs/` root, and the CI validate job. Zero third-party
dependencies.

Invoked two ways:
  1. By the /sdlc skill after its interview (see SKILL.md), or
  2. Directly by a human:
       python init.py --answers '{"project_name": "...", "adoption": "...", "stack": "..."}' [--cwd DIR]

Answer keys (all required):
  project_name  (str)   e.g. "billing-service"
  adoption      (str)   greenfield | brownfield
  stack         (str)   free text, e.g. "python" / "dotnet" / "typescript"

Behavior:
  - {{ var }} substitution across templates; today's date is stamped.
  - NO-CLOBBER: an existing target is skipped and reported, never overwritten.
  - MERGE TARGETS (.pre-commit-config.yaml, .vscode/settings.json): when the
    file already exists, its snippet is printed for manual merge instead of
    silently skipped - the payload still reaches the user.
  - TOOLING PROFILE (ADR 0018): the stack answer selects an overlay at
    templates/profiles/{stack}/ declared by its profile.json manifest;
    overlay entries add surfaces or replace base ones by target, under the
    same no-clobber and merge semantics. No or empty overlay = the base
    payload exactly.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import namedtuple
from datetime import date
from pathlib import Path

KIT_REPO = "https://github.com/JJandDjango/sdlc-kit"
# Pinned distribution ref (contract: distribution-reconciliation, unit
# release-tagging). Bump KIT_VERSION together with pyproject [project].version -
# tests hold the two equal - and tag v{KIT_VERSION} at the merge that ships the
# bump. Consumers upgrade by bumping the rendered ref themselves: pull, not push.
KIT_VERSION = "0.7.0"
KIT_REF = f"git+{KIT_REPO}.git@v{KIT_VERSION}"
SCHEMA_URL = ("https://raw.githubusercontent.com/JJandDjango/sdlc-kit/"
              f"v{KIT_VERSION}/taskcontract/schemas/task-contract.schema.json")

TEMPLATE_TO_TARGET = {
    "SDLC.md.template": "SDLC.md",
    "config.yaml.template": ".sdlc/config.yaml",
    "clocks.yaml.template": ".sdlc/clocks.yaml",
    "reds.yaml.template": ".sdlc/reds.yaml",
    "specs-README.md.template": "specs/README.md",
    "workflow.yml.template": ".github/workflows/sdlc.yml",
}

# Files a repo commonly already has: written only when absent, else the
# rendered snippet is printed for the user to merge by hand.
MERGE_TEMPLATE_TO_TARGET = {
    "pre-commit-config.yaml.template": ".pre-commit-config.yaml",
    "vscode-settings.json.template": ".vscode/settings.json",
}

# Drift classes consumed by update.py - the single source for both engines
# (contract: dotnet-profile-g0, unit update-parity):
#   kit-owned     diffed against the current render; drift is applyable
#   merge-target  diffed; merged by hand, never applied
#   consumer      born from a template, consumer-owned data thereafter
SURFACE_CLASSES = {
    "workflow.yml.template": "kit-owned",
    "specs-README.md.template": "kit-owned",
    "SDLC.md.template": "consumer",
    "config.yaml.template": "consumer",
    "clocks.yaml.template": "consumer",
    "reds.yaml.template": "consumer",
    "pre-commit-config.yaml.template": "merge-target",
    "vscode-settings.json.template": "merge-target",
}

PROFILE_MANIFEST = "profile.json"
PROFILE_CLASSES = {"kit-owned", "merge-target", "consumer"}

# One resolved scaffold surface: absolute template path, template name
# (manifest/classification key), target relative path, drift class.
Surface = namedtuple("Surface", ["path", "name", "target", "klass"])

REQUIRED_ANSWER_KEYS = {"project_name", "adoption", "stack"}

NEXT_STEPS = f"""
Next steps:
  1. First task: run `/sdlc intake` (or `python -m taskcontract new <id>`
     and fill the TODOs) - a task enters development only through a ready
     contract.
  2. Local validation needs the kit once:
       pip install "{KIT_REF}"
     (the scaffolded CI job installs it itself).
  3. Health check any time: `/sdlc audit` (report-only).
  4. `.sdlc/clocks.yaml` holds placeholder numbers until this repo's first
     green run calibrates them.
"""

DOTNET_NOTE = """
Note (dotnet profile): the CI job installs its own Python on the runner -
your .NET build workflow is untouched. Per-gate binding status and fit
notes: docs/dotnet-profile.md in the kit repo.
"""


def substitute(template_text: str, variables: dict) -> str:
    """Substitute {{ var }} placeholders in one pass."""
    pattern = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    def replace(match):
        key = match.group(1)
        if key not in variables:
            raise KeyError(f"Template references unknown variable: {key}")
        return str(variables[key])

    return pattern.sub(replace, template_text)


def build_var_dict(answers: dict, today: str) -> dict:
    """Validate interview answers and expand the template namespace."""
    project_name = str(answers["project_name"]).strip()
    if not project_name or "/" in project_name or "\\" in project_name:
        raise ValueError(f"project_name must be non-empty with no slashes, got {answers['project_name']!r}")
    adoption = answers["adoption"]
    if adoption not in {"greenfield", "brownfield"}:
        raise ValueError(f"adoption must be 'greenfield' or 'brownfield', got {adoption!r}")
    stack = str(answers["stack"]).strip()
    if not stack:
        raise ValueError("stack must be a non-empty string (free text)")

    return {
        "project_name": project_name,
        "adoption": adoption,
        "stack": stack,
        "date": today,
        "kit_repo": KIT_REPO,
        "kit_ref": KIT_REF,
        "schema_url": SCHEMA_URL,
    }


def load_profile(templates_dir: Path, stack: str) -> dict[str, dict]:
    """Load the stack's overlay manifest; {} when no overlay ships.

    Manifest (templates/profiles/{stack}/profile.json):
      {"templates": {"<name>.template": {"target": "<rel>", "class": <class>}}}
    """
    if not stack or not stack.strip():
        return {}
    manifest_path = templates_dir / "profiles" / stack / PROFILE_MANIFEST
    if not manifest_path.exists():
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"profile manifest unparseable: {manifest_path}: {exc}")
    entries = data.get("templates", {})
    if not isinstance(entries, dict):
        raise ValueError(f"profile manifest 'templates' must be a dict: {manifest_path}")
    for name, entry in entries.items():
        if not isinstance(entry, dict) or "target" not in entry or "class" not in entry:
            raise ValueError(f"profile manifest entry needs target + class: {stack}/{name}")
        if entry["class"] not in PROFILE_CLASSES:
            raise ValueError(
                f"profile manifest class must be one of {sorted(PROFILE_CLASSES)}: "
                f"{stack}/{name} has {entry['class']!r}")
    return entries


def resolve_surfaces(templates_dir: Path, stack: str) -> list[Surface]:
    """The full scaffold surface list: base maps, then the stack's overlay.

    An overlay entry whose target collides with a base surface replaces it
    (the profile's render wins); new targets append. Base surfaces missing
    from SURFACE_CLASSES classify as 'unclassified' - update.py's safety net.
    """
    surfaces: list[Surface] = []
    for name, target in TEMPLATE_TO_TARGET.items():
        surfaces.append(Surface(templates_dir / name, name,
                                target, SURFACE_CLASSES.get(name, "unclassified")))
    for name, target in MERGE_TEMPLATE_TO_TARGET.items():
        surfaces.append(Surface(templates_dir / name, name,
                                target, SURFACE_CLASSES.get(name, "unclassified")))
    profile_dir = templates_dir / "profiles" / stack
    for name, entry in sorted(load_profile(templates_dir, stack).items()):
        surfaces = [s for s in surfaces if s.target != entry["target"]]
        surfaces.append(Surface(profile_dir / name, name,
                                entry["target"], entry["class"]))
    return surfaces


def render_all(answers: dict, templates_dir: Path, cwd: Path, today: str):
    """Render the payload. Returns (created, skipped, merge_printouts).

    merge_printouts: [(target_rel, rendered_text)] for merge targets that
    already existed - printed, never written. No-clobber throughout.
    """
    variables = build_var_dict(answers, today)
    created: list[Path] = []
    skipped: list[Path] = []
    merge_printouts: list[tuple[str, str]] = []

    def render(surface: Surface) -> str:
        if not surface.path.exists():
            raise FileNotFoundError(f"Missing template: {surface.path}")
        return substitute(surface.path.read_text(encoding="utf-8"), variables)

    for surface in resolve_surfaces(templates_dir, variables["stack"]):
        target_path = cwd / surface.target
        if surface.klass == "merge-target":
            rendered = render(surface)
            if target_path.exists():
                merge_printouts.append((surface.target, rendered))
                continue
        else:
            if target_path.exists():
                skipped.append(target_path)
                continue
            rendered = render(surface)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(rendered, encoding="utf-8")
        created.append(target_path)

    return created, skipped, merge_printouts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the SDLC gate spine into a target repository."
    )
    parser.add_argument(
        "--answers",
        required=True,
        help=("JSON dict of interview answers. Required keys: project_name (str), "
              "adoption (greenfield|brownfield), stack (str, free text)."),
    )
    parser.add_argument(
        "--cwd",
        default=".",
        help="Target repository root (default: current directory).",
    )
    args = parser.parse_args(argv)

    try:
        answers = json.loads(args.answers)
    except json.JSONDecodeError as exc:
        print(f"ERROR: --answers is not valid JSON: {exc}", file=sys.stderr)
        return 1

    missing = REQUIRED_ANSWER_KEYS - set(answers)
    if missing:
        print(f"ERROR: missing required answer keys: {sorted(missing)}", file=sys.stderr)
        return 1

    cwd = Path(args.cwd).resolve()
    templates_dir = Path(__file__).parent / "templates"
    if not templates_dir.exists():
        print(f"ERROR: templates directory not found: {templates_dir}", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    try:
        created, skipped, merge_printouts = render_all(answers, templates_dir, cwd, today)
    except (FileNotFoundError, KeyError, TypeError, ValueError) as exc:
        print(f"ERROR: init failed: {exc}", file=sys.stderr)
        return 1

    for f in created:
        print(f"created  {f.relative_to(cwd)}")
    for f in skipped:
        print(f"skipped  {f.relative_to(cwd)}  (exists)")
    for target_rel, rendered in merge_printouts:
        print(f"\nmerge-by-hand  {target_rel}  (exists - snippet below)")
        print("-" * 60)
        print(rendered.rstrip("\n"))
        print("-" * 60)

    if not created:
        print("\nNothing new to create - the gate spine already exists here.")
    print(NEXT_STEPS.rstrip())
    if str(answers.get("stack", "")).strip() == "dotnet":
        print(DOTNET_NOTE.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
