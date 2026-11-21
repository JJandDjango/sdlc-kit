# Session 163 plan: the feature document for session-loop

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** how sessions end and start: the wrap, `/resume-session`, and the herdr panes the user watches them in.
**Feature:** session-loop (new): sessions that wrap and restart themselves until a human is needed.
**Unit:** none. This is the interview: it writes only the requirements document and its state file.

## 1. The deliverable

`docs/features/session-loop.md`, the requirements document, written by `/sdlc:product-specification-interview session-loop` through its request half and signed by the PO seat; its state file beside it; a draft PR.

## 2. Where this sits

No Next was picked after session 162. In session 163 the user reviewed two videos on "tiny software factories", then named the bottleneck: a session that reaches its context limit waits for the user to run `/clear` and `/resume-session` by hand. The talk settled the design ideas below; they are the interview's material at O5, each confirmed by the PO seat there.

- Human-needed stop: the question goes to a `needs-ruling` issue at the stop; a reply continues the same session; 55 minutes without one (inside the one-hour prompt cache) and the session wraps itself.
- No progress: the wrap records a position (plan step, unit task); two sessions at the same position stop the loop; the launcher checks, so a crashed session is caught.
- Empty or not-ready Next: the wrap files "Pick the next deliverable"; the loop never picks one itself.
- The launcher runs on herdr: after the wrap's sentinel it types `/clear` and `/resume-session` into the same pane; the sidebar shows each loop's state. The kit writes only files; the herdr side lives in `E:\herdr-sdlc`.

## 3. The steps

1. Branch `session-163-session-loop` off main at `95833c7`; this plan committed and pushed.
2. Opening O1 to O6: id, origin, title, PO seat, the material above; r1 written.
3. Request half Q1 to Q15, one question at a time, then Terms and the Gherkin.
4. The checks P1 to P7; the PO seat signs.
5. Output W1 and W2.
6. `plan.md` out; push; a draft PR naming the design run's command.

## 4. Where Claude stops for the user

At every interview question (the PO seat's answers are the document) and at the PR's review.

## 5. Where Claude goes on alone, and by what rule

The branch, commits, pushes and the draft PR: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

None beyond the interview's own questions.

## 7. What could go wrong, already ruled

- The interview outlasts the context: wrap at a natural stop past about 20%; the state file resumes at the exact step.
- The two unverified mechanisms (a timer that wakes an idle session; `herdr pane send-keys` typing slash commands into a Claude pane) go in as open questions, for the design run to test.

## 8. This session's cost, with its basis

No agent tokens: the interview runs in the main session, about 25 questions, one a turn.

## 9. Not in this session

- The design run (`/sdlc:product-specification-interview session-loop design`), intake and any build.
- The per-seat time and token budget idea from the second video (unanswered).
- The other Next items.

## 10. Words

- **wrap**: a session's close: record Next, commit, push.
- **launcher**: the process outside any session that starts the next session after a wrap and checks progress.
- **sentinel**: the file the wrap writes last, telling the launcher the wrap finished.
- **`needs-ruling`**: the GitHub issue label `/cairn status` prints under "Waiting on you".
- **herdr**: the user's terminal multiplexer; Claude sessions run in its panes.
- **PO seat**: the person who owns and signs the request half of a feature document.
- **Next**: the backlog's list of upcoming work; `/cairn status` prints its first open item.
