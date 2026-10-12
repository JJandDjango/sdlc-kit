# Session metrics

> One row a build session, appended at the wrap. Started 2026-10-08
> (session 89), when the user delegated to Claude the approvals between
> plan approval and the work PR's review. A first look comes after five
> build rows past the marker, the full review after ten.

The record answers one question: do the gates and the delegation give
more consistent, less buggy, streamlined work? Five to ten rows can show
a broken delegation. They cannot prove that quality improved.

## Measures

1. **Delivered**: the session shipped its named deliverable.
2. **Rounds**: Two-Key rounds to PASS.
3. **Defects**: defects that failed a Two-Key round, code / wording.
   Advisories are not counted.
4. **Escaped**: defects found after the merge, charged to the session
   that shipped them. The cell changes when one is found.
5. **Touches**: replies Claude needed from the user between plan
   approval and PR review. The target is 0.
6. **Tokens**: agent tokens in thousands, the total and each role.
7. **Delegated**: approvals Claude gave / approvals or readings the user
   overturned at PR review.
8. **Deferred**: lines added to / closed on the deferred list.

A blank cell was never recorded. Wall-clock time is left out: no
reliable source measures it. Only a session that ships a unit gets a row.

## The tripwire

A delegated item returns to the user at once on either event: one
escaped defect traced to an approval Claude gave, or two overturns of
the same kind at PR review.

## Rows

| Session | Unit | Delivered | Rounds | Defects | Escaped | Touches | Tokens (K) | Delegated | Deferred |
|---|---|---|---|---|---|---|---|---|---|
| 78 | `document-split/d1-requirements` | yes | 1 | 0 / 0 | | | 667: drafter 198, retirer 159, developer 95, Two-Key 215 | 2 / | |
| 79 | `document-split/d2-design` | yes | 1 | 0 / 0 | | | 690: drafter 207, retirer 109, developers 114 + 58, Two-Key 202 | 2 / | |
| 80 | `document-split/d3-signing` | yes | 1 | 0 / 0 | | | 629: drafter 179, retirer 91, developers 107 + 60, Two-Key 192 | 2 / | |
| 81 | `document-split/d4-tree` | yes | 1 | 0 / 0 | | | 561: drafter 213, developers 94 + 75, Two-Key 179 | 2 / | |
| 82 | `document-split/d5-intake` | yes | 1 | 0 / 0 | | | 555: drafter 159, retirer 117, developer 78, Two-Key 201 | 2 / | |
| 83 | `document-split/d6-release` | yes | 1 | 0 / 0 | | | 546: drafter 199, developer 66, Two-Key 281 | 2 / | |
| 88 | `g1-requirements-spec/s1-lint` | yes | 2 | 2 / 0 | 4 | | 911: drafter 225, developers 104 + 60 + 69, Two-Key 205 + 247 | 2 / | |
| 89 | marker: the delegation starts (a talk session, no unit) | | | | | | | | |
| 90 | `g1-requirements-spec/s2-model` | yes | 2 | 1 / 1 | 2 | 4 | 965: drafter 212, developers 115 + 76 + 61 + 59, Two-Key 236 + 205 | 2 / 0 | 9 / 1 |
| 92 | `g1-requirements-spec/s3-review` | yes | 1 | 0 / 0 | | 0 | 781: drafters 232 + 129, developers 114 + 80, Two-Key 226 | 2 / 0 | |
| 94 + 95 | `g1-requirements-spec/s4-tree` | yes, in session 95 | 4, no PASS: the user waived round 5 | 5 / 1 | | 2 | 1,642: drafter 256, developers 144 + 71 + 102 + 89 + 61, Two-Key 256 + 207 + 242 + 214 | 2 / 0 | |

## Notes on the baseline

- Sessions 78 to 88 are backfilled from `STATE.md`'s recorded figures
  and from `.sdlc/progress/`. Each unit's two delegated approvals are its
  `approve-tests` and `approve-commit`, both recorded `by: claude`.
- Sessions 84 to 87 shipped no unit (the design, an amendment, the terms
  and intake) and hold no row. Session 84's explorers took 897K tokens
  and its retirer 62K.
- Live-run seat agents (session 80: 66K and 63K) stand outside the
  totals, as in `STATE.md`'s count.
- Two gaps found after 0.19.0's release are not yet charged to a
  session: a design run's opening fixes no shape for its copy of the
  terms, and the interview's `SKILL.md` reads `$1` as the second word.

## Notes on the rows past the marker

- Session 90: the tripwire fired. The escaped defect is session 88's:
  `s1-lint` reads G1.1 `done` for a contract whose YAML cannot be read
  or that holds no `scope`. The developer of `s2-model` found it, Claude
  confirmed it with a live run, and the user counted it on 2026-10-09.
  It traces to the test list Claude approved, so from that day the user
  approves each test list.
- Session 90's four touches: the ruling on the escaped defect, and three
  approvals of added tests (three tests on review of the first developer
  round, then two amendments of one table). Claude approved the
  session's first list, 89 cases, before the event, and that list held
  the rule that lost round 1: when a hard core is in a feature's scope.
- Session 90's lost round cost 325K tokens: developers 61K and 59K, and
  the second grade at 205K. Its defects count 1 / 1: the rule in the
  code, and one USAGE sentence that claimed more than the rule did.
- Session 92: no approval stood before the PR review, on the user's
  ruling of 2026-10-11. The plan took none, and Claude approved both
  test lists. The touches count from that ruling: the session's first
  plan asked four rulings and was declined before it. The 12 readings
  in PR #112's body were each kept at the review, in session 93. The
  three live runs' seat agents took 173K more, outside the total. The
  deferred lines were not counted.
- Sessions 94 and 95 are one build and one row. Session 94 built
  `s4-tree` and stopped after three failed rounds, as its plan ruled;
  session 95 shipped it. The unit holds no Two-Key PASS. Rounds 1 to 3
  each failed on one class, a hand-written text that made G1's reading
  raise and so stopped the whole tree print: five defects in the code
  (a NUL in a schema folder; a date no calendar holds, in a record and
  in the component declaration; a lint record's path as a list; a
  `g1.exempt` entry Python cannot turn into text). Round 4 found no
  defect in the code and failed on one USAGE sentence Claude had
  written: an escape typed into an edit was decoded into its characters.
  That sentence was fixed and not regraded, and the user waived round 5
  on 2026-10-12.
- The two touches of that row: the ruling for a round 4 with one guard
  at the boundary, and the waiver. The four failed rounds cost 919K of
  the 1,642K. Session 94's plan read about 0.6 million. The 15 readings
  in PR #116's body were merged with none overturned, and the deferred
  lines were not counted.
- Escaped defects charged by that build, each a traceback in `g1-check`
  on main for a hand-written text. Session 88 (`s1-lint`) gains three:
  a NUL in a pin or a schema pattern's folder, a date no calendar holds
  in a record, and a lint record's path as a list. Session 90
  (`s2-model`) gains two: a NUL in a model configuration, and that date
  in `specs/components.yaml`. Each test list was Claude's approval. The
  user has not said whether these count for the tripwire; PR #116's
  body named them, and the user merged it.
