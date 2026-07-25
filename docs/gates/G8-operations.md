# G8 - Operations

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Operations gate contain,
> and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 8;
> the G7 admission interlocks ([G7 page](G7-release-deploy.md)); the G6
> conversion machinery ([G6 page](G6-uat-staging.md)); the G5.6 shared
> instrumentation ([G5 page](G5-integration-system.md)); ADR
> [0007](../../decisions/0007-hard-core-designation-criteria.md).
> Two-layer per [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** the production runtime - the only gate whose venue never
  convenes on a schedule. G8's conditions are **standing invariants**
  (frame ruling): the gate convenes *on breach*, event-driven. Every
  prior gate answers "may this proceed?"; G8 answers "does what
  proceeded still hold?"
- **Cadence:** continuous.
- **Inputs:** live traffic; telemetry from the shared instrumentation
  surface (the G5.6 action-emission layer plus SLI streams); incident
  and crash-report channels; external defect reports.
- **FAIL blocks:** further rollout - **red seizes rollouts, never
  operations** (frame ruling; the G5 red-seizes-promotion shape
  transposed): production keeps running, mitigation is an ops action,
  not a gate action. Mechanically, every standing G8 red funnels into
  G7's admission interlock 4, with the fix-lane exception (the red
  blocks features, never the fix). And **convergence closure**: a G8
  finding closes only through conversion (G8.3) or an explicit
  recorded disposition - never by fading.
- **V-model position:** past the deploy - the loop-closing gate. G6
  and G8.3 are the convergence loop's two intake ports: G6 catches
  conformant-but-wrong before ship; G8 catches what escaped
  everything, and converts it.
- **Trust boundary:** monitoring, alert, and monitor-derivation
  configs are **class E** (frame ruling) - gutting an alert is
  deleting a gate, so the telemetry stack is enforcement-layer by
  construction, PL-PIPE-governed. G8.1/G8.2 are mechanical; G8.3's
  grader is the **operations principal** - non-delegable on the G6
  precedent; agents cluster, draft, and scout as suggestions only.
  Conversions ride the established front door (Spec agent drafts,
  G1.3 reviews, G2.5 arms red).

## Why this gate exists

The generic taxonomy seeded the gate set; the actual defect
distribution tunes it. G8 turns every escaped defect into an upstream
gate: detection (G8.1/G8.2, the tripwires) feeds triage (G8.3, the
judgment), and triage mints criteria that G1 owns forever - closure by
conversion, not prevention. An escape that does not produce a new
criterion is itself a process failure, and the disposition schema
makes that mechanical (G8.3 clause 3).

Detection honesty, stated on the page (frame + stop-6 ruling): G8 is
a **tripwire, never a verifier**. Sampled production silence is
evidence, not proof - G8.1 buys mean-time-to-detection and never
substitutes for G5.6's offline admissibility over total capture. The
detection ladder stays honest about what each rung certifies.

Classes closed: escaped defects - by conversion (G8.3); the runtime
residue of every upstream class, detected at its production surface
(G8.1 impossible-states, G8.2 service-level breaches)
([taxonomy](../taxonomy.md)).

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Object default: the production runtime of the current
production version.

### G8.1 Runtime contract assertions

- **Shape (pass condition):** the standing invariant is **zero fires
  on the gated set**. Clauses:
  1. **The gated set is spec-derived only** - (a) *boundary point
     contracts*, compiled from G1's boundary schemas: universal,
     always-on, in-process, stateless; (b) *stream monitors* for
     0007 hard cores - safety properties over the action stream,
     out-of-process, on a sampled stream (sampling rate = class E
     config). Both mechanically compiled from class-S sources, both
     residing class E, derivation golden-tested (PL-PIPE.2) - the
     enforced thing provably matches the declared thing.
  2. **Fire-to-telemetry, never fire-to-crash** - assertions ship
     enabled; detection must not cost availability.
  3. **Fire semantics** - a gated-set fire is by construction an
     impossible state reached: finding auto-opens, standing red,
     rollouts of the service seize (interlock 4). A fire inside a
     canary cohort is additionally an immediate G7.4 stage-FAIL ->
     revert. Every fire routes to G8.3; a wrong-assertion
     disposition routes the fix through the assertion's *own*
     channel (spec/model side) - there is no production mute button.
  4. **Developer assertions are bonus tripwires** - they ride the
     same telemetry but are never gate substance: the Developer can
     *add* detection inside the G3 write surface and cannot weaken
     the gated set, which was never theirs. 0010 stays clean with no
     new audit vector.
  5. **Liveness - absence of evidence is not silence** - monitors
     emit heartbeats; instrumented services under traffic carry a
     minimum-event-rate floor. A dead listener or a silent emitter
     reads red, not green (zero-traces-FAIL transposed to a venue
     that never convenes).
- **Reference binding (.NET):** the OpenTelemetry-family emission
  layer G5.6 already requires - **one instrumentation surface, two
  consumers** (banked S9, formalized here): G5.6 offline proves the
  instrumentation sound per snapshot (its action-coverage clause
  remains the gutted-instrumentation detector); G8.1 online inherits
  it *verified*. Emission overhead needs no separate budget - it is
  inside the system G7.1 benchmarks and G5.7 soaks.
