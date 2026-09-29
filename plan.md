# Plan - Session 62 (2026-09-28) - tree-first-level t2

**Deliverable:** unit `t2-before-intake` of `tree-first-level` on one PR,
with a Two-Key PASS:

- `USAGE.md`'s "Features before intake" (section 9) refined at pass zero,
  its marks still red.
- `taskcontract/tree.py`: each `.md` file directly under `docs/features/`
  with no `specs/<id>/contract.yaml` shows at the first level as a feature
  before intake. Its id is the file name, its plain name the title line's
  words after the first ` - `, its reference its document. Its G0 verdict
  and conditions read `to do` with no validator run, its next gate reads
  `inactive`, and the G0 verdict counts in `gates/G0`'s roll-up. It stands
  among the features with a contract by its id. Once a contract exists,
  the feature stays one item, as today. Checks SC2.1, SC2.2, SC2.3, SC4.1.
- Retired: the module docstring's "opens each contract's
  docs/features/<id>.md for its revision table only", and any assertion
  that a document without a contract shows nothing, found by
  `test-retirer.js` with `overlay`.

On the kit itself, `g1-requirements-spec` joins the first level and
`gates/G0` moves from `done` to `doing`.

**Ruling at plan review:** delegation as in session 61. The user approves
the USAGE text in chat before any drafting. Claude approves the test list
and the commit on review. The push, the PR and the merge stay on the
user's word.

**Closed.** The deliverable is met: t2 at `83532e5` (USAGE) and
`556c0eb` (code and tests), Two-Key PASS at round 1 with three
advisories, carried in `STATE.md`. Suite 696 passed, scope-check green,
and the kit's `gates/G0` now reads `doing`, held by
`g1-requirements-spec`.

## Steps

1. ~~Open.~~ Branch cut from `8afca18` (PR #72's merge); the plan at
   `da94a6e`, with the user's three readings for pass zero.
2. ~~t2, pass zero.~~ At `83532e5` on the user's word: a document with no
   revision shows; a title line with no words after ` - ` reads `(no
   title)`; the query paragraph moved here from t3's subsection; and a
   fourth reading, a verdict before intake names `page:` and no `file:`.
3. ~~t2, draft.~~ 20 tests (32 cases) in `tests/test_tree_before_intake.py`,
   red 32 of 32 on assertions; the prototype changed `tree.py` and
   `pane.py` and caught 11 mutations. Claude ruled the item's level
   `feature`, never `contract`, so `progress` refuses it; one more test
   pins that (21 tests, 33 cases).
4. ~~t2, retire.~~ With the prototype as `overlay`, two kit-tree tests
   failed (`test_tree.py`, `test_tree_titles.py`), both amended, none
   retired.
5. ~~t2, approve the list and prove red.~~ The whole suite on the
   prototype in a scratch worktree, 696 passed; approved by Claude;
   `SC2.1+SC4.1`, `SC2.2` and `SC2.3` red (24, 8 and 1 failing).
6. ~~t2, green.~~ Round 1, no deviation; suite 696 passed, the developer's
   run and Claude's. Claude reworded one docstring sentence.
7. ~~t2, commit and Two-Key.~~ At `556c0eb`; the three checks green at
   the clean commit; PASS at round 1; the unit closed. The first launch
   was stopped: a receipt meant to exit 2 would have failed it.
8. Close. `STATE.md` regenerated; this plan struck; the push and the PR
   on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: seven. The user's: (1) the plan with its three
readings, (2) the USAGE text with the fourth. Claude's: (3) the item
level `feature`, (4) t2's test list, (5) t2's commit. The user's at the
close: (6) the push and the PR, (7) the merge.

Deferred, not this session:
- `t3-halves`, `t4-release` (ships 0.17.0).
- G1's solution half, then its intake.
- `STATE.md` Next actions 3 to 6 and its open questions, carried
  unchanged.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an
OPEN and a re-intake, never a silent edit.
