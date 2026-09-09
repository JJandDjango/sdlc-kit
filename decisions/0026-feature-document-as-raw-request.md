# 26. The feature document is the raw request

Status: accepted
Date: 2026-09-08

## Context

The kit is pitched to a consumer with a PO team and an engineer team
whose venue is a feature document, a Google Doc the PO team edits:
authors, the request at a high level, the business use case,
prerequisites (usually permissions), technical details (endpoint
table, stack, integrations), functional tests as Gherkin, and Q&A. A
document is a new feature or a bug fix. The question: does the
contract replace the document or consume it? Bound by the eight
fields and immutability by channel (0005, 0010), one criterion per
REQ-ID (0011), the human census fixed at six (0015), the unit graph
computed from the contract (0024), and seats with `confirmed_by`
(0025). Proposed in session 28 (NOTES_g0-pitch_2026-09-08.md), held
by the session-29 video check and the playbook crosswalk (0027).

## Decision

- **The document stays and is the raw request.** Intake consumes it;
  the contract is what the meeting produces, never a replacement. The
  document holds worth and design in the PO team's words; the contract
  holds form and entry. The business case is decided in the document
  by its owners before intake: the "worth" gap closes upstream of G0,
  with no seventh human condition.
- **Every section has one landing place.** Authors are the seats in
  `confirmed_by`. The request is `intent`. The business case stays,
  linked by `provenance.ref`. A prerequisite is a ratified term under
  `entities`, a `dependencies` entry when another task must create it,
  or a guard unit when it is the access rule itself. Technical details
  give `scope` at G0; the endpoint table is the boundary schema G1.1
  lints and G2.2 locks. Gherkin gives one to three sketches per unit
  at G0 and the numbered criteria at G1. A decided Q&A answer is a
  sketch, a criterion, a non-goal, or a term; open ones carry to G1.3.
  Feature or bug fix is `provenance.origin`; `g8-escape` carries the
  incident ref (TC009).
- **The document stops at Gherkin.** Unit tests appear nowhere in it:
  they are the implementer's only write surface (G3), derived from the
  implementation, and the spec channel stays decorrelated (THEORY).
- **Three template changes, in order:** "Not in scope" (`non_goals`,
  TC002); Gherkin grouped by unit, each group titled by its unit's
  `done_means`; "Terms", the PO's nouns as the source of vocabulary
  files. Plus a status line naming the contract, its state, and its
  merge SHA: linkage as the minimum bar (0027). A change after ready
  goes back through intake: new answers, new merge.

Recorded non-goals: no business fields in the contract (priority is
not immutable; the tracker keeps it); no check on who was in the room
(0025); no G1 artifact (criteria stay hand-written until the G1 slice,
which takes Gherkin as its authoring format).

## Consequences

- USAGE gains a section beside section 8 holding the mapping table;
  the template changes are advice to the consumer, never enforced.
- The demo intake, one real document in a sandbox consumer, is the
  first run and the pitch artifact.
- A bug fix is the convergence loop verbatim: a `g8-escape` document
  whose regression scenario becomes a test the implementer cannot edit.
- G0 keeps zero human conditions: the gate checks the record of the
  answer, never the meeting.
