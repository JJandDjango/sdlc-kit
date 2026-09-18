---
name: spec-interview-flow-output
description: The Output flow of /sdlc:product-specification-interview - render the document from the template, write it without overwriting, the Google Docs form on request, name the intake command.
---

<purpose>
The Output flow of `/sdlc:product-specification-interview`: render the
feature document from the template with the state file's answers,
write it at the confirmed path without overwriting, render the Google
Docs form on request, and name the command that consumes it.
Dispatched by {skill-dir}/SKILL.md when the state file's `phase` is
`output`; its constraints and criteria bind here. {skill-dir} is the
directory holding SKILL.md.
</purpose>

<instructions>
W1. RENDER the document from {skill-dir}/templates/feature-document.md.template with the state file's answers. Fill every `{{ placeholder }}`; drop the template's guidance lines (the lines in italics); a section with no content keeps its heading and the line "(none)". The revision table's first row is today, the PO seat, "Created by /sdlc:product-specification-interview"; the second row stays reserved for intake. Gherkin groups under its success criterion as "### SC{n}: {text}", one "Scenario:" block per scenario. Every `open` entry lands inline in its section as "OPEN: {text}". A bug fix adds two lines under Background Information: the incident reference and the regression scenario.

W2. CHECK the path from the state file with one Bash call `ls "{path}"`. A hit means REPORT "A document already exists at {path}. Name another path." and ASK for one; record the new path; never overwrite.

W3. WRITE the document at the path (Write tool). WRITE the state file with `phase: complete`, `next: null`, and `history: + {at: now, event: document written}`.

W4. ASK "Do you want the Google Docs form?" When yes, SHOW the same content in the Google Docs form: a first line "Paste with Edit > Paste from Markdown.", no code fences (Gherkin as indented plain lines), pipe tables kept, headings and bold kept. Nothing further is written.

W5. REPORT: the document path, the state file path, the OPEN count, and the next command verbatim: `/sdlc intake {path}`. Return to the conversation.
</instructions>
