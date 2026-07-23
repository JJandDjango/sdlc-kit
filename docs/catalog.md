# Spec-first gate catalog - sdlc_development_kit

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what are the spec-first patterns, and where is
> each authored and enforced?*
> Living page (source: handoff section 4) - update when a pattern's authoring
> or enforcement venue moves. Moved here from the registry's cross-reference
> section; `docs/gates.md` links back.

Spec-first artifacts share three defining properties (THEORY invariant):
authored **before and independently of** the implementation; **mechanically
checkable**; **immutable to the implementer** - enforced by path checks
(G4.6), never by prompt instructions.

| # | Pattern | Authored | Enforced by |
|---|---|---|---|
| 1 | Immutable acceptance tests + traceability | G1 | G4.3, G4.6 |
| 2 | Type-first scaffolding + API surface lock | G2 | G4.5 (source), G7.2 (binary) |
| 3 | Property-based + metamorphic specs | G1 | G4.4 |
| 4 | Boundary contracts | G1 | G1.1 (lint), G4.5 (schema diff), G5.1 (consumer pacts) |
| 5 | Approval tests with locked snapshots | G1/G2 | G4.3 (suite) + G4.6 (`.approved.*` immutability) |
| 6 | Differential gates | G1 (reference impl) | G5.2 |
| 7 | Mutation threshold | - (meta: adequacy of the suites) | G5.5 |
| 8 | Formal models for hard cores | G1 | G1.2, G2.1, G5.6 |

## The patterns

1. **Immutable acceptance tests + traceability.** The spec stage emits
   numbered criteria (REQ-IDs) and executable tests; implementer tests carry
   `[Criterion("REQ-014")]`-style annotations; CI requires every REQ-ID ->
   >=1 passing test; any diff touching spec paths fails the build.
   Attacks: requirements misinterpretation.
2. **Type-first scaffolding + API surface lock.** The spec stage writes
   interfaces / domain types / DTOs; `PublicAPI.Shipped.txt`
   (PublicApiAnalyzers) is the source-time lock; ApiCompat the binary lock at
   release. Attacks: API misuse, unapproved breaking change.
3. **Property-based and metamorphic specs.** FsCheck/CsCheck; declarative
   behavioral specifications over the input space, hard to satisfy vacuously.
   Attacks: missing edge cases, logic/algorithmic defects.
4. **Boundary contracts.** OpenAPI / JSON Schema / protobuf written first;
   schema validation in tests; breaking-change detection (oasdiff,
   `buf breaking`); consumer-driven contract tests (PactNet).
   Attacks: interface drift, interaction defects.
5. **Approval tests with locked snapshots.** Verify; `.approved.*` files are
   human/spec-approved and non-regenerable by the implementer.
   Attacks: silent behavioral change on complex outputs.
6. **Differential gates.** A naive obviously-correct reference implementation
   from the spec stage; the optimized implementation is gated by equivalence
   over generated inputs. Strongest oracle for algorithmic code.
   Attacks: logic/algorithmic defects.
7. **Mutation threshold.** Stryker.NET score floor. Gates the *spec's
   adequacy* - proves the acceptance/property suite actually constrains
   implementations; closes the vacuous-test loophole.
   Attacks: vacuous specs (meta-pattern over 1 and 3).
8. **Formal models for hard cores.** TLA+/Alloy/P model-checked
   pre-implementation, linked by trace-conformance tests or model-based test
   generation; Dafny where proof-carrying code is itself the gate. Reserved
   for components where ladder positions (c)-(d) are unacceptable
   ([taxonomy](taxonomy.md)).
   Attacks: concurrency/protocol design flaws.
