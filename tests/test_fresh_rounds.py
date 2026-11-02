"""Fresh-rounds suite (contract: run-restart, unit rs3-fresh-rounds, checks SC3.1, SC3.2
and SC3.3).

After a third FAIL a stop record stands. `task.py restart --unit C/U --go --fresh
--scratch DIR` does what `--go` does and also clears the failed rounds of the stopped
task's channel in the unit's rounds.json (write-tests and its peers approve-tests and
prove-red; green and its peers approve-commit, commit and two-key), so the next
`task.py start` of that task prints round 1 and the task stops again only at the third
FAIL of its three fresh rounds. The other channel's rounds stay. The flow `restart.md`
asks the second question after a third FAIL, reads `--enough`, passes `--fresh` only after
an enough ruling, and on a not-enough ruling shows its line, stops with no PR and runs no
`--go`. The flow is read as text.

`task.py` runs as a subprocess on a fixture repository under tmp_path (the way
tests/test_restart.py does); nothing is imported from it.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import taskcontract

ROOT = Path(taskcontract.__file__).resolve().parents[1]
TASK_PY = ROOT / "workflows" / "tools" / "task.py"
EXECUTE = ROOT / "skills" / "sdlc" / "flows" / "execute.md"
RESTART = ROOT / "skills" / "sdlc" / "flows" / "restart.md"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
CEILING = 12_000
EXECUTE_CHARS = 11_991

CONTRACT, U, U2 = "exec-fix", "u1-work", "u2-more"
UNIT, UNIT2 = f"{CONTRACT}/{U}", f"{CONTRACT}/{U2}"
BRANCH = "feat/exec-fix-u1-work"
INTENT = ("A fixture contract for the fresh-rounds suite, with a scope of its own and "
          "enough words to pass the door of the ready profile.")
STARTED = "Task {task}: {operator}, round {round}\n"
STOPPED = "Task {task} failed 3 rounds. The run stops here; the failures follow.\n"
WRONG_BRANCH = ("Execution did not restart: the run stopped on branch {branch}; "
                "this session is on {current}.\n")
AT = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
OLD = ["old one: 2 sketches failed: SC1.1 (a.py:4), SC1.2 (a.py:9)",
       "old two: 1 sketch failed: SC1.2 (a.py:9)",
       "old three: 1 sketch failed: SC1.2 (a.py:11)"]
NEW = ["new one: 3 sketches failed: SC3.1 (b.py:2), SC3.2 (b.py:5), SC3.3 (b.py:6)",
       "new two: 1 sketch failed: SC3.2 (b.py:7)",
       "new three: 1 sketch failed: SC3.2 (b.py:8)"]
DRAFT = {"test_file": "tests/test_cli.py", "interface": "parse_args(argv) -> Args",
         "tests": [{"name": "t1", "proves": "SC1.1", "intent": "pins parse_args"}],
         "red_proof": {"command": "prove", "summary": "red"}, "questions": []}
DRAFT_BYTES = b"def test_parse_args():\n    assert False\n"
KEPT_AT_GREEN = {"draft": DRAFT, "draft-file": "draft/test_cli.py"}
NONE = {"state": "none", "task": None, "operator": None, "round": None, "kind": None,
        "text": None, "kept": {}}

# Each channel: the task a FAIL returns to, its member, the verifier whose FAIL was the
# third, the other channel, and the peers that count their rounds under the channel.
CHANNELS = {
    "green": {"member": "developer", "printed": "Developer", "verifier": "dev-verifier",
              "other": "write-tests",
              "peers": [("two-key", "dev-verifier", "Dev verifier"),
                        ("approve-commit", "receipts", "receipts"),
                        ("commit", "orchestrator", "Orchestrator")]},
    "write-tests": {"member": "qa", "printed": "QA", "verifier": "qa-verifier",
                    "other": "green",
                    "peers": [("approve-tests", "qa-verifier", "QA verifier"),
                              ("prove-red", "qa-verifier", "QA verifier")]},
}
BOTH = pytest.mark.parametrize("channel", list(CHANNELS))


# --- the scratch repository ---------------------------------------------------------

def _dump(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _unit(uid: str) -> dict:
    return {"unit": "work for " + uid, "id": uid, "confirmed_by": ["po"],
            "done_means": "the work for " + uid + " is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}


def _document(revision: int) -> str:
    def row(text, by="Ann Lee"):
        return f"| 2026-10-07 | {by} | {text} |\n"
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{CONTRACT}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return (f"# {CONTRACT} - A fixture feature\n\n"
            "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"
            + rows + ready + "\n## Statement\n\nWords.\n")


def _roster(root: Path) -> None:
    vocab = root / "specs" / "vocabulary"
    vocab.mkdir(parents=True, exist_ok=True)
    (vocab / "intake-seat.yaml").write_text(yaml.safe_dump({
        "term": "intake-seat", "name": "Intake seat",
        "definition": "A human position that answers for a decomposition unit at intake.",
        "kind": "value-set", "values": ["po", "engineer"], "status": "ratified",
        "since": "2026-08-26"}, sort_keys=False), encoding="utf-8")


def git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                          encoding="utf-8", errors="replace", creationflags=NO_WINDOW)
    return done.stdout


def commit(root: Path, message: str = "seed") -> None:
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@example.com", "-c", "user.name=t",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=no-hooks",
        "commit", "-q", "--allow-empty", "-m", message)


def make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    (tmp_path / "cwd").mkdir()
    (root / ".sdlc").mkdir()
    (root / ".sdlc" / "config.yaml").write_text(
        "kit: fixture\ntest:\n  command: [test.bat]\n", encoding="utf-8")
    _dump(root / "specs" / CONTRACT / "contract.yaml", {
        "id": CONTRACT, "title": "A fixture feature", "intent": INTENT,
        "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
        "decomposition": [_unit(U), _unit(U2)], "dependencies": [], "entities": [],
        "provenance": {"origin": "human-request"}})
    (root / "docs" / "features").mkdir(parents=True)
    (root / "docs" / "features" / f"{CONTRACT}.md").write_text(_document(5), encoding="utf-8")
    (root / "docs" / "features" / f"{CONTRACT}.design.md").write_text(
        _document(4), encoding="utf-8")
    _roster(root)
    git(root, "init", "-q")
    git(root, "symbolic-ref", "HEAD", f"refs/heads/{BRANCH}")
    commit(root)
    return root


def call(tmp_path: Path, root: Path, *args: str):
    argv = [sys.executable, str(TASK_PY), *args, "--root", str(root)]
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path), "PYTHONUTF8": "1"}
    done = subprocess.run(argv, cwd=tmp_path / "cwd", env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=100,
                          creationflags=NO_WINDOW)
    return done.returncode, done.stdout, done.stderr


def start(tmp_path, root, task="green", operator="developer", unit=UNIT):
    return call(tmp_path, root, "start", "--unit", unit, "--task", task, "--operator", operator)


def end(tmp_path, root, task="green", by=None, unit=UNIT):
    extra = ["--by", by] if by else []
    return call(tmp_path, root, "end", "--unit", unit, "--task", task, *extra)


def fail(tmp_path, root, task="green", reason=None, unit=UNIT, operator=None):
    extra = ["--reason", reason] if reason is not None else []
    extra += ["--operator", operator] if operator else []
    return call(tmp_path, root, "fail", "--unit", unit, "--task", task, *extra)


def stop(tmp_path, root, question="Which exit code?", task="green", operator="developer",
         kind="question", unit=UNIT):
    return call(tmp_path, root, "stop", "--unit", unit, "--task", task, "--operator", operator,
                "--kind", kind, "--question", question)


def keep(tmp_path, root, key, value=None, file=None, unit=UNIT):
    extra = ["--value", value] if value is not None else ["--file", str(file)]
    return call(tmp_path, root, "keep", "--unit", unit, "--key", key, *extra)


def restart(tmp_path, root, *extra, unit=UNIT):
    return call(tmp_path, root, "restart", "--unit", unit, *extra)


def go_fresh(tmp_path, root, scratch=None, unit=UNIT):
    scratch = scratch or tmp_path / "fresh-session" / "scratch"
    return restart(tmp_path, root, "--go", "--fresh", "--scratch", str(scratch), unit=unit)


def run_dir(root: Path, unit: str = UNIT) -> Path:
    return root / ".git" / "sdlc-run" / unit


def task_file(root: Path) -> Path:
    return root / ".git" / "sdlc-task.json"


def load(path: Path):
    assert path.is_file(), f"{path} is not written"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        raise AssertionError(f"{path} does not hold JSON") from None


def run_json(root: Path, unit: str = UNIT) -> dict:
    return load(run_dir(root, unit) / "run.json")


def stop_json(root: Path, unit: str = UNIT) -> dict:
    return load(run_dir(root, unit) / "stop.json")


def rounds_of(root: Path, unit: str = UNIT) -> dict:
    """The failed reasons a task the rounds file holds; {} when the file is gone."""
    path = run_dir(root, unit) / "rounds.json"
    if not path.is_file():
        return {}
    doc = load(path)
    assert isinstance(doc, dict) and doc.get("unit", unit) == unit, doc
    return doc.get("rounds", {})


def records(root: Path) -> list[dict]:
    path = root / ".sdlc" / "progress" / f"{CONTRACT}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["records"] if path.is_file() else []


def snapshot(root: Path) -> dict:
    """Every path under the repository, git folder's sdlc-* entries included, with the bytes."""
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*")
            if ".git" not in p.relative_to(root).parts
            or (len(p.relative_to(root).parts) > 1
                and p.relative_to(root).parts[1].startswith("sdlc-"))}


