# 29. The feature document has one format and a definition of done

Status: accepted
Date: 2026-09-18

## Context

ADR 0026 made the feature document the raw request and named four
template changes as advice to the consumer: "Not in scope", Gherkin
grouped by unit, "Terms", and a status line. The interview skill (0028)
shipped the first, and the template has no status line and no Terms.
In session 32 the user brought a seventeen-section format in use on
another project (no kit) and asked for one format that serves both
readers: the PO team's Google Doc and the kit's intake. The two were
reconciled call by call; the record is `NOTES_feature-document_
2026-09-18.md`. Bound by the eight fields (0005), immutability by
channel (0010), the human census (0015), the unit graph computed from
the contract (0024), seats with `confirmed_by` (0025), and 0026 itself.
Alternatives weighed and rejected: one mixed "not in scope" list (the
kit's own contracts show it enforces neither kind); the Gherkin copied
under each unit (two copies drift, and the copy below the line reads
as the implementer's to edit); Gherkin grouped by unit as 0026 said
(it assumes one unit per criterion, which the real contracts do not
bear out); an editable contract in the appendix (a second spec
channel); a typed traceability table (the first thing nobody updates);
a "last measured" field in the status line (a date nobody updates).

## Decision

- **One format, eighteen sections, one seat boundary.** The request
  stands above the line and the PO seat signs it; the solution stands
  below and the engineer seat signs it; the record follows. Acceptance
  criteria sit above the line, before the proposed solution: units are
  cut from checks, never the reverse. The owner names who signs, not
  who types. Every section carries a tag: owner and kind (authored, or
  derived from revision rN).
- **Two lists per half.** Success criteria and scope are whitelists,
  proved or enforced; non-goals (capabilities, a promise people check)
  and out of scope (paths; intake cuts `scope` so none falls inside
  it) are blacklists that record refusals and test the whitelist.
- **Three levels of proof.** A success criterion is an outcome. Under
  it, two or three one-line checks with ids (SC3.1), signed by the PO
  seat, stored per unit as `acceptance_sketch`. Under each check, one
  Gherkin scenario, derived, never hand-edited; a Then may not carry a
  fact its check lacks. At intake every check is assigned to exactly
  one unit. This replaces 0026's "grouped by unit": grouped by
  criterion, joined by check id.
- **Derived blocks are read-only and stamped**: the contract, the
  Gherkin, the traceability record, all in the appendix or the record,
  each with the revision it was rendered from. Where the kit runs,
  `specs/{id}/contract.yaml` is the authority and the appendix shows a
  copy; without the kit the appendix is the contract's only home and
  read-only is a discipline. A stamp older than the newest revision
  row is stale; a "Measured:" row that changed no text is the one row
  that does not age a stamp.
- **Measurement is a revision row**, not a field: a row whose changes
  start with "Measured:" and name what was looked at, added even when
  no text changed. The newest such row is the last-measured date.
- **The definition of done.** The document is ready when intake can
  derive a ready-green contract from it without asking the request
  half a single new question. Ten checks, eight the request half's
  (advisory in the interview, hard at intake) and two intake's exit.
  Zero OPEN marks at ready above the line or in Decisions and open
  questions; an undecidable question parks the document. Three
  states, three signatures: ready (both seats and the validator),
  merged (the verifier per unit and whoever merges), closed (the PO
  seat on a closing measurement). Understanding cannot be checked; a
  named seat's signature on a named revision is its record.
- **A surprise enters the document before the conversation.** During
  development it stops the unit, lands as an OPEN entry with the unit
  id and the finding plus a revision row, stales the derived blocks,
  pauses every unit, and goes back through intake with the finding in
  the text (0026's change-after-ready, with the venue named).

Recorded non-goals: no check on understanding (0025's line holds); no
business fields in the contract (risks and cost stay in the document);
no headings read by the tooling (the template stays advice, 0026).

## Consequences

- The template, the interview's sections flow and the readiness check
  change under a contract of their own: the reorder, the tags, numbered
  revision rows, the status line, Terms, three sections dissolved
  (Business Requirements, Previously Defined, Misc.), and the readiness
  rules growing from five to ten plus the stale-stamp rule.
- Intake changes: an open question no longer carries to G1.3; every
  check is assigned to one unit, and an orphan check or an empty unit
  is a finding. The mapping section beside USAGE section 8 still lands
  with the demo.
- Deriving Gherkin from checks is one interview step, upstream of the
  carried G1 slice, which it feeds.
- Wave B may make the pause mechanical: the hook refuses a commit while
  a derived block is stale or an OPEN mark stands.
- Harder: the consumer's PO team learns new headings and a stricter
  exit (parked, not "ready with caveats"); a document in Google Docs
  needs the discipline of the revision row, because the tooling reads
  the row number and never the row's words.
