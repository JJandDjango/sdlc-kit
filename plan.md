# Session 168 plan: G1 for session-loop (backlog Next 30)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G1, the gate between a ready contract and a unit's first task: schemas linted, models checked, the requirements reviewed by a person.
**Feature:** session-loop: sessions that wrap and restart themselves until a human is needed.
**Unit:** none built: this session passes G1 so `l1-loop-files` can start.

## 1. The deliverable

`python -m taskcontract g1-check session-loop` exits 0, with the G1.1, G1.2 and G1.3 records committed on this branch.

## 2. Where this sits

Sessions 163 to 167 wrote the requirements (r9, signed r10), the design (r10, signed r11) and the contract, ready-green at lang-check zero (PR #173, merged at `6a5f4f0`). The `Ready:` rows are requirements r11 and design r12. G1 is the last step before `l1-loop-files`' approve-tests. At session start `g1-check` reads: G1.1 done, G1.2 done, G1.3 to do.

## 3. The steps

1. This plan committed and pushed to `session-168-session-loop-g1`.
2. R1 and R2 (done at session start): the contract is ready-green, G1 is active, both declarations stand.
3. R3 and R4: `g1-record lint` and `g1-record model` record G1.1 and G1.2.
4. R5: the 11 items of G1.3, one at a time, read against the requirements r9 and the design r10. Claude shows a one-line reading for each, drawn from the pair; the user answers checked or unchecked.
5. R6: the user's name, seat and word to sign; then `g1-record review`.
6. R7: `g1-check`; the records committed.
7. Wrap: the backlog's Next 30 names `l1-loop-files` as next, `plan.md` out, push, PR.

## 4. Where Claude stops for the user

At each of the 11 items (step 4), at the signature (step 5), then at the PR review.

## 5. Where Claude goes on alone, and by what rule

The plan, the lint and model records, `g1-check`, the commits, the push and the wrap: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The review's answers and signature are the user's alone (the G1 flow's rule).

## 6. Rulings needed

The 11 answers and the signature, nothing else.

## 7. What could go wrong, already ruled

- An item is unchecked: the review records it and G1 reads not passed; the fix is a new revision of the named document and a re-intake, in a later session.
- `g1-record lint` or `model` exits 1: the record holds the failure; Claude reports it and goes on, as R3 and R4 say.
- A reading of Claude's contradicts the pair: the user's answer stands; the reading is a draft.

## 8. This session's cost, with its basis

No agent runs. The main session reads the pair once (about 34 KB, near 9K tokens) to draft the readings. No local suite run: the change is three record files, and CI runs the suite on the PR.

## 9. Not in this session

- The build of `l1-loop-files` and the later units.
- The `needs-ruling` label: at session start `gh label list` on `JJandDjango/sdlc-kit` shows no such label; the user's prerequisite, before l1's first live run.
- session-loop-sidebar (Next 31) and the backlog's other open items.

## 10. Words

- **G1.1**: the boundary schemas in scope, linted; **G1.2**: the model of each hard core in scope (a component whose bugs a model checker must catch), checked.
- **G1.3**: a person's review of the requirements on 11 items, signed by name and seat.
- **`g1-record`**: the one writer of G1's records; **`g1-check`**: reads them and gives the verdict, writing nothing.
- **ready-green**: `taskcontract validate --profile ready` exits with no diagnostic.
- **`Ready:` row**: intake's line in each document's revision table, naming the revision the contract came from.
- **seat**: the role a signer holds, one value of the `intake-seat` term (such as the PO seat or the engineer seat).