def scratch_draft(tmp_path: Path) -> Path:
    path = tmp_path / "qa-scratch" / "draft" / "tests" / "test_cli.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(DRAFT_BYTES)
    return path


def passes_to_green(tmp_path: Path, root: Path, unit: str = UNIT) -> None:
    """QA's tasks pass and keep what they hand on; green is then in hand (task file standing)."""
    assert start(tmp_path, root, "write-tests", "qa", unit)[0] == 0
    assert keep(tmp_path, root, "draft", json.dumps(DRAFT), unit=unit) == (0, "", "")
    assert keep(tmp_path, root, "draft-file", file=scratch_draft(tmp_path), unit=unit) == (0, "", "")
    assert end(tmp_path, root, "write-tests", unit=unit) == (0, "", "")
    assert start(tmp_path, root, "approve-tests", "qa-verifier", unit)[0] == 0
    assert end(tmp_path, root, "approve-tests", "qa-verifier", unit) == (0, "", "")
    assert start(tmp_path, root, "prove-red", "qa-verifier", unit)[0] == 0
    assert end(tmp_path, root, "prove-red", unit=unit) == (0, "", "")
    assert start(tmp_path, root, "green", "developer", unit)[0] == 0


def third_fail(tmp_path, root, channel, reasons=OLD, other_reasons=(), unit=UNIT, draft=False):
    """The unit's `channel` task fails three rounds: a stop record of kind fail stands.
    `other_reasons` are failed rounds of the other channel, put in before."""
    spec = CHANNELS[channel]
    if draft:
        passes_to_green(tmp_path, root, unit)
    else:
        assert start(tmp_path, root, channel, spec["member"], unit)[0] == 0
    for reason in other_reasons:
        assert fail(tmp_path, root, spec["other"], reason, unit=unit) == (0, "", "")
    for reason in reasons[:2]:
        assert fail(tmp_path, root, channel, reason, unit=unit,
                    operator=spec["verifier"]) == (0, "", "")
    assert fail(tmp_path, root, channel, reasons[2], unit=unit, operator=spec["verifier"]) == (
        1, STOPPED.format(task=channel) + "".join(
            f"  Round {n}: {r}\n" for n, r in enumerate(reasons, 1)), "")
    assert stop_json(root, unit)["kind"] == "fail"
    assert not task_file(root).exists()


