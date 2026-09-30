# Plan - Session 68 (2026-09-30) - feature-document f1

**Deliverable:** unit `f1-format` of `feature-document` on one PR, with a
Two-Key PASS:

- `USAGE.md` gains the new interview section first, every status mark
  red; the old interview text goes.
- `skills/product-specification-interview/`: the interview writes the
  ratified format (ADR 0029, as 0033 to 0036 amend it) at
  `docs/features/<id>.md` from r1, with its state file beside it. The
  title line reads `# <id> - <title>`; each section stands in order, with
  the seat boundary and a tag under its name; revision rows carry
  numbers, and r1 names both seats. The four fix sections stand only in a
  fix's document. The interview writes only the document and its state
  file, never runs intake, still errors on an existing path, and the
  Google Docs form writes nothing. Check SC1.1.
- Retired: the template's ADR 0026 sections; the
  `REQUEST_{slug}_{date}.md` path and its root state file
  (`spec-interview-state/1`); `SKILL.md`'s "never edit an existing
  document"; `output.md`'s render at the end (W1 to W3); and the tests
  that pin them, found by test-retirer (seen: `TEMPLATE_SECTIONS`,
  `test_opening_writes_the_state_file_and_never_overwrites`,
  `test_output_writes_from_the_template_and_names_intake`).
- Every prompt file f1 touches passes `python -m prompt_lang` and stays
  under 12,000 characters (Constraints 1).

Approvals split as in sessions 61 to 64: the user approves the USAGE
section in chat before any drafting; Claude approves the test list and
the commit on review; the push, the PR and the merge stay on the user's
word.

## Steps

1. Open. Branch `session-68-feature-document-f1` from `5d3051a`; commit
   this plan.
2. f1, pass zero. Write USAGE's interview section, marks red, shown in
   chat before and after; commit on the user's word.
3. f1, draft. `spec-channel-drafter.js`: the SC1.1 test list, red from
   the scratchpad, satisfiable on a scratch prototype.
4. f1, retire. `test-retirer.js` with `overlay` (the prototype rewrites
   the template in place); amend or retire what fails.
5. f1, approve the list and prove red. The whole suite on the prototype
   in a scratch worktree; each fixed detail checked against the contract,
   the document and its Constraints; then `progress run SC1.1 --expect
   red`.
6. f1, green. `unit-developer.js`; Claude runs the suite, `prompt_lang`
   and the size cap after the round.
7. f1, commit and Two-Key. Commit with the `Contract:` trailer; SC1.1
   green at the clean commit; `two-key-unit-verifier.js`; `progress done`
   on PASS.
8. Close. `STATE.md` regenerated; this plan struck; the push and the PR
   on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: six. The user's: (1) this plan, (2) the USAGE
section. Claude's, on review: (3) the test list, (4) the commit. The
user's at the close: (5) the push and the PR, (6) the merge.

Deferred, not this session:
- `f2-sections`, `f3-signing`, `f4-intake`, `f5-release` (ships 0.18.0).
- G1's solution half by hand (risk 5), after 0.18.0.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an
OPEN and a re-intake, never a silent edit.
