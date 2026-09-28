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

## Steps

1. Open. Branch cut from `8afca18` (PR #72's merge); this plan committed.
2. t2, pass zero. Refine "Features before intake" (`USAGE.md:1212`),
   marks red; before and after shown in chat, each reading flagged;
   committed on the user's word.
3. t2, draft. `spec-channel-drafter.js`: tests for SC2.1, SC2.2, SC2.3
   and SC4.1, red from the scratchpad, satisfied by a prototype of
   `tree.py`.
4. t2, retire. `test-retirer.js` with the prototype as `overlay`: each
   test that fails on the export, amended or retired.
5. t2, approve the list and prove red. The whole suite on the prototype
   in a scratch worktree; each fixed detail checked against the contract
   and the feature document; `progress run --expect red` per check.
6. t2, green. `unit-developer.js` from the interface note; Claude runs the
   suite after each round.
7. t2, commit and Two-Key. The four checks green at the clean commit;
   `two-key-unit-verifier.js`; `progress done` on PASS.
8. Close. `STATE.md` regenerated; this plan struck; the push and the PR
   on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: six. The user's: (1) the plan, (2) the USAGE
text with its readings. Claude's, on review: (3) t2's test list, (4) t2's
commit. The user's at the close: (5) the push and the PR, (6) the merge.

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
