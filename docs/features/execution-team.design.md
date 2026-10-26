| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-25 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r3. Engineer seat: Johnathan Hyden |
| 2026-10-25 | Johnathan Hyden | r2: Measured: the checks before signing, on the solution half: 27 findings (CL006 22, CL008 5); Scope against the release unit's paths: covered; ready checks 11 to 15: 9 OPEN |
| 2026-10-25 | Johnathan Hyden | r3: Measured: the checks before signing, on the solution half: 16 findings (CL006 16); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-25 | Johnathan Hyden | r4: The solution half finished: 12 sections written, 1 OPEN |
| 2026-10-25 | Johnathan Hyden | r5: Signed: solution half. The engineer seat signs r4 |

# execution-team - Standard Development Workflow

`sdlc_development_kit` · seat: engineer Johnathan Hyden · requirements: `docs/features/execution-team.md` · contract: `execution-team`, draft · PR: none · merge SHA: none

## Proposed solution

`[Engineer seat · authored]`

### Scope

1. `workflows/` (new, tracked, at the plugin root): the drafter, developer, verifier and retirer workflows move here from `.claude/workflows/`. The plugin ships the tracked tree (`.claude-plugin/marketplace.json`, source `./`), so an untracked file never ships (SC1.2).
2. `workflows/tools/prove.py` and `workflows/tools/receipts.py`: moved, and changed to run the declared test command; their tests `test_prove.py` and `test_receipts.py` move to `tests/`. `workflows/tools/task.py` (new): the running task's file, its rounds and its stop messages.
3. `skills/sdlc/` (`SKILL.md` and a new `flows/execute.md`): the Orchestrator, as `/sdlc execute {contract} {unit}`, run in the session `python -m taskcontract node execution` starts. A skill whose steps call the Workflow tool is the user's opt-in, and it launches each workflow by its path under the plugin root.
4. `taskcontract/`: reads the test command from `.sdlc/config.yaml`; `python -m taskcontract interface {file}` prints a Python file's signatures without their bodies, for QA (in C++, QA reads the `.h` files).
5. `.sdlc/config.yaml`: the kit declares its own test command.
6. `tests/`: the team's tests, and a fixture repo whose test command is a batch file (SC2.2).
7. `docs/usage/` (a new page), `USAGE.md`, `docs/operators.md` (the roster gains the Orchestrator and the two verifiers) and `CHANGELOG.md`.
8. `hooks/` (`hooks.json` and a new hook script): the wall, a PreToolUse hook that refuses a tool call crossing it while a task runs.
9. The release unit's (e6, kit 0.21.0): `pyproject.toml`, `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml`.

### Out of scope

1. The engine's repository (`E:/ImSimProject/engine`): the kit ships, and the engine pulls a release.
2. The registrations of `sdlc-spec` and `sdlc-qa`: both stay registered and unshipped (`docs/operators.md:34-35`).
3. `skills/sdlc/templates/profiles/`: no `cpp` profile is added.
4. `.sdlc/workflow.md`: the execution row already reads `sonnet`, `high` and the five operators.
5. `agents/sdlc-developer.md` and `agents/sdlc-verifier.md`: unchanged, `model: inherit` kept; the team runs through the workflows' own prompts.
6. `live-run-seats` and the other session tools in `.claude/workflows/`: they stay untracked and do not ship.

### Interfaces

These stay as they are:

1. `python -m taskcontract node execution --print` prints `Node execution: claude --model sonnet --effort high`.
2. The three error messages of the requirements document, verbatim: SC2.3, SC4.2 and SC4.3.
3. `prove.py` and `receipts.py` keep their exit codes (0, 1, 2 and 254; `receipts.py` adds 124). `receipts.py` keeps its JSON stdout; `prove.py`'s changes as item 7 says.

The declaration. A consumer's `.sdlc/config.yaml` gains two blocks; each command is an argv list, since `receipts.py` runs no shell. The engine's, drawn:

```yaml
test:
  command: [test.bat]            # the whole suite: green and two-key
  file: ["{file}"]               # one test file, its path from the repo root: prove-red
  build: [build.bat]             # optional; runs before `file`
wall:
  functional: [tests/run_*.bat]  # QA's tests: the Developer never reads them
  unit: [tests/*.cpp]            # the Developer's tests: QA never reads them
  code: [src/]                   # QA reads only these files' interface
  interface: [src/*.h]           # the interface QA reads whole (Python: `taskcontract interface`)
```

The kit's own declares its pytest commands and `functional: [tests/]`. With no `test.command`, a task prints SC2.3's message.

4. The wall. Before each task, `/sdlc execute` runs `workflows/tools/task.py`, which writes `.git/sdlc-task.json` with the task, its operator and its round (never committed), counts the rounds, and prints SC2.3's and SC4.2's messages. A PreToolUse hook in the plugin's `hooks/hooks.json` refuses each tool call that crosses the wall, a Bash call naming a walled path among them:

