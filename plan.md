# Plan - Session 3 (2026-07-23)

Program ratified: iterate the gates G0 -> G10 -> PL-DOC -> PL-PIPE, one deep page
per gate (ADR 0004 template), depth = document + specify only, roster policy =
normative with user ratification, light gates batched. Full plan:
`~/.claude/plans/the-top-priorities-for-shimmering-frost.md`.

## This session

1. ADR 0004 - the program rules (page location, template, order, depth, roster
   policy, lifecycle-advance rule).
2. Substrate pages: `docs/taxonomy.md` (bug classes + detectability ladder),
   `docs/catalog.md` (8 spec-first patterns); MAP.md deep-doc links filled.
3. `docs/gates/G0-planning-intake.md` - exemplar page; task-contract field set
   drafted inline (Q2).
4. `docs/gates/G1-requirements-spec.md` - G1.1-G1.3 documented; review checklist
   drafted inline.
5. Ratification checkpoint: field set (-> ADR 0005), G1.1 strictness, G1.3
   checklist, proposed G2.5. Then registry lifecycle/count updates.
6. Spine touches: gates.md per-gate links + catalog/taxonomy pointers,
   CONVENTIONS.md gate-page rule; cairn audit clean.
7. Session end (user-triggered): STATE.md regen, commit (Theory trailer),
   approved push; then apply `.github/ruleset-protect-main.json` - PR flow from
   session 4 onward.

## Schedule (sessions 4-9)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 4 | G2 + G3 | 7 (+G2.5 if ratified) | Q3 first analyzers; Q8 hard-core criteria ADR |
| 5 | G4 solo | 9 | Q1 immutability mechanism ADR; REQ-ID format; ratchet shape |
| 6 | G5 + G6 | 8 | Q4 mutation-floor procedure; trace-conformance criteria |
| 7 | G7 + G8 | 7 | benchmark-budget + SLO procedure shapes |
| 8 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 9 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |
