"""G1.1 suite (contract: g1-requirements-spec, unit s1-lint).

A temporary repository per test: one ready contract under specs/, a
.sdlc/config.yaml that turns G1 on and declares the boundary schemas, the
schema files and the pin. No test needs a linter on the machine: a
stand-in stands on a PATH the test sets, as a real child process, and
answers as Spectral 6.17.0 was measured to answer. It leaves a mark each
time it starts, so a test can prove that no tool ran.

What the unit pins: `g1-record lint` runs the pinned linter on each
boundary schema in the feature's scope and appends one record to
.sdlc/g1/<id>.yaml; `g1-check` reads that record against the files on
disk, runs no tool and writes nothing. G1.1 reads done only from a clean
record that still matches the schema's hash and the pin's (done_means); a
warning fails it as an error does (SC2.1); no schema in scope passes it
with no linter run (SC2.2); a linter that is not installed fails it with
RS101 (SC2.3). The exit codes, each printed line, the record's keys and
the three `rules:` lists of G1 in gates.yaml each have a case.

No fixture holds specs/components.yaml or a review record, so G1.2 and
G1.3 read `to do` in every summary line here.
"""

from __future__ import annotations

import hashlib
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
from conftest import write_seat_roster
from taskcontract.__main__ import main

ID = "apply-discount"
RECORD = f".sdlc/g1/{ID}.yaml"
GIT = shutil.which("git")
ENVIRON = dict(os.environ)  # as the suite started, before a test cuts PATH
ABSENT = object()

CONTRACT = """id: {id}
title: A fixture feature
intent: >
  A contract with a scope of its own, enough words to pass the door as a
  fixture for the G1.1 suite.
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
BUF = {"paths": ["proto/*.proto"], "linter": "buf", "pin": "buf.yaml"}

ERROR, WARNING, INFO, HINT = 0, 1, 2, 3  # Spectral's severities

# The stand-in linter. It runs as `python stand_in.py <tool> <the tool's
# arguments>` behind a file named for the tool, logs each start beside
# itself, and answers from plan.json. As Spectral it follows the measured
# 6.17.0: `--version` prints the version alone; `lint` with `--format json`
# prints a JSON array of rows, and without `--quiet` a clean run's output
# is no JSON; it exits 1 when a row stands at `--fail-severity` or above,
# which is an error unless the flag says `warn`, so 0 on a warning alone
# without the flag; and 2 with lines on stderr for an error of its own.
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
        err.write(b"No ruleset has been found. Please provide a ruleset using the --ruleset "
                  b"CLI argument, or make sure your ruleset file matches "
                  b".?spectral.(js|ya?ml|json)\n")
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
    else:
        for row in rows:
            out.write(("%s\n 1:1  %s  %s  %s\n" % (
                row["source"], ("error", "warning", "information", "hint")[row["severity"]],
                row["code"], row["message"])).encode("utf-8"))
        if rows:
            out.write(("\n%d problems\n" % len(rows)).encode("utf-8"))
    if not rows and "--quiet" not in options:
        out.write(b"No results with a severity of 'error' found!\n")
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
        self.contract(ID, "api/", "src/")
        self.config()
        self.write(".spectral.yaml", "rules: {}\n")
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

    def config(self, schemas=(SPECTRAL,), active=("G0", "G1"),
               exempt=("controlled-language",)) -> None:
        """.sdlc/config.yaml as a person writes it; ABSENT leaves a key out."""
        g1 = {}
        if exempt is not ABSENT:
            g1["exempt"] = list(exempt)
        if schemas is not ABSENT:
            g1["schemas"] = list(schemas)
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

    def plan(self, rows=None, version="6.17.0", own_error=None, raw=False) -> None:
        """What the stand-in answers: `rows` maps a schema's path to a list
        of [code, severity]; a path it does not name lints clean."""
        (self.bin / "plan.json").write_text(json.dumps({
            "root": str(self.root), "rows": rows or {}, "version": version,
            "own_error": own_error, "raw": raw}), encoding="utf-8")

    def calls(self) -> list[dict]:
        """Each start of a stand-in, in order: the mark it leaves."""
        log = self.bin / "calls.jsonl"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    def lints(self) -> list[dict]:
        return [call for call in self.calls() if call["argv"][:1] == ["lint"]]

    def records(self) -> list[dict]:
        return yaml.safe_load((self.root / RECORD).read_text(encoding="utf-8"))["records"]

    def files(self) -> dict[str, bytes]:
        """Every file under the root with its bytes: what a call wrote shows
        as a difference."""
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in sorted(self.root.rglob("*")) if path.is_file()}


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


def summary(g1_1: str) -> str:
    return f"{ID}: G1.1 {g1_1}, G1.2 to do, G1.3 to do"


def clean(path: str, tool: str = "spectral") -> str:
    return f"G1.1: {path} lints clean under {tool}"


def rs101(tool: str = "spectral") -> str:
    return f"G1.1: {tool} is not installed; install it and pin it in the repository"


def rs102(path: str, n: int, tool: str = "spectral") -> str:
    return f"G1.1: {path} does not lint clean: {tool} reports {n}"


RECORDED = f"recorded: {RECORD}"


def g1_rules() -> dict[str, list[str]]:
    """G1's conditions with the codes each owns, from the packaged list."""
    path = Path(taskcontract.__file__).parent / "data" / "gates.yaml"
    gates = yaml.safe_load(path.read_text(encoding="utf-8"))["gates"]
    gate = next(g for g in gates if g["id"] == "G1")
    return {c["id"]: c.get("rules") for c in gate["conditions"]}


