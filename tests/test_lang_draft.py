"""`lang-check --draft`: the checks before signing, run on the interview's state file.

The command reads the state file that sits beside a feature document, and
never the document. It adds the state file's new terms to the glossary as
drafts, reports a new term that matches a ratified one (CL014), reports
the dictionary's health with the drafts, and runs the contract rules on a
draft contract of the statement, the non-goals, the checks and each
unit's `done_means`. It writes nothing. Its last line counts what it read
and found. Without the flag, `lang-check` prints what it printed before.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract
from taskcontract.__main__ import main
from taskcontract.lang import lang_check

REPO = Path(__file__).resolve().parent.parent
PACKAGE = Path(taskcontract.__file__).resolve().parent

DICTIONARY = {
    "class": "E",
    "style": "restricted choice, never unnatural construction",
    "words": [
        {"word": "verify", "pos": "verb"},
        {"word": "run", "pos": "verb"},
        {"word": "runs", "pos": "verb"},
        {"word": "rejects", "pos": "verb"},
        {"word": "reads", "pos": "verb"},
        {"word": "parser", "pos": "noun"},
        {"word": "input", "pos": "noun"},
        {"word": "module", "pos": "noun"},
        {"word": "check", "pos": "noun"},
        {"word": "acceptance-test", "pos": "noun"},
        {"word": "bad", "pos": "modifier"},
    ],
    "fields": [
        {"artifact": "task-contract", "path": "intent", "text_type": "descriptive"},
        {"artifact": "task-contract", "path": "non_goals[]", "text_type": "descriptive"},
        {"artifact": "task-contract", "path": "decomposition[].done_means",
         "text_type": "procedural"},
        {"artifact": "task-contract", "path": "decomposition[].acceptance_sketch[]",
         "text_type": "procedural"},
    ],
}

HEAD = "schema: spec-interview-state/2\nid: x\nphase: request\nnext: Q8\n"
NONE_FOUND = "draft: 0 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; 0 findings"
AT_REST = " (no dictionary here - door at rest)"

# One sentence of 27 words, each of them an approved word.
LONG = "The parser must " + "verify the input and " * 5 + "run the module now."


def _doc(**overrides):
    doc = copy.deepcopy(DICTIONARY)
    doc.update(overrides)
    return doc


def _term(slug, name, status="ratified", aliases=()):
    """One glossary term file: its slug and its text."""
    doc = {
        "term": slug,
        "name": name,
        "definition": f"The meaning of {name}, stated so that a reader can check it.",
        "kind": "entity",
        "status": status,
        "since": "2026-07-28",
    }
    if aliases:
        doc["aliases"] = list(aliases)
    return slug, yaml.safe_dump(doc, sort_keys=False)


GATE = _term("gate", "Gate")
STALE = _term("stale", "Stale")
SEAT = _term("intake-seat", "Intake seat", aliases=["seat"])
TASK_CONTRACT = _term("task-contract", "Task contract")


def _repo(tmp_path, dictionary=None, terms=(), contract=None):
    """Lay a small specs tree under tmp_path; return its root."""
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


def _state(root, answers=None, raw=None, name="x"):
    """Write the interview's state file at docs/features/<name>.state.yaml."""
    folder = Path(root) / "docs" / "features"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.state.yaml"
    if raw is None:
        doc = {"schema": "spec-interview-state/2", "id": name, "phase": "request",
               "next": "Q8", "seats": {"po": "ann", "engineer": "raj"}}
        if answers is not None:
            doc["answers"] = answers
        doc["open"] = []
        doc["history"] = []
        raw = yaml.safe_dump(doc, sort_keys=False)
    if isinstance(raw, bytes):
        path.write_bytes(raw)
    else:
        path.write_text(raw, encoding="utf-8")
    return path


def _draft(capsys, state, root=None):
    """Run `lang-check --draft`; return its exit code, its stdout lines, its stderr."""
    argv = ["lang-check", "--draft", str(state)]
    if root is not None:
        argv += ["--root", str(root)]
    capsys.readouterr()
    try:
        code = main(argv)
    except SystemExit as exc:  # a parser that refuses the flag exits here
        code = exc.code
    out, err = capsys.readouterr()
    return code, out.splitlines(), err


def _plain(capsys, root, *options):
    """Run `lang-check` without the flag; return its exit code and its stdout."""
    capsys.readouterr()
    code = main(["lang-check", "--root", str(root), *options])
    return code, capsys.readouterr().out


def _dictionary_file(root):
    return str(Path(root) / "specs" / "vocabulary" / "dictionary.yaml")


def _cl003(root, word, dictionary=DICTIONARY):
    index = [entry["word"] for entry in dictionary["words"]].index(word)
    return (f"{_dictionary_file(root)}: $.words[{index}].word: CL003 '{word}' collides "
            f"with a glossary term name, alias, or slug - the glossary is the open "
            f"class; keep the layers disjoint")


