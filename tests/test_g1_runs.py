"""G1.1's record holds a `runs` list (contract: g1-requirements-spec, unit
s1-lint, the fix of kit session 101: design revisions r9 to r11).

A temporary repository per test: one contract under specs/, a
.sdlc/config.yaml that turns G1 on and declares the boundary schemas, the
schema files and the pins. No test needs a linter on the machine: a
stand-in stands on a PATH the test sets, as a real child process, and
answers as Spectral 6.17.0 and buf were measured to answer. It leaves a mark
each time it starts, so a test can prove that no tool ran. Each record a
test reads is written by the test, as YAML in the new shape.

What this file pins, beside tests/test_g1_lint.py (which still pins the flat
shape in places and is amended by the session):

- `g1-record lint` lints every `g1.schemas` entry that has a schema in
  scope and appends ONE record: `condition`, `at`, `head`, `runs`, with one
  run for each such entry, in the order of `g1.schemas`: `tool`,
  `tool_version`, `installed`, `pin`, `files` (SC2.1);
- an entry with no schema in scope has no run and no look at its linter
  (SC2.1, SC2.2); a tool that is not installed is recorded for its own run
  alone, the other runs stand, the call exits 1 (SC2.3);
- the refusals come in an order, a linter the kit does not know in any
  entry with a schema in scope is one, and a tool that ends on its own
  error in any run writes nothing though earlier runs finished;
- a contract whose scope cannot be read is a refused call for `lint`, and
  reads G1.1 `to do` for `g1-check` and the tree (done_means);
- `g1-check` and the tree match each schema by run; a record in the older
  shape counts as absent; a record, a run or a value the reader cannot read
  counts as absent for what it holds, and nothing raises (done_means).

Every reading a test takes goes through `reading`, which asks `g1-check
--json` and the tree print, and holds the two to one status and one list of
messages for G1.1.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract.__main__ import main

ID = "apply-discount"
RECORD = f".sdlc/g1/{ID}.yaml"
ABSENT = object()

CONTRACT = """id: {id}
title: A fixture feature
intent: >
  A contract with a scope of its own, enough words to pass the door as a
  fixture for the G1.1 runs suite.
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
BUF = {"paths": ["proto/*.proto"], "linter": "buf", "pin": "buf.yaml"}
SPECTRAL_B = {"paths": ["schemas/*.json"], "linter": "spectral", "pin": ".spectral-b.yaml"}
SPECTRAL_SAME_PIN = {"paths": ["schemas/*.json"], "linter": "spectral", "pin": ".spectral.yaml"}
ESLINT = {"paths": ["schemas/*.json"], "linter": "eslint", "pin": ".eslintrc"}
RUFF = {"paths": ["src/*.py"], "linter": "ruff", "pin": "ruff.toml"}

SCOPE = ("api/", "proto/", "schemas/", "src/")

ERROR, WARNING, INFO, HINT = 0, 1, 2, 3  # Spectral's severities

# The stand-in linter. It runs as `python stand_in.py <tool> <the tool's
# arguments>` behind a file named for the tool, logs each start beside
# itself, and answers from plan.json (the plan's `per_tool` mapping changes
# any key of the plan for one tool). As Spectral it follows the measured
# 6.17.0: `--version` prints the version alone; `lint` with `--format json`
# prints a JSON array of rows; it exits 1 when a row stands at
# `--fail-severity` or above, and 2 with lines on stderr for an error of its
# own. As buf: `--version`; `lint --path <file> --error-format json` prints
# one JSON object a line for each report and exits 100 when there is one,
# and with an error of its own it prints on stderr and exits 1.
STAND_IN = r'''
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = b"@@RAW@@"
NOT_UTF8 = b"\x81\xff"
VALUED = {
    "spectral": {"--ruleset": "--ruleset", "-r": "--ruleset", "--format": "--format",
                 "-f": "--format", "--fail-severity": "--fail-severity",
                 "-F": "--fail-severity", "--encoding": "--encoding", "-e": "--encoding",
                 "--output": "--output", "-o": "--output"},
    "buf": {"--config": "--config", "--path": "--path",
            "--error-format": "--error-format", "--exclude-path": "--exclude-path"},
}
FLAGS = {"-q": "--quiet"}


def split(tool, args):
    valued, options, rest, at = VALUED[tool], {}, [], 0
    while at < len(args):
        arg = args[at]
        name, eq, value = arg.partition("=")
        if arg in valued:
            options.setdefault(valued[arg], []).append(args[at + 1] if at + 1 < len(args) else "")
            at += 2
            continue
        if eq and name in valued:
            options.setdefault(valued[name], []).append(value)
        elif arg.startswith("-"):
            options.setdefault(FLAGS.get(arg, arg), []).append(True)
        else:
            rest.append(arg)
        at += 1
    return options, rest


def rel(path, root):
    return os.path.relpath(os.path.realpath(path), os.path.realpath(root)).replace(os.sep, "/")


def source(path):
    full = os.path.abspath(path).replace("\\", "/")
    return full[0].lower() + full[1:] if full[1:2] == ":" else full


def raw(data, plan):
    return data.replace(RAW, NOT_UTF8 if plan.get("raw") else b"")


def spectral(plan, args, out, err):
    options, files = split("spectral", args)
    if plan.get("own_error"):
        err.write(raw((plan["own_error"] + "\n").encode("utf-8"), plan))
        return 2
    if "--ruleset" not in options:
        err.write(b"No ruleset has been found.\n")
        return 2
    ruleset = options["--ruleset"][-1]
    if not os.path.isfile(ruleset):
        err.write(("Error running Spectral!\nUse --verbose flag to print the error stack.\n"
                   "Error #1: ENOENT: no such file or directory, open '%s'\n"
                   % os.path.abspath(ruleset)).encode("utf-8"))
        return 2
    if not files or not all(os.path.isfile(name) for name in files):
        err.write(b"No files found to lint. Please check your file path and extension "
                  b"and try again\n")
        return 2
    rows = []
    for name in files:
        for code, severity in plan["rows"].get(rel(name, plan["root"]), []):
            rows.append({
                "code": code, "path": [], "message": "The stand-in reports %s.@@RAW@@" % code,
                "severity": severity,
                "range": {"start": {"line": 0, "character": 0},
                          "end": {"line": 1, "character": 18}},
                "source": source(name)})
    if options.get("--format", ["stylish"])[-1] == "json":
        out.write(raw(json.dumps(rows, indent="\t").encode("utf-8"), plan))
    if not rows and "--quiet" not in options:
        out.write(b"No results with a severity of 'error' found!\n")
    if plan.get("exit") is not None:
        return plan["exit"]
    fail = {"error": 0, "warn": 1, "info": 2, "hint": 3}[
        options.get("--fail-severity", ["error"])[-1]]
    return 1 if any(row["severity"] <= fail for row in rows) else 0


def buf(plan, args, out, err):
    options, _ = split("buf", args)
    if plan.get("own_error"):
        err.write((plan["own_error"] + "\n").encode("utf-8"))
        return 1
    if "--path" in options:
        names = [rel(name, plan["root"]) for name in options["--path"]]
    else:
        names = sorted(plan["rows"])
    as_json = options.get("--error-format", ["text"])[-1] == "json"
    lines = []
    for name in names:
        for code, _ in plan["rows"].get(name, []):
            message = "The stand-in reports %s." % code
            if as_json:
                lines.append(json.dumps({
                    "path": name, "start_line": 1, "start_column": 1, "end_line": 1,
                    "end_column": 1, "type": code, "message": message}))
            else:
                lines.append("%s:1:1:%s" % (name, message))
    for line in lines:
        out.write((line + "\n").encode("utf-8"))
    return 100 if lines else 0


def main():
    tool, args = sys.argv[1], sys.argv[2:]
    with open(os.path.join(HERE, "calls.jsonl"), "a", encoding="utf-8") as log:
        log.write(json.dumps({"tool": tool, "argv": args, "cwd": os.getcwd()}) + "\n")
    with open(os.path.join(HERE, "plan.json"), encoding="utf-8") as handle:
        plan = json.load(handle)
    plan = {**plan, **plan.get("per_tool", {}).get(tool, {})}
    out, err = sys.stdout.buffer, sys.stderr.buffer
    if args == ["--version"]:
        out.write((plan["version"] + "\n").encode("utf-8"))
        return 0
    if args[:1] != ["lint"]:
        err.write(b"the stand-in takes --version and lint\n")
        return 2
    return (spectral if tool == "spectral" else buf)(plan, args[1:], out, err)


sys.exit(main())
'''


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Rec(dict):
    """A record as read back: asking it for the `runs` it does not hold is a
    failed assertion about the missing behavior, not a KeyError."""

    def __missing__(self, key):
        assert key != "runs", f"the record holds no `runs` list: {list(self)}"
        raise KeyError(key)


