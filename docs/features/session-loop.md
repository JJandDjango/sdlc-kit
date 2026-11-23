| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-11-21 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: Johnathan Hyden |
| 2026-11-22 | Johnathan Hyden | r2: Measured: the checks before signing, on the request half: 60 findings (CL003 1, CL006 56, CL008 3); ready checks 1 to 8: 2 OPEN |
| 2026-11-22 | Johnathan Hyden | r3: Measured: the checks before signing, on the request half: 59 findings (CL006 56, CL008 3); ready checks 1 to 8: 1 OPEN |
| 2026-11-22 | Johnathan Hyden | r4: The request half finished: 11 sections written, 1 OPEN |
| 2026-11-22 | Johnathan Hyden | r5: Signed: request half. The PO seat signs r4 |
| 2026-11-22 | intake | r6: Parked: OPEN: Ready check 3: SC1 holds five checks and SC2 four, past the two or three a criterion takes; the extras are Q11's regression checks. Decisions and open questions 9: OPEN: can a timer (`CronCreate`) wake an idle interactive session? Decisions and open questions 10: OPEN: can `herdr pane send-keys` type slash commands into a Claude pane? Decisions and open questions 11: OPEN: how does the 55-minute notice reach the user: phone, email or desktop toast? |
| 2026-11-22 | Johnathan Hyden | r7: Q11 again: SC1.1 takes SC1.3, a new SC1.3 joins SC1.4 and SC1.5, SC2.1 takes SC2.3, SC5.1 takes SC5.2, so each criterion holds two or three checks (14 in all); Decisions 9 to 11 closed by the design run's trials (session 165) |
| 2026-11-22 | Johnathan Hyden | r8: Measured: the checks before signing, on the request half: 61 findings (CL006 54, CL008 7); ready checks 1 to 8: 0 OPEN |
| 2026-11-22 | Johnathan Hyden | r9: The request half finished: 11 sections written, 0 OPEN |
| 2026-11-22 | Johnathan Hyden | r10: Signed: request half. The PO seat signs r9 |
| 2026-11-22 | intake | r11: Ready: contract `session-loop` validates ready-green, derived from r9; the PO seat (Johnathan Hyden) signed the request half at r9 (r10) |

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
  - No progress: two sessions in a row end where they started.
  - Next empty: the wrap files a "Pick the next deliverable" issue.

## Background

`[PO seat · authored]`

Since 2026-11-14 a session wraps itself past about 20% context at a natural stop, but the user restarts it by hand with `/clear` and `/resume-session`, so work waits whenever the user is away. The idea came from two IndyDevDan videos (2026-11-02 and 2026-11-09) on "tiny software factories": agents that keep working with the user near the loop rather than in it. run-restart (0.22.0) restarts a stopped team run in a fresh session, but only on the user's answer.

### Existing behavior touched

1. The close rule: a session's closing message is its last and asks nothing. A stop that waits on the user's word ends on a question instead (the user's standing rule, session 100 and 2026-11-14; held in Claude's memory, not in the repo). Regression check: SC2.3.
2. `/cairn status` prints open issues labelled `needs-ruling` under "Waiting on you" (`status.py:17`). Regression check: SC3.3.
3. run-restart's non-goal: a run never relaunches itself in a loop (`docs/features/run-restart.md:56`). Regression check: SC1.3.
4. A session left overnight is never resumed; a new one starts from the handoff (`docs/conventions/standing-practice.md:11`). Regression check: SC1.1.
5. The herdr hook flags the tree pane on the kit's notify command (`E:\herdr-sdlc\herdr_seat.py`, run as a repo's `tree: notify:`; `E:\herdr-sdlc\README.md:4-7`). Regression check: SC1.3.

## Success criteria

`[PO seat · authored]`

- SC1: After a wrap with a ready Next, the next session starts in the same pane with no keystroke from the user.
- SC2: A stop for the user's answer files its `needs-ruling` issue at the stop, and a reply within 55 minutes continues the same session.
- SC3: With no reply in 55 minutes, the session wraps itself.
- SC4: Two sessions in a row that end where they started, or a crashed session, stop the loop with an issue.
- SC5: An empty Next stops the loop with one issue.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added.
- The loop never picks a deliverable itself; a new feature still starts with the user's interview.
- No resume of an old session: every restart is a fresh session.
- No new window or tab per session.
- No built-in compaction as the restart.
- The kit has no dependency on herdr.
- No time or token budget per session.

