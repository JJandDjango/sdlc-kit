---
name: spec-interview-flow-opening
description: The Opening flow of /sdlc:product-specification-interview - origin, title, seats, materials, path; the first write of the state file.
---

<purpose>
The Opening flow of `/sdlc:product-specification-interview`: the five
answers that shape the interview (origin, title, seats, materials, path)
and the first write of the state file. Dispatched by
{skill-dir}/SKILL.md when no state file exists for the slug; its
constraints and criteria bind here. {skill-dir} is the directory holding
SKILL.md.
</purpose>

<instructions>
O1. ORIGIN - ASK: "Is this a new feature or a bug fix?" A bug fix takes two more answers, one at a time: the incident reference (ticket or alert id) and the regression scenario in one sentence (the case that failed). Record `origin: feature | bug-fix`, `incident_ref`, `regression`.

O2. TITLE - ASK for the Jira key and the feature name, in the template's form "ABC-1234 - Feature name". The title is the document's heading; intake derives the task id from it. When the consumer has no tracker, the slug serves as the key. Record `title`.

O3. SEATS - ASK who holds the PO seat, then who holds the engineer seat. The engineer seat can be empty (record `null`); it decides whether Implementation is asked (sections.md Q9). Record `seats: {po, engineer}`; the names land on the Seats line and, at intake, in `confirmed_by`.

O4. MATERIALS - ASK whether there is material to start from: a ticket, a PRD, notes, a prior document, as pasted text or a path. When given, READ it and EXTRACT what maps to the template's sections (feature statement, description, background, success criteria, not in scope, requirements, previously defined, prerequisites, business requirements, implementation, questions). SHOW the extraction section by section and ASK the user to confirm each; record confirmed items under `answers.{section}` with `source: material`, so sections.md confirms instead of asking afresh. A conflict between the material and a spoken answer is asked, never resolved silently: "The material says X; you said Y. Which stands?"

O5. PATH - PROPOSE `REQUEST_{slug}_{date}.md` at the repo root (date = today, ISO form) and ASK the user to confirm it or name another path. CHECK it with one Bash call `ls {path}`; a hit means REPORT "A document already exists at {path}. Name another path." and ASK again. Record `path`.

O6. WRITE the state file `{path without .md}.state.yaml`: `schema: spec-interview-state/1`, `slug`, `started` (today), `phase: sections`, `next: Q1`, `origin`, `incident_ref`, `regression`, `title`, `seats`, `path`, `answers` (from O4, else `{}`), `open: []`, `history: [{at: now, event: opening complete}]`. REPORT the state file path in one line and return to SKILL.md step 1.
</instructions>
