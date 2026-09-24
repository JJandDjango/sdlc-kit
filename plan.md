# Plan - Session 47 (2026-09-23) - tree-view t6 and t9, release 0.15.0

**Deliverable:** the last two units of `tree-view` on one PR, each with a
Two-Key PASS (one agent re-runs every check, a second grades the commit
against the contract, and a script computes the verdict), then the release:
the merge, the annotated tag `v0.15.0` at the merge, and the self-pin through
its own PR.

- t6 `t6-query-face`: `taskcontract tree <id>` prints that item in at most
  20 lines: its source field, status, links and each file reference (a repo
  path plus the line of its source; a gate or a task step names its kit
  page). An unknown id exits `2` and prints `no node '{id}' - print the tree
  to list every node id`. It lands in `taskcontract/tree_view.py`, tested in
  `tests/test_tree_query.py`.
- t9 `t9-release`: the `USAGE.md` marks of tree-view and pane-view read
  green; the version reads `0.15.0` in `pyproject.toml` and `KIT_VERSION`;
  `CHANGELOG.md` gains the entry and `MAP.md` a row.

**Rulings at plan review** (the user's):

1. An id that names two items (a check named like a task step, or a unit
   named like an active gate) prints both, in tree order, each in at most
   20 lines.
2. Claude approves t6's test list and commit on review. The user approves
   t9's commit, shown in chat. The push, the PR, the merge, the tag and the
   self-pin stay on the user's word.

**Closed at the PR, on the user's word.** Both units are built and pass
Two-Key: t6 at round 3 (`c1380d5`, `ba4c117`, `7945f13`), t9 at round 2
(`497418a`, `bf18594`, `c48ae8c`). The contract is closed in progress.
Suite 592 passed, fifteen contracts ready-green, scope-check green. The
release, step 11, opens session 48.

## Steps

1. ~~Open.~~ Branch cut from `84ebc5e`; the plan at `719a309`.
2. ~~t6, draft and approve the test list.~~ Twelve tests, red 12 of 12,
   green on the drafter's prototype; approved by Claude.
3. ~~t6, write the tests and prove red.~~ SC6.1 to SC6.3 red as expected;
   the suite 12 failed, 577 passed.
4. ~~t6, green.~~ Suite 589 passed.
5. ~~t6, approve the commit and commit.~~ At `c1380d5`; the three checks
   green; the query answered on the kit's own tree.
6. ~~t6 Two-Key.~~ Round 1 FAIL: the `doc:` line carried no line. Round 2
   FAIL: line breaks in free text passed the 20-line cap. Round 3 PASS.
   Claude amended two tests and added three, each red first.
7. ~~t9, the USAGE pass, the version, the CHANGELOG entry and the MAP
   row.~~ Four code-wording notes carried to t9 rode t6 instead, since t6
   edited the same text.
8. ~~t9, the user approves the commit; commit.~~ At `497418a`; the query
   example dated at `bf18594`.
9. ~~t9, the release sweep, then Two-Key.~~ The sweep clean; round 1 FAIL
   on one sentence about a close's evidence, fixed at `c48ae8c`; round 2
   PASS. t9 and the contract closed.
10. ~~Close.~~ STATE.md regenerated; this plan struck; the push and the PR
    on the user's word ("stop at PR").
11. Release: merge on the user's word, the annotated tag `v0.15.0` at the
    merge, then the self-pin (`.github/workflows/sdlc.yml` and USAGE
    section 7 to `@v0.15.0`) through its own PR. Deferred to session 48.

Steps 1, 10 and 11 sit outside a contract unit, so the pane does not show
them.

Decisions this session: ten. The user's at plan review: (1) the
deliverable: yes; (2) the delegation: yes; (3) the id ruling: yes; (4) this
plan: yes. Claude's, on review: (5) t6's test list; (6) t6's commit, and
each fix round's tests and commits. The user's: (7) t9's commit: yes; (8)
the boundary: stop at the PR; (9) the push and the PR: yes, with (8).
Session 48's: (10) the merge, the tag and the self-pin.

Deferred, not this session:
- The release of 0.15.0 (step 11).
- G1: its criteria review, before the pilot's M0 code.
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
