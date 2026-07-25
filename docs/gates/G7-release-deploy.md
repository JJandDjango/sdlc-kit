# G7 - Release / Deploy

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Release / Deploy gate
> contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 7;
> the G5 promotion ladder ([G5 page](G5-integration-system.md)); the G6
> acceptance record ([G6 page](G6-uat-staging.md)); ADRs
> [0007](../../decisions/0007-hard-core-designation-criteria.md),
> [0010](../../decisions/0010-write-surface-immutability.md). Two-layer
> per [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** the release pipeline - the *same* committed environment
  definition and deploy pipeline G6.3 certified, parameterized by
  target and nothing else (frame ruling). By the time G7 fires, this
  exact deploy operation has been rehearsed against staging *for this
  exact artifact*, per candidate rather than per quarter - ODC
  build/package defects die at the rehearsal. The pipeline definition
  is class E, PL-PIPE-governed; its interlocks are golden-testable
  under PL-PIPE.2.
- **Vocabulary** (frame ruling): *release* = the admitted candidate
  plus its versioned artifact set; *deploy* = placing it in the
  production venue; *rollout* = progressive traffic exposure (canary
  -> cohorts -> full). G7 spans admission through rollout completion;
  G8 is steady state beyond it.
- **Cadence:** per release. Deploy *timing* is business policy outside
  the gate: G7 rules whether a release *may* ship, never when it must.
- **Inputs:** the accepted candidate (verified artifact, pinned sha);
  the acceptance record (class S, per the G6 page); the G5.1
  verification matrix; the SLO declarations + performance budgets
  (spec set, class S); the committed environment definition.
- **Admission** (frame ruling) - the venue refuses to convene unless
  four interlocks hold; conditions judge the candidate, admission is
  the venue refusing to sit without its inputs:
  1. **Record** - acceptance record present, verdict accepted, no
     unresolved blocking findings. Default-deny carries forward: no
     record, no release.
  2. **Artifact identity** - the deploy subject is digest-identical to
     the artifact the record covers: G5 verified *it*, G6 accepted
     *it*, G7 ships *it*. No rebuild lane - rebuilding un-verifies
     (the G5 ruling carried to its end). The provenance attestation
     (G7.5) is this interlock's mechanical substrate, and the
     production environment-definition hash must match the certified
     hash modulo the declared-delta allowlist.
  3. **Can-i-deploy** - the G5.1 verification matrix closes over the
     *target environment*: every consumer/provider version pair that
     will coexist after this deploy has a green verification. G5.1
     checked the artifact; admission re-queries environment-scoped,
     because deploy is the moment the version *set* changes.
  4. **No standing G8 red** on the target service - error-budget
     exhaustion (G8.2), assertion fires (G8.1), aging unconverted
     escapes (G8.3) all funnel into this one check. Fix-lane
     exception: a release whose task contract references the open red
     may admit - the red blocks features, never the fix.
  Enforcement is structural (the pipeline definition itself), on the
  G4 precedent: queue semantics were frame, not condition.
- **FAIL blocks:** the deploy; a failing canary auto-reverts the
  rollout (G7.4). **Rollout completion** = final stage at 100% held
  for the declared full-exposure window with G8.2 green; G7 closes
  there, and that is the moment the binary baseline captures (G7.2)
  and the artifact becomes "the production version" - not at first
  deploy byte.
- **V-model position:** the mechanical re-entry after the human
  boundary - everything here re-verifies *fitness to ship* (budgets,
  compatibility, infrastructure, integrity) against artifacts authored
  upstream; nothing re-judges intent. The last gate before live
  traffic.
- **Trust boundary:** fully mechanical, zero human conditions, QA
  executes (frame ruling). The human release judgment already happened
  - it *is* the acceptance record. The source table's release-manager
  sign-off is human-SDLC residue, rejected at close-out.

## Why this gate exists

Three regression families are only decidable at the ship boundary:
performance against absolute budgets (measurable only on quiet,
fingerprinted infrastructure), compatibility of the *shipped* form
(the packaged binaries consumers link, not the source surface G4.5
froze), and infrastructure safety of the definition about to take
production effect. G7 also carries the artifact-integrity residue:
proving the thing shipped is the thing verified (G7.5, adopted this
walk). The gate re-verifies nothing upstream gates proved - each
condition here binds a baseline or budget *no earlier venue could
bind* (last-ship baselines, current advisory feeds, live-cohort
comparison).

Principles bearing:

- **Earliest affordable venue (principle 4):** last-ship baselines
  and current-feed scans are undecidable before a release exists;
  canary verdicts are undecidable before live traffic. Nothing here
  could run earlier; everything here still blocks.
- **Spec-first properties (principle 5):** budgets, SLO declarations,
  break records, and the chaos/rollout policies are all authored
  upstream (G1/G2 spec channel or class E enforcement channel) and
  executed here by an operator who is not their author.
- **Detectability ladder (principle 1):** the ladder's production
  rungs - statistical comparison on quiet infra, cohort A/B under
  ambient load - the last mechanical venues, entered only with the
  human boundary already passed.

Classes closed: performance (CWE-400, 407 - absolute half of the S9
soak split; trend half at G5.7), build/config/deployment (ODC
build/package - the rehearsal + G7.3), binary-compatibility breaks
(interface class at the shipped boundary - G7.2), artifact integrity
(CWE-494 family, SLSA build-tampering/substitution - G7.5)
([taxonomy](../taxonomy.md)).

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Object default: the admitted release (verified artifact +
its packaged form + the pinned environment definition). The component
designation record (`specs/components.yaml`, class S) scopes G7.1
via its budget-designated column.

### G7.1 Benchmark budgets

The absolute half of the S9 performance split: G5.7 gates trend
shapes over soak windows; G7.1 gates absolute ceilings on quiet
infrastructure at the ship boundary.

- **Shape (pass condition):** object = the admitted release, executed
  on a declared quiet runner class. Clauses:
  1. **Budgets-only gate** - every budget-designated operation's
     measured statistic lands within its authored ceiling; budgets
     are (operation, statistic, ceiling, fingerprint) tuples in the
     spec set (class S, authored at G2, requirement-derived where an
     SLO decomposes). No relative-regression clause - examined and
     rejected (close-out): it doubles the flake surface on the
     noisiest measurement class, and creep-within-budget is owned by
     G9's tightening loop (0010 direction-conditional: tightenings
     auto-approve), which reclaims slack headroom on cadence.
  2. **Per-fingerprint binding** - the runner-class fingerprint is
     recorded; budgets bind per-fingerprint, and a fingerprint with
     no matching budget = FAIL, not silent pass.
  3. **Committed protocol** - warmup, iteration count, outlier policy
     in committed config (class E); the verdict is single-shot on the
     protocol's output, no retry-to-green.
  4. **Noise-floor guard** - the protocol measures dispersion; a
     budget whose margin over current observed is inside the noise
     floor is rejected *at authoring* as unenforceable. A gate that
     flakes is a gate that gets ignored - the kit's own thesis.
  5. **Vacuity guard** - a budget-designated operation with no
     discoverable benchmark = FAIL (zero-tests-FAIL transposed).
  6. **Measurement record** - every green run commits one; it never
     gates. It is G9's tightening input and the audit trail.
