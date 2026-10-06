# Plan - Session 74 (2026-10-06) - document-split, the request half

**Deliverable:** the feature document for `document-split` (a working
id, set at O1), written through `/sdlc:product-specification-interview`,
with its request half signed by the PO seat.

The feature: the one feature document becomes two, a requirements
document the PO seat signs and a design document one engineer seat
writes and signs alone.

Origin: the user's team, 2026-10-05, on the process 0.18.0 proposes. The
PO team reads only the request. Other engineers see a design before the
PR only on one of four triggers: an ambiguity, more than one solution, a
solution unconventional to the codebase, a change to a public contract.
The final PR review by another engineer stays.

Approvals: the plan, the struck list, each interview answer, the
signature, each commit, the push, the PR and the merge stay on the
user's word.

**Closed.** The deliverable is met: `docs/features/document-split.md`
stands at r4, `Signed: request half. The PO seat signs r3`, with five
criteria, 13 checks, 13 scenarios, nine new terms and five amended, and
no OPEN. The draft check's 179 findings are left to intake's rewrite.

## Steps

1. ~~Open.~~ Branch `session-74-document-split` from `5252799`; the plan
   at `0f76de8`.
2. ~~Strike.~~ Candidates 1 to 9 kept; 10 to 12 moved to later features.
3. ~~Notes.~~ `NOTES_document-split_2026-10-06.md`, the team's feedback
   word for word. The user's closing remark is left out: the repo is
   public.
4. ~~Interview, opening.~~ Run from the repo's skill folder, which
   equals the `v0.18.0` tag: the installed plugin was stale at `36c0720`
   and was updated mid-session. The five answers in one reply; r1.
5. ~~Interview, request half.~~ Q1 to Q15 in six replies, each on
   proposed text. Q5 gained three entries read from the code; Q8 folded
   the nine candidates into five criteria; Q11's 13 checks carry seven
   readings, recorded under Decisions and open questions.
6. ~~Checks before signing.~~ The draft check found 179, as
   `feature-document`'s 174. Two gaps (entry 8 against its source, two
   prerequisites with no owner) closed on the seat's word before the
   `Measured:` row, r2. The finishing row r3; the signature r4.
7. ~~Close.~~ `STATE.md` regenerated, this plan struck. The commit, the
   push, the PR and the merge wait on the user's word.

Decisions this session: thirteen, all the user's. (1) Take the team's
lifecycle, and build it ahead of G1's solution half; (2) the push of
`session-73-wrap`; (3) the plan and the struck list; (4) the opening's
five answers; (5) the statement; (6) the description and the background;
(7) the nine entries of existing behavior; (8) the five criteria; (9)
the non-goals; (10) the prerequisites and the 13 checks with their seven
readings; (11) the messages, the terms and SC1.3's addition; (12) the 13
scenarios; (13) the two fixes and the signature. Claude's, each told to
the user: the plan's commit, the Background worded without quoting, the
closing remark cut from the notes, and `jsonschema` installed into
Python 3.14 so the draft check could run.

Deferred, not this session:
- The solution half (S1 to S11, E1 to E7), intake and the build.
- G1's solution half: behind this feature, since it would be written in
  the format this feature replaces.
- The PR and the merge of `session-73-wrap` (pushed 2026-10-06).
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer,
alone in the final paragraph, on every commit that touches a non-free
path; no spawn opens a window.
