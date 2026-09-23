# Plan - Session 45 (2026-09-23) - pane-view p0 to p2

**Deliverable:** three units of `pane-view` (the request for a pane that
shows where the current task sits) on one PR, each with a Two-Key PASS
(one agent re-runs every check, a second grades the commit against the
contract, and a script computes the verdict):

- p0 `p0-usage-pass-zero`: USAGE section 9 gains "The pane's lines": the
  where-am-I line, short ids and the two `tree: pane:` settings (`parts:`,
  `fold:`), every mark red until tree-view's t9 turns them green.
- p1 `p1-where-line`: the pane gains a where-am-I line, under the waiting
  line at an approval and first otherwise:
  `specs/pane-view/contract.yaml > pane-view > p2-short-ids > approve-tests`.
- p2 `p2-short-ids`: each item line under a parent opens on the last
  segment of its id (`p2-short-ids`, `approve-tests`); the whole tree, the
  waiting line, the links and `SDLC_NODE` keep full ids.

**Closed.** The deliverable is met: p0 at `7d31d4a`, p1 at `b80aed3`, p2 at
`3802a8c`, each Two-Key PASS at round 1 with advisories only. Suite 505
passed, all fifteen contracts ready-green, scope-check green. The live
check after p1 passed in herdr. The push and the PR wait on the user's
word.

p3 and p4 take session 46: they share the `tree: pane:` reader p3 adds, and
five units in one session is five Two-Key rounds.

## Steps

1. ~~Open.~~ Branch cut from `22c4982`; the plan at `0ba7289`.
2. ~~p0, the section.~~ "The pane's lines", shown in chat in full.
3. ~~p0, commit.~~ At `7d31d4a`, on the user's word.
4. ~~p0 Two-Key.~~ PASS at round 1; advisory: the example's `14 more` now
   reads `15 more`, carried to t9.
5. ~~p1, draft and approve the test list.~~ Ten tests, seven t7 and t8
   tests amended; approved by Claude.
6. ~~p1, write the tests and prove red.~~ SC1.1 and SC1.2 red as expected.
7. ~~p1, green.~~ Suite 496 passed; every receipt green.
8. ~~p1, approve the commit and commit.~~ At `b80aed3`; both checks green.
9. ~~p1 Two-Key.~~ PASS at round 1; its docstring advisory fixed at p2's
   placement.
10. ~~The live check in herdr.~~ A probe pane at p2's `approve-tests` kept
    the waiting line first, and the hook flagged it `sdlc`, `blocked`.
11. ~~p2, draft and approve the test list.~~ Nine tests, four p1 and nine
    t7 and t8 tests amended; approved by Claude.
12. ~~p2, write the tests and prove red.~~ SC3.1 and SC3.2 red as expected.
13. ~~p2, green.~~ Suite 505 passed; every receipt green.
14. ~~p2, approve the commit and commit.~~ At `3802a8c`; both checks green.
15. ~~p2 Two-Key.~~ PASS at round 1; advisory: the copied test helpers,
    carried to p3.
16. ~~Close.~~ STATE.md regenerated; this plan struck; the push and the PR
    go to the user.

Decisions this session: ten. The user's: (1) the deliverable, p0 to p2:
yes; (2) the delegation of p1's and p2's approvals: yes; (3) this plan:
yes; (4) p0's section: yes. Claude's, on review: (5) p1's test list; (6)
p1's commit; (7) p2's test list; (8) p2's commit. The user's at the close:
(9) the push and the PR; (10) the merge.

Deferred, not this session:
- p3 and p4 (session 46), then tree-view t6 and t9 (0.15.0), then G1.
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