```
Task green: the Developer reads no functional test: tests/run_command_line.bat
```

5. `/sdlc execute {contract} {unit}`, run in the session `python -m taskcontract node execution` starts. A run with one failed round:

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

QA writes the tests; the QA verifier holds approve-tests and prove-red; the Developer holds green; `receipts.py`'s exit 0 holds approve-commit; the Orchestrator commits; two-key takes both verifiers. A run that stops on SC4.2's or SC4.3's message opens no PR. A unit takes at least 5 agents.

6. `python -m taskcontract interface {file}` prints each public name's signature and docstring, and no body:

```
$ python -m taskcontract interface taskcontract/workflow.py
def read(root: Path) -> Workflow:
    """The workflow file's nodes, edges and rows; raises on a structural fault."""
def settings(root: Path, node_id: str) -> Settings:
    """One node's agent model and effort, read from the settings table. ..."""
```

A file that is not Python exits 2: `No interface for {file}: only a .py file has one.`

7. `prove.py --scratch DIR --test PATH [--at REV] [--mutations FILE]` exports REV (default HEAD), places the draft at PATH, and runs `test.build`, then `test.file` (or `test.command` when no `file` is declared). `red_ok`: for a pytest command, every test fails on an assertion (junitxml, as today); for another command, the run exits 1. QA writes no prototype: QA reads no implementation body (SC3.2). The mutations run at two-key, on an export of the commit, written by the QA verifier; a mutation no test catches fails QA's channel, its reason naming the behavior, never the code. The JSON drops `green`, `proto_imported` and `package`.
8. `receipts.py` keeps its options. An `argv[0]` naming a file in the repository (`test.bat`) resolves there; a command other than pytest keeps its last line as its key output (`test: ok`).

9. `prove.py`'s JSON, for a command other than pytest (one result per test file; for pytest, `summary` is pytest's line and `caught_by` lists test ids, as today). At prove-red:

```
{"ok":true,"scratch":"<scratch>","red":{"summary":"test: command line: FAILED: imsim --frames 0: exit code 0, expected 2","red_ok":true,"log":"logs/red.log"}}
```

At two-key, `--at 9c04e7d --mutations mutations.json`, one mutation caught and one not:

```
{"ok":false,"scratch":"<scratch>","mutations":[
 {"name":"frames accepts 0","applied":true,"caught_by":["tests/run_command_line.bat"],"caught_count":1,"log":"logs/mutation-1.log"},
 {"name":"device needs no text","applied":true,"caught_by":"not caught","log":"logs/mutation-2.log"}]}
```

A mutation whose `old` text matches no place, or several, reads `{"name":...,"applied":false,"error":"old matches 2 places, not 1"}`. Exit 0: red and every mutation hold; 1: a check failed; 2: usage; 254: the test command never started.

10. `workflows/tools/task.py`, one command a task step:

```
$ python workflows/tools/task.py start --task green --operator developer
Task green: Developer, round 2
```

`start` writes `.git/sdlc-task.json` (`{"task":"green","operator":"developer","round":2}`) and exits 0; with no `test.command` it prints SC2.3's message, writes nothing and exits 1. `fail --task green` counts the failed round; the third prints SC4.2's message, removes the file and exits 1. `stop --task green --operator developer --question "{question}"` prints SC4.3's message, removes the file and exits 1. `end` removes the file, prints nothing and exits 0.

11. A run that stops. On a third failed round, the failures follow one line a round, and no PR line prints:

```
Task two-key: Dev verifier, round 3: FAIL (1 sketch failed)
Task green failed 3 rounds. The run stops here; the failures follow.
  Round 1: 2 sketches failed: SC5.1 (src/command_line.cpp:41), SC5.2 (src/command_line.cpp:58)
  Round 2: 1 sketch failed: SC5.2 (src/command_line.cpp:58)
  Round 3: 1 sketch failed: SC5.2 (src/command_line.cpp:60)
```

On a question:

```
Task green: Developer, round 1: done
Task green stopped on a question from Developer: Which exit code does --frames 0 take?
```