- **Reference binding (.NET):** BenchmarkDotNet on a dedicated runner
  class; fingerprint = hardware class id; benchmark definitions are
  spec-channel executable criteria (class S, Developer-immutable per
  0010 - a Developer who can rewrite the benchmark can benchmark the
  fast path); records land in the release record set. Bootstrap
  variant (Q6 pilot family): first green run's measurements + margin
  *proposed* as budgets through the spec channel.
- **Gap status:** none - benchmark harnesses exist per ecosystem;
  profiles bind their own runner discipline.
- **Why:** absolute ceilings are the only performance statement a
  release can make that is independent of history; the ratchet loop
  (G9) converges them toward observed reality so headroom cannot
  silently accumulate. Budget authorship is upstream (G2) because the
  implementer never authors their own pass bar - the source table's
  "budgets authored at release" was human-SDLC residue, corrected
  this walk.
- **Kind & loopability:** mechanical; diagnostic = per-operation
  measured-vs-ceiling with dispersion - loopable, though the loop
  consumer is usually the spec channel (budget revision) or the
  Developer (regression fix).
- **Parameters:** ceiling values, margin sizes, statistic defaults
  (p50 vs p95 per operation class), iteration counts = **Q4**.
- **Lifecycle:** `specified` (ratified 2026-07-25).

### G7.2 ApiCompat binary compatibility

Not G4.5 re-run later: G4.5 gates the *designed* surface (source
level, per merge, bidirectional equality against the G2.2 lock);
G7.2 gates the *shipped* surface (binary level, per release, against
the last ship). Neither subsumes the other - G4.5 never sees the
package, and binary compatibility is a different relation than source
compatibility (field->property, struct->class, default-parameter
changes are source-clean, binary-breaking).

