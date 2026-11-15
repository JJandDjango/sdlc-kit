"""G1 reads only what a tool or a review checked (contract: g1-requirements-spec,
unit s8-honest-reads: checks SC2.1+SC3.1, SC4.1 and SC5.2, and done_means).

What the unit pins, each from "The edges ruled at r16" of the design:

- a `.sdlc/config.yaml` that stands and cannot be read is never read as G1 off:
  `new` exits 1, `progress start|done` and `g1-check|g1-record` exit 2, each with
  one line (SC4.1, SC4.2's refusal, done_means);
- G1 is no active gate for a contract whose origin is `g8-escape` or
  `g9-maintenance`, and `new --origin` writes the origin (SC4.1, SC5.2);
- the tree's second build reads `g1.exempt` (SC5.2);
- a `g1.schemas` pattern that matches no file, is absolute, holds `..`, differs
  from the disk in case, or lies in `.git` makes the declaration unreadable; a
  leading `./` is dropped; `lint` with no `g1.schemas` key refuses (SC2.1);
- a linter or a checker that resolves inside the repository is refused (SC2.1,
  SC3.1);
- a G1.2 record binds the model's folder; a record of the two-file form counts
  as absent; a P configuration with no `-tc` is refused; two components with one
  id, or a model path outside the repository, make the declaration unreadable
  (SC3.1).

A temporary repository per test, with stand-in tools on a PATH the test sets (a
real child process behind a file named for the tool): no test needs a linter or
a checker on the machine. Every test asserts the new behavior, so none passes on
today's code. The live runs (Spectral, TLC) are manual receipts.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

import pytest
import yaml

from taskcontract import tree
from taskcontract.__main__ import main
from taskcontract.scaffold import scaffold

ROOT = Path(__file__).resolve().parent.parent
if not (ROOT / "skills").is_dir():  # run from a scratch folder: read the tree at the cwd
    ROOT = Path.cwd()
INTAKE = ROOT / "skills" / "sdlc" / "flows" / "intake.md"

ID = "apply-discount"
OTHER = "refund-order"
U = "u1-rate"
UNIT = f"{ID}/{U}"
TASK = f"{UNIT}/write-tests"
OTHER_UNIT = f"{OTHER}/{U}"
OTHER_TASK = f"{OTHER_UNIT}/write-tests"
RECORD = f".sdlc/g1/{ID}.yaml"
RECORDED = f"recorded: {RECORD}"
CONFIG = ".sdlc/config.yaml"
COMPONENTS = "specs/components.yaml"
ROSTER = "specs/vocabulary/intake-seat.yaml"
PROBLEM = "taskcontract tree: "
TO_DO, DONE, FAILED = "to do", "done", "failed"
ERROR, WARNING = 0, 1  # Spectral's severities
ABSENT = object()

NAMES = ["Testable", "Unambiguous", "Traceable", "Complete over units",
         "Covers the sketch", "Consistent", "Respects non-goals",
         "Boundary + error paths", "Property-spec applicability",
         "Schema presence", "Oracle designation answered"]
ALL = "1,2,3,4,5,6,7,8,9,10,11"

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
          "as a fixture for the suite of the honest reads.")
TITLE = "# {id} - A fixture feature\n\n"
HEAD = "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"
ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
SUMMARY = re.compile(rf"^{ID}: G1\.1 (?P<g1_1>[a-z ]+), G1\.2 (?P<g1_2>[a-z ]+), "
                     r"G1\.3 (?P<g1_3>[a-z ]+)$")


def message_8(feature: str) -> str:
    return (f"taskcontract new: no feature document for {feature}, and G1 is active for "
            f"it; write docs/features/{feature}.md, or add {feature} to g1.exempt")


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


def contract_doc(cid: str, origin: str = "human-request", units=(U, "u2-cap")) -> dict:
    provenance = {"origin": origin}
    if origin != "human-request":
        provenance["ref"] = "ticket-1"
    return {"id": cid, "title": "A fixture feature", "intent": INTENT,
            "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
            "decomposition": [unit(uid) for uid in units], "dependencies": [],
            "entities": [], "provenance": provenance}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# The stand-in tool: `python stand_in.py <tool> <the tool's arguments>` behind a
# file named for the tool. It logs each start beside itself and answers from
# plan.json. As Spectral it follows the measured 6.17.0 (`--version` prints the
# version alone; `lint ... --format json` prints a JSON array of rows and exits 1
# when a row stands at `--fail-severity` or above). As TLC it follows the measured
# 2.19 (`-metadir <folder> -config <file> <model>`; the exit code the plan holds
# for the model; with `trace` set it writes a `<model>_TTrace_<n>.tla` beside the
# model, as TLC does on a violation). As P it takes `compile --pproj <file>`, then
# `check` with any words, and ends on the code planned for the compiled project.
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
    if plan.get("trace"):
        with open(os.path.join(HERE, "calls.jsonl"), encoding="utf-8") as log:
            number = len(log.read().splitlines())
        beside = os.path.dirname(os.path.abspath(model))
        for ext in (".tla", ".bin"):
            with open(os.path.join(beside, "%s_TTrace_17000000%02d%s" % (name, number, ext)),
                      "w", encoding="utf-8") as handle:
                handle.write("---- MODULE trace ----\n====\n")
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
    contract of `apply-discount` (unless `feature` is False) and its pair at r5 and
    r4 (unless `docs` is False), a config that turns G0 and G1 on and declares the
    Spectral pin, one schema file, and a component declaration with the ledger
    (a TLC hard core in the contract's scope) and its model."""

    def __init__(self, tmp: Path, name: str = "repo", feature: bool = True, docs: bool = True,
                 origin: str = "human-request"):
        self.tmp = tmp
        self.root = tmp / name
        self.bin = tmp / f"{name}-bin"
        self.root.mkdir()
        self.bin.mkdir()
        self.write(ROSTER, yaml.safe_dump(SEAT_TERM, sort_keys=False))
        if feature:
            self.contract(ID, origin)
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

    def contract(self, cid: str, origin: str = "human-request") -> None:
        self.write(f"specs/{cid}/contract.yaml", yaml.safe_dump(
            contract_doc(cid, origin), sort_keys=False))

    def config(self, active=("G0", "G1"), exempt=(), schemas=(SPECTRAL,)) -> None:
        """.sdlc/config.yaml as a person writes it; ABSENT leaves `schemas` out."""
        g1 = {"exempt": list(exempt)}
        if schemas is not ABSENT:
            g1["schemas"] = list(schemas)
        self.write(CONFIG, yaml.safe_dump({"active_gates": list(active), "g1": g1},
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

    def plan(self, rows=None, tlc=None, p=None, trace=False, version="6.17.0") -> None:
        self.bin.mkdir(parents=True, exist_ok=True)
        (self.bin / "plan.json").write_text(json.dumps({
            "root": str(self.root), "rows": rows or {}, "version": version,
            "tlc": tlc or {}, "p": p or {}, "trace": trace}), encoding="utf-8")

    def calls(self) -> list[dict]:
        log = self.bin / "calls.jsonl"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    def files(self) -> dict[str, bytes]:
        """Every file under the root with its bytes: what a call wrote shows."""
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in sorted(self.root.rglob("*")) if path.is_file()}

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


def cli(capsys, *argv):
    """Run one taskcontract command in this process: (exit code, stdout, stderr)."""
    words = [str(arg) for arg in argv]
    capsys.readouterr()
    try:
        code = main(words)
    except SystemExit:  # argparse refused the words themselves
        code = None
    out, err = capsys.readouterr()
    assert code is not None, (
        f"taskcontract does not take `{' '.join(words[:4])}`: "
        f"{(err.strip().splitlines() or ['no line'])[-1]}")
    return code, out, err


def new(capsys, repo: Repo, feature: str = ID, *extra: str):
    return cli(capsys, "new", feature, "--root", repo.root, *extra)


def check(repo: Repo, capsys, feature: str = ID):
    return cli(capsys, "g1-check", feature, "--root", repo.root)


def lint(capsys):
    return cli(capsys, "g1-record", "lint", ID)


def model(capsys):
    return cli(capsys, "g1-record", "model", ID)


def review(capsys):
    return cli(capsys, "g1-record", "review", ID, "--by", "Ann Lee", "--seat", "po",
               "--checked", ALL)


def progress(repo: Repo, capsys, action: str, rid: str, *options):
    return cli(capsys, "progress", action, rid, "--root", repo.root, *options)


def tree_print(repo: Repo, capsys):
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0, err
    return out, err


def statuses(out: str) -> tuple[str, str, str]:
    """G1.1, G1.2 and G1.3 as the last line of `g1-check` reads them."""
    last = out.splitlines()[-1]
    if last == f"g1-green: {ID}":  # the green line stands for three `done`
        return DONE, DONE, DONE
    match = SUMMARY.match(last)
    assert match, f"no summary line: {out!r}"
    return match["g1_1"], match["g1_2"], match["g1_3"]


def clean(path: str, tool: str = "spectral") -> str:
    return f"G1.1: {path} lints clean under {tool}"


def rs102(path: str, n: int, tool: str = "spectral") -> str:
    return f"G1.1: {path} does not lint clean: {tool} reports {n}"


def passes(component: str, tool: str = "tlc") -> str:
    return f"G1.2: the model of {component} passes {tool}"


def rows_of(out: str) -> dict:
    """Each tree item's (status, rest of its line) by id."""
    rows = {}
    for text in out.splitlines():
        item = ITEM.match(text)
        if item:
            rows[item["id"]] = (item["tag"], item["rest"])
    return rows


def block(out: str, fid: str) -> list[str]:
    """The feature's own lines: its line, then every line under it."""
    lines = out.splitlines()
    start = next(n for n, text in enumerate(lines) if text.startswith(f"{fid} "))
    size = next((n for n, text in enumerate(lines[start + 1:]) if not text.startswith(" ")),
                len(lines) - start - 1)
    return lines[start:start + 1 + size]


def verdicts(out: str, fid: str) -> list[str]:
    """The feature's gate lines, in print order."""
    return [text for text in block(out, fid)
            if re.fullmatch(rf"  {re.escape(fid)}/G\d+ .*", text)]


# --- a config that stands and cannot be read is never read as G1 off ---------------------

UNREADABLE = [
    ("not-utf-8", b"active_gates: [G0, G1]\n\xff\xfe\x00"),
    ("no-yaml", b"active_gates: [G0, G1\n"),
    ("no-mapping", b"- G0\n- G1\n"),
    ("active-gates-no-list", b"active_gates: G1\n"),
    ("active-gates-no-text", b"active_gates: [G0, 5]\n"),
    ("g1-no-mapping", b"active_gates: [G0, G1]\ng1: [exempt]\n"),
    ("exempt-no-list", b"active_gates: [G0, G1]\ng1:\n  exempt: apply-discount\n"),
    ("exempt-no-text", b"active_gates: [G0, G1]\ng1:\n  exempt: [5]\n"),
]
UNREADABLE_IDS = [case for case, _ in UNREADABLE]


@pytest.mark.parametrize("docs", ["a-plain-request", "a-pair"])
@pytest.mark.parametrize("case, held", UNREADABLE, ids=UNREADABLE_IDS)
def test_sc4_1_new_refuses_a_config_it_cannot_read_and_an_absent_one_means_no_gate(
        tmp_path, monkeypatch, capsys, docs, case, held):
    repo = Repo(tmp_path, feature=False, docs=docs == "a-pair").enter(monkeypatch)
    repo.write(CONFIG, held)
    before = repo.snapshot()
    code, out, err = new(capsys, repo)
    assert (code, out) == (1, "")
    assert re.fullmatch(r"taskcontract new: \.sdlc/config\.yaml cannot be read: \S[^\n]*\n",
                        err), err
    assert repo.snapshot() == before, "a refused `new` wrote under the root"
    assert not (repo.root / "specs" / ID).exists()
    # an absent file still means no gate is active
    (repo.root / CONFIG).unlink()
    code, _, err = new(capsys, repo)
    assert (code, err) == (0, "")
    assert (repo.root / "specs" / ID / "contract.yaml").is_file()


@pytest.mark.parametrize("case, held", UNREADABLE, ids=UNREADABLE_IDS)
def test_sc4_1_progress_refuses_a_config_it_cannot_read_and_the_tree_goes_on(
        repo, capsys, case, held):
    repo.write(CONFIG, held)
    before = repo.snapshot()
    for call, opens in [(("start", TASK), U), (("done", TASK), U), (("done", UNIT), U),
                        (("done", ID), ID)]:
        code, out, err = progress(repo, capsys, *call)
        assert (code, out) == (2, ""), call
        assert re.fullmatch(
            re.escape(f"{opens} cannot start: .sdlc/config.yaml cannot be read: ") + r"\S[^\n]*\n",
            err), (call, err)
    assert repo.snapshot() == before
    out, _ = tree_print(repo, capsys)  # the print keeps going
    assert ID in rows_of(out)


@pytest.mark.parametrize("command", ["check", "lint", "model", "review"])
@pytest.mark.parametrize("case, held", UNREADABLE, ids=UNREADABLE_IDS)
def test_sc4_1_g1_check_and_g1_record_refuse_a_config_they_cannot_read(
        repo, capsys, command, case, held):
    repo.install("spectral")
    repo.install("tlc")
    repo.write(CONFIG, held)
    before = repo.snapshot()
    if command == "check":
        code, out, err = check(repo, capsys)
    else:
        code, out, err = {"lint": lint, "model": model, "review": review}[command](capsys)
    assert (code, out) == (2, "")
    assert re.fullmatch(
        re.escape(f"{ID}: .sdlc/config.yaml cannot be read: ") + r"\S[^\n]*\n", err), err
    assert repo.snapshot() == before
    assert repo.calls() == []


# --- G1 is no active gate for a contract born of an escape or maintenance -----------------

ORIGINS = ["g8-escape", "g9-maintenance"]


def scaffold_without_origin(tmp_path: Path) -> dict:
    """The contract `new` writes where G1 is no active gate, less its provenance."""
    other = tmp_path / "reference"
    other.mkdir(exist_ok=True)
    doc = yaml.safe_load(scaffold(ID, root=other).read_text(encoding="utf-8"))
    return {key: value for key, value in doc.items() if key != "provenance"}


@pytest.mark.parametrize("docs", ["a-plain-request", "a-pair"])
@pytest.mark.parametrize("origin", ORIGINS)
def test_sc4_1_new_with_an_origin_g1_does_not_gate_writes_the_contract_with_that_origin(
        tmp_path, monkeypatch, capsys, origin, docs):
    repo = Repo(tmp_path, feature=False, docs=docs == "a-pair").enter(monkeypatch)
    code, out, err = new(capsys, repo, ID, "--origin", origin)
    assert (code, err) == (0, ""), (out, err)
    written = yaml.safe_load((repo.root / "specs" / ID / "contract.yaml")
                             .read_text(encoding="utf-8"))
    assert written["provenance"]["origin"] == origin
    assert {k: v for k, v in written.items() if k != "provenance"} == scaffold_without_origin(
        tmp_path)


def test_sc4_1_new_writes_human_request_when_no_origin_is_given_and_when_it_is(
        tmp_path, monkeypatch, capsys):
    repo = Repo(tmp_path, feature=False, docs=True).enter(monkeypatch)
    repo.write(f"docs/features/{OTHER}.md", document(5, OTHER))
    assert new(capsys, repo)[0] == 0
    assert new(capsys, repo, OTHER, "--origin", "human-request")[0] == 0
    for feature in (ID, OTHER):
        written = yaml.safe_load((repo.root / "specs" / feature / "contract.yaml")
                                 .read_text(encoding="utf-8"))
        assert written["provenance"]["origin"] == "human-request"


def test_sc4_1_new_with_origin_human_request_is_gated_as_with_no_flag(
        tmp_path, monkeypatch, capsys):
    repo = Repo(tmp_path, feature=False, docs=False).enter(monkeypatch)
    before = repo.snapshot()
    assert new(capsys, repo, ID, "--origin", "human-request") == (1, "", message_8(ID) + "\n")
    assert repo.snapshot() == before
    assert new(capsys, repo) == (1, "", message_8(ID) + "\n")


@pytest.mark.parametrize("origin", ORIGINS)
def test_done_means_g1_is_no_active_gate_for_a_contract_born_of_an_escape_or_maintenance(
        tmp_path, monkeypatch, capsys, origin):
    repo = Repo(tmp_path, docs=False, origin=origin).enter(monkeypatch)  # no feature document
    repo.install("spectral")
    repo.install("tlc")
    before = repo.snapshot()
    refusal = f"{ID}: G1 is not active\n"
    assert check(repo, capsys) == (2, "", refusal)
    for command in (lint, model, review):
        assert command(capsys) == (2, "", refusal)
    assert repo.snapshot() == before
    assert repo.calls() == []
    # no call is refused
    assert progress(repo, capsys, "start", TASK) == (0, f"{TASK}: doing\n", "")
    assert progress(repo, capsys, "done", TASK) == (0, f"{TASK}: done\n", "")
    assert progress(repo, capsys, "done", ID) == (0, f"{ID}: done\n", "")
    # its tree prints as an exempt feature's does, byte for byte
    twin = Repo(tmp_path, name="twin", docs=False, origin=origin)
    twin.config(exempt=[ID])
    escaped = repo.root / ".sdlc" / "progress"
    for path in escaped.glob("*") if escaped.exists() else []:
        path.unlink()  # the calls above left records the twin does not hold
    assert tree_print(repo, capsys) == tree_print(twin, capsys)
    # and a contract with a human request, G1 on, prints G1's conditions
    gated = Repo(tmp_path, name="gated", docs=False)
    assert f"{ID}/G1/G1.1" in rows_of(tree_print(gated, capsys)[0])


# --- the tree's second build reads g1.exempt ---------------------------------------------

def test_sc5_2_in_the_trees_second_build_an_exempt_feature_prints_as_today_and_is_never_refused(
        repo, capsys, monkeypatch):
    repo.contract(OTHER)
    repo.config(exempt=[OTHER], schemas=[])
    repo.components()
    first_out, first_err = tree_print(repo, capsys)
    exempt_lines = block(first_out, OTHER)
    assert verdicts(first_out, OTHER)[-1] == f"  {OTHER}/G1 Requirements / Spec [to do] inactive"
    assert f"{ID}/G1/G1.1" in rows_of(first_out)  # the other feature holds G1 active

    def boom(*args, **kwargs):
        raise RuntimeError("no such reading")

    # the build's own G1 step ends on an error: the tree makes its second build
    monkeypatch.setattr(tree, "g1_problems", boom)
    out, err = tree_print(repo, capsys)
    assert block(out, OTHER) == exempt_lines
    assert verdicts(out, OTHER)[-1] == f"  {OTHER}/G1 Requirements / Spec [to do] inactive"
    rows = rows_of(out)
    tag, rest = rows[f"{ID}/G1"]
    assert (tag, "inactive" in rest.split()) == (TO_DO, False)
    assert [rows[f"{ID}/G1/{c}"][0] for c in ("G1.1", "G1.2", "G1.3")] == [TO_DO] * 3
    assert "inactive" in rows[f"{ID}/G2"][1].split()  # the next gate stays inactive
    assert err.splitlines()[-1] == (f"{PROBLEM}unreadable G1 reading: G1 "
                                    "(RuntimeError: no such reading)")
    # the exempt feature is never refused, and the other one is
    assert progress(repo, capsys, "start", OTHER_TASK) == (0, f"{OTHER_TASK}: doing\n", "")
    assert progress(repo, capsys, "start", TASK) == (
        2, "", f"{U} cannot start: G1 has not passed for {ID}\n")


# --- intake's text: the two origins ------------------------------------------------------

def step(text: str, label: str, following: str) -> str:
    start = text.index(f"\n{label}. ")
    return text[start:text.index(following, start + 1)]


def test_sc4_1_i3_passes_origin_for_an_escape_or_maintenance_and_the_prompt_stays_in_its_cap():
    text = INTAKE.read_text(encoding="utf-8")
    i3 = step(text, "I3", "\nI4. ")
    assert "python -m taskcontract new {id}" in i3
    assert "--origin" in i3
    assert "g8-escape" in i3 and "g9-maintenance" in i3
    assert len(text) < 12000  # constraint 10


def test_sc4_1_i9_names_both_origins_and_keeps_the_g1_line_and_its_place():
    text = INTAKE.read_text(encoding="utf-8")
    i9 = step(text, "I9", "</instructions>")
    assert "g8-escape" in i9 and "g9-maintenance" in i9
    assert "Next step: G1. Run /sdlc g1 {id}." in i9
    assert i9.index("one-line scope summary") < i9.index("Next step: G1.")
    assert "python -m taskcontract" not in i9  # constraint 11: no fifth command
    assert "absent from `active_gates`" in i9 and "`g1.exempt`" in i9  # the ways out stay


# --- SC2.1: what the linter is run on ---------------------------------------------------

def test_sc2_1_lint_with_no_g1_schemas_key_refuses_the_call(repo, capsys):
    repo.install("spectral")
    for held in (None, {"exempt": []}):
        if held is None:
            repo.write(CONFIG, yaml.safe_dump({"active_gates": ["G0", "G1"]}))
        else:
            repo.write(CONFIG, yaml.safe_dump({"active_gates": ["G0", "G1"], "g1": held}))
        before = repo.files()
        assert lint(capsys) == (2, "", f"{ID}: no g1.schemas in .sdlc/config.yaml\n")
        assert repo.files() == before
        assert repo.calls() == []
    # `schemas: []` says none
    repo.config(schemas=[])
    assert lint(capsys) == (0, "G1.1: no boundary schema in scope\n", "")


UNMATCHED = [
    ("a-pattern-with-no-file", lambda r: "docs/*.yaml", []),
    ("a-pattern-for-another-folder", lambda r: "schemas/*.json", []),
    ("a-folder-in-another-case", lambda r: "API/*.yaml", []),
    ("a-file-inside-dot-git", lambda r: ".git/*.yaml", [".git/x.yaml"]),
    ("an-absolute-pattern", lambda r: (r.root / "api").as_posix() + "/*.yaml", []),
    ("a-pattern-with-dot-dot", lambda r: "api/../api/*.yaml", []),
    ("a-pattern-that-leaves-the-root", lambda r: "../repo/api/*.yaml", []),
]


@pytest.mark.parametrize("case, make, extra", UNMATCHED, ids=[row[0] for row in UNMATCHED])
def test_sc2_1_a_pattern_that_matches_no_file_makes_the_declaration_unreadable(
        repo, capsys, case, make, extra):
    pattern = make(repo)
    repo.config(schemas=[{**SPECTRAL, "paths": [pattern]}])
    for name in extra:
        repo.write(name, "x: 1\n")
    repo.install("spectral")
    before = repo.files()
    code, out, err = lint(capsys)
    assert (code, out) == (2, "")
    assert err.startswith(f"{ID}: g1.schemas cannot be read: ") and pattern in err, err
    assert len(err.splitlines()) == 1
    assert repo.files() == before
    assert repo.calls() == []  # no tool started
    # G1.1 reads to do, and lists nothing
    code, out, _ = check(repo, capsys)
    assert code == 1 and statuses(out)[0] == TO_DO
    assert "RS1" not in out
    # the tree names the declaration's problem once
    _, tree_err = tree_print(repo, capsys)
    assert any(line.startswith(f"{PROBLEM}unreadable g1.schemas: {CONFIG} (")
               and pattern in line for line in tree_err.splitlines()), tree_err


@pytest.mark.parametrize("pattern", ["./api/*.yaml", "./api/openapi.yaml"])
def test_sc2_1_a_pattern_that_opens_with_dot_slash_lints_its_file_under_the_pin(
        repo, capsys, pattern):
    repo.config(schemas=[{**SPECTRAL, "paths": [pattern]}])
    repo.install("spectral")
    code, out, _ = lint(capsys)
    assert (code, out.splitlines()) == (0, [clean("api/openapi.yaml"), RECORDED])
    (call,) = [c for c in repo.calls() if c["argv"][:1] == ["lint"]]
    assert call["argv"] == ["lint", "api/openapi.yaml", "--ruleset", ".spectral.yaml",
                            "--format", "json", "--quiet", "--fail-severity", "warn"]
    code, out, _ = check(repo, capsys)
    assert statuses(out)[0] == DONE


def test_sc2_1_a_warning_on_a_file_a_dot_slash_pattern_names_fails_g1_1_as_an_error_does(
        repo, capsys):
    repo.config(schemas=[{**SPECTRAL, "paths": ["./api/*.yaml"]}])
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [["schema-has-a-title", WARNING]]})
    code, out, _ = lint(capsys)
    assert (code, out.splitlines()) == (1, [rs102("api/openapi.yaml", 1), RECORDED])
    code, out, _ = check(repo, capsys)
    assert code == 1
    assert f"{ID}: RS102 {rs102('api/openapi.yaml', 1)}" in out.splitlines()
    assert statuses(out)[0] == FAILED


