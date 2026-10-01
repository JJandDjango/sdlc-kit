---
name: spec-interview-flow-request
description: The Request flow of /sdlc:product-specification-interview - the request half's sections in order, one question at a time, then Terms and the Gherkin step; the document and the state file written as each step closes.
---

<purpose>
The Request flow of `/sdlc:product-specification-interview`: the request
half's sections in the template's order, Statement through Acceptance
criteria, one question at a time, each section written into the document
as its step closes and the state file written after every step. Terms
and the Gherkin step close the half: the PO seat owns both, and the
checks before signing read the terms. Dispatched by {skill-dir}/SKILL.md
at the step `next` names; its constraints and criteria bind here.
{skill-dir} is the directory holding SKILL.md.
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
Each step Q1-Q15 ends the same way: SUMMARIZE the section in two lines, ASK "correct?", WRITE the section into the document under its heading and tag, then WRITE the state file with the section's answers and `next` set to the following step.

Q1. STATEMENT - ASK for the statement in one sentence, in the form "As a {role}, I want {capability}, so that {outcome}." Probe until the outcome clause names a state of the world, not a feature. Record `answers.statement` (one text).

Q2. DESCRIPTION - ASK "What is the feature, in prose?" Record `answers.description`.

Q3. FINDINGS AT A GLANCE - Only when `origin` is `bug-fix`; for a feature WRITE the state file with `next: Q4` and go to Q4. ASK "What failed, for whom, and since when? Three lines at most." The document shows the incident reference O2 recorded above the answer. Record `answers.findings_at_a_glance`.

Q4. BACKGROUND - ASK "Why now? What history and links does a reader need?" Record `answers.background`.

Q5. EXISTING BEHAVIOR TOUCHED - ASK "Which behavior that stands today does this feature touch?" Take one entry at a time, and for each ASK the file or step it was read from; probe an entry with no source. Each entry gets a regression check at Q11. Record `answers.existing_behavior: [{text, source}]`.

Q6. FINDINGS - Only when `origin` is `bug-fix`; for a feature WRITE the state file with `next: Q7` and go to Q7. ASK "What did the investigation find?" Take one finding at a time, each with its evidence. Record `answers.findings` (list).

Q7. WHY THIS HAPPENED - Only when `origin` is `bug-fix`; for a feature WRITE the state file with `next: Q8` and go to Q8. ASK "What caused it, and what let it through?" Record `answers.why_this_happened`.

Q8. SUCCESS CRITERIA - ASK for success criteria one at a time: "One line, an outcome a test can decide. SC1?" Probe a line that names an activity instead of an outcome. The document wants three to five: below three, ASK whether the feature is a slice of a larger one or a bug fix, record the answer, and go on. Stop asking at five. When the user offers a sixth, REPORT "Six criteria is two features. Which criteria form the second document?" and record the answer under `answers.split`; the interview goes on with the kept set. Record `answers.success_criteria: [{id: SC1, text}]`.

Q9. NON-GOALS - First the standing line: ASK "Non-goal: 'No new authorizations are added.' Still true for this feature?" Then ASK "What else is out? The test: would an engineer plausibly build it, or a stakeholder expect it? If nobody would wonder, it does not belong here." For each refusal ASK "Is that a thing we will not build, or a place we will not touch?" A thing we will not build goes to `answers.non_goals`; a place we will not touch goes to `answers.out_of_scope`, which S2 shows the engineer seat. Record `answers.non_goals` (list, the standing line first when it holds).

Q10. PREREQUISITES - ASK "What must exist first: a permission, a role, another ticket?" Record `answers.prerequisites: [{item, exists}]`.

Q11. CHECKS - For each success criterion in turn, ASK for its two or three checks, one at a time: "One testable line under SC{n}, opening with 'verify'. SC{n}.1?" Probe a check that names no outcome a test can observe. Then, for each entry of `answers.existing_behavior`, ASK which check carries its regression check, and take a new check when none does. Record `answers.checks: [{id, text}]`; the document lists the checks under their criterion, each on a line `- SC{n}.{m}: verify ...`.

Q12. ERROR MESSAGES - ASK for the error messages the feature shows, one at a time, each verbatim and with the check it serves. Record `answers.error_messages` (list, each message verbatim).

Q13. REGRESSION CHECK - Only when `origin` is `bug-fix`; for a feature WRITE the state file with `next: Q14` and go to Q14. SHOW the regression scenario O2 recorded and ASK "Is this still the case that failed, in one sentence?" A change replaces the top-level `regression`, O2's key; this step records nothing under `answers`.

Q14. TERMS - ASK "Which words does this document use in a sense a reader must be told?" Take one term at a time: its name, then its definition in one sentence. A term that changes the definition of a ratified term carries `amends` with that term's slug. Record `answers.terms: [{name, definition}]`.

Q15. GHERKIN - Derived, once the checks stand: PROPOSE one scenario per check in `answers.checks`, in the checks' order, each joined to its check by the check's id: a line `Scenario: {id} {name}`, then its Given, When and Then lines. Every fact in a scenario comes from its check. A scenario whose Then needs a fact its check lacks is never shown: the check is a thin check instead, with the reason `its Then needs {fact}`. SHOW the other scenarios one at a time and ASK the PO seat to accept, change or drop each; a change is held to the same rule, and a changed scenario the PO seat then accepts counts as confirmed. A scenario the PO seat drops makes its check a thin check, with the reason `scenario dropped`. Record `answers.gherkin: [{check, name, given, when, then, status}]`, the status `accepted`, `changed` or `dropped`, and WRITE the state file after each scenario, so a pause resumes at the first check with neither an entry nor a thin mark.
   For a thin check, WRITE into the document, under its line in Checks, `OPEN: Ready check 3: {id} is thin: {reason}.`; record `thin: {reason}` on its `answers.checks` entry and the OPEN line in `open`; REPORT `Ready check 3: {gap}. Marked OPEN.`
   When every check has its answer, WRITE the Gherkin block into the document under its heading: the tag `[PO seat · derived from r{n}]`, where r{n} is the newest revision, the highest `rN` of a row that opens on none of `Ready:`, `Measured:`, `Signed:` or `Parked:`; then each scenario with the status `accepted` or `changed`, in the checks' order.
   At the signature of the request half, a check with no confirmed scenario carries an OPEN. Before the hand-off, READ `answers.gherkin`: for each check that is not thin and has no `accepted` or `changed` scenario, WRITE into the document, under its line in Checks, `OPEN: Ready check 3: {id} has no confirmed scenario.`, add the line to `open`, and REPORT it in the same form. Then WRITE the state file with `phase: request`, `next: P1`, and return to SKILL.md step 1.
</instructions>
