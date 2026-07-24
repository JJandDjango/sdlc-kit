# Plan - Session 9 (2026-07-24)

The ADR-0004 program sequence continues: the G5 + G6 walk - the nightly
tier (G5 Integration/System, 6 conditions, outcome = promotion to
release candidate) and the staging tier (G6 UAT/Staging, 2 conditions,
outcome = candidate acceptance). Interactive walk-through mode (tour,
rulings one at a time, ratified before edits land); docs authored after
the tour. Decisions this session likely forces (schedule row): the Q4
mutation-floor procedure (G5.5) and trace-conformance criteria (G5.6).
Banked inputs consumed here: G4.11 as G5.5's named precondition
(one-run totality substrate enforced at merge); the native-interop
memory-safety gap (taxonomy `-` row; couples to G3.3 clause 4's
compensating-control demand); the mandatory generated-input oracle
scope (anti-overfit - G5.2/G5.3 must fix which components carry
generated-input oracles; likely back-propagates a G1.3 checklist item).

## This session

1. Refresh this plan (done - this file).
2. Tour stop 1 - Frame: G5 identity (nightly on main, hours budget,
   promotion to release candidate) + G6 identity (staging, per
   candidate, candidate acceptance); venue semantics after G4's merge
   queue - what a red nightly seizes (promotion, not merges?);
   operators (G5 execution-only like G4? who is G6's human subject);
   roster agenda 6 + 2.
3. Stop 2 - G5.1 consumer-driven contract verification: pact-set
   totality (all consumers), pact provenance and residence, PactNet.
4. Stop 3 - G5.2 + G5.3 the generated-input oracle pair: differential
   testing against the authored naive reference (a spec-stage artifact
   - its provenance and protection) and fuzzing (SharpFuzz); banked
   scope ruling - which components MUST carry generated-input oracles
   (anti-overfit; G1.3 back-propagation); native-interop memory-safety
   gap disposition (fuzzing as the compensating control for the
   taxonomy `-` row). -> both `specified`.
5. Stop 4 - G5.4 systematic concurrency testing: Coyote scope (which
   components; 0007 hard-core coupling), interleaving budget.
   -> `specified`.
6. Stop 5 - G5.5 mutation threshold: Q4 mutation-floor procedure
   (likely forced; floor numbers stay Q4-open), changed-code scope,
   G4.11 precondition linkage. -> `specified`.
7. Stop 6 - G5.6 model trace-conformance: conformance criteria (likely
   forced), 0007 hard-core designation coupling, trace-capture
   mechanics. -> `specified`.
8. Stop 7 - G6.1 + G6.2: human validation against REQ-IDs (staging
   walk; 0011 criteria.yaml as the checklist source) + exploratory
   testing (findings become new REQ-IDs - the loop back into the spec
   channel). -> both `specified`.
9. Stop 8 - Close-out: completeness check, operators & harness,
   decisions inventory, S10 banked inputs.
10. Authoring pass: `docs/gates/G5-integration-system.md` +
    `docs/gates/G6-uat-staging.md` (0008 two-layer template, G4 page
    as exemplar) + registry cascade (Deep-page lines, lifecycle flips,
    counts 23 -> 31, open-parameter index) + ADR(s) if forced + STATE.
    Commit the G5+G6 wrap (Theory trailer); push on explicit approval.
11. Session end: STATE.md regen, commit, push on explicit approval.

## Schedule (rebased: G2+G3 split, later gates shift one right)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 8 | G4 solo (done) | 11 ruled | Q1 -> ADR 0010; REQ-ID -> ADR 0011; ratchet shape |
| 9 | G5 + G6 (this session) | 8 | Q4 mutation-floor procedure; trace-conformance criteria |
| 10 | G7 + G8 | 7 | benchmark-budget + SLO procedure shapes |
| 11 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 12 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |

Banked inputs (detail in STATE.md): consumed this session - G4.11 ->
G5.5 precondition; native-interop memory-safety gap; generated-input
oracle scope. Held for S11 - G9 tightening-job shape (0010
direction-conditional auto-approve), G9.2 SLA windows (G4.9's
soft-seize backstop consumes them), G9.3 license-sweep division. Held
for S12 - Q7 worked example (0010/G4.8 channel-weight tiering);
PL-PIPE.2 fixture pattern (traceability + battery golden tests).
