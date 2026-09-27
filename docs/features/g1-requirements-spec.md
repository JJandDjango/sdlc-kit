| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-09-27 | user | r1: Created in kit session 58 through an interview with the user, one question at a time, in the format ADR 0029 ratified and ADR 0033 amended; typed by Claude on the user's word. The request half, in progress. PO seat: user; engineer seat: user |
| 2026-09-27 | user | r2: Measured: ADR 0033's checks before signing, on the request half, run by Claude on the user's word: no new term clashes with a ratified term; `component` and `venue` trip CL003, and the dictionary cedes both at intake; lang-check's contract rules find 86 in the text intake copies (76 unknown words, 10 sentences over the cap), each left to intake's rewrite of the contract's wording |
| 2026-09-27 | user | r3: The request half finished in kit session 58: the terms (Q9), ADR 0033's checks before signing (r2), ready checks 1 to 8 read back with two fixes (message 5 for SC1.2; SC1.1's review tied to the revision its contract was derived from); typed by Claude on the user's word. Signed by the PO seat (user) |

# g1-requirements-spec - Failure points found before development starts

`sdlc_development_kit` · seats: PO user, engineer user · contract:
`g1-requirements-spec`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As a developer, I want a requirements/spec gate, so that I can know as
soon as possible the failure points that need to be addressed before
development starts: in the requirements themselves, in boundary schemas,
and in a hard core's design.

## Description

`[PO seat · authored]`

Today nothing checks a feature document's requirements before
development starts, so their failure points surface during the build or
after it ships. Three cases:

- project-tree's document was ready at r3, and its build still asked me
  12 questions about content that r3 could have settled. The gaps cost
  three Two-Key FAILs (o4, o5 and o7, each at round 1) and a drafter
  stopped past 400K tokens (ADR 0033).
