# Plan - Session 59 (2026-09-27) - The pane's top level

**Deliverable:** one feature document at `docs/features/<id>.md`, both
halves signed, ready for intake. It closes two gaps in project-tree's
requirements: a gate item's status (`gates/G0` reads `to do` whatever each
feature's G0 verdict reads) and a feature that has a document but no
contract yet (`g1-requirements-spec` is absent from the pane).

## Steps

1. ~~Open.~~ Branch `session-59-tree-first-level` from `6ca8492`.
2. ~~The request half.~~ Nine questions: id and title; statement;
   description; background with six entries of existing behavior
   touched; four success criteria; eight non-goals; seven prerequisites;
   twelve checks and two messages; eleven new terms and Feature's new
   definition.
3. ~~The checks before signing, request half.~~ No term clash; `half` and
   `intake` trip CL003, ceded at intake; 90 language findings, left to
   intake's rewrite (r2). Ready checks 1 to 8 read back with no fix.
4. ~~The PO seat signs.~~ r3, restated as `r4: Signed: request half`.
5. ~~The solution half.~~ Six questions: the signature form (Q10);
   Interfaces with examples and edges; Sources; Scope, Out of scope and
   Constraints; four units and their order; Risks and cost, with the worth
   decision to build this before G1's solution half.
6. ~~The checks before signing, solution half.~~ Scope green; no new
   term; ready check 11 found two missing Sources rows, added (r5, r6).
7. ~~The engineer seat signs.~~ `r7: Signed: solution half`.
8. Close. `STATE.md` regenerated; this plan struck; the commit, push and
   PR on the user's word.

**Closed** once step 8's commit lands: the deliverable is met,
`docs/features/tree-first-level.md` signed on both halves.

Decisions this session: twenty-one, all the user's. (1) Both gaps in
scope; (2) the plan; Q1 to Q9 (3 to 11); (12) the request half's
checks and signature; Q10 to Q15 (13 to 18); (19 to 21) the Sources
fix, the r4 restatement, the engineer's signature. The commit, push and
PR come next.

Deferred, not this session:
- Intake and the build of this document: ADR 0034, the terms, G1's
  backfill row, then t1 to t4.
- G1's solution half, then its intake.
- `feature-document`, prerequisite 7, and `STATE.md` Next actions 5 and
  6, carried unchanged.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; the push, the PR and the
merge on the user's word.