- **Shape (pass condition):** object = the shipped package set, every
  assembly, every TFM in the package manifest. Baseline = the last
  shipped release on the line. Clauses:
  1. **Compatibility relation** - consumer-linkable surface
     compatible at the binary level; a TFM present in baseline but
     absent in candidate is a break; a new TFM is additive.
  2. **Declared-break discipline** - a binary-breaking delta passes
     only when matched to a spec-channel break record; the
     suppression file is class S, Developer-immutable (G4.10's
     polarity). No silent breaks ship.
  3. **Version coherence** - the version increment matches the
     measured delta class: identical -> patch permitted; additive ->
     minor+; breaking -> major *and* the break record. "Shipped a
     break as a patch" dies here mechanically.
  4. **Baseline capture** - on rollout completion the shipped set
     auto-commits as the new baseline: a class-E pipeline job writing
     a factual record, never a judgment. Bootstrap: first release on
     a line runs vacuously green and *records*.
- **Reference binding (.NET):** Microsoft.DotNet.ApiCompat over all
  packaged TFMs; the computed diff is retained as the release's
  contract-diff payload - G10's consumer notification consumes it
  (banked S11).
- **Gap status:** ecosystems where shipped form = source form bind a
  package-level surface diff (e.g. `.d.ts` diff) or register a 0008
  gap-closure item; the shape never bends.
- **Why:** the compiled-consumer contract and packaging-layer
  divergence are invisible to every source-level venue; the ship
  boundary is the first moment the shipped form exists to check.
- **Kind & loopability:** mechanical; diagnostic = per-member compat
  violations + delta classification - loopable.
- **Parameters:** none open - relations and record shapes fixed;
  line/support-window policy is business policy.
- **Lifecycle:** `specified` (ratified 2026-07-25).

### G7.3 IaC scanning

No separate "IaC" artifact class exists: the subject is exactly the
committed environment definition + deploy-pipeline configuration that
G6.3 certifies and admission hash-matches - the class E set the
pipeline already governs. G7.3 is the static half of a pair G6.3
completes dynamically: G6.3 proves the definition *deploys and runs*,
G7.3 proves it *contains no known-bad configuration*.

- **Shape (pass condition):** object = the pinned environment
  definition + deploy-pipeline config the release will use, across
  **every committed target instantiation** (a staging-only hole is
  still a hole in a certified venue). Clauses:
  1. **Zero findings at gating severity, current advisory feeds** -
     ratchet-at-zero, never baseline-relative (G4.7 transposed): a
     misconfiguration is a defect, not entropy to pay down. An
     unchanged definition can legitimately go red between releases -
     the feeds moved (the G4.9 logic).
  2. **Dismissal discipline** - false-positive dismissals only via
     committed class-E suppression config, which takes PL-PIPE.1's
     second channel to change.
  3. **Secrets rules on** - G4.9 owns secret material in the code
     diff, G7.3 owns it in the definition; two artifact sets, no gap.
  4. **Vacuity guard** - scan didn't run, or discovered zero
     scannable resources against a non-empty definition = FAIL.
  5. **Echo venue** - the same scan blocks enforcement-layer CI on
     any change to the definition (authoring-time, minutes-loopable);
     the per-release run at G7 is authoritative (G4's
     preview/authoritative split).
- **Reference binding:** trivy config-mode as the multi-format
  default; PSRule where the definition is Azure-shaped. Two-layer
  nuance, named deliberately: G7.3 is the first condition whose
  binding keys off the **infrastructure format, not the language
  ecosystem** - a .NET shop on Terraform and a .NET shop on Bicep
  bind different scanners to the same shape.
- **Gap status:** none at shape level; per-format scanner gaps
  register 0008 items as usual.
- **Why:** the definition takes production effect at deploy; the
  release is the last moment before that effect, and the only venue
  where "current feeds" and "the version about to ship" coincide.
- **Kind & loopability:** mechanical; diagnostic = per-resource
  finding with rule id - loopable by the enforcement channel
  (definition fixes are class E work, never Developer work).
- **Parameters:** gating severity threshold = policy config (class
  E); reference default: high+.
- **Lifecycle:** `specified` (ratified 2026-07-25).

### G7.4 Canary with SLO-based rollback

The intra-rollout gate (frame ruling): this candidate's exposure may
not progress past a breach, and breach auto-reverts. Its inter-rollout
sibling is G8.2 - one SLO declaration feeds both (the SLO pair,
ruled stop 5).

