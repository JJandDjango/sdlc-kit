# Plan - Session 37 (2026-09-21) - tree-view: the strike pass

**Closed.** The deliverable is met: `REQUEST_tree-view_2026-09-21.md` is
at r2, signed by the PO seat, with zero OPEN marks. The next session starts
a new plan at r3.

Where things stand: the strike kept eight of the nine candidates, moved SC9
under Decisions, answered the three OPENs and recorded two more decisions.
It took five human decisions, not the eight planned: ADR 0024 had already
answered OPEN 1, and OPEN 2 was SC1's question.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a criterion that needs an unbuilt
request). Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~STATE.md takes engine session 10.~~ Done at `ce0cdec`, with this plan.
2. ~~The strike.~~ One batch: SC2, SC4, SC6 and SC8 kept, SC5 reworded, SC9
   struck, OPEN 1 answered by ADR 0024, two non-goals. Two contested calls:
   SC1 starts at the contracts and reads no document; check runs are
   recorded, so SC3 and SC7 stand as written.
3. ~~The three OPENs.~~ OPEN 1 in the batch, OPEN 2 with SC1, OPEN 3 its
   own call: one fixed task list per unit, Two-Key last, never enforced.
4. ~~r2 into the REQUEST.~~ Written and signed by the PO seat, 2026-09-21.
5. ~~Close.~~ STATE.md regenerated and this plan struck through; the PR
   carrying this commit merges on your word.

Deferred, not this session:
- `tree-view` after r2: the checks and the solution half (r3), intake to
  ready (r4), the units, the herdr plugin.
- G1: the pilot's M0 code waits on its criteria review.
- `no-check-reads-the-source-document`: which request carries it.
- `derived-language`, `feature-document`, `spec-doc-type`; the demo intake
  in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b; the G4.6
  finding.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer, alone in the final paragraph, on every commit that
touches a non-free path; uncontested decisions batched in one message,
contested ones one per message, each with a recommendation; approval
content shown in chat in full.
