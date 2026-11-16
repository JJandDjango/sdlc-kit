"""A file that cannot be read stops no command (contract: g1-requirements-spec,
unit s9-one-line-refusals: checks SC3.3 and SC5.1, and done_means).

What the unit pins, each from "No hand-written file ends a command on a traceback"
in the design:

- each writer (`g1-record lint|model|review`) exits 2 with one line on stderr and
  writes nothing where it ended on a traceback: a record file that cannot be
  written, a NUL in a declared path or in a P configuration, and a damaged file
  of the kit's own (SC3.3);
- a date no calendar holds, written with no quotes, a contract that is not UTF-8
  and a scope number past 4300 digits are read as a YAML error by `tree._load`,
  `scope_check.contract_scope` and `g1._seat`, and stop no command (SC3.3, SC5.1);
- `g1-check` holds each reader's failure to one line, `{id}: unreadable G1
  reading: {condition} ({class}: {message})`, on stderr, with exit 2 (done_means);
- every command writes a character its output cannot hold as its backslash
  escape, through a pipe in a narrow code page (SC3.3);
- with G0 active, the tree goes on past a contract it cannot read (SC5.1);
- with RS302 the tree shows no review's evidence beside the line (SC5.1).

A temporary repository per test, with stand-in tools on a PATH the test sets (a
real child process behind a file named for the tool): no test needs a linter or
a checker on the machine. Commands run in this process, except where a test
needs a pipe or a damaged install: those run `python -m taskcontract` as a child
process, the damaged install as a copy of the package. Every test asserts the new
behavior, so none passes on today's code.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract
from taskcontract import g1, scope_check
from taskcontract.__main__ import main

ORIGINAL_PATH = os.environ.get("PATH", "")
CODE = Path(taskcontract.__file__).resolve().parent  # the package under test

ID = "apply-discount"
OTHER = "refund-order"
RECORD = f".sdlc/g1/{ID}.yaml"
RECORDED = f"recorded: {RECORD}"
CONFIG = ".sdlc/config.yaml"
COMPONENTS = "specs/components.yaml"
ROSTER = "specs/vocabulary/intake-seat.yaml"
CONTRACT = f"specs/{ID}/contract.yaml"
SCHEMA_NAME = "component-declaration.schema.json"

ALL = "1,2,3,4,5,6,7,8,9,10,11"
WIDE = "日"  # a character no Western code page holds
SECTION = f"Séc{WIDE}tion"  # one the code page holds, one it does not
NARROW = {"PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}
BROAD = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}

SPECTRAL = {"paths": ["api/*.yaml"], "linter": "spectral", "pin": ".spectral.yaml"}
LEDGER = {"id": "ledger", "paths": ["src/ledger/"], "hard_core": True,
          "oracle": "concurrency", "model": "specs/models/ledger.tla",
          "model_config": "specs/models/ledger.cfg", "checker": "tlc"}
API = {"id": "api", "paths": ["src/api/"], "hard_core": False, "oracle": "none",
       "oracle_reason": "read-only pass-through, covered by its acceptance tests"}
WALLET = {"id": "wallet", "paths": ["src/wallet/"], "hard_core": True,
          "oracle": "property-only", "model": "specs/p/wallet.pproj",
          "model_config": "specs/p/wallet.check", "checker": "p"}

SEAT_TERM = {"term": "intake-seat", "name": "Intake seat",
             "definition": "A human position that answers for a unit at intake.",
             "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
             "since": "2026-08-26"}

INTENT = ("A contract with a scope of its own, enough words to pass the door "
          "as a fixture for the suite of the one-line refusals.")
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


def unit(uid: str) -> dict:
    return {"unit": "work for " + uid, "id": uid, "confirmed_by": ["po"],
            "done_means": "the work for " + uid + " is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}


def contract_doc(cid: str, scope=("api/", "src/")) -> dict:
    return {"id": cid, "title": "A fixture feature", "intent": INTENT,
            "scope": list(scope), "non_goals": ["nothing beyond the scope"],
            "decomposition": [unit("u1-rate"), unit("u2-cap")], "dependencies": [],
            "entities": [], "provenance": {"origin": "human-request"}}


# The stand-in tool: `python stand_in.py <tool> <the tool's arguments>` behind a
# file named for the tool. It logs each start beside itself and answers from
# plan.json. As Spectral it follows the measured 6.17.0 (`--version` prints the
# version alone; `lint ... --format json` prints a JSON array of rows and exits 1
# when a row stands at `--fail-severity` or above). As TLC it follows the measured
# 2.19 (`-metadir <folder> -config <file> <model>`; the exit code the plan holds
# for the model). As P it takes `compile --pproj <file>`, then `check` with any
# words, and ends on the code planned for the compiled project.
STAND_IN = r'''
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAMP = "26-10-09-15-44-39"
TLC_LINES = {
    0: "Model checking completed. No error has been found.",
    11: "Error: Deadlock reached.",
    12: "Error: Invariant Inv is violated.",
}
VALUED = {"--ruleset": "--ruleset", "-r": "--ruleset", "--format": "--format",
          "-f": "--format", "--fail-severity": "--fail-severity", "-F": "--fail-severity"}


def say(stream, text):
    stream.write(text.encode("utf-8") + b"\n")


def split(args):
    options, rest, at = {}, [], 0
    while at < len(args):
        arg = args[at]
        if arg in VALUED:
            options.setdefault(VALUED[arg], []).append(args[at + 1] if at + 1 < len(args) else "")
            at += 2
            continue
        if arg.startswith("-"):
            options.setdefault("--quiet" if arg == "-q" else arg, []).append(True)
        else:
            rest.append(arg)
        at += 1
    return options, rest


def rel(path, root):
    return os.path.relpath(os.path.realpath(path), os.path.realpath(root)).replace(os.sep, "/")


def source(path):
    full = os.path.abspath(path).replace("\\", "/")
    return full[0].lower() + full[1:] if full[1:2] == ":" else full


def spectral(plan, args, out, err):
    options, files = split(args)
    if "--ruleset" not in options or not os.path.isfile(options["--ruleset"][-1]):
        say(err, "the stand-in finds no ruleset")
        return 2
    if not files or not all(os.path.isfile(name) for name in files):
        say(err, "No files found to lint.")
        return 2
    rows = []
    for name in files:
        for code, severity in plan["rows"].get(rel(name, plan["root"]), []):
            rows.append({"code": code, "path": [], "message": "The stand-in reports %s." % code,
                         "severity": severity,
                         "range": {"start": {"line": 0, "character": 0},
                                   "end": {"line": 1, "character": 18}},
                         "source": source(name)})
    if options.get("--format", ["stylish"])[-1] == "json":
        out.write(json.dumps(rows, indent="\t").encode("utf-8"))
    fail = {"error": 0, "warn": 1, "info": 2, "hint": 3}[
        options.get("--fail-severity", ["error"])[-1]]
    return 1 if any(row_["severity"] <= fail for row_ in rows) else 0


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
    say(out, "TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)")
    if not os.path.isfile(model):
        say(out, "Error: Parsing or semantic analysis failed.")
        return 150
    if config is not None and not os.path.isfile(config):
        say(out, "The exception was a tlc2.tool.ConfigFileException")
        return 255
    work = os.path.join(metadir if metadir is not None else "states", STAMP)
    if os.path.exists(work):
        say(err, "the stand-in finds the folder of its run standing already")
        return 1
    os.makedirs(work)
    name = os.path.splitext(os.path.basename(model))[0]
    with open(os.path.join(work, name + ".st"), "w", encoding="utf-8") as handle:
        handle.write("states\n")
    code = plan["tlc"].get(os.path.basename(model), 0)
    say(out, TLC_LINES.get(code, "Error: the stand-in ends on exit %d." % code))
    return code


def p(plan, args, out, err):
    last = os.path.join(HERE, "compiled.txt")
    if args[:1] == ["compile"]:
        if os.path.exists(last):
            os.remove(last)
        name = args[args.index("--pproj") + 1] if "--pproj" in args[:-1] else ""
        if not os.path.isfile(name):
            say(err, "the stand-in finds no project file")
            return 2
        code = plan["p"].get(os.path.basename(name), {}).get("compile", 0)
        if code == 0:
            with open(last, "w", encoding="utf-8") as handle:
                handle.write(os.path.basename(name))
            say(out, "the stand-in compiled the project")
        return code
    if args[:1] == ["check"]:
        if not os.path.isfile(last):
            say(err, "the stand-in finds no compiled project")
            return 2
        with open(last, encoding="utf-8") as handle:
            name = handle.read()
        code = plan["p"].get(name, {}).get("check", 0)
        say(out if code in (0, 1) else err, "the stand-in found %d bugs" % code)
        return code
    say(err, "the stand-in takes compile and check")
    return 2


def main():
    tool, args = sys.argv[1], sys.argv[2:]
    with open(os.path.join(HERE, "calls.jsonl"), "a", encoding="utf-8") as log:
        log.write(json.dumps({"tool": tool, "argv": args, "cwd": os.getcwd()}) + "\n")
    with open(os.path.join(HERE, "plan.json"), encoding="utf-8") as handle:
        plan = json.load(handle)
    out, err = sys.stdout.buffer, sys.stderr.buffer
    if tool == "spectral":
        if args == ["--version"]:
            say(out, plan["version"])
            return 0
        if args[:1] != ["lint"]:
            say(err, "the stand-in takes --version and lint")
            return 2
        return spectral(plan, args[1:], out, err)
    if tool == "tlc":
        return tlc(plan, args, out, err)
    return p(plan, args, out, err)


sys.exit(main())
'''


class Repo:
    """One fixture repository at <tmp>/<name>, with its tool folder <tmp>/<name>-bin,
    the only folder on PATH once `enter` ran. It holds a ratified seat roster, the
    contract of `apply-discount` and its pair at r5 and r4 (unless `docs` is
    False), a config that turns G0 and G1 on and declares the Spectral pin, one
    schema file, and a component declaration with the ledger (a TLC hard core in
    the contract's scope) and its model."""

    def __init__(self, tmp: Path, name: str = "repo", docs: bool = True):
        self.tmp = tmp
        self.root = tmp / name
        self.bin = tmp / f"{name}-bin"
        self.root.mkdir()
        self.bin.mkdir()
        self.write(ROSTER, yaml.safe_dump(SEAT_TERM, sort_keys=False))
        self.contract(ID)
        if docs:
            self.write(f"docs/features/{ID}.md", document(5))
            self.write(f"docs/features/{ID}.design.md", document(4))
        self.config()
        self.write(".spectral.yaml", "rules: {}\n")
        self.write("api/openapi.yaml", "openapi: 3.1.0\n")
        self.components(LEDGER, API)
        self.core(LEDGER)
        self.plan()

    def enter(self, monkeypatch) -> "Repo":
        """Make the tool folder the whole PATH and the root the working folder."""
        monkeypatch.setenv("PATH", str(self.bin))
        if os.name == "nt":
            monkeypatch.setenv("PATHEXT", ".COM;.EXE;.BAT;.CMD")
        monkeypatch.chdir(self.root)
        return self

    def write(self, rel: str, text) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def remove(self, rel: str) -> None:
        path = self.root / rel
        if path.is_file():
            path.unlink()

    def contract(self, cid: str, text=None) -> None:
        self.write(f"specs/{cid}/contract.yaml", yaml.safe_dump(
            contract_doc(cid), sort_keys=False) if text is None else text)

    def config(self, active=("G0", "G1"), exempt=(), schemas=(SPECTRAL,)) -> None:
        g1_ = {"exempt": list(exempt), "schemas": list(schemas)}
        self.write(CONFIG, yaml.safe_dump({"active_gates": list(active), "g1": g1_},
                                          sort_keys=False))

    def components(self, *entries) -> None:
        self.write(COMPONENTS, yaml.safe_dump(
            {"version": 1, "components": list(entries)}, sort_keys=False))

    def core(self, entry: dict, config: str | None = None) -> None:
        """A hard core's model and configuration: a TLA+ module and a TLC
        configuration, or a P project and the words of `p check`."""
        if entry["checker"] == "p":
            self.write(entry["model"], "<Project><ProjectName>Wallet</ProjectName></Project>\n")
            words = "-tc tcTransfer\n  -s 100\n" if config is None else config
        else:
            name = Path(entry["model"]).stem
            self.write(entry["model"], f"---- MODULE {name} ----\n====\n")
            words = "SPECIFICATION Spec\nINVARIANT Inv\n" if config is None else config
        self.write(entry["model_config"], words)

    def install(self, tool: str) -> None:
        """Put a stand-in named `tool` in the tool folder: a .cmd on Windows, an
        executable script elsewhere."""
        self.bin.mkdir(parents=True, exist_ok=True)
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

    def plan(self, rows=None, tlc=None, p=None, version="6.17.0") -> None:
        self.bin.mkdir(parents=True, exist_ok=True)
        (self.bin / "plan.json").write_text(json.dumps({
            "root": str(self.root), "rows": rows or {}, "version": version,
            "tlc": tlc or {}, "p": p or {}, "trace": False}), encoding="utf-8")

    def snapshot(self) -> dict:
        """Every path under the root, a folder as None: a refused call leaves no
        file and no empty folder either."""
        return {path.relative_to(self.root).as_posix():
                (path.read_bytes() if path.is_file() else None)
                for path in sorted(self.root.rglob("*"))}


@pytest.fixture(autouse=True)
def _no_git_above(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Repo:
    return Repo(tmp_path).enter(monkeypatch)


@pytest.fixture
def int_limit(monkeypatch):
    """Python's limit on an integer's text, as it ships: 4300 digits."""
    if not hasattr(sys, "set_int_max_str_digits"):
        pytest.skip("this Python sets no limit on an integer's text")
    held = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(4300)
    yield 4300
    sys.set_int_max_str_digits(held)


@pytest.fixture(scope="session")
def package(tmp_path_factory) -> Path:
    """A copy of the package under test, to damage one of its files: the folder
    that holds `taskcontract/`."""
    base = tmp_path_factory.mktemp("package")
    shutil.copytree(CODE, base / "taskcontract", ignore=shutil.ignore_patterns("__pycache__"))
    return base


def cli(capsys, *argv):
    """Run one taskcontract command in this process: (exit code, stdout, stderr).
    A command that ends on an exception gives a code that names it, so a test
    reads that as a failed assertion about the exit code."""
    words = [str(arg) for arg in argv]
    capsys.readouterr()
    try:
        code = main(words)
    except SystemExit:  # argparse refused the words themselves
        code = None
    except Exception as exc:  # a traceback: no command may end on one
        try:
            said = str(exc)[:120]
        except Exception:  # an error whose message cannot be made
            said = "no message"
        code = f"a traceback ({type(exc).__name__}: {said})"
    out, err = capsys.readouterr()
    assert code is not None, (
        f"taskcontract does not take `{' '.join(words[:4])}`: "
        f"{(err.strip().splitlines() or ['no line'])[-1]}")
    return code, out, err


def child(repo: Repo, *argv, env=None, package: Path | None = None):
    """Run `python -m taskcontract` as a child process in the repository: (exit
    code, stdout, stderr), the two streams as text with line ends as `\\n`."""
    full = dict(os.environ)
    full["PYTHONPATH"] = str(package if package is not None else CODE.parent)
    full["PATH"] = os.pathsep.join([str(repo.bin), ORIGINAL_PATH])
    full["GIT_CEILING_DIRECTORIES"] = str(repo.tmp)
    full["COLUMNS"] = "500"
    full.update(env if env is not None else BROAD)
    done = subprocess.run([sys.executable, "-m", "taskcontract", *[str(a) for a in argv]],
                          cwd=repo.root, env=full, capture_output=True)
    return (done.returncode, done.stdout.replace(b"\r\n", b"\n"),
            done.stderr.decode("utf-8", "replace").replace("\r\n", "\n"))


def check(capsys, feature: str = ID, *options):
    return cli(capsys, "g1-check", feature, *options)


def lint(capsys):
    return cli(capsys, "g1-record", "lint", ID)


def model(capsys):
    return cli(capsys, "g1-record", "model", ID)


def review(capsys, *extra):
    return cli(capsys, "g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po", *extra)


def passing(capsys):
    return review(capsys, "--checked", ALL)


def tree_print(capsys, *path):
    return cli(capsys, "tree", *path, "--root", ".")


WRITERS = {"lint": lint, "model": model, "review": passing}


def the_record_cannot_be_written(path: str = RECORD) -> str:
    return re.escape(f"taskcontract g1-record: the record cannot be written: {path} (") + r"\S[^\n]*\)\n"


# --- SC3.3: a record that cannot be written --------------------------------------------

@pytest.mark.parametrize("writer", sorted(WRITERS))
def test_sc3_3_a_record_that_cannot_be_written_ends_each_writer_in_one_line_and_writes_nothing(
        repo, capsys, writer):
    repo.install("spectral")
    repo.install("tlc")
    repo.write(".sdlc/g1", "a file where the record folder belongs\n")
    before = repo.snapshot()
    code, out, err = WRITERS[writer](capsys)
    assert (code, out) == (2, ""), (code, out, err)
    assert re.fullmatch(the_record_cannot_be_written(), err), err
    assert repo.snapshot() == before, "a refused writer wrote under the root"


@pytest.mark.parametrize("writer", sorted(WRITERS))
def test_sc3_3_a_value_error_while_the_record_is_written_ends_each_writer_as_an_os_error_does(
        repo, capsys, monkeypatch, writer):
    repo.install("spectral")
    repo.install("tlc")
    under_record_folder = re.compile(r"(^|/)\.sdlc/g1(/|$)")

    def refusing(original):
        def guarded(self, *args, **kwargs):
            if under_record_folder.search(self.as_posix()):
                raise UnicodeEncodeError("utf-8", WIDE, 0, 1, "the record cannot be encoded")
            return original(self, *args, **kwargs)
        return guarded

    for name in ("write_bytes", "write_text", "mkdir"):
        monkeypatch.setattr(Path, name, refusing(getattr(Path, name)))
    before = repo.snapshot()
    code, out, err = WRITERS[writer](capsys)
    assert (code, out) == (2, ""), (code, out, err)
    assert len(err.splitlines()) == 1 and "Traceback" not in err, err
    assert re.fullmatch(the_record_cannot_be_written(), err), err
    assert repo.snapshot() == before, "a refused writer wrote under the root"
    assert not (repo.root / RECORD).exists()


def test_sc3_3_a_hard_core_whose_checker_is_not_installed_reads_failed_and_its_record_is_one_line_when_unwritable(
        repo, capsys):
    # no tool is installed: the run of `model` is recorded as not installed
    code, out, err = model(capsys)
    assert (code, err) == (1, "")
    assert out.splitlines() == [
        "G1.2: tlc is not installed; install it and pin it in the repository", RECORDED]
    assert check(capsys)[1].splitlines()[0] == (
        f"{ID}: RS202 G1.2: tlc is not installed; install it and pin it in the repository")
    assert check(capsys)[1].splitlines()[-1] == f"{ID}: G1.1 to do, G1.2 failed, G1.3 to do"
    # the same run with a record folder that is a file ends in one line, writes nothing
    (repo.root / RECORD).unlink()
    (repo.root / ".sdlc" / "g1").rmdir()
    repo.write(".sdlc/g1", "a file where the record folder belongs\n")
    before = repo.snapshot()
    code, out, err = model(capsys)
    assert (code, out) == (2, ""), (code, out, err)
    assert re.fullmatch(the_record_cannot_be_written(), err), err
    assert repo.snapshot() == before


# --- SC3.3: a NUL in a declared path or in a P configuration --------------------------

def refused_with(capsys, writer, pattern: str, repo: Repo):
    before = repo.snapshot()
    code, out, err = WRITERS[writer](capsys)
    assert (code, out) == (2, ""), (code, out, err)
    assert re.fullmatch(pattern, err), err
    assert repo.snapshot() == before, "a refused writer wrote under the root"


def test_sc3_3_a_nul_in_the_pin_of_g1_schemas_makes_the_declaration_unreadable_for_lint(
        repo, capsys):
    repo.install("spectral")
    repo.write(CONFIG, 'active_gates: [G0, G1]\ng1:\n  exempt: []\n  schemas:\n'
                       '    - paths: ["api/*.yaml"]\n      linter: spectral\n'
                       '      pin: "a\\0b.yaml"\n')
    refused_with(capsys, "lint", re.escape(f"{ID}: g1.schemas cannot be read: ") + r"\S[^\n]*\n", repo)


def test_sc3_3_a_nul_in_a_model_configuration_path_makes_the_component_declaration_unreadable_for_model(
        repo, capsys):
    repo.install("tlc")
    repo.components(dict(LEDGER, model_config="specs/models/led\0ger.cfg"), API)
    refused_with(capsys, "model",
                 re.escape(f"{ID}: specs/components.yaml cannot be read: ") + r"\S[^\n]*\n", repo)


def test_sc3_3_a_nul_in_a_model_path_makes_the_component_declaration_unreadable_for_model(
        repo, capsys):
    repo.install("tlc")
    repo.components(dict(LEDGER, model="specs/models/led\0ger.tla"), API)
    refused_with(capsys, "model",
                 re.escape(f"{ID}: specs/components.yaml cannot be read: ") + r"\S[^\n]*\n", repo)


def test_sc3_3_a_nul_in_a_p_configuration_makes_that_configuration_unreadable_for_model(
        repo, capsys):
    repo.install("p")
    repo.config(schemas=[])
    repo.components(WALLET, API)
    repo.core(WALLET, config="-tc tcTransfer\n\x00 -s 1\n")
    refused_with(capsys, "model", re.escape(
        f"{ID}: the configuration of wallet cannot be read: specs/p/wallet.check\n"), repo)


# --- SC3.3: a file of the kit's own that is damaged ------------------------------------

DAMAGED = [("not-json", b"{"), ("empty", b""), ("not-utf-8", b"\xff\xfe\x00"), ("absent", None)]


@pytest.fixture
def damaged(package):
    """Damage one file of the package copy for a test, and mend it after."""
    schema = package / "taskcontract" / "schemas" / SCHEMA_NAME
    items = package / "taskcontract" / "data" / "g1-items.yaml"
    held = {path: path.read_bytes() for path in (schema, items)}

    def damage(path: Path, body):
        if body is None:
            path.unlink()
        else:
            path.write_bytes(body)

    yield damage, schema, items
    for path, body in held.items():
        path.write_bytes(body)


@pytest.mark.parametrize("kind, body", DAMAGED, ids=[case for case, _ in DAMAGED])
def test_sc3_3_a_damaged_schema_of_the_kit_ends_model_in_one_line_and_writes_nothing(
        repo, damaged, package, kind, body):
    damage, schema, _ = damaged
    damage(schema, body)
    repo.install("tlc")
    before = repo.snapshot()
    code, out, err = child(repo, "g1-record", "model", ID, package=package)
    assert (code, out) == (2, b""), (code, out, err)
    assert re.fullmatch(
        re.escape(f"taskcontract g1-record: the kit's schema cannot be read: {SCHEMA_NAME} (")
        + r"\S[^\n]*\)\n", err), err
    assert repo.snapshot() == before


def test_sc3_3_a_kit_schema_that_is_no_schema_ends_model_in_one_line_and_writes_nothing(
        repo, damaged, package):
    damage, schema, _ = damaged
    damage(schema, b"[1]")
    repo.install("tlc")
    before = repo.snapshot()
    code, out, err = child(repo, "g1-record", "model", ID, package=package)
    assert (code, out) == (2, b""), (code, out, err)
    assert len(err.splitlines()) == 1 and "Traceback" not in err, err
    assert repo.snapshot() == before


@pytest.mark.parametrize("kind, body", [("not-yaml", b"[\n"), ("absent", None)])
def test_sc3_3_a_damaged_items_file_of_the_kit_ends_review_in_one_line_and_writes_nothing(
        repo, damaged, package, kind, body):
    damage, _, items = damaged
    damage(items, body)
    before = repo.snapshot()
    code, out, err = child(repo, "g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po",
                           "--checked", ALL, package=package)
    assert (code, out) == (2, b""), (code, out, err)
    assert len(err.splitlines()) == 1 and "Traceback" not in err, err
    assert repo.snapshot() == before


@pytest.mark.parametrize("kind, body, cause", [
    ("not-yaml", b"[\n", "ParserError"), ("absent", None, "FileNotFoundError")])
def test_done_means_g1_check_holds_a_damaged_items_file_to_one_line_with_exit_2(
        repo, damaged, package, kind, body, cause):
    damage, _, items = damaged
    damage(items, body)
    before = repo.snapshot()
    for options in ((), ("--json",)):
        code, out, err = child(repo, "g1-check", ID, *options, package=package)
        assert (code, out) == (2, b""), (options, code, out, err)
        assert re.fullmatch(
            re.escape(f"{ID}: unreadable G1 reading: G1.3 ({cause}: ") + r"[^\n]+\)\n", err), err
    assert repo.snapshot() == before


# --- SC3.3: a date with no quotes, and a file that is no text, in each reader ----------

def unreadable_text(kind: str) -> bytes:
    """A contract the YAML loader or the decoder cannot read, by kind: one whose
    scope holds a date no calendar holds, a number past 4300 digits, or bytes that
    are no UTF-8."""
    if kind == "not-utf-8":
        return b"id: apply-discount\n\xff\xfe\n"
    doc = contract_doc(ID, scope=("api/", "src/", "PLACE"))
    text = yaml.safe_dump(doc, sort_keys=False)
    assert "- PLACE\n" in text
    return text.replace("PLACE", "2026-02-30" if kind == "no-calendar-date" else "9" * 5000).encode()


KINDS = ["no-calendar-date", "past-4300-digits", "not-utf-8"]


@pytest.mark.parametrize("kind", KINDS)
def test_sc3_3_contract_scope_reads_a_contract_it_cannot_decode_as_a_scope_that_cannot_be_read(
        repo, int_limit, kind):
    def scope() -> object:
        try:
            return scope_check.contract_scope(repo.root, ID)
        except Exception as exc:  # the loader's or the decoder's error leaks out
            return f"raised {type(exc).__name__}: {str(exc)[:80]}"

    # a contract with a YAML error reads as no scope, as it does today
    repo.contract(ID, b"id: [\n")
    assert scope() == []
    repo.contract(ID, unreadable_text(kind))
    assert scope() == []


def test_sc3_3_g1_seat_reads_a_roster_with_an_unquoted_impossible_date_as_a_yaml_error(
        repo, capsys):
    text = yaml.safe_dump(SEAT_TERM, sort_keys=False)
    assert "since: '2026-08-26'" in text
    refusal = f"{ID}: no ratified intake-seat term at {ROSTER}\n"
    repo.write(ROSTER, b"term: [\n")  # a YAML error: today's refusal
    assert passing(capsys) == (2, "", refusal)
    repo.write(ROSTER, text.replace("since: '2026-08-26'", "since: 2026-02-30"))
    before = repo.snapshot()
    assert passing(capsys) == (2, "", refusal)
    assert repo.snapshot() == before


@pytest.mark.parametrize("kind", KINDS)
def test_sc3_3_a_contract_that_cannot_be_read_stops_no_g1_command_and_reads_as_a_yaml_error_does(
        repo, capsys, int_limit, kind):
    repo.install("spectral")
    repo.install("tlc")
    commands = {"g1-check": lambda: check(capsys), "lint": lambda: lint(capsys),
                "model": lambda: model(capsys), "review": lambda: passing(capsys)}
    for active in (["G0"], ["G0", "G1"]):
        repo.config(active=active)
        repo.contract(ID, b"id: [\n")  # today's reading of a YAML error
        wanted = {name: run() for name, run in commands.items()}
        assert all(isinstance(code, int) for code, _, _ in wanted.values()), wanted
        repo.contract(ID, unreadable_text(kind))
        before = repo.snapshot()
        for name, run in commands.items():
            assert run() == wanted[name], (kind, active, name)
        assert repo.snapshot() == before
    # and for G1 active the words are the ones of a scope that cannot be read
    scope_line = f"{ID}: the contract's scope cannot be read at {CONTRACT}\n"
    assert model(capsys) == (2, "", scope_line)
    assert lint(capsys) == (2, "", scope_line)
    assert passing(capsys) == (2, "", scope_line)
    assert check(capsys) == (1, f"{ID}: G1.1 to do, G1.2 to do, G1.3 to do\n", "")


# --- done_means: g1-check holds each reader's failure to one line ---------------------

READERS = [("read_lint", "G1.1"), ("read_model", "G1.2"), ("read_review", "G1.3")]


@pytest.fixture
def prepared(repo, capsys):
    """A feature whose three readers each have a reading, and its files as they stand."""
    repo.install("spectral")
    repo.install("tlc")
    assert lint(capsys)[0] == 0 and model(capsys)[0] == 0 and passing(capsys)[0] == 0
    assert check(capsys) == (0, f"g1-green: {ID}\n", "")
    return repo


@pytest.mark.parametrize("reader, condition", READERS, ids=[row_[1] for row_ in READERS])
@pytest.mark.parametrize("options", [(), ("--json",)], ids=["text", "json"])
def test_done_means_g1_check_holds_a_reader_that_raises_to_one_line_with_exit_2(
        prepared, capsys, monkeypatch, reader, condition, options):
    def raises(*args, **kwargs):
        raise RuntimeError("no such\nreading")

    monkeypatch.setattr(g1, reader, raises)
    before = prepared.snapshot()
    code, out, err = check(capsys, ID, *options)
    assert (code, out) == (2, ""), (code, out, err)
    assert err == f"{ID}: unreadable G1 reading: {condition} (RuntimeError: no such reading)\n"
    assert prepared.snapshot() == before


def test_done_means_g1_check_names_the_class_alone_where_an_errors_message_cannot_be_made(
        prepared, capsys, monkeypatch):
    class Mute(Exception):
        def __str__(self):
            raise ValueError("no text")

    def mute(*args, **kwargs):
        raise Mute()

    monkeypatch.setattr(g1, "read_model", mute)
    assert check(capsys) == (2, "", f"{ID}: unreadable G1 reading: G1.2 (Mute)\n")


def test_done_means_g1_check_gives_one_line_for_the_first_of_several_readers_that_raise(
        prepared, capsys, monkeypatch):
    def raises(*args, **kwargs):
        raise RuntimeError("no such reading")

    for reader, _ in READERS:
        monkeypatch.setattr(g1, reader, raises)
    assert check(capsys) == (2, "", f"{ID}: unreadable G1 reading: G1.1 (RuntimeError: no such reading)\n")


# --- SC3.3: a character outside the code page, through a pipe -------------------------

def escaped(text: bytes) -> bytes:
    """What a stream of the narrow code page holds of a text: the character it holds
    as it is, the one it cannot hold as its backslash escape."""
    return text.decode("utf-8").encode("cp1252", "backslashreplace")


def both_ways(repo: Repo, *argv):
    """The same command through a pipe of a UTF-8 code page and of a narrow one:
    the broad run's reading, and the narrow run's, as (code, stdout bytes, stderr)."""
    return child(repo, *argv, env=BROAD), child(repo, *argv, env=NARROW)


def test_sc3_3_a_hard_core_with_no_model_reads_failed_with_its_error_through_a_narrow_pipe(
        repo):
    repo.components(dict(LEDGER, id=f"led{WIDE}ger"), API)
    repo.remove(LEDGER["model"])
    for argv, wanted in [(("g1-check", ID), 1), (("g1-record", "model", ID), 1)]:
        before = repo.snapshot()
        broad, narrow = both_ways(repo, *argv)
        assert broad[0] == wanted and WIDE in broad[1].decode("utf-8"), broad
        assert broad[2] == "" == narrow[2], (argv, narrow)
        assert narrow[0] == wanted and narrow[1] == escaped(broad[1]), (argv, narrow)
        assert b"\\u65e5" in narrow[1] and WIDE.encode("utf-8") not in narrow[1]
        assert repo.snapshot() == before  # no model: a message and no record
    assert narrow[1] == f"G1.2: hard core led\\u65e5ger has no model\n".encode()


def test_sc3_3_g1_record_review_writes_a_character_its_output_cannot_hold_as_its_escape(
        repo):
    argv = ("g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po",
            "--checked", "1,2,3,4,5,7,8,9,10,11", "--unchecked", f"6={SECTION}")
    broad = child(repo, *argv, env=BROAD)
    assert broad[0] == 1 and broad[2] == ""
    assert broad[1].decode("utf-8").splitlines() == [
        f"G1.3: item 6 Consistent is unchecked in {SECTION}", RECORDED]
    narrow = child(repo, *argv, env=NARROW)
    assert narrow[0] == 1 and narrow[2] == ""
    assert narrow[1] == escaped(broad[1])
    assert narrow[1].decode("cp1252").splitlines() == [
        "G1.3: item 6 Consistent is unchecked in Séc\\u65e5tion", RECORDED]


def test_sc5_1_each_condition_takes_its_status_from_its_own_rules_and_each_diagnostic_prints_through_a_narrow_pipe(
        repo, capsys):
    repo.install("spectral")
    repo.install("tlc")
    repo.components(dict(LEDGER, id=f"led{WIDE}ger"), API)
    repo.remove(LEDGER["model"])
    assert lint(capsys)[0] == 0  # G1.1 reads done from its record
    assert review(capsys, "--checked", "1,2,4,5,7,8,9,10,11", "--unchecked", f"3=Other",
                  "--unchecked", f"6={SECTION}")[0] == 1
    broad_check, narrow_check = both_ways(repo, "g1-check", ID)
    lines = broad_check[1].decode("utf-8").splitlines()
    assert broad_check[0] == 1
    assert lines[-1] == f"{ID}: G1.1 done, G1.2 failed, G1.3 failed"
    assert sorted(lines[:-1]) == sorted([
        f"{ID}: RS201 G1.2: hard core led{WIDE}ger has no model",
        f"{ID}: RS301 G1.3: item 3 Traceable is unchecked in Other",
        f"{ID}: RS301 G1.3: item 6 Consistent is unchecked in {SECTION}"])
    assert narrow_check[0] == 1 and narrow_check[2] == ""
    assert narrow_check[1] == escaped(broad_check[1])
    broad_tree, narrow_tree = both_ways(repo, "tree", "--root", ".")
    text = broad_tree[1].decode("utf-8")
    for line in (f"  {ID}/G1 Requirements / Spec [failed]",
                 f"    {ID}/G1/G1.1 Spec/schema linting [done]",
                 f"    {ID}/G1/G1.2 Model checking [failed]",
                 f"      - G1.2: hard core led{WIDE}ger has no model",
                 f"      - G1.3: item 3 Traceable is unchecked in Other",
                 f"      - G1.3: item 6 Consistent is unchecked in {SECTION}"):
        assert line in text.splitlines(), line
    assert any(line.startswith(f"    {ID}/G1/G1.3 ") and "[failed]" in line
               for line in text.splitlines())
    assert narrow_tree[0] == 0 and narrow_tree[1] == escaped(broad_tree[1])


# --- SC5.1: with G0 active, the tree goes on past a contract it cannot read -----------

def settled(out: str) -> str:
    """The tree's text with the message of an unreadable contract's diagnostic made
    one word: the loader's and the decoder's messages differ."""
    return re.sub(r"(?m)^(\s+- unreadable contract: ).*$", r"\1<message>", out)


def reasons(err: str) -> str:
    return re.sub(r"(?m)^(taskcontract tree: unreadable contract: \S+) \(.*\)$", r"\1 (<reason>)", err)


@pytest.mark.parametrize("kind", KINDS)
def test_sc5_1_the_tree_goes_on_past_a_contract_it_cannot_read_and_prints_it_as_an_unreadable_contract(
        repo, capsys, int_limit, kind):
    repo.contract(OTHER)
    repo.write(f"docs/features/{OTHER}.md", document(5, OTHER))
    for label, active in (("no config", None), ("G0", ["G0"]), ("G0 and G1", ["G0", "G1"])):
        if kind == "not-utf-8" and active is None:
            continue  # the print goes on there today
        if active is None:
            (repo.root / CONFIG).unlink(missing_ok=True)
        else:
            repo.config(active=active)
        repo.contract(ID, b"id: [\n")  # a YAML error: the print goes on today
        code, wanted_out, wanted_err = tree_print(capsys)
        assert code == 0, (label, wanted_err)
        repo.contract(ID, unreadable_text(kind))
        code, out, err = tree_print(capsys)
        assert code == 0, (kind, label, code)
        assert f"{OTHER}" in out and f"{ID}" in out
        assert settled(out) == settled(wanted_out), (kind, label)
        assert reasons(err) == reasons(wanted_err), (kind, label, err)
        problem = re.search(
            rf"(?m)^taskcontract tree: unreadable contract: {re.escape(CONTRACT)} \((.*)\)$", err)
        assert problem, (kind, label, err)
        reason = problem.group(1)
        if kind == "not-utf-8":
            assert reason == "cannot be read", reason
        else:
            assert re.fullmatch(r"YAML error( at line \d+)?", reason), reason
        if active is not None:
            assert "unreadable contract: " in out, (kind, label)


# --- SC5.1: with RS302 the tree shows no review's evidence beside the line ------------

G1_3 = "Criteria completeness + ambiguity review"
RS302 = (f"G1.3: no feature document at docs/features/{ID}.md; write it and run intake "
         f"again, or add {ID} to g1.exempt")


def test_sc5_1_the_tree_shows_no_review_evidence_beside_the_line_of_rs302(repo, capsys):
    evidence = " by po at r5, design r4"
    assert passing(capsys)[0] == 0
    out = tree_print(capsys)[1].splitlines()
    assert f"    {ID}/G1/G1.3 {G1_3} [done]{evidence}" in out
    assert tree_print(capsys, f"{ID}/G1/G1.3")[1].splitlines()[0] == (
        f"{ID}/G1/G1.3 {G1_3} [done]{evidence}")
    # an unchecked item: G1.3 reads failed, and the evidence stays
    assert review(capsys, "--checked", "1,2,3,4,5,7,8,9,10,11", "--unchecked", "6=Statement")[0] == 1
    out = tree_print(capsys)[1].splitlines()
    assert f"    {ID}/G1/G1.3 {G1_3} [failed]{evidence}" in out
    # no feature document: RS302, and the review's evidence stands nowhere
    assert passing(capsys)[0] == 0
    repo.remove(f"docs/features/{ID}.md")
    code, out_text, err = tree_print(capsys)
    assert (code, err) == (0, "")
    out = out_text.splitlines()
    assert f"    {ID}/G1/G1.3 {G1_3} [failed]" in out, out
    at = out.index(f"    {ID}/G1/G1.3 {G1_3} [failed]")
    assert out[at + 1] == f"      - {RS302}"
    assert not any(line.startswith(f"    {ID}/G1/G1.3 ") and "by po" in line for line in out)
    assert tree_print(capsys, f"{ID}/G1/G1.3")[1].splitlines()[0] == f"{ID}/G1/G1.3 {G1_3} [failed]"
    assert "by po" not in tree_print(capsys, f"{ID}/G1/G1.3")[1]
    assert check(capsys)[1].splitlines()[0] == f"{ID}: RS302 {RS302}"
