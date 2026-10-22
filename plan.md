# Plan - session 111

**Deliverable:** a ready-green contract for small-session-flow at `specs/small-session-flow/contract.yaml`, derived by `/sdlc intake` from the signed pair (PRs #130 and #131, merged at `3c11093`). No code, no agent edits.

## Steps

1. Branch `session-111-flow-intake` off `main` at `3c11093`.
2. I1: check the `intake-seat` roster is ratified (`python -m taskcontract vocab-list`).
3. I2: read the pair for refusals (OPEN marks, ready-check gaps, check-to-unit assignment) and stops (signatures, staleness). A refusal parks the pair with one `Parked:` row in each table and ends the deliverable.
4. I3-I4: scaffold the contract and author it from the two documents, each field from its one source, each `done_means` copied word for word.
5. I5: render the unit graph; you answer each unit (keep, change, strike) and name its seats.
6. I6-I7: write the confirmed contract, loop `validate --profile ready` to green (cap 5), then add one `Ready:` row to each document's revision table.
7. Commit, push, open the PR; the branch's last commit takes `plan.md` out.

## Deferred (one line each, read at close)

- Items 1 to 9 build after intake, one item per session, retry cap and session rule first.
- G2 feature list and G1 open edges: the hold lifts when the engine cursor passes unit 1 (it read 10.1 on 2026-10-21); confirm with `status.py`, then lift.
- Backlog Next 6: first real use of `prove.py` and `receipts.py`.
- Park branch `session-108-park-g2-g1` has no PR.
- Items 4 to 7 change agent definitions: they go through that approval channel.
- Stale local branches `session-109-flow-feature-doc` and `session-110-flow-design-doc`: both merged, delete at close.
