| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-29 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: Johnathan Hyden |
| 2026-10-30 | Johnathan Hyden | r2: Measured: the checks before signing, on the request half: 62 findings (CL003 2, CL006 53, CL008 7); ready checks 1 to 8: 2 OPEN |
| 2026-10-30 | Johnathan Hyden | r3: Measured: the checks before signing, on the request half: 57 findings (CL006 50, CL008 7); ready checks 1 to 8: 0 OPEN |
| 2026-10-30 | Johnathan Hyden | r4: The request half finished: 11 sections written, 0 OPEN |
| 2026-10-30 | Johnathan Hyden | r5: Signed: request half. The PO seat signs r4 |

# run-restart - Restart a stopped run in a fresh session

`sdlc_development_kit` · seat: PO Johnathan Hyden · contract: `run-restart`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As the human developer, I want a stopped team run to start again in a fresh session at the task where it stopped, so that the restart begins near a first launch's 45K tokens of context instead of carrying the stopped session's whole context.

## Description

`[PO seat · authored]`

A stop writes a stop record: the unit, the task, the round counts, and the question or the FAIL reasons. `/sdlc execute` reads the stop record, the progress records and the branch, shows the stop, and asks the user for an answer, the ruling for every stop (a member's question or error, a task's third failed round, a task `task.py start` refused). The run then starts at the stopped task, with the answer handed to it. After a third failed round, the user first judges why the task failed: an answer enough to restart gives the task three fresh rounds; otherwise the run does not restart, and the design may need revisiting. A run abandoned mid-task (the session killed, crashed or out of context) writes no stop record. `/sdlc execute` finds it from what the run left, shows what it found, and on the user's word starts again at the task that was running.

## Background

`[PO seat · authored]`

`task.py stop` and a third failed round remove the task file and the rounds file, so a stopped run keeps no state. Session 129 went on by `--resume`, and the headless session's starting context grew from 45K to 281K tokens over eight runs (31.0M cache reads).

### Existing behavior touched

- `task.py stop` removes the task file and the rounds file (`workflows/tools/task.py:242-246`).
- A task's third failed round, `task.py fail`, removes both files and exits 1 (`workflows/tools/task.py:220-235`).
- `/sdlc execute` always starts a unit at the write-tests task, round 1 (`skills/sdlc/flows/execute.md:25-34`).
- The run holds QA's interface note, its draft and the base commit only in the session (and the draft in its scratch folder), so a fresh session has none of them; the Developer's green task reads the note (`skills/sdlc/flows/execute.md:25, 34, 46`).

## Success criteria

`[PO seat · authored]`

- SC1: Every stop (a member's question or error, a third failed round, a refused task start) leaves a stop record naming the unit, the task, the round counts, and the question or the FAIL reasons.
- SC2: A restart in a fresh session starts at the stopped task with the user's answer, and redoes no task the run finished before the stop.
- SC3: After a third failed round, an answer the user rules enough gives the task three fresh rounds; one the user rules not enough starts nothing.
- SC4: A restart's starting context is at most 50K tokens (a first launch's is near 45K).
- SC5: A run abandoned mid-task restarts in a fresh session at the task that was running, on the user's word.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added.
- A member that waits on the parent, since a headless session kills a waiting workflow after 10 minutes and keeps its whole context.
- A restart without the user's answer: the run never relaunches itself in a loop.
- A restart on another machine or another branch than the one the run stopped on.

## Prerequisites

`[PO seat · authored]`

e6 shipped the team in 0.21.0 (met; 0.21.1 is current).

## Acceptance criteria

`[PO seat · authored]`

### Checks

SC1:
- SC1.1: verify that a member's question or error, or a task start `task.py start` refuses, stops the run with a stop record naming the unit, the task, the round counts and the question, error or refusal.
- SC1.2: verify that a task's third failed round leaves a stop record naming the unit, the task, the round counts and each round's FAIL reasons.
- SC1.3: verify that after any stop the run ends with no PR and no task file left, so the wall holds no call.

SC2:
- SC2.1: verify that after a stop at the green task, a restart in a fresh session starts at green with QA's interface note and test file, and runs no earlier task again.
- SC2.2: verify that the restarted task's member receives the user's answer together with the stop record's question or FAIL reasons.
- SC2.3: verify that a restart on a branch other than the run's starts nothing and shows the wrong-branch message.

SC3:
- SC3.1: verify that after a third failed round, an answer the user rules enough restarts the task at round 1.
- SC3.2: verify that a task restarted this way stops again only after three more failed rounds.
- SC3.3: verify that an answer the user rules not enough starts no task and leaves the stop record in place.

SC4:
- SC4.1: verify that a restart's first turn in a fresh headless session holds at most 50K tokens of context.
- SC4.2: verify that a restart reads no transcript of the stopped session: only the stop record, the progress records and the branch.
- SC4.3: verify that the fourth restart of one unit still starts at most 50K tokens, so restarts do not grow the context the way session 129's eight `--resume` runs did.

