# Session 165 plan: the design document for session-loop

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** how sessions end and start: the wrap, `/resume-session`, and the herdr panes the user watches them in.
**Feature:** session-loop: sessions that wrap and restart themselves until a human is needed. Its requirements document is signed and on main (PR #171).
**Unit:** none. This is the design run: it writes only the design document and its state file.

## 1. The deliverable

`docs/features/session-loop.design.md`, written by `/sdlc:product-specification-interview session-loop design` and signed by the engineer seat; its state file beside it; a draft PR naming `/sdlc intake docs/features/session-loop.md`.

## 2. Where this sits

The requirements document (`docs/features/session-loop.md`, signed at r4) leaves three OPEN questions for the design run: (9) can a timer wake an idle interactive session; (10) can `herdr pane send-keys` type a slash command into a Claude pane; (11) how the 55-minute notice reaches the user. The design rests on their answers, so each is tried live before the question that needs it, and the result goes into the design as a measured fact, not a guess.

## 3. The steps

1. Branch `session-165-session-loop-design` off main at `e3d627f`; this plan committed and pushed.
2. Design read and design confirm; O1 to O6; r1 written.
3. The three trials, each a few minutes in a scratch herdr pane or this session: a scheduled wake on an idle session; `send-keys` typing `/clear` into a Claude pane; a push notification to the user's devices.
4. Solution half S1 to S12, one question a turn.
5. The checks; the engineer seat signs.
6. Output; `plan.md` out; push; the draft PR.

## 4. Where Claude stops for the user

At every interview question (the engineer seat's answers are the document), at each trial that needs the user to watch a device, and at the PR's review.

## 5. Where Claude goes on alone, and by what rule

The branch, commits, pushes, the trials' setup and the draft PR: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

None beyond the interview's own questions.

## 7. What could go wrong, already ruled

- A trial fails (no wake, no keys typed): the design records the failure and names the fallback the requirements allow; a failure that leaves a signed success criterion unbuildable is a stop for the user.
- The run outlasts the context: wrap at a natural stop past about 20%; the state file resumes at the exact step.

## 8. This session's cost, with its basis

No agent tokens: the run is in the main session, about 20 questions one a turn (the design flow's O1 to O6 and S1 to S12), plus three short trials.

## 9. Not in this session

- Intake (`/sdlc intake`) and any build.
- The `needs-ruling` label on the remote (the user's prerequisite).
- session-loop-sidebar (Next 31) and the other Next items.

## 10. Words

- **design run**: the interview's second pass, after the requirements are signed; it writes how the feature will be built.
- **engineer seat**: the person who owns and signs the design document; here the user alone.
- **wrap**: a session's close: record Next, commit, push.
- **launcher**: the process outside any session that starts the next session after a wrap and checks progress.
- **herdr**: the user's terminal multiplexer; Claude sessions run in its panes.
- **OPEN**: a question the requirements document leaves for the design run.
- **intake**: `/sdlc intake`, the step that turns signed documents into contract units.
