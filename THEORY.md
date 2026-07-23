# Theory - sdlc_development_kit

> **Contract** - one question: *why does this exist, and what must stay true?*
> <=1 page - update when purpose or invariants change - hand-edited, rare.

## Intent
An SDLC gate architecture for automated LLM development - spec-first gates plus static enforcement so agent-written code cannot degrade the codebase, and bug classes are systematically closed at the earliest decidable point.

## Invariants
<!-- What must stay true no matter what changes below. The load-bearing constraints. -->
- **Spec-first gates** are authored before and independently of the implementation,
  mechanically checkable, and **immutable to the implementer** - enforced by path
  checks in CI/Verifier diffs, never by prompt instructions.
- **Two-channel principle.** Spec and implementation come from separate agents with
  decorrelated context; shared context reproduces shared misreadings.
- **A gate = a human judgment converted into a text artifact plus a mechanical
  check.** Every gate emits machine-actionable diagnostics an agent can loop
  against until clean.
- **Earliest decidable point.** Cost determines cadence (inner-loop seconds to
  nightly hours), never rigor - slow gates still block release.
- **Detectability ladder.** Engineering effort pushes bug classes *up* the ladder
  (correct-by-construction > statically decidable > approximable > dynamic >
  spec-relative), rather than accumulating detectors at the bottom.
- **The enforcement layer is the highest-privilege artifact set** (CI config,
  rulesets, agent prompts, spec paths). It gets a separate approval channel from
  what it enforces, plus its own regression suite.
- **Convergence loop.** Every escaped defect becomes a new immutable acceptance
  criterion - the gate set tunes to the actual defect distribution.
- **Explicit retirement.** Agents add code and almost never delete it; a
  deprecation phase is mandatory or the codebase grows monotonically.
- **Specs stay declarative** (criteria, properties, schemas) so spec review stays
  cheap - that is the one place human attention concentrates.

## Success criteria
<!-- How you'll know it's working. -->
- A pilot repo runs agent-driven development with structural degradation held flat
  by ratchets, architecture tests, and analyzers - measured, not asserted.
- Residual defects concentrate only in spec-relative classes, and each escape
  converts into a new gate (convergence loop demonstrably closing).
- Every gate is loopable: an agent can drive it to green from its diagnostics
  alone, without human interpretation.

## Non-goals
<!-- What this explicitly does NOT try to do - the anti-scope that stops drift. -->
- **Not** eliminating all bugs by static analysis - settled: Rice's theorem makes
  general semantic correctness undecidable; analyzers are heuristic.
- **Not** a generic linter/detector collection - gates are selected against the
  actual defect distribution, not the full generic taxonomy.
- **Not** prompt-level enforcement - an agent that can edit a failing test will
  edit the test; only mechanical checks on immutable paths count.
- **Not** solving the oracle problem - a wrong spec yields conformant wrong code;
  the kit keeps spec review cheap, it does not replace it.
