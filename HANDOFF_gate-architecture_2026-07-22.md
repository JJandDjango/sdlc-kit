# HANDOFF — Gate Architecture for Automated LLM Development

**Session date:** 2026-07-22
**Status:** Design/exploration complete for this pass. No implementation started.
**Related work:** agentic-harness (Spec → Developer → QA → Verifier pipeline, contract-first file-based protocols); convention-extraction skill concept (scan codebase → extract StyleCop/IDE rules, patterns, review comments into a reference rule base); per-codebase ontology/rule-base goal from the pace-layered docs effort. This document is decisions/THEORY-layer material with a STATE-layer status section (§9–10).

---

## 1. Framing question and verdict

**Question:** Can a sufficiently structured set of static analysis tools and conventions make automated LLM development run without bugs or codebase degradation?

**Verdict (established, treat as settled):**

- **Degradation: largely preventable.** Degradation is structural — complexity creep, duplication, coupling growth, convention drift, dead code — and structural properties are statically measurable. Enforced via ratchets, architecture tests, and custom analyzers.
- **Bugs: not eliminable by static analysis alone.** Rice's theorem — every non-trivial semantic property of programs is undecidable — so no static tool certifies functional correctness in general. Practical analyzers are heuristic (neither sound nor complete). What is achievable: elimination of specific bug *classes* plus spec-relative gates for the rest.
- **Residual defect mass for LLM-generated code** concentrates empirically in requirements misinterpretation, missing edge cases, and API misuse — classes invisible to linters. Hence the strategic conclusion: spec-first gates over ever-more static detectors.

---

## 2. Core design principles

1. **Detectability ladder.** Every bug class sits at one of: (a) eliminable by construction, (b) statically decidable, (c) statically approximable, (d) dynamic-only, (e) spec-relative. Engineering effort pushes classes *up* the ladder (e.g., typestate encoding moves API call-order misuse from (d) to (a)) rather than accumulating detectors at the bottom.
2. **Correct-by-construction beats detect-after-generation.** Shrink the space of representable programs — strong domain types, parse-don't-validate, illegal states unrepresentable — so generation lands inside the valid space.
3. **A gate = a human judgment converted into a text artifact plus a mechanical check.** Every gate must emit machine-actionable diagnostics the agent can loop against until clean; auto-fixable rules are best.
4. **Enforce at the earliest decidable point.** Cost determines cadence (inner-loop seconds → nightly hours), never rigor — slow gates still block release.
5. **Spec-first gates have three defining properties:** authored before and independently of the implementation; mechanically checkable; **immutable to the implementer**. Immutability is enforced by path checks in CI/Verifier diffs, not prompt instructions — an agent that can edit a failing test will edit the test.
6. **Two-channel principle.** Spec and implementation come from separate agents with decorrelated context; shared context reproduces shared misreadings.
7. **The enforcement layer is the highest-privilege artifact set** (CI config, analyzer rulesets, agent prompts, spec paths). It requires a separate approval channel from what it enforces, plus its own regression suite (golden tests for gate configs, evals for agent behavior).
8. **Convergence loop.** Every escaped production defect becomes a new immutable acceptance criterion, tuning the gate set to the actual defect distribution rather than the generic taxonomy.
9. **Agents add code and almost never delete it.** An explicit deprecation/retirement phase is mandatory or the codebase grows monotonically regardless of all other gates.
10. **The oracle problem persists.** A wrong spec yields conformant wrong code. Keep specs declarative (criteria, properties, schemas) so spec review stays cheap — that is the one place human attention concentrates.

---

## 3. Bug-class taxonomy

**Anchors:**
- **CWE** (MITRE) — ~900+ weaknesses, hierarchical, machine-readable; analyzers (CodeQL, Semgrep, Roslyn security rules) tag rules with CWE IDs. CWE-1000 "Research Concepts" view, ten pillars: 284 access control, 435 improper interaction between entities, 664 resource lifetime, 682 incorrect calculation, 691 control flow, 693 protection mechanism failure, 697 incorrect comparison, 703 exceptional-condition handling, 707 improper neutralization, 710 coding-standard violations.
- **ODC** (Chillarege/IBM) — eight defect types: function, interface, checking, assignment, algorithm, timing/serialization, build/package, documentation. Covers the plain functional defects CWE's security weighting undercovers.

