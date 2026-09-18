# 28. The specification interview writes the feature document

Status: accepted
Date: 2026-09-17

## Context

The G0 venue takes a raw request, and 0026 fixed that request's shape:
the consumer's feature document, mapped section by section against the
consumer's own template on 2026-09-10 (revision table, title as the
Jira key, a Seats line, Feature statement, Description, Background,
Success Criteria, Requirements with "Not in scope" on top, Previously
Defined, Prerequisites, Business Requirements, Implementation, Misc.,
Acceptance Criteria as Gherkin grouped under each success criterion,
Additional Notes). Nothing in the kit writes that document: a PO fills
the template by hand or arrives at intake without it.

The user's global skill `product-specification-interview` (v7.2,
fourteen core prompt files and ten personal domain modules) interviews
for a product specification: twelve to thirteen sections, three depths,
domain modules, a pause-and-resume payload, a gate, five output
templates and five output formats. It predates the current PromptLang
rules. Measured 2026-09-17: eleven of the fourteen core files pass the
validator; `interview-full-existing.md` carries a stray closing tag and
4904 tokens against the 4000 cap; `output-core.md` and
`modules/MODULE-SPEC.md` carry placeholder angle-bracket text the parser
reads as tags; the ten domain modules all fail. Its frontmatter name,
`product-spec-interview`, is not the command asked for, and it has no
constraints block. Session 31 ratified twelve features and five
non-goals for bringing it into the kit. The task contract is
`specs/spec-interview/`.

Rulings already on record that bind the design:

- The raw request stays the requester's and is never lexicon-policed
  (0022, 0026). The document stops at Gherkin; unit tests never enter
  it (0026).
- Intake writes only the contract, and the human act at G0 is the I5
  answer per unit, recorded as seats (0025). The human census is fixed
  at six (0015): nothing upstream of G0 becomes a condition.
- Every prompt file validates under PromptLang's 4000-token ceiling,
  one flow per file, dispatch in `SKILL.md` (0025).
- The skill rides the plugin and is never scaffolded into a repo (0016,
  0025); a plugin update replaces the plugin directory.
- Every Bash call is a single segment; writes are no-clobber (the
  `/sdlc` constraints).

## Decision

- **A second plugin skill, `product-specification-interview`.**
  `skills/product-specification-interview/SKILL.md` dispatches; the
  flows live one per file beside it; the command is
  `/sdlc:product-specification-interview [slug]`, installed and updated
  with the kit. The global skill is the ancestor and stays as it is.
  The kit's copy is a re-cut, not a port: the ancestor is product-sized,
  the kit's unit of work is one feature, and nothing in the kit
  consumes a product specification.
- **Its product is the intake-ready feature document.** One Markdown
  file in the ratified template's shape, written to a path the user
  confirms (default `REQUEST_{slug}_{date}.md` at the repo root, the
  kit's own inbox convention), consumed by `/sdlc intake` unchanged. A
  second rendering, paste-ready for Google Docs, on request. The
  Notion, Confluence, and Jira adapters do not carry over.
- **The interview is feature-sized.** The questions follow the
  template's sections: story and background; three to five success
  criteria with two or three Gherkin scenarios each; non-goals under
  the agreed test (would an engineer plausibly build it, or a
  stakeholder expect it); previously defined items and prerequisites;
  business requirements as additions, subtractions, and error messages;
  open questions. One depth replaces lite and full; more than five
  criteria prompts a split into two documents. The opening question
  sets the origin, feature or bug fix; a bug fix collects the incident
  reference and the regression scenario.
- **Seats are asked; Implementation only with the engineer seat.** The
  Seats line names the PO seat and the engineer seat. The
  Implementation section (files, order, proving tests, the endpoint
  table) is asked only when the engineer seat is present; otherwise it
  is left marked for intake.
- **Materials first.** Pasted or pointed-at material is extracted and
  confirmed; only the gaps are asked.
- **Pause and resume.** State saves after every section to a file
  beside the document; a later run resumes at the exact question.
- **The readiness check is advisory.** Before writing, the interview
  reads the document back and checks what intake will need: an
  outcome-shaped story, a non-goal, scenarios under every criterion,
  seats named. Gaps are marked OPEN. The check never blocks: the
  document is the requester's.
- **Domain modules are deferred.** The mechanism returns after the demo
  intake; when it does, modules live in the consumer's repo, never in
  the plugin directory. The flow names the seam.
- **The write surface is the document and its state file.** The skill
  never overwrites an existing document, never touches `specs/`, and
  never runs intake; it ends by naming the `/sdlc intake` command with
  the path. A failed step returns control to the conversation.
- **PromptLang by construction, held by a test.** Every shipped prompt
  file passes `python -m prompt_lang` under the cap; a structural test
  in the suite holds the file set, the frontmatter, the tag set, and
  chain-free command lines, on the operator-defs pattern.
- **It ships in kit 0.13.0 with `playbook-guardrails`.** One release,
  two contracts; 0027's release numbers hold.

Recorded non-goals: no change to `/sdlc intake` (the section-to-field
mapping lands with the demo, 0026); no product-level specification
output or templates; none of the ancestor's ten domain modules ship;
the global skill under `~/.claude/skills` is untouched; no Drive or
Jira writes; no new gate condition.

## Consequences

- The pitch gains its front end: a PO with no knowledge of the template
  gets an intake-ready document, and the demo intake can start from
  the interview.
- USAGE gains a section on writing the feature document, before the
  intake section, authored red at pass zero and flipped green as the
  units land.
- The plugin carries two skills. Consumers are untouched: the skill is
  never scaffolded, so `/sdlc update` has nothing to report.
- The PromptLang receipt grows from eight files; the suite grows by the
  structural test.
- The kit's copy and the ancestor diverge from this day; a fix flows
  between them by hand, and nothing keeps them in step.
- Kit 0.13.0 carries two contracts and one self-pin.
