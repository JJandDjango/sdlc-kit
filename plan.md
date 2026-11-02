# Session 144 plan: rs4-abandoned, an abandoned run restarts at the task in hand on the user's word

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built by the execution team (`/sdlc execute`).
**Feature:** run-restart (contract `run-restart`): a stopped team run restarts in a fresh session from a stop record, not by `--resume`; five units, rs1 to rs5, kit 0.22.0 at rs5. rs1 merged as PR #156, rs2 as PR #157, rs3 (fresh rounds) as PR #158 at `cf23f04`.
**Unit:** `rs4-abandoned` (checks SC5.1, SC5.2): a run folder with no stop record reads as abandoned; `/sdlc execute` shows the unit and the task and waits for the user's word; on it, the leftover task file goes and the run starts at that task.

## 1. The deliverable

One draft PR holding `rs4-abandoned`, built by the team's members, with a Two-Key PASS from both verifiers and the SC5.1 manual receipt.

## 2. Where this sits

The requirements (`docs/features/run-restart.md`, r7) and design (`docs/features/run-restart.design.md`, signed on r11) are signed; the contract `specs/run-restart/contract.yaml` is ready-green; G1 passed. rs2 already reads an abandoned run: `task.py restart` prints `state` `abandoned` with the task in hand and its round, and `--go` removes a leftover task file. What is missing is the flow: `restart.md` R1 shows the record and stops ("an abandoned run starts nothing until rs4"). This unit gives R1 the question and the word, and fixes one edge in `--go`. The design's Interfaces draw the lines; this plan holds only this session's facts.

## 3. The steps

1. Branch `session-144-rs4-abandoned` off main at `cf23f04`; this plan committed and pushed.
2. write-tests: QA (`workflows/qa.js`, by `scriptPath`) drafts the tests for SC5.1 and SC5.2 from the contract, the requirements, the design and the readings in section 6, given as `pins`.
3. approve-tests, then prove-red: the QA verifier (`workflows/qa-verifier.js`) grades the draft with the same readings as `rulings`, then proves it red at the base commit through `prove.py`. The draft goes into the tree.
4. green: the Developer (`workflows/developer.js`) changes `restart.md` (R1's abandoned path: the question, the word, the no line; {answer} held `null`; R4's `--go` for an abandoned run; R6 at a task with no member) and `task.py` (`--go` keeps another unit's task file; the docstring). `execute.md` does not change.
5. The whole suite in the session. Older tests that pin the retired behavior (seen: `tests/test_fresh_rounds.py:696`, "until rs4") go to the test-retirer (`workflows/test-retirer.js`) with the Developer's files as its overlay; the session places the amended modules.
6. The usage page by hand: rs4's red paragraph (`docs/usage/the-team.md:349`) turns green with the no line, and rs2's "An abandoned run waits for rs4" (`:324`) is fixed.
7. approve-commit: `receipts.py` runs the test command; commit with the `Contract: run-restart` trailer.
8. two-key: the Dev verifier (`workflows/dev-verifier.js`), then the QA verifier with about four mutations. A FAIL returns the task to its channel with the reasons, up to three rounds.
9. The SC5.1 manual receipt, a session killed mid-task, on a toy repository (`E:/sdlc_rs4`, a fresh clone of the rs2 toy's fixture; the plugin a detached worktree of the kit at the unit's commit). Launch 1: `/sdlc execute greet greeting` headless, killed with its process tree once QA starts. Launch 2, no `--answer`: the abandoned line shows, and no `--go`, `start` or member runs; the run folder and the task file hash the same before and after. Launch 3, `--answer yes`: `restart --go`, then `start` at the task in hand, then that task's member; killed there. Written up in `RECEIPT_run-restart-rs4_2026-11-02/sc5_1_abandoned.md`, untracked.
10. Close: `progress done run-restart/rs4-abandoned`, the backlog's Next 24 updated (rs5 next), a row in `docs/session-metrics.md`, `plan.md` out, push, draft PR with the readings and the receipt's findings at its top.

## 4. Where Claude stops for the user

At the PR's review. Before it, only on a case the signed documents leave open that their purpose cannot settle, or a discovery that needs a decision. None is foreseen.

## 5. Where Claude goes on alone, and by what rule

Every step above: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The test list is Claude's, recorded `--by claude`; usage text that restates the signed design is Claude's.

## 6. Rulings needed

None. Readings from the documents' purpose, listed at the top of the PR:

- On an abandoned run R1 SHOWs `Execution was abandoned: {contract} unit {unit}, task {task}, round {n}. Restart at {task}?`, {n} being the JSON line's `round`. The word comes from `--answer` first, else from chat, as R2 reads the answer. A headless session with no `--answer` ends its turn at the question, starting nothing; the run folder and the task file stay.
- A reply that says yes restarts; any other reply is no. On no the session SHOWs `Execution did not restart: {contract} unit {unit} stays abandoned at {task}.` and STOPs with no PR; nothing is removed. The design names no line for no; this one joins its "Execution did not restart" family.
- An abandoned run has no stop question, so no answer goes to a member: {answer} is held `null` after the word, since E2 holds the raw `--answer` text.
- On yes, R4 runs `task.py restart --go`, never `--fresh`: it removes the leftover task file and writes any kept draft under {scratch}/draft. R5 and R6 then run as for a stop. At a task with no member (approve-commit, commit), the step runs as `execute.md` says, with no answer to show.
- `--go` removes the task file only when it names this unit, as the design's Sources row reads it "when its unit matches". Another unit's task file stays, and R6's `task.py start` refuses as today. Today `task.py:555` removes it whatever its unit; this is the one change to `task.py`.
- Tests run `task.py` as a command on fixture git repositories and never import its internals; flow tests are text tests on `restart.md`. SC5.1: a read-only restart of an abandoned run leaves the run folder and the task file byte-identical, and `restart.md` starts nothing before the word. SC5.2: after `--go` the task file is gone, `task.py start` at the task in hand prints its round, and R6 runs no earlier step.
- `execute.md` does not change (12,052 bytes, at its 12,000-character ceiling as the test counts); the lines `task.py start`, `end`, `fail` and `stop` print keep their wording (SC5.3); `restart.md` stays under the ceiling.

## 7. What could go wrong, already ruled

- A run still going in another session reads as abandoned (nothing marks a run live): the design's accepted risk; the word is the guard, and the question names the task.
- QA's draft hooks a name inside `task.py`: a draft that imports internals goes back to write-tests.
- The new prose fails the controlled-register check: the suite holds the `lang` tests, and a fix round is narrow.
- A whole-suite run dies when an agent returns: the session runs the suite and classifies from its output. Never two suites at once.
- The QA verifier's mutation run outlasts the 600 s Bash cap: the session runs `prove.py` with its `mutations.json` in the background, as in session 142.
- A killed headless session leaves a member's process behind: the receipt kills the whole tree (`taskkill /T /F` by the launcher's recorded PID) and checks no `claude` child stands after.

