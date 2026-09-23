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

## Steps

1. Open. Branch `session-46-pane-view-p3-p4` cut from `ee05d24`; this plan.
2. p3, draft and approve the test list. SC2.1 to SC2.3; the drafter writes
   `tests/test_pane_view.py` whole and moves `_cut` and `_short` into
   `tests/conftest.py` (p2's Two-Key advisory).
3. p3, write the tests and prove red.
4. p3, green: the developer adds the `tree: pane:` reader to `tree.py`.
5. p3, approve the commit and commit.
6. p3 Two-Key. p4's drafter may run beside it.
7. p4, draft and approve the test list. SC4.1 and SC4.2.
8. p4, write the tests and prove red.
9. p4, green.
10. p4, approve the commit and commit.
11. p4 Two-Key.
12. The live check in herdr: a probe pane on a scratch copy of the root,
    with `parts:` and `fold: names` set.
13. Close. STATE.md regenerated; this plan struck; the push and the PR go
    to the user.

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