class Repo:
    """One fixture repository at <tmp>/repo, and beside it <tmp>/bin, the
    only folder on PATH: empty until a test installs a stand-in there."""

    def __init__(self, tmp: Path, monkeypatch):
        self.root = tmp / "repo"
        self.bin = tmp / "bin"
        self.root.mkdir()
        self.bin.mkdir()
        self.monkeypatch = monkeypatch
        write_seat_roster(self.root)
        self.contract(ID, *SCOPE)
        self.config()
        self.write(".spectral.yaml", "rules: {}\n")
        self.plan()
        monkeypatch.setenv("PATH", str(self.bin))
        monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp))
        monkeypatch.setenv("COLUMNS", "500")
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
                   CONTRACT.format(id=contract_id, scope=f"scope:\n{entries}"))

    def contract_with(self, scope_text: str | None, contract_id: str = ID) -> None:
        """The contract with its `scope` written as the given text, or left
        out when None."""
        self.write(f"specs/{contract_id}/contract.yaml", CONTRACT.format(
            id=contract_id, scope="" if scope_text is None else scope_text).replace("\n\n", "\n"))

    def config(self, schemas=(SPECTRAL,), active=("G0", "G1"),
               exempt=("controlled-language",)) -> None:
        """.sdlc/config.yaml as a person writes it; ABSENT leaves a key out."""
        g1 = {}
        if exempt is not ABSENT:
            g1["exempt"] = list(exempt)
        if schemas is not ABSENT:
            g1["schemas"] = schemas if not isinstance(schemas, tuple) else list(schemas)
        doc = {"active_gates": list(active)}
        if g1:
            doc["g1"] = g1
        self.write(".sdlc/config.yaml", yaml.safe_dump(doc, sort_keys=False))

    def install(self, tool: str) -> None:
        """Put a stand-in named `tool` on PATH: a .cmd on Windows, as npm
        installs Spectral there, an executable script elsewhere."""
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

    def plan(self, rows=None, version="6.17.0", own_error=None, raw=False, exit_code=None,
             per_tool=None) -> None:
        """What the stand-in answers: `rows` maps a schema's path to a list
        of [code, severity]; a path it does not name lints clean. `per_tool`
        maps a tool's name to the keys of the plan it changes for itself."""
        (self.bin / "plan.json").write_text(json.dumps({
            "root": str(self.root), "rows": rows or {}, "version": version,
            "own_error": own_error, "raw": raw, "exit": exit_code,
            "per_tool": per_tool or {}}), encoding="utf-8")

    def calls(self) -> list[dict]:
        """Each start of a stand-in, in order: the mark it leaves."""
        log = self.bin / "calls.jsonl"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    def lints(self, tool: str | None = None) -> list[dict]:
        return [call for call in self.calls() if call["argv"][:1] == ["lint"]
                and tool in (None, call["tool"])]

    def records(self) -> list[dict]:
        """The records as the file holds them; a record that holds no `runs`
        fails an assertion where a test asks for them."""
        held = yaml.safe_load((self.root / RECORD).read_text(encoding="utf-8"))["records"]
        return [Rec(record) if isinstance(record, dict) else record for record in held]

    def files(self) -> dict[str, bytes]:
        """Every file under the root with its bytes: what a call wrote shows
        as a difference."""
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in sorted(self.root.rglob("*")) if path.is_file()}

    # --- hand-written records -----------------------------------------------------

    def hash(self, rel: str) -> str | None:
        path = self.root / rel
        return sha(path) if path.is_file() else None

    def run(self, tool: str = "spectral", pin: str = ".spectral.yaml",
            files=(("api/a.yaml", 0),), installed: bool = True, version: str = "6.17.0") -> dict:
        """One run as `lint` writes it, hashed from the disk as it stands."""
        return {"tool": tool, "tool_version": version if installed else None,
                "installed": installed,
                "pin": {"path": pin, "sha256": self.hash(pin)},
                "files": [{"path": path, "sha256": self.hash(path),
                           "reported": count if installed else None}
                          for path, count in files]}

    def record(self, *runs, **keys) -> dict:
        record = {"condition": "G1.1", "at": "2026-10-17T10:00:00Z", "head": "3c41d2a",
                  "runs": list(runs)}
        record.update(keys)
        return record

    def records_file(self, *records) -> None:
        self.write(RECORD, yaml.safe_dump({"records": list(records)}, sort_keys=False))

    def two(self, a: int = 0, b: int = 0, x: int = 0) -> tuple[dict, dict]:
        """The two-entry fixture: Spectral on api/a.yaml and api/b.yaml, buf
        on proto/x.proto, each file with the count given. The files are
        written; the two runs are returned, and no record is."""
        self.config(schemas=[SPECTRAL, BUF])
        self.write("api/a.yaml", "a: 1\n")
        self.write("api/b.yaml", "b: 1\n")
        self.write("proto/x.proto", 'syntax = "proto3";\n')
        self.write("buf.yaml", "version: v2\n")
        return (self.run("spectral", ".spectral.yaml", [("api/a.yaml", a), ("api/b.yaml", b)]),
                self.run("buf", "buf.yaml", [("proto/x.proto", x)], version="1.47.2"))


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


def lint(capsys):
    """`g1-record lint <id>`, run at the repository's root."""
    return cli(capsys, "g1-record", "lint", ID)


def check(repo: Repo, capsys, *extra: str):
    return cli(capsys, "g1-check", ID, "--root", repo.root, *extra)


def tree_g1_1(repo: Repo, capsys) -> tuple[str, list[str]]:
    """The tree print's G1.1 line for the feature: its status and the
    diagnostics printed under it. The print must complete, and no G1 reader
    may have raised."""
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0, err
    assert "unreadable G1 reading" not in err, err
    lines = out.splitlines()
    head = f"{ID}/G1/G1.1 "
    at = next((n for n, line in enumerate(lines) if line.strip().startswith(head)), None)
    assert at is not None, f"the tree prints no G1.1 line for {ID}:\n{out}"
    tag = re.search(r"\[([^\]]*)\]", lines[at])
    assert tag, lines[at]
    indent = len(lines[at]) - len(lines[at].lstrip())
    found = []
    for line in lines[at + 1:]:
        if len(line) - len(line.lstrip()) > indent and line.strip().startswith("- "):
            found.append(line.strip()[2:])
        else:
            break
    return tag.group(1), found


def reading(repo: Repo, capsys) -> tuple[str, list[str]]:
    """G1.1's status and its messages as `g1-check --json` gives them; the
    tree print gives the same, or the test fails here. No command may
    raise."""
    code, out, err = check(repo, capsys, "--json")
    assert code in (0, 1), (code, err)
    answer = json.loads(out)
    status = dict(part.split(" ", 1) for part in answer["note"].split(", "))["G1.1"]
    messages = [f["message"] for f in answer["findings"] if f["condition"] == "G1.1"]
    assert tree_g1_1(repo, capsys) == (status, messages), "the tree and g1-check differ"
    if status != "failed":
        assert messages == []  # a to do and a done list nothing
    return status, messages


def quick(repo: Repo, capsys) -> tuple[str, list[str]]:
    """G1.1's status and messages by `g1-check --json` alone."""
    code, out, err = check(repo, capsys, "--json")
    assert code in (0, 1), (code, err)
    answer = json.loads(out)
    status = dict(part.split(" ", 1) for part in answer["note"].split(", "))["G1.1"]
    return status, [f["message"] for f in answer["findings"] if f["condition"] == "G1.1"]


def runs_of(record: dict) -> list:
    """The record's `runs` list; the test fails here when the record holds none."""
    assert "runs" in record, f"the record holds no `runs` list: {list(record)}"
    return record["runs"]


def clean(path: str, tool: str = "spectral") -> str:
    return f"G1.1: {path} lints clean under {tool}"


def rs101(tool: str = "spectral") -> str:
    return f"G1.1: {tool} is not installed; install it and pin it in the repository"


