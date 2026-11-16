"""The words of `g1-record`, pinned (contract: g1-requirements-spec, unit
s10-words-and-folds: check SC1.1).

The design's words are built and read right on HEAD, so every test here passes
today: they are pins, not a red list. They hold the words in place, so that a
change to one word, one stream, one exit code or one file written by a refused
call fails a test here.

What the file pins:

- each refusal line of the three writers (`lint`, `model`, `review`): on stderr
  alone, exit 2, nothing on stdout, and nothing written under the root (SC1.1);
- both green lines, the review's and the verdict's, word for word (SC1.1);
- the lines of a review that leaves several items unchecked, one for each in
  item order, and `g1-check`'s line for each of them (SC1.1);
- a person who declines to sign gets no review record: R6's words, R7's words
  and a verdict that reads `to do` (SC1.1).

A temporary repository per test, with a trivial stand-in tool on a PATH the test
sets for the two cases that need an installed checker: no test needs a linter or
a checker on the machine. Commands run in this process.
"""

from __future__ import annotations

import os
import re
import stat
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

from taskcontract.__main__ import main

ROOT = Path(__file__).resolve().parent.parent
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
FLOW = ROOT / "skills" / "sdlc" / "flows" / "g1.md"

ID = "apply-discount"
RECORD = f".sdlc/g1/{ID}.yaml"
RECORDED = f"recorded: {RECORD}"
GREEN = f"g1-green: {ID}"
PASSED = "G1.3: the review checks all 11 items"
ALL = "1,2,3,4,5,6,7,8,9,10,11"

NAMES = ["Testable", "Unambiguous", "Traceable", "Complete over units",
         "Covers the sketch", "Consistent", "Respects non-goals",
         "Boundary + error paths", "Property-spec applicability",
         "Schema presence", "Oracle designation answered"]

SEAT_TERM = {"term": "intake-seat", "name": "Intake seat",
             "definition": "A human position that answers for a unit at intake.",
             "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
             "since": "2026-08-26"}
SPECTRAL = {"paths": ["api/*.yaml"], "linter": "spectral", "pin": ".spectral.yaml"}
LEDGER = {"id": "ledger", "paths": ["src/ledger/"], "hard_core": True,
          "oracle": "concurrency", "model": "specs/models/ledger.tla",
          "model_config": "specs/models/ledger.cfg", "checker": "tlc"}
WALLET = {"id": "wallet", "paths": ["src/wallet/"], "hard_core": True,
          "oracle": "property-only", "model": "specs/p/wallet.pproj",
          "model_config": "specs/p/wallet.check", "checker": "p"}
API = {"id": "api", "paths": ["src/api/"], "hard_core": False, "oracle": "none",
       "oracle_reason": "read-only pass-through, covered by its acceptance tests"}

INTENT = ("A contract with a scope of its own, enough words to pass the door "
          "as a fixture for the suite of the words and the folds.")
TITLE = "# {id} - A fixture feature\n\n"
HEAD = "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"


def row(text: str, by: str = "Ann Lee") -> str:
    return f"| 2026-10-07 | {by} | {text} |\n"


def document(revision: int, feature: str = ID) -> str:
    """A feature document with text rows r1 to r<revision>, then the `Ready:`
    row that names r<revision> as the one the contract is derived from."""
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{feature}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return TITLE.format(id=feature) + HEAD + rows + ready + "\n## Statement\n\nWords.\n"


def contract_text(feature: str = ID) -> str:
    unit = {"unit": "the unit", "id": "the-unit", "confirmed_by": ["po"],
            "done_means": "the unit is done",
            "acceptance_sketch": ["verify the unit is done (SC1.1)"]}
    return yaml.safe_dump({
        "id": feature, "title": "A fixture feature", "intent": INTENT,
        "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
        "decomposition": [unit], "dependencies": [], "entities": [],
        "provenance": {"origin": "human-request"}}, sort_keys=False)