# --- SC2.1 and SC3.1: a tool inside the repository is refused ----------------------------

@pytest.mark.parametrize("tool, command", [("spectral", "lint"), ("tlc", "model"), ("p", "model")])
def test_sc2_1_sc3_1_a_linter_or_a_checker_that_resolves_inside_the_repository_is_refused(
        repo, capsys, monkeypatch, tool, command):
    repo.bin = repo.root / "tools"  # the only folder on PATH stands inside the root
    monkeypatch.setenv("PATH", str(repo.bin))
    if tool == "p":
        repo.components(WALLET, API)
        repo.core(WALLET)
    repo.install(tool)
    repo.plan()
    before = repo.files()
    code, out, err = cli(capsys, "g1-record", command, ID)
    shim = f"{tool}.cmd" if os.name == "nt" else tool
    assert (code, out) == (2, "")
    assert len(err.splitlines()) == 1, err
    # the path is the file's, from the root, with forward slashes
    assert err.replace("\\", "/").lower() == (
        f"{ID}: {tool} resolves inside the repository: tools/{shim}\n").lower()
    assert repo.calls() == []  # the file never started, not even for its version
    assert repo.files() == before


# --- SC3.1: a G1.2 record binds the model's folder ---------------------------------------

def helper(repo: Repo) -> None:
    repo.write("specs/models/helper.tla", "---- MODULE helper ----\n====\n")


