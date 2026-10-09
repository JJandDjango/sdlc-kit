"""G1.2 suite (contract: g1-requirements-spec, unit s2-model).

A temporary repository per test: one ready contract under specs/, a
.sdlc/config.yaml that turns G1 on, the component declaration record at
specs/components.yaml, and each hard core's model and configuration. No
test needs TLC, P or Java on the machine: a stand-in stands on a PATH the
test sets, as a real child process behind a file named `tlc` or `p`. It
answers as TLC 2.19 was measured to answer, and as P's repository says the
P checker answers. It leaves a mark each time it starts, with its
arguments and its working folder, so a test can prove which calls ran and
that no tool ran.

What the unit pins: `g1-record model` runs each hard core's checker on its
model, for each hard core whose paths overlap the feature's scope, and
appends one record to .sdlc/g1/<id>.yaml; `g1-check` reads that record
against the declaration and the files on disk, runs no tool and writes
nothing. G1.2 reads done only from a record that shows each hard core in
scope passing and still matches the model's hash and the configuration's
(done_means); each hard core in scope has a model that TLC or P passes
(SC3.1); no hard core in scope passes it with no checker run (SC3.2); a
hard core with no model fails it with RS201, and a checker that is not
installed fails it with RS202 (SC3.3). The exit codes, each printed line,
the record's keys and the declaration's schema each have a case.

The fixture's `g1.schemas` pattern matches no file, so G1.1 reads `done`
in every summary line here, and no fixture holds a review record, so G1.3
reads `to do`.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

import jsonschema
import pytest
import yaml

import taskcontract
from conftest import write_seat_roster
from taskcontract.__main__ import main

ID = "apply-discount"
RECORD = f".sdlc/g1/{ID}.yaml"
RECORDED = f"recorded: {RECORD}"
DECLARATION = "specs/components.yaml"
SCHEMA_NAME = "component-declaration.schema.json"
NO_CORE = "G1.2: no hard core in scope"
ORACLES = ["differential", "fuzz", "property-only", "concurrency", "soak", "none"]

CONTRACT = """id: {id}
title: A fixture feature
intent: >
  A contract with a scope of its own, enough words to pass the door as a
  fixture for the G1.2 suite.
scope:
{scope}
non_goals:
  - nothing beyond the scope
decomposition:
  - unit: the unit
    id: the-unit
    confirmed_by: [user]
    done_means: the unit is done
    acceptance_sketch:
      - verify the unit is done
dependencies: []
entities: []
provenance:
  origin: human-request
"""

SPECTRAL = {"paths": ["api/*.yaml"], "linter": "spectral", "pin": ".spectral.yaml"}

# The design's drawing of specs/components.yaml, word for word.
DRAWING = """version: 1
components:
  - id: ledger
    paths: [src/ledger/]
    hard_core: true
    oracle: concurrency
    model: specs/models/ledger.tla
    model_config: specs/models/ledger.cfg
    checker: tlc
  - id: api
    paths: [src/api/]
    hard_core: false
    oracle: none
    oracle_reason: read-only pass-through, covered by its acceptance tests
