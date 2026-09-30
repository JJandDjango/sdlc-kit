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

**Closed.** The deliverable is met: f1 at `6e0b381` (USAGE) and
`0e1514e` (skill and tests), Two-Key PASS at round 1 with four
advisories, carried in `STATE.md`. Suite 766 passed, scope-check green,
`prompt_lang` green on all five prompt files; the unit closed.

## Steps

1. ~~Open.~~ Branch cut from `5d3051a`; the plan at `8ad7c21`.
2. ~~f1, pass zero.~~ Section 4's interview subsection rewritten for
   f1 to f4, every mark red, at `6e0b381` on the user's word, with three
   readings kept: the section covers f1 to f4; section 9's lists of rows
   that change no text gain `Parked:` in f4; the Next step line keeps
   its behavior with the new path.
3. ~~f1, draft.~~ 19 tests in `tests/test_interview_format.py`, red 19
   of 19; the prototype changed four skill files, passed `prompt_lang`,
   and caught nine mutations. Claude renamed four tests that carried
   session labels and pinned ADR 0026's section names out of the prose.
4. ~~f1, retire.~~ The retirer's own suite run was killed when its agent
   returned; Claude ran the overlaid export in the session: three
   failures in `test_skill_interview.py`, two retired with
   `TEMPLATE_SECTIONS`, the chain-free count amended to two.
5. ~~f1, approve the list and prove red.~~ The worktree suite passed
   766; approved by Claude; SC1.1 red, 19 failing.
6. ~~f1, green.~~ Round 1; three deviations, none against `done_means`
   (a stray `</output>` it reported removing was the Read tool's
   wrapper; nothing changed). Suite 766, the developer's run and
   Claude's.
7. ~~f1, commit and Two-Key.~~ At `0e1514e`; SC1.1 green at the clean
   commit; PASS at round 1; the unit closed.
8. ~~Close.~~ `STATE.md` regenerated; this plan struck; the push and the
   PR on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: six. The user's: (1) this plan, (2) the USAGE
section. Claude's, on review: (3) the test list, (4) the commit. The
user's at the close: (5) the push and the PR, (6) the merge.

Deferred, not this session:
- `f2-sections`, `f3-signing`, `f4-intake`, `f5-release` (ships 0.18.0).
- G1's solution half by hand (risk 5), after 0.18.0.
- `test-retirer.js` waits on the whole suite inside its agent, and the
  run dies when the agent returns; hand the suite run to the session.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an
OPEN and a re-intake, never a silent edit.
