# Session 129 plan: e5-rounds, built by the shipped team

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where the units of a ready contract are built.
**Feature:** execution-team (contract `execution-team`): the agent team that builds one unit, shipped in the plugin; e1 to e4 are on main.
**Unit:** e5-rounds: a FAIL returns its reasons, three failures or a question stop the run, and a pass opens a draft PR.

## 1. The deliverable

e5-rounds, built by the shipped team (`/sdlc execute execution-team e5-rounds`), with both verifiers' PASS, on a draft PR.

## 2. Where this sits

e1 (the declaration), e2 (the scripts), e3 (the wall) and e4 (the team) are on main at `f182701`. e5 gives `workflows/tools/task.py` its `end`, `fail` and `stop` commands and the rounds file, and gives the flow its rounds and its draft PR (design `docs/features/execution-team.design.md`, Interfaces 10 and 11). e6 runs a batch-file repository and ships kit 0.21.0. e5 is the first unit the kit's own team builds.

## 3. The steps

1. Branch `session-129-e5-rounds` off main; this plan committed and pushed.
2. The blocker (section 7): the kit's `test.command` drops the word `tests`, since `pyproject.toml`'s `testpaths` already names it; its pin at `tests/test_declaration.py:228` follows. The suite runs green once before the team starts.
3. A detached worktree of main at `E:/sdlc_e5/kit-e5` holds the plugin, so the tools the team edits do not change under its own run.
4. A headless session at the execution row (`claude --model sonnet --effort high`, plus `--plugin-dir`) runs `/kit-e5:sdlc execute execution-team e5-rounds` in this repository. A launcher gives it a liveness marker, stderr in a file and exit 254 when it never starts. This session watches its stream.
5. e4's flow has one round: a FAIL or a question stops it. This session then resumes the headless session at that task with the verifier's reasons, up to round 3.
6. After both verifiers PASS: the usage page's markers, the backlog and `docs/session-metrics.md`; then `plan.md` out and the draft PR.

## 4. Where Claude stops for the user

At the draft PR's review. Before it, only on a case no document settles or a discovery that needs the user's decision. A task's third failed round is one.

## 5. Where Claude goes on alone, and by what rule

Every step above: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

None. Two readings from the design's purpose, listed at the top of the PR:

- Backlog Next actions 12 (the wall refuses a task's own end when the contract's id starts a walled path) is ruled: the hook passes the flow's own commands word for word, one run of the plugin's `task.py` and the declared `test.command` and `test.build`. A later unit builds it before e6: this contract's id starts no walled path, and the team builds e5 from the design alone.
- The blocker in section 7 is fixed for the kit by its declaration now, and for every consumer by the same hook rule.

## 7. What could go wrong, already ruled

- Found this session, a defect on main (e3 with e4): the wall refuses the Developer's run of a declared command that names a walled folder. Probe: `python -P -m pytest tests -q -n auto` under `functional: [tests/]` gives `Task green: Developer reads no functional test: tests`. e4's receipt missed it, since its consumer ran `pytest -q`. Ruled in section 6; charged in the session metrics.
- The team edits `task.py` and `execute.md`, which its own run uses: the plugin comes from the worktree, so the run keeps e4's tools.
- The headless session ends early or never starts: the launcher's three marks tell which.
- A member passes 300K tokens: stop it and resume the task with a narrower brief.

## 8. This session's cost, with its basis

About 1M agent tokens, plus 3M to 6M read by the headless session. Basis: a unit takes at least five agents (design, Risks and cost 4), here six agent runs at Sonnet high, each starting near 54K; e2 and e3 took about 0.5M agent tokens with four agents each; e4's toy run of the whole flow read 3.0M at Haiku. Each failed round adds an agent run.

## 9. Not in this session

- The hook rule of section 6 (Next actions 12 and the defect).
- e6-batch-run and kit 0.21.0.

## 10. Words

- **task**: one of a unit's seven steps (write-tests, approve-tests, prove-red, green, approve-commit, commit, two-key), listed in `taskcontract/data/tasks.yaml`.
- **round**: one try at a task; a FAIL sends the task back, up to 3 rounds.
- **wall**: a hook that, while a task runs, keeps the Developer from the functional tests and QA from implementation bodies and unit tests.
- **task file**: `.git/sdlc-task.json`, the running task, its operator and its round; the wall holds only while it stands.
- **rounds file**: `.git/sdlc-rounds.json`, the failed rounds of each task in one unit's run.
- **QA, QA verifier, Developer, Dev verifier, Orchestrator**: the team's roles (`docs/operators.md`); QA writes the functional tests, the Developer the code.
- **Two-Key**: the last task, where the Dev verifier and the QA verifier each grade the commit; both must PASS.
- **headless session**: `claude -p`, a session with no terminal, its output streamed to a file.
- **draft PR**: a GitHub pull request not yet marked ready for review.
