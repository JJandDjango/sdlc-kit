---
name: product-specification-interview
description: Write an intake-ready feature document through a one-question-at-a-time interview - the raw request /sdlc intake consumes. Resumable, with an advisory readiness check; writes only the document and its state file.
argument-hint: "[slug]"
---

# `/sdlc:product-specification-interview` - write the feature document

<purpose>
Write the consumer's feature document, the raw request `/sdlc intake`
consumes (ADR 0026, ADR 0028), through a structured interview: the
template's sections one question at a time, state saved after every
section, an advisory readiness check, then the document in the
template's shape at a path the user confirms. The skill sits upstream
of G0 and adds no gate condition. This file dispatches; the flow files
execute; the constraints and criteria here bind inside every flow.
</purpose>

<variables>
| Variable | Description | Default |
|---|---|---|
| `$1` | Feature slug matching `^[a-z][a-z0-9-]{2,63}$`; names the document and its state file, which is found by `REQUEST_{slug}_*.state.yaml` at the repo root | asked when absent |
</variables>

<context>
Runs in the consumer repo's Claude Code session; cwd is the repo root.
{skill-dir} is the directory holding this file:
  {skill-dir}/flows/opening.md    O1-O6: path, origin, title, seats, materials; the state file written from O1 on
  {skill-dir}/flows/sections.md   Q1-Q12: the template's sections in order, one question at a time
  {skill-dir}/flows/readiness.md  R1-R4: readback, advisory check, OPEN marks
  {skill-dir}/flows/output.md     W1-W5: render, write (no-clobber), Google Docs form, name the next command
  {skill-dir}/templates/feature-document.md.template

Files: the document, `REQUEST_{slug}_{date}.md` by default at the repo
root (the user confirms the path in O1), and beside it the state file
`REQUEST_{slug}_{date}.state.yaml` (YAML: `phase`, `next`, `origin`,
`title`, `seats`, `path`, `answers`, `open`, `history`). The state file
is the only memory between runs: every flow reads it on entry and
writes it after every answered step, so a later run resumes at the
exact step `next` names.

The template is the consumer's own (ADR 0026; the 2026-09-10 mapping):
revision table; title as the Jira key; Seats line; Feature statement;
Description; Background Information; Success Criteria; Requirements
with "Not in scope" on top; Previously Defined; Prerequisites; Business
Requirements; Implementation; Misc.; Acceptance Criteria (Gherkin
grouped under each success criterion); Additional Notes.

Domain modules, the ancestor skill's question packs, are deferred (ADR
0028); the seam is Q9 in sections.md, after Business Requirements.
Interview disciplines in force in every flow: one question at a time;
quantify vague terms; probe a thin answer once, then mark it and move
on; summarize after each section.
</context>

<instructions>
0. DISPATCH on the argument. PARSE `$1` as the slug; ASK for it when absent or when it fails the pattern. LOAD the state file with one Bash call `ls REQUEST_{slug}_*.state.yaml` at the repo root. Exactly one file resumes; none starts a new run; two or more means ASK which one (AskUserQuestion).
1. ROUTE by the state file's `phase`, and EXECUTE the flow from the step `next` names (a new run starts at O1): `opening` - LOAD {skill-dir}/flows/opening.md; `sections` - LOAD {skill-dir}/flows/sections.md; `readiness` - LOAD {skill-dir}/flows/readiness.md; `output` - LOAD {skill-dir}/flows/output.md; `complete` - REPORT the document path and `/sdlc intake {path}`, then return.
2. EXECUTE the loaded flow's steps in order, exactly as written there. A flow ends by writing `phase` and `next` to the state file and returning here; step 1 routes again until `complete` or the user pauses.
3. REPORT at every pause and at the end: the state file path, the phase, the step to resume at, and after output the document path and `/sdlc intake {path}`. A failed step returns control to the conversation with the failure stated in one line - never a silent stop.
</instructions>

<constraints>
- Write ONLY the document and its state file. Never write under `specs/`, never run `/sdlc intake`, never edit an existing document.
- Never overwrite: an existing file at the document path is reported and another path asked for; only this skill rewrites the state file, and only in place.
- The readiness check advises and never blocks: the document is the requester's; gaps are marked OPEN and the user decides.
- Ask one question at a time; wait for the answer; never batch sections.
- Do NOT chain shell commands - every Bash call is a single segment: no pipes, no semicolons, no `&&`, no redirects.
- No domain modules, no Drive or Jira writes, no formats beyond Markdown and the Google Docs form.
- A failed engine or missing file returns control to the conversation with the failure stated in one line - never a silent stop.
</constraints>

<criteria>
- [ ] Dispatch honored: the slug parsed or asked; the state file found by the `ls` pattern; one file resumes at `next` in whatever phase, none starts at O1, several ask.
- [ ] Every flow loaded from its own file under {skill-dir}/flows/ before it runs.
- [ ] State written after every section; a later run resumes at the exact step.
- [ ] The document lands in the template's shape at the confirmed path; no overwrite; `specs/` untouched.
- [ ] The final report names `/sdlc intake {path}`.
- [ ] Every Bash call a single segment.
</criteria>
