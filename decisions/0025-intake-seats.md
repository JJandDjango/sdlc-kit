# 25. Intake seats and unit confirmation

Status: accepted
Date: 2026-08-26

## Context

Session-27 walk of Phase 0 for a consumer with two human teams (a PO
team and an engineer team). The intake venue takes a human answer for
every unit before the contract lands (0024's render-and-confirm step,
approved, unlanded), but nothing records who answered: the answer
lives in chat, and the PR merge records approval of the whole
contract, not of a unit. Who holds which contract field is a proposal
in working notes. The task contract is `specs/intake-seats/`.

Rulings already on record that bind the design:

- The human census is fixed at six (0015). No seventh human
  condition: the human act stays inside the existing `/sdlc intake`
  venue; whatever G0 gains must be mechanical.
- Vocabulary terms are per-repo artifacts; a `value-set` term carries
  a closed set; the join resolves ratified terms only, draft never
  resolves, and loose files stay schema-only (0017).
- Contracts are immutable to implementers by channel, not by author
  (0010); spec-channel deltas are lawful, and a mechanical migration
  that adds lines only is distinguishable from tampering in the diff
  (0024 precedent).
- Class-E deltas ride 0014's lanes; the direction classifier does not
  exist, so a tightening takes the human principal's approval with
  the pull merge as the record (0024 precedent).
- Execution state never lives under `specs/` (0024).
- The schema is `additionalProperties: false` at every `$def`, so a
  new unit field is TC005 until shipped (0024).
- Every skill prompt validates under PromptLang's 4000-token ceiling.
  Measured at the session-26 close: `skills/sdlc/SKILL.md` at ~3978;
  the approved confirm step lands it at 4149 in its approved wording
  and 4036 at maximal compression; only dropping the step passes.

Facts established at intake: TC016 is unused (TC000-TC015 are taken);
the census is 66 units across 10 contracts, 57 of them in the nine
contracts ratified before this task; and `intake-seats` cannot declare
its own confirmations until the schema unit ships, the same shape 0024
met with `id`.

## Decision

- **An intake seat is a vocabulary term, not a schema enum.** The
  seats a repo recognizes live at `specs/vocabulary/intake-seat.yaml`,
  kind `value-set`, one value per seat, ratified by the consumer's
  own flip (0017). The kit's own set has one value, `user`. The roster
  of humans is per-consumer, so a schema enum would turn every
  consumer's roster into a kit release; a term keeps it a class-S edit
  in the consumer's tree.
- **Every unit records who answered: `confirmed_by`, a unique list of
  seat values, at least one.** The field means: the seats whose
  answer for this unit was taken at intake. It is optional in the
  schema (1.2.0 -> 1.3.0, additive; no consumer breaks) and demanded
  by the door below.
- **G0.3 unit confirmation is a mechanical ready-profile check, armed
  by a ratified seat term.** When the sibling vocabulary carries
  `intake-seat` at `ratified`, every unit must carry `confirmed_by`
  and every value must be one of the term's values; otherwise TC016,
  its message naming the unit or the unknown seat. A draft term or no
  term leaves the check inactive (adoption pace, the vocab-check and
  lang-check precedent). The draft profile never runs it: a parked
  contract may lack answers. Loose files stay schema-only. This is not
  a seventh human condition: the human act is the existing I5 answer,
  and the gate checks the record of it.
- **Intake writes the record.** I5 becomes render the graph, take a
  human answer for every unit, write `confirmed_by` from the answers,
  then write the contract; a red door after the write reports the
  findings and returns. This lands 0024's render-and-confirm step, so
  `unit-dag`'s open unit `g0-intake-review` closes on the same edit.
- **The flows leave `SKILL.md`.** Each flow moves to its own file at
  `skills/sdlc/flows/<flow>.md` (init, new, intake, vocab, lang,
  audit, update); `SKILL.md` keeps dispatch, constraints, criteria,
  and one line per flow naming its file; every file validates under
  the same ceiling on its own. A one-time trim of the description
  buys about 200 tokens once; the confirm step and the write both
  queue on the wall now, and every later addition to the venue would
  too. The structural fix is taken instead of the trim.
- **The seat map is consumer policy, recorded in USAGE, never
  enforced.** The kit's default map for a PO team and an engineer
  team: the PO seat holds `intent`, `non_goals`, `provenance`, and
  domain-term ratification; the engineer seat holds `scope`,
  `decomposition`, `depends_on`, `dependencies`, and technical-term
  ratification; `acceptance_sketch` is answered by both; the agent
  authors the YAML and neither seat writes it. The door reads the
  answer, never the author: no check on who wrote a field exists or
  is planned.
- **The pull merge stays the outer record.** `confirmed_by` records
  the answer per unit; the merge records approval of the contract as
  a whole. Both are needed; neither replaces the other.
- **The migration is a lawful class-S delta** (0024 precedent). Every
  unit in every contract gains `confirmed_by: [user]` in one commit
  that adds lines and nothing else. The evidence for the value: each
  of those contracts entered through the intake venue with the user
  present, and its merge is on record.
- **The G0 roster grows from two conditions to three under 0014's full
  lane.** G0.3 joins the registry row and the deep page; the direction
  is tightening; the human principal approves and the pull merge is
  the record, carried as its own unit (`g0-3-row`) so the answer is
  recorded against it.

Recorded non-goals: no G1 artifact (the criteria record and the G4.3
join stay a separate task); no check on the author of a field; no
change to `entities` or `dependencies`; no work in a consumer repo (the
USAGE section names the consumer's steps, the consumer runs them); no
execution state.

## Consequences

- Schema 1.3.0 is additive: every 1.2.0 contract validates unchanged.
  Kit version 0.12.0. The one outside consumer, pinned at v0.10.0, is
  undisturbed.
- `intake-seats` cannot carry its own answers until `schema-1-3-0`
  ships, so its nine units gain `confirmed_by` inside the migration
  unit, as `unit-dag`'s units gained ids. Every later contract is born
  with answers, written by intake.
- A consumer with no ratified seat term pays nothing. One with a term
  pays one line per unit and gets a mechanical record of who answered,
  checked at the door and in CI.
- `SKILL.md` shrinks to dispatch; the flows become files beside it.
  Consumers are untouched: the skill rides the plugin and is never
  scaffolded into a repo, so `/sdlc update` has nothing to report.
- The suite grows by the door's cases: a unit with no `confirmed_by`,
  a seat the term lacks, a draft term leaving the check inactive, no
  term at all, the draft profile skipping it, a loose file skipping it.
- USAGE gains the two-team section, authored red at pass zero and
  flipped green as the units land.
- The `unit-dag` contract closes: its last open unit is satisfied by
  `g0-confirm-write`.