# --- SC2.1: the linter runs under its pin on each boundary schema in scope ---

def test_sc2_1_a_clean_file_is_recorded_and_g1_1_reads_done(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/openapi.yaml"), RECORDED]
    assert code == 0
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("done")]
    assert code == 1  # G1 is not done while G1.2 and G1.3 read to do


def test_sc2_1_the_record_holds_the_drawings_keys_and_the_whole_hashes(repo, capsys):
    schema = repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(version="6.99.1")
    lint(capsys)
    text = (repo.root / RECORD).read_text(encoding="utf-8")
    assert list(yaml.safe_load(text)) == ["records"]
    (record,) = repo.records()
    assert list(record) == ["condition", "at", "head", "tool", "tool_version",
                            "installed", "pin", "files"]
    assert record["condition"] == "G1.1"
    assert record["tool"] == "spectral"
    assert record["tool_version"] == "6.99.1"  # read from the tool's own --version
    assert record["installed"] is True
    assert record["pin"] == {"path": ".spectral.yaml",
                             "sha256": sha(repo.root / ".spectral.yaml")}
    assert record["files"] == [{"path": "api/openapi.yaml", "sha256": sha(schema),
                                "reported": 0}]
    assert len(record["pin"]["sha256"]) == 64
    assert re.search(r"\bat: ['\"]?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z['\"]?\s", text)
    assert record["head"] == "no commit"  # no git on this PATH, as progress records it
    # A committed file: the folder holds the record and nothing beside it.
    assert [p.name for p in (repo.root / ".sdlc" / "g1").iterdir()] == [f"{ID}.yaml"]