"""

LEDGER = {"id": "ledger", "paths": ["src/ledger/"], "hard_core": True,
          "oracle": "concurrency", "model": "specs/models/ledger.tla",
          "model_config": "specs/models/ledger.cfg", "checker": "tlc"}
API = {"id": "api", "paths": ["src/api/"], "hard_core": False, "oracle": "none",
       "oracle_reason": "read-only pass-through, covered by its acceptance tests"}
WALLET = {"id": "wallet", "paths": ["src/wallet/"], "hard_core": True,
          "oracle": "property-only", "model": "specs/p/wallet.pproj",
          "model_config": "specs/p/wallet.check", "checker": "p"}
QUEUE = {"id": "queue", "paths": ["src/queue/"], "hard_core": True,
         "oracle": "concurrency", "model": "specs/models/queue.tla",
         "model_config": "specs/models/queue.cfg", "checker": "tlc"}
# A hard core outside the fixture's scope.
VAULT = {"id": "vault", "paths": ["lib/vault/"], "hard_core": True, "oracle": "soak",
         "model": "specs/models/vault.tla", "model_config": "specs/models/vault.cfg",
         "checker": "tlc"}

# The stand-in checker. It runs as `python stand_in.py <tool> <the tool's
# arguments>` behind a file named for the tool, logs each start beside
# itself, and ends on the exit code plan.json holds for the model.
#
# As TLC it follows the measured 2.19: `-metadir <folder>` names where its
# working files go, `-config <file>` the configuration, and the last word
# is the model. It writes a folder named from the clock under the metadir,
# or under `states/` in its working folder when the call holds no
# `-metadir`, and a run that finds that folder standing ends on exit 1. A
# model it cannot find ends on 150, a configuration it cannot find on 255.
# Its report goes to stdout.
#
# As P it takes two calls: `compile --pproj <file>`, then `check` with any
# words. `check` ends on the code planned for the project that was last
# compiled, and on 2 when none was.
STAND_IN = r'''
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOT_UTF8 = b"\x81\xff"
STAMP = "26-10-09-15-44-39"
TLC_LINES = {
    0: "Model checking completed. No error has been found.",
    11: "Error: Deadlock reached.",
    12: "Error: Invariant Inv is violated.",
    13: "Error: Temporal properties were violated.",
    75: "Error: TLC threw an unexpected exception.",
    150: "Error: Parsing or semantic analysis failed.",
    255: "The exception was a tlc2.tool.ConfigFileException",
}


def say(stream, text, plan):
    stream.write(text.encode("utf-8") + (NOT_UTF8 if plan.get("raw") else b"") + b"\n")


def tlc(plan, args, out, err):
    metadir = config = None
    rest, at = [], 0
    while at < len(args):
        if args[at] in ("-metadir", "-config") and at + 1 < len(args):
            if args[at] == "-metadir":
                metadir = args[at + 1]
            else:
                config = args[at + 1]
            at += 2
            continue
        rest.append(args[at])
        at += 1
    model = rest[-1] if rest else ""
    say(out, "TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)", plan)
    if not os.path.isfile(model):
        say(out, TLC_LINES[150], plan)
        return 150
    if config is not None and not os.path.isfile(config):
        say(out, TLC_LINES[255], plan)
        return 255
    work = os.path.join(metadir if metadir is not None else "states", STAMP)
    if os.path.exists(work):
        say(err, "the stand-in finds the folder of its run standing already", plan)
        return 1
    os.makedirs(work)
    name = os.path.splitext(os.path.basename(model))[0]
    with open(os.path.join(work, name + ".st"), "w", encoding="utf-8") as handle:
        handle.write("states\n")
    code = plan["tlc"].get(os.path.basename(model), 0)
    say(out, TLC_LINES.get(code, "Error: the stand-in ends on exit %d." % code), plan)
    return code


def p(plan, args, out, err):
    last = os.path.join(HERE, "compiled.txt")
    if args[:1] == ["compile"]:
        if os.path.exists(last):
            os.remove(last)
        name = args[args.index("--pproj") + 1] if "--pproj" in args[:-1] else ""
        if not os.path.isfile(name):
            say(err, "the stand-in finds no project file", plan)
            return 2
        code = plan["p"].get(os.path.basename(name), {}).get("compile", 0)
        if code == 0:
            with open(last, "w", encoding="utf-8") as handle:
                handle.write(os.path.basename(name))
            say(out, "the stand-in compiled the project", plan)
        else:
            say(err, "the stand-in cannot compile the project", plan)
        return code
    if args[:1] == ["check"]:
        if not os.path.isfile(last):
            say(err, "the stand-in finds no compiled project", plan)
            return 2
        with open(last, encoding="utf-8") as handle:
            name = handle.read()
        code = plan["p"].get(name, {}).get("check", 0)
        if code == 0:
            say(out, "the stand-in found 0 bugs", plan)
        elif code == 1:
            say(out, "the stand-in found 1 bug", plan)
        else:
            say(err, "the stand-in ends on an internal error", plan)
        return code
    say(err, "the stand-in takes compile and check", plan)
    return 2


def main():
    tool, args = sys.argv[1], sys.argv[2:]
    entry = {"tool": tool, "argv": args, "cwd": os.getcwd()}
    if tool == "tlc" and "-metadir" in args[:-1]:
        folder = args[args.index("-metadir") + 1]
        stood = os.path.isdir(folder)
        entry["metadir"] = {"path": os.path.abspath(folder), "stood": stood,
                            "held": sorted(os.listdir(folder)) if stood else []}
    with open(os.path.join(HERE, "calls.jsonl"), "a", encoding="utf-8") as log:
        log.write(json.dumps(entry) + "\n")
    with open(os.path.join(HERE, "plan.json"), encoding="utf-8") as handle:
        plan = json.load(handle)
    out, err = sys.stdout.buffer, sys.stderr.buffer
    if tool == "tlc":
        return tlc(plan, args, out, err)
    if tool == "p":
        return p(plan, args, out, err)
    return 0


sys.exit(main())
'''


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Repo:
    """One fixture repository at <tmp>/repo, and beside it <tmp>/bin, the
    only folder on PATH: empty until a test installs a stand-in there. The
    declaration holds the drawing's two components, and the hard core's
    model and configuration stand on disk."""

    def __init__(self, tmp: Path, monkeypatch):
        self.root = tmp / "repo"
        self.bin = tmp / "bin"
        self.root.mkdir()
        self.bin.mkdir()
        self.monkeypatch = monkeypatch
        write_seat_roster(self.root)
        self.contract(ID, "api/", "src/")
        self.config()
        self.components(LEDGER, API)
        self.core(LEDGER)
        self.plan()
        monkeypatch.setenv("PATH", str(self.bin))
        if os.name == "nt":
            monkeypatch.setenv("PATHEXT", ".COM;.EXE;.BAT;.CMD")
        monkeypatch.chdir(self.root)

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return path

    def contract(self, contract_id: str, *scope: str) -> None:
        entries = "\n".join(f"  - {s}" for s in scope)
        self.write(f"specs/{contract_id}/contract.yaml",
                   CONTRACT.format(id=contract_id, scope=entries))

    def config(self, active=("G0", "G1"), exempt=("controlled-language",)) -> None:
        """.sdlc/config.yaml as a person writes it."""
        self.write(".sdlc/config.yaml", yaml.safe_dump({
            "active_gates": list(active),
            "g1": {"exempt": list(exempt), "schemas": [SPECTRAL]}}, sort_keys=False))

    def components(self, *entries) -> None:
        """specs/components.yaml as a person writes it."""
        self.write(DECLARATION, yaml.safe_dump(
            {"version": 1, "components": list(entries)}, sort_keys=False))

    def core(self, entry: dict, config: str | None = None) -> tuple[Path, Path]:
        """Write a hard core's model and configuration: a TLA+ module and a
        TLC configuration, or a P project and the words of `p check`."""
        if entry["checker"] == "p":
            model = self.write(entry["model"], "<Project><ProjectName>Wallet</ProjectName>"
                                               "</Project>\n")
            words = "-tc tcTransfer\n  -s 100\n" if config is None else config
        else:
            name = Path(entry["model"]).stem
            model = self.write(entry["model"], f"---- MODULE {name} ----\n====\n")
            words = "SPECIFICATION Spec\nINVARIANT Inv\n" if config is None else config
        return model, self.write(entry["model_config"], words)

    def install(self, tool: str) -> None:
        """Put a stand-in named `tool` on PATH: a .cmd on Windows, as a TLC
        wrapper is there, an executable script elsewhere."""
        script = self.bin / "stand_in.py"
        script.write_text(STAND_IN, encoding="utf-8")
        if os.name == "nt":
            (self.bin / f"{tool}.cmd").write_text(
                f'@echo off\r\n"{sys.executable}" "{script}" {tool} %*\r\n'
                "exit /b %ERRORLEVEL%\r\n", encoding="utf-8", newline="")
        else:
            shim = self.bin / tool
            shim.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" {tool} "$@"\n',
                            encoding="utf-8", newline="")
            shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def plan(self, tlc=None, p=None, raw=False) -> None:
        """The exit code each run ends on. `tlc` maps a model's file name to
        TLC's exit code. `p` maps a project's file name to a mapping with
        `compile` and `check`, each call's exit code. A name the plan does
        not hold, and a call it does not hold, ends on 0. `raw` puts bytes
        that are no UTF-8 at the end of each line the stand-in prints."""
        (self.bin / "plan.json").write_text(json.dumps({
            "tlc": tlc or {}, "p": p or {}, "raw": raw}), encoding="utf-8")

    def calls(self) -> list[dict]:
        """Each start of a stand-in, in order: the mark it leaves."""
        log = self.bin / "calls.jsonl"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    def records(self) -> list[dict]:
        return yaml.safe_load((self.root / RECORD).read_text(encoding="utf-8"))["records"]

    def cores(self) -> list[dict]:
        """The entries of the last G1.2 record."""
        return [r for r in self.records() if r["condition"] == "G1.2"][-1]["cores"]

    def files(self) -> dict[str, bytes]:
        """Every file under the root with its bytes: what a call wrote shows
        as a difference."""
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in sorted(self.root.rglob("*")) if path.is_file()}

    def folders(self) -> set[str]:
        return {path.relative_to(self.root).as_posix()
                for path in self.root.rglob("*") if path.is_dir()}


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Repo:
    return Repo(tmp_path, monkeypatch)


def cli(capsys, *argv):
    """Run one taskcontract command in this process: (exit code, stdout,
    stderr). A command the parser does not hold fails here, by name."""
    words = [str(arg) for arg in argv]
    capsys.readouterr()
    try:
        code = main(words)
    except SystemExit:  # argparse refused the words themselves
        code = None
    out, err = capsys.readouterr()
    assert code is not None, (
        f"taskcontract does not take `{' '.join(words[:2])}`: "
        f"{(err.strip().splitlines() or ['no line'])[-1]}")
    return code, out, err


def model(capsys):
    """`g1-record model <id>`, run at the repository's root."""
    return cli(capsys, "g1-record", "model", ID)