class Repo:
    """One fixture repository at <tmp>/repo, the working directory, with its tool
    folder <tmp>/bin as the whole PATH. It holds a ratified seat roster, the
    contract of `apply-discount`, its pair at r5 and r4, a config that turns G0 and
    G1 on and declares the Spectral pin, one schema file in scope and a component
    declaration with the ledger, a TLC hard core in the contract's scope."""

    def __init__(self, tmp: Path, monkeypatch):
        self.root = tmp / "repo"
        self.bin = tmp / "bin"
        self.root.mkdir()
        self.bin.mkdir()
        self.write("specs/vocabulary/intake-seat.yaml", yaml.safe_dump(SEAT_TERM, sort_keys=False))
        self.write(f"specs/{ID}/contract.yaml", contract_text())
        self.write(f"docs/features/{ID}.md", document(5))
        self.write(f"docs/features/{ID}.design.md", document(4))
        self.config()
        self.write(".spectral.yaml", "rules: {}\n")
        self.write("api/openapi.yaml", "openapi: 3.1.0\n")
        self.components(LEDGER, API)
        self.write(LEDGER["model"], "---- MODULE ledger ----\n====\n")
        self.write(LEDGER["model_config"], "SPECIFICATION Spec\nINVARIANT Inv\n")
        monkeypatch.setenv("PATH", str(self.bin))
        if os.name == "nt":
            monkeypatch.setenv("PATHEXT", ".COM;.EXE;.BAT;.CMD")
        monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp))
        monkeypatch.setenv("COLUMNS", "500")
        monkeypatch.chdir(self.root)

    def write(self, rel: str, text) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def config(self, active=("G0", "G1"), schemas=(SPECTRAL,)) -> None:
        self.write(".sdlc/config.yaml", yaml.safe_dump(
            {"active_gates": list(active), "g1": {"exempt": [], "schemas": list(schemas)}},
            sort_keys=False))

    def components(self, *entries) -> None:
        self.write("specs/components.yaml", yaml.safe_dump(
            {"version": 1, "components": list(entries)}, sort_keys=False))

    def install(self, tool: str) -> None:
        """A stand-in named `tool` that answers every call with a version line and
        exit 0: a .cmd on Windows, an executable script elsewhere."""
        script = self.bin / "stand_in.py"
        script.write_text("print('%s 1.0.0')\n" % tool, encoding="utf-8")
        if os.name == "nt":
            (self.bin / f"{tool}.cmd").write_text(
                f'@echo off\r\n"{sys.executable}" "{script}" %*\r\nexit /b 0\r\n',
                encoding="utf-8", newline="")
        else:
            shim = self.bin / tool
            shim.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" "$@"\n',
                            encoding="utf-8", newline="")
            shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def files(self) -> dict[str, bytes | None]:
        """Every path under the root, a folder as None: a refused call leaves no
        file and no empty folder either."""
        return {path.relative_to(self.root).as_posix():
                (path.read_bytes() if path.is_file() else None)
                for path in sorted(self.root.rglob("*"))}

    def records(self) -> list[dict]:
        return yaml.safe_load((self.root / RECORD).read_text(encoding="utf-8"))["records"]


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Repo:
    return Repo(tmp_path, monkeypatch)


def cli(capsys, *argv):
    """Run one taskcontract command in this process: (exit code, stdout, stderr)."""
    words = [str(arg) for arg in argv]
    capsys.readouterr()
    try:
        code = main(words)
    except SystemExit:  # argparse refused the words themselves
        code = None
    out, err = capsys.readouterr()
    assert code is not None, f"taskcontract does not take `{' '.join(words[:4])}`: {err.strip()}"
    return code, out, err


def lint(capsys, feature: str = ID):
    return cli(capsys, "g1-record", "lint", feature)


def model(capsys, feature: str = ID):
    return cli(capsys, "g1-record", "model", feature)


def review(capsys, *extra, feature: str = ID):
    return cli(capsys, "g1-record", "review", feature, "--by", "Ann Lee", "--seat", "po", *extra)


def passing(capsys, feature: str = ID):
    return review(capsys, "--checked", ALL, feature=feature)


