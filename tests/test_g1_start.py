"""The refusal before G1 passes (contract: g1-requirements-spec, unit
s5-start, check SC4.2 and the second clause of its done_means).

`taskcontract progress start <task>` and `progress done <task | unit |
contract>` refuse while G1 is an active gate for the feature and its G1
verdict does not read `done`: one line on stderr,
`{unit} cannot start: G1 has not passed for {feature}`, exit 2, and nothing
written. `progress block` and `progress run` stay open.

A temporary repository per test, built by hand, in the idiom of
tests/test_g1_tree.py: `apply-discount` under specs/ with two units, its
pair under docs/features/ (a requirements document whose newest `Ready:`
row names r5 and a design document whose row names r4), a ratified
`intake-seat` term and a .sdlc/config.yaml each test writes. Every record
under .sdlc/g1/ is written by hand, so no test starts a linter or a checker.

Each test reads the tree's own print beside the call: a call is refused
exactly where the tree prints `<feature>/G1` with no `inactive` mark and a
status other than `done`. A test whose last word is that a call goes
through first proves, on the same repository, that the refusal stands.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

from conftest import write_seat_roster
from taskcontract import tree
from taskcontract.__main__ import main

ID = "apply-discount"
U = "u1-rate"
UNIT = f"{ID}/{U}"
TASK = f"{UNIT}/write-tests"
APPROVAL = f"{UNIT}/approve-tests"
CHECK = f"{UNIT}/SC1.1"
OTHER = "refund-order"
OTHER_U = "r1-refund"
SAME = "price-list"      # a feature whose one unit has the feature's id
IDEA = "new-idea"        # a feature before intake
CONFIG = ".sdlc/config.yaml"
COMPONENTS = "specs/components.yaml"
PROGRESS = ".sdlc/progress"
TO_DO, DOING, DONE, FAILED = "to do", "doing", "done", "failed"
ALONE = "review alone"   # a signed review and no declaration: G1 reads doing

# A state of the fixture, and the status the tree prints for G1 in it.
SHORT_OF_DONE = [(TO_DO, TO_DO), (DOING, DOING), (ALONE, DOING), (FAILED, FAILED)]

# G1.3's 11 items as its page ratified them (docs/gates/G1-requirements-spec.md).
NAMES = ["Testable", "Unambiguous", "Traceable", "Complete over units",
         "Covers the sketch", "Consistent", "Respects non-goals",
         "Boundary + error paths", "Property-spec applicability",
         "Schema presence", "Oracle designation answered"]

INTENT = ("A contract with a scope of its own, enough words to pass the door "
          "as a fixture for the suite of the refusal before G1.")
TITLE = "# {id} - A fixture feature\n\n"
HEAD = "| Date | Revised By | Changes |\n| :-- | :-- | :-- |\n"

ITEM = re.compile(r"^(?P<indent>(?:  )*)(?P<id>\S+)(?: (?P<name>.*?))? \[(?P<tag>[^\]]*)\]"
                  r"(?P<rest>.*)$")
PROBLEM = "taskcontract tree: "

# The refusal, verbatim (message 4 of the requirements).
MESSAGE = "{unit} cannot start: G1 has not passed for {feature}\n"

# The older lines of `taskcontract progress`, as tests/test_progress.py pins them.
UNKNOWN = "no node '{id}' - print the tree to list every node id\n"
NOT_A_TASK = ("taskcontract progress: '{id}' is a {kind}, not a task - "
              "{action} takes a task id\n")
NOT_CLOSABLE = ("taskcontract progress: '{id}' is a {kind}, not a task, unit or contract - "
                "done takes a task, unit or contract id\n")
NEEDS_REASON = ("taskcontract progress: block needs --reason <text> - "
                "say why '{id}' is blocked\n")
UNREADABLE = r"taskcontract progress: unreadable progress: \.sdlc/progress/{id}\.yaml \(.+\)\n"
REASON = "G1 has not passed"

PY = [sys.executable, "-S"]  # no site import: a faster start
GREEN = [*PY, "-c", "raise SystemExit(0)"]


def calls(feature: str = ID, unit: str = U, seat: str = "po"):
    """Each kind of call the refusal covers, with the id its line opens on
    and the stdout line it prints when it goes through."""
    base = f"{feature}/{unit}"
    task, approval = f"{base}/write-tests", f"{base}/approve-tests"
    return [
        (("start", task), unit, f"{task}: doing\n"),
        (("start", approval), unit, f"{approval}: doing\n"),
        (("done", task), unit, f"{task}: done\n"),
        (("done", approval, "--by", seat), unit, f"{approval}: done by {seat}\n"),
        (("done", base), unit, f"{base}: done\n"),
        (("done", feature), feature, f"{feature}: done\n"),
    ]


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, and find no git repository
    above the fixture."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.setenv("COLUMNS", "500")


# --- the fixture repository -------------------------------------------------------

def row(text: str, by: str = "Ann Lee") -> str:
    return f"| 2026-10-07 | {by} | {text} |\n"


def document(revision: int, feature: str) -> str:
    """A feature document with text rows r1 to r<revision>, then the
    `Ready:` row that names r<revision> as the one the contract is derived
    from."""
    rows = "".join(row(f"r{n}: the text at r{n}") for n in range(1, revision + 1))
    ready = row(f"r{revision + 1}: Ready: contract `{feature}` validates ready-green, "
                f"derived from r{revision}", by="intake")
    return TITLE.format(id=feature) + HEAD + rows + ready + "\n## Statement\n\nWords.\n"


def review(unchecked: dict | None = None) -> dict:
    """A G1.3 record as `g1-record review` writes it for a fixture pair."""
    unchecked = unchecked or {}
    held = []
    for n, name in enumerate(NAMES, start=1):
        entry = {"n": n, "name": name, "checked": n not in unchecked}
        if n in unchecked:
            entry["section"] = unchecked[n]
        held.append(entry)
    return {"condition": "G1.3", "at": "2026-10-07T14:20:40Z", "head": "8635064",
            "by": "Ann Lee", "seat": "po", "requirements": "r5", "design": "r4",
            "items": held}


def unit(uid: str) -> dict:
    return {"unit": "work for " + uid, "id": uid, "confirmed_by": ["po"],
            "done_means": "the work for " + uid + " is done",
            "acceptance_sketch": ["verify the work holds (SC1.1)"]}


class Repo:
    """One fixture repository at <tmp>/repo; never the working directory."""

    def __init__(self, tmp: Path):
        self.tmp = tmp
        self.root = tmp / "repo"
        self.root.mkdir()
        write_seat_roster(self.root, values=("po", "engineer"))
        self.feature(ID, U, "u2-cap")
        self.config()

    def write(self, rel: str, text) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def dump(self, rel: str, doc) -> Path:
        return self.write(rel, yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

    def remove(self, rel: str) -> None:
        path = self.root / rel
        if path.is_file():
            path.unlink()

    def feature(self, cid: str, *units: str) -> None:
        """A contract that reads ready-green, with its pair at r5 and r4."""
        self.dump(f"specs/{cid}/contract.yaml", {
            "id": cid, "title": "A fixture feature", "intent": INTENT,
            "scope": ["api/", "src/"], "non_goals": ["nothing beyond the scope"],
            "decomposition": [unit(uid) for uid in units], "dependencies": [],
            "entities": [], "provenance": {"origin": "human-request"}})
        self.write(f"docs/features/{cid}.md", document(5, cid))
        self.write(f"docs/features/{cid}.design.md", document(4, cid))

    def idea(self, fid: str = IDEA) -> None:
        """A feature before intake: a requirements document and no contract."""
        self.write(f"docs/features/{fid}.md", TITLE.format(id=fid) + HEAD
                   + row("r1: the first text") + "\n## Statement\n\nWords.\n")

    def config(self, active=("G0", "G1"), **g1_keys) -> None:
        """.sdlc/config.yaml as a person writes it: the `g1` key holds the
        given keys as given, and is left out when none is given."""
        doc = {"kit": "fixture", "active_gates": list(active)}
        if g1_keys:
            doc["g1"] = g1_keys
        self.dump(CONFIG, doc)

    def records(self, *records: dict, cid: str = ID) -> None:
        self.dump(f".sdlc/g1/{cid}.yaml", {"records": list(records)})

    def put(self, state: str, *features: str, active=("G0", "G1"), **g1_keys) -> None:
        """Put each named feature (`apply-discount` when none is named)
        where its G1 reads the state. The two declarations stand for the
        whole repository: with them G1.1 and G1.2 read done for a scope
        that holds no schema and no hard core, and without them each reads
        `to do`. G1.3 reads done by a review that checks all 11 items on r5
        and r4, failed by one that leaves item 6 unchecked, `to do` by none."""
        declared = state in (DOING, FAILED, DONE)
        if declared:
            g1_keys.setdefault("schemas", [])
        self.config(active, **g1_keys)
        if declared:
            self.dump(COMPONENTS, {"version": 1, "components": []})
        else:
            self.remove(COMPONENTS)
        for cid in features or (ID,):
            if state in (TO_DO, DOING):
                self.remove(f".sdlc/g1/{cid}.yaml")
            else:
                self.records(review({6: "Statement"} if state == FAILED else None), cid=cid)

    def hand(self, *records: dict, cid: str = ID) -> Path:
        """Seed the feature's progress file by hand."""
        return self.dump(f"{PROGRESS}/{cid}.yaml", {"records": list(records)})

    def progress(self, cid: str = ID) -> list[dict]:
        return yaml.safe_load((self.root / PROGRESS / f"{cid}.yaml")
                              .read_text(encoding="utf-8"))["records"]

    def snapshot(self) -> dict:
        """Every path under the temporary folder, with each file's bytes."""
        return {path.relative_to(self.tmp).as_posix(): None if path.is_dir()
                else path.read_bytes() for path in self.tmp.rglob("*")}