def check(repo: Repo, capsys, *extra: str):
    return cli(capsys, "g1-check", ID, "--root", repo.root, *extra)


def summary(g1_2: str) -> str:
    return f"{ID}: G1.1 done, G1.2 {g1_2}, G1.3 to do"


def passes(component: str, tool: str = "tlc") -> str:
    return f"G1.2: the model of {component} passes {tool}"


def rs201(component: str) -> str:
    return f"G1.2: hard core {component} has no model"


def rs202(tool: str = "tlc") -> str:
    return f"G1.2: {tool} is not installed; install it and pin it in the repository"


def rs203(component: str, tool: str = "tlc") -> str:
    return f"G1.2: the model of {component} does not pass {tool}"


def entry_of(repo: Repo, core: dict, installed: bool, result) -> dict:
    """The record entry of one hard core as the files stand now."""
    config = repo.root / core["model_config"]
    return {"component": core["id"], "tool": core["checker"], "installed": installed,
            "model": {"path": core["model"], "sha256": sha(repo.root / core["model"])},
            "config": {"path": core["model_config"],
                       "sha256": sha(config) if config.exists() else None},
            "result": result}


def schema() -> dict:
    """The declaration's schema, from the package."""
    path = Path(taskcontract.__file__).parent / "schemas" / SCHEMA_NAME
    assert path.is_file(), f"the package holds no schemas/{SCHEMA_NAME}"
    return json.loads(path.read_text(encoding="utf-8"))


def passes_schema(doc) -> bool:
    return jsonschema.Draft202012Validator(schema()).is_valid(doc)


def g1_rules() -> dict[str, list[str]]:
    """G1's conditions with the codes each owns, from the packaged list."""
    path = Path(taskcontract.__file__).parent / "data" / "gates.yaml"
    gates = yaml.safe_load(path.read_text(encoding="utf-8"))["gates"]
    gate = next(g for g in gates if g["id"] == "G1")
    return {c["id"]: c.get("rules") for c in gate["conditions"]}


def same(path: str, other: Path) -> bool:
    """Whether two paths name one file or folder, whatever their slashes."""
    return os.path.samefile(path.replace("\\", "/"), other)


# --- SC3.1: each hard core in scope has a model, and TLC or P passes it ---

def test_sc3_1_a_passing_model_is_recorded_and_g1_2_reads_done(repo, capsys):
    repo.install("tlc")
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("ledger"), RECORDED]
    assert code == 0
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("done")]
    assert code == 1  # G1 is not done while G1.3 reads to do


def test_sc3_1_the_record_holds_one_entry_for_the_hard_core_with_the_whole_hashes(
        repo, capsys):
    repo.install("tlc")
    model(capsys)
    text = (repo.root / RECORD).read_text(encoding="utf-8")
    assert list(yaml.safe_load(text)) == ["records"]
    (record,) = repo.records()
    assert list(record) == ["condition", "at", "head", "cores"]
    assert record["condition"] == "G1.2"
    assert re.search(r"\bat: ['\"]?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z['\"]?\s", text)
    assert record["head"] == "no commit"  # no git on this PATH, as progress records it
    (entry,) = record["cores"]  # the component that is no hard core gets no entry
    # No tool version: a checker has no version call.
    assert list(entry) == ["component", "tool", "installed", "model", "config", "result"]
    assert entry == {
        "component": "ledger", "tool": "tlc", "installed": True,
        "model": {"path": "specs/models/ledger.tla",
                  "sha256": sha(repo.root / "specs/models/ledger.tla")},
        "config": {"path": "specs/models/ledger.cfg",
                   "sha256": sha(repo.root / "specs/models/ledger.cfg")},
        "result": "pass"}
    assert len(entry["model"]["sha256"]) == 64
    assert len(entry["config"]["sha256"]) == 64
    assert [p.name for p in (repo.root / ".sdlc" / "g1").iterdir()] == [f"{ID}.yaml"]


def test_sc3_1_tlc_starts_once_inside_the_models_folder_with_a_fresh_metadir(repo, capsys):
    repo.install("tlc")
    assert model(capsys)[0] == 0
    assert model(capsys)[0] == 0
    first, second = repo.calls()  # one start a run: no call for a version
    for call in (first, second):
        assert call["tool"] == "tlc"
        argv = call["argv"]
        assert len(argv) == 5  # no flag beside the two
        assert (argv[0], argv[2], argv[4]) == ("-metadir", "-config", "ledger.tla")
        assert os.path.isabs(argv[3])
        assert same(argv[3], repo.root / "specs/models/ledger.cfg")
        assert same(call["cwd"], repo.root / "specs/models")
        metadir = Path(call["metadir"]["path"])
        assert os.path.realpath(repo.root) not in [
            os.path.realpath(parent) for parent in (metadir, *metadir.parents)]
        assert call["metadir"]["held"] == []  # fresh: nothing stood in it
        assert not metadir.exists()  # and the call removed it, with what TLC wrote there
    assert first["metadir"]["path"] != second["metadir"]["path"]


def test_sc3_1_a_run_leaves_no_file_under_the_root_but_the_record(repo, capsys):
    """The configuration may stand in another folder than the model: it goes
    to TLC by its absolute path."""
    core = {**LEDGER, "model_config": "cfgs/strict.cfg"}
    repo.components(core, API)
    repo.core(core)
    repo.install("tlc")
    files, folders = repo.files(), repo.folders()
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("ledger"), RECORDED]
    assert code == 0
    after = repo.files()
    assert set(after) - set(files) == {RECORD}
    assert {path: after[path] for path in files} == files
    assert repo.folders() - folders == {".sdlc/g1"}
    (call,) = repo.calls()
    assert same(call["argv"][3], repo.root / "cfgs/strict.cfg")
    assert repo.cores()[0]["config"] == {"path": "cfgs/strict.cfg",
                                         "sha256": sha(repo.root / "cfgs/strict.cfg")}


