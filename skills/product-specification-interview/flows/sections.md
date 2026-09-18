---
name: spec-interview-flow-sections
description: The Sections flow of /sdlc:product-specification-interview - the template's sections in order, one question at a time, the state file written after every section.
---

<purpose>
The Sections flow of `/sdlc:product-specification-interview`: the
template's sections in order, Feature statement through Additional
Notes, one question at a time, with a summary and a state write after
every section. Dispatched by {skill-dir}/SKILL.md at the step `next`
names; its constraints and criteria bind here. {skill-dir} is the
directory holding SKILL.md.
</purpose>

<context>
Rules in force for every step:
- Ask one question; wait for the answer. When O4 recorded material for
  the section, SHOW it and ASK to confirm or change instead of asking
  afresh.
- Quantify vague terms: "fast" becomes a number and a unit; "many"
  becomes a count.
- Probe a thin answer once; then record it with `thin: true` and move
  on.
- A pause ("pause", "later", "stop") writes the state file with `next`
  unchanged and returns to SKILL.md step 3.
Answers live in the state file under `answers.{section}` as named in
each step.
</context>

<instructions>
Each step Q1-Q12 ends the same way: SUMMARIZE the section in two lines, ASK "correct?", then WRITE the state file with the section's answers and `next` set to the following step.

Q1. FEATURE STATEMENT - ASK for the user story in the template's form: "As a {role}, I want {capability}, so I can {outcome}." Probe until the outcome clause names a state of the world, not a feature. Record `answers.feature_statement: {role, capability, outcome}`.

Q2. DESCRIPTION - ASK "What is the feature, in prose?" Record `answers.description`.

Q3. BACKGROUND - ASK "Why now? What history and links does a reader need?" Record `answers.background`.

Q4. SUCCESS CRITERIA - ASK for success criteria one at a time: "One line, an outcome a test can decide. SC1?" Each criterion becomes one decomposition unit at intake, so probe a line that names an activity instead of an outcome. The document wants three to five: below three, ASK whether the feature is a slice of a larger one or a bug fix, record the answer, and go on. Stop asking at five. When the user offers a sixth, REPORT "Six criteria is two features. Which criteria form the second document?" and record the answer under `answers.split`; the interview goes on with the kept set. Record `answers.success_criteria: [{id: SC1, text}]`.

Q5. REQUIREMENTS - Three questions in turn. First the standing line: "Not in scope: 'No new authorizations are added.' Still true for this feature?" Then: "What else is out? The test: would an engineer plausibly build it, or a stakeholder expect it? If nobody would wonder, it does not belong here." Then: "Which constraints must hold?" Record `answers.not_in_scope` (list, the standing line first when it holds) and `answers.requirements` (list).

Q6. PREVIOUSLY DEFINED - ASK "Which existing operations and permission rules does this feature touch?" Record `answers.previously_defined` (list).

Q7. PREREQUISITES - ASK "What must exist first: a permission, a role, another ticket?" Record `answers.prerequisites: [{item, exists}]`.

Q8. BUSINESS REQUIREMENTS - Three questions in turn: the additions, the subtractions, the error messages (each message verbatim). Record `answers.business_requirements: {additions, subtractions, error_messages}`.

Q9. IMPLEMENTATION - When `seats.engineer` is null: record `answers.implementation: null`, add "Implementation: left for intake (no engineer seat)" to `open`, WRITE the state file with `next: Q10`, and go to Q10. Else ASK the engineer's three answers in turn: which files change, in what order, which tests prove it. Then ASK for the endpoint table when there is one (method, path, request, response per row). Record `answers.implementation: {files, order, tests, endpoints}`. This step is the seam where a domain module would add its questions; modules are deferred (ADR 0028).

Q10. MISC - ASK "Which questions came up, and which have a decided answer?" Record `answers.misc: [{q, a}]`; an undecided question gets `a: OPEN` and a line in `open`.

Q11. ACCEPTANCE CRITERIA - For each success criterion in turn, ASK for two or three scenarios: "Scenario name; Given; When; Then." Probe a Then that names no observable outcome. Record `answers.scenarios: [{sc, name, given, when, then}]`.

Q12. ADDITIONAL NOTES - ASK "Anything else the document must carry?" Record `answers.additional_notes`. WRITE the state file with `phase: readiness`, `next: R1`, and return to SKILL.md step 1.
</instructions>