- **Gap status:** none at shape level; stream-monitor wiring joins
  the trace-validation build item on first hard-core activation
  (0008 rule 2 - the G5.6 conditional, shared).
- **Why:** the production surface of the impossible-state class. The
  spec says these states cannot occur; a fire is therefore always a
  defect somewhere (code, spec, model, or mapping) - the highest
  signal-to-noise detection channel the pipeline owns.
- **Kind & loopability:** mechanical; diagnostic = assertion id +
  trace context + service version; the loop consumer is G8.3's
  triage, then the front door.
- **Parameters:** sampling rate, heartbeat cadence, event-rate
  floors = class E monitoring config (reference defaults).
- **Lifecycle:** `specified` (ratified 2026-07-25).

### G8.2 SLO / error-budget license

The inter-rollout gate (frame ruling): G7.4 gates *this* rollout's
progression; G8.2 gates the pipeline's license to start the *next*
one. One SLO declaration feeds both (the SLO pair, ruled stop 5).

- **Shape (pass condition):** the standing invariant is **error
  budget not exhausted**, per service. Clauses:
  1. **One declaration, mechanical derivation** - SLIs, objectives,
     windows, and error-budget policy live in
     `specs/<service>/slo.yaml` (class S, authored at G2;
     tightenings auto-approve, loosenings take spec sign-off, 0010
     unchanged). Monitoring queries, alert rules, and G7.4's canary
     analysis all *compile* from it; the compile is golden-tested
     (PL-PIPE.2). Alert-config drift cannot silently unhook the gate
     from the spec.
  2. **Budget accounting** - budget = 1 - objective over the
     declared rolling window; consumption tracked continuously from
     the same compiled rules.
  3. **License semantics** - exhaustion opens a standing red whose
     blocking effect is G7 admission interlock 4: no new rollout for
     the service. Fix lane: a release whose task contract references
     the open finding may admit - the budget blocks features, never
     the fix.
  4. **Alerts are the notification surface, not the gate** -
     burn-rate alerts (fast/slow) page the ops principal; the *gate*
     is the license state. An alarm that does not block is ignored
     by construction - here the block is structural.
- **Reference binding:** SLI pipelines + burn-rate rules compiled to
  the monitoring stack (Prometheus-family / Azure Monitor);
  reference burn thresholds as config defaults.
- **Gap status:** none - SLO machinery is ecosystem-universal.
- **Why:** the error budget is the production risk ledger: it prices
  every escape and every self-inflicted risk (chaos practice below)
  in one currency and spends rollout capacity accordingly. SLO
  *targets* are per-service spec values - never Q4.
- **Kind & loopability:** mechanical; diagnostic = budget state +
  breaching SLI series; loop consumers are the fix lane and G8.3
  (breach incidents enter triage).
- **Parameters:** kit-level none beyond G7.4's shared canary
  constants (Q4); windows and targets ride the declaration.
- **Lifecycle:** `specified` (ratified 2026-07-25).

### G8.3 Escape triage + conversion

Renamed from "crash triage" (0008 rename precedent): crashes are one
detection channel among four; the substance is the convergence loop.

- **Procedure (pass condition):** the standing invariant is **no
  escape candidate past its disposition window, and no escape without
  its conversion**. Clauses:
  1. **Intake totality** - the escape-candidate stream: crashes,
     G8.1 fires, G8.2 incident events, externally-reported defects.
     Every candidate auto-opens a triage item; every crash-group
     links to an item (mechanically checked); intake channels
     inherit G8.1's liveness clause - a dead crash-reporting
     pipeline reads red, not quiet.
  2. **Aging bound** - disposition within the declared window or the
     item becomes a standing red (interlock 4; fix lane applies).
     Window number = the G9.2 SLA-window family (S11/Q4).
  3. **Disposition taxonomy + the teeth** - five dispositions:
     *escape* (traversed the gate set), *spec-indicting mismatch*
     (behaves as specified, spec wrong or silent - G6's "findings
     indict the spec layer" carried to production), *true
     not-a-defect* (transient environment, correct degradation),
     *duplicate*, *wrong-tripwire* (the assertion is the bug).
     **Conversion is the default; declining requires written
     rationale.** An escape disposition is schema-incomplete without
     its minted criterion ref, regression-test ref, and **ladder
     assignment** (which gate should have caught it) - the
     mechanization of "an escape without a new criterion is a
     process failure," and the input that tunes the gate set to the
     actual defect distribution.
  4. **Front door** - minted criteria ride the normal spec channel:
     Spec agent drafts (REQ-ID per 0011), G1.3 reviews, G2.5 arms
     red, the fix closes, G4.3 witnesses forever.
  5. **Attestation** - the ops principal attests the queue on a
     declared cadence *even at zero activity*: a quiet month is
     either genuinely quiet or a dead intake, and attestation plus
     clause 1's liveness distinguishes them (G6.2's session
     attestation, continuous-venue form).