def rs102(path: str, n: int, tool: str = "spectral") -> str:
    return f"G1.1: {path} does not lint clean: {tool} reports {n}"


RECORDED = f"recorded: {RECORD}"
NO_SCHEMA = "G1.1: no boundary schema in scope"
RUN_KEYS = ["tool", "tool_version", "installed", "pin", "files"]
SPECTRAL_ARGV = ["lint", "{file}", "--ruleset", "{pin}", "--format", "json", "--quiet",
                 "--fail-severity", "warn"]


def spectral_argv(file: str, pin: str = ".spectral.yaml") -> list[str]:
    return [word.format(file=file, pin=pin) for word in SPECTRAL_ARGV]


def buf_argv(file: str, pin: str = "buf.yaml") -> list[str]:
    return ["lint", "--config", pin, "--path", file, "--error-format", "json"]


def baseline_done(repo: Repo, capsys) -> None:
    """Run `lint` on the repository as it stands and see G1.1 read done
    from a record in the new shape."""
    code, _, err = lint(capsys)
    assert code == 0, err
    runs_of(repo.records()[-1])
    assert reading(repo, capsys) == ("done", [])


# --- SC2.1: the record holds one run for each entry with a schema in scope ------------

def test_sc2_1_one_entry_gives_one_record_of_four_keys_holding_one_run(repo, capsys):
    schema = repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(version="6.99.1")
    code, out, err = lint(capsys)
    assert out.splitlines() == [clean("api/openapi.yaml"), RECORDED]
    assert (code, err) == (0, "")
    text = (repo.root / RECORD).read_text(encoding="utf-8")
    assert list(yaml.safe_load(text)) == ["records"]
    (record,) = repo.records()
    assert list(record) == ["condition", "at", "head", "runs"]
    assert record["condition"] == "G1.1"
    assert re.search(r"\bat: ['\"]?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z['\"]?\s", text)
    assert record["head"] == "no commit"  # no git on this PATH, as progress records it
    (run,) = record["runs"]
    assert list(run) == RUN_KEYS
    assert run["tool"] == "spectral"
    assert run["tool_version"] == "6.99.1"  # read from the tool's own --version
    assert run["installed"] is True
    assert list(run["pin"]) == ["path", "sha256"]
    assert run["pin"] == {"path": ".spectral.yaml", "sha256": sha(repo.root / ".spectral.yaml")}
    assert len(run["pin"]["sha256"]) == 64
    assert run["files"] == [{"path": "api/openapi.yaml", "sha256": sha(schema), "reported": 0}]
    assert list(run["files"][0]) == ["path", "sha256", "reported"]
    # A committed file: the folder holds the record and nothing beside it.
    assert [p.name for p in (repo.root / ".sdlc" / "g1").iterdir()] == [f"{ID}.yaml"]
    assert reading(repo, capsys) == ("done", [])


def test_sc2_1_two_entries_give_two_runs_each_under_its_own_tool_and_pin(repo, capsys):
    a, b = repo.write("api/a.yaml", "a: 1\n"), repo.write("proto/x.proto", 'syntax = "proto3";\n')
    pin_b = repo.write("buf.yaml", "version: v2\n")
    repo.config(schemas=[SPECTRAL, BUF])
    repo.install("spectral")
    repo.install("buf")
    repo.plan(per_tool={"spectral": {"version": "6.17.0"}, "buf": {"version": "1.47.2"}})
    code, out, err = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), clean("proto/x.proto", "buf"), RECORDED]
    assert (code, err) == (0, "")
    (record,) = repo.records()  # one call, one record
    assert list(record) == ["condition", "at", "head", "runs"]
    first, second = record["runs"]
    assert list(first) == RUN_KEYS and list(second) == RUN_KEYS
    assert (first["tool"], first["tool_version"], first["installed"]) == ("spectral", "6.17.0", True)
    assert first["pin"] == {"path": ".spectral.yaml", "sha256": sha(repo.root / ".spectral.yaml")}
    assert first["files"] == [{"path": "api/a.yaml", "sha256": sha(a), "reported": 0}]
    assert (second["tool"], second["tool_version"], second["installed"]) == ("buf", "1.47.2", True)
    assert second["pin"] == {"path": "buf.yaml", "sha256": sha(pin_b)}
    assert second["files"] == [{"path": "proto/x.proto", "sha256": sha(b), "reported": 0}]
    assert [call["argv"] for call in repo.lints("spectral")] == [spectral_argv("api/a.yaml")]
    assert [call["argv"] for call in repo.lints("buf")] == [buf_argv("proto/x.proto")]
    assert reading(repo, capsys) == ("done", [])


def test_sc2_1_the_runs_follow_the_order_of_g1_schemas_and_the_lines_follow_the_runs(
        repo, capsys):
    """buf stands first in the config, so its run and its line come first
    though its file's path sorts after Spectral's."""
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("proto/x.proto", 'syntax = "proto3";\n')
    repo.write("buf.yaml", "version: v2\n")
    repo.config(schemas=[BUF, SPECTRAL])
    repo.install("spectral")
    repo.install("buf")
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("proto/x.proto", "buf"), clean("api/a.yaml"), RECORDED]
    assert code == 0
    (record,) = repo.records()
    assert [run["tool"] for run in record["runs"]] == ["buf", "spectral"]
    assert [call["tool"] for call in repo.lints()] == ["buf", "spectral"]


def test_sc2_1_an_entry_with_no_schema_in_scope_between_two_that_have_one_has_no_run(
        repo, capsys):
    """proto/ is outside the contract's scope, so buf's entry has no schema
    in scope: no run, no line, no start, and no look at its linter."""
    repo.contract(ID, "api/", "schemas/")
    repo.config(schemas=[SPECTRAL, BUF, SPECTRAL_B])
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("proto/x.proto", 'syntax = "proto3";\n')  # a pattern match outside the scope
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.write(".spectral-b.yaml", "rules: {}\n")
    repo.install("spectral")  # and buf is not installed
    code, out, err = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), clean("schemas/s.json"), RECORDED]
    assert (code, err) == (0, "")
    (record,) = repo.records()
    assert [(run["tool"], run["pin"]["path"], [f["path"] for f in run["files"]])
            for run in record["runs"]] == [
        ("spectral", ".spectral.yaml", ["api/a.yaml"]),
        ("spectral", ".spectral-b.yaml", ["schemas/s.json"])]
    assert {call["tool"] for call in repo.calls()} == {"spectral"}
    assert reading(repo, capsys) == ("done", [])


@pytest.mark.parametrize("middle", [BUF, ESLINT], ids=[
    "a linter the kit knows", "a linter the kit does not know"])
def test_sc2_1_an_entry_with_no_schema_in_scope_is_never_looked_at_for_its_linter(
        repo, capsys, middle):
    repo.contract(ID, "api/")
    repo.config(schemas=[middle, SPECTRAL])  # the first entry's files are out of scope
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.write("proto/x.proto", 'syntax = "proto3";\n')
    repo.install("spectral")
    code, out, err = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), RECORDED]
    assert (code, err) == (0, "")
    (record,) = repo.records()
    assert [run["tool"] for run in record["runs"]] == ["spectral"]


def test_sc2_1_two_entries_with_one_linter_and_one_pin_still_give_two_runs(repo, capsys):
    repo.config(schemas=[SPECTRAL, SPECTRAL_SAME_PIN])
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.install("spectral")
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), clean("schemas/s.json"), RECORDED]
    assert code == 0
    (record,) = repo.records()
    assert len(record["runs"]) == 2
    assert [(run["tool"], run["pin"]["path"], [f["path"] for f in run["files"]])
            for run in record["runs"]] == [
        ("spectral", ".spectral.yaml", ["api/a.yaml"]),
        ("spectral", ".spectral.yaml", ["schemas/s.json"])]
    assert reading(repo, capsys) == ("done", [])


