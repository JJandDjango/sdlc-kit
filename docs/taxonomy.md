# Bug-class taxonomy - sdlc_development_kit

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *which bug classes exist, where is each closed,
> and how detectable is it?*
> Living page (source: handoff section 3) - update when a class's closure
> moves or a gap closes. Anchors every gate page's "why" section.

## The detectability ladder

Every bug class sits at one of five positions; engineering effort pushes
classes *up* the ladder rather than accumulating detectors at the bottom
(THEORY invariant).

| Pos | Meaning | Example mechanism |
|---|---|---|
| (a) | eliminable by construction | type system, parse-don't-validate, typestate |
| (b) | statically decidable | definite assignment, exhaustiveness |
| (c) | statically approximable | taint/dataflow, lifetime analyzers |
| (d) | dynamic-only | fuzzing, systematic concurrency testing, benchmarks |
| (e) | spec-relative | acceptance/property/differential suites - correct only relative to an authored spec |

## Anchors

- **CWE** (MITRE) - ~900+ weaknesses, hierarchical; analyzers tag rules with
  CWE IDs, making coverage mechanically auditable. CWE-1000 "Research
  Concepts" view, ten pillars: 284 access control, 435 improper interaction
  between entities, 664 resource lifetime, 682 incorrect calculation,
  691 control flow, 693 protection mechanism failure, 697 incorrect
  comparison, 703 exceptional-condition handling, 707 improper
  neutralization, 710 coding-standard violations.
- **ODC** (Chillarege/IBM) - eight defect types: function, interface,
  checking, assignment, algorithm, timing/serialization, build/package,
  documentation. Covers the plain functional defects CWE's security
  weighting undercovers.

## Class -> closure mapping

Condition anchors are registry IDs ([gates.md](gates.md)); "-" marks a class
with no registered condition yet - an input to that gate's completeness
check when its session arrives.

| Bug class | Anchor | Ladder | Closed by |
|---|---|---|---|
| Type/interface misuse | CWE-704, ODC interface | (a) | G3.3 strict compile |
| Null/uninitialized state | CWE-476, 457 | (a)/(b) | G3.3 (`Nullable` enable, definite assignment) |
| Memory safety (managed code) | CWE-119, 416, 415 | (a) | language choice (GC) - closed by construction, no condition needed |
| Memory safety (native interop) | CWE-119 family | (d) | G5.3 mandatory fuzz-gating of interop wrappers + sanitizer instrumentation - the compensating control G3.3 clause 4 demands (S9 ruling) |
| Resource lifetime | CWE-664, 772 | (c) | G3.2 / G4.1 (lifetime analyzers, e.g. CA2000) |
| Injection / neutralization | CWE-707: 79, 89, 78 | (c), strong | G4.7 taint/dataflow scan |
| Input validation / parsing | CWE-20 | (a) + (d) | G1/G2 parse-don't-validate types; G5.3 fuzzing |
| Numeric / calculation | CWE-682: 190, 193 | (a)/(c) + (e) | G3.3 checked arithmetic; G2 unit-of-measure types; G4.4 property tests |
| Incorrect comparison | CWE-697 | (b)/(e) | G3.2/G4.1 battery rules; G5.5 mutation floor |
| Error/exception handling | CWE-703, 390 | (c)/(e) | G4.1 (swallowed-catch rules); G5.5 mutation floor |
| Control flow (non-concurrency) | CWE-691: 484, 835 | (b) | G3.3 strict compile; G3.2/G4.1 battery |
| Concurrency | CWE-362, 667 | (d); (a) with ownership types | G2.1 design model check; G5.4 systematic testing; G5.6 trace conformance |
| Improper interaction between entities | CWE-435 | (d)/(e) | G5.1 consumer-driven contracts; G5 integration suite |
| Access control / authz | CWE-284, 693 | (c)/(e), design-level | G2.4 threat model -> abuse-case tests (run in G4.3); G4.7 CodeQL patterns |
| API/protocol misuse (call order) | ODC interface | (d) -> (a) via typestate | G2 typestate scaffolding; G3.2 custom analyzers |
| Logic / algorithmic | ODC algorithm | (e) | G4.4 property; G5.2 differential; G5.5 adequacy floor |
| Requirements misinterpretation | ODC function | (e) | G1 spec set (G1.3 review), enforced at G4.3 traceability; G6 catches the residue |
| Build / config / deployment | ODC build/package | (b)/(c) | G6.3 certified-path rehearsal incl. revert leg (dynamic half, per candidate - S10); G7.3 IaC scanning (static half) |
| Performance | CWE-400, 407 | (d) | G5.7 soak/resource-trend (trend class - the earlier rung, S9); G7.1 benchmark budgets (absolute ceilings, quiet infra - S10) |
| Breaking change (consumer contract) | ODC interface | (b) | G4.5 surface diff (source, per merge); G7.2 binary compat (shipped form, per release - S10; row added S10, gap found at the G7 walk) |
| Artifact integrity (shipped supply chain) | CWE-494 family / SLSA threats | (b) | G7.5 SBOM + provenance attestation (S10); consumed by G7 admission interlock 2 |

The 435/691/697 rows close the pillar-tagging gap found in the session-7
sweep - every CWE-1000 pillar now has >=1 tagged row; rule-level
substantiation of the battery-anchored rows = the battery-CWE map +
PL-PIPE.2 golden test (G4-session ruling: three strata - vendor-shipped
imports, load-bearing hand-tags incl. 703, tier-level style tag; build
item, rides pilot activation).

Structural degradation (complexity, duplication, coupling, drift, dead code)
is deliberately not a row here - it is not a bug class but an entropy
process, closed by ratchets and architecture tests (G4.2, G4.8, G10.2) per
[0002-spec-first-gates-over-static-detectors](../decisions/0002-spec-first-gates-over-static-detectors.md).

## Gap-analysis method

Enumerate the ten pillars -> map enabled analyzer rules (by CWE tag) against
them -> every uncovered node is a decision point: write an analyzer or write
a test. Program role: this method runs inside each gate page's completeness
check (the G3 and G4 sessions especially); findings become PROPOSED
conditions per
[0004-per-gate-documentation-program](../decisions/0004-per-gate-documentation-program.md).
