# 33. The solution half names sources, examples and retirements

Status: accepted
Date: 2026-09-27

## Context

ADR 0029 fixed the feature document's format and its definition of done.
project-tree was the first feature written to it: ready at r3, then built
in sessions 51 to 56, where the user made 43 decisions. 26 were process by
design (plans, delegation, commits, pushes, merges, the tag). Of the 17
about content, 12 answered questions r3 could have settled, and the gaps
cost three Two-Key FAILs (o4, o5 and o7, each at round 1) and a drafter
stopped past 400K tokens (o6). Every gap sat below the line; the request
half held. The format told the engineer seat what to decide (scope,
interfaces, units) but not where each fact comes from and which source
wins, what each output looks like at its edges, or what each unit takes
away. The post-mortem and its evidence are in
`NOTES_feature-document-amendment_2026-09-27.md`, ratified call by call in
session 57. Bound by the format and its tags (0029), seats (0025) and no
headings read by the tooling (0026, 0029). Alternatives weighed and
rejected: leaving these questions to rulings at each session's plan
review (the status quo, which produced the 12 rulings and the FAILs); a
size threshold on the split rule, such as "split when the retirement needs
its own drafting" (kept out: the rule as written matches the practice o6
taught); letting the engineer seat's signature stand as G0.3's unit
confirmation (a change to 0025's seats, not the format).

## Decision

- **Sources**, a new 13.4. A table: each fact the feature shows, stores or
  acts on; the field, file or record it reads; and where two sources can
  disagree, which one wins and when.
- **Examples**, under 13.3 Interfaces. Each output drawn literally, one
  per kind (a line, a response body, a screen), then its edges: the
  smallest size it must fit, the empty case, a missing or unreadable
  input, and each error. A test may pin an example word for word.
- **Retirements**, a field on each unit. What the unit removes, replaces
  or reverses: code, tests, user-facing text, and any earlier unit's test
  it flips; "none" when nothing. A unit that both adds behavior and
  retires old behavior splits in two.
- **Tests by check id.** A unit lists its tests by check id and kind:
  automated, or a manual receipt a person gives, such as a live run. This
  replaces 0029's "tests by kind or file"; a file name goes stale when a
  later unit moves the tests.
- **Order with its reason.** Each ordering in Sequencing names why; "any
  order" only when no unit changes a shape another unit's tests pin.
- **The checks, run before signing.** Before a seat signs its half, the
  interview runs on the draft each automated check that intake and the
  gates will run, and writes the result into the document: the terms
  through the vocabulary and language checks, Scope against the release
  unit's paths. A finding the seat cannot answer is an OPEN.
- **Four ready checks for the solution half**, advisory in the interview
  and hard at intake, as checks 1 to 8 are for the request half: (11)
  every fact a check names has a Sources row, and every pair of sources
  that can disagree names its winner; (12) every output kind has a drawn
  example, with its edges; (13) every unit names its retirements or
  "none", and lists its tests by check id and kind; (14) the checks run
  before signing read green, or each finding stands answered in the
  document.

This amends 0029: section 13 gains 13.4 Sources, and Constraints, Units
and Sequencing renumber to 13.5, 13.6 and 13.7. The format keeps eighteen
sections.

Recorded non-goals: no change to the seats (0025), so unit confirmation
at intake stays; no change to the process approvals, which the house rules
keep on the user's word; no tooling reads the new blocks, so checks 11 to
14 are asked, never parsed (0029).

## Consequences

- `feature-document` carries the change into the template, the
  interview's flow and the readiness check, which grows to fourteen rules
  plus the stale-stamp rule.
- The PO seat sees one change, the run of its terms before it signs; the
  other five sit with the engineer seat.
- A consumer without the kit runs the checks it has; call 6 names what to
  run, not a kit command.
- project-tree's document predates this ADR and stays as written.
- Harder: the engineer seat's half grows by three blocks. For a small
  feature, a one-row Sources table and "none" under Retirements are
  complete answers.
