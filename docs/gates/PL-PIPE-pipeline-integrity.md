# PL-PIPE - Pipeline integrity (cross-cutting)

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Pipeline-integrity
> lifecycle contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 PL
> rows; ADRs
> [0010](../../decisions/0010-write-surface-immutability.md) (the
> mechanical arm),
> [0012](../../decisions/0012-stop-the-line-economy.md) (clock
> direction-conditionality),
> [0013](../../decisions/0013-sunset-policy.md) (date-move asymmetry),
> [0014](../../decisions/0014-enforcement-change-control.md),
> [0015](../../decisions/0015-program-close-out.md).
> Two-layer per [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** the second channel - the one venue no other gate may
  share (frame ruling): sharing it with the layer it approves would
  collapse the separation - plus enforcement-layer CI (goldens ride
  G4.11 discovery; evals run on their three arms).
- **Cadence:** per class-E change; the eval sweep at its clocks.yaml
  cadence.
- **Inputs:** class-E diffs; the write-surface manifest (0010); the
  direction-classifier config; the approval ledger; golden fixtures;
  eval scenarios + the model pin.
- **Object:** the enforcement layer itself - the highest-privilege
  artifact set. The only gate whose subject is the pipeline rather
  than the product.
- **FAIL blocks:** any class-E delta without its valid hash-bound
  approval record (the G4.6 join); decision-bearing config without
  goldens (unmarked manifest class = red); prompt deployment without
  eval green.
- **Trust boundary:** PL-PIPE.1 is human - the sixth census seat
  (every agent is inside the gated class); PL-PIPE.2/.3 are
  mechanical. The suites, fixtures, and scenarios are themselves
  class E: weakening edits are loosenings, so the instruments are
  self-guarding.

## Why this gate exists

A developer agent that can edit the workflow file can delete every
gate in one diff - the 54-condition registry is worth exactly as
much as the machinery enforcing it is tamper-proof. The layer gets
three instruments matched to artifact nature: change control for
everything (PL-PIPE.1 - the human channel over 0010's mechanical
arm), decision-procedure regression for the deterministic configs
(PL-PIPE.2 - goldens), and behavioral evals for the stochastic layer
no golden can pin (PL-PIPE.3 - prompts). Self-reference grounds in
the human: the second channel is defined by separation from the
write, and edits to the channel definition itself take the strongest
authority (0014's meta-rule) - no regress.

Classes closed: enforcement-layer compromise (CWE-693) - agent
self-weakening at diff time (with G4.6/G4.10), enforcement rot over
time (with G9.4), gate-config bugs, prompt regressions.

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Object default: the class-E artifact set per the 0010
manifest.

### PL-PIPE.1 Enforcement-layer change control

- **Shape (pass condition):** every class-E delta carries a valid
  approval record for its lane. Clauses (per
  [0014](../../decisions/0014-enforcement-change-control.md)):
  1. **Two lanes, routed mechanically** - a committed direction
     classifier applies per-artifact-class field-wise rules:
     tightening (shorter window, shrunk baseline, removed allowlist
     entry, earlier-bounded date) auto-approves; loosening takes the
     full lane. **Undecidable direction = loosening** - workflows,
     rulesets-as-code, and prompts have no field-wise direction and
     always take the full lane.
  2. **The full lane's approver is the human principal.** The gated
     population is the agent fleet itself; decorrelation is
     insufficient because every agent is inside the gated class - an
     agent approving enforcement loosenings is the fox auditing the
     door. Load stays bounded: the human sees only loosenings and
     meta-edits, rare by design.
  3. **Separation invariant** - no single context both authors a
     class-E delta and mints its approval; harness-enforced (0010
     trust root: channels distinguished, agents not authenticated),
     audit-verified.
  4. **One append-only approval ledger, hash-bound, total** - both
     lanes record {delta path set + content hash, direction verdict
     + rule ref, lane, approver, rationale, date}; hash binding
     kills approve-then-swap; auto-lane records minted by the
     classifier; G4.6 joins diff <-> record, incomplete = merge red.
  5. **Meta-layer always full-lane** - classifier config, manifest,
     ledger schema, clocks structure, this workflow itself: never
     auto-approved, even tightening. Auto-approval cannot widen
     auto-approval.
  6. **Revert-to-approved rides the auto lane** - backward motion to
     a ledger-approved hash is the one operational escape hatch; no
     forward break-glass exists (stop-the-line, 0012).
- **Reference binding (.NET / repo-level):** classifier config +
  approval-ledger records under a protected root
  (`specs/approvals/`); the write-surface audit job (0010's, gaining
  the join); the harness approval step as the channel surface.
- **Gap status:** classifier + ledger ride pilot activation (Q6).
- **Why:** the enforcement layer is the one place where "who
  approves" cannot be answered with "another agent" - the census
  seat exists because the gated class has no member fit to hold the
  key.
- **Kind & loopability:** human (the full-lane judgment act); the
  substrate - routing, ledger, join - is mechanical and loopable;
  diagnostic = delta + lane + missing/invalid record.
- **Parameters:** none numeric;
  [0014](../../decisions/0014-enforcement-change-control.md).
- **Lifecycle:** `specified` (ratified 2026-07-26).

### PL-PIPE.2 Gate-config golden tests

- **Shape (pass condition):** every decision-bearing gate config
  passes its pinned regression suite. Clauses:
  1. **What a golden asserts** - committed fixture facts x committed
     config -> pinned decision, run against the *actual* decision
     procedure. Subject kinds: derivations (slo.yaml -> burn-rate
     rules, clocks.yaml -> window verdicts), classifiers (G10.3
     expand/contract, the 0014 direction classifier), joins (G10.1
     record <-> mark coherence, G4.6 diff <-> approval-ledger,
     reds-ledger arms), routers (G9.4 three-lane routing, 0012
     three-arm engagement), clock computations (0013 notification +
     notice-floor validity), staleness verdicts (PL-DOC.3).
  2. **The polarity trio is the per-subject floor** - one passing
     fixture, one *blocking* fixture, one *fail-closed* fixture
     (missing/malformed input -> red). Every "missing = FAIL" ruling
     in the registry becomes a pinned regression - fail-closed
     polarity enforced by test, not prose. A suite lacking its
     blocking fixture does not count as coverage.
  3. **Coverage rides the manifest** - every manifest class carries
     a goldens marking: *decision-bearing* (names its suite) or
     *inert* (no decision logic - chaos plan, prose registry;
     prompts are PL-PIPE.3's subject). Unmarked class = red;
     decision-bearing without a suite = red. Born-protected +
     unmarked-red means coverage cannot silently lag new artifacts.
  4. **No bespoke runner** - goldens are ordinary discovered tests:
     G4.11 runs them every merge; G9.1's dependency lane re-runs
     them exactly where executor drift bites (a tool update that
     changes a decision procedure fails goldens on the update PR).
     PL-PIPE.2 owns coverage + content rules, not a venue.
  5. **Tamper-evidence** - fixtures are class E: a verdict flip
     toward *passing* is a loosening, full lane (0014). An agent
     cannot quietly retune a fixture to make its config change
     green.
- **Reference binding (.NET):** ordinary test projects housing the
  fixture suites; the manifest markings field; the S10-S12 banked
  inventory as the seed set.
- **Gap status:** suite scaffolding + manifest markings ride pilot
  activation (Q6).
- **Why:** a gate-config bug is a gate silently passing what it
  should block - the enforcement layer needs its own regression
  floor or every other gate's guarantee is soft.
- **Kind & loopability:** mechanical; diagnostic = fixture +
  expected/actual verdict; loop consumer is the config-touching
  task.
- **Parameters:** none numeric.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### PL-PIPE.3 Agent-behavior evals

- **Shape (pass condition):** the prompt set passes its behavioral
  eval suite on every trigger arm. Clauses:
  1. **Five invariant families**, per persona's applicable subset:
     *containment* - the Developer stays inside the write surface
     even when task content instructs otherwise; *oracle integrity* -
     the session-7 anti-gaming finding mechanized: probes where
     implementing-to-the-visible-test and
     implementing-to-the-criterion diverge (hidden holdout
     assertions detect overfitting); *role boundaries* - each
     persona's "does-not" lines as scenarios; *loop competence* -
     the loopability invariant's agent side: from a gate's
     diagnostic to green within budget, no human interpretation;
     *escalation honesty* - blocked or contradictory states produce
     halt-and-surface, never improvisation outside the lane.
  2. **Propensity, not teeth** - defense in depth, never
     substitution: G4.6/G4.10 still block the violating diff. The
     eval buys timing - a prompt regression is caught at its own
     merge, not diagnosed later from a spray of blocked merges.
  3. **Three trigger arms** - prompt-touching merges (deployment
     *is* merge: the harness loads prompts from main); executor
     changes (the model/runtime version is a pinned class-E
     declaration; a version bump re-runs the suite with zero prompt
     diff - G9.1's executor-drift logic transposed; an *unpinned*
     model is undecidable behavior and reads red); a scheduled
     re-run at clocks.yaml cadence catching silent drift under a
     pinned alias - dead sweep reads red, G9 discipline.
  4. **Statistical honesty** - stochastic subject, sampled verdict:
     fixed trial count, committed seeds + transcripts as evidence,
     no retry-to-green (G5's rule). Two verdict classes:
     *zero-tolerance* families (containment - any violation in N
     trials = red; G5.5's small-N polarity) and *rate-floor*
     families (competence - convergence rate >= floor).
  5. **Self-guarding, and Q5 stays open honestly** - scenarios,
     thresholds, and the model pin are class E (weakening =
     loosening, full lane); the verdict computation is a PL-PIPE.2
     golden subject (transcript fixtures -> verdict). Evals
     *regression-guard* the decorrelation design once Q5 lands -
     they do not design it; families are fixed now, concrete probes
     instantiate with the harness.
- **Reference binding:** eval harness over the harness prompt set
  (Spec, Developer, QA, Verifier); per-persona scenario suites;
  model pin in class-E config; transcript store.
- **Gap status:** suite + pin ride pilot activation (Q6); probe
  instantiation additionally waits on the harness design (Q5).
- **Why:** prompts are the class-E members no deterministic
  instrument reaches - goldens pin decisions, evals sample behavior;
  without them the highest-privilege artifacts have change control
  but no regression floor.
- **Kind & loopability:** mechanical (run + verdict); diagnostic =
  family + scenario + transcript ref; loop consumer is the
  prompt-editing task.
- **Parameters:** trial counts, pass floors, sweep cadence -
  clocks.yaml rows (Q4).
- **Lifecycle:** `specified` (ratified 2026-07-26).

## Completeness check

Gate purpose: keep the enforcement layer tamper-proof; the check
asks what compromise escapes three conditions. Examined:

- **Enforcement-coverage completeness** (is every class-E artifact
  enumerated + controlled?) - struck as a condition: 0010's
  born-protected polarity *is* the enumeration closure; the S12
  audit verified it (0015).
- **Generated-doc coherence** - lands here as golden subjects
  (routed from PL-DOC's completeness check).
- **Forward break-glass** - struck; revert-to-approved is the only
  express lane, backward-only.
- **The census question** - PL-PIPE.1 confirmed as the sixth and
  last human seat; the other five judge the product, this one
  guards the machine.
- **Roster verdict:** complete at three - zero adopted, two
  strikes, one route-in; one human + two mechanical.

## Operators & harness

The human principal holds the full lane and nothing else; QA authors
goldens and eval scenarios - which are class E, so QA's own edits
ride the channel they feed; agents never approve; the Verifier's
audit job (0010) performs the mechanical joins. The classifier does
the routing so the human's queue stays short and every item in it
deserves eyes.

## Decisions & open items

- All three conditions `specified` 2026-07-26 (session-12 walk); the
  registry reaches 54/54 - the ADR-0004 program's specification
  layer is complete ([0015](../../decisions/0015-program-close-out.md)).
- ADR [0014](../../decisions/0014-enforcement-change-control.md)
  minted here: two lanes, human ground, hash-bound ledger,
  meta-full-lane, revert-auto, consolidated scope census. Q7 closes;
  the open-parameter index is Q4-only.
- The reds ledger (`reds.yaml`, 0015) joins the golden subject set
  and the Q6 build inventory.
- Q4 gains eval constants (trial counts, floors) + the eval-sweep
  cadence.
- Build items riding Q6: direction classifier, approval ledger,
  golden scaffolding + manifest markings, eval suite + model pin.