def _cl006(word):
    return (f"CL006 unknown word '{word}' - add it to the dictionary (full lane) "
            f"or rewrite with approved words")


def _cl014(state, written, name, slug):
    return (f"{state}: answers.terms[{written}]: CL014 new term '{name}' matches "
            f"ratified term '{slug}' - map it to that term, or rename it")


def _block(key, text, style="|", per_line=6, indent="  "):
    """A YAML block scalar that holds the text over several lines."""
    words = text.split()
    rows = [" ".join(words[i:i + per_line]) for i in range(0, len(words), per_line)]
    assert len(rows) > 1
    return f"{indent}{key}: {style}\n" + "".join(f"{indent}  {row}\n" for row in rows)


def _tree_digest(root):
    return sorted(
        (p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest())
        for p in Path(root).rglob("*") if p.is_file())


# --- the drawn output --------------------------------------------------


def _drawn_answers():
    return {
        "statement": LONG,
        "non_goals": ["No module reads the input twice."],
        "checks": [
            {"id": "SC1.1", "text": "verify the parser rejects bad input"},
            {"id": "SC2.1", "text": "each parser rejects bad input"},
        ],
        "terms": [
            {"name": "Check",
             "definition": "One line under a success criterion that a test proves."},
            {"name": "Seat",
             "definition": "A human position that answers for a feature document."},
            {"name": "Stale", "amends": "stale",
             "definition": "A feature whose document changed after its contract."},
        ],
        "units": [],
    }


def _drawn_lines(dictionary_file, state):
    return [
        f"{dictionary_file}: $.words[8].word: CL003 'check' collides with a glossary "
        f"term name, alias, or slug - the glossary is the open class; keep the "
        f"layers disjoint",
        f"{state}: answers.statement: CL008 sentence of 27 words exceeds the "
        f"descriptive cap of 25",
        f"{state}: answers.checks[SC2.1]: CL012 acceptance sketch must open with an "
        f"approved verb (got 'each')",
        f"{state}: answers.terms[Seat]: CL014 new term 'seat' matches ratified term "
        f"'intake-seat' - map it to that term, or rename it",
        "draft: 2 new terms, 1 amended; 1 non-goals; 2 checks; 0 units; "
        "4 findings (CL003 1, CL008 1, CL012 1, CL014 1)",
    ]


def test_sc2_1_the_command_prints_the_dictionary_line_the_state_file_lines_and_the_count(
        tmp_path, capsys):
    """One run prints, in order, the dictionary's line, a line per finding in
    the state file, and the count line; a finding that is an error gives exit 1."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[SEAT, STALE])
    state = _state(root, _drawn_answers())
    code, lines, err = _draft(capsys, state, root)
    assert lines == _drawn_lines(_dictionary_file(root), state)
    assert err == ""
    assert code == 1


def test_sc2_1_the_module_command_takes_the_draft_flag(tmp_path):
    """`python -m taskcontract lang-check --draft <state file>` reads the
    repository in the working folder and names each file as its path reads."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[SEAT, STALE])
    _state(root, _drawn_answers())
    env = dict(os.environ, PYTHONPATH=str(PACKAGE.parent), PYTHONIOENCODING="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "taskcontract", "lang-check", "--draft",
         "docs/features/x.state.yaml"],
        cwd=root, env=env, capture_output=True, encoding="utf-8", errors="replace")
    assert run.stdout.splitlines() == _drawn_lines(
        str(Path("specs") / "vocabulary" / "dictionary.yaml"),
        str(Path("docs/features/x.state.yaml")))
    assert run.stderr == ""
    assert run.returncode == 1


def test_sc2_1_a_new_term_named_seat_matches_the_kit_term_intake_seat(tmp_path, capsys):
    """Against the kit's own glossary, a new term `Seat` is reported against
    the ratified term `intake-seat`, which holds `seat` as an alias."""
    state = _state(tmp_path, {"terms": [
        {"name": "Seat", "definition": "A human position that answers for a document."}]})
    code, lines, err = _draft(capsys, state, REPO)
    assert _cl014(state, "Seat", "seat", "intake-seat") in lines
    assert lines[-1].startswith(
        "draft: 1 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; ")
    assert "CL014 1" in lines[-1]
    assert err == ""
    assert code == 1


# --- new terms: CL014 --------------------------------------------------


@pytest.mark.parametrize("written, name, slug", [
    ("Gate", "gate", "gate"),
    ("Task contract", "task contract", "task-contract"),
    ("Seat", "seat", "intake-seat"),
    ("Unit Test", "unit test", "acceptance-check"),
    ("Ready check", "ready check", "ready-check"),
    ("Definition Of Ready", "definition of ready", "dor"),
], ids=["name-and-slug", "two-word-name", "one-word-alias", "two-word-alias",
        "slug-only", "name-only"])
