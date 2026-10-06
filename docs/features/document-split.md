| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-06 | user | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: user; engineer seat: user |
| 2026-10-06 | user | r2: Measured: the checks before signing, on the request half: 179 findings (CL003 1, CL006 145, CL008 14, CL010 3, CL012 16); ready checks 1 to 8: 0 OPEN |
| 2026-10-06 | user | r3: The request half finished: 7 sections written, 0 OPEN |
| 2026-10-06 | user | r4: Signed: request half. The PO seat signs r3 |

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

(not yet asked)

### Out of scope

(not yet asked)

### Interfaces

(not yet asked)

### Sources

(not yet asked)

### Constraints

(not yet asked)

### Units

(not yet asked)

### Order

(not yet asked)

## Risks and cost

`[Both seats · authored]`

Risks:

1. The final PR reviewer arrives without context.
2. One engineer who designs alone has blind spots.
3. The two documents drift: the design is written against one revision
   of the requirements, and the requirements change after it.

## Decisions and open questions

`[Both seats · authored]`

- Q: One document or two? A: Two: a requirements document and a design
  document (the user, 2026-10-06, on the team's answer of 2026-10-05).
- Q: Which candidates stay in this feature? A: Candidates 1 to 9; the
  three under Non-goals move to later features (2026-10-06).
- Q: Before or after G1's solution half? A: Before: G1's solution half
  would otherwise be written in the format this feature replaces
  (2026-10-06).
- Q: Are any combined documents in flight in another repo? A: not yet
  decided. If so, candidate 8 needs a path for them.
- Q: Which document carries each part of the record? A: Gherkin and
  Terms go with the requirements; Risks and cost, Traceability and the
  Contract block go with the design; each document keeps its own
  Decisions and open questions and its own Notes (SC1.1, SC1.2;
  2026-10-06).
- Q: Which document carries the four bug-fix sections? A: The
  requirements document (SC1.1; 2026-10-06).
- Q: What are the pair's file names and paths, and is there one state
  file or two? A: not yet decided.
- Q: Does "feature document" stay as a term? A: Yes, as the umbrella: a
  pair, or one combined document (Terms; 2026-10-06).
- Q: May a design run start on unsigned requirements? A: No: it stops
  with its message (SC2.2; 2026-10-06).
- Q: Does a stale design park or stop intake? A: It stops, like a
  missing signature, with no `Parked:` row (SC3.2, SC4.2; 2026-10-06).
- Q: Which document takes intake's row? A: Both (SC4.1; 2026-10-06).
- Q: With one engineer seat and no PO seat at the design run, which seat
  confirms each unit at intake (G0.3)? A: not yet decided.
- Q: Who does the engineer seat tell when one of the four cases turns to
  yes after the signature, during the build? A: not yet decided.

## Traceability

### Links out

`[Both seats · authored]`

(not yet asked)

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

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/document-split/contract.yaml`)

### Gherkin

`[PO seat · derived from r3]`

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
