# 37. A feature document is a pair, and each document has one seat

Status: accepted
Date: 2026-10-06

## Context

ADR 0029 fixed one feature document with two halves, the request above
a line and the solution below it, and 0033 to 0036 amended it. Kit
0.18.0 shipped that format with an interview that writes both halves
into one file. The first team to use it outside this repo answered on
2026-10-05 (`NOTES_document-split_2026-10-06.md`): the PO team reads the
request and never the design; one engineer writes the design alone;
another engineer is asked before the PR only in four cases; the final PR
review stays. The request is the feature document
`docs/features/document-split.md`, written through the 0.18.0 interview:
the PO seat signed its request half at r3 and the engineer seat its
solution half at r6. Its Prerequisites name this ADR, and its Notes list
what the ADR carries.

Bound by the seats (0025), no section read by the tooling (0026, 0029),
the signature's form (0034), the tree computed at print (0031) and the
contract schema, which the feature leaves at 1.5.0. Alternatives
rejected: a second engineer's review of a design before the PR (the team
holds it to double the PR review time); a design run on unsigned
requirements (the design would rest on text no seat has signed); a stale
design that parks the pair (it stops intake as a missing signature does:
a seat's word is missing, not text); a command that reads signatures and
staleness (the flows read them, asked and never parsed); a command that
splits a combined document (no document here needs one: G1's holds no
solution half, and a document through intake stays as written).

## Decision

- **A feature document is a pair.** The requirements document, at
  `docs/features/<id>.md`, holds the request half, and the PO seat signs
  it. The design document, at `docs/features/<id>.design.md`, holds the
  solution half, and one engineer seat writes and signs it alone. Each
  is written in its own interview run, and a design run starts only from
  a requirements document whose newest text revision the PO seat has
  signed. A document in 0029's format, both halves in one file, is a
  combined document.
- **Each document holds its own half and its own record.** The
  requirements document: the revision table, the title line, a status
  line, the request half's sections in the ratified order, a bug fix's
  four among them, then Decisions and open questions, Notes, and the
  Appendix with Gherkin and Terms. The design document: the revision
  table, the same title line, a status line, Proposed solution with its
  seven sections, Risks and cost, Consult cases, Decisions and open
  questions, Traceability with Links out and Record, Notes, and the
  Appendix with Contract. Neither holds a line between halves. No
  section of either half is reworded, reordered or dropped.
- **Every tag names one seat.** The requirements document's authored
  sections read `[PO seat · authored]`, and its Gherkin `[PO seat ·
  derived from rN]`. The design document's read `[Engineer seat ·
  authored]`; Record and Contract keep `[Intake · derived]`. No section
  is tagged for both seats.
- **r1 and the status line name the document's one seat.** Drawn on a
  feature `x`, PO seat ann, engineer seat raj, first the requirements
  document's two lines, then the design document's:

  ```
  r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: ann
  `repo` · seat: PO ann · contract: `x`, draft · PR: none · merge SHA: none

  r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r3. Engineer seat: raj
  `repo` · seat: engineer raj · requirements: `docs/features/x.md` · contract: `x`, draft · PR: none · merge SHA: none
  ```

- **A design names one requirements revision**: the `requirements r{m}`
  of its newest text row that names one. r1 names it first. When the
  requirements document holds a newer text revision, the engineer seat
  confirms the design against it in a text row, `rN: Confirmed against
  requirements r{m}`, and signs again. A design that names a revision
  older than the requirements document's newest text revision is stale.
- **A text revision** is a row that opens on none of `Ready:`,
  `Measured:`, `Signed:` or `Parked:`. A `Signed:` row stands in its
  half's own document and signs the newest text revision of that table.
- **Consult cases, and ready check 15.** The design document answers the
  four cases in which the engineer seat asks another engineer before the
  PR: an ambiguity in the requirements; more than one solution; a
  solution unconventional to the codebase; a change to a public contract
  (routes, a gateway definition, events, a schema). Each answer is yes
  or no, and a yes names who was asked and what was decided. Ready check
  15 asks whether each case has an answer and each yes names both. The
  solution half's ready checks are 11 to 15, advisory in the interview
  and hard at intake. Ready check 8 names the PO seat alone, where it
  named both seats.
- **Intake reads a pair and writes one row in each table.** It takes the
  requirements document's path and reads the design document beside it.
  The contract takes its title, statement, non-goals, checks and terms
  from the requirements document, and its scope, units, each
  `done_means` word for word, order and tests from the design document.
  Ready-green writes one `Ready:` row in each table: each names its own
  table's signed text revision, and the design's adds `against
  requirements r{m}`. A refusal in either document parks the pair: one
  `Parked:` row in each table, numbered in its own table, both holding
  the same list, the requirements document's things first.
- **A missing signature or a stale design stops intake**, with no row
  and no contract. The stops are read only when no refusal stands.
- **Intake reads no combined document.** One with no `Ready:` row stops
  it with the message the document's request half holds. Three edges the
  request half gives no words for take these, each a stop with nothing
  written. Intake with no design document: `No design document for {id}.
  Run the design interview first.` A design run on a combined document:
  `{path} is a combined document. Split it by hand, then run the design
  interview.` Intake on a combined document that holds a `Ready:` row:
  `{path} is a combined document through intake. Its contract stands.`
- **The tree shows a pair as one feature.** A design document is never a
  feature of its own. The feature's line gains the mark `design rN`, the
  design's newest text revision, and the solution half reads its
  signature from the design document's table. After intake the drift
  mark reads each table against its own `Ready:` row, and the design's
  reads `stale: design rN, contract from rM`.

This amends 0029: "one format, eighteen sections, one seat boundary"
describes a combined document; a new feature document is a pair with no
line between halves, every tag names one seat, ready check 8 names the
PO seat alone, and a design behind its requirements is stale as a stamp
behind its revision is. It amends 0033: the solution half's ready checks
are 11 to 15, and they and the checks run before signing read the design
document. It amends 0034: each `Signed:` row stands in its half's own
document. It amends 0035: a feature before intake is a requirements
document, a pair or a combined document, shown as one feature, and the
title line read is the requirements document's. It amends 0036: the
Gherkin stands in the requirements document's Appendix and the Contract
block in the design document's, intake copies each `done_means` from the
design document's Units table, and a `Ready:` or `Parked:` row is
written in each table.

Recorded non-goals: no change to the seats (0025), so I5 stands: each
unit takes a human answer, and no rule names which seat confirms it; no
second engineer signs or reviews a design before the PR; no command
splits a combined document; no new command, since the interview and
intake read signatures and a stale design in their flows, and ready
check 15 is asked, never parsed (0029); no change to the contract
schema.

## Consequences

- `document-split` carries the change in six units, `d1-requirements` to
  `d6-release`, as kit 0.19.0: two templates and two runs in the
  interview, the pair read in intake, and the tree's marks. Until
  `d5-intake` ships, intake reads one document.
- The PO team reads and signs a document that holds no design, and a
  design is ready to build on one engineer's signature.
- A document through intake stays as written, `feature-document`,
  `project-tree` and `tree-first-level` among them. `document-split`'s
  own document is the last one written combined, and takes its `Ready:`
  row from kit 0.18.0's intake.
- G1's document holds no solution half: it stands unchanged as a
  requirements document, and its design is written through a design run,
  to this ADR.
- Harder: a feature holds two files and two state files; a requirements
  change after the design's signature costs the engineer seat a
  confirmation row and a second signature; a combined document with no
  `Ready:` row is split by hand or finished under kit 0.18.0.
