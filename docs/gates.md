# Gates - sdlc_development_kit

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what is each gate, and what conditions attach to it?*
> Living registry - update when a condition is added / specified / enforced or a
> gate changes shape. The source table (`HANDOFF_gate-architecture_2026-07-22.md`
> section 5) stays frozen as provenance. Vocabulary fixed by
> [0003-gate-vocabulary-and-registry](../decisions/0003-gate-vocabulary-and-registry.md).

## Vocabulary

- **Gate** - the blocking enforcement venue at the end of an SDLC phase (one row
  of the source table). Stable IDs `G0`-`G10`, plus cross-cutting `PL-DOC` and
  `PL-PIPE` for the two parallel lifecycles.
- **Condition** - an individual check attached to a gate, ID `Gn.m`. Kind is
  `mechanical` (emits machine-actionable diagnostics an agent can loop against -
  THEORY's loopability invariant binds these) or `human` (judgment checkpoints -
  concentrated at G1 and G6 by design; they do not claim loopability).
- **Condition lifecycle** - `registered` (named, check intent fixed) ->
  `specified` (exact mechanical pass condition and parameters fixed) ->
  `enforced` (live and blocking in its venue). **Per-condition states are
  carried on each gate's Deep-page line; the count line under the overview
  totals them.** Where a near-final pass
  shape already exists it appears in the Check column, open parameters flagged.
- **Numbering provenance** - the original session table ran phases 1-7 with an
  addendum adding 0, 5.5, 8, 9; the handoff merged these to 0-10 (5.5 UAT -> 6,
  Release -> 7, Operations -> 8, Maintenance -> 9, Deprecation -> 10).

