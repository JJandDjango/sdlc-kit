# Plan - Session 56 (2026-09-26) - history backfill and titles

**Deliverable:** prerequisites 8 and 9 of `docs/features/project-tree.md`:
a close record for each shipped contract that reads `to do`, and a
one-line `title` in all 16 contracts. The tree then shows finished work as
done and every feature by its plain name.

**Rulings at plan review** (the user's; Claude's recommendation first):

1. Scope is prerequisites 8 and 9. Prerequisite 7 (feature documents for
   the older contracts) parks: each document needs its own interview.
   `STATE.md` numbered these 7 and 8; the feature document's numbers
   stand.
2. Close 12 of the 13, each matched unit by unit to a CHANGELOG release
   (the map below). `glossary-alias-disjointness` stays `to do`: VT010
   appears only in its own contract, so it never shipped.
3. A close record names today's `HEAD`, not the release commit: the
   writer takes no other, and CHANGELOG carries the release. The records
   stay local (`.sdlc/progress/` is gitignored, ADR 0031).
4. Claude drafts the 16 titles from each contract's intent;
   `project-tree`'s comes from its document's title line, as intake would
   copy it. The user approves them in one batch shown in chat, then the
   commits: one per contract, each with its `Contract:` trailer.
5. No Two-Key: no code changes. The receipts are each contract's ready
   validation, the tree, and CI's `contracts` job on the PR.

**The map** (contract, release):

| Contract | Release |
|---|---|
| `vocabulary-layer` | 0.3.0 |
| `distribution-reconciliation` | 0.4.0 |
| `dotnet-profile-g0` | 0.5.0 |
| `dotnet-profile-g3` | 0.6.0 |
| `dotnet-profile-g4` | 0.7.0 |
| `operator-layer` | 0.8.0 |
| `controlled-language` | 0.9.0 |
| `unit-dag` | 0.11.0; its intake review with 0.12.0's I5 |
| `intake-seats` | 0.12.0 |
| `playbook-guardrails` | 0.13.0 |
| `spec-interview` | 0.13.0 |
| `g0-declaration` | 0.14.0 |
| `glossary-alias-disjointness` | not shipped |

**Closed.** The deliverable is met: 12 closes recorded at `4986614`;
16 titles at `a55fb7e` to `0d392ad`, each ready-green; the tree prints 15
features `[done]`, `glossary-alias-disjointness` `[to do]`, and no feature
`(no title)`.

## Steps

1. ~~Open.~~ Branch `session-56-backfill` from `7767767`; the plan at
   `4986614`.
2. ~~The closes.~~ `progress done` for the 12; each reads `[done]` at
   `4986614`.
3. ~~The titles.~~ Approved in one batch; one commit each by a scratch
   script; all 16 ready-green.
4. ~~Close.~~ `STATE.md` regenerated, this plan struck; the push and the
   PR on the user's word; the merge once CI reads green.

Decisions this session: four, all the user's. (1) The scope (item 1);
(2) this plan and rulings 1 to 5; (3) the title batch and its commits;
(4) the push and the PR.

Deferred, not this session:
- Prerequisite 7: feature documents for the 13 older contracts.
- The tree's order (finished features closed to one line), a feature
  document candidate.
- G1, and `STATE.md` Next actions 5 and 6, carried unchanged.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer, alone
in the final paragraph, on every contract commit; the push, the PR and the
merge on the user's word.
