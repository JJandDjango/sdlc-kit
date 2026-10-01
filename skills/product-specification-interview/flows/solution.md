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
after every step. The engineer seat answers S1 to S7, and both seats
answer S8; with no engineer seat the eight are skipped. Dispatched by
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
Answers live in the state file under `answers`, by the key each step
names.
</context>

<instructions>
Each step S1-S11 ends the same way: SUMMARIZE the section in two lines, ASK "correct?", WRITE the section into the document under its heading and tag, then WRITE the state file with the section's answers and `next` set to the following step.

S1. SCOPE - When `seats.engineer` is null: the interview skips the solution half's steps S1 to S8, its checks and its signature. Their sections stay as r1 wrote them, "(not yet asked)" or the material O5 confirmed, with one exception: WRITE into the document, under Out of scope, each place Q9 sorted into `answers.out_of_scope`, marked `(from the PO seat, not confirmed)`. This step adds no line to `open`, since ready check 8 has marked the missing seat OPEN. WRITE the state file with `next: S9`, and go to S9. Else ASK the engineer seat "Which files and directories does the build change?" Record `answers.scope` (list of paths).

S2. OUT OF SCOPE - SHOW each place Q9 sorted into `answers.out_of_scope` and ASK the engineer seat to confirm it. Then ASK "Which places will the build leave untouched?" For each refusal ASK "Is that a thing we will not build, or a place we will not touch?" A place we will not touch stays here; a thing we will not build goes to `answers.non_goals` and lands in the document under Non-goals; that write lands in the signed request half, so it adds a text row, and the interview asks the PO seat to sign again. Record `answers.out_of_scope` (list).

S3. INTERFACES - ASK "What does a user or a caller see: each command, option, output and message, drawn as it will appear?" Then ASK for the endpoint table when there is one (method, path, request, response per row). Record `answers.interfaces`. This step is the seam where a domain module would add its questions; modules are deferred (ADR 0028).

S4. SOURCES - ASK "Where is each fact the feature shows read from, and which source wins when two disagree?" Take one fact at a time. Record `answers.sources: [{fact, read_from, when_two_disagree}]`; the document shows one row per fact.

S5. CONSTRAINTS - ASK "Which constraints must hold?" Record `answers.constraints` (list).

S6. UNITS - ASK for the units one at a time, and each unit's fields one question at a time: its id; the checks it delivers by their ids in `answers.checks` (`+` joins two that share a sketch); its done means in one sentence; its tests, by check id and kind (automated, or a manual receipt and what it is); and what it retires, which is what it removes, replaces or leaves with no caller, and the tests that pin it, or "none". Probe a check that stands in no unit or in two, and a unit that delivers no check. Record `answers.units: [{id, checks, done_means}]`; each entry also holds `tests` and `retirements`. The document shows one row per unit under the columns Unit, Checks, Done means, Tests by check id and kind, Retirements, and intake copies the done means word for word.

S7. ORDER - ASK "In what order are the units built, and why?" Record `answers.order`.

S8. RISKS AND COST - ASK "What can go wrong, and what does the build cost?" Both seats answer. Record `answers.risks_and_cost`.

S9. DECISIONS AND OPEN QUESTIONS - ASK "Which questions came up, and which have a decided answer?" Record `answers.decisions: [{q, a}]`; an undecided question gets `a: OPEN` and a line in `open`.

S10. LINKS OUT - ASK "Which tickets, decisions and documents does a reader follow from here?" Record `answers.links_out` (list).

S11. NOTES - ASK "Anything else the document must carry?" Record `answers.notes`. WRITE the state file with `phase: solution`, `next: E1`, or with no engineer seat `phase: output`, `next: W1`, and return to SKILL.md step 1.
</instructions>
