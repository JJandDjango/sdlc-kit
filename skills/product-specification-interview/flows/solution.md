---
name: spec-interview-flow-solution
description: The Solution flow of /sdlc:product-specification-interview - the solution half's sections in order, then the record's authored sections, one question at a time; the document and the state file written as each step closes.
---

<purpose>
The Solution flow of `/sdlc:product-specification-interview`: the
solution half's sections in the template's order, Scope through Risks
and cost, then the record's authored sections (Decisions and open
questions, Links out, Notes), one question at a time, each section
written into the document as its step closes and the state file written
after every step. Consult cases stands between the two, at S9. A design
run asks the twelve steps, and the engineer seat answers each of them
alone. Dispatched by
{skill-dir}/SKILL.md at the step `next` names; its constraints and
criteria bind here. {skill-dir} is the directory holding SKILL.md.
</purpose>

<context>
Rules in force for every step:
- Ask one question; wait for the answer. When O5 recorded material for
  the section, SHOW it and ASK to confirm or change instead of asking
  afresh. An answer that conflicts with the material is asked, never
  settled silently: "The material says X; you said Y. Which stands?"
- Quantify vague terms: "fast" becomes a number and a unit; "many"
  becomes a count.
- Probe a thin answer once; then record it with `probed: true` and move
  on.
- A step adds no revision row: it writes its section in place, under
  the heading and tag r1 laid down. One exception, from SKILL.md's
  constraints: a write into a half after its seat signed adds a text
  row, and the interview asks that seat to sign again.
- A pause ("pause", "later", "stop") writes the state file with `next`
  unchanged and returns to SKILL.md step 3.
- The document is the design document, `docs/features/{id}.design.md`,
  and the state file the design run's own,
  `docs/features/{id}.design.state.yaml`. The requirements document and
  the requirements run's state file are read and never written.
Answers live in the state file under `answers`, by the key each step
names.
</context>

<instructions>
Each step S1-S12 ends the same way: SUMMARIZE the section in two lines, ASK "correct?", WRITE the section into the document under its heading and tag, then WRITE the state file with the section's answers and `next` set to the following step.

S1. SCOPE - ASK the engineer seat "Which files and directories does the build change?" Record `answers.scope` (list of paths).

S2. OUT OF SCOPE - READ the requirements run's state file, `docs/features/{id}.state.yaml`, and SHOW the engineer seat each place the PO seat refused at Non-goals, its `answers.out_of_scope`; ASK the seat to confirm each. With no such state file, show no refused places and say so. Then ASK "Which places will the build leave untouched?" For each refusal ASK "Is that a thing we will not build, or a place we will not touch?" A place we will not touch stays here. A thing we will not build is for the PO seat: WRITE it under the design document's Decisions and open questions as `OPEN: a non-goal for the PO seat: {thing}`, add the line to `open`, and write nothing in the requirements document. Record `answers.out_of_scope` (list).

S3. INTERFACES - ASK "What does a user or a caller see: each command, option, output and message, drawn as it will appear?" Then ASK for the endpoint table when there is one (method, path, request, response per row). Record `answers.interfaces`. This step is the seam where a domain module would add its questions; modules are deferred (ADR 0028).

S4. SOURCES - ASK "Where is each fact the feature shows read from, and which source wins when two disagree?" Take one fact at a time. Record `answers.sources: [{fact, read_from, when_two_disagree}]`; the document shows one row per fact.

S5. CONSTRAINTS - ASK "Which constraints must hold?" Record `answers.constraints` (list).

S6. UNITS - ASK for the units one at a time, and each unit's fields one question at a time: its id; the checks it delivers by their ids in the requirements document's Checks (`+` joins two that share a sketch); its done means in one sentence; its tests, by check id and kind (automated, or a manual receipt and what it is); and what it retires, which is what it removes, replaces or leaves with no caller, and the tests that pin it, or "none". Probe a check that stands in no unit or in two, and a unit that delivers no check. Record `answers.units: [{id, checks, done_means}]`; each entry also holds `tests` and `retirements`. The document shows one row per unit under the columns Unit, Checks, Done means, Tests by check id and kind, Retirements, and intake copies the done means word for word.

S7. ORDER - ASK "In what order are the units built, and why?" Record `answers.order`.

S8. RISKS AND COST - ASK the engineer seat "What can go wrong, and what does the build cost?" Record `answers.risks_and_cost`.

S9. CONSULT CASES - ASK the engineer seat the four cases, one case per question, in this order: "Case {k}: {case}. Does it hold for this design: yes or no?" Record each answer as `yes` or `no`. A `yes` takes two more questions, one at a time: "Who was asked?" and then "What was decided?" Record `answers.cases: [{case, answer, asked, decided}]`, and WRITE the state file after each case, so a pause resumes at the first case with no entry. The document shows one row per case, and a `yes` row shows who was asked and what was decided:
   | Case | Answer | Who was asked | What was decided |
   | :-- | :-: | :-- | :-- |
   | 1. An ambiguity in the requirements | {answer} | {asked} | {decided} |
   | 2. More than one solution | {answer} | {asked} | {decided} |
   | 3. A solution unconventional to the codebase | {answer} | {asked} | {decided} |
   | 4. A change to a public contract: routes, a gateway definition, events, a schema | {answer} | {asked} | {decided} |
   A `no` row leaves its last two cells empty.

S10. DECISIONS AND OPEN QUESTIONS - ASK "Which questions came up, and which have a decided answer?" Record `answers.decisions: [{q, a}]`; an undecided question gets `a: OPEN` and a line in `open`. An `OPEN:` line S2 wrote under the heading stays when S10 writes the section.

S11. LINKS OUT - ASK "Which tickets, decisions and documents does a reader follow from here?" Record `answers.links_out` (list).

S12. NOTES - ASK "Anything else the document must carry?" Record `answers.notes`. WRITE the state file with `phase: solution`, `next: E1`, and return to SKILL.md step 1.
</instructions>
