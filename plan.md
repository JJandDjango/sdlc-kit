# Plan - Session 52 (2026-09-25) - project-tree o1

**Deliverable:** unit `o1-conditions` of `project-tree` on one PR, with a
Two-Key PASS (one agent re-runs every check, a second grades the commit
against the contract, and a script computes the verdict):

- `USAGE.md` gains the project-tree section first, every status mark red.
- `taskcontract/data/gates.yaml`: each gate gains `conditions:` in page
  order, 57 in all, each an `id` and a `name`; G0's three conditions also
  carry `rules`: G0.1 TC000 to TC009 and TC013 to TC015, G0.2 TC010 to
  TC012 and TC017, G0.3 TC016 and TC018.
- `taskcontract/tree.py`: each gate opens into its conditions; a G0
  condition takes its status from its own rules, and one that is not done
  lists its diagnostics, one line each, with no code; warnings (W001) stay
  out; each contract's G0 verdict reads as before.
- `tests/test_tree_conditions.py` carries SC2.1 to SC2.3, and one test
  holds each code the validator emits to exactly one condition.

**Rulings at plan review** (the user's):

1. The user approves the USAGE section, shown in chat in full. Claude
   approves o1's test list and commit on review, as in sessions 45 to 47.
   The push, the PR and the merge stay on the user's word.

## Steps

1. Open: branch `session-52-project-tree-o1` cut from `df7cbb6`; this plan
   committed.
2. o1, pass zero: the USAGE section, marks red, shown in chat; commit on
   the user's word.
3. o1, draft and approve the test list. Before approving: the 57
   conditions against `docs/gates/`; each fixed detail against every use
   of its terms in the contract and the feature document; session labels
   stripped; no repeated test name.
4. o1, write the tests and prove red.
5. o1, green: the developer works from the interface note, without
   opening `tests/`.
6. o1, approve the commit and commit; the checks green.
7. o1 Two-Key; o1 closed.
8. Close: STATE.md regenerated; this plan struck; the push and the PR go
   to the user.

Steps 1 and 8 sit outside a contract unit, so the pane does not show them.

Decisions this session: eight. The user's at plan review: (1) the
deliverable; (2) the delegation; (3) this plan. The user's: (4) the USAGE
section. Claude's, on review: (5) o1's test list; (6) o1's commit. The
user's at the close: (7) the push and the PR; (8) the merge.

Deferred, not this session:
- o2 to o7: o2, o3 and o4 next, then o5, o6 and o7 (0.16.0).
- G1, after project-tree ships.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on every
commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an OPEN
(a question written back into the feature document) and a re-intake, never
a silent edit.
