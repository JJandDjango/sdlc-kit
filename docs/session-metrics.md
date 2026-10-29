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
| 97 + 98 | `g1-requirements-spec/s5-start` | yes, in session 98 | 2 | 1 / 0 | | 0 | 1,157: drafters 187 + 156, developers 96 + 65, Two-Key 239 + 203 + 211 | 2 / 0 | |
| 101 + 102 | `g1-requirements-spec/s1-lint`, the G1.1 record fix | yes, in session 102 | 1 | 0 / 0 | | 0 | 631: drafter 353, developer 93, Two-Key 185 | 2 / | 1 / 4 |
| 103 + 104 | `g1-requirements-spec/s6-release` | yes, in session 104 | 2 | 0 / 1 | | 0 | 730: drafter 299, Two-Key 220 + 211 | 2 / | 1 / 0 |
| 112 + 113 | `small-session-flow/w1-session-size` | yes, in session 113 | 1 | 0 / 0 | | 2 | 295: drafter 129, developer 70, Two-Key 96 | 2 / | 1 / 1 |
| 114 | `small-session-flow/w4-session-notes` | yes | 1 | 0 / 0 | | 0 | 93: Two-Key 93 | 2 / | 0 / 0 |
| 115 | `small-session-flow/w2-workflow-file` | yes | 1 | 0 / 0 | | 0 | 270: drafter 106, developer 70, Two-Key 94 | 2 / | 1 / 0 |
| 116 | `small-session-flow/w3-node-start` | yes | 1 | 0 / 0 | | 0 | 297: drafter 126, developer 70, Two-Key 101 | 2 / | 2 / 1 |
| 124 | `execution-team/e1-declaration` | yes | 3 | 0 / 2 | | 0 | 507: drafter 131, developer 75, Two-Key 301 (95, 108, 98) | 2 / | 0 / 0 |
| 125 | `execution-team/e2-scripts` | yes | 1 | 0 / 0 | | 0 | 499: drafter 152, retirer 103, developer 98, Two-Key 146 | 2 / | 1 / 0 |
| 126 | `execution-team/e3-wall` | yes | 1 | 0 / 0 | | 0 | 493: probe 117 (Haiku, two runs), drafter 195, developer 78, Two-Key 103 | 2 / | 1 / 0 |
| 127 + 128 | `execution-team/e4-team` | yes, in session 128 | 1 | 0 / 0 | 2 | 0 | 805: probe 205 (Haiku), drafter 280, developer 184 (127, fix 57), Two-Key 136 | 2 / | 1 / 0 |
| 129 | `execution-team/e5-rounds`, built by the shipped team | yes | 4 | 3 / 0 | | 1 | 1,846: QA 396 (three rounds), QA verifier 597 (approve-tests 412, prove-red 38, two-key 68 killed + 85 + 101), Developer 311 (four runs, one killed), Dev verifier 435 (four rounds) | 7 readings / | 2 / 1 |
| 131 | `execution-team/e6-batch-run`, the release, its receipt run by the shipped team | yes | 3 | 0 / 6 | | 0 | 755: the receipt's members 267 (run 1 QA 40 killed; run 2 QA 45, QA verifier 107 over three tasks, Developer 35, Dev verifier 40), the kit's Dev verifier 488 (141, 170, 177) | 6 readings / | 2 / 1 |
| 133 | `execution-team` fixes: e3-wall, e5-rounds with e4-team, the 0.21.1 release pages | yes | e3 2, e5 1, e6 2 | 0 / 2 | | 0 | 1,031: probe 41 (Haiku), QA 313 (118, 195), Developer 138 (66, 72; one run stopped before any edit), Dev verifier 539 (e3 90 + 84, e5 118, e6 128 + 119) | 11 readings / | 1 / 1 |

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
- Sessions 97 and 98 are one build and one row, the first split at the
  test list on the user's ruling of 2026-10-12. Round 1's defect sat in
  the prompt half's behavior, counted as code: I9 ran a fifth kit
  command against the design's constraint 11, on a reading Claude
  approved in the test list. Two-Key caught it before the merge, so it
  did not escape. Round 2's receipts ran twice: the Haiku receipts agent
  returned with two commands still running, and the receipts were taken
  again on Opus (211K of the Two-Key total). The 12 readings in PR
  #119's body were merged with none overturned. The user's `/usage`
  readings at each session's start and end were no touch, and the
  deferred lines were not counted.
- Sessions 101 and 102 are one build and one row, split at the test list
  as session 96 ruled; the fix reopened a done unit. The drafter took
  353K tokens against a plan of 200K, which came from `d4`'s smaller
  list. Round 1 passed with five advisories and no blocking defect: two
  pages stale until the later commits, the `lint` guard on a contract
  that is not UTF-8 or holds an impossible date has no test, and the
  commit message counted four tree tests where the diff edits the helper
  and two bodies. The Haiku receipts agent's first three-file call hit
  its 120 s limit and ran again in the foreground (155 s); no round was
  taken again. Eighteen older tests that pinned the flat record were
  amended and tried on the prototype first. No `/usage` readings were
  taken, on the user's ruling of 2026-10-17. The deferred count is one
  line added (the untested guard) and four closed (two edges, one
  refusal line, one docstring wrap).