@pytest.fixture
def repo(tmp_path) -> Repo:
    return Repo(tmp_path)


# --- driving the CLI and reading the tree ------------------------------------------

def cli(capsys, *argv):
    capsys.readouterr()
    try:
        code = main([str(arg) for arg in argv])
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def mark(repo: Repo, capsys, action: str, rid: str, *options):
    """(exit code, stdout, stderr) of one `progress start|done|block`."""
    return cli(capsys, "progress", action, rid, "--root", repo.root, *options)


def show(repo: Repo, capsys) -> tuple[dict[str, tuple[str, str]], list[str]]:
    """One tree print: each item's (status, rest of its line) by id, and
    the problem lines."""
    code, out, err = cli(capsys, "tree", "--root", repo.root)
    assert code == 0, err
    rows = {}
    for text in out.splitlines():
        item = ITEM.match(text)
        if item:
            rows[item["id"]] = (item["tag"], item["rest"])
    return rows, err.splitlines()


def g1(repo: Repo, capsys, fid: str = ID) -> str | None:
    """What the tree prints for the feature's G1: its status where the
    verdict stands active, `inactive` where it carries the mark, None where
    no such line prints."""
    rows, _ = show(repo, capsys)
    if f"{fid}/G1" not in rows:
        return None
    tag, rest = rows[f"{fid}/G1"]
    return "inactive" if "inactive" in rest.split() else tag


