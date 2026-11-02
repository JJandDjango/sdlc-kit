# Session 143 plan: rs3-fresh-rounds, an answer ruled enough gives a task three fresh rounds

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built by the execution team (`/sdlc execute`).
**Feature:** run-restart (contract `run-restart`): a stopped team run restarts in a fresh session from a stop record, not by `--resume`; five units, rs1 to rs5, kit 0.22.0 at rs5. rs1 (the stop record) merged as PR #156, rs2 (the restart) as PR #157 at `8c492dd`.
**Unit:** `rs3-fresh-rounds` (checks SC3.1, SC3.2, SC3.3): after a third FAIL, an answer the user rules enough (`--enough`) restarts the task at round 1 with three fresh rounds; an answer ruled not enough starts nothing and keeps the stop record.

## 1. The deliverable

One draft PR holding `rs3-fresh-rounds`, built by the team's members, with a Two-Key PASS from both verifiers.

## 2. Where this sits

The requirements (`docs/features/run-restart.md`, r7) and design (`docs/features/run-restart.design.md`, signed on r11) are signed; the contract `specs/run-restart/contract.yaml` is ready-green; G1 passed. rs2 built the restart: `task.py restart` (read-only and `--go`), `skills/sdlc/flows/restart.md`, `--answer` and each member's `answer`. Today a stop of kind `fail` (a third FAIL) shows its record and starts nothing (`restart.md` R1). This unit adds the second question, `--enough`, and `task.py restart --go --fresh`, which clears the stopped task's failed rounds. The design's Interfaces draw the commands and lines; this plan holds only this session's facts.

## 3. The steps

