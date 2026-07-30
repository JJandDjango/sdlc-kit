# Dotnet tooling profile - the kit's C# binding, gate by gate

<!-- covers: specs/dotnet-profile-g0/contract.yaml -->

> **Contract** - one question: *how does the kit bind to a .NET
> consumer, and what ships per gate?*
> Component deep page (MAP row landed with the container, 2026-07-29).
> Feature set ratified in-session 2026-07-29 (F1-F9, nothing struck);
> task contract `specs/dotnet-profile-g0/contract.yaml` - entities
> resolved through `tooling-profile` (ratified at this intake),
> `scaffold`, `consumer`.

**Status legend:** 🔴 ratified, not yet shipped · 🟢 shipped ·
⚪ deferred behind a named trigger. Docs Pass 0 authored 2026-07-29,
before any implementation; markers flip as units land.

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
and one stack-aware next-steps line at init. The dotnet overlay ships
**deliberately empty** at this slice - the first real payload arrives
with the G3 slice below.

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
| G3 implementation | `dotnet format`, analyzer battery (StyleCop + custom Roslyn), strict compile props | 🔴 next slice |
| G4 pre-merge CI | the 11-condition merge queue core (echo, arch tests, suites, ratchets, audits) | 🔴 |
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

## ⚪ Gap register - deferred, triggers on record

- **Azure DevOps pipeline variant** - trigger: the first real
  consumer on AzDO; the kit's CI substrate is GitHub Actions until
  then.
- **Husky.NET local hooks** (pre-commit alternative) - trigger: the
  G3 slice, where local hooks first carry real checks (formatter).
- **`dotnet tool` validator wrapper** - trigger: local-Python
  friction reported by a real .NET consumer.

## Roadmap - slice order

1. **G0 (this task)** - the container: overlay resolution, update
   parity, this page.
2. **G3** - the first heavy payload: `Directory.Build.props` strict
   compile, `.editorconfig` + `dotnet format`, the analyzer battery,
   and the inner-loop workflow job.
3. **G4 mechanical core** - echo, full test execution,
   secret/dependency audit.
4. **Beyond** - by the consumer's actual defect distribution
   (convergence loop); findings from real C# repos file back as gaps
   or slices here, per the promotion rule in
   [0018](../decisions/0018-tooling-profile-distribution.md):
   project config → profile binding → shape change, each step
   deliberate.
