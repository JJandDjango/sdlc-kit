# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-28._

## Now
- Session 16 (2026-07-28): **the vocabulary layer is implemented and
  live** - ADR 0017's ratified set shipped end to end in seven commits
  (5e47b87..2f7e11a + close). V9 self-host first: /sdlc init
  (brownfield, python) makes the kit consumer 2, and the
  vocabulary-layer contract went ready-green through this repo's own
  intake - G0.1 (and now G0.2) read enforced-in-fact here. Docs Pass 0
  authored red, flipped green as passes shipped.
- Shipped surfaces: glossary door (glossary-term schema v1, VT000-009,
  bare-date normalization, stable-ID + closed-world relation checks);
  `entities:` + the G0.2 coverage join (contract schema 1.1.0,
  TC010-012 errors + W001 sunset-window warning on a new severity
  channel); `/sdlc vocab` family (vocab-list computed listing,
  vocab-add VT002-tripwire skeleton, extract flow + greenfield seed in
  SKILL.md, intake taught the fork move); constraint registry born
  non-empty (5 entries incl. the live entities-coverage row, class E
  self-declared, VC000-003). Extraction fixture is real: 10 terms from
  the kit's own registry, 3 ratified (task-contract, gate,
  vocabulary-term - per the contract's own sketch), 7 draft.
- Found-and-fixed en route: the wheel shipped **no schemas at all**
  (editable install masked it; any consumer CI crashed at first
  contract) - schemas now live inside the package, proven by a
  non-editable install validating this repo green from outside
  (Two-Key pass). Audit: severity-aware (CONTRACT-WARNED), vocab door
  (VOCAB-INVALID), specs/vocabulary/ exempt from the orphan sweep -
  that one found live by the stale installed audit. Kit 0.3.0. Suite
  37 -> 85 green; audit clean.
- **Pushed to origin/main at session end** (user-approved wrap). The
  scaffolded CI now installs the pushed kit - the first GitHub run of
  the vocab-check step is the 0.3.0 distribution loop's confirmation.
  Remaining consumer move: update the /sdlc plugin (the cache copy
  predates this session and mis-flags the glossary as an orphan).
- Out of contract scope, left stale for the user (one-liners or a g9
  intake): README.md tree line, CONVENTIONS.md schema ref,
  .vscode/settings.json raw URL - all still name the old root
  schemas/ path.

## Blockers
- None.

## Next actions
1. **Plugin update**, and verify the first GitHub CI run green
   (vocab-check step included) - that closes the 0.3.0 distribution
   loop.
2. **Ratify or prune the 7 draft terms** - class-S status flips, the
   user's cheap action; the glossary is the approval venue now.
3. **Per-gate agent arc** (0017 V4's named neighbor): harness, venue,
   verdict plumbing, plugin agents/ distribution; V4 fixed the G0
   agent's vocabulary interface.
4. **Pilot M0 session** (engine repo): first consumer of the vocab
   family via `/sdlc vocab extract`; Q5 reality data.
5. Deferrals unchanged: Q4 numbers (now incl. the sunset notice
   floor), PyPI publish, explainer PDF; V8 RDF map trigger-gated.

## Open questions
- Q4 thresholds, numeric only - vocabulary sunset notice floor rides
  here.
- Q5 two-channel decorrelation; the M0 session remains the first live
  data point for the Developer's context contents.
- Per-gate agent shape: venue, context assembly, verdict format,
  plugin versioning - G0's vocabulary judgments fixed by 0017 V4; the
  rest open.

(Q6 resolved in fact: the engine repo is consumer 1, this repo is
consumer 2 - both initialized, both under their own gates.)
