# 5. Fix the task-contract definition-of-ready fields

Status: accepted
Date: 2026-07-23

## Context
G0.1 rejects malformed work by validating the task contract, but the field
set (open question Q2) was never fixed - "acceptance criteria unwritable,
dependencies unresolved, scope unbounded" needed decomposition into
checkable fields. Drafted in `docs/gates/G0-planning-intake.md` from handoff
section 5 row 0 and principle 8; ratified by the user 2026-07-23.

## Decision
Eight required fields: `id` (stable identifier), `intent` (one-paragraph
outcome statement in user language), `scope` (touchable surfaces),
`non_goals` (>=1 explicit exclusion), `decomposition` (>=1 independently
gateable unit with a stated done-meaning), `acceptance_sketch` (1-3 draft
criteria per unit - the writability witness), `dependencies` (each
`resolved` or `blocked-by: <ref>`; all must be resolved), `provenance`
(human request | G8 escape | G9 maintenance). Pass = schema-valid with all
field constraints met; any failure rejects with a field-level diagnostic.

## Consequences
- G0.1 advances `registered -> specified`; JSON-Schema encoding and harness
  wiring remain enforcement-pass work.
- The acceptance sketch makes "criteria unwritable" decidable at intake and
  seeds G1's criteria; `provenance` keeps the convergence loop auditable.
- Q2 closes; the registry's open-parameter index drops it.
