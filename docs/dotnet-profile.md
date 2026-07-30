# Dotnet tooling profile - the kit's C# binding, gate by gate

<!-- covers: specs/dotnet-profile-g0/contract.yaml,
     specs/dotnet-profile-g3/contract.yaml,
     specs/dotnet-profile-g4/contract.yaml -->

> **Contract** - one question: *how does the kit bind to a .NET
> consumer, and what ships per gate?*
> Component deep page (MAP row landed with the container, 2026-07-29).
> Feature set ratified in-session 2026-07-29 (F1-F9, nothing struck);
> task contract `specs/dotnet-profile-g0/contract.yaml` - entities
> resolved through `tooling-profile` (ratified at this intake),
> `scaffold`, `consumer`. G3 slice ratified 2026-07-30 (its own F1-F9
> kept whole); contract `specs/dotnet-profile-g3/contract.yaml` -
> ready-green at intake, drift classes ruled in-contract. G4
> mechanical-core slice ratified 2026-07-30 (F1-F10 kept whole);
> contract `specs/dotnet-profile-g4/contract.yaml` - ready-green at
> intake, venue + distribution shape ruled in-contract (ADR 0020).

**Status legend:** 🔴 ratified, not yet shipped · 🟢 shipped ·
⚪ deferred behind a named trigger. Docs Pass 0 authored 2026-07-29,
before any implementation; G3 fit notes Pass 0 authored 2026-07-30;
markers flip as units land.

## What a tooling profile is

A **tooling profile** is the kit's per-stack binding layer: a template
overlay under `skills/sdlc/templates/profiles/{stack}/` that init
resolves on top of the stack-neutral base payload, selected by the
consumer's declared stack. It binds gate *shapes* to ecosystem tooling
without changing them - the registry's two-layer model
([0008](../decisions/0008-two-layer-condition-model.md)) applied at
the distribution layer; architecture recorded in
[0018](../decisions/0018-tooling-profile-distribution.md). An absent
or empty overlay renders the base exactly - non-dotnet consumers are
byte-identical to the pre-profile kit, and a dotnet consumer
scaffolded before a slice ships sees the new surfaces as honest
`absent` rows in `/sdlc update`, applied per-file on consent.

## 🟢 The container (units: profile-overlay-resolution, update-parity)

