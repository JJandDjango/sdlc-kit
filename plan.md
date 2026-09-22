# Plan - Session 38, second deliverable (2026-09-21) - tree-view intake to ready (r4)

**Closed.** The deliverable is met: `specs/tree-view/contract.yaml` is
ready-green at `f3c80d0`, the language door at zero, every unit
`confirmed_by: [user]`, committed alone. The REQUEST carries its r4 row and
the appendix. The units start in a fresh session.

Where things stand: five decisions as planned, each answered yes. The
readback kept all ten units as written; no fact of r3 was lost to the
controlled register, so no OPEN entered the REQUEST.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a fact the contract cannot keep).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Open.~~ Done at `ef1d99d`, with this plan.
2. ~~Author.~~ Scaffolded and written from r3; draft-green on the first
   pass, the language door at zero after one rewrite (every sketch
   sentence opens on "verify").
3. ~~Readback.~~ The unit graph, the ten units, the three plan answers and
   the seven entities; all kept.
4. ~~Write and loop.~~ `confirmed_by: [user]` on every unit, ready-green on
   the first pass; the r4 row and the appendix written; the intake
   committed at `f3c80d0`.
5. ~~Close.~~ STATE.md regenerated and this plan struck through; the PR
   carrying this commit merges on your word.

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
