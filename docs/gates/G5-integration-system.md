# G5 - Integration / System

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Integration / System gate
> contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 5,
> principles 1, 4, 5 (section 2); the G4 choke point
> ([G4 page](G4-pre-merge-ci.md)); ADRs
> [0007](../../decisions/0007-hard-core-designation-criteria.md),
> [0010](../../decisions/0010-write-surface-immutability.md),
> [0011](../../decisions/0011-criterion-traceability-format.md). Two-layer
> per [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** the deep-verification tier - a pipeline run over a **pinned
  snapshot** of merged main. One sha per run, pinned at trigger; every
  condition evaluates that snapshot and its build artifacts (frame
  ruling). Promotion promotes the *verified artifact* - never a rebuild:
  rebuilding un-verifies, the same logic that forced merged-result
  semantics at G4.
- **Cadence:** budget-class **hours**; the schedule is *policy, not
  shape* (frame ruling). "Nightly" is the reference binding's default
  number - same status as an iteration budget - and rolling runs (pin
  newest sha, run, promote on green, re-pin) or on-demand deep runs
  satisfy the identical shape. Normative content: cost sets cadence,
  never rigor - a check too slow for G4's minutes lands here rather
  than being weakened.
- **Inputs:** the pinned snapshot (merged main build). Whole-state is
  the default object; a delta-scoped condition declares its reference
  point explicitly (G5.5: since the last G5.5-green snapshot).
- **FAIL blocks:** promotion to release candidate. **Red-run
  semantics** (frame ruling): a red seizes promotion immediately and
  merges never - G4 stays merge-authoritative, since a deep finding is
  often not the last merge's fault. Backstop for a standing red: past
  its remediation window (numeric = Q4/G9 family, S11) the red
  escalates to **stop-the-line at task intake** - no new task admitted
  unless its contract references the open red (the fix lane, decidable
  at G0's venue). Examined and rejected: merge-queue freeze (blocks the
  fix path, wastes verified work) and promotion starvation as mere
  observable (an alarm that does not block is ignored by construction -
  the kit's own thesis).
- **Determinism posture** (frame ruling): the deliberate complement of
  G4.4's derived seed - each run *extends* the explored space: fresh
  seeds, corpus growth, new interleavings. Two teeth: every red ships a
  complete replay recipe (seed / input / schedule), so a finding that
  replays on the pinned sha is real even if a rerun does not rediscover
  it; and **no retry-to-green** - a red clears only by a fix or the
  committed quarantine path (class E, G4.10-watched). Retry-until-green
  is suppression with extra steps.
- **V-model position:** between the choke point and the human boundary -
  the venue for everything hours-decidable that needs the whole built
  system, and for proving the enforcement instruments themselves have
  teeth. The G4/G5 split is economic, not metaphysical: principle 4's
  "earliest decidable point" means earliest *affordable* point, and
  conditions migrate up the ladder if merge-time compute allows (the
  G4 page's G4.7 split note is the same elasticity, opposite
  direction).
- **Trust boundary:** subject integrity is *inherited* (frame ruling) -
  everything in the snapshot crossed G4's diff policing and G5 adds no
  write surface. The run writes nothing in place; discovered state
  (corpus growth, minimized crashers) lands as **tightening candidates
  through the merge queue**, auto-approving under 0010's
  direction-conditional lane. No Verifier presence, no human: pure QA
  execution.

## Why this gate exists

Two purposes fused. First: the interaction, schedule, and robustness
defects only whole-system execution reveals - the classes below G4's
minutes budget. Second, the sharper one: **prove the spec suite has
teeth.** An enumerable example suite is gameable in principle, and an
LLM implementer is specifically good at optimizing "make the tests
pass" - so G5 holds the distribution oracles that make "pass" mean
"correct over a distribution" (G5.2/G5.3, input side) and the
sensitivity floor that stops "green" meaning "nothing was checked"
(G5.5, test side). G2.5 proved each test *can* fail at birth; G5.5
proves the living suite still pins the implementation.

**The oracle-designation rubric** (ruled this walk; the G1.3 checklist
enforces it): every component answers the oracle question **at G1**, in
one declaration record - differential-gated, fuzz-gated, property-only,
concurrency-gated, soak-designated, or none - and *none requires
written justification*, reviewed at G1.3. Silence is not an option:
absence of an oracle is an authored, human-reviewed decision.
Must-differential: algorithmic cores with a definable naive reference
an order simpler than the optimized form. Must-fuzz, no opt-out:
trust-boundary parsers (the CWE-20 surface) and every native-interop
wrapper. Concurrency-gated: shared-state concurrency,
tripwire-detected (G5.4). Trace-gated: derived from 0007's hard-core
designation, never opted. Soak-designated: long-running /
service-shaped components (G5.7).

Principles bearing:

- **Earliest affordable venue (principle 4):** every condition here is
  undecidable at G4's budget on real hardware - hours of exploration,
  whole-system execution, statistical trends - and decidable well
  before the human boundary.
- **Spec-first properties (principle 5):** the naive reference, the
  model package, the consumer pacts, the concurrency harnesses are all
  G1/G2-authored instruments executed here against the object by an
  operator that is not their author - two-channel decorrelation doing
  work inside one repo, and, for pacts, across principals.
- **Detectability ladder (principle 1):** the deepest mechanical rungs -
  systematic schedule exploration, mutation analysis, trace
  conformance - the last venues before judgment takes over.

Classes closed: interaction bugs (G5.1 + the system-scope suites),
concurrency (CWE-362, 667 - G5.4, with G5.6 on modeled cores),
parsing/input validation (CWE-20 - G5.3), vacuous specs (G5.5, with
G5.2's oracle pressure), resource-trend defects (CWE-400 trend class -
G5.7, adopted this walk), native-interop memory safety (the taxonomy's
former `-` row - G5.3's mandatory-fuzz disposition)
([taxonomy](../taxonomy.md)).

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Objects default to the pinned snapshot; the component
designation record (reference binding `specs/components.yaml`, class S)
scopes G5.2-G5.4 and G5.7.

### G5.1 Consumer-driven contract verification

The cross-principal oracle: G4.5 froze the surface's *syntax* at merge
speed; G5.1 verifies its *behavior* at hours speed - against
expectations the consumer authored. Two-channel decorrelation between
components: the provider cannot have overfit its tests to its own
misreading of what consumers need.

- **Shape (pass condition):** object = the pinned snapshot's real
  build. Two clauses and a report lane:
  1. **Totality (both directions, the G4.3 pattern)** - the declared
     consumer registry (class S, authored spec-channel alongside the
     G1 boundary schemas) joins the accepted pact set: every declared
     consumer has a current accepted pact, every pact maps to a
     declared consumer. Missing pact = FAIL; **unknown pact = FAIL**
     (allowlist polarity - an undeclared consumer must not silently
     gate the pipeline; the routing diagnostic names the fix: register
     the consumer or drop the pact). The registry must exist even when
     empty: authored-empty is a legitimate statement (leaf
     application; clause 2 trivially green); absent = FAIL.
  2. **Verification** - the provider, as the real built artifact from
     the pinned sha (never a stub), verifies every accepted pact
     green. Provider-state handlers seed state through legitimate
     interfaces only and are spec-suite material outside the Developer
     write surface - a Developer-editable state handler is the lever
     that hollows the gate from inside.
  3. **Acceptance lane (report)** - the blocking check runs against
     **accepted pact versions**, a class S artifact moved only by our
     spec channel: accepting a new contract version is spec work that
     mints criteria and tasks. Latest-published-but-unaccepted
     versions verify as advisory report feeding the spec channel
     (G4.5's report-to-approver semantics). Consumers drive the
     agenda, never the gate.
- **Reference binding (.NET):** PactNet verifier against the built
  service from pinned artifacts; pact source = broker pinned by
  accepted tag (tag moved only by the spec-channel job) or committed
  files under `specs/contracts/pacts/` for intra-repo consumers - a
  mono-repo's consumer test projects generate pacts in the same build,
  no broker required; registry at `specs/contracts/consumers.yaml`;
  verification project in the spec-authored test stratum.
- **Gap status:** none - Pact bindings exist across every plausible
  profile (pact-jvm, pact-js, pact-python, pact-go).
- **Why:** boundary behavior is the classic integration failure and
  surface lock cannot see semantics; the consumer's pact is the
  strongest mechanical "did we break someone" oracle because its
  author is decorrelated by construction. The verification matrix
  (which provider sha verified which pact versions) is a kept output -
  G7's walk decides its can-i-deploy use (banked, S10).
- **Kind & loopability:** mechanical; per-interaction diagnostic -
  consumer, interaction, expected/actual diff. Provider regression
  loops to the Developer; contract evolution routes spec-channel both
  sides (G10's deprecation machinery at sunset).
- **Parameters:** pact-source residence + acceptance mechanics =
  enforcement-pass config; nothing numeric.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G5.2 Differential + deep property campaign

Registry row renamed from "Differential testing" (G4.1 precedent): the
deep property campaign is a second clause the old name did not cover.

- **Shape (pass condition):** object = pinned snapshot. Three clauses:
  1. **Differential equivalence** - for every differential-gated
     component, the optimized implementation is equivalent to the
     naive reference over freshly generated inputs, under a **declared
     equivalence relation**: default exact equality; declared
     tolerance/normalization where the domain demands it (float
     epsilon, unordered collections); and **error agreement** - inputs
     one side rejects, the other rejects in the same class. The
     relation is spec material: a Developer-tunable tolerance is a
     gate-hollowing lever.
  2. **Deep property campaign** - the property/metamorphic suites
     G4.4 runs at minutes budget under a derived seed run here at
     hours budget under fresh seeds. Same machinery; this is where
     generative depth lives - G4.4 keeps merges deterministic, G5.2
     explores.
  3. **Mechanics** (frame ruling) - fresh seeds per run; every failure
     ships seed + failing input + shrunk form. With a reference in
     hand the diagnostic names the *expected* answer - the strongest
     loop diagnostic in the kit.
- **Provenance teeth:** the naive reference is authored at G1 by the
  Spec channel, before and independently of the implementation - a
  reference derived from the implementation is self-agreement, not an
  oracle. Class S, immutable to the Developer; generators likewise.
- **Reference binding (.NET):** reference implementations as plain C#
  in the spec stratum; CsCheck/FsCheck generators shared with G4.4;
  equivalence harness at campaign budget; shrunk counterexample + seed
  to the gate.
- **Gap status:** none - references and generators are plain code in
  every ecosystem; generator libraries are universal.
- **Why:** the input-side anti-overfit closure. Enumerable examples
  are gameable by an implementer optimizing pass-the-tests;
  distribution oracles are not. Differential is the strongest oracle
  for algorithmic code (catalog pattern 6): the reference answers
  *what correct is* for inputs no one enumerated.
- **Kind & loopability:** mechanical; expected-vs-actual + shrunk
  input + seed - fully loopable.
- **Parameters:** campaign budgets, generator sizes = enforcement-pass
  config (G4.4 precedent); nothing joins Q4.
- **Lifecycle:** `specified` (ratified 2026-07-24; renamed this
  session).

### G5.3 Fuzzing

- **Shape (pass condition):** object = pinned snapshot. Every declared
  fuzz target runs corpus + freshly generated inputs within budget;
  any crash, hang past threshold, or sanitizer finding = FAIL, with
  the minimized crashing input as the replay recipe.
- **Corpus governance** (frame ruling cashed out): the corpus is
  accumulated enforcement state under a class E path. Run discoveries -
  new-coverage inputs, minimized crashers - land as tightening
  candidates through the merge queue (0010's direction-conditional
  lane: growth strengthens the gate, auto-approves); pruning takes the
  full second channel. The corpus is the regression memory: a fixed
  crash's input re-runs forever. No criterion minting - a G5 catch
  needs no new REQ-ID (the G4 close-out's logic: the gate already
  existed).
- **Native-interop disposition** (taxonomy `-` row, closed this
  session): G3.3 keeps `unsafe` off, but P/Invoke imports
  memory-unsafety the managed type system cannot see. Fuzzing *is* the
  compensating control G3.3 clause 4 demands: interop wrappers are
  mandatorily fuzz-gated - no opt-out justification accepted - with
  native-side sanitizer instrumentation (ASan) where native source is
  available, boundary-input fuzzing of the wrapper where it is not.
  The taxonomy row flips `-` -> G5.3.
- **Reference binding (.NET):** SharpFuzz (afl-fuzz/libFuzzer over
  instrumented IL); targets declared at `specs/fuzz/targets.yaml`;
  corpus per target under the class E path; minimization before corpus
  admission. Mixed-mode rung, honestly: SharpFuzz instruments IL, not
  native code - mixed-mode targets are a documented thinner rung; the
  build item waits until a profile with real native interop activates
  (0008 rule 2, no speculative builds).
- **Gap status:** fuzzers are ecosystem-universal (libFuzzer/AFL
  family, Jazzer, Atheris, cargo-fuzz); the mixed-mode note above is
  the only thin rung.
- **Why:** the robustness oracle over the same generated-input idea as
  G5.2 - "pass" means "does not crash on the distribution", which no
  enumerable suite approximates. Must-fuzz scope (trust-boundary
  parsers) is where CWE-20 lives; the interop mandate closes the kit's
  last uncovered memory-safety surface.
- **Kind & loopability:** mechanical; the minimized crashing input is
  the complete recipe - maximally loopable.
- **Parameters:** per-target budgets, hang thresholds =
  enforcement-pass config; nothing numeric joins Q4.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G5.4 Systematic concurrency testing

The heisenbug venue: the taxonomy parks CWE-362/667 here because
schedule-dependent bugs are invisible per-candidate - an interleaving
campaign does not fit minutes, and naive stress is flaky-by-nature,
exactly what G4.4's determinism rule exiled from the queue. Systematic
exploration seizes the scheduler and emits the failing schedule as a
deterministic replay: a heisenbug converted into a loopable
diagnostic - which also drains the quarantine-abuse vector, since a
bug that replays deterministically has no claim on G4.11's class E
quarantine list.

- **Shape (pass condition):** object = pinned snapshot. Three clauses:
  1. For every concurrency-gated component, scheduled-interleaving
     exploration within budget finds zero failures: no deadlock,
     assertion violation, unhandled exception, or livelock past
     threshold.
  2. **Totality** - declared set >= detected set: a static tripwire
     scan for shared-state constructs (locks, `Interlocked`,
     semaphores, `volatile`, concurrent collections, channels,
     `Task.Run`/`Parallel`, mutable statics touched from async
     contexts - deliberately *not* plain request-flow `async/await`,
     which would designate the world) cross-checked against the
     declaration record. Detected-but-undeclared = finding; over-fire
     resolves through the none-with-justification valve,
     G1.3-reviewed. Every declared component has a harness -
     missing = FAIL.
  3. **Mechanics** (frame ruling) - fresh scheduling seeds per run;
     every failure ships the schedule trace, replayable exactly.
- **Harness provenance:** concurrency harnesses - entry points that
  create contention and assert invariants - are spec-suite material,
  class S: a harness that never contends passes vacuously, and an
  agent that can edit the exam will. Stated residue: "does the harness
  genuinely exercise the declared contention" is not fully
  mechanizable; the G1.3 review of the designation record carries that
  judgment.
- **Reference binding (.NET):** Microsoft.Coyote - IL rewriting for
  controlled scheduling; `coyote test` under committed strategy +
  budget config (PCT); `coyote replay` on the emitted trace; harnesses
  in the spec-authored test stratum. The tripwire detector is 0009
  custom-analyzer material, first-tranche candidate at pilot
  activation; until then the totality clause binds through
  declaration + review (documented rung).
- **Gap status:** profile-relative (0008 rule 4): Rust (loom, shuttle)
  and JVM (Lincheck) bind strong rungs; Go and C/C++ profiles hold a
  thinner rung - dynamic race detection (TSan, `-race`) under stress,
  documented as compensation. No build item until such a profile
  activates.
- **Why:** agents write plausible-*looking* concurrent code - imitated
  lock patterns without the invariant reasoning behind them - and
  G2.1's models cover only what earned one. G5.4 is the
  implementation-level backstop for everything else, at the only venue
  that can afford it. Hard cores with concurrency join automatically;
  G5.4 needs no model - that is G5.6's job.
- **Kind & loopability:** mechanical; the schedule trace is a
  deterministic replay - loopable.
- **Parameters:** iteration budgets, strategy (PCT depth), livelock
  thresholds = enforcement-pass config; nothing joins Q4.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G5.5 Mutation threshold

The gate that audits the auditors: every other gate trusts the suites;
this one measures them. A mutant the suite does not kill is behavior
the suite does not constrain. Scope stated honestly: mutation measures
*sensitivity*, not correctness - correctness pressure stays with the
spec-channel oracles; this is the floor under vacuity, necessary not
sufficient.

- **Shape (pass condition):** object = code changed between the pinned
  sha and the **last G5.5-green snapshot** (the declared delta
  reference). Four clauses:
  1. **Floor** - mutation score >= floor over the run's changed-code
     mutant population; below a small-population cutoff of N mutants
     the rule shifts to **zero survivors** - stricter at small N,
     deliberately: ratios on five mutants are statistical noise, and
     each survivor in a tiny delta is individually reviewable. Floor
     value and N = Q4 numerics; the *procedure* is fixed here.
  2. **Killing population = the whole suite** - any partition may kill
     (unit, acceptance, property, arch). The condition gates whether
     *some enforced check* pins the behavior, not which layer does.
  3. **Dismissals** - equivalent-mutant markers follow the G4.7 FP
     pattern: committed class E suppression config, second-channel
     approved, G4.10-watched. **In-source ignore comments are
     banned** - vector-1 suppression inside the writable surface; the
     binding adds them to G4.10's construct list (G4 page cascade).
  4. **Overrides & tightening** - direction-conditional (0010's lane):
     per-component floors stricter than global are freely authorable
     spec-side; looser takes the full second channel. The floor
     belongs to the ratchet family - it moves only at G9 tightening
     events (tighten auto-approves, loosen takes the channel; cadence
     = Q4, S11).
- **Precondition (G4.11, named):** mutation over a red suite is
  meaningless - and the queue makes redness impossible by
  construction: main at any instant *is* some candidate's evaluated
  merged result, so G4.11's suite-green transfers to every snapshot by
  induction. A non-green suite discovered here is definitionally a
  pipeline defect (environment divergence, routed PL-PIPE) - the G4.1
  echo-divergence logic one tier up.
- **Bootstrap:** retrofit adoptions grandfather standing code (the
  G4.7 frozen-legacy precedent - bootstrap material, not the shape);
  greenfield needs nothing: induction covers the tree, every line was
  once changed code.
- **Reference binding (.NET):** Stryker.NET in diff mode against the
  last-green ref; committed config = class E (thresholds, mutator set,
  dismissals); survivor list + score to the gate; coverage-selected
  test execution per mutant as binding detail.
- **Gap status:** none that gates - PIT (JVM), StrykerJS, mutmut /
  cosmic-ray (Python), cargo-mutants (Rust) bind; weaker ecosystems
  document rung differences on activation.
- **Why:** the vacuous-spec closure. In an agent pipeline the suite is
  the contract's enforcement arm and the Developer benefits from its
  weakness - so sensitivity must be measured, not assumed. Stated
  caveat: a Developer can kill mutants with behavior-pinning tests
  (asserting what the code *does*, not what it *should*) - legitimate
  regression value; correctness stays decorrelated in the spec
  channel; the floor never pretends otherwise.
- **Kind & loopability:** mechanical; per-survivor diagnostic -
  location, mutation operator, mutated form, the covering tests that
  stayed green. Default loop: the Developer authors a killing unit
  test (inside the write surface); escalation by name when the kill
  needs spec authority - the survivor reveals an unspecified
  behavioral dimension.
- **Parameters:** floor value, small-N cutoff, mutator set = Q4 /
  enforcement-pass; procedure closed this session.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G5.6 Model trace-conformance

The hard-core chain's last link: G1.2 proved the *model* checks clean,
G2.1 proved the *design* was modeled before code existed - every
guarantee so far is about a document. G5.6 connects model to code:
captured execution traces, mapped to model vocabulary, checked as
behaviors the model admits.

- **Shape (pass condition):** object = pinned snapshot; scope = 0007's
  hard-core set exactly, never opted (the designation record's trace
  column is *derived*). Four clauses:
  1. **Conformance relation** - a trace conforms when, after the
     refinement mapping translates concrete events to model actions,
     the sequence is an admissible behavior of the checked model:
     implementation-traces within model-behaviors, deliberately
     safety-side. The liveness residue (a do-nothing implementation
     conforms) is named, not hidden: liveness was checked *in* the
     model at G1.2; implementation-side liveness lives with G5.4's
     deadlock/livelock exploration and G8's runtime venue.
  2. **Anti-vacuity** - zero captured traces = FAIL (G2.5/G4.11
     precedent); **action coverage** - every model action witnessed in
     the run's trace corpus except actions the model package annotates
     `rare` (spec-channel annotation, the justified-none valve,
     reviewed). Coverage doubles as the gutted-instrumentation
     detector: removing an emission point makes its actions vanish and
     coverage goes red - the exam cannot be hollowed by silencing it.
  3. **Mapping totality** - the mapping is total over captured events:
     an event with no rule = FAIL naming the event. Silent-drop is the
     hollowing vector; emission/mapping drift surfaces as a
     diagnostic, never as quiet forgiveness.
  4. **Fail-if-missing** - a designated core with no model package or
     no conformance wiring = FAIL: "model exists, conformance never
     wired" is the likeliest silent decay path.
- **Capture:** two sources - a dedicated spec-authored scenario
  harness (drives the model's scenario vocabulary; makes action
  coverage reachable) and piggyback capture from G5.4's Coyote runs
  (systematically explored interleavings are exactly the traces worth
  checking; the two conditions share a run). Emission goes through a
  small structured-event shim. Production-side capture is G8.1's
  adjacency - banked to S10.
- **Model package = class S:** model, checker config, refinement
  mapping, scenario set, rare-annotations - authored with the model at
  G1.2/G2.1 time, under `specs/models/<core>/`. A Developer-editable
  mapping is conformance theater: map everything to stutter.
- **Reference binding (.NET):** structured JSON event logs; TLA+ cores
  checked via TLC trace-validation (a trace-spec replaying the log
  against the model - the MongoDB/CCF pattern); P cores use P's
  compiled runtime monitors observing events directly. Harness wiring
  = **build item on first hard-core activation** - not registered now
  (0008 rule 2: active-profile need, never speculative; the pilot may
  designate zero cores).
- **Gap status:** the kit's thinnest-tooling condition by nature -
  trace validation is a pattern you wire, not a product you install,
  in every ecosystem; bounded deliberately by 0007 keeping the
  hard-core set small.
- **Why:** an LLM implementing a modeled protocol reproduces its
  *shape* without its invariant discipline - plausible-but-divergent -
  and no example suite catches a rare-interleaving protocol violation.
  G5.4 + G5.6 is the mechanical bridge from proved design to running
  code; the model is the second channel on the implementation's
  behavior.
- **Kind & loopability:** mechanical; step-level diagnostic - "at step
  k the implementation did X; the model admits {Y, Z}". Default route:
  Developer (the model was checked and human-reviewed; the generated
  implementation is the suspect); named escalation to spec-channel
  model revision when the implementation is right and the model
  incomplete - the checker cannot tell which artifact is wrong, so the
  diagnostic names both paths.
- **Parameters:** scenario budgets = enforcement-pass config; nothing
  numeric - the forced decision was the relation itself, closed above.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G5.7 Soak / resource-trend

Adopted at this walk's close-out (roster addition). The performance
question split: throughput/latency *budgets* need quiet
production-like infra and stay at G7.1/G7.4 - the G4 close-out's noise
argument, one tier up. **Trend-class defects** - memory growth, handle
leaks, event-handler accumulation, unbounded caches - are noise-robust
(a monotone growth curve reads through noisy runners), hours-shaped,
and otherwise surface first in a canary with production blast radius.

- **Shape (pass condition):** object = pinned snapshot. Every
  soak-designated component (declaration record; service-shaped /
  long-running - leaf libraries opt out naturally) runs its
  spec-authored sustained scenario for the soak window; pass = no
  unbounded-growth trend in the declared resource curves (memory,
  handles, threads, plus per-component declared extras) and zero
  crashes over the window. **Trend shapes gate; absolute values do
  not** - budgets live at G7 where infra is quiet.
- **Reference binding (.NET):** dotnet-counters / EventCounters
  sampling under the scenario harness; trend assertion over the
  sampled series (monotone-growth detection with declared envelope
  parameters); scenario in the spec-authored stratum.
- **Gap status:** none - counter sampling and trend assertion are
  ecosystem-universal.
- **Why:** agents write exactly this class - plausible-looking
  undisposed resources, accumulating handlers, caches without
  eviction - and the battery catches only the static easy cases
  (CA2000 family). Hours of sustained execution is the earliest venue
  where the trend exists to observe. CWE-400 gains an earlier rung
  (taxonomy cascade).
- **Kind & loopability:** mechanical; diagnostic = the resource curve
  + the scenario + the growth interval - loopable (the scenario
  replays; the curve localizes the leak window).
- **Parameters:** soak window, sampling rate, per-component envelope
  parameters = enforcement-pass config; nothing joins Q4.
- **Lifecycle:** `specified` (adopted + ratified 2026-07-24).

## Completeness check

Gate purpose: everything hours-decidable on the whole built system
blocks before promotion; the check asks what escapes seven conditions.
Examined:

- **Performance.** Split ruled: trend-class defects adopted as G5.7
  (noise-robust, hours-shaped, earliest venue); throughput/latency
  budgets stay G7.1/G7.4 where infra is quiet and traffic real.
- **Fault injection / chaos.** Rejected as a G5 condition; coverage
  routed through existing machinery: G1.3 item 8 extended one notch -
  system-level failure criteria per *external dependency* ("on
  dependency X unavailable, system does Y"; G1 page cascade) - so
  failure scenarios run as ordinary acceptance material in G5's system
  venue; hard-core models include failure actions (0007 guidance
  note), so G5.6 traces cover modeled failure behavior; production
  chaos is G8's venue question (banked, S10).
- **Adversarial pen-testing.** Not mandated: the mechanical security
  stack is G2.4 -> G4.7 -> G5.3; human adversarial probing is
  available as G6.2-flavored practice at the principal's discretion.
- **Pillar sweep verdict:** with the adoption, everything
  hours-decidable between merge and the human boundary has a home -
  interaction (G5.1 + suites), generated-input correctness (G5.2),
  robustness (G5.3), schedules (G5.4), spec adequacy (G5.5), model
  conformance (G5.6), resource trends (G5.7). The judgment residue is
  G6's by design.

Roster verdict: complete at seven - one adopted at close-out (G5.7),
one renamed (G5.2); zero further additions.

## Operators & harness

The QA agent executes everything: the run is pure execution - subject
integrity inherited from G4's choke point (nothing reaches the
snapshot that did not cross the diff policing), so no Verifier
presence and no human appears at G5. The run writes nothing in place:
discovered state - corpus growth, minimized crashers - lands as
tightening candidates through the merge queue under 0010's
direction-conditional lane. On red: promotion seizes, the replay
recipe routes to the Developer's loop as a fix task, and bisection
over the merge window is a harness job - replay recipe + cheap agents
make attribution nearly free. A red past its remediation window
escalates to stop-the-line at intake (fix lane exempted by contract
reference; mechanics with G9's walk, S11). The pipeline definition
implementing the run is class E (PL-PIPE), as everywhere.

## Decisions & open items

- All seven conditions `specified` 2026-07-24 (session-9 walk: eight
  stops, every ruling ratified in-conversation before edits landed).
- Frame rulings: snapshot pinning + verified-artifact promotion; red
  seizes promotion never merges, stop-the-line escalation past window
  (fix lane via contract reference); fresh-exploration posture with
  replay recipes and no retry-to-green; subject integrity inherited +
  tightening-candidate emissions; cadence = budget-class, schedule =
  policy ("nightly" demoted to reference default).
- Oracle-designation rubric ruled (no new ADR): one declaration record
  per component at G1, G1.3-reviewed; must-differential, must-fuzz (no
  opt-out: trust-boundary parsers + native interop), concurrency
  tripwire, trace derived from 0007, soak column;
  none-with-justification valve. G1 page cascade carries the checklist
  item.
- G5.5's Q4 entry sharpened: floor *procedure* fixed (ratio +
  zero-survivor small-N rule; class E dismissals; in-source ignores
  banned -> G4.10 vector-1 list, G4 page cascade;
  direction-conditional overrides; ratchet-family tightening at G9);
  numbers open: floor value, small-N cutoff.
- G5.6's conformance criteria fixed: safety-side admissibility;
  anti-vacuity package (zero-traces FAIL, action coverage + rare
  valve, gutted-instrumentation detection); mapping totality; model
  package class S; Coyote piggyback capture; conditional build item on
  first hard-core activation.
- Native-interop disposition: mandatory fuzz + sanitizer
  instrumentation; taxonomy `-` row flips to G5.3 (cascade).
- Roster: G5.7 adopted (soak/resource-trend; performance split with
  G7); G5.2 renamed "Differential + deep property campaign". Counts 50
  -> 52 total; 23 -> 33 `specified` (with G6's three).
- 0010's direction-conditional lane reused: corpus growth
  auto-approves / pruning takes the channel; mutation-floor
  tightenings auto-approve / loosenings take the channel.
- S10 inputs banked: G5.1 verification matrix (can-i-deploy); the soak
  split's budget half (G7.1); G5.6 <-> G8.1 shared instrumentation;
  production chaos (G8). S11: stop-the-line mechanics incl. the
  contract fix-lane field (0005 touch); mutation-floor + ratchet
  cadence numbers (Q4).
