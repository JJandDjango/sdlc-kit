# G3 - Implementation (inner loop)

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Implementation gate contain,
> and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 3,
> principles 1, 2, 4 (section 2); THEORY's loopability invariant. First page
> authored under the two-layer model
> ([0008](../../decisions/0008-two-layer-condition-model.md)): shapes
> normative and ecosystem-free, bindings = the .NET reference profile.

## Identity

- **Venue:** editor / local build.
- **Cadence:** seconds per iteration - the fast end of the cost-sets-cadence
  spectrum.
- **Inputs:** the working diff - implementation + unit tests, the only
  agent-mutable artifacts in the pipeline.
- **FAIL blocks:** code leaving the inner loop (the local build stays red).
- **V-model position:** the pipeline's inversion point. G0-G2 author
  enforcement instruments (contracts, criteria, baselines, threat models,
  red suites); G4+ execute those instruments against the object. G3 is the
  only phase that authors no instrument - its outputs are the *object* of
  enforcement, never the means. The mutability model seen from the other
  side: the Developer's sole write surface is exactly the artifact set no
  gate trusts.
- **Unique exposure:** the only gate that executes inside the context of
  the agent it constrains. Every other venue (CI, nightly, staging) is out
  of the Developer's reach; G3's enforcing artifacts sit within arm's reach
  of their subject - which is why their governance (echo division, clause
  3) matters more here than anywhere.

## Why this gate exists

Keep the inner loop clean at zero human cost: every violation surfaced in
seconds, with a machine-applicable fix wherever possible. G3 is the
loopability invariant in its purest form - all three conditions are
mechanical, and their diagnostics are not merely machine-actionable but
largely machine-*applicable* (formatter rewrites, code-fix providers,
line-precise compiler errors).

Principles bearing:

- **Earliest decidable point (principle 4):** these three checks are
  decidable from the working diff alone in seconds - deferring them to G4
  wastes the cheapest venue in the pipeline. Cost sets cadence, never
  rigor.
