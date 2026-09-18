# Feature document notes - the ratified format

_Session 32, 2026-09-18. Working notes, not a Cairn stratum. Ratified
call by call in session 32: six reconciliation calls and one marker
rule. Amends ADR 0026's template changes; the ADR follows once the
definition of done is ratified. Sources: the kit's intake-ready
template (`skills/product-specification-interview/templates/
feature-document.md.template`) and the user's work format (seventeen
sections, a different project, no kit)._

## Purpose

One format for two readers: the PO team's document at the consumer,
and the kit's intake, which derives the contract from it (ADR 0026).
The work format brought five things the template lacked: the status
line, the bug-fix analysis, an explicit proposed solution, risks and
cost, and terms. The template brought four the work format lacked:
seats, existing behavior touched, the interface table, verbatim error
messages, plus the question log with OPEN marks.

## Rules

1. **One seat boundary.** The request stands above the line and the PO
   seat signs it; the solution stands below and the engineer seat signs
   it. Acceptance criteria sit above the line, before the proposed
   solution: units are cut from checks, never the reverse. The owner
   names who signs, not who types (an engineer drafts Findings; the PO
   seat signs them).
2. **Two lists per half.** A whitelist that is proved or enforced
   (success criteria; scope) and a blacklist that records refusals
   (non-goals; out of scope). A non-goal is a capability: a promise
   people check. An out-of-scope entry is a path: it tightens `scope`,
   and the session hook and `scope-check` enforce the result. The
   blacklist tests the whitelist and never replaces it.
3. **Three levels of proof.** A success criterion is an outcome, one
   line. Under it, acceptance criteria: two or three one-line checks
   with ids (SC3.1), written and signed by the PO seat, stored in the
   contract as `acceptance_sketch`. Under each check, one Gherkin
   scenario, derived and never hand-edited: a wrong scenario means a
   thin check. A scenario may fill in its Given; its Then may not carry
   a fact the check lacks (mark the check thin instead). At intake every
   check is assigned to exactly one unit; units list check ids.
4. **Derived blocks are read-only and stamped** with the revision (rN)
   they were rendered from: the contract, the Gherkin, the traceability
   record. Where the kit runs, `specs/{id}/contract.yaml` is the
   authority and the appendix shows a rendered copy with its path. At a
   consumer without the kit the appendix is the contract's only home
   and read-only is a discipline: edit the sections, re-render. A change
   after ready goes back through intake (ADR 0026).
5. **Traceability is half authored, half rendered.** Authored: the links
   out (ticket, incident, related documents, contract, PR). Rendered
   after merge: unit, commit, tests, from the `Contract:` trailers. The
   status line is the glanceable subset.
6. **Every section carries a tag** under its heading: owner and kind.
   `[PO seat · authored]`, `[Engineer seat · authored]`,
   `[Both seats · authored]`, `[Intake · derived from r4]`. A derived
   block whose stamp is older than the newest revision row is stale,
   and stale is an OPEN mark at readiness; a "Measured:" row that
   changed no text is the one row that does not age a stamp.
   Re-rendering an unchanged derivation is cheap, so the rule reads the
   row number and never the row's words.
7. **Three template sections dissolve.** Business Requirements:
   additions and subtractions are the units; error messages move under
   acceptance criteria. Previously Defined becomes Existing behavior
   touched, under Background. Misc. becomes Decisions and open
   questions.

## The format

Landing place in the contract in parentheses. Sections marked "bug fix
only" are omitted for a feature, never left empty.

Header

1. Revision table `[Both seats · authored; intake writes its own row]`.
   Rows numbered r1, r2, ...; columns: date, revised by, changes. Rows
   stay simple ("Added two functional tests"). A measurement is a row
   whose changes start with "Measured:" and name what was looked at
   (the findings, the existing behavior, the prerequisites, the closing
   measurement after merge), added even when no text changed; the
   newest such row is the last-measured date, read by the readiness
   check and typed nowhere else. A comment resolved without a text
   change adds no row.
2. Title `KEY-123 - Title` `[PO seat · authored]`. The key becomes the
   task id and `provenance.ref`.
3. Status line `[Engineer seat · authored; intake fills contract, PR,
   SHA]`. Repository or service · seats: PO, engineer (`confirmed_by`)
   · contract id and state (draft, ready, parked, merged) · PR · merge
   SHA.
