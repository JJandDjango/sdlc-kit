---
name: spec-interview-flow-opening
description: The Opening flow of /sdlc:product-specification-interview - id, origin, title, seats, materials; the state file written from the first answer on, the document written as r1 at the close.
---

<purpose>
The Opening flow of `/sdlc:product-specification-interview`: the five
answers that shape the interview (id, origin, title, seats, materials),
with the state file written from the first answer on so a pause anywhere
resumes at the exact step, and the document written as r1 at the close.
Dispatched by {skill-dir}/SKILL.md when no state file exists for the id,
or at the step `next` names; its constraints and criteria bind here.
{skill-dir} is the directory holding SKILL.md.
</purpose>

<instructions>
Each step O1-O5 ends by writing the state file with its answer and `next` set to the following step.

O1. ID - CONFIRM the id from SKILL.md step 0; the document's path is `docs/features/{id}.md`. CHECK it with one Bash call `ls docs/features/{id}.md`; a hit means REPORT "A document already exists at {path}. Name another path." and ASK for another id. WRITE the state file `docs/features/{id}.state.yaml`: `schema: spec-interview-state/2`, `id`, `started` (today), `phase: opening`, `next: O2`, `answers: {}`, `open: []`, `history: [{at: now, event: id confirmed}]`.

O2. ORIGIN - ASK: "Is this a new feature or a bug fix?" A bug fix takes two more answers, one at a time: the incident reference (ticket or alert id) and the regression scenario in one sentence (the case that failed). Record `origin: feature` or `origin: bug-fix`, with `incident_ref` and `regression` for a bug fix.

O3. TITLE - ASK for the feature's title: the outcome, in a few words. The document's title line reads `# {id} - {title}`; the tree and intake read it. Record `title`.

O4. SEATS - ASK who holds the PO seat, then who holds the engineer seat. The engineer seat can be empty (record `null`); it decides whether the solution half is asked (solution.md S1). Record `seats: {po, engineer}`; the names land in r1, on the status line and, at intake, in `confirmed_by`.

O5. MATERIALS - ASK whether there is material to start from: a ticket, a PRD, notes, a prior document, as pasted text or a path. When given, READ it and EXTRACT what maps to the template's sections (statement, description, background, existing behavior touched, success criteria, non-goals, prerequisites, checks, error messages, the solution half, decisions and open questions, notes, terms). SHOW the extraction section by section and ASK the user to confirm each; record confirmed items under `answers.{section}` with `source: material`, so the section's own step shows the material and asks to confirm instead of asking afresh. A conflict between the material and a spoken answer is asked, never resolved silently: "The material says X; you said Y. Which stands?"

O6. CLOSE - WRITE the document `docs/features/{id}.md` as r1 from {skill-dir}/templates/feature-document.md.template: fill `{date}` (today), `{po}`, `{engineer}` ("none" when empty), `{id}`, `{title}` and `{repo}` (the repo directory's name); a section confirmed at O5 gets its text, and a section that no step has written and O5 did not confirm reads "(not yet asked)"; a derived block not yet written carries no stamp, so the Gherkin block gets the tag `[PO seat · derived]` and the body "(none: the Gherkin step writes one scenario per check)", and the Record block gets the tag `[Intake · derived]` and the body "(none: intake writes the record)", while the template keeps its stamped tags for the step that writes each block; a feature's document drops each block from `{bug fix only}` to `{end bug fix only}`, marker lines included, so it omits the four bug-fix sections and never leaves them empty; a bug fix's document keeps each block with `incident_ref` and `regression` filled and drops only the two marker lines. WRITE the state file with `phase: request`, `next: Q1`, and `history: + {at: now, event: opening complete, document written as r1}`. REPORT the document path and the state file path in one line and return to SKILL.md step 1.
</instructions>
