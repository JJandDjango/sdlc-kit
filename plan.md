# Session 131 plan: e6-batch-run, the release unit

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built.
**Feature:** execution-team (contract `execution-team`): the agent team that builds one unit, shipped in the plugin; e1 to e5 are on main.
**Unit:** e6-batch-run: in a batch-file fixture repository, one unit runs from write-tests to two-key and ends green, and kit 0.21.0 ships.

## 1. The deliverable

e6-batch-run on a PR: the fixture repository under `tests/`, the receipt of the team's run in a copy of it, and kit 0.21.0's release files, with a Two-Key PASS.

## 2. Where this sits

e1 (the declaration), e2 (the scripts), e3 (the wall), e4 (the team) and e5 (rounds, stops and the draft PR) are on main at `17a6fbd`. e6 is the last unit (design `docs/features/execution-team.design.md`, the e6 row and Scope items 6 and 9). It proves SC2.2 by a manual receipt: the shipped team builds one unit in a repository whose test command is a batch file, as the engine's is (`E:/ImSimProject/engine/test.bat`). Then the kit ships 0.21.0, since the engine pulls only a release.

## 3. The steps

1. Branch `session-131-e6-batch-run` off main; this plan committed and pushed.
2. The fixture at `tests/fixtures/batch-repo/`: a ready contract `greet` of one unit `greeting` (`src\greet.bat NAME` prints `Hello, NAME!`), its two signed documents, `.sdlc/config.yaml` with `test.command: [test.bat]` and `test.file: [test.bat, "{file}"]`, the wall `functional: [tests/]` and `code: [src/]`, the execution row at sonnet and high, a root `test.bat` that runs `tests\*.bat`, and a stub `src\greet.bat`. The kit's suite stays green with it in.
3. The receipt: copy the fixture to `E:/sdlc_e6/fixture` and commit it there on branch `e6-receipt`, with no remote. A detached worktree of main at `E:/sdlc_e6/kit-e6` holds the plugin. A headless session at the execution row runs `/kit-e6:sdlc execute greet greeting` there, by a launcher with a liveness marker, stderr in a file and exit 254 when it never starts; this session watches its stream. The receipt (`RECEIPT_execution-team-e6_2026-10-28/batch_run.md`, untracked) holds the run's lines and the fixture's green.
4. The release: `pyproject.toml` and `skills/sdlc/init.py` read 0.21.0; `CHANGELOG.md` gains the 0.21.0 entry (e1 to e6); `README.md` gains the team's row; `docs/usage/the-team.md` turns e6's markers green; `tests/test_g1_release.py` finds 0.20.0's entry where it stands. The suite runs green.
5. Two-Key on the unit commit: `receipts.py` on the kit, then the Dev verifier (`workflows/dev-verifier.js`, sonnet and high).
6. Wrap: the backlog (Next 23 closed; the self-pin as the next item), `docs/session-metrics.md`, the progress record; then `plan.md` out and the PR, draft until CI is green.
7. After the user merges and tags `v0.21.0`: the self-pin PR (`.github/workflows/sdlc.yml` and the pinned install lines in `USAGE.md` and `docs/usage/`), the 0.20.0 shape (PR #125).

## 4. Where Claude stops for the user

At the PR's review, and at the tag, which the user pushes. Before them, only on a case no document settles or a discovery that needs the user's decision; a third failed round in the run is one.

## 5. Where Claude goes on alone, and by what rule

Every step above: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The release files are hand edits; the Dev verifier grades them.

## 6. Rulings needed

None. Five readings from the design's purpose, listed at the top of the PR:

- The fixture's command is a root `test.bat`, as the engine's is, so it names no walled folder. Backlog Next actions 13 (the wall refuses a declared command that names a walled folder) does not block the run and keeps its red line on the usage page in 0.21.0.
- The fixture has no remote, so the run's push exits non-zero and the run ends with no Draft PR line, as the flow draws (E9). SC2.2 ends at two-key; e5 proved the PR (SC5.1).
- `tests/test_g1_release.py` pins 0.20.0 as the newest changelog entry; the release moves that pin to finding 0.20.0's entry where it stands, as the 0.19.0 test does. The design's e6 row names no retirement: a gap.
- Two-Key on the kit's commit is the Dev verifier alone: the unit adds no functional test, since SC2.2's test is the receipt, and the run's own two-key ran both verifiers.
- The self-pin rides its own PR after the user's tag, as 0.20.0's did, though the design lists `sdlc.yml` under e6: a pin to a tag that does not exist yet breaks CI.

## 7. What could go wrong, already ruled

- A verifier's reason holds a backtick, a `$` or a double quote, which breaks the flow's `--reason "{reasons}"` call (Next actions 14). The headless session's standing orders: escape those characters in any double-quoted value; list each case.
- A member waits more than 10 minutes and the headless session kills it (Next actions 14). The fixture's suite runs in seconds, so no member should; if one is killed, this session runs that member by its `scriptPath` and resumes the headless session at the next task.
- A member asks a question: the standing orders rule open details from the fixture's documents, list them, and stop only on a third FAIL or a change to a signed line.
- `test.bat` starts a program that hangs, and `prove.py`'s timeout kills only `cmd` (Next actions 11): the fixture starts no program but `cmd`'s own commands.
- The headless session ends early or never starts: the launcher's three marks tell which.

## 8. This session's cost, with its basis

About 0.7M agent tokens, plus 3M to 5M read by the headless session. Basis: the run starts at least six agents at sonnet high (QA, the QA verifier three times, the Developer, the Dev verifier), each near 54K at start and growing on a toy repository; e4's toy run of the whole flow read 3.0M at Haiku; the kit's Dev verifier took about 146K in e5. Each failed round adds an agent run.

## 9. Not in this session

- Next actions 13 (the hook passes the declared commands) and 14 (e5's advisories).
- Next 24 (restart a stopped run in a fresh session), which starts once 0.21.0 ships.

## 10. Words

- **fixture repository**: a small repository kept under `tests/fixtures/`, copied out and run, never run in place.
- **batch file**: a Windows `cmd` script (`.bat`); the engine's tests run through one.
- **task**: one of a unit's seven steps (write-tests, approve-tests, prove-red, green, approve-commit, commit, two-key).
- **round**: one try at a task; a FAIL sends the task back, up to 3 rounds.
- **wall**: a hook that, while a task runs, keeps the Developer from the functional tests and QA from implementation bodies and unit tests.
- **QA, QA verifier, Developer, Dev verifier, Orchestrator**: the team's roles (`docs/operators.md`); QA writes the functional tests, the Developer the code.
- **Two-Key**: the last task, where the Dev verifier and the QA verifier each grade the commit; both must PASS.
- **headless session**: `claude -p`, a session with no terminal, its output streamed to a file.
- **manual receipt**: a written record of a run a person or a session made by hand, for a check no test automates.
- **self-pin**: the PR after a tag that moves the kit's own CI and install lines to the new tag.
