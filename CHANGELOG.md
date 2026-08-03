# Changelog - sdlc-kit

The migration-notes venue (contract: `distribution-reconciliation`).
Two house rules, enforced in review:

- **No schema `version:` bump merges without its delta note here.**
- **Tag on bump:** every kit version bump is tagged `v{X.Y.Z}` at the
  merge that ships it, and the scaffolded install ref pins to that
  tag. Consumers upgrade by bumping the ref in their committed
  workflow - pull, not push - with this file in hand.

## 0.10.0 - 2026-08-03 (tag `v0.10.0`)

- Work adoption behind a one-way membrane (ADR 0023): USAGE gains
  §7 - kit flows to restricted environments by public tag, findings
  flow home in controlled-dictionary terms, gate IDs, and counts;
  no network calls anywhere in the enforcement path; `uv run` line
  for local checks without managing Python.
- The base scaffold grows two kit-owned surfaces (6 -> 8):
  `.sdlc/findings/TEMPLATE.yaml`, the return-channel finding form
  with its rule printed on the form (no identifiers, no code), and
  `.sdlc/NOTICE.md`, provenance for the rendered scaffold (upstream,
  rendering tag, license, tag-pinned policy link). `kit_version`
  joins the template namespace in both engines (init render, update
  compare). Consumers at older pins see the new surfaces as honest
  `absent` rows in `/sdlc update` after they bump.
- Dotnet day-one posture ruled consumer-side: a fresh render builds
  red on pristine code (SA0001, the IDE0005 doc-file refusal,
  CA1303) - that is the posture decision surfacing, not debt. The
  menu (GenerateDocumentationFile / CS1591 / SA0001 / CA1303) with
  exact lines and the baseline-not-diff venue rule joins
  docs/dotnet-profile.md; templates ship maximal, unchanged.
- Suite 188 -> 190.

## 0.9.0 - 2026-08-02 (tag `v0.9.0`)

- The controlled-language layer ships whole (contract
  `controlled-language`, ADR 0022): bounded interpretation for
  executed prose - form checked, meaning not checked. A set-ratified
  dictionary at `specs/vocabulary/dictionary.yaml` (closed
  general-word class + field registry + exempt ratchet) arms
  `python -m taskcontract lang-check` over the six contract prose
  fields: CLnnn codes, tier-1 rules (unknown/banned word, caps by
  text type, modal policing, pronoun subjects,
  comparative-without-number, verb-first sketches) + integrity
  checks (glossary disjointness, use_instead resolution, base
  shadowing at info). Absence of the dictionary = green.
- `lang-extract` is the report-only calibration harvest (candidates,
  banned hits, per-contract census); the seed is born from the
  repo's own ready-green corpus. `/sdlc lang` + `/sdlc lang extract`
  join the skill; the audit gains `LANG-INVALID` / `LANG-EXEMPT`;
  the scaffolded workflow template gains the backstop step.
  Consumers at older pins are unaffected until they bump - the
  kit's own workflow takes the step with the self-pin PR.
- Base layer (function words + vagueness/evasive-verb bans, no
  content verbs) rides the wheel at
  `taskcontract/data/base_dictionary.yaml` - never copied per repo;
  local glossary shadows base. New wheel data path packaged
  (`data/*.yaml`).
- Vocabulary: `controlled-dictionary` + `controlled-field` enter as
  drafts; the constraint registry gains
  `glossary-dictionary-disjointness` (enforced, entry 6);
  `dictionary` joins the reserved stems beside `constraints`.
- Schemas: `dictionary.schema.json` born `1.0.0` (new file - no
  migration; the artifact is optional and absent = green).
  task-contract, glossary-term, constraint-registry unchanged.

## 0.8.0 - 2026-07-31 (tag `v0.8.0`)

- The operator layer ships its first slice (contract
  `operator-layer`, ADR 0021): plugin `agents/` carries the Two-Key
  pair - `sdlc-developer` (G3 write surface: implementation + unit
  tests only; never reads acceptance-test source) and
  `sdlc-verifier` (zero-trust grader: re-runs every check fresh,
  writes nothing - no Edit/Write in its toolset). `sdlc-spec` and
  `sdlc-qa` are registered, shipping when their venues exist.