- The pilot's M0 document says in its intent that the engine selects the
  RT-capable device, and in SC3.2 that it prefers one. Both wordings
  stand in the ready document (the engine's `PILOT-NOTES.md`).
- After project-tree shipped in kit 0.16.0, the pane's top item reads
  `gates/G0 Planning / Intake [to do] (3 items: 3 to do)`, although G0 is
  finished on the kit's 15 features done. The document never said what that
  line's status comes from: it holds only the findings filed against G0,
  so with none filed it reads `to do` whatever each feature's own G0
  verdict reads.

With G1, failure points like these are found before development starts,
and the document is fixed before any code is written.

## Background

`[PO seat · authored]`

The kit defines G1, Requirements / Spec, on its page
(`docs/gates/G1-requirements-spec.md`). Its three conditions were ratified
on 2026-07-23, and none is built:

- G1.1 Spec/schema linting: every boundary schema and spec file lints
  clean under Spectral (OpenAPI, JSON Schema) or `buf lint` (protobuf);
  warnings block.
- G1.2 Model checking: every component designated a hard core (ADR 0007)
  has a formal model that TLC or the P checker passes before
  implementation.
- G1.3 Criteria completeness + ambiguity review: a person attests each
  item of an 11-item checklist; an unchecked item returns the document
  with that item named.

Measured on the kit at `af8c261`, 2026-09-27: `.sdlc/config.yaml`
activates G0 alone, and the tree shows each feature's G1 marked inactive
after its G0, with its three conditions `to do`. Intake's last step (I9,
`skills/sdlc/flows/intake.md:33`) reports the contract ready-green and
says "Development starts only from green", naming no next step; the pilot
filed this as `intake-exit-names-no-successor-venue` (2026-09-20, kit
0.13.0). The feature document's ready checks, 1 to 14, already ask part
of G1.3's checklist in the interview and at intake (ADRs 0029 and 0033).
The pilot's M0 code waits for G1's review (the engine's `plan.md`).

### Existing behavior touched

Each entry gets a regression check under Acceptance criteria.

1. Intake's last step reports the contract's path, its state, the seats
   recorded and a one-line scope summary (I9).
2. Each contract's G0 verdict reads as the validator says: `done` at
   ready-green, `blocked` when draft-green with `TC003`, `to do` when
   draft-green otherwise, `failed` when draft-red.
3. The tree shows each feature's active gates, then the next gate in the
   kit's order marked inactive (project-tree SC2.1).
4. The feature document's ready checks 1 to 14 are asked in the
   interview, advisory there, and at intake, hard there (ADRs 0029 and
   0033).

## Success criteria

`[PO seat · authored]`

1. SC1: Before development starts, each feature's requirements are
   reviewed against G1.3's checklist, and each item left unchecked comes
   back to its document's seats.
2. SC2: Before development starts, every boundary schema a feature adds or
   changes lints clean, and a feature with none passes.
3. SC3: Before development starts, every hard core a feature touches has a
   model its checker passes, and a feature with none passes.
4. SC4: Intake's report names G1 as the next step, and a feature's
   development starts only once its G1 passes.
5. SC5: The tree shows each feature's G1 conditions with their status and
   their diagnostics.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added (the standing line).
- No new condition: G1 builds the three conditions its page ratified,
  and G1.3's 11 checklist items stay as ratified.
- No agent attests G1.3: an agent may draft the review, and only a
  person signs it.
- No bundled tools: the kit ships no linter or model checker; Spectral,
  `buf`, TLC and P are the consumer's to install and pin.
- No retroactive review: the 15 features already done get no G1 review,
  and their G1 reads inactive, as today.
- Not G2.5: the red run of the acceptance tests stays G2's, though the
  pilot's finding proposed it as intake's next step.
- Not the tree's `gates/G0` line: its status stays as it reads today.

## Prerequisites

`[PO seat · authored]`

1. G1's page, its three conditions and G1.3's 11-item checklist (exist:
   `docs/gates/G1-requirements-spec.md`).
2. G1's conditions in the kit's gate list, and the tree's condition items
   (exist: `taskcontract/data/gates.yaml`, kit 0.16.0).
3. The hard-core designation criteria (exist: ADR 0007).
4. A record of which components are hard cores and each component's
   oracle designation, the component declaration record G1.3's item 11
   reviews (missing: the G1 page defers where it lives; owner: this
   feature).
5. A record of each G1.3 review: who signed which revision, and what it
   found (missing: the G1 page defers its form and storage; owner: this
   feature).
6. The rules behind each G1 condition, so each takes its status from its
   own rules (missing: only G0's conditions list rules; owner: this
   feature).
7. A venue for G1 between intake and the first unit's test list
   (missing: the pilot's finding says none is bound; owner: this
   feature).
8. Spectral at the kit, to lint its four JSON Schemas under
   `taskcontract/schemas/` (missing: not installed; Node, which it runs
   on, exists; owner: the kit session). `buf`, TLC and P are not needed at
   the kit today: it holds no protobuf file and no hard core.
9. The pilot pins a kit release carrying G1 (missing; owner: the engine
   session).
10. A person to sign G1.3 (exists: the user, holding both seats).

## Acceptance criteria

`[PO seat · authored]`

### Checks

Three checks under each success criterion. SC4.1, SC4.3, SC5.2 and SC1.3
carry the regression checks for Existing behavior touched, entries 1 to 4
in that order.

SC1 The G1.3 review

- SC1.1: verify the review asks each of G1.3's 11 items against the
  feature's document, and a named person signs it on the revision its
  contract was derived from
- SC1.2: verify each unchecked item shows as a diagnostic under G1.3,
  naming the item and the document's section it concerns, and G1.3 reads
  failed until a later revision's review passes
- SC1.3: verify ready checks 1 to 14 are still asked in the interview and
  at intake as today, and the review does not ask them again

SC2 Schema linting

- SC2.1: verify every JSON Schema, OpenAPI or protobuf file the feature
  adds or changes lints under the repository's pinned ruleset, and a
  warning fails G1.1 as an error does
- SC2.2: verify a feature that adds or changes no boundary schema passes
  G1.1 without running a linter
- SC2.3: verify a linter the repository has not installed fails G1.1 with
  its message under Error messages, rather than passing

SC3 Model checking

- SC3.1: verify every hard core in the component declaration record whose
  paths fall within the feature's scope has a model that TLC or P passes
  under its pinned configuration
- SC3.2: verify a feature whose scope holds no hard core passes G1.2
  without running a checker
- SC3.3: verify a hard core with no model, or with its checker not
  installed, fails G1.2 with its message under Error messages

SC4 G1 before development

- SC4.1: verify intake's report names G1 as the next step, after the
  contract's path, state, seats and scope summary as today
- SC4.2: verify no unit's task can be recorded as started while its
  feature's G1 has not passed, and the refusal prints its message under
  Error messages
- SC4.3: verify each contract's G0 verdict still reads as the validator
  says: done at ready-green, blocked when draft-green with TC003, to do
  when draft-green otherwise, failed when draft-red

SC5 The tree

- SC5.1: verify a feature past G0 shows G1 active, with G1.1, G1.2 and
  G1.3 each taking its status from its own rules, and a condition that is
  not done lists its diagnostics
- SC5.2: verify the 15 features already done show G1 inactive, as today,
  and the tree still marks the next gate after the active ones inactive
- SC5.3: verify G1's status is the roll-up of its three conditions, and a
  signed G1.3 review shows its seat and revision

### Error messages, verbatim

Five new messages:

1. `G1.1: {tool} is not installed; install it and pin it in the repository` (SC2.3)
2. `G1.2: hard core {component} has no model` (SC3.3)
3. `G1.2: {tool} is not installed; install it and pin it in the repository` (SC3.3)
4. `{unit} cannot start: G1 has not passed for {feature}` (SC4.2)
5. `G1.3: item {n} {item} is unchecked in {section}` (SC1.2), such as
   `G1.3: item 6 Consistent is unchecked in Statement`

Every message the kit prints today stays word for word.

---

## Decisions and open questions

`[Both seats · authored]`

- Q: The feature's id? A: `g1-requirements-spec`, matching
  `g0-declaration` and the gate's page (decided 2026-09-27).
- Q: Which failure points? A: All three: in the requirements themselves,
  in boundary schemas and in a hard core's design (Q2, decided
  2026-09-27).
