# Plan - Session 38, second deliverable (2026-09-21) - tree-view intake to ready (r4)

**Deliverable:** `specs/tree-view/contract.yaml`, derived from r3,
validating ready-green with the language door at zero, every unit
`confirmed_by`, committed alone. The REQUEST gains its r4 "Ready:" row and
the appendix. The units start in a fresh session.

Where things stand: r3 is signed by both seats and merged with ADR 0031
(PR #47 at `7d66466`). The seat roster is ratified, so intake can author.
The contract restates r3 in the controlled register; any fact a rewrite
cannot keep becomes an OPEN, not a silent edit.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a fact the contract cannot keep).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. Open. Branch `session-38-tree-view-intake`, this plan and its diagram.
   The open commit lands on your word.
2. Author. Scaffold `specs/tree-view/contract.yaml` and write it from r3:
   intent, scope, non-goals, ten units t0 to t9 with their done_means and
   sketches (check ids trailing), `depends_on` from the sequencing, and
   `entities` from the ratified glossary. Loop the language door to zero
   and the draft profile to green before you see it.
3. Readback. The unit graph, every unit's done_means and sketches, the
   three plan answers beside r3, and the entities, in one message. You
   keep, change or strike each unit and name the seats that answered.
4. Write and loop. `confirmed_by` on every unit; the ready profile to green
   and the language door at zero. The REQUEST gains the r4 row and the
   appendix: the contract pointer, 22 Gherkin scenarios, the terms. The
   intake commit, the contract alone with `Contract: tree-view`, lands on
   your word.
5. Close. STATE.md regenerated, this plan struck through, the close commit
   and the PR. The PR merges on your word.

## Decisions: five after this plan

1. The open commit.
2. The readback, one batch: each unit kept, changed or struck; the seats;
   the entities.
3. The intake commit.
4. The close commit and the PR.
5. The merge.

Deferred, not this session:
- `tree-view` units t0 to t9, then the release; the herdr plugin outside
  the kit.
- G1: the pilot's M0 code waits on its criteria review.
- `no-check-reads-the-source-document`: which request carries it.
- `derived-language`, `feature-document`, `spec-doc-type`; the demo intake
  in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b; the G4.6
  finding.
- From r3: a status field on the finding form; the agent personas writing
  progress.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer, alone in the final paragraph, on every commit that
touches a non-free path; uncontested decisions batched in one message,
contested ones one per message, each with a recommendation; approval
content shown in chat in full.
