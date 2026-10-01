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

## Steps

1. Open. Branch `session-70-feature-document-f3` cut from `8cd3d27`;
   this plan committed once the user has read it.
2. f3, the rulings. Three readings go to the user in one message, each
   with a recommendation: when the Gherkin stamp moves; what a request
   half changed after its signature does to that signature; where Q9's
   places land with no engineer seat. Then any USAGE text they change,
   approved in chat and committed on its own.
3. f3, draft. Two narrow drafter runs: the command (`lang-check --draft`,
   `CL014`), its prototype the `taskcontract` package; then the flows,
   their prototype a scratch copy of the skill folder. Each list proved
   red, each prototype proved green.
4. f3, retire. The session runs the overlaid suite in a scratch
   worktree, then test-retirer reads only the failing tests' module.
5. f3, approve the list and prove red. The worktree suite passes; each
   fixed detail checked against the contract, the feature document and
   its Constraints; `progress run --expect red` per check.
6. f3, green. Two developer rounds at least: the command, then the
   flows. The session runs the suite after each.
7. f3, commit. Each check green at the clean commit.
8. f3, the live run. The receipt for SC1.3, in a scratch worktree at the
   commit. Its shape goes to the user first (recommended: a second
   Claude session in a herdr pane runs the skill from the worktree, and
   this session answers as two toy seats). The document and its state
   file are kept for f4's receipt.
9. f3, Two-Key. The receipt's text rides as a focus pointer; the unit
   closes on PASS.
10. Close. `STATE.md` regenerated; this plan struck; the push and the PR
    on the user's word.

Steps 1 and 10 sit outside a contract unit, so the tree does not show
them.

Session boundary: f3 is the largest unit (code, prompt text and a live
run). If context nears 40% before step 8, the session wraps at step 7's
commit, and session 71 opens on the live run and Two-Key.

Decisions this session: ten. The user's: (1) this plan, (2) to (4) the
three rulings, (5) the USAGE text they change, (6) the live run's shape.
Claude's, on review: (7) the test list, (8) the commit. The user's at
the close: (9) the push and the PR, (10) the merge.

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
