# Plan - Session 38 (2026-09-21) - tree-view r3: the checks and the solution half

**Closed.** The deliverable is met: `REQUEST_tree-view_2026-09-21.md` is
at r3, the checks signed by the PO seat and the solution half by the
engineer seat, with zero OPEN marks. The next session starts a new plan at
intake (r4).

Where things stand: the nine decisions went as planned, each as
recommended. One surprise rode the checks batch: a finding names a gate and
never a contract, and records no status, so SC1 changed shape before any
check was written. ADR 0031 records the rulings.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a question r3 cannot close).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Open.~~ Done at `4e9d474`, with this plan.
2. ~~The checks.~~ The red run ruled: a run records its expectation. SC1
   reworded for the findings; 22 checks and three verbatim messages signed
   by the PO seat.
3. ~~The solution half.~~ An ADR ruled in; the cursor derived from task
   states. Ten units, t0 to t9, signed by the engineer seat.
4. ~~r3 into the REQUEST.~~ Written with both signatures; ADR 0031
   committed at `205818e`.
5. ~~Close.~~ STATE.md regenerated and this plan struck through; the PR
   carrying this commit merges on your word.

Deferred, not this session:
- `tree-view` after r3: intake to ready (r4), the units, the herdr plugin.
- G1: the pilot's M0 code waits on its criteria review.
- `no-check-reads-the-source-document`: which request carries it.
- `derived-language`, `feature-document`, `spec-doc-type`; the demo intake
  in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b; the G4.6
  finding.
- From r3: a status field on the finding form; the agent personas writing
  progress.
- The engine's uncommitted `plan.md` edit (its cursor ticked after the
  push) is the engine session's to commit.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer, alone in the final paragraph, on every commit that
touches a non-free path; uncontested decisions batched in one message,
contested ones one per message, each with a recommendation; approval
content shown in chat in full.
