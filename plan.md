# Session 139 plan: rs1-stop-record, a stop writes a stop record

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built by the execution team (`/sdlc execute`).
**Feature:** run-restart (contract `run-restart`): a stopped team run restarts in a fresh session from a stop record, not by `--resume`; five units, rs1 to rs5, kit 0.22.0 at rs5.
**Unit:** `rs1-stop-record` (checks SC1.1 to SC1.3): every stop writes `stop.json` in the unit's run folder, and the run ends with no PR and no task file.

## 1. The deliverable

One draft PR holding `rs1-stop-record`, built by the team's members, with a Two-Key PASS from both verifiers.

## 2. Where this sits

The requirements (`docs/features/run-restart.md`, r4) and design (`docs/features/run-restart.design.md`, signed at r9) are signed; the contract `specs/run-restart/contract.yaml` is ready-green (PR #155, merged at `24362f2`). Today `task.py stop` and a third `fail` delete the task file and the rounds file (`workflows/tools/task.py:211, 235, 246`), so a stopped run keeps nothing. This unit makes each stop leave a record; rs2 then restarts from it. The design's Interfaces and Sources sections draw the files and commands; this plan holds only this session's facts.

## 3. The steps

1. Branch `session-139-rs1-stop-record` off main; this plan committed and pushed.
2. Pass 0, by hand: `docs/usage/the-team.md` gains its restart section, every line red, restating the design (the stop record, the run folder, the restart, fresh rounds, the abandoned run, the 50K start). Own commit.
3. write-tests: QA (`workflows/qa.js`, by `scriptPath`) drafts the tests for SC1.1 to SC1.3 from the contract, the requirements and the design.
4. approve-tests, then prove-red: the QA verifier (`workflows/qa-verifier.js`) grades the draft, then proves it red at the base commit through `prove.py`. The draft goes into the tree.
5. green: the Developer (`workflows/developer.js`) changes `task.py` (the run folder, `stop.json`, `rounds.json`, `stop --unit --kind`, `end --run --unit`) and `skills/sdlc/flows/execute.md` (the new options, and a refused start that stops with a record), keeping `execute.md` under its 12,000-character ceiling.
6. The whole suite in the session. Older tests that pin the retired behavior (seen: `tests/test_rounds.py`, `tests/test_flow_fixes.py`'s drawn `stop` options) go to the test-retirer (`workflows/test-retirer.js`) with the Developer's files as its overlay; the session places the amended modules.
7. The usage page by hand: rs1's red lines turn green, and the three "removes both files" sentences (`docs/usage/the-team.md:203-226`) say what the code now does.
8. approve-commit: `receipts.py` runs the test command; commit with the `Contract: run-restart` trailer.
9. two-key: the Dev verifier (`workflows/dev-verifier.js`), then the QA verifier with its mutations. A FAIL returns the task to its channel with the reasons, up to three rounds.
10. Close: `progress done run-restart/rs1-stop-record`, the backlog's Next 24 updated (rs2 next), a row in `docs/session-metrics.md`, `plan.md` out, push, draft PR.

## 4. Where Claude stops for the user

At the PR's review. Before it, only on a case the signed documents leave open that their purpose cannot settle, or a discovery that needs a decision. None is foreseen.

## 5. Where Claude goes on alone, and by what rule

Every step above: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The test list is Claude's, recorded `--by claude`; usage text that restates the signed design is Claude's.

## 6. Rulings needed

None. Readings from the documents' purpose, listed at the top of the PR:

- rs1 builds what SC1.1 to SC1.3 and its Retirements cell need: `stop.json`, `rounds.json` in the run folder, `stop --unit --kind`, `end --run --unit`, the refused-start stop. `run.json`, `task.py keep`, `task.py restart` and the task file's `unit` wait for rs2, whose SC2.1 reads them.
- `fail` takes an optional `--operator`, which the flow passes: the flow removes the task file before `fail`, and the design's stop sample names the operator. Without it the field is null.
- A stop's round is 1 plus the failed rounds of the task's channel, as `start` counts it, since the task file is gone when `stop` runs (Sources, "Round n").
- A refusal stop prints no line of its own: `start`'s refusal line already showed why, and the design adds no new printed line. A question or an error prints today's line.
- With no git repository, `stop` writes no record and prints as today; no run folder can exist.
- A `--unit` whose contract or unit half is empty, `.` or `..`, or holds a slash or a backslash is a usage error (exit 2): the run folder must stay inside the git folder.
- A round with no reason is written `""` in `reasons`, as the design's sample shows.
- `rounds.json` is written whole by `os.replace`, as `run.json` and `stop.json` are: it moves into the same folder, and a half-written file would lose a count.
- An old `sdlc-rounds.json` left by kit 0.21.x is never read or removed.

## 7. What could go wrong, already ruled

- `execute.md` passes 12,000 characters: the Developer trims elsewhere, as the design's Constraints say; the ceiling test holds it.
- QA's draft hooks a name inside `task.py`: the tests run `task.py` as a command on fixture repositories, as the design's Units cell says; a draft that imports internals goes back to write-tests.
- The new prose fails the controlled-register check: the suite holds the `lang` tests, and a fix round is narrow.
- A whole-suite run dies when an agent returns: the session runs the suite and classifies from its output. Never two suites at once.
- The QA verifier's mutation run outlasts a Bash call: it runs from this interactive session by `scriptPath`, never headless (a headless session kills a waiting workflow after 10 minutes).

## 8. This session's cost, with its basis

About 0.5M to 0.8M agent tokens at one round each: the design's estimate for rs1 is 0.5M, and the execution team's rows in `docs/session-metrics.md` (e1 to e4, on the same files) ran 0.49M to 0.81M. Each failed round adds one member run, about 100K to 200K. The session's own context targets 200K; if it passes 40% before step 5, the build splits there with a handoff file in the receipt folder.

## 9. Not in this session

- rs2 to rs5, and `run.json`, `keep`, `restart`, `restart.md`, the members' `answer` argument.
- `CHANGELOG.md`, `USAGE.md` and the version: rs5's release sweep.
- Next actions 11 (e2's and e3's advisories).

## 10. Words

- **execution team**: the agents `/sdlc execute` starts to build one unit: QA, the QA verifier, the Developer and the Dev verifier.
- **Orchestrator**: the session running the team's flow; here, this session, starting each member by `scriptPath`.
- **member**: a workflow agent the flow starts for one task.
- **task**: one of seven steps of a run: write-tests, approve-tests, prove-red, green, approve-commit, commit, two-key.
- **round**: one try at a task; a FAIL returns the task to its channel with its reasons, up to 3 rounds.
- **channel**: which task a FAIL returns to: write-tests (QA's) or green (the Developer's).
- **task file**: `{git folder}/sdlc-task.json`, the running task; while it stands, the wall holds a member's calls.
- **wall**: a hook that keeps the Developer from the functional tests and QA from the code while a task runs.
- **stop**: the run ends early on a member's question or error, a refused task start, or a third FAIL.
- **stop record**: `stop.json`, what a stop writes so a fresh session can start where the run stopped.
- **run folder**: `{git folder}/sdlc-run/{contract}/{unit}/`, one a unit, never committed.
- **rounds file**: the failed reasons a task; today `sdlc-rounds.json`, after this unit `rounds.json` in the run folder.
- **prove-red**: the task that shows the new tests fail before the code exists.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **test-retirer**: an agent that finds and amends the older tests a change makes false.