## 8. This session's cost, with its basis

About 0.9M to 1.1M agent tokens at one round each, plus about 0.4M to 0.7M cache reads in the receipt's three headless sessions. Basis: rs1 ran 1,019K, rs2 994K and rs3 1,007K (`docs/session-metrics.md`), mostly the members' fixed costs (QA about 200K, QA verifier about 260K at one round); rs2's SC2.1 receipt opened at 53.6K a turn, and these launches end at the first member. The design's 0.5M sits below every actual. Each failed round adds one member run, about 100K to 200K. The session's own context targets 200K; past 40% before step 4, the build splits there with a handoff file in `RECEIPT_run-restart-rs4_2026-11-02/`.

## 9. Not in this session

- rs5: the 50K receipts, the release, kit 0.22.0.
- `CHANGELOG.md`, `USAGE.md` and the version: rs5's release sweep.
- Next actions 18 and 19 (rs2's Dev verifier advisories; the QA verifier's opening mutation count).

## 10. Words

- **execution team**: the agents `/sdlc execute` starts to build one unit: QA, the QA verifier, the Developer and the Dev verifier.
- **Orchestrator**: the session running the team's flow; here, this session, starting each member by `scriptPath`.
- **member**: a workflow agent the flow starts for one task.
- **task**: one of seven steps of a run: write-tests, approve-tests, prove-red, green, approve-commit, commit, two-key.
- **round**: one try at a task; a FAIL returns the task to its channel with its reasons, up to 3 rounds.
- **channel**: which task a FAIL returns to: write-tests (QA's) or green (the Developer's).
- **stop record**: `stop.json`, what a stop writes so a fresh session can start where the run stopped.
- **abandoned run**: a run folder with no stop record: a session that ended mid-task, killed or closed, with nothing written.
- **the word**: the user's yes or no to `Restart at {task}?`; `--answer` when headless.
- **task file**: `{git folder}/sdlc-task.json`, the task in hand, with its unit; `task.py start` refuses every task while one stands.
- **leftover task file**: the task file an abandoned run left behind, naming its unit.
- **run folder**: `{git folder}/sdlc-run/{contract}/{unit}/`, one a unit, never committed: `run.json`, `stop.json`, `rounds.json`, `draft/`.
- **restart**: `task.py restart`, which reads the run folder and the branch and prints where the run starts or why it cannot; with `--go` it clears the stop and the leftover task file.
- **prove-red**: the task that shows the new tests fail before the code exists.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **test-retirer**: an agent that finds and amends the older tests a change makes false.
- **manual receipt**: a check run by hand on a real session, written up as evidence, where a test cannot reach.
- **toy repository**: a small throwaway repository the receipt runs the kit against, never the kit itself.
