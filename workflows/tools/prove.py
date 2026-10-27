"""Prove a test file red, or prove mutations caught, on an export of the repository.

usage: prove.py --scratch DIR --test PATH [--at REV] [--mutations FILE] [--timeout SECONDS]

Run from the repository root. PATH is a file from the root (forward slashes,
relative, no `..` part). The script reads the repository's declared test
command from its `.sdlc/config.yaml` (the `taskcontract` beside this script),
exports REV (default HEAD) to DIR/export/, copies the draft DIR/draft/PATH
over export/PATH when that file exists, and runs the commands from the export
root with no shell. The repository's tree and index are never changed and
nothing is written outside DIR. The run is `test.file` with `{file}` replaced
by PATH, or `test.command` when no `file` is declared; a declared `test.build`
runs first, before every run. An `argv[0]` that names a file in the export
runs that file, ahead of a program of the same name on PATH.

Only a pytest command (the word `pytest` in its argv, or `pytest` or `py.test`
as its program) gets `--tb=short`, a junit file and `-p no:cacheprovider`,
and is read test by test: ids are the function name, or `Class::name` in a
class named Test*. Any other command is read by its exit code and last line.

Without --mutations the script proves red. stdout is one compact JSON object:
  ok, scratch, red{summary, red_ok, log, passed?, skipped?, not_assertion?, timeout?}
`red_ok` holds when every pytest test fails on an assertion, or when another
command exits 1; a build that exits non-zero gives red_ok false and a summary
`build: exit N: {last line}`.

With --mutations FILE (a JSON list of {name, file, old, new}; `file` is
relative to the export root) it proves the mutations and not red. It first
runs the unmutated export, which must pass. Each `old` text must match exactly
one place in the file; the loop applies it, runs, records what failed, and
restores the file byte for byte. stdout is
  ok, scratch, mutations: [{name, applied, caught_by, caught_count?, log} |
  {name, applied: false, error}], or "skipped: ..." when the baseline fails.
Each `log` prints relative to the scratch folder; each run's full output is
DIR/logs/<run>.log and the build's is DIR/logs/build.log.

exit: 0 red holds, or every mutation is caught; 1 a check failed; 2 usage;
254 git, a build or the test command never started.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import NamedTuple

# The plugin root goes first, so the taskcontract beside this script wins.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from taskcontract.declaration import read_test  # noqa: E402

SPAWN_FAILED = 254
LINE_CAP = 200
IDS_CAP = 8
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # absent off Windows


class SpawnFailed(Exception):
    """git, a build or the test command could not be started at all."""


class Usage(Exception):
    """The command line or a file it names is wrong."""


class Plan(NamedTuple):
    """What every run needs: where it runs, what it runs, and how long it may take."""
    export: Path
    logs: Path
    build: list[str]
    selected: list[str]
    test: str
    timeout: int


def clip(line: str) -> str:
    return line if len(line) <= LINE_CAP else line[:LINE_CAP - 3] + "..."


def last_line(text: str) -> str:
    """The last non-empty line, stripped; empty when there is none."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return clip(lines[-1]) if lines else ""


def is_pytest(argv: list[str]) -> bool:
    return "pytest" in argv or Path(argv[0]).stem in ("pytest", "py.test")


def inside_repository(test: str) -> bool:
    """True when `test` is a relative path with no `..` part."""
    if not test or PurePosixPath(test).is_absolute() or PureWindowsPath(test).is_absolute():
        return False
    if test.startswith(("/", "\\")):
        return False
    return ".." not in test.replace("\\", "/").split("/")


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True,
                              creationflags=NO_WINDOW)
    except OSError as err:
        raise SpawnFailed(f"git did not start: {err}") from err


def kind_of(tag: str, first: str) -> str:
    """assertion, error (setup or collection), or the exception's name."""
    if tag == "error":
        return "error"
    if first.startswith(("assert", "AssertionError", "Failed:")):
        return "assertion"
    return first.split(":", 1)[0].split()[0] if first else "failure"


def read_cases(xml: Path) -> list[dict]:
    cases = []
    for case in ET.parse(xml).getroot().iter("testcase"):
        name, cls = case.get("name", "?"), (case.get("classname") or "").rsplit(".", 1)[-1]
        item = {"id": f"{cls}::{name}" if cls.startswith("Test") else name,
                "outcome": "passed", "kind": "", "line": ""}
        for child in case:
            if child.tag in ("failure", "error"):
                message = (child.get("message") or child.text or "").strip()
                first = message.splitlines()[0] if message else child.tag
                item.update(outcome="failed", kind=kind_of(child.tag, first), line=clip(first))
            elif child.tag == "skipped":
                item["outcome"] = "skipped"
        cases.append(item)
    return cases


def program(first: str, export: Path) -> str | None:
    """The program to start for `first`: a file under the export, else PATH's."""
    if not Path(first).is_absolute():
        try:
            local = (export / first).resolve()
            if local.is_file() and local.is_relative_to(export):
                return str(local)
        except (OSError, ValueError):
            pass
    return shutil.which(first)


