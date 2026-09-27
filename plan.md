# Plan - Session 58 (2026-09-27) - G1's feature document

**Deliverable:** G1's feature document at `docs/features/<id>.md`, its
request half written through an interview and signed by the PO seat: the
first document written to ADR 0033. The solution half is the next
session's.

**Closed.** The deliverable is met: `docs/features/g1-requirements-spec.md`,
request half signed by the PO seat at r3.

## Steps

1. ~~Open.~~ Branch `session-58-g1-feature-document` from `af8c261`.
2. ~~The interview.~~ Nine questions, each section written before the
   next: the id and title; the statement; the description; the
   background, with four entries of existing behavior touched; five
   success criteria; seven non-goals; ten prerequisites; fifteen checks
   and four messages; fifteen new terms, with Finding, Rule and Ready
   check settled.
3. ~~The checks before signing.~~ No term clash; `component` and `venue`
   trip CL003, ceded at intake; 86 language findings, left to intake's
   rewrite (r2). Ready checks 1 to 8 read back: a fifth message (SC1.2),
   and SC1.1's review tied to the contract's revision.
4. ~~The PO seat signs.~~ r3.
5. ~~Close.~~ `STATE.md` regenerated; this plan struck; the commit, push
   and PR on the user's word.

Decisions this session: thirteen, all the user's. (1) The plan; Q1 to
Q9 (2 to 10); (11) the checks' three findings; (12) the signature;
(13) the commit, push and PR.

Deferred, not this session:
- G1's solution half, then intake.
- The tree's `gates/G0` item reads `to do` with no finding filed,
  whatever each feature's G0 verdict reads: decide what its status means.
- `feature-document`, prerequisite 7, and `STATE.md` Next actions 4 and
  5, carried unchanged.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; the push, the PR and the
merge on the user's word.
