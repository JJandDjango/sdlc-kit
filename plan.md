# Plan - Session 10 (2026-07-24)

The ADR-0004 program sequence continues: the G7 + G8 walk - the release
tier (G7 Release/Deploy, 4 conditions, outcome = the deploy + rollout
continuation) and the production tier (G8 Operations, 3 conditions,
outcome = further rollout + convergence closure). Interactive
walk-through mode (tour, rulings one at a time, ratified before edits
land); docs authored after the tour. Decisions this session likely
forces (schedule row): the benchmark-budget procedure shape (G7.1) and
the SLO procedure shape (G7.4 + G8.2) - numbers stay Q4-open. Banked
inputs consumed here: the G6 acceptance record as G7's admission input
(present + accepted + no unresolved blocking findings); the G5.1
verification matrix (can-i-deploy); the soak split's budget half (G7.1
owns absolute budgets on quiet infra); G6.3 deploy-rehearsal formalized
from G7's side; G5.6 <-> G8.1 shared trace instrumentation; production
chaos (G8 venue question, routed at S9 close-out); G8.3 reusing the
G6.2 conversion-record shape.

## This session

1. Refresh this plan (done - this file).
2. Tour stop 1 - Frame: G7 identity (release pipeline, per release,
   FAIL blocks the deploy; failing canary auto-reverts) + G8 identity
   (production runtime, continuous, FAIL blocks further rollout); the
   admission chain (G6 acceptance record + G5.1 can-i-deploy - what
   exactly G7 mechanically checks before anything runs); the
   verified-artifact chain end-to-end (G5 pins -> G6.3 certifies ->
   G7 deploys the same artifact; deploy-rehearsal from G7's side);
   operators (execution-only? who owns release; what "operator" means
   for a continuous venue); roster agenda 4 + 3; the SBOM/provenance
   gap (authored-here line names it, no condition enforces it -
   close-out candidate).
3. Stop 2 - G7.1 benchmark budgets: the soak split's budget half -
   absolute budgets on quiet infra; budget authorship + residence
   (spec-side artifact? G2 ratchet-baseline precedent); the
   benchmark procedure shape (likely forced: variance control,
   baseline discipline, what "vs baseline" means); numbers -> Q4.
   -> `specified`.
4. Stop 3 - G7.2 ApiCompat binary compatibility: binary vs source
   compat (relationship to G4.5's surface diff; G2.2 baseline chain);
   scope (which shipped binaries); delta + breaking-change semantics.
   -> `specified`.
5. Stop 4 - G7.3 IaC scanning: scope = the committed environment
   definition (G6.3 coupling - same artifact set, class E); gating
   severity (ratchet-at-zero precedent from G4.7); suppression
   discipline. -> `specified`.
6. Stop 5 - G7.4 + G8.2 the SLO pair: canary with SLO-based rollback
   (the G7<->G8 hinge) + SLO/error-budget alerts; SLO criteria
   authorship + residence (one artifact consumed by both); the SLO
   procedure shape (likely forced); auto-revert semantics; breach
   halts further rollouts (coupling back to G7.4). -> both
   `specified`.
7. Stop 6 - G8.1 runtime contract assertions: G5.6 <-> G8.1 shared
   trace instrumentation (banked - one instrumentation surface, two
   consumers); "stays silent" semantics (what an assertion fire is -
   incident? escape? auto-escalation); production overhead/sampling;
   hard-core coupling (0007). -> `specified`.
8. Stop 7 - G8.3 crash triage (human): the convergence loop's teeth
   ("an escape that does not produce a new criterion is itself a
   process failure" - how that is checked); the G6.2
   conversion-record shape reused (banked); triage operator + the
   human boundary (G6 precedent: principal grades); production chaos
   venue question (banked from S9 rejection routing). -> `specified`.
9. Stop 8 - Close-out: completeness check (SBOM/provenance candidate;
   anything else the walk surfaced), rejections with routing,
   taxonomy + checklist cascades, decisions inventory, S11 banked
   inputs.
10. Authoring pass: `docs/gates/G7-release-deploy.md` +
    `docs/gates/G8-operations.md` (0008 two-layer template, G5/G6
    pages as exemplar) + registry cascade (Deep-page lines, lifecycle
    flips, counts 33 -> 40, open-parameter index) + ADR(s) if forced
    + STATE.
11. Session end: STATE.md regen, commit the G7+G8 wrap (Theory
    trailer); push on explicit approval.

## Schedule (rebased: G2+G3 split, later gates shift one right)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 8 | G4 solo (done) | 11 ruled | Q1 -> ADR 0010; REQ-ID -> ADR 0011; ratchet shape |
| 9 | G5 + G6 (done) | 10 ruled | Q4 mutation-floor procedure; trace-conformance criteria |
| 10 | G7 + G8 (this session) | 7 | benchmark-budget + SLO procedure shapes |
| 11 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 12 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |

Banked inputs (detail in STATE.md): consumed this session - G6
acceptance record -> G7 admission; G5.1 can-i-deploy matrix; soak
split budget half; G6.3 deploy-rehearsal from G7's side; G5.6 <->
G8.1 trace instrumentation; production chaos venue question; G6.2
conversion-record shape -> G8.3. Held for S11 - G9 tightening-job
shape (0010 direction-conditional lane - now also corpus growth and
mutation-floor moves), G9.2 SLA windows (G4.9's soft-seize AND the G5
red-window escalation consume them), stop-the-line mechanics incl.
the contract fix-lane field (0005 touch), G9.3 license-sweep
division, Q4 numbers. Held for S12 - Q7 worked example (0010/G4.8
channel-weight tiering); PL-PIPE.2 fixture pattern (traceability +
battery golden tests).