def launch(argv: list[str], export: Path, timeout: int) -> dict:
    """Run argv from the export root; return its exit code, merged output and timeout."""
    exe = program(argv[0], export)
    if exe is None:
        raise SpawnFailed(f"the test command did not start: {argv[0]} names no program "
                          f"and no file in the repository")
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    try:
        done = subprocess.run([exe, *argv[1:]], cwd=export, env=env,
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout,
                              creationflags=NO_WINDOW)
    except subprocess.TimeoutExpired as expired:
        return {"code": None, "timeout": True,
                "text": (expired.stdout or b"").decode("utf-8", "replace")}
    except OSError as err:
        raise SpawnFailed(f"the test command did not start: {argv[0]}: {clip(str(err))}") from err
    return {"code": done.returncode, "timeout": False,
            "text": done.stdout.decode("utf-8", "replace")}


def run_stage(plan: Plan, label: str) -> dict:
    """Run the build when one is declared, then the selected command, as `label`.

    Returns the stage's facts: built, log, summary, code, timeout, pytest,
    cases and crashed.
    """
    log, pytest = plan.logs / f"{label}.log", is_pytest(plan.selected)
    facts = {"built": True, "log": log, "summary": "", "code": None, "timeout": False,
             "pytest": pytest, "cases": [], "crashed": False}
    if plan.build:
        built = launch(plan.build, plan.export, plan.timeout)
        build_log = plan.logs / "build.log"
        build_log.write_text(built["text"], encoding="utf-8")
        if built["timeout"] or built["code"] != 0:
            reason = (f"timeout after {plan.timeout}s" if built["timeout"]
                      else f"exit {built['code']}")
            tail = last_line(built["text"])
            summary = f"build: {reason}: {tail}" if tail else f"build: {reason}"
            return {**facts, "built": False, "log": build_log, "summary": summary,
                    "code": built["code"], "timeout": built["timeout"]}
    argv, xml = list(plan.selected), plan.logs / f"{label}.xml"
    if pytest:
        xml.unlink(missing_ok=True)
        argv += ["--tb=short", f"--junitxml={xml}", "-p", "no:cacheprovider"]
    run = launch(argv, plan.export, plan.timeout)
    if run["timeout"]:
        log.write_text(run["text"] + f"\nTIMEOUT after {plan.timeout}s\n", encoding="utf-8")
        return {**facts, "timeout": True, "summary": f"timeout after {plan.timeout}s"}
    log.write_text(run["text"], encoding="utf-8")
    facts["code"] = run["code"]
    if pytest:
        line = last_line(run["text"]).strip("= ").strip()
        try:
            facts["cases"] = read_cases(xml) if xml.is_file() else []
        except ET.ParseError:
            facts["cases"] = []
        facts["crashed"] = not facts["cases"]
    else:
        line = last_line(run["text"])
    facts["summary"] = line or f"exit {run['code']}, no output"
    return facts


def passes(run: dict) -> bool:
    """True when the stage built, did not time out, and every test passed or the command exited 0."""
    if not run["built"] or run["timeout"]:
        return False
    if run["pytest"]:
        return bool(run["cases"]) and all(c["outcome"] == "passed" for c in run["cases"])
    return run["code"] == 0


def prove_red(plan: Plan, scratch: Path) -> dict:
    run = run_stage(plan, "red")
    out = {"summary": run["summary"], "red_ok": False, "log": rel(run["log"], scratch)}
    if run["built"] and not run["timeout"]:
        if run["pytest"]:
            cases = run["cases"]
            passed = [c["id"] for c in cases if c["outcome"] == "passed"]
            skipped = [c["id"] for c in cases if c["outcome"] == "skipped"]
            bad = [{"id": c["id"], "kind": c["kind"], "line": c["line"]}
                   for c in cases if c["outcome"] == "failed" and c["kind"] != "assertion"]
            out["red_ok"] = bool(cases) and not (passed or skipped or bad or run["crashed"])
            for key, value in (("passed", passed), ("skipped", skipped), ("not_assertion", bad)):
                if value:
                    out[key] = value
        else:
            out["red_ok"] = run["code"] == 1
    if run["timeout"]:
        out["timeout"] = True
    return out


