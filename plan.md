# Plan - Session 54 (2026-09-26) - project-tree o5, o6

**Deliverable:** units `o5-pane-outline` and `o6-pane-keys` of
`project-tree` on one PR, each with its own Two-Key PASS:

- o5: with the `pane` extra (Textual `>=8.2,<9`), `taskcontract tree
  --follow` runs a Textual app in the new `taskcontract/pane.py`: the whole
  tree as an outline, each feature open down to its units, the current
  task marked and in view, and a line under the outline with the plain
  name and document reference of the item at the cursor. Without the
  extra, the install line on stderr and exit 2. Checks SC4.1 and SC1.2.
- o6: Up, Down, Right, Left, a click and the wheel; a redraw within two
  seconds of a source change keeps the cursor and every open and closed
  item; the waiting line stays first; notify runs once per arrival at an
  approval; Ctrl-C exits 0. Checks SC4.2, SC4.3 and SC3.3.

**Rulings at plan review** (the user's; Claude's recommendation first):

1. Delegation as in session 53. The user approves the USAGE batch (step
   2) in chat before any drafting; Claude approves each test list and
   commit on review. The push, the PR and the merge stay on the user's
   word.
2. The 0.15.0 loop: o5 points `--follow` at the app and leaves
   `tree_view.follow()` callable in-process, so its notify and redraw
   tests hold while the app has neither. o6 moves the watch, notify and
   Ctrl-C into the app, retires `follow()`, and moves its tests to
   `tests/test_pane.py`. Retiring it at o5 would drop tested behavior for
   one unit.
3. Tests drive the app through Textual's headless `App.run_test()` inside
   `asyncio.run`, so the `test` extra gains Textual alone, no
   pytest-asyncio.

## Steps

1. Open. Branch `session-54-project-tree-o5-o6` from `9d0e897`; install
   Textual `>=8.2,<9` locally; commit this plan.
2. USAGE, one batch. Refine "The interactive pane" for o5 and o6, shown
   in chat in full. It settles what the contract leaves open: the cursor
   line's shape; the current task's mark (`current`, as today); whether
   the where-am-I line stays under the waiting line; Right and Left on an
   item with nothing under it; where the stderr lines sit; and how the
   outline cuts a line whose plain name (a unit's `done_means`) pushes
   its status past the pane's edge. Any narrowing of a contract sentence
   is flagged before approval.
3. o5. Drafter, then a full-suite run on its prototype in a scratch
   worktree, approval, prove red, developer, commit, Two-Key.
4. o6, the same way; its drafter may run beside o5's Two-Key.
5. Close. PR; STATE.md regenerated; this plan struck.

Steps 1, 2 and 5 sit outside a contract unit, so the tree does not show
them.

Decisions now: four. Rulings 1 to 3, and this plan. Later: the USAGE
batch (the user's), two test lists and two or more commits (Claude's on
review), then the push, the PR and the merge (the user's).

Deferred, not this session:
- o7 (ships 0.16.0) with its sweep, STATE.md Next actions 2.
- The test row pattern's ` [` split (Next actions 3).
- Prerequisites 7 to 9, G1, and the rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on every
commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an OPEN
and a re-intake, never a silent edit.
