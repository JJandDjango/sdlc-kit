# Session 138 plan: restart a stopped run, intake of the signed pair (backlog Next 24)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G0, the gate where `/sdlc intake` turns a signed pair of feature documents into a ready task contract.
**Feature:** run-restart: a stopped team run starts again in a fresh session from a stop record, not by `--resume`.
**Unit:** none built: this session writes the contract that names the five units `rs1` to `rs5`.

## 1. The deliverable

`specs/run-restart/contract.yaml`, validated ready-green by `/sdlc intake docs/features/run-restart.md`, with one `Ready:` row in each document's revision table.

## 2. Where this sits

Session 135 signed the requirements document `docs/features/run-restart.md` at r4 (PR #152). Session 137 signed the design document `docs/features/run-restart.design.md` at r4 (r5): 12 sections, 0 OPEN, five units built in order (PR #154, merged at `101e2ab`). Intake reads both now; G1 and the build of `rs1` follow in later sessions.

## 3. The steps

1. Branch `session-138-run-restart-intake` off main; this plan committed and pushed.
2. I1 to I2: the seat roster (ratified), then the pair read: OPEN marks, ready checks 1 to 8 and 11 to 15, each check of the requirements in exactly one unit, then the two signatures and staleness.
3. I3 to I4: `taskcontract new run-restart`, then the contract written from the pair: title, statement, non-goals, checks and terms from the requirements; scope, units, `done_means` word for word, order and tests from the design.
4. I5: the unit graph shown; each of the five units kept, changed or struck by the seats; the plan answers shown beside their sections; the seats recorded.
5. I6 to I7: the contract written, validated `--profile ready` to green (at most 5 loops), one `Ready:` row in each revision table.
6. Wrap: the backlog's Next 24 names G1 as its next step, `plan.md` out, the PR, draft until CI is green.

## 4. Where Claude stops for the user

At I5: every unit needs a human answer before the contract is final. At the PR's review. If the pair parks or stops at I2, Claude reports what stands and returns.

## 5. Where Claude goes on alone, and by what rule

The roster check, the pair read, the scaffold, the draft contract, the validate loop and the two `Ready:` rows follow the Intake flow word for word. The branch, the plan, the wrap and the draft PR: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

Only I5's: keep, change or strike for each unit, and which seats answered.

## 7. What could go wrong, already ruled

- A ready-check gap or an OPEN mark: the pair parks with one `Parked:` row in each table and no contract; each seat fixes its document through its own run.
- A seat changes a `done_means` at I5: the change goes to the design's Units row through the interview and a new signature; intake never rewords it.
- A TC010 or TC011 (a term the vocabulary lacks): fork the term or drop the ref, never ratify to turn green.

## 8. This session's cost, with its basis

No agent runs: intake runs in the main session. Reads: the two documents (about 31 KB) and the ready-check questions in `signing.md`, not the code they cite.

## 9. Not in this session

- G1 and the build of `rs1-stop-record`: later sessions.
- Next action 11 (e2's and e3's advisories) and the backlog's other open items.

## 10. Words

- **pair**: the requirements document (the PO seat's half) and the design document (the engineer seat's half) of one feature.
- **ready-green**: `taskcontract validate --profile ready` exits with no diagnostic.
- **`Ready:` row**: the revision-table row intake writes when the contract validates, naming the revision each seat signed.
- **`Parked:` row**: the row intake writes instead when something stands; no contract follows.
- **ready check**: one of the questions a document must answer before it is signed: 1 to 8 for the requirements, 11 to 15 for the design.
- **unit**: one buildable slice of the feature with its `done_means` and up to three acceptance-sketch entries.
- **seat**: one of the `intake-seat` term's values, a role that answers for a unit (PO, engineer).
