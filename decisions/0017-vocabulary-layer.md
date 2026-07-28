# 17. Vocabulary layer

Status: accepted
Date: 2026-07-28

## Context

Standing directive: maximize deterministic, executable checks; LLM
judgment rides on top and converts into code over time. Design input:
review of "Why Agentic Systems Need Ontologies" (Coyle, AI Engineer,
2026-07-22) - the import is the constraint *semantics* (enumeration,
cardinality, disjointness, reference integrity, reachability), never
the machinery. RDF/OWL ruled out for gating: open-world semantics with
no unique-name assumption merge where a gate must reject (the
functional-property/sameAs trap); SHACL is the W3C answer if formal
checking is ever wanted. JSON-LD ruled out as operating format:
serialization is not semantics, JSON-Schema validation forces a pinned
canonical form that nullifies it, and the cost lands on the kit's most
friction-sensitive surfaces (intake authoring, zero-dep audit, consumer
distribution). Substrate stays plain YAML/JSON - schema at the door,
Python joins at the ledger. The right-first-time layer is the entity
model + stable IDs + named constraint kinds; serializations migrate
mechanically once IDs are stable. Vocabulary definitions decide what
passes gates, so they are enforcement-layer artifacts: CRUD rides the
[0014](0014-enforcement-change-control.md) lanes, retirement rides the
[0013](0013-sunset-policy.md) pattern. Shared understanding between
human and agent is established by both being bound to the same
executable definitions - never by prose both parties merely read.

## Decision

Feature set ratified 2026-07-28:

1. **Glossary family (V1)** - `specs/vocabulary/<term-slug>.yaml`, one
   file per term, flat directory, filename = stable ID. Kit-side
   schema (`schemas/glossary-term.schema.json`): term, name,
   definition, kind (entity | relation | attribute | value-set),
   relations (is_a, part_of, disjoint_with), values (value-sets),
   status (draft | ratified | deprecated), since, sunset, sources
   (extraction provenance), aliases. No stored index - the landing
   point is the `/sdlc vocab` computed listing, drift-impossible by
   construction. Stored-index need-trigger registered: a consumer that
   must read summaries without executing code.
2. **`entities:` contract field (V2)** - optional array declaring the
   terms a task operates on; schema tightening via the
   [0005](0005-task-contract-fields.md) amendment path.
3. **G0 coverage join (V3)** - every `entities:` ref resolves to a
   **ratified** term; unresolved = unresolved dependency under the
   existing ready profile - forks a small vocabulary task, never fails
   the work; diagnostics name the missing terms. Draft terms do not
   resolve: ratification is deliberately the human bottleneck - one
   cheap action per term, concentrated exactly on shared meaning.
4. **G0 agent vocabulary interface (V4)** - inputs: raw request +
   contract + glossary; judgments: undeclared concepts in the prose,
   drifted use of declared terms, drafted candidate definitions;
   output: annotations only - never edits, never a sole verdict.
   Agent harness, venue, and plugin distribution stay in the per-gate
   agent arc.
5. **Generation (V5)** - greenfield: init interview elicits 5-15 seed
   terms, born ratified (the interviewee is the principal; answers are
   interview-equivalent). Brownfield: LLM extraction over declared
   surfaces (API baselines, schemas, domain types, docs) with
   `sources:` provenance, born draft, ratified selectively. Day-2
   family so initialized repos adopt without re-init: `/sdlc vocab`
   (computed listing), `vocab add {id}`, `vocab extract`; the init
   branch calls the same machinery. Ratification stays un-tooled in
   v1: the status flip is a class-S edit and the PR merge is the
   interim approval record.
6. **Constraint registry (V6)** - `specs/vocabulary/constraints.yaml`,
   class E (manifest-marked): id, kind (enumeration | cardinality |
   disjointness | reference-integrity | reachability), subjects (term
   refs), check (implementing validator), status. Born non-empty: the
   four existing pipeline joins (G4.3 traceability, G4.6 write
   surface, `fixes:` resolution, G10.1 coherence) enumerated
   retroactively.
7. **Evolution (V7)** - (a) intake accretion is the growth mechanism:
   vocabulary grows at the rate work demands it, never faster. (b)
   Conversion ratchet: a recurring agent finding becomes a constraint
   entry + executable check - principle recorded now, tooling when the
   agents are live. (c) Lifecycle: deprecation sets sunset; the join
   warns inside the notice window, errors past it; deletion only at
   zero references (notice floor rides Q4). (d) Kit-vocabulary
   versioning: schemas carry `version:`, deltas ship migration notes
   in the plugin changelog; tooled consumer migration deferred until
   consumer count makes manual lockstep untenable.
8. **RDF projection map (V8)** - deferred build item per
   [0008](0008-two-layer-condition-model.md) discipline. Trigger: an
   external consumer wanting the artifact graph as RDF; enters as one
   out-of-band context document - and SHACL, not OWL, if checking
   follows.
9. **Kit self-hosting (V9)** - `/sdlc init` runs on this repo at
   implementation start; the first contract through its own G0 is this
   feature set.
10. **Docs Pass 0 (V10)** - `docs/vocabulary.md` + USAGE section
    authored red-marked before code; `gates.md` G0 row + deep page and
    `task-contract.md` updated as passes ship.

Out of scope, named: per-gate agent harness/distribution (own arc);
RDF/OWL/SHACL machinery beyond V8's deferral; numeric windows (Q4);
product-domain vocabulary content for consumer repos - theirs to
author through these venues.

## Consequences

- G0 gains its first ledger join and its first agent-interface
  definition; the two-layer split - script decides the decidable, LLM
  judges the residue, human ratifies meaning - is instantiated on the
  vocabulary itself, and the script's share grows as the glossary
  grows.
- The contract schema tightens (V2/V3) via the 0005 path: ADR + schema
  delta + tests; existing consumer contracts stay valid (field
  optional, join activates on presence).
- The pilot adopts via V5c without re-init; this repo becomes the
  second initialized consumer (V9) and its brownfield extraction -
  formalizing the registry's existing terms - is the extractor's first
  fixture.
- `specs/vocabulary/` joins the protected write surface; constraints
  registry entries join the manifest's class-E census.