No endpoint table: the feature has no HTTP surface.

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| Agent model and effort | The execution row of `.sdlc/workflow.md` | The row: no other file holds either (`docs/usage/node.md:6-13`) |
| The task list | `taskcontract/data/tasks.yaml` | (one source) |
| A unit's sketches and done means | `specs/{id}/contract.yaml` | The contract |
| The test command | `.sdlc/config.yaml`, its `test:` block | The declaration; pytest runs only where it is declared |
| The wall's paths | `.sdlc/config.yaml`, its `wall:` block | The declaration |
| The running task, its operator and its round | `.git/sdlc-task.json`, written by `/sdlc execute` | The file; with no file no task runs, and the hook refuses nothing |
| A Python file's interface | `python -m taskcontract interface`, from the code at HEAD | The code |
| The Two-Key verdict | `receipts.py`'s exit codes, never its `ok` field (`two-key-unit-verifier.js:102-108`), then both verifiers' grades | The exit code: no grade overrides a non-zero exit |
| The draft PR's branch | The current git branch | Git |
| Which operators ship | The plugin's `agents/` folder | `agents/`: a roster line in `docs/operators.md` that disagrees is a defect on that page |
| Whether a file the team runs ships | `git ls-files` (the plugin ships the tracked tree) | Git |
| A failure's reasons | The verifier's result: its reasons, failed sketches, blocking defects or uncaught mutations | The result: the Orchestrator passes it whole to the next round |
| An operator's question | The `questions` field of the task's workflow result | The result: a non-empty list stops the task |

### Constraints

1. Every shell call is one segment: no pipes, chains or redirects.
2. A spawned process opens no window.
3. Tests run in the foreground with a set timeout; no task polls an output file.
4. No new dependency.
5. The Developer writes implementation and unit tests only (ADR 0010); contracts are read-only to every operator.
6. Agent definitions are class E: a change passes the enforcement-layer approval channel.
7. Each check loops at most 5 times, and each task runs at most 3 rounds.
8. The wall is enforced by the hook, never by a prompt alone: the Developer reads no functional test; QA reads no implementation body and no unit test.
9. One unit runs at a time: `.git/sdlc-task.json` holds one task.
10. A run never marks its PR ready and never merges it.
11. Each commit the Orchestrator makes carries the `Contract:` and `Theory:` trailers the grader checks.
12. Nothing is copied into a consumer: the team runs from `${CLAUDE_PLUGIN_ROOT}`.

### Units

| Unit | Checks | Done means | Tests by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| e1-declaration | SC2.3 | A repository declares `test:` and `wall:`, the kit declares its own, and a task with no `test.command` prints SC2.3's message. | SC2.3: automated | none |
| e2-scripts | SC2.1 | `prove.py` and `receipts.py` ship under `workflows/tools/` and run the declared test command, pytest only where it is declared, with no prototype. | SC2.1: automated, on a pytest fixture and a batch-file fixture | `prove.py`'s prototype (`setup`'s package copy, `prove_green`, `PACKAGE`) and the tests in `test_prove.py` that pin it |
| e3-wall | SC3.1 + SC3.2 | `python -m taskcontract interface` prints signatures without bodies, and the hook refuses each tool call across the wall during a task. | SC3.1, SC3.2: automated, the hook fed tool calls | none |
| e4-team | SC1.1, SC1.2, SC1.3 | The team ships in the plugin, and each team member starts in a consumer session at the execution row's settings. | SC1.1: automated, and a manual receipt (a consumer session starts each team member); SC1.2, SC1.3: automated | the untracked copies under `.claude/workflows/` (no test pins them) |
| e5-rounds | SC4.1, SC4.2, SC4.3, SC5.1, SC5.2 | A FAIL returns its reasons, three failures or a question stop the run, and a pass opens a draft PR. | SC4.1, SC4.2, SC4.3, SC5.1, SC5.2: automated (`task.py`'s rounds and messages; the flow's one PR command is `gh pr create --draft`) | none |
| e6-batch-run | SC2.2 | In a batch-file fixture repository, one unit runs from write-tests to two-key and ends green, and kit 0.21.0 ships. | SC2.2: manual receipt (the run's lines and the fixture's green) | none |

e6 is the release unit: it ships kit 0.21.0 through `pyproject.toml`, `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml`, since the engine pulls only a release. The usage page is written in e1 with every marker red; each unit turns its own markers green as it ships.

The draft check's CL006 words in the done means go to intake's full lane as dictionary candidates: repository, prototype, signatures, bodies, tool, team, member, reasons, failures, stop, opens, batch-file, write-tests, ends.

### Order

e1, e2, e3, e4, e5, e6, one at a time; each unit uses what the one before made:

1. e1 first: every later unit reads the declaration.
2. e2: the scripts run the declared command.
3. e3 before the team ships: no team member runs without its wall.
4. e4, then e5: the team, then its rounds and its PR.
5. e6 last: the live batch-file run needs all five.

## Risks and cost

`[Engineer seat · authored]`

