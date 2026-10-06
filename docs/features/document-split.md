| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-06 | user | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: user; engineer seat: user |
| 2026-10-06 | user | r2: Measured: the checks before signing, on the request half: 179 findings (CL003 1, CL006 145, CL008 14, CL010 3, CL012 16); ready checks 1 to 8: 0 OPEN |
| 2026-10-06 | user | r3: The request half finished: 7 sections written, 0 OPEN |
| 2026-10-06 | user | r4: Signed: request half. The PO seat signs r3 |
| 2026-10-06 | user | r5: Measured: the checks before signing, on the solution half: 179 findings (CL003 1, CL006 145, CL008 14, CL010 3, CL012 16); Scope against the release unit's paths: covered; ready checks 11 to 14: 0 OPEN |
| 2026-10-06 | user | r6: The solution half finished: 8 sections written, 0 OPEN |
| 2026-10-06 | user | r7: Signed: solution half. The engineer seat signs r6 |

# document-split - Requirements and design stand in two documents, each signed by its own seat

`sdlc_development_kit` · seats: PO user, engineer user · contract: `document-split`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As an engineer who holds the engineer seat alone, I want a feature's
request and its design in two documents, each signed by its own seat, so
that the PO team signs only text it reads and a design is ready to build
on one engineer's signature.

## Description

`[PO seat · authored]`

A feature's request and its design become two documents. The
requirements document holds what the PO seat signs: the statement, the
description, the background, the success criteria, the non-goals, the
prerequisites and the acceptance criteria. It holds no scope, unit or
interface. The design document holds what the engineer seat signs: the
proposed solution, and the risks and cost. One engineer writes and signs
it alone, in a later interview run that starts from a signed
requirements document.

The design document names the requirements revision it was written
against, so a later change to the requirements shows as a stale design,
before the signature and again at intake. It also answers the four cases
in which the engineer asks another engineer before the PR, and a yes
names who was asked and what was decided. Intake takes the pair and
writes one contract. The Google Docs form renders each document on its
own, so the PO team receives the requirements document alone. A combined
document that intake has already read stays as the record of its
feature.

## Background

`[PO seat · authored]`

Kit 0.18.0 asks a PO team and an engineering team to write one feature
document together and to sign a half each. The first team to use it
outside this repo answered on 2026-10-05 that this is not the process it
wants:

1. The request and the design do not belong in one document. The PO
   team reads what the request looks like, never the design or the
   implementation.
2. Every engineer seat item goes into its own design document.
3. One engineer writes and reads the design document. A second
   engineer's review of a design before the PR is held to double the PR
   review time.

The lifecycle that team asked for:

1. The engineer and the PO team write a requirements document.
2. The engineer alone writes a design document.
3. Claude implements the design document.
4. The engineer reviews Claude's PR.
5. Another engineer gives the final PR review.

Before the PR, the engineer asks another engineer only in four cases:

1. to clarify an ambiguity;
2. when there is more than one solution;
3. when the solution is unconventional to the codebase;
4. when the solution changes a public contract (routes, a gateway
   definition, events, a schema).

Why now: the user's own work runs through that lifecycle, and G1's
document (`docs/features/g1-requirements-spec.md`) would otherwise take
its solution half in the format this feature replaces.

### Existing behavior touched

Each entry gets a regression check under Acceptance criteria.

1. One document per feature holds both halves: the request half above a
   `---` line and the solution half below it
   (`skills/product-specification-interview/templates/feature-document.md.template:89`).
2. Each seat signs its half in its own `Signed:` row (ADR 0034;
   `skills/product-specification-interview/SKILL.md:81`).
3. One interview writes both halves into the one document, and one state
   file holds the run
   (`skills/product-specification-interview/SKILL.md:36`).
4. With no engineer seat, the interview skips the solution half and its
   signature (`skills/product-specification-interview/flows/solution.md:41`).
5. Intake reads one document. It derives the contract from the newest
   revision both seats signed, and it stops, with no row and no
   contract, when a half has no signature
   (`skills/sdlc/flows/intake.md:23`).
6. Intake writes its `Ready:` or `Parked:` row into that one document's
   revision table (`skills/sdlc/flows/intake.md:22`).
7. The tree shows each `.md` file directly under `docs/features/` as one
   feature before intake, and reads a feature's document at
   `docs/features/<id>.md` (`taskcontract/tree.py:27`, `:929`).
8. `lang-check --draft` reads the run's one state file for both halves:
   the statement, the non-goals, the checks and the terms at P1, and
   each unit's `done_means` at E1
   (`skills/product-specification-interview/flows/signing.md:49`, `:71`).
9. The Google Docs form shows the whole document
   (`skills/product-specification-interview/flows/output.md:17`).

## Success criteria

`[PO seat · authored]`

1. SC1: A feature's request and its design stand in two documents: the
   requirements document holds the PO seat's sections alone, and the
   design document holds the engineer seat's sections alone.
2. SC2: Each document is written in its own interview run and signed by
   its own seat: the requirements run asks nothing of an engineer seat,
   and the design run starts from a signed requirements document and
   asks nothing of a PO seat.
3. SC3: A design document names the requirements revision it was written
   against, and a requirements change after that revision makes the
   design read stale, both before the engineer seat signs and at intake.
4. SC4: Intake writes one contract from a pair whose two signatures
   stand and whose design is not stale, and writes none from anything
   else.
5. SC5: A design document answers each of the four cases, a yes names
   who was asked and what was decided, and a missing answer is reported
   before the engineer seat signs.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added (the standing line).
- No computed fourth case: no config list of public contract paths is
  checked against the design's Scope. Moved to a later feature.
- No review of the design by Claude in a fresh context before the
  engineer seat signs. Moved to a later feature.
- No PR brief generated from the design document for the final reviewer.
  Moved to a later feature.
- No second engineer signs or reviews the design document before the PR.
- No command splits a combined document: G1's is split by hand.
- No section of either half is reworded, reordered or dropped. The
  design document gains only the named revision and the four cases.

## Prerequisites

`[PO seat · authored]`

- Kit 0.18.0, the interview and intake this feature changes: exists
  (`v0.18.0`).
- An ADR that amends ADR 0029 and ADRs 0033 to 0036 for the pair: does
  not exist; the user ratifies it before intake.
- The terms `requirements document` and `design document`, ratified: do
  not exist; the user ratifies them before intake, in their own commit.
