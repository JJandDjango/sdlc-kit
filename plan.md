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

## Steps

1. Open. Branch `session-74-document-split` from `5252799`; this plan
   committed on its own.
2. Strike. The candidate list, shown in chat; the user strikes.
3. Notes. `NOTES_document-split_2026-10-06.md`: the team's feedback word
   for word, the three risks, the kept candidates and the open points.
   The interview's materials step (O5) reads it.
4. Interview, opening (O1 to O6): id, origin, title, seats, materials;
   the document lands as r1.
5. Interview, request half (Q1 to Q15), one question at a time.
6. Checks before signing (P1 to P7), then the PO seat's signature.
7. Close. `STATE.md` regenerated, this plan struck, one commit.

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