1. Branch `session-143-rs3-fresh-rounds` off main at `8c492dd`; this plan committed and pushed.
2. write-tests: QA (`workflows/qa.js`, by `scriptPath`) drafts the tests for SC3.1 to SC3.3 from the contract, the requirements, the design and the readings in section 6, given as `pins`.
3. approve-tests, then prove-red: the QA verifier (`workflows/qa-verifier.js`) grades the draft with the same readings as `rulings`, then proves it red at the base commit through `prove.py`. The draft goes into the tree.
4. green: the Developer (`workflows/developer.js`) changes `task.py` (`--fresh` on `restart --go`, its usage error, the docstring) and `restart.md` (R1's `fail` path: the second question, `--enough`, the not-enough line, `--fresh` at R4, the member rule after a FAIL). `execute.md` does not change.
5. The whole suite in the session. Older tests that pin the retired behavior (seen: `tests/test_restart.py:1040`, "restarts nothing until the enough ruling exists") go to the test-retirer (`workflows/test-retirer.js`) with the Developer's files as its overlay; the session places the amended modules.
6. The usage page by hand: rs3's red paragraph (`docs/usage/the-team.md:342`) turns green, and rs2's "A stop after a third FAIL waits for rs3" (`:324`) is fixed.
7. approve-commit: `receipts.py` runs the test command; commit with the `Contract: run-restart` trailer.
8. two-key: the Dev verifier (`workflows/dev-verifier.js`), then the QA verifier with about four mutations. A FAIL returns the task to its channel with the reasons, up to three rounds.
9. Close: `progress done run-restart/rs3-fresh-rounds`, the backlog's Next 24 updated (rs4 next), a row in `docs/session-metrics.md`, `plan.md` out, push, draft PR with the readings at its top.

## 4. Where Claude stops for the user

At the PR's review. Before it, only on a case the signed documents leave open that their purpose cannot settle, or a discovery that needs a decision. None is foreseen.

## 5. Where Claude goes on alone, and by what rule

Every step above: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The test list is Claude's, recorded `--by claude`; usage text that restates the signed design is Claude's.

## 6. Rulings needed

None. Readings from the documents' purpose, listed at the top of the PR:

- `restart.md` reads `--enough` from the invocation, as R2 reads `--answer`; `execute.md` stands at 11,991 of its 12,000 characters and does not change.
- Only a stop of kind `fail` asks the second question, after the answer: `Is that answer enough to give {task} three fresh rounds?`. `--enough` answers yes. An interactive session asks in chat; a headless one with no `--enough` ends its turn there, starting nothing, and the stop record stays. `--enough` on any other stop is unused.
- Yes: R4 runs `task.py restart --go --fresh`. `--fresh` clears the failed rounds of the stopped task's channel in `rounds.json`, so the next `task.py start` there prints round 1, and the third fresh FAIL stops the run again. The other channel's count stays.
- No: the session shows `Execution did not restart: {contract} unit {unit} stays stopped at {task}. The design may need revisiting.` and stops with no PR. No `--go` runs, so `stop.json` and `rounds.json` stay.
- `--fresh` without `--go` is a usage error, exit 2, like `--go` without `--scratch`.
- After a third FAIL the stopped task is its channel (write-tests or green), and that channel's member, QA or the Developer, takes the answer. The stop record's operator names the verifier or receipts whose FAIL was the third, so R6's "no member" rule reads the task, not that operator. The member's `reasons` start at `[]` (round 1); the reasons ride in the answer's `stopped`.
- Tests run `task.py` as a command on fixture git repositories and never import its internals; flow tests are text tests on `restart.md`. SC3.2 is shown by `fail` after `--go --fresh`: the first and second fresh fails return 0, the third returns 1 and writes a new stop record.
- The lines `task.py start`, `end`, `fail` and `stop` print today keep their wording (SC5.3); `restart.md` stays under the 12,000-character ceiling.

## 7. What could go wrong, already ruled

- `execute.md` would pass its ceiling: it does not change; the restart's steps stay in `restart.md`.
- A fresh restart loops: each restart takes the user's enough ruling; nothing grants fresh rounds alone.
- QA's draft hooks a name inside `task.py`: a draft that imports internals goes back to write-tests.
- The new prose fails the controlled-register check: the suite holds the `lang` tests, and a fix round is narrow.
- A whole-suite run dies when an agent returns: the session runs the suite and classifies from its output. Never two suites at once.
- The QA verifier's mutation run outlasts the 600 s Bash cap: as in session 142, the session runs `prove.py` with its `mutations.json` in the background.

## 8. This session's cost, with its basis

About 0.7M to 0.9M agent tokens at one round each. Basis: rs1 ran 1,019K and rs2 994K (`docs/session-metrics.md`), mostly the members' fixed costs (QA about 200K, QA verifier about 260K); rs3's change is smaller and has no manual receipt. The design's 0.4M sits below both actuals. Each failed round adds one member run, about 100K to 200K. The session's own context targets 200K; past 40% before step 4, the build splits there with a handoff file in `RECEIPT_run-restart-rs3_2026-11-02/`.

## 9. Not in this session

- rs4 and rs5: the abandoned path, the 50K receipts, the release.
- `CHANGELOG.md`, `USAGE.md` and the version: rs5's release sweep.
- Next actions 18 (rs2's Dev verifier advisories).

## 10. Words

- **execution team**: the agents `/sdlc execute` starts to build one unit: QA, the QA verifier, the Developer and the Dev verifier.
- **Orchestrator**: the session running the team's flow; here, this session, starting each member by `scriptPath`.
- **member**: a workflow agent the flow starts for one task.
- **task**: one of seven steps of a run: write-tests, approve-tests, prove-red, green, approve-commit, commit, two-key.
- **round**: one try at a task; a FAIL returns the task to its channel with its reasons, up to 3 rounds.
- **channel**: which task a FAIL returns to: write-tests (QA's) or green (the Developer's).
- **third FAIL**: the third failed round of one channel; the run stops with a stop record of kind `fail`.
- **fresh rounds**: three new rounds for a stopped task, counted from 1, given only on an answer the user rules enough.
- **enough**: the user's ruling that the answer gives the task a fair chance at three fresh rounds; `--enough` when headless.
- **stop record**: `stop.json`, what a stop writes so a fresh session can start where the run stopped.
- **run folder**: `{git folder}/sdlc-run/{contract}/{unit}/`, one a unit, never committed: `run.json`, `stop.json`, `rounds.json`, `draft/`.
- **rounds.json**: each channel's failed reasons for the unit; `task.py start` counts the round from it.
- **restart**: `task.py restart`, which reads the run folder and the branch and prints where the run starts or why it cannot; with `--go` it clears the stop.
- **prove-red**: the task that shows the new tests fail before the code exists.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **test-retirer**: an agent that finds and amends the older tests a change makes false.