def started(channel: str, task: str, operator: str, printed: str, n: int):
    return (0, STARTED.format(task=task, operator=printed, round=n), "")


# --- SC3.1: --go --fresh restarts the task at round 1 --------------------------------

@BOTH
def test_sc3_1_go_fresh_after_a_third_fail_prints_the_stop_and_the_next_start_is_round_1(
        tmp_path, channel):
    spec = CHANNELS[channel]
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, channel)
    asked = restart(tmp_path, root)
    assert json.loads(asked[1])["kind"] == "fail" and json.loads(asked[1])["round"] == 3
    code, out, err = go_fresh(tmp_path, root)
    assert (code, err) == (0, ""), (code, out, err)
    assert out == asked[1], "--go --fresh prints the line the read-only restart printed"
    assert not (run_dir(root) / "stop.json").exists()
    assert start(tmp_path, root, channel, spec["member"]) == started(
        channel, channel, spec["member"], spec["printed"], 1)
    assert json.loads(task_file(root).read_text(encoding="utf-8")) == {
        "task": channel, "operator": spec["member"], "unit": UNIT, "round": 1}


@BOTH
def test_sc3_1_the_peers_of_the_channel_start_at_round_1_after_go_fresh(tmp_path, channel):
    spec = CHANNELS[channel]
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, channel)
    assert go_fresh(tmp_path, root)[0] == 0
    for peer, operator, printed in spec["peers"]:
        assert start(tmp_path, root, peer, operator) == started(
            channel, peer, operator, printed, 1), peer
        task_file(root).unlink()