@pytest.mark.skipif(GIT is None, reason="git not on PATH")
def test_sc2_1_the_record_names_the_short_head_of_the_repository(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")

    def git(*args: str) -> str:
        return subprocess.run([GIT, *args], cwd=repo.root, check=True, env=ENVIRON,
                              capture_output=True, encoding="utf-8").stdout

    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    git("config", "commit.gpgsign", "false")
    git("add", "-A")
    git("commit", "-q", "-m", "seed")
    head = git("rev-parse", "--short", "HEAD").strip()
    repo.monkeypatch.setenv("PATH", os.pathsep.join([str(repo.bin), str(Path(GIT).parent)]))
    code, _, _ = lint(capsys)
    assert code == 0
    assert repo.records()[-1]["head"] == head


def test_sc2_1_the_linter_starts_once_for_each_file_under_the_pin(repo, capsys):
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("api/b.yaml", "b: 1\n")
    repo.install("spectral")
    lint(capsys)
    # `--fail-severity warn`: the linter's exit code then reads 0 for a clean
    # file alone, since it exits 0 on a warning without it.
    assert [call["argv"] for call in repo.lints()] == [
        ["lint", "api/a.yaml", "--ruleset", ".spectral.yaml", "--format", "json", "--quiet",
         "--fail-severity", "warn"],
        ["lint", "api/b.yaml", "--ruleset", ".spectral.yaml", "--format", "json", "--quiet",
         "--fail-severity", "warn"],
    ]
    assert {os.path.realpath(call["cwd"]) for call in repo.calls()} == {
        os.path.realpath(repo.root)}
    assert {call["tool"] for call in repo.calls()} == {"spectral"}


def test_sc2_1_only_a_file_that_matches_a_pattern_and_the_scope_is_linted(repo, capsys):
    """In scope: a schemas pattern and a scope entry both match the path. A
    scope entry that ends in a slash is a folder; another is the path itself."""
    repo.contract(ID, "api/openapi.yaml", "src/", "docs/")
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")  # pattern and scope: linted
    repo.write("api/other.yaml", "x: 1\n")              # pattern, outside the scope
    repo.write("src/openapi.yaml", "x: 1\n")            # scope, no pattern
    repo.write("docs/api/x.yaml", "x: 1\n")             # the pattern reads from the root
    repo.write("api/readme.md", "x\n")
    repo.install("spectral")
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/openapi.yaml"), RECORDED]
    assert code == 0
    assert [f["path"] for f in repo.records()[-1]["files"]] == ["api/openapi.yaml"]
    assert [call["argv"][1] for call in repo.lints()] == ["api/openapi.yaml"]
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc2_1_one_entry_with_two_patterns_lints_a_json_schema_and_an_openapi_file(
        repo, capsys):
    repo.contract(ID, "api/", "schemas/")
    repo.config(schemas=[{"paths": ["api/*.yaml", "schemas/*.schema.json"],
                          "linter": "spectral", "pin": ".spectral.yaml"}])
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.write("schemas/discount.schema.json", '{"title": "Discount", "type": "object"}\n')
    repo.install("spectral")
    repo.plan(rows={"schemas/discount.schema.json": [["schema-names-its-dialect", ERROR]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/openapi.yaml"),
                                rs102("schemas/discount.schema.json", 1), RECORDED]
    assert code == 1
    assert [call["argv"][1] for call in repo.lints()] == [
        "api/openapi.yaml", "schemas/discount.schema.json"]
    assert len(repo.records()) == 1


def test_sc2_1_a_warning_alone_fails_g1_1_as_an_error_does(repo, capsys):
    schema = repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [["schema-has-a-title", WARNING]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [rs102("api/openapi.yaml", 1), RECORDED]
    assert code == 1
    assert repo.records()[-1]["files"] == [
        {"path": "api/openapi.yaml", "sha256": sha(schema), "reported": 1}]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS102 {rs102('api/openapi.yaml', 1)}",
                                summary("failed")]
    assert code == 1


def test_sc2_1_an_error_fails_g1_1_and_n_counts_errors_and_warnings_alike(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [
        ["schema-names-its-dialect", ERROR], ["schema-has-a-title", WARNING],
        ["a-note", INFO], ["a-hint", HINT]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [rs102("api/openapi.yaml", 2), RECORDED]
    assert code == 1
    assert repo.records()[-1]["files"][0]["reported"] == 2
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS102 {rs102('api/openapi.yaml', 2)}",
                                summary("failed")]
    assert code == 1


def test_sc2_1_what_the_linter_reports_below_a_warning_is_recorded_clean(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [["a-note", INFO], ["a-hint", HINT]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/openapi.yaml"), RECORDED]
    assert code == 0
    assert repo.records()[-1]["files"][0]["reported"] == 0
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc2_1_several_files_print_and_record_by_path_each_with_its_count(repo, capsys):
    repo.write("api/c.yaml", "c: 1\n")
    repo.write("api/a.yaml", "a: 1\n")
    repo.write("api/b.yaml", "b: 1\n")
    repo.install("spectral")
    repo.plan(rows={"api/b.yaml": [["r1", ERROR], ["r2", WARNING]],
                    "api/c.yaml": [["r2", WARNING]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/a.yaml"), rs102("api/b.yaml", 2),
                                rs102("api/c.yaml", 1), RECORDED]
    assert code == 1
    assert len(repo.records()) == 1  # one call, one record
    assert [(f["path"], f["reported"]) for f in repo.records()[0]["files"]] == [
        ("api/a.yaml", 0), ("api/b.yaml", 2), ("api/c.yaml", 1)]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS102 {rs102('api/b.yaml', 2)}",
                                f"{ID}: RS102 {rs102('api/c.yaml', 1)}",
                                summary("failed")]
    assert code == 1


def test_sc2_1_g1_check_json_is_the_envelope_of_note_and_findings(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {"note": "G1.1 to do, G1.2 to do, G1.3 to do", "findings": []}
    assert code == 1
    repo.plan(rows={"api/openapi.yaml": [["schema-has-a-title", WARNING]]})
    lint(capsys)
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {
        "note": "G1.1 failed, G1.2 to do, G1.3 to do",
        "findings": [{"feature": ID, "condition": "G1.1", "rule": "RS102",
                      "message": rs102("api/openapi.yaml", 1)}]}
    assert code == 1


def test_sc2_1_a_linter_that_ends_on_its_own_error_gives_no_result(repo, capsys):
    """Spectral exits 2 on an error of its own. That is no lint result: the
    tool's lines are shown, nothing is written, and the last record stands."""
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    assert lint(capsys)[0] == 0
    before = repo.files()
    repo.plan(own_error="Error running Spectral!\nError #1: the ruleset holds no rule")
    code, out, err = lint(capsys)
    assert code == 2
    assert "Error running Spectral!" in err.splitlines()
    assert "Error #1: the ruleset holds no rule" in err.splitlines()
    assert out == ""
    assert repo.files() == before
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc2_1_a_pin_whose_file_is_absent_gives_no_result(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    (repo.root / ".spectral.yaml").unlink()
    repo.install("spectral")
    before = repo.files()
    code, out, err = lint(capsys)
    assert code == 2
    assert len(repo.lints()) == 1  # the linter started, and ended on its own error
    assert "Error running Spectral!" in err.splitlines()
    assert out == ""
    assert repo.files() == before
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]
    assert code == 1


def test_sc2_1_a_byte_that_is_not_utf8_in_the_report_does_not_break_the_call(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [["schema-has-a-title", WARNING]]}, raw=True)
    code, out, _ = lint(capsys)
    assert out.splitlines() == [rs102("api/openapi.yaml", 1), RECORDED]
    assert code == 1
    assert repo.records()[-1]["files"][0]["reported"] == 1


def test_sc2_1_a_byte_that_is_not_utf8_in_the_tools_own_error_does_not_break_the_call(
        repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(own_error="Error running Spectral!\nError #1: cannot read @@RAW@@", raw=True)
    code, out, err = lint(capsys)
    assert code == 2
    assert "Error running Spectral!" in err.splitlines()
    assert any(line.startswith("Error #1: cannot read ") for line in err.splitlines())
    assert not (repo.root / RECORD).exists()


def test_sc2_1_buf_lints_a_protobuf_file_and_the_lines_name_buf(repo, capsys):
    repo.contract(ID, "proto/")
    repo.config(schemas=[BUF])
    schema = repo.write("proto/discount.proto", 'syntax = "proto3";\n')
    pin = repo.write("buf.yaml", "version: v2\n")
    repo.install("buf")
    repo.plan(version="1.47.2")
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("proto/discount.proto", "buf"), RECORDED]
    assert code == 0
    record = repo.records()[-1]
    assert (record["tool"], record["installed"]) == ("buf", True)
    assert record["pin"] == {"path": "buf.yaml", "sha256": sha(pin)}
    assert record["files"] == [{"path": "proto/discount.proto", "sha256": sha(schema),
                                "reported": 0}]
    assert {call["tool"] for call in repo.calls()} == {"buf"}
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc2_1_buf_reporting_on_a_protobuf_file_fails_g1_1_with_its_count(repo, capsys):
    repo.contract(ID, "proto/")
    repo.config(schemas=[BUF])
    repo.write("proto/discount.proto", 'syntax = "proto3";\n')
    repo.write("buf.yaml", "version: v2\n")
    repo.install("buf")
    repo.plan(version="1.47.2", rows={"proto/discount.proto": [
        ["PACKAGE_DEFINED", ERROR], ["ENUM_ZERO_VALUE_SUFFIX", ERROR]]})
    code, out, _ = lint(capsys)
    assert out.splitlines() == [rs102("proto/discount.proto", 2, "buf"), RECORDED]
    assert code == 1
    assert repo.records()[-1]["files"][0]["reported"] == 2
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS102 {rs102('proto/discount.proto', 2, 'buf')}",
                                summary("failed")]
    assert code == 1


# --- done_means: G1.1 reads done only when the record shows the schema clean ---

def test_done_means_a_schema_in_scope_with_no_record_reads_to_do_and_lists_nothing(
        repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]  # a to do lists nothing
    assert code == 1


def test_done_means_g1_1_reads_to_do_while_the_schemas_key_is_absent(repo, capsys):
    repo.config(schemas=ABSENT)
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]
    assert code == 1
    repo.config(schemas=ABSENT, exempt=ABSENT)  # no g1 key at all
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("to do")]
    assert code == 1


def test_done_means_a_schema_changed_after_a_clean_run_returns_g1_1_to_to_do(repo, capsys):
    schema = repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    lint(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    schema.write_bytes(b"openapi: 3.1.0\ninfo: {}\n")
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]
    assert lint(capsys)[0] == 0
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_done_means_a_pin_changed_after_a_clean_run_returns_g1_1_to_to_do(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    lint(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    repo.write(".spectral.yaml", "rules: {}\n# a rule more\n")
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]


def test_done_means_a_schema_added_after_the_run_has_no_record_so_g1_1_reads_to_do(
        repo, capsys):
    repo.write("api/a.yaml", "a: 1\n")
    repo.install("spectral")
    lint(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    repo.write("api/b.yaml", "b: 1\n")
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]


def test_done_means_a_failed_record_whose_file_changed_counts_as_absent(repo, capsys):
    schema = repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [["schema-has-a-title", WARNING]]})
    assert lint(capsys)[0] == 1
    assert check(repo, capsys)[1].splitlines()[-1] == summary("failed")
    schema.write_bytes(b"openapi: 3.1.0\ninfo: {title: Discount}\n")
    assert check(repo, capsys)[1].splitlines() == [summary("to do")]


def test_done_means_each_call_appends_one_record_and_the_last_one_counts(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    assert lint(capsys)[0] == 0
    repo.plan(rows={"api/openapi.yaml": [["schema-has-a-title", WARNING]]})
    assert lint(capsys)[0] == 1
    assert [r["files"][0]["reported"] for r in repo.records()] == [0, 1]
    assert check(repo, capsys)[1].splitlines()[-1] == summary("failed")
    repo.plan()
    assert lint(capsys)[0] == 0
    assert [r["files"][0]["reported"] for r in repo.records()] == [0, 1, 0]
    assert [r["condition"] for r in repo.records()] == ["G1.1"] * 3
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("done")]
    assert code == 1


def test_done_means_a_record_file_that_cannot_be_read_counts_as_absent(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    lint(capsys)
    assert check(repo, capsys)[1].splitlines() == [summary("done")]
    repo.write(RECORD, "records: [not closed\n")
    code, out, _ = check(repo, capsys)
    assert out.splitlines()[-1] == summary("to do")
    assert not any(" RS" in line for line in out.splitlines())
    assert code == 1


def test_done_means_g1_check_runs_no_tool_and_writes_nothing(repo, capsys, tmp_path):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [["schema-has-a-title", WARNING]]})
    lint(capsys)
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
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    if case == "not listed":
        repo.config(active=("G0",))
    elif case == "exempt":
        repo.config(exempt=("controlled-language", ID))
    else:
        (repo.root / ".sdlc" / "config.yaml").unlink()
    before = repo.files()
    code, out, err = check(repo, capsys)
    assert err.splitlines() == [f"{ID}: G1 is not active"]
    assert out == ""
    assert code == 2
    code, out, _ = lint(capsys)
    assert code == 2
    assert RECORDED not in out and "G1.1:" not in out
    assert repo.calls() == []  # no linter started
    assert repo.files() == before  # and nothing was written


def test_done_means_an_id_with_no_contract_is_a_call_neither_command_can_use(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    before = repo.files()
    code, out, _ = cli(capsys, "g1-record", "lint", "no-such-feature")
    assert code == 2
    assert "recorded:" not in out and "G1.1:" not in out
    code, out, _ = cli(capsys, "g1-check", "no-such-feature", "--root", repo.root)
    assert code == 2
    assert "g1-green" not in out and "G1.1" not in out
    assert repo.calls() == []
    assert repo.files() == before


@pytest.mark.parametrize("condition, codes", [
    ("G1.1", ["RS101", "RS102"]),
    ("G1.2", ["RS201", "RS202", "RS203"]),
    ("G1.3", ["RS301"]),
])
def test_done_means_gates_yaml_lists_the_rules_each_g1_condition_owns(condition, codes):
    assert g1_rules()[condition] == codes


def test_done_means_each_code_reported_under_g1_1_is_one_g1_1_owns(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    lint(capsys)  # no linter on PATH: RS101
    not_installed = json.loads(check(repo, capsys, "--json")[1])["findings"]
    repo.install("spectral")
    repo.plan(rows={"api/openapi.yaml": [["r1", ERROR]]})
    lint(capsys)  # the linter reports: RS102
    unclean = json.loads(check(repo, capsys, "--json")[1])["findings"]
    assert [f["rule"] for f in not_installed + unclean] == ["RS101", "RS102"]
    for finding in not_installed + unclean:
        assert set(finding) == {"feature", "condition", "rule", "message"}
        assert finding["condition"] == "G1.1"
        assert finding["rule"] in (g1_rules()["G1.1"] or [])
        assert finding["message"].startswith("G1.1: ")


# --- SC2.2: no boundary schema in scope passes G1.1, and no linter runs ---

def test_sc2_2_a_feature_with_no_schema_in_scope_passes_g1_1_and_no_linter_runs(
        repo, capsys):
    repo.contract(ID, "src/")
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")  # a schema, outside the scope
    repo.write("src/discount.py", "RATE = 0.1\n")
    repo.install("spectral")  # a linter stands ready, and leaves a mark if it starts
    before = repo.files()
    code, out, _ = lint(capsys)
    assert out.splitlines() == ["G1.1: no boundary schema in scope"]
    assert code == 0
    assert repo.calls() == []
    assert repo.files() == before
    assert not (repo.root / ".sdlc" / "g1").exists()
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [summary("done")]
    assert code == 1
    assert repo.calls() == []


def test_sc2_2_an_empty_schemas_list_says_none_and_g1_1_reads_done(repo, capsys):
    repo.config(schemas=[])
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    repo.install("spectral")
    before = repo.files()
    code, out, _ = lint(capsys)
    assert out.splitlines() == ["G1.1: no boundary schema in scope"]
    assert code == 0
    assert repo.calls() == []
    assert repo.files() == before
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc2_2_a_pattern_that_matches_no_file_on_disk_puts_no_schema_in_scope(repo, capsys):
    repo.write("api/readme.md", "no schema here\n")
    repo.install("spectral")
    code, out, _ = lint(capsys)
    assert out.splitlines() == ["G1.1: no boundary schema in scope"]
    assert code == 0
    assert repo.calls() == []
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc2_2_no_schema_in_scope_passes_with_no_linter_on_the_machine(repo, capsys):
    repo.contract(ID, "src/")
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    code, out, _ = lint(capsys)  # PATH holds no linter at all
    assert out.splitlines() == ["G1.1: no boundary schema in scope"]
    assert code == 0
    assert not (repo.root / ".sdlc" / "g1").exists()
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {"note": "G1.1 done, G1.2 to do, G1.3 to do", "findings": []}
    assert code == 1


# --- SC2.3: a linter that is not installed fails G1.1 with its message ---

def test_sc2_3_a_linter_that_is_not_installed_is_recorded_and_fails_g1_1(repo, capsys):
    a = repo.write("api/a.yaml", "a: 1\n")
    b = repo.write("api/b.yaml", "b: 1\n")
    code, out, _ = lint(capsys)  # PATH holds no spectral
    assert out.splitlines() == [rs101(), RECORDED]  # one line for the tool, not one a file
    assert code == 1
    (record,) = repo.records()
    assert list(record) == ["condition", "at", "head", "tool", "tool_version",
                            "installed", "pin", "files"]
    assert (record["condition"], record["tool"]) == ("G1.1", "spectral")
    assert record["installed"] is False
    assert record["tool_version"] is None
    assert record["pin"] == {"path": ".spectral.yaml",
                             "sha256": sha(repo.root / ".spectral.yaml")}
    assert record["files"] == [
        {"path": "api/a.yaml", "sha256": sha(a), "reported": None},
        {"path": "api/b.yaml", "sha256": sha(b), "reported": None}]
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS101 {rs101()}", summary("failed")]
    assert code == 1  # G1.1 does not pass
    code, out, _ = check(repo, capsys, "--json")
    assert json.loads(out) == {
        "note": "G1.1 failed, G1.2 to do, G1.3 to do",
        "findings": [{"feature": ID, "condition": "G1.1", "rule": "RS101",
                      "message": rs101()}]}
    assert code == 1


def test_sc2_3_the_record_wins_over_the_readers_path_until_the_next_run(repo, capsys):
    repo.write("api/openapi.yaml", "openapi: 3.1.0\n")
    assert lint(capsys)[0] == 1
    repo.install("spectral")  # installed now, and not yet run
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS101 {rs101()}", summary("failed")]
    assert repo.calls() == []
    code, out, _ = lint(capsys)
    assert out.splitlines() == [clean("api/openapi.yaml"), RECORDED]
    assert code == 0
    assert [r["installed"] for r in repo.records()] == [False, True]
    assert check(repo, capsys)[1].splitlines() == [summary("done")]


def test_sc2_3_buf_that_is_not_installed_fails_g1_1_with_its_own_name(repo, capsys):
    repo.contract(ID, "proto/")
    repo.config(schemas=[BUF])
    repo.write("proto/discount.proto", 'syntax = "proto3";\n')
    repo.write("buf.yaml", "version: v2\n")
    repo.install("spectral")  # another linter on PATH does not stand in for buf
    code, out, _ = lint(capsys)
    assert out.splitlines() == [rs101("buf"), RECORDED]
    assert code == 1
    assert (repo.records()[-1]["tool"], repo.records()[-1]["installed"]) == ("buf", False)
    assert repo.calls() == []
    code, out, _ = check(repo, capsys)
    assert out.splitlines() == [f"{ID}: RS101 {rs101('buf')}", summary("failed")]
    assert code == 1
