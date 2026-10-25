| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-25 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: Johnathan Hyden |
| 2026-10-25 | Johnathan Hyden | r2: Measured: the checks before signing, on the request half: 49 findings (CL006 42, CL007 1, CL008 6); ready checks 1 to 8: 0 OPEN |
| 2026-10-25 | Johnathan Hyden | r3: The request half finished: 11 sections written, 0 OPEN |
| 2026-10-25 | Johnathan Hyden | r4: Signed: request half. The PO seat signs r3 |

# execution-team - Standard Development Workflow

`sdlc_development_kit` · seat: PO Johnathan Hyden · contract: `execution-team`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As the human developer, I want the execution node's team to ship with the kit and run in any consumer repo, so that ImSimEngine builds its units with the same workflow the kit uses.

## Description

`[PO seat · authored]`

- Execution runs at the agent model and effort of `.sdlc/workflow.md`'s execution row (Sonnet at high). The Orchestrator launches one subagent per task, a task being one of the seven steps every unit follows (`taskcontract/data/tasks.yaml`): QA for write-tests and prove-red, the Developer for green, a verifier for two-key.
- Developer: code and unit tests; cannot see the functional tests.
- QA: functional tests; it reads the code's public interface but no implementation body and no unit test.
- Dev verifier and QA verifier: each grades its own channel's work.
- A failed verifier sends Dev or QA back, up to 3 rounds. The third failed round, or a question, goes to the user through the Orchestrator.
- It ends in a draft PR for the user.
- A consumer declares its own test command, and the team runs that command where the kit's runs pytest (the engine: `test.bat`). This answers the engine's finding `no-cpp-tooling-profile`.

## Background

`[PO seat · authored]`

The kit's sessions run this team today through five workflows: `spec-channel-drafter` (QA's tests), `unit-developer`, `two-key-unit-verifier`, `test-retirer` and `live-run-seats`. They stand untracked in `.claude/workflows/`, exist only on this machine, and call pytest directly or through `prove.py` and `receipts.py`. Why now: the engine (ImSimEngine) needs the team to continue its M0 units. It has no workflows, and its stack is `cpp`, which has no tooling profile (its finding `no-cpp-tooling-profile`); it tests through `test.bat`. History: small-session-flow ruled the execution team out of its scope and into this second document (2026-10-21; `docs/features/small-session-flow.md`, Non-goals and Decisions and open questions).

### Existing behavior touched

1. The shipped agents `sdlc-developer` and `sdlc-verifier` ride the plugin with `model: inherit`. The developer binds the stack profile's `g3` and `g4-preflight` commands; a profile with no `commands:` block binds nothing (`docs/operators.md:147-156`).
2. Four workflows require `model` and `effort` arguments, read from the execution row (`.claude/workflows/spec-channel-drafter.js:11-16`, `unit-developer.js:11-16`, `test-retirer.js:11-16`, `two-key-unit-verifier.js:57-62`).
3. The drafter, developer and retirer run `python -P -m pytest tests -q -n auto` (`spec-channel-drafter.js:78`, `unit-developer.js:40`, `test-retirer.js:66`); the grader's verdict reads `receipts.py`'s exit codes (`two-key-unit-verifier.js:106-108`).
4. `sdlc-spec` and `sdlc-qa` are registered, not shipped (`docs/operators.md:34-35`).
5. `python -m taskcontract node execution` starts `claude` at the execution row's settings, the session the Orchestrator runs in (`docs/usage/node.md:15-20`).
6. The Dev/QA wall holds on one side today: `sdlc-developer` must not read acceptance-test source (`docs/operators.md:103-106`).

## Success criteria

`[PO seat · authored]`

- SC1: The team installs with the kit, with no hand copy.
- SC2: The team builds a unit in a repo whose stack is not Python, through that repo's own test command.
- SC3: The Developer reads no functional test, and QA reads no implementation body or unit test.
- SC4: A failed verifier sends work back up to 3 rounds; the third failure or a question reaches the user.
- SC5: Each build ends in a draft PR.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added.
- No mechanism substitutes one node for another.
- No full `cpp` tooling profile (format, lint, strict compile): the team needs only a declared test command.
- No G4 to G7 role for the registered `sdlc-qa` operator: this feature's QA writes functional tests only.
- No agents for the feature and design nodes: they keep their seats.
- No run of several units at once: one unit at a time.
- No merge: a run stops at the draft PR, and the user merges.

## Prerequisites

`[PO seat · authored]`

1. The execution row of `.sdlc/workflow.md` and `python -m taskcontract node execution --print` (exist).
2. Changes to agent definitions pass the enforcement-layer approval channel (exists; class E, `docs/operators.md`).

## Acceptance criteria

`[PO seat · authored]`

### Checks

SC1: installs with the kit
- SC1.1: verify that after the plugin's install or update, a consumer session can start each team member with no file copied by hand, and `sdlc-spec` and `sdlc-qa` stay registered and unshipped.
- SC1.2: verify that every file the team runs is tracked in the kit and ships in the plugin, and none stands only under the untracked `.claude/workflows/`.
- SC1.3: verify that each team member runs at the execution row's agent model and effort.

SC2: a repo that is not Python
- SC2.1: verify that the team runs the consumer's declared test command for prove-red, green and two-key, and calls pytest only where it is declared (the kit's own builds).
- SC2.2: verify that in a fixture repo whose declared test command is a batch file, one unit runs from write-tests to two-key and ends green.
- SC2.3: verify that a consumer with no declared test command starts no task and is told which declaration is missing.

