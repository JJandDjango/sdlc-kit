"""The query suite for ADR 0031 (contract tree-view, unit t6-query-face).

`taskcontract tree ID` prints one item of the tree in at most 20 lines, for
an agent that needs one fact without reading a document (SC6.1). The first
line is the item's line as the whole tree prints it, cut after its status,
marks and evidence. Then one labeled field per line, each only when the item
has it, in this order: `summary: <text>`; one line per link kind, its
targets joined by ", " (`depends_on: <id>, <id>`, `gate: <value>`);
`doc: docs/features/<id>.md:1`; `file: <path>:<line>` per file reference;
`page: <kit page>`. One line per field kind keeps an item within 20 lines by
the format, never by cutting.

Every id the tree prints answers, and an id that names two items prints
both, in tree order, one blank line between them; an unknown id prints one
line on stderr and exits 2 (SC6.2). A file reference is a repo path with the
line its item starts at: a contract and a finding at line 1 of their file, a
unit and a check at the line their entry starts in the contract file, and a
contract's feature doc, a file reference too (SC4.2), at its line 1. A gate
and a task point to the kit page that defines them, and a verdict to both
its contract file and its gate's page (SC6.3).

Each test drives the CLI in process against a fixture repo under tmp_path.
The contract files are written by hand, so each unit and sketch starts on a
line the test can name.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

import taskcontract
from conftest import ROW, write_seat_roster
from taskcontract import tree_view
from taskcontract.__main__ import main

# The kit whose package runs: its lists and the pages they name.
KIT = Path(taskcontract.__file__).resolve().parent.parent
DATA = KIT / "taskcontract" / "data"

UNKNOWN = "no node '{id}' - print the tree to list every node id\n"
FOLLOW = "taskcontract tree: --follow takes no id - give the id or --follow, not both\n"
LIMIT = 20
TASK_KEYS = ["approve-tests", "write-tests", "prove-red", "green",
             "approve-commit", "commit", "two-key"]

INTENT = ("A fixture contract for the query suite; its units carry the sketch "
          "shapes that check ids come from.")
BETA_INTENT = "A second fixture contract, with one unit that depends on nothing."
STATEMENT = "A fixture finding for the query suite."
RUN = "python -m pytest -k sc1_1"

ALPHA = """\
# alpha: the query suite's fixture contract, written by hand so that each
# unit and each sketch starts on a line the tests can name.
id: alpha
intent: >
  A fixture contract for the query suite; its units carry the sketch
  shapes that check ids come from.
scope:
  - src/
non_goals:
  - No other work
dependencies: []
entities: []
provenance:
  origin: human-request
decomposition:
  - unit: work for a1-core
    id: a1-core
    confirmed_by: [user]
    done_means: the work for a1-core is done
    acceptance_sketch:
      - verify the core prints (SC1.1)
      - verify both links print (SC5.1, SC5.2)

  # a2 waits on a1; its done_means and its last sketch run over two lines
  - unit: work for a2-edges
    id: a2-edges
    depends_on: [a1-core]
    confirmed_by: [user]
    done_means: >
      the work for a2-edges
      is done
    acceptance_sketch:
      - verify an edge holds
      - >
        verify it again
        on two lines (SC2.1)
"""

BETA = """\
id: beta
intent: A second fixture contract, with one unit that depends on nothing.
scope: [src/]
non_goals: [No other work]
dependencies: []
entities: []
provenance: {origin: human-request}
decomposition:
  - unit: work for b1-solo
    id: b1-solo
    confirmed_by: [user]
    done_means: the work for b1-solo is done
    acceptance_sketch:
      - verify the price rounds (by the house rule)
"""

# A green run as expected makes alpha/a1-core/SC1.1 done with its evidence;
# alpha then holds the latest record, so its first task to do,
# alpha/a1-core/approve-tests, is the current task and waits on a seat.
PROGRESS = f"""\
records:
  - item: alpha/a1-core/SC1.1
    run: green
    expect: green
    command: {RUN}
    head: abc1234
    at: 2026-09-22T10:00:00Z
