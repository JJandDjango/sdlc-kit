# Plan - Session 17 (2026-07-29) - EXECUTED

Ratified by the user in-session: sequence + feature set (F4 struck).
All four steps ran to completion: PR #6 (ratification, merged),
PR #7 (distribution reconciliation, merged, tag v0.4.0), PR #8
(self-pin, merged - CI proved the pinned install). Suite 85 -> 95;
audit clean; glossary 12/12 ratified; v0.3.0 + v0.4.0 on origin.

## Steps

1. **Ratification PR** - commit the 7 glossary flips on
   `session-17-vocab-ratification`, push, open the PR (the merge is
   the interim approval record per docs/vocabulary.md), CI green,
   merge, update local main.
2. **Operational pair** (no new capability):
   a. Verify the first GitHub CI run of the vocab-check step - DONE
      before commit: runs 30418987462/30418987423 green on main
      2026-07-29T03:13Z; the 0.3.0 distribution loop is confirmed.
   b. Update the stale /sdlc plugin cache (predates session 16;
      mis-flags the glossary as an orphan).
3. **Intake: distribution reconciliation loop** - `/sdlc intake` on
   the ratified set:
   - F1: pin the scaffolded install ref to a release tag; tagging
     discipline on version bumps.
   - F2: CHANGELOG.md materialized, backfilled 0.1.0-0.3.0;
     delta-note house rule per schema version bump.
   - F3: `/sdlc update` day-2 command - report-only scaffold drift,
     consented per-file apply.
   - F4 (PyPI publish): struck - stays deferred behind its trigger.
   - entities: let TC010 fork accretion-born vocabulary tasks if the
     contract names unresolved terms (consumer, scaffold, ...).
4. Implement the kept set, gated by the ready-green contract.

Carried user one-liners (out of scope, unchanged): README.md tree
line, CONVENTIONS.md schema ref, .vscode/settings.json raw URL still
name the old root schemas/ path.

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos.