def check(capsys, *extra, feature: str = ID):
    return cli(capsys, "g1-check", feature, "--root", ".", *extra)


WRITERS = {"lint": lint, "model": model, "review": passing}


# --- SC1.1: each refusal line of the writer, word for word ------------------------------
# Each line stands on stderr alone, with exit 2 and nothing on stdout, and the call
# writes nothing: every path under the root keeps its bytes, no empty folder included.

def refused(repo: Repo, capsys, writer: str, line: str, feature: str = ID) -> None:
    """The writer's call is refused with exactly this one line (a regular
    expression for a line that holds a reason the design leaves free)."""
    before = repo.files()
    code, out, err = WRITERS[writer](capsys, feature)
    assert (code, out) == (2, ""), (code, out, err)
    assert re.fullmatch(line, err), err
    assert err.count("\n") == 1
    assert repo.files() == before, "a refused writer wrote under the root"


def break_contract_scope(repo: Repo) -> None:
    repo.write(f"specs/{ID}/contract.yaml", "scope: [\n")


def break_the_record(repo: Repo) -> None:
    repo.write(RECORD, "records: [\n")


def turn_g1_off(repo: Repo) -> None:
    repo.config(active=("G0",))


WRITER_LINES = [
    pytest.param(lambda repo: None, re.escape("nope: no contract at specs/nope/contract.yaml\n"),
                 "nope", id="no-contract"),
    pytest.param(turn_g1_off, re.escape(f"{ID}: G1 is not active\n"), ID, id="g1-not-active"),
    pytest.param(break_contract_scope,
                 re.escape(f"{ID}: the contract's scope cannot be read at "
                           f"specs/{ID}/contract.yaml\n"), ID, id="scope-cannot-be-read"),
    pytest.param(break_the_record,
                 re.escape("taskcontract g1-record: unreadable record: " + RECORD + " (")
                 + r"\S[^\n]*\)\n", ID, id="unreadable-record"),
]


@pytest.mark.parametrize("writer", sorted(WRITERS))
@pytest.mark.parametrize("damage, line, feature", WRITER_LINES)
def test_sc1_1_word_each_writer_refuses_the_calls_it_cannot_use_in_the_designs_words(
        repo, capsys, writer, damage, line, feature):
    damage(repo)
    refused(repo, capsys, writer, line, feature)


def test_sc1_1_word_lint_refuses_a_g1_schemas_that_cannot_be_read(repo, capsys):
    repo.write(".sdlc/config.yaml", "active_gates: [G0, G1]\ng1:\n  schemas: 5\n")
    refused(repo, capsys, "lint", re.escape(f"{ID}: g1.schemas cannot be read: ") + r"\S[^\n]*\n")


def test_sc1_1_word_lint_refuses_a_linter_the_kit_does_not_know(repo, capsys):
    repo.config(schemas=[{"paths": ["api/*.yaml"], "linter": "eslint", "pin": ".spectral.yaml"}])
    refused(repo, capsys, "lint",
            re.escape(f"{ID}: g1.schemas names a linter the kit does not know: eslint\n"))


def test_sc1_1_word_model_refuses_a_component_declaration_that_cannot_be_read(repo, capsys):
    repo.write("specs/components.yaml", "components: [\n")
    refused(repo, capsys, "model",
            re.escape(f"{ID}: specs/components.yaml cannot be read: ") + r"\S[^\n]*\n")


def test_sc1_1_word_model_refuses_a_repository_with_no_component_declaration(repo, capsys):
    (repo.root / "specs" / "components.yaml").unlink()
    refused(repo, capsys, "model",
            re.escape(f"{ID}: no component declaration at specs/components.yaml\n"))


