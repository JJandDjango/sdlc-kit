# Session 133 plan: the execution team's open defects (backlog Next actions 13 to 15)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built.
**Feature:** execution-team (contract `execution-team`): the agent team that builds one unit, shipped in kit 0.21.0; all six units are on main.
**Unit:** fixes to three units on main: e3-wall (the hook), e5-rounds (the flow's rounds and end) and e4-team (one member's prompt), plus the release pages e6 left stale.

## 1. The deliverable

One PR that fixes the defects in backlog Next actions 13, 14 and 15 that the signed documents settle, with kit 0.21.1's release files and a Two-Key PASS for each fixed unit.

## 2. Where this sits

Kit 0.21.0 (tag `v0.21.0` at `0fa7441`) ships the team; the self-pin is merged (`6411e63`). Three e-unit sessions left defects on the backlog's Next actions (`docs/backlog.md:430-469`). The engine's first team run would meet two of them: the wall refuses a declared test command that names a walled folder (13), and it refuses the Orchestrator's own calls while a member's task runs (15). Next 24 (restart a stopped run) waits for this PR. The design is `docs/features/execution-team.design.md`; no document changes.

## 3. The steps

1. Branch `session-133-team-fixes` off main; this plan committed and pushed.
2. Probe: a headless session under `--plugin-dir`, at Haiku, with a plugin hook that logs its input. One Bash call from the session itself, one from an inline one-agent workflow. The question: does the session's own call reach the hook with no `agent_id`? Receipt `RECEIPT_execution-team-fixes_2026-10-28/hook_probe.md` (untracked). The launcher writes a liveness mark, keeps stderr in a file and exits 254 when the session never starts.
3. e3-wall, fix (items 13 and 15.1): QA by `scriptPath` (`workflows/qa.js`, unit `e3-wall`, the two defects as its `reasons`) drafts the tests; `prove.py` proves them red; the Developer (`workflows/developer.js`) changes `hooks/wall.py`; `docs/usage/the-team.md` turns both lines green. Suite green, commit, `receipts.py`, then the Dev verifier (`workflows/dev-verifier.js`).
4. e5-rounds and e4-team, fix (items 14.1, 14.2, 14.3, 14.6, 15.2 and 15.5; 14.n and 15.n number each item's findings in the backlog's order): QA drafts the tests, red proved, then the Developer changes `skills/sdlc/flows/execute.md`, `workflows/qa-verifier.js` and `workflows/dev-verifier.js`. Suite green, commit, `receipts.py`, Dev verifier.
5. Pages, by hand: `docs/conventions/standing-practice.md:13-14` (Two-Key's receipts agent no longer runs on Haiku), `CHANGELOG.md`'s 0.21.0 bullets for e2 (`receipts.py` runs the receipts file's lists) and e4 (the Orchestrator and `receipts` are no workflows), `ARCHITECTURE.md:38` (the same), and kit 0.21.1's release files (`pyproject.toml`, `skills/sdlc/init.py`, a 0.21.1 changelog entry, the release test's pin).
6. Close execution-team in `.sdlc/progress/`: `progress done` for e1 to e6, then the contract, so the tree reads it done.
7. Wrap: the backlog (Next actions 13 to 15 cut to what stays open; Next 24 stays first), `docs/session-metrics.md`, `plan.md` out, the PR, draft until CI is green.

## 4. Where Claude stops for the user

At the PR's review, and at the tag `v0.21.1`, which is the user's. Before them, only on a discovery that needs a decision. One is foreseen: if the probe shows the session's own call carries an `agent_id`, the hook has no field that tells the Orchestrator from a member, and the fix for 15.1 needs the user.

## 5. Where Claude goes on alone, and by what rule

Every step above: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The test lists are Claude's, recorded `--by claude`.

## 6. Rulings needed

None. Nine readings from the design's purpose, listed at the top of the PR:

- The wall passes a call with no `agent_id`: it is the session's own, the Orchestrator's. The design says "the hook never walls the Orchestrator's own steps" (Interfaces 10), and assumed it made none during a task.
- The wall passes a Bash call whose words equal `test.command` or `test.build`, word for word: the design has the Developer run the declared command at green (session 129's reading).
- The flow passes `{reasons}` and `{question}` in single quotes, each `'` inside written `'\''`: `task.py`'s options stay as drawn, and a backtick or `$` no longer runs.
- Prove-red runs at the unit's base commit, held at the run's start and passed to `prove.py --at`: after a QA-channel FAIL at two-key, the code is already green, and HEAD cannot prove red. In round 1 the base is HEAD, so nothing changes there.
- A question from the QA verifier at two-key stops as `qa-verifier`, not as the task's `dev-verifier`.
- A FAIL's reasons join as the design's stop sample draws them (`2 sketches failed: SC5.1 (...), SC5.2 (...)`), not by `; `.
- After both verifiers pass, the flow closes the unit (`taskcontract progress done {contract}/{unit}`), as a build by hand does once its Two-Key passes (standing practice): a green run reads the unit done.
- The Dev verifier reads the feature document's "Error messages, verbatim" and "Constraints" sections where the document has them.
- The PR carries kit 0.21.1's release files, since the engine pulls only a release (e6's reading); the tag stays the user's.

## 7. What could go wrong, already ruled

- Claude Code drops `agent_id` from a member's hook input in a later release: the wall would pass every member's call. The tests pin the field; the usage page names it as the wall's one discriminator.
- A QA draft hooks a name internal to the code (e2's retirer did): the Developer's note names only the behavior to change, and Claude re-hooks a test on the public call.
- The flow's prose fails the controlled-register check: the suite holds `lang` checks, and a fix round is narrow.
- A whole-suite run dies when an agent returns: the session runs it and classifies from its output.

## 8. This session's cost, with its basis

About 1.0M agent tokens: the probe near 75K (e3's probe, Haiku); two QA drafts near 200K each (e3's drafter 195K); two Developer runs near 100K each (e3's 78K, e4's 127K); two Dev verifier runs near 140K each (e4's 136K, e5's 146K). Each failed round adds an agent run.

## 9. Not in this session

- 14.4, the rounds file outlives an abandoned run: Next 24 decides what a stopped or abandoned run keeps.
- 14.5, `gh pr create`'s failure path: closed already (`skills/sdlc/flows/execute.md`, E9).
- 14.7, the design's e5 row ("Retirements: none", `gh pr create --draft` alone): a change to a signed document, and no behavior turns on it.
- 14.8, a headless session kills a workflow that waits 10 minutes: Claude Code's limit, and Next 24 leaves waiting members out.
- 15.3, Git Bash's `find` before System32's: the engine's `test.bat` fixes it in the engine's repository; the usage page already says so.
- 15.4, a name holding `&` or `^` breaks the fixture's `greet.bat`: no consumer runs the fixture.
- Next actions 11 (e2's and e3's advisories) and Next 24.

## 10. Words

- **wall**: a hook that, while a task runs, keeps the Developer from the functional tests and QA from implementation bodies and unit tests (`hooks/wall.py`).
- **Orchestrator**: the session running `/sdlc execute`; it starts each member and records each task.
- **member**: a workflow agent the flow starts for one task: QA, the QA verifier, the Developer or the Dev verifier.
- **`agent_id`**: a field in a hook's input; the probe of session 126 saw it on a member's call.
- **task file**: `.git/sdlc-task.json`, which names the running task and its operator.
- **round**: one try at a task; a FAIL sends the task back with its reasons, up to 3 rounds.
- **channel**: which task a FAIL returns to: write-tests (QA's) or green (the Developer's).
- **prove-red**: the task that shows the new tests fail before the code exists.
- **close**: a `progress done` record on a unit or contract, which reads every task and check under it done.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **probe**: a small live run that measures one fact before the code relies on it.
- **headless session**: `claude -p`, a session with no terminal, its output in a file.