## Prerequisites

`[PO seat · authored]`

- herdr 0.9.1, whose `herdr pane send-text` and `herdr pane send-keys` drive a pane's input. Exists.
- `gh` installed and signed in with `repo` scope, for the `needs-ruling` issues. Exists.
- The `needs-ruling` label in the repo. Missing; owner: the user, who runs `gh label create needs-ruling` once before the first loop.

## Acceptance criteria

`[PO seat · authored]`

### Checks

- SC1.1: verify that within 60 seconds of the wrap's sentinel appearing, the launcher types `/clear` and then `/resume-session` into the same pane, and the new session's ready-state names the Next the wrap recorded.
- SC1.2: verify that the sentinel appears only after the wrap's commit is on the remote branch.
- SC1.3: verify that while a loop runs, a team run that stops with no wrap gets no keystroke from the launcher, and the kit's `tree: notify:` command still flags the tree pane.
- SC2.1: verify that at a stop for the user's answer, an open `needs-ruling` issue holds the question before the session waits, and that on the reply the session closes that issue.
- SC2.2: verify that a reply in the session 54 minutes after the stop continues that session, with no wrap and no sentinel.
- SC2.3: verify that a human-needed stop's last message ends on its question, and a wrap's closing message asks nothing.
- SC3.1: verify that with no reply, the session starts its wrap 55 minutes after the stop, give or take one minute.
- SC3.2: verify that after this self-wrap the launcher types nothing into the pane, and the `needs-ruling` issue stays open.
- SC3.3: verify that in the session the user starts next, `/cairn status` lists that issue under "Waiting on you".
- SC4.1: verify that when a second session in a row ends at the position it started from, the launcher types nothing and files one issue naming that position.
- SC4.2: verify that a session that moves the position resets the strike count to zero.
- SC4.3: verify that when the Claude process in the pane exits with no sentinel, or the pane shows no change for 60 minutes with no sentinel, the launcher types nothing and files one issue naming the pane and the last position.
- SC5.1: verify that when `/cairn status` prints Next as "(none)", the wrap files one "Pick the next deliverable" issue labelled `needs-ruling`, none when one is already open, and the launcher types nothing.
- SC5.2: verify that when Next is empty, the wrap's commit leaves it empty.

### Error messages, verbatim

- SC2.1: `session-loop: the needs-ruling label is missing; run: gh label create needs-ruling`
- SC4.1: `session-loop stopped: two sessions in a row ended at {position}`
- SC4.3: `session-loop stopped: the session in pane {pane} exited without a wrap; last position {position}`
- SC4.3: `session-loop stopped: the session in pane {pane} showed no change for 60 minutes; last position {position}`
- SC5.1: `Pick the next deliverable`

## Decisions and open questions

`[PO seat · authored]`