**Gap-analysis method:** enumerate pillars → map enabled analyzer rules (by CWE tag) against them → every uncovered node is a decision point: write an analyzer or write a test.

### Class → gate mapping (with ladder position)

| Bug class | Anchor | Primary gate | Ladder |
|---|---|---|---|
| Type/interface misuse | CWE-704, ODC interface | Compiler, strict typing | (a) |
| Null/uninitialized state | CWE-476, 457 | Nullable reference types, definite assignment | (a)/(b) |
| Memory safety | CWE-119, 416, 415 | Language choice (GC/borrow checker); sanitizers for native interop | (a); (d) at interop |
| Resource lifetime | CWE-664, 772 | Lifetime analyzers (CA2000), `using` discipline | (c) |
| Injection / neutralization | CWE-707: 79, 89, 78 | Taint/dataflow analysis | (c), strong |
| Input validation / parsing | CWE-20 | Parse-don't-validate types + fuzzing | (a) + (d) |
| Numeric / calculation | CWE-682: 190, 193 | Checked arithmetic, unit-of-measure types, property tests | (a)/(c) + (e) |
| Error/exception handling | CWE-703, 390 | Analyzers (swallowed catch), Result discipline, mutation testing | (c)/(e) |
| Concurrency | CWE-362, 667 | Ownership types; model checking; systematic testing (Coyote) | (d); (a) with ownership types |
| Access control / authz | CWE-284, 693 | Policy-as-code tests, CodeQL patterns | (c)/(e), design-level |
| API/protocol misuse (call order) | ODC interface | Typestate encodings, custom Roslyn analyzers, integration tests | (d) → (a) via typestate |
| Logic / algorithmic | ODC algorithm | Property-based, metamorphic, differential testing; verification as limit | (e) |
| Requirements misinterpretation | ODC function | Executable acceptance specs written before implementation | (e) |
| Build / config / deployment | ODC build/package | IaC scanners, environment-parity checks | (b)/(c) |
| Performance | CWE-400, 407 | CI benchmarks with budgets | (d) |

---

## 4. Spec-first gate catalog

1. **Immutable acceptance tests + traceability.** Spec stage emits numbered criteria (REQ-IDs) and executable tests; implementer tests carry `[Criterion("REQ-014")]`-style annotations; a CI script requires every REQ-ID → ≥1 passing test; any diff touching spec paths fails the build.
2. **Type-first scaffolding + API surface lock.** Spec stage writes interfaces/domain types/DTOs; `PublicAPI.Shipped.txt` (PublicApiAnalyzers) is the source-time lock; ApiCompat is the binary lock at release.
3. **Property-based and metamorphic specs.** FsCheck/CsCheck; declarative behavioral specifications over the input space, hard to satisfy vacuously; attacks missing-edge-case class.
4. **Boundary contracts.** OpenAPI/JSON Schema/protobuf written first; schema validation in tests; breaking-change detection (oasdiff, `buf breaking`); consumer-driven contract tests (PactNet).
5. **Approval tests with locked snapshots.** Verify; `.approved.*` files are human/spec-approved and non-regenerable by the implementer.
6. **Differential gates.** Naive obviously-correct reference implementation from the spec stage; optimized implementation gated by equivalence over generated inputs. Strongest oracle for algorithmic code.
7. **Mutation threshold** (Stryker.NET score floor). Gates the *spec's adequacy* — proves the acceptance/property suite actually constrains implementations; closes the vacuous-test loophole.
8. **Formal models for hard cores.** TLA+/Alloy/P model-checked pre-implementation, linked via trace-conformance tests or model-based test generation; Dafny where proof-carrying code is itself the gate. Reserve for components where ladder positions (c)–(d) are unacceptable.

