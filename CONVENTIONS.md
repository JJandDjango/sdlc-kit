# Conventions - sdlc_development_kit

> **Contract** - one question: *how do we do things here?*
> <=1 page - update when a rule is adopted / revised / retired - hand-edited,
> significant entries link their ADR.

<!-- An index, not an essay: one line per rule (bold name + statement, ADR link
     when significant). Detail overflows to docs/conventions/ pages. Inferred
     entries carry "(inferred - confirm)" - confirm them and delete the tag. -->

- **Decisions get recorded.** A choice a future you would question gets an ADR
  ([[0001-record-architecture-decisions]]).
- **Gate vocabulary.** A *gate* is a phase's blocking enforcement venue
  (G0-G10, PL-*); a *condition* is a check attached to it, lifecycle
  `registered -> specified -> enforced`. Registry: `docs/gates.md`
  ([[0003-gate-vocabulary-and-registry]]).
- **Gate pages.** Each gate gets a deep page `docs/gates/<ID>-<slug>.md` on
  the fixed template; the registry stays the one-line index; PROPOSED roster
  changes enter only on user ratification
  ([[0004-per-gate-documentation-program]]).
- **Task contracts.** One per task at `specs/<task-id>/contract.yaml`, valid
  against `taskcontract/schemas/task-contract.schema.json` (`ready`
  profile) via `python -m taskcontract validate`
  ([[0006-task-contract-enforcement]]).
<!-- Example code rule - adapt or delete:
- **Match the idiom.** New code follows the touched layer's dominant pattern.
-->
