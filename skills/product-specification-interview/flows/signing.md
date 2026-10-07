---
name: spec-interview-flow-signing
description: The Signing flow of /sdlc:product-specification-interview - the checks before each seat signs its half, a Measured row for each run, then the Signed row; the checks advise and never block.
---

<purpose>
The Signing flow of `/sdlc:product-specification-interview`: the checks
before each seat signs its half, then the signature. P1 to P7 run before
the PO seat signs the request half; E1 to E7 run before the engineer seat
signs the solution half. Each run shows the draft check's lines, reads
the half's ready checks, reports stale blocks, and lands as a `Measured:`
row; the seat's word then signs or goes back (ADR 0034). Dispatched by
{skill-dir}/SKILL.md at the step `next` names; its constraints and
criteria bind here. {skill-dir} is the directory holding SKILL.md.
</purpose>

<context>
The checks advise and never block: the seat's word to sign, or to write,
stands whatever the count of findings and OPEN marks.
- A ready check is asked, never parsed: the interview reads the document
  against the question. A gap is marked inline in its section, as
  `OPEN: Ready check {n}: {gap}.`; the line is added to the state file's
  `open`; and the interview reports `Ready check {n}: {gap}. Marked OPEN.`
  A gap that already carries its mark is never marked twice and counts
  once; a gap the seat's answer closes loses its mark and its line in
  `open`.
- Each seat's checks and rows stand in that seat's own document. P1 to
  P7 read and write the requirements document, `docs/features/{id}.md`,
  and the requirements run's state file; E1 to E7 the design document,
  `docs/features/{id}.design.md`, and the design run's state file. No E
  step changes a line of the requirements document or of the
  requirements run's state file.
- The newest revision is the highest `rN` of a row that opens on none of
  `Ready:`, `Measured:`, `Signed:` or `Parked:`.
- A derived block is stale when its tag's `derived from r{n}` stands
  below the newest revision. The report reads `{block} is stamped r{n};
  the newest revision is r{m}. Stale.`, with `{block}` the block's name. A
  requirements document holds one derived block, `Gherkin`; `Contract`
  and `Record` stand in a design document. Before intake the Contract and the Record carry
  no stamp and are never stale.
- A half's checks are one run, P1 to P5 or E1 to E5. `next` stays at the
  run's first step until the `Measured:` row is written: a pause
  ("pause", "later", "stop") writes the state file with `next` unchanged
  and returns to SKILL.md step 3, so a pause inside a run resumes at that
  first step. Inside a run the state file takes only the lines added to
  `open`.
- Each row the flow writes is numbered one past the table's last row,
  and carries today's date and, in its Revised By cell, the half's seat:
  `seats.po` for the request half, `seats.engineer` for the solution
  half.
- The interview never writes a `Ready:` or `Parked:` row, and writes
  nothing under `specs/`.
</context>

<instructions>
P1. DRAFT CHECK - RUN one Bash call `python -m taskcontract lang-check --draft docs/features/{id}.state.yaml` at the repo root and SHOW its lines as printed. The command reads the state file, never the document, and writes nothing: it runs the new terms of `answers.terms` as drafts through the vocabulary check and CL003, and a draft contract of the statement, the non-goals and the checks through the language check. It exits 1 when a finding is an error: a result, never a failed step, and the interview reads the lines either way. HOLD the findings part of the command's last line, the words after its last semicolon, for P5. When the state file cannot be read, the last line is a `CL000` line, not a `draft:` line: HOLD the line from `CL000` on as the findings part, as in `CL000 unreadable draft: {reason}`, so the `Measured:` row still records the run.

P2. EXISTING BEHAVIOR - READ each entry of `answers.existing_behavior` against the file or step its `source` names. The source wins. An entry that no longer holds gets an OPEN under ready check 6: WRITE into the document, under the entry in Existing behavior touched, `OPEN: Ready check 6: {entry} no longer holds: {what the source says}.`, add the line to `open`, and REPORT it in the report's form. An entry with no `source` cannot be read: P3 marks it, a gap under ready check 6.

P3. READY CHECKS - READ the document against ready checks 1 to 8, each a question, and mark each gap as the context says:
   1. Does the statement's outcome clause name a state of the world?
   2. Are there three to five success criteria, one line each, each an outcome a test can decide?
   3. Does every criterion hold two or three checks, each with an id, none marked thin? A thin check, and a check with no confirmed scenario, carries its OPEN from Q15.
   4. Does Non-goals hold the standing line and at least one line specific to this feature?
   5. Is every prerequisite marked exists or missing, and does a missing one name its ticket or owner?
   6. Is Existing behavior touched listed, or does it say "none", and does every entry name the file or step it was measured from and have a regression check? An OPEN from P2 counts here.
   7. Is every error message a check rejects with written verbatim?
   8. Is the PO seat named, and for a bug fix does a `Measured:` row for the findings fall inside the consumer's window?

P4. STALE BLOCKS - READ each derived block's stamp against the newest revision. REPORT each stale block with its message.

P5. MEASURED ROW - WRITE into the document the row `r{n}: Measured: the checks before signing, on the request half: {findings}; ready checks 1 to 8: {count} OPEN`. `{findings}` copies the findings part of the command's last line, as in `4 findings (CL003 1, CL008 1, CL012 1, CL014 1)`; `{count}` is the number of OPEN marks that stand under ready checks 1 to 8. Each run of the checks writes one row. Then WRITE the state file with `next: P6`.

