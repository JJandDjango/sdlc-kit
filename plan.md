# Plan - Session 51 (2026-09-25) - project-tree to intake

**Deliverable:** contract `project-tree` at
`specs/project-tree/contract.yaml`, derived from the feature document's
r3: ready-green, zero at the language door, units o1 to o7 each answered
by seat `user`; the document stamped r4 with its Ready row.

Where things stand: `docs/features/project-tree.md` r3 is signed by both
seats (`a18ea25`); PR #59 merged at `7f2b5c1`; main is clean. Nothing
before o1 is a contract unit, so the pane shows none of this session's
work.

## Steps

1. Open: this plan, committed on branch `session-51-project-tree-intake`.
2. Terms: the document's 22 new terms enter `specs/vocabulary/` as
   drafts; the user ratifies them (G0.2), so intake can declare them in
   `entities`. Their own commit.
3. Intake, I1 to I6 (`/sdlc intake docs/features/project-tree.md`): the
   seat roster, id `project-tree`, the scaffold, the contract from r3
   with no `title` (o2 adds the field; TC005 otherwise); the unit graph
   shown and each unit answered; the three plan answers read from the
   solution half (Scope, Sequencing, Units) for the engineer seat to keep
   or change.
4. Validate: `--profile ready` looped to green (cap 5); the language
   door, filtered to `project-tree`, looped to zero.
5. r4: the revision table gains `r4: Ready: ... derived from r3 ...`, by
   hand this once (o3 teaches intake to write it).
6. Commit the contract and r4, once all 16 contracts read ready-green and
   pytest and scope-check pass.
7. Close: STATE.md regenerated, this plan struck, memory updated; the
   push, the PR and its merge on the user's word.

Decisions this session, six, all the user's: (1) this plan; (2) ratify
the 22 terms; (3) keep, change or strike each of o1 to o7, in two asks;
(4) keep or change the three plan answers; (5) prerequisite 9's count;
(6) the push, the PR and the merge.

Prerequisite 9 names "the 15 existing contracts"; project-tree's own
contract becomes a 16th with no title. Recommendation: leave r3's count,
note it in the Ready row, and let the backfill title every contract that
lacks one. An edit after derivation marks the contract stale against its
own document; an edit before it costs a re-sign for one number.

Deferred, not this session:
- The build, o1 to o7: about three sessions; o5 and o6 need Textual in
  the test env.
- G1, after project-tree ships.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer, alone
in the final paragraph, on every commit that touches a non-free path; the
push, the PR and the merge on the user's word.
