# G2 - Design / Architecture

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Design/Architecture gate
> contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 2,
> principles 1, 2, 4, 5 (section 2), catalog patterns 2, 5, 8
> ([catalog](../catalog.md)).

## Identity

- **Venue:** design sign-off + baseline lock.
- **Cadence:** per task/component.
- **Inputs:** the signed-off spec set ([G1](G1-requirements-spec.md)).
- **FAIL blocks:** implementation start - without locked baselines there is
  nothing to gate the implementation against.
- **V-model position:** where the pipeline stops *describing* correctness
  (G1's job) and starts *constraining the space the Developer can move in*.
  Authored here -> enforced downstream:
  - interface + domain-type scaffolding -> G2.5 (compiles now), G3.3
    (constrains generation from the first token)
  - `PublicAPI.Shipped/Unshipped.txt` + schema baseline locks -> G4.5
    (source diff), G7.2 (binary compat)
  - architecture rule tests (NetArchTest) -> G4.2
  - typestate encodings -> the compiler itself at G3.3 - (a)-class closure,
    no dedicated condition needed
  - ratchet budgets/baselines -> G4.8 (enforcement sharpening exported to
    the G4 session - see completeness check)
  - threat model -> abuse-case criteria + tests -> G4.3 (suite), G4.6
    (protected)
- **Authoring vs locking:** boundary schemas are authored at G1 (pattern
  4); G2's act for them is the *lock* - registering each as the immutable
  diff reference. The code-surface baseline is both authored and locked
  here, because the scaffold it captures is a G2 artifact (pattern 2).

## Why this gate exists

G2 fixes the *shape* - types, surfaces, structure rules. Principle 2 is
the headline: correct-by-construction beats detect-after-generation -
shrink the space of representable programs so generation lands inside the
valid space.

Principles bearing:

- **Detectability ladder (principle 1):** G2 is the pipeline's main
  ladder-climbing venue. Typestate encodings move API call-order misuse
  (d) -> (a); parse-don't-validate types move input validation to (a);
  unit-of-measure types move calculation errors to (a). Each climb is an
  authoring act that happens here.
- **Earliest decidable point (principle 4):** the lock happens *before*
  implementation because that is the last moment the baseline is
  uncontaminated - a baseline captured after code exists merely ratifies
  whatever the code did.
- **Spec-first properties (principle 5):** every G2 artifact is a spec
  artifact - authored before and independently of the implementation,
  mechanically checkable, immutable to the implementer. The entire
  authored set enters G4.6 protection at the lock moment.

Classes closed: API misuse, concurrency design flaws, architectural
erosion (an entropy process, closed via authored arch tests + ratchets
enforced at G4.2/G4.8), design-level security flaws - plus G2 authors the
(a)-half of the parse-don't-validate (CWE-20) and unit-of-measure
(CWE-682) rows ([taxonomy](../taxonomy.md)).

**The G1.2 <-> G2.1 division** (ratified this session): G1.2 checks the
*spec-side model* - the required guarantees of the protocol, as
requirements. G2.1 checks the *design-side model* - the chosen
realization: concrete component interactions, state machines, lock
orders, message flows as the design fixes them. Same hard-core set
([0007](../../decisions/0007-hard-core-designation-criteria.md)), same
tooling family, different artifact under check: a G1.2 failure means the
requirement itself is contradictory or unrealizable; a G2.1 failure means
this design violates a requirement already proven satisfiable. This is
also why Alloy (structural models) appears in G2.1's tooling but is
peripheral at G1.2.

## Conditions

### G2.1 Design-level model checking

- **What (pass condition):** for every component designated a hard core
  ([0007](../../decisions/0007-hard-core-designation-criteria.md), applied
  at spec time), a design-level model of the chosen realization exists and
  checks clean before implementation start - TLC (TLA+), the P checker, or
  the Alloy analyzer exits success under the model's pinned configuration.
  The model must **assert the spec-side guarantees the G1.2 model fixed**
  (plus any design-introduced invariants) - a model with no properties
  asserted checks "clean" vacuously, so property carry-forward is part of
  the pass condition. State-space bounds are model config,
  enforcement-pass material (G1.2 precedent).
- **Why:** the division above - G1.2 proved the requirement satisfiable;
  G2.1 proves *this design* does not violate it, while the design is
  still text. For hard cores, (c)/(d)-grade detection is unacceptable by
  designation; this is the (a)-by-proof rung for the concurrency row.
  Catalog pattern 8; G5.6 later ties implementation traces back to this
  checked model.
- **Kind & loopability:** mechanical; counterexample traces are the
  diagnostic - loopable, and (with G1.2) the costliest loop in the
  pipeline, which is why 0007 rations the designation set.
- **Tooling:** TLA+/TLC, P; Alloy for structural models.
- **Parameters:** designation procedure = 0007 (procedure-bound);
  properties carried from the G1.2 model = all applicable; pinned checker
  config = enforcement-pass material.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G2.2 Breaking-change baseline lock

- **What (pass condition):** before implementation start, every public
  surface in the task's scope has its baseline committed under the
  G4.6-protected spec paths: code - `PublicAPI.Shipped.txt` /
  `.Unshipped.txt` per scaffold assembly (PublicApiAnalyzers); HTTP - the
  OpenAPI document registered as oasdiff's reference; proto - the buf
  breaking baseline. The surface enumeration is mechanically derived, not
  hand-declared: every assembly in the locked scaffold needs its PublicAPI
  pair; every G1-authored boundary schema needs its baseline registration.
  Check = each derived surface's baseline exists at its expected path.
  **"Locked" means committed into the protected paths** - the lock is
  G4.6's path immutability, not a property of the file.
- **Why:** a breaking change is only detectable relative to a baseline
  that predates the code (principle 4). Pattern 2: the scaffold *is* the
  API spec; the baseline is what makes it diffable downstream.
- **Kind & loopability:** mechanical; diagnostics are path-level
  ("missing baseline for assembly X / schema Y") - the cheapest loop in
  the gate: generate, commit, re-run.
- **Tooling:** PublicApiAnalyzers, oasdiff, buf. Shipped/Unshipped
  population mechanics (new surface enters Unshipped until release
  promotes it) are tooling discipline, enforcement-pass material.
- **Parameters:** surface enumeration = derived from scaffold + spec set
  (procedure-bound). Baseline path layout fixed by
  [0010](../../decisions/0010-write-surface-immutability.md):
  `specs/baselines/` via AdditionalFiles wiring. Ratchet baselines are
  *not* this condition (see completeness check).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G2.3 ADR review

- **What (pass condition):** a human reviewer attests every item of the
  checklist below; any unchecked item returns the design set to the Spec
  agent with that item as the finding.
- **Why kind=human is irreducible:** no mechanical check can decide
  whether every significant choice *got recorded* (significance coverage
  is judgment) or whether a recorded rationale holds together. This is
  the Theory rule's venue inside the pipeline - commit nothing you could
  not explain; the ADR is the explanation, G2.3 checks it exists and
  reconciles. Distinction on record: the pipeline's two human *attention
  concentration* points - where the oracle problem forces judgment on
  what correct means - are G1.3 and G6. G2.3 is human for a narrower,
  cheaper reason (rationale review, deliberately rationed so it never
  grows into a third correctness bottleneck); G8.3 (triage) and PL-PIPE.1
  (second-channel approval) complete the six-condition human roster.
- **Loopability:** not claimed (human); findings are per-item and
  actionable.
- **Tooling:** the repo's `decisions/` convention; the checklist below.
  Sign-off mechanics = enforcement-pass material (G1.3 precedent).
- **Parameters:** the triggers + checklist content - ratified 2026-07-24.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G2.3 significance triggers (spec) - ratified 2026-07-24

An ADR is owed when a design choice:

1. fixes or changes a **public surface or baseline** (what G2.2 locks);
2. **crosses or creates a trust boundary** (what G2.4 models);
3. **designates or de-designates a hard core** (0007 application);
4. fixes a **structural rule** (what an architecture rule test enforces);
5. is **irreversible without a migration** (persisted shape, protocol
   version).

Significance is not taste: each trigger is defined by a downstream gate
consuming the choice - "significant" means *some enforcement artifact
will embody this*.

### G2.3 review checklist (spec) - ratified 2026-07-24

Per ADR:

1. **Why articulated** - context states the forces; the decision
   reconciles with them.
2. **Alternatives recorded** - with the reason each lost.
3. **Consequences name the enforcing artifact** - which baseline, rule
   test, threat model, or formal model embodies the decision downstream.
   An ADR nothing enforces is a wish.
4. **No conflict** with accepted ADRs, or an explicit supersession.

Per design set:

5. **Trigger coverage** - every trigger-hitting choice in the design has
   its ADR.
6. **Structural rules have teeth** - every structural rule an ADR fixes
   has its architecture rule test in the scaffold.
7. **Typestate applicability** - call-order-sensitive surfaces carry
   typestate encodings, or a recorded reason why not.

### G2.4 Threat-model existence

- **What (pass condition):** every trust-boundary crossing the design
  declares has a STRIDE-per-boundary threat model recorded in the design
  set, and every abuse case a model identifies has entered the spec suite
  as a numbered security acceptance criterion with its test. Mechanical
  check = existence + linkage: (a) each declared boundary crossing -> a
  threat-model artifact; (b) each abuse case -> >=1 criterion test. The
  tests are spec artifacts like any other - G4.3 runs them, G4.6 protects
  them, and at G2 exit they are red with the rest of the suite (G2.5).
- **Why:** the taxonomy puts access control / authz at (c)/(e),
  design-level - after code exists, the best available is CodeQL patterns.
  The threat model moves identification to design time, and the
  **compilation clause keeps it from being shelf-ware**: a model that does
  not emit executable abuse-case tests is documentation, not a gate. Same
  anti-vacuity instinct as G2.1's property carry-forward and G2.5's red
  run - every G2 artifact must have a downstream mechanical consumer.
- **Division of labor:** G2.4 checks existence + linkage *against the
  declared boundary enumeration*. Whether the enumeration is complete -
  whether the design silently crosses a boundary it never declared - is
  not mechanically decidable; that judgment lives at G2.3 via trigger 2
  and checklist item 5. Human judges the enumeration; machine verifies
  everything enumerated got its model and tests.
- **Kind & loopability:** mechanical; diagnostics per boundary / per
  abuse case ("boundary B lacks a model", "abuse case n has no test"),
  loopable.
- **Tooling:** STRIDE process; the linkage check is the same shape as
  G4.3's traceability script - abuse cases enter the numbered criteria
  set, so criterion -> test mapping rides the existing traceability
  mechanism rather than growing a parallel one.
- **Parameters:** boundary enumeration = design artifact, completeness
  judged at G2.3; abuse-case criterion ID mechanics ride
  [0011](../../decisions/0011-criterion-traceability-format.md) (kind
  metadata, one grammar); model recording venue = enforcement-pass
  material (0007 precedent).
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G2.5 Spec-suite red run

- **What (pass condition):** three clauses.
  1. **Compile** - the G1-authored acceptance + property suites compile
     against the locked scaffold; compile failure = FAIL. This is where
     the spec suite and the design shape provably meet.
  2. **Coverage** - every criterion in the spec set (functional + G2.4
     security criteria) has >=1 discovered test: G4.3's traceability
     check run in *existence* mode, pass-status ignored.
  3. **Red** - executing the suites, every criterion-annotated test is
     red (fail or error - both count; `NotImplementedException` from a
     scaffold stub is the normal red here) and **zero criterion tests
     pass**. Architecture rule tests run *green* by design - they check
     the scaffold's structure, which exists. Runner crash or zero tests
     discovered = FAIL.
- **Why:** the condition's design source is G1's completeness finding
  (ratified 2026-07-23, exported here): "mechanically checkable"
  (principle 5, property 2) is unproven until the suite *runs*, and a
  suite green before any implementation is vacuous or mis-targeted. The
  deeper why: after G2, every criterion test transitions red -> green
  exactly once, and that transition *is* the implementation's progress
  signal - the Developer loops against red tests until green. A test that
  starts green never signals anything; G2.5 is the last moment "green" is
  still unambiguous evidence of a spec defect. TDD's red-green
  discipline, promoted from practice to gate.
- **Clause 2 goes beyond the registry row** (ratified addition): a
  criterion with no test at all sails through a red run invisibly, and
  G4.3 catching it at merge is too late by the pipeline's own logic -
  tests must exist *before* implementation (principle 4, pattern 1). Cost
  is nil: the G4.3 script with pass-checking off.
- **Kind & loopability:** mechanical; diagnostics per test (compile
  errors with file/line; uncovered criteria named; unexpectedly-green
  tests named), loopable by the Spec agent.
- **Tooling:** test runner + the traceability script in existence mode.
- **Parameters:** criterion-annotation format fixed by
  [0011](../../decisions/0011-criterion-traceability-format.md) (shared
  with G2.4); red = fail-or-error, fixed here.
- **Lifecycle:** `specified` (ratified 2026-07-24).

## Completeness check

Gate purpose: fix the shape; every artifact authored here must have a
downstream mechanical consumer. Examined:

- **Architecture-rule-test existence.** Authored here, enforced at G4.2 -
  but nothing gated that the tests *exist* per structural rule. Absorbed
  as G2.3 checklist item 6 (the reviewer walks the ADR-fixed rules
  against the scaffold); mechanizing is a later ladder climb, noted, not
  proposed.
- **Typestate presence.** Authored artifact whose enforcement is the
  compiler ((a)-class); which surfaces need it is design judgment.
  Absorbed as G2.3 checklist item 7 (G1.3 item-9 shape: encode, or record
  why not).
- **Ratchet-baseline lock.** Authored here ("ratchet baselines"), enforced
  at G4.8, gated nowhere. Candidate G2.6 (mechanical existence check)
  examined and **rejected**: the G2.2 capture-timing argument does not
  transfer (the complexity budget is an authored number - Q4 threshold
  selection, not a measurement; the duplication baseline is captured from
  main, which never contains the in-flight diff - uncontaminated
  regardless of timing), and a per-repo artifact behind a per-task gate is
  a noise condition - genuinely checked once at bootstrap, trivially
  green forever after. The teeth live at G4: **exported to the G4
  session** - G4.8's pass condition must include fail-if-baseline-missing;
  ratchet budgets/baselines reside in the G4.6-protected paths (an agent
  that can edit a ratchet baseline will loosen it - principle 5's
  test-editing logic verbatim); bootstrap = author budgets (Q4) + capture
  duplication from main. Registry drift fixed in the same pass: the G2
  authored line read "(complexity, coverage)" - no coverage ratchet is
  registered anywhere (adequacy is G5.5's mutation floor); the metric set
  is G4.8's, selection Q4's.

Roster verdict: complete, zero additions - two findings absorbed into the
G2.3 checklist, one exported to the G4 session, one registry drift fix.

## Operators & harness

The Spec agent authors every G2 artifact (handoff section 6: phases 0-2
are its surface). G2 exit is the **lock moment** - the venue name's
"baseline lock" is the flip from draft to G4.6-protected, after which the
Developer can read everything and touch nothing. The QA agent executes
the downstream suites (G4-G6); the Verifier audits the immutability
diffs. G2.3's reviewer is human - the rationed, non-oracle human venue
(the pipeline's two attention-concentration points stay G1.3 and G6).

## Decisions & open items

- All five conditions `specified` 2026-07-24 (session-6 walk); rulings
  ratified in-conversation before edits landed.
- The G1.2 <-> G2.1 two-model division ratified (spec-side guarantees vs
  design-side realization); anchors both pages' why-sections.
- G2.1 property carry-forward clause ratified as part of the pass
  condition (anti-vacuity).
- G2.3 significance triggers (5) + review checklist (7) ratified; items
  6-7 absorb completeness findings.
- G2.5 clause 2 (coverage existence) ratified as an addition beyond the
  registry row (principle 4 + pattern 1).
- Ratchet-baseline enforcement exported to the G4 session (no G2.6);
  G4-session inputs now: protected set = single root + task contracts
  (G0 page note) + ratchet fail-if-missing/residence/bootstrap (here).
- Shared open parameter: REQ-ID / criterion-annotation format - closed
  at the G4 session ->
  [0011](../../decisions/0011-criterion-traceability-format.md); G2.4
  linkage and G2.5 coverage ride it.
- Recording venues (threat models, hard-core designations) deferred to
  the enforcement pass throughout (0007 precedent).