"""


def _finding(slug, gate, kind):
    return {"finding": slug, "date": "2026-09-22", "kit_pinned": "v0.14.0",
            "gate": gate, "diagnostic": "none", "kind": kind, "count": 1,
            "statement": STATEMENT, "proposal": "none"}


def _dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _config(root, gates):
    _dump(root / ".sdlc" / "config.yaml", {
        "kit": "fixture", "adoption": "greenfield", "stack": "python",
        "active_gates": list(gates)})


def _repo(tmp_path, alpha=ALPHA, beta=BETA):
    """Every kind of item: G0 active with a finding, G3 named by a finding
    but not active, gates/none, alpha with its G0 verdict and a feature doc,
    a unit with depends_on and units without, the tasks, and checks named by
    one id, by ids joined with "+" and by sketch-<n>; one done check."""
    root = tmp_path / "repo"
    _config(root, ["G0"])
    _write(root / "specs" / "alpha" / "contract.yaml", alpha)
    _write(root / "specs" / "beta" / "contract.yaml", beta)
    write_seat_roster(root)
    findings = root / ".sdlc" / "findings"
    _dump(findings / "TEMPLATE.yaml", _finding("TODO", "TODO", "TODO"))
    _dump(findings / "stale-pin.yaml", _finding("stale-pin", "G0", "gap"))
    _dump(findings / "slow-loop.yaml", _finding("slow-loop", "G3.1", "friction"))
    _dump(findings / "idea.yaml", _finding("idea", "none", "proposal"))
    _write(root / "docs" / "features" / "alpha.md", "# alpha\n\nThe feature document.\n")
    _write(root / ".sdlc" / "progress" / "alpha.yaml", PROGRESS)
    return root


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Run from a folder that is not the root, and never find a git repo
    above the fixture, so a verdict's evidence reads `no commit`."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))


# --- the CLI --------------------------------------------------------------------

def _call(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:  # argparse's own exit
        code = exc.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _query(root, capsys, node, *options):
    """(exit code, stdout, stderr) of `taskcontract tree <node>`."""
    return _call(["tree", node, "--root", str(root), *options], capsys)


def _whole(root, capsys):
    """(rows, stderr) of the whole tree, which exits 0; each row is
    (depth, id, tag, rest)."""
    code, out, err = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    rows = []
    for text in out.splitlines():
        if text.lstrip().startswith("- "):
            continue  # a condition's diagnostic line, no item (project-tree o1)
        match = ROW.match(text)
        assert match, f"not an item line: {text!r}"
        rows.append((len(match["indent"]) // 2, match["id"], match["tag"], match["rest"]))
    return rows, err


def _rows_of(rows, rid):
    return [row for row in rows if row[1] == rid]


_LINKED = re.compile(r" (?:depends_on|gate|doc): \S+")


def _first(row):
    """The query's first line for a row of the whole tree: its id, its tag,
    its marks and its evidence, without its links, doc and summary."""
    _, rid, tag, rest = row
    return f"{rid} [{tag}]" + _LINKED.sub("", rest.partition(" | ")[0])


def _blocks(out):
    """The item blocks of one query's stdout, each a list of lines."""
    assert out.endswith("\n"), repr(out)
    return [block.splitlines() for block in out[:-1].split("\n\n")]


def _line_of(text, entry):
    """The 1-based line of `text` that is exactly `entry`, found once."""
    lines = text.splitlines()
    assert lines.count(entry) == 1, entry
    return lines.index(entry) + 1


def _pages(name):
    """{id: page} from one of the kit's name lists."""
    doc = yaml.safe_load((DATA / f"{name}.yaml").read_text(encoding="utf-8"))
    return {entry["id"]: entry["page"] for entry in doc[name]}


def _names(name):
    doc = yaml.safe_load((DATA / f"{name}.yaml").read_text(encoding="utf-8"))
    return {entry["id"]: entry["name"] for entry in doc[name]}


def _fields(out, label):
    """The value of each line of stdout that opens on `<label>: `."""
    return [text[len(label) + 2:] for text in out.splitlines()
            if text.startswith(f"{label}: ")]


A2_LINE = _line_of(ALPHA, "  - unit: work for a2-edges")


# --- SC6.1 one item: its status, summary, links and file references ----------