---

## 5. Unified SDLC gate map

Structural notes: rows 3–5 decompose the canonical implementation/testing phases by feedback latency (venue: editor / merge queue / nightly), because gates attach to enforcement venues and cadence, not textbook phase names. Overall shape is V-model: each authoring phase pairs with later enforcement stages.

| # | Phase | Authored here → becomes downstream gate | Enforced here (blocking) | Defect classes closed |
|---|---|---|---|---|
| 0 | Planning / Intake | Task contract: scope, explicit non-goals, decomposition into independently gateable units | Definition-of-ready check — reject if acceptance criteria are unwritable, dependencies unresolved, or scope unbounded | Mis-selection, scope creep. Dominant upstream failure for agent pipelines; a malformed task defeats every downstream gate |
| 1 | Requirements / Spec (input: task contract) | Numbered acceptance criteria; immutable acceptance tests; property + metamorphic specs; boundary schemas (OpenAPI/protobuf); formal models for hard cores (TLA+/P) | Schema/spec linting (Spectral, `buf lint`); model checking (TLC); criteria completeness + ambiguity review — human attention concentrates here | Requirements misinterpretation (ODC function) |
| 2 | Design / Architecture | Interface + domain-type scaffolding; `PublicAPI.Shipped.txt` baseline; architecture rule tests (NetArchTest); typestate encodings; ratchet baselines; threat model (STRIDE per trust boundary) → abuse cases compiled into security acceptance tests | Design-level model checking; breaking-change baseline lock; ADR review; threat-model-existence gate for components crossing trust boundaries | API misuse, concurrency design flaws, architectural erosion, design-level security flaws |
| 3 | Implementation (inner loop, seconds) | Implementation + unit tests — the only agent-mutable artifacts | Formatter; StyleCop + custom Roslyn analyzers with code fixes; strict compile (`Nullable`, `TreatWarningsAsErrors`, `AnalysisLevel latest-all`) | Type/null, resource lifetime, convention drift |
| 4 | Pre-merge CI (minutes) | Regression tests from review findings | Full analyzer set; architecture tests; acceptance suite + REQ-ID traceability check; property tests; API surface diff (PublicApiAnalyzers, oasdiff); **spec-path immutability check**; taint/security scan (CodeQL/Semgrep); duplication + complexity ratchets; secret/dependency audit | Injection, calculation, error handling, erosion; misinterpretation via traceability |
| 5 | Integration / System (hours; nightly cadence) | — | Consumer-driven contract verification (PactNet); differential testing vs reference implementation; fuzzing (SharpFuzz); systematic concurrency testing (Coyote); mutation threshold (Stryker.NET); model trace-conformance | Interaction bugs, concurrency, parsing/input validation, vacuous specs |
| 6 | UAT / Staging | Findings → new acceptance criteria | Human validation against REQ-IDs in production-like environment; exploratory testing | Residual misinterpretation — the conformant-but-wrong code a mechanically satisfied spec still permits |
| 7 | Release / Deploy | Performance budgets; SBOM/provenance | Benchmark budgets (BenchmarkDotNet + CI comparison); ApiCompat binary compatibility; IaC scanning; canary with SLO-based rollback | Performance; build/config/deployment (ODC build/package) |
| 8 | Operations | New acceptance criteria + regression tests from incidents → phase 1 (convergence loop) | Runtime contract assertions with telemetry; SLO/error-budget alerts; crash triage | Escaped defects, converted into upstream gates |
| 9 | Maintenance / Evolution | Dependency update policy; scheduled ratchet tightening; refactoring budgets | Automated dependency PRs gated by the full suite; vulnerability-fix SLAs; license audit | Supply-chain rot; slow entropy accruing between features |
| 10 | Deprecation / Retirement | Sunset dates on `[Obsolete]`; migration specs; consumer notification via contract diff | Analyzer escalating warning → error at sunset date; dead-code ratchet; data-migration verification | Accretion — monotonic growth absent an explicit removal phase |

