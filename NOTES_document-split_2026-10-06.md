# Notes - document split (2026-10-06)

Status: in flight, session 74. Material for the interview's materials
step (O5). Working id `document-split`. No contract, no ratified term.

Source: the user's team at work, 2026-10-05, on the process kit 0.18.0
proposes; told to the session on 2026-10-06.

## The feedback, word for word

> The feecback I got downstream from my team at work was that the
> process I proposed is different than the one I wanted.
>
> What I proposed:
> 1. Work with PO Team and Engineering Team to make a Feature Document
>    that combined Requirements and Design/Implementation details.
> 2. Each team would approve and sign off on each section
> 3. After approval Claude would take the document as input to complete
>    the required work
> 4. I review the PR after Claude opens it
> 5. Another engineer reviews the PR after I request
> 6. Merge to main
>
> What I was met with:
> 1. These should not be one combined document: the PO team will only
>    care about what the request looks like, not the actual
>    design/implementation details
> 2. All of the Engineer Seat items go in their own
>    Design/Implementation document
> 3. I will be only engineer looking at the Design/Implementation
>    document; other engineers already find their time pressed and
>    don't want to use any more of it than they have to and believe it
>    would be doubling PR review time.
>
> The target lifecyle that was requested:
> 1. Work with PO Team to make Requirements Document
> 2. Work alone to make Design Document
> 3. Pass work to Claude to get Design Document details implemented
> 4. Review Claude's PR
> 5. Request final PR review from another engineer
>
> The only time I should reach out to another engineer is:
> 1. Clarifying ambiguity
> 2. Multiple solutions
> 3. Solution is unconventional to the codebase
> 4. Solution changes a public contract (routes, gateway definition,
>    events, schema, etc.)
>
> The risks this plan carries are:
> 1. PR reviewer arrives without context
> 2. One engineer designing alone has blindspots

The message's closing paragraph, the user's own remark, is left out:
this repo is public.

The user, 2026-10-06: "two documents instead of one and I'm expected to
be the only Engineer seat in the second document".

## What the kit holds today

- One feature document per feature, `docs/features/<id>.md`, in ADR
  0029's format as ADRs 0033 to 0036 amend it. The request half stands
  above a `---` line and the PO seat signs it; the solution half stands
  below and the engineer seat signs it. Each half has its own `Signed:`
  row (ADR 0034).
- One interview writes both halves, and one state file holds the run.
- Intake derives the contract from the newest text revision both seats
  signed.
- The gate list already separates the two subjects: G1, Requirements /
  Spec (`docs/gates.md:129`), and G2, Design / Architecture
  (`docs/gates.md:154`).
- The session's reading of the four triggers against that list, not a
  ruling: an ambiguity falls on G1.3 (criteria completeness and
  ambiguity review, human); more than one solution and an
  unconventional solution fall on G2.3 (significant design choices are
  recorded and reviewed, human); a public contract change falls on G2.2
  (breaking-change baseline lock).

## Risks

1. The PR reviewer arrives without context (the user's).
2. One engineer designing alone has blind spots (the user's).
3. The two documents drift: the design is written against one revision
   of the requirements, and the requirements change after it (the
   session's).

## Candidates kept (the user, 2026-10-06)

1. Two documents replace the one: a requirements document and a design
   document, one pair per feature.
2. The requirements document holds only what the PO seat signs,
   Statement through Acceptance criteria. It names no file, unit or
   interface.
3. The design document holds every engineer seat section (Proposed
   solution, Risks and cost), and one engineer seat signs it alone.
4. Two interview runs. The requirements run ends at the PO seat's
   signature. The design run starts later from a signed requirements
   document, with no PO seat present.
5. The design document names the requirements revision it was written
   against. A later requirements change makes the design signature
   stale, and both the checks before signing and intake say so.
6. Intake takes the pair. It parks when either signature is missing or
   the pinned revision is stale.
7. The design document carries the four triggers as four answered
   lines. A yes names who was asked and what was decided, and the
   checks report a missing answer.
8. Combined documents already through intake stay as records, and
   intake reads pairs only. G1's document, the one still before intake
   in this repo, is split by hand.
9. The Google Docs form renders each document on its own, so the PO
   team receives the requirements document alone.

## Moved later, out of this feature

10. Trigger 4 computed: a config list of public contract paths, checked
    against the design's Scope.
11. Claude reviews the design in a fresh context before the engineer
    signs, and answers the triggers itself.
12. A PR brief generated from the design document for the final
    reviewer: the decision, the alternatives rejected, the trigger
    answers, and which test proves which check.

## Open points

- Are any combined documents in flight on the second machine? Asked
  2026-10-06, not yet answered. If so, candidate 8 needs a path for
  them.
- Where the record goes: Decisions and open questions, Traceability,
  Notes, and the Appendix's Contract, Gherkin and Terms blocks. Which
  document carries each, and does the PO seat's document carry anything
  that seat does not sign?
- The four bug-fix sections: one document or the other.
- File names and paths for the pair, and one state file or two.
- Does "feature document" stay as a term, as the name of the pair, or
  retire for the two new names?
- Unit confirmation (G0.3): with one engineer seat and no PO seat at the
  design run, which seat confirms each unit at intake.
- Who the engineer seat tells when a trigger reads yes after the
  signature, during the build.