SC5:
- SC5.1: verify that after a session dies mid-task, `/sdlc execute` finds the abandoned run, shows the unit and the task that was running, and starts nothing before the user's word.
- SC5.2: verify that on the user's word the restart starts at the task that was running and redoes no task the run finished before it.
- SC5.3: verify that with no stop record and no abandoned run, `/sdlc execute` starts the unit at write-tests, round 1, as today.

### Error messages, verbatim

- SC2.2: `Execution stopped: {contract} unit {unit}, task {task}, round {n} of 3: {question or reasons}. Your answer?`
- SC3.3: `Execution did not restart: {contract} unit {unit} stays stopped at {task}. The design may need revisiting.`
- SC5.1: `Execution was abandoned: {contract} unit {unit}, task {task}, round {n}. Restart at {task}?`
- SC2.3: `Execution did not restart: the run stopped on branch {branch}; this session is on {current}.`

## Decisions and open questions

`[PO seat · authored]`

It ships in `/sdlc execute`, not as a personal skill.

## Notes

`[PO seat · authored]`

(none)

## Appendix

### Gherkin

`[PO seat · derived from r4]`

```gherkin
Scenario: SC1.1 A question, an error or a refused start stops the run with a record
  Given a run of a unit at a task
  When the task's member returns a question or an error, or task.py start refuses to open the task
  Then the run stops
  And a stop record names the unit, the task, the round counts and the question, error or refusal

Scenario: SC1.2 A third failed round leaves a stop record
  Given a run whose task has failed two rounds
  When the task fails its third round
  Then a stop record names the unit, the task, the round counts and each round's FAIL reasons

Scenario: SC1.3 A stop leaves no PR and no task file
  Given a run of a unit
  When the run stops
  Then the run opens no PR
  And no task file is left, so the wall holds no call

Scenario: SC2.1 A restart at green hands over QA's work and redoes no earlier task
  Given a run stopped at the green task
  When a restart runs in a fresh session
  Then the run starts at green
  And the Developer receives QA's interface note and test file from the stopped run
  And no earlier task runs again

Scenario: SC2.2 The restarted member receives the answer and the stop
  Given a stopped run and its stop record
  When the restart shows "Execution stopped: {contract} unit {unit}, task {task}, round {n} of 3: {question or reasons}. Your answer?"
  And the user answers
  Then the restarted task's member receives the user's answer and the stop record's question or FAIL reasons

Scenario: SC2.3 A restart on another branch starts nothing
  Given a run stopped on branch {branch}
  When a restart runs on branch {current}
  Then no task starts
  And the session shows "Execution did not restart: the run stopped on branch {branch}; this session is on {current}."

Scenario: SC3.1 An answer ruled enough restarts the task at round 1
  Given a task stopped after its third failed round
  When the user rules the answer enough
  Then the task restarts at round 1

Scenario: SC3.2 A restarted task stops again only after three more failed rounds
  Given a task restarted at round 1 after a third failed round
  When the task fails two fresh rounds
  Then the run goes on to a third fresh round
  When the third fresh round fails
  Then the run stops

Scenario: SC3.3 An answer ruled not enough starts nothing
  Given a task stopped after its third failed round
  When the user rules the answer not enough
  Then no task starts
  And the stop record stays in place
  And the session shows "Execution did not restart: {contract} unit {unit} stays stopped at {task}. The design may need revisiting."

Scenario: SC4.1 A restart starts at most 50K tokens
  Given a stopped run
  When a restart runs in a fresh headless session
  Then its first turn holds at most 50K tokens of context

Scenario: SC4.2 A restart reads no transcript of the stopped session
  Given a stopped run and the stopped session's transcript
  When a restart runs
  Then it reads the stop record, the progress records and the branch
  And it reads no transcript of the stopped session

Scenario: SC4.3 The fourth restart still starts at most 50K tokens
  Given a unit restarted three times
  When it restarts a fourth time
  Then the restart's first turn holds at most 50K tokens of context

Scenario: SC5.1 An abandoned run is shown and waits for the user's word
  Given a run whose session died mid-task, with no stop record
  When /sdlc execute runs for the unit in a fresh session
  Then the session shows "Execution was abandoned: {contract} unit {unit}, task {task}, round {n}. Restart at {task}?"
  And no task starts before the user's word

Scenario: SC5.2 On the user's word, the abandoned task starts again
  Given an abandoned run shown to the user
  When the user gives the word
  Then the restart starts at the task that was running
  And no task the run finished before it runs again

Scenario: SC5.3 A unit with nothing to restart starts as today
  Given a unit with no stop record and no abandoned run
  When /sdlc execute runs
  Then the unit starts at write-tests, round 1
```

### Terms

`[PO seat · authored]`

- team run: one `/sdlc execute` of one unit by the execution team, from its first task until it passes or stops.
- stopped run: a team run that ended short of a pass: a member's question or error, a task's third failed round, or a task start `task.py start` refuses.
- stop record: the file a stop writes so a fresh session can start where the run stopped.
- abandoned run: a team run whose session ended mid-task with no stop written: killed, crashed or out of context.
- restart: an `/sdlc execute` in a fresh session that starts a stopped or abandoned run again at the task where it ended.