### Parallel lifecycles (not phases)

- **Documentation.** For agent pipelines docs are injected context, so staleness is a defect *vector*: gates = doc code samples compiled/executed in CI, coverage analyzers, staleness dating. Maps onto the pace-layered scheme: fast layers get automated drift gates; slow layers get change-control review.
- **The pipeline itself.** Gate definitions, CI config, rulesets, agent prompts, spec paths — see principle 7 (§2). A developer agent that can edit the workflow file can delete every gate in one diff.

---

## 6. Harness integration

- **Spec agent** authors phases 0–2 artifacts: task contracts, acceptance criteria + tests, property specs, boundary schemas, type scaffolding, architecture baselines, threat models.
- **Developer agent** operates in phase 3 only. Sole mutable artifacts: implementation + unit tests. All spec paths are read-only to its diffs.
- **QA agent** owns execution of phases 4–6.
- **Verifier agent** is cross-cutting: gate integrity, spec-path immutability diff checks, enforcement-layer change control at every phase — this stack is the Verifier's deterministic core.
- The per-codebase ontology/rule-base goal (from the documentation-system work) is the input pipeline for the custom-analyzer layer: extracted conventions → Roslyn analyzer rules.

---

## 7. Tooling shortlist (C#/.NET-first)

- **Style/conventions:** StyleCop.Analyzers; custom Roslyn analyzers with code-fix providers; `.editorconfig` + `stylecop.json`
- **Compile strictness:** `<Nullable>enable</Nullable>`, `TreatWarningsAsErrors`, `AnalysisLevel latest-all`
- **Surface/compat:** Microsoft.CodeAnalysis.PublicApiAnalyzers; Microsoft.DotNet.ApiCompat; oasdiff; buf
- **Architecture/degradation:** NetArchTest; jscpd or PMD CPD (duplication); complexity ratchets
- **Security/dataflow:** CodeQL; Semgrep
- **Semantic layer:** FsCheck/CsCheck (properties); Stryker.NET (mutation); SharpFuzz (fuzzing); Coyote (concurrency); Verify (approvals); PactNet (contracts); Reqnroll (optional Gherkin)
- **Performance:** BenchmarkDotNet + CI result comparison
- **Formal:** TLA+/TLC; P; Alloy; Dafny/F*
- **Spec linting:** Spectral

---

## 8. Open questions

1. Spec-path immutability mechanism: protected directories + CI diff check vs CODEOWNERS vs separate repo/submodule.
2. Task-contract schema for phase 0 — definition-of-ready fields.
3. Which house conventions to encode as custom Roslyn analyzers first; whether the convention-extraction skill generates analyzer stubs.
4. Threshold selection: mutation score floor, complexity budgets, ratchet-tightening cadence.
5. How the harness achieves two-channel decorrelation when constructing Spec vs Developer contexts.
6. Pilot repository selection; greenfield vs retrofit sequencing.
7. Enforcement-layer change-control workflow — who/what approves gate edits.
8. Which components merit formal models (identify the phase-1 hard cores).

## 9. Candidate next steps (proposed, not yet decided)

1. CWE gap analysis: enumerate currently enabled analyzer rules against the ten pillars; list uncovered nodes.
2. Prototype one custom Roslyn analyzer + code fix for a single house convention (end-to-end proof of the leverage claim).
3. Define the REQ-ID traceability format and write the CI traceability script.
4. Stand up the minimal phase 3–4 stack on a pilot repo (formatter, StyleCop, strict compile, arch tests), then add ratchets.
5. Draft the Verifier spec-path immutability check.
6. Write the phase-0 task-contract schema.

## 10. Session provenance

Thread progressed: StyleCop overview → feasibility of static analysis as sufficient guarantee (verdict in §1) → bug-class taxonomies (CWE/ODC) and gate mapping → spec-first gate catalog → SDLC gate table → completeness analysis adding phases 0, 6, 9, 10, the threat-modeling amendment, and the two parallel lifecycles. An abbreviation glossary for all table entries exists in the source chat if needed.
