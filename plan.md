# Session 145 plan: rs5-release, the restart's starting context measured and kit 0.22.0 shipped

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built by the execution team (`/sdlc execute`).
**Feature:** run-restart (contract `run-restart`): a stopped team run restarts in a fresh session from a stop record, not by `--resume`; five units, rs1 to rs5. rs1 to rs4 are on main (PRs #156 to #159, the last at `e8d33b9`).
**Unit:** `rs5-release` (checks SC4.1, SC4.2, SC4.3): a headless restart's first turn holds at most 50K tokens, the fourth restart of one unit too, and kit 0.22.0 ships.

## 1. The deliverable

One draft PR holding `rs5-release`: the restart reading the progress records as the design's Sources row says, the 0.22.0 release files, a Two-Key PASS from both verifiers, and the SC4.1 and SC4.3 manual receipt.

## 2. Where this sits

The requirements (`docs/features/run-restart.md`, r7) and design (`docs/features/run-restart.design.md`, signed on r11) are signed; the contract `specs/run-restart/contract.yaml` is ready-green and unchanged since `025fdc4`; G1.3 stands. One signed line is not built: the Sources row "The tasks already finished" (`run-restart.design.md:107`) has the restart read the progress records, with `run.json` winning and a disagreeing record shown in one line. `task.py restart` reads none today (backlog Next actions 18). SC4.2's check names the progress records among the restart's only sources, so this unit builds the row; `task.py`, `restart.md` and `tests/` are in the contract's scope, so no re-intake. The receipts' streams already show the scale: a fresh session's first request is 40.0K in all four rs2 and rs4 launches.

## 3. The steps

1. Branch `session-145-rs5-release` off main at `e8d33b9`; this plan committed and pushed.
2. write-tests: QA (`workflows/qa.js`, by `scriptPath`) drafts the tests for SC4.2 from the contract, the requirements, the design and the readings in section 6, given as `pins`.
3. approve-tests, then prove-red: the QA verifier (`workflows/qa-verifier.js`) grades the draft with the same readings as `rulings`, then proves it red at the base commit through `prove.py`. The draft goes into the tree.
4. green: the Developer (`workflows/developer.js`) changes `task.py` (`restart` reads `.sdlc/progress/{contract}.yaml` through `taskcontract.progress.read_progress`; its JSON line gains `progress`; `--go`'s help text at `task.py:200` says it removes the task file only when it names the unit) and `restart.md` (R1 and R2 show each `progress` line). `execute.md` does not change.
5. The whole suite in the session. Older tests that pin `restart`'s JSON line go to the test-retirer (`workflows/test-retirer.js`) with the Developer's files as its overlay; the session places the amended modules.
6. approve-commit: `receipts.py` runs the test command; commit with the `Contract: run-restart` trailer.
7. two-key: the Dev verifier (`workflows/dev-verifier.js`), then the QA verifier with about four mutations. A FAIL returns the task to its channel with the reasons, up to three rounds.
8. The release by hand, as e6's: `pyproject.toml` and `skills/sdlc/init.py` (`KIT_VERSION`) read 0.22.0; `CHANGELOG.md` gains the 0.22.0 entry (rs1 to rs5); `USAGE.md` and `docs/usage/the-team.md` turn rs5's markers green. The suite runs green; the Dev verifier grades the release commit.
9. The SC4.1 and SC4.3 manual receipt on a toy (`E:/sdlc_rs5`, a fresh clone of the rs4 toy's fixture; the plugin a detached worktree of the kit at the release commit). Four rounds of: a stop at green built by hand with the unit's `task.py` (`start`, then `stop --kind question` with the same question each time), then a headless `/sdlc execute greet greeting --answer "{same text}"`, killed with its process tree once the Developer launches (`launch.py --kill-at-member`), the toy's tree restored. Each stream gives the first request's context and the context at the member launch; `context_breakdown.py` reads the first and the fourth restart's transcripts. Written up in `RECEIPT_run-restart-rs5_2026-11-02/sc4_restarts.md`, untracked.
10. Close: `progress done run-restart/rs5-release`, the backlog's Next 24 closed (the self-pin next), a row in `docs/session-metrics.md`, `plan.md` out, push, draft PR with the readings and the receipt's findings at its top. After the user merges and tags `v0.22.0`: the self-pin PR (`.github/workflows/sdlc.yml` and the pinned install lines), the 0.21.1 shape (PR #151).

## 4. Where Claude stops for the user

At the PR's review, and at the tag, which the user pushes. Before them, only on a case the signed documents leave open that their purpose cannot settle, or a discovery that needs a decision; a third failed round is one.

## 5. Where Claude goes on alone, and by what rule

Every step above: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The test list is Claude's, recorded `--by claude`; the release files are hand edits the Dev verifier grades.

## 6. Rulings needed

None. Readings from the documents' purpose, listed at the top of the PR:

- "First turn" (SC4.1, SC4.3) is the first request's context: input plus cache read plus cache write on the session's first assistant message. That is the point where session 129's 45K and 281K were read, since `--resume` carries the old transcript into the first request. The receipt also records the context at the first member launch (rs2's receipt read 53.6K there, after `execute.md` and `restart.md`) as evidence, not as the bar.
- "Never grows" (SC4.3): with the same question and answer text, the fourth restart's first request is within 1K of the first's.
- The restart reads the progress records of its contract only. A task before the task in hand, in the seven tasks' order, whose latest record is missing or reads other than `done`, disagrees. Tasks at or after the task in hand are not compared: after a FAIL, a later task's old record stands, and the task in hand may read `done` from an earlier round.
- `restart`'s JSON line gains `progress`: a list of one-line strings, one a disagreeing record, `[]` when all agree, and `[]` for state `none`. Each reads `Progress record disagrees: {task} reads {state}, but the run is at {task in hand}.`, {state} being `doing`, `blocked` or `no record`. `run.json` wins: the restart starts at the same task as before, exit 0.
- R1 and R2 SHOW each `progress` line, before the question. `--go` prints the same line as the read.
- Tests run `task.py` as a command on fixture git repositories and never import its internals; flow tests are text tests on `restart.md`. SC4.2's text test: `restart.md` names the run folder, the progress records and the branch as its sources, and no transcript, `--resume` or `--continue`.
- `execute.md` does not change (11,991 of its 12,000 characters); the lines `task.py start`, `end`, `fail` and `stop` print keep their wording (SC5.3); `restart.md` (4,936 characters) stays under the ceiling.

## 7. What could go wrong, already ruled

- Older tests compare `restart`'s whole JSON line: the test-retirer amends them to the new field, as rs2's retirer did.
- The new prose fails the controlled-register check: the suite holds the `lang` tests, and a fix round is narrow.
- The QA verifier opens two-key with more mutations than the 600 s Bash cap holds (Next actions 19): its prompt asks for four; if a run is killed, the session runs `prove.py` with its `mutations.json` in the background.
- A whole-suite run dies when an agent returns: the session runs the suite and classifies from its output. Never two suites at once.
- A killed restart leaves the Developer's edits in the toy: the toy's tree is restored by `git checkout` and its task file removed by the next hand `stop` before the next launch; the receipt checks `git status` is clean before each.
- A killed headless session leaves a child process: the launcher kills the whole tree (`taskkill /T /F`) and the receipt checks no `claude` child stands after.

## 8. This session's cost, with its basis

About 0.7M to 1.0M agent tokens for the team at one round each, plus 0.1M to 0.15M for the release's Dev verifier, plus about 1.6M to 2.0M cache reads in the receipt's four headless sessions. Basis: rs4 ran 634K and rs1 to rs3 about 1.0M each (`docs/session-metrics.md`); e5's Dev verifier took about 146K; rs4's three headless launches read 1.40M over 7 to 13 messages each. The design's 0.75M sits below the actuals. Each failed round adds one member run, about 100K to 200K. Past 40% of this session's window before step 8, the build splits there with a handoff file in `RECEIPT_run-restart-rs5_2026-11-02/`.

## 9. Not in this session

- The self-pin PR: after the user's tag.
- Next actions 18 to 20's other advisories: `keep --value`'s quoting rule, `--answer` with no stop record, `end --run`'s empty contract folder, `test.file` without `-n auto`, `--fresh` on any stop, `--enough` absent from `execute.md`, the not-enough block outside a step, R4's "On yes" paragraph, the untested R1-to-R5 path, the receipts' cache reads.

## 10. Words

- **execution team**: the agents `/sdlc execute` starts to build one unit: QA, the QA verifier, the Developer and the Dev verifier.
- **Orchestrator**: the session running the team's flow; here, this session, starting each member by `scriptPath`.
- **member**: a workflow agent the flow starts for one task.
- **task**: one of seven steps of a run: write-tests, approve-tests, prove-red, green, approve-commit, commit, two-key.
- **task in hand**: the task a run restarts at, as `task.py restart` reads it.
- **round**: one try at a task; a FAIL returns the task to its channel with its reasons, up to 3 rounds.
- **stop record**: `stop.json`, what a stop writes so a fresh session can start where the run stopped.
- **run folder**: `{git folder}/sdlc-run/{contract}/{unit}/`, one a unit, never committed: `run.json`, `stop.json`, `rounds.json`, `draft/`.
- **progress record**: one line in `.sdlc/progress/{contract}.yaml` that `task.py start` and `end` append, giving a task's state: `doing`, `done` or `blocked`.
- **restart**: `task.py restart`, which reads the run folder, the progress records and the branch and prints where the run starts or why it cannot; with `--go` it clears the stop and the leftover task file.
- **first request**: the first call a session makes to the model; its context is everything loaded before any tool runs.
- **headless session**: `claude -p`, a session with no terminal, its output streamed to a file.
- **prove-red**: the task that shows the new tests fail before the code exists.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **test-retirer**: an agent that finds and amends the older tests a change makes false.
- **manual receipt**: a check run by hand on a real session, written up as evidence, where a test cannot reach.
- **toy repository**: a small throwaway repository the receipt runs the kit against, never the kit itself.
- **self-pin**: the PR after a tag that moves the kit's own CI and install lines to the new tag.
