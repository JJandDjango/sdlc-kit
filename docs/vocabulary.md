# Vocabulary - executable shared language (the G0 coverage join)

<!-- covers: decisions/0017-vocabulary-layer.md -->

> **Contract** - one question: *how does shared meaning between human
> and agent become something the pipeline executes?*
> Component deep page (MAP row lands when the first surface ships).
> Ratified 2026-07-28 in [0017](../decisions/0017-vocabulary-layer.md).
> Import ruling: constraint *semantics* (enumeration, cardinality,
> disjointness, reference integrity, reachability), never machinery -
> RDF/OWL rejected for gating (open-world / no-unique-name semantics
> merge where a gate must reject), JSON-LD rejected as operating
> format; plain YAML, schema at the door, Python joins at the ledger.

**Status legend:** 🔴 ratified, not yet shipped · 🟢 shipped ·
⚪ deferred behind a named trigger. Docs Pass 0 authored 2026-07-28,
before any vocabulary code; markers flip as passes land.

## The two-layer split, applied to meaning

The script decides the decidable: schema validation at the door,
ratified-only resolution at the join, reference integrity in the
registry. The LLM judges the residue: undeclared concepts, drifted
usage, candidate definitions (the V4 interface, deferred with the
agent arc). The human ratifies meaning: one cheap `draft -> ratified`
flip per term, concentrated exactly where shared understanding is
created. Human and agent are bound to the same executable definitions -
never to prose both merely read.

## 🟢 Glossary family - `specs/vocabulary/<term-slug>.yaml`

One file per term; the filename is the stable ID; flat directory; no
stored index - the landing point is the `/sdlc vocab` computed
listing, drift-impossible by construction (a stored index returns only
if a consumer must read summaries without executing code - trigger
registered in 0017). Kit-side schema
`taskcontract/schemas/glossary-term.schema.json`, versioned, packaged
in the wheel. Door: `python -m taskcontract vocab-check` - stable
VTnnn diagnostics (VT000-VT009), bare YAML dates normalized, an absent
directory vacuously green; the scaffolded CI workflow carries the
backstop step. Fields:

| Field | Meaning |
|---|---|
| `term` | slug; must equal the filename (the stable ID) |
| `name` | display name |
| `definition` | the meaning, stated so drift is checkable |
| `kind` | `entity` / `relation` / `attribute` / `value-set` |
| `relations` | `is_a` / `part_of` / `disjoint_with` - term refs |
| `values` | the closed set (`value-set` kind only) |
| `status` | `draft` / `ratified` / `deprecated` |
| `since` / `sunset` | lifecycle dates; `sunset` set at deprecation |
| `sources` | extraction provenance (brownfield births) |
| `aliases` | alternate names extraction may fold in |

Terms are enforcement-layer artifacts: they decide what passes gates,
so CRUD rides the [0014](../decisions/0014-enforcement-change-control.md)
lanes, retirement rides the [0013](../decisions/0013-sunset-policy.md)
pattern, and `specs/vocabulary/` joins the protected write surface.

## 🔴 `entities:` field + the G0 coverage join

Contracts gain an optional `entities:` array - the terms a task
operates on - via the [0005](../decisions/0005-task-contract-fields.md)
amendment path: existing contracts stay valid, the join activates on
presence. Ready-profile semantics:

- every ref must resolve to a **ratified** term;
- a missing or draft ref is an *unresolved dependency* under the
  existing ready profile - diagnostics name each missing term; the
  move is to fork a small vocabulary task, never to fail the work;
- draft does not resolve - ratification is deliberately the human
  bottleneck, one cheap action per term, concentrated on meaning;
- a deprecated term warns inside its sunset window and errors past it
  (the notice floor is a Q4 number).

## 🔴 Generation - born ratified or born draft

| Path | Mechanism | Born |
|---|---|---|
| greenfield | init interview elicits 5-15 seed terms (the interviewee is the principal; answers are interview-equivalent) | ratified |
| brownfield | `vocab extract` over declared surfaces (API baselines, schemas, domain types, docs), `sources:` provenance | draft |
| single term | `vocab add <slug>` skeleton | draft |

Ratification is un-tooled in v1: the status flip is a class-S edit and
the PR merge is the interim approval record. The extractor's first
fixture is this repo's own registry terms - the kit is its own second
initialized consumer.

## 🔴 `/sdlc vocab` day-2 family

`/sdlc vocab` (computed listing) · `/sdlc vocab add <slug>` ·
`/sdlc vocab extract`. Day-2 so initialized repos adopt without
re-init; the init greenfield branch calls the same machinery.

## 🔴 Constraint registry - `specs/vocabulary/constraints.yaml`

Class E, manifest-marked. Entry shape: `id`, `kind` (`enumeration` /
`cardinality` / `disjointness` / `reference-integrity` /
`reachability`), `subjects` (term refs - reference integrity
enforced), `check` (the implementing validator), `status`. Born
non-empty: the pipeline's four existing cross-artifact joins - G4.3
criterion traceability, G4.6 write surface, `fixes:` resolution,
G10.1 coherence - enumerated retroactively; each entry's kind and
implementing check are fixed when the registry ships.

## 🔴 Evolution

- **Accretion** - vocabulary grows at the rate work demands it: the
  coverage join forks vocabulary tasks; nothing grows speculatively.
- **Conversion ratchet** - a recurring agent finding becomes a
  constraint entry plus an executable check; principle on record now,
  tooling when the agents are live.
- **Lifecycle** - deprecation sets `sunset`; the join warns inside the
  notice window, errors past it; deletion only at zero references.
- **Versioning** - schemas carry `version:`; deltas ship migration
  notes in the plugin changelog; tooled consumer migration is deferred
  until consumer count makes manual lockstep untenable.

## ⚪ Deferred, triggers on record

- **G0 agent vocabulary interface (V4)** - inputs: raw request +
  contract + glossary; judgments: undeclared concepts in the prose,
  drifted use of declared terms, drafted candidate definitions;
  output: annotations only - never edits, never a sole verdict. Ships
  with the per-gate agent arc.
- **RDF projection map (V8)** - one out-of-band context document,
  built when an external consumer wants the artifact graph as RDF
  ([0008](../decisions/0008-two-layer-condition-model.md) discipline);
  SHACL, not OWL, if formal checking follows.