- G1's document (`docs/features/g1-requirements-spec.md`) with its
  signed request half: exists.

## Acceptance criteria

`[PO seat · authored]`

### Checks

Three checks under SC1, SC2 and SC4, two under SC3 and SC5. The
regression checks for Existing behavior touched: entry 1 in SC1.1 and
SC1.2; 2 and 8 in SC2.3; 3 in SC2.1 and SC2.2; 4 in SC2.1; 5 in SC4.1
and SC4.2; 6 in SC4.1; 7 in SC1.3; 9 in SC1.2.

SC1 Two documents

- SC1.1: verify a requirements run writes a requirements document that
  holds the request half's sections in the ratified order, each with its
  heading and tag as kit 0.18.0 writes them, then its own Decisions and
  open questions and Notes, and the Appendix's Gherkin and Terms blocks.
  It holds no Proposed solution, no Risks and cost, no Traceability and
  no Contract block. A bug fix's four sections stand in it
- SC1.2: verify a design run writes a design document that holds the
  requirements revision it was written against, the Proposed solution's
  seven sections in the ratified order, Risks and cost, the four cases,
  its own Decisions and open questions, Traceability, Notes and the
  Appendix's Contract block. It holds no section tagged for the PO seat.
  The Google Docs form of either document shows that document alone
- SC1.3: verify the tree shows a pair as one feature before intake, with
  each document's newest revision and its signature, and shows a
  combined document already through intake as it does today. A feature
  with a requirements document and no design document yet shows as one
  feature too

SC2 Two runs

- SC2.1: verify a requirements run asks for a PO seat and for no
  engineer seat, asks only the request half's steps, the Terms and the
  Gherkin, runs the checks before the PO seat signs, and ends at that
  signature by naming the design run as the next command. A pause
  resumes at the step its state names
- SC2.2: verify a design run starts only for a feature whose
  requirements document stands with the PO seat's signature on its
  newest text revision, and otherwise stops with its message and writes
  nothing. It asks for an engineer seat and for no PO seat, shows the
  engineer seat each place the PO seat refused at Non-goals, asks only
  the solution half's steps and the four cases, and resumes at the step
  its state names
- SC2.3: verify each seat's signature lands in its own document as a row
  `rN: Signed: request half` or `rN: Signed: solution half`, written
  right after the row it signs. The checks before each seat signs run on
  that seat's document and land there as a `Measured:` row. A design run
  changes no line of the requirements document

SC3 A stale design

- SC3.1: verify a design document names one requirements revision: the
  newest text revision of the requirements document when the engineer
  seat last confirmed the design against it. A design run that resumes
  on a newer requirements revision names the revisions between and asks
  the engineer seat to confirm the design against them. On that word the
  design names the newer revision in a text row, and the engineer seat
  is asked to sign again
- SC3.2: verify that when the requirements document holds a text
  revision newer than the one the design names, the checks before the
  engineer seat signs report the design stale with its message, and
  intake on that pair stops with the same message

SC4 Intake takes the pair

- SC4.1: verify intake, given a pair whose two signatures stand and
  whose design names the requirements' newest text revision, writes one
  contract: the statement, the non-goals, the checks and the terms from
  the requirements document, and the scope, the units and each
  `done_means` from the design document, word for word. Its `Ready:`
  row, or its `Parked:` row when a refusal stands in either document,
  lands in both revision tables
- SC4.2: verify intake stops, with no row and no contract, and reports
  which case holds: the requirements document has no PO signature on its
  newest text revision, the design document has no engineer signature on
  its newest text revision, or the design is stale
- SC4.3: verify intake, given a combined document that holds no `Ready:`
  row, stops with its message and writes nothing. A combined document
  that holds a `Ready:` row stays unchanged, and its contract validates
  as before. G1's document stands as a pair, with its request half's
  text and signature carried over unchanged

SC5 The four cases

- SC5.1: verify a design run asks the engineer seat the four cases one
  at a time (an ambiguity in the requirements; more than one solution; a
  solution unconventional to the codebase; a change to a public
  contract: routes, a gateway definition, events, a schema) and writes
  each answer into the design document as yes or no. A yes takes two
  more answers, who was asked and what was decided, and the document
  shows both
- SC5.2: verify the checks before the engineer seat signs report each
  case with no answer, and each yes that lacks who was asked or what was
  decided, as an OPEN with its message. The seat's word to sign still
  stands

### Error messages, verbatim

Six new messages:

1. `No requirements document for {id}. Run the requirements interview
   first.` (SC2.2)
2. `The requirements document is unsigned at r{n}. The PO seat signs
   before the design starts.` (SC2.2)
3. `The design names requirements r{n}; the requirements stand at r{m}.
   Stale.` (SC3.2, SC4.2)
4. `The requirements document has no PO signature on r{n}.` (SC4.2)
5. `The design document has no engineer signature on r{n}.` (SC4.2)
6. `{path} is a combined document with no Ready: row. Intake reads a
   pair.` (SC4.3)

Three new gaps under the kept shape `Ready check {n}: {gap}. Marked
OPEN.` (SC5.2):

7. `case {k} has no answer`
8. `case {k} reads yes and names no one asked`
9. `case {k} reads yes and names no decision`

Kept word for word: `Ready check {n}: {gap}. Marked OPEN.`; `r{n}:
Parked: {what stands}`; `{block} is stamped r{n}; the newest revision is
r{m}. Stale.`; and "A document already exists at {path}. Name another
path."

---

## Proposed solution

`[Engineer seat · authored]`

### Scope

- `skills/product-specification-interview/`: the skill, its flows and its
  templates: two runs, two skeletons, the four cases, the stale report
  (SC1.1, SC1.2, SC2.1 to SC2.3, SC3.1, SC3.2, SC5.1, SC5.2)
- `skills/sdlc/flows/intake.md`: the pair read, the three stops, the
  combined document's refusal, and the `Ready:` or `Parked:` row in both
  tables (SC3.2, SC4.1 to SC4.3)
- `skills/sdlc/SKILL.md`: its three sentences on intake's row and its
  stops (SC4.1, SC4.2)
- `taskcontract/tree.py`: a pair shows as one feature before intake
  (SC1.3)
- `taskcontract/tree_view.py`, `taskcontract/pane.py`: their docstrings'
  words on a half's file; no code
- `tests/`
- `USAGE.md`
- The release unit's: `pyproject.toml`, `skills/sdlc/init.py`
  (`KIT_VERSION`), `.github/workflows/sdlc.yml`