@pytest.mark.parametrize("exit_code", [10, 11, 12, 13, 14])
def test_sc3_1_a_violation_tlc_finds_is_recorded_as_fail_and_g1_2_reads_failed(
        repo, capsys, exit_code):
    repo.install("tlc")
    repo.plan(tlc={"ledger.tla": exit_code})
    code, out, _ = model(capsys)
    assert out.splitlines() == [rs203("ledger"), RECORDED]
    assert code == 1
    assert repo.cores() == [entry_of(repo, LEDGER, True, "fail")]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS203 {rs203('ledger')}", summary("failed")]
    assert code == 1


@pytest.mark.parametrize("exit_code, line", [
    (1, "Error: the stand-in ends on exit 1."),
    (9, "Error: the stand-in ends on exit 9."),
    (15, "Error: the stand-in ends on exit 15."),
    (75, "Error: TLC threw an unexpected exception."),
    (150, "Error: Parsing or semantic analysis failed."),
    (255, "The exception was a tlc2.tool.ConfigFileException"),
])
def test_sc3_1_tlc_ending_on_an_error_of_its_own_gives_no_result(
        repo, capsys, exit_code, line):
    """An exit code that is neither 0 nor a violation is no result: the
    tool's lines are shown, nothing is written, and the last record stands."""
    repo.install("tlc")
    assert model(capsys)[0] == 0
    before = repo.files()
    repo.plan(tlc={"ledger.tla": exit_code})
    code, out, err = model(capsys)
    assert code == 2
    assert line in err.splitlines()
    assert out == ""
    assert repo.files() == before
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc3_1_a_configuration_whose_file_is_absent_gives_no_result_under_tlc(repo, capsys):
    (repo.root / LEDGER["model_config"]).unlink()
    repo.install("tlc")
    before = repo.files()
    code, out, err = model(capsys)
    assert code == 2
    assert len(repo.calls()) == 1  # TLC started, and ended on its own error
    assert "The exception was a tlc2.tool.ConfigFileException" in err.splitlines()
    assert out == ""
    assert repo.files() == before


def test_sc3_1_p_compiles_the_project_then_checks_it_with_the_configurations_words(
        repo, capsys):
    repo.components(WALLET)
    repo.core(WALLET, config="-tc tcTransfer\n  -s 100\n")
    repo.install("p")
    files = repo.files()
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("wallet", "p"), RECORDED]
    assert code == 0
    assert [call["argv"] for call in repo.calls()] == [
        ["compile", "--pproj", "wallet.pproj"],
        ["check", "-tc", "tcTransfer", "-s", "100"]]
    assert {call["tool"] for call in repo.calls()} == {"p"}
    for call in repo.calls():
        assert same(call["cwd"], repo.root / "specs/p")
    assert repo.cores() == [entry_of(repo, WALLET, True, "pass")]
    assert set(repo.files()) - set(files) == {RECORD}
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc3_1_a_bug_p_check_finds_is_recorded_as_fail_and_g1_2_reads_failed(repo, capsys):
    repo.components(WALLET)
    repo.core(WALLET)
    repo.install("p")
    repo.plan(p={"wallet.pproj": {"check": 1}})
    code, out, _ = model(capsys)
    assert out.splitlines() == [rs203("wallet", "p"), RECORDED]
    assert code == 1
    assert repo.cores() == [entry_of(repo, WALLET, True, "fail")]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS203 {rs203('wallet', 'p')}", summary("failed")]
    assert code == 1


@pytest.mark.parametrize("exit_code", [1, 2])
def test_sc3_1_a_p_compile_that_does_not_exit_0_gives_no_result(repo, capsys, exit_code):
    """Exit 1 from `p compile` is no bug found: only `p check` says that."""
    repo.components(WALLET)
    repo.core(WALLET)
    repo.install("p")
    repo.plan(p={"wallet.pproj": {"compile": exit_code}})
    before = repo.files()
    code, out, err = model(capsys)
    assert code == 2
    assert [call["argv"][0] for call in repo.calls()] == ["compile"]  # no check follows
    assert "the stand-in cannot compile the project" in err.splitlines()
    assert out == ""
    assert repo.files() == before


def test_sc3_1_p_check_ending_on_an_error_of_its_own_gives_no_result(repo, capsys):
    repo.components(WALLET)
    repo.core(WALLET)
    repo.install("p")
    assert model(capsys)[0] == 0
    before = repo.files()
    repo.plan(p={"wallet.pproj": {"check": 2}})
    code, out, err = model(capsys)
    assert code == 2
    assert "the stand-in ends on an internal error" in err.splitlines()
    assert out == ""
    assert repo.files() == before
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc3_1_a_configuration_whose_file_is_absent_gives_no_result_under_p(repo, capsys):
    repo.components(WALLET)
    repo.core(WALLET)
    (repo.root / WALLET["model_config"]).unlink()
    repo.install("p")
    before = repo.files()
    code, out, err = model(capsys)
    assert code == 2
    assert err.strip()
    assert out == ""
    assert repo.calls() == []  # the words are read before P starts
    assert repo.files() == before


def test_sc3_1_a_working_folder_that_cannot_be_made_is_a_call_the_writer_cannot_use(
        repo, capsys, monkeypatch):
    """TLC needs a working folder of its own. When none can be made, no tool
    starts and nothing is written, and the call exits 2: exit 1 would say
    the model does not pass."""
    repo.install("tlc")

    def refuse(*args, **kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(tempfile, "mkdtemp", refuse)
    before = repo.files()
    code, out, err = model(capsys)
    assert code == 2
    assert err.strip()
    assert out == ""
    assert repo.calls() == []
    assert repo.files() == before


def test_sc3_1_two_hard_cores_under_two_checkers_stand_in_one_record(repo, capsys):
    repo.components(LEDGER, API, WALLET)
    repo.core(WALLET)
    repo.install("tlc")
    repo.install("p")
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("ledger"), passes("wallet", "p"), RECORDED]
    assert code == 0
    (record,) = repo.records()  # one call, one record
    assert record["cores"] == [entry_of(repo, LEDGER, True, "pass"),
                               entry_of(repo, WALLET, True, "pass")]
    assert [call["tool"] for call in repo.calls()] == ["tlc", "p", "p"]
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc3_1_each_hard_core_has_its_own_result_in_the_declarations_order(repo, capsys):
    repo.components(WALLET, QUEUE, API, LEDGER)
    repo.core(WALLET)
    repo.core(QUEUE)
    repo.install("tlc")
    repo.install("p")
    repo.plan(tlc={"queue.tla": 12}, p={"wallet.pproj": {"compile": 0, "check": 0}})
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("wallet", "p"), rs203("queue"), passes("ledger"),
                                RECORDED]
    assert code == 1
    assert repo.cores() == [entry_of(repo, WALLET, True, "pass"),
                            entry_of(repo, QUEUE, True, "fail"),
                            entry_of(repo, LEDGER, True, "pass")]
    assert [call["argv"][-1] for call in repo.calls() if call["tool"] == "tlc"] == [
        "queue.tla", "ledger.tla"]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS203 {rs203('queue')}", summary("failed")]
    assert code == 1


