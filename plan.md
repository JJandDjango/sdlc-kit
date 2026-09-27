# Plan - Session 55 (2026-09-26) - project-tree o7, release 0.16.0

**Deliverable:** unit `o7-release` of `project-tree` with its Two-Key
PASS, then the release: the merge, the annotated tag `v0.16.0` at the
merge, and the self-pin through its own PR. o7's done_means: kit 0.16.0
ships with the `USAGE.md` marks all green, its `CHANGELOG.md` entry and
ADR 0032; `taskcontract tree` still prints every item and exits 0, and
`taskcontract tree <id>` answers every id in at most seven lines (SC1.3).

**Rulings at plan review** (the user's; Claude's recommendation first):

1. Merge PR #63 by merge commit once CI reads green, then cut
   `session-55-project-tree-o7` from main's new tip. Cutting from session
   54's tip would stack two unmerged PRs.
2. The live run comes first, before any release text: the pane runs in a
   herdr pane on Windows, and the user drives its keys. A defect it finds
   is an OPEN and a re-intake, never a silent fix inside o7, whose
   done_means covers no pane behavior.
3. No test list for o7. o1's tests already pin SC1.3
   (`tests/test_tree_conditions.py:801` and `:842`), so o7 records
   SC1.3's run green on them, as t9 did for tree-view. The feature
   document names `tests/test_tree_view.py`, which no longer exists; the
   contract names no test file, and Two-Key grades the contract.
4. Claude writes the release text: the USAGE sweep, the CHANGELOG entry,
   ADR 0032 and MAP's work-tree row. The user approves all of it in one
   batch, shown in chat as before and after, and then approves the commit
   (o7's seat is `user`). Two-Key runs through the verifier Workflow.

**Closed.** The deliverable is met: o7 at `3040fa7` and its fix
`1bab527`, Two-Key PASS at round 2, `project-tree` closed at `1bab527`;
PR #64 merged at `17da7fd`, tagged `v0.16.0`; the self-pin at `72e9b9e`.
Suite 638 passed.

## Steps

1. ~~Open.~~ PR #63 merged at `ea3c83c`; the branch cut from it; the plan
   at `d465cd4`.
2. ~~The live run.~~ Pane `w9:pE`: the keys by `send-keys`, a render on
   o7's `approve-tests` record that kept the cursor and the open items,
   then the user's clicks, wheel and Ctrl-C. The pane closed itself on
   exit.
3. ~~The release text.~~ Approved in one batch. ADR 0031 stays as written
   (ADRs are append-only, `DOCS-SYSTEM.md:45`); ADR 0032 amends it. The
   first suite run failed on the o1 test that pinned the marks red; it
   now pins them green and no red mark in section 9, approved with the
   batch.
4. ~~The version.~~ `0.16.0` in both.
5. ~~o7's commit.~~ At `3040fa7`, approved by the user; SC1.3 green after
   it.
6. ~~Two-Key.~~ Round 1 FAIL: the evidence paragraph said a closed unit or
   contract always reads done, while a later record wins; the sweep found
   three test comments stating retired pane lines. Fix at `1bab527`,
   approved by the user; PASS at round 2; o7 and the contract closed.
7. ~~Close.~~ STATE.md regenerated, this plan struck; the push and the PR
   on the user's word.
8. ~~Release.~~ PR #64 merged at `17da7fd` once CI read green; the
   annotated tag `v0.16.0` there; the self-pin at `72e9b9e` on
   `session-55-release`, its PR merged once CI reads green. USAGE's `uv`
   line, run with `python -P` against the tag, installed 0.16.0 and read
   `specs/project-tree` ready-green.

Steps 1, 2, 7 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: ten, all the user's. (1) This plan and rulings 1
to 4; (2) the merge of PR #63; (3) the live run's verdict; (4) the release
text batch, with the test amendment; (5) o7's commit; (6) the fix commit;
(7) the push and the PR; (8) the merge; (9) the tag and its message; (10)
the self-pin PR.

Deferred, not this session:
- The history backfill first next session: one `progress done` per
  contract that shipped, checked against CHANGELOG first, so finished
  work stops reading `to do` above live work. With it, prerequisites 7 and
  8 (titles, feature documents).
- The tree's order: contracts sort by folder name and each opens down to
  its units, so finished features stand above live ones. A feature
  document candidate (finished features closed to one line, or live ones
  first), decided after the backfill.
- `taskcontract/__main__.py:85`: the `--follow` help still describes the
  0.15.0 pane; the file sits outside project-tree's scope.
- Two-Key advisories, wording: CHANGELOG's and ADR 0032's "a closed
  contract reads done whatever its verdicts read" omit the later-record
  limit; USAGE's evidence paragraph reads best as "after its own close";
  the no-red test covers section 9 only.
- Test gaps: no pane test checks that a `parts:` list without `evidence`
  hides an approval's seat; the row pattern in `tests/conftest.py` splits
  a plain name at its first ` [`.
- G1, the pilot's config line, and the rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on every
commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; every herdr probe closes the
panes it opens; the merge, the tag, the push and the PR on the user's word.
