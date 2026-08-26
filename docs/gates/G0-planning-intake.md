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
  unit; every unit carries a unique `id` and >=1 acceptance-sketch
  criterion; declared order resolves and is acyclic. Any failure
  rejects the task with the field-level diagnostic.
- **Why:** the three registered rejection reasons - acceptance criteria
  unwritable, dependencies unresolved, scope unbounded - each decompose into
  field checks (sketch present, dependency statuses, scope + non-goals
  bounded). The field set below is that decomposition.
- **Kind & loopability:** mechanical - `python -m taskcontract validate`
  emits the per-field diagnostics ("`non_goals` empty", "dependency X
  unresolved" - stable TCnnn rule ids), so an agent can loop the contract
  to green without human interpretation.
- **Tooling:** `taskcontract/schemas/task-contract.schema.json` (JSON Schema Draft
  2020-12, draft/ready profiles) checked by the `taskcontract` validator -
  encoding, tooling and wiring ratified in
  [0006](../../decisions/0006-task-contract-enforcement.md); deep page:
  [../task-contract.md](../task-contract.md). Checklist-only human review
  served as the interim state and is retired.
- **Parameters:** the field set - fixed below
  ([0005](../../decisions/0005-task-contract-fields.md)).
- **Lifecycle:** `specified` (field set 0005; schema + validator +
  backstops shipped per 0006); `enforced` in this kit repo since the V9
  self-host (the vocabulary-layer contract entered through `/sdlc intake`,
  2026-07-28) - per-target elsewhere; the Q6 pilot flips at its M0
  session.

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
| `entities` | optional ([0017](../../decisions/0017-vocabulary-layer.md) amendment) - the ratified vocabulary terms the task operates on | the G0.2 coverage join; absent = join inactive, contract valid |
| `confirmed_by` (per unit) | optional in the schema ([0025](../../decisions/0025-intake-seats.md) amendment) - the seats whose answer for the unit was taken at intake | the G0.3 join; demanded on every unit once the repo's `intake-seat` term is ratified, inactive before |

### G0.2 Vocabulary coverage join - added 2026-07-28, [0017](../../decisions/0017-vocabulary-layer.md)

- **What (pass condition):** every `entities:` ref on the contract resolves
  to a *ratified* term at `specs/vocabulary/{term}.yaml`. A missing or
  draft term is an unresolved dependency - the diagnostic names the term
  and the exact file to fork, and the work itself is never failed for
  vocabulary. A deprecated term warns inside its sunset window
  (non-gating) and errors past it. Term files and the constraint registry
  validate at the door.
- **Why:** shared meaning between human and agent holds only when both are
  bound to the same executable definitions - the join makes the contract's
  own language an artifact the gate checks, while ratification stays the
  one cheap human action, concentrated exactly on meaning.
- **Kind & loopability:** mechanical - stable rule ids on both surfaces:
  TC010/TC011/TC012 + W001 from `validate --profile ready`; VT000-VT009 /
  VC000-VC003 from `vocab-check`. The field is optional, so the join
  activates on presence and existing contracts stay valid.
- **Tooling:** `taskcontract/schemas/glossary-term.schema.json` +
  `constraint-registry.schema.json`, the coverage join inside the
  validator, the `/sdlc vocab` family (list / add / extract); deep page:
  [../vocabulary.md](../vocabulary.md).
- **Parameters:** the sunset notice floor rides Q4.
- **Lifecycle:** `enforced` in this repo - the join runs in the live
  intake venue and the CI backstop; per-target elsewhere, as with G0.1.

### G0.3 Unit confirmation - added 2026-08-26, [0025](../../decisions/0025-intake-seats.md)

- **What (pass condition):** when the sibling vocabulary carries
  `intake-seat` at `ratified` (a `value-set` naming the seats this repo
  recognizes), every decomposition unit carries `confirmed_by` and every
  value in it is one of the term's values; otherwise TC016, naming the
  unanswered unit or the unknown seat and the roster. A draft term or
  no term leaves the check inactive; the draft profile never runs it (a
  parked contract may lack answers); loose files stay schema-only.
- **Why:** the intake venue takes a human answer for every unit before
  a contract lands (0024's render-and-confirm step), and until 0025
  nothing recorded who answered - the answer lived in chat, and the PR
  merge records approval of the whole contract, never of a unit. For a
  consumer with more than one human seat (a PO team and an engineer
  team) the record is the artifact the seats and the pipeline share.
  The seat roster is a per-repo term rather than a schema enum because
  who a consumer's humans are is that consumer's meaning, ratified in
  its own tree. Not a seventh human condition (0015): the human act is
  the existing I5 answer; this condition checks the record of it.
- **Kind & loopability:** mechanical - TC016 from `validate --profile
  ready`, one line per unanswered unit or unknown seat, the remedy
  named (return to intake I5 for that unit).
- **Tooling:** `confirmation_join` beside the coverage join in
  `taskcontract/vocabulary.py`, wired in `checker.validate_path`'s
  ready-profile specs-tree block; the record written by `/sdlc intake`
  I5-I6 (`skills/sdlc/flows/intake.md`); registry entry
  `g0-3-unit-confirmation` in `specs/vocabulary/constraints.yaml`;
  deep page: [../task-contract.md](../task-contract.md).
- **Parameters:** none open. The seat map (which fields each seat
  holds) is consumer policy recorded in USAGE §8, never enforced: the
  door reads the answer, not the author.
- **Lifecycle:** `specified` (0025); `enforced` in this repo since the
  kit's own `intake-seat` term (one value, `user`) was ratified
  2026-08-26 and every unit stamped; per-target elsewhere, armed by
  each consumer's own ratification.

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

- **Per-field authorship check** (did the PO seat write `intent`?):
  examined at the 0025 walk and rejected - the door reads the answer,
  never the author; field ownership is consumer policy (USAGE §8).

Roster verdict: complete - three conditions (G0.1 definition-of-ready,
G0.2 vocabulary coverage, G0.3 unit confirmation); fully specifying them
*is* the gate.

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
  built (`taskcontract/` with its packaged `schemas/`, fixtures + CI). E5
  sharpens the G4.6
  input: the protected set becomes the single root `specs/**`.
- G0.3 added 2026-08-26 ->
  [0025](../../decisions/0025-intake-seats.md): the roster grows 2 -> 3
  under 0014's full lane (tightening; the human principal's answer
  recorded at the pull merge, carried by its own unit `g0-3-row`).
  Schema 1.3.0 (additive `confirmed_by`), TC016, intake I5-I6, the
  kit's seat term ratified and every unit stamped in the same arc.
