---
name: spec-interview-flow-output
description: The Output flow of /sdlc:product-specification-interview - the Google Docs form on request, then name the next command.
---

<purpose>
The Output flow of `/sdlc:product-specification-interview`: show the
feature document in the Google Docs form on request, and name the
next command. The document already stands at its path,
written from r1 on as each step closed. Dispatched by
{skill-dir}/SKILL.md when the state file's `phase` is `output`; its
constraints and criteria bind here. {skill-dir} is the directory holding
SKILL.md.
</purpose>

<instructions>
W1. ASK "Do you want the Google Docs form?" When yes, SHOW the document's content in the Google Docs form: a first line "Paste with Edit > Paste from Markdown.", no code fences (Gherkin as indented plain lines), pipe tables kept, headings and bold kept. The form shows the run's own document, and that one alone: the requirements document after a requirements run, the design document after a design run, never the pair. Nothing is written: the form stands in the conversation only.

W2. WRITE the state file with `phase: complete`, `next: null`, and `history: + {at: now, event: output complete}`. REPORT: the document path, the state file path, the OPEN count, and the next command verbatim: `/sdlc:product-specification-interview {id} design`. After a design run the next command is `/sdlc intake docs/features/{id}.md` instead, verbatim: intake takes the requirements document's path. Return to the conversation.
</instructions>