- **Shape (pass condition):** object = the rollout, over the staged
  exposure ladder from committed rollout policy (class E). Clauses:
  1. **Dual-clause verdict per stage** - (a) *absolute*: the canary
     cohort breaches no SLO from the service's declaration
     (`specs/<service>/slo.yaml`, class S); (b) *relative*:
     canary-vs-control delta stays within declared degradation
     bounds, control = the incumbent version under the same ambient
     load.
  2. **Sample-floor guard** - a stage cannot verdict without its
     declared minimum sample; the window extends to a timeout, and
     timeout-without-sample = FAIL, not skip. A low-traffic service
     must author longer windows or synthetic load - you cannot
     certify what you cannot measure (the noise-floor guard's
     sibling).
  3. **Auto-revert, no manual-continue lane** - breach reverts the
     rollout; a continue-past-breach lane is an alarm that does not
     block. A re-attempt of the same artifact is a fresh admission
     with the red dispositioned - no automatic retry-to-green, but
     ambient causes exist, so a human-dispositioned re-admission is
     legitimate.
  4. **Assertion-fire wire** - any G8.1 gated-set fire inside the
     canary cohort is an immediate stage-FAIL -> revert (the
     cheapest catch of a regression mid-exposure).
  5. **Migration revert-safety** (close-out clause) - auto-revert is
     only sound if the incumbent still runs against the migrated
     schema. Carried migrations are classified expand/contract with
     the classification committed; expand-class ships freely;
     contract-class ships only referencing a completed predecessor
     rollout (N+1 discipline). Far end lands at G10.3 (banked S11).
  6. **Completion** - final stage at 100% held for the declared
     full-exposure window with G8.2 green closes G7 (baseline
     capture + production-version designation fire here).
- **Reference binding:** progressive-delivery tooling per infra
  (Argo-Rollouts-style controllers, deployment slots); canary
  analysis rules **compiled from `slo.yaml`** - the compile step is
  mechanical and golden-tested under PL-PIPE.2, so the enforced
  thing provably matches the declared thing (G5.6's mapping-totality
  logic transposed to monitoring).
- **Gap status:** none at shape level - staged exposure and cohort
  comparison are ecosystem-universal; profiles bind their delivery
  controller.
- **Why relative gating here after its rejection at G7.1** (stated to
  preempt the consistency challenge): benchmarks measure the same
  code twice on quiet infra with tool-grade repeatability - the
  ratchet owns creep, a relative clause only adds flake. A canary
  compares two live cohorts under *identical* ambient conditions -
  there the delta is the cleanest causal signal available and the
  absolute numbers are the noisy ones. The cost asymmetry also
  inverts: missed creep at G7.1 is headroom spent; a missed
  regression here is an incident.
- **Kind & loopability:** mechanical; diagnostic = per-stage verdict
  with breaching SLI + cohort deltas; the loop consumer is the fix
  task (revert already happened - the gate's remedy is never manual
  repair of a live rollout).
- **Parameters:** ladder stages + durations = rollout policy (class
  E); confidence parameters + minimum-sample derivation constants =
  **Q4**. SLO targets themselves are per-service spec values, never
  Q4.
- **Lifecycle:** `specified` (ratified 2026-07-25).

### G7.5 SBOM + provenance attestation

Adopted at this walk's close-out (roster addition; mechanical). The
registry's authored-here line named SBOM/provenance with no condition
enforcing it; and admission interlock 2 was already *assuming* a
trustworthy digest chain - this condition is that chain's mechanical
substrate.

- **Shape (pass condition):** object = the shipped artifact set.
  Every shipped artifact carries:
  1. **SBOM** - a generated software bill of materials, committed to
     the release record set.
  2. **Provenance attestation** - a signed attestation binding
     artifact digest -> pipeline run -> source sha, verified at
     admission (interlock 2 consumes it).
  Missing either = nothing ships.
- **Reference binding:** CI-platform attestation (SLSA provenance);
  CycloneDX SBOM emission at package time.
- **Gap status:** none - attestation and SBOM tooling are
  ecosystem-universal at the CI layer.
- **Why:** the artifact-integrity class (CWE-494 family, SLSA
  build-tampering/substitution): the verified-artifact chain
  G5 -> G6 -> G7 is a provenance chain, and formalizing it as a
  signed attestation gives it teeth outside the repo. The SBOM is
  what G9.2's vulnerability response needs to answer "which shipped
  versions carry CVE-X" about the *field*, not the repo (banked
  S11).
