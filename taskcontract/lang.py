"""Controlled-language door + extractor (session-23 arc).

Ratified design: docs/controlled-language.md. The claim is bounded
interpretation, never determinism - form checked; meaning not checked.

lang-check - the door beside vocab-check: validates the dictionary
artifact (specs/vocabulary/dictionary.yaml) and enforces the tier-1
writing rules on the registry-bound prose fields of specs contracts.
Speaks the verdict contract: exit 0 green / 1 red with CLnnn findings;
absence of the repo dictionary is green by design (adoption pace, the
vocab-check precedent). The --json envelope carries the form-note.

lang-extract - report-only calibration: harvests candidate words with
frequencies, base banned-candidate hits, and the per-contract census
from the registry-bound fields. Writes nothing; runs before the door
arms (calibration before enforcement).

Two layers (F7): the base dictionary (function words + bans only)
rides the wheel at taskcontract/data/base_dictionary.yaml and is never
copied per repo; the domain layer is the repo artifact. The door
unions base + repo + glossary with local-glossary-shadows-base
precedence (CL013, info). Base bans are suggestions whose use_instead
is not integrity-checked - a base bump must never brick a consumer;
the repo artifact's own bans get the strict CL004/CL005 checks.

One word, one approved part of speech - tagging is dictionary lookup,
so shape rules stay decidable with stdlib string operations only.

Skip classes (never word-checked): backtick code spans, raw tokens
starting with '-' (CLI flags), tokens containing '/', '\\', '_' or
'.' (paths, identifiers), tokens containing digits (numbers, gate
IDs, diagnostic codes, versions), all-caps tokens (acronyms),
capitalized tokens off sentence start (proper names), and glossary
term names/aliases/slugs (consumed as phrases, longest first).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from .checker import Violation, _leaf_errors
from .vocabulary import VOCAB_DIR, load_terms

DICTIONARY_SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "dictionary.schema.json"
BASE_DICTIONARY_PATH = Path(__file__).resolve().parent / "data" / "base_dictionary.yaml"
DICTIONARY_FILE = VOCAB_DIR / "dictionary.yaml"

FORM_NOTE = "form checked; meaning not checked"

# Sentence caps by text type - door constants until the Q4 clocks land.
CAPS = {"descriptive": 25, "procedural": 20}
# Modal policing (procedural fields): only must-semantics belong there.
MODALS = {"should", "may", "might", "could"}
# Pronoun-subject restriction: sentence-initial approximates subject position.
PRONOUN_SUBJECTS = {"it", "this", "that", "they", "these", "those"}
# Comparatives that need a number in the same sentence.
COMPARATIVES = {"faster", "slower", "quicker", "better", "worse",
                "larger", "smaller", "higher", "lower"}
NUMBER_WORDS = {"zero", "one", "two", "three", "four", "five",
                "six", "seven", "eight", "nine", "ten"}

# Kit-default field registry - used whenever the repo artifact is absent
# (extract before seeding) and mirrored into the seeded artifact.
DEFAULT_FIELDS = (
    {"artifact": "task-contract", "path": "intent", "text_type": "descriptive"},
    {"artifact": "task-contract", "path": "scope[]", "text_type": "descriptive"},
    {"artifact": "task-contract", "path": "non_goals[]", "text_type": "descriptive"},
    {"artifact": "task-contract", "path": "decomposition[].unit", "text_type": "procedural"},
    {"artifact": "task-contract", "path": "decomposition[].done_means", "text_type": "procedural"},
    {"artifact": "task-contract", "path": "decomposition[].acceptance_sketch[]",
     "text_type": "procedural"},
)

_CODE_SPAN = re.compile(r"`[^`]*`")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_STRIP_PUNCT = "()[]{}<>.,;:!?\"'*"
_WORD = re.compile(r"[a-z][a-z-]*\Z")


def load_dictionary_schema(schema_path: Path | None = None) -> dict:
    return json.loads((schema_path or DICTIONARY_SCHEMA_PATH).read_text(encoding="utf-8"))


def load_base() -> dict:
    """The wheel-shipped base layer; missing/broken base is a packaging bug."""
    return yaml.safe_load(BASE_DICTIONARY_PATH.read_text(encoding="utf-8"))


def load_repo_dictionary(root=Path(".")):
    """(doc, violations) - doc None when absent (green) or unreadable (CL000)."""
    path = Path(root) / DICTIONARY_FILE
    if not path.is_file():
        return None, []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return None, [Violation(str(path), "$", "CL000", f"unreadable dictionary: {exc}")]
    if not isinstance(doc, dict):
        return None, [Violation(str(path), "$", "CL000", "dictionary is not a mapping")]
    return doc, []


def _glossary_surfaces(terms: dict[str, dict]) -> tuple[set[str], list[list[str]]]:
    """(single tokens, multi-word phrases) a glossary resolves in prose.

    Slugs, single-word names, and single-word aliases join the token
    set; multi-word names and aliases become phrases, consumed longest
    first before token checks.
    """
    tokens: set[str] = set()
    phrases: list[list[str]] = []
    for slug, doc in terms.items():
        tokens.add(slug)
        names = [doc.get("name")] + list(doc.get("aliases") or [])
        for name in names:
            if not isinstance(name, str) or not name.strip():
                continue
            words = name.lower().split()
            if len(words) == 1:
                tokens.add(words[0])
            else:
                phrases.append(words)
    phrases.sort(key=len, reverse=True)
    return tokens, phrases


def validate_dictionary_doc(doc: dict, name: str, terms: dict[str, dict],
                            schema_doc: dict | None = None) -> list[Violation]:
    """Artifact health: CL001 schema, CL002 duplicates, CL003 disjointness,
    CL004/CL005 use_instead integrity (repo bans only), CL013 base shadow."""
    violations: list[Violation] = []
    schema = schema_doc or load_dictionary_schema()
    seen: set[tuple[str, str]] = set()
    for err in _leaf_errors(Draft202012Validator(schema).iter_errors(doc)):
        key = (err.json_path, err.message)
        if key not in seen:
            seen.add(key)
            violations.append(Violation(name, err.json_path, "CL001", err.message))

    words = doc.get("words") if isinstance(doc.get("words"), list) else []
    bans = doc.get("banned") if isinstance(doc.get("banned"), list) else []
    glossary_tokens, glossary_phrases = _glossary_surfaces(terms)
    phrase_words = {w for phrase in glossary_phrases for w in phrase}

    approved: dict[str, str] = {}
    listed: set[str] = set()
    for i, entry in enumerate(words):
        if not isinstance(entry, dict) or not isinstance(entry.get("word"), str):
            continue
        surface = entry["word"].lower()
        if surface in listed:
            violations.append(Violation(
                name, f"$.words[{i}].word", "CL002",
                f"duplicate entry '{surface}' (one word, one meaning, one row)"))
        listed.add(surface)
        approved[surface] = str(entry.get("pos", ""))
        if surface in glossary_tokens:
            violations.append(Violation(
                name, f"$.words[{i}].word", "CL003",
                f"'{surface}' collides with a glossary term name, alias, or slug "
                f"- the glossary is the open class; keep the layers disjoint"))
    banned_surfaces: set[str] = set()
    for i, entry in enumerate(bans):
        if not isinstance(entry, dict) or not isinstance(entry.get("word"), str):
            continue
        surface = entry["word"].lower()
        if surface in listed or surface in banned_surfaces:
            violations.append(Violation(
                name, f"$.banned[{i}].word", "CL002",
                f"'{surface}' is listed twice (approved and banned, or two bans)"))
        banned_surfaces.add(surface)
        if surface in glossary_tokens:
            violations.append(Violation(
                name, f"$.banned[{i}].word", "CL003",
                f"banned '{surface}' collides with a glossary surface - deprecate "
                f"the term or drop the ban; one surface form, one owner"))
    base = load_base()
    base_words = {e["word"].lower() for e in base.get("words", [])
                  if isinstance(e, dict) and isinstance(e.get("word"), str)}
    for i, entry in enumerate(bans):
        if not isinstance(entry, dict):
            continue
        targets = entry.get("use_instead")
        if not isinstance(targets, list):
            continue
        for j, target in enumerate(targets):
            if not isinstance(target, str):
                continue
            t = target.lower()
            if t in banned_surfaces:
                violations.append(Violation(
                    name, f"$.banned[{i}].use_instead[{j}]", "CL005",
                    f"replacement '{t}' is itself banned - no ban chains"))
            elif t not in approved and t not in base_words \
                    and t not in glossary_tokens and t not in phrase_words:
                violations.append(Violation(
                    name, f"$.banned[{i}].use_instead[{j}]", "CL004",
                    f"replacement '{t}' resolves to no approved word or glossary surface"))

    for surface in sorted(base_words & glossary_tokens):
        violations.append(Violation(
            name, "$", "CL013",
            f"local glossary shadows base word '{surface}' - the term wins here",
            severity="info"))

    violations.sort(key=lambda v: (v.path, v.rule))
    return violations


def _walk_field(instance, path: str):
    """Yield (jsonpath, text) for a registry path - grammar: seg(.seg)*,
    each segment optionally suffixed [] to iterate a list."""
    def rec(node, segments, trail):
        if not segments:
            if isinstance(node, str):
                yield trail, node
            return
        seg = segments[0]
        iterate = seg.endswith("[]")
        key = seg[:-2] if iterate else seg
        if not isinstance(node, dict) or key not in node:
            return
        child = node[key]
        if iterate:
            if isinstance(child, list):
                for i, item in enumerate(child):
                    yield from rec(item, segments[1:], f"{trail}.{key}[{i}]")
        else:
            yield from rec(child, segments[1:], f"{trail}.{key}")
    yield from rec(instance, path.split("."), "$")


def _sentences(text: str) -> list[str]:
    clean = _CODE_SPAN.sub(" ", text)
    return [s for s in (_SENTENCE_END.split(clean.strip())) if s]


def _tokens(sentence: str) -> list[tuple[str, str | None]]:
    """[(raw, checkable)] - checkable None when a skip class applies;
    sentence-initial capitalized tokens normalize to lowercase."""
    out: list[tuple[str, str | None]] = []
    for raw in sentence.split():
        if raw.startswith("-"):
            out.append((raw, None))
            continue
        token = raw.strip(_STRIP_PUNCT)
        if token.endswith("'s"):
            token = token[:-2]
        if not token:
            continue
        if any(c in token for c in "/\\_.=@") or any(c.isdigit() for c in token):
            out.append((raw, None))
            continue
        bare = token.replace("-", "")
        if bare.isupper() and len(bare) >= 2:
            out.append((raw, None))
            continue
        if token[0].isupper() and out:
            out.append((raw, None))
            continue
        word = token.lower()
        out.append((raw, word if _WORD.fullmatch(word) else None))
    return out


def _consume_phrases(tokens: list[tuple[str, str | None]],
                     phrases: list[list[str]]) -> list[tuple[str, str | None]]:
    """Blank out glossary phrase matches (longest first) before word checks."""
    if not phrases:
        return tokens
    words = [t[1] for t in tokens]
    i = 0
    while i < len(words):
        for phrase in phrases:
            n = len(phrase)
            if words[i:i + n] == phrase:
                for k in range(i, i + n):
                    tokens[k] = (tokens[k][0], None)
                    words[k] = None
                i += n - 1
                break
        i += 1
    return tokens


class _Lexicon:
    """The check-time union: repo words + base words + glossary surfaces."""

    def __init__(self, repo_doc: dict | None, terms: dict[str, dict]):
        base = load_base()
        self.pos: dict[str, str] = {}
        self.banned: dict[str, tuple[list[str], str]] = {}
        for source in (base, repo_doc or {}):
            for entry in source.get("words", []) or []:
                if isinstance(entry, dict) and isinstance(entry.get("word"), str):
                    self.pos[entry["word"].lower()] = str(entry.get("pos", ""))
            for entry in source.get("banned", []) or []:
                if isinstance(entry, dict) and isinstance(entry.get("word"), str):
                    targets = [t for t in entry.get("use_instead", [])
                               if isinstance(t, str)]
                    self.banned[entry["word"].lower()] = (
                        targets, str(entry.get("reason", "")))
        self.glossary_tokens, self.phrases = _glossary_surfaces(terms)
        fields = (repo_doc or {}).get("fields")
        self.fields = fields if isinstance(fields, list) and fields else list(DEFAULT_FIELDS)
        self.exempt = {p.replace("\\", "/") for p in (repo_doc or {}).get("exempt", [])
                       if isinstance(p, str)}

    def knows(self, word: str) -> bool:
        return word in self.pos or word in self.glossary_tokens

    def is_verb(self, word: str) -> bool:
        return self.pos.get(word) == "verb"


def check_contract(file, lexicon: _Lexicon) -> list[Violation]:
    """Tier-1 rules over the registry-bound fields of one contract."""
    name = str(file)
    try:
        instance = yaml.safe_load(Path(file).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return []  # unreadable contracts are validate's finding, not the door's
    if not isinstance(instance, dict):
        return []

    violations: list[Violation] = []
    for row in lexicon.fields:
        if not isinstance(row, dict) or row.get("artifact") != "task-contract":
            continue
        text_type = str(row.get("text_type", "descriptive"))
        cap = CAPS.get(text_type, CAPS["descriptive"])
        verb_first = str(row.get("path", "")).endswith("acceptance_sketch[]")
        for jsonpath, text in _walk_field(instance, str(row.get("path", ""))):
            for sentence in _sentences(text):
                tokens = _consume_phrases(_tokens(sentence), lexicon.phrases)
                checkable = [t for t in tokens if t[1] is not None]
                if len(checkable) > cap:
                    violations.append(Violation(
                        name, jsonpath, "CL008",
                        f"sentence of {len(checkable)} words exceeds the "
                        f"{text_type} cap of {cap}"))
                first = next((t[1] for t in tokens if t[1] is not None), None)
                if first in PRONOUN_SUBJECTS:
                    violations.append(Violation(
                        name, jsonpath, "CL010",
                        f"sentence opens on pronoun '{first}' - name the subject"))
                if verb_first and first is not None and not lexicon.is_verb(first):
                    violations.append(Violation(
                        name, jsonpath, "CL012",
                        f"acceptance sketch must open with an approved verb "
                        f"(got '{first}')"))
                has_number = any(
                    (word in NUMBER_WORDS) or any(c.isdigit() for c in raw)
                    for raw, word in tokens)
                for raw, word in tokens:
                    if word is None:
                        continue
                    if word in lexicon.banned:
                        targets, reason = lexicon.banned[word]
                        tail = f" ({reason})" if reason else ""
                        hint = (f" - use instead: {', '.join(targets)}"
                                if targets else " - delete it or state the bound")
                        violations.append(Violation(
                            name, jsonpath, "CL007",
                            f"banned word '{word}'{tail}{hint}"))
                    elif word in MODALS:
                        # rule-owned class: legal in descriptive prose
                        if text_type == "procedural":
                            violations.append(Violation(
                                name, jsonpath, "CL009",
                                f"modal '{word}' in a procedural field - only "
                                f"must-semantics belong here"))
                    elif word in COMPARATIVES:
                        # rule-owned class: legal with a number in the sentence
                        if not has_number:
                            violations.append(Violation(
                                name, jsonpath, "CL011",
                                f"comparative '{word}' without a number in the sentence"))
                    elif not lexicon.knows(word):
                        violations.append(Violation(
                            name, jsonpath, "CL006",
                            f"unknown word '{word}' - add it to the dictionary "
                            f"(full lane) or rewrite with approved words"))
    violations.sort(key=lambda v: (v.path, v.rule))
    return violations


def _contracts(root=Path(".")) -> list[Path]:
    specs = Path(root) / "specs"
    if not specs.is_dir():
        return []
    return sorted(p for p in specs.glob("*/contract.yaml")
                  if p.parent.name != "vocabulary")


def lang_check(root=Path("."), schema_doc: dict | None = None):
    """(violations, armed) - armed False when no repo dictionary exists."""
    doc, violations = load_repo_dictionary(root)
    if doc is None:
        return violations, False
    terms = load_terms(root)
    name = str(Path(root) / DICTIONARY_FILE)
    violations = violations + validate_dictionary_doc(doc, name, terms,
                                                      schema_doc=schema_doc)
    lexicon = _Lexicon(doc, terms)
    root_resolved = Path(root).resolve()
    for contract in _contracts(root):
        findings = check_contract(contract, lexicon)
        rel = contract.resolve().relative_to(root_resolved).as_posix()
        if rel in lexicon.exempt:
            findings = [Violation(v.file, v.path, v.rule,
                                  f"{v.message} [exempt - standing red, ratchet "
                                  f"on next edit]", severity="warning")
                        for v in findings]
        violations.extend(findings)
    return violations, True


def main_lang_check(args) -> int:
    violations, armed = lang_check(args.root, schema_doc=(
        load_dictionary_schema(args.schema) if args.schema else None))
    errors = [v for v in violations if v.severity == "error"]
    if args.as_json:
        print(json.dumps({"note": FORM_NOTE,
                          "findings": [vars(v) for v in violations]}, indent=2))
    else:
        for violation in violations:
            print(violation.line)
        if not errors:
            state = "armed" if armed else "no dictionary here - door at rest"
            print(f"lang-green: {Path(args.root) / DICTIONARY_FILE} ({state}; {FORM_NOTE})")
    return 1 if errors else 0


def main_lang_extract(args) -> int:
    """Report-only calibration harvest. Writes nothing."""
    root = Path(args.root)
    doc, load_errors = load_repo_dictionary(root)
    for violation in load_errors:
        print(violation.line)
    terms = load_terms(root)
    lexicon = _Lexicon(doc, terms)
    contracts = _contracts(root)
    if not contracts:
        print("lang-extract: no specs contracts here")
        return 0

    freq: dict[str, int] = {}
    census: list[tuple[str, int, int, int]] = []
    banned_hits: dict[str, int] = {}
    for contract in contracts:
        try:
            instance = yaml.safe_load(contract.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(instance, dict):
            continue
        tokens_total = 0
        distinct: set[str] = set()
        hits = 0
        for row in lexicon.fields:
            if not isinstance(row, dict) or row.get("artifact") != "task-contract":
                continue
            for _, text in _walk_field(instance, str(row.get("path", ""))):
                for sentence in _sentences(text):
                    for _, word in _consume_phrases(_tokens(sentence), lexicon.phrases):
                        if word is None:
                            continue
                        tokens_total += 1
                        distinct.add(word)
                        if word in lexicon.banned:
                            hits += 1
                            banned_hits[word] = banned_hits.get(word, 0) + 1
                        elif not lexicon.knows(word):
                            freq[word] = freq.get(word, 0) + 1
        census.append((str(contract), tokens_total, len(distinct), hits))

    src = "repo dictionary" if doc is not None else "kit defaults (no dictionary present)"
    print(f"lang-extract: {len(contracts)} contracts, fields per {src}")
    print("candidates (frequency, word) - not yet approved anywhere:")
    for word in sorted(freq, key=lambda w: (-freq[w], w)):
        print(f"  {freq[word]:4} {word}")
    print("banned hits (base + repo bans):")
    if banned_hits:
        for word in sorted(banned_hits, key=lambda w: (-banned_hits[w], w)):
            print(f"  {banned_hits[word]:4} {word}")
    else:
        print("  none")
    print("census (contract - checkable tokens / distinct / banned hits):")
    for name, total, distinct_n, hits in census:
        print(f"  {name}  {total} / {distinct_n} / {hits}")
    print(f"summary: {len(freq)} candidate words; writes nothing")
    return 0
