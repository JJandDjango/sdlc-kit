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

**Closed.** The deliverable is met: f2 at `df00510` (USAGE) and
`432da9c` (skill and tests), Two-Key PASS at round 1 with seven
advisories, carried in `STATE.md`. Suite 795 passed, scope-check green,
`prompt_lang` green on all six prompt files; the unit closed.

## Steps

1. ~~Open.~~ Branch cut from `310991d`; the plan at `282ace4`.
2. ~~f2, the two advisories.~~ The user ruled both as recommended: a
   derived block not yet written carries no stamp, and a section not yet
   asked reads "(not yet asked)". USAGE's text at `df00510`, approved in
   chat.
3. ~~f2, draft.~~ 32 tests in `tests/test_interview_sections.py`, red 32
   of 32; the prototype passed 32 and `prompt_lang`, and caught twelve
   mutations.
4. ~~f2, retire.~~ The session ran the overlaid suite in a worktree: four
   failures in `tests/test_skill_interview.py`. The retirer retired
   three with `FLOW_FILES` and `SECTION_STEPS` and amended one.
5. ~~f2, approve the list and prove red.~~ The worktree suite passed
   795; approved by Claude; SC1.2, SC3.1 and SC3.2+SC3.3 red (21, 4 and
   4 failing).
6. ~~f2, green.~~ Two rounds, no deviation. Round 2 was Claude's to ask
   for: S6 gained each unit's tests and retirements (ADR 0033). The
   session's first suite run was stopped while the developer's ran;
   its second read 795.
7. ~~f2, commit and Two-Key.~~ At `432da9c`; each check green at the
   clean commit; PASS at round 1; the unit closed.
8. ~~Close.~~ `STATE.md` regenerated; this plan struck; the push and the
   PR on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: eight. The user's: (1) this plan, (2) and (3)
the two placeholder readings, (4) the USAGE text they change. Claude's,
on review: (5) the test list, (6) the commit. The user's at the close:
(7) the push and the PR, (8) the merge.

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
