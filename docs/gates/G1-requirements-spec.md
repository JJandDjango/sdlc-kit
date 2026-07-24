# G1 - Requirements / Spec

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Requirements/Spec gate contain,
> and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 1,
> principles 5, 6, 10 (section 2), catalog patterns 1, 3, 4, 5, 6, 8
> ([catalog](../catalog.md)).

## Identity

- **Venue:** spec sign-off at the harness spec-stage exit.
- **Cadence:** per task.
- **Inputs:** the accepted task contract
  ([G0](G0-planning-intake.md)).
- **FAIL blocks:** release of the spec set - design (G2) and implementation
  (G3) cannot start against an unlinted or ambiguous spec.
- **V-model position:** the widest authoring gate in the pipeline. Authored
  here -> enforced downstream:
  - numbered acceptance criteria (REQ-IDs) -> G4.3 traceability
  - immutable acceptance tests -> G4.3 (must pass) + G4.6 (untouchable)
  - property + metamorphic specs -> G4.4
  - boundary schemas (OpenAPI/protobuf) -> G1.1 (linted now), G4.5 (diffed),
    G5.1 (pact-verified)
  - formal models for hard cores -> G1.2 (checked now), G5.6 (trace
    conformance)
  - naive reference implementation for differential-gated components ->
    G5.2. *Roster correction:* absent from the section 5 row's authored
    column but required by catalog pattern 6 ("from the spec stage") -
    carried here source-faithfully.
  - approval-test snapshots (`.approved.*`) -> G4.3 + G4.6 (pattern 5,
    authored G1/G2).

## Why this gate exists

G1 fixes *what correct means*. Every spec-relative (e) check downstream -
acceptance, property, differential, mutation-adequacy - is only as good as
the spec set authored here.
[0002](../../decisions/0002-spec-first-gates-over-static-detectors.md)
concentrates the whole strategy on these artifacts because the residual
defect mass of LLM-generated code (misinterpretation, missing edge cases,
API misuse) is invisible to linters.

Principles bearing:

- **Spec-first properties (principle 5):** authored before and independently
  of the implementation; mechanically checkable; immutable to the
  implementer.
- **Two-channel (principle 6):** the Spec agent's context is decorrelated
  from the Developer's - shared context reproduces shared misreadings.
  (Mechanism is Q5 - a harness design question, not a condition parameter.)
- **Oracle problem (principle 10):** a wrong spec yields conformant wrong
  code. Specs stay declarative so review stays cheap - G1.3 is the one place
  human attention concentrates in the whole pipeline.

Classes closed: requirements misinterpretation (ODC function) - and G1
authors the spec half of every downstream (e)-class closure
([taxonomy](../taxonomy.md)).

## Conditions

### G1.1 Spec/schema linting

- **What (pass condition):** every boundary schema and spec file in the
  task's spec set lints clean under the repo-pinned ruleset configs -
  Spectral exit 0 over OpenAPI/JSON Schema files, `buf lint` exit 0 over
  proto files. Errors AND warnings block - house posture matches G3.3
  `TreatWarningsAsErrors` (ratified 2026-07-23).
- **Why:** an unlintable schema poisons every downstream consumer of it
  (G4.5 diffs, G5.1 pacts) - and lint noise wastes the scarce resource G1.3
  spends, human attention. Catalog pattern 4.
- **Kind & loopability:** mechanical; linter diagnostics are file/line/rule,
  loopable to green.
- **Tooling:** Spectral (OpenAPI / JSON Schema), buf (protobuf). Ruleset
  content is enforcement-layer material - PL-PIPE governs changes to it.
- **Parameters:** the pinned ruleset configs - procedure-bound (whatever the
  repo pins); no open question.
- **Lifecycle:** `specified` (strictness ratified 2026-07-23).

### G1.2 Model checking

- **What (pass condition):** for every component designated a hard core, a
  formal model exists and checks clean pre-implementation - TLC (TLA+) or
  the P checker exits success under the model's pinned configuration
  (state-space bounds are model config, enforcement-pass material).
- **Why:** for components where (c)/(d)-grade detection is unacceptable,
  model checking moves concurrency/protocol flaws to design time - ladder
  position (a)-by-proof. Catalog pattern 8: reserved for hard cores; G5.6
  later ties the implementation to the checked model.
- **Kind & loopability:** mechanical; counterexample traces are the
  diagnostic - loopable, though trace interpretation is the costliest loop
  in the pipeline, part of why hard-core designation is rationed.