def tree_refuses(repo: Repo, capsys, fid: str = ID) -> bool:
    """Reading 1: the tree prints `<feature>/G1` active and not `[done]`."""
    return g1(repo, capsys, fid) not in (None, "inactive", DONE)


def refused(repo: Repo, capsys, feature: str = ID, unit: str = U) -> None:
    """Each kind of call is refused with its line, and nothing is written."""
    assert tree_refuses(repo, capsys, feature)
    before = repo.snapshot()
    for call, opens, _ in calls(feature, unit):
        assert mark(repo, capsys, *call) == (
            2, "", MESSAGE.format(unit=opens, feature=feature)), call
    assert repo.snapshot() == before


def through(repo: Repo, capsys, feature: str = ID, unit: str = U) -> None:
    """Each kind of call goes through as it does with no G1: its stdout
    line, exit 0, and one record with the older keys."""
    assert not tree_refuses(repo, capsys, feature)
    held = len(repo.progress(feature)) if (
        repo.root / PROGRESS / f"{feature}.yaml").is_file() else 0
    for call, _, line in calls(feature, unit):
        assert mark(repo, capsys, *call) == (0, line, ""), call
    records = repo.progress(feature)[held:]
    assert [(r["item"], r["state"]) for r in records] == [
        (call[1], "doing" if call[0] == "start" else "done")
        for call, _, _ in calls(feature, unit)]
    base = {"item", "state", "head", "at"}  # outside git: no `dirty`
    assert [set(r) for r in records] == [base, base, base, base | {"by"}, base, base]
    assert records[3]["by"] == "po"
    assert {r["head"] for r in records} == {"no commit"}