- Q: Is the tree's `gates/G0` line a bug? A: A gap in project-tree's
  requirements, not a code fault; a non-goal here, and on the kit's
  deferred list (Q3, decided 2026-09-27).
- Q: May an agent sign G1.3? A: No: an agent may draft the review, and
  only a person signs it (Q6, decided 2026-09-27).
- Q: Do the features already done get a G1 review? A: No: their G1 reads
  inactive (Q6, decided 2026-09-27).
- Q: What does an unchecked review item show as? A: A diagnostic under
  G1.3; Finding keeps its ratified meaning, an observation about the kit
  (Q9, decided 2026-09-27).
- Q: What are G1's rules? A: Tests the kit's validator applies, with
  codes, as the ratified Rule says: they read the recorded lint result,
  model-check result and signed review (Q9, decided 2026-09-27).
- Q: "Ready check" or a new name? A: Ready check, its own two-word term;
  the ratified Check stays an acceptance line such as SC1.1 (Q9, decided
  2026-09-27).
- Q: Does a review still count after the document changes? A: No: a
  review counts on the revision its contract was derived from, so a later
  revision needs a new one (SC1.1, decided 2026-09-27).
- Q: Do the checks before signing read green? A: No, and each finding is
  answered: `component` and `venue` are ceded by the dictionary at intake;
  the 86 language findings in the statement, the non-goals and the checks
  are answered by intake's rewrite of the contract's wording, and this
  document keeps the PO seat's words (r2, decided 2026-09-27).

## Appendix

### Terms

`[PO seat · authored]`

Decided at the interview's Q9 (2026-09-27). Fifteen map to the kit's
ratified terms: Feature, Feature document, Gate, Active gate, Condition,
Rule, Diagnostic, Verdict, Finding (the pilot's), Unit
(`decomposition-unit`), Task, Check (`acceptance-sketch`), Seat
(`intake-seat`, by its alias), Tree and Status. The rest become terms to
ratify at intake.

- Failure point: anything in a feature's requirements, boundary schemas
  or hard cores' designs that would fail development.
- Development: the work on a feature's units; it starts when its first
  unit's first task is recorded as started.
- Boundary schema: a file that fixes the shape of data crossing a service
  or trust boundary: JSON Schema, OpenAPI or protobuf.
- Hard core: a component whose defect would be concurrency- or
  protocol-shaped, invisible until late, and costly to reverse; all three
  hold (ADR 0007).
- Model: a formal description of a hard core's design, in TLA+ or P.
- Linter: the tool that lints a boundary schema: Spectral or `buf lint`.
- Checker: the tool that explores a model: TLC or the P checker.
- Pin: a tool's version and settings, committed in the repository: a
  linter's ruleset, or a model's configuration.
- Component: a part of a consumer's system with its own paths.
- Component declaration record: each component's paths, whether it is a
  hard core, and its oracle designation.
- Oracle designation: how a component's generated inputs are judged:
  differential, fuzz, property-only, concurrency, soak, or none with a
  reason.
- Review: a person's pass over G1.3's 11 items against a feature
  document at one revision, signed with the seat and revision.
- Venue: where and when a gate runs.
- Ready check: one of the 14 questions a feature document answers before
  intake reads it ready (ADRs 0029 and 0033).
- Two-Key: the independent verifier's grade of one unit, PASS or FAIL.
