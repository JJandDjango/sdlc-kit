# Plan - Session 48 (2026-09-23) - release 0.15.0

**Deliverable:** kit 0.15.0 released: PR #57 merged by merge commit, the
annotated tag `v0.15.0` at the merge, and the self-pin through its own PR,
merged once CI reads green.

**Closed at PR #58.** PR #57 merged at `fdd6fe2`, tagged `v0.15.0` there;
the self-pin at `7a453e7`. PR #58 carries the plan, the self-pin and this
wrap, and merges once CI reads green, on the user's word given at open.

## Steps

1. ~~Open: this plan, shown in chat for the user's overview.~~ At
   `f1c6fa3`.
2. ~~Merge PR #57 by merge commit.~~ At `fdd6fe2`; CI green on main there.
3. ~~Tag `v0.15.0` (annotated) at the merge commit; push the tag.~~
4. ~~Cut `session-48-release` from main's new tip; commit this plan.~~
5. ~~The self-pin.~~ At `7a453e7`: `.github/workflows/sdlc.yml` and
   `USAGE.md` read `@v0.15.0`; scope-green from `fdd6fe2`. USAGE's `uv`
   line, run as written, installs `v0.15.0` and reads tree-view
   ready-green.
6. The user restarts the tree pane (`w9:p8`), so it runs the released code.
   STATE.md carries it.
7. ~~Close: STATE.md regenerated, this plan struck, memory updated.~~
8. Push, open the PR, merge it by merge commit once CI reads green. Pushed
   and opened as #58 before the close, so STATE names its number; the
   merge follows CI's green run on the wrap.

Every step sits outside a contract unit, so the pane shows none of them.
No Two-Key round: the self-pin changes two install refs and no code, and
CI's green run is its receipt.

Decisions this session: six, all the user's, all yes in one word: (1) the
deliverable; (2) this plan; (3) the merge of PR #57; (4) the tag and its
message; (5) the self-pin commit; (6) the push, the PR and its merge.

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