# --- SC4.2: the two lines of the design, verbatim ------------------------------------

def test_sc4_2_the_designs_two_refusals_print_verbatim_on_stderr_and_exit_2(repo, capsys):
    assert g1(repo, capsys) == TO_DO
    assert mark(repo, capsys, "start", f"{ID}/u1-rate/approve-tests") == (
        2, "", "u1-rate cannot start: G1 has not passed for apply-discount\n")
    assert mark(repo, capsys, "done", ID) == (
        2, "", "apply-discount cannot start: G1 has not passed for apply-discount\n")


def test_sc4_2_reading_3_a_task_and_its_unit_print_the_units_own_id_never_the_tree_id(
        repo, capsys):
    line = "u2-cap cannot start: G1 has not passed for apply-discount\n"
    for call in (("start", f"{ID}/u2-cap/green"), ("done", f"{ID}/u2-cap/green"),
                 ("done", f"{ID}/u2-cap")):
        assert mark(repo, capsys, *call) == (2, "", line), call


def test_sc4_2_reading_4_a_refused_done_prints_cannot_start_too(repo, capsys):
    for call in (("done", TASK), ("done", APPROVAL, "--by", "po"), ("done", UNIT)):
        code, out, err = mark(repo, capsys, *call)
        assert (code, out) == (2, ""), call
        assert err == f"{U} cannot start: G1 has not passed for {ID}\n", call


# --- SC4.2: each state short of done, each kind of call -----------------------------

@pytest.mark.parametrize("state, status", SHORT_OF_DONE,
                         ids=[state.replace(" ", "-") for state, _ in SHORT_OF_DONE])
def test_sc4_2_each_kind_of_call_is_refused_while_g1_reads_short_of_done(
        repo, capsys, state, status):
    repo.put(state)
    assert g1(repo, capsys) == status
    refused(repo, capsys)


def test_sc4_2_ruling_3_a_refusal_makes_no_progress_folder_and_no_file(repo, capsys):
    refused(repo, capsys)
    assert not (repo.root / PROGRESS).exists()
    assert sorted(path.name for path in (repo.root / ".sdlc").iterdir()) == ["config.yaml"]


def test_sc4_2_ruling_3_a_refusal_appends_no_record_to_a_file_that_stands(repo, capsys):
    path = repo.hand({"item": TASK, "state": "blocked", "reason": REASON,
                      "at": "2026-10-12T09:00:00Z", "head": "1a2b3c4", "note": "kept"})
    held = path.read_bytes()
    refused(repo, capsys)
    assert path.read_bytes() == held
    assert sorted(p.name for p in (repo.root / PROGRESS).iterdir()) == [f"{ID}.yaml"]


# --- SC4.2: the order of the checks (reading 2) --------------------------------------

