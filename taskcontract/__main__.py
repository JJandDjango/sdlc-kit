"""python -m taskcontract - CLI for the G0.1 definition-of-ready check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .checker import PROFILES, load_schema, validate_path


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
    args = parser.parse_args(argv)

    schema_doc = load_schema(args.schema)
    violations = []
    for file in args.files:
        violations.extend(validate_path(file, profile=args.profile, schema_doc=schema_doc))

    if args.as_json:
        print(json.dumps([vars(v) for v in violations], indent=2))
    else:
        for violation in violations:
            print(violation.line)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
