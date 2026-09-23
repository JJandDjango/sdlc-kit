# Plan - Session 44 (2026-09-23) - pane-view to intake

**Deliverable:** `pane-view` ready at intake. r3 adds the checks and the
solution half, signed by both seats; `/sdlc intake` then writes contract
`pane-view`, which validates ready-green and reads zero at the language
door.

**Closed.** The deliverable is met: contract `pane-view` at `6fd9c17`,
ready-green on the first pass, language door zero after one rewrite, five
units each `confirmed_by: [user]`; all fifteen kit contracts ready-green,
pytest 486 passed, scope-check green. The REQUEST stands at r4. The push
and the PR wait on the user's word.

Where things stood: the request was at r2 (features 1 to 4 kept, 5 and 6
struck, OPEN 1 left for the checks). It lands before tree-view's t6; t9's
USAGE pass and 0.15.0 carry it. The tree pane (`w9:p8`) still runs,
flagged `sdlc`, `blocked` on t6's `approve-tests`. Nothing before intake is
a contract unit, so the pane showed none of this session's work.

## Decisions

The user ruled both yes on 2026-09-23.

1. The deliverable stops at intake; the units build from session 45.
   Tree-view took the same step as one session (38), and intake is where
   both seats sign.
2. OPEN 1: the id part is always shown; `parts:` picks among the other
   six. The id is what a reader copies into the query face.

## Steps

1. ~~Open.~~ Done at `cf200b0`.
2. ~~Back up the REQUEST.~~ r2 copied to the scratchpad.
3. ~~r3, the checks.~~ Prerequisites, nine checks, two verbatim messages;
   OPEN 1 answered. Signed by the PO seat.
4. ~~r3, the solution half.~~ Five units p0 to p4, eight decisions, no
   ADR. Signed by the engineer seat.
5. ~~Intake.~~ Done at `6fd9c17`: ready-green first pass, language door
   zero after one rewrite (setting for key, field for part, the last
   segment for the short id); every unit kept by seat `user`; the
   appendix derived and r4 stamped.
6. ~~Close.~~ STATE.md regenerated; this plan struck; the push and the PR
   go to the user.

Deferred, not this session:
- pane-view's units, then tree-view t6 and t9 (0.15.0), then G1.
- The pilot's config line, in the engine's session.
- `.sdlc/config.yaml` still lists `plan.workflow.json` as a free path.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; every herdr probe closes the panes it opens.