def test_sc3_1_one_error_of_a_tools_own_leaves_no_entry_for_any_hard_core(repo, capsys):
    repo.components(LEDGER, WALLET)
    repo.core(WALLET)
    repo.install("tlc")
    repo.install("p")
    repo.plan(p={"wallet.pproj": {"compile": 2}})
    before = repo.files()
    code, out, _ = model(capsys)
    assert code == 2
    assert out == ""  # not even the line of the model that passed
    assert repo.files() == before
    assert not (repo.root / RECORD).exists()


def test_sc3_1_only_a_hard_core_whose_paths_overlap_the_scope_is_checked(repo, capsys):
    """One path of several is enough. A hard core outside the scope, and a
    component in scope that is no hard core, start no checker."""
    ledger = {**LEDGER, "paths": ["lib/ledger/", "src/ledger/"]}
    repo.components(VAULT, ledger, API)
    repo.core(VAULT)
    repo.install("tlc")
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("ledger"), RECORDED]
    assert code == 0
    assert [entry["component"] for entry in repo.cores()] == ["ledger"]
    assert [call["argv"][-1] for call in repo.calls()] == ["ledger.tla"]
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


@pytest.mark.parametrize("scope, path, overlap", [
    ("src/", "src/ledger/", True),
    ("src/ledger/core/", "src/ledger/", True),
    ("src/ledger/core.py", "src/ledger/", True),
    ("src/ledger/*.py", "src/ledger/", True),
    ("src/*/core.py", "src/ledger/", True),
    ("src/", "src/ledger/*.py", True),
    ("src/ledger/core.py", "src/ledger/*.py", True),
    ("src/ledger/c*.py", "src/ledger/*.py", True),
    ("src/ledger/core.py", "src/ledger/core.py", True),
    ("src/api/", "src/ledger/", False),
    ("src/ledger2/", "src/ledger/", False),
    ("src/ledger.py", "src/ledger/", False),
    ("docs/*.md", "src/ledger/", False),
    ("src/ledger/core.tla", "src/ledger/*.py", False),
    ("src/ledger/core.py", "src/ledger/other.py", False),
], ids=["a folder under the scope's folder", "the scope's folder under the folder",
        "the scope's file under the folder", "the scope's pattern under the folder",
        "a wildcard before the folder's name", "a pattern under the scope's folder",
        "a pattern that matches the scope's file", "two patterns under one folder",
        "the same file", "two folders apart", "a folder whose name only starts the same",
        "a file beside the folder", "a pattern in another folder",
        "a pattern that does not match the file", "two files"])
def test_sc3_1_a_hard_core_is_in_scope_when_a_path_and_a_scope_entry_overlap(
        repo, capsys, scope, path, overlap):
    """Neither side needs a file on disk: G1 reads before development."""
    repo.contract(ID, scope)
    repo.components({**LEDGER, "paths": [path]})
    repo.install("tlc")
    code, out, _ = model(capsys)
    assert code == 0
    if overlap:
        assert out.splitlines() == [passes("ledger"), RECORDED]
        assert len(repo.calls()) == 1
    else:
        assert out.splitlines() == [NO_CORE]
        assert repo.calls() == []
        assert not (repo.root / RECORD).exists()
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc3_1_the_checker_is_found_by_its_bare_name_and_no_other_program_starts(
        repo, capsys):
    """The kit starts `tlc`, never `java`, and makes no call for a version."""
    repo.install("java")
    repo.install("p")
    repo.install("tlc")
    assert model(capsys)[0] == 0
    assert [call["tool"] for call in repo.calls()] == ["tlc"]


def test_sc3_1_a_byte_that_is_not_utf8_in_the_checkers_lines_does_not_break_the_call(
        repo, capsys):
    repo.install("tlc")
    repo.plan(tlc={"ledger.tla": 12}, raw=True)
    code, out, _ = model(capsys)
    assert out.splitlines() == [rs203("ledger"), RECORDED]
    assert code == 1
    repo.plan(tlc={"ledger.tla": 150}, raw=True)
    code, out, err = model(capsys)
    assert code == 2
    assert out == ""
    assert any(line.startswith("Error: Parsing or semantic analysis failed.")
               for line in err.splitlines())
    assert len(repo.records()) == 1


# --- done_means: G1.2 reads done only when the record shows the model passing ---

def test_done_means_a_hard_core_in_scope_with_no_record_reads_to_do_and_lists_nothing(
        repo, capsys):
    repo.components()
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    repo.components(LEDGER, API)
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]  # a to do lists nothing
    assert code == 1


def test_done_means_a_model_changed_after_a_passing_run_returns_g1_2_to_to_do(repo, capsys):
    repo.install("tlc")
    model(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    (repo.root / LEDGER["model"]).write_bytes(b"---- MODULE ledger ----\nVARIABLE x\n====\n")
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]
    assert model(capsys)[0] == 0
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_done_means_a_configuration_changed_after_a_passing_run_returns_g1_2_to_to_do(
        repo, capsys):
    repo.install("tlc")
    model(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    repo.write(LEDGER["model_config"], "SPECIFICATION Spec\nINVARIANT Tight\n")
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]


def test_done_means_a_failed_entry_whose_model_changed_counts_as_absent(repo, capsys):
    repo.install("tlc")
    repo.plan(tlc={"ledger.tla": 12})
    assert model(capsys)[0] == 1
    assert check(repo, capsys)[1].splitlines()[-1] == summary("failed")
    (repo.root / LEDGER["model"]).write_bytes(b"---- MODULE ledger ----\nVARIABLE x\n====\n")
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]


