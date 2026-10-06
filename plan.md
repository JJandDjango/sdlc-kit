# Plan - Session 75 (2026-10-06) - document-split, the solution half

**Deliverable:** the solution half of `docs/features/document-split.md`,
written through the interview's steps S1 to S11, checked by E1 to E5,
and signed by the engineer seat at E7.

The feature: the one feature document becomes two, a requirements
document the PO seat signs and a design document one engineer seat
writes and signs alone. Its request half is signed at r4 (session 74,
PR #86 at `5553193`). The format change is permanent; the one-time part,
splitting an existing combined document, is a non-goal (G1's is split by
hand). This document is the last one written combined.

Approvals: this plan, each batch of proposed text, the signature, each
commit, the push, the PR and the merge stay on the user's word. The
user holds both seats (`seats.po: user`, `seats.engineer: user`).

## Steps

1. Open. Branch `session-75-document-split` from `5553193` (done). The
   plan's commit follows the user's overview.
2. Materials. Read the document's request half end to end, then only
   the code each section's facts come from: the interview's five flows
   and `SKILL.md`, its templates, intake's flow, and the tree's reading
   of a feature before intake. `feature-document.md`'s solution half is
   the shape to match. The flows run from `skills/` here: the installed
   plugin holds `40eb767`, not main's tip, and `git diff --stat v0.18.0
   HEAD -- skills/` prints nothing.
3. S1 Scope and S2 Out of scope, one batch. A refusal that turns out to
   be a thing not built goes to Non-goals: that write lands in the
   signed request half, adds a text row, and asks the PO seat to sign
   again.
4. S3 Interfaces, one batch. The seat's open calls land here: the
   pair's file names and paths; one state file or two; how a design run
   is started; each output kind drawn with its edges (ready check 12).
5. S4 Sources and S5 Constraints, one batch. One Sources row per fact a
   check names, with the winner when two sources disagree (ready check
   11).
6. S6 Units and S7 Order, one batch. Each unit: its checks, its done
   means in one sentence, its tests by check id and kind, its
   retirements or "none". Every check stands in one unit; a unit holds
   at most three sketches; the release unit is named, with its paths in
   Scope.
7. S8 Risks and cost, S9 Decisions and open questions, S10 Links out,
   S11 Notes, one batch. Open for S9: which seat confirms each unit at
   intake, who the engineer seat tells when a case turns to yes during
   the build, and whether combined documents are in flight on the
   second machine.
8. E1 to E5, the checks before signing. The draft check now reads each
   unit's `done_means`; Scope is checked against the release unit's
   paths; ready checks 11 to 14 are read; one `Measured:` row.
9. E6 and E7. The gaps reported in one block; the seat signs or names a
   section to go back to. The signature writes two rows, and the state
   file reads `phase: output`, `next: W1`.
10. Close. `STATE.md` regenerated, this plan struck; the commit, the
    push, the PR and the merge wait on the user's word.

The session's practice, as in session 74: each batch is proposed text
with its decision count said first, and one reply covers it. Five
batches and the signature: about seven replies.

Deferred, not this session:
- The ADR that amends 0029 and 0033 to 0036; the nine terms and five
  amendments, ratified in their own commit; intake, with the draft
  check's 179 findings rewritten there; the build, as kit 0.19.0.
- G1's solution half, by hand from the two NOTES files, and G1's
  document split by hand into a pair (SC4.3).
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer,
alone in the final paragraph, on every commit that touches a non-free
path; no spawn opens a window.