At intake, outside the build: prerequisite 2's ADR, and the nine terms
with the five amendments, the dictionary ceding `pair`. `CHANGELOG.md`,
`MAP.md`, `decisions/` and `docs/` are free paths: G1's document is split
by hand under `docs/features/`, and `docs/gates/G0-planning-intake.md`
takes one sentence.

### Out of scope

- The documents and contracts of features already through intake,
  `feature-document`, `project-tree` and `tree-first-level` among them
  (from the PO seat, confirmed). This feature's own combined document
  joins them: it takes its `Ready:` row from kit 0.18.0's intake.
- `taskcontract/lang.py`, `taskcontract/__main__.py`: `lang-check
  --draft` runs unchanged on either run's state file (no new flag, no
  second input)
- `taskcontract/checker.py`: the validator's rules, G0.3's among them (no
  rule on which seat confirms a unit)
- `taskcontract/schemas/task-contract.schema.json`: the contract's schema
  stays at 1.5.0
- `taskcontract/data/gates.yaml`: the gates and their conditions
- `taskcontract/progress.py`: the half ids `<id>/request` and
  `<id>/solution` and their refusals
- `skills/sdlc/flows/` other than `intake.md`

### Interfaces

One new argument, `design`; one new document and one new state file per
feature; one new section, Consult cases; one new ready check, 15; two
new tree marks. Each output is drawn on a feature `x`, PO seat ann,
engineer seat raj.

The files:

```
docs/features/x.md                  the requirements document, at the path a combined document held
docs/features/x.state.yaml          the requirements run's state file
docs/features/x.design.md           the design document
docs/features/x.design.state.yaml   the design run's state file
```

An id holds no dot, so `x.design.md` is never another feature's
document. Both state files keep `schema: spec-interview-state/2` and its
nine keys. The design run's adds `requirements_revision`; its `answers`
hold the solution half's keys, `cases`, and under `terms` a copy of the
new terms in the requirements document's Terms block, so the draft check
reads each `done_means` beside them.

The two runs:

```
/sdlc:product-specification-interview x          the requirements run: starts or resumes
/sdlc:product-specification-interview x design   the design run: starts or resumes
```

The requirements run asks O1 to O6 with the PO seat alone at O4, then Q1
to Q15 and P1 to P7. P7 hands over to W1, and W2 names the design run's
command. It writes `docs/features/x.md` from
`templates/requirements-document.md.template`.

The design run reads `docs/features/x.md` before it writes anything, and
stops on:

```
No requirements document for x. Run the requirements interview first.
The requirements document is unsigned at r3. The PO seat signs before the design starts.
```

The first when no file stands at the path; the second when no `Signed:
request half` row signs the newest text revision, here r3. Then it asks
O1 (the id, and no document at the design's path), O4 (the engineer seat
alone), O5 and O6. It asks no origin and no title: it reads both from
the requirements document. It writes `docs/features/x.design.md` from
`templates/design-document.md.template`, asks S1 to S12 and E1 to E7,
and W2 names `/sdlc intake docs/features/x.md`.