def test_sc2_1_a_file_that_two_entries_match_belongs_to_the_first_and_only_its_run_lists_it(
        repo, capsys):
    both = {"paths": ["api/*.yaml", "schemas/*.json"], "linter": "spectral",
            "pin": ".spectral-b.yaml"}
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.write(".spectral-b.yaml", "rules: {}\n")
    repo.install("spectral")
    repo.config(schemas=[SPECTRAL, both])
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), clean("schemas/s.json"), RECORDED]
    assert code == 0
    assert [(run["pin"]["path"], [f["path"] for f in run["files"]])
            for run in repo.records()[-1]["runs"]] == [
        (".spectral.yaml", ["api/a.yaml"]), (".spectral-b.yaml", ["schemas/s.json"])]
    assert [call["argv"] for call in repo.lints()] == [
        spectral_argv("api/a.yaml"), spectral_argv("schemas/s.json", ".spectral-b.yaml")]
    # The same two entries the other way round: the entry that now stands
    # first takes both files, and the other has no schema left, so no run.
    repo.config(schemas=[both, SPECTRAL])
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), clean("schemas/s.json"), RECORDED]
    assert code == 0
    assert [(run["pin"]["path"], [f["path"] for f in run["files"]])
            for run in repo.records()[-1]["runs"]] == [
        (".spectral-b.yaml", ["api/a.yaml", "schemas/s.json"])]
    assert reading(repo, capsys) == ("done", [])


def test_sc2_1_a_run_lists_its_files_by_path_and_each_run_is_one_group_of_lines(repo, capsys):
    for name in ("c", "a", "b"):
        repo.write(f"api/{name}.yaml", f"{name}: 1\n")
    repo.write("proto/x.proto", 'syntax = "proto3";\n')
    repo.write("buf.yaml", "version: v2\n")
    repo.config(schemas=[SPECTRAL, BUF])
    repo.install("spectral")
    repo.install("buf")
    repo.plan(rows={"api/b.yaml": [["r1", ERROR], ["r2", WARNING]], "api/c.yaml": [["r2", WARNING]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), rs102("api/b.yaml", 2),
                                rs102("api/c.yaml", 1), clean("proto/x.proto", "buf"), RECORDED]
    assert code == 1
    (record,) = repo.records()
    spectral_run, buf_run = record["runs"]
    assert [(f["path"], f["reported"]) for f in spectral_run["files"]] == [
        ("api/a.yaml", 0), ("api/b.yaml", 2), ("api/c.yaml", 1)]
    assert [(f["path"], f["reported"]) for f in buf_run["files"]] == [("proto/x.proto", 0)]
    status, messages = reading(repo, capsys)
    assert status == "failed"
    assert messages == [rs102("api/b.yaml", 2), rs102("api/c.yaml", 1)]


def test_sc2_1_a_warning_alone_in_one_run_fails_g1_1_as_an_error_does(repo, capsys):
    repo.two()
    repo.install("spectral")
    repo.install("buf")
    repo.plan(rows={"proto/x.proto": [["PACKAGE_DEFINED", WARNING]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), clean("api/b.yaml"),
                                rs102("proto/x.proto", 1, "buf"), RECORDED]
    assert code == 1
    assert repo.records()[-1]["runs"][1]["files"][0]["reported"] == 1
    assert reading(repo, capsys) == ("failed", [rs102("proto/x.proto", 1, "buf")])
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS102 {rs102('proto/x.proto', 1, 'buf')}",
                                f"{ID}: G1.1 failed, G1.2 to do, G1.3 to do"]
    assert code == 1


def test_sc2_1_the_record_is_appended_after_the_records_already_there(repo, capsys):
    repo.write("api/a.yaml", "a: 1\n")
    repo.install("spectral")
    review = {"condition": "G1.3", "at": "2026-10-07T14:20:40Z", "head": "8635064",
              "by": "Ann Lee", "seat": "user", "requirements": "r5", "items": []}
    repo.records_file(review)
    assert lint(capsys)[0] == 0
    records = repo.records()
    assert records[0] == review
    assert [r["condition"] for r in records] == ["G1.3", "G1.1"]
    assert list(records[1]) == ["condition", "at", "head", "runs"]


def test_sc2_1_each_call_appends_one_record_and_the_last_one_counts(repo, capsys):
    repo.two()
    repo.install("spectral")
    repo.install("buf")
    assert lint(capsys)[0] == 0
    repo.plan(rows={"api/b.yaml": [["schema-has-a-title", WARNING]]})
    assert lint(capsys)[0] == 1
    assert reading(repo, capsys) == ("failed", [rs102("api/b.yaml", 1)])
    repo.plan()
    assert lint(capsys)[0] == 0
    assert [r["condition"] for r in repo.records()] == ["G1.1"] * 3
    assert [[f["reported"] for run in r["runs"] for f in run["files"]]
            for r in repo.records()] == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert reading(repo, capsys) == ("done", [])


@pytest.mark.parametrize("where", ["the second run", "the first run", "after a missing tool"])
def test_sc2_1_a_tool_that_ends_on_its_own_error_in_any_run_gives_exit_2_and_writes_nothing(
        repo, capsys, where):
    repo.two()
    repo.install("spectral")
    spectral_text = "Error running Spectral!\nError #1: the ruleset holds no rule"
    if where == "the second run":
        repo.install("buf")
        repo.plan(per_tool={"buf": {"own_error": "buf: the configuration is invalid"}})
        wanted = ["buf: the configuration is invalid"]
    elif where == "the first run":
        repo.install("buf")
        repo.plan(per_tool={"spectral": {"own_error": spectral_text}})
        wanted = spectral_text.splitlines()
    else:
        repo.config(schemas=[BUF, SPECTRAL])  # buf is not installed; Spectral errors second
        repo.plan(per_tool={"spectral": {"own_error": spectral_text}})
        wanted = spectral_text.splitlines()
    before = repo.files()
    code, out, err = lint(capsys)
    assert code == 2
    assert out == ""  # nothing is printed before every run has finished
    for line in wanted:
        assert line in err.splitlines()
    assert repo.files() == before
    assert not (repo.root / ".sdlc" / "g1").exists()
    if where == "the second run":
        assert [call["tool"] for call in repo.lints()] == ["spectral", "spectral", "buf"]


def test_sc2_1_a_tool_error_leaves_the_last_record_standing(repo, capsys):
    repo.two()
    repo.install("spectral")
    repo.install("buf")
    baseline_done(repo, capsys)
    before = repo.files()
    repo.plan(per_tool={"buf": {"own_error": "buf: the configuration is invalid"}})
    code, out, err = lint(capsys)
    assert (code, out) == (2, "")
    assert "buf: the configuration is invalid" in err.splitlines()
    assert repo.files() == before
    assert reading(repo, capsys) == ("done", [])


def test_sc2_1_a_buf_run_and_a_spectral_run_report_their_own_counts(repo, capsys):
    repo.two()
    repo.install("spectral")
    repo.install("buf")
    repo.plan(rows={"api/a.yaml": [["r1", ERROR]],
                    "proto/x.proto": [["PACKAGE_DEFINED", ERROR], ["ENUM_ZERO_VALUE_SUFFIX", ERROR]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [rs102("api/a.yaml", 1), clean("api/b.yaml"),
                                rs102("proto/x.proto", 2, "buf"), RECORDED]
    assert code == 1
    assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 1),
                                                rs102("proto/x.proto", 2, "buf")])


# --- refusals: unknown linters, and the order the checks come in -----------------------

@pytest.mark.parametrize("entries, unknown", [
    ([SPECTRAL, ESLINT], "eslint"),
    ([ESLINT, SPECTRAL], "eslint"),
    ([SPECTRAL, ESLINT, RUFF], "eslint"),
], ids=["unknown linter in the second entry", "unknown linter in the first entry",
        "two unknown linters: the first entry's is named"])
def test_sc2_1_a_linter_the_kit_does_not_know_in_any_entry_with_a_schema_in_scope_refuses(
        repo, capsys, entries, unknown):
    repo.config(schemas=entries)
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.write("src/m.py", "X = 1\n")
    repo.install("spectral")
    before = repo.files()
    code, out, err = lint(capsys)
    assert code == 2
    assert err.splitlines() == [
        f"{ID}: g1.schemas names a linter the kit does not know: {unknown}"]
    assert out == ""
    assert repo.calls() == []  # no tool started, not even for its version
    assert repo.files() == before


def test_sc2_1_the_refusals_come_in_order_when_every_fault_stands_at_once(repo, capsys):
    """contract, gate, scope, declaration, linter name, record file, then
    the tools. Each step mends the fault that was named and leaves the rest."""
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.install("spectral")
    repo.plan(own_error="Error running Spectral!\nError #1: the ruleset holds no rule")
    unreadable_record = "records: [not closed\n"
    no_pin = {"paths": ["schemas/*.json"], "linter": "spectral"}

    def refused(first_line: str, expected_id: str = ID, *, prefix: bool = False):
        before = repo.files()
        code, out, err = cli(capsys, "g1-record", "lint", expected_id)
        assert code == 2
        assert out == ""
        assert len(err.splitlines()) == 1, err
        assert (err.startswith(first_line) if prefix else err.strip() == first_line), err
        assert repo.calls() == []
        assert repo.files() == before

    # the contract comes first: an id with no contract, whatever else stands
    repo.config(schemas=[ESLINT, no_pin], exempt=("ghost",))
    repo.write(RECORD, unreadable_record)
    refused("ghost: no contract at specs/ghost/contract.yaml", "ghost")
    # then the gate: G1 is off for the feature, and its scope and declaration are bad
    repo.contract_with(None)
    repo.config(schemas=[ESLINT, no_pin], exempt=(ID,))
    refused(f"{ID}: G1 is not active")
    # then the scope, before the declaration is read
    repo.config(schemas=[ESLINT, no_pin])
    refused(f"{ID}: the contract's scope cannot be read at specs/{ID}/contract.yaml")
    # then the declaration, before any linter's name
    repo.contract(ID, *SCOPE)
    refused(f"{ID}: g1.schemas cannot be read: ", prefix=True)
    # then the linter's name, before the record file
    repo.config(schemas=[ESLINT])
    refused(f"{ID}: g1.schemas names a linter the kit does not know: eslint")
    # then the record file, before any tool
    repo.config(schemas=[SPECTRAL])
    refused(f"taskcontract g1-record: unreadable record: {RECORD} (", prefix=True)
    # then the tools: the record file mended, Spectral ends on its own error
    (repo.root / RECORD).unlink()
    code, out, err = lint(capsys)
    assert code == 2
    assert out == ""
    assert "Error #1: the ruleset holds no rule" in err.splitlines()
    assert len(repo.lints()) == 1
    assert not (repo.root / RECORD).exists()


# --- SC2.2: no boundary schema in scope passes G1.1, and no linter runs ----------------

def test_sc2_2_no_schema_in_scope_for_any_entry_says_so_and_a_scope_that_cannot_be_read_does_not(
        repo, capsys):
    """Entries with no schema in scope (their files stand outside the
    scope) run no tool and write nothing; G1.1 reads done. The same
    contract with a scope that cannot be read does not read done."""
    repo.contract(ID, "src/")
    repo.config(schemas=[SPECTRAL, ESLINT])
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.install("spectral")  # a linter stands ready, and leaves a mark if it starts
    before = repo.files()
    code, out, err = lint(capsys)
    assert out.splitlines() == [NO_SCHEMA]
    assert (code, err) == (0, "")
    assert repo.calls() == []
    assert repo.files() == before
    assert not (repo.root / ".sdlc" / "g1").exists()
    assert reading(repo, capsys) == ("done", [])
    repo.contract_with(None)  # the scope is gone: nothing reads done now
    assert reading(repo, capsys) == ("to do", [])
    code, out, err = lint(capsys)
    assert (code, out) == (2, "")
    assert err.splitlines() == [f"{ID}: the contract's scope cannot be read at "
                                f"specs/{ID}/contract.yaml"]


def test_sc2_2_an_entry_whose_files_the_first_entry_took_gives_no_run_and_no_look_at_its_linter(
        repo, capsys):
    """The unknown linter's only match is a file the first entry owns, so
    that entry has no schema in scope: the call is not refused."""
    greedy = {"paths": ["api/*.yaml"], "linter": "eslint", "pin": ".eslintrc"}
    repo.config(schemas=[SPECTRAL, greedy])
    repo.write("api/a.yaml", "a: 1\n")
    repo.install("spectral")
    code, out, err = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), RECORDED]
    assert (code, err) == (0, "")
    assert [run["tool"] for run in repo.records()[-1]["runs"]] == ["spectral"]