@BOTH
def test_sc3_1_go_fresh_clears_the_failed_rounds_of_the_stopped_channel_only(tmp_path, channel):
    spec = CHANNELS[channel]
    other = spec["other"]
    other_spec = CHANNELS[other]
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, channel, other_reasons=["other a", "other b"])
    assert rounds_of(root)[channel] == OLD, "the third FAIL's rounds stand before the restart"
    assert go_fresh(tmp_path, root)[0] == 0
    assert rounds_of(root).get(channel, []) == []
    assert rounds_of(root)[other] == ["other a", "other b"], "the other channel stays as it was"
    assert start(tmp_path, root, other, other_spec["member"]) == started(
        other, other, other_spec["member"], other_spec["printed"], 3)
    task_file(root).unlink()
    assert start(tmp_path, root, channel, spec["member"]) == started(
        channel, channel, spec["member"], spec["printed"], 1)


def test_sc3_1_go_fresh_clears_the_rounds_of_the_stopped_unit_only(tmp_path):
    root = make_repo(tmp_path)
    for reason in ("u2 a", "u2 b"):
        assert fail(tmp_path, root, "green", reason, unit=UNIT2) == (0, "", "")
    third_fail(tmp_path, root, "green")
    assert go_fresh(tmp_path, root)[0] == 0
    assert rounds_of(root, UNIT2) == {"green": ["u2 a", "u2 b"]}
    assert start(tmp_path, root, "green", "developer", UNIT2) == started(
        "green", "green", "developer", "Developer", 3)
    task_file(root).unlink()
    assert start(tmp_path, root, "green", "developer", UNIT) == started(
        "green", "green", "developer", "Developer", 1)


