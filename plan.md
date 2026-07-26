# Plan - Session 11 (2026-07-25)

The ADR-0004 program sequence continues: the G9 + G10 walk - the
maintenance tier (G9 Maintenance/Evolution, 3 conditions, scheduled
venue - the first gate that runs *between* changes rather than on
them) and the retirement tier (G10 Deprecation/Retirement, 3
conditions, sunset-driven - the only gate that forces deletion).
Interactive walk-through mode (tour, rulings one at a time, ratified
before edits land); docs authored after the tour. Decisions this
session likely forces (schedule row): Q4 ratchet-tightening cadence
(the tightening-job procedure) and the sunset policy (authorship,
notice, escalation) - numbers stay Q4-open. Structural question the
walk must answer: G9's authored-here line (dependency update policy,
scheduled ratchet tightening, refactoring budgets) has no condition
enforcing it - the S10 SBOM gap produced G7.5 by the same shape, so
a G9.4 tightening-job condition is a live candidate.

## This session

1. Refresh this plan (done - this file).
2. Tour stop 1 - Frame: G9 identity (scheduled jobs, weekly+, no
   diff and no PR to gate - what FAIL blocks in a venue with no
   change in flight; SLA breach escalates); G10 identity (build +
   scheduled, sunset-driven; accretion is the defect class); the
   between-features thesis (supply-chain rot + slow entropy accrue
   in quiet weeks); operators for operator-less venues (scheduled
   jobs run unattended - who owns a G9 red); roster agenda 3 + 3;
   the tightening-job gap named (stop 5 decides).
3. Stop 2 - G9.1 dependency PRs gated by full suite: what "full
   suite" spans (G4 + G5 per registry - does G6 acceptance or G7
   admission apply to bot PRs; is a bot PR an agent task with a
   task contract); G7.5 SBOM consumed for field-impact mapping
   (banked - which updates touch shipped surface); batch vs
   single-dependency discipline; G4.9 lockfile/advisory coupling
   (same audit, different trigger). -> `specified`.
4. Stop 3 - G9.2 vulnerability-fix SLAs: the SLA-window family is
   already consumed three ways (G4.9 soft-seize, G5 red-window
   escalation, G8.3 triage window - banked) - one policy artifact,
   authorship + residence; severity -> window mapping; what breach
   escalation means mechanically (stop-the-line mechanics incl. the
   0005 fix-lane field, banked - serves G5 and G8 reds alike);
   windows numeric -> Q4. -> `specified`.
5. Stop 4 - G9.3 license audit: the license-sweep division (banked
   - G4.9 gates the diff-time delta, G9.3 sweeps the full standing
   set; why both); allowlist authorship + residence (one artifact,
   two consumers); transitive scope; suppression/exception
   discipline. -> `specified`.
6. Stop 5 - The tightening job (G9's authored-here core): four
   input families banked (ratchet cadence Q4; corpus growth;
   mutation-floor moves; budget re-tightening from measurement
   records + ladder-assignment statistics); the cadence procedure
   shape (likely forced - what runs, what it reads, what it may
   tighten, who ratifies); condition or policy - adopt G9.4 or
   route; refactoring budgets' place. Cadence numbers -> Q4.
7. Stop 6 - G10.1 obsolete-sunset escalation: sunset-date
   authorship + residence (the deprecation mark shape - where the
   date lives so an analyzer can read it); warning -> error
   mechanics at the date (custom analyzer, enforcer-arc coupling);
   consumer notification via G7.2's contract-diff payload (banked -
   G10's authored-here line); sunset policy likely forced (minimum
   notice, who may set/move a date). -> `specified`.
8. Stop 7 - G10.2 dead-code ratchet: what counts as dead (tooling
   reach vs reflection/DI false-liveness); ratchet-family precedent
   (G4.8 shrink-only baseline shape - same discipline or G9-owned
   tightening); "trending down" semantics (<= baseline is a
   ratchet; a trend mandate is a different animal). -> `specified`.
9. Stop 8 - G10.3 data-migration verification: the
   contract-migration far end (banked - G7.4 proved N and N+1
   coexist at rollout; G10.3 proves the old path is safe to
   remove); migration-spec authorship (G10 authored-here) +
   verification venue (per-retirement, not weekly); relation to
   G6.3's certified environment for rehearsal. -> `specified`.
10. Stop 9 - Close-out: completeness check (tightening-job ruling
    lands; anything else the walk surfaced), rejections with
    routing, taxonomy + checklist cascades, decisions inventory
    (ratchet-cadence + sunset-policy ADRs if forced), S12 banked
    inputs.
11. Authoring pass: `docs/gates/G9-maintenance.md` +
    `docs/gates/G10-retirement.md` (0008 two-layer template, G7/G8
    pages as exemplar) + registry cascade (Deep-page lines,
    lifecycle flips, counts 41 -> 47, open-parameter index) +
    ADR(s) if forced + STATE.
12. Session end: STATE.md regen, commit the G9+G10 wrap (Theory
    trailer); push on explicit approval.

## Schedule (rebased: G2+G3 split, later gates shift one right)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 8 | G4 solo (done) | 11 ruled | Q1 -> ADR 0010; REQ-ID -> ADR 0011; ratchet shape |
| 9 | G5 + G6 (done) | 10 ruled | Q4 mutation-floor procedure; trace-conformance criteria |
| 10 | G7 + G8 (done) | 8 ruled (G7.5 adopted) | benchmark-budget + SLO procedure shapes |
| 11 | G9 + G10 (this session) | 6 | Q4 ratchet cadence; sunset policy |
| 12 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |

Banked inputs (detail in STATE.md): consumed this session - G9
tightening job's four input families (cadence Q4, corpus growth,
mutation-floor moves, budget re-tightening from measurement records
+ ladder-assignment statistics); G9.2 SLA windows already consumed
three ways (G4.9 soft-seize, G5 red-window escalation, G8.3 triage
window); stop-the-line mechanics incl. the 0005 fix-lane field; G9.1
<- G7.5 SBOM field-impact mapping; G9.3 license-sweep division; G10
notification <- G7.2 contract-diff payload; G10.3 = the
contract-migration far end. Held for S12 - Q7 worked example
(0010/G4.8 channel-weight tiering); PL-PIPE.2 fixture pattern (scope
grew S10: G7 admission interlocks + slo.yaml derivation compiles as
golden-test subjects); PL-PIPE scope consolidation (environment
definition, monitoring config, rollout policy, chaos plan - the
class E inventory grew S9-S10).
