# 24. Unit dependency graph in the task contract

Status: accepted
Date: 2026-08-22

## Context

Relayed request, 2026-08-22: `decomposition` is an unordered list.
Unit order lives only in plan prose - no door reads it, nothing
validates it, and a rewritten plan drifts it silently. The ask is
order declared in the contract, checked at G0, and rendered as
Mermaid so a decomposition is reviewable as a shape rather than a
list a human holds in their head.

Rulings already on record that bind the design:

- The schema is `additionalProperties: false` at root and at every
  `$def`. `$defs.unit` carries `unit`, `done_means`, and
  `acceptance_sketch` only, so any new field is TC005 until shipped.
- Contracts are immutable to implementers (0010, enforced G4.6).
  Progress state can therefore never live in the contract.
- The human census is fixed at six (0015). No seventh human
  condition: node-by-node review rides the existing `/sdlc intake`
  venue rather than becoming a new gate.
- Two-layer model (0008): the graph is shape, Mermaid is rendering.

Precedent: 0017's `entities` field records its coverage join in the
schema description as "a Python-side ready check - not expressible
here." Graph validity is the same category - JSON Schema cannot
express reference resolution or acyclicity.

Facts established at the intake that authored `specs/unit-dag/`:
TC013 through TC015 are unused (TC000-TC012 are taken); the census
was 46 units across 7 contracts, and 49 across 8 once the orphaned
`glossary-alias-disjointness` contract landed; and the direction
classifier that 0014 routes class-E deltas through does not exist -
0014's own Consequences list it as a Q6 build item.

## Decision

- **`id` is required on every unit.** Optional ids leave references
  unstable across insertion and reorder, and a conditional
  required-rule ("ids only when the contract declares `depends_on`")
  buys zero migration at the price of two classes of unit and a
  second render path. Breaking: schema 1.1.0 -> 1.2.0, and every
  unit in every contract gains an `id` in the same commit. The kit
  is pre-1.0 and its own first consumer, and the one outside
  consumer pins v0.10.0, so the migration is contained here and
  never cheaper than now. **This amends 0006 E1**, which ratified
  the unit shape as `{unit, done_means, acceptance_sketch}` with
  "No per-unit id" on the grounds that 0011 needed none - criteria
  cite units by name. That reasoning held while nothing else
  referenced a unit; `depends_on` is the first thing that does, and
  a reference needs a referent that survives an edit to the prose.
  0011's format is untouched: criteria may still cite units by name.
- **`depends_on` is optional; a unit names the units before it.**
  New diagnostics, firing in both profiles: TC013 duplicate `id`,
  TC014 a `depends_on` entry naming no unit in this contract, TC015
  a cycle, its message naming the ring. Isolated units are valid -
  parallel work is the point - so there is no connectivity check. A
  cycle is malformed at draft too, not only at ready.
- **Graph validity is a Python-side ready check**, recorded as such
  in the schema description, mirroring 0017's `entities` join. The
  schema declares the fields; the checker decides the graph.
- **The render is computed, never stored.** No `.mmd` file enters
  the tree. This follows 0017 V5, which denies `vocab-list` a stored
  index precisely so nothing can drift, and it drops a `--check`
  drift mode, a new CI step, and an entire drift class from the
  work. The graph is a function of the contract; storing it would
  manufacture a second truth and then demand new machinery to police
  the gap between them. Review of the picture is served at intake,
  where the decision is actually taken.
- **Execution state lives at `.sdlc/progress/<id>.yaml`, never under
  `specs/`.** Ruled here so nobody later reaches for the contract.
  Building it is out of scope for `unit-dag`; progress is disposable
  local state and never a gate input.
- **The id migration is a lawful class-S delta, not a write-surface
  violation.** 0010 protects `specs/**` by channel, not by author:
  class-S deltas ride spec-channel candidates. This migration is
  spec-channel work carried by the `unit-dag` contract itself, and
  it is mechanically distinguishable from tampering because the diff
  adds `id` lines and nothing else - no intent, scope, `done_means`,
  or acceptance text moves. G4.6 reads the diff, so the audit sees
  the same evidence a human does.
- **The G0.1 check text tightens under 0014's full lane.** The row
  moves from "every unit sketched" to "every unit identified and
  ordered (acyclic, resolvable)". The delta is class E and the
  direction is tightening, which would auto-approve once a
  classifier exists; absent one, the human principal approves and
  the pull merge is the approval record, the interim convention
  already used for vocabulary ratification. The edit is carried as
  its own decomposition unit so the answer is recorded against it
  rather than buried in a mixed commit.

Recorded non-goals: no scheduling, estimates, durations, or critical
path - the graph records order, never time. No cross-contract edges;
the `dependencies` field stays separate and unchanged. No execution
semantics - the graph never runs a unit.

## Consequences

- Schema 1.2.0 is breaking for any consumer authoring contracts
  against 1.1.0. The one outside consumer pins v0.10.0 and is
  undisturbed until it re-pins, so the break is paid entirely
  in-repo and at the cheapest moment available.
- The contract that introduces ordering cannot declare its own.
  `additionalProperties: false` makes `id` a TC005 until the schema
  unit ships, so `unit-dag`'s units gain ids inside the migration
  unit it defines. Every later contract is born with ids.
- `/sdlc intake` gains a render-and-confirm step between drafting the
  decomposition and writing it. G0.1's definition-of-ready grows a
  condition that is checkable rather than advisory.
- Refusing the committed render means the graph cannot be reviewed
  as a file diff in a pull request. Accepted: a Mermaid diff is read
  as a picture, not as text, and the picture is presented at intake
  where the ordering decision is actually made.
- The suite grows by roughly ten tests (190 -> ~200): cycle shapes at
  one, two, and three units; a dangling reference; a duplicate id; an
  isolated unit; a valid diamond rendering identically across runs.