- **Detectability ladder (principle 1):** G3.3 is the enforcement point of
  the pipeline's (a)/(b) rungs - the venue where G2's ladder climbs
  (typestate, parse-don't-validate, unit-of-measure types) actually reject
  violating code. G3.2 moves convention drift from review-caught to
  statically decidable.
- **Correct-by-construction (principle 2):** the strict compiler
  constrains generation from the first token - the valid space shrinks
  before any detection runs.

Classes closed: type/interface misuse (CWE-704), null/uninitialized state
(CWE-476, 457), resource lifetime (CWE-664, 772 - battery, (c)-grade),
numeric overflow (CWE-682, trap half), incorrect comparison (CWE-697),
non-concurrency control flow (CWE-691 remainder), convention drift
(pillar 710) ([taxonomy](../taxonomy.md)).

**The G3 <-> G4.1 echo division** (ratified this session): G3 optimizes
*latency*; G4 holds *authority*. Three clauses:

1. Nothing is decided solely at G3 - G4.1 re-runs the entire analyzer
   battery as a superset on the merged build; formatting and strict
   compile re-verify there under the identical configuration. G3's FAIL
   (local build red) is a productivity mechanism; merge-blocking authority
   is G4's. Deep-page consequence: every G3 condition names its G4
   re-check locus.
2. Single-sourced configuration: the artifacts defining all three
   conditions are committed repo artifacts consumed verbatim by both
   venues - local-vs-CI drift is impossible by construction, not by
   discipline. A local-pass/CI-fail divergence is definitionally a
   pipeline-integrity defect (PL-PIPE), not a Developer error.
3. The config set is enforcement-layer (PL-PIPE): G3 is the one gate whose
   enforcement its own subject could silently delete - one `.editorconfig`
   edit and the loop goes permissive. The Developer's write surface
   excludes the G3 config set, mechanically - protected-path machinery
   shared with G4.6 (mechanism = Q1, the G4 session); changes flow only
   through PL-PIPE.1's second channel.

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape** is
normative and ecosystem-free; **Reference binding** is the .NET profile. A
profile that cannot reach a shape registers a build item (gap-closure
directive); a missing binding gates that profile's `enforced` flip, never
the shape's `specified`.

### G3.1 Formatter

- **Shape (pass condition):** the ecosystem formatter, in verify mode,
  reports zero deviations from canonical form tree-wide; any deviation =
  FAIL with the deviating file list as the diagnostic. Three clauses:
  1. **Totality boundary** - the condition covers only rules with a total,
     idempotent, judgment-free fixer (layout); anything semantic is
     analyzer material -> G3.2. This keeps G3.1 the pipeline's only
     condition whose fix is canonical, so apply mode is unconditionally
     safe.
  2. **Single source** - formatting rules live in one committed config;
     the G4 echo runs the identical tool + config in the tamper-proof
     venue.
  3. **Fix channel** - the inner loop runs apply mode (fix and diagnostic
     are the same act; the loop is one iteration by construction); verify
     mode is the gate form. Diff-scoping locally is permitted for latency
     since the echo supersets tree-wide.
- **Reference binding (.NET):** gate form `dotnet format whitespace
  --verify-no-changes` exits 0 solution-wide; apply form `dotnet format
  whitespace`; config `.editorconfig` (repo root, PL-PIPE-governed). G4
  echo = the identical command as an explicit G4 job step - not assumed
  covered by G4.1's battery, because the whitespace verb's rule set and
  IDE0055-as-analyzer are not provably identical (G4-session input).
  IDExxxx style rules and StyleCop layout rules belong to G3.2's battery
  per the totality boundary.
- **Gap status:** none - every plausible profile has a verify+apply
  formatter (`rustfmt --check`, `gofmt -l`, `ruff format --check`,
  `prettier --check`). The kit's zero-gap condition.
- **Why:** pillar 710's lowest rung, closed at (b) with a total fix - the
  cheapest ladder position in the kit. In an agent pipeline canonical form
  means every diff carries only semantic change: G3's own input is the
  working diff, and a formatter-clean tree keeps it minimal, kills
  format-noise merge conflicts, and stabilizes what G4.8's duplication
  ratchet measures.
- **Kind & loopability:** mechanical; the fix is canonical - the purest
  loop in the pipeline (apply once, converged).
- **Parameters:** none open. Tool-version pinning = enforcement-pass
  material (updates ride G9.1).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G3.2 Analyzer battery

Registry row renamed from "StyleCop + custom Roslyn analyzers"
(ecosystem-bound) to "Analyzer battery" per 0008; the .NET specifics live
in the binding.

- **Shape (pass condition):** three clauses.
  1. **Battery cleanliness** - a declared static-analyzer set produces
     zero diagnostics at gating severity tree-wide; the venue event is the
     local build. Set composition + severity map live in committed config
     (single source, PL-PIPE-governed), consumed identically by the G4.1
     echo, which supersets (G4 may add analyzers, never drop one).
  2. **Convention encoding** - every gating house convention is encoded as
     a native analyzer (or declarative rule-pack entry where that
     suffices) with a machine-applicable fix wherever the rule's nature
     permits. Conventions enter the battery only from the ratified
     conventions registry
     ([0009](../../decisions/0009-custom-analyzer-adoption-policy.md)) -
     never directly from taste, human or agent.
  3. **No self-weakening** (beyond the registry row - ratified addition,
     G2.5-clause-2 precedent) - the battery must be clean *and
     unweakened*: a new in-source suppression of a gating rule is itself a
     violation; severity/exclusion changes flow only through the
     PL-PIPE-governed config. Rationale: the configs are protected (echo
     division clause 3), but in-source suppressions live inside the
     Developer's legitimate write surface - the one tamper vector config
     protection cannot see. Enforcement locus: the G4 echo's suppression
     audit (G4-session input).
- **Reference binding (.NET):** battery = StyleCop.Analyzers (stock style
  tier) + IDExxxx code-style rules with `EnforceCodeStyleInBuild=true`
  (what makes style rules actually gate in the build) + the custom tier -
  pipeline-native analyzers (sunset escalation for G10.1; the suppression
  audit) and house analyzers compiled from ratified conventions per 0009;
  severities via `.editorconfig`; analyzers as package/project references.
  Gate form: the build (G3.3's zero-warning regime makes gating severity =
  warning). Apply forms: code-fix providers in-editor; `dotnet format
  style` / `dotnet format analyzers` for bulk fixes. Suppression-audit
  watch list: `#pragma warning disable`, `[SuppressMessage]`,
  `GlobalSuppressions.cs`, severity downgrades, `<NoWarn>`,
  strictness-flag overrides (G3.3), generated-code exclusion edits.
- **Gap status:** two build items registered under the gap-closure
  directive (0008): the sunset-escalation analyzer (.NET binding of
  G10.1's shape; other profiles bind their own) and the suppression-audit
  diff check. Both small; both activate with the .NET profile.
- **Why:** three taxonomy rows route here - convention drift (710),
  resource lifetime at (c) (the CA2000-family lifetime rules), call-order
  API misuse where G2 typestate was not applied. The agent-pipeline
  argument is throughput: a convention living in review comments is
  re-litigated on every PR at LLM speed - O(PRs) human cost forever;
  encoded once as an analyzer with a fixer it is O(1) authoring cost
  riding the loopability invariant. "A gate = a human judgment converted
  into a text artifact plus a mechanical check" at its finest grain: one
  judgment, one rule, one fixer.
- **Kind & loopability:** mechanical; per-rule, per-location diagnostics
  with fix providers - the strongest fix-carrying condition in the
  pipeline.
- **Parameters:** severity map + first-tranche instantiation ride pilot
  activation (Q6). Q3 closed as policy -> 0009.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G3.3 Strict compile

- **Shape (pass condition):** the build succeeds under the ecosystem's
  maximum generally-available static strictness, from committed
  configuration. Four clauses:
  1. **Full static strictness on** - the null-safety regime fully enabled;
     the compiler's complete *current* analysis breadth on (tracking
     latest, never pinned). Deliberate consequence: toolchain updates
     arriving through G9.1 tighten this condition automatically; a
     new-rule breakage surfaces as a failing dependency PR gated by the
     full suite, not as a reason to pin.
  2. **Zero-warning regime** - every diagnostic escalates to error; the
     warning channel is empty by construction. A ratchet-at-zero: unlike
     G4.8's baselines, which tighten over time, warning debt is pinned at
     zero from day one and can never open.
  3. **Loud-failure numerics** (registry-drift fix: the taxonomy already
     credited "G3.3 checked arithmetic"; the Check column now names the
     flag) - silent-wrongness switches flip to loud failure where the
     ecosystem offers them; numeric overflow traps rather than wraps.
  4. **Escape hatches fenced** - language-level escapes from the static
     guarantees (unsafe memory, dynamic typing, project-scope nullability
     suppression) are off by default; enabling one anywhere is an
     enforcement-layer change (PL-PIPE) that must name its compensating
     control (unsafe interop -> the native-interop sanitizer item, G5
     session). This clause mechanically fences the taxonomy's "memory
     safety closed by construction (GC)" row, which otherwise silently
     evaporates the first time an unsafe block opens. Micro-escapes no
     compiler flag governs (the null-forgiving operator) route to G3.2's
     pipeline-native analyzer tier.
- **Reference binding (.NET):** `Directory.Build.props` at repo root
  (single point, every project inherits, PL-PIPE-governed):
  `<Nullable>enable</Nullable>`,
  `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`,
  `<AnalysisLevel>latest-all</AnalysisLevel>`,
  `<CheckForOverflowUnderflow>true</CheckForOverflowUnderflow>`, explicit
  `<AllowUnsafeBlocks>false</AllowUnsafeBlocks>`. Per-project overrides of
  any strictness flag, and `<NoWarn>` additions, are suppressions - caught
  by the G3.2 suppression audit (one audit, both conditions' tamper
  vectors). G4 echo: the merged-result build under the identical props.
- **Gap status:** no mainstream profile lacks a strict mode (TS `strict`,
  mypy `--strict`, Rust `deny(warnings)`); rung differences are real but
  narrow - a Go profile would document nullability tracking as unreachable
  (compensation: static nilness analysis + fuzz pressure); a Rust binding
  must set `overflow-checks = true` for release. Nothing here triggers the
  build directive.
- **Division from G3.2** (stated once): one build event evaluates both
  conditions. G3.3 owns the compiler *configuration* - flags present,
  strictness maximal, escalation total; G3.2 owns the loaded analyzer
  set's composition and cleanliness. A CA diagnostic failing the build is
  G3.2 content riding G3.3's escalation regime; no double-counting.
- **Why:** the (a)/(b) engine of the gate - closes CWE-704 and CWE-476/457
  (the gate's headline classes) and is the enforcement point of G2's
  ladder climbs: typestate and parse-don't-validate types are authored at
  G2, but the artifact that rejects their violations is this compiler
  under these flags. The compiler is the one oracle the Developer consults
  hundreds of times per task at zero marginal cost - every guarantee moved
  into it executes at conversation speed. One committed props file
  converts the ecosystem's correct-by-construction capability from opt-in
  to mandatory - the closest thing to a free lunch in the kit.
- **Kind & loopability:** mechanical; file/line-precise, frequently
  fix-carrying - the canonical loop diagnostic.
- **Parameters:** none open.
- **Lifecycle:** `specified` (ratified 2026-07-24).

## Completeness check

Gate purpose: everything seconds-decidable from the working diff surfaces
in the inner loop with a machine-applicable fix; G3 authors no instrument,
so the check asks what escapes the three conditions. Examined:

- **Unit-suite execution.** No registered condition anywhere executes the
  Developer's unit suite: "local build stays red" covers compile,
  G4.3/G4.4 run the spec-authored suites, and G5.5's mutation floor
  *presupposes* a green baseline. A fourth G3 condition was considered and
  rejected - running one's own tests is the loop itself, not a gate, and
  gate-grade teeth belong in the tamper-proof venue (echo division clause
  1). **Exported to the G4 session:** proposed condition - merged-build
  test execution green, Developer suite included (also G5.5's
  precondition).
- **Pillar-tagging gap (435, 691, 697).** Three pillars were covered
  functionally but invisible to the mechanical audit ("map enabled rules
  by CWE tag"). Fixed in this session's cascade: taxonomy rows added for
  incorrect comparison (697 -> battery + G5.5), non-concurrency control
  flow (691 -> G3.3 + battery), improper interaction (435 -> G5.1/G5).
  Rule-level substantiation = the G4 session's battery audit.
- **Generated-code exclusions.** Formatter and analyzers need
  generated-code fencing, and an over-broad exclusion glob blinds the
  battery as effectively as any pragma. Absorbed into the suppression
  audit's watch list (fourth tamper vector: pragmas, NoWarn/severity,
  flag overrides, exclusion edits).
- **Anti-gaming coverage (session finding, user-raised).** Two additions
  beyond G3's remit, banked: (1) mutation does not catch overfit
  implementations (a hardcoded special-case kills its own mutants); the
  only mechanical guard is generated-input exposure, and nothing currently
  forces per-component generated-input coverage -> **G5-session input**:
  G5.2/G5.3 scope must answer "which components must carry generated-input
  oracles", likely back-propagating a G1.3 checklist item ("each criterion
  class has generated-input coverage or a recorded why-not"). (2) What the
  Developer's context contains (test source vs criteria + diagnostics
  only) is unfixed -> named **Q5 sub-question**.
- **Pillar sweep verdict:** with the overflow clause and the tagging fix,
  every pillar node seconds-decidable from the working diff is covered;
  707-taint, 284/693, and 435 are not seconds-decidable and correctly live
  downstream - cadence-bounded, not gaps.

Roster verdict: complete at three conditions, zero additions - one export
to the G4 session, two findings absorbed (suppression watch list, taxonomy
rows), two banked (G5-session input, Q5 sub-question).

## Operators & harness

The Developer is G3's sole operator - the only gate operated by the agent
it constrains. Its loop: apply formatter -> build (battery + strict flags,
one event) -> run tests -> repeat until the working diff is clean and the
spec suite progresses red -> green. Its write surface is implementation +
unit tests; everything enforcing (`.editorconfig`, `Directory.Build.props`,
the analyzer set) it consumes but cannot touch. The suppression audit
joins the Verifier's deterministic core alongside G4.6 (placement fixed at
the G4 session). No human appears at G3 by design - the pipeline's
attention concentration stays at G1.3 and G6. The build is authoritative;
editor live-analysis is advisory preview of the same rules.

