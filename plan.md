# Plan - Session 65 (2026-09-30) - feature-document's request half

**Deliverable:** `docs/features/feature-document.md`, its request half
written through an interview and signed by the PO seat, in the format
ADR 0029 ratified and ADRs 0033 to 0035 amended. The source is the
untracked `REQUEST_feature-document_2026-09-18.md` (r1, typed by hand):
each section is asked again, never copied. The solution half is the next
session's.

**Closed.** The deliverable is met: `docs/features/feature-document.md`,
request half signed by the PO seat at r3 (r4). The tree reads it `doing`,
request half done at r3, solution half to do.

## Steps

1. ~~Open.~~ Branch `session-65-feature-document` from `e833283`.
2. ~~The interview.~~ Nine questions, each section written before the
   next: the id and title; the statement; the description; the
   background, with seven entries of existing behavior touched; five
   success criteria; nine non-goals; eight prerequisites; fourteen checks
   and six messages; fifteen new terms, with Stale amended. The five
   questions at `a800c34:STATE.md` are answered in Decisions and open
   questions.
3. ~~The checks before signing.~~ No term clash; `check` and `tag` trip
   CL003, ceded at intake; 174 language findings, left to intake's
   rewrite; the seven existing-behavior entries hold (r2).
4. ~~Ready checks 1 to 8.~~ Three fixes: SC4 one sentence, entry 7's
   source, intake's roster message in full (r3).
5. ~~The PO seat signs.~~ r4 signs r3.
6. ~~Close.~~ `STATE.md` regenerated; this plan struck; the commit, push
   and PR on the user's word.

Decisions this session: thirteen, all the user's. (1) This plan; (2) to
(10) Q1 to Q9; (11) the checks' findings and the three fixes; (12) the
signature; (13) the commit, push and PR.

Deferred, not this session:
- The solution half (session 66), then intake, the build and the 0.18.0
  release. It opens with the OPEN in Decisions: `taskcontract/tree.py:196`
  counts a `Parked:` row as a text change.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; the push, the PR and the
merge on the user's word.
