# Changelog - sdlc-kit

The migration-notes venue (contract: `distribution-reconciliation`).
Two house rules, enforced in review:

- **No schema `version:` bump merges without its delta note here.**
- **Tag on bump:** every kit version bump is tagged `v{X.Y.Z}` at the
  merge that ships it, and the scaffolded install ref pins to that
  tag. Consumers upgrade by bumping the ref in their committed
  workflow - pull, not push - with this file in hand.

## 0.5.0 - 2026-07-29 (tag `v0.5.0`)

- Tooling profiles (ADR 0018): the recorded `stack:` now selects a
  template overlay at `templates/profiles/{stack}/` (profile.json
  manifest; add or replace-by-target; same no-clobber and merge
  semantics). The dotnet overlay ships as the live container -
  deliberately empty until its G3 slice; `docs/dotnet-profile.md` is
  the profile's status page (binding table, fit notes, gap register).
- `/sdlc update` resolves the consumer's profile from
  `.sdlc/config.yaml` and reports overlay surfaces in their declared
  classes; a consumer scaffolded before a profile slice ships sees
  the new surfaces as `absent` rows with per-file consented apply -
  no forced migration.
- Existing consumers: bump the install ref in
  `.github/workflows/sdlc.yml` and the schema URL in
  `.vscode/settings.json` when you take this version (`/sdlc update`
  reports exactly this drift). Schemas: none changed. The glossary
  gains the ratified `tooling-profile` term.

## 0.4.0 - 2026-07-29 (tag `v0.4.0`)

- Scaffolded install ref pins to the release tag (`@v{version}`)
  instead of floating main; the editor schema URL pins the same way.
  Existing consumers: bump the ref in `.github/workflows/sdlc.yml`
  and the raw URL in `.vscode/settings.json` when you take this
  version - `/sdlc update` reports exactly this drift.
- `/sdlc update` day-2 flow + report-only drift engine (update.py):
  renders the current templates, names each drifted scaffold file,
  applies per-file and only on consent.
- CHANGELOG.md born (this file), backfilled to 0.1.0; docs gain
  docs/distribution.md (the three channels + reconciliation story).
- Schemas: none changed. Migration: none beyond the consumer ref
  bump above.

## 0.3.0 - 2026-07-28 (tag `v0.3.0`)

- Vocabulary layer ships end to end (ADR 0017): glossary door at
  `specs/vocabulary/` with stable VT000-VT009 diagnostics; vocab CLI
  family (`vocab-list` / `vocab-add` / `vocab-check`); constraint
  registry born non-empty (VC000-VC003); audit gains VOCAB-INVALID
  and CONTRACT-WARNED, with `specs/vocabulary/` exempt from the
  orphan sweep.
- **Schema delta - task-contract 1.0.0 → 1.1.0** (the delta-note
  exemplar): optional `entities:` array of vocabulary-term refs.
  Existing contracts stay valid with no edits; the G0.2 coverage
  join activates only on presence (TC010-TC012 errors + W001
  sunset-window warning in `validate --profile ready`). Migration:
  none required; declare `entities:` when a contract's nouns are
  ratified vocabulary.
- Schemas born: glossary-term 1.0.0, constraint-registry 1.0.0.
- Packaging fix: all schemas now ship inside the wheel. Previously
  the wheel carried none - any non-editable consumer install failed
  at its first contract validation.

## 0.2.0 - 2026-07-26

- The /sdlc skill ships: no-clobber init renderer (SDLC.md, `.sdlc/`
  config + clocks + standing-red ledger, protected `specs/` root, CI
  validate job, merge-target snippets), report-only audit engine.
  The kit goes public as `sdlc-kit` (GitHub install, plugin
  marketplace).
- Schemas: none changed.

## 0.1.0 - 2026-07-23

- Kit born: task-contract schema 1.0.0 (draft + ready profiles in
  one file), `taskcontract` validator with stable TC000-TC009
  diagnostics, contract scaffold (`new`), golden fixtures + suite,
  kit CI.