- `docs/operators.md` is the layer's deep page and makes two
  contracts normative: the verdict contract (exit 0/1/2, `--json`
  findings arrays, stable codes - existing surfaces grandfathered
  with named deltas) and the loop protocol (single-segment
  invocations, fix what diagnostics name, cap 5, no retry-to-green,
  checks read-only to the looper). Venue map covers all 13 gates;
  G4's agent venue is local preflight - CI stays authoritative and
  agentless.
- The dotnet `profile.json` gains `commands:` - `g3` (format verify,
  build) and `g4-preflight` (locked restore, build, full tests,
  suppression audit vs `origin/main`) - data operator defs bind at
  runtime, never rendered scaffold; the CI-side secrets scan stays
  workflow-only. Scaffold output is unchanged for every stack: ref
  bump only, no drift to reconcile.
- Vocabulary: `operator` and `verdict` enter as drafts (sources:
  `docs/operators.md`); ratification stays a review act.
- Agents ride the plugin channel: `claude plugin update` delivers
  them; `/sdlc update` deliberately does not cover `agents/`.
  Schemas: none changed.

## 0.7.0 - 2026-07-30 (tag `v0.7.0`)

- The dotnet workflow grows into the merge gate (contract
  `dotnet-profile-g4`) - G4's mechanical core, four conditions bound:
  the standing echo as G4.1's three clauses, full test execution
  (G4.11: `dotnet test` after the build, zero tests discovered =
  FAIL), secrets scan (G4.9 clause 1: gitleaks diff-mode as one
  docker step, output masked), dependency audit (G4.9 clause 2:
  NuGetAudit over a locked graph), and the four-vector suppression
  audit (G4.10) run from the pinned kit install.
- `Directory.Build.props` (merge-target) gains the locked-graph
  block: `RestorePackagesWithLockFile`, `NuGetAudit` + mode + level,
  NU1901-1904 raised to errors. Brownfield: a repo without committed
  `packages.lock.json` files lands red at CI restore until
  `dotnet restore` writes them and they land.
- Workflow venue per ADR 0020: one file serves both venues -
  `merge_group` added (queue-authoritative) beside `pull_request`
  (advisory preview); diff-scoped steps skip push-main runs. Job
  renamed `inner-loop` -> `merge-gate`: repos using it as a required
  check must update the check name.
- New subcommand: `python -m taskcontract suppression-audit` - G4.10's
  four vectors (in-source suppressions, severity downgrades,
  strictness weakening, exclusion widening; construct lists are
  binding material). Exit 0 clean / 1 findings / 2 environment;
  `--json` for the loop. Pipeline-native checks distribute this way -
  kit modules behind the pin, never copied scripts (ADR 0020).
- Existing dotnet consumers: `/sdlc update` reports workflow drift
  (kit-owned - take it with `--apply`) and props drift (merge-target -
  merge the audit block by hand; `--show` prints the render).
  Non-dotnet consumers: byte-identical payload, ref bump only.
- Existing consumers: bump the install ref in
  `.github/workflows/sdlc.yml` and the schema URL in
  `.vscode/settings.json` when you take this version. Schemas: none
  changed.

## 0.6.0 - 2026-07-30 (tag `v0.6.0`)

- The dotnet overlay carries its first payload (contract
  `dotnet-profile-g3`) - G3's inner loop, four surfaces:
  `Directory.Build.props` (merge-target; the five strict-compile flags
  + `EnforceCodeStyleInBuild` + pinned StyleCop.Analyzers),
  `.editorconfig` (merge-target; layout rules + severity map),
  `.github/workflows/sdlc-dotnet.yml` (kit-owned; format verify +
  strict build beside the G0 backstop), and a pre-commit replacement
  adding the `dotnet format` hook (merge-target, like its base).
- Drift classes per ADR 0019: enforcement configs consumers extend
  are merge-target - written when absent, snippet when present, drift
  reported never applied; kit process artifacts stay kit-owned.
- Existing dotnet consumers: `/sdlc update` reports the three new
  surfaces `absent` and the pre-commit target as merge-target drift.
  Take the workflow with `--apply`; merge the two configs and the
  hook by hand (`--show` prints each render). Non-dotnet consumers:
  byte-identical payload, ref bump only.
- Existing consumers: bump the install ref in
  `.github/workflows/sdlc.yml` and the schema URL in
  `.vscode/settings.json` when you take this version (`/sdlc update`
  reports exactly this drift). Schemas: none changed.

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