def test_done_means_a_passing_entry_does_not_stand_for_another_configuration_or_checker(
        repo, capsys):
    """The entry names the configuration's path and the tool: a declaration
    that now names another of either has no record."""
    repo.install("tlc")
    model(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    other = {**LEDGER, "model_config": "specs/models/copy.cfg"}
    repo.components(other, API)
    repo.core(other)  # the same bytes under another name
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]
    repo.components({**LEDGER, "checker": "p"}, API)
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]
    repo.components(LEDGER, API)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_done_means_a_passing_entry_with_no_configuration_hash_never_reads_done(
        repo, capsys):
    """A result whose configuration's file is absent is no pinned result,
    also when the entry holds a null hash to match it."""
    repo.install("tlc")
    model(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    (repo.root / LEDGER["model_config"]).unlink()
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]
    doc = yaml.safe_load((repo.root / RECORD).read_text(encoding="utf-8"))
    doc["records"][-1]["cores"][0]["config"]["sha256"] = None
    repo.write(RECORD, yaml.safe_dump(doc, sort_keys=False))
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]
    assert code == 1


def test_done_means_a_hard_core_added_after_the_run_has_no_entry_so_g1_2_reads_to_do(
        repo, capsys):
    repo.install("tlc")
    model(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    repo.components(LEDGER, API, QUEUE)
    repo.core(QUEUE)
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]
    assert model(capsys)[0] == 0
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_done_means_each_call_appends_one_record_and_the_last_one_counts(repo, capsys):
    repo.install("tlc")
    assert model(capsys)[0] == 0
    repo.plan(tlc={"ledger.tla": 12})
    assert model(capsys)[0] == 1
    assert [r["cores"][0]["result"] for r in repo.records()] == ["pass", "fail"]
    assert check(repo, capsys)[1].splitlines()[-1] == summary("failed")
    repo.plan()
    assert model(capsys)[0] == 0
    assert [r["cores"][0]["result"] for r in repo.records()] == ["pass", "fail", "pass"]
    assert [r["condition"] for r in repo.records()] == ["G1.2"] * 3
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("done")]
    assert code == 1


def test_done_means_a_lint_record_and_a_model_record_stand_in_one_file(repo, capsys):
    """Each condition reads its own last record, whatever follows it."""
    repo.install("tlc")
    assert model(capsys)[0] == 0
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.write(".spectral.yaml", "rules: {}\n")
    code, out, _ = cli(capsys, "g1-record", "lint", ID)  # no spectral on PATH
    assert code == 1
    assert [r["condition"] for r in repo.records()] == ["G1.2", "G1.1"]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [
        f"{ID}: RS101 G1.1: spectral is not installed; install it and pin it in the "
        "repository",
        f"{ID}: G1.1 failed, G1.2 done, G1.3 to do"]
    assert code == 1
    repo.plan(tlc={"ledger.tla": 13})
    assert model(capsys)[0] == 1
    assert [r["condition"] for r in repo.records()] == ["G1.2", "G1.1", "G1.2"]
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {
        "note": "G1.1 failed, G1.2 failed, G1.3 to do",
        "findings": [
            {"feature": ID, "condition": "G1.1", "rule": "RS101",
             "message": "G1.1: spectral is not installed; install it and pin it in the "
                        "repository"},
            {"feature": ID, "condition": "G1.2", "rule": "RS203",
             "message": rs203("ledger")}]}
    assert code == 1


def test_done_means_a_record_file_that_cannot_be_read_counts_as_absent(repo, capsys):
    repo.install("tlc")
    model(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    repo.write(RECORD, "records: [not closed\n")
    code, out, _ = check(repo, capsys)
    assert out.splitlines()[-1] == f"{ID}: G1.1 done, G1.2 to do, G1.3 to do"
    assert not any(" RS" in line for line in out.splitlines())
    assert code == 1
    before, started = repo.files(), len(repo.calls())
    code, out, err = model(capsys)  # the writer refuses it before a tool starts
    assert code == 2
    assert err.strip()
    assert out == ""
    assert len(repo.calls()) == started
    assert repo.files() == before


def test_done_means_g1_2_reads_to_do_while_the_declaration_is_absent(repo, capsys):
    """Absent is not the empty list: with no declaration G1.2 reads to do,
    and the writer refuses the call."""
    repo.components()
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    (repo.root / DECLARATION).unlink()
    repo.install("tlc")
    before = repo.files()
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]
    assert code == 1
    code, out, err = model(capsys)
    assert code == 2
    assert ID in err
    assert out == ""
    assert repo.calls() == []
    assert repo.files() == before


ONE_STRING = object()  # `components` written as one string, where a list stands
NO_YAML = object()  # a file that is no YAML


@pytest.mark.parametrize("entry", [
    {**VAULT, "paths": "lib/vault/"},
    {**VAULT, "hard_core": "yes"},
    {**VAULT, "checker": "apalache"},
    {**VAULT, "oracle": "manual"},
    {"id": "vault", "paths": ["lib/vault/"], "hard_core": False, "oracle": "none"},
    {key: value for key, value in VAULT.items() if key != "model_config"},
    {key: value for key, value in VAULT.items() if key != "checker"},
    {key: value for key, value in VAULT.items() if key != "id"},
    {key: value for key, value in VAULT.items() if key != "paths"},
    {key: value for key, value in VAULT.items() if key != "hard_core"},
    {key: value for key, value in VAULT.items() if key != "oracle"},
    {**VAULT, "paths": []},
    "vault",
    ONE_STRING,
    NO_YAML,
], ids=["paths is no list", "hard_core is no boolean", "a checker the kit does not know",
        "an oracle outside the ratified values", "none with no oracle_reason",
        "a model with no model_config", "a model with no checker",
        "an entry with no id", "an entry with no paths", "an entry with no hard_core",
        "an entry with no oracle", "paths is an empty list",
        "an entry is no mapping", "components is no list", "the file is no YAML"])
def test_done_means_a_declaration_that_cannot_be_read_never_reads_done(repo, capsys, entry):
    """One entry the reader cannot use makes the whole declaration
    unreadable, also when it stands outside the scope beside a hard core
    whose record passes: G1.2 reads to do, and the writer refuses the call."""
    repo.install("tlc")
    assert model(capsys)[0] == 0
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    if entry is NO_YAML:
        repo.write(DECLARATION, "components: [not closed\n")
    else:
        doc = {"version": 1,
               "components": "ledger" if entry is ONE_STRING else [LEDGER, API, entry]}
        assert not passes_schema(doc)
        repo.write(DECLARATION, yaml.safe_dump(doc, sort_keys=False))
    before, started = repo.files(), len(repo.calls())
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]  # the passing record does not stand in
    assert code == 1
    code, out, err = model(capsys)
    assert code == 2
    assert ID in err
    assert out == ""
    assert len(repo.calls()) == started  # no checker started
    assert repo.files() == before  # and nothing was written