def test_sc2_1_a_new_term_that_matches_a_ratified_term_gets_cl014(
        tmp_path, capsys, written, name, slug):
    """A new term matches a ratified term when its name in lower case, or its
    slug, equals that term's name, slug or alias; CL014 is an error."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[
        GATE, TASK_CONTRACT, SEAT,
        _term("acceptance-check", "Acceptance check", aliases=["Unit test"]),
        _term("ready-check", "Readiness question"),
        _term("dor", "Definition of ready"),
    ])
    state = _state(root, {"terms": [
        {"name": written, "definition": "A definition the seat gave for this term."}]})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        _cl014(state, written, name, slug),
        "draft: 1 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL014 1)",
    ]
    assert err == ""
    assert code == 1


def test_sc2_1_a_new_term_that_matches_only_a_draft_term_gets_no_cl014(tmp_path, capsys):
    """CL014 reads ratified terms alone: a glossary term still at draft, and a
    new term that matches nothing, each print no line."""
    root = _repo(tmp_path, dictionary=_doc(),
                 terms=[_term("gate", "Gate", status="draft"), SEAT])
    state = _state(root, {"terms": [
        {"name": "Gate", "definition": "A blocking venue in the pipeline of a kit."},
        {"name": "Widget", "definition": "A thing the parser reads from its input."},
    ]})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        "draft: 2 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; 0 findings"]
    assert err == ""
    assert code == 0


def test_sc2_1_an_amended_term_is_counted_apart_and_never_gets_cl014(tmp_path, capsys):
    """A term that carries `amends: <slug>` replaces that ratified term's
    definition among the drafts: it counts as amended, never as new, and its
    own name is no match."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[GATE, STALE])
    state = _state(root, {"terms": [
        {"name": "Gate", "amends": "gate",
         "definition": "A blocking venue in the pipeline, with a new bound."},
        {"name": "Stale", "amends": "stale",
         "definition": "A feature whose document changed after its contract."},
        {"name": "Widget", "definition": "A thing the parser reads from its input."},
    ]})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        "draft: 1 new terms, 2 amended; 0 non-goals; 0 checks; 0 units; 0 findings"]
    assert err == ""
    assert code == 0


def test_sc2_1_a_term_that_amends_a_slug_the_glossary_lacks_reads_as_a_new_term(
        tmp_path, capsys):
    """`amends` that names no glossary term changes nothing: the term counts
    among the new terms and gets CL014 when it matches a ratified term."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[GATE])
    state = _state(root, {"terms": [
        {"name": "Gate", "amends": "portal",
         "definition": "A blocking venue in the pipeline, with a new bound."}]})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        _cl014(state, "Gate", "gate", "gate"),
        "draft: 1 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL014 1)",
    ]
    assert err == ""
    assert code == 1


def test_sc2_1_a_term_name_written_over_several_lines_is_read_as_one_name(
        tmp_path, capsys):
    """A name written as a block of several lines prints on one line, with
    one space where each line break stood, and still matches."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[TASK_CONTRACT, SEAT])
    state = _state(root, raw=HEAD + (
        "answers:\n"
        "  terms:\n"
        "    - name: |\n"
        "        Task\n"
        "        contract\n"
        "      definition: >-\n"
        "        The contract of one task, written here\n"
        "        over two lines.\n"
        "    - name: >\n"
        "        Seat\n"
        "      definition: A human position that answers for a document.\n"))
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        _cl014(state, "Task contract", "task contract", "task-contract"),
        _cl014(state, "Seat", "seat", "intake-seat"),
        "draft: 2 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "2 findings (CL014 2)",
    ]
    assert err == ""
    assert code == 1


# --- new terms as drafts: the dictionary's health ----------------------


@pytest.mark.parametrize("written, word", [
    ("Check", "check"),
    ("Acceptance test", "acceptance-test"),
], ids=["one-word-name", "slug"])
def test_sc2_1_a_new_term_that_equals_a_dictionary_word_gets_the_dictionary_cl003_line(
        tmp_path, capsys, written, word):
    """A new term joins the glossary as a draft: a dictionary word that equals
    its one-word name or its slug gets the dictionary's CL003 line, an error.
    The same dictionary is clean before the term stands."""
    root = _repo(tmp_path, dictionary=_doc())
    state = _state(root, {"terms": []})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [NONE_FOUND]
    assert code == 0

    state = _state(root, {"terms": [
        {"name": written, "definition": "A definition the seat gave for this term."}]})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        _cl003(root, word),
        "draft: 1 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL003 1)",
    ]
    assert err == ""
    assert code == 1


