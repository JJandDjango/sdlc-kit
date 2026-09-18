---
name: spec-interview-flow-opening
description: The Opening flow of /sdlc:product-specification-interview - path, origin, title, seats, materials; the state file written from the first answer on.
---

<purpose>
The Opening flow of `/sdlc:product-specification-interview`: the five
answers that shape the interview (path, origin, title, seats,
materials), with the state file written from the first answer on so a
pause anywhere resumes at the exact step. Dispatched by
{skill-dir}/SKILL.md when no state file exists for the slug, or at the
step `next` names; its constraints and criteria bind here. {skill-dir}
is the directory holding SKILL.md.
</purpose>

<instructions>
Each step O1-O5 ends by writing the state file with its answer and `next` set to the following step.

O1. PATH - PROPOSE `REQUEST_{slug}_{date}.md` at the repo root (date = today, ISO form) and ASK the user to confirm it or name another path. CHECK it with one Bash call `ls "{path}"`; a hit means REPORT "A document already exists at {path}. Name another path." and ASK again. WRITE the state file `{path without .md}.state.yaml`: `schema: spec-interview-state/1`, `slug`, `started` (today), `phase: opening`, `next: O2`, `path`, `answers: {}`, `open: []`, `history: [{at: now, event: path confirmed}]`.

O2. ORIGIN - ASK: "Is this a new feature or a bug fix?" A bug fix takes two more answers, one at a time: the incident reference (ticket or alert id) and the regression scenario in one sentence (the case that failed). Record `origin: feature | bug-fix`, `incident_ref`, `regression`.

O3. TITLE - ASK for the Jira key and the feature name, in the template's form "ABC-1234 - Feature name". The title is the document's heading; intake derives the task id from it. When the consumer has no tracker, the slug serves as the key. Record `title`.

O4. SEATS - ASK who holds the PO seat, then who holds the engineer seat. The engineer seat can be empty (record `null`); it decides whether Implementation is asked (sections.md Q9). Record `seats: {po, engineer}`; the names land on the Seats line and, at intake, in `confirmed_by`.

O5. MATERIALS - ASK whether there is material to start from: a ticket, a PRD, notes, a prior document, as pasted text or a path. When given, READ it and EXTRACT what maps to the template's sections (feature statement, description, background, success criteria, not in scope, requirements, previously defined, prerequisites, business requirements, implementation, questions, scenarios, additional notes). SHOW the extraction section by section and ASK the user to confirm each; record confirmed items under `answers.{section}` with `source: material`, so sections.md confirms instead of asking afresh. A conflict between the material and a spoken answer is asked, never resolved silently: "The material says X; you said Y. Which stands?"

O6. CLOSE - WRITE the state file with `phase: sections`, `next: Q1`, and `history: + {at: now, event: opening complete}`. REPORT the state file path in one line and return to SKILL.md step 1.
</instructions>