def test_done_means_the_declarations_schema_is_born_at_1_0_0_and_takes_the_drawing():
    doc = schema()
    assert doc["version"] == "1.0.0"
    contract = json.loads((Path(taskcontract.__file__).parent / "schemas"
                           / "task-contract.schema.json").read_text(encoding="utf-8"))
    assert isinstance(doc["$id"], str) and doc["$id"]
    assert doc["$id"] != contract["$id"]  # its own
    assert contract["version"] == "1.5.0"  # the contract's schema does not move
    assert passes_schema(yaml.safe_load(DRAWING))
    assert passes_schema({"version": 1, "components": []})  # the empty list says none


def test_done_means_the_schema_takes_each_ratified_oracle_and_both_checkers():
    for oracle in ORACLES:
        entry = {"id": "ledger", "paths": ["src/ledger/"], "hard_core": False,
                 "oracle": oracle}
        if oracle == "none":
            entry["oracle_reason"] = "covered by its acceptance tests"
        assert passes_schema({"version": 1, "components": [entry]}), oracle
    for core in (LEDGER, WALLET):
        assert passes_schema({"version": 1, "components": [core]}), core["checker"]
    # A hard core with no model is a declaration the reader can use: RS201 reads it.
    bare = {key: value for key, value in LEDGER.items()
            if key not in ("model", "model_config", "checker")}
    assert passes_schema({"version": 1, "components": [bare]})


def test_done_means_g1_check_runs_no_tool_and_writes_nothing(repo, capsys, tmp_path):
    repo.install("tlc")
    repo.plan(tlc={"ledger.tla": 12})
    model(capsys)
    before, started = repo.files(), len(repo.calls())
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    repo.monkeypatch.chdir(elsewhere)  # --root names the repository
    for extra in ((), ("--json",)):
        assert check(repo, capsys, *extra)[0] == 1
    assert check(repo, capsys)[1].splitlines()[-1] == summary("failed")
    assert len(repo.calls()) == started
    assert repo.files() == before
    assert list(elsewhere.iterdir()) == []
    repo.monkeypatch.chdir(repo.root)  # and with no --root, the working directory
    code, out, _ = cli(capsys, "g1-check", ID)
    assert out.splitlines()[-1] == summary("failed")
    assert code == 1


@pytest.mark.parametrize("case", ["not listed", "exempt", "no config"])
def test_done_means_a_feature_that_does_not_hold_g1_is_refused_with_exit_2(
        repo, capsys, case):
    repo.install("tlc")
    if case == "not listed":
        repo.config(active=("G0",))
    elif case == "exempt":
        repo.config(exempt=("controlled-language", ID))
    else:
        (repo.root / ".sdlc" / "config.yaml").unlink()
    before = repo.files()
    code, out, err = model(capsys)
    assert code == 2
    assert err.strip()
    assert out == ""
    assert repo.calls() == []  # no checker started
    assert repo.files() == before  # and nothing was written


def test_done_means_an_id_with_no_contract_is_a_call_the_writer_cannot_use(repo, capsys):
    repo.install("tlc")
    before = repo.files()
    code, out, err = cli(capsys, "g1-record", "model", "no-such-feature")
    assert code == 2
    assert err.strip()
    assert out == ""
    assert repo.calls() == []
    assert repo.files() == before


def test_done_means_each_code_reported_under_g1_2_is_one_g1_2_owns(repo, capsys):
    bare = {key: value for key, value in LEDGER.items()
            if key not in ("model", "model_config", "checker")}
    repo.components(bare)
    no_model = json.loads(check(repo, capsys, "--json")[1])["findings"]  # RS201
    repo.components(LEDGER)
    model(capsys)  # no checker on PATH: RS202
    not_installed = json.loads(check(repo, capsys, "--json")[1])["findings"]
    repo.install("tlc")
    repo.plan(tlc={"ledger.tla": 12})
    model(capsys)  # the checker finds a violation: RS203
    failing = json.loads(check(repo, capsys, "--json")[1])["findings"]
    found = no_model + not_installed + failing
    assert [f["rule"] for f in found] == ["RS201", "RS202", "RS203"]
    for finding in found:
        assert set(finding) == {"feature", "condition", "rule", "message"}
        assert finding["condition"] == "G1.2"
        assert finding["rule"] in (g1_rules()["G1.2"] or [])
        assert finding["message"].startswith("G1.2: ")


@pytest.mark.parametrize("contract", ["a YAML error", "no scope"])
def test_done_means_a_contract_whose_scope_cannot_be_read_never_reads_g1_2_done(
        repo, capsys, contract):
    """With no scope to read a hard core against, nothing shows that no hard
    core is in scope: G1.2 reads to do over a passing record, and the
    writer refuses the call."""
    repo.install("tlc")
    assert model(capsys)[0] == 0
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    path = f"specs/{ID}/contract.yaml"
    text = (repo.root / path).read_text(encoding="utf-8")
    if contract == "a YAML error":
        repo.write(path, text + "entities: [not closed\n")
    else:
        repo.write(path, "".join(
            line for line in text.splitlines(keepends=True)
            if not line.startswith(("scope:", "  - api/", "  - src/"))))
    before, started = repo.files(), len(repo.calls())
    note = json.loads(check(repo, capsys, "--json")[1])["note"]
    assert "G1.2 to do" in note
    code, out, err = model(capsys)
    assert code == 2
    assert ID in err
    assert out == ""
    assert len(repo.calls()) == started
    assert repo.files() == before


# --- SC3.2: no hard core in scope passes G1.2, and no checker runs ---

def test_sc3_2_a_feature_with_no_hard_core_in_scope_passes_g1_2_and_no_checker_runs(
        repo, capsys):
    repo.contract(ID, "api/", "src/api/")  # the hard core's folder is outside it
    repo.install("tlc")  # a checker stands ready, and leaves a mark if it starts
    repo.install("p")
    before = repo.files()
    code, out, _ = model(capsys)
    assert out.splitlines() == [NO_CORE]
    assert code == 0
    assert repo.calls() == []
    assert repo.files() == before
    assert not (repo.root / ".sdlc" / "g1").exists()
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("done")]
    assert code == 1
    assert repo.calls() == []