`stack:` selected nothing before 0.5.0 ("the v1 payload is
stack-neutral"). This slice made it live: base + overlay resolution
in init (no-clobber and merge-target semantics unchanged), the same
resolution in `/sdlc update` (stack read from `.sdlc/config.yaml`),
and one stack-aware next-steps line at init. The dotnet overlay
shipped **deliberately empty** at this slice; its first real payload
landed with the G3 slice below (0.6.0).

## Binding status, gate by gate

G0's two conditions are stack-neutral by construction - the C# delta
at G0 is zero checks, and that is a finding, not a gap. Bindings
below name the registry's .NET reference tooling
([gates.md](gates.md)); each ships as its own slice, activation
ordered by cost and the actual defect distribution, never by row
order.

| Gate | dotnet binding (registry reference profile) | Status |
|---|---|---|
| G0 planning/intake | identical to base - contract validation + vocabulary join are artifact checks; fit notes below | 🟢 0.5.0 |
| G1 requirements/spec | Spectral / buf lint; TLA+ for hard cores | 🔴 |
| G2 design/architecture | PublicAPI baselines, NetArchTest rules, STRIDE, red spec-suite run | 🔴 |
| G3 implementation | `dotnet format`, analyzer battery (StyleCop + custom Roslyn), strict compile props | 🟢 0.6.0 |
| G4 pre-merge CI | the 11-condition merge queue core (echo, arch tests, suites, ratchets, audits) | 🟢 0.7.0 mechanical core (G4.1, G4.9.1-2, G4.10, G4.11) · 🔴 remainder |
| G5 integration/system | Pact, differential + property campaigns, SharpFuzz, Coyote, Stryker.NET | 🔴 |
| G6 UAT/staging | certified-venue walk sheets; principal grades | 🔴 |
| G7 release/deploy | BenchmarkDotNet budgets, ApiCompat, IaC scan, canary, SBOM/provenance | 🔴 |
| G8 operations | OTel-family runtime contracts, SLO license, escape triage | 🔴 |
| G9 maintenance | Renovate lane, NuGetAudit/OSV SLAs, license audit, tightening job | 🔴 |
| G10 retirement | obsolete-sunset analyzer, dead-code ratchet, migration verification | 🔴 |
| PL-DOC documentation | samples csproj, CS1591-family coverage, staleness dating | 🔴 |
| PL-PIPE pipeline integrity | change control, gate-config goldens, behavior evals | 🔴 |

## 🟢 G0 fit notes for .NET shops (unit: dotnet-g0-doc)

- **Both conditions bind identically.** G0.1 validates the contract
  artifact, G0.2 joins `entities:` against the vocabulary - neither
  reads code. The intake venue (`/sdlc intake`), the validator, and
  the diagnostics are the same in a C# repo as anywhere.
- **The CI backstop is language-independent.** `sdlc.yml` sets up
  Python on the runner and validates contracts; it sits beside the
  repo's .NET build workflow and touches nothing of it.
- **Local validation needs Python once** (`pip install` of the pinned
  kit ref) - or lean on CI alone. The dotnet-tool wrapper stays a
  registered gap below.
- **Author `scope` at solution/project granularity** - project paths
  (`src/Foo/`, `*.csproj`) are the natural .NET scope units, and
  scope is the baseline later diff-scoped gates check against.

## 🟢 G3 fit notes for .NET shops (unit: dotnet-g3-doc)

Four surfaces land, resolved by the overlay at init and tracked by
`/sdlc update` in their ruled classes:

- **`Directory.Build.props`** (repo root, merge-target) - G3.3's
  strict compile (`Nullable` enable, `TreatWarningsAsErrors`,
  `AnalysisLevel latest-all`, checked arithmetic, unsafe off) plus
  G3.2's wiring (`EnforceCodeStyleInBuild`, pinned StyleCop.Analyzers
  reference). One file at the root; every project inherits.
- **`.editorconfig`** (repo root, merge-target) - G3.1's layout rules
  and G3.2's severity map, gating at warning under the zero-warning
  regime.
- **`.github/workflows/sdlc-dotnet.yml`** (kit-owned) - format verify
  plus strict build as chain-free steps, beside the G0 backstop; the
  consumer's own .NET workflows untouched.
- **`.pre-commit-config.yaml`** (merge-target, replaces the base
  entry) - adds the `dotnet format` hook in apply mode, G3.1's fix
  channel.

Fit notes:

- **The build is the gate.** One `dotnet build` evaluates battery and
  strict flags together; the formatter runs apply-mode in the loop,
  verify-mode in CI. Both venues read the identical committed configs -
  venue drift is impossible by construction.
- **Brownfield lands red, deliberately.** The props surface the
  existing warning debt at once; merge-target leaves adoption pace
  with the consumer - init prints snippets beside existing files,
  update reports drift on these two but never applies them. The class
  ruling:
  [0019](../decisions/0019-enforcement-config-drift-classes.md).
- **Severity edits are enforcement-layer changes.** Per-project
  strictness overrides, `<NoWarn>`, and in-source suppressions are
  tamper vectors - and since 0.7.0 the four-vector suppression audit
  (G4.10, `python -m taskcontract suppression-audit`) trips on each
  in CI; severity policy routes through PL-PIPE.1, not the diff.
- **House analyzers are not here yet.** The battery ships stock
  StyleCop + IDE tiers; the custom tranche instantiates at pilot
  activation ([0009](../decisions/0009-custom-analyzer-adoption-policy.md)).

## 🟢 G4 fit notes for .NET shops (unit: dotnet-g4-doc)

The merge gate's mechanical core: `sdlc-dotnet.yml` stops being
inner-loop-only and becomes the G4 venue - four of the gate's eleven
conditions bound, the rest deferred honestly below.

