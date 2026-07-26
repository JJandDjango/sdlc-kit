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
- **Two-layer model**
  ([0008](../decisions/0008-two-layer-condition-model.md)) - a condition's
  pass condition is authored as a language-agnostic **shape**; the
  Check/Tooling columns and deep-page binding sections are the **reference
  profile (.NET)**. Additional per-ecosystem profiles bind shapes without
  changing them; a profile that cannot reach a shape registers a kit build
  item (gap-closure directive), which gates that profile's `enforced` flip -
  never the shape's `specified`.

**Mutability model** (applies everywhere): the Developer agent's sole write
surface is implementation + unit tests (G3's artifacts). Every spec artifact
authored at G0-G2 is immutable to the implementer, enforced mechanically by
G4.6 ([0010](../decisions/0010-write-surface-immutability.md)) - never by
prompt instructions. Gate configurations themselves are
enforcement-layer artifacts governed by PL-PIPE. Operators per the harness
design: Spec agent authors G0-G2 artifacts, Developer works only inside G3, QA
executes G4-G7 (the human principal grades G6.1/G6.2; the operations
principal grades G8.3), Verifier is cross-cutting (gate integrity,
immutability diffs).

## Open-parameter index

Conditions with unresolved parameters link here; the questions live in
`STATE.md` (mirrored from handoff section 8).

| Ref | Open question | Conditions affected |
|---|---|---|
| Q4 | Threshold selection, numeric only - shapes closed through G10: mutation floor + small-N cutoff (G5.5 - procedure fixed S9), complexity budgets + capture parameters (G4.8), benchmark ceilings/margins/statistic defaults (G7.1 - procedure fixed S10), canary confidence + minimum-sample constants (G7.4), and every clock in the clocks artifact - SLA windows (severity x exposure), remediation/disposition/breach windows, notice floors, drainage window, tightening + sweep + attestation cadences (0012 - S11) | G4.8, G5.5, G7.1, G7.4, clocks.yaml (0012) |
| Q7 | Enforcement-layer change-control workflow | PL-PIPE.1 |

(Q2 resolved 2026-07-23 -> [0005](../decisions/0005-task-contract-fields.md);
Q8 resolved 2026-07-23 ->
[0007](../decisions/0007-hard-core-designation-criteria.md);
Q3 resolved 2026-07-24 ->
[0009](../decisions/0009-custom-analyzer-adoption-policy.md) - policy, not
list; first-tranche instantiation rides pilot activation (Q6).
Q1 resolved 2026-07-24 ->
[0010](../decisions/0010-write-surface-immutability.md) - write-surface
manifest + CI diff audit, allowlist polarity, channel provenance; G4.6
renamed. Q7 carries a worked example on record (0010/G4.8):
direction-conditional channel weight - tightenings auto-approve,
loosenings take the full second channel.
Q5 two-channel decorrelation and Q6 pilot selection are harness/rollout
questions, not condition parameters; named Q5 sub-question on record: what
the Developer's context contains - test source vs criteria + diagnostics
(session-7 anti-gaming finding).)

## Overview

| ID | Gate | Venue | Cadence | FAIL blocks | Conditions |
|---|---|---|---|---|---|
| G0 | Planning / Intake | harness intake step | per task | task entering spec | 1 |
| G1 | Requirements / Spec | spec sign-off | per task | spec release downstream | 3 |
| G2 | Design / Architecture | design sign-off + baseline lock | per task | implementation start | 5 |
| G3 | Implementation | editor / local build | seconds | code leaving the inner loop | 3 |
| G4 | Pre-merge CI | merge queue (PR CI = preview) | minutes | merge to main | 11 |
| G5 | Integration / System | pinned-snapshot pipeline | hours (schedule = policy) | promotion to release candidate | 7 |
| G6 | UAT / Staging | certified staging environment | per candidate, principal-paced | candidate acceptance | 3 |
| G7 | Release / Deploy | release pipeline | per release | deploy; rollout continuation | 5 |
| G8 | Operations | production runtime | continuous | further rollout; convergence closure | 3 |
| G9 | Maintenance / Evolution | scheduled jobs | weekly+ (clocks.yaml) | dependency merge; aging breaches -> standing reds | 4 |
| G10 | Deprecation / Retirement | build + scheduled | sunset-driven | merge past sunset; retirement completion | 3 |
| PL-DOC | Documentation lifecycle | CI + scheduled sweep | per merge / dated | doc-touching merges | 3 |
| PL-PIPE | Pipeline integrity | separate approval channel + CI | per gate-config change | enforcement-layer edits | 3 |

54 conditions total - 48 `specified` (G0.1, G1.1-G1.3, G2.1-G2.5,
G3.1-G3.3, G4.1-G4.11, G5.1-G5.7, G6.1-G6.3, G7.1-G7.5, G8.1-G8.3,
G9.1-G9.4, G10.1-G10.3), 6 `registered`.

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
**Deep page:** [gates/G1-requirements-spec.md](gates/G1-requirements-spec.md) - G1.1, G1.2, G1.3 all `specified`; G1.2's designation criteria ratified in [0007](../decisions/0007-hard-core-designation-criteria.md).

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G1.1 | Spec/schema linting | mechanical | Boundary schemas and spec files lint clean | Spectral, `buf lint` | - |
| G1.2 | Model checking | mechanical | Formal models for hard cores check clean pre-implementation | TLA+/TLC, P | [0007](../decisions/0007-hard-core-designation-criteria.md) |
| G1.3 | Criteria completeness + ambiguity review | human | Numbered criteria are complete, unambiguous, testable - the concentration point of human attention in the whole pipeline | review checklist | - |

## G2 - Design / Architecture

**Purpose:** fix the *shape* - types, surfaces, structure rules - so generation
lands inside the valid space (correct-by-construction over detect-after).
**Venue & cadence:** design sign-off + baseline lock, per task/component.
**Inputs:** signed-off spec set (G1).
**Authored here -> downstream gate material:** interface + domain-type
scaffolding; `PublicAPI.Shipped.txt` baseline; architecture rule tests
(NetArchTest); typestate encodings; ratchet baselines for the metrics G4.8
enforces; performance budgets + SLO declarations (`slo.yaml`, S10);
threat model (STRIDE per trust boundary) -> abuse cases compiled
into security acceptance tests. Enforced downstream at G4.2, G4.3, G4.5,
G4.8, G7.1, G7.2, G7.4, G8.2.
**FAIL blocks:** implementation start - without locked baselines there is
nothing to gate the implementation against.
**Closes:** API misuse, concurrency design flaws, architectural erosion,
design-level security flaws.
**Deep page:** [gates/G2-design-architecture.md](gates/G2-design-architecture.md) - G2.1-G2.5 all `specified`; G2.1 consumes [0007](../decisions/0007-hard-core-designation-criteria.md); ratchet-baseline enforcement exported to the G4 session.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G2.1 | Design-level model checking | mechanical | Concurrency/protocol designs model-check clean before code exists | TLA+/TLC, Alloy, P | [0007](../decisions/0007-hard-core-designation-criteria.md) |
| G2.2 | Breaking-change baseline lock | mechanical | API surface and schema baselines exist and are locked before implementation begins | PublicApiAnalyzers, schema baselines | - |
| G2.3 | ADR review | human | Significant design choices are recorded and reviewed | `decisions/` | - |
| G2.4 | Threat-model existence | mechanical | Every component crossing a trust boundary has a STRIDE threat model, with abuse cases compiled into security acceptance tests | STRIDE process | - |
| G2.5 | Spec-suite red run | mechanical | Acceptance + property suites compile against the locked scaffold and every unimplemented criterion's test fails (red) before implementation starts | test runner | - |

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
numeric overflow (CWE-682, trap half), incorrect comparison (CWE-697),
non-concurrency control flow (CWE-691 remainder), convention drift.
**Deep page:** [gates/G3-implementation.md](gates/G3-implementation.md) -
G3.1-G3.3 all `specified`; first page under the two-layer model
([0008](../decisions/0008-two-layer-condition-model.md)); Q3 closed by
[0009](../decisions/0009-custom-analyzer-adoption-policy.md).

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G3.1 | Formatter | mechanical | Zero formatting diffs: verify mode exits clean tree-wide; total fixer, layout only | `dotnet format whitespace`, `.editorconfig` | - |
| G3.2 | Analyzer battery | mechanical | Declared analyzer set clean at gating severity *and unweakened* (no new in-source suppressions); house conventions encoded as analyzers with code-fix providers (auto-fixable preferred) | StyleCop.Analyzers, custom Roslyn, `EnforceCodeStyleInBuild` | [0009](../decisions/0009-custom-analyzer-adoption-policy.md); tranche at Q6 |
| G3.3 | Strict compile | mechanical | Builds with `Nullable` enable, `TreatWarningsAsErrors`, `AnalysisLevel latest-all`, checked arithmetic, unsafe off | compiler configuration (`Directory.Build.props`) | - |

## G4 - Pre-merge CI

**Purpose:** the merge is the last cheap moment to stop a defect - everything
decidable in minutes blocks here.
**Venue & cadence:** merge queue (authoritative) / PR CI (advisory preview),
minutes. Queue semantics required: conditions evaluate the merged result
against main-at-queue-time.
**Inputs:** candidate diff + full build of the merged result.
**Authored here:** - (execution-only gate; ruled session 8 - the source
table's "regression tests from review findings" was human-SDLC residue;
conversion loops live at G6/G8.3).
**FAIL blocks:** merge to main.
**Operator note:** QA agent executes the result-scoped conditions; the
Verifier's deterministic core owns the diff-scoped subject checks (G4.6 +
G4.10, one write-surface audit job). The CI definition itself is
enforcement-layer (PL-PIPE). Zero human conditions - the pipeline's largest
fully-mechanical gate.
**Closes:** injection (CWE-707: 79, 89, 78), calculation (CWE-682), error
handling (CWE-703), architectural erosion + duplication entropy,
secret/vulnerable-dependency introduction, misinterpretation via
traceability - and agent self-weakening (subject integrity: G4.5/G4.6/G4.10).
**Deep page:** [gates/G4-pre-merge-ci.md](gates/G4-pre-merge-ci.md) -
G4.1-G4.11 all `specified`; roster 9 -> 11 (G4.10 suppression audit, G4.11
full test execution adopted); Q1 closed by
[0010](../decisions/0010-write-surface-immutability.md); traceability format
fixed by [0011](../decisions/0011-criterion-traceability-format.md); renames
G4.1 + G4.6 per the 0008 precedent.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G4.1 | Inner-loop echo | mechanical | Merged result builds under identical committed strict config; declared battery clean at gating severity (superset: add, never drop); formatter verify-mode clean as explicit step | Roslyn battery, `dotnet format`, committed props | - |
| G4.2 | Architecture tests | mechanical | Arch-rule partition green on the merged result; per-rule + violating-edge diagnostics; traces to ADRs, not REQ-IDs | NetArchTest | - |
| G4.3 | Acceptance suite + REQ-ID traceability | mechanical | Acceptance + security partitions green AND traceability total: every criterion >=1 passing witness, every spec-suite test annotated, no dangling refs - computed from `criteria.yaml` x runner results | test runner + traceability script (pass mode) | [0011](../decisions/0011-criterion-traceability-format.md) |
| G4.4 | Property tests | mechanical | Property/metamorphic partition green under derived seed f(base sha, candidate sha); diagnostic carries seed + shrunk counterexample | FsCheck/CsCheck | - |
| G4.5 | API surface diff | mechanical | Every declared surface equals its locked baseline, bidirectional; spec-channel candidates get breaking-classification as report | PublicApiAnalyzers (RS0016/17), oasdiff, buf | - |
| G4.6 | Write-surface immutability | mechanical | Candidate diff (merged result vs main-at-queue) lands inside the manifest's writable set, or carries channel provenance (S: spec sign-off; E: PL-PIPE.1); no implementation bypass; manifest missing = FAIL | write-surface audit job (CI diff) | [0010](../decisions/0010-write-surface-immutability.md) |
| G4.7 | Taint/security scan | mechanical | Zero findings at gating severity on the merged result (ratchet-at-zero, not baseline-relative); FP dismissals only via committed class-E suppression config | CodeQL, Semgrep | - |
| G4.8 | Duplication + complexity ratchets | mechanical | Duplication <= captured shrink-only baseline; complexity per authored per-method budgets, violation count ratcheted (zero at greenfield); baselines static between G9 tightenings; missing = FAIL | jscpd / PMD CPD, CA1502/1505/1506 thresholds | Q4 (numbers) |
| G4.9 | Secret/dependency audit | mechanical | No secret material in the diff (masked, rotation-first); dependency delta over the locked graph introduces no advisory-matched or license-disallowed package; nothing past its G9.2 SLA window | gitleaks, NuGetAudit + lockfile, license allowlist | - |
| G4.10 | Suppression audit | mechanical | Candidate diff introduces no weakening - four vectors: in-source suppressions/skips, severity downgrades, strictness overrides, exclusion widening | write-surface audit job | - |
| G4.11 | Full test execution | mechanical | Entire discovered suite green on the merged result, unit partition included; zero tests = FAIL; skips zero outside committed quarantine | `dotnet test` solution-wide | - |