# --- SC2.3: a tool that is not installed fails G1.1 with its message --------------------

def test_sc2_3_a_tool_not_installed_in_one_run_is_recorded_for_that_run_and_the_other_stands(
        repo, capsys):
    a = repo.write("api/a.yaml", "a: 1\n")
    x = repo.write("proto/x.proto", 'syntax = "proto3";\n')
    pin_b = repo.write("buf.yaml", "version: v2\n")
    repo.config(schemas=[SPECTRAL, BUF])
    repo.install("spectral")  # PATH holds no buf
    code, out, err = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), rs101("buf"), RECORDED]
    assert (code, err) == (1, "")
    (record,) = repo.records()
    assert list(record) == ["condition", "at", "head", "runs"]
    first, second = record["runs"]
    assert (first["tool"], first["installed"], first["tool_version"]) == ("spectral", True, "6.17.0")
    assert first["files"] == [{"path": "api/a.yaml", "sha256": sha(a), "reported": 0}]
    assert list(second) == RUN_KEYS
    assert second["tool"] == "buf"
    assert second["installed"] is False
    assert second["tool_version"] is None
    assert second["pin"] == {"path": "buf.yaml", "sha256": sha(pin_b)}
    assert second["files"] == [{"path": "proto/x.proto", "sha256": sha(x), "reported": None}]
    assert {call["tool"] for call in repo.calls()} == {"spectral"}
    status, messages = reading(repo, capsys)
    assert (status, messages) == ("failed", [rs101("buf")])
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS101 {rs101('buf')}",
                                f"{ID}: G1.1 failed, G1.2 to do, G1.3 to do"]
    assert code == 1


@pytest.mark.parametrize("entries, installed, wanted_lines, wanted_findings", [
    ([SPECTRAL, BUF], ["spectral"],
     [clean("api/a.yaml"), rs101("buf")], [rs101("buf")]),
    ([BUF, SPECTRAL], ["spectral"],
     [rs101("buf"), clean("api/a.yaml")], [rs101("buf")]),
    ([SPECTRAL, BUF], [], [rs101(), rs101("buf")], [rs101(), rs101("buf")]),
    ([SPECTRAL, BUF, SPECTRAL_B], ["buf"],
     [rs101(), clean("proto/x.proto", "buf")], [rs101()]),
], ids=["clean run then a missing tool", "a missing tool then a clean run",
        "two tools missing: one line for each tool name",
        "one tool missing in two runs: the line at the first run that names it"])
def test_sc2_3_the_not_installed_line_prints_once_for_each_tool_name_at_the_first_run(
        repo, capsys, entries, installed, wanted_lines, wanted_findings):
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("proto/x.proto", 'syntax = "proto3";\n')
    repo.write("buf.yaml", "version: v2\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.write(".spectral-b.yaml", "rules: {}\n")
    repo.config(schemas=entries)
    for tool in installed:
        repo.install(tool)
    code, out, err = lint(capsys)
    assert out.splitlines() == [*wanted_lines, RECORDED]
    assert (code, err) == (1, "")
    record = repo.records()[-1]
    assert [run["tool"] for run in record["runs"]] == [e["linter"] for e in entries]
    assert [run["installed"] for run in record["runs"]] == [
        e["linter"] in installed for e in entries]
    for run in record["runs"]:
        if not run["installed"]:
            assert run["tool_version"] is None
            assert all(f["reported"] is None for f in run["files"])
    assert reading(repo, capsys) == ("failed", wanted_findings)  # RS101 once for a tool name


def test_sc2_3_a_missing_tool_is_not_started_and_a_later_install_replaces_the_reading(
        repo, capsys):
    repo.two()
    repo.install("spectral")
    assert lint(capsys)[0] == 1
    assert {call["tool"] for call in repo.calls()} == {"spectral"}
    assert reading(repo, capsys) == ("failed", [rs101("buf")])
    repo.install("buf")  # installed now, and not yet run: the record wins until the next run
    assert reading(repo, capsys) == ("failed", [rs101("buf")])
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), clean("api/b.yaml"),
                                clean("proto/x.proto", "buf"), RECORDED]
    assert code == 0
    assert [[run["installed"] for run in r["runs"]] for r in repo.records()] == [
        [True, False], [True, True]]
    assert reading(repo, capsys) == ("done", [])