def test_sc6_1_an_item_prints_its_summary_links_doc_and_file_reference(tmp_path, capsys):
    root = _repo(tmp_path)
    rows, _ = _whole(root, capsys)
    assert _query(root, capsys, "alpha/a2-edges") == (0, (
        "alpha/a2-edges [to do]\n"
        "summary: the work for a2-edges is done\n"
        "depends_on: alpha/a1-core\n"
        f"file: specs/alpha/contract.yaml:{A2_LINE}\n"), "")
    assert _query(root, capsys, "gates/G3/G3.1/slow-loop") == (0, (
        "gates/G3/G3.1/slow-loop [kind: friction]\n"
        f"summary: {STATEMENT}\n"
        "gate: G3.1\n"
        "file: .sdlc/findings/slow-loop.yaml:1\n"), "")
    assert _query(root, capsys, "alpha") == (0, (
        _first(_rows_of(rows, "alpha")[0]) + "\n"
        f"summary: {INTENT}\n"
        "doc: docs/features/alpha.md:1\n"
        "file: specs/alpha/contract.yaml:1\n"), "")


def test_sc6_1_the_first_line_carries_the_status_marks_and_evidence(tmp_path, capsys):
    root = _repo(tmp_path)
    sketch = _line_of(ALPHA, "      - verify the core prints (SC1.1)")
    assert _query(root, capsys, "alpha/a1-core/SC1.1") == (0, (
        f"alpha/a1-core/SC1.1 [done] via {RUN} at abc1234\n"
        "summary: verify the core prints (SC1.1)\n"
        f"file: specs/alpha/contract.yaml:{sketch}\n"), "")
    assert _query(root, capsys, "alpha/a1-core/approve-tests") == (0, (
        "alpha/a1-core/approve-tests [waiting on a seat] current\n"
        f"summary: {_names('tasks')['approve-tests']}\n"
        f"page: {_pages('tasks')['approve-tests']}\n"), "")
    assert _query(root, capsys, "gates/G3") == (0, (
        "gates/G3 [to do] inactive\n"
        f"summary: {_names('gates')['G3']}\n"
        f"page: {_pages('gates')['G3']}\n"), "")


def _wide():
    """A contract whose last unit depends on 25 others, with a done_means of
    forty lines and 25 sketches: the largest item a fixture holds."""
    units = [f"  - unit: work for w{n:02}\n    id: w{n:02}\n    confirmed_by: [user]\n"
             f"    done_means: w{n:02} is done\n    acceptance_sketch: [verify w{n:02}]\n"
             for n in range(25)]
    deps = ", ".join(f"w{n:02}" for n in range(25))
    done = "".join(f"      line {n} of a done_means that runs long on purpose\n"
                   for n in range(40))
    sketches = "".join(f"      - verify part {n} of the last unit (SC9.{n})\n"
                       for n in range(25))
    units.append(f"  - unit: the last unit\n    id: w-last\n    depends_on: [{deps}]\n"
                 f"    confirmed_by: [user]\n    done_means: |\n{done}"
                 f"    acceptance_sketch:\n{sketches}")
    return ("id: wide\nintent: A contract with one very wide unit.\nscope: [src/]\n"
            "non_goals: [No other work]\ndependencies: []\nentities: []\n"
            "provenance: {origin: human-request}\ndecomposition:\n" + "".join(units))


def test_sc6_1_the_largest_item_prints_whole_in_at_most_twenty_lines(tmp_path, capsys):
    root = _repo(tmp_path)
    text = _wide()
    _write(root / "specs" / "wide" / "contract.yaml", text)
    code, out, err = _query(root, capsys, "wide/w-last")
    assert (code, err) == (0, "")
    lines = out.splitlines()
    assert lines[0] == "wide/w-last [to do]"
    assert len(lines) <= LIMIT, out
    # every link and the whole summary print: the cap holds by the format
    assert _fields(out, "depends_on") == [", ".join(f"wide/w{n:02}" for n in range(25))]
    assert _fields(out, "summary") == [" ".join(
        f"line {n} of a done_means that runs long on purpose" for n in range(40))]
    assert _fields(out, "file") == [
        f"specs/wide/contract.yaml:{_line_of(text, '  - unit: the last unit')}"]


# --- SC6.2 every id answers; an unknown id is refused in one line ------------