def test_sc1_1_word_model_refuses_a_model_whose_working_folder_cannot_be_made(
        repo, capsys, monkeypatch):
    repo.install("tlc")

    def refuse(*args, **kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(tempfile, "mkdtemp", refuse)
    refused(repo, capsys, "model",
            re.escape(f"{ID}: no working folder for the model of ledger: ") + r"\S[^\n]*\n")


def test_sc1_1_word_model_refuses_a_p_configuration_that_cannot_be_read(repo, capsys):
    repo.install("p")
    repo.components(WALLET, API)
    repo.write(WALLET["model"], "<Project><ProjectName>Wallet</ProjectName></Project>\n")
    # no configuration file: the words of `p check` cannot be read
    refused(repo, capsys, "model",
            re.escape(f"{ID}: the configuration of wallet cannot be read: specs/p/wallet.check\n"))


# --- SC1.1: both green lines, and a review with several items unchecked -----------------

def test_sc1_1_word_the_review_green_line_and_the_verdict_green_line_stand_word_for_word(
        repo, capsys):
    assert passing(capsys) == (0, f"{PASSED}\n{RECORDED}\n", "")
    # G1.1 and G1.2 read `done` once a schema in scope is absent and no hard core is
    repo.config(schemas=[])
    repo.components(dict(LEDGER, hard_core=False, oracle="none", oracle_reason="a fixture"), API)
    assert check(capsys) == (0, f"{GREEN}\n", "")


def test_sc1_1_word_a_review_with_several_items_unchecked_prints_one_line_for_each_in_item_order(
        repo, capsys):
    code, out, err = review(
        capsys, "--checked", "1,2,3,4,5,8,9,10", "--unchecked", "6=Statement",
        "--unchecked", "7=Non goals", "--unchecked", "11=a=b")
    assert (code, err) == (1, "")
    assert out.splitlines() == [
        "G1.3: item 6 Consistent is unchecked in Statement",
        "G1.3: item 7 Respects non-goals is unchecked in Non goals",
        "G1.3: item 11 Oracle designation answered is unchecked in a=b",
        RECORDED]
    held = repo.records()[-1]["items"]
    assert [(e["n"], e["checked"], e.get("section")) for e in held if not e["checked"]] == [
        (6, False, "Statement"), (7, False, "Non goals"), (11, False, "a=b")]
    assert [e["name"] for e in held] == NAMES


def test_sc1_1_word_g1_check_names_each_unchecked_item_after_the_review(repo, capsys):
    assert review(capsys, "--checked", "1,2,3,4,5,8,9,10,11", "--unchecked", "6=Statement",
                  "--unchecked", "7=Non goals")[0] == 1
    code, out, err = check(capsys)
    assert (code, err) == (1, "")
    assert [line for line in out.splitlines() if "RS301" in line] == [
        f"{ID}: RS301 G1.3: item 6 Consistent is unchecked in Statement",
        f"{ID}: RS301 G1.3: item 7 Respects non-goals is unchecked in Non goals"]
    assert out.splitlines()[-1].endswith("G1.3 failed")


# --- SC1.1: a person who declines to sign ----------------------------------------------

DECLINE = "A person who declines to sign gets no review record: run no writer, and go on to R7."
NOT_PASSED = "G1 has not passed for {id}. Fix each line above, then run /sdlc g1 {id} again."


def step(text: str, label: str) -> str:
    """One step of the flow: from its label at a line's start to the next step's
    label or the close of the instructions block."""
    found = re.search(rf"^{label}\. ", text, re.MULTILINE)
    assert found, f"the flow holds no {label}"
    rest = text[found.start():]
    end = re.search(r"\n\n[A-Z]+\d+\. |\n</instructions>", rest)
    return rest[:end.start()] if end else rest


def test_sc1_1_word_a_person_who_declines_to_sign_gets_no_record_and_the_verdict_reads_not_passed(
        repo, capsys):
    text = FLOW.read_text(encoding="utf-8")
    r6, r7 = step(text, "R6"), step(text, "R7")
    assert DECLINE in r6 and text.count(DECLINE) == 1
    assert NOT_PASSED in r7
    # no writer ran: no record file, and the verdict does not pass
    assert not (repo.root / RECORD).exists()
    code, out, err = check(capsys)
    assert code == 1 and err == ""
    assert out.splitlines()[-1].endswith("G1.3 to do")
    assert not (repo.root / RECORD).exists()
