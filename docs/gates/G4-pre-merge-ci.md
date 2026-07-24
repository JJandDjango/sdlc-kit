# G4 - Pre-merge CI

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Pre-merge CI gate contain,
> and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 4,
> principles 1, 4, 5 (section 2); the G3<->G4 echo division
> ([G3 page](G3-implementation.md)); ADRs
> [0010](../../decisions/0010-write-surface-immutability.md) and
> [0011](../../decisions/0011-criterion-traceability-format.md), ratified
> this session. Two-layer per
> [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** merge queue (authoritative) / PR CI (advisory preview). The
  shape *requires* queue semantics: every condition evaluates against
  the main the candidate will actually land on (main-at-queue-time) -
  plain PR CI's stale-base race admits semantic conflicts between
  individually-green candidates. PR-CI-on-push remains as a latency
  courtesy: the same relationship editor live-analysis has to G3's
  build, one level up. Queue-less fallback (binding note): strict
  serial merges with required-up-to-date branches.
- **Cadence:** minutes - and the minutes budget is an *admission rule*
  (frame ruling): a condition joins G4 only if minutes-decidable on the
  merged result; slower checks are G5 material regardless of mechanical
  purity. Cost sets cadence, never rigor.
- **Inputs:** the candidate diff + the full build of the merged result.
  **Object rubric** (frame ruling): every condition declares its object
  - the *merged result* (default: what main will become) or the
  *candidate diff* (only where the check is about the change-act
  itself).
- **FAIL blocks:** merge to main.
- **V-model position:** the pipeline's choke point - the only venue
  every change crosses exactly once, at machine speed, before becoming
  shared state. Eleven of the kit's 50 conditions sit here because the
  merge is where enforcement is cheapest per unit of authority: before
  it a defect is private to the task branch (fix = one loop iteration);
  after it, shared state surfacing at G5's nightly cadence at the
  earliest. **Execution-only:** G4 authors nothing - the source table's
  "regression tests from review findings" was human-SDLC residue
  (close-out ruling); conversion loops live at G6/G8.3, and a G4 catch
  needs no new criterion by definition.
- **Trust boundary:** the first venue out of the Developer's reach.
  G3's green is a productivity signal; authority lives here (echo
  division clause 1, receiving end). The pipeline never consumes G3's
  report - G4 recomputes it.

## Why this gate exists

