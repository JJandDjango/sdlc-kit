# Plan - Session 5 (2026-07-23)

User directive (recorded at session-4 close): a once-over of G1 - walk the
user through `docs/gates/G1-requirements-spec.md` until fully understood.
Interactive walk-through mode (tour, rulings one at a time - the session-4
pacing preference), no new artifacts unless rulings force them. The ADR-0004
program sequence (G2 + G3) resumes session 6; the schedule shifts one more
right (table below).

## This session

1. Refresh this plan (done - this file).
2. Tour stop 1 - Frame: identity + why (widest authoring gate, the
   authored -> enforced fan-out, principles 5/6/10, roster corrections).
3. Tour stop 2 - G1.1 spec/schema linting (`specified`; strictness already
   ratified). Confirm and move.
4. Tour stop 3 - G1.2 model checking (`registered`) - the Q8 stop: ratify /
   amend / defer the drafted hard-core designation criteria. If ratified:
   ADR 0007, G1.2 -> `specified`, registry + index cascade.
5. Tour stop 4 - G1.3 review checklist (`specified`; 10 items). Walk each;
   amendments possible, not expected.
6. Tour stop 5 - Close-out: completeness check (G2.5 export), operators
   (Q5), decisions; housekeeping ruling on the page's stale "session 4"
   references (recommend gate-anchored phrasing: "the G2+G3 session").
7. Session end: STATE.md regen, commit (Theory trailer), push on explicit
   approval.

## Schedule (shifted one more right by this session; was sessions 5-10)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 6 | G2 + G3 | 8 | Q3 first analyzers; Q8 ADR if still open after session 5 |
| 7 | G4 solo | 9 | Q1 immutability mechanism ADR; REQ-ID format; ratchet shape |
| 8 | G5 + G6 | 8 | Q4 mutation-floor procedure; trace-conformance criteria |
| 9 | G7 + G8 | 7 | benchmark-budget + SLO procedure shapes |
| 10 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 11 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |
