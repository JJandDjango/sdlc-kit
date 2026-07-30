"""Report scaffold drift against the current kit templates - /sdlc update.

The committed scaffold is rendered once by init and never rewritten
(no-clobber); this engine makes the resulting drift visible when the kit
moves on. REPORT-ONLY by default: `--apply <rel>` is the single consented
write path - exactly one named kit-owned file per invocation. Merge
targets and consumer-owned files are never applied.

The consumer's tooling profile joins the comparison (ADR 0018): the
`stack:` recorded in .sdlc/config.yaml resolves the same base-plus-overlay
surface list init renders, so overlay surfaces report drift and absence in
their manifest-declared classes. No stack line or no shipped overlay =
the base surfaces exactly.

Row classes (declared in init.SURFACE_CLASSES and profile manifests):
  kit-owned      diffed against the current render; drift is applyable
                 (.github/workflows/sdlc.yml, specs/README.md)
  merge-target   diffed; drift is merged by hand (--show prints the
                 current render), never applied
                 (.pre-commit-config.yaml, .vscode/settings.json)
  consumer       born from a template, consumer-owned data thereafter -
                 existence checked, content never diffed
                 (SDLC.md, .sdlc/config.yaml, .sdlc/clocks.yaml, .sdlc/reds.yaml)
  unclassified   a template neither engine knows how to treat -
                 reported, never silently skipped

Invoked two ways:
  1. By the /sdlc skill (`/sdlc update`), or
  2. Directly:  python update.py [--cwd DIR] [--format text|json]
                                 [--apply REL | --show REL]

Exit codes:
  0 - clean (or --apply/--show succeeded)
  1 - drift or absence reported, or a refused --apply
  2 - no gate spine here, bad usage, or an unusable profile manifest
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import namedtuple
from datetime import date
from pathlib import Path


def _load_init():
    path = Path(__file__).parent / "init.py"
    spec = importlib.util.spec_from_file_location("sdlc_skill_init_for_update", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INIT = _load_init()

# The date stamped at render time is legitimate per-consumer variance,
# not drift: it is compared as a wildcard, every other variable as the
# current kit truth. The consumer's stack is read from .sdlc/config.yaml
# and compared as a real value.
DATE_SENTINEL = "@@DATE@@"

STATUS_RANK = {"drift": 0, "absent": 0, "unrenderable": 0, "ok": 1, "data": 2}

Row = namedtuple("Row", ["status", "klass", "path", "note"])


def read_stack(cwd: Path) -> str:
    """The consumer's recorded stack; '' when config or the line is absent."""
    config = cwd / ".sdlc" / "config.yaml"
    if not config.is_file():
        return ""
    match = re.search(r"^stack:\s*['\"]?([^'\"#\s]+)",
                      config.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else ""


def _compare_vars(stack: str) -> dict:
    return {
        "date": DATE_SENTINEL,
        "stack": stack,
        "kit_repo": INIT.KIT_REPO,
        "kit_ref": INIT.KIT_REF,
        "schema_url": INIT.SCHEMA_URL,
    }


def _render(surface, variables: dict) -> str | None:
    """Render one surface; None when it needs a variable we cannot supply."""
    text = surface.path.read_text(encoding="utf-8")
    try:
        return INIT.substitute(text, variables)
    except KeyError:
        return None


def _matches(rendered: str, target_text: str) -> bool:
    """Line-wise equality with the date sentinel matching anything."""
    rendered_lines = rendered.splitlines()
    target_lines = target_text.splitlines()
    if len(rendered_lines) != len(target_lines):
        return False
    for expected, actual in zip(rendered_lines, target_lines):
        if DATE_SENTINEL in expected:
            parts = [re.escape(p) for p in expected.split(DATE_SENTINEL)]
            if not re.fullmatch(".+".join(parts), actual):
                return False
        elif expected != actual:
            return False
    return True


def scan(cwd: Path, templates_dir: Path, stack: str) -> tuple[list[Row], bool]:
    """Scan every scaffold surface. Returns (rows, is_spine)."""
    is_spine = (cwd / ".sdlc").is_dir() or (cwd / "SDLC.md").is_file()
    if not is_spine:
        return [], False

    variables = _compare_vars(stack)
    rows: list[Row] = []
    for surface in INIT.resolve_surfaces(templates_dir, stack):
        target = cwd / surface.target
        if not target.is_file():
            rows.append(Row("absent", surface.klass, surface.target,
                            "restore it or re-run /sdlc init (no-clobber)"))
            continue
        if surface.klass == "consumer":
            rows.append(Row("data", surface.klass, surface.target,
                            "existence only - never diffed"))
            continue
        rendered = _render(surface, variables)
        if rendered is None:
            rows.append(Row("unrenderable", surface.klass, surface.target,
                            "template needs interview answers - review by hand"))
            continue
        if _matches(rendered, target.read_text(encoding="utf-8")):
            rows.append(Row("ok", surface.klass, surface.target, ""))
        elif surface.klass == "kit-owned":
            rows.append(Row("drift", surface.klass, surface.target,
                            f"differs from the v{INIT.KIT_VERSION} render (--apply {surface.target})"))
        else:
            rows.append(Row("drift", surface.klass, surface.target,
                            f"differs - merge by hand (--show {surface.target}); never auto-applied"))
    rows.sort(key=lambda r: (STATUS_RANK[r.status], r.klass, r.path))
    return rows, True


def _surface_for_rel(templates_dir: Path, stack: str, rel: str):
    for surface in INIT.resolve_surfaces(templates_dir, stack):
        if surface.target == rel:
            return surface
    return None


def apply_one(cwd: Path, templates_dir: Path, stack: str, rel: str) -> tuple[bool, str]:
    """Overwrite one kit-owned target with the current render. Consent is
    the invocation itself: the user named exactly this file."""
    surface = _surface_for_rel(templates_dir, stack, rel)
    if surface is None:
        return False, f"refused: {rel} is not a scaffold surface"
    if surface.klass != "kit-owned":
        return False, (f"refused: {rel} is {surface.klass} - "
                       f"{'merge it by hand (--show prints the render)' if surface.klass == 'merge-target' else 'consumer-owned; the kit never rewrites it'}")
    variables = dict(_compare_vars(stack), date=date.today().isoformat())
    rendered = _render(surface, variables)
    if rendered is None:
        return False, f"refused: {surface.name} needs interview answers"
    target = cwd / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    return True, f"applied  {rel}  (v{INIT.KIT_VERSION} render)"


def show_one(templates_dir: Path, stack: str, rel: str) -> tuple[bool, str]:
    surface = _surface_for_rel(templates_dir, stack, rel)
    if surface is None:
        return False, f"refused: {rel} is not a scaffold surface"
    variables = dict(_compare_vars(stack), date=date.today().isoformat())
    rendered = _render(surface, variables)
    if rendered is None:
        return False, f"refused: {surface.name} needs interview answers"
    return True, rendered.rstrip("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report committed-scaffold drift against the current kit (report-only)."
    )
    parser.add_argument("--cwd", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--apply", metavar="REL",
                        help="Overwrite exactly this kit-owned file with the current render.")
    parser.add_argument("--show", metavar="REL",
                        help="Print the current render of this scaffold surface.")
    args = parser.parse_args(argv)

    cwd = Path(args.cwd).resolve()
    templates_dir = Path(__file__).parent / "templates"
    stack = read_stack(cwd)

    if args.apply and args.show:
        print("ERROR: --apply and --show are mutually exclusive", file=sys.stderr)
        return 2

    try:
        if args.show:
            ok, message = show_one(templates_dir, stack, args.show)
            print(message)
            return 0 if ok else 1

        if args.apply:
            ok, message = apply_one(cwd, templates_dir, stack, args.apply)
            print(message, file=None if ok else sys.stderr)
            return 0 if ok else 1

        rows, is_spine = scan(cwd, templates_dir, stack)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not is_spine:
        print("No SDLC gate spine here (no .sdlc/ and no SDLC.md) - run /sdlc to initialize.",
              file=sys.stderr)
        return 2

    attention = [r for r in rows if STATUS_RANK[r.status] == 0]
    if args.format == "json":
        print(json.dumps([r._asdict() for r in rows], indent=2))
    else:
        for r in rows:
            note = f"  ({r.note})" if r.note else ""
            print(f"{r.status:12} {r.klass:13} {r.path}{note}")
        if attention:
            print(f"{len(attention)} surface(s) drifted or absent - apply is per-file and consented")
        else:
            print(f"scaffold current - matches the v{INIT.KIT_VERSION} render")
    return 1 if attention else 0


if __name__ == "__main__":
    sys.exit(main())