def test_sc2_1_an_info_line_counts_as_a_finding_and_leaves_exit_0(tmp_path, capsys):
    """A new term that shadows a base word gets the dictionary's CL013 line.
    The line is an info: the count line counts it, and the exit code stays 0."""
    root = _repo(tmp_path, dictionary=_doc())
    state = _state(root, {"terms": [
        {"name": "First", "definition": "The unit that a build makes before the rest."}]})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{_dictionary_file(root)}: $: CL013 local glossary shadows base word 'first' "
        f"- the term wins here",
        "draft: 1 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL013 1)",
    ]
    assert err == ""
    assert code == 0


def test_sc2_1_a_finding_the_dictionary_holds_without_the_drafts_still_prints(
        tmp_path, capsys):
    """The dictionary's health is the whole report: a duplicate word prints
    its CL002 line on a state file that holds no term."""
    dictionary = _doc()
    dictionary["words"].append({"word": "verify", "pos": "verb"})
    root = _repo(tmp_path, dictionary=dictionary)
    state = _state(root, {"statement": "The parser must verify the input."})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{_dictionary_file(root)}: $.words[11].word: CL002 duplicate entry 'verify' "
        f"(one word, one meaning, one row)",
        "draft: 0 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL002 1)",
    ]
    assert err == ""
    assert code == 1


def test_sc2_1_a_new_term_is_a_known_word_in_the_draft_contract(tmp_path, capsys):
    """The draft contract reads each new term as a glossary term: its one-word
    name is a known word and its name of several words is read as one phrase."""
    root = _repo(tmp_path, dictionary=_doc())
    statement = "The parser must verify the widget and the frob gizmo."
    state = _state(root, {"statement": statement})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.statement: {_cl006('widget')}",
        f"{state}: answers.statement: {_cl006('frob')}",
        f"{state}: answers.statement: {_cl006('gizmo')}",
        "draft: 0 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "3 findings (CL006 3)",
    ]
    assert code == 1

    state = _state(root, {"statement": statement, "terms": [
        {"name": "Widget", "definition": "A thing the parser reads from its input."},
        {"name": "Frob gizmo", "definition": "A second thing the parser reads."},
    ]})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        "draft: 2 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; 0 findings"]
    assert err == ""
    assert code == 0


# --- the draft contract ------------------------------------------------


def test_sc2_1_each_finding_carries_the_message_the_door_prints_for_a_contract(
        tmp_path, capsys):
    """The statement, the non-goals, the checks and a unit's `done_means` get
    the findings `lang-check` gives the same texts in a contract's `intent`,
    `non_goals`, `acceptance_sketch` and `done_means`, message for message."""
    intent = ("It must frobnicate the input faster. "
              "The parser should ensure the bad input.")
    non_goals = ["No parser runs faster.", "No module must handle the input properly."]
    sketch = ["the parser should reject input", "verify the parser rejects bad input"]
    done_means = "They must " + "verify the input and " * 5 + "run the module."
    contract = yaml.safe_dump({
        "intent": intent,
        "non_goals": non_goals,
        "decomposition": [{"id": "u1-parse", "done_means": done_means,
                           "acceptance_sketch": sketch}],
    }, sort_keys=False)
    root = _repo(tmp_path, dictionary=_doc(), contract=contract)
    state = _state(root, {
        "statement": intent,
        "non_goals": non_goals,
        "checks": [{"id": "SC1.1", "text": sketch[0]}, {"id": "SC1.2", "text": sketch[1]}],
        "units": [{"id": "u1-parse", "checks": ["SC1.1", "SC1.2"],
                   "done_means": done_means}],
    })
    places = {
        "$.intent": "answers.statement",
        "$.non_goals[0]": "answers.non_goals[0]",
        "$.non_goals[1]": "answers.non_goals[1]",
        "$.decomposition[0].acceptance_sketch[0]": "answers.checks[SC1.1]",
        "$.decomposition[0].acceptance_sketch[1]": "answers.checks[SC1.2]",
        "$.decomposition[0].done_means": "answers.units[u1-parse]",
    }
    door = [v for v in lang_check(root)[0] if v.file.endswith("contract.yaml")]
    assert {v.rule for v in door} == {
        "CL006", "CL007", "CL008", "CL009", "CL010", "CL011", "CL012"}
    expected = sorted(f"{state}: {places[v.path]}: {v.rule} {v.message}" for v in door)

    code, lines, err = _draft(capsys, state, root)
    assert sorted(lines[:-1]) == expected
    assert lines[-1].startswith(
        f"draft: 0 new terms, 0 amended; 2 non-goals; 2 checks; 1 units; "
        f"{len(expected)} findings (CL006 ")
    assert err == ""
    assert code == 1