The design run reads, and never writes, the requirements document's
revision table, title line, Checks (S6's check ids) and Terms, and the
requirements run's state file for the places the PO seat refused at
Non-goals (S2).

The requirements document's first lines:

```
| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-07 | ann | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: ann |

# x - The outcome, in a few words

`repo` · seat: PO ann · contract: `x`, draft · PR: none · merge SHA: none
```

Then the request half's sections, each heading and tag as kit 0.18.0
writes them, a bug fix's four among them; then Decisions and open
questions and Notes, each tagged `[PO seat · authored]`; then the
Appendix with Gherkin and Terms. No `---` line.

The design document's first lines:

```
| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-08 | raj | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r3. Engineer seat: raj |

# x - The outcome, in a few words

`repo` · seat: engineer raj · requirements: `docs/features/x.md` · contract: `x`, draft · PR: none · merge SHA: none
```

Then Proposed solution with its seven sections, Risks and cost, Consult
cases, Decisions and open questions, Traceability (Links out, Record),
Notes, and the Appendix with Contract. Each authored section is tagged
`[Engineer seat · authored]`; Record and Contract keep `[Intake ·
derived]`.

Consult cases is asked at S9, one case at a time, after Risks and cost
(S8, the engineer seat alone). A yes takes two more answers. Decisions
and open questions, Links out and Notes move to S10, S11 and S12. State:
`answers.cases: [{case, answer, asked, decided}]`.

```
## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | no | | |
| 2. More than one solution | yes | lee | the retry lives in the client, not the gateway |
| 3. A solution unconventional to the codebase | no | | |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | no | | |
```

The design names one requirements revision: the `requirements r{m}` of
its newest text row that names one. r1 names it first. Every dispatch of
a design run, at any phase, reads the requirements document's newest
text revision, and on a newer one shows the revisions between and asks:

```
The design names requirements r3; the requirements stand at r5.
  r4: A non-goal added: no export to CSV
  r5: SC2.1 reworded
Confirm the design against r4 and r5?
```

On yes the design takes a text row, and a signed design is asked for its
signature again:

```
| 2026-10-10 | raj | r5: Confirmed against requirements r5 |
| 2026-10-10 | raj | r6: Signed: solution half. The engineer seat signs r5 |
```

On no, nothing is written, and E4 reports the design stale.

The checks before the engineer seat signs run on the design run's state
file and the design document:

```
$ python -m taskcontract lang-check --draft docs/features/x.design.state.yaml
docs/features/x.design.state.yaml: answers.units[u2]: CL008 sentence of 31 words exceeds the descriptive cap of 25
draft: 2 new terms, 0 amended; 0 non-goals; 0 checks; 3 units; 1 findings (CL008 1)
```

E3 reads ready checks 11 to 15. Check 15 asks: does each of the four
cases have an answer, and does each yes name who was asked and what was
decided? Its gaps, each marked under Consult cases as `OPEN: Ready check
15: case 2 has no answer.`:

```
Ready check 15: case 2 has no answer. Marked OPEN.
Ready check 15: case 2 reads yes and names no one asked. Marked OPEN.
Ready check 15: case 2 reads yes and names no decision. Marked OPEN.
```

E4 reports a stale design, and the seat's word to sign still stands:

```
The design names requirements r3; the requirements stand at r5. Stale.
```

The rows, each in its own document's table. The requirements
document's:

```
| 2026-10-07 | ann | r2: Measured: the checks before signing, on the request half: 4 findings (CL003 1, CL008 1, CL012 1, CL014 1); ready checks 1 to 8: 0 OPEN |
| 2026-10-07 | ann | r3: The request half finished: ... |
| 2026-10-07 | ann | r4: Signed: request half. The PO seat signs r3 |
| 2026-10-09 | intake | r5: Ready: contract `x` validates ready-green, derived from r3; the PO seat (ann) signed the request half at r3 (r4) |
```

The design document's:

```
| 2026-10-08 | raj | r2: Measured: the checks before signing, on the solution half: 1 findings (CL008 1); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-08 | raj | r3: The solution half finished: ... |
| 2026-10-08 | raj | r4: Signed: solution half. The engineer seat signs r3 |
| 2026-10-09 | intake | r5: Ready: contract `x` validates ready-green, derived from r3, against requirements r3; the engineer seat (raj) signed the solution half at r3 (r4) |
```

Intake takes the requirements document's path, `/sdlc intake
docs/features/x.md`, and finds the design document beside it. In I2's
order:

1. A combined document, one that holds a `## Proposed solution` heading,
   stops with nothing written. With no `Ready:` row:
   `docs/features/x.md is a combined document with no Ready: row. Intake
   reads a pair.` With one: `docs/features/x.md is a combined document
   through intake. Its contract stands.`
2. No design document stops with nothing written: `No design document
   for x. Run the design interview first.`
3. The refusals are read on both documents: an OPEN mark in either;
   ready checks 1 to 8 on the requirements document and 11 to 15 on the
   design document; a check of the requirements document in no unit, or
   in two, of the design document's Units. A refusal parks the pair: one
   `Parked:` row in each table, numbered in its own table, both holding
   the same list, the requirements document's things first. The row, the
   same in each table:

   ```
   | 2026-10-09 | intake | r5: Parked: Check SC2.3 is assigned to no unit. |
   ```

4. The stops are read only when nothing stands, and write no row and no
   contract. Each case that holds is reported, in this order:

   ```
   The requirements document has no PO signature on r5.
   The design document has no engineer signature on r5.
   The design names requirements r3; the requirements stand at r5. Stale.
   ```

5. The contract takes its `title` from the requirements document's title
   line; the statement, the non-goals, the checks and the terms from the
   requirements document; the scope, the units, each `done_means` word
   for word, the order and the tests from the design document. I5 stands
   as it is: each unit takes a human answer, and intake asks which seats
   answered.
6. Ready-green writes one `Ready:` row in each table, as drawn above.
   Each row's `derived from r{m}` names its own table's signed text
   revision.

The tree shows a pair before intake as one feature; `x.design.md` is
never a feature of its own. The feature line gains a second mark, the
design's newest text revision, and the solution half reads its signature
from the design document:

```
x The outcome, in a few words [doing] no contract: document r3 design r3 doc: docs/features/x.md
  x/request Request half [done] by ann at r3
  x/solution Solution half [done] by raj at r3

$ python -m taskcontract tree x/solution
x/solution Solution half [done] by raj at r3
file: docs/features/x.design.md:6
```

Edges:

- With no design document, a feature prints as kit 0.18.0 prints it: one
  mark, and the solution half from the document's own `Signed: solution
  half` row, else `[to do]`. Once a design document stands, its table
  alone gives the solution half.
- A design document with no text row: the mark reads `design: no
  revision table`. A design document with no requirements document
  beside it prints nothing.
- A pair through intake: the drift mark reads each table against that
  table's `Ready:` row. The design's reads `stale: design r5, contract
  from r3`, after the requirements document's mark. A combined document
  through intake prints byte for byte as today.
- Before intake the tree shows no mark for a stale design: the interview
  and intake report it.
- A design run on a combined document stops with nothing written:
  `docs/features/x.md is a combined document. Split it by hand, then run
  the design interview.`
- A document at the design's path with no design state file: "A document
  already exists at {path}. Name another path.", as for the requirements
  run.
- A thing the engineer seat will not build (S2): the design run writes
  it under the design's Decisions and open questions as `OPEN: a
  non-goal for the PO seat: {thing}`, and nothing in the requirements
  document. The PO seat adds it through a requirements run; the design
  run then confirms against the newer revision, and the engineer seat
  closes the mark.
- A requirements run on a finished state reports its paths and the
  design run's command, then offers the way back to a section: that
  section's step writes a text row, the checks run again, and the PO
  seat signs again.
- In a requirements run no step asks Decisions and open questions or
  Notes: each holds the material O5 confirmed, else "(none)".
- With no requirements state file (G1's), S2 shows no refused places and
  says so.
- The draft check on the design's state file reports the copied terms'
  findings again.
- The Google Docs form shows the run's own document alone, on request,
  and is written nowhere.
- G1's document holds no solution half, so it stands as a requirements
  document unchanged; its design document is opened beside it by a
  design run.

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| A feature's id and its two paths | the id the seat confirms at a run's opening; the paths are `docs/features/<id>.md` and `docs/features/<id>.design.md` | the requirements document's file name wins over the id in either title line, as the tree reads it (ADR 0035) |
| Which run is asked for | the command's second argument: `design`, or none | none |
| The title line | the PO seat's answer at the requirements run's opening, written as `# <id> - <title>`; a design run copies the requirements document's line | the requirements document's line wins: the tree and intake read it |
| A run's seat | the answer at that run's O4, in that run's state file's `seats`, written into its r1 and status line | the state file wins; a changed seat is a new answer and a text row |
| A feature or a bug fix | the requirements run's answer at O2; a design run reads it from the requirements document, which holds the four bug-fix sections or not | none: a design document's sections are the same for both |
| The ratified sections, their order and tags | the two templates, written from ADR 0029 as ADRs 0033 to 0036 and prerequisite 2's ADR amend it | the ADRs win: a template that disagrees is a bug |
| A section's text | that run's state file's answer, written into that run's document as its step closes | a hand edit found at resume goes to the seat, whose word decides; never silently |
| The step to resume at | that run's state file's `next` | the state file wins; a document never moves `next` |
| The newest text revision | the highest `rN` of a row that opens on none of `Ready:`, `Measured:`, `Signed:` or `Parked:`, in that document's own table | one rule, shared by the interview, intake and the tree; each table counts alone |
| A seat's signature | its document's latest `Signed:` row for its half; the signer from the row's Revised By cell; the revision is the newest text row above it | the latest row wins (ADR 0034); once a design document stands, its table alone gives the solution half |
| The requirements revision a design names | the `requirements r{m}` of the design table's newest text row that names one | the design's table wins over its state file's `requirements_revision` |
| The revisions between | the requirements table's text rows above the named revision | none |
| A stale design | the named revision against the requirements document's newest text revision | one rule and one message, shared by E4 and intake |
| The check ids | the requirements document's Checks | the document wins over either state file |
| The new terms the draft check reads at E1 | the requirements document's Terms block, copied into the design run's state file at its opening and at each confirmation | the requirements document wins |
| The places the PO seat refused | the requirements run's state file, `answers.out_of_scope` | none: with no state file none are shown |
| A consult case's answer | the design run's state file's `answers.cases`, written under Consult cases at S9 | ready check 15 reads the document; a hand edit goes to the seat |
| The checks' results before signing | `lang-check --draft`'s lines on that run's state file | the command wins; the `Measured:` row copies its last line |
| A ready check's result | the interview's reading of that seat's document against the questions in ADRs 0029 and 0033 and prerequisite 2's ADR | asked, never parsed; a seat's answer closes the OPEN |
| A combined document | a file at `docs/features/<id>.md` that holds a `## Proposed solution` heading | none |
| A feature through intake | for the tree, a contract at `specs/<id>/contract.yaml`; for intake's refusal of a combined document, a `Ready:` row in its table | none: each reader has one source |
| Each contract field | the statement, the non-goals, the checks and the terms from the requirements document; the scope, the units, the order and the tests from the design document | none: each field has one source |
| A unit's `done_means` | its row's Done means cell under the design document's Units, word for word | the document wins over any wording intake would derive |
| A check's unit | the Checks cell of its row under Units, where `+` joins two that share a sketch | none: a check in no row or in two is intake's refusal |
| An OPEN mark that parks | any `OPEN` in either document | Notes never carries one |
| The revision a contract was derived from | the `derived from r{m}` of the newest `Ready:` row, read in each table for that document | each table against its own row |
| The release unit's paths | the release unit's row under Units; the kit's are `pyproject.toml`, `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml` | the Units row wins |
| The kit's version | `pyproject.toml`'s `version` and `KIT_VERSION` | they must agree; a release moves both |
| What a machine installs | the `v0.19.0` tag, through the plugin and through `uv`, as USAGE's lines say | the tag wins over any branch |
| G1's request half | `docs/features/g1-requirements-spec.md` as it stands before the build | the file wins: the build changes no byte of it |
| That a combined document's contract still validates | `python -m taskcontract validate specs/*/contract.yaml --profile ready`, as CI runs it (`.github/workflows/sdlc.yml:23`) | the command wins |
| An entry of Existing behavior touched | the file or step the entry names | the source wins: an entry that no longer holds is an OPEN under ready check 6 |

### Constraints

1. Every prompt file the build touches (the interview's `SKILL.md` and
   its five flows, `skills/sdlc/flows/intake.md`, `skills/sdlc/SKILL.md`)
   passes `python -m prompt_lang`, keeps the PromptLang tag set, and
   stays under the 12,000-character ceiling its suites pin
   (`tests/test_skill_interview.py:32`, `tests/test_intake_flow.py:16`).
   `signing.md` stands at 10,802 and `intake.md` at 10,029, so each
   rewrite replaces sentences. A flow that still outgrows the ceiling
   splits by run into another flow file.
2. Every shell command a prompt file authors is one segment: no pipe,
   chain or redirect.
3. The skill stays prompt-only: its directory holds Markdown and the two
   templates, no code. The build adds no `taskcontract` command: a
   signature, a newest text revision and a stale design are read by the
   prompt, asked and never parsed. `signing.md` keeps its two Bash calls,
   and intake its four commands.
4. No tool reads a feature document's sections: `lang-check --draft`
   reads only a state file, and the tree only each document's revision
   table and the requirements document's title line, each file once per
   print.
5. A run writes only its own document and its own state file. A design
   run changes no line of the requirements document or of the
   requirements run's state file. The interview never writes a `Ready:`
   or `Parked:` row; intake writes those, one in each table, and never a
   `Signed:` row.
6. Intake keeps its nine steps, I1 to I9, and their order: the roster
   stop, the read, then the scaffold. The word `Signed:` stands in I2 and
   I7 alone.
7. Kept byte for byte: what `lang-check` prints, with `--draft` and
   without; what the tree prints for a feature with no design document,
   before intake and through it; the half ids `<id>/request` and
   `<id>/solution`, their plain names and their level; the row words
   `Signed: request half`, `Signed: solution half`, `Measured:`,
   `Parked:`, and `Ready:` through `derived from r{m}`.
8. No section of either half is reworded, reordered or dropped: the
   requirements template's headings and tags equal kit 0.18.0's for the
   request half, and the design template's seven sections and Risks and
   cost keep their headings and order.
9. The build changes no byte of `docs/features/feature-document.md`,
   `project-tree.md` or `tree-first-level.md`, the combined documents
   through intake, or of `docs/features/g1-requirements-spec.md`.
10. No new dependency, and the contract's schema stays at 1.5.0.

### Units

| Unit | Checks | Done means | Tests, by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| `d1-requirements` | SC1.1, SC2.1 | A requirements run writes a requirements document with the PO seat only, and names the design run after its signature. | one automated test per check | `templates/feature-document.md.template`, replaced by the requirements template (its solution half returns in d2's); O4's engineer seat question; P7's hand-over to S1; ready check 8's "both seats" and its `no engineer seat is named` OPEN; W2's intake command after a requirements run; the count "fifteen of the eighteen sections"; USAGE's 0.18.0 interview text, since this unit writes the new USAGE text first, under red marks; the tests that pin them, found by test-retirer (seen: `FEATURE_OUTLINE`, `TAGS`, `R1_CHANGES`, the three file-set tests, `test_sc2_2_no_engineer_seat_skips_the_solution_halfs_steps_checks_and_signature`, and the release suite's `BANNER`, `COUNT` and two red-mark tests) |
| `d2-design` | SC1.2, SC2.2, SC5.1 | A design run needs a requirements document with its signature, writes a design document that names its revision, and records each consult case. | one automated test per check | S1's branch for no engineer seat and S11's hand-over for it; "both seats answer S8"; S2's write into Non-goals and its PO signature; the span `S1-S11`, now S1 to S12; the tests that pin them, found by test-retirer (seen: `SOLUTION_STEPS`, `test_sc1_2_engineer_seat_decides_whether_the_solution_half_is_asked`, `test_sc1_3_solution_flows_purpose_agrees_with_the_step_both_seats_answer`) |
| `d3-signing` | SC2.3, SC3.1, SC5.2 | A design run writes its checks, each text revision and its signature into the design document, and marks a consult case with no answer OPEN. | one automated test per check; for SC2.3 also a manual receipt: a live run of both runs on a small feature in a scratch worktree, each seat signed in its own document, the requirements document unchanged by the design run | E6's way back into the request half; E7's move of the Gherkin stamp; E1's path to the one state file; the span "ready checks 11 to 14"; the tests that pin them, found by test-retirer (seen: `DRAFT_COMMAND`, `MEASURED_SOLUTION`, `test_sc2_2_ready_checks_11_to_14_stand_as_questions_before_the_engineer_seat_signs`, the two tests that draw one combined document for the tree) |
| `d4-tree` | SC1.3 | The tree shows a pair as one feature with each half's revision and signature, and marks a design document past its contract. | automated; also a manual receipt: `taskcontract tree` on d3's saved pair prints one feature with both marks and both signers | none |
| `d5-intake` | SC3.2+SC4.2, SC4.1 | Intake writes one contract from a pair, and stops on a missing signature or on a stale design. | one automated test per sketch; also two manual receipts, each a live intake run on d3's pair that ends in one turn: with a newer requirements text row it stops with the stale message and writes nothing; with one check left out of Units it writes a `Parked:` row in each table and no contract | intake's one r{m}, "the newest revision both seats signed", and its stop in free words; refusal 1's two "seat boundary" sentences; "intake's only write"; `skills/sdlc/SKILL.md`'s three one-row sentences; the tests that pin them, found by test-retirer (seen: nine in `tests/test_intake_refusals.py`, `test_intake_writes_the_ready_row_in_the_shape_the_tree_reads`, and the release suite's `PARKS`, `SIGNATURE_STOP`, `SECTION_8`, `STRATA_EXCEPTION`, `INTAKE_WRITES` and `INTAKE_CRITERION`) |
| `d6-release` | SC4.3 | Kit 0.19.0 ships the pair: intake stops on a combined document with no `Ready:` row, G1 stands as a pair, and USAGE reads green. | automated; also two manual receipts: a design run for `g1-requirements-spec`, run from the unit's commit through its opening, writes its design document as r1 against requirements r3; and after the tag, USAGE's `uv` line run with `python -P` reads 0.19.0 and the plugin at the tag holds the new flows | `KIT_VERSION` and `pyproject.toml` move to 0.19.0, and `sdlc.yml` after the tag; USAGE's red marks go green under the new banner; a `CHANGELOG.md` entry; `MAP.md`'s interview, intake and tree rows; `docs/gates/G0-planning-intake.md`'s title sentence; the tests that pin them, found by test-retirer (seen: the kit's own tree on G1, `tests/test_tree_halves.py:638`) |

### Order

`d1-requirements`, then `d2-design`, then `d3-signing`, then `d4-tree`,
then `d5-intake`, then `d6-release`. d1 lays down the requirements
skeleton and the hand-over a design run starts from, and writes USAGE's
new text first, under red marks. d2's run needs d1's signed requirements
document, and d3's checks need d2's design document; d3's live run needs
both runs asked. d4 is code alone, but its receipt reads d3's saved
pair, and d5's two receipts run intake on that pair. d5 leaves room
under intake's ceiling for d6's two refusals. d6 ships. No two units run
side by side: d1 to d3 each change the skill's file set or its
`SKILL.md`, which the others' tests pin.

## Risks and cost

`[Both seats · authored]`

Risks:

1. The final PR reviewer arrives without context.
2. One engineer who designs alone has blind spots.
3. The two documents drift: the design is written against one revision
   of the requirements, and the requirements change after it.
4. A signature, a newest text revision and a stale design are read by
   the prompt in three places: the design run's start, E4 and intake.
   Tests pin the words, never the reading, so two readers can differ.
   Sources gives them one rule, and the receipts are the only proof of
   behavior.
5. No live run takes intake to ready-green on a pair before the release:
   `d5`'s receipts end at a stop and at a park. The two `Ready:` rows
   are pinned as text; the first real run is G1's intake.
6. `signing.md` has 1,198 characters free under its ceiling and
   `intake.md` 1,971. A flow that splits by run adds a file to the
   dispatch and to the three file-set tests.
7. After `d5` the repo's own intake reads a pair, and this feature's
   document is combined. A re-intake during the build runs through the
   installed 0.18.0 plugin until the release.
8. A consumer's combined document with no `Ready:` row is refused from
   0.19.0 on. It is split by hand or finished under 0.18.0; the
   CHANGELOG's delta note says how.
9. The three edge messages and the design's drift mark stand under no
   check. They are pinned only where a drafter pins Interfaces, and the
   PO seat signed none of their words.
10. A design run copies the check ids and the new terms by reading the
    requirements document. A check renamed in a later requirements
    revision reaches the design only through the confirmation.

Cost: six units, one session each, as `feature-document`'s five were.
`d1` to `d3` and `d5` are prompt text with structural tests, `d4` is
code, `d6` the release. Four units take manual receipts; `d3`'s live run
of both runs is the long one, about 35 minutes as session 70's was.
Before the build, one session: prerequisite 2's ADR, the nine terms with
the five amendments, and intake.

Worth: the PO team receives and signs the requirements document alone; a
design is ready to build on one engineer's signature; and a design run
starts from a requirements document it did not write, so G1's design is
written through the interview, not by hand from two NOTES files.

## Decisions and open questions

`[Both seats · authored]`

- Q: One document or two? A: Two: a requirements document and a design
  document (the user, 2026-10-06, on the team's answer of 2026-10-05).
- Q: Which candidates stay in this feature? A: Candidates 1 to 9; the
  three under Non-goals move to later features (2026-10-06).
- Q: Before or after G1's solution half? A: Before: G1's solution half
  would otherwise be written in the format this feature replaces
  (2026-10-06).
- Q: Are any combined documents in flight in another repo? A: Not known:
  the user has not said (asked 2026-10-06). Either way they take no path
  here: a combined document with no `Ready:` row is split by hand or
  finished under kit 0.18.0, and the CHANGELOG's delta note says how
  (2026-10-06).
- Q: Which document carries each part of the record? A: Gherkin and
  Terms go with the requirements; Risks and cost, Traceability and the
  Contract block go with the design; each document keeps its own
  Decisions and open questions and its own Notes (SC1.1, SC1.2;
  2026-10-06).
- Q: Which document carries the four bug-fix sections? A: The
  requirements document (SC1.1; 2026-10-06).
- Q: What are the pair's file names and paths, and is there one state
  file or two? A: `docs/features/<id>.md` and
  `docs/features/<id>.design.md`, each with its own state file beside
  it. The requirements document keeps the combined document's path, so
  G1's file, intake's argument and the tree's `doc:` stay (Interfaces;
  2026-10-06).
- Q: Does "feature document" stay as a term? A: Yes, as the umbrella: a
  pair, or one combined document (Terms; 2026-10-06).
- Q: May a design run start on unsigned requirements? A: No: it stops
  with its message (SC2.2; 2026-10-06).
- Q: Does a stale design park or stop intake? A: It stops, like a
  missing signature, with no `Parked:` row (SC3.2, SC4.2; 2026-10-06).
- Q: Which document takes intake's row? A: Both (SC4.1; 2026-10-06).
- Q: With one engineer seat and no PO seat at the design run, which seat
  confirms each unit at intake (G0.3)? A: I5 stands as it is: intake
  asks which seats answered for each unit. The units come from the
  design document, so the engineer seat answers for them; the PO seat's
  word is still asked for an empty `entities`. No rule names a seat
  (2026-10-06).
- Q: Who does the engineer seat tell when one of the four cases turns to
  yes after the signature, during the build? A: The design document. The
  engineer seat goes back to Consult cases through the design run, which
  writes a text row and asks for the signature again; a re-intake then
  reads the pair. The kit tells no one else: the final reviewer reads
  the design document (2026-10-06).
- Q: How is a design run started? A: By the same skill with a second
  argument, `design`. Message 1 needs an explicit request, so the run is
  never guessed from the files (2026-10-06).
- Q: Where does a design name its requirements revision? A: In its
  revision table: r1, then each `Confirmed against requirements r{m}`
  row (SC1.2, SC3.1; 2026-10-06).
- Q: Which ready check holds the cases' gaps? A: A new one, 15, which
  prerequisite 2's ADR adds; ready check 8 then asks for the PO seat
  alone (SC5.2, SC2.1; 2026-10-06).
- Q: The request half gives no words for intake on a requirements
  document with no design document, for a design run on a combined
  document, or for intake on a combined document through intake. Reopen
  it? A: No: each is an edge under Interfaces with its own words, and
  the request half stays as signed. It is the first consult case, an
  ambiguity in the requirements; the user holds both seats and decided
  it (2026-10-06).
- Q: Does the tree mark a design newer than its contract? A: Yes, though
  no check asks: a combined document shows that drift today, and session
  72's re-intake was a design change (Interfaces; 2026-10-06).
- Q: Is G1's document a combined document? A: No: it holds no solution
  half. It stands unchanged as a requirements document, and `d6` opens
  its design document (SC4.3; 2026-10-06).
- Q: What becomes of a thing the engineer seat will not build? A: An
  open mark in the design's Decisions and open questions, for the PO
  seat to close; the design run writes nothing in the requirements
  document (SC2.3; 2026-10-06).
- Q: Does the build add a command that reads signatures and staleness?
  A: No: the prompt reads them, asked and never parsed (Constraints;
  2026-10-06).
- Q: Which unit ships the release, with no release check? A: `d6`, on
  SC4.3, as `tree-first-level`'s release unit took SC4.2 (2026-10-06).
- Q: 0.19.0 or 1.0.0? A: 0.19.0: the contract's schema does not change
  (2026-10-06).

## Traceability

### Links out

`[Both seats · authored]`

- `NOTES_document-split_2026-10-06.md`: the team's answer of 2026-10-05,
  the origin.
- `decisions/0029-feature-document-format-and-done.md` and ADRs 0033 to
  0036: the format prerequisite 2's ADR amends.
- `docs/features/feature-document.md`: kit 0.18.0's own document, the
  format this feature splits.
- `docs/features/g1-requirements-spec.md`: the first requirements
  document to take a design run.
- `docs/gates.md`: G1 and G2, which the two documents follow (Notes).
- `USAGE.md`, the interview's section and section 9: the pages `d1` and
  `d6` rewrite.
- PR #86: the request half, signed at r4.

### Record

`[Intake · derived]`

(none: intake writes the record)

## Notes

`[Both seats · authored]`

The gate list already separates the two subjects: G1, Requirements /
Spec (`docs/gates.md:129`), and G2, Design / Architecture
(`docs/gates.md:154`). A reading of the four cases against that list,
not a ruling: an ambiguity falls on G1.3 (criteria completeness and
ambiguity review); more than one solution and an unconventional solution
fall on G2.3 (significant design choices are recorded and reviewed); a
public contract change falls on G2.2 (breaking-change baseline lock).

For prerequisite 2's ADR, what this half asks it to carry: the two
templates and each document's sections; each section's one-seat tag; the
r1 rows and the status lines; ready check 8 for the PO seat alone and
the new ready check 15; the named revision and its `Confirmed against
requirements r{m}` row; one `Ready:` or `Parked:` row in each table; the
three edge messages.

For the term commit at intake: `seat-boundary` ("The line between the
request half and the solution half.") and `parked-document` rest on one
document and stand outside the five amendments
(`specs/vocabulary/seat-boundary.yaml:11`,
`specs/vocabulary/parked-document.yaml:11`). Consult cases is the
section's heading; Consult case is the term.

This document is the last one written combined. The draft check's
findings at E1 are left to intake's rewrite, as r2's 179 were.

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/document-split/contract.yaml`)

### Gherkin

`[PO seat · derived from r6]`

```gherkin
Scenario: SC1.1 A requirements run writes a requirements document
  Given a requirements run for a feature
  When the run writes its document
  Then it holds the request half's sections in the ratified order, each with its heading and tag as kit 0.18.0 writes them
  And it holds its own Decisions and open questions and Notes, and the Appendix's Gherkin and Terms blocks
  And it holds no Proposed solution, no Risks and cost, no Traceability and no Contract block
  And a bug fix's four sections stand in it

Scenario: SC1.2 A design run writes a design document
  Given a design run for a feature
  When the run writes its document
  Then it holds the requirements revision it was written against, the Proposed solution's seven sections in the ratified order, Risks and cost, the four cases, its own Decisions and open questions, Traceability, Notes and the Appendix's Contract block
  And it holds no section tagged for the PO seat
  And the Google Docs form of either document shows that document alone

Scenario: SC1.3 The tree shows a pair as one feature
  Given a pair before intake, a feature with a requirements document and no design document yet, and a combined document already through intake
  When the tree prints
  Then the pair shows as one feature before intake, with each document's newest revision and its signature
  And the feature with no design document yet shows as one feature too
  And the combined document shows as it does today

Scenario: SC2.1 A requirements run ends at the PO seat's signature
  Given a requirements run
  When it goes from its opening to the PO seat's signature
  Then it asks for a PO seat and for no engineer seat
  And it asks only the request half's steps, the Terms and the Gherkin
  And it runs the checks before the PO seat signs
  And it ends by naming the design run as the next command
  And a pause resumes at the step its state names

Scenario: SC2.2 A design run starts only on signed requirements
  Given a feature whose requirements document stands with the PO seat's signature on its newest text revision
  When a design run starts
  Then it asks for an engineer seat and for no PO seat
  And it shows the engineer seat each place the PO seat refused at Non-goals
  And it asks only the solution half's steps and the four cases
  And it resumes at the step its state names
  And for a feature without that signed requirements document, it stops with its message and writes nothing

Scenario: SC2.3 Each seat signs in its own document
  Given a pair written in two runs
  When each seat signs
  Then the signature lands in that seat's own document as a row "rN: Signed: request half" or "rN: Signed: solution half", written right after the row it signs
  And the checks before each seat signs run on that seat's document and land there as a "Measured:" row
  And the design run changes no line of the requirements document

Scenario: SC3.1 A design document names one requirements revision
  Given a design document that names the requirements' newest text revision at the engineer seat's last confirmation, and a requirements document that now holds a newer one
  When a design run resumes
  Then it names the revisions between and asks the engineer seat to confirm the design against them
  And on that word the design names the newer revision in a text row
  And the engineer seat is asked to sign again

Scenario: SC3.2 A stale design is reported
  Given a requirements document that holds a text revision newer than the one the design names
  When the checks before the engineer seat signs run, and when intake reads the pair
  Then the checks report the design stale with its message
  And intake stops with the same message

Scenario: SC4.1 Intake writes one contract from a pair
  Given a pair whose two signatures stand and whose design names the requirements' newest text revision
  When intake runs
  Then it writes one contract: the statement, the non-goals, the checks and the terms from the requirements document, and the scope, the units and each done_means from the design document, word for word
  And its "Ready:" row lands in both revision tables
  And when a refusal stands in either document, its "Parked:" row lands in both revision tables instead

Scenario: SC4.2 Intake stops on a missing signature or a stale design
  Given a pair in which the requirements document has no PO signature on its newest text revision, or the design document has no engineer signature on its newest text revision, or the design is stale
  When intake runs
  Then it stops with no row and no contract
  And it reports which case holds

Scenario: SC4.3 Intake refuses a combined document before intake
  Given a combined document that holds no "Ready:" row
  When intake runs on it
  Then it stops with its message and writes nothing
  And a combined document that holds a "Ready:" row stays unchanged, and its contract validates as before
  And G1's document stands as a pair, with its request half's text and signature carried over unchanged

Scenario: SC5.1 A design run asks the four cases
  Given a design run
  When it reaches the four cases
  Then it asks the engineer seat each case one at a time: an ambiguity in the requirements; more than one solution; a solution unconventional to the codebase; a change to a public contract (routes, a gateway definition, events, a schema)
  And it writes each answer into the design document as yes or no
  And a yes takes two more answers, who was asked and what was decided, and the document shows both

Scenario: SC5.2 A missing answer is an OPEN
  Given a design document with a case that has no answer, or a yes that lacks who was asked or what was decided
  When the checks before the engineer seat signs run
  Then each is reported as an OPEN with its message
  And the seat's word to sign still stands
```

### Terms

`[PO seat · authored]`

Decided at the interview's Q14 (2026-10-06). The document also uses the
kit's ratified terms Feature, Intake, Signature, Seat (`intake-seat`, by
its alias), Unit (`decomposition-unit`), Tree, Check, Checks before
signing, Measured row, OPEN (`open-mark`), Ready check, State file, Tag,
Scenario and Contract (`task-contract`).

Nine become terms to ratify at intake:

- Requirements document: the document of a feature that holds its
  request half and that the PO seat signs.
- Design document: the document of a feature that holds its solution
  half and that one engineer seat signs.
- Pair: a feature's requirements document and its design document, taken
  together.
- Combined document: a document in kit 0.18.0's format, with both halves
  in one file.
- Requirements run: an interview run that writes a requirements
  document.
- Design run: an interview run that writes a design document, started
  from a signed requirements document.
- Text revision: a revision whose row opens on none of "Ready:",
  "Measured:", "Signed:" or "Parked:".
- Consult case: one of the four conditions under which the engineer seat
  asks another engineer before the PR: an ambiguity in the requirements,
  more than one solution, a solution unconventional to the codebase, or
  a change to a public contract. The checks call them the four cases.
- Public contract: a surface that code outside the feature depends on:
  routes, a gateway definition, events, a schema.

Five ratified terms take a new definition at intake:

- Feature document: what a feature's contract is derived from: a pair,
  or one combined document.
- Half: the request half, which the PO seat signs and a requirements
  document holds, or the solution half, which the engineer seat signs
  and a design document holds. A combined document holds both.
- Stale: a feature whose document holds a revision newer than the one
  its contract was derived from, or a derived block whose stamp is older
  than its document's newest revision, or a design document that names a
  requirements revision older than the requirements document's newest
  text revision. A "Ready:", "Measured:", "Signed:" or "Parked:" row
  never counts.
- Revision: one numbered row of a document's revision table, the first
  table in a requirements document, a design document or a combined
  document: r1, r2 and on.
- Feature before intake: a feature with a requirements document, a pair
  or a combined document, and no contract yet at
  `specs/<id>/contract.yaml`.
