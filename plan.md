# Session 166 plan: session-loop, intake of the signed pair (backlog Next 30)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G0, the gate where `/sdlc intake` turns a signed pair of feature documents into a ready task contract.
**Feature:** session-loop: sessions that wrap and restart themselves until a human is needed.
**Unit:** none built: this session writes the contract that names the three units `l1` to `l3`.

## 1. The deliverable

`specs/session-loop/contract.yaml`, validated ready-green by `/sdlc intake docs/features/session-loop.md`, with one `Ready:` row in each document's revision table.

## 2. Where this sits

Session 164 signed the requirements document `docs/features/session-loop.md` at r4 (PR #171). Session 165 signed the design document `docs/features/session-loop.design.md` at r4 (r5): 0 OPEN, three units built in order, `l1-loop-files`, `l2-loop-launcher` (in `E:\herdr-sdlc`) and `l3-loop-rules` (kit 0.23.0) (PR #172, merged at `94d2ee8`). Intake reads both now; G1 and the build of `l1` follow in later sessions.

## 3. The steps

1. Branch `session-166-session-loop-intake` off main at `94d2ee8`; this plan committed and pushed.
2. I1 to I2: the seat roster, then the pair read: OPEN marks, the ready checks, each check of the requirements in exactly one unit, the two signatures and staleness.
3. I3 to I4: `taskcontract new session-loop`, then the contract written from the pair: title, statement, non-goals, checks and terms from the requirements; scope, units, `done_means` word for word, order and tests from the design.
4. I5: the unit graph shown; each of the three units kept, changed or struck by the seats; the seats recorded.
5. I6 to I7: the contract validated `--profile ready` to green (at most 5 loops), one `Ready:` row in each revision table; new terms ratified and the contract's prose lang-checked, as session 138 did.
6. Wrap: the backlog's Next 30 names G1 and `l1` as its next step, `plan.md` out, the PR, draft until CI is green.

## 4. Where Claude stops for the user

At I5: every unit needs a human answer before the contract is final. At the PR's review. If the pair parks or stops at I2, Claude reports what stands and returns.

## 5. Where Claude goes on alone, and by what rule

The roster check, the pair read, the scaffold, the draft contract, the validate loop and the two `Ready:` rows follow the Intake flow word for word. The branch, the plan, the wrap and the draft PR: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

Only I5's: keep, change or strike for each unit, and which seats answered.

## 7. What could go wrong, already ruled

- A ready-check gap or an OPEN mark: the pair parks with one `Parked:` row in each table and no contract; each seat fixes its document through its own run.
- A seat changes a `done_means` at I5: the change goes to the design's Units row through the interview and a new signature; intake never rewords it.
- `l2-loop-launcher` builds in `E:\herdr-sdlc`, outside this repository: the contract names it as the design does; if the contract's scope cannot name another repository's files, Claude records the gap against the design and carries on with the kit's own scope.
- A TC010 or TC011 (a term the vocabulary lacks): fork the term or drop the ref, never ratify to turn green.

## 8. This session's cost, with its basis

No agent runs: intake runs in the main session. Reads: the two documents (about 25 KB together, by their line counts) and the intake flow's pages, not the code they cite.

## 9. Not in this session

- G1 and the build of `l1-loop-files`: later sessions.
- The `needs-ruling` label on the remote (the user's prerequisite, before l1's first live run).
- session-loop-sidebar (Next 31) and the backlog's other open items.

## 10. Words

- **pair**: the requirements document (the PO seat's half) and the design document (the engineer seat's half) of one feature.
- **ready-green**: `taskcontract validate --profile ready` exits with no diagnostic.
- **`Ready:` row**: the revision-table row intake writes when the contract validates, naming the revision each seat signed.
- **`Parked:` row**: the row intake writes instead when something stands; no contract follows.
- **ready check**: one of the questions a document must answer before it is signed.
- **unit**: one buildable slice of the feature with its `done_means` and up to three acceptance-sketch entries.
- **seat**: a role that answers for a unit (PO, engineer); here the user holds both.
- **G1**: the gate after intake that reviews the contract before any unit is built.
