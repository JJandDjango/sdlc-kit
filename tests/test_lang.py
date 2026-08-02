"""The controlled-language door + extractor (session-23 arc, F1-F12).

Covers the contract's acceptance sketches: schema shape (CL001), the
integrity set (CL002-CL005, CL013), every tier-1 rule red and green
(CL006-CL012), skip classes, the exempt ratchet, phrase consumption,
the report-only extractor, the --json envelope's form-note, the CI
template step, and the kit's own self-host green. The claim under
test is the door's, verbatim: form checked; meaning not checked.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import yaml

from taskcontract.__main__ import main
from taskcontract.lang import (
    BASE_DICTIONARY_PATH,
    DICTIONARY_SCHEMA_PATH,
    FORM_NOTE,
    lang_check,
    load_dictionary_schema,
    load_repo_dictionary,
    validate_dictionary_doc,
)

REPO = Path(__file__).resolve().parent.parent
SCHEMA = load_dictionary_schema()
STYLE = "restricted choice, never unnatural construction"

BASE_DOC = {
    "class": "E",
    "style": STYLE,
    "words": [
        {"word": "verify", "pos": "verb"},
        {"word": "run", "pos": "verb"},
        {"word": "runs", "pos": "verb"},
        {"word": "rejects", "pos": "verb"},
        {"word": "parser", "pos": "noun"},
        {"word": "input", "pos": "noun"},
        {"word": "module", "pos": "noun"},
        {"word": "bad", "pos": "modifier"},
    ],
    "fields": [
        {"artifact": "task-contract", "path": "intent", "text_type": "descriptive"},
        {"artifact": "task-contract", "path": "decomposition[].done_means",
         "text_type": "procedural"},
        {"artifact": "task-contract", "path": "decomposition[].acceptance_sketch[]",
         "text_type": "procedural"},
    ],
}

TERM_GATE = """\
term: gate
name: Gate
definition: A blocking enforcement venue in the pipeline, per the registry.
kind: entity
status: ratified
since: 2026-07-28
"""

TERM_TASK_CONTRACT = """\
term: task-contract
name: Task contract
definition: The phase-0 definition-of-ready artifact, one per task directory.
kind: entity
status: ratified
since: 2026-07-28
"""


def _doc(**overrides):
    doc = copy.deepcopy(BASE_DOC)
    doc.update(overrides)
    return doc


def _repo(tmp_path, dictionary=None, contract=None, terms=()):
    """Lay a minimal specs tree; return its root."""
    vocab = tmp_path / "specs" / "vocabulary"
    vocab.mkdir(parents=True)
    if dictionary is not None:
        (vocab / "dictionary.yaml").write_text(
            yaml.safe_dump(dictionary, sort_keys=False), encoding="utf-8")
    for slug, text in terms:
        (vocab / f"{slug}.yaml").write_text(text, encoding="utf-8")
    if contract is not None:
        task = tmp_path / "specs" / "demo" / "contract.yaml"
        task.parent.mkdir(parents=True)
        task.write_text(contract, encoding="utf-8")
    return tmp_path


def _errors(violations):
    return [v for v in violations if v.severity == "error"]


# --- dictionary artifact health (unit: dictionary-schema + F4) ---------


def test_schema_rejects_ban_without_use_instead():
    doc = _doc(banned=[{"word": "ensure"}])
    rules = {v.rule for v in validate_dictionary_doc(doc, "d", {}, SCHEMA)}
    assert "CL001" in rules


def test_schema_rejects_registry_row_with_bad_text_type():
    doc = _doc()
    doc["fields"][0]["text_type"] = "poetic"
    rules = {v.rule for v in validate_dictionary_doc(doc, "d", {}, SCHEMA)}
    assert "CL001" in rules


def test_packaged_data_files_exist():
    assert DICTIONARY_SCHEMA_PATH.is_file()
    assert BASE_DICTIONARY_PATH.is_file()
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    assert "schemas/*.json" in pyproject
    assert "data/*.yaml" in pyproject


def test_duplicate_word_red():
    doc = _doc()
    doc["words"].append({"word": "verify", "pos": "verb"})
    rules = {v.rule for v in validate_dictionary_doc(doc, "d", {}, SCHEMA)}
    assert "CL002" in rules


def test_glossary_collision_red():
    terms = {"gate": yaml.safe_load(TERM_GATE)}
    doc = _doc()
    doc["words"].append({"word": "gate", "pos": "noun"})
    rules = {v.rule for v in validate_dictionary_doc(doc, "d", terms, SCHEMA)}
    assert "CL003" in rules


def test_use_instead_unresolved_red():
    doc = _doc(banned=[{"word": "ensure", "use_instead": ["nonexistent"]}])
    rules = {v.rule for v in validate_dictionary_doc(doc, "d", {}, SCHEMA)}
    assert "CL004" in rules


def test_use_instead_banned_target_red():
    doc = _doc(banned=[
        {"word": "ensure", "use_instead": ["confirm"]},
        {"word": "confirm", "use_instead": ["verify"]},
    ])
    rules = {v.rule for v in validate_dictionary_doc(doc, "d", {}, SCHEMA)}
    assert "CL005" in rules


def test_base_shadow_reports_info_never_error(tmp_path):
    term_off = TERM_GATE.replace("gate", "off").replace("Gate", "Off")
    root = _repo(tmp_path, dictionary=_doc(), terms=[("off", term_off)])
    violations, armed = lang_check(root)
    assert armed
    shadows = [v for v in violations if v.rule == "CL013"]
    assert shadows and all(v.severity == "info" for v in shadows)
    assert not _errors(violations)


# --- door behavior (unit: lang-check-door) -----------------------------


def test_no_dictionary_is_green(tmp_path):
    violations, armed = lang_check(tmp_path)
    assert (violations, armed) == ([], False)
    assert main(["lang-check", "--root", str(tmp_path)]) == 0


def test_banned_word_red_names_replacement(tmp_path):
    contract = "decomposition:\n  - done_means: The module must ensure the input.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    violations, _ = lang_check(root)
    banned = [v for v in _errors(violations) if v.rule == "CL007"]
    assert banned and "use instead: verify" in banned[0].message


def test_unknown_word_red(tmp_path):
    contract = "intent: The parser must frobnicate the input.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    rules = {v.rule for v in _errors(lang_check(root)[0])}
    assert rules == {"CL006"}


def test_sentence_caps_by_text_type(tmp_path):
    long_proc = "The parser must " + "verify the input and " * 5 + "run the module now."
    contract = f"decomposition:\n  - done_means: {long_proc}\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    rules = {v.rule for v in _errors(lang_check(root)[0])}
    assert "CL008" in rules


def test_modal_polices_procedural_only(tmp_path):
    contract = ("intent: The parser should verify the input.\n"
                "decomposition:\n  - done_means: The parser should verify the input.\n")
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    modals = [v for v in _errors(lang_check(root)[0]) if v.rule == "CL009"]
    assert len(modals) == 1
    assert "done_means" in modals[0].path


def test_pronoun_subject_red(tmp_path):
    contract = "decomposition:\n  - done_means: It rejects bad input.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    rules = {v.rule for v in _errors(lang_check(root)[0])}
    assert "CL010" in rules


def test_comparative_needs_number(tmp_path):
    red = "decomposition:\n  - done_means: The parser rejects input faster.\n"
    green = "decomposition:\n  - done_means: The parser rejects input faster by 3 runs.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=red)
    assert {v.rule for v in _errors(lang_check(root)[0])} == {"CL011"}
    (root / "specs" / "demo" / "contract.yaml").write_text(green, encoding="utf-8")
    assert not _errors(lang_check(root)[0])


def test_sketch_verb_first(tmp_path):
    contract = ("decomposition:\n  - acceptance_sketch:\n"
                "      - The parser rejects bad input.\n"
                "      - Verify the parser rejects bad input.\n")
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    twelves = [v for v in _errors(lang_check(root)[0]) if v.rule == "CL012"]
    assert len(twelves) == 1
    assert "acceptance_sketch[0]" in twelves[0].path


def test_skip_classes_never_word_checked(tmp_path):
    contract = ("intent: Verify `frobnicate()` under specs/demo.py at G4 with "
                "TC007 in 100ms via YAML.\n")
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    assert not _errors(lang_check(root)[0])


def test_glossary_phrase_consumed(tmp_path):
    contract = "intent: Verify the task contract rejects bad input.\n"
    root = _repo(tmp_path, dictionary=_doc(),
                 contract=contract, terms=[("task-contract", TERM_TASK_CONTRACT)])
    assert not _errors(lang_check(root)[0])


def test_exempt_downgrades_to_warning(tmp_path):
    doc = _doc(exempt=["specs/demo/contract.yaml"])
    contract = "decomposition:\n  - done_means: It should frobnicate faster.\n"
    root = _repo(tmp_path, dictionary=doc, contract=contract)
    violations, _ = lang_check(root)
    demo = [v for v in violations if "demo" in v.file]
    assert demo and all(v.severity == "warning" for v in demo)
    assert all("standing red" in v.message for v in demo)
    assert main(["lang-check", "--root", str(root)]) == 0


def test_cli_json_envelope_carries_form_note(tmp_path, capsys):
    root = _repo(tmp_path, dictionary=_doc())
    assert main(["lang-check", "--root", str(root), "--json"]) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["note"] == FORM_NOTE
    assert envelope["findings"] == []


# --- extractor (unit: lang-extract) ------------------------------------


def _tree_digest(root: Path) -> list[tuple[str, str]]:
    return sorted(
        (p.relative_to(root).as_posix(),
         hashlib.sha256(p.read_bytes()).hexdigest())
        for p in root.rglob("*") if p.is_file())


def test_extract_reports_candidates_and_census(tmp_path, capsys):
    contract = "intent: The parser must frobnicate the widget twice.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    assert main(["lang-extract", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "   1 frobnicate" in out
    assert "   1 widget" in out
    assert "specs" in out and "census" in out


def test_extract_writes_nothing(tmp_path, capsys):
    contract = "intent: The parser must ensure the widget frobnicates.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    before = _tree_digest(root)
    assert main(["lang-extract", "--root", str(root)]) == 0
    assert _tree_digest(root) == before
    assert "writes nothing" in capsys.readouterr().out


def test_extract_skip_classes_absent(tmp_path, capsys):
    contract = ("intent: Verify `frobnicate()` under specs/demo.py at G4 with "
                "TC007 in 100ms via YAML.\n")
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    assert main(["lang-extract", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    for absent in ("demo.py", "TC007", "100ms", "YAML", "frobnicate()"):
        assert absent not in out


def test_extract_banned_hits_counted(tmp_path, capsys):
    contract = "intent: The parser must ensure the input properly.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    assert main(["lang-extract", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "   1 ensure" in out
    assert "   1 properly" in out


# --- venue joins (unit: venue-joins) -----------------------------------


def test_workflow_template_carries_single_segment_step():
    template = (REPO / "skills" / "sdlc" / "templates" /
                "workflow.yml.template").read_text(encoding="utf-8")
    lines = [l for l in template.splitlines() if "taskcontract lang-check" in l]
    assert len(lines) == 1
    step = lines[0]
    for token in (";", "&&", "|", ">"):
        assert token not in step


def test_audit_reports_lang_invalid(tmp_path, skill_audit):
    root = _repo(tmp_path, dictionary=_doc())
    (root / ".sdlc").mkdir()
    (root / "specs" / "vocabulary" / "dictionary.yaml").write_text(
        "words: [\n", encoding="utf-8")
    findings, is_spine = skill_audit.audit(root)
    assert is_spine
    assert any(f.code == "LANG-INVALID" and f.severity == "ERROR" for f in findings)


def test_audit_reports_exempt_info(tmp_path, skill_audit):
    doc = _doc(exempt=["specs/demo/contract.yaml"])
    contract = "decomposition:\n  - done_means: It should frobnicate faster.\n"
    root = _repo(tmp_path, dictionary=doc, contract=contract)
    (root / ".sdlc").mkdir()
    findings, _ = skill_audit.audit(root)
    exempt = [f for f in findings if f.code == "LANG-EXEMPT"]
    assert exempt and all(f.severity == "INFO" for f in exempt)


# --- self-host (unit: dictionary-seed + F12) ---------------------------


def test_repo_dictionary_validates_clean():
    doc, load_errors = load_repo_dictionary(REPO)
    assert doc is not None and not load_errors
    from taskcontract.vocabulary import load_terms
    assert not _errors(validate_dictionary_doc(
        doc, "dictionary.yaml", load_terms(REPO), SCHEMA))


def test_repo_lang_check_green_with_exempt_warnings_only():
    violations, armed = lang_check(REPO)
    assert armed
    assert not _errors(violations)
    assert any(v.severity == "warning" for v in violations), \
        "the six pre-arc contracts ride the exempt ratchet"


def test_repo_lang_check_cli_exit_zero():
    assert main(["lang-check", "--root", str(REPO)]) == 0
