# Plan - Session 46 (2026-09-23) - pane-view p3 and p4

**Deliverable:** the last two units of `pane-view` (the request for a pane
that shows where the current task sits) on one PR, each with a Two-Key PASS
(one agent re-runs every check, a second grades the commit against the
contract, and a script computes the verdict):

- p3 `p3-line-parts`: `tree: pane: parts:` in `.sdlc/config.yaml` lists the
  fields each item line of the pane shows after its id, in the fixed order
  `status`, `marks`, `evidence`, `links`, `doc`, `summary`. A value that is
  not a list, or names an unknown field, leaves every field and prints
  `pane parts ignored: ...` on stderr. The `tree: pane:` reader lands in
  `tree.py`, beside `notify_command`.
- p4 `p4-fold-names`: `tree: pane: fold: names` makes each collapse line
  name the other items as `<id> [<status>]` instead of counts. `counts`
  and a missing setting keep the counts; any other value keeps them and
  prints `pane fold ignored: ...` on stderr.

**Closed.** The deliverable is met: p3 at `4e298af`, p4 at `3be9db2`, each
Two-Key PASS at round 1 with advisories only. Suite 577 passed, all fifteen
contracts ready-green, scope-check green. The live check after p4 passed in
herdr. pane-view's five units and the contract are closed in progress. The
push and the PR wait on the user's word.

## Steps

1. ~~Open.~~ Branch cut from `ee05d24`; the plan at `b2d8541`.
2. ~~p3, draft and approve the test list.~~ Nineteen tests; `_cut` and
   `_short` moved to `tests/conftest.py`; one p1 test name the rename
   glued (`..._iscut_lines`) restored at placement; approved by Claude.
3. ~~p3, write the tests and prove red.~~ SC2.1 to SC2.3 red as expected;
   the suite 41 failed, 505 passed.
4. ~~p3, green.~~ Suite 546 passed; every receipt green.
5. ~~p3, approve the commit and commit.~~ At `4e298af`; the three checks
   green.
6. ~~p3 Two-Key.~~ PASS at round 1; its docstring advisory fixed at p4.
7. ~~p4, draft and approve the test list.~~ Fifteen tests; approved by
   Claude.
8. ~~p4, write the tests and prove red.~~ SC4.1 and SC4.2 red as expected;
   the suite 31 failed, 546 passed.
9. ~~p4, green.~~ Suite 577 passed; every receipt green.
10. ~~p4, approve the commit and commit.~~ At `3be9db2`; both checks green.
11. ~~p4 Two-Key.~~ PASS at round 1; three advisories, carried to t9.
12. ~~The live check in herdr.~~ The request's example drawn live at t6's
    first approval; the hook flagged the probe `sdlc`, `blocked`; a bad
    `fold:` brought the counts back with its message.
13. ~~Close.~~ STATE.md regenerated; this plan struck; the push and the PR
    go to the user.

Steps 1, 12 and 13 sit outside a contract unit, so the pane does not show
them.

Decisions this session: nine. The user's: (1) the deliverable, p3 and p4:
yes; (2) the delegation of p3's and p4's approvals: yes; (3) this plan:
yes. Claude's, on review: (4) p3's test list; (5) p3's commit; (6) p4's
test list; (7) p4's commit. The user's at the close: (8) the push and the
PR; (9) the merge.

Deferred, not this session:
- tree-view t6 and t9 (0.15.0), then G1.
- The pilot's config line, in the engine's session.
- `.sdlc/config.yaml` still lists `plan.workflow.json` as a free path.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on every
commit that touches a non-free path; before placing a drafted list, session
labels stripped from its names and the module checked for a repeated test
name; no tracked file touched while a verifier runs; every herdr probe
closes the panes it opens; a surprise mid-build is an OPEN (a question
written back into the request) and a re-intake, never a silent edit.