- Sessions 103 and 104 are one build and one row, split at the test list.
  The drafter took 299K tokens against a plan of 200K, and no developer
  ran: the unit changes no code. Round 1 failed on one USAGE sentence the
  release left false (the kit computes no condition at any gate after G0,
  with G1 computed), found by the sweep; the fix was that sentence and one
  test, and a second round (211K of the 431K for both). Two of round 1's
  three reasons were Claude's: two `g1-check` receipts that exit 1 and 2 by
  design counted as failed receipts, so round 2 dropped them. Round 2
  passed with five advisories. The receipts ran in three parts, since the
  whole suite takes 607 s against the 600 s foreground cap; the Haiku
  receipts agent's results matched the session's own in both rounds. No
  `/usage` readings were taken. The deferred count is one line added (the
  sweep's advisories) and none closed.
- Sessions 112 and 113 are one build and one row, split at the test list
  (231K of context), and the first build on `prove.py` and `receipts.py`.
  The drafter took 129K tokens and 32 calls against `s6-release`'s 299K
  and 124. `receipts.py` ran the whole suite once in the background (2017
  passed, 453 s) with no agent, so Two-Key was its grader alone. Round 1
  passed with five advisories. The two touches: the user's G1.3
  signature, a review the plan missed, and part two's go-ahead at the
  resume. The live receipt's headless session (Sonnet 5.5, 367K of
  context) stands outside the total. The deferred count is one line added
  (the round's advisories) and one closed (the Haiku receipts agent's
  question).
- Session 114 built the first unit with no automated test, so no drafter
  or developer ran. Its two checks are manual receipts, each a script
  whose exit reads `status.py`'s output, recorded through `progress run`;
  `write-tests` and `prove-red` stay unrecorded. Round 1 passed with
  three advisories: the wrap fixed one (a list indent), the PR's opening
  makes another true, and the design's own SC4.2 receipt, at w2's
  session start, is backlog Next 10's opener. The SC4.2 headless session
  (Haiku 5.5, 102K tokens over two turns) stands outside the total, as
  w1's live receipt did.
- Session 115 built a unit with code in one session, from one command of
  the user's, with no split at the test list. The drafter took 106K
  tokens and 19 calls (w1's 129K and 32), the developer 70K and 12 calls,
  and `receipts.py` ran the whole suite once (2050 passed, 429 s). Round 1
  passed with four advisories: one goes to Next 11 (w3 rules the line for
  a missing workflow file), the other three are the one deferred line
  added.
- Session 116 built the feature's last unit in one session, with no
  split at the test list. The drafter took 126K tokens and 29 calls, the
  developer 70K and 14. Two-Key's grader was the first agent to run at a
  row's values (the execution row's `sonnet` and `high`, passed into the
  changed script): 101K tokens, 27 calls, 75 s. The whole suite ran
  three times at about 465 s each: on the prototype, then `receipts.py`
  before the unit commit (a sequencing slip, run again at the commit).
  Round 1 passed with three advisories: `USAGE.md` and
  `docs/components.md` never describe `node` (Next 12, with an unguarded
  `Popen` for the design's next text row), and the Ctrl+C note follows
  the plan's reading. Next 11 closed; Next 12 and 13 are the two lines
  added.
- Session 124 built execution-team's first unit in one session, its
  context peaking at 303K (over the 200K target). The drafter took 131K
  tokens and 36 calls, the developer 75K and 27. Both failed Two-Key
  rounds were one wording defect on one sentence: `task.py`'s docstring
  listed its outside dependencies "only". Claude's hand fix of round 1
  named PyYAML and missed jsonschema, which reaches the script through
  `g1`; round 2's grader proved it by blocking the package. The second
  fix dropped the list and swept every line that stated a later unit's
  work as present. The lesson: a fix to a factual claim is checked
  against the code, as the claim was. The prototype's whole-suite run
  found `test_g1_release.py` pinning 0.20.0's state (no red mark
  anywhere in USAGE), which refused the page the design writes red in
  e1. The count now leaves out that page, a reading from both documents'
  purpose. It is not charged as an escaped defect, since it held when it
  shipped. The deferred list added and closed nothing: its four lines
  sit in later units.
- Sessions 127 and 128 are one build and one row, split at the test list
  (session 127 passed its 200K target). The drafter took 280K tokens and
  89 calls against a plan of 150K to 250K. The manual receipt, the first
  run of `/sdlc execute` in a consumer, found a defect before Two-Key:
  the Developer ran its test file alone, a path behind its own wall, so
  the hook refused it. The fix was a test amendment and a 57K developer
  round; it is not counted, since no Two-Key round failed on it. Round 1
  passed with three advisories; the wrap fixed two wording ones. The
  receipt's three headless Haiku runs (6,501K, of which 5,859K cache
  reads, against a plan of 300K to 400K) stand outside the total, as
  w1's did. The deferred count is one line added (Next actions 12, the
  wall at a task's end, for e5) and none closed. Its Escaped cell reads 1
  since session 129: the wall refuses the Developer's run of a declared
  command that names a walled folder (Next actions 13).
- Session 129 is the first unit the shipped team built, on e4's
  one-round flow, so the session resumed a headless Sonnet Orchestrator
  for each round. Rounds counts the two-key task's four runs: the Dev
  verifier failed rounds 1 and 2 (the round shown after a failed round,
  then the reasons' detail), and the QA verifier failed round 3 on three
  uncaught mutations. The QA channel took four rounds, the fourth on the
  user's waiver of the cap, which is the one touch. The 7 readings are
  the PR body's items 2 to 7 and 9. Agents took 1,846K against a plan
  of about 1M; the headless Orchestrator read 31.0M from cache (347K
  output) against a plan of 3M to 6M, since each resume re-reads its
  whole context. The deferred count is two lines added (Next actions
  13 and 14) and one closed (12).
