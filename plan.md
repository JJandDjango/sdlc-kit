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

**Closed.** The deliverable is met: t1 at `a0f36e2` (USAGE) and
`709d2cc` (code and tests), Two-Key PASS at round 1 with four
advisories, carried in `STATE.md`. Suite 663 passed, scope-check green,
and the kit's own `gates/G0` now reads `done`.

## Steps

1. ~~Open.~~ Branch cut from `1f30226`; the plan at `27aeb6b`.
2. ~~t1, pass zero.~~ Three red subsections in section 9, a second
   callout, and the old line 891 scoped to a feature's other gates, at
   `a0f36e2` on the user's word. A gate reads `doing` over a mix of
   `done` and `to do` verdicts, following the document's example; the
   user kept that reading.
3. ~~t1, draft.~~ 25 tests (16 names) in `tests/test_tree_rollup.py`,
   red 25 of 25 on assertions; the prototype changed `tree.py` alone and
   caught ten mutations.
4. ~~t1, retire.~~ `test-retirer.js` gained `overlay`; with the
   prototype over `tree.py`, nine tests failed in five modules, all
   amended, none retired, including the release test `a0f36e2` broke.
5. ~~t1, approve the list and prove red.~~ Approved by Claude; SC1.1,
   SC1.2 and SC1.3 red (13, 10 and 1 failing).
6. ~~t1, green.~~ Round 1, no deviation; suite 663 passed, the
   developer's run and Claude's. Claude rewrapped two `pane.py`
   docstring lines.
7. ~~t1, commit and Two-Key.~~ At `709d2cc`; the three checks green at
   the clean commit; PASS at round 1; the unit closed.
8. Close. `STATE.md` regenerated; this plan struck; the push and the PR
   on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: eight. The user's at plan review: (1) the plan,
(2) ruling 1, (3) ruling 2. The user's: (4) the USAGE section, with the
`doing` reading. Claude's, on review: (5) t1's test list, (6) t1's
commit. The user's at the close: (7) the push and the PR, (8) the merge.

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
