"""python -m taskcontract - CLI for the G0.1 definition-of-ready check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .checker import PROFILES, load_schema, validate_path
from .graph import main_graph
from .lang import main_lang_check, main_lang_extract
from .progress import RUNS, main_progress
from .scaffold import scaffold
from .scope_check import main_scope_check
from .suppression_audit import main_audit
from .tree_view import main_tree
from .vocabulary import (VOCAB_DIR, list_terms, load_glossary_schema,
                         registry_size, scaffold_term, validate_vocab_root)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="taskcontract",
        description="Validate task contracts (G0.1 definition-of-ready, ADR 0006).",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    val = sub.add_parser("validate", help="validate task-contract files")
    val.add_argument("files", nargs="+", help="contract files (YAML or JSON)")
    val.add_argument("--profile", choices=PROFILES, default="ready",
                     help="ready = the G0.1 gate (default); draft admits blocked dependencies")
    val.add_argument("--json", action="store_true", dest="as_json",
                     help="emit violations as a JSON array (the agent loop substrate)")
    val.add_argument("--schema", type=Path, default=None,
                     help="override the packaged schema file")
    new = sub.add_parser("new", help="scaffold a red contract skeleton at specs/<id>/contract.yaml (F11)")
    new.add_argument("id", help="task id (schema pattern: lowercase, digits, hyphens)")
    new.add_argument("--root", type=Path, default=Path("."),
                     help="repo root that holds specs/ (default: cwd)")
    vocab = sub.add_parser("vocab-check",
                           help="validate the specs/vocabulary/ glossary at the door (ADR 0017)")
    vocab.add_argument("--root", type=Path, default=Path("."),
                       help="repo root that holds specs/ (default: cwd)")
    vocab.add_argument("--json", action="store_true", dest="as_json",
                       help="emit violations as a JSON array (the agent loop substrate)")
    vocab.add_argument("--schema", type=Path, default=None,
                       help="override the packaged glossary schema file")
    vlist = sub.add_parser("vocab-list",
                           help="computed glossary listing - no stored index (ADR 0017 V5)")
    vlist.add_argument("--root", type=Path, default=Path("."),
                       help="repo root that holds specs/ (default: cwd)")
    vadd = sub.add_parser("vocab-add",
                          help="scaffold a draft term skeleton at specs/vocabulary/<slug>.yaml")
    vadd.add_argument("slug", help="term slug (schema pattern: lowercase, digits, hyphens)")
    vadd.add_argument("--root", type=Path, default=Path("."),
                      help="repo root that holds specs/ (default: cwd)")
    lang = sub.add_parser(
        "lang-check",
        help="controlled-language door: tier-1 rules over registry-bound "
             "prose fields (form checked; meaning not checked)")
    lang.add_argument("--root", type=Path, default=Path("."),
                      help="repo root that holds specs/ (default: cwd)")
    lang.add_argument("--json", action="store_true", dest="as_json",
                      help="emit findings in the note+findings envelope")
    lang.add_argument("--schema", type=Path, default=None,
                      help="override the packaged dictionary schema file")
    lext = sub.add_parser(
        "lang-extract",
        help="report-only calibration harvest: candidate words, banned hits, "
             "per-contract census; writes nothing")
    lext.add_argument("--root", type=Path, default=Path("."),
                      help="repo root that holds specs/ (default: cwd)")
    graph = sub.add_parser(
        "graph",
        help="render one contract's unit dependency graph as Mermaid (ADR 0024)")
    graph.add_argument("file", help="contract file (YAML or JSON)")
    tree = sub.add_parser(
        "tree",
        help="print the work as one tree, derived from the repo's files at each run (ADR 0031)")
    tree.add_argument("--root", type=Path, default=Path("."),
                      help="repo root that holds specs/ and .sdlc/ (default: cwd)")
    progress = sub.add_parser(
        "progress",
        help="record the work's progress under .sdlc/progress/ (ADR 0031)")
    actions = progress.add_subparsers(dest="action", required=True)
    run = actions.add_parser(
        "run",
        help="run a check's command and record red or green beside what it expected")
    run.add_argument("check", help="the check's id, as the tree prints it")
    run.add_argument("--expect", choices=RUNS, default="green",
                     help="the result the run should give (default: green)")
    run.add_argument("--root", type=Path, default=Path("."),
                     help="repo root that holds specs/ and .sdlc/ (default: cwd)")
    run.add_argument("argv", nargs="+", metavar="COMMAND",
                     help="the command and its arguments, after --")
    audit = sub.add_parser(
        "suppression-audit",
        help="G4.10 four-vector diff check: no new weakening of gating constraints")
    audit.add_argument("--base", default=None,
                       help="diff base sha (default: resolved from the Actions event)")
    audit.add_argument("--head", default="HEAD",
                       help="diff head (default: HEAD)")
    audit.add_argument("--repo", default=".",
                       help="repository to diff (default: cwd)")
    audit.add_argument("--json", action="store_true", dest="as_json",
                       help="emit findings as a JSON array (the agent loop substrate)")
    scope = sub.add_parser(
        "scope-check",
        help="G4.12: every commit in the range stays within the scope of the "
             "contract its Contract: trailer names")
    scope.add_argument("--base", default=None,
                       help="range base sha (default: resolved from the Actions event)")
    scope.add_argument("--head", default="HEAD",
                       help="range head (default: HEAD)")
    scope.add_argument("--root", default=".",
                       help="repo root that holds specs/ and .sdlc/ (default: cwd)")
    scope.add_argument("--json", action="store_true", dest="as_json",
                       help="emit findings in the note+findings envelope")
    args = parser.parse_args(argv)

    if args.command == "graph":
        return main_graph(args)

    if args.command == "tree":
        return main_tree(args)

    if args.command == "progress":
        return main_progress(args)

    if args.command == "suppression-audit":
        return main_audit(args)

    if args.command == "scope-check":
        return main_scope_check(args)

    if args.command == "lang-check":
        return main_lang_check(args)

    if args.command == "lang-extract":
        return main_lang_extract(args)

    if args.command == "new":
        try:
            path = scaffold(args.id, root=args.root)
        except (ValueError, FileExistsError, OSError) as exc:
            print(f"taskcontract new: {exc}", file=sys.stderr)
            return 1
        print(f"created {path}")
        print("fill every TODO, then loop to green:")
        print(f"  python -m taskcontract validate {path} --profile ready")
        return 0

    if args.command == "vocab-add":
        try:
            path = scaffold_term(args.slug, root=args.root)
        except (ValueError, FileExistsError, OSError) as exc:
            print(f"taskcontract vocab-add: {exc}", file=sys.stderr)
            return 1
        print(f"created {path}")
        print("author the term, then loop to green:")
        print("  python -m taskcontract vocab-check")
        return 0

    if args.command == "vocab-list":
        rows, unreadable = list_terms(args.root)
        for term, kind, status, name in rows:
            print(f"{term:24} {kind:10} {status:10} {name}")
        for path in unreadable:
            print(f"unreadable: {path} (run vocab-check)")
        by_status = [sum(1 for r in rows if r[2] == s)
                     for s in ("ratified", "draft", "deprecated")]
        print(f"terms: {len(rows)} (ratified {by_status[0]}, "
              f"draft {by_status[1]}, deprecated {by_status[2]})")
        return 0

    if args.command == "vocab-check":
        schema_doc = load_glossary_schema(args.schema)
        violations, count = validate_vocab_root(args.root, schema_doc=schema_doc)
        errors = [v for v in violations if v.severity == "error"]
        if args.as_json:
            print(json.dumps([vars(v) for v in violations], indent=2))
        else:
            for violation in violations:
                print(violation.line)
            if not errors:
                state = f"{count} terms" if count else "no vocabulary here"
                entries = registry_size(args.root)
                if entries is not None:
                    state += f", registry {entries} constraints"
                print(f"vocab-green: {Path(args.root) / VOCAB_DIR} ({state})")
        return 1 if errors else 0

    schema_doc = load_schema(args.schema)
    violations = []
    for file in args.files:
        violations.extend(validate_path(file, profile=args.profile, schema_doc=schema_doc))

    errors = [v for v in violations if v.severity == "error"]
    if args.as_json:
        print(json.dumps([vars(v) for v in violations], indent=2))
    else:
        for violation in violations:
            print(violation.line)
        if not errors:
            for file in args.files:
                print(f"{args.profile}-green: {file}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
