# Plan - Session 37 (2026-09-21) - tree-view: the strike pass

**Deliverable:** `REQUEST_tree-view_2026-09-21.md` at r2: the nine
candidate criteria struck or kept, the three OPENs ruled, signed by the PO
seat. No check is written before r2.

Where things stand: kit 0.14.0 is released and nothing is in flight. The
pilot consumer, ImSim Engine, closed its session 10 by vetting G0 on 0.14.0
and handing the kit a finding (`no-check-reads-the-source-document`) and
the request half of `tree-view`. The user chose `tree-view` for this
session; G1 follows it. About eight decisions: one batch of uncontested
criteria, about three contested ones, the three OPENs, the r2 signature.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a criterion that needs an unbuilt
request). Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. STATE.md takes engine session 10: the G0 vetting, the new finding, the
   `tree-view` pick, G1 next. Committed with this plan on
   `session-37-tree-view`, which carries `c87ef7f`.
2. The strike, nine criteria. One message lists all nine with my
   recommendation (keep, strike, reword); you accept the uncontested ones
   as a set, and each contested one gets its own message. The grounds: ADRs
   0024, 0027 and 0029, the engine's cursor prototype
   (`tools/plan_graph.py`) and its `plan-granularity-one-node-one-task`
   finding. A criterion that needs `spec-doc-type` or `derived-language`
   moves to a later cut, not a wait. SC8 carries the herdr seam: the kit
   ships the tree as a plain command, and the herdr plugin wraps it outside
   the kit.
3. The three OPENs, one message each, each with a recommendation: where
   tasks, approvals and the cursor live under ADR 0027; how the view reads
   the spec doc's rows while ADR 0029 keeps tooling off headings; whether
   the per-unit task template becomes the kit's code-writing plan.
4. r2 into the REQUEST: the kept criteria reworded where the strike changed
   them, the OPENs answered under Decisions, a revision row signed by the
   PO seat. The file stays the requester's, untracked.
5. Close: STATE.md regenerated, this plan struck through, one PR carrying
   `c87ef7f` and this session's commits, merged on your word.

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