## G5 - Integration / System

**Purpose:** catch what only whole-system execution reveals - and prove the
spec suite itself has teeth (the distribution oracles + the sensitivity
floor).
**Venue & cadence:** deep-verification tier over **pinned snapshots** of
main - one sha per run; promotion promotes the verified artifact, never a
rebuild. Budget-class hours; the schedule is policy, not shape ("nightly" =
the reference default; rolling / on-demand runs satisfy the same shape).
Slow gates still block release - cost sets cadence, never rigor.
**Inputs:** the pinned snapshot (merged main build).
**Authored here:** - (execution-only gate; discovered state - corpus
growth, minimized crashers - lands as tightening candidates through the
merge queue, 0010's direction-conditional lane).
**FAIL blocks:** promotion to release candidate. Red seizes promotion,
never merges; past its remediation window (clocks.yaml) it escalates to
stop-the-line at task intake (fix lane via the 0012 `fixes` field;
numbers Q4).
**Operator note:** pure QA execution - subject integrity inherited from
G4's diff policing; no Verifier, no human. Fresh exploration each run;
every red ships a replay recipe; no retry-to-green.
**Closes:** interaction bugs, concurrency (CWE-362, 667), parsing/input
validation (CWE-20), vacuous specs, resource-trend defects (CWE-400 trend
class), native-interop memory safety (via G5.3's mandatory-fuzz
disposition).
**Deep page:** [gates/G5-integration-system.md](gates/G5-integration-system.md) -
G5.1-G5.7 all `specified`; roster 6 -> 7 (G5.7 soak/resource-trend adopted
at close-out); G5.2 renamed; the oracle-designation rubric ruled (G1
declaration record, G1.3-reviewed); G5.5's floor procedure fixed (numbers
stay Q4); G5.6's conformance criteria fixed.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G5.1 | Consumer-driven contract verification | mechanical | Declared-consumer registry x accepted pact set closed both directions; the real built provider verifies every accepted pact; unaccepted versions verify as advisory report | PactNet | - |
| G5.2 | Differential + deep property campaign | mechanical | Optimized equivalent to the spec-authored naive reference over generated inputs under the declared equivalence relation (error agreement included); property/metamorphic suites re-run at campaign budget under fresh seeds | reference implementation + generators, CsCheck/FsCheck | - |
| G5.3 | Fuzzing | mechanical | No crashes/hangs/sanitizer findings on corpus + fresh inputs for every declared target; corpus grows via tightening candidates; interop wrappers mandatorily fuzz-gated | SharpFuzz | - |
| G5.4 | Systematic concurrency testing | mechanical | Scheduled-interleaving exploration clean for every concurrency-gated component; declared set >= tripwire-detected set; failures ship replayable schedules | Coyote | - |
| G5.5 | Mutation threshold | mechanical | Mutation score >= floor on code changed since the last green run (zero survivors below the small-N cutoff) - gates the *spec's adequacy*; G4.11 is the named precondition | Stryker.NET | Q4 (numbers; procedure fixed) |
| G5.6 | Model trace-conformance | mechanical | Mapped implementation traces are admissible behaviors of the checked model; action coverage + mapping totality; zero traces = FAIL | TLA+/P trace checking | [0007](../decisions/0007-hard-core-designation-criteria.md) |
| G5.7 | Soak / resource-trend | mechanical | Soak-designated components run sustained scenarios: no unbounded resource-growth trend, zero crashes over the window; trend shapes gate - absolute budgets stay G7 | dotnet-counters + trend assertion | - |

