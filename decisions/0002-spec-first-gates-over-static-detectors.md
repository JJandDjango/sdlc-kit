# 2. Gate with spec-first artifacts, not ever-more static detectors

Status: accepted
Date: 2026-07-22

## Context
Framing question: can a sufficiently structured set of static analysis tools and
conventions make automated LLM development run without bugs or codebase
degradation? Established in the 2026-07-22 design pass
(`HANDOFF_gate-architecture_2026-07-22.md`, sections 1-2):

- Degradation is structural (complexity creep, duplication, coupling, drift,
  dead code) and therefore statically measurable and largely preventable.
- Bugs are not eliminable by static analysis alone - Rice's theorem; practical
  analyzers are heuristic (neither sound nor complete).
- Residual defect mass for LLM-generated code concentrates in requirements
  misinterpretation, missing edge cases, and API misuse - classes invisible to
  linters.

## Decision
Treat the two problems differently. Degradation is closed with static
enforcement (ratchets, architecture tests, custom analyzers). Bugs are closed
with spec-first gates - immutable acceptance tests, property/metamorphic specs,
boundary contracts, differential oracles - authored before and independently of
the implementation. Engineering effort pushes bug classes *up* the detectability
ladder (toward correct-by-construction) rather than accumulating detectors at
the bottom.

## Consequences
- Human attention concentrates at the spec stage; specs stay declarative so that
  review stays cheap.
- Spec authorship becomes the critical path - the pipeline needs a dedicated
  spec channel, decorrelated from the implementer.
- The oracle problem remains: a wrong spec yields conformant wrong code. This is
  accepted residual risk, mitigated by spec review, UAT, and the convergence
  loop (escaped defects become new acceptance criteria).
- Treat this verdict as settled; do not re-litigate static-analysis sufficiency
  in future sessions.