1. A plugin may not load workflows: today they load only from `.claude/workflows/`, which is untracked. Answer: `/sdlc execute` launches each by its path under `${CLAUDE_PLUGIN_ROOT}`; e4's manual receipt proves it.
2. `prove.py` hard-wires the `taskcontract` package and pytest's junitxml (`prove.py:40`, `prove.py:262`); a batch-file runner gives neither. e2 removes both.
3. `test.bat` builds and runs every test, with no way to select one: a red proof sees one exit code, not one result per test. Answer: `test.file` runs one test file.
4. Cost: at least 5 agents a unit at Sonnet high, each starting near 54K tokens; each retry round adds to it.
5. The highest risk: a workflow's agents may not fire the session's hooks. Then the wall is prompt-only and SC3 fails. e3 opens with a probe that proves an agent's tool call reaches the hook, before it builds anything else.
6. A Bash call can read a walled file without naming it (a glob, a script). The hook matches walled paths and globs over walled folders; an indirect read can still pass.
7. In the engine, each mutation rebuilds and runs the whole suite: 4 mutations cost 4 full builds, time not yet measured.
8. The build's cost: six build sessions, one a unit; e6 adds a live run of the whole team.

## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | yes | Johnathan Hyden, the engineer seat (also the PO seat), at S3 | The requirements name no holder for approve-tests and approve-commit: the QA verifier holds approve-tests; `receipts.py`'s exit 0 holds approve-commit. |
| 2. More than one solution | yes | Johnathan Hyden, the engineer seat, at S3 | The test command lives in `.sdlc/config.yaml`, not a `cpp` tooling profile (a non-goal); QA's proof uses mutations at two-key, not a prototype (SC3.2 forbids it); a hook holds the wall, not a prompt alone. |
| 3. A solution unconventional to the codebase | yes | Johnathan Hyden, the engineer seat, at S1 and S3 | `workflows/` is a new plugin folder, launched by path, beside `agents/`, `skills/` and `hooks/`; the kit writes a runtime file under `.git/` (`.git/sdlc-task.json`) for the first time. |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | yes | Johnathan Hyden, the engineer seat, at S3 | A consumer's `.sdlc/config.yaml` gains `test:` and `wall:` (additive: a config with no `test:` is refused only when it starts a task); the plugin's `hooks.json` gains a PreToolUse hook (it refuses nothing while no task runs); the term `operator` gains the Orchestrator (waits for intake). |

## Decisions and open questions

`[Engineer seat · authored]`

1. Does the QA verifier run through `prove.py`? Decided: yes, the red proof at prove-red and the mutations at two-key.
2. Does the Sonnet ruling supersede the 2026-10-12 process-cost ruling in an ADR? Decided: yes; one ADR, written in e4, records it with the plugin's new `workflows/` folder (Consult case 3).
3. How does QA get an existing function's signature without its body? Decided: in C++, through the `.h` files `wall.interface` lists; in Python, through `python -m taskcontract interface`.
4. Where does a consumer declare its test command? Decided: `.sdlc/config.yaml`, its `test:` block.
5. How do `prove.py` and `receipts.py` stop assuming pytest? Decided: both run the declared commands, and read results per test only when the command is pytest.
6. Who holds the tasks approve-tests and approve-commit (`taskcontract/data/tasks.yaml`) when a run stops for the user only at the draft PR? Decided: the QA verifier holds approve-tests; `receipts.py`'s exit 0 holds approve-commit.
7. How does QA prove its tests can pass without reading a body? Decided: QA writes no prototype; the QA verifier's mutations at two-key prove the tests catch broken behavior.
8. OPEN: does a workflow's agent fire the session's hooks? The probe that opens e3 answers it.

## Traceability

### Links out

`[Engineer seat · authored]`

- `docs/features/execution-team.md` (requirements r3) and `docs/features/small-session-flow.md`
- `docs/operators.md`, `docs/usage/node.md` and `.sdlc/workflow.md`
- ADR 0010, ADR 0021, ADR 0031 and ADR 0039 (`decisions/`)
- The engine's finding `no-cpp-tooling-profile` (`E:/ImSimProject/engine/.sdlc/findings/no-cpp-tooling-profile.yaml`)
- `NOTES_process-cost_2026-10-12.md`
- `docs/distribution.md`: the plugin's channels, which the new `workflows/` folder joins (Consult case 3)
- `taskcontract/data/tasks.yaml`: the seven tasks a run reports
- `hooks/hooks.json`: the kit's shipped hooks, which the wall's hook joins (ADR 0039)

### Record

`[Intake · derived]`

(none: intake writes the record)

## Notes

`[Engineer seat · authored]`

1. The engine splits signatures from bodies: `src/*.h` and `src/*.cpp`.
2. The engine's functional tests are `tests\run_*.bat`; its unit tests build into `imsim_tests.exe`.
3. `live-run-seats` serves the interview's receipts, not a build.
4. Each team member is a workflow's own agent, not a shipped agent definition, so `sdlc-qa` stays unshipped (SC1.1).
5. After the release, the engine adds its own `test:` and `wall:` blocks in its own repository; the kit never writes them there.

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/execution-team/contract.yaml`)
