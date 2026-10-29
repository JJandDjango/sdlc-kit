### The execution team: `/sdlc execute` 🟢

> 🟢 **Shipped** (kit 0.21.0, contract `specs/execution-team/`, units e1 to e6;
> design [execution-team.design.md](../features/execution-team.design.md);
> [ADR 0040](../../decisions/0040-the-team-ships-in-the-plugins-workflows-folder-and-runs-at-its-rows-settings.md)).
> A kit before 0.21.0 has no team: no `test:` or `wall:` declaration, no
> wall and no `/sdlc execute`. Kit 0.21.0 had two gaps in [the wall](#the-wall-):
> the hook refused a declared command that names a walled folder, and it
> walled the Orchestrator's calls as the running member's. Kit 0.21.1 fixes
> both: the hook passes a Bash call equal to a declared `test.command` or
> `test.build`, word for word, and any call with no `agent_id` (the
> session's own, the Orchestrator's).

The execution node runs each task of a unit through one agent, at the
agent model and effort of the execution row in `.sdlc/workflow.md`
([Nodes](node.md)). QA writes each functional test; the Developer writes
the code and each unit test; the QA verifier and the Dev verifier each
hold the verdict on one channel. A hook holds the wall between the two
sides, and every task runs the test command the repository declares.

#### The declaration 🟢

🟢 A repository declares its test command and its wall in
`.sdlc/config.yaml`, each command an argument list. A consumer whose
suite is a batch file declares (the comments say what each entry is
for; the hook that holds the wall is in [The wall](#the-wall-)
below):

```yaml
test:
  command: [test.bat]            # the whole suite: green and two-key
  file: ["{file}"]               # one test file, its path from the repo root: prove-red
  build: [build.bat]             # optional; runs before `file`
wall:
  functional: [tests/run_*.bat]  # QA's tests: the Developer never reads them
  unit: [tests/*.cpp]            # the Developer's tests: QA never reads them
  code: [src/]                   # QA reads only these files' interface
  interface: [src/*.h]           # the interface QA reads whole
```

🟢 The kit declares its own: its pytest commands and
`functional: [tests/]`. `/sdlc init` writes neither block; a consumer
writes its own. A `command` that is not a non-empty list of non-empty
strings counts as none; `file` and `build` read as empty when absent.

#### Starting a task: `task.py start` 🟢

🟢 `workflows/tools/task.py start` opens one task step (`/sdlc execute`
calls it for each task, below): it writes the task
file, `sdlc-task.json` in the repository's git folder (never
committed), and prints the task's line:

```
$ python workflows/tools/task.py start --unit execution-team/e1-declaration --task green --operator developer
Task green: Developer, round 1
```

🟢 `--task` is one of the seven task ids; `--operator` is one of `qa`,
`qa-verifier`, `developer`, `dev-verifier`, `receipts` and
`orchestrator`, printed as QA, QA verifier, Developer, Dev verifier,
receipts and Orchestrator; `--root` names the repository (default `.`).
Any other value is a usage error, exit 2. The task file sits in the
folder `git rev-parse --absolute-git-dir` names: `.git/` in a clone, the
worktree's own folder in a linked worktree. A task's round is its channel's
round: one more than the failed rounds in the rounds file (below) of
write-tests, for approve-tests and prove-red, or of green, for
approve-commit, commit and two-key; the task's own count, when higher.
It is 1 when the file holds none.

🟢 Each refusal goes to stderr, exits 1 and writes nothing, checked in
this order:

- No `test.command`: `Task {task} did not start: the repository declares no test command.`
- No git repository: `Task {task} did not start: no git repository at {root}.`
- A running task: `Task {task} did not start: task {running} is running.`
- `taskcontract progress start` refuses: its own line prints as it gave
  it, such as `{unit} cannot start: G1 has not passed for {feature}`.

#### The scripts run the declared command 🟢

🟢 `prove.py` and `receipts.py` ship under `workflows/tools/` and run the
declared command for prove-red, green and two-key; pytest runs only where
it is declared. Run from the repository root:

```
$ python workflows/tools/prove.py --scratch DIR --test tests/run_command_line.bat
{"ok":true,"scratch":"<DIR>","red":{"summary":"test: FAILED","red_ok":true,"log":"logs/red.log"}}
```

🟢 `prove.py` exports REV (`--at`, default HEAD) into `DIR/export/`
afresh each run, copies the draft from `DIR/draft/PATH` when one sits
there (else the committed file at PATH runs), and runs `test.build`,
then `test.file` with `{file}` as PATH, or `test.command` when no `file`
is declared. Without `--mutations` it proves red: a pytest command's
tests each fail on an assertion, any other command exits 1. With
`--mutations FILE` it proves the mutations instead: the unmutated export
must pass, then each mutation must make the run fail (`caught_by` lists
test ids for pytest, PATH otherwise). It has no prototype. Exit 0 holds,
1 a check failed, 2 usage, 254 the test command never started.

🟢 `receipts.py` keeps its options and JSON. An `argv[0]` naming a file
in the repository (`test.bat`) runs that file ahead of a program on
PATH, and a command other than pytest reports its last line
(`test: ok`).

#### The wall 🟢

🟢 While a task runs, a PreToolUse hook in the plugin refuses each tool
call that crosses the wall, a Bash call naming a walled path among them:

```
Task green: Developer reads no functional test: tests/run_command_line.bat
Task write-tests: QA reads no unit test: tests/test_command_line.cpp
Task write-tests: QA reads no implementation body: src/command_line.cpp
```

🟢 The Developer stands behind `functional`; QA stands behind `unit` and
`code`, with the files `interface` lists open to it. The two verifiers,
`receipts` and the Orchestrator stand behind no list of their own. The
hook holds only a call whose event carries an `agent_id` (a workflow
member's); a call with no `agent_id`, or a null one, is the session's
own, the Orchestrator's, and passes. `agent_id` is the hook's one sign of
a member: a Claude Code that stopped sending it would let every call
through. The hook checks the
path a Read, Edit, Write or NotebookEdit names, a Grep's `path` and
`glob`, a Glob's `path` and `pattern`, and each word of a Bash command.
A folder entry ends in `/`; any other entry is a glob. A call that
reads a walled file without naming it, such as a Grep over the whole
repository, can still pass, and so can a Bash path glued to a shell
operator (`cat tests/run_a.bat;`) under a glob entry, or a Git Bash
path on Windows (`/e/repo/tests/run_a.bat`).

🟢 The hook passes a Bash call whose words equal the declared
`test.command` or `test.build`, element for element (quotes and extra
spaces do not matter), though it names a walled folder (`pytest tests`
beside `functional: [tests/]`). Any other call is checked as above: one
more or fewer word, a different case, an operator glued to a word or a
chain is held, and so is `test.file`. The hook cuts each `--opt=value`
word of the call to its value before it compares, so a declared word of
that form never matches: declare such an option as two words where the
tool takes them (`--rootdir`, `tests`). The kit declares
`python -P -m pytest tests -q -n auto`.

🟢 `python -m taskcontract interface {file}` prints each public
function's and class's signature with its docstring's first line, and
no body, for QA (in C++, QA reads the `.h` files); QA may run it on a
code file. A file that is not Python, a missing file and one that does
not parse each exit 2 with one line. Between tasks no task file stands,
and the hook refuses nothing.

#### Running a unit: `/sdlc execute {contract} {unit}` 🟢

🟢 Run in the session `python -m taskcontract node execution` starts. The
team ships in the plugin's `workflows/` folder and runs from the plugin
root: nothing is copied into a consumer. The flow starts each member by
its plugin name, `sdlc:qa` and so on (under `--plugin-dir`, the plugin
folder's name), and passes it the row's model and effort; a member given
neither starts no agent.

🟢 A FAIL returns its task to its channel for another round (below). An
error, a question or a third failed round shows its output and stops the
run, with no PR.

🟢 A contract whose id starts a walled path (contract `greet` beside
`wall.code: [greet/]`) runs: the Orchestrator's `task.py end`, `fail`
and `stop` carry no `agent_id`, so the wall passes them. The flow still
removes the task file before each, as kit 0.21.0 needed.

🟢 A run with one failed round:

```
Execution: execution-team unit u1, sonnet at high, test command: test.bat
Task write-tests: QA, round 1: done
Task approve-tests: QA verifier, round 1: PASS
Task prove-red: QA verifier, round 1: PASS
Task green: Developer, round 1: done
Task approve-commit: receipts, round 1: exit 0
Task commit: Orchestrator: 3f2a1bc
Task two-key: Dev verifier, round 1: FAIL (2 sketches failed)
Task green: Developer, round 2: done
Task approve-commit: receipts, round 2: exit 0
Task commit: Orchestrator: 9c04e7d
Task two-key: Dev verifier, round 2: PASS
Task two-key: QA verifier, round 2: PASS (mutations: 4 of 4 caught)
Draft PR: #12 https://github.com/{owner}/{repo}/pull/12
```

🟢 Two refusals stop a run before any task and open no PR:
`Execution did not start: no unit {unit} in specs/{contract}/contract.yaml.`
and `Execution did not start: specs/{contract}/contract.yaml is not ready-green.`

#### Rounds, stops and the draft PR 🟢

🟢 A FAIL returns the task to its channel with its reasons, and the next
round starts from them: a QA-channel FAIL (approve-tests, prove-red or
the QA verifier's two-key) to the next write-tests round, a
Developer-channel FAIL (the Dev verifier, or receipts' non-zero exit) to
the next green round. The reasons reach only that channel's member, in
its `reasons` arg, and reset to none once the check that failed passes.

🟢 `task.py fail --unit {contract}/{unit} --task {write-tests|green}
[--reason TEXT]` counts one failed round of the task in `sdlc-rounds.json`
(in the git folder, for one unit at a time) and removes the task file. A
first or second failure prints nothing and exits 0. The third removes
both files, exits 1 and prints, one line a round, each reason on one
line (`no reason given` when none):

```
Task green failed 3 rounds. The run stops here; the failures follow.
  Round 1: 2 sketches failed: SC5.1 (src/command_line.cpp:41), SC5.2 (src/command_line.cpp:58)
  Round 2: 1 sketch failed: SC5.2 (src/command_line.cpp:58)
  Round 3: no reason given
```

🟢 `task.py stop --task {task} --operator {operator} --question TEXT`
removes both files and exits 1, printing
`Task {task} stopped on a question from {Operator}: {question}`; it needs
no git repository and writes no progress record.

🟢 `task.py end --unit {contract}/{unit} --task {task} [--by SEAT]` runs
`taskcontract progress done` for the task (an approval takes its holder in
`--by`) and removes the task file; it prints nothing. When `progress done`
refuses, its line goes to stderr, the task file stays and `end` exits 1.
`task.py end --run` removes both files, after the draft PR. A task's
failed rounds survive its `end`.

🟢 A green run closes the unit with `taskcontract progress done
{contract}/{unit}`, so the tree reads it done.

🟢 A run whose last task passes pushes the unit's branch with
`git push -u origin {branch}`, then opens a draft PR on it with
`gh pr create --draft`. When either exits non-zero the run shows its
output and ends with no Draft PR line. It never marks the PR ready and never merges it:
the user does.

#### A batch-file repository 🟢

🟢 In a fixture repository whose test command is a batch file, one unit
runs from write-tests to two-key and ends green. The kit keeps one at
`tests/fixtures/batch-repo/`: `test.command: [test.bat]`, `test.file:
[test.bat, "{file}"]` and the wall `functional: [tests/]`, `code: [src/]`.
In a copy of it, the team ran every task in round 1:

```
Execution: greet unit greeting, sonnet at high, test command: test.bat
Task write-tests: QA, round 1: done
Task approve-tests: QA verifier, round 1: PASS
Task prove-red: QA verifier, round 1: PASS
Task green: Developer, round 1: done
Task approve-commit: receipts, round 1: exit 0
Task commit: Orchestrator: e79311c
Task two-key: Dev verifier, round 1: PASS
Task two-key: QA verifier, round 1: PASS (mutations: 8 of 8 caught)
```

🟢 On Windows the team's Bash is Git Bash, whose PATH puts GNU `find`
and `sort` before Windows' own. A batch suite that calls them puts
System32 first itself, as the fixture's `test.bat` does; without it,
`find /c` walks the whole C: drive and the run hangs:

```bat
set "PATH=%SystemRoot%\System32;%PATH%"
```
