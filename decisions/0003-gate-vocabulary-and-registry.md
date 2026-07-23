# 3. Define gates as phase venues with attached conditions

Status: accepted
Date: 2026-07-22

## Context
The SDLC gate map (`HANDOFF_gate-architecture_2026-07-22.md` section 5) packs
several distinct checks into each phase row - phase 4 alone carries nine. Before
conditions
can be specified and enforced, the unit of identity must be fixed: is "a gate"
each individual check, or the blocking venue a phase's checks attach to?
Downstream artifacts (CI stage names, Verifier checks, traceability scripts)
will reference these identities; renaming later is costly.

## Decision
A **gate** is one row of the gate map: the blocking enforcement venue for a
phase. A **condition** is an individual check attached to a gate. Gates carry
stable IDs `G0`-`G10` (handoff numbering, which merged the original addendum:
old 5.5 UAT -> 6, subsequent phases shifted +1) plus `PL-DOC` and `PL-PIPE` for
the two parallel lifecycles. `docs/gates.md` is the living registry of gate
definitions and condition rosters; the handoff file stays frozen as provenance.

## Consequences
- Conditions are added, specified, and tightened per gate without new identity
  churn - "create the gates, then apply conditions" becomes the roadmap shape.
- Condition lifecycle is explicit: `registered` (named, intent known) ->
  `specified` (mechanical pass condition fixed) -> `enforced` (live in the venue).
- Human checkpoints (spec ambiguity review, ADR review, UAT) are conditions
  tagged `human`; the THEORY loopability invariant binds `mechanical` conditions.
- The registry consolidates only - inventing a gate or condition there without a
  design source is drift, not progress.
