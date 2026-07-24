# Plan - Session 6 (2026-07-24)

The ADR-0004 program sequence resumes: G2 + G3 deep pages (8 conditions).
User opened with the G2 walk. Interactive walk-through mode (tour, rulings
one at a time - the session-4 pacing preference); docs authored after the
tour. Q8 already resolved (0007), so G2's session slims to condition
specification; Q3 waits at the G3 walk.

## This session

1. Refresh this plan (done - this file).
2. G2 tour stop 1 - Frame: identity + why (correct-by-construction
   headline, principles 1/2/4/5, authored -> enforced fan-out); land the
   G1.2 <-> G2.1 model-checking division (spec-side vs design-side model).
3. Tour stop 2 - G2.1 design-level model checking: consume 0007, fix pass
   condition -> `specified`.
4. Tour stop 3 - G2.2 breaking-change baseline lock: fix pass condition
   (PublicAPI / OpenAPI / buf baselines committed + G4.6-protected before
   implementation) -> `specified`; ratchet baselines routed to stop 7.
5. Tour stop 4 - G2.3 ADR review (human): ratify significance triggers +
   review attestation checklist -> `specified`.
6. Tour stop 5 - G2.4 threat-model existence: fix pass condition (STRIDE
   per trust boundary; every abuse case -> >=1 security acceptance test);
   recording venue deferred (0007 precedent) -> `specified`.
7. Tour stop 6 - G2.5 spec-suite red run: fix pass condition (suites
   compile against locked scaffold; every criterion test red, zero pass)
   -> `specified`.
8. Tour stop 7 - Close-out: completeness check (three prepared findings:
   ratchet-baseline lock gap - candidate G2.6; arch-rule-test existence ->
   G2.3 checklist item; typestate presence -> G2.3 checklist item);
   operators & harness; decisions.
9. Authoring pass: `docs/gates/G2-design-architecture.md` (0004 template,
   G1 page as exemplar) + registry cascade (Deep-page line, lifecycle
   flips, counts). Commit the G2 wrap (Theory trailer); push on explicit
   approval.
10. The G3 walk (own itinerary at its start; Q3 couples to the
    conventions-enforcer arc in `E:\claude-orchestrator`).
11. Session end: STATE.md regen, commit, push on explicit approval.

## Schedule (unchanged from session 5)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 6 | G2 + G3 | 8 | Q3 first analyzers (this session) |
| 7 | G4 solo | 9 | Q1 immutability mechanism ADR; REQ-ID format; ratchet shape |
| 8 | G5 + G6 | 8 | Q4 mutation-floor procedure; trace-conformance criteria |
| 9 | G7 + G8 | 7 | benchmark-budget + SLO procedure shapes |
| 10 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 11 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |
