# 7. Hard-core designation criteria

Status: accepted
Date: 2026-07-23

## Context

Q8 - which components merit formal models - is the open parameter shared by
G1.2, G2.1, and G5.6. Model checking is the pipeline's costliest loop
(counterexample-trace interpretation), so the designation set must be
rationed: catalog pattern 8 reserves formal models for components where
detectability-ladder positions (c)-(d) are unacceptable. The G1 deep page
drafted three-part criteria; the session-5 once-over surfaced them and the
user ratified as drafted.

## Decision

Designate a component a hard core when a defect in it would be all three of:

1. **concurrency- or distributed-protocol-shaped** - interleavings, message
   orders, partial failure;
2. **invisible until (d)-time or later** - no static rung or review-time
   check would catch it;
3. **costly-irreversible in production** - data loss, safety, money movement.

A conjunction: the prongs prune independently (shape, detectability, blast
radius) and together keep the set small. Components failing any prong route
to the (d)-rung conditions instead (G5.3 fuzzing, G5.4 Coyote). Where a
designation is recorded (contract field vs spec-set annotation) is deferred
to the enforcement pass, like state-space bounds and G1.3 sign-off mechanics.

## Consequences

- G1.2's parameter is now procedure-bound (apply the test per component at
  spec time): G1.2 `registered` -> `specified` under
  [0004](0004-per-gate-documentation-program.md)'s parameter rule.
- G2.1 and G5.6 stay `registered` (pass conditions fixed at their own
  sessions); their shared parameter resolves to this ADR.
- Q8 moves to the registry index's resolved list.
