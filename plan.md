# Plan - Session 69 (2026-09-30) - feature-document f2

**Deliverable:** unit `f2-sections` of `feature-document` on one PR, with
a Two-Key PASS:

- `skills/product-specification-interview/`: the interview asks each
  section in the ratified order, one question at a time, writes its
  state file after each step, and a later run goes on at the step `next`
  names. It asks `a thing we will not build, or a place we will not
  touch?` at Non-goals and Out of scope, gives the six-criteria prompt
  past five, reads the seat's content back per section, and covers each
  answer that differs. Check SC1.2.
- Once the checks stand, the interview derives one scenario per check,
  joined by the check's id; the PO seat accepts, changes or drops each
  (SC3.1). A scenario whose Then needs a fact its check lacks is never
  shown and makes a thin check; ready check 3 reads a thin check as an
  OPEN; a check with no accepted scenario gets an OPEN at the Request
  half's signature; a dropped scenario makes a thin check (SC3.2+SC3.3).
- Retired: `flows/sections.md` (Q1 to Q12), replaced by one flow per
  half; the tests that pin it, found by test-retirer (seen: `FLOW_FILES`,
  `SECTION_STEPS`, `test_skill_file_set_is_exactly_the_ratified_set`).
- f1's two Two-Key advisories that f2 owns get settled: what a Gherkin
  block not yet derived reads in place of `r{n}`, and what a section not
  yet asked reads in place of "(none)". O4's pointer to `sections.md` Q9
  moves to the new solution-half flow.
- Every prompt file f2 touches passes `python -m prompt_lang` and stays
  under 12,000 characters (Constraints 1).

`USAGE.md` already holds f2's text ("The run", "The Gherkin step", the
thin check), approved in session 68; its marks stay red until f5. Any
change to that text comes to the user in chat first.

Approvals split as in sessions 61 to 64 and 68: Claude approves the test
list and the commit on review; the push, the PR and the merge stay on
the user's word.

## Steps

1. Open. Cut `session-69-feature-document-f2` from `310991d`; commit
   this plan on its own.
2. f2, the two advisories. Claude shows the two placeholder readings in
   chat, with a recommendation each, checked against USAGE's approved
   text; the user rules.
3. f2, draft. `spec-channel-drafter.js` drafts the test list for SC1.2,
   SC3.1 and SC3.2+SC3.3, proves it red, and proves it satisfiable on a
   scratch copy of the skill folder.
4. f2, retire. `test-retirer.js` with `overlay`; the session runs the
   overlaid suite itself and classifies from its output.
5. f2, approve the list and prove red. The whole suite on the prototype
   in a scratch worktree; each fixed detail checked against the
   contract, the feature document and Constraints; session labels
   stripped; then `progress run <check> --expect red`.
6. f2, green. `unit-developer.js` from the interface note; Claude runs
   the suite after each round and tests any deviation against
   `done_means`.
7. f2, commit and Two-Key. Each check green at the clean commit;
   `two-key-unit-verifier.js`; `progress done` on PASS.
8. Close. `STATE.md` regenerated; this plan struck; the push and the PR
   on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: seven. The user's: (1) this plan, (2) and (3)
the two placeholder readings. Claude's, on review: (4) the test list,
(5) the commit. The user's at the close: (6) the push and the PR, (7)
the merge.

Deferred, not this session:
- `f3-signing`, `f4-intake`, `f5-release` (ships 0.18.0).
- `flows/readiness.md`'s five rules and its line 25, f3's.
- The "then eighteen sections" wording at `SKILL.md:44` and
  `USAGE.md:139`, f5's sweep.
- G1's solution half by hand (risk 5), after 0.18.0.
- `test-retirer.js` waits on the whole suite inside its agent; the fix
  stays parked, and step 4 works around it.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an
OPEN and a re-intake, never a silent edit.
