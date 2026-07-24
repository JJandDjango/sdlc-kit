# 11. Criterion traceability format

Status: accepted
Date: 2026-07-24

## Context

The REQ-ID / criterion-annotation format, exported to the G4 session by
G2 (consumers G2.4, G2.5, G4.3; also G1 authoring, G6.1, G8.3).
Parallel spec tasks make a global ID sequence collide; annotations must
be consumable from run results, not source archaeology.

## Decision

1. **ID grammar `REQ-<task>-<nnn>`,** task-scoped: uniqueness inherits
   from task IDs (G0), allocation is local, provenance built in. One
   grammar; classification (functional / security / property) is
   criterion *metadata*, never an ID prefix. G8.3 escapes take their
   converting spec task's ID - no special grammar.
2. **Record `specs/<task>/criteria.yaml`** (id, statement, kind) - the
   enumeration source every mode reads, the artifact G1.3 reviews,
   class S protected.
3. **Annotation surfaces in runner results** (.NET: `[Criterion]`
   trait -> TRX); many-to-many. **Totality both directions** over the
   spec suites: an un-annotated acceptance/property test = FAIL
   (shadow-spec closure); a dangling reference = FAIL. Architecture
   partition exempt - it traces to ADRs; `[StructuralRule("ADR-nnnn")]`
   reserved for mechanizing G2.3 item 6 later.
4. **One script, three modes:** existence (G2.5 cl. 2), red (G2.5
   cl. 3), pass (G4.3) - criteria records x runner results, never
   source grep. Script = class E, PL-PIPE.2-golden-tested against
   fixture corpora.

## Consequences

- G4.3 `specified`; G2.4/G2.5's shared parameter closes.
- G6.1 walks `criteria.yaml`; G8.3 conversion lands new rows in it.
- Property tests join uniformly - a property is a criterion shape.
- Build item: traceability script + fixture corpus (0008 register).