TLC_CHANGES = [
    ("a-module-added", lambda r: None,
     lambda r: helper(r)),
    ("a-module-edited", helper,
     lambda r: r.write("specs/models/helper.tla", "---- MODULE helper ----\nX == 1\n====\n")),
    ("a-module-removed", helper,
     lambda r: (r.root / "specs/models/helper.tla").unlink()),
    ("a-module-renamed", helper,
     lambda r: (r.root / "specs/models/helper.tla").rename(r.root / "specs/models/helper2.tla")),
    ("another-configuration-added", lambda r: None,
     lambda r: r.write("specs/models/strict.cfg", "SPECIFICATION Spec\n")),
    ("a-module-in-a-subfolder", lambda r: None,
     lambda r: r.write("specs/models/lib/deep.tla", "---- MODULE deep ----\n====\n")),
]


@pytest.mark.parametrize("case, setup, change", TLC_CHANGES, ids=[row[0] for row in TLC_CHANGES])
def test_sc3_1_a_record_binds_the_models_folder_under_tlc(repo, capsys, case, setup, change):
    setup(repo)
    repo.install("tlc")
    repo.plan(trace=True)  # TLC writes a trace module beside the model on each run
    for _ in range(2):
        code, out, _ = model(capsys)
        assert (code, out.splitlines()) == (0, [passes("ledger"), RECORDED])
    assert statuses(check(repo, capsys)[1])[1] == DONE
    # a file whose extension is no TLC's, and a trace module TLC wrote: no change
    repo.write("specs/models/notes.txt", "x\n")
    repo.write("specs/models/ledger_TTrace_1800000000.tla", "---- MODULE trace ----\n====\n")
    repo.write("specs/models/ledger_TTrace_1800000000.bin", "x")
    assert statuses(check(repo, capsys)[1])[1] == DONE
    # a change among the files TLC reads: the record no longer matches, and G1.2 lists nothing
    change(repo)
    code, out, _ = check(repo, capsys)
    assert statuses(out)[1] == TO_DO
    assert "RS2" not in out
    # a new run binds the folder as it stands
    assert model(capsys)[0] == 0
    assert statuses(check(repo, capsys)[1])[1] == DONE