def test_sc6_2_every_id_the_tree_prints_answers(tmp_path, capsys):
    root = _repo(tmp_path)
    rows, _ = _whole(root, capsys)
    ids = [row[1] for row in rows]
    assert len(ids) == len(set(ids))  # one item per id in this fixture
    for kind in ("gates/G0", "gates/G0/stale-pin", "gates/G3", "gates/G3/G3.1/slow-loop",
                 "gates/none", "gates/none/idea", "alpha", "alpha/G0",
                 "alpha/a1-core", "alpha/a2-edges", "beta/b1-solo",
                 *(f"alpha/a1-core/{task}" for task in TASK_KEYS),
                 "alpha/a1-core/SC1.1", "alpha/a1-core/SC5.1+SC5.2",
                 "alpha/a2-edges/sketch-1", "beta/b1-solo/sketch-1"):
        assert kind in ids, kind
    for row in rows:
        code, out, err = _query(root, capsys, row[1])
        assert (code, err) == (0, ""), row[1]
        blocks = _blocks(out)
        assert len(blocks) == 1, out
        assert blocks[0][0] == _first(row), row[1]
        assert len(blocks[0]) <= LIMIT, out


def test_sc6_2_an_unknown_id_exits_2_with_one_line(tmp_path, capsys):
    root = _repo(tmp_path)
    broken = root / "specs" / "broken" / "contract.yaml"
    _write(broken, "id: [unclosed\n")  # an unreadable source adds nothing to the refusal
    for node in ("alpha/a1-core/nope",   # no such check or task
                 "ALPHA",                # the case differs
                 "alpha/",               # a trailing slash
                 "alpha\\a1-core",       # a backslash for the slash
                 "a1-core",              # a unit's last segment alone
                 "gates/G4",             # a gate neither active nor named
                 "broken/u1"):           # under a contract that does not parse
        assert _query(root, capsys, node) == (2, "", UNKNOWN.format(id=node)), node


def test_sc6_2_a_sketch_naming_a_task_key_prints_the_task_then_the_check(tmp_path, capsys):
    beta = BETA + "      - verify the commit lands (commit)\n"
    root = _repo(tmp_path, beta=beta)
    rows, _ = _whole(root, capsys)
    assert [row[2:] for row in _rows_of(rows, "beta/b1-solo/commit")] == [
        ("to do", f" | {_names('tasks')['commit']}"),
        ("to do", " | verify the commit lands (commit)")]
    sketch = _line_of(beta, "      - verify the commit lands (commit)")
    code, out, err = _query(root, capsys, "beta/b1-solo/commit")
    assert (code, err) == (0, "")
    assert out == (
        "beta/b1-solo/commit [to do]\n"
        f"summary: {_names('tasks')['commit']}\n"
        f"page: {_pages('tasks')['commit']}\n"
        "\n"
        "beta/b1-solo/commit [to do]\n"
        "summary: verify the commit lands (commit)\n"
        f"file: specs/beta/contract.yaml:{sketch}\n")
    assert all(len(block) <= LIMIT for block in _blocks(out))


def test_sc6_2_a_unit_named_like_an_active_gate_prints_the_verdict_then_the_unit(
        tmp_path, capsys):
    beta = BETA + (
        "  - unit: work named like a gate\n"
        "    id: G0\n"
        "    confirmed_by: [user]\n"
        "    done_means: the work named like a gate is done\n"
        "    acceptance_sketch:\n"
        "      - verify the unit shares its id with a verdict\n")
    root = _repo(tmp_path, beta=beta)
    rows, _ = _whole(root, capsys)
    verdict, unit = _rows_of(rows, "beta/G0")  # the verdict first, then the unit
    code, out, err = _query(root, capsys, "beta/G0")
    assert (code, err) == (0, "")
    assert out == (
        _first(verdict) + "\n"
        f"summary: {_names('gates')['G0']}\n"
        "file: specs/beta/contract.yaml:1\n"
        f"page: {_pages('gates')['G0']}\n"
        "\n"
        "beta/G0 [to do]\n"
        "summary: the work named like a gate is done\n"
        f"file: specs/beta/contract.yaml:{_line_of(beta, '  - unit: work named like a gate')}\n")
    assert _first(unit) == "beta/G0 [to do]"
    assert all(len(block) <= LIMIT for block in _blocks(out))


# --- SC6.3 each file reference a path an agent can open ----------------------

