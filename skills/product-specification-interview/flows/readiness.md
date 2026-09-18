---
name: spec-interview-flow-readiness
description: The Readiness flow of /sdlc:product-specification-interview - readback, the advisory check of what intake will need, OPEN marks; never blocks.
---

<purpose>
The Readiness flow of `/sdlc:product-specification-interview`: read the
document back, check what intake will need, mark the gaps OPEN, and let
the user decide. The check advises and never blocks: the document is
the requester's (ADR 0026). Dispatched by {skill-dir}/SKILL.md when the
state file's `phase` is `readiness`; its constraints and criteria bind
here. {skill-dir} is the directory holding SKILL.md.
</purpose>

<instructions>
R1. READBACK - LOAD the state file. SHOW the document as it stands, section by section in the template's order, one line per item. ASK "Anything to change before the checks?" A change names a section: EXECUTE that section's step from {skill-dir}/flows/sections.md, then return to R1.

R2. CHECK what intake will need, and record every miss under `open` with its section name:
   - the feature statement's outcome clause names a state of the world ("so I can ...")
   - `not_in_scope` holds at least one line
   - three to five success criteria, each with two or three scenarios, each scenario with Given, When, and Then
   - the PO seat is named
   - every answer recorded `thin: true`, and every `misc` entry answered OPEN

R3. REPORT the OPEN marks in one block, or "no gaps". ASK "Write the document now with these marks, or go back to a section?" Going back routes as in R1 and returns here; the user's word to write is final, whatever the count.

R4. WRITE the state file with `phase: output`, `next: W1`, and `open` as recorded, and return to SKILL.md step 1.
</instructions>