P_CHANGES = [
    ("a-source-added-under-the-folder",
     lambda r: r.write("specs/p/PSrc/main.p", "machine Main {}\n")),
    ("a-project-added", lambda r: r.write("specs/p/other.pproj", "<Project/>\n")),
]


@pytest.mark.parametrize("case, change", P_CHANGES, ids=[row[0] for row in P_CHANGES])
def test_sc3_1_a_record_binds_the_models_folder_under_p(repo, capsys, case, change):
    repo.components(WALLET)
    repo.core(WALLET)
    repo.install("p")
    code, out, _ = model(capsys)
    assert (code, out.splitlines()) == (0, [passes("wallet", "p"), RECORDED])
    assert statuses(check(repo, capsys)[1])[1] == DONE
    # a file whose extension is no P's, TLC's modules included: no change
    repo.write("specs/p/notes.txt", "x\n")
    repo.write("specs/p/other.tla", "---- MODULE other ----\n====\n")
    assert statuses(check(repo, capsys)[1])[1] == DONE
    change(repo)
    assert statuses(check(repo, capsys)[1])[1] == TO_DO
    assert model(capsys)[0] == 0
    assert statuses(check(repo, capsys)[1])[1] == DONE


def test_sc3_1_a_g1_2_record_of_the_two_file_form_counts_as_absent(repo, capsys):
    old = {"component": "ledger", "tool": "tlc", "installed": True,
           "model": {"path": LEDGER["model"], "sha256": sha(repo.root / LEDGER["model"])},
           "config": {"path": LEDGER["model_config"],
                      "sha256": sha(repo.root / LEDGER["model_config"])},
           "result": "pass"}
    repo.write(RECORD, yaml.safe_dump({"records": [{
        "condition": "G1.2", "at": "2026-10-07T14:02:11Z", "head": "8635064",
        "cores": [old]}]}, sort_keys=False))
    code, out, _ = check(repo, capsys)
    assert code == 1
    assert out.splitlines()[-1].split(", ")[1] == "G1.2 to do"
    assert "RS2" not in out