## Decisions & open items

- All three conditions `specified` 2026-07-24 (session-7 walk); rulings
  ratified in-conversation before edits landed.
- The G3 <-> G4.1 echo division ratified (latency vs authority /
  single-sourced config / PL-PIPE governance); anchors this page and the
  G4 page's G4.1 section.
- Two-layer model + gap-closure directive adopted ->
  [0008](../../decisions/0008-two-layer-condition-model.md); this page is
  the pattern-setter (shape + reference binding per condition). G3.2
  renamed "Analyzer battery" in the cascade.
- Q3 closed as policy ->
  [0009](../../decisions/0009-custom-analyzer-adoption-policy.md):
  source of truth, selection function, pipeline-native tier, bounded stub
  generation, fixture-before-gating. First tranche instantiates at pilot
  activation (Q6).
- G3.2 clause 3 (no self-weakening) ratified as an addition beyond the
  registry row.
- Build items registered (0008 gap-closure): sunset-escalation analyzer
  (G10.1 .NET binding), suppression-audit diff check.
- G4-session inputs banked (four): the G3.1 echo step; the four-vector
  suppression audit; the unit-suite-green candidate condition; the battery
  audit substantiating the 691/697 taxonomy rows.
- G5-session input banked: mandatory generated-input oracle scope
  (anti-overfit). Q5 sub-question named: Developer context contents (test
  source vs criteria + diagnostics).
