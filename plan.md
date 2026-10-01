# Plan - Session 70 (2026-10-01) - feature-document f3

**Deliverable:** unit `f3-signing` of `feature-document` on one PR, with
a Two-Key PASS:

- `taskcontract/lang.py`, `taskcontract/__main__.py`: `lang-check --draft
  <state file>` reads the interview's state file, never the document, and
  writes nothing. It adds the new terms as drafts, reports `CL014` for a
  new term that matches a ratified one, runs the dictionary's health and
  the contract rules on a draft contract, and ends on its count line.
  Without `--draft`, `lang-check` prints byte for byte what 0.17.0 prints
  (Constraints 6). Check SC2.1, the command's side.
- `skills/product-specification-interview/`: before the PO seat signs,
  the interview runs the command, reads each entry of Existing behavior
  touched against its source, records the run as a `Measured:` row, and
  reads ready checks 1 to 8. Before the engineer seat signs, it runs the
  command on each `done_means`, checks Scope against the release unit's
  paths, and reads ready checks 11 to 14. Each gap gets `Ready check {n}:
  {gap}. Marked OPEN.`, a derived block stamped below the newest revision
  gets the stale message, and the seat's word to sign stands at any count
  (SC2.1, SC2.2+SC2.3).
- A signature lands as `rN: Signed: request half` or `rN: Signed:
  solution half`, right after the row it signs, and the tree shows the
  document as a feature before intake with each signed half (SC1.3).
- Retired: `flows/readiness.md` and its five rules;
  `test_readiness_advises_and_never_blocks`; f2's file-set test flips.
  The tests that pin them are found by test-retirer.
- The advisories f3 owns get settled (`STATE.md` Next actions 1): the
  Gherkin stamp, the two meanings of `thin`, a request half changed
  after its signature, Out of scope with no engineer seat, and the three
  wording lines (`request.md:11`, `solution.md:12`, `readiness.md:25`).
- Every prompt file f3 touches passes `python -m prompt_lang` and stays
  under 12,000 characters (Constraints 1).
- One manual receipt for SC1.3: a live run on a small feature in a
  scratch worktree, both halves signed, `taskcontract tree` showing both
  halves done.

`USAGE.md` already holds f3's text ("The checks before signing", "The
signatures"), approved in session 68; its marks stay red until f5. Any
change to that text comes to the user in chat first.

Approvals split as in sessions 61 to 64, 68 and 69: Claude approves the
test list and the commit on review; the plan, the rulings, the USAGE
text, the push, the PR and the merge stay on the user's word.

**Closed.** The deliverable is met: f3 at `9fd60ad` and `dddef83`
(USAGE) and `5ddd858` (the command, the skill and the tests), Two-Key
PASS at round 1 with five advisories, carried in `STATE.md`. Suite 877
passed, scope-check green, `prompt_lang` green on the four touched
prompt files; the unit closed.

## Steps

1. ~~Open.~~ Branch cut from `8cd3d27`; the plan at `19e4c40`.
2. ~~f3, the rulings.~~ The user ruled all three as recommended. USAGE's
   three paragraphs at `9fd60ad`, approved in chat.
3. ~~f3, draft.~~ Two drafter runs side by side. The command: 27 tests
   (45 cases) in `tests/test_lang_draft.py`, red 45 of 45, the prototype
   green with thirteen mutations caught. The flows: 37 tests (38 cases)
   in `tests/test_interview_signing.py`, red 38 of 38, the prototype
   green with eighteen mutations caught.
4. ~~f3, retire.~~ The overlaid suite in a worktree: eight failures in
   two modules. The retirer retired
   `test_readiness_advises_and_never_blocks` and amended seven.
5. ~~f3, approve the list and prove red.~~ The worktree suite passed
   877; approved by Claude; SC1.3, SC2.1 and SC2.2+SC2.3 red (15, 53 and
   15 failing).
6. ~~f3, green.~~ Two developers side by side, no deviation; the
   session's suite read 877. Round 2 was Claude's to ask for, on
   `flows/signing.md`: which row is the release unit, the path back into
   a request-half section from E6, and the `CL000` line copied without
   its locator. Plain `lang-check` proved byte for byte on three roots.
7. ~~f3, commit.~~ At `5ddd858`; each check green at the clean commit;
   scope-check green.
8. ~~f3, the live run.~~ The approved shape changed in how it ran: the
   second session ran headless, turn by turn, and an agent answered as
   the two seats from a script (about 100 turns would not fit a pane
   read from this session). Two false starts: a session may not write in
   its own plugin's folder, and the driver opened a window per turn
   until it started the session hidden. 99 turns, both halves signed,
   the tree showing both `done`. Kept in
   `RECEIPT_feature-document-f3_2026-10-01/`.
9. ~~f3, Two-Key.~~ One USAGE sentence first, on the user's approval:
   the `Measured:` row lands once the ready checks are read (`dddef83`).
   PASS at round 1 on the three commits, thirteen receipts, five
   advisories; the unit closed.
10. ~~Close.~~ `STATE.md` regenerated; this plan struck; the three
    scratch worktrees removed; pushed and merged through PR #82, each on
    the user's word.

Steps 1 and 10 sit outside a contract unit, so the tree does not show
them.

Decisions this session: eleven. The user's: (1) this plan, (2) to (4)
the three rulings, (5) the USAGE text they change, (6) the live run's
shape, (7) the `Measured:` row's sentence in USAGE. Claude's, on review:
(8) the test list, (9) the commit. The user's at the close: (10) the
push and the PR, (11) the merge. Readings Claude settled with the test
list and told the user: no `VT` line from the command (now an open
question in `STATE.md`), and a seat that declines to sign pauses the
run before the solution half opens.

Deferred, not this session:
- `f4-intake`, `f5-release` (ships 0.18.0).
- `solution.md:49`'s "intake copies the done means word for word", made
  true by f4.
- The "then eighteen sections" wording at `SKILL.md:45` and
  `USAGE.md:139`, and "accepts, edits or drops" against the flow's
  "accept, change or drop": f5's sweep.
- G1's solution half by hand (risk 5), after 0.18.0.
- `test-retirer.js` waits on the whole suite inside its agent; the fix
  stays parked, and step 4 works around it.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; never two whole suites at
once; a surprise mid-build is an OPEN and a re-intake, never a silent
edit.