def test_sc3_1_go_fresh_does_what_go_does_removes_the_stop_and_task_file_writes_the_draft(
        tmp_path):
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, "green", draft=True)
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert task_file(root).is_file(), "a task file is left standing"
    held_records = records(root)
    assert held_records, "the earlier tasks are recorded done"
    run_bytes = (run_dir(root) / "run.json").read_bytes()
    scratch = tmp_path / "fresh-session" / "scratch"
    code, out, err = go_fresh(tmp_path, root, scratch)
    assert (code, err) == (0, ""), (code, out, err)
    assert json.loads(out)["state"] == "stopped" and json.loads(out)["task"] == "green"
    assert not (run_dir(root) / "stop.json").exists()
    assert not task_file(root).exists()
    assert (scratch / "draft" / "tests" / "test_cli.py").read_bytes() == DRAFT_BYTES
    assert (run_dir(root) / "run.json").read_bytes() == run_bytes
    assert run_json(root)["kept"] == KEPT_AT_GREEN
    assert records(root) == held_records, "no earlier task runs again"
    assert rounds_of(root).get("green", []) == []
    assert start(tmp_path, root, "green", "developer") == started(
        "green", "green", "developer", "Developer", 1)


@pytest.mark.parametrize("kind", ["question", "error", "refusal"])
def test_sc3_1_go_fresh_clears_the_channel_whatever_the_kind_of_the_stop(tmp_path, kind):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert fail(tmp_path, root, "write-tests", "w one") == (0, "", "")
    for reason in OLD[:2]:
        assert fail(tmp_path, root, "green", reason) == (0, "", "")
    assert start(tmp_path, root, "green", "developer") == started(
        "green", "green", "developer", "Developer", 3)
    assert stop(tmp_path, root, "Which header?", "green", "developer", kind)[0] == 1
    assert stop_json(root)["kind"] == kind
    code, out, err = go_fresh(tmp_path, root)
    assert (code, err) == (0, ""), (code, out, err)
    assert json.loads(out)["kind"] == kind
    assert not (run_dir(root) / "stop.json").exists()
    assert start(tmp_path, root, "green", "developer") == started(
        "green", "green", "developer", "Developer", 1)
    task_file(root).unlink()
    assert start(tmp_path, root, "write-tests", "qa") == started(
        "write-tests", "write-tests", "qa", "QA", 2)


def test_sc3_1_go_fresh_with_no_failed_round_on_file_starts_the_task_at_round_1(tmp_path):
    root = make_repo(tmp_path)
    assert start(tmp_path, root, "write-tests", "qa")[0] == 0
    assert stop(tmp_path, root, "Which flag?", "write-tests", "qa", "question")[0] == 1
    assert not (run_dir(root) / "rounds.json").exists()
    code, out, err = go_fresh(tmp_path, root)
    assert (code, err) == (0, ""), (code, out, err)
    assert json.loads(out)["task"] == "write-tests"
    assert not (run_dir(root) / "stop.json").exists()
    assert start(tmp_path, root, "write-tests", "qa") == started(
        "write-tests", "write-tests", "qa", "QA", 1)


def test_sc3_1_go_fresh_on_another_branch_starts_nothing_and_clears_nothing(tmp_path):
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, "green")
    git(root, "checkout", "-q", "-b", "elsewhere")
    before = snapshot(root)
    scratch = tmp_path / "fresh-session" / "scratch"
    code, out, err = go_fresh(tmp_path, root, scratch)
    assert (code, out) == (1, ""), (code, out, err)
    assert err == WRONG_BRANCH.format(branch=BRANCH, current="elsewhere")
    assert snapshot(root) == before
    assert not scratch.exists()


def test_sc3_1_go_fresh_on_a_unit_with_no_run_folder_starts_nothing_and_writes_nothing(tmp_path):
    root = make_repo(tmp_path)
    before = snapshot(root)
    scratch = tmp_path / "fresh-session" / "scratch"
    code, out, err = go_fresh(tmp_path, root, scratch)
    assert (code, err) == (0, ""), (code, out, err)
    assert json.loads(out) == NONE
    assert snapshot(root) == before
    assert not scratch.exists() and not (root / ".git" / "sdlc-run").exists()


# --- SC3.2: the task stops again only at the third FAIL of its fresh rounds ---------------

