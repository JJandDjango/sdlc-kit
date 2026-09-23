# Plan - Session 43 (2026-09-23) - the herdr hook

**Deliverable:** the herdr hook on t8's notify command, outside the kit.
When the tree pane arrives at an approval, herdr shows that a seat is
waiting; once the seat is answered, the flag clears.

**Closed.** The deliverable is met: the hook at `787e415` in
`E:\herdr-sdlc`, a Two-Key PASS at round 1, its README verified at
`a03ee84`; the kit's config line at `28d09d8`. Started on the kit, the
pane reads `waiting on a seat` for t6's `approve-tests`, and herdr shows it
as `sdlc`, `blocked`. The push and the PR wait on the user's word.

## What the probe found

Measured this session on herdr 0.9.1 (client) and 0.9.0 (server):

- An outside `herdr pane report-agent --state blocked` never changes a
  Claude pane's state: idle or working, from any source, with or without
  the session id. `herdr agent explain` shows why: herdr reads Claude's
  state only from its screen-detection rules. The hook cannot flag the
  Claude pane.
- On a pane with no detected agent, the same report shows as agent `sdlc`,
  state `blocked`, and `release-agent` clears it. The tree pane is such a
  pane, and the notify command inherits its `HERDR_PANE_ID`, so the hook
  needs no other pane's id.

## Features (strike what you don't want)

1. **Seat flag.** At each arrival at an approval, the tree pane shows in
   herdr's sidebar as agent `sdlc`, state `blocked`, with the message
   `approve-tests for tree-view/t6-query-face`.
2. **The flag clears.** Once the pane's first line stops reading `waiting
   on a seat`, the hook releases the flag; Ctrl-C in the pane releases it
   too. When the line names a different seat, the hook leaves the flag to
   that seat's hook.
3. **Toast.** At each arrival, a herdr toast reads `waiting on a seat`,
   names the approval and the unit, and plays the request sound.
4. **One key opens the pane.** A herdr plugin action splits a pane beside
   the focused one and runs `python -m taskcontract tree --follow`.
   Recommended: strike it for now. It needs a herdr key binding and the
   Windows action workaround, and two commands open the pane by hand.
5. **The config line.** `tree: notify: python E:/herdr-sdlc/herdr_seat.py`
   in the kit's `.sdlc/config.yaml`, a free path, so no contract. The
   pilot's line waits for the engine's session.

Outside herdr (`HERDR_ENV` not 1) the hook does nothing and exits 0.

## Decisions

The user ruled all three yes on 2026-09-23, after herdr's server moved to
0.9.1; the probe, re-run there, gave the same two facts.

1. The features: keep 1, 2, 3 and 5; strike 4.
2. Placement: a new local repo, `E:\herdr-sdlc`, holding the script, its
   tests and a README that records the kept features. Not
   `E:\claude-orchestrator`, whose `main` holds another session's
   uncommitted `launch.py` edit; not the kit, whose REQUEST puts the plugin
   outside it. No GitHub remote until you ask.
3. Delegation as in session 42: Workflow subagents build and verify;
   Claude approves the test list and the commit on review; you approve the
   push and the PR at the close.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, approvals dropping onto
it from above, an exception lane below for a Two-Key FAIL). Render and
open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Open.~~ Done at `12e2275`, after herdr's server moved to 0.9.1 and
   the probe, re-run, held.
2. ~~README first.~~ Done at `5b9219b` in `E:\herdr-sdlc`.
3. ~~Test list.~~ 31 tests (37 cases), drafted in the scratchpad, red on a
   stub, green on a prototype; approved as drafted. One README line added
   from its questions: another seat's exit carries a failed toast as 1.
4. ~~Tests red.~~ The module absent: collection fails.
5. ~~Green.~~ `herdr_seat.py`, 37 passed, no deviations.
6. ~~Live check.~~ Flag in 1.6 s, cleared about 2 s after the line went;
   Ctrl-C released it; hook exit 0 both times.
7. ~~Commit.~~ Done at `787e415`.
8. ~~Two-Key.~~ PASS at round 1, about 133K tokens: 37 green, four live
   paths ok, no blocking finding; four advisories, recorded in the README.
9. ~~The config line.~~ Done at `28d09d8`; the kit's pane flags t6's
   `approve-tests`.
10. ~~Close.~~ README markers 🟢 at `a03ee84`; STATE.md regenerated; this
    plan struck; the G1 question and the push and the PR go to the user.

Deferred, not this session:
- Flag the Claude pane itself: it needs a detection rule (a local
  `claude.toml` shadows herdr's remote one) or a change in herdr.
- Feature 4, the key action.
- The pilot's config line, in the engine's session.
- t6 (the query face) and t9 (the 0.15.0 release), with the advisories
  carried in STATE.md.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; every herdr probe closes the panes it opens.