def test_sc6_3_each_file_reference_is_a_repo_path_at_the_line_its_item_starts(
        tmp_path, capsys):
    root = _repo(tmp_path)
    alpha, beta = "specs/alpha/contract.yaml", "specs/beta/contract.yaml"
    expected = {
        "alpha": f"{alpha}:1",
        "alpha/G0": f"{alpha}:1",
        "alpha/a1-core": f"{alpha}:{_line_of(ALPHA, '  - unit: work for a1-core')}",
        "alpha/a2-edges": f"{alpha}:{A2_LINE}",
        "alpha/a1-core/SC1.1":
            f"{alpha}:{_line_of(ALPHA, '      - verify the core prints (SC1.1)')}",
        "alpha/a1-core/SC5.1+SC5.2":
            f"{alpha}:{_line_of(ALPHA, '      - verify both links print (SC5.1, SC5.2)')}",
        "alpha/a2-edges/sketch-1":
            f"{alpha}:{_line_of(ALPHA, '      - verify an edge holds')}",
        "alpha/a2-edges/SC2.1": f"{alpha}:{_line_of(ALPHA, '      - >')}",  # a folded sketch
        "beta": f"{beta}:1",
        "beta/b1-solo": f"{beta}:{_line_of(BETA, '  - unit: work for b1-solo')}",
        "beta/b1-solo/sketch-1":
            f"{beta}:{_line_of(BETA, '      - verify the price rounds (by the house rule)')}",
        "gates/G0/stale-pin": ".sdlc/findings/stale-pin.yaml:1",
        "gates/none/idea": ".sdlc/findings/idea.yaml:1",
    }
    for node, reference in expected.items():
        code, out, err = _query(root, capsys, node)
        assert (code, err) == (0, ""), node
        assert _fields(out, "file") == [reference], node
        path, _, line = reference.rpartition(":")
        assert (root / path).is_file(), reference
        assert 1 <= int(line) <= len((root / path).read_text(encoding="utf-8").splitlines())
    # a contract's feature doc is a file reference too (SC4.2): its path at line 1
    code, out, err = _query(root, capsys, "alpha")
    assert (code, err) == (0, "")
    assert _fields(out, "doc") == ["docs/features/alpha.md:1"]
    assert (root / "docs" / "features" / "alpha.md").is_file()


def test_sc6_3_a_gate_a_task_and_a_verdict_point_to_their_kit_page(tmp_path, capsys):
    root = _repo(tmp_path)
    _config(root, ["G0", "X1"])  # X1: a gate the kit's list lacks
    gates, tasks = _pages("gates"), _pages("tasks")
    expected = {"gates/G0": gates["G0"], "gates/G3": gates["G3"], "alpha/G0": gates["G0"],
                **{f"beta/b1-solo/{task}": tasks[task] for task in TASK_KEYS}}
    for node, page in expected.items():
        code, out, err = _query(root, capsys, node)
        assert (code, err) == (0, ""), node
        assert _fields(out, "page") == [page], node
        assert (KIT / page).is_file(), page  # a path in the kit's repository
    # the no-gate item and a gate the list lacks have no page and no file
    for node in ("gates/none", "gates/X1"):
        code, out, err = _query(root, capsys, node)
        assert (code, err) == (0, ""), node
        assert out == f"{node} [to do]\n", node
    code, out, _ = _query(root, capsys, "alpha/X1")
    assert (code, _fields(out, "file"), _fields(out, "page")) == (
        0, ["specs/alpha/contract.yaml:1"], [])


# --- a line break inside a field ------------------------------------------------

REASON = "\n".join(f"reason line {n}" for n in range(25))


def test_sc6_1_a_field_holding_line_breaks_prints_on_one_line(tmp_path, capsys):
    """A progress record and a finding hold their text as written, line
    breaks included; each item's line reads them as spaces, on the whole
    tree and in the query, so a block keeps within its cap."""
    root = _repo(tmp_path)
    _dump(root / ".sdlc" / "progress" / "alpha.yaml", {"records": [
        {"item": "alpha/a1-core/SC1.1", "run": "green", "expect": "green",
         "command": "python -m pytest\n-k sc1_1", "head": "abc1234",
         "at": "2026-09-22T10:00:00Z"},
        {"item": "alpha/a1-core/approve-tests", "state": "done", "by": "the\nuser",
         "head": "abc1234", "at": "2026-09-22T10:01:00Z"},
        {"item": "alpha/a1-core/write-tests", "state": "blocked", "reason": REASON,
         "head": "abc1234", "at": "2026-09-22T10:02:00Z"},
    ]})
    _dump(root / ".sdlc" / "findings" / "odd-kind.yaml",
          _finding("odd-kind", "G0", "friction\nand more"))
    rows, _ = _whole(root, capsys)  # every line of the whole tree is one item's line
    expected = {
        "alpha/a1-core/SC1.1": "alpha/a1-core/SC1.1 [done] via python -m pytest -k sc1_1 at abc1234",
        "alpha/a1-core/approve-tests": "alpha/a1-core/approve-tests [done] by the user at abc1234",
        "alpha/a1-core/write-tests":
            "alpha/a1-core/write-tests [blocked] because " + REASON.replace("\n", " "),
        "gates/G0/odd-kind": "gates/G0/odd-kind [kind: friction and more]",
    }
    for node, first in expected.items():
        assert _first(_rows_of(rows, node)[0]) == first, node
        code, out, err = _query(root, capsys, node)
        assert (code, err) == (0, ""), node
        lines = out.splitlines()
        assert lines[0] == first, node
        assert len(lines) <= LIMIT, out


