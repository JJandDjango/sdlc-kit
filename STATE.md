# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-28._

## Now
- Session 15 (2026-07-28): **the vocabulary layer is designed and
  ratified** (decisions/0017-vocabulary-layer.md). Design input was a
  transcript-based review of "Why Agentic Systems Need Ontologies"
  (Coyle, AI Engineer, 2026-07-22) against the standing
  deterministic-first directive. Import ruling: constraint *semantics*
  (enumeration, cardinality, disjointness, reference integrity,
  reachability), never machinery - RDF/OWL rejected for gating
  (open-world / no-unique-name semantics merge where a gate must
  reject; SHACL is the W3C answer if formal checking is ever wanted),
  JSON-LD rejected as operating format. Substrate confirmed: plain
  YAML/JSON, schema at the door, Python joins at the ledger;
  right-first-time layer = entity model + stable IDs + named
  constraint kinds.
- Ratified set V1-V10, headline shapes: per-term glossary files at
  `specs/vocabulary/` (filename = stable ID, flat dir, no stored
  index - `/sdlc vocab` computed listing is the landing point);
  optional `entities:` contract field (0005 amendment path); G0
  coverage join (ratified-only resolution; missing term = unresolved
  dependency, forks a vocab task, never fails the work); G0 agent
  vocabulary interface (annotations only - harness stays in the
  per-gate arc); greenfield seed interview (terms born ratified) and
  brownfield extractor (born draft, `sources:` provenance);
  `/sdlc vocab` / `vocab add` / `vocab extract` day-2 family
  (ratification un-tooled: class-S edit, PR merge = interim approval
  record); class-E `constraints.yaml` born non-empty (G4.3 / G4.6 /
  `fixes:` / G10.1 enumerated retroactively); evolution = intake
  accretion + conversion ratchet + sunset lifecycle + versioning
  policy; RDF projection map deferred per 0008 discipline.
- Verified this session: the kit repo is **not** self-initialized (no
  SDLC.md / .sdlc/ / specs/ at root). V9 decides `/sdlc init` runs
  here at implementation start - the first contract through this
  repo's own G0 is the vocabulary feature itself, and the kit's
  brownfield extraction (formalizing the registry's existing terms)
  is the extractor's first fixture.
- Uncommitted at handoff: `decisions/0017-vocabulary-layer.md` (new),
  `plan.md` (session-15 refresh), this STATE regen - commit-session
  lands them as the session commit.

## Blockers
- None.

## Next actions
1. **Implementation plan for the ratified set** (plan.md step 5), ADR
   order: V9 self-host init, V10 docs Pass 0 (docs/vocabulary.md +
   USAGE, red markers), then engine-before-skill passes: glossary
   schema + door check, `entities:` field + G0 join, `/sdlc vocab`
   subcommands + extractor, constraints.yaml; suites green throughout.
2. **Per-gate agent arc** (0017 V4's named neighbor): harness, venue,
   verdict plumbing, plugin `agents/` distribution. V4 fixed the G0
   agent's vocabulary interface; the G0 slot's design input stays on
   record at engine `PILOT-NOTES.md`.
3. **Pilot continues** (engine repo's own session): M0 through the
   gates with a fresh Developer context - Q5 reality data; gate-passage
   notes keep feeding the agent design.
4. Unchanged deferrals: Q4 numbers + activation build items (0015
   inventory); PyPI publish; explainer PDF into docs/ if wanted.

## Open questions
- Q4 thresholds, numeric only - vocabulary sunset notice floor (0017
  V7c) now rides here too.
- Q5 two-channel decorrelation; named sub-question: the Developer's
  context contents - the M0 implementation session is the first live
  data point.
- Per-gate agent shape: venue, context assembly, verdict format,
  plugin versioning - G0's vocabulary judgments now fixed by 0017 V4;
  the rest stays open.

(Q6 stream framing holds: the engine is consumer 1; this repo becomes
consumer 2 at the V9 self-host.)
