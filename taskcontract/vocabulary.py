"""Validate the specs/vocabulary/ glossary at the door (ADR 0017 V1).

Same thin-wrapper discipline as checker.py: the glossary-term schema is
the single source of truth for per-file shape; this module reshapes raw
jsonschema errors into stable VTnnn diagnostics and adds the two checks
a per-file schema cannot express - the filename/term stable-ID rule and
relation-ref resolution across the directory (closed world at the door,
per the ADR's import ruling).
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from .checker import Violation, _leaf_errors

GLOSSARY_SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "glossary-term.schema.json"
VOCAB_DIR = Path("specs") / "vocabulary"
RESERVED_STEMS = {"constraints"}  # constraints.yaml is the registry - own schema (V6), never a term


def load_glossary_schema(schema_path: Path | None = None) -> dict:
    return json.loads((schema_path or GLOSSARY_SCHEMA_PATH).read_text(encoding="utf-8"))


DATE_FIELDS = ("since", "sunset")


def _normalized(instance):
    """YAML parses bare dates as datetime.date; the schema wants ISO strings.

    Only clean dates normalize - a full timestamp stays foreign and fails
    the date pattern, which is the intended rejection.
    """
    if isinstance(instance, dict):
        for field in DATE_FIELDS:
            value = instance.get(field)
            if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
                instance[field] = value.isoformat()
    return instance


def _forbidden_fields(err) -> list[str]:
    """Field names a failed `not: {required: [...]}` branch forbids."""
    negated = err.validator_value if isinstance(err.validator_value, dict) else {}
    required = negated.get("required", [])
    return required if isinstance(required, list) else []


def _classify(err) -> tuple[str, str]:
    path = list(err.absolute_path)
    kw = err.validator

    if kw == "required":
        name = err.message.split("'")[1] if "'" in err.message else "?"
        if name == "values":
            return "VT004", "kind 'value-set' requires values (the closed set)"
        if name == "sunset":
            return "VT007", "status 'deprecated' requires sunset (0013 pattern)"
        return "VT001", f"missing required field '{name}'"
    if kw == "not":
        forbidden = _forbidden_fields(err)
        if "values" in forbidden:
            return "VT004", "values allowed only on kind 'value-set'"
        if "sunset" in forbidden:
            return "VT007", "sunset allowed only on status 'deprecated'"
        return "VT002", err.message
    if kw == "additionalProperties":
        return "VT005", err.message
    if path[:1] == ["term"] and kw == "pattern":
        return "VT006", f"term must match ^[a-z][a-z0-9-]{{2,63}}$ (got {err.instance!r})"
    if path[:1] == ["definition"] and kw in ("minLength", "maxLength"):
        return "VT002", f"definition must be 20-1200 chars (got {len(err.instance)})"
    if path[:1] == ["relations"]:
        return "VT008", f"malformed relations: {err.message}"
    return "VT002", err.message


def validate_term_path(file, schema_doc: dict | None = None,
                       known_terms: set[str] | None = None) -> list[Violation]:
    """Validate one term file; known_terms=None skips ref resolution (single-file mode)."""
    name = str(file)
    path_obj = Path(file)
    try:
        instance = _normalized(yaml.safe_load(path_obj.read_text(encoding="utf-8")))
    except (OSError, yaml.YAMLError) as exc:
        return [Violation(name, "$", "VT000", f"unreadable term file: {exc}")]

    doc = schema_doc or load_glossary_schema()
    seen: set[tuple[str, str, str]] = set()
    violations: list[Violation] = []
    for err in _leaf_errors(Draft202012Validator(doc).iter_errors(instance)):
        rule, message = _classify(err)
        key = (err.json_path, rule, message)
        if key not in seen:
            seen.add(key)
            violations.append(Violation(name, err.json_path, rule, message))

    if isinstance(instance, dict):
        term = instance.get("term")
        if isinstance(term, str) and term != path_obj.stem:
            violations.append(Violation(
                name, "$.term", "VT003",
                f"term '{term}' must equal the filename '{path_obj.stem}' (stable-ID rule)"))
        if known_terms is not None:
            relations = instance.get("relations")
            if isinstance(relations, dict):
                for rel, refs in relations.items():
                    if not isinstance(refs, list):
                        continue
                    for ref in refs:
                        if isinstance(ref, str) and ref not in known_terms:
                            violations.append(Violation(
                                name, f"$.relations.{rel}", "VT009",
                                f"relation ref '{ref}' names no term file"))

    violations.sort(key=lambda v: (v.path, v.rule))
    return violations


def load_terms(root=Path(".")) -> dict[str, dict]:
    """Term slug -> parsed doc for every parseable term under <root>/specs/vocabulary/.

    Unreadable or non-mapping files are simply absent here - the door
    (vocab-check) is where they get reported; the join then sees their
    refs as unresolved, which is the right compound failure.
    """
    vocab = Path(root) / VOCAB_DIR
    terms: dict[str, dict] = {}
    if not vocab.is_dir():
        return terms
    for file in sorted(vocab.glob("*.yaml")):
        if file.stem in RESERVED_STEMS:
            continue
        try:
            doc = _normalized(yaml.safe_load(file.read_text(encoding="utf-8")))
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(doc, dict):
            terms[file.stem] = doc
    return terms


def coverage_join(contract_file, instance, root,
                  today: datetime.date | None = None) -> list[Violation]:
    """G0 coverage join (ADR 0017 V3): every entities ref resolves ratified-only.

    Missing and draft terms are unresolved dependencies - the remedy is a
    small vocabulary task, never failing the work itself. Deprecated terms
    warn inside their sunset window and error past it (V7c).
    """
    refs = instance.get("entities") if isinstance(instance, dict) else None
    if not isinstance(refs, list):
        return []
    name = str(contract_file)
    today = today or datetime.date.today()
    terms = load_terms(root)
    out: list[Violation] = []
    for i, ref in enumerate(refs):
        if not isinstance(ref, str):
            continue  # shape is the schema's finding, not the join's
        path = f"$.entities[{i}]"
        term = terms.get(ref)
        if term is None:
            out.append(Violation(
                name, path, "TC010",
                f"entity '{ref}' names no vocabulary term - fork a vocabulary "
                f"task (specs/vocabulary/{ref}.yaml)"))
            continue
        status = term.get("status")
        if status == "ratified":
            continue
        if status == "deprecated":
            sunset_raw = term.get("sunset")
            try:
                sunset = datetime.date.fromisoformat(str(sunset_raw))
            except (TypeError, ValueError):
                sunset = None
            if sunset is None or sunset < today:
                tail = f"sunset {sunset_raw} passed" if sunset else "sunset unknown"
                out.append(Violation(
                    name, path, "TC012", f"entity '{ref}' is deprecated ({tail})"))
            else:
                out.append(Violation(
                    name, path, "W001",
                    f"entity '{ref}' is deprecated, sunset {sunset_raw} "
                    f"(inside the notice window)", severity="warning"))
            continue
        out.append(Violation(
            name, path, "TC011",
            f"entity '{ref}' is not ratified (status: {status}) - draft does "
            f"not resolve; ratify the term or fork the vocabulary task"))
    return out


def validate_vocab_root(root=Path("."), schema_doc: dict | None = None):
    """Validate every term under <root>/specs/vocabulary/.

    Returns (violations, term_count). An absent or empty directory is
    vacuously green - the layer activates on presence, like the join.
    """
    vocab = Path(root) / VOCAB_DIR
    if not vocab.is_dir():
        return [], 0
    files = sorted(p for p in vocab.glob("*.yaml") if p.stem not in RESERVED_STEMS)
    if not files:
        return [], 0
    doc = schema_doc or load_glossary_schema()
    known = {p.stem for p in files}
    violations: list[Violation] = []
    for file in files:
        violations.extend(validate_term_path(file, schema_doc=doc, known_terms=known))
    return violations, len(files)
