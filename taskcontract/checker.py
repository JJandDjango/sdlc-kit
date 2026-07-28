"""Validate task contracts against the task-contract schema (ADR 0006).

Thin wrapper over python-jsonschema: the schema file is the single source of
truth for every rule; this module only reshapes raw validation errors into
the stable per-field TCnnn diagnostics G0.1's loopability bar requires, and
enriches them with instance data (which dependency, which unit).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "task-contract.schema.json"
PROFILES = ("ready", "draft")


@dataclass(frozen=True)
class Violation:
    file: str
    path: str
    rule: str
    message: str

    @property
    def line(self) -> str:
        return f"{self.file}: {self.path}: {self.rule} {self.message}"


def load_schema(schema_path: Path | None = None) -> dict:
    return json.loads((schema_path or SCHEMA_PATH).read_text(encoding="utf-8"))


def _leaf_errors(errors):
    for err in errors:
        if err.context:
            yield from _leaf_errors(err.context)
        else:
            yield err


def _dependency(instance, err):
    """Return the dependency object an error occurred inside, if any."""
    path = list(err.absolute_path)
    if len(path) >= 2 and path[0] == "dependencies" and isinstance(path[1], int):
        deps = instance.get("dependencies") if isinstance(instance, dict) else None
        if isinstance(deps, list) and path[1] < len(deps) and isinstance(deps[path[1]], dict):
            return deps[path[1]]
    return None


def _classify(err, instance) -> tuple[str, str]:
    path = list(err.absolute_path)
    kw = err.validator
    dep = _dependency(instance, err)

    if dep is not None:
        ref = dep.get("ref", "<unnamed>")
        if kw == "const":
            blocker = dep.get("blocked_by")
            tail = f" (blocked-by: {blocker})" if blocker else ""
            return "TC003", f"dependency '{ref}' unresolved{tail}"
        return "TC008", f"malformed dependency '{ref}': {err.message}"
    if path[:1] == ["provenance"]:
        if kw == "required" and "'ref'" in err.message:
            origin = ""
            if isinstance(instance, dict) and isinstance(instance.get("provenance"), dict):
                origin = instance["provenance"].get("origin", "")
            return "TC009", f"origin '{origin}' requires ref (the escape's incident)"
        return "TC009", err.message
    if kw == "required":
        name = err.message.split("'")[1] if "'" in err.message else "?"
        return "TC001", f"missing required field '{name}'"
    if kw == "additionalProperties":
        return "TC005", err.message
    if path[:1] == ["id"] and kw == "pattern":
        return "TC006", f"id must match ^[a-z][a-z0-9-]{{2,63}}$ (got {err.instance!r})"
    if path[:1] == ["intent"] and kw in ("minLength", "maxLength"):
        return "TC007", f"intent must be 40-1200 chars (got {len(err.instance)})"
    if path and path[-1] == "acceptance_sketch" and kw in ("minItems", "maxItems"):
        return "TC004", "acceptance_sketch must carry 1-3 criteria"
    return "TC002", err.message


def validate_instance(instance, profile: str = "ready", schema_doc: dict | None = None):
    """Validate a loaded contract; return raw jsonschema errors, leaf-level."""
    doc = schema_doc or load_schema()
    validators = [Draft202012Validator(doc)]
    if profile == "ready":
        validators.append(Draft202012Validator(doc["$defs"]["ready_delta"]))
    for validator in validators:
        yield from _leaf_errors(validator.iter_errors(instance))


def validate_path(file, profile: str = "ready", schema_doc: dict | None = None) -> list[Violation]:
    """Validate one contract file; return TCnnn violations (empty = pass)."""
    name = str(file)
    try:
        instance = yaml.safe_load(Path(file).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [Violation(name, "$", "TC000", f"unreadable contract: {exc}")]

    seen: set[tuple[str, str, str]] = set()
    violations: list[Violation] = []
    for err in validate_instance(instance, profile=profile, schema_doc=schema_doc):
        rule, message = _classify(err, instance)
        key = (err.json_path, rule, message)
        if key not in seen:
            seen.add(key)
            violations.append(Violation(name, err.json_path, rule, message))
    violations.sort(key=lambda v: (v.path, v.rule))
    return violations