- **The workflow is the gate seed.** `merge_group` joins
  `pull_request` and push-main as triggers: with a merge queue enabled
  the gate evaluates main-at-queue-time (authoritative); the PR run is
  the advisory preview on the test-merge ref. Queue-less fallback,
  binding note: strict serial merges with required-up-to-date
  branches. Branch-protection settings are the consumer's - documented
  here, never kit-written
  ([0020](../decisions/0020-merge-gate-distribution-shape.md)).
- **Echo stands (G4.1).** The three G3 steps are the echo's three
  clauses received: strict build (clause 1), battery in-build
  (clause 2), formatter verify as an explicit step (clause 3). Same
  committed configs, tamper-proof venue.
- **Full test execution (G4.11).** `dotnet test` solution-wide after
  the strict build; zero tests discovered fails the gate; skip
  constructs are the suppression audit's vector-4 material (quarantine
  policy = enforcement-pass config, deferred named line).
- **Secrets (G4.9 clause 1).** gitleaks diff mode over base..head as
  one docker-run step of the MIT image (no org license wall);
  diagnostics masked - a hit means rotate the credential, not just
  remove the line.
- **Dependencies (G4.9 clause 2).** The props audit block turns the
  locked graph on (`RestorePackagesWithLockFile`, `NuGetAuditMode`
  all, NU1901-1904 as errors) and CI restores locked-mode.
  **Brownfield lands red at restore, deliberately** - a repo without
  committed lockfiles fails until they land; merge-target pace, same
  doctrine as the G3 props.
- **Suppression audit (G4.10).** `python -m taskcontract
  suppression-audit` runs from the pinned kit install: four vectors
  (in-source suppressions incl. Skip/Ignore forms, severity
  downgrades, strictness weakening, exclusion widening) over the
  candidate diff, each diagnostic naming the construct, location, and
  the legitimate channel.
- **Deferral register, named:** license allowlist (G4.9 clause 2's
  policy artifact), SLA backstop (G4.9 clause 3, needs G9.2
  tracking), quarantine-list content (enforcement-pass config), and
  the seven unbound conditions G4.2-G4.8 (roadmap step 4).

## ⚪ Gap register - deferred, triggers on record

- **Azure DevOps pipeline variant** - trigger: the first real
  consumer on AzDO; the kit's CI substrate is GitHub Actions until
  then.
- **Husky.NET local hooks** (pre-commit alternative) - trigger: a
  consumer without Python tolerance. The original trigger (the G3
  slice) fired and closed on pre-commit: Python is already the kit's
  local substrate, so the formatter hook rides the existing config;
  Husky.NET remains registered for shops that will not run local
  Python.
- **`dotnet tool` validator wrapper** - trigger: local-Python
  friction reported by a real .NET consumer.
- **Battery-CWE map** (three strata substantiating the taxonomy's
  691/697/703 rows + golden test) - trigger: the first G4.7 scanner
  slice or the next taxonomy session. Banked at the G3 walk as a
  G4-session input; addressed at the G4 slice by re-registration
  (the mechanical core ships venue payload; the map is registry
  substantiation - Husky.NET precedent, ruled in-contract).

## Roadmap - slice order

1. **G0 (shipped, 0.5.0)** - the container: overlay resolution, update
   parity, this page.
2. **G3 (shipped, 0.6.0)** - the first heavy payload:
   `Directory.Build.props` strict compile, `.editorconfig` +
   `dotnet format`, the analyzer battery (stock tiers), and the
   inner-loop workflow job.
3. **G4 mechanical core (shipped, 0.7.0)** - the merge-gate workflow:
   the echo received, full test execution, secrets + dependency audit
   over a locked graph, and the suppression audit as a kit subcommand
   (venue + distribution shape: ADR 0020).
4. **Beyond** - by the consumer's actual defect distribution
   (convergence loop); findings from real C# repos file back as gaps
   or slices here, per the promotion rule in
   [0018](../decisions/0018-tooling-profile-distribution.md):
   project config → profile binding → shape change, each step
   deliberate.
