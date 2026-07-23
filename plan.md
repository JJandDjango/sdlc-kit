# Plan - Session 4 (2026-07-23)

User directive: pull G0's enforcement pass forward. Walk G0 thoroughly and
survey what exists / could be built to enforce it - task-contract schema
encoding, validator tooling, harness intake wiring. Spec baseline:
`docs/gates/G0-planning-intake.md` + ADR 0005. The ADR-0004 program sequence
(G2 + G3) resumes session 5; the schedule shifts one right (table below), and
session numbers cited inside earlier pages ("session 5" for G4, "session 6"
for native-interop) now read +1.

## This session

1. Walk-through: decompose G0.1 into mechanical clauses; map each to JSON
   Schema expressibility; isolate what stays human (unit quality -> G1.3).
2. Survey: in-house enforcement patterns (foundations validator contract,
   cairn audit scripts, orchestrator harness surfaces) and off-the-shelf
   tooling (python-jsonschema 4.26.0 installed, check-jsonschema, ajv-cli).
3. Author `docs/task-contract.md` (component deep page): encoding decisions
   E1-E5, parameters P1-P2, recommended validator + wiring shape, strikeable
   feature list F1-F12. Status PROPOSED.
4. Cross-links: MAP component row -> deep page; G0 page open-items pointer;
   cairn audit clean.
5. **Ratification checkpoint (user):** strike/keep E1-E5, P1-P2 defaults,
   F1-F12 -> ADR 0006 records the kept set.
6. Implement the kept set (post-ratification): `schemas/`, `taskcontract`
   package, fixtures + tests, CI. G0.1 stays `specified` until the intake
   venue is live; the registry Check column gains the near-final shape.
7. Session end: STATE.md regen, commit (Theory trailer), approved push.

## Schedule (shifted one right by this directive; was sessions 4-9)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 5 | G2 + G3 | 8 | Q3 first analyzers; Q8 hard-core criteria ADR |
| 6 | G4 solo | 9 | Q1 immutability mechanism ADR; REQ-ID format; ratchet shape |
| 7 | G5 + G6 | 8 | Q4 mutation-floor procedure; trace-conformance criteria |
| 8 | G7 + G8 | 7 | benchmark-budget + SLO procedure shapes |
| 9 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 10 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |
