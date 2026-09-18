# Plan - Session 31 (2026-09-17) - The interview, then the six gaps

Where things stand (2026-09-17): main at 16426dd (PR #39, the session 30
close). v0.12.0 closed, PR #37 merged (673cc24). PR #38 merged (7824b7a)
carrying the ratified NOTES_g0-pitch_2026-09-08.md, ADR 0026 and 0027, one
CONVENTIONS line, and this plan. Anthropic's AI-Native SDLC playbook
(claude.com/blog/the-ai-native-sdlc-playbook, 2026-08-21) is mapped against
the 56 conditions. Verdict: the kit covers every play, mostly stronger; six
gaps ratified for implementation (user, 2026-09-08). Prototype venue decided
(session 30): Google Docs, the intake-ready template in the user's Drive.
Session 31 ratified a new first step (ADR 0028): the specification
interview, a second plugin skill that writes the feature document, and
shipped it the same day on `session-31-spec-interview` (unmerged). Steps
1-4 done. Next: step 5, gated on two decisions.

## The six gaps

1. Hooks: deny writes to ready contracts and ratified terms in the session,
   before merge. 2. Scope check: a G4 condition failing a diff that leaves its
   contract's `scope`. 3. Code re-scan: a G9 sweep over unchanged first-party
   code with current rules. 4. Flow metrics: time-to-ready, rework count,
   first-pass merge, in-scope rate. 5. PO venue: intake without an engineer at
   the prompt. 6. Advisory review pass named in USAGE; escapes add an agent eval.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, reshaped 2026-09-09 into a step spine: one lane of plan steps read
left to right, human gates dropping onto it from above, an exception lane for
parked contracts and Verifier fails below, phases per wave, five guided views
starting with "Where we are"). Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed. Every code unit lands as one commit,
Developer then Verifier (Two-Key). The unit graph per contract is computed
(`python -m taskcontract graph`), never committed; the diagram is the
session-level view of both contracts.

## Steps

1. ~~Video check~~ - done; playbook fetched; six gaps ratified.
2. ~~Ratify the notes with the five amendments; write ADR 0026 and ADR 0027
   (alternatives = the playbook's four disagreements: mutable plan, advisory
   templates, committed plan, co-generated tests).~~ - done, session 30.
3. ~~Close v0.12.0: merge PR #37 on the user's word, sync main, delete
   `session-27-self-pin`, prune the five gone local branches; PR
   `session-28-g0-pitch` carrying notes + ADRs, merge on green.~~ - done,
   2026-09-09 (PR #37 at 673cc24, PR #38 at 7824b7a).
4. ~~Specification interview (ADR 0028, ratified 2026-09-17): the request is
   the kit's first feature document (`REQUEST_spec-interview_2026-09-17.md`);
   `/sdlc intake spec-interview` to ready-green; units S1-S5 (the diagram's
   cards), one commit each, Two-Key; USAGE section first (pass zero).~~ -
   done, 2026-09-17: seven commits on `session-31-spec-interview` (intake,
   S1-S5, the verifier's advisories), Two-Key PASS by a workflow verifier
   (16/16 sketches). Ships in v0.13.0 with wave A, no tag of its own.
5. Wave A: the two decisions below (done), then `/sdlc intake
   playbook-guardrails` to ready-green (done 2026-09-18: nine units u0-u8,
   the diagram's cards; u7 is amendment 2's intake prompts), one commit per
   unit with the `Contract:` trailer, Two-Key, PR, merge, tag v0.13.0
   (carrying step 4), self-pin. Branch `session-31-wave-a`, stacked on PR
   #40.
   - 5b, proposed and unratified: `taskcontract graph` emits Archify beside
     its Mermaid, so a contract's picture is derived, never hand authored
     (0024). Two units, its own small contract, after 0.13.0, before the demo.
6. Demo intake: the user copies the Drive template for one real feature (3-5
   success criteria, 2-3 Gherkin scenarios each), or runs the step-4
   interview; the contract is drafted in a sandbox consumer, not the kit's
   own specs/; USAGE gains the section beside section 8.
7. Wave B: intake `playbook-loop` (V1-V5), same discipline, v0.14.0.
8. Session close: STATE.md regenerated, this plan struck through.

Decided before intake A (user, 2026-09-17, on the recommendation). (1) The
diff-to-contract binding is a `Contract:` commit trailer, parsed like the
Theory trailer; every kit commit carries one from intake A on. (2) Gap 1 on
class-E paths (0027's open consequence): no special case; the hook denies the
spec channel and warns outside the bound contract's scope, tightening to
deny in wave B. Open before intake B: cadence for the re-scan (clocks.yaml,
Q4 placeholder) and which four metrics stay.

House rules in force: no pipes/chains in any authored command string;
commit messages via Write + git commit -F; Two-Key on every code unit.
