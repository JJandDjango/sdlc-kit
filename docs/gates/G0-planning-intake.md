# G0 - Planning / Intake

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Planning/Intake gate contain,
> and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 0 and
> principles 3, 4, 8, 10 (section 2).

## Identity

- **Venue:** harness intake step - before any spec authoring.
- **Cadence:** per task; the pipeline's entry point.
- **Inputs:** the candidate task - a raw work request (human ask, G8 escape
  conversion, G9 scheduled maintenance).
- **FAIL blocks:** the task entering the spec stage. Nothing downstream runs.
- **V-model position:** authors the **task contract**; G1 consumes it as its
  input, and every later gate implicitly checks against its scope baseline.
  Nothing sits upstream - G0 is where work enters the system.

## Why this gate exists

Mis-selection is the dominant upstream failure for agent pipelines: a
malformed task defeats every downstream gate, because those gates check
conformance to artifacts derived from it. Closing malformedness at intake is
the cheapest possible rejection point - principle 4 (earliest decidable
point) applied at cost zero, before any artifact exists.

Ladder: mis-selection and scope creep are inherently spec-relative (e) - but
the definition-of-ready check pushes *malformedness* down to (b) statically
decidable, once the task contract is a schema-validatable artifact. That is
principle 3 verbatim: a human judgment ("is this task ready?") converted
into a text artifact (the contract) plus a mechanical check (validation).

Classes closed: mis-selection, scope creep - the upstream half of
requirements misinterpretation ([taxonomy](../taxonomy.md)). Principle 10
also bears: G0 is the first oracle guard - a wrong task yields conformant
wrong everything downstream.

## Conditions

### G0.1 Definition-of-ready check

- **What (pass condition):** the task contract validates against the
  task-contract schema: all required fields present and non-empty; every
  dependency `resolved`; the decomposition lists >=1 independently gateable
  unit; every unit carries >=1 acceptance-sketch criterion. Any failure
  rejects the task with the field-level diagnostic.
- **Why:** the three registered rejection reasons - acceptance criteria
  unwritable, dependencies unresolved, scope unbounded - each decompose into
  field checks (sketch present, dependency statuses, scope + non-goals
  bounded). The field set below is that decomposition.
- **Kind & loopability:** mechanical - `python -m taskcontract validate`
  emits the per-field diagnostics ("`non_goals` empty", "dependency X
  unresolved" - stable TCnnn rule ids), so an agent can loop the contract
  to green without human interpretation.
- **Tooling:** `schemas/task-contract.schema.json` (JSON Schema Draft
  2020-12, draft/ready profiles) checked by the `taskcontract` validator -
  encoding, tooling and wiring ratified in
  [0006](../../decisions/0006-task-contract-enforcement.md); deep page:
  [../task-contract.md](../task-contract.md). Checklist-only human review
  served as the interim state and is retired.
- **Parameters:** the field set - fixed below
  ([0005](../../decisions/0005-task-contract-fields.md)).
- **Lifecycle:** `specified` (field set 0005; schema + validator +
  backstops shipped per 0006). `enforced` awaits the intake venue going
  live in a harness (pilot, Q6).

### Task-contract field set (Q2) - ratified 2026-07-23, [0005](../../decisions/0005-task-contract-fields.md)

| Field | Requirement | Grounding |
|---|---|---|
| `id` | stable task identifier | downstream traceability - REQ-IDs trace to a task; G8 escapes file new tasks |
| `intent` | one-paragraph outcome statement in user language | the authored intent G1 criteria must reconcile with |
| `scope` | the surfaces/components the task may touch | "scope unbounded" rejection; the baseline later gates check diffs against |
| `non_goals` | >=1 explicit exclusion | handoff section 5 row 0; scope-creep detection needs the negative space fixed |
| `decomposition` | >=1 unit, each independently gateable, each with a stated done-meaning | section 5 row 0 authored column |
| `acceptance_sketch` | 1-3 draft criteria per unit | the writability witness - "criteria unwritable" is decidable only by attempting one; full criteria remain G1's job |
| `dependencies` | list; each `resolved` or `blocked-by: <ref>`; all must be `resolved` to pass | "dependencies unresolved" rejection |
| `provenance` | origin: human request / G8 escape / G9 maintenance | (derived - principle 8) the convergence loop needs escapes distinguishable at intake |

## Completeness check

Gate purpose: reject malformed work at entry. The CWE pillars do not apply -
no code exists at intake; the failure surface is process-level and covered
by G0.1's field checks. Examined and **not** proposed:

- **Unit-size bound** (a "too big to gate" unit): intent is covered by the
  decomposition field; a mechanical size bound is threshold-territory
  (Q4-like). Revisit if pilot intake shows oversized units passing.
- **Concurrent-task scope conflict** (two open tasks touching one scope): a
  harness scheduling concern, not an intake-correctness check. Logged as a
  harness observation.

Roster verdict: complete - one condition; fully specifying it *is* the gate.

## Operators & harness

The Spec agent authors the task contract from the raw request; the intake
check runs in the harness before the spec stage opens. The accepted contract
is a G0-authored spec artifact - immutable to the Developer under the
mutability model. **Cross-reference note, honored at the G4 session:** G4.6's
protected set is now the single root `specs/**`, task contracts included
([0010](../../decisions/0010-write-surface-immutability.md), class S) -
the mutability model's promise kept.

## Decisions & open items

- Q2 resolved: field set ratified ->
  [0005](../../decisions/0005-task-contract-fields.md); G0.1 `specified`.
- Observations parked: unit-size bound; concurrent-scope harness note;
  G4.6 enumeration must add task contracts (input to the G4 session;
  honored -> [0010](../../decisions/0010-write-surface-immutability.md)).
- Enforcement pass (session 4): three-stop walk-through ratified encoding,
  validator and wiring ->
  [0006](../../decisions/0006-task-contract-enforcement.md); mechanism
  built (`schemas/`, `taskcontract/`, fixtures + CI). E5 sharpens the G4.6
  input: the protected set becomes the single root `specs/**`.
