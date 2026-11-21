| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-11-21 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: Johnathan Hyden |

# session-loop - Sessions restart themselves until you are needed

`sdlc_development_kit` · seat: PO Johnathan Hyden · contract: `session-loop`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As the developer running kit sessions, I want a wrapped session to start the next one itself, so that work goes on without my hand-run `/clear` and `/resume-session` until a decision needs me.

## Description

`[PO seat · authored]`

- At a natural stop, the wrap records Next and the position, commits, pushes, and writes a sentinel file last.
- A launcher outside any session sees the sentinel and types `/clear` and `/resume-session` into the same herdr pane, so the next session starts where the last one stopped.
- The loop stops in three cases:
  - Human needed: the session writes its question to a `needs-ruling` issue at the stop and waits. A reply continues the same session. After 55 minutes with no reply, the session wraps itself.
  - No progress: two sessions in a row end at the same position.
  - Next empty or not ready: the wrap files a "Pick the next deliverable" issue.
- The herdr sidebar shows each loop's position, strike count and waiting state.

## Background

`[PO seat · authored]`

Since 2026-11-14 a session wraps itself past about 20% context at a natural stop, but the user restarts it by hand with `/clear` and `/resume-session`, so work waits whenever the user is away. The idea came from two IndyDevDan videos (2026-11-02 and 2026-11-09) on "tiny software factories": agents that keep working with the user near the loop rather than in it. run-restart (0.22.0) restarts a stopped team run in a fresh session, but only on the user's answer.

### Existing behavior touched

1. The close rule: a session's closing message is its last and asks nothing. A stop that waits on the user's word ends on a question instead.
2. `/cairn status` prints open issues labelled `needs-ruling` under "Waiting on you" (`status.py:17`).
3. run-restart's non-goal: a run never relaunches itself in a loop (`docs/features/run-restart.md:56`).
4. A session left overnight is never resumed; a new one starts from the handoff (`docs/conventions/standing-practice.md:11`).
5. The herdr hook in `E:\herdr-sdlc`, which flags the tree pane on the kit's notify command.

## Success criteria

`[PO seat · authored]`

- SC1: After a wrap with a ready Next, the next session starts in the same pane with no keystroke from the user.
- SC2: A stop for the user's answer files its `needs-ruling` issue at the stop, and a reply within 55 minutes continues the same session.
- SC3: With no reply in 55 minutes, the session wraps itself.
- SC4: Two sessions in a row at the same position, or a crashed session, stop the loop with an issue.
- SC5: An empty or not-ready Next stops the loop with one issue.
- SC6: The herdr sidebar shows each loop's position, strike count and waiting state.

## Non-goals

`[PO seat · authored]`

- The loop never picks a deliverable itself; a new feature still starts with the user's interview.
- No resume of an old session: every restart is a fresh session.
- No new window or tab per session.
- No built-in compaction as the restart.
- The kit has no dependency on herdr.

## Prerequisites

`[PO seat · authored]`

- herdr 0.9.1, whose `herdr pane send-keys` drives a pane's keys.
- `gh` installed and signed in, for the `needs-ruling` issues.

## Acceptance criteria

`[PO seat · authored]`

### Checks

(not yet asked)

### Error messages, verbatim

(not yet asked)

## Decisions and open questions

`[PO seat · authored]`

1. Decided (session 163): the 55-minute timer, which sits inside the one-hour prompt cache.
2. Decided (session 163): progress is the wrap's recorded position, and two strikes stop the loop.
3. Decided (session 163): the launcher checks progress, not the session, so a crashed or hung session is caught.
4. Decided (session 163): the launcher runs on herdr from the start.
5. Decided (session 163): ADR 0031's split: the kit writes files (sentinel, position, stop issue); the herdr side in `E:\herdr-sdlc` reads them.
6. OPEN: can a timer (`CronCreate`) wake an idle interactive session?
7. OPEN: can `herdr pane send-keys` type slash commands into a Claude pane?
8. OPEN: how does the 55-minute notice reach the user: phone, email or desktop toast?

## Notes

`[PO seat · authored]`

(none)

## Appendix

### Gherkin

`[PO seat · derived]`

(none: the Gherkin step writes one scenario per check)

### Terms

`[PO seat · authored]`

- **wrap**: a session's close: record Next and the position, commit, push, then write the sentinel.
- **launcher**: the process outside any session that, after a wrap, starts the next session in the same herdr pane and checks progress.
- **sentinel**: the file the wrap writes last; it tells the launcher the wrap finished.
- **position**: where a wrap stopped: the plan step and the unit task.
- **strike**: a session that ends at the same position as the one before it; two strikes stop the loop.
- **`needs-ruling`**: the GitHub issue label `/cairn status` prints under "Waiting on you".
