# Session 141 plan: rs2-restart, a stopped run restarts at its stopped task

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built by the execution team (`/sdlc execute`).
**Feature:** run-restart (contract `run-restart`): a stopped team run restarts in a fresh session from a stop record, not by `--resume`; five units, rs1 to rs5, kit 0.22.0 at rs5. rs1 (the stop record) merged as PR #156 at `7a1e96d`.
**Unit:** `rs2-restart` (checks SC2.1, SC2.2, SC2.3+SC5.3): `/sdlc execute {contract} {unit} --answer TEXT` in a fresh session on the run's branch starts at the stopped task, with what the earlier tasks kept and the user's answer.

## 1. The deliverable

One draft PR holding `rs2-restart`, built by the team's members, with a Two-Key PASS from both verifiers and the SC2.1 manual receipt.

## 2. Where this sits

The requirements (`docs/features/run-restart.md`, r7) and design (`docs/features/run-restart.design.md`, signed on r11) are signed; the contract `specs/run-restart/contract.yaml` is ready-green with `tests/` in its scope; G1 passed. rs1 made every stop write `stop.json` and `rounds.json` in the unit's run folder. This unit adds what a restart reads (`run.json`, `task.py keep`, the task file's `unit`), the restart itself (`task.py restart`, `skills/sdlc/flows/restart.md`, `--answer` on `/sdlc execute`) and each member's `answer` argument. The design's Interfaces, Sources and Constraints draw the files and commands; this plan holds only this session's facts.

## 3. The steps

1. Branch `session-141-rs2-restart` off main at `7a1e96d`; this plan committed and pushed.
2. write-tests: QA (`workflows/qa.js`, by `scriptPath`) drafts the tests for SC2.1 to SC2.3+SC5.3 from the contract, the requirements, the design and the readings in section 6, given as `pins`.
3. approve-tests, then prove-red: the QA verifier (`workflows/qa-verifier.js`) grades the draft with the same readings as `rulings`, then proves it red at the base commit through `prove.py`. The draft goes into the tree.
4. green: the Developer (`workflows/developer.js`) changes `task.py` (`run.json`, `keep`, `restart` and `restart --go`, the task file's `unit`, the drive-letter fix), `execute.md` (E2 runs `task.py restart` first; each passed task keeps what it hands on; under 12,000 characters), the new `restart.md`, `SKILL.md` (names `restart.md`) and the four member scripts (`answer`).
5. The whole suite in the session. Older tests that pin the retired behavior go to the test-retirer (`workflows/test-retirer.js`) with the Developer's files as its overlay; the session places the amended modules.
6. The usage page by hand: rs2's red paragraph (`docs/usage/the-team.md:310`) turns green, and any line the code makes false is fixed.
7. approve-commit: `receipts.py` runs the test command; commit with the `Contract: run-restart` trailer.
8. two-key: the Dev verifier (`workflows/dev-verifier.js`), then the QA verifier with about four mutations. A FAIL returns the task to its channel with the reasons, up to three rounds.
9. The SC2.1 manual receipt (section 6): a fresh headless session restarts a toy unit stopped at green; the transcript and a note go in `RECEIPT_run-restart-rs2_2026-11-02/`.
10. Close: `progress done run-restart/rs2-restart`, the backlog's Next 24 updated (rs3 next), a row in `docs/session-metrics.md`, `plan.md` out, push, draft PR with the readings at its top.

## 4. Where Claude stops for the user

At the PR's review. Before it, only on a case the signed documents leave open that their purpose cannot settle, or a discovery that needs a decision. None is foreseen.

## 5. Where Claude goes on alone, and by what rule

Every step above: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The test list is Claude's, recorded `--by claude`; usage text that restates the signed design is Claude's.

## 6. Rulings needed

None. Readings from the documents' purpose, listed at the top of the PR:

- rs2 builds `run.json`, `keep`, `restart` (read-only and `--go`), the task file's `unit`, `restart.md` and each member's `answer`. `--fresh` and `--enough` wait for rs3; the flow's abandoned path (its question, the leftover task file on the user's word) waits for rs4.
- `task.py restart` reads all three states as the Sources table draws them, since SC2.3+SC5.3 tells "no abandoned run" from a stopped one. Until rs4, the flow starts nothing on an abandoned run: nothing starts before the user's word (Constraints).
- A refused first start writes no `run.json` (a refused start writes nothing), so `stop` writes one when none stands: the branch, HEAD as base, the task. Every stop record then has a branch to check (non-goal 4).
- A record that does not parse, or a `stop.json` with no `run.json`, is reported and starts nothing (Constraints: "never guessed").
- A stopped task whose operator is no member (`receipts`, `orchestrator`) shows the answer and runs its command; only members take `answer`.
- `--answer` with no stop record starts as today; the answer is unused, as the design draws no line for it.
- A `--unit` half holding a drive colon (`c:`) is a usage error, exit 2, like the other unsafe halves: rs1's check passed it and `Path.joinpath` then left the git folder (rs1's Dev verifier advisory, `task.py:104`). A defect in a unit on main: named at the PR's top and charged in the metrics row.
- The SC2.1 receipt builds its stop by hand: `task.py start`, `keep` and `end` through prove-red on a toy consumer, then `stop --kind question` at green. One fresh headless `/sdlc execute ... --answer` then shows it starts at green, the Developer gets the interface note and the test file, and no earlier task runs. rs1 already proved the stop; the receipt is about the fresh session.