**Mutability model** (applies everywhere): the Developer agent's sole write
surface is implementation + unit tests (G3's artifacts). Every spec artifact
authored at G0-G2 is immutable to the implementer, enforced mechanically by
G4.6 - never by prompt instructions. Gate configurations themselves are
enforcement-layer artifacts governed by PL-PIPE. Operators per the harness
design: Spec agent authors G0-G2 artifacts, Developer works only inside G3, QA
executes G4-G6, Verifier is cross-cutting (gate integrity, immutability diffs).

## Open-parameter index

Conditions with unresolved parameters link here; the questions live in
`STATE.md` (mirrored from handoff section 8).

| Ref | Open question | Conditions affected |
|---|---|---|
| Q1 | Spec-path immutability mechanism (protected dirs + CI diff vs CODEOWNERS vs separate repo) | G4.6, PL-PIPE.1 |
| Q3 | Which house conventions become custom analyzers first | G3.2 |
| Q4 | Threshold selection: mutation floor, complexity budgets, ratchet cadence | G4.8, G5.5, G9 (authored policy) |
| Q7 | Enforcement-layer change-control workflow | PL-PIPE.1 |
| Q8 | Which components merit formal models | G1.2, G2.1, G5.6 |

(Q2 resolved 2026-07-23 -> [0005](../decisions/0005-task-contract-fields.md).
Q5 two-channel decorrelation and Q6 pilot selection are harness/rollout
questions, not condition parameters.)

## Overview

| ID | Gate | Venue | Cadence | FAIL blocks | Conditions |
|---|---|---|---|---|---|
| G0 | Planning / Intake | harness intake step | per task | task entering spec | 1 |
| G1 | Requirements / Spec | spec sign-off | per task | spec release downstream | 3 |
| G2 | Design / Architecture | design sign-off + baseline lock | per task | implementation start | 5 |
| G3 | Implementation | editor / local build | seconds | code leaving the inner loop | 3 |
| G4 | Pre-merge CI | merge queue | minutes | merge to main | 9 |
| G5 | Integration / System | nightly pipeline | hours, nightly | promotion to release candidate | 6 |
| G6 | UAT / Staging | staging environment | per candidate | candidate acceptance | 2 |
| G7 | Release / Deploy | release pipeline | per release | deploy; rollout continuation | 4 |
| G8 | Operations | production runtime | continuous | further rollout; convergence closure | 3 |
| G9 | Maintenance / Evolution | scheduled jobs | weekly+ | dependency merge; SLA compliance | 3 |
| G10 | Deprecation / Retirement | build + scheduled | sunset-driven | merge past sunset; retirement completion | 3 |
| PL-DOC | Documentation lifecycle | CI + scheduled sweep | per merge / dated | doc-touching merges | 3 |
| PL-PIPE | Pipeline integrity | separate approval channel + CI | per gate-config change | enforcement-layer edits | 3 |

48 conditions total - 3 `specified` (G0.1, G1.1, G1.3), 45 `registered`.

---

## G0 - Planning / Intake

**Purpose:** reject malformed work before it enters the pipeline - a malformed
task defeats every downstream gate; mis-selection is the dominant upstream
failure for agent pipelines.
**Venue & cadence:** harness intake step, per task, before any spec authoring.
**Inputs:** candidate task.
**Authored here -> downstream gate material:** task contract - scope, explicit
non-goals, decomposition into independently gateable units. Becomes G1's input
and the scope baseline every later gate implicitly checks against.
**FAIL blocks:** the task entering the spec stage.
**Closes:** mis-selection, scope creep (upstream of misinterpretation).
**Deep page:** [gates/G0-planning-intake.md](gates/G0-planning-intake.md) - G0.1 `specified`; enforcement mechanism shipped ([0006](../decisions/0006-task-contract-enforcement.md), [task-contract.md](task-contract.md)) - `enforced` awaits the intake venue (Q6).

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G0.1 | Definition-of-ready check | mechanical | Contract at `specs/<id>/contract.yaml` validates against `schemas/task-contract.schema.json` (`ready` profile): fields present + bounded, every unit sketched, all dependencies resolved | `python -m taskcontract validate` (jsonschema) | [0005](../decisions/0005-task-contract-fields.md), [0006](../decisions/0006-task-contract-enforcement.md) |

## G1 - Requirements / Spec

**Purpose:** fix *what correct means* - spec artifacts authored before and
independently of the implementation, mechanically checkable downstream.
**Venue & cadence:** spec sign-off at the harness spec-stage exit, per task.
**Inputs:** accepted task contract (G0).
**Authored here -> downstream gate material:** numbered acceptance criteria
(REQ-IDs); immutable acceptance tests; property + metamorphic specs; boundary
schemas (OpenAPI/protobuf); formal models for hard cores (TLA+/P); naive
reference implementation for differential-gated components (catalog pattern 6);
approval snapshots (`.approved.*`, pattern 5). Enforced
downstream at G4.3-G4.6, G5.1, G5.2, G5.5, G5.6.
**FAIL blocks:** release of the spec set - design and implementation cannot
start against an unlinted or ambiguous spec.
**Operator note:** Spec agent, context decorrelated from the Developer
(two-channel principle; mechanism is open question Q5).
**Closes:** requirements misinterpretation (ODC function).
**Deep page:** [gates/G1-requirements-spec.md](gates/G1-requirements-spec.md) - G1.1, G1.3 `specified`; G1.2 `registered` (Q8).

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G1.1 | Spec/schema linting | mechanical | Boundary schemas and spec files lint clean | Spectral, `buf lint` | - |
| G1.2 | Model checking | mechanical | Formal models for hard cores check clean pre-implementation | TLA+/TLC, P | Q8 |
| G1.3 | Criteria completeness + ambiguity review | human | Numbered criteria are complete, unambiguous, testable - the concentration point of human attention in the whole pipeline | review checklist | - |

## G2 - Design / Architecture

**Purpose:** fix the *shape* - types, surfaces, structure rules - so generation
lands inside the valid space (correct-by-construction over detect-after).
**Venue & cadence:** design sign-off + baseline lock, per task/component.
**Inputs:** signed-off spec set (G1).
**Authored here -> downstream gate material:** interface + domain-type
scaffolding; `PublicAPI.Shipped.txt` baseline; architecture rule tests
(NetArchTest); typestate encodings; ratchet baselines (complexity, coverage);
threat model (STRIDE per trust boundary) -> abuse cases compiled into security
acceptance tests. Enforced downstream at G4.2, G4.5, G4.8, G7.2.
**FAIL blocks:** implementation start - without locked baselines there is
nothing to gate the implementation against.
**Closes:** API misuse, concurrency design flaws, architectural erosion,
design-level security flaws.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G2.1 | Design-level model checking | mechanical | Concurrency/protocol designs model-check clean before code exists | TLA+/TLC, Alloy, P | Q8 |
| G2.2 | Breaking-change baseline lock | mechanical | API surface and schema baselines exist and are locked before implementation begins | PublicApiAnalyzers, schema baselines | - |
| G2.3 | ADR review | human | Significant design choices are recorded and reviewed | `decisions/` | - |
| G2.4 | Threat-model existence | mechanical | Every component crossing a trust boundary has a STRIDE threat model, with abuse cases compiled into security acceptance tests | STRIDE process | - |
| G2.5 | Spec-suite red run | mechanical | Acceptance + property suites compile against the locked scaffold and every unimplemented criterion's test fails (red) before implementation starts | test runner | - |

G2.5 added 2026-07-23 by ratified completeness finding - design source:
[gates/G1-requirements-spec.md](gates/G1-requirements-spec.md) (completeness
check), per [0004](../decisions/0004-per-gate-documentation-program.md).

## G3 - Implementation (inner loop)

**Purpose:** keep the inner loop clean at zero human cost - every violation
surfaced in seconds with a machine-applicable fix wherever possible.
**Venue & cadence:** editor / local build, seconds per iteration.
**Inputs:** working diff - implementation + unit tests, the only agent-mutable
artifacts in the pipeline.
**Authored here -> downstream gate material:** implementation + unit tests.
**FAIL blocks:** code leaving the inner loop (local build stays red).
**Operator note:** the Developer agent's only write surface.
**Closes:** type/null misuse (CWE-476, 457), resource lifetime (CWE-664, 772),
convention drift.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G3.1 | Formatter | mechanical | Zero formatting diffs | `dotnet format`, `.editorconfig` | - |
| G3.2 | StyleCop + custom Roslyn analyzers | mechanical | Analyzer set clean; house conventions encoded as analyzers with code-fix providers (auto-fixable preferred) | StyleCop.Analyzers, custom Roslyn | Q3 |
| G3.3 | Strict compile | mechanical | Builds with `Nullable` enable, `TreatWarningsAsErrors`, `AnalysisLevel latest-all` | compiler configuration | - |

## G4 - Pre-merge CI

**Purpose:** the merge is the last cheap moment to stop a defect - everything
decidable in minutes blocks here.
**Venue & cadence:** merge queue / PR CI, minutes.
**Inputs:** candidate diff + full build of the merged result.
**Authored here -> downstream gate material:** regression tests from review
findings.
**FAIL blocks:** merge to main.
**Operator note:** QA agent owns execution; G4.6 is part of the Verifier's
deterministic core. The CI definition itself is enforcement-layer (PL-PIPE).
**Closes:** injection (CWE-707: 79, 89, 78), calculation (CWE-682), error
handling (CWE-703), architectural erosion; misinterpretation via traceability.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G4.1 | Full analyzer set | mechanical | Entire analyzer battery clean on the merged build (superset of the G3 run) | Roslyn analyzer set | - |
| G4.2 | Architecture tests | mechanical | Dependency and layering rules hold | NetArchTest | - |
| G4.3 | Acceptance suite + REQ-ID traceability | mechanical | Acceptance tests green AND every REQ-ID maps to >=1 passing test via `[Criterion("REQ-nnn")]`-style annotations | test runner + CI traceability script | format + script = candidate next-step 3 |
| G4.4 | Property tests | mechanical | Property/metamorphic suites green | FsCheck/CsCheck | - |
| G4.5 | API surface diff | mechanical | No unapproved public-surface change - code (`PublicAPI.Shipped.txt`), HTTP (oasdiff), proto (`buf breaking`) | PublicApiAnalyzers, oasdiff, buf | - |
| G4.6 | Spec-path immutability | mechanical | Any diff touching a spec path (acceptance tests, criteria, schemas, baselines, `.approved.*`) fails the build - never prompt-enforced | CI diff check | Q1 |
| G4.7 | Taint/security scan | mechanical | No new taint/dataflow findings | CodeQL, Semgrep | - |
| G4.8 | Duplication + complexity ratchets | mechanical | Both metrics <= current baseline; baseline only ever tightens | jscpd / PMD CPD, complexity ratchet | Q4 |
| G4.9 | Secret/dependency audit | mechanical | No secrets in the diff; no known-vulnerable dependencies | secret scan, dependency audit | - |

## G5 - Integration / System

**Purpose:** catch what only whole-system execution reveals - and prove the
spec suite itself has teeth.
**Venue & cadence:** nightly pipeline, hours. Slow gates still block release -
cost sets cadence, never rigor.
**Inputs:** merged main build.
**Authored here:** - (execution-only gate).
**FAIL blocks:** promotion to release candidate.
**Closes:** interaction bugs, concurrency (CWE-362, 667), parsing/input
validation (CWE-20), vacuous specs.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G5.1 | Consumer-driven contract verification | mechanical | Provider verifies all consumer pacts | PactNet | - |
| G5.2 | Differential testing | mechanical | Optimized implementation equivalent to the naive reference (authored at spec stage) over generated inputs - strongest oracle for algorithmic code | reference implementation + generators | - |
| G5.3 | Fuzzing | mechanical | No crashes/hangs on corpus + newly generated inputs | SharpFuzz | - |
| G5.4 | Systematic concurrency testing | mechanical | Scheduled-interleaving exploration runs clean | Coyote | - |
| G5.5 | Mutation threshold | mechanical | Mutation score >= floor on changed code - gates the *spec's adequacy*, closing the vacuous-test loophole | Stryker.NET | Q4 |
| G5.6 | Model trace-conformance | mechanical | Implementation traces conform to the checked formal model | TLA+/P trace checking | Q8 |

## G6 - UAT / Staging

**Purpose:** catch conformant-but-wrong - the code a mechanically satisfied
spec still permits (the oracle problem's residue).
**Venue & cadence:** production-like staging environment, per release candidate.
**Inputs:** candidate promoted by G5.
**Authored here -> downstream gate material:** findings -> new acceptance
criteria (convergence loop into G1).
**FAIL blocks:** candidate acceptance.
**Closes:** residual requirements misinterpretation.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G6.1 | Human validation against REQ-IDs | human | Walk the numbered criteria in a production-like environment | staging environment | - |
| G6.2 | Exploratory testing | human | Unscripted probing beyond the criteria; findings become new REQ-IDs | - | - |

## G7 - Release / Deploy

**Purpose:** nothing ships that regresses performance, compatibility, or
infrastructure safety.
**Venue & cadence:** release pipeline, per release.
**Inputs:** accepted candidate (G6).
**Authored here -> downstream gate material:** performance budgets;
SBOM/provenance.
**FAIL blocks:** the deploy; a failing canary auto-reverts the rollout.
**Closes:** performance (CWE-400, 407); build/config/deployment (ODC
build/package).

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G7.1 | Benchmark budgets | mechanical | Benchmarks within authored budgets vs baseline | BenchmarkDotNet + CI comparison | - |
| G7.2 | ApiCompat binary compatibility | mechanical | Shipped binaries compatible with the locked baseline | Microsoft.DotNet.ApiCompat | - |
| G7.3 | IaC scanning | mechanical | Infrastructure-as-code scan clean | IaC scanners | - |
| G7.4 | Canary with SLO-based rollback | mechanical | Canary meets SLO criteria or rollout auto-reverts | deploy tooling | - |

## G8 - Operations

**Purpose:** turn every escaped defect into an upstream gate - the convergence
loop that tunes the gate set to the actual defect distribution instead of the
generic taxonomy.
**Venue & cadence:** production runtime, continuous.
**Inputs:** live traffic, telemetry, incidents.
**Authored here -> downstream gate material:** new acceptance criteria +
regression tests from incidents, fed back to G1 as immutable spec artifacts.
**FAIL blocks:** further rollout (error budget); an escape that does not
produce a new criterion is itself a process failure.
**Closes:** escaped defects - by conversion, not prevention.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G8.1 | Runtime contract assertions | mechanical | Contract assertions with telemetry stay silent in production | telemetry | - |
| G8.2 | SLO / error-budget alerts | mechanical | SLOs within budget; breach halts further rollouts | monitoring | - |
| G8.3 | Crash triage | human | Every crash triaged; escapes convert to new REQ-IDs + regression tests | triage process | - |

## G9 - Maintenance / Evolution

**Purpose:** hold the line between features - supply-chain rot and slow entropy
accrue in the quiet weeks, not inside feature work.
**Venue & cadence:** scheduled jobs, weekly+ cadence.
**Inputs:** dependency ecosystem changes, vulnerability feeds, aging baselines.
**Authored here -> downstream gate material:** dependency update policy;
scheduled ratchet tightening (cadence is open question Q4); refactoring budgets.
**FAIL blocks:** dependency merge; an SLA breach escalates.
**Closes:** supply-chain rot; slow entropy accruing between features.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G9.1 | Dependency PRs gated by full suite | mechanical | Automated dependency updates merge only through G4 + G5 | update bot + full gate stack | - |
| G9.2 | Vulnerability-fix SLAs | mechanical | Known vulnerabilities fixed within the policy window | dependency audit | - |
| G9.3 | License audit | mechanical | No disallowed licenses in the dependency set | license audit | - |

## G10 - Deprecation / Retirement

**Purpose:** force deletion - agents add code and almost never delete it;
without an explicit removal phase the codebase grows monotonically regardless
of every other gate.
**Venue & cadence:** build (analyzer escalation) + scheduled, sunset-date
driven.
**Inputs:** deprecation marks, migration specs, consumer contract diffs.
**Authored here -> downstream gate material:** sunset dates on `[Obsolete]`;
migration specs; consumer notification via contract diff.
**FAIL blocks:** merges past a sunset date; retirement completion without
verified migration.
**Closes:** accretion.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G10.1 | Obsolete-sunset escalation | mechanical | `[Obsolete]` warning escalates to error at the sunset date | custom analyzer | - |
| G10.2 | Dead-code ratchet | mechanical | Dead-code count <= baseline, trending down | dead-code detection | - |
| G10.3 | Data-migration verification | mechanical | Migrations verified before the old path is removed | migration tests | - |

## PL-DOC - Documentation lifecycle (cross-cutting)

**Purpose:** for agent pipelines documentation is injected context, so
staleness is a defect *vector*, not a cosmetic issue.
**Venue & cadence:** CI on doc-touching merges + scheduled staleness sweep.
Pace-layered: fast layers get automated drift gates; slow layers get
change-control review.
**FAIL blocks:** doc-touching merges; stale docs flagged before reuse as
context.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| PL-DOC.1 | Doc samples compile/execute | mechanical | Every code sample in docs compiles/runs in CI | doc-sample harness | - |
| PL-DOC.2 | Doc coverage | mechanical | Coverage analyzer clean over the public surface | coverage analyzers | - |
| PL-DOC.3 | Staleness dating | mechanical | Docs carry dates; stale-past-threshold entries flagged | dating check | - |

## PL-PIPE - Pipeline integrity (cross-cutting)

**Purpose:** the enforcement layer is the highest-privilege artifact set - a
developer agent that can edit the workflow file can delete every gate in one
diff.
**Venue & cadence:** separate approval channel + CI self-tests, per
enforcement-layer change.
**Scope:** gate definitions, CI config, analyzer rulesets, agent prompts, spec
paths - and this registry itself.
**FAIL blocks:** any enforcement-layer edit lacking second-channel approval.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| PL-PIPE.1 | Enforcement-layer change control | human | Gate-config edits approved through a channel separate from what they enforce | approval workflow | Q7, Q1 |
| PL-PIPE.2 | Gate-config golden tests | mechanical | Gate configurations pass their own regression suite | golden tests | - |
| PL-PIPE.3 | Agent-behavior evals | mechanical | Agent prompts pass behavioral evals before deployment | eval suite | - |

---

## Cross-references

The eight spec-first patterns with their authored-at / enforced-by mapping
live in [catalog.md](catalog.md). The bug-class taxonomy anchoring each
gate's **Closes** line, with per-class ladder positions and the gap-analysis
method, lives in [taxonomy.md](taxonomy.md).
