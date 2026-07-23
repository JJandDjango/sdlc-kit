# 4. Specify conditions through per-gate deep pages

Status: accepted
Date: 2026-07-23

## Context
All 47 conditions are `registered`; exact pass conditions and per-condition
rationale live half in the frozen handoff, half nowhere. User directive
(session 3): iterate the gates one by one and fully document what each gate
must contain and why. The registry (`docs/gates.md`) is a scan surface with a
row-per-condition budget - deep material needs its own stratum, and advancing
lifecycle without recorded rationale would violate the Theory rule (no change
without its why).

## Decision
Run a sequential per-gate documentation program: G0 -> G10, then PL-DOC,
PL-PIPE. Each gate gets a deep page `docs/gates/<ID>-<slug>.md` with fixed
sections: identity; why the gate exists (defect classes, ladder positions,
invariants); per-condition what / why / kind & loopability / tooling /
parameters / lifecycle; completeness check; operators & harness; decisions.
Depth is document + specify: a condition advances to `specified` when its
exact pass condition and parameters are fixed - a parameter may be a bound
procedure, never a vague intent; building enforcement artifacts is a later
pass. Roster policy is normative: completeness gaps become PROPOSED
conditions that enter the registry only on user ratification - the ratified
analysis is their design source (per 0003's no-invention rule). Light gates
batch (~7 sessions); soft budget <=2 pages per gate page.

## Consequences
- The registry stays the index: one line per condition plus a deep-page link;
  rationale and exact pass conditions live in the gate pages.
- Open questions Q1-Q8 resolve (ADR) or are explicitly deferred in the
  session documenting their owning gate.
- Substrate pages `docs/taxonomy.md` and `docs/catalog.md` carry the shared
  why-material so gate pages link instead of duplicating the handoff.
- The registry's "all registered" claim goes stale by design; counts and
  per-gate state lines update as pages land.