def test_sc2_3_a_tool_not_installed_and_not_pinned_still_fails_g1_1_never_to_do(repo, capsys):
    """Advisory of round 1: a linter that is not installed reads failed."""
    schema = repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    (repo.root / ".spectral.yaml").unlink()
    code, out, _ = lint(capsys)  # PATH holds no spectral
    assert out.splitlines() == [rs101(), RECORDED]
    assert code == 1
    (run,) = repo.records()[-1]["runs"]
    assert run["installed"] is False
    assert run["pin"] == {"path": ".spectral.yaml", "sha256": None}
    assert run["files"] == [{"path": "api/openapi.yaml", "sha256": sha(schema), "reported": None}]
    assert reading(repo, capsys) == ("failed", [rs101()])
    repo.write(".spectral.yaml", "rules: {}\n")  # the pin written after the run
    assert reading(repo, capsys) == ("to do", [])


def test_sc2_3_a_missing_tool_and_a_report_in_another_run_both_show(repo, capsys):
    repo.two()
    repo.install("spectral")
    repo.plan(rows={"api/a.yaml": [["r1", ERROR]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [rs102("api/a.yaml", 1), clean("api/b.yaml"),
                                rs101("buf"), RECORDED]
    assert code == 1
    assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 1), rs101("buf")])


# --- done_means: the reader matches by run ---------------------------------------------

def test_done_means_a_record_written_for_one_order_reads_done_after_the_config_lists_the_other(
        repo, capsys):
    repo.two()
    repo.install("spectral")
    repo.install("buf")
    baseline_done(repo, capsys)
    repo.config(schemas=[BUF, SPECTRAL])
    assert reading(repo, capsys) == ("done", [])
    repo.records_file(repo.record(*reversed(repo.records()[-1]["runs"])))  # the runs, reversed
    assert reading(repo, capsys) == ("done", [])


def _stale_a(repo):
    repo.write("api/a.yaml", "a: 2\n")


def _stale_x(repo):
    repo.write("proto/x.proto", 'syntax = "proto2";\n')


@pytest.mark.parametrize("state, findings", [
    ("stale-a", []),
    ("failed-x-stale-a", ["x"]),
    ("stale-x-failed-a", ["a"]),
    ("failed-a", ["a"]),
    ("clean", None),
    ("failed-both", ["a", "x"]),
], ids=["one run stale, one clean: to do",
        "one run failed, one stale: the failed one's findings",
        "one run stale, one failed: the failed one's findings",
        "one run failed, one clean: failed",
        "two runs clean: done",
        "two runs failed: both runs' findings"])
def test_done_means_one_run_stale_or_failed_beside_another_reads_by_the_rule(
        repo, capsys, state, findings):
    a_count = 2 if state in ("failed-a", "failed-both", "stale-x-failed-a") else 0
    x_count = 3 if state in ("failed-x-stale-a", "failed-both") else 0
    S, B = repo.two(a=a_count, b=0, x=x_count)
    repo.records_file(repo.record(S, B))
    # before a file changes, the record reads as its counts say
    assert quick(repo, capsys)[0] == ("failed" if a_count or x_count else "done")
    if state in ("stale-a", "failed-x-stale-a"):
        _stale_a(repo)
    if state == "stale-x-failed-a":
        _stale_x(repo)
    messages = {"a": rs102("api/a.yaml", 2), "x": rs102("proto/x.proto", 3, "buf")}
    if findings is None:
        assert reading(repo, capsys) == ("done", [])
    elif findings == []:
        assert reading(repo, capsys) == ("to do", [])
    else:
        assert reading(repo, capsys) == ("failed", [messages[k] for k in findings])


def test_done_means_the_reader_needs_the_good_result_in_some_run_and_does_not_mind_the_order(
        repo, capsys):
    S, B = repo.two()
    repo.records_file(repo.record(B, S))
    assert reading(repo, capsys) == ("done", [])
    repo.records_file(repo.record(S))  # buf's schema has no run
    assert reading(repo, capsys) == ("to do", [])
    repo.records_file(repo.record(B))  # Spectral's schemas have none
    assert reading(repo, capsys) == ("to do", [])


def _swap_tool(repo, run):
    run["tool"] = "buf" if run["tool"] == "spectral" else "spectral"


def _pin_path(repo, run):
    run["pin"]["path"] = ".other-pin.yaml"


def _file_hash(repo, run):
    run["files"][0]["sha256"] = "0" * 64


def _pin_hash(repo, run):
    run["pin"]["sha256"] = "0" * 64


FILES = ("api/a.yaml", "proto/x.proto")
PINS = (".spectral.yaml", "buf.yaml")


@pytest.mark.parametrize("index", [0, 1], ids=["the first run", "the second run"])
@pytest.mark.parametrize("cell", [
    "schema file changed on disk", "pin file changed on disk",
    "recorded schema hash", "recorded pin hash", "recorded tool", "recorded pin path",
    "entry's linter in the config", "entry's pin in the config",
])
def test_done_means_each_cell_of_the_matching_rule_changes_the_reading_when_it_changes(
        repo, capsys, cell, index):
    repo.two()
    repo.install("spectral")
    repo.install("buf")
    baseline_done(repo, capsys)
    if cell == "schema file changed on disk":
        repo.write(FILES[index], "changed: true\n")
    elif cell == "pin file changed on disk":
        repo.write(PINS[index], "rules: {changed: true}\n")
    elif cell.startswith("recorded"):
        doc = yaml.safe_load((repo.root / RECORD).read_text(encoding="utf-8"))
        change = {"recorded schema hash": _file_hash, "recorded pin hash": _pin_hash,
                  "recorded tool": _swap_tool, "recorded pin path": _pin_path}[cell]
        change(repo, doc["records"][-1]["runs"][index])
        repo.write(RECORD, yaml.safe_dump(doc, sort_keys=False))
    else:
        entries = [dict(SPECTRAL), dict(BUF)]
        if cell == "entry's linter in the config":
            entries[index]["linter"] = "buf" if index == 0 else "spectral"
        else:
            entries[index]["pin"] = ".other-pin.yaml"
            repo.write(".other-pin.yaml", "rules: {}\n")
        repo.config(schemas=entries)
    assert reading(repo, capsys) == ("to do", [])


def test_done_means_a_pin_file_that_is_absent_reads_null_on_both_sides_and_an_installed_run_is_no_result(
        repo, capsys):
    S, B = repo.two()
    repo.records_file(repo.record(S, B))
    assert quick(repo, capsys) == ("done", [])  # with the pin there
    (repo.root / ".spectral.yaml").unlink()
    S = repo.run("spectral", ".spectral.yaml", [("api/a.yaml", 0), ("api/b.yaml", 0)])
    assert S["pin"]["sha256"] is None
    repo.records_file(repo.record(S, B))
    # an installed run whose pin hash is null is no pinned result: never done
    assert reading(repo, capsys) == ("to do", [])
    # a report above 0 does not show either, since the result is no result
    S["files"][0]["reported"] = 2
    repo.records_file(repo.record(S, B))
    assert reading(repo, capsys) == ("to do", [])


# --- done_means: the older shape reads as absent ---------------------------------------

def _flat_record(repo, kind):
    run = repo.run("spectral", ".spectral.yaml", [("api/a.yaml", {"clean": 0, "failed": 2,
                                                                   "missing": 0}[kind])],
                   installed=kind != "missing")
    return {"condition": "G1.1", "at": "2026-10-07T14:02:11Z", "head": "8635064", **run}


@pytest.mark.parametrize("kind", ["clean", "failed", "missing"], ids=[
    "a clean record", "a record that reports", "a record of a tool not installed"])
def test_done_means_a_record_in_the_older_shape_counts_as_absent_and_lint_replaces_it(
        repo, capsys, kind):
    repo.write("api/a.yaml", "a: 1\n")
    repo.records_file(_flat_record(repo, kind))
    assert list(repo.records()[-1])[3:] == RUN_KEYS  # the fixture is the older shape
    assert reading(repo, capsys) == ("to do", [])
    repo.install("spectral")
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), RECORDED]
    assert code == 0
    assert len(repo.records()) == 2  # appended; the older record stays in the file
    assert list(repo.records()[-1]) == ["condition", "at", "head", "runs"]
    assert reading(repo, capsys) == ("done", [])


# --- done_means: a path that reaches done with no record is a defect --------------------