def test_sc2_1_each_field_gets_the_cap_and_the_rules_of_its_contract_field(
        tmp_path, capsys):
    """The statement and a non-goal are descriptive text, cap 25. A check and
    a `done_means` are procedural text, cap 20, where a modal is a finding.
    Only a check must open with an approved verb."""
    root = _repo(tmp_path, dictionary=_doc())
    text = "Verify " + "the parser rejects bad input and " * 3 + "runs it now."
    assert len(text.split()) == 22
    state = _state(root, {
        "statement": text,
        "non_goals": [text],
        "checks": [{"id": "SC1.1", "text": text}],
        "units": [{"id": "u1-parse", "checks": ["SC1.1"], "done_means": text}],
    })
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.checks[SC1.1]: CL008 sentence of 22 words exceeds the "
        f"procedural cap of 20",
        f"{state}: answers.units[u1-parse]: CL008 sentence of 22 words exceeds the "
        f"procedural cap of 20",
        "draft: 0 new terms, 0 amended; 1 non-goals; 1 checks; 1 units; "
        "2 findings (CL008 2)",
    ]
    assert code == 1

    text = "The parser should verify the input."
    state = _state(root, {
        "statement": text,
        "non_goals": [text],
        "checks": [{"id": "SC1.1", "text": text}],
        "units": [{"id": "u1-parse", "checks": ["SC1.1"], "done_means": text}],
    })
    code, lines, err = _draft(capsys, state, root)
    modal = "CL009 modal 'should' in a procedural field - only must-semantics belong here"
    assert lines == [
        f"{state}: answers.checks[SC1.1]: {modal}",
        f"{state}: answers.checks[SC1.1]: CL012 acceptance sketch must open with an "
        f"approved verb (got 'the')",
        f"{state}: answers.units[u1-parse]: {modal}",
        "draft: 0 new terms, 0 amended; 1 non-goals; 1 checks; 1 units; "
        "3 findings (CL009 2, CL012 1)",
    ]
    assert err == ""
    assert code == 1


def test_sc2_1_a_field_the_dictionary_registry_leaves_out_gets_no_rule(tmp_path, capsys):
    """The repository's field registry decides which fields the rules read, as
    it does for a contract: with no `non_goals[]` row, a non-goal is counted
    and never checked."""
    dictionary = _doc()
    dictionary["fields"] = [row for row in dictionary["fields"]
                            if row["path"] != "non_goals[]"]
    root = _repo(tmp_path, dictionary=dictionary)
    state = _state(root, {
        "statement": "The parser must frobnicate the input.",
        "non_goals": ["No parser must frobnicate the input."],
    })
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.statement: {_cl006('frobnicate')}",
        "draft: 0 new terms, 0 amended; 1 non-goals; 0 checks; 0 units; "
        "1 findings (CL006 1)",
    ]
    assert err == ""
    assert code == 1


@pytest.mark.parametrize("style", ["|", "|-", ">", ">-"])
def test_sc2_1_a_statement_written_over_several_lines_is_read_as_one_text(
        tmp_path, capsys, style):
    """A statement written as a block of several lines is one text: a sentence
    of 25 words over five lines is inside the cap, and one of 26 is over it."""
    root = _repo(tmp_path, dictionary=_doc())
    inside = "The parser must " + "verify the input and " * 5 + "run now."
    over = "The parser must " + "verify the input and " * 5 + "run it now."
    assert (len(inside.split()), len(over.split())) == (25, 26)

    state = _state(root, raw=HEAD + "answers:\n" + _block("statement", over, style))
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.statement: CL008 sentence of 26 words exceeds the "
        f"descriptive cap of 25",
        "draft: 0 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL008 1)",
    ]
    assert code == 1

    state = _state(root, raw=HEAD + "answers:\n" + _block("statement", inside, style))
    code, lines, err = _draft(capsys, state, root)
    assert lines == [NONE_FOUND]
    assert err == ""
    assert code == 0


def test_sc2_1_a_check_written_over_several_lines_is_read_as_one_text(tmp_path, capsys):
    """A line break inside a check starts no new sentence: the word after it
    need not be a verb, and the cap of 20 counts the words of every line."""
    root = _repo(tmp_path, dictionary=_doc())
    inside = "verify " + "the parser rejects bad input and " * 3 + "runs"
    over = "verify " + "the parser rejects bad input and " * 3 + "runs now"
    assert (len(inside.split()), len(over.split())) == (20, 21)
    state = _state(root, raw=HEAD + (
        "answers:\n"
        "  checks:\n"
        "    - id: SC1.1\n" + _block("text", inside, "|", 5, "      ") +
        "    - id: SC1.2\n" + _block("text", over, ">-", 5, "      ")))
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.checks[SC1.2]: CL008 sentence of 21 words exceeds the "
        f"procedural cap of 20",
        "draft: 0 new terms, 0 amended; 0 non-goals; 2 checks; 0 units; "
        "1 findings (CL008 1)",
    ]
    assert err == ""
    assert code == 1


