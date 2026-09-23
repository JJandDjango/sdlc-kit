# Plan - Session 44 (2026-09-23) - pane-view to intake

**Deliverable:** `pane-view` ready at intake. r3 adds the checks and the
solution half, signed by both seats; `/sdlc intake` then writes contract
`pane-view`, which validates ready-green and reads zero at the language
door.

Where things stand: the request is at r2 (features 1 to 4 kept, 5 and 6
struck, OPEN 1 left for the checks). It lands before tree-view's t6; t9's
USAGE pass and 0.15.0 carry it. The tree pane (`w9:p8`) still runs,
flagged `sdlc`, `blocked` on t6's `approve-tests`. Nothing before intake is
a contract unit, so the pane shows none of this session's work until
contract `pane-view` exists.

## Decisions

The user ruled both yes on 2026-09-23.

1. The deliverable stops at intake; the units build from session 45.
   Tree-view took the same step as one session (38), and intake is where
   both seats sign.
2. OPEN 1: the id part is always shown; `parts:` picks among the other
   six. The id is what a reader copies into the query face.

## Steps

1. Open. Branch `session-44-pane-view`; this plan; `plan.workflow.json` and
   the Diagram section removed, since the user retired Archify plans for
   the pane (2026-09-23). Commit; the PR opens at the close.
2. Back up the REQUEST to the scratchpad: it is untracked, so git cannot
   restore it.
3. r3, the checks: OPEN 1 answered; checks for features 1 to 4, with their
   messages verbatim. The PO seat signs.
4. r3, the solution half: scope, interfaces, constraints, units (a USAGE
   pass zero first, documentation first), sequencing; risks and cost;
   decisions; traceability; notes; an ADR only if a ruling needs one.
   Each sketch sentence opens on "verify". The engineer seat signs.
5. Intake: `/sdlc intake` writes contract `pane-view`: ready-green, zero
   at the language door, `confirmed_by: [user]` on each unit; r4 stamped.
   Commit.
6. Close: STATE.md regenerated, this plan struck; the push and the PR on
   your word.

Deferred, not this session:
- pane-view's units, then tree-view t6 and t9 (0.15.0), then G1.
- The pilot's config line, in the engine's session.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; every herdr probe closes the panes it opens.
