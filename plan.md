# Plan - Session 50 (2026-09-24) - project-tree's feature document, ready for intake

**Deliverable:** `docs/features/project-tree.md` ready for `/sdlc intake`:
the request half signed by the PO seat, the solution half by the
engineer seat.

## Steps

1. Open: this plan, committed on `session-49-pane-spec`.
2. Q11, the terms: each drafted term read back one at a time, kept,
   reworded or struck on the user's word.
3. Readiness: the format's checks 1 to 8 read back; OPEN marks on the
   user's word; the PO seat signs the request half as a revision row.
4. The solution half, one question at a time: proposed solution (it
   answers the title OPEN), risks and cost.
5. The engineer seat signs the solution half.
6. Close: STATE.md regenerated, this plan struck, memory updated.
7. One push and one PR carrying sessions 49 and 50; merge by merge commit
   once CI reads green, on the user's word.

If context runs short, the session stops after step 3, and the solution
half opens session 51. Every step sits outside a contract unit, so the
pane shows none of them.

Decisions this session: four, all the user's: (1) this plan; (2) the PO
seat's signature on the request half; (3) the engineer seat's signature
on the solution half; (4) the push, the PR and its merge. The
interview's answers are the document's content, not counted here.

Deferred, not this session:
- Intake (`/sdlc intake docs/features/project-tree.md`): session 51's
  opener.
- G1: after project-tree is built, so the pane shows G1's conditions.
- The interview skill writes ADR 0026's template (the carried
  `feature-document` request).
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer, alone
in the final paragraph, on every commit that touches a non-free path; the
push, the PR and the merge on the user's word.
