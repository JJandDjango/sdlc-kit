# Plan - Session 48 (2026-09-23) - release 0.15.0

**Deliverable:** kit 0.15.0 released: PR #57 merged by merge commit, the
annotated tag `v0.15.0` at the merge, and the self-pin through its own PR,
merged once CI reads green.

## Steps

1. Open: this plan, shown in chat for the user's overview.
2. Merge PR #57 by merge commit. CI reads green at `96579dc` (`test` and
   `contracts`), and GitHub reports the merge clean.
3. Tag `v0.15.0` (annotated) at the merge commit; push the tag.
4. Cut `session-48-release` from main's new tip; commit this plan.
5. The self-pin: `.github/workflows/sdlc.yml` line 20 and `USAGE.md` line
   377 move from `@v0.14.0` to `@v0.15.0`, as `af9e587` did for 0.14.0.
   `CHANGELOG.md`'s heading already carries the date and the tag; a tag
   made after midnight moves its date too. Both paths sit in tree-view's
   scope, so the commit carries `Contract: tree-view`. `scope-check`
   against main's tip before the push.
6. The user restarts the tree pane (`w9:p8`), so it runs the released code.
7. Close: STATE.md regenerated, this plan struck, memory updated.
8. Push, open the PR, merge it by merge commit once CI reads green. CI's
   `contracts` job installs the kit from the new tag, so its green run
   proves the tag installs.

Every step sits outside a contract unit, so the pane shows none of them.
No Two-Key round: the self-pin changes two install refs and no code, and
CI's green run is its receipt.

Decisions this session: six, all the user's. (1) The deliverable; (2) this
plan; (3) the merge of PR #57; (4) the tag and its message; (5) the
self-pin commit; (6) the push, the PR and its merge.

Deferred, not this session:
- G1: its criteria review, before the pilot's M0 code. Session 49's
  deliverable, on a fresh context.
- The pilot's config line, in the engine's session.
- `.sdlc/config.yaml` still lists `plan.workflow.json` as a free path.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer, alone
in the final paragraph, on every commit that touches a non-free path; the
merge, the tag, the push and the PR on the user's word.
