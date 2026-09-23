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

p3 and p4 take session 46: they share the `tree: pane:` reader p3 adds, and
five units in one session is five Two-Key rounds.

Where things stand: PR #54 merged at `22c4982`; `main` is clean and even
with origin. At session 44's close the suite read 486 passed and all
fifteen contracts ready-green. p1 and p2 change pane lines that t7's and
t8's tests pin as equal to the whole tree's lines, so each drafter names
those tests and amends them in `tests/test_tree_pane.py`; new tests go in
`tests/test_pane_view.py`.

**Who does what.** The user rules on the deliverable, the delegation, this
plan and p0's section, and at the close on the push and the merge.
Subagents do p1's and p2's work through the Workflow tool, launched by
`scriptPath`: the drafter drafts the test list, proves it red from the
scratchpad and prototypes the interface; the developer greens the tests
from the interface note without opening `tests/`; Two-Key grades last.
Claude approves each test list and each commit (`--by claude`), places the
tests, records each task with `taskcontract progress`, and runs the
receipts (the commands the verifier re-runs) before each verifier round.

## Steps

1. **Open.** Branch `session-45-pane-view-p0-p2` from `22c4982`; this plan
   committed on the user's word.
2. **p0, the section.** "The pane's lines", written into USAGE section 9,
   every mark red, shown in chat in full. p0 has no test, so approve-tests,
   write-tests and prove-red close with the unit; the pane shows p0's
   `green` while the section is written and its `approve-commit` while the
   section waits on the user.
3. **p0, commit** on the user's word, `Contract: pane-view`.
4. **p0 Two-Key**, sweep off (the repo-wide search runs only in a release
   unit), focus on p0's two sketches; on PASS, `progress done` closes p0.
5. **p1, draft and approve the test list**: SC1.1, SC1.2, and the t7 and
   t8 tests the new line shifts.
6. **p1, write the tests and prove red**, each check's red recorded with
   `progress run --expect red`.
7. **p1, green**, then the receipts: the suite, every contract ready-green,
   the vocabulary and language doors (`vocab-check`, `lang-check`), and
   `scope-check --base 22c4982`.
8. **p1, approve the commit and commit**, each check's green recorded with
   `progress run`.
9. **p1 Two-Key**, with p2's drafter beside it (neither touches tracked
   files); on PASS, `progress done` closes p1.
10. **The live check in herdr.** While the kit sits on p2's
    `approve-tests`, a pane split with `--no-focus` runs the new pane: the
    waiting line stays first, and the hook flags the seat. The pane closes
    after.
11. **p2, approve the test list**: SC3.1, SC3.2, and the t7 and t8 tests
    whose lines shorten.
12. **p2, write the tests and prove red.**
13. **p2, green**, then the receipts.
14. **p2, approve the commit and commit.**
15. **p2 Two-Key**; on PASS, `progress done` closes p2.
16. **Close.** STATE.md regenerated and this plan struck; the push and the
    PR on the user's word.

Decisions this session: ten. The user's, now: (1) the deliverable, p0 to
p2; (2) the delegation of p1's and p2's approvals; (3) this plan. The
user's, mid-session: (4) p0's section. Claude's, on review: (5) p1's test
list; (6) p1's commit; (7) p2's test list; (8) p2's commit. The user's at
the close: (9) the push and the PR; (10) the merge.

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