@BOTH
def test_sc3_2_two_fresh_fails_stop_nothing_and_the_third_stops_with_the_fresh_reasons_only(
        tmp_path, channel):
    spec = CHANNELS[channel]
    other = spec["other"]
    member, printed, verifier = spec["member"], spec["printed"], spec["verifier"]
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, channel, other_reasons=["other a"])
    assert go_fresh(tmp_path, root)[0] == 0
    # The first fresh round fails: silent, exit 0, no stop record, the next start is round 2.
    assert start(tmp_path, root, channel, member) == started(
        channel, channel, member, printed, 1)
    assert fail(tmp_path, root, channel, NEW[0], operator=verifier) == (0, "", "")
    assert not (run_dir(root) / "stop.json").exists()
    assert not task_file(root).exists()
    assert start(tmp_path, root, channel, member) == started(
        channel, channel, member, printed, 2)
    # The second fresh round fails: still no stop, the next start is round 3.
    assert fail(tmp_path, root, channel, NEW[1], operator=verifier) == (0, "", "")
    assert not (run_dir(root) / "stop.json").exists()
    assert start(tmp_path, root, channel, member) == started(
        channel, channel, member, printed, 3)
    # The third fresh round fails: the run stops, with the three fresh reasons and no old one.
    code, out, err = fail(tmp_path, root, channel, NEW[2], operator=verifier)
    assert (code, err) == (1, "")
    assert out == STOPPED.format(task=channel) + "".join(
        f"  Round {n}: {r}\n" for n, r in enumerate(NEW, 1))
    got = stop_json(root)
    assert AT.match(got.pop("at"))
    assert got == {"unit": UNIT, "task": channel, "operator": verifier, "kind": "fail",
                   "round": 3, "failed": {channel: 3, other: 1}, "reasons": NEW}
    assert rounds_of(root)[channel] == NEW
    assert rounds_of(root)[other] == ["other a"]
    assert not task_file(root).exists()


def test_sc3_2_after_the_second_stop_the_restart_reads_the_fresh_reasons(tmp_path):
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, "green")
    assert go_fresh(tmp_path, root)[0] == 0
    for reason in NEW[:2]:
        assert start(tmp_path, root, "green", "developer")[0] == 0
        assert fail(tmp_path, root, "green", reason, operator="dev-verifier") == (0, "", "")
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert fail(tmp_path, root, "green", NEW[2], operator="dev-verifier")[0] == 1
    code, out, err = restart(tmp_path, root)
    assert (code, err) == (0, "")
    got = json.loads(out)
    assert (got["state"], got["task"], got["operator"], got["round"], got["kind"]) == (
        "stopped", "green", "dev-verifier", 3, "fail")
    assert got["text"] == "; ".join(NEW)


def test_sc3_2_a_second_enough_ruling_gives_a_third_set_of_fresh_rounds(tmp_path):
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, "green")
    assert go_fresh(tmp_path, root)[0] == 0
    for reason in NEW[:2]:
        assert start(tmp_path, root, "green", "developer")[0] == 0
        assert fail(tmp_path, root, "green", reason, operator="dev-verifier") == (0, "", "")
    assert start(tmp_path, root, "green", "developer")[0] == 0
    assert fail(tmp_path, root, "green", NEW[2], operator="dev-verifier")[0] == 1
    assert go_fresh(tmp_path, root)[0] == 0
    assert start(tmp_path, root, "green", "developer") == started(
        "green", "green", "developer", "Developer", 1)


# --- SC3.3 and the usage errors: --fresh needs --go ------------------------------------

def test_sc3_3_a_not_enough_ruling_runs_no_go_so_the_stop_and_the_rounds_stay(tmp_path):
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, "green")
    before = snapshot(root)
    for _ in range(2):
        code, out, err = restart(tmp_path, root)
        assert (code, err) == (0, "")
        assert json.loads(out)["state"] == "stopped"
    assert snapshot(root) == before, "restart without --go stays read-only"
    # --fresh does nothing by itself: it is refused without --go, and nothing changes.
    code, out, err = restart(tmp_path, root, "--fresh")
    assert code == 2 and out == "" and "--fresh requires --go" in err, (code, out, err)
    assert snapshot(root) == before
    assert stop_json(root)["kind"] == "fail"
    assert rounds_of(root)["green"] == OLD
    assert start(tmp_path, root, "green", "developer") == started(
        "green", "green", "developer", "Developer", 4)