- **The record:** per item - source events, disposition, rationale,
  criterion refs, ladder note. Class S, committed; the G6.2
  conversion-record shape at a different venue (banked S9, applied
  here).
- **Reference binding:** crash-reporting + incident tooling feeding
  one triage queue; record schema rides the 0011 script family.
- **Gap status:** none - queues and records are ecosystem-free.
- **Why:** the convergence loop's production intake port. G6.3
  shrank the pre-ship residue; G8.3 shrinks the post-ship residue
  the same way - each escape becomes a criterion the mechanical
  layer holds forever. The ladder assignment is the gate set's own
  feedback instrument.
- **Kind:** human - judgment checkpoint (disposition is grading);
  loopability not claimed. The scaffold is mechanical: auto-opened
  items, schema-checked records, aging bounds, attestation - the
  G1.3/G6 pattern. G8.3 stays a *narrow* venue - minutes per item;
  the pipeline's attention concentrations remain exactly G1.3 and
  G6.
- **Parameters:** disposition window = G9.2 family (S11/Q4);
  attestation cadence = policy config.
- **Lifecycle:** `specified` (ratified 2026-07-25).

## Production chaos (governed practice)

The S9 rejection of chaos-as-condition stands; the banked venue
question closes as **governed practice, not condition** (close-out
ruling): experiments run only from a **committed chaos plan** (class
E - it manipulates production through the enforcement layer); the
**error budget is the license** - no self-inflicted risk under an
exhausted budget, the budget gates features and chaos alike; and
chaos-surfaced weaknesses enter G8.3's intake as ordinary escape
candidates, converting like any escape. S9's routing is thereby fully
discharged: expected-failure *criteria* at G1.3 item 8, failure
*actions* in hard-core models, failure *practice* governed here.

## Completeness check

Gate purpose: turn every escaped defect into an upstream gate; the
check asks what escapes three conditions. Examined:

- **Chaos-as-condition.** Re-affirmed rejected; governed practice
  above.
- **General observability (logs, dashboards, tracing breadth).**
  Practice, not gate: the kit gates invariants, not instrumentation
  inventory. The gated telemetry is exactly the spec-derived set
  (G8.1) plus the SLI streams (G8.2).
- **Incident response / on-call.** Ops practice outside gate scope;
  the gate consumes its outputs through G8.3's intake.
- **Alert-completeness drift.** Owned structurally: alerts compile
  from the SLO declaration and the compile is golden-tested -
  completeness is a property of the derivation, not a condition.
- **Pillar sweep verdict:** detection (mechanical, two conditions) +
  conversion (human, one condition) covers the gate's purpose;
  everything else production-shaped is either practice or another
  gate's far end (absolute budgets G7.1, trend shapes G5.7).

Roster verdict: complete at three - zero adopted, two renamed (G8.2
license semantics, G8.3 escape triage + conversion); the
human-condition census across the pipeline: G1.3, G2.3, G6.1, G6.2,
G8.3, PL-PIPE.1 - concentrations unchanged.

## Operators & harness

The monitoring stack runs itself; QA owns its class-E configuration
through the enforcement channel. The **operations principal** grades
G8.3 - non-delegable; agents cluster crash groups, draft dispositions
and criterion text, and surface anomalies as suggestions entering the
principal's triage, never verdicts (the G6 division, transposed).
Findings route spec-channel by construction; the Developer appears at
G8 only as the downstream consumer of fix tasks. The fix lane
(interlock 4's exception) keeps every standing red remediable without
loosening it.

## Decisions & open items

- All three conditions `specified` 2026-07-25 (session-10 walk; G8.3
  renamed at stop 7).
- Frame rulings applied: standing-invariant venue, event-driven
  convening; red seizes rollouts never operations; convergence
  closure; interlock-4 consolidation (one admission check covers
  G8.1 fires, G8.2 exhaustion, G8.3 aging); telemetry config = class
  E; ops principal grades, agents scout.
- G8.1 ruled: spec-derived gated set (boundary contracts + hard-core
  stream monitors); fire-to-telemetry; fire = auto-finding + rollout
  seizure + canary wire; Developer assertions = bonus; epistemic
  honesty (tripwire, never verifier); liveness clause.
- G8.2 ruled: one declaration two consumers; mechanical golden-tested
  derivation; license semantics via interlock 4; fix lane; alerts
  notify, the license blocks.
- G8.3 ruled: intake totality; aging bound (window -> G9.2 family);
  five dispositions, conversion-by-default with written-rationale
  decline; schema-incomplete-without-conversion teeth; ladder
  assignment as gate-set feedback; front door; class-S record (G6.2
  shape); queue attestation; narrow human venue.
- Chaos ruled: governed practice - committed plan (class E), error
  budget as license, findings convert via G8.3.
- S11 banked from here: triage window joins G9.2's SLA family; the
  tightening job's inputs now include ladder-assignment statistics
  (gate-set tuning evidence); the 0005 fix-lane field serves G5 and
  G8 reds alike (stop-the-line mechanics, S11).
