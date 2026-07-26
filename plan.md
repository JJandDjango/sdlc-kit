# Plan - Session 12 (2026-07-26)

The ADR-0004 program sequence closes: the PL-DOC + PL-PIPE walk - the
two cross-cutting lifecycles (PL-DOC Documentation, 3 conditions, CI +
scheduled sweep: docs are injected context, staleness is a defect
vector; PL-PIPE Pipeline integrity, 3 conditions, separate approval
channel: the enforcement layer is the highest-privilege artifact set),
the last six `registered` conditions - then the program close-out
audit over all 54. Interactive walk-through mode (tour, rulings one at
a time, ratified before edits land); docs authored after the tour.
Decisions this session likely forces (schedule row): the Q7
enforcement-layer change-control ADR (four direction-conditional
worked instances banked: 0010/G4.8 channel weight, G9.2 windows, G9.3
allowlist exceptions, 0013 date moves). Structural questions the walk
must answer: the PL-DOC/PL-PIPE boundary (agent prompts are class E -
which docs are context-load-bearing enough to join them); whether
PL-DOC inherits the diff/world two-arm division (merge arm + sweep
arm, G4.9/G9.3 precedent); how PL-PIPE.1's second channel escapes
self-reference (who approves changes to the approval workflow).

## This session

1. Refresh this plan (done - this file).
2. Tour stop 1 - Frame: PL identity (cross-cutting lifecycles, not
   phase exits - conditions convene inside existing venues; PL-PIPE
   alone owns a venue no other gate may share, the second channel);
   PL-DOC identity (docs-as-injected-context thesis; pace-layering -
   fast layers drift-gated, slow layers change-controlled; the
   two-arm question); PL-PIPE identity (one diff can delete every
   gate; the registry itself is in scope; why the other 48
   conditions stay conditions); the boundary line between them;
   roster agenda 3 + 3; gap candidates named (close-out decides).
3. Stop 2 - PL-DOC.1 doc samples compile/execute: subject inventory
   (which docs carry samples; generated subjects banked - release
   notes from G7.2 payloads, deprecation dossiers); extraction +
   execution harness shape (two-layer: .NET reference profile);
   vacuity polarity (zero samples extracted - green or red); venue
   (doc-touching merges). -> `specified`.
4. Stop 3 - PL-DOC.2 doc coverage: the denominator
   (one-artifact-many-consumers: the locked API baselines /
   PublicAPI.Shipped.txt as coverage input); what counts as covered;
   ratchet vs absolute (zero-missing at greenfield, G4.8
   discipline); undocumented-new-surface at merge vs sweep.
   -> `specified`.
5. Stop 4 - PL-DOC.3 staleness dating: the dating mechanism
   (authored dates vs git facts; the covers-marker precedent);
   thresholds per pace layer -> clocks.yaml (0012, numbers Q4); what
   staleness blocks (sweep red vs flagged-before-context-reuse -
   intake coupling); sweep liveness (dead sweep reads red, G9
   discipline). -> `specified`.
6. Stop 5 - PL-PIPE.1 enforcement-layer change control (human, the
   sixth census seat): class-E inventory consolidation (scope line +
   S9-S11 growth: environment definition, monitoring config, rollout
   policy, chaos plan, clocks artifact, allowlists, root configs,
   flag schema, tightening-job config); the Q7 workflow ruling - who
   the second channel is, how approval is recorded, 0010's
   mechanical arm (G4.6 E-provenance) as the teeth;
   direction-conditionality generalized (tightenings auto-approve,
   loosenings take the full channel - four instances on record);
   self-reference (changes to this workflow take the strongest
   channel). -> `specified` + ADR 0014.
7. Stop 6 - PL-PIPE.2 gate-config golden tests: what a golden test
   asserts (config x fixture facts -> decision, regression-pinned);
   subject inventory (S10-S11 banked: admission interlocks, slo.yaml
   derivation, clocks.yaml derivations, record<->mark coherence,
   notification-clock computation, migration classification, G9.4
   three-lane routing); coverage teeth (decision-bearing class-E
   config without goldens reads red); venue (enforcement-layer CI).
   -> `specified`.
8. Stop 7 - PL-PIPE.3 agent-behavior evals: subjects (the harness
   prompt set - Spec, Developer, QA, Verifier); what an eval asserts
   (behavioral invariants - anti-gaming probes, session-7 finding;
   write-surface discipline under adversarial instruction);
   eval-before-deployment mechanics (prompt edit = class E:
   PL-PIPE.1 channel + PL-PIPE.3 green); the suite itself is class
   E; relation to Q5 (evals regression-guard decorrelation, don't
   design it). -> `specified`.
9. Stop 8 - Program close-out audit (all 54): the x3 pattern sweeps
   (fail-closed polarity; schema-incompleteness teeth;
   one-artifact-many-consumers - where each should apply and
   doesn't); human census (exactly six, each with non-delegability
   rationale); taxonomy closure both directions (every row a closing
   condition, every Closes line anchored); open-parameter index
   post-Q7 (Q4-numeric-only confirmed); build-item register + the
   Q6-conditional inventory complete; counts 54/54.
10. Stop 9 - Close-out: rejections with routing; cascades (taxonomy
    rows for doc-staleness / enforcement-compromise classes if
    ruled; checklist); decisions inventory (0014 + anything the
    audit forces); the program's forward hand-off (everything
    activation-shaped rides Q6 - the pilot checklist).
11. Authoring pass: `docs/gates/PL-DOC-documentation.md` +
    `docs/gates/PL-PIPE-pipeline-integrity.md` (0008 two-layer
    template, G9/G10 pages as exemplar) + registry cascade
    (Deep-page lines, lifecycle flips, counts 48 -> 54 mod
    adoptions, open-parameter index post-Q7) + ADR 0014 +
    audit-driven cascades + STATE.
12. Session end: STATE.md regen, commit the program wrap (Theory
    trailer); push on explicit approval.

## Schedule (rebased: G2+G3 split, later gates shift one right)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 8 | G4 solo (done) | 11 ruled | Q1 -> ADR 0010; REQ-ID -> ADR 0011; ratchet shape |
| 9 | G5 + G6 (done) | 10 ruled | Q4 mutation-floor procedure; trace-conformance criteria |
| 10 | G7 + G8 (done) | 8 ruled (G7.5 adopted) | benchmark-budget + SLO procedure shapes |
| 11 | G9 + G10 (done) | 7 ruled (G9.4 adopted; G10.2 trend struck) | ADR 0012 stop-the-line; ADR 0013 sunset |
| 12 | PL-DOC + PL-PIPE (this session) | 6 + program audit | Q7 -> ADR 0014; close-out findings |

Banked inputs (detail in STATE.md): Q7 worked-example set = four
direction-conditional instances (0010/G4.8 channel weight, G9.2
windows, G9.3 allowlists, 0013 date moves). PL-PIPE.2 golden-test
inventory: S10 (admission interlocks, slo.yaml derivation) + S11
(clocks.yaml derivations, record<->mark coherence, notification-clock
computation, migration classification, G9.4 three-lane routing).
PL-PIPE.1 class-E inventory grown S9-S11: environment definition,
monitoring config, rollout policy, chaos plan, clocks artifact,
allowlists, root configs, flag schema, tightening-job config. PL-DOC
subjects banked: deprecation dossiers + release-notes generation from
G7.2 payloads. Audit inputs: patterns named x3 (fail-closed polarity,
schema-incompleteness teeth, one-artifact-many-consumers); human
census six (G1.3, G2.3, G6.1, G6.2, G8.3, PL-PIPE.1).
