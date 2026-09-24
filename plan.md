# Plan - Session 49 (2026-09-23) - the request from the tree sketch

**Deliverable:** a request written from the user's tree sketch (engine
session 10, 2026-09-21), not from tree-view's r1: each contract's gates
open into their conditions, each with its status and findings, and the
pane shows the whole outline instead of folding it. Done when the user's
strike is recorded as r2.

## Steps

1. Open: this plan, shown in chat for the user's overview.
2. Fast-forward local `main` to `7c79ba3` (PR #58's merge), cut
   `session-49-gate-outline` from it, and commit this plan.
3. Map the sketch onto the kit's sources, reading only what r1 needs: G0.1
   to G0.3 and the checks behind each (`docs/gates/G0-planning-intake.md`,
   the validator); G1's conditions (`docs/gates/G1-requirements-spec.md`);
   what a finding's `gate:` field can name; the ADR 0031 rulings the
   request keeps or amends; the fold in `taskcontract/tree_view.py`.
4. Write r1 in ADR 0029's format as `REQUEST_gate-outline_2026-09-23.md`
   (untracked, in the kit root; the id is a proposal). The request half
   only: features as candidates to strike, OPENs for what the sources
   cannot settle. Its Background opens with a trace table: each element of
   the sketch, and whether r1 offers it, 0.15.0 built it, or an earlier
   ruling removed it (named, and the user's to reopen).
5. Show r1 in chat. The user strikes features and answers the OPENs in one
   message.
6. Record r2: the strike in the revision table, signed by the PO seat.
7. Close: STATE.md regenerated, this plan struck, memory updated.
8. Push, open the PR, and merge it by merge commit once CI reads green, on
   the user's word.

Every step sits outside a contract unit, so the pane shows none of them.

Decisions this session: three, all the user's: (1) this plan; (2) the
strike, at step 5; (3) the push, the PR and its merge.

Deferred, not this session:
- r3 (the checks and the solution half) and intake: session 50.
- G1: after this request is built, so the pane shows G1's conditions as
  they land.
- The backfill of the 13 earlier contracts, so the pane's statuses read
  true.
- `.sdlc/config.yaml` still lists `plan.workflow.json` as a free path.
- The rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer, alone
in the final paragraph, on every commit that touches a non-free path; the
push, the PR and the merge on the user's word.