The merge is the last cheap moment: everything minutes-decidable blocks
here (principle 4). And G4 has a dual character no other gate carries:
every gate checks the *object* (is the code correct?); G4 additionally
checks the *subject* (did the agent behave?) - write-surface
immutability (G4.6), constraint weakening (G4.10), surface expansion
(G4.5's pincer half). **Three of eleven conditions exist only because
the implementer is an agent**; a human-team G4 would have been "review
and trust." This is the review-replacement thesis made concrete - and
why G4 is the pipeline's largest fully-mechanical gate: eleven
conditions, zero human.

Principles bearing:

- **Earliest decidable point (principle 4):** each condition sits at
  the first venue where its check is decidable on the true merge
  result - one venue earlier and the result doesn't exist, one later
  and the defect is shared state.
- **Spec-first properties (principle 5):** G4 is where immutability
  stops being an assertion and becomes a diff check - and where every
  G0-G2 instrument (criteria, baselines, rule tests, threat-model
  tests) is executed against the object by an operator that is not its
  author.
- **Detectability ladder (principle 1):** the (b)/(c) enforcement venue
  for everything the working diff alone cannot decide - cross-file
  clones, dependency edges, taint flows, merged-result conflicts.

Classes closed: injection (CWE-707: 79, 89, 78 - G4.7), calculation
(682 - G4.4, with G3.3/G2 upstream), error handling (703 - battery
rules + G1.3 item-8 criteria), architectural erosion + duplication
entropy (G4.2/G4.8), secret / vulnerable-dependency introduction
(G4.9), misinterpretation via traceability (G4.3), and agent
self-weakening - subject integrity, the kit's own class
(G4.5/G4.6/G4.10) ([taxonomy](../taxonomy.md)).

**The echo, received** (division ratified at the G3 walk): G3.1 -> the
explicit formatter job step (G4.1 clause 3); G3.2 -> the battery clause
(G4.1 clause 2) + the suppression audit (G4.10); G3.3 -> the merged
build under identical committed props (G4.1 clause 1). Single-sourced
configuration consumed verbatim by both venues; a local-pass/CI-fail
divergence is definitionally a PL-PIPE defect, never a Developer error.

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Objects per the frame rubric; operators per the close-out (QA
executes result-scoped conditions; the Verifier owns the diff-scoped
subject checks).

### G4.1 Inner-loop echo

Registry row renamed from "Full analyzer set": three clauses span
compile, battery, and formatter - the old name undersold two of them.

- **Shape (pass condition):** object = merged result. Three clauses
  mirroring G3's three conditions:
  1. **Build clause (G3.3 echo)** - the merged result builds under the
     identical committed strictness configuration. The gate's substrate
     (nothing else runs without it), stated as a clause so the
     strict-compile echo is explicit rather than incidental.
  2. **Battery clause (G3.2 echo)** - the declared battery produces
     zero diagnostics at gating severity, same committed config
     consumed verbatim. Superset rule: G4 may add, never drop or
     weaken - any CI-only members live as a tier flag *in the same
     committed config* (one file, tiers marked, default empty), so
     single-source survives the superset.
  3. **Formatter clause (G3.1 echo)** - verify mode reports zero
     deviations tree-wide, as an **explicit job step**: the whitespace
     verb's rule set and IDE0055-as-analyzer are not provably
     identical, so battery-clean does not imply formatter-clean.
- **Reference binding (.NET):** `dotnet build` of the merged solution
  under the committed `Directory.Build.props` + `.editorconfig`;
  battery via the same package/project references with
  `EnforceCodeStyleInBuild=true`; formatter step = `dotnet format
  whitespace --verify-no-changes` (identical to G3.1's gate form).
- **Gap status:** none beyond G3's own - every profile with a G3
  binding has this echo by construction (same tools, tamper-proof
  venue).
- **Why:** the pipeline never consumes G3's report - G3 runs inside the
  subject's context, so even with protected configs a green claim is
  unverifiable there. G4.1 is where battery status becomes *known*
  rather than *claimed*; and the first run against what main will
  become - semantic-merge findings surface only here.
- **Kind & loopability:** mechanical; identical diagnostics to G3's
  (per-rule, per-location, fix-carrying) - the same loop, one venue
  later.
- **Parameters:** CI-only tier contents = enforcement-pass material
  (default empty).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.2 Architecture tests

- **Shape (pass condition):** object = merged result. The
  architecture-rule partition of the test run is green; diagnostics per
  rule with the violating dependency edge. Partition semantics per the
  one-run model (see G4.11): G4.2 owns this partition's *evaluation*,
  not a separate execution.
- **Annotation carve-out (0011):** arch tests are exempt from criterion
  annotation - they witness ADR-fixed structural rules, not G1
  criteria; forcing REQ-IDs would fabricate traceability. The
  `[StructuralRule("ADR-nnnn")]` kind is reserved: the rung that later
  mechanizes G2.3 checklist item 6 (rules x tests as a join). Reserved,
  not built.
- **Reference binding (.NET):** NetArchTest suite in the spec-authored
  arch-test project; partition membership by project.
- **Gap status:** Java (ArchUnit), JS (dependency-cruiser), Python
  (import-linter) bind directly; a Rust profile is thinner - workspace
  privacy + custom lint compensate (documented rung difference; no
  build item until such a profile activates).
- **Why:** erosion is an entropy process - every diff locally
  plausible, only the rule test sees global structure - and agents
  *accelerate* it: generation-by-imitation replicates a bad dependency
  edge into every neighboring diff within days. G4.2 is G2's shape
  decisions holding at LLM speed.
- **Kind & loopability:** mechanical; rule + offending edge, loopable.
- **Parameters:** none open (rule content is G2's authored artifact).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.3 Acceptance suite + REQ-ID traceability

- **Shape (pass condition):** object = merged result. Three clauses:
  1. **Green** - the acceptance + security partitions pass.
  2. **Traceability total
     ([0011](../../decisions/0011-criterion-traceability-format.md))** -
     every criterion in the criteria records has >=1 *passing*
     annotated witness; every acceptance/property test carries >=1
     criterion annotation; no annotation references an unknown ID.
     Both directions closed: no untested criteria, no shadow-spec
     tests, no dangling refs.
  3. **Computed from records x results** - the join reads
     `criteria.yaml` x runner results (0011's script, pass mode),
     never source grep.
- **Reference binding (.NET):** xUnit `[Criterion("REQ-<task>-<nnn>")]`
  trait surfacing in TRX; the traceability script in pass mode over
  TRX + `specs/*/criteria.yaml`.
- **Gap status:** none - every mainstream runner has trait/tag/marker
  metadata surfacing in results (JUnit tags, pytest markers).
- **Why:** the misinterpretation closure. Criteria are the pipeline's
  requirement currency - G1.3 reviews them, G6.1 walks them, G8.3
  mints new ones - and G4.3 is where each is proven implemented: the
  red->green transition G2.5 armed, completed exactly once per
  criterion. The totality clauses keep the currency honest in both
  directions.
- **Kind & loopability:** mechanical; diagnostics name the criterion
  (uncovered / failing / dangling) or the unannotated test - loopable
  by the Developer (failing test) or routed upstream by name (missing
  criterion = spec-channel work).
- **Parameters:** format + script fixed by 0011; none open.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.4 Property tests

- **Shape (pass condition):** object = merged result. The
  property/metamorphic partition passes under a **derived seed** =
  f(merge-base sha, candidate sha): deterministic per candidate
  (retries reproduce exactly - no queue flake), fresh across
  candidates (generative value retained). The diagnostic carries the
  seed + the shrunk counterexample. Open-ended randomness is
  explicitly G5 territory (G5.2/G5.3 corpus work). Property tests join
  the annotation scheme uniformly - a property is a criterion shape
  (0011).
- **Reference binding (.NET):** CsCheck / FsCheck with seed injection
  from the derived value; shrunk counterexample + seed in the failure
  output; iteration budgets in committed run settings.
- **Gap status:** none - Hypothesis, jqwik, proptest, fast-check all
  take injected seeds.
- **Why:** the merge gate must be deterministic - a flaky gate is
  queue poison (retry storms, authority erosion) - but a fixed-forever
  seed decays the suite into example tests. The derived seed is the
  point between: candidate-stable, population-diverse.
- **Kind & loopability:** mechanical; seed + counterexample is a
  complete reproduction recipe - loopable.
- **Parameters:** iteration budgets = enforcement-pass config (G1.2
  state-space-bounds precedent).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.5 API surface diff

- **Shape (pass condition):** object = merged result vs locked
  baselines. Every declared public surface **equals** its baseline -
  bidirectional: nothing beyond it, nothing missing from it; deviation
  = FAIL with the surface delta as diagnostic. On spec-channel
  candidates - the only place baselines legitimately move - the check
  runs in breaking-classification mode as report-to-approver
  (mirroring G4.10's channel semantics); the merge path itself carries
  zero judgment.
- **The pincer (with G4.6):** a surface change without a baseline
  update fails here (surface != baseline); a baseline update without
  channel provenance fails G4.6. No path exists by which the Developer
  changes a public surface - not "requires approval": *does not
  exist*. The registry row's "unapproved" dissolved into 0010's
  channel provenance.
- **Baseline timing (G2.2):** Unshipped entries are authored at G2
  lock, pre-implementation - the scaffold fixes the intended surface
  and the implementation must land exactly on it. The .NET
  add-as-you-code convention is exactly what we don't do
  (capture-timing contamination). Shipped-promotion = release-side
  mechanics (G7.2 adjacency).
- **Reference binding (.NET):** PublicApiAnalyzers RS0016 + RS0017 as
  errors over `specs/baselines/<assembly>/PublicAPI.*.txt` (relocated
  via `AdditionalFiles`; the wiring props are class E); oasdiff /
  `buf breaking` in spec-channel classification mode.
- **Gap status:** Java (japicmp/revapi), TS (api-extractor) bind; a
  Python profile is thinner (no standard surface baseline - stub-diff
  compensation, documented on activation).
- **Why:** a breaking change is only detectable relative to a baseline
  predating the code (principle 4); and the pincer closes the "agent
  quietly widens its own surface" hole by construction.
- **Kind & loopability:** mechanical; per-symbol diagnostics; the
  routing diagnostic names the legitimate path ("surface changes
  require a spec-channel re-lock, G2.2").
- **Parameters:** none open.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.6 Write-surface immutability

Registry row renamed from "Spec-path immutability"
([0010](../../decisions/0010-write-surface-immutability.md)): allowlist
polarity makes the invariant broader than spec paths - *the Developer's
write surface is closed*.

- **Shape (pass condition):** object = candidate diff (merged result
  vs main-at-queue-time; adds, modifies, deletes, renames, mode
  changes all count). Per 0010: every delta lands inside the committed
  write-surface manifest's writable set, or carries its class's
  channel provenance - class S (spec, `specs/**`) legitimate only on
  spec-channel candidates exiting G1/G2 sign-off; class E (enforcement
  layer, incl. the manifest itself) only with PL-PIPE.1 second-channel
  approval. Implementation candidates have no bypass. Manifest absent
  or empty = FAIL.
- **Reference binding (git/CI):** the write-surface audit job (build
  item): `git diff --name-status <main-at-queue> <merged>` evaluated
  against the manifest (repo root, reference name
  `write-surface.yaml`); writable reference set `src/**`,
  `tests/unit/**`.
- **Gap status:** none - the mechanism is git + CI, ecosystem-free by
  construction. The kit's second zero-gap condition (G3.1 was the
  first).
- **Why:** the mutability model's teeth. Every spec artifact is
  immutable to the implementer *by mechanism* - principle 5's
  test-editing logic ("an agent that can edit the test will") applied
  to every enforcing artifact at once. Allowlist polarity fails
  closed: new artifact classes are born protected - twice during the
  walk a whole condition-candidate (IaC scanning; ratchet-baseline
  existence) dissolved because the allowlist already covered its
  threat.
- **Kind & loopability:** mechanical; path + class + governing channel
  in the diagnostic (routing diagnostic: names where the change must
  go, not just "no").
- **Parameters:** exact writable globs = pilot binding; mechanism
  fixed by 0010.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.7 Taint/security scan

- **Shape (pass condition):** object = merged result. **Zero findings
  at gating severity, tree-wide - ratchet-at-zero** (G3.3 clause-2
  shape), not baseline-relative: findings-vs-main diffing normalizes a
  standing-debt pool, SARIF fingerprint matching flakes across
  refactors, and a committed findings-baseline is suppression-shaped.
  FP dismissals exist only as committed class-E suppression config
  (second-channel approved, G4.10-watched vectors 2/4); platform-side
  dismissal UIs are not the mechanism (outside the diff machinery's
  sight). Retrofit bootstrap: a frozen shrink-only legacy baseline as
  documented compensation - bootstrap material, not the shape.
- **Reference binding (.NET):** CodeQL (default + security-extended
  packs) + Semgrep with committed rule config; SARIF to the gate;
  suppression file committed, class E.
- **Gap status:** language coverage varies by scanner but every
  plausible profile has a taint engine; pack selection is per-profile
  config.
- **Why:** ADR 0002's carve-out - detectors as *members* of a
  spec-first stack where the pattern is the defect signature;
  injection is the canonical case, and interpolated-SQL-by-imitation
  is a characteristic agent failure mode worth a dedicated tripwire.
  CWE tags on scanner findings are stratum (a) of the battery-CWE map
  - the taxonomy's 707 rows draw their golden-test evidence here.
- **Kind & loopability:** mechanical; source->sink trace per finding,
  loopable. Division from G4.1, stated once: battery = in-build
  analyzers; G4.7 = the out-of-build deep scanner - different latency
  class, first candidate to split if the minutes budget breaks.
- **Parameters:** gating severities (reference: errors + warnings) and
  pack selection = enforcement-pass config.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.8 Duplication + complexity ratchets

- **Shape (pass condition):** object = merged result, tree-wide (clone
  detection is inherently global). Four clauses:
  1. **Duplication** - measured metric <= the committed shrink-only
     baseline (captured from main at bootstrap - a measurement, not a
     policy number).
  2. **Complexity** - every method within the authored per-method
     budget (a Q4 policy number); violations counted against a ratchet
     starting at zero on greenfield.
  3. **Fail-if-missing** - absent budget or baseline = FAIL (the
     anti-vacuity pattern).
  4. **Static between tightenings** - baselines move only at G9's
     scheduled tightening events (cadence Q4); no auto-capture on
     improvement (transient dips must not lock floors). Ratchet
     artifacts are class E under 0010 with **direction-conditional
     channel weight**: mechanically direction-verified tightenings
     auto-approve (monotone-safe - the automation can only strengthen
     the gate); any loosening takes the full second channel.
- **Reference binding (.NET):** jscpd or PMD CPD (selection =
  enforcement pass) for duplication; complexity via
  CA1502/CA1505/CA1506 thresholds in committed config; ratchet state
  under `specs/ratchets/` (residence banked; class E governance).
- **Gap status:** none - clone detectors and complexity metrics are
  ecosystem-universal.
- **Why:** trend-defects. No single diff is the violation - the slope
  is - and the ratchet is the only gate shape converting a slope into
  a per-merge mechanical fact. Agent-sharpened: duplication is the
  dominant agent entropy vector (copy-adapt is the cheapest token
  path); complexity budgets are context-window hygiene - an
  over-budget method degrades the agent's own future economics.
  Division restated: no coverage ratchet exists anywhere - adequacy is
  G5.5's mutation floor. G3.1 tie: canonical form stabilizes what the
  clone detector measures.
- **Kind & loopability:** mechanical; clone pairs with both locations
  / method + value vs budget - loopable.
- **Parameters:** Q4, now purely numeric - budget values, capture
  parameters (min clone length et al.), G9 cadence.
- **Lifecycle:** `specified` (ratified 2026-07-24; shape closed, Q4
  numbers open).

### G4.9 Secret/dependency audit

The repo's trust boundary policed in both directions - credentials
leaking out, foreign code trusted in. Bundled, with a recorded rubric
exception: clause objects differ ((a) diff, (b) delta, (c) result
state), but the row is registered, all clauses share one operator and
one character (hygiene against external knowledge), and no
subject-check dimension exists - the G4.10 split tracked an operator
boundary, not object purity alone.

- **Shape (pass condition):** three clauses:
  1. **Secrets** - no secret material in the candidate diff.
     Diagnostics masked (never echo the value into CI logs - leak
     amplification) and rotation-first ("removal does not un-leak;
     rotate the credential"). Fixture-dummy allowlist = class E.
  2. **Dependency introduction** - the dependency-graph delta,
     evaluated over the **locked graph**, introduces no
     advisory-matched or license-disallowed package. Locked-graph
     precondition: lockfile committed + enforced restore; absent or
     floating = FAIL (delta semantics presuppose it; merged-build
     determinism does too). Advisory-DB snapshot pinned per run;
     diagnostic names advisory + package + clean version.
     Upgrade-to-vulnerable counts as introduction.
  3. **SLA backstop** - no dependency past its G9.2 remediation
     window. The deliberate soft-seize: within the window a standing
     advisory never blocks unrelated merges (no pipeline seizure by
     overnight CVE); past it, everything blocks.
- **Reference binding (.NET):** gitleaks (diff mode) for secrets;
  NuGetAudit + `packages.lock.json` with `RestoreLockedMode=true`;
  license allowlist over the lock graph; SLA state fed from G9.2's
  tracking.
- **Gap status:** none - secret scanners are language-free; every
  ecosystem has an advisory audit and lockfile enforcement.
- **Why:** supply-boundary hygiene at the choke point. Division from
  G9.2 fixed: G4.9 polices what candidates *introduce* (+ the SLA
  backstop); G9.2 owns newly-disclosed-in-place on its own cadence -
  the timeline partitioned with no gap and no overlap. Same split
  applied to licenses: new deps clear the allowlist here; G9.3 keeps
  the standing-set sweep.
- **Kind & loopability:** mechanical; per-clause diagnostics (masked
  location + class / advisory + package + remediation / package +
  deadline), loopable.
- **Parameters:** SLA windows = G9.2 policy (S11 walk); license
  allowlist content = policy artifact (class E).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.10 Suppression audit

Adopted this session (roster addition; the G3 walk's banked export).
Diff-scoped and Verifier-owned - split from G4.1 because the frame
rubrics do real work: the battery run is result-scoped QA territory;
this is a subject check on the change-act.

- **Shape (pass condition):** object = candidate diff. The diff
  introduces no new weakening of any gating constraint - four
  ecosystem-free vectors:
  1. in-source suppression constructs (pragmas, suppression
     attributes, inline disables - incl. test-disabling constructs:
     skip/ignore annotations, the suppression of G4.11 by other
     means);
  2. severity downgrades / rule de-listing in analysis config;
  3. strictness-flag weakening in build config;
  4. exclusion-scope widening (generated-code globs, per-path
     exemptions, test-category exclusions, quarantine-list additions).
  On implementation candidates all four FAIL - vectors 2-4 are
  path-blocked by G4.6 already, kept here as defense-in-depth with the
  sharper diagnostic ("you downgraded CA2000" beats "you touched
  .editorconfig"); vector 1 is the audit's unique content - the one
  tamper vector inside the legitimate write surface. On
  channel-approved candidates the audit reports the weakening to the
  approver rather than blocking (Q7 binding).
- **Reference binding (.NET):** the write-surface audit job (one diff
  computation with G4.6): `#pragma warning disable`,
  `[SuppressMessage]`, `GlobalSuppressions.cs`, `// Stryker disable`
  comments (S9 cascade - G5.5's dismissal ruling bans in-source
  mutation ignores), `<NoWarn>`, severity downgrades in
  `.editorconfig`, strictness-flag edits in props, exclusion-glob
  edits, `Skip=` / `[Ignore]` / category-exclusion edits.
- **Gap status:** the audit job is a kit build item (0008 register);
  vector construct lists are per-profile (every ecosystem has pragma
  and skip forms).
- **Why:** G3.2 clause 3's enforcement locus - the battery must be
  clean *and unweakened*, and in-source suppression is the one channel
  config protection cannot see. Baseline-shifting as a fifth vector:
  rejected - already covered path-wise (class S) and direction-wise
  (G4.8 tighten-only).
- **Kind & loopability:** mechanical; vector + location + the weakened
  rule - loopable, and the routing diagnostic names the legitimate
  channel (severity changes = PL-PIPE.1).
- **Parameters:** none open (construct lists = binding material).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G4.11 Full test execution

Adopted this session (roster addition; the G3 walk's banked candidate -
rejected there, because running your own tests is the loop, not a gate,
and adopted here, where the venue is trusted).

- **Shape (pass condition):** object = merged result. The complete
  discovered test suite executes green - unit partition included. The
  **one-run partition model's totality owner**: every discovered test
  belongs to a partition (arch / acceptance+security / property /
  unit-remainder) and every partition executed. Zero tests discovered
  = FAIL (G2.5 precedent); skipped count zero outside the committed
  quarantine list (class E; additions are G4.10 vector-4 material).
- **Reference binding (.NET):** `dotnet test` solution-wide; TRX
  totality check (projects executed x tests discovered x skips vs
  quarantine).
- **Gap status:** none - test runners are universal.
- **Why:** a red unit test at merge means the candidate fails its own
  author's stated checks - an incoherence no pipeline should merge.
  And G5.5's floor presupposes a green suite (mutation over red is
  meaningless): **G4.11 is G5.5's named precondition**, enforced one
  gate earlier. Division from G4.3 (no double-counting): G4.11 owns
  run totality + the unit partition; G4.3 owns traceability.
- **Kind & loopability:** mechanical; failing test with output - the
  Developer's most familiar loop diagnostic.
- **Parameters:** flaky-test retry/quarantine policy =
  enforcement-pass material (quarantine residence fixed: class E,
  audited).
- **Lifecycle:** `specified` (ratified 2026-07-24).

## Completeness check

Gate purpose: everything minutes-decidable on the merged result blocks
before main; the check asks what escapes eleven conditions. Examined:

- **The authored line.** The source table gave G4 "regression tests
  from review findings" - human-SDLC residue; no reviewer exists here.
  Ruled: G4 is execution-only (authors nothing; joins G5). Conversion
  loops live where findings originate - G6 findings and G8.3 escapes;
  a G4 catch needs no new criterion by definition (the gate already
  existed). Registry line corrected in the cascade.
- **Venue semantics.** "Merge queue / PR CI" hid a real distinction -
  the stale-base race. Ruled into the identity: queue authoritative,
  PR CI advisory preview.
- **CWE-703 coverage.** The Closes line credits G4 with error
  handling; substantiation: the battery's swallowed-catch family
  carries the (c) rung - 703 joins the stratum-(b) hand-tag set - and
  the spec side (does the system behave correctly under failure?) is
  already mandated upstream: G1.3 checklist item 8 requires an
  error-path criterion per input surface (verified this session; no
  retrofit needed). The taxonomy's 703 row already names G4.1.
- **Locked graph + license introduction.** Two G4.9(b) elaborations
  absorbed (within-ratified-shape): delta semantics presuppose a
  pinned graph (fail-if-missing); new deps clear the license allowlist
  at merge, G9.3 keeps the in-place sweep.
- **Examined and rejected:** commit-message gating (no defect class of
  its own); IaC scanning at G4 (the allowlist excludes infra from the
  write surface - the second condition-candidate the allowlist
  absorbed); performance at G4 (CI-runner noise makes minutes-scale
  benchmarks lies - G7.1's venue is correct); doc conditions
  (PL-DOC's; venue overlap noted).
- **Pillar sweep verdict:** everything minutes-decidable on the merged
  result is covered; the residue (mutation, fuzz, differential,
  concurrency, contract, perf) is cadence-bounded downstream, not
  gapped.

Roster verdict: complete at eleven - two adopted this session (G4.10,
G4.11), zero further additions; two registry corrections queued
(authored line, venue line) and two renames (G4.1, G4.6).

## Operators & harness

The QA agent executes everything result-scoped - the merged build, the
one-run partitions, the scanners, the ratchets - and owns the gate's
execution. The Verifier owns the diff-scoped subject checks - G4.6 +
G4.10, its **deterministic core** - implemented as one write-surface
audit job (one diff computation, two conditions' diagnostics). The
Developer operates nothing at G4 but is the diagnostics' primary
consumer: loopable findings route back to its inner loop; subject-check
findings route upstream *by name* (spec-channel re-lock, PL-PIPE.1) -
the routing diagnostic is the kit's cheapest anti-gaming instrument.
The CI definition implementing all of this is class E (PL-PIPE): one
Developer-editable workflow line would delete every gate in one diff.
No human appears at G4 by design - the pipeline's attention stays
concentrated at G1.3 and G6.

## Decisions & open items

- All eleven conditions `specified` 2026-07-24 (session-8 walk: eight
  stops, every ruling ratified in-conversation before edits landed).
- Frame rulings: object rubric (merged result vs candidate diff);
  object/subject operator split; minutes budget as admission rule;
  echo receiving-end table; CI definition = class E.
- Q1 closed -> [0010](../../decisions/0010-write-surface-immutability.md):
  write-surface manifest + CI diff audit; allowlist polarity; channel
  provenance (class S spec sign-off / class E PL-PIPE.1; no
  implementation bypass); fail-if-missing; harness as explicit trust
  root. G4.6 renamed.
- Traceability format fixed ->
  [0011](../../decisions/0011-criterion-traceability-format.md):
  `REQ-<task>-<nnn>`; `criteria.yaml`; results-surfacing annotations;
  totality both directions; one script, three modes. G4.3's open note
  closed; G2.4/G2.5's shared parameter closed.
- Roster additions ratified: G4.10 suppression audit (four vectors,
  Verifier-owned, G3.2 clause-3 locus) and G4.11 full test execution
  (one-run totality owner, G5.5's precondition). Counts 48 -> 50; 23
  `specified`.
- Renames: G4.1 "Full analyzer set" -> "Inner-loop echo"; G4.6
  "Spec-path immutability" -> "Write-surface immutability" (0008
  rename precedent).
- Ratchet shape closed (banked G2 package + direction-conditional
  channel weight - the Q7 worked example); Q4 residue purely numeric.
- Detector rulings: G4.7 ratchet-at-zero with the class-E FP path;
  G4.9 timeline partition with G9.2 (+ license split with G9.3;
  locked-graph precondition).
- Build-item register consolidated to four: sunset-escalation
  analyzer; write-surface audit job (absorbs the suppression-audit
  check); battery-CWE map + golden test (three strata: vendor-shipped
  imports, taxonomy-load-bearing hand-tags incl. 703, tier-level style
  tag); traceability script + fixture corpus.
- S9+ inputs banked: G5 session - G4.11 as G5.5's stated precondition;
  native-interop gap and generated-input oracle scope (carried). G6
  session - G6.1 walks `criteria.yaml`. S11 - G9 tightening-job shape,
  SLA windows, license-sweep division. S12 - Q7 channel-weight tiering
  example; PL-PIPE.2 fixture pattern (traceability + battery golden
  tests).
