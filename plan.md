# Plan - Session 61 (2026-09-28) - tree-first-level t1

**Deliverable:** unit `t1-gate-rollup` of `tree-first-level` on one PR,
with a Two-Key PASS:

- `USAGE.md` gains the `tree-first-level` section first, every status
  mark red.
- `taskcontract/tree.py`: each gate item reads the roll-up of the
  verdicts at its gate, each `inactive` verdict left out, a closed
  feature's verdicts counted as they read, `to do` with no verdict. Each
  condition reads the roll-up of that condition across the same
  verdicts. A gate item or condition that is not `done` names each
  feature holding it back: `{feature} holds {id} at {status}`. A finding
  stands once under the condition or gate its `gate:` field names, shows
  its kind, and counts in no roll-up. Checks SC1.1 to SC1.3.
- Retired: the rule that a gate item and its conditions always read
  `to do`, in `tree.py`'s module and `derive` docstrings and at
  `USAGE.md:891`, and the assertions that pin it over done verdicts
  (about ten, seen in six modules: `test_tree_status.py`,
  `test_tree_conditions.py`, `test_tree_titles.py`, `test_tree_query.py`,
  `test_pane.py`, `test_pane_keys.py`).

**Rulings at plan review** (Claude's recommendation first):

1. Delegation as in sessions 52 to 55. The user approves the USAGE
   section in chat before any drafting. Claude approves the test list and
   the commit on review. The push, the PR and the merge stay on the
   user's word.
2. `test-retirer.js` gains an optional `overlay` argument: step 2 copies
   the drafter's prototype source files over the export, in place of
   deleting names. t1's retirement flips values on existing fixtures, so
   there is no name to delete. The feature document names test-retirer
   for it (Q14), and the spec channel, never the developer, writes tests.
   The script is local and untracked: one edit, launched by `scriptPath`.

## Steps

1. Open. Branch `session-61-tree-first-level-t1` from `1f30226`; commit
   this plan.
2. t1, pass zero. The `tree-first-level` section, marks red, and the
   edit at `USAGE.md:891`, shown in chat in full. It settles what the
   contract leaves open: where a `holds` diagnostic stands under its item,
   and the roll-up's order when verdicts disagree (the rule for a
   feature's roll-up, restated for a gate). Any narrowing of a contract
   sentence is flagged before approval. Commit on the user's word.
3. t1, draft. `spec-channel-drafter.js` for SC1.1 to SC1.3 into a new
   `tests/test_tree_rollup.py`, with a prototype; the whole suite on the
   prototype in a scratch worktree.
4. t1, retire. The ruling 2 edit, then `test-retirer.js` with the
   prototype as its overlay: each failing assertion amended or retired.
5. t1, approve the list and prove red. The standing checks (each fixed
   detail against the contract and the document, repeated names, session
   labels, every `done` resting on a rule that ran); the tests written;
   `progress run --expect red` per check.
6. t1, green. `unit-developer.js` from its interface note; the docstrings
   retire with the rule. Claude runs the suite after each round.
7. t1, commit and Two-Key. The commit on review; each check green at the
   clean commit; `two-key-unit-verifier.js`; `progress done` on PASS.
8. Close. PR; `STATE.md` regenerated (it still says PR #71 waits); this
   plan struck.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions now: three. Rulings 1 and 2, and this plan. Later: the USAGE
section (the user's), the test list and the commit (Claude's on review),
then the push, the PR and the merge (the user's).

Deferred, not this session:
- `t2-before-intake`, `t3-halves`, `t4-release` (ships 0.17.0).
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