def test_sc6_2_an_unknown_id_holding_a_line_break_prints_one_line(tmp_path, capsys):
    root = _repo(tmp_path)
    assert _query(root, capsys, "alpha/no\nsuch") == (
        2, "", UNKNOWN.format(id="alpha/no such"))


def test_sc6_2_an_id_holding_a_line_break_answers_as_the_tree_prints_it(tmp_path, capsys):
    alpha = ALPHA + (
        "  - unit: work named on two lines\n"
        '    id: "two\\nlines"\n'
        "    confirmed_by: [user]\n"
        "    done_means: the work on two lines is done\n"
        "    acceptance_sketch:\n"
        "      - verify the id folds\n")
    root = _repo(tmp_path, alpha=alpha)
    code, out, _ = _call(["tree", "--root", str(root)], capsys)
    assert code == 0
    assert "  alpha/two lines [to do] | the work on two lines is done" in out.splitlines()
    unit = (
        "alpha/two lines [to do]\n"
        "summary: the work on two lines is done\n"
        f"file: specs/alpha/contract.yaml:{_line_of(alpha, '  - unit: work named on two lines')}\n")
    assert _query(root, capsys, "alpha/two lines") == (0, unit, "")  # as the tree prints it
    assert _query(root, capsys, "alpha/two\nlines") == (0, unit, "")  # as the contract holds it


# --- a link prints once --------------------------------------------------------

def test_a_repeated_depends_on_entry_links_once_in_its_first_order(tmp_path, capsys):
    alpha = ALPHA + (
        "  - unit: work for a3-join\n"
        "    id: a3-join\n"
        "    depends_on: [a2-edges, a1-core, a2-edges, a1-core]\n"
        "    confirmed_by: [user]\n"
        "    done_means: the work for a3-join is done\n"
        "    acceptance_sketch:\n"
        "      - verify the join holds\n")
    root = _repo(tmp_path, alpha=alpha)
    rows, _ = _whole(root, capsys)
    assert _rows_of(rows, "alpha/a3-join")[0][3] == (
        " depends_on: alpha/a2-edges depends_on: alpha/a1-core"
        " | the work for a3-join is done")
    code, out, err = _query(root, capsys, "alpha/a3-join")
    assert (code, err) == (0, "")
    assert _fields(out, "depends_on") == ["alpha/a2-edges, alpha/a1-core"]


# --- where the output goes -------------------------------------------------------

def test_an_unreadable_source_prints_on_stderr_beside_the_block(tmp_path, capsys):
    root = _repo(tmp_path)
    _write(root / "specs" / "broken" / "contract.yaml", "id: [unclosed\n")
    rows, whole_err = _whole(root, capsys)
    assert whole_err.startswith("taskcontract tree: unreadable contract: ")
    # the unparsed contract keeps line 1 and shows no unit, as the tree shows it
    assert _query(root, capsys, "broken") == (0, (
        _first(_rows_of(rows, "broken")[0]) + "\n"
        "file: specs/broken/contract.yaml:1\n"), whole_err)


def test_an_id_with_follow_is_refused_in_one_line(tmp_path, capsys, monkeypatch):
    def pane(*args, **kwargs):
        raise AssertionError("the pane started")

    monkeypatch.setattr(tree_view, "follow", pane)
    root = _repo(tmp_path)
    assert _query(root, capsys, "alpha", "--follow") == (2, "", FOLLOW)