def test_sc2_1_a_done_means_written_over_several_lines_is_read_as_one_text(
        tmp_path, capsys):
    """Each unit's `done_means` is read under the cap of 20, counted over every
    line of its block, and its finding names the unit by its id."""
    root = _repo(tmp_path, dictionary=_doc())
    part = "runs the parser and rejects bad input and "
    inside = "The module " + part * 2 + "runs now."
    over = "The module " + part * 2 + "runs it now."
    assert (len(inside.split()), len(over.split())) == (20, 21)
    state = _state(root, raw=HEAD + (
        "answers:\n"
        "  units:\n"
        "    - id: u1-parse\n"
        "      checks: [SC1.1]\n" + _block("done_means", inside, ">", 5, "      ") +
        "    - id: u2-report\n"
        "      checks: [SC1.2]\n" + _block("done_means", over, "|", 5, "      ")))
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.units[u2-report]: CL008 sentence of 21 words exceeds the "
        f"procedural cap of 20",
        "draft: 0 new terms, 0 amended; 0 non-goals; 0 checks; 2 units; "
        "1 findings (CL008 1)",
    ]
    assert err == ""
    assert code == 1


# --- the order of the lines, and the count line -------------------------


def test_sc2_1_the_lines_stand_in_one_order_and_the_count_line_lists_each_code(
        tmp_path, capsys):
    """The dictionary's lines come first, then the statement, the non-goals,
    the checks, the units and the terms, each list in the state file's order.
    One entry's lines stand by code. A non-goal is named by its place from 0.
    The count line stands last, its codes in ascending order."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[GATE])
    non_goals = ["No module reads the input twice."] * 11
    non_goals[2] = "No parser must ensure the input."
    non_goals[10] = "No module rejects the widget."
    state = _state(root, {
        "statement": ("It must " + "verify the input and " * 5 +
                      "frobnicate the bad module now."),
        "non_goals": non_goals,
        "checks": [
            {"id": "SC1.1", "text": "the parser rejects bad input"},
            {"id": "SC1.2", "text": "verify the parser rejects bad input"},
        ],
        "units": [{"id": "u1-parse", "checks": ["SC1.1", "SC1.2"],
                   "done_means": "The parser should verify the input."}],
        "terms": [
            {"name": "Check",
             "definition": "One line under a success criterion that a test proves."},
            {"name": "Gate", "definition": "A blocking venue in the pipeline of a kit."},
        ],
    })
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        _cl003(root, "check"),
        f"{state}: answers.statement: {_cl006('frobnicate')}",
        f"{state}: answers.statement: CL008 sentence of 27 words exceeds the "
        f"descriptive cap of 25",
        f"{state}: answers.statement: CL010 sentence opens on pronoun 'it' - name "
        f"the subject",
        f"{state}: answers.non_goals[2]: CL007 banned word 'ensure' (state the check, "
        f"not the hope) - use instead: verify",
        f"{state}: answers.non_goals[10]: {_cl006('widget')}",
        f"{state}: answers.checks[SC1.1]: CL012 acceptance sketch must open with an "
        f"approved verb (got 'the')",
        f"{state}: answers.units[u1-parse]: CL009 modal 'should' in a procedural "
        f"field - only must-semantics belong here",
        _cl014(state, "Gate", "gate", "gate"),
        "draft: 2 new terms, 0 amended; 11 non-goals; 2 checks; 1 units; 9 findings "
        "(CL003 1, CL006 2, CL007 1, CL008 1, CL009 1, CL010 1, CL012 1, CL014 1)",
    ]
    assert err == ""
    assert code == 1


@pytest.mark.parametrize("body", [
    "",
    "answers:\n",
    "answers: {}\n",
    "answers:\n  statement: ''\n  non_goals: []\n  checks: []\n  terms: []\n  units: []\n",
    "answers:\n  statement:\n  non_goals:\n  checks:\n  terms:\n  units:\n",
    "answers:\n  problem: The parser must ensure the frobnicate properly.\n"
    "  out_of_scope:\n    - It should frobnicate faster.\n",
], ids=["no-answers", "answers-null", "answers-empty", "each-key-empty",
        "each-key-null", "only-other-sections"])
def test_sc2_1_a_key_the_state_file_lacks_reads_as_empty(tmp_path, capsys, body):
    """A state file with no `answers`, or with none of the five keys the
    command reads, counts nothing and finds nothing: one line, exit 0. The
    other sections' answers are never read."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[GATE])
    state = _state(root, raw=HEAD + body)
    code, lines, err = _draft(capsys, state, root)
    assert lines == [NONE_FOUND]
    assert err == ""
    assert code == 0


# --- edges --------------------------------------------------------------