## G6 - UAT / Staging

**Purpose:** catch conformant-but-wrong - the code a mechanically satisfied
spec still permits (the oracle problem's residue).
**Venue & cadence:** production-like staging reached only through G6.3's
certified deploy path; per candidate, principal-paced (G5 emits a rolling
stream of promotable snapshots; G6 draws at the principal's pace - no 1:1
coupling).
**Inputs:** promoted candidate (verified artifact); delta criteria records
(0011); prior acceptance record.
**Authored here -> downstream gate material:** findings -> new acceptance
criteria through the front door (Spec agent drafts, G1.3 reviews, G2.5
arms red - the convergence loop into G1); the per-candidate acceptance
record (class S) that G7's admission mechanically consumes.
**FAIL blocks:** candidate acceptance; default-deny - no record = not
accepted.
**Operator note:** QA operates the venue (certified deploy, walk sheets,
recording, assistive scouting - suggestions never verdicts); **the human
principal grades** - non-delegable: an agent's only oracle is the spec
text, and G6 exists to catch what the spec text missed.
**Closes:** residual requirements misinterpretation; venue drift (G6.3).
**Deep page:** [gates/G6-uat-staging.md](gates/G6-uat-staging.md) -
G6.1-G6.3 all `specified`; roster 2 -> 3 (G6.3 venue certification adopted
at close-out); the acceptance record ruled (class S, G7-consumed).

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G6.1 | Human validation against REQ-IDs | human | Walk the delta criteria (new/changed since last acceptance) in the certified environment; per-criterion verdicts recorded; findings indict the spec layer; accept-with-findings = auto-armed forward obligation | staging environment + criteria.yaml walk sheet | - |
| G6.2 | Exploratory testing | human | Timeboxed unscripted probing beyond the criteria; principal grades (agent scouting = suggestions only); validated findings become new REQ-IDs; session attested even at zero findings | - | - |
| G6.3 | Venue certification | mechanical | Candidate reached staging via the committed environment definition through the production deploy path; deviations only per the declared-delta allowlist; certification recorded or the walk cannot start | environment definition + deploy pipeline (class E) | - |

## G7 - Release / Deploy

**Purpose:** nothing ships that regresses performance, compatibility,
infrastructure safety, or artifact integrity - the mechanical re-entry
after the human boundary.
**Venue & cadence:** release pipeline - the same committed definition
and deploy path G6.3 certifies, parameterized by target - per release.
Deploy timing is business policy: G7 rules whether a release *may*
ship, never when it must.
**Inputs:** accepted candidate (verified artifact + acceptance record);
G5.1 verification matrix; SLO declarations + performance budgets
(class S); the committed environment definition.
**Admission (four interlocks, structural):** acceptance record present
+ accepted + no unresolved blocking findings; artifact identity
(digest + attestation, no rebuild lane; environment-definition hash
per G6.3); can-i-deploy over the target environment; no standing G8
red (fix lane via contract reference).
**Authored here -> downstream gate material:** the release record set,
all pipeline facts - measurement records (G9 tightening input), binary
baselines + contract-diff payloads (-> G10 notification), SBOM +
provenance attestations (G7.5). Budgets and SLOs are authored
*upstream* (G2, class S) - the source table's "budgets authored at
release" was human-SDLC residue (session-10 correction).
**FAIL blocks:** the deploy; a failing canary auto-reverts the rollout
(G7.4). Rollout completion (100% + full-exposure window, G8.2 green)
closes G7 - baseline capture and production-version designation fire
there.
**Operator note:** fully mechanical, zero human conditions, QA
executes; pipeline definition + rollout policy + suppressions are
class E (PL-PIPE); interlocks golden-tested via PL-PIPE.2.
**Closes:** performance (CWE-400, 407 - absolute half of the S9 soak
split); build/config/deployment (ODC build/package - rehearsal +
G7.3); binary-compat breaks at the shipped boundary (G7.2); artifact
integrity (CWE-494 family / SLSA threats - G7.5).
**Deep page:** [gates/G7-release-deploy.md](gates/G7-release-deploy.md) -
G7.1-G7.5 all `specified`; roster 4 -> 5 (G7.5 SBOM + provenance
adopted at close-out); four-interlock admission ruled; benchmark +
canary procedure shapes fixed (numbers stay Q4); migration
revert-safety clause on G7.4.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G7.1 | Benchmark budgets | mechanical | Every budget-designated operation within its authored ceiling (class S tuples, per runner fingerprint); committed protocol, noise-floor + vacuity guards; measurement record committed, never gating (G9 input) | BenchmarkDotNet, dedicated runner class | Q4 (numbers) |
| G7.2 | ApiCompat binary compatibility | mechanical | Shipped package set (all TFMs) binary-compatible with the last shipped release; breaks only via spec-channel break records; version increment coheres with delta class; baseline captured at rollout completion | Microsoft.DotNet.ApiCompat | - |
| G7.3 | IaC scanning | mechanical | The certified environment definition + pipeline config scan clean at gating severity across all target instantiations, current feeds, ratchet-at-zero; dismissals via class-E suppression config; echo at enforcement-layer CI | trivy config-mode, PSRule (infra-format-keyed) | - |
| G7.4 | Canary with SLO-based rollback | mechanical | Staged exposure; per-stage dual verdict (absolute SLO + canary-vs-control delta); sample-floor guard; breach auto-reverts, no manual-continue; G8.1 fires = stage-FAIL; migration revert-safety (expand/contract) | progressive delivery + analysis compiled from slo.yaml | Q4 (canary constants) |
| G7.5 | SBOM + provenance attestation | mechanical | Every shipped artifact carries a committed SBOM + signed provenance (digest -> pipeline run -> source sha), verified at admission; missing either = nothing ships | SLSA provenance via CI attestation, CycloneDX | - |

## G8 - Operations

**Purpose:** turn every escaped defect into an upstream gate - the convergence
loop that tunes the gate set to the actual defect distribution instead of the
generic taxonomy.
**Venue & cadence:** production runtime, continuous - the only gate that
never convenes on a schedule: conditions are **standing invariants**,
the gate convenes on breach (event-driven).
**Inputs:** live traffic; telemetry from the shared instrumentation
surface (G5.6's action-emission layer + SLI streams); incident, crash,
and external-report channels.
**Authored here -> downstream gate material:** new acceptance criteria +
regression tests from escapes, minted through the front door (Spec agent
drafts, G1.3 reviews, G2.5 arms red); ladder-assignment statistics (the
gate set's own tuning evidence); triage records (class S, G6.2
conversion-record shape).
**FAIL blocks:** further rollout - red seizes rollouts, never operations
(all standing G8 reds funnel into G7's admission interlock 4; fix lane
via contract reference); convergence closure - a finding closes only by
conversion or recorded disposition. An escape that does not produce a
new criterion is itself a process failure (mechanized in G8.3's record
schema).
**Operator note:** monitoring/alert/derivation configs are class E
(gutting an alert is deleting a gate); G8.1/G8.2 mechanical; the
**operations principal** grades G8.3 (non-delegable; agents cluster and
draft as suggestions). Production chaos = governed practice, not a
condition: committed chaos plan (class E), error budget as license,
findings convert via G8.3.
**Closes:** escaped defects - by conversion, not prevention; the
runtime residue of every upstream class at its production surface.
**Deep page:** [gates/G8-operations.md](gates/G8-operations.md) -
G8.1-G8.3 all `specified`; G8.3 renamed (escape triage + conversion),
G8.2 renamed (license, not alerts); standing-invariant venue ruled;
shared-instrumentation chain formalized (G5.6 proves, G8.1 inherits);
S9's chaos routing discharged.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G8.1 | Runtime contract assertions | mechanical | Zero fires on the spec-derived gated set (boundary contracts + hard-core stream monitors), shipped enabled, fire-to-telemetry; fire = auto-finding + rollout seizure + canary stage-FAIL; liveness floors - dead listener reads red | shared OTel-family instrumentation, compiled monitors | - |
| G8.2 | SLO / error-budget license | mechanical | Error budget not exhausted per service; SLIs/objectives/windows compiled from `specs/<service>/slo.yaml` (class S), derivation golden-tested; exhaustion = standing red -> admission interlock 4; alerts notify, the license blocks | SLI pipeline + burn-rate rules | - |
| G8.3 | Escape triage + conversion | human | Every escape candidate (crashes, G8.1 fires, G8.2 incidents, external reports) triaged to disposition within window; conversion by default, declining takes written rationale; escape dispositions schema-incomplete without criterion + regression-test + ladder refs; queue attested even at zero | triage queue + 0011-family records | window in clocks.yaml (0012; Q4) |

## G9 - Maintenance / Evolution

**Purpose:** hold the line between features - supply-chain rot and slow entropy
accrue in the quiet weeks, not inside feature work.
**Venue & cadence:** scheduled jobs, weekly+ reference (clocks.yaml) - the
clock-driven venue: the first gate that convenes on time, not change.
Conditions are standing invariants over the dependency graph and the
enforcement baseline set; the sweep is the *detection* mechanism (feeds
are polled, never pushed). A sweep past its declared cadence reads red -
a dead sweep is a gutted gate, not a quiet week.
**Inputs:** advisory + EOL feeds; license metadata; the locked dependency
closure; the G7.5 SBOM join (exposure classes); the pipeline's own
records (G7.1 measurements, G5 corpus state, G5.5 scores, G8.3 ladder
statistics).
**Authored here -> downstream gate material:** the dependency update
policy (the bot lane's standing task contract, class E); tightenings
landed/drafted/reported by G9.4; refactoring-work candidates (capacity =
business policy, routed out S11).
**FAIL blocks:** the diff/world division - G4.9 gates what a change
introduces, G9 gates what time introduced into the unchanged set. A
breach opens a standing red in the 0012 economy: intake + merge +
admission arms, fix lane via `fixes`, windows in clocks.yaml.
**Operator note:** fully mechanical - no principal; bot and sweeps run
unattended; QA owns schedules, feeds, allowlists, and the tightening
job's config as class E (PL-PIPE); tightenings ride 0010's
direction-conditional lane.
**Closes:** supply-chain rot (known-vuln + EOL + license); enforcement
staleness (Goodhart decay of the gate set itself - G9.4).
**Deep page:** [gates/G9-maintenance.md](gates/G9-maintenance.md) -
G9.1-G9.4 all `specified`; roster 3 -> 4 (G9.4 tightening & baseline
freshness adopted at stop 5); aging-window family + clocks artifact +
`fixes` field -> ADR [0012](../decisions/0012-stop-the-line-economy.md);
EOL folded into G9.2; refactoring budgets routed to business policy.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G9.1 | Dependency PRs gated by full suite | mechanical | Updates ride the full ordinary gate set (G4 at merge incl. G4.9's delta arm, G5 downstream) - no reduced profile; write surface = manifest + lockfile, source-touching updates exit to ordinary intake; single-dependency PRs, batching only in declared version-locked groups; queue ordered by SBOM exposure class; holds never stop the G9.2 clock | Renovate/Dependabot, central package mgmt + lockfile, G7.5 SBOM join | - |
| G9.2 | Vulnerability-fix SLAs | mechanical | No advisory- or EOL-matched component past its window; clock from publication (EOL: announced date); windows = severity x exposure class; fixed = clean graph merged or VEX-shaped suppression (rationale + expiry); breach = standing red, three arms + fix lane (0012) | NuGetAudit/OSV + EOL feeds over the lockfile closure | Q4 (windows) |
| G9.3 | License audit | mechanical | Full locked closure licensed within each package's exposure class; unknown reads red; one class-E allowlist, two arms (G4.9 delta, G9.3 sweep); exceptions = rationale + expiry, always second channel; breach joins the aging family | SPDX from NuGet metadata + ClearlyDefined-family enrichment | - |
| G9.4 | Tightening & baseline freshness | mechanical | No ratchet-managed parameter past its tightening cadence; every candidate from the four evidence families landed (class E, auto), drafted (class S, spec channel), or dispositioned - tighten-by-default, declining takes written rationale; the job never loosens | scheduled job over committed records + baseline configs | Q4 (cadences) |

## G10 - Deprecation / Retirement

**Purpose:** force deletion - agents add code and almost never delete it;
without an explicit removal phase the codebase grows monotonically regardless
of every other gate.
**Venue & cadence:** the deadline gate - no pipeline of its own; deadlines
injected into existing venues (analyzer at build for G10.1, graph count at
the scheduled sweep for G10.2, record checks at merge + admission for
G10.3), sunset-date driven.
**Inputs:** deprecation records + sunset dates (class S, 0013); usage
telemetry from the shared instrumentation surface; fleet version facts
(G7.2 release records); migration specs.
**Authored here -> downstream gate material:** sunset dates on marks and
flag declarations; migration specs; consumer notification = the G7.2
contract-diff payload of the release shipping the mark (structurally
enforced: record schema + clock-from-notification, 0013).
**FAIL blocks:** merges past a sunset date (analyzer error, no suppression
lane); dead-count breach = standing red (0012); contract-class migration
without its complete retirement record (no merge, no admission).
**Operator note:** fully mechanical; deprecation records ride the spec
channel; analyzer + root configs + flag schema are class E (PL-PIPE);
removal work enters ordinary intake.
**Closes:** accretion (dead code, stale feature flags, zero-edge
packages); unsafe removal - contraction is the pipeline's only
irreversible act, so verification front-loads.
**Deep page:** [gates/G10-retirement.md](gates/G10-retirement.md) -
G10.1-G10.3 all `specified`; sunset policy -> ADR
[0013](../decisions/0013-sunset-policy.md); feature flags folded into
G10.1's subject class; trend mandate struck (downtrend is structural);
the deletion pipeline: G10.1 starves -> G10.2 counts -> G10.3 clears ->
G7.2 records the break.

| ID | Condition | Kind | Check | Tooling | Open |
|---|---|---|---|---|---|
| G10.1 | Obsolete-sunset escalation | mechanical | Sunset-bearing subjects (APIs + declared config surfaces incl. feature flags): usage warns before the date, errors at and past it, no suppression lane; class-S record <-> compiled mark coherence both ways, incomplete = merge red; date valid only >= notification + notice floor; moves per 0013 asymmetry | custom Roslyn analyzer (0009-family) + specs/deprecations/ records | Q4 (notice floors) |
| G10.2 | Dead-code ratchet | mechanical | Graph-level dead count from declared roots <= shrink-only baseline (G4.8 discipline, G9.4-managed, zero at greenfield); undeclared liveness reads dead; post-sunset members + zero-edge packages count; breach = standing red (0012) | ILLink-informed reachability, trimmer root descriptors + [DynamicDependency] | - |
| G10.3 | Data-migration verification | mechanical | Every schema migration classifies expand/contract (unclassifiable = contract); contract-class merges/admits only with the complete retirement record: deprecation chain, backfill reconciliation, drainage evidence, fleet coherence, certified-env rehearsal, recoverability ref | EF migration lexicon, OTel usage counters, G6.3 rehearsal | Q4 (drainage window) |

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
| PL-PIPE.1 | Enforcement-layer change control | human | Gate-config edits approved through a channel separate from what they enforce | approval workflow | Q7; mechanical arm = [0010](../decisions/0010-write-surface-immutability.md) |
| PL-PIPE.2 | Gate-config golden tests | mechanical | Gate configurations pass their own regression suite | golden tests | - |
| PL-PIPE.3 | Agent-behavior evals | mechanical | Agent prompts pass behavioral evals before deployment | eval suite | - |

---

## Cross-references

The eight spec-first patterns with their authored-at / enforced-by mapping
live in [catalog.md](catalog.md). The bug-class taxonomy anchoring each
gate's **Closes** line, with per-class ladder positions and the gap-analysis
method, lives in [taxonomy.md](taxonomy.md).