@pytest.mark.parametrize("state", [
    "no record file", "no records", "an empty file", "only a review record",
    "a lint record with no runs", "a run for other files only", "a run of a tool not asked",
])
def test_done_means_a_schema_in_scope_with_no_record_of_its_result_never_reads_done(
        repo, capsys, state):
    repo.two()
    repo.install("spectral")
    repo.install("buf")
    baseline_done(repo, capsys)  # the run that records them, so the file stands and then goes
    other = repo.run("spectral", ".spectral.yaml", [("api/other.yaml", 0)])
    review = {"condition": "G1.3", "at": "2026-10-07T14:20:40Z", "head": "8635064",
              "by": "Ann Lee", "seat": "user", "requirements": "r5", "items": []}
    if state == "no record file":
        (repo.root / RECORD).unlink()
    elif state == "no records":
        repo.write(RECORD, "records: []\n")
    elif state == "an empty file":
        repo.write(RECORD, "")
    elif state == "only a review record":
        repo.records_file(review)
    elif state == "a lint record with no runs":
        repo.records_file(repo.record())
    elif state == "a run for other files only":
        repo.records_file(repo.record(other))
    else:
        asked = repo.run("buf", "buf.yaml", [("api/a.yaml", 0), ("api/b.yaml", 0),
                                              ("proto/x.proto", 0)])
        repo.records_file(repo.record(asked))
    status, messages = reading(repo, capsys)
    assert status == "to do"
    assert messages == []


def test_done_means_a_clean_run_of_the_right_tool_for_other_files_gives_no_result_for_these(
        repo, capsys):
    S, B = repo.two()
    repo.records_file(repo.record(S, B))
    assert quick(repo, capsys) == ("done", [])
    repo.write("api/c.yaml", "c: 1\n")  # a schema in scope that no run holds
    assert reading(repo, capsys) == ("to do", [])


# --- done_means: a contract whose scope cannot be read ----------------------------------

SCOPES = {
    "the YAML does not parse": "id: apply-discount\nscope: [api/\n",
    "no scope key": None,
    "scope is a string": "scope: api/",
    "scope is a mapping": "scope: {api: 1}",
    "scope is empty": "scope: []",
    "scope has no value": "scope:",
}


def _break_scope(repo, how: str) -> None:
    text = SCOPES[how]
    if how == "the YAML does not parse":
        repo.write(f"specs/{ID}/contract.yaml", text)
    else:
        repo.contract_with(text)


@pytest.mark.parametrize("how", list(SCOPES))
@pytest.mark.parametrize("declaration", ["a schema on disk with a clean record", "an empty list"])
def test_done_means_a_contract_whose_scope_cannot_be_read_reads_g1_1_to_do_with_no_finding(
        repo, capsys, how, declaration):
    repo.write("api/a.yaml", "a: 1\n")
    repo.install("spectral")
    if declaration == "an empty list":
        repo.config(schemas=[])
        assert reading(repo, capsys) == ("done", [])  # no schema in scope, the scope readable
    else:
        baseline_done(repo, capsys)
    _break_scope(repo, how)
    before = repo.files()
    assert reading(repo, capsys) == ("to do", [])
    assert repo.files() == before  # and the readers wrote nothing


@pytest.mark.parametrize("how", list(SCOPES))
def test_done_means_a_contract_whose_scope_cannot_be_read_reads_to_do_over_a_failed_record(
        repo, capsys, how):
    repo.write("api/a.yaml", "a: 1\n")
    repo.install("spectral")
    repo.plan(rows={"api/a.yaml": [["r1", ERROR]]})
    assert lint(capsys)[0] == 1
    assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 1)])
    _break_scope(repo, how)
    assert reading(repo, capsys) == ("to do", [])


@pytest.mark.parametrize("how", list(SCOPES))
@pytest.mark.parametrize("schemas", [(SPECTRAL,), ABSENT, (SPECTRAL, ESLINT)], ids=[
    "g1.schemas declared", "g1.schemas absent", "an entry with a linter the kit does not know"])
def test_done_means_lint_refuses_a_scope_that_cannot_be_read_before_it_reads_the_declaration(
        repo, capsys, how, schemas):
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("schemas/s.json", '{"title": "S"}\n')
    repo.install("spectral")
    repo.config(schemas=schemas)
    _break_scope(repo, how)
    before = repo.files()
    code, out, err = lint(capsys)
    assert code == 2
    assert err.splitlines() == [f"{ID}: the contract's scope cannot be read at "
                                f"specs/{ID}/contract.yaml"]
    assert out == ""
    assert repo.calls() == []
    assert repo.files() == before
    assert not (repo.root / ".sdlc" / "g1").exists()  # no folder is made


def test_done_means_the_tree_prints_g1_1_to_do_for_a_scope_that_cannot_be_read(repo, capsys):
    repo.write("api/a.yaml", "a: 1\n")
    repo.install("spectral")
    baseline_done(repo, capsys)
    assert tree_g1_1(repo, capsys) == ("done", [])
    repo.contract_with(None)
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0
    assert f"    {ID}/G1/G1.1 Spec/schema linting [to do]" in out.splitlines()
    assert "unreadable G1 reading" not in err
    code, out, _ = check(repo, capsys)  # and g1-check's own print
    assert out.splitlines() == [f"{ID}: G1.1 to do, G1.2 to do, G1.3 to do"]
    assert code == 1


# --- done_means: a reading never rests on what the reader cannot read -------------------
# The fixture: Spectral on api/a.yaml and api/b.yaml, buf on proto/x.proto. A style
# runs the fault on an all-clean record (the reading must not be done); B style on
# a record where api/a.yaml reports 2 (what the fault does not touch still counts).

def _file(run, n=0):
    return run["files"][n]


FAULTS = {
    "files is a string": lambda r: {**r, "files": "proto/x.proto"},
    "files is a number": lambda r: {**r, "files": 5},
    "files holds a number": lambda r: {**r, "files": [5]},
    "files holds a string": lambda r: {**r, "files": ["proto/x.proto"]},
    "files holds a null": lambda r: {**r, "files": [None]},
    "files is a mapping": lambda r: {**r, "files": {"path": "proto/x.proto"}},
    "a file's path is a list": lambda r: {**r, "files": [{**_file(r), "path": [_file(r)["path"]]}]
                                          + r["files"][1:]},
    "a file's path is a mapping": lambda r: {**r, "files": [{**_file(r), "path": {"p": 1}}]
                                             + r["files"][1:]},
    "a file's hash is a list": lambda r: {**r, "files": [{**_file(r), "sha256": [1]}]
                                          + r["files"][1:]},
    "reported is a bool true": lambda r: {**r, "files": [{**_file(r), "reported": True}]
                                          + r["files"][1:]},
    "reported is a bool false": lambda r: {**r, "files": [{**_file(r), "reported": False}]
                                           + r["files"][1:]},
    "reported is a string": lambda r: {**r, "files": [{**_file(r), "reported": "0"}]
                                       + r["files"][1:]},
    "reported is a float": lambda r: {**r, "files": [{**_file(r), "reported": 0.0}]
                                      + r["files"][1:]},
    "reported is a null": lambda r: {**r, "files": [{**_file(r), "reported": None}]
                                     + r["files"][1:]},
    "pin is a list": lambda r: {**r, "pin": [r["pin"]["path"]]},
    "pin is a string": lambda r: {**r, "pin": r["pin"]["path"]},
    "pin is a null": lambda r: {**r, "pin": None},
    "pin path is a list": lambda r: {**r, "pin": {**r["pin"], "path": [r["pin"]["path"]]}},
    "pin hash is a mapping": lambda r: {**r, "pin": {**r["pin"], "sha256": {"h": 1}}},
    "tool is a list": lambda r: {**r, "tool": [r["tool"]]},
    "tool is a mapping": lambda r: {**r, "tool": {"name": r["tool"]}},
    "the run is a string": lambda r: r["tool"],
    "the run is a number": lambda r: 7,
    "the run is a null": lambda r: None,
    "the run is a list": lambda r: [r],
}