def test_sc4_2_reading_2_the_g1_line_wins_over_each_check_of_by(repo, capsys):
    before = repo.snapshot()
    line = MESSAGE.format(unit=U, feature=ID)
    # an approval's done with no seat, an empty one and a blank one
    for options in ((), ("--by", ""), ("--by", "   ")):
        assert mark(repo, capsys, "done", APPROVAL, *options) == (2, "", line), options
    # a done that may take no --by: a plain task, a unit, a contract
    assert mark(repo, capsys, "done", TASK, "--by", "po") == (2, "", line)
    assert mark(repo, capsys, "done", UNIT, "--by", "po") == (2, "", line)
    assert mark(repo, capsys, "done", ID, "--by", "po") == (
        2, "", MESSAGE.format(unit=ID, feature=ID))
    assert repo.snapshot() == before


def test_sc4_2_reading_2_the_unknown_id_and_the_wrong_kind_lines_win_over_the_g1_line(
        repo, capsys):
    repo.idea()
    refused(repo, capsys)  # the refusal stands on this repository
    before = repo.snapshot()
    for rid in (f"{UNIT}/review", f"{ID}/u9-none/approve-tests", "nowhere"):
        for call in (("start",), ("done",), ("done", "--by", "po")):
            assert mark(repo, capsys, call[0], rid, *call[1:]) == (
                2, "", UNKNOWN.format(id=rid)), (call, rid)
    not_tasks = ((CHECK, "check"), (UNIT, "unit"), (ID, "contract"), (f"{ID}/G1", "verdict"),
                 (f"{ID}/G1/G1.3", "condition"), ("gates/G1", "gate"), (IDEA, "feature"))
    for rid, kind in not_tasks:
        assert mark(repo, capsys, "start", rid) == (
            2, "", NOT_A_TASK.format(id=rid, kind=kind, action="start")), rid
        if kind not in ("unit", "contract"):
            assert mark(repo, capsys, "done", rid) == (
                2, "", NOT_CLOSABLE.format(id=rid, kind=kind)), rid
    assert repo.snapshot() == before


def test_sc4_2_the_g1_line_wins_over_a_progress_file_that_cannot_be_read(repo, capsys):
    path = repo.write(f"{PROGRESS}/{ID}.yaml", "records: [unclosed\n")
    # the tree drops the file with one line and still reads G1 `to do`
    rows, problems = show(repo, capsys)
    assert rows[f"{ID}/G1"][0] == TO_DO
    assert len(problems) == 1 and problems[0].startswith(f"{PROBLEM}unreadable progress: ")
    refused(repo, capsys)
    assert path.read_bytes() == b"records: [unclosed\n"
    # `block` stays open, so it meets the file as it does with no G1
    code, out, err = mark(repo, capsys, "block", TASK, "--reason", REASON)
    assert (code, out) == (2, "") and re.fullmatch(UNREADABLE.format(id=ID), err), err


# --- SC4.2: block and run stay open (ruling 4) ---------------------------------------

def test_sc4_2_ruling_4_block_and_run_stay_open_while_g1_has_not_passed(repo, capsys):
    refused(repo, capsys)
    assert mark(repo, capsys, "block", TASK, "--reason", REASON) == (
        0, f"{TASK}: blocked\n", "")
    assert mark(repo, capsys, "block", APPROVAL, "--reason", REASON) == (
        0, f"{APPROVAL}: blocked\n", "")
    assert mark(repo, capsys, "block", TASK) == (2, "", NEEDS_REASON.format(id=TASK))
    code, out, err = cli(capsys, "progress", "run", CHECK, "--root", repo.root, "--", *GREEN)
    assert (code, out, err) == (0, f"{CHECK}: green, expected green\n", "")
    records = repo.progress()
    assert [(r["item"], r.get("state"), r.get("run")) for r in records] == [
        (TASK, "blocked", None), (APPROVAL, "blocked", None), (CHECK, None, "green")]
    assert records[0]["reason"] == REASON
    rows, _ = show(repo, capsys)
    assert (rows[TASK][0], rows[CHECK][0]) == ("blocked", DONE)
    # a blocked task is no way round: the start and the done stay refused
    held = repo.snapshot()
    for call, opens, _ in calls():
        assert mark(repo, capsys, *call) == (
            2, "", MESSAGE.format(unit=opens, feature=ID)), call
    assert repo.snapshot() == held


# --- SC4.2: where no call is refused -------------------------------------------------

