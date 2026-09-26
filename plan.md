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

**Closed.** The deliverable is met: o5 at `b9a2cb1` and its fix
`afad4b0`, o6 at `202f01d` and its fix `39811d7`; Two-Key PASS for each at
round 2. Suite 638 passed, scope-check green. The push and the PR wait on
the user's word.

## Steps

1. ~~Open.~~ Branch cut from `9d0e897`; Textual 8.2.8 installed; the plan
   at `c87808d`.
2. ~~USAGE, one batch.~~ "The interactive pane" refined with four
   readings (the current task's unit opens at the start and on a move, the
   plain-name cut, the 0.15.0 lines retired), approved in chat, at
   `c9e05e6`.
3. ~~o5.~~ 20 tests (31 cases); Claude added a line-break plain name at
   approval. At `b9a2cb1`; Two-Key FAIL at round 1: the cut dropped
   `current`, so a pane under 72 columns lost the marker (Claude had
   accepted that deviation). Fix at `afad4b0` with a test at 60 and 68
   columns and USAGE's cut sentence aligned; PASS at round 2.
4. ~~o6.~~ The first drafter passed 400K tokens and was stopped on the
   user's word; three narrow agents replaced it: keys (11 tests), renders
   and notify (21), and the 0.15.0 loop's retirement (150 cases retired,
   eleven tests amended). Claude ruled that a finding counts by its kind,
   added an unset-notify test, and, reviewing the code, pinned red a
   notify failure a render dropped unseen, which the developer fixed. The
   tests went to `tests/test_pane_keys.py` and `tests/test_pane_renders.py`,
   not `tests/test_pane.py`. At `202f01d`; Two-Key FAIL at round 1 on a
   test docstring stating the old tick order; fix at `39811d7`; PASS at
   round 2.
5. Close. PR; STATE.md regenerated; this plan struck.

Steps 1, 2 and 5 sit outside a contract unit, so the tree does not show
them.

Decisions this session: fourteen. The user's: rulings 1 to 3 and the plan
(1 to 4); the USAGE batch and its four readings (5); the drafter split
(6). Claude's, on review: the two test lists (7, 8), with the finding
ruling in o6's; the four commits (9 to 12). The user's at the close: (13)
the push and the PR; (14) the merge.

Deferred, not this session:
- o7 (ships 0.16.0) with its sweep: STATE.md Next actions 2, plus this
  session's Two-Key advisories.
- A live run of the pane in a herdr pane on Windows; the receipts are
  headless.
- Prerequisites 7 to 9, G1, and the rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on every
commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an OPEN
and a re-intake, never a silent edit.
