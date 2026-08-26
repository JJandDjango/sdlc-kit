# Plan - Session 27 (2026-08-25) - Phase 0 to completeness (intake seats)

The plan is the task contract `specs/intake-seats/contract.yaml`
(ready-green at schema 1.2.0); the graph is `python -m taskcontract
graph specs/intake-seats/contract.yaml`, computed, never committed.
Companions: draft term `specs/vocabulary/intake-seat.yaml`, notes
`NOTES_phase0_2026-08-25.md`.

What lands: a per-unit `confirmed_by` field, a ratified seat term the
ready door joins against (TC016), the intake venue writing the answers
(closing unit-dag's open `g0-intake-review` on the same edit), the
skill flows restructured so the venue has room to grow, and a USAGE
section for a consumer with more than one seat.

## Steps (topological order of the unit graph)

0. ~~Ratify~~ - 2026-08-26: all 9 units kept; skill flows split into
   reference files; seat map as tabled in the notes; REQ-002 rounds
   half up on the third decimal (1.25 at 50 returns 0.63). The
   `intake-seat` term stays draft until step 6.
1. adr-0025 - rulings recorded.
2. g0-usage-section - USAGE Pass 0 with red markers (docs first).
3. g0-skill-flows - SKILL.md passes prompt_lang with I5 present.
4. schema-1-3-0 - optional `confirmed_by` on units; 1.2.0 stays green.
5. tc016-door - ready profile joins `confirmed_by` against the term.
6. g0-seat-term - ratify `intake-seat` (your flip); migrate every
   contract, `confirmed_by` lines only.
7. g0-3-row - registry row + deep page; PR records the class-E answer.
8. g0-confirm-write - intake renders, asks, writes `confirmed_by`.
9. g0-docs-and-tests - task-contract page, CHANGELOG 0.12.0,
   CONVENTIONS line, markers flip green, suite covers the door; then
   bump, tag, self-pin per the v0.11.0 precedent.

Steps 2, 3, 4, 7 are parallel after 1; 8 waits on 3 and 5; 9 waits on
all. Branch `session-27-intake-seats`; the contract + term + notes +
this plan commit first; one commit per unit after.

House rules in force: no pipes/chains in any authored command string;
commit messages via Write + git commit -F; Two-Key on every code unit.