def test_sc3_2_an_empty_components_list_says_none_and_g1_2_reads_done(repo, capsys):
    repo.components()
    repo.install("tlc")
    before = repo.files()
    code, out, _ = model(capsys)
    assert out.splitlines() == [NO_CORE]
    assert code == 0
    assert repo.calls() == []
    assert repo.files() == before
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc3_2_components_in_scope_that_are_no_hard_core_pass_with_no_checker_on_the_machine(
        repo, capsys):
    repo.components(API, {**LEDGER, "hard_core": False})
    code, out, _ = model(capsys)  # PATH holds no checker at all
    assert out.splitlines() == [NO_CORE]
    assert code == 0
    assert not (repo.root / ".sdlc" / "g1").exists()
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {"note": "G1.1 done, G1.2 done, G1.3 to do", "findings": []}
    assert code == 1


# --- SC3.3: no model, or a checker that is not installed, fails G1.2 ---

def test_sc3_3_a_hard_core_with_no_model_fails_g1_2_and_gets_no_record(repo, capsys):
    bare = {key: value for key, value in LEDGER.items()
            if key not in ("model", "model_config", "checker")}
    repo.components(bare, API)
    repo.install("tlc")
    before = repo.files()
    code, out, _ = model(capsys)
    assert out.splitlines() == [rs201("ledger")]  # no record, so no `recorded:` line
    assert code == 1
    assert repo.calls() == []
    assert repo.files() == before
    code, out, _ = check(repo, capsys)  # the rule reads the declaration
    assert out.splitlines() == [f"{ID}: RS201 {rs201('ledger')}", summary("failed")]
    assert code == 1  # G1.2 does not pass


def test_sc3_3_g1_check_json_is_the_drawings_envelope_for_a_hard_core_with_no_model(
        repo, capsys):
    bare = {key: value for key, value in LEDGER.items()
            if key not in ("model", "model_config", "checker")}
    repo.components(bare, API)
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {
        "note": "G1.1 done, G1.2 failed, G1.3 to do",
        "findings": [{"feature": "apply-discount", "condition": "G1.2", "rule": "RS201",
                      "message": "G1.2: hard core ledger has no model"}]}
    assert code == 1


def test_sc3_3_a_model_whose_file_is_absent_is_no_model(repo, capsys):
    """Also over a record that passed while the file stood."""
    repo.install("tlc")
    assert model(capsys)[0] == 0
    (repo.root / LEDGER["model"]).unlink()
    before, started = repo.files(), len(repo.calls())
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS201 {rs201('ledger')}", summary("failed")]
    assert code == 1
    code, out, _ = model(capsys)
    assert out.splitlines() == [rs201("ledger")]
    assert code == 1
    assert len(repo.calls()) == started  # no checker starts on a model that is absent
    assert repo.files() == before


def test_sc3_3_one_hard_core_with_no_model_beside_one_that_passes(repo, capsys):
    bare = {key: value for key, value in LEDGER.items()
            if key not in ("model", "model_config", "checker")}
    repo.components(bare, WALLET)
    repo.core(WALLET)
    repo.install("p")
    code, out, _ = model(capsys)
    assert out.splitlines() == [rs201("ledger"), passes("wallet", "p"), RECORDED]
    assert code == 1
    assert repo.cores() == [entry_of(repo, WALLET, True, "pass")]  # no entry for ledger
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS201 {rs201('ledger')}", summary("failed")]
    assert code == 1


def test_sc3_3_a_checker_that_is_not_installed_is_recorded_and_fails_g1_2(repo, capsys):
    code, out, _ = model(capsys)  # PATH holds no tlc
    assert out.splitlines() == [rs202(), RECORDED]
    assert code == 1
    (record,) = repo.records()
    assert list(record) == ["condition", "at", "head", "cores"]
    (entry,) = record["cores"]
    assert list(entry) == ["component", "tool", "installed", "model", "config", "result"]
    assert entry == entry_of(repo, LEDGER, False, None)
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS202 {rs202()}", summary("failed")]
    assert code == 1  # G1.2 does not pass
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {
        "note": "G1.1 done, G1.2 failed, G1.3 to do",
        "findings": [{"feature": ID, "condition": "G1.2", "rule": "RS202",
                      "message": rs202()}]}
    assert code == 1


def test_sc3_3_a_checker_that_is_not_installed_fails_g1_2_with_the_configuration_absent_too(
        repo, capsys):
    """Neither installed nor pinned: the record of a tool that is not
    installed still counts, so G1.2 reads failed, never to do."""
    (repo.root / LEDGER["model_config"]).unlink()
    code, out, _ = model(capsys)  # PATH holds no tlc
    assert out.splitlines() == [rs202(), RECORDED]
    assert code == 1
    (entry,) = repo.cores()
    assert entry["installed"] is False
    assert entry["config"] == {"path": "specs/models/ledger.cfg", "sha256": None}
    assert entry["model"]["sha256"] == sha(repo.root / LEDGER["model"])
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS202 {rs202()}", summary("failed")]
    assert code == 1
    # The configuration written after the run: the entry no longer matches it.
    repo.core(LEDGER)
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]


def test_sc3_3_the_record_wins_over_the_readers_path_until_the_next_run(repo, capsys):
    assert model(capsys)[0] == 1
    repo.install("tlc")  # installed now, and not yet run
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS202 {rs202()}", summary("failed")]
    assert repo.calls() == []
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("ledger"), RECORDED]
    assert code == 0
    assert [r["cores"][0]["installed"] for r in repo.records()] == [False, True]
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc3_3_p_that_is_not_installed_fails_g1_2_with_its_own_name_beside_a_passing_tlc(
        repo, capsys):
    repo.components(LEDGER, WALLET)
    repo.core(WALLET)
    repo.install("tlc")  # another checker on PATH does not stand in for p
    code, out, _ = model(capsys)
    assert out.splitlines() == [passes("ledger"), rs202("p"), RECORDED]
    assert code == 1
    assert repo.cores() == [entry_of(repo, LEDGER, True, "pass"),
                            entry_of(repo, WALLET, False, None)]
    assert [call["tool"] for call in repo.calls()] == ["tlc"]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS202 {rs202('p')}", summary("failed")]
    assert code == 1


def test_sc3_3_two_hard_cores_under_one_checker_that_is_not_installed_get_one_line(
        repo, capsys):
    repo.components(LEDGER, QUEUE)
    repo.core(QUEUE)
    code, out, _ = model(capsys)  # PATH holds no tlc
    assert out.splitlines() == [rs202(), RECORDED]  # one line for the tool
    assert code == 1
    assert repo.cores() == [entry_of(repo, LEDGER, False, None),
                            entry_of(repo, QUEUE, False, None)]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS202 {rs202()}", summary("failed")]
    assert code == 1
