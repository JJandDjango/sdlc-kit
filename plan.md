# Plan - Session 29 (2026-09-08) - Playbook alignment: close the six gaps

Where things stand: v0.12.0 released; PR #37 (self-pin) open, green at cc29aa5,
mergeable. Branch `session-28-g0-pitch` (e7af41e, pushed, no PR) carries
NOTES_g0-pitch_2026-09-08.md. Step 1 done: video reviewed, Anthropic's
AI-Native SDLC playbook fetched (claude.com/blog/the-ai-native-sdlc-playbook,
2026-08-21) and mapped against the 56 conditions. Verdict: the kit covers every
play, mostly stronger; six gaps ratified for implementation (user, 2026-09-08).

## The six gaps

1. Hooks: deny writes to ready contracts and ratified terms in the session,
   before merge. 2. Scope check: a G4 condition failing a diff that leaves its
   contract's `scope`. 3. Code re-scan: a G9 sweep over unchanged first-party
   code with current rules. 4. Flow metrics: time-to-ready, rework count,
   first-pass merge, in-scope rate. 5. PO venue: intake without an engineer at
   the prompt. 6. Advisory review pass named in USAGE; escapes add an agent eval.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow: lanes by actor, phases per wave, an exception lane for parked
contracts and Verifier fails, three guided views). Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed. Every code unit lands as one commit,
Developer then Verifier (Two-Key). The unit graph per contract is computed
(`python -m taskcontract graph`), never committed; the diagram is the
session-level view of both contracts.

## Steps

1. ~~Video check~~ - done; playbook fetched; six gaps ratified.
2. Ratify the notes with the five amendments; write ADR 0026 and ADR 0027
   (alternatives = the playbook's four disagreements: mutable plan, advisory
   templates, committed plan, co-generated tests).
3. Close v0.12.0: merge PR #37 on the user's word, sync main, delete
   `session-27-self-pin`, prune the five gone local branches; PR
   `session-28-g0-pitch` carrying notes + ADRs, merge on green.
4. Wave A: intake `playbook-guardrails` (units U1-U7 in the diagram's cards),
   one commit per unit, Two-Key, PR, merge, tag v0.13.0, self-pin.
5. Demo intake: one real feature document, contract drafted in a sandbox
   consumer, not the kit's own specs/.
6. Wave B: intake `playbook-loop` (V1-V6), same discipline, v0.14.0.
7. Session close: STATE.md regenerated (stale "cc29aa5 never pushed" line
   retired), this plan struck through.

Open before intake A: the diff-to-contract binding for the scope check (branch
name, PR body, or a `Contract:` commit trailer; recommend the trailer, it is
what the Theory hook already parses). Open before intake B: cadence for the
re-scan (clocks.yaml, Q4 placeholder) and which four metrics stay.

House rules in force: no pipes/chains in any authored command string;
commit messages via Write + git commit -F; Two-Key on every code unit.
