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
1. ~~adr-0025~~ - 266387c.
2. ~~g0-usage-section~~ - 792aa79 (Pass 0, red markers).
3. ~~g0-skill-flows~~ - e19bc7d (flows split; description trimmed on
   the user's word; SKILL.md 3978 -> 1852 tokens).
4. ~~schema-1-3-0~~ - 10c1218 (additive; version pin moved).
5. ~~tc016-door~~ - e6d0202 (8 tests; suite 222).
6. ~~g0-seat-term~~ - 04f986a (term ratified; 66 units stamped;
   registry row kept on the user's word; pins moved 6 -> 7).
7. ~~g0-3-row~~ - 95632b5 (G0 count 1 -> 3, total 54 -> 56 corrected).
8. ~~g0-confirm-write~~ - c2f81da (I5-I6; closes unit-dag).
9. ~~g0-docs-and-tests~~ - 97a060b (markers green; kit 0.12.0).
10. Push, open the PR with the human answers in its body (the class-E
    roster delta, the ratification flip, the trimmed description, the
    registry row), merge on green.
11. After merge: tag `v0.12.0` at the merge commit, then the self-pin
    PR (workflow pin, USAGE uv line -> v0.12.0), the contracts check
    proving the tag installs, per the v0.11.0 precedent.
12. Session close: STATE.md regenerated from receipts on main.

Steps 2, 3, 4, 7 are parallel after 1; 8 waits on 3 and 5; 9 waits on
all. Branch `session-27-intake-seats`; the contract + term + notes +
this plan commit first; one commit per unit after.

House rules in force: no pipes/chains in any authored command string;
commit messages via Write + git commit -F; Two-Key on every code unit.