@pytest.mark.parametrize("index", [0, 1], ids=["first run", "second run"])
@pytest.mark.parametrize("fault", list(FAULTS))
def test_done_means_a_value_the_reader_cannot_read_counts_as_absent_for_what_it_holds(
        repo, capsys, fault, index):
    # A style: all clean. The fault makes one schema's result unreadable.
    S, B = repo.two()
    repo.records_file(repo.record(S, B))
    assert quick(repo, capsys) == ("done", [])  # the record without the fault
    runs = [S, B]
    runs[index] = FAULTS[fault](copy.deepcopy(runs[index]))
    repo.records_file(repo.record(*runs))
    assert reading(repo, capsys) == ("to do", [])
    # B style: api/a.yaml reports 2; the fault in the second run leaves that finding,
    # in the first run it takes it away, and nothing else changes.
    S, B = repo.two(a=2)
    repo.records_file(repo.record(S, B))
    assert quick(repo, capsys) == ("failed", [rs102("api/a.yaml", 2)])
    runs = [S, B]
    runs[index] = FAULTS[fault](copy.deepcopy(runs[index]))
    repo.records_file(repo.record(*runs))
    if index == 1:
        assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 2)])
    else:
        assert reading(repo, capsys) == ("to do", [])


@pytest.mark.parametrize("junk", ["a string", 7, None, ["a", "list"], {"a": "mapping"}],
                         ids=["a string", "a number", "a null", "a list", "a mapping"])
def test_done_means_a_run_that_cannot_be_read_beside_good_runs_leaves_them_standing(
        repo, capsys, junk):
    S, B = repo.two(a=2)
    repo.records_file(repo.record(S, B))
    assert quick(repo, capsys) == ("failed", [rs102("api/a.yaml", 2)])
    repo.records_file(repo.record(junk, S, junk, B, junk))
    assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 2)])
    S, B = repo.two()
    repo.records_file(repo.record(junk, S, B))
    assert reading(repo, capsys) == ("done", [])


def _hostile_text(kind: str, good: dict) -> str:
    """The record file as text: the good record's YAML with the fault in it."""
    dumped = yaml.safe_dump({"records": [good]}, sort_keys=False)
    if kind == "runs is a string":
        return yaml.safe_dump({"records": [{**good, "runs": "spectral"}]}, sort_keys=False)
    if kind == "runs is a mapping":
        return yaml.safe_dump({"records": [{**good, "runs": good["runs"][0]}]}, sort_keys=False)
    if kind == "runs is a number":
        return yaml.safe_dump({"records": [{**good, "runs": 3}]}, sort_keys=False)
    if kind == "runs is a null":
        return yaml.safe_dump({"records": [{**good, "runs": None}]}, sort_keys=False)
    if kind == "runs holds only junk":
        return yaml.safe_dump({"records": [{**good, "runs": ["a", 1, None]}]}, sort_keys=False)
    if kind == "runs is empty":
        return yaml.safe_dump({"records": [{**good, "runs": []}]}, sort_keys=False)
    if kind == "the record has no runs key":
        return yaml.safe_dump({"records": [{k: v for k, v in good.items() if k != "runs"}]},
                              sort_keys=False)
    if kind == "the file is no YAML":
        return "records: [not closed\n  - {oops\n"
    if kind == "the top level is a list":
        return yaml.safe_dump([good], sort_keys=False)
    if kind == "the top level is a string":
        return "just some words\n"
    if kind == "records is a string":
        return "records: not a list\n"
    if kind == "records is a mapping":
        return yaml.safe_dump({"records": good}, sort_keys=False)
    if kind == "a record is a string":
        return yaml.safe_dump({"records": ["junk"]}, sort_keys=False)
    if kind == "a date no calendar holds":
        return dumped.replace("2026-10-17T10:00:00Z", "2026-13-45").replace("'2026-13-45'", "2026-13-45")
    if kind == "the file is empty":
        return ""
    if kind == "a later record cannot be read":
        return yaml.safe_dump({"records": [good, {**good, "runs": "spectral"}]}, sort_keys=False)
    raise AssertionError(kind)


HOSTILE_FILES = ["runs is a string", "runs is a mapping", "runs is a number", "runs is a null",
                 "runs holds only junk", "runs is empty", "the record has no runs key",
                 "the file is no YAML", "the top level is a list", "the top level is a string",
                 "records is a string", "records is a mapping", "a record is a string",
                 "a date no calendar holds", "the file is empty", "a later record cannot be read"]


@pytest.mark.parametrize("kind", HOSTILE_FILES)
def test_done_means_a_record_file_the_reader_cannot_read_counts_as_absent(repo, capsys, kind):
    S, B = repo.two(a=2)
    good = repo.record(S, B)
    repo.records_file(good)
    assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 2)])  # the good record
    repo.write(RECORD, _hostile_text(kind, good))
    if kind == "a date no calendar holds":
        assert "2026-13-45" in (repo.root / RECORD).read_text(encoding="utf-8")
    assert reading(repo, capsys) == ("to do", [])


def test_done_means_two_runs_for_one_entry_never_read_done_and_a_finding_prints_once(
        repo, capsys):
    S, B = repo.two()
    repo.records_file(repo.record(S, copy.deepcopy(S)))  # buf's schema has no run
    assert reading(repo, capsys) == ("to do", [])
    repo.records_file(repo.record(S, B, copy.deepcopy(B)))  # a run twice is harmless
    assert reading(repo, capsys) == ("done", [])
    S, B = repo.two(a=2)
    repo.records_file(repo.record(S, copy.deepcopy(S), B))
    assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 2)])


def test_done_means_a_missing_tool_run_twice_prints_its_finding_once(repo, capsys):
    S, B = repo.two()
    gone = repo.run("buf", "buf.yaml", [("proto/x.proto", 0)], installed=False)
    repo.records_file(repo.record(S, gone, copy.deepcopy(gone)))
    assert reading(repo, capsys) == ("failed", [rs101("buf")])


# --- done_means: a declaration that cannot be read holds G1.1 at to do -------------------

@pytest.mark.parametrize("entry", [
    {"paths": "api/*.yaml", "linter": "spectral", "pin": ".spectral.yaml"},
    {"linter": "spectral", "pin": ".spectral.yaml"},
    {"paths": ["api/*.yaml"], "linter": "spectral"},
    {"paths": ["api/*.yaml"], "pin": ".spectral.yaml"},
    "api/*.yaml",
], ids=["paths is no list", "no paths", "no pin", "no linter", "an entry is no mapping"])
@pytest.mark.parametrize("record", ["failed", "not installed"])
def test_done_means_an_entry_that_cannot_be_read_holds_g1_1_at_to_do_whatever_the_runs_hold(
        repo, capsys, entry, record):
    S, B = repo.two(a=2)
    if record == "failed":
        repo.records_file(repo.record(S, B))
        assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 2)])
    else:
        gone = repo.run("buf", "buf.yaml", [("proto/x.proto", 0)], installed=False)
        repo.records_file(repo.record(S, gone))
        assert reading(repo, capsys) == ("failed", [rs102("api/a.yaml", 2), rs101("buf")])
    repo.config(schemas=[SPECTRAL, BUF, entry])
    assert reading(repo, capsys) == ("to do", [])


def test_done_means_g1_check_and_the_tree_run_no_tool_and_write_nothing(repo, capsys, tmp_path):
    repo.two(a=2)
    repo.install("spectral")
    repo.install("buf")
    assert lint(capsys)[0] in (0, 1)
    before, started = repo.files(), len(repo.calls())
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    repo.monkeypatch.chdir(elsewhere)  # --root names the repository
    reading(repo, capsys)
    assert len(repo.calls()) == started
    assert repo.files() == before
    assert list(elsewhere.iterdir()) == []


def test_done_means_the_tree_prints_the_runs_findings_under_g1_1(repo, capsys):
    S, B = repo.two(a=2, x=1)
    gone = repo.run("buf", "buf.yaml", [("proto/x.proto", 0)], installed=False)
    repo.records_file(repo.record(S, B))
    code, out, _ = cli(capsys, "tree", "--root", repo.root)
    assert code == 0
    lines = out.splitlines()
    row = f"    {ID}/G1/G1.1 Spec/schema linting [failed]"
    assert row in lines
    at = lines.index(row)
    assert lines[at + 1: at + 3] == [f"      - {rs102('api/a.yaml', 2)}",
                                     f"      - {rs102('proto/x.proto', 1, 'buf')}"]
    repo.records_file(repo.record(S, gone))
    code, out, _ = cli(capsys, "tree", "--root", repo.root)
    lines = out.splitlines()
    assert row in lines
    at = lines.index(row)
    assert lines[at + 1: at + 3] == [f"      - {rs102('api/a.yaml', 2)}",
                                     f"      - {rs101('buf')}"]
