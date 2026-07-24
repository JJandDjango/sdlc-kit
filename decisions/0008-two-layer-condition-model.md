# 8. Two-layer condition model

Status: accepted
Date: 2026-07-24

## Context

Never ruled: is the kit C#-only? The architecture layer is
language-neutral; the registry's Check/Tooling columns are .NET end to end
- source-handoff provenance, not a decision. 0003's `specified` demands an
*exact* pass condition; exactness dissolves under genericization, registry
forks drift, and some ecosystem strengths have no universal equivalent.
User directive: build tooling gaps, don't just document them.

## Decision

Two layers per condition: a **shape** - normative, ecosystem-free pass
condition; `specified` = shape exact - and per-ecosystem **tooling
profiles** binding it to exact commands and exit semantics. **.NET is the
reference profile** (the registry's Check/Tooling columns, the deep
pages' binding sections).

1. Unreachable shape -> **kit build item** (gap-closure directive): the
   kit authors missing enforcement tooling rather than downgrading shapes.
2. Build trigger = an active profile's need, never speculative
   completeness; no speculative profiles - .NET stays the only authored
   profile until a real second-ecosystem target exists.
3. A missing binding gates that profile's `enforced` flip, never
   `specified` (G0.1 precedent).
4. Profiles document unreachable rungs + compensations (gap-analysis per
   profile); ladder positions go profile-relative where they must.

## Consequences

- [G3-implementation](../docs/gates/G3-implementation.md) sets the pattern
  (Shape / Reference binding / Gap status); G0-G2 retrofit lazily.
- Registry vocabulary gains the two-layer bullet; ecosystem-bound names
  de-ecosystem as pages are authored (first: G3.2 -> "Analyzer battery").
- First build items: sunset-escalation analyzer (G10.1), suppression-audit
  diff check. Cost: two-layer text + gap tables, bounded by no-speculation.