@pytest.mark.parametrize("extra", [[], ["--scratch", "SCRATCH"]],
                         ids=["fresh-alone", "fresh-with-scratch"])
def test_r5_fresh_without_go_is_a_usage_error_and_changes_nothing(tmp_path, extra):
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, "green", draft=True)
    scratch = tmp_path / "scratch"
    argv = [str(scratch) if a == "SCRATCH" else a for a in extra]
    before = snapshot(root)
    code, out, err = restart(tmp_path, root, "--fresh", *argv)
    assert code == 2 and out == "", (code, out, err)
    assert "usage:" in err and "--fresh requires --go" in err, err
    assert snapshot(root) == before
    assert not scratch.exists()
    assert rounds_of(root)["green"] == OLD and (run_dir(root) / "stop.json").is_file()


def test_r5_go_fresh_without_a_scratch_folder_is_a_usage_error_and_changes_nothing(tmp_path):
    root = make_repo(tmp_path)
    third_fail(tmp_path, root, "green")
    before = snapshot(root)
    code, out, err = restart(tmp_path, root, "--go", "--fresh")
    assert code == 2 and out == "", (code, out, err)
    assert "usage:" in err and "--go requires --scratch" in err, err
    assert snapshot(root) == before
    assert rounds_of(root)["green"] == OLD and (run_dir(root) / "stop.json").is_file()


# --- the flow: restart.md -----------------------------------------------------------------

TASKPY = "python {skill-dir}/../../workflows/tools/task.py"
RESTART_CMD = f"{TASKPY} restart --unit {{contract}}/{{unit}}"
FRESH_GO = f"{RESTART_CMD} --go --fresh --scratch {{scratch}}"
PLAIN_GO = f"{RESTART_CMD} --go --scratch {{scratch}}"
ENOUGH_Q = "Is that answer enough to give {task} three fresh rounds?"
NOT_ENOUGH = ("Execution did not restart: {contract} unit {unit} stays stopped at {task}. "
              "The design may need revisiting.")
QUESTION_LINE = re.compile(
    r"Execution stopped: \{contract\} unit \{unit\}, task \{task\}, round \{\w+\} of 3: "
    r"\{\w+\}\. Your answer\?")


def read(path: Path) -> str:
    assert path.is_file(), f"{path.relative_to(ROOT).as_posix()} is not written"
    return path.read_text(encoding="utf-8")


def spans(text: str) -> list[tuple[int, str]]:
    return [(m.start(), m[1]) for m in re.finditer(r"`([^`\n]+)`", text)
            if m[1].startswith(("python ", "git ", "rm ", "gh "))]


def around(text: str, needle: str, before: int = 400, after: int = 400) -> str:
    at = text.index(needle)
    return text[max(0, at - before):at + len(needle) + after]


def test_sc3_1_restart_md_asks_the_second_question_verbatim_after_the_answer_for_a_fail_only():
    text = read(RESTART)
    assert text.count(ENOUGH_Q) == 1, "the second question stands once, verbatim"
    shown = QUESTION_LINE.search(text)
    assert shown, "the first question stays in restart.md"
    assert shown.end() < text.index(ENOUGH_Q), "the second question follows the answer"
    window = around(text, ENOUGH_Q)
    assert "`fail`" in window and "kind" in window, "only a stop of kind fail asks it"