# --- SC3.1: a P configuration that names no test case ----------------------------------

@pytest.mark.parametrize("words", ["-s 100\n", "-s 100 -v\n"], ids=["a-seed", "two-flags"])
def test_sc3_1_a_p_configuration_that_names_no_test_case_is_refused(repo, capsys, words):
    repo.components(WALLET)
    repo.core(WALLET, config=words)
    repo.install("p")
    before = repo.files()
    code, out, err = model(capsys)
    assert (code, out) == (2, "")
    assert err == f"{ID}: the configuration of wallet names no test case: specs/p/wallet.check\n"
    assert repo.files() == before
    assert [c for c in repo.calls() if c["argv"][:1] == ["check"]] == []  # P never checked
    assert statuses(check(repo, capsys)[1])[1] == TO_DO


# --- SC3.1: a declaration that cannot be read -------------------------------------------

def outside(repo: Repo, name: str) -> str:
    """A file beside the root, in the folder above it: outside the repository."""
    path = repo.tmp / "outside" / name
    path.parent.mkdir(exist_ok=True)
    path.write_text("---- MODULE ledger ----\n====\n", encoding="utf-8")
    return path.as_posix()


BAD_DECLARATIONS = [
    ("two-components-with-one-id",
     lambda r: r.components(LEDGER, {**LEDGER, "paths": ["lib/ledger/"]})),
    ("a-model-above-the-root",
     lambda r: (outside(r, "ledger.tla"),
                r.components({**LEDGER, "model": "../outside/ledger.tla"}, API))),
    ("a-model-at-an-absolute-path",
     lambda r: r.components({**LEDGER, "model": outside(r, "ledger.tla")}, API)),
    ("a-configuration-above-the-root",
     lambda r: (outside(r, "ledger.cfg"),
                r.components({**LEDGER, "model_config": "../outside/ledger.cfg"}, API))),
    ("a-configuration-at-an-absolute-path",
     lambda r: r.components({**LEDGER, "model_config": outside(r, "ledger.cfg")}, API)),
]


