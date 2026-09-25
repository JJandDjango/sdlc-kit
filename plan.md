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

**Closed.** The deliverable is met: o1 at `5864783` (USAGE) and `d277595`
(code and tests), Two-Key PASS at round 1 with four advisories, carried to
o2. Suite 618 passed, scope-check green. PR #61 carries the session; the
merge waits on the user's word.

## Steps

1. ~~Open.~~ Branch cut from `df7cbb6`; the plan at `75cb76b`.
2. ~~o1, pass zero.~~ Five red subsections in section 9, shown in chat in
   full, at `5864783` on the user's word.
3. ~~o1, draft and approve the test list.~~ 26 tests and six amended
   modules; the 57 conditions match the gate pages. Approved by Claude
   with one change: a contract the tree cannot read as a mapping reads
   `to do` at G0.2 and G0.3, never a false `done`.
4. ~~o1, write the tests and prove red.~~ SC2.1 to SC2.3 red as expected;
   all 26 fail on assertions.
5. ~~o1, green.~~ Suite 618 passed; two deviations, both accepted (the
   cache's type, and the ready profile read on a draft-red contract).
6. ~~o1, approve the commit and commit.~~ At `d277595`; the three checks
   green at the clean commit.
7. ~~o1 Two-Key; o1 closed.~~ PASS at round 1.
8. ~~Close.~~ PR #61; STATE.md regenerated; this plan struck.

Steps 1 and 8 sit outside a contract unit, so the pane does not show them.

Decisions this session: eight. The user's at plan review: (1) the
deliverable: yes; (2) the delegation: yes; (3) this plan: yes. The user's:
(4) the USAGE section: yes. Claude's, on review: (5) o1's test list, with
the unreadable-contract change; (6) o1's commit. The user's at the close:
(7) the push and the PR: yes; (8) the merge: open.

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
