# Plan - Session 15 (2026-07-28)

The session's design input arrived from the user: a review of "Why
Agentic Systems Need Ontologies" (Coyle, AI Engineer) against the
standing deterministic-first directive. Outcome: the vocabulary layer -
shared language as executable definitions - designed, ratified, and
recorded as ADR 0017 (glossary family, `entities:` field, G0 coverage
join, G0 agent vocabulary interface, greenfield seed / brownfield
extraction, `/sdlc vocab` day-2 family, constraint registry, evolution
loops, RDF map deferred, kit self-hosting, docs Pass 0). The import
ruling: constraint semantics, never RDF/OWL/JSON-LD machinery - plain
YAML/JSON, schema at the door, Python joins at the ledger.

## This session

1. Refresh this plan (done).
2. Design input: video review + kit docs mapping (done - review
   delivered in-conversation; gates.md + 0008 grounded the mapping).
3. Feature list interrogated and ratified (done - V1-V10; V1 closed
   per-term-files + computed listing, no stored index).
4. Record the design doc (done - decisions/0017-vocabulary-layer.md).
5. Next: implementation plan scoped to the ratified set. Order per
   ADR: V9 self-host (`/sdlc init` on this repo; first contract = the
   vocabulary feature), V10 docs Pass 0 (docs/vocabulary.md + USAGE,
   red markers), then engine-first passes (glossary schema + door,
   `entities:` + G0 join, `/sdlc vocab` subcommands + extractor,
   constraints.yaml), suites green throughout.

Deferred until wanted or until pilot reality: per-gate agent harness
arc (ADR 0017's named neighbor); PyPI publish; explainer PDF into
docs/; Q4 numbers + activation build items (0015 inventory).

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos.