@pytest.mark.parametrize("raw", [
    None,
    "answers: [\n",
    b"\xff\xfe\x00 not text",
    "- a list\n- at the top\n",
    "",
], ids=["missing", "broken-yaml", "not-utf-8", "not-a-mapping", "empty-file"])
def test_sc2_1_a_state_file_that_cannot_be_read_gets_one_cl000_line(tmp_path, capsys, raw):
    """A state file that is missing, is not YAML or holds no mapping prints
    one CL000 line with its reason, on one line, and exits 1; no count line."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[GATE])
    if raw is None:
        state = root / "docs" / "features" / "x.state.yaml"
    else:
        state = _state(root, raw=raw)
    code, lines, err = _draft(capsys, state, root)
    opening = f"{state}: $: CL000 unreadable draft: "
    assert len(lines) == 1
    assert lines[0].startswith(opening)
    assert lines[0][len(opening):].strip()
    assert err == ""
    assert code == 1


def test_sc2_1_with_no_dictionary_only_cl014_runs_and_the_count_line_says_so(
        tmp_path, capsys):
    """In a repository with a glossary and no dictionary, no dictionary line
    and no contract rule runs: CL014 alone reports, and the count line ends
    with the door's own words for a repository with no dictionary."""
    root = _repo(tmp_path, terms=[GATE])
    answers = {
        "statement": "It should frobnicate the input properly.",
        "non_goals": ["No parser must ensure the input."],
        "checks": [{"id": "SC1.1", "text": "the parser rejects bad input"}],
        "units": [{"id": "u1-parse", "checks": ["SC1.1"],
                   "done_means": "It should verify the input."}],
        "terms": [
            {"name": "Gate", "definition": "A blocking venue in the pipeline of a kit."},
            {"name": "First", "definition": "The unit that a build makes before the rest."},
        ],
    }
    state = _state(root, answers)
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        _cl014(state, "Gate", "gate", "gate"),
        "draft: 2 new terms, 0 amended; 1 non-goals; 1 checks; 1 units; "
        "1 findings (CL014 1)" + AT_REST,
    ]
    assert err == ""
    assert code == 1

    answers["terms"] = answers["terms"][1:]
    state = _state(root, answers)
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        "draft: 1 new terms, 0 amended; 1 non-goals; 1 checks; 1 units; "
        "0 findings" + AT_REST]
    assert err == ""
    assert code == 0

    bare = tmp_path / "bare"
    bare.mkdir()
    state = _state(bare, {})
    code, lines, err = _draft(capsys, state, bare)
    assert lines == [NONE_FOUND + AT_REST]
    assert code == 0
    assert _plain(capsys, bare) == (0, (
        f"lang-green: {_dictionary_file(bare)} (no dictionary here - door at rest; "
        f"form checked; meaning not checked)\n"))


# --- what the command reads and writes ----------------------------------


