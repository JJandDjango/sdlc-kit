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
  characters (Constraints 1). It holds 5,358 now, so no split is
  planned; a split would need a path outside Scope, and so a re-intake.
- One manual receipt for SC4.1: a live intake on f3's document
  (`RECEIPT_feature-document-f3_2026-10-01/hello-name.md`) with one check
  left out of Units writes the `Parked:` row and no contract.

`USAGE.md` already holds f4's text ("Intake's refusals", lines 269 to
291), approved in session 68; its marks stay red until f5. Any change to
that text comes to the user in chat first.

Approvals split as in sessions 61 to 64 and 68 to 70: Claude approves
the test list and the commit on review; the plan, any ruling, the USAGE
text, the receipt's shape, the push, the PR and the merge stay on the
user's word.

## Steps

1. Open. Branch `session-71-feature-document-f4` cut from `795c175`;
   this plan committed on the user's word.
2. f4, draft. Two drafter runs side by side, each with its own scratch
   folder and test file. The flow: SC4.1, SC4.2 and SC4.3 against a
   scratch copy of `skills/sdlc/`. The tree: SC4.2's `Parked:` reading
   against `taskcontract/tree.py`. Each proves its list red, then green
   on its prototype.
3. f4, retire. The overlaid suite runs in a scratch worktree; the
   retirer gets the failing tests by name and runs only their modules.
4. f4, approve the list and prove red. The whole suite on the prototype
   in the worktree; each fixed detail read against the contract, the
   feature document and its Constraints; Claude approves; SC4.1, SC4.2
   and SC4.3 recorded red.
5. f4, green. Two developers side by side on separate files (the flow,
   the tree), each from an interface note file, neither running the
   whole suite; the session runs it once after both. `prompt_lang` on
   `intake.md`.
6. f4, commit. On Claude's review; each check green at the clean
   commit; scope-check green against `795c175`.
7. f4, the receipt. Two worktrees at the unit commit (the plugin folder
   and the repository), `hello-name.md` and its state file copied to
   `docs/features/`. Run A, the document as f3 left it: intake parks on
   the OPEN under ready check 12 or 14, one `Parked:` row, no contract.
   Then a hand edit as the toy engineer seat: both OPEN marks answered,
   one check taken out of a Units row, one text row and a `Signed:
   solution half` row after it. Run B: the row reads `Parked: Check {id}
   is assigned to no unit.`, and no contract stands. Both runs headless
   and hidden through `live-run-driver.py`. The documents and
   transcripts are kept in `RECEIPT_feature-document-f4_2026-10-01/`.
8. f4, Two-Key. On the unit's commits, the receipt as a focus pointer;
   `progress done` on PASS.
9. Close. `STATE.md` regenerated; this plan struck; the scratch
   worktrees removed; push, PR and merge, each on the user's word.

Steps 1 and 9 sit outside a contract unit, so the tree does not show
them.

Decisions expected: six. The user's: (1) this plan, with the receipt's
shape in step 7; (2) the push and the PR; (3) the merge. Claude's, on
review: (4) the test list, (5) the commit. Open until the draft: (6)
which message a `Parked:` row carries when more than one thing stands
(an OPEN and a check in no unit). The contract names one row and one
`{what stands}`; a reading that narrows it comes to the user before the
list is approved.

Deferred, not this session:
- `f5-release` (ships 0.18.0), with its sweep list in `STATE.md` Next
  actions 1.
- `lang-check --draft` runs neither VT002 nor VT006 on a draft term:
  left to intake, the gap logged for f5's sweep.
- G1's solution half by hand (risk 5), after 0.18.0.
- `test-retirer.js` waits on the whole suite inside its agent; the fix
  stays parked, and step 3 works around it.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; never two whole suites at
once; no spawn opens a window; a surprise mid-build is an OPEN and a
re-intake, never a silent edit.