1. Decided (session 163): the 55-minute timer, which sits inside the one-hour prompt cache.
2. Decided (session 163): progress is the wrap's recorded position, and two strikes stop the loop.
3. Decided (session 163): the launcher checks progress, not the session, so a crashed or hung session is caught.
4. Decided (session 163): the launcher runs on herdr from the start.
5. Decided (session 163): ADR 0031's split: the kit writes files (sentinel, position, stop issue); the herdr side in `E:\herdr-sdlc` reads them.
6. Decided (session 164): the herdr sidebar (each loop's position, strike count and waiting state) is a second feature, `session-loop-sidebar`.
7. Decided (session 164): the reply comes in the session (the pane or a remote client); the `needs-ruling` issue is the notice and the record, never the reply channel.
8. Decided (session 164): after a self-wrap at 55 minutes the loop stays stopped until the user restarts it.
9. Decided (session 165, the design run's trial 1): a one-shot `CronCreate` wakes an idle interactive session; it fired at 17:44:02 for 17:44.
10. Decided (session 165, trial 2): `herdr pane send-text` then `send-keys Enter` types `/clear` and a skill into a Claude pane, when herdr is called with an argument list; Git Bash rewrites `/clear` to a path.
11. Decided (session 165, trial 3): the notice is `PushNotification` from the session, a desktop notice and the phone over Remote Control; the `needs-ruling` issue is the record.

## Notes

`[PO seat · authored]`

- From the Q11 regression mappings through Q15, the answers are Claude's recommendations, taken on the PO seat's word of 2026-11-22: "Go with all of your recommendations for the remainder of these questions."
- Session 166's way back to Q11 and Decisions (after intake parked the pair at r6) took Claude's recommendation on each answer, on the PO seat's word of 2026-11-22: "Yes". Three merges join two checks one unit already delivered; SC1.1 takes SC1.3 from the live sitting, so the launcher's live restart reads the new session's ready-state.

## Appendix

### Gherkin

`[PO seat · derived from r9]`

```gherkin
Scenario: SC1.1 The launcher restarts the session where it stopped
  Given a session in a herdr pane whose wrap recorded Next and writes its sentinel
  When 60 seconds pass after the sentinel appears
  Then the launcher has typed `/clear` and then `/resume-session` into the same pane
  And the new session's ready-state names the same Next

Scenario: SC1.2 The sentinel follows the push
  Given a session running its wrap
  When the sentinel appears
  Then the wrap's commit is already on the remote branch

Scenario: SC1.3 A loop leaves team runs and the tree pane as they were
  Given a loop running in a herdr pane
  When a team run in it stops with no wrap, and the kit runs its `tree: notify:` command
  Then the launcher types nothing into the pane
  And the tree pane is flagged

Scenario: SC2.1 The stop files its question first, and the reply closes it
  Given a session that needs the user's answer
  When it stops, and the user later replies in the session
  Then an open `needs-ruling` issue held the question before the session waited
  And the session closed that issue on the reply

Scenario: SC2.2 A reply inside 55 minutes continues the session
  Given a session waiting at a human-needed stop
  When the user replies in the session 54 minutes after the stop
  Then the same session continues
  And no wrap runs and no sentinel appears

Scenario: SC2.3 A stop ends on its question and a wrap asks nothing
  Given a session in a loop
  When it reaches a human-needed stop, or it wraps
  Then the stop's last message ends on its question
  And the wrap's closing message asks nothing

Scenario: SC3.1 No reply in 55 minutes starts the wrap
  Given a session waiting at a human-needed stop
  When no reply comes
  Then the session starts its wrap between 54 and 56 minutes after the stop

Scenario: SC3.2 After a self-wrap the loop stays stopped
  Given a session that wrapped itself 55 minutes after a stop
  When the wrap's sentinel appears
  Then the launcher types nothing into the pane
  And the `needs-ruling` issue stays open

Scenario: SC3.3 The open question waits for the user
  Given a self-wrap that left its `needs-ruling` issue open
  When the user starts the next session and runs `/cairn status`
  Then "Waiting on you" lists that issue

Scenario: SC4.1 Two strikes stop the loop
  Given a session that ended at the position it started from
  When the next session also ends at the position it started from
  Then the launcher types nothing
  And it files one issue naming that position

Scenario: SC4.2 Progress resets the strikes
  Given a loop with one strike
  When a session ends at a position other than the one it started from
  Then the strike count is zero

Scenario: SC4.3 A crashed or hung session stops the loop
  Given a session in a loop
  When its Claude process exits with no sentinel, or its pane shows no change for 60 minutes with no sentinel
  Then the launcher types nothing
  And it files one issue naming the pane and the last position

Scenario: SC5.1 An empty Next files one pick issue, never a second
  Given `/cairn status` prints Next as "(none)"
  When the session wraps
  Then the wrap files one "Pick the next deliverable" issue labelled `needs-ruling`, none when one is already open
  And the launcher types nothing

Scenario: SC5.2 The loop never picks a deliverable
  Given Next is empty
  When the session wraps
  Then the wrap's commit leaves Next empty
```

### Terms

`[PO seat · authored]`

- **wrap**: a session's close: record Next and the position, commit, push, then write the sentinel.
- **launcher**: the process outside any session that, after a wrap, starts the next session in the same herdr pane and checks progress.
- **sentinel**: the file the wrap writes last; it tells the launcher the wrap finished.
- **position**: where a wrap stopped: the plan step and the unit task.
- **strike**: a session that ends at the position it started from; two strikes in a row stop the loop.
- **`needs-ruling`**: the GitHub issue label `/cairn status` prints under "Waiting on you".
- **session loop**: the chain of sessions in one herdr pane, each started by the launcher after the last one's wrap.
- **human-needed stop**: a stop where the session needs the user's answer: it files a `needs-ruling` issue and waits.
- **self-wrap**: the wrap a session runs on its own 55 minutes after a human-needed stop with no reply; the loop stays stopped after it.
- **hung**: a session whose pane shows no change for 60 minutes with no sentinel; the launcher treats it as crashed.