- **Kind & loopability:** mechanical; diagnostic = missing/unverified
  attestation or absent SBOM - loopable by the enforcement channel.
- **Parameters:** none open - formats are reference-binding detail.
- **Lifecycle:** `specified` (adopted + ratified 2026-07-25).

## The release record set

G7's committed residue - all factual pipeline records (contrast the
acceptance record, which is judgment):

- **Measurement record** (G7.1) - per green run; G9's tightening
  input.
- **Binary baseline** (G7.2) - captured at rollout completion; next
  release's comparison point.
- **Contract-diff payload** (G7.2) - G10's consumer-notification
  input.
- **SBOM + provenance attestation** (G7.5) - the field inventory and
  the identity chain.

All auto-written by the pipeline (class E jobs); none is a judgment;
each is consumed by a named downstream venue.

## Completeness check

Gate purpose: nothing ships that regresses performance,
compatibility, or infrastructure safety - plus artifact integrity;
the check asks what escapes five conditions. Examined:

- **Release-manager sign-off.** Rejected as human-SDLC residue: the
  human judgment *is* the acceptance record (G6); G7 verifies
  fitness, never re-judges. Deploy timing is business policy.
- **Relative perf regression.** Rejected at G7.1 (flake surface;
  G9's ratchet owns creep) and re-admitted in the one venue where
  relative is the *clean* signal: the canary's cohort delta (G7.4).
- **Rollback capability.** Real gap, resolved as a **G6.3 cascade**:
  the certified rehearsal gains a deploy -> revert -> redeploy leg,
  so every candidate's revert is exercised before production needs
  it. G7.4's auto-revert then runs a per-candidate-rehearsed
  operation.
- **Migration safety.** Landed as G7.4 clause 5 (expand/contract
  discipline) - what makes auto-revert sound for stateful services -
  not a separate condition.
- **Runtime config / feature-flag drift.** Covered: runtime
  configuration is environment-definition substance (class E);
  out-of-band mutation is a G6.3-certification drift breach; PL-PIPE
  governs changes; G7.3 scans them.
- **SBOM/provenance.** Adopted as G7.5 (the interlock-2 substrate).
- **Pillar sweep verdict:** the three registry families (perf,
  compat, infra) plus integrity are each held by a condition binding
  a baseline no earlier venue could bind; everything judgment-shaped
  was already spent at G6.

Roster verdict: complete at five - one adopted at close-out (G7.5);
zero human conditions, and the vocabulary's "concentrated at G1 and
G6" holds.

## Operators & harness

QA executes the release pipeline end to end; there is no human
condition to operate. The pipeline definition, rollout policy,
suppression configs, and record-writing jobs are all class E -
PL-PIPE.1 governs their change, PL-PIPE.2 golden-tests the admission
interlocks. The Verifier appears only in its cross-cutting role;
artifact identity is structural (attestation verification), not a
judgment. On a red: G7.1/G7.2/G7.3 reds route as fix or
spec-revision tasks through the normal front door; a G7.4 revert
leaves production on the incumbent and the re-attempt path is a
fresh admission. The fix lane (admission interlock 4's exception)
keeps G8 reds from deadlocking their own remedy.

## Decisions & open items

- All five conditions `specified` 2026-07-25 (session-10 walk; G7.5
  adopted at close-out).
- Frame rulings applied: four-interlock admission (record, artifact
  identity + no-rebuild, can-i-deploy, no standing G8 red with fix
  lane); release/deploy/rollout vocabulary; deploy-path identity
  with G6.3 (rehearsal formalized from G7's side); fully mechanical
  gate, QA-executed, timing = business policy.
- G7.1 ruled: budgets-only (relative clause rejected -> G9 ratchet);
  designation-record scoping (budget-designated column); spec-side
  benchmarks; noise-floor + vacuity guards; measurement records.
  Numbers = Q4.
- G7.2 ruled: last-ship baseline; declared-break discipline; version
  coherence; completion-time baseline capture.
- G7.3 ruled: subject = the certified environment definition; two
  venues one shape; ratchet-at-zero; infra-format-keyed binding.
- G7.4 ruled: dual-clause verdict; sample floor; auto-revert with no
  manual-continue; assertion-fire wire; migration revert-safety;
  completion semantics. Canary constants = Q4.
- G7.5 adopted: SBOM + provenance as interlock-2 substrate.
- S11 banked from here: G9 tightening consumes measurement records;
  G9.2 consumes the SBOM for field mapping; G10 notification
  consumes the contract-diff payload; G10.3 takes the
  contract-migration far end.
