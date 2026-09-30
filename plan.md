# Plan - Session 63 (2026-09-29) - tree-first-level t3

**Deliverable:** unit `t3-halves` of `tree-first-level` on one PR, with a
Two-Key PASS:

- `USAGE.md`'s "Revisions and halves" (section 9) refined at pass zero,
  its marks still red.
- `taskcontract/tree.py`: a feature before intake names its document's
  revision, `no contract: document rN`, or `no revision table`. After its
  verdicts come two half items, `<id>/request` and `<id>/solution`. A half
  reads `done` with `by <signer> at rN` when a row in ADR 0034's form
  signs it, else `to do`. The feature reads `to do` until a half is
  signed, then `doing`. Checks SC3.1, SC3.2, SC3.3+SC4.3.
- Retired: the drift rule's "every row but `Ready:` and `Measured:`"
  (`tree.py:98` docstring, `drift` at `tree.py:313`); a `Signed:` row no
  longer counts as text. Found by `test-retirer.js`.
- Receipt: a live herdr pane on the kit shows
  `g1-requirements-spec/request [done] by user at r3`,
  `g1-requirements-spec/solution [to do]` and `gates/G0 [doing]`.

On the kit itself, `tree-first-level` loses `stale: document r7, contract
from r6`, since r7 is a `Signed:` row.

**Ruling at plan review:** delegation as in sessions 61 and 62. The user
approves the USAGE text in chat before any drafting. Claude approves the
test list and the commit on review. The push, the PR and the merge stay on
the user's word.

**Closed.** The deliverable is met: t3 at `a09278b` (USAGE), `00ce617`
(code and tests), `e5a814f` and `f1374c8` (two fixes), Two-Key PASS at
round 2. Suite 749 passed, scope-check green; on the kit,
`g1-requirements-spec` shows both halves and `tree-first-level` lost its
stale mark. The user chose to wrap before t4.

## Steps

1. ~~Open.~~ Branch cut from `1a86561`; the plan at `ca3bea5`.
2. ~~t3, pass zero.~~ At `a09278b` on the user's word, with five readings:
   a text row; newest and latest as the highest revision, a tie to the
   lower row; no text row above or a blank `Revised By` cell is no
   signature; the fixed words after `rN:`; every `Signed:` row out of both
   revisions. `USAGE.md:994` goes to t4's sweep.
3. ~~t3, draft.~~ 16 tests (52 cases) in `tests/test_tree_halves.py`, red
   52 of 52; the prototype changed `tree.py` only and caught 8 mutations.
4. ~~t3, retire.~~ Nothing retired or amended: 696 passed on the overlay.
5. ~~t3, approve the list and prove red.~~ 748 passed on the prototype in a
   scratch worktree. Claude's rulings: the kit path by the house idiom; the
   pane test not called live; the no-active-gate edge left unpinned
   (reversed at step 8). Checks red: 20, 29 and 3 cases.
6. ~~t3, green.~~ Round 1, no behavior deviation (`_last_cells` became
   `_rows` and `_counted`); suite 748 passed, the developer's run and
   Claude's.
7. ~~t3, commit and receipt.~~ At `00ce617`; checks green clean; a live
   herdr pane on the kit showed both halves under `gates/G0 [doing]`.
8. ~~t3, Two-Key.~~ Before launch Claude saw the unpinned edge contradict
   the approved USAGE text: fix `e5a814f`, a feature before intake never
   reads `done`. Round 1 FAIL: the document opened twice per print
   (Constraint 4). Fix `f1374c8`, read once, with a test counting opens.
   Round 2 PASS; the unit closed.
9. ~~Close.~~ `STATE.md` regenerated; this plan struck; the push and the PR
   on the user's word.

Steps 1 and 9 sit outside a contract unit, so the tree does not show
them.

Decisions this session: ten. The user's: (1) this plan, (2) the USAGE
text, (3) the order after t3 (t4, then `feature-document` ahead of G1),
(4) wrap before t4. Claude's: (5) t3's test list, (6) t3's commit, (7)
the fix to never `done`, (8) the fix to one read. The user's at the
close: (9) the push and the PR, (10) the merge.

Deferred, not this session:
- `t4-release` (ships 0.17.0, sweeps t1's, t2's and t3's Two-Key
  advisories, listed in `STATE.md`); next session.
- `feature-document` after 0.17.0, ahead of G1's solution half (user,
  2026-09-29): interview its REQUEST into `docs/features/`, intake,
  build, release 0.18.0. When it ships, tell the user the kit is ready to
  use on another machine.
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