def test_sc4_2_with_g1_done_each_call_goes_through_with_its_older_line_and_keys(
        repo, capsys):
    repo.put(DOING)  # both declarations, and no review yet
    refused(repo, capsys)
    repo.put(DONE)
    assert g1(repo, capsys) == DONE
    through(repo, capsys)
    assert sorted(p.name for p in (repo.root / PROGRESS).iterdir()) == [
        ".gitignore", f"{ID}.yaml"]
    rows, _ = show(repo, capsys)
    assert (rows[ID][0], rows[TASK][0], rows[f"{ID}/G1"][0]) == (DONE, DONE, DONE)


def test_sc4_2_the_refusal_follows_the_tree_each_time_g1_changes(repo, capsys):
    repo.put(DONE)
    assert mark(repo, capsys, "start", TASK) == (0, f"{TASK}: doing\n", "")
    # the review loses item 6: G1 reads failed, and the next call is refused
    repo.put(FAILED)
    assert g1(repo, capsys) == FAILED
    held = repo.snapshot()
    assert mark(repo, capsys, "done", TASK) == (2, "", MESSAGE.format(unit=U, feature=ID))
    assert repo.snapshot() == held
    # a review that checks all 11 again: G1 reads done, and the call goes through
    repo.put(DONE)
    assert g1(repo, capsys) == DONE
    assert mark(repo, capsys, "done", TASK) == (0, f"{TASK}: done\n", "")
    assert [(r["item"], r["state"]) for r in repo.progress()] == [
        (TASK, "doing"), (TASK, "done")]


def test_sc4_2_a_feature_g1_exempt_names_is_never_refused(repo, capsys):
    refused(repo, capsys)
    repo.put(TO_DO, exempt=[ID])
    assert g1(repo, capsys) == "inactive"
    through(repo, capsys)


def test_sc4_2_an_exempt_list_that_names_another_feature_leaves_this_one_refused(
        repo, capsys):
    repo.feature(OTHER, OTHER_U)
    repo.put(TO_DO, exempt=[OTHER, "Apply-Discount", f"{ID} "])  # letter for letter
    refused(repo, capsys)
    through(repo, capsys, OTHER, OTHER_U)


@pytest.mark.parametrize("active", [("G0",), ()], ids=["g0-alone", "no-gate"])
def test_sc4_2_with_g1_absent_from_active_gates_no_call_is_refused(repo, capsys, active):
    repo.put(FAILED)
    refused(repo, capsys)
    repo.put(FAILED, active=active)  # every G1 source stands, and none is read
    assert g1(repo, capsys) in (None, "inactive")
    through(repo, capsys)


def test_sc4_2_of_two_features_only_the_one_whose_g1_has_not_passed_is_refused(
        repo, capsys):
    repo.feature(OTHER, OTHER_U)
    repo.put(DONE)  # apply-discount holds a signed review, refund-order none
    assert (g1(repo, capsys, ID), g1(repo, capsys, OTHER)) == (DONE, DOING)
    refused(repo, capsys, OTHER, OTHER_U)
    assert mark(repo, capsys, "start", f"{OTHER}/{OTHER_U}/green") == (
        2, "", "r1-refund cannot start: G1 has not passed for refund-order\n")
    through(repo, capsys)
    assert not (repo.root / PROGRESS / f"{OTHER}.yaml").exists()
    refused(repo, capsys, OTHER, OTHER_U)  # the first feature's records open nothing
    # and the other way round
    repo.put(DONE, OTHER)
    repo.remove(f".sdlc/g1/{ID}.yaml")
    assert (g1(repo, capsys, ID), g1(repo, capsys, OTHER)) == (DOING, DONE)
    refused(repo, capsys)
    through(repo, capsys, OTHER, OTHER_U)


# --- SC4.2: where the tree cannot read G1 (reading 5) --------------------------------