4. Statement `[PO seat · authored]`. As a {role}, I want {capability},
   so I can {a state of the world} (`intent`).

The request: the PO seat signs

5. Description. 5.1 Findings at a glance (bug fix only).
6. Background. 6.1 Existing behavior touched: operations and permission
   rules the feature touches; each lands as a term (18.3) and a
   regression check.
7. Findings (bug fix only): the evidence.
8. Why this happened (bug fix only): the cause; its regression check is
   12.3.
9. Success criteria: three to five, one line each, an outcome a test
   can decide.
10. Non-goals (`non_goals`): the adjacent capability someone would
    plausibly expect, deliberately left out; if nobody would wonder, it
    does not belong; the consumer's standing line first.
11. Prerequisites: permissions, roles, other teams' tickets, each marked
    exists or missing (`dependencies`, a term, or a guard unit).
12. Acceptance criteria. 12.1 Checks, two or three per criterion, ids
    SCn.m (`acceptance_sketch`). 12.2 Error messages, verbatim: each a
    check's Then and a term. 12.3 Regression check (bug fix only): the
    test the implementer cannot edit.

The line.

The solution: the engineer seat signs

13. Proposed solution. 13.1 Scope: paths (`scope`). 13.2 Out of scope:
    three to five paths near the change it must not touch; intake cuts
    `scope` so none falls inside it. 13.3 Interfaces: the endpoint or
    schema table (G1.1 lints it, G2.2 locks it). 13.4 Constraints that
    hold across every unit. 13.5 Units: id, the check ids it delivers,
    files, tests by kind or file (`decomposition`; `done_means` is the
    engineer's sentence). 13.6 Sequencing (`depends_on`); the graph is
    computed, never drawn.
14. Risks and cost `[Both seats · authored]`: the worth decision, closed
    before intake; stays in the document, never in the contract.

The record

15. Decisions and open questions `[Both seats · authored]`: question
    and answer, OPEN marked; a decided answer becomes a check, a
    criterion, a non-goal or a term; an open one carries to the
    requirements gate.
16. Traceability. 16.1 Links out `[Both seats · authored]`. 16.2 Record
    `[Intake · derived from rN]`, after merge: unit, commit, tests.
17. Notes `[Both seats · authored]`: freeform.
18. Appendix. 18.1 Contract `[Intake · derived from rN]`. 18.2 Gherkin
    `[Intake · derived from rN]`, one scenario per check. 18.3 Terms
    `[PO seat · authored]`: the PO's nouns, the source of the
    vocabulary files.

Eighteen sections, four bug-fix only, three derived, all three at the
bottom.

## Derivation and change

One direction: document at rN, intake, contract (validated ready-green),
Gherkin per check, tests at G1; git trailers to the traceability record.
A change edits sections, makes a new revision, re-runs intake,
regenerates the contract, re-renders the appendix, and logs a row.

States, carried in the status line: draft (the interview), ready
(intake green, contract derived, appendix stamped), merged (PR in, SHA
recorded, traceability rendered). The definition of done is asked per
state; it is the next item of this session.

## Consequences for the kit (not yet contracted)

- The template: the reorder, the tags, numbered revision rows, the
  status line, Terms, and the three dissolved sections. The interview's
  sections flow follows the new order. The readiness check gains the
  stale-stamp rule and the thin-check rule.
- Deriving Gherkin from checks is one interview step and one unit,
  upstream of the carried G1 slice (Gherkin as the authoring format).
- ADR 0026's template changes amended: Gherkin grouped by criterion and
  joined to units by check id, not grouped by unit; the status line and
  the tags added. The mapping section beside USAGE section 8 still lands
  with the demo.
- The work format gains the tags, the status line's state, numbered
  revisions and the appendix Gherkin; its contract stays in the appendix.

## Open

- A verifier verdict column in the traceability record needs receipts
  persisted per unit; today they live in commit messages.

Closed 2026-09-18: "last measured" is not a field. A measurement is a
revision row ("Measured:"), for a bug fix (the findings) and a feature
(the existing behavior, the prerequisites) alike, and the closing
measurement after merge is what closes an escape in production; the
regression test only proves it in CI.