def mutate(spec: dict, n: int, plan: Plan, scratch: Path) -> dict:
    """Apply one mutation to the export, run, restore; return its record."""
    result = {"name": spec["name"]}
    path = (plan.export / spec["file"]).resolve()
    if not path.is_relative_to(plan.export) or not path.is_file():
        return {**result, "applied": False, "error": f"{spec['file']} is not a file under the export"}
    original = path.read_bytes()
    text = original.decode("utf-8", "replace")
    matches = text.count(spec["old"])
    if matches != 1:
        return {**result, "applied": False, "error": f"old matches {matches} places, not 1"}
    try:
        path.write_bytes(text.replace(spec["old"], spec["new"], 1).encode("utf-8"))
        run = run_stage(plan, f"mutation-{n}")
    finally:
        path.write_bytes(original)
    if run["timeout"]:
        caught = ["(timeout)"]
    elif run["pytest"]:
        caught = [c["id"] for c in run["cases"] if c["outcome"] != "passed"]
        if not run["built"]:
            caught = ["(build)"]
    else:
        caught = [] if passes(run) else [plan.test]
    out = {**result, "applied": True,
           "caught_by": caught[:IDS_CAP] if caught else "not caught",
           "log": rel(run["log"], scratch)}
    if caught:
        out["caught_count"] = len(caught)
    return out


def load_mutations(path: str | None) -> list[dict] | None:
    if path is None:
        return None
    try:
        items = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        raise Usage(f"cannot read the mutations file {path}: {err}") from err
    ok = isinstance(items, list) and all(
        isinstance(i, dict) and all(isinstance(i.get(k), str) for k in ("name", "file", "old", "new"))
        and i["old"] for i in items)
    if not ok:
        raise Usage(f"{path} must be a JSON list of {{name, file, old, new}} with a non-empty old")
    return items


def rel(path: Path, scratch: Path) -> str:
    """`path` relative to the scratch folder, with forward slashes."""
    return path.relative_to(scratch).as_posix()


def export_commit(root: Path, sha: str, export: Path) -> None:
    """Recreate `export` from the commit, keeping executable bits."""
    shutil.rmtree(export, ignore_errors=True)
    export.mkdir(parents=True, exist_ok=True)
    done = git(root, "archive", "--format=tar", sha)
    if done.returncode != 0:
        raise Usage(f"git archive failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    with tarfile.open(fileobj=io.BytesIO(done.stdout)) as tar:
        tar.extractall(export, filter="data")


def run_all(args: argparse.Namespace) -> tuple[dict, bool]:
    root, scratch = Path.cwd().resolve(), Path(args.scratch).resolve()
    if not inside_repository(args.test):
        raise Usage(f"--test {args.test} is not a path inside the repository")
    if git(root, "rev-parse", "--git-dir").returncode != 0:
        raise Usage(f"{root} is not a git repository")
    declared = read_test(root)
    if declared is None:
        raise Usage("the repository declares no test command")
    sha = None
    if not args.at.startswith("-"):
        found = git(root, "rev-parse", "--verify", "--quiet", f"{args.at}^{{commit}}")
        sha = found.stdout.decode("utf-8", "replace").strip() if found.returncode == 0 else None
    if not sha:
        raise Usage(f"{args.at} is not a commit in {root}")
    draft = scratch / "draft" / args.test
    if not draft.is_file():
        kind = git(root, "cat-file", "-t", f"{sha}:{args.test}")
        if kind.returncode != 0 or kind.stdout.strip() != b"blob":
            raise Usage(f"no draft at {draft} and no {args.test} at {args.at}")
    specs = load_mutations(args.mutations)
    export, logs = scratch / "export", scratch / "logs"
    export_commit(root, sha, export)
    logs.mkdir(parents=True, exist_ok=True)
    if draft.is_file():
        (export / args.test).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(draft, export / args.test)
    selected = ([word.replace("{file}", args.test) for word in declared.file]
                if declared.file else list(declared.command))
    plan = Plan(export, logs, declared.build, selected, args.test, args.timeout)
    if specs is None:
        red = prove_red(plan, scratch)
        return {"ok": red["red_ok"], "scratch": str(scratch), "red": red}, red["red_ok"]
    if not passes(run_stage(plan, "baseline")):
        skipped = f"skipped: the tests do not pass at {args.at}"
        return {"ok": False, "scratch": str(scratch), "mutations": skipped}, False
    records = [mutate(spec, n, plan, scratch) for n, spec in enumerate(specs, 1)]
    holds = all(r["applied"] and r["caught_by"] != "not caught" for r in records)
    return {"ok": holds, "scratch": str(scratch), "mutations": records}, holds


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="prove.py", description="Prove a test file red or its mutations caught.")
    parser.add_argument("--scratch", required=True, help="the scratch folder")
    parser.add_argument("--test", required=True, help="the test file's path from the repository root")
    parser.add_argument("--at", default="HEAD", help="the git revision to export (default HEAD)")
    parser.add_argument("--mutations", help="JSON list of {name, file, old, new}")
    parser.add_argument("--timeout", type=int, default=600, help="seconds one command may take")
    args = parser.parse_args(argv)
    try:
        result, holds = run_all(args)
    except Usage as err:
        print(f"prove.py: {err}", file=sys.stderr)
        return 2
    except SpawnFailed as err:
        print(f"prove.py: {err}", file=sys.stderr)
        return SPAWN_FAILED
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=False))
    return 0 if holds else 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