P6. SIGN OR GO BACK - REPORT the OPEN marks that stand, in one block, or "no gaps". ASK the PO seat "Sign the request half now, or go back to a section?" The seat's word to sign stands, whatever the count: WRITE the state file with `next: P7` and go to P7. To go back, the seat names a section: EXECUTE that section's step from {skill-dir}/flows/request.md, WRITE the state file with `next: P1`, and go to P1, so the command and the ready checks run again. A check changed there loses its entry in `answers.gherkin`: the Gherkin step, Q15, proposes that check's scenario again before the checks run again, so the stamp can move at P7. A seat that declines to sign gets no `Signed:` row: WRITE the state file with `next: P6`, REPORT the step to resume at, and return to SKILL.md step 3.

P7. SIGNATURE - WRITE into the document the text row `r{n}: The request half finished: {sections} sections written, {open} OPEN`, where `{sections}` counts the half's sections written and `{open}` the OPEN marks that stand in the half; the Gherkin block's stamp moves to this row, once every check changed since the last stamp has a confirmed scenario again. Then WRITE into the document, right after the first, with no row between, the row `r{n}: Signed: request half. The PO seat signs r{m}`, where r{m} is that text row. Both rows carry `seats.po` in Revised By. WRITE the state file with `phase: output`, `next: W1` and `history: + {at: now, event: request half signed}`, and return to SKILL.md step 1.

E1. DRAFT CHECK - RUN one Bash call `python -m taskcontract lang-check --draft docs/features/{id}.design.state.yaml` at the repo root and SHOW its lines as printed. For this half the run reads each unit's `done_means`, from `answers.units`, through the language check, and reports the copied terms' findings again, since `answers.terms` holds a copy of the requirements document's new terms. Exit 1 is a result, as at P1. HOLD the findings part of the command's last line for E5; a `CL000` line is held from `CL000` on, as at P1.

E2. SCOPE - CHECK Scope against the paths of the release unit's row under Units: each path that row names stands in `answers.scope`, or is a finding. The release unit is the unit that ships the release: its row names the release's own paths, such as a version file. ASK the engineer seat which row it is when the rows leave it unclear. HOLD the result for E5. A document with no release unit skips this check and says so in its `Measured:` row.

E3. READY CHECKS - READ the document against ready checks 11 to 15, each a question, and mark each gap as the context says:
   11. Does every fact a check names have a Sources row, and does every pair of sources that can disagree name its winner?
   12. Does every output kind have a drawn example, with its edges?
   13. Does every unit name its retirements or "none", and list its tests by check id and kind?
   14. Do the checks run before signing read green, or does each finding stand answered in the document?
   15. Does each of the four cases have an answer, and does each yes name who was asked and what was decided?
   A gap under the last question is one of three, each marked under Consult cases as `OPEN: Ready check 15: {gap}.`: `case {k} has no answer`, `case {k} reads yes and names no one asked`, `case {k} reads yes and names no decision`.

E4. STALE BLOCKS - READ each derived block's stamp against the newest revision. REPORT each stale block with its message. A design is stale when the requirements document holds a text revision newer than the one the design names: REPORT `The design names requirements r{n}; the requirements stand at r{m}. Stale.` The seat's word to sign still stands.

E5. MEASURED ROW - WRITE into the design document the row `r{n}: Measured: the checks before signing, on the solution half: {findings}; Scope against the release unit's paths: {scope}; ready checks 11 to 15: {count} OPEN`. `{findings}` and `{count}` read as at P5, the count under ready checks 11 to 15; `{scope}` reads `covered`, or `{paths} outside Scope`, or with no release unit `no release unit, check skipped`. Each run of the checks writes one row. Then WRITE the state file with `next: E6`.

E6. SIGN OR GO BACK - REPORT the OPEN marks that stand, in one block, or "no gaps". ASK the engineer seat "Sign the solution half now, or go back to a section?" The seat's word to sign stands, whatever the count: WRITE the state file with `next: E7` and go to E7. To go back, the seat names a section of the design document: EXECUTE that section's step from {skill-dir}/flows/solution.md, WRITE the state file with `next: E1`, and go to E1, so the command and the ready checks run again. When the seat names a section of the requirements document, REPORT the requirements run's command, `/sdlc:product-specification-interview {id}`, WRITE nothing and ASK the question again: a design run changes no line of the requirements document. A seat that declines to sign gets no `Signed:` row: WRITE the state file with `next: E6`, REPORT the step to resume at, and return to SKILL.md step 3.

E7. SIGNATURE - WRITE into the design document the text row `r{n}: The solution half finished: {sections} sections written, {open} OPEN`, where `{sections}` counts the design document's sections written and `{open}` the OPEN marks that stand in it. Then WRITE into the design document, right after the first, with no row between, the row `r{n}: Signed: solution half. The engineer seat signs r{m}`, where r{m} is that text row. Both rows carry `seats.engineer` in Revised By. E7 changes no line of the requirements document. WRITE the state file with `phase: output`, `next: W1` and `history: + {at: now, event: solution half signed}`, and return to SKILL.md step 1.
</instructions>
