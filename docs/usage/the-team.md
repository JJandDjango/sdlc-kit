### The execution team: `/sdlc execute` 🔴

> 🔴 **Not shipped** (contract `specs/execution-team/`, units e1 to e6;
> design [execution-team.design.md](../features/execution-team.design.md)).
> Each unit turns its own markers green as it ships; e6 ships kit 0.21.0.

The execution node runs each task of a unit through one agent, at the
agent model and effort of the execution row in `.sdlc/workflow.md`
([Nodes](node.md)). QA writes each functional test; the Developer writes
the code and each unit test; the QA verifier and the Dev verifier each
hold the verdict on one channel. A hook holds the wall between the two
sides, and every task runs the test command the repository declares.

#### The declaration 🟢

🟢 A repository declares its test command and its wall in
`.sdlc/config.yaml`. Each command is an argument list, run with no shell.
A consumer whose suite is a batch file declares:

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

🟢 Each task step starts with `workflows/tools/task.py start`, which
writes the task file, `sdlc-task.json` in the repository's git folder
(never committed), and prints the task's line:

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
worktree's own folder in a linked worktree. The round reads 1 until the
rounds file ships.

🟢 Each refusal goes to stderr, exits 1 and writes nothing, checked in
this order:

- No `test.command`: `Task {task} did not start: the repository declares no test command.`
- No git repository: `Task {task} did not start: no git repository at {root}.`
- A running task: `Task {task} did not start: task {running} is running.`
- `taskcontract progress start` refuses: its own line prints as it gave
  it, such as `{unit} cannot start: G1 has not passed for {feature}`.

#### The scripts run the declared command 🔴

🔴 `prove.py` and `receipts.py` ship under `workflows/tools/` and run the
declared command for prove-red, green and two-key; pytest runs only where
it is declared. QA writes no prototype: the QA verifier's mutations run at
two-key, on an export of the commit.

#### The wall 🔴

🔴 While a task runs, a PreToolUse hook in the plugin refuses each tool
call that crosses the wall, a Bash call naming a walled path among them:

```
Task green: Developer reads no functional test: tests/run_command_line.bat
Task write-tests: QA reads no unit test: tests/test_command_line.cpp
Task write-tests: QA reads no implementation body: src/command_line.cpp
```

🔴 `python -m taskcontract interface {file}` prints a Python file's
signatures and docstrings, with no body, for QA (in C++, QA reads the
`.h` files). Between tasks no task file stands, and the hook refuses
nothing.

#### Running a unit: `/sdlc execute {contract} {unit}` 🔴

🔴 Run in the session `python -m taskcontract node execution` starts. The
team ships in the plugin's `workflows/` folder and runs from the plugin
root: nothing is copied into a consumer. A run with one failed round:

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

🔴 Two refusals stop a run before any task and open no PR:
`Execution did not start: no unit {unit} in specs/{contract}/contract.yaml.`
and `Execution did not start: specs/{contract}/contract.yaml is not ready-green.`

#### Rounds, stops and the draft PR 🔴

🔴 A FAIL returns the task to its channel with its reasons, and the next
round starts from them. A task runs at most 3 rounds: the third failure
stops the run, prints
`Task {task} failed 3 rounds. The run stops here; the failures follow.`
and one line a round, and opens no PR. A question from an operator stops
its task: `Task {task} stopped on a question from {operator}: {question}`.

🔴 A run whose last task passes opens a draft PR on the unit's branch. It
never marks the PR ready and never merges it: the user does.

#### A batch-file repository 🔴

🔴 In a fixture repository whose test command is a batch file, one unit
runs from write-tests to two-key and ends green.