SC3: the Dev/QA wall
- SC3.1: verify that the Developer's tool calls read no functional test file.
- SC3.2: verify that QA's tool calls read no implementation body and no unit test file.

SC4: three rounds, then the user
- SC4.1: verify that a verifier's FAIL sends the task back to its channel with the failure's reasons, and the next round starts from them.
- SC4.2: verify that a third failed round stops the run, puts the failures before the user, and starts no fourth round.
- SC4.3: verify that an operator's question stops its task and reaches the user through the Orchestrator.

SC5: the draft PR
- SC5.1: verify that a run whose last task passes opens a draft PR on the unit's branch, and never marks it ready or merges it.
- SC5.2: verify that a run that stops on a third failure or a question opens no PR.

Regression checks for Existing behavior touched: 1 in SC1.3 and SC2.1; 2 in SC1.3; 3 in SC2.1; 4 in SC1.1; 5 in SC1.3; 6 in SC3.1.

### Error messages, verbatim

- SC2.3: `Task {task} did not start: the repository declares no test command.`
- SC4.2: `Task {task} failed 3 rounds. The run stops here; the failures follow.`
- SC4.3: `Task {task} stopped on a question from {operator}: {question}`

## Decisions and open questions

`[PO seat · authored]`

- Execution runs on Sonnet at high (user ruling 2026-10-21, carried from small-session-flow).
- Retry cap is 3 rounds per task; the 5 loops inside one check stay (user ruling 2026-10-21, carried).
- Operators apply to execution only; the document stages use seats (user ruling 2026-10-21, carried).
- Open: whether the QA verifier runs mostly through `prove.py` (recommended, not ratified).
- Open: whether the Sonnet ruling supersedes the 2026-10-12 process-cost ruling in an ADR.

## Notes

`[PO seat · authored]`

Carried from small-session-flow: the existing behavior of the 5-loop caps (`agents/sdlc-developer.md:72`, `agents/sdlc-verifier.md:62`) and of the Opus 5.5 ruling (`NOTES_process-cost_2026-10-12.md:110`).

## Appendix

### Gherkin

`[PO seat · derived from r3]`

```gherkin
Scenario: SC1.1 Each team member starts after the plugin's install
  Given a consumer repo with the kit's plugin installed or updated, and no file copied by hand
  When a session starts each team member
  Then each one starts, and sdlc-spec and sdlc-qa stay registered and unshipped

Scenario: SC1.2 Every file the team runs ships in the plugin
  Given the kit's tracked files and its plugin
  When the files the team runs are listed
  Then each is tracked and ships in the plugin, and none stands only under .claude/workflows/

Scenario: SC1.3 Each team member runs at the execution row's settings
  Given the execution row's agent model and effort
  When each team member runs
  Then it runs at that agent model and effort

Scenario: SC2.1 The team runs the declared test command
  Given a consumer with a declared test command
  When the team runs prove-red, green and two-key
  Then each runs the declared command, and pytest runs only where it is declared

Scenario: SC2.2 A batch-file repo builds one unit
  Given a fixture repo whose declared test command is a batch file
  When the team runs one unit from write-tests to two-key
  Then the unit ends green

Scenario: SC2.3 No declared test command starts no task
  Given a consumer with no declared test command
  When the team is asked to start a task
  Then no task starts, and it prints "Task {task} did not start: the repository declares no test command."

Scenario: SC3.1 The Developer reads no functional test
  Given a unit with functional tests
  When the Developer runs its task
  Then its tool calls read no functional test file

Scenario: SC3.2 QA reads no implementation body or unit test
  Given a unit with code and unit tests
  When QA runs its tasks
  Then its tool calls read no implementation body and no unit test file

Scenario: SC4.1 A FAIL sends the task back with its reasons
  Given a task whose verifier grades FAIL
  When the round ends
  Then the task goes back to its channel with the failure's reasons, and the next round starts from them

Scenario: SC4.2 A third failed round stops the run
  Given a task that has failed two rounds
  When its third round fails
  Then the run prints "Task {task} failed 3 rounds. The run stops here; the failures follow." and the failures, and no fourth round starts

Scenario: SC4.3 A question stops its task
  Given an operator running a task
  When it asks a question
  Then its task stops, and the Orchestrator prints "Task {task} stopped on a question from {operator}: {question}"

Scenario: SC5.1 A passing run opens a draft PR
  Given a run whose last task passes
  When the run ends
  Then a draft PR opens on the unit's branch, and it is neither marked ready nor merged

Scenario: SC5.2 A stopped run opens no PR
  Given a run that stops on a third failure or a question
  When the run ends
  Then no PR opens
```

### Terms

`[PO seat · authored]`

Decided at the interview's Q14 (2026-10-25). Used as ratified: Task, Round, Node, Agent model, Workflow file, Seat (`intake-seat`, by its alias) and Two-Key; Developer and QA are the roster's developer and qa that the ratified Operator names. One amendment and seven new terms to ratify at intake:

- **Operator** (amends `operator`): the roster of four (spec, developer, qa, verifier) gains a fifth, the Orchestrator.
- **Orchestrator**: The operator that runs a unit's tasks: it launches one subagent per task, sends a failed task back to its channel, and puts a third failed round or a question before the user.
- **Dev verifier**: The verifier convened on the Developer's work.
- **QA verifier**: The verifier convened on QA's work.
- **Functional test**: A test QA writes that checks a unit's behavior through its public interface.
- **Unit test**: A test the Developer writes beside the code it checks.
- **Public interface**: The names, parameters, return types, commands and options a test calls, without any implementation body.
- **Test command**: The command a repository declares to run its tests (the kit: pytest on workers; the engine: `test.bat`).
