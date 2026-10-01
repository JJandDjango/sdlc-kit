# Plan - Session 71 (2026-10-01) - feature-document f4

**Deliverable:** unit `f4-intake` of `feature-document` on one PR, with
a Two-Key PASS:

- `skills/sdlc/flows/intake.md`: on a feature document, intake derives
  from the newest revision both seats signed. It refuses ready while a
  check stands in no unit or in two, or a unit delivers no check, and
  names the id with `Check {id} is assigned to no unit.`, `Check {id} is
  assigned to units {a} and {b}.` or `Unit {id} delivers no check.`
  (SC4.1). It parks the document while an OPEN mark stands above the
  seat boundary or in Decisions and open questions, or a ready check has
  a gap (SC4.2). Every refusal writes one `r{n}: Parked: {what stands}`
  row and no contract.
- On ready, intake copies each unit's `done_means` word for word from
  its row under Units, pairs two checks in one sketch entry when a unit
  holds more than three, and writes a `Ready:` row that names both seats
  and the revision each signed. The roster stop, the title line into
  `title`, the unit confirmation and the `blocked` dependency held at
  draft all stay (SC4.3).
- `taskcontract/tree.py`: a `Parked:` row changes no text. It never ages
  a stamp or the drift mark, never moves the newest revision, and is
  never the row a `Signed:` row signs (SC4.2). Otherwise the tree prints
  byte for byte what 0.17.0 prints (Constraints 6).
- Retired: I4 and I5 reading the Implementation section;
  `test_i4_and_i5_take_the_answers_from_an_implementation_section`;
  `_NOT_TEXT`'s "none of the three words" (docstring and tuple). The
  tests that pin them are found by test-retirer.
- `intake.md` passes `python -m prompt_lang` and stays under 12,000
  characters (Constraints 1).
- One manual receipt for SC4.1: a live intake on f3's document
  (`RECEIPT_feature-document-f3_2026-10-01/hello-name.md`) with one check
  left out of Units writes the `Parked:` row and no contract.

Approvals split as in sessions 61 to 64 and 68 to 70: Claude approves
the test list and the commit on review; the plan, any ruling, the USAGE
text, the receipt's shape, the push, the PR and the merge stay on the
user's word.

**Closed.** The deliverable is met: f4 at `b654e6d` (the flow, the tree
and the tests), `40c16ce` and `e5680cd` (USAGE), Two-Key PASS at round 1
with six advisories, carried in `STATE.md`. Suite 915 passed, scope-check
green, `prompt_lang` green on `intake.md` (9,989 characters); the unit
closed.

## Steps

1. ~~Open.~~ Branch cut from `795c175`; the plan at `4221674`.
2. ~~f4, draft.~~ Two drafter runs side by side. The tree: 8 tests (14
   cases) in `tests/test_tree_parked.py`, red 14 of 14, the prototype
   green on one changed line, seven mutations caught. The flow: 21 tests
   in `tests/test_intake_refusals.py`, red 21 of 21, the prototype green.
   The user then ruled on three points, and a narrow amendment round took
   the flow list to 25 tests, red 25 of 25, twelve mutations caught.
3. ~~f4, retire.~~ The overlaid suite in a worktree: two failures. The
   retirer retired
   `test_i4_and_i5_take_the_answers_from_an_implementation_section` and
   amended one assertion of `tests/test_tree_stale.py`, which counted the
   word `Ready:` in the flow.
4. ~~f4, approve the list and prove red.~~ The worktree suite passed
   915; approved by Claude; SC4.1, SC4.2 and SC4.3 red (6, 24 and 9
   failing).
5. ~~f4, green.~~ Two developers side by side, no deviation; the flow
   came out identical to the reviewed prototype. The session's suite
   read 915.
6. ~~f4, commit.~~ At `b654e6d`; each check green at the clean commit;
   scope-check green.
7. ~~f4, the receipt.~~ Two headless, hidden intake runs at `b654e6d`,
   one turn each. Run A parked on the two OPEN marks (`r8`). After the
   hand edit (rows r9 and r10), run B parked with `Check SC2.2 is
   assigned to no unit.` (`r11`). No contract either time. Kept in
   `RECEIPT_feature-document-f4_2026-10-01/`.
8. ~~f4, Two-Key.~~ One USAGE sentence first, on the user's approval: a
   `Parked:` row is no text row (`e5680cd`), under its own red
   subsection because a standing test keeps section 9's green
   subsections free of red marks. PASS at round 1 on the three commits,
   nine receipts, six advisories; the unit closed.
9. ~~Close.~~ `STATE.md` regenerated; this plan struck; the three
   scratch worktrees removed. The push, the PR and the merge wait on the
   user's word.

Steps 1 and 9 sit outside a contract unit, so the tree does not show
them.

Decisions this session: eleven, the eleventh the user's at the close:
the re-intake for `skills/sdlc/SKILL.md` opens session 72. The other
ten. The user's: (1) this plan, with the
receipt's shape; (2) park before stop; (3) a copied `done_means` is
never reworded at intake; (4) USAGE's plan-answers paragraph; (5)
USAGE's `Parked:` sentence; (6) its place, a red subsection. Claude's,
on review: (7) the test list, (8) the commit. The user's at the close:
(9) the push and the PR, (10) the merge. Readings Claude settled with
the test list and told the user: one `Parked:` row names every thing
that stands; a pair of checks in one sketch entry reads `(SC2.2,
SC2.3)`, as the tree parses it; a ready-check gap intake finds goes in
the row as `Ready check {n}: {gap}. Marked OPEN.`, and intake writes no
inline mark.

Deferred, not this session:
- `f5-release` (ships 0.18.0), with its sweep list in `STATE.md` Next
  actions 1, f4's six advisories among them.
- `skills/sdlc/SKILL.md` says intake writes only the contract, outside
  this contract's Scope: a re-intake that adds it to Scope opens session
  72 (user, 2026-10-01), in `STATE.md` Next actions 1.
- `lang-check --draft` runs neither VT002 nor VT006 on a draft term:
  left to intake, an open question in `STATE.md`.
- G1's solution half by hand (risk 5), after 0.18.0.
- `test-retirer.js` waits on the whole suite inside its agent; the fix
  stays parked, and step 3 worked around it.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; never two whole suites at
once; no spawn opens a window; a surprise mid-build is an OPEN and a
re-intake, never a silent edit.
