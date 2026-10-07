---
name: product-specification-interview
description: Write an intake-ready feature document through a one-question-at-a-time interview - the raw request /sdlc intake consumes. Resumable, with advisory checks before each seat signs its half; writes only the document and its state file.
argument-hint: "[id]"
---

# `/sdlc:product-specification-interview` - write the feature document

<purpose>
Write the consumer's feature document, the raw request `/sdlc intake`
consumes (ADR 0028, ADR 0029), through a structured interview: the
ratified sections one question at a time, the document written as r1 at
the close of the opening and each section written into it as its step
closes, state saved after every step, and the checks before each seat
signs its half. The skill sits upstream of G0 and adds no gate condition. This file
dispatches; the flow files execute; the constraints and criteria here
bind inside every flow.
</purpose>

<variables>
| Variable | Description | Default |
|---|---|---|
| `$1` | Feature id matching `^[a-z][a-z0-9-]{2,63}$`; names the document `docs/features/{id}.md` and its state file `docs/features/{id}.state.yaml` | asked when absent |
</variables>

<context>
Runs in the consumer repo's Claude Code session; cwd is the repo root.
{skill-dir} is the directory holding this file:
  {skill-dir}/flows/opening.md    O1-O6: id, origin, title, seats, materials; the state file from O1 on, the document as r1 at O6
  {skill-dir}/flows/request.md    Q1-Q15: the request half in order, one question at a time, then Terms and the Gherkin step
  {skill-dir}/flows/solution.md   S1-S11: the solution half in order, then the record's authored sections
  {skill-dir}/flows/signing.md    P1-P7, E1-E7: the checks before each seat signs its half, then the signature
  {skill-dir}/flows/output.md     W1-W2: Google Docs form, name the next command
  {skill-dir}/templates/requirements-document.md.template

Files: the document at `docs/features/{id}.md`, and beside it the state
file `docs/features/{id}.state.yaml` (YAML, `schema:
spec-interview-state/2`: `id`, `phase`, `next`, `origin`, `title`,
`seats`, `answers`, `open`, `history`). The state file is the only memory
between runs: every flow reads it on entry and writes it after every
answered step, so a later run resumes at the exact step `next` names.

The template is the requirements document of ADR 0037, which amends
ADR 0029's format: the revision table with numbered rows; the title line
`# {id} - {title}`; a status line that names the PO seat; then the
request half's sections, each heading followed by its tag, owner and
kind (`[PO seat · authored]`, or derived with its stamp,
`[PO seat · derived from r{n}]`). The request half (Statement,
Description, Background with Existing behavior touched, Success
criteria, Non-goals, Prerequisites, Acceptance criteria with Checks and
Error messages) comes first, and the PO seat signs it. Then follow
Decisions and open questions, Notes, and the Appendix with Gherkin and
Terms. The document holds no solution half, no Traceability, no
Contract block and no line between halves. The Gherkin
carries no stamp until its step writes it. The four
bug-fix sections (Findings at a glance, Findings, Why this happened,
Regression check) stand only in a bug fix's document.

Domain modules, the ancestor skill's question packs, are deferred (ADR
0028); the seam is the solution flow, solution.md. Interview disciplines
in force in every flow: one question at a time; quantify vague terms;
probe a thin answer once, then mark it `probed: true` and move on;
summarize after each section.
</context>

<instructions>
0. DISPATCH on the argument. PARSE `$1` as the feature id; ASK for it when absent or when it fails the pattern. LOAD the state file with one Bash call `ls docs/features/{id}.state.yaml` at the repo root. Exactly one file resumes; none starts a new run at O1.
   A state file at the old `REQUEST_{slug}_*.state.yaml` path is never read: a run for that id starts fresh.
1. ROUTE by the state file's `phase`, and EXECUTE the flow from the step `next` names (a new run starts at O1): `opening` - LOAD {skill-dir}/flows/opening.md; `request` - LOAD {skill-dir}/flows/request.md, or {skill-dir}/flows/signing.md when `next` names a P step; `solution` - LOAD {skill-dir}/flows/solution.md, or {skill-dir}/flows/signing.md when `next` names an E step; `output` - LOAD {skill-dir}/flows/output.md; `complete` - REPORT the document path, the state file path and the design run's command, `/sdlc:product-specification-interview {id} design`, then OFFER the way back to a section: for a section the seat names, EXECUTE its step from {skill-dir}/flows/request.md and WRITE the state file with `phase: request`, `next: P1`, so the checks run again and the PO seat signs again; else return.
2. EXECUTE the loaded flow's steps in order, exactly as written there. After O6 writes r1, WRITE each section into the document as its step closes, in the template's place under its heading and tag; a section with nothing to say reads "(none)", and one no step has written yet reads "(not yet asked)". A flow ends by writing `phase` and `next` to the state file and returning here; step 1 routes again until `complete` or the user pauses.
3. REPORT at every pause and at the end: the state file path, the phase, the step to resume at, and after output the document path and `/sdlc:product-specification-interview {id} design`. A failed step returns control to the conversation with the failure stated in one line - never a silent stop.
</instructions>

<constraints>
- Write ONLY the document and its state file. Never write under `specs/`, never run `/sdlc intake`, and never write a `Ready:` or `Parked:` row: intake writes those.
- Every revision row opens `r{n}: `, numbered one past the table's last row; a section's step adds no row, with one exception: a write into a half after its seat signed adds a text row, `r{n}: {what changed}`, and the interview asks that seat to sign again, with a new `Signed:` row right after it: `r{n}: Signed: request half. The PO seat signs r{m}` or `r{n}: Signed: solution half. The engineer seat signs r{m}`, where r{m} is that text row. The seat's word stands: a seat that declines keeps its older signature, and the interview names the revision it covers.
- Each text row the interview writes moves the Gherkin block's stamp to that row, once every check changed since the last stamp has a confirmed scenario again. A row written by hand moves no stamp, so the checks before signing report the block stale.
- Never overwrite: an existing document at the opening is reported and another id asked for; only this skill rewrites the document and the state file, and only in place.
- A section changed by hand since the interview last wrote it is shown beside the answer, and the seat says which stands; never overwrite a hand edit silently.
- The checks before signing advise and never block: the document is the requester's; gaps are marked OPEN, and the seat's word to sign, or to write, stands whatever the count.
- Ask one question at a time; wait for the answer; never batch sections.
- Do NOT chain shell commands - every Bash call is a single segment: no pipes, no semicolons, no `&&`, no redirects.
- No domain modules, no Drive or Jira writes, no formats beyond Markdown and the Google Docs form.
- A failed engine or missing file returns control to the conversation with the failure stated in one line - never a silent stop.
</constraints>

<criteria>
- [ ] Dispatch honored: the id parsed or asked; the state file found at its one path; a hit resumes at `next` in whatever phase, none starts at O1.
- [ ] Every flow loaded from its own file under {skill-dir}/flows/ before it runs.
- [ ] State written after every step; a later run resumes at the exact step.
- [ ] The document lands at `docs/features/{id}.md` as r1 in the template's format, and each section lands as its step closes; no overwrite; `specs/` untouched.
- [ ] Each half's checks ran before its seat was asked to sign, and each run landed as a `Measured:` row; no seat was blocked.
- [ ] The final report names the design run's command.
- [ ] Every Bash call a single segment.
</criteria>
