# Plan - Session 7 (2026-07-24)

The ADR-0004 program sequence continues: the G3 deep page (3 conditions,
G3.1-G3.3). G2 consumed all of session 6, so the S6 G2+G3 slot splits
across two sessions and every later gate shifts one right (schedule
below). Interactive walk-through mode (tour, rulings one at a time);
docs authored after the tour. Q3 resolves or defers at stop 3 - it
couples to the conventions-enforcer arc in `E:\claude-orchestrator`
(ratified design + E1-E5 seed list at `designs/conventions-skill.md`
there; rollout discipline extract -> ratify -> compile, advisory ->
gating).

## This session

1. Refresh this plan (done - this file).
2. G3 tour stop 1 - Frame: identity + why (inner loop clean at zero
   human cost, seconds cadence, machine-applicable fixes; the Developer
   agent's only write surface; the pipeline's inversion point - G0-G2
   author enforcement instruments, G3 authors only their object); land
   the G3 <-> G4.1 echo division (latency vs authority, single-sourced
   config, PL-PIPE governance of the configs).
3. Tour stop 2 - G3.1 formatter: fix pass condition (zero formatting
   diffs) -> `specified`.
4. Tour stop 3 - G3.2 StyleCop + custom Roslyn analyzers: resolve or
   defer Q3 (first analyzer list; does convention extraction generate
   stubs; pipeline-native analyzers like G10.1 sunset escalation vs
   house-convention analyzers from the enforcer arc); fix pass
   condition -> `specified`. ADR 0008 if Q3 lands a policy.
5. Tour stop 4 - G3.3 strict compile: fix pass condition (`Nullable`
   enable, `TreatWarningsAsErrors`, `AnalysisLevel latest-all`) ->
   `specified`.
6. Tour stop 5 - Close-out: completeness check (one prepared finding:
   no explicit unit-tests-green condition at G3 or G4 - "local build
   red" covers compile, no G4 row runs the Developer's unit suite,
   though G5.5 mutation presupposes it); operators & harness;
   decisions.
7. Authoring pass: `docs/gates/G3-implementation.md` (0004 template, G2
   page as exemplar) + registry cascade (Deep-page line, lifecycle
   flips, counts) + ADR 0008 if ratified. Commit the G3 wrap (Theory
   trailer); push on explicit approval.
8. Session end: STATE.md regen, commit, push on explicit approval.

## Schedule (rebased: G2+G3 split, later gates shift one right)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 7 | G3 solo | 3 | Q3 first analyzers (this session) |
| 8 | G4 solo | 9 | Q1 immutability mechanism ADR; REQ-ID format; ratchet shape |
| 9 | G5 + G6 | 8 | Q4 mutation-floor procedure; trace-conformance criteria |
| 10 | G7 + G8 | 7 | benchmark-budget + SLO procedure shapes |
| 11 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 12 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |

Banked inputs (detail in STATE.md): the G4 session inherits the
protected root `specs/**` (incl. task contracts), the ratchet
enforcement package, and the REQ-ID / criterion-annotation format; the
G5 session inherits the native-interop memory-safety taxonomy gap.
