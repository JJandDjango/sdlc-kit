# Plan - Session 49 (2026-09-23) - the pane's feature document, from the beginning

**Deliverable:** the request half of the pane's feature document
(sections 1 to 12 of the format ADR 0029 ratified, written out in
`NOTES_feature-document_2026-09-18.md`), written with the user from the
beginning, one question at a time, in the user's words. Done when the PO
seat signs it, the format's checks 1 to 8 passing or marked OPEN on the
user's word.

**Replanned at the user's word.** The first plan (`2311a17`) wrote a
request from the user's 2026-09-21 sketch; its r1,
`REQUEST_gate-outline_2026-09-23.md`, showed the drift a sketch invites.
The pane work goes back to the beginning: a feature document before any
build. The kit's interview skill still asks ADR 0026's questions (the
`feature-document` request moves it), so the interview runs by hand in
the ratified format's order. r1 stays untracked, as material.

**Stopped at the user's word, 2026-09-24,** at Q11 (terms). The
deliverable is not reached: session 50 resumes the interview at the
drafted terms, marked OPEN in the document's appendix, then readiness.

## Steps

1. ~~Replan: this plan; rename the branch `session-49-pane-spec`; commit
   this plan.~~ At `979f2f0`.
2. ~~Opening: the feature's id and title, then the document's path.~~ Id
   `project-tree` (`pane-view` is the closed 0.15.0 contract); the
   document at `docs/features/project-tree.md`, tracked.
3. The request half, one question at a time in the format's order.
   ~~Statement; description; background and existing behavior touched;
   success criteria; non-goals; prerequisites; acceptance criteria, with
   their checks and verbatim error messages.~~ Terms: drafted, OPEN,
   session 50.
4. Readiness: the format's checks 1 to 8, read back; OPEN marks on the
   user's word; the PO seat signs the request half. Session 50.
5. ~~Close: STATE.md regenerated, this plan struck, memory updated; the
   interview's friction recorded.~~
6. Push, open the PR, and merge it by merge commit once CI reads green, on
   the user's word. Waits for that word.

The document is the resume point: if the session ends first, session 50
resumes at its first unwritten section. Every step sits outside a
contract unit, so the pane shows none of them.

Decisions this session: three, all the user's: (1) this plan; (2) the PO
seat's signature on the request half, with any OPEN marks; (3) the push,
the PR and its merge. The interview's answers are the document's content,
not counted here.

Deferred, not this session:
- The solution half (proposed solution, risks and cost), signed by the
  engineer seat, then intake: session 50.
- G1: after the pane is built, so the pane shows G1's conditions.
- The interview skill writes ADR 0026's template (the carried
  `feature-document` request).
- The backfill of the 13 earlier contracts, so the pane's statuses read
  true.
- `.sdlc/config.yaml` still lists `plan.workflow.json` as a free path.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer, alone
in the final paragraph, on every commit that touches a non-free path; the
push, the PR and the merge on the user's word.