def test_sc4_2_reading_5_where_the_tree_makes_its_second_build_the_call_is_refused(
        repo, capsys, monkeypatch):
    repo.put(DONE)
    assert g1(repo, capsys) == DONE

    def raises(*args, **kwargs):
        raise RuntimeError("no such reading")

    # the build's own G1 step ends on an error, so the tree reads no G1 source
    with monkeypatch.context() as patch:
        patch.setattr(tree, "g1_problems", raises)
        rows, problems = show(repo, capsys)
        assert [rows[f"{ID}/G1{key}"][0]
                for key in ("", "/G1.1", "/G1.2", "/G1.3")] == [TO_DO] * 4
        assert problems[-1] == (f"{PROBLEM}unreadable G1 reading: G1 "
                                "(RuntimeError: no such reading)")
        refused(repo, capsys)
    assert mark(repo, capsys, "start", TASK) == (0, f"{TASK}: doing\n", "")


# --- SC4.2: texts a person may leave in a G1 source ----------------------------------

def _exempt_is_no_list(repo: Repo) -> None:
    repo.put(TO_DO, exempt=ID)


def _g1_listed_twice(repo: Repo) -> None:
    repo.put(DOING, active=("G0", "G1", "G1"))


def _record_is_no_yaml(repo: Repo) -> None:
    repo.put(DONE)
    repo.write(f".sdlc/g1/{ID}.yaml", "records: [unclosed\n")


def _record_is_no_mapping(repo: Repo) -> None:
    repo.put(DONE)
    repo.write(f".sdlc/g1/{ID}.yaml", "- a list\n")


HOSTILE = [_exempt_is_no_list, _g1_listed_twice, _record_is_no_yaml, _record_is_no_mapping]


@pytest.mark.parametrize("text", HOSTILE, ids=[text.__name__.strip("_") for text in HOSTILE])
def test_sc4_2_a_g1_text_the_tree_reads_as_not_passed_is_refused(repo, capsys, text):
    text(repo)
    status = g1(repo, capsys)
    assert status in (TO_DO, DOING, FAILED), status
    refused(repo, capsys)


def test_sc4_2_g1_in_lower_case_lists_no_g1_so_no_call_is_refused(repo, capsys):
    refused(repo, capsys)
    repo.put(TO_DO, active=("G0", "g1"))
    assert g1(repo, capsys) == "inactive"
    through(repo, capsys)


def test_sc4_2_a_unit_whose_id_is_its_features_prints_that_id_on_each_call(repo, capsys):
    repo.feature(SAME, SAME)
    rows, _ = show(repo, capsys)
    assert rows[f"{SAME}/{SAME}"][0] == TO_DO and f"{SAME}/{SAME}/write-tests" in rows
    refused(repo, capsys, SAME, SAME)
    assert mark(repo, capsys, "done", f"{SAME}/{SAME}") == (
        2, "", "price-list cannot start: G1 has not passed for price-list\n")
    repo.put(DONE, SAME)
    through(repo, capsys, SAME, SAME)
    refused(repo, capsys)  # apply-discount holds no review


# --- done_means: no unit's task reads done before its feature's G1 passes ------------

def test_done_means_no_task_reads_done_before_g1_passes_and_each_does_after(repo, capsys):
    repo.put(DOING)
    refused(repo, capsys)
    for uid in (U, "u2-cap"):
        for step in ("write-tests", "green", "approve-commit"):
            assert mark(repo, capsys, "done", f"{ID}/{uid}/{step}", "--by", "po")[0] == 2
        assert mark(repo, capsys, "done", f"{ID}/{uid}")[0] == 2
    rows, _ = show(repo, capsys)
    under = {rid: tag for rid, (tag, _) in rows.items()
             if rid.startswith(f"{ID}/u") or rid == ID}
    assert len(under) == 1 + 2 * (1 + 7 + 1)  # the contract, two units, each seven tasks and a check
    assert DONE not in under.values(), under
    assert not (repo.root / PROGRESS).exists()
    # G1 passes: the same close now reads every task done
    repo.put(DONE)
    assert mark(repo, capsys, "done", ID) == (0, f"{ID}: done\n", "")
    rows, _ = show(repo, capsys)
    assert {rows[rid][0] for rid in under} == {DONE}
