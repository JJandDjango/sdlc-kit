# 22. Controlled language: bounded interpretation for executed prose

Status: accepted
Date: 2026-08-02

## Context

Session-23 opener (user-named): ASD-STE100-style restriction for kit
artifacts so tasks execute the same way each time. Designed in a live
walk - review, STE anatomy, six pros, seven cons at depth, shape -
feature list F1-F12 ratified whole (design record:
docs/controlled-language.md, Pass 0). The kit-specific leverage: the
anti-gaming ruling makes criterion prose the developer's only spec
view, so the contract is the last open-natural-language input in the
G3 loop.

## Decision

- **Named "bounded interpretation," never "determinism."** The
  executor stays stochastic; controlled language shrinks the surface
  stochasticity acts on and converts prose checks from LLM judgment
  to string operations. Form checked; meaning not checked - the door
  says so in its docs, `--help`, and `--json` envelope. Verification
  (Two-Key) remains the guarantee; the oracle problem stays a
  non-goal.
- **Adopt STE's method, never its dictionary.** Closed core + open
  technical classes + checkable rules + conformance checker. The
  glossary is the open class (Technical Names); the new dictionary is
  the closed one - standalone, set-ratified (the merge is the
  ratification), disjoint from the glossary by mechanical check
  (constraint `glossary-dictionary-disjointness`, alias-aware,
  surface forms never stems). Seeded by harvest from the seven
  ready-green contracts - restriction within a familiar register,
  never an alien one.
- **First surface: the six contract prose fields** (intent, scope,
  non_goals, unit, done_means, acceptance_sketch), bound through the
  field registry inside the dictionary artifact - the door's sole
  scope authority; registry rows carry text_type (descriptive cap
  25 / procedural cap 20 + modal policing + verb-first sketches);
  extensions are class-E deltas on the full lane. Triage ladder
  before any field enters: enum it (schema), ref it (glossary),
  control it only if irreducibly prose.
- **Register boundary:** controlled where prose is executed (an
  operator loops on it); free where deliberated (THEORY, ADRs, docs
  literature, conversation). Raw human requests are never
  lexicon-policed - intake translates raw to controlled; the agent
  absorbs the rewrite tax inside the loop protocol.
- **Posture: hard at intake for new/changed contracts; legacy
  empirical.** Census 2026-08-02: zero banned hits; sentence caps
  and verb-first material (~130 findings). Disposition: the six
  pre-arc contracts ride the `exempt:` list in the dictionary
  (prose findings at warning severity - visible, never gating),
  paired with ledger entry `cl-legacy-tranche` (ADR 0015 fields).
  Removal is a tightening on the auto lane; a contract leaves the
  list at its next edit. New contracts never enter.
- **Two layers (distribution):** machinery in wheel + skill; the base
  layer (function words + bans + rules, no content verbs in v1)
  rides the wheel at `taskcontract/data/base_dictionary.yaml`, never
  copied per repo; the domain layer is per-repo. The door unions
  base + repo + glossary; a local glossary shadows a base word
  (CL013, info) so a kit bump can never break a consumer. Base ban
  `use_instead` is suggestion-only - integrity checks bind the repo
  artifact alone. Verb promotion into base waits on self-host
  evidence.
- **Rule-owned word classes:** modals and comparatives are approved
  by their rules, not the dictionary - a modal is legal in
  descriptive prose (CL009 fires procedural-only); a comparative is
  legal with a number in the sentence (CL011 otherwise).
- **0014 lanes govern deltas:** adding a word loosens - full human
  lane; banning or removing tightens - auto lane. Trace-fed
  curation (M0 traces, verifier divergence, rework) proposes deltas
  through draft -> ratify, never auto-entry; misreading-born deltas
  carry observation provenance (the g8-escape pattern transposed).
- **Naming:** the artifact filename `dictionary.yaml` joins
  RESERVED_STEMS (never a term), so the glossary terms are
  `controlled-dictionary` and `controlled-field` (drafts;
  ratification stays the user's class-S flip).
- **Vocabulary stays one meaning layer** - no business / technical /
  execution pillar partition (Neo4j-talk review): the catalog
  (schemas, registries, profiles) and the evidence (verdicts,
  ledgers) are their own strata; evidence enters meaning only
  through ratification.
- **Empirics front-run, admitted:** whether restriction helps the
  model reader is open. Registered: a PL-PIPE.3 comprehension eval
  family and M0 trace tagging; the door's KPI is escape-rate among
  greens (numeric threshold rides Q4). A null result re-prices one
  benefit; semantic diffs and mechanical checkability stand
  regardless. Style guardrail in the artifact: restricted choice,
  never unnatural construction.

## Consequences

- `lang-check` + `lang-extract` ship as taskcontract subcommands
  (CLnnn codes, verdict-contract native; absence of dictionary =
  green). CI template gains the backstop step; the kit's own
  workflow gains it in the self-pin PR (the v0.8.0 pin predates the
  subcommand). Audit reports LANG-INVALID / LANG-EXEMPT.
- Suite 158 -> 188. Kit 0.9.0; dictionary schema born 1.0.0.
- Deferred with triggers: base verb promotion (self-host evidence),
  F-item region checking (record-artifact insufficiency), prompt
  lexicon (foundations-side PromptLang extension), slot templates
  (per-field escape evidence), greenfield day-one arming (base
  maturity).
