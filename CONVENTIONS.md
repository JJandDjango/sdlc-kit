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
<!-- Example code rule - adapt or delete:
- **Match the idiom.** New code follows the touched layer's dominant pattern.
-->
