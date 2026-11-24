# Session 180 plan: the design document for session-loop-sidebar

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session loop as the user watches it: the herdr panes and the sidebar beside them.
**Feature:** session-loop-sidebar: herdr's sidebar shows each loop's position, strike count, waiting state and stop reason. Requirements signed at r3 (PR #186, merged).
**Unit:** none. This is the design run: it writes only the design document and its state file, then intake writes the contract.

## 1. The deliverable

`docs/features/session-loop-sidebar.design.md`, the design document, written by `/sdlc:product-specification-interview session-loop-sidebar design` on requirements r3 and signed by the engineer seat; its state file beside it; then `/sdlc intake` writes `specs/session-loop-sidebar/contract.yaml`; one PR.

## 2. Where this sits

session-loop shipped as kit 0.23.0. The requirements (r3) ask for four criteria: SC1 position and strikes within 10 s of a restart, SC2 minutes left while a stop waits, SC3 the stop reason for five ends, SC4 nothing left within 10 s of loop off. Material the design starts from:

- The launcher (`herdr/herdr_loop.py`) holds position and strikes in memory only (`:185-209`) and polls every 2 s.
- herdr 0.9.5's `herdr pane report-metadata <pane> --source ID --token NAME=VALUE` shows as `$NAME` in `[ui.sidebar.agents] rows`, or in `[ui.sidebar.agents.rows_by_agent] claude` for Claude panes alone. It also takes `--clear-token NAME`, `--ttl-ms N` (a token that expires) and `--seq N`.
- ADR 0043: herdr code lives in the opt-in `herdr/` folder; the kit's core runs no herdr command. The kit never writes the user's herdr config, so `herdr/README.md` names the row to add.

## 3. The steps

1. Branch `session-180-loop-sidebar-design` off main at `f6fe799`; this plan committed and pushed.
2. Measure: report a token on this Claude pane with a test row in the user's herdr config, and see whether it shows; then remove the row. The user looks at the sidebar.
3. Design run, one question at a time: the opening, then each section of the design half.
4. The checks; the engineer seat signs.
5. `/sdlc intake session-loop-sidebar`: the contract.
6. `plan.md` out; push; a PR; backlog Next 33 marked and the build named as the next Next.

## 4. Where Claude stops for the user

At step 2's look at the sidebar, at every interview question (the engineer seat's answers are the document), and at the PR's review.

## 5. Where Claude goes on alone, and by what rule

The branch, commits, pushes, the test row's add and removal, and the PR: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

None beyond the interview's own questions.

## 7. What could go wrong, already ruled

- The token row does not show on a Claude pane: the design rules the fallback (a `--display-agent` or `--title` text, or the launcher's own pane) as an interview question, on the measured result.
- The interview outlasts the context: wrap at a natural stop past about 20%; the state file resumes at the exact step, and intake moves to the next Next.

## 8. This session's cost, with its basis

No agent tokens: the interview runs in the main session, one question a turn (session 165's design run of session-loop: one session, three live trials).

## 9. Not in this session

- The build (test lists, developer, Two-Key) and any release.
- The launcher's advisories carried from l2 and l3; the flaky `test_sc4_3_a_source_change_renders_within_two_seconds`.

## 10. Words

- **loop**: on while `loop.json` sits in `{git folder}/sdlc-loop/`; a launcher in another pane restarts the session after each wrap.
- **launcher**: `herdr/herdr_loop.py`, the process that restarts a loop's pane and stops the loop.
- **sidebar entry**: a pane's row in herdr's sidebar, where the loop's state shows beside the pane's name.
- **token**: a `NAME=VALUE` pair a process reports on a pane; a sidebar row shows it where the config names `$NAME`.
- **engineer seat**: the person who owns and signs the design half of a feature document (here, the user).
- **intake**: `/sdlc intake`, which turns a signed feature and design document into a task contract under `specs/`.