## 7. What could go wrong, already ruled

- `execute.md` passes 12,000 characters: the restart's steps go in `restart.md`, and `execute.md` trims elsewhere (Constraints); the ceiling test holds it.
- QA's draft hooks a name inside `task.py`: the tests run `task.py` as a command on fixture repositories (Units cell); a draft that imports internals goes back to write-tests.
- The new prose fails the controlled-register check: the suite holds the `lang` tests, and a fix round is narrow.
- A whole-suite run dies when an agent returns: the session runs the suite and classifies from its output. Never two suites at once.
- The QA verifier's mutation run outlasts a Bash call: it runs from this interactive session by `scriptPath`, about four mutations (about 100 s each against the 600 s cap).
- The receipt's headless session meets the 10-minute workflow kill: the toy unit is one small function, so each member runs well under it.

## 8. This session's cost, with its basis

About 0.8M agent tokens at one round each, the design's estimate for rs2 (rs1 ran 0.84M, `docs/session-metrics.md`). Each failed round adds one member run, about 100K to 200K. The receipt adds about 1M to 2M headless tokens, mostly cache reads: session 128's three Haiku receipt runs cost 6.5M. The session's own context targets 200K; if it passes 40% before step 4, the build splits there with a handoff file in the receipt folder.

## 9. Not in this session

- rs3 to rs5: `--fresh`, `--enough`, the abandoned path, the 50K receipts, the release.
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
- **stop record**: `stop.json`, what a stop writes so a fresh session can start where the run stopped.
- **run folder**: `{git folder}/sdlc-run/{contract}/{unit}/`, one a unit, never committed: `run.json`, `stop.json`, `rounds.json`, `draft/`.
- **run.json**: the run's branch, base commit, task in hand and the values kept for later tasks.
- **keep**: `task.py keep`, which saves a passed task's hand-on value (QA's draft and note, the commit, the receipts) into `run.json`.
- **restart**: `task.py restart`, which reads the run folder and the branch and prints where the run starts or why it cannot.
- **abandoned run**: a run folder with `run.json` and no `stop.json`, a session that ended mid-task.
- **prove-red**: the task that shows the new tests fail before the code exists.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **test-retirer**: an agent that finds and amends the older tests a change makes false.
- **manual receipt**: a check run by hand and recorded in a receipt folder, for what an automated test cannot show.