@pytest.mark.parametrize("case, make", BAD_DECLARATIONS, ids=[row[0] for row in BAD_DECLARATIONS])
def test_sc3_1_a_component_declaration_with_a_duplicate_id_or_a_path_outside_the_repository_is_unreadable(
        repo, capsys, case, make):
    make(repo)
    repo.install("tlc")
    before = repo.files()
    code, out, err = model(capsys)
    assert (code, out) == (2, "")
    match = re.fullmatch(re.escape(f"{ID}: specs/components.yaml cannot be read: ")
                         + r"(?P<reason>[^\n]*ledger[^\n]*)\n", err)
    assert match, err  # the component is named in the reason
    assert repo.files() == before
    assert repo.calls() == []
    code, out, _ = check(repo, capsys)
    assert code == 1
    assert out.splitlines() == [out.splitlines()[-1]]  # G1.2 lists nothing
    assert statuses(out)[1] == TO_DO
    # the tree names the same reason, once
    _, tree_err = tree_print(repo, capsys)
    assert (f"{PROBLEM}unreadable component declaration: {COMPONENTS} ({match['reason']})"
            in tree_err.splitlines()), tree_err


# --- done_means: G1 reads done only for what a tool or a review checked -------------------

def test_done_means_g1_reads_done_only_for_what_a_tool_or_a_review_checked(repo, capsys):
    repo.install("spectral")
    repo.install("tlc")
    assert lint(capsys)[0] == 0
    assert model(capsys)[0] == 0
    assert review(capsys)[0] == 0
    assert check(repo, capsys) == (0, f"g1-green: {ID}\n", "")
    # a pattern that names no file: the lint record checked nothing of it
    repo.config(schemas=[{**SPECTRAL, "paths": ["schemas/*.json"]}])
    code, out, _ = check(repo, capsys)
    assert (code, statuses(out)[0]) == (1, TO_DO)
    repo.config()
    assert check(repo, capsys) == (0, f"g1-green: {ID}\n", "")
    # a config that cannot be read is no reading of G1 as off
    repo.write(CONFIG, b"active_gates: [G0, G1\n")
    code, out, err = check(repo, capsys)
    assert (code, out) == (2, "")
    assert err.startswith(f"{ID}: .sdlc/config.yaml cannot be read: ")

