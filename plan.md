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

## Steps

1. Open. Branch cut from `1a86561` (PR #73's merge); this plan.
2. t3, pass zero. Refine "Revisions and halves"; flag each narrowing or
   reading against the contract and the feature document; the user
   approves the text in chat; commit, marks red.
3. t3, draft. `spec-channel-drafter.js` drafts the list for SC3.1, SC3.2
   and SC3.3+SC4.3, proves it red, and proves it satisfiable on a
   prototype.
4. t3, retire. `test-retirer.js`, with the prototype as `overlay`, finds
   the tests that pin a `Signed:` row counting as text.
5. t3, approve the list and prove red. The whole suite on the prototype in
   a scratch worktree; the standing checks (details against the contract,
   caps against free text with line breaks, no session labels, no repeated
   name); Claude approves; `progress run --expect red` per check.
6. t3, green. `unit-developer.js` from the interface note; Claude runs the
   suite after each round.
7. t3, commit and receipt. Checks green at the clean commit; the live pane
   receipt above.
8. t3, Two-Key. `two-key-unit-verifier.js`; every receipt exits 0; the unit
   closes through `progress done` on PASS.
9. Close. `STATE.md` regenerated (and its stale "not pushed" line gone);
   this plan struck; the push and the PR on the user's word.

Steps 1 and 9 sit outside a contract unit, so the tree does not show
them.

Decisions this session: six. The user's: (1) this plan, (2) the USAGE
text. Claude's: (3) t3's test list, (4) t3's commit. The user's at the
close: (5) the push and the PR, (6) the merge.

Deferred, not this session:
- `t4-release` (ships 0.17.0, sweeps t1's and t2's Two-Key advisories,
  and `USAGE.md:994`); next after t3, this session if it fits.
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
