# 30. A door's input is a declaration, not an option

Status: accepted
Date: 2026-09-20

## Context

The pilot consumer (ImSimEngine, session 8, against kit `5e26c1b`) measured
G0 and found two of its three conditions passing on nothing. G0.2's coverage
join (0017) reads `entities` and returns empty when the field is absent; its
one contract validated ready with no field while its prose named six terms of
a glossary that held fifteen, none ratified. G0.3's confirmation join (0025)
arms only on a ratified `intake-seat`; with the term at draft, stamping every
unit `nobody-at-all` also passed. After the consumer's human work the same
contract passes with six resolved references and five units checked against
a two-seat roster, and no condition changed. The conditions are right; each
reads an optional input, so the gate reports one word, ready-green, whether
it examined everything or nothing. The kit shows the same shape: eleven of
its twelve contracts declare `entities`, and `vocabulary-layer` validates
ready without it. Bound by the eight fields and the ready profile (0005,
0006), the write surface (0010), enforcement change control (0014), the
vocabulary layer (0017), and intake seats (0025). The request is
`REQUEST_g0-declaration_2026-09-20.md`, signed by both seats at r3.

Alternatives weighed and rejected: the consumer finding's converse check (a
glossary term in a contract's prose must be declared), which needs a matcher
and a threshold, and stays filed; both requirements in the join code, which
leaves a contract validated outside a specs tree free to skip `entities`; a
default `entities: []` in the scaffold, which restores silence by default; an
exemption list for contracts written before the door, unneeded because the
write-guard's exemption is dynamic; a warning when `[]` stands beside
ratified terms, which fires on every legitimate infrastructure contract.

## Decision

- **At the ready profile, the input a door reads is a required
  declaration.** One principle, applied twice. Neither application invents a
  check; each gives an existing check something it cannot dodge. The draft
  profile is unchanged, so a parked contract may carry neither.
- **G0.2: `entities` is required at ready, and the empty list is valid.**
  The schema's `ready_delta` requires the field; the base drops
  `minItems: 1`, so `entities: []` is a positive statement that the contract
  operates on no glossary term. The miss is TC017. Living in the schema, the
  requirement reaches a contract validated outside a specs tree too.
- **G0.3: a ratified seat roster is required at ready.** Inside a specs
  tree, `confirmation_join` returns TC018 for every contract when
  `intake-seat` is absent or not ratified, in two wordings that say which,
  each naming the file to author. With the roster ratified, behavior is
  today's.
- **The kit's flows move with the door.** Intake checks the roster before
  authoring and stops with one line when none is ratified; it always writes
  `entities`, and writes `[]` only on the PO seat's confirmed answer.
  Greenfield init asks who holds the seats and seeds the term; brownfield
  init reports the need. The scaffold names the field in a comment and sets
  no value.
- **Adoption is an edit, not a re-intake.** A contract the new door fails
  stops validating ready, so the write-guard's dynamic exemption opens it to
  the edit that repairs it, and it locks again once it passes. USAGE says
  so. The kit runs this path on its own `vocabulary-layer` contract.
- **Lanes under 0014.** Two tightenings ride the auto lane: `entities`
  required at ready, and TC018. Three deltas took the full lane and were
  approved by the human principal on 2026-09-20: the `minItems` removal
  (field-wise a loosening: `entities: []`, rejected today, becomes valid at
  both profiles; without it a contract with no terms could not meet the
  requirement at all), the three prompt files (`intake.md`, `init.md`,
  `new.md`; prompts have no field-wise direction), and the ready fixtures
  that gain the field (edits toward green). The ledger and classifier are
  unbuilt; this ADR and the merge approval are the record.
- **Schema 1.4.0, kit 0.14.0.** The CHANGELOG delta note names both
  diagnostics and their remedies.

Recorded non-goals: no prose-to-registry matcher; no change to what
ratification means or who may ratify; no new gate and no new condition; no
seat map and no authorship check (0025's line holds); no opinion about which
terms a consumer ratifies; no change to the write-guard.

## Consequences

- Green at G0 means every condition checked something: a ready contract
  states its terms, even when the statement is "none", and every unit's
  answerer is on a ratified roster.
- Closing the roster gap also closes the consumer finding
  `intake-write-locks-its-own-confirmation`: that trap springs only when an
  authored contract validates ready without confirmation, which can no
  longer happen.
- A consumer on an unpinned install turns red at upgrade until it declares
  `entities` and ratifies a roster; both remedies take minutes and are named
  in the diagnostics. The pilot already passes.
- `entities: []` is the new place to say nothing. Intake's confirmed answer
  is the guard today; the converse check stays filed as the next step if the
  empty list is abused.
- Adoption depends on the write-guard's exemption staying dynamic; the
  request's SC5 tests pin it, so a later change to the guard must keep them
  green. The guard's own gap (shell writes pass it) waits for its request.