def test_sc3_1_restart_md_reads_enough_from_the_invocation_and_a_headless_session_ends_its_turn():
    text = read(RESTART)
    assert "--enough" in text, "restart.md reads no --enough"
    window = around(text, ENOUGH_Q, 600, 600)
    assert re.search(r"interactive session asks[^\n]*chat", window), \
        "an interactive session asks in chat"
    assert re.search(r"headless session with no `?--enough`? ends its turn at that question",
                     window), "a headless session with no --enough ends its turn at the question"
    assert "starting nothing" in window and "stop record stays" in window
    assert re.search(r"`?--enough`? answers yes", window), "--enough answers yes"
    assert "--answer" in text


def test_sc3_1_restart_md_leaves_enough_unused_on_a_stop_of_another_kind():
    text = read(RESTART)
    assert re.search(r"`--enough` on a stop of another kind is unused", text), \
        "--enough on a stop of another kind is unused"


def test_sc3_1_restart_md_runs_go_fresh_only_after_the_enough_question_and_one_bash_call():
    text = read(RESTART)
    found = [c for at, c in spans(text) if c.startswith(RESTART_CMD)]
    assert FRESH_GO in found, found
    assert PLAIN_GO in found, "the other kinds still restart by --go alone"
    assert [c for c in found if "--fresh" in c] == [FRESH_GO]
    assert ENOUGH_Q in text and text.index(ENOUGH_Q) < text.index(FRESH_GO), \
        "--fresh runs only after the enough ruling"
    at = text.index(FRESH_GO)
    assert "one Bash call" in text[at + len(FRESH_GO):at + len(FRESH_GO) + 40]
    assert re.search(r"yes", text[text.index(ENOUGH_Q):at]), "the yes ruling leads to --fresh"
    assert re.search(r"HOLD \{reasons\} as `\[\]`", text[at:]), \
        "the member's reasons start at [] after --fresh (round 1)"


def test_sc3_3_restart_md_shows_the_not_enough_line_stops_with_no_pr_and_runs_no_go():
    text = read(RESTART)
    assert text.count(NOT_ENOUGH) == 1, "the not-enough line stands once, verbatim"
    assert ENOUGH_Q in text and text.index(ENOUGH_Q) < text.index(NOT_ENOUGH)
    block = next(b for b in text.split("\n\n") if NOT_ENOUGH in b)
    assert "SHOW" in block and "STOP" in block and "no PR" in block, block
    assert re.search(r"[Nn]o `?--go`? runs", block), "a not-enough ruling runs no --go"
    assert "stop record stays" in block
    assert "task.py" not in block, "the not-enough path runs no task.py command"


def test_sc3_1_restart_md_gives_the_answer_to_the_channels_member_not_the_verifier():
    text = read(RESTART)
    lines = [ln for ln in text.splitlines()
             if "`fail`" in ln and "member" in ln and "{task}" in ln]
    assert any("QA" in ln and "Developer" in ln and "{operator}" in ln
               and "`write-tests`" in ln and "`green`" in ln for ln in lines), lines


def test_sc3_1_restart_md_reads_the_task_not_the_operator_for_a_task_with_no_member():
    text = read(RESTART)
    lines = [ln for ln in text.splitlines() if "has no member" in ln]
    assert len(lines) == 1, lines
    line = lines[0]
    assert "{task}" in line and "`approve-commit`" in line and "`commit`" in line, line
    assert "{operator}" not in line, "the stop's operator is the verifier after a third FAIL"
    assert "SHOW" in line and "answer" in line


def test_sc3_1_restart_md_no_longer_holds_a_stop_of_kind_fail_until_rs3():
    text = read(RESTART)
    assert "until rs3" not in text
    assert ENOUGH_Q in text, "the fail path goes on to the enough question"
    assert "until rs4" in text, "an abandoned run still waits for rs4"


def test_sc3_1_restart_md_stays_under_the_ceiling_with_the_fresh_steps_and_execute_md_is_unchanged():
    text = read(RESTART)
    assert ENOUGH_Q in text and "--fresh" in text
    assert len(text) < CEILING, len(text)
    execute = read(EXECUTE)
    assert len(execute) == EXECUTE_CHARS, len(execute)
    assert "--fresh" not in execute and "--enough" not in execute
