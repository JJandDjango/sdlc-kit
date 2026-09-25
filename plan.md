# Plan - Session 51 (2026-09-25) - project-tree to intake

**Deliverable:** contract `project-tree` at
`specs/project-tree/contract.yaml`, derived from the feature document's
r3: ready-green, zero at the language door, units o1 to o7 each answered
by seat `user`; the document stamped r4 with its Ready row.

**Closed.** The deliverable is met: contract `project-tree` at `1618daa`,
ready-green on the first pass, language door zero after one rewrite,
seven units each `confirmed_by: [user]`; r4 stamped; all sixteen kit
contracts ready-green, pytest 592 passed, scope-check green. PR #60
carries the session, merged once CI reads green.

Nothing before o1 is a contract unit, so the pane showed none of this
session's work.

## Steps

1. ~~Open: this plan, committed on branch
   `session-51-project-tree-intake`.~~ At `c614518`.
2. ~~Terms: the document's 22 new terms enter `specs/vocabulary/` as
   drafts; the user ratifies them (G0.2). Their own commit.~~ At
   `ac19ee4`: 40 terms; the dictionary ceded eight words (CL003); `verdict`
   says diagnostics.
3. ~~Intake, I1 to I6.~~ Every unit kept; the engineer seat added
   `skills/sdlc/init.py` and `.github/workflows/sdlc.yml` to scope.
4. ~~Validate.~~ Ready-green on the first I7 pass; the language door zero
   after one rewrite.
5. ~~r4, by hand this once.~~ The Ready row and the status line;
   prerequisite 9 kept at 15, the row noting the 16th.
6. ~~Commit the contract and r4.~~ At `1618daa`.
7. ~~Close: STATE.md regenerated, this plan struck, memory updated; the
   push, the PR and its merge on the user's word.~~ PR #60.

Decisions this session, six, all the user's: (1) this plan; (2) ratify
the 22 terms, with the `verdict` edit; (3) keep all seven units; (4) the
scope change; (5) r4 and prerequisite 9's count; (6) the push, the PR and
the merge.

Deferred, not this session:
- The build, o1 to o7: about three sessions; o5 and o6 need Textual in
  the test env.
- G1, after project-tree ships.
- ADR 0029's appendix copy and Gherkin for project-tree, with
  `feature-document`'s open question.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer, alone
in the final paragraph, on every commit that touches a non-free path; the
push, the PR and the merge on the user's word.