- **Tooling:** TLA+/TLC, P; Alloy for structural models (handoff section 7).
- **Parameters:** the hard-core designation procedure, ratified in
  [0007](../../decisions/0007-hard-core-designation-criteria.md): designate
  a component when a defect in it would be (i) concurrency/distributed-
  protocol shaped, (ii) invisible until (d)-time or later, and (iii)
  costly-irreversible in production (data loss, safety, money movement) -
  all three prongs must hold. Procedure-bound like G1.1's pinned rulesets;
  the per-component set is decided at spec time, its recording venue
  deferred to the enforcement pass.
- **Lifecycle:** `specified` (designation criteria ratified 2026-07-23,
  [0007](../../decisions/0007-hard-core-designation-criteria.md)).

### G1.3 Criteria completeness + ambiguity review

- **What (pass condition):** a human reviewer attests every item of the
  review checklist below; any unchecked item returns the spec set to the
  Spec agent with that item as the finding.
- **Why kind=human is irreducible:** no mechanical check can decide whether
  criteria mean the *user's intent* - the oracle problem's chokepoint. The
  design concentrates human attention exactly here (and at G6) and keeps
  specs declarative so the judgment stays cheap.
- **Loopability:** not claimed (human condition); the checklist makes the
  judgment structured and its findings actionable.
- **Tooling:** the review checklist (specified below; the operational
  artifact - form, storage, sign-off record - is enforcement-pass work).
- **Parameters:** the checklist content - PROPOSED.
- **Lifecycle:** `specified` (checklist ratified 2026-07-23).

### G1.3 review checklist (spec) - ratified 2026-07-23

Per criterion:

1. **Testable** - a mechanical check could decide it; names observable
   behavior, not internals.
2. **Unambiguous** - one reading; quantities carry units and bounds; error
   behavior stated, not implied.
3. **Traceable** - cites the task-contract unit it satisfies.

Per spec set:

4. **Complete over units** - every decomposition unit has >=1 criterion.
5. **Covers the sketch** - every `acceptance_sketch` item matured into a
   criterion, or explicitly retired with a reason.
6. **Consistent** - no two criteria demand conflicting behavior.
7. **Respects non-goals** - nothing specifies excluded scope.
8. **Boundary + error paths** - each in-scope input surface has >=1 boundary
   criterion and >=1 error-path criterion.
9. **Property-spec applicability** - surfaces with algorithmic/invariant
   behavior carry property or metamorphic specs (pattern 3), or a recorded
   reason why not.
10. **Schema presence** - every in-scope service/trust boundary has a
    boundary schema (pattern 4).

## Completeness check

Gate purpose: fix what correct means, mechanically checkable downstream.
Examined:

- **Spec-suite executability.** Nothing registered proves the authored
  acceptance suite *runs*. A suite that cannot execute is not "mechanically
  checkable" (principle 5, property 2) - and a suite green before any
  implementation exists is vacuous or mis-targeted. The check belongs at G2
  exit, not here: the tests need G2's interface scaffolding to compile.
  **G2.5 - spec-suite red run** (ratified 2026-07-23): the acceptance +
  property suites compile against the locked scaffold, and every
  not-yet-implemented criterion's test fails (red) before implementation
  starts. Entered G2's roster as `registered`; to be specified at the
  G2+G3 session.
- **Vacuity guards** (criteria per unit, property-spec presence, schema
  presence): absorbed as checklist items 4 / 9 / 10 at the human venue -
  mechanizing them is a later ladder climb, noted, not proposed.

Roster verdict: complete, with one ratified condition exported to G2 (G2.5).

## Operators & harness

The Spec agent authors every G1 artifact; two-channel decorrelation from the
Developer is Q5 (harness design). The entire authored set becomes
G4.6-protected spec paths - immutable to the Developer. The QA agent later
executes the suites (G4-G6); the Verifier's deterministic core audits the
immutability diffs.

## Decisions & open items

- G1.1 strictness (warnings block) and G1.3 checklist ratified 2026-07-23;
  both conditions `specified`.
- Q8 designation criteria ratified 2026-07-23 (session-5 once-over) ->
  [0007](../../decisions/0007-hard-core-designation-criteria.md); G1.2
  `specified`. G2.1 and G5.6 consume the same criteria at their own
  sessions.
- G2.5 ratified into G2's roster as `registered`; specified at the G2+G3
  session.
- Roster corrections recorded: G1 also authors the differential reference
  implementation (pattern 6) and approval snapshots (pattern 5).