def test_sc2_1_the_command_never_reads_the_document_beside_the_state_file(
        tmp_path, capsys):
    """A feature document beside the state file, whose text would trip the
    rules, changes no line of the output, and no line names it."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[GATE])
    state = _state(root, {
        "statement": "The parser must frobnicate the input.",
        "terms": [{"name": "Widget",
                   "definition": "A thing the parser reads from its input."}],
    })
    expected = [
        f"{state}: answers.statement: {_cl006('frobnicate')}",
        "draft: 1 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL006 1)",
    ]
    code, lines, err = _draft(capsys, state, root)
    assert lines == expected

    (state.parent / "x.md").write_text(
        "# x - a feature\n\n"
        "## Statement\n\nIt should ensure the gizmo properly, faster.\n\n"
        "## Terms\n\n| Name | Definition |\n|---|---|\n| Gate | A second gate. |\n\n"
        "## Checks\n\n- the gizmo should frobnicate (SC9.9)\n",
        encoding="utf-8")
    code, lines, err = _draft(capsys, state, root)
    assert lines == expected
    assert not any("x.md" in line or "gizmo" in line for line in lines)
    assert err == ""
    assert code == 1


def test_sc2_1_the_command_writes_nothing(tmp_path, capsys, monkeypatch):
    """A run with new terms and findings leaves every file of the repository
    as it was: no file under `specs/`, no new file, the state file unchanged
    byte for byte."""
    root = _repo(tmp_path, dictionary=_doc(), terms=[GATE, STALE])
    state = _state(root, {
        "statement": "The parser must frobnicate the input.",
        "non_goals": ["No module reads the input twice."],
        "checks": [{"id": "SC1.1", "text": "verify the parser rejects bad input"}],
        "units": [{"id": "u1-parse", "checks": ["SC1.1"],
                   "done_means": "The parser rejects bad input."}],
        "terms": [
            {"name": "Widget", "definition": "A thing the parser reads from its input."},
            {"name": "Gate", "definition": "A blocking venue in the pipeline of a kit."},
            {"name": "Stale", "amends": "stale",
             "definition": "A feature whose document changed after its contract."},
        ],
    })
    monkeypatch.chdir(root)
    before_bytes = state.read_bytes()
    before = _tree_digest(root)
    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.statement: {_cl006('frobnicate')}",
        _cl014(state, "Gate", "gate", "gate"),
        "draft: 2 new terms, 1 amended; 1 non-goals; 1 checks; 1 units; "
        "2 findings (CL006 1, CL014 1)",
    ]
    assert err == ""
    assert code == 1
    assert state.read_bytes() == before_bytes
    assert _tree_digest(root) == before
    assert sorted(p.name for p in (root / "specs" / "vocabulary").iterdir()) == [
        "dictionary.yaml", "gate.yaml", "stale.yaml"]


# --- without the flag ---------------------------------------------------


def test_sc2_1_without_the_flag_a_repository_with_findings_prints_what_it_printed(
        tmp_path, capsys):
    """Without `--draft`, a repository with findings prints the same bytes
    and gives the same exit code as before the flag stood, before and after
    a run with it. With the flag, no line reads the repository's contracts."""
    contract = ("intent: The parser must frobnicate the input.\n"
                "decomposition:\n"
                "  - acceptance_sketch:\n"
                "      - The parser rejects bad input.\n")
    root = _repo(tmp_path, dictionary=_doc(), contract=contract,
                 terms=[_term("off", "Off")])
    state = _state(root, {"statement": "The parser must verify the input."})
    shadow = (f"{_dictionary_file(root)}: $: CL013 local glossary shadows base word "
              f"'off' - the term wins here")
    file = root / "specs" / "demo" / "contract.yaml"
    before = (
        f"{shadow}\n"
        f"{file}: $.decomposition[0].acceptance_sketch[0]: CL012 acceptance sketch "
        f"must open with an approved verb (got 'the')\n"
        f"{file}: $.intent: {_cl006('frobnicate')}\n")
    assert _plain(capsys, root) == (1, before)

    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        shadow,
        "draft: 0 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "1 findings (CL013 1)",
    ]
    assert err == ""
    assert code == 0
    assert _plain(capsys, root) == (1, before)


def test_sc2_1_without_the_flag_a_repository_with_no_finding_prints_what_it_printed(
        tmp_path, capsys):
    """Without `--draft`, a clean repository prints its green line, and its
    JSON form, byte for byte as before: a state file with findings changes
    neither. With the flag, the same state file's finding prints."""
    contract = "intent: The parser must verify the input.\n"
    root = _repo(tmp_path, dictionary=_doc(), contract=contract, terms=[GATE])
    state = _state(root, {"statement": "The parser must frobnicate the input.",
                          "terms": [{"name": "Gate", "definition": "A second gate."}]})
    green = (f"lang-green: {_dictionary_file(root)} (armed; form checked; meaning "
             f"not checked)\n")
    as_json = '{\n  "note": "form checked; meaning not checked",\n  "findings": []\n}\n'
    assert _plain(capsys, root) == (0, green)
    assert _plain(capsys, root, "--json") == (0, as_json)

    code, lines, err = _draft(capsys, state, root)
    assert lines == [
        f"{state}: answers.statement: {_cl006('frobnicate')}",
        _cl014(state, "Gate", "gate", "gate"),
        "draft: 1 new terms, 0 amended; 0 non-goals; 0 checks; 0 units; "
        "2 findings (CL006 1, CL014 1)",
    ]
    assert err == ""
    assert code == 1
    assert _plain(capsys, root) == (0, green)
    assert _plain(capsys, root, "--json") == (0, as_json)


# --- no new dependency --------------------------------------------------


def test_sc2_1_the_command_needs_no_new_dependency(tmp_path, capsys):
    """The command runs on what the package needs today: the project's
    dependency list is unchanged, and the two modules that hold the command
    import only the standard library, PyYAML, jsonschema and the package."""
    root = _repo(tmp_path, dictionary=_doc())
    state = _state(root, {})
    code, lines, err = _draft(capsys, state, root)
    assert lines == [NONE_FOUND]
    assert code == 0

    project = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    listed = project.split("\ndependencies = [", 1)[1].split("]", 1)[0]
    assert re.findall(r'"([^"]+)"', listed) == ["jsonschema>=4.18", "PyYAML>=6"]

    allowed = set(sys.stdlib_module_names) | {"yaml", "jsonschema", "taskcontract"}
    for module in ("lang.py", "__main__.py"):
        tree = ast.parse((PACKAGE / module).read_text(encoding="utf-8"))
        roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                roots.add((node.module or "").split(".")[0])
        assert roots <= allowed, f"{module} imports {sorted(roots - allowed)}"
