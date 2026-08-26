---
name: sdlc
description: Lay a spec-first SDLC gate spine into a repository (greenfield or brownfield, no-clobber), then operate it - `intake` (the G0 venue), `new`, `audit`, `update`, and the `vocab` and `lang` families. Pairs with /cairn. Use when starting, adopting, or operating gated agent-driven development.
---

# `/sdlc` - lay a spec-first gate spine

<purpose>
Initialize and operate the SDLC Kit's gate architecture in a target
repository: spec-first gates plus static enforcement so agent-written
code cannot degrade the codebase. A task enters development only through
a ready contract (`specs/{task-id}/contract.yaml`, immutable to
implementers); CI re-validates every contract; gate health is auditable
on demand. The skill interviews the user, then calls zero-dependency
engines.
</purpose>

<context>
Runs in the target repo's Claude Code session; cwd is the target. This
skill's own directory ({skill-dir}, the directory holding this file)
holds the engines, templates, and flows:
  {skill-dir}/init.py       (no-clobber renderer)
  {skill-dir}/audit.py      (report-only health check, exit 0/1/2)
  {skill-dir}/update.py     (scaffold-drift report, per-file apply)
  {skill-dir}/templates/*.template
  {skill-dir}/flows/*.md    (one file per flow, below)

Flows live beside this file, one PromptLang file per subcommand (ADR
0025): init.md, new.md, intake.md, vocab.md, lang.md, audit.md,
update.md. This file dispatches; the flow file executes. The
constraints and criteria here bind inside every flow.

Contract machinery (`python -m taskcontract` + the schemas) comes from
the pip-installed kit:
  pip install "git+https://github.com/JJandDjango/sdlc-kit.git"
The scaffolded CI job installs it itself; local `new`/`validate` and the
vocabulary subcommands (`vocab-list` / `vocab-add` / `vocab-check`) need
it once. If `python -m taskcontract` reports no such module, offer that
install command and continue with whatever needs no validator.

The vocabulary layer (ADR 0017): terms live one-per-file at
specs/vocabulary/{term-slug}.yaml (filename = stable ID), validated at
the door by `vocab-check`; contracts may declare `entities:` refs that
G0 resolves against ratified terms only. Ratification is always a human
act - the status flip is a class-S edit approved in review.

Payload (no-clobber; the two merge targets are printed instead of
written when they already exist):
  SDLC.md - .sdlc/config.yaml - .sdlc/clocks.yaml - .sdlc/reds.yaml -
  specs/README.md - .github/workflows/sdlc.yml -
  .pre-commit-config.yaml - .vscode/settings.json
A stack with a shipped tooling profile overlays additional surfaces
(templates/profiles/{stack}/profile.json, ADR 0018); dotnet's overlay
is the live container, deliberately empty until its G3 slice
(docs/dotnet-profile.md).
</context>

<instructions>
0. DISPATCH. If this skill was invoked with a first argument naming a subcommand, do NOT run the interview:
   - `audit` - LOAD {skill-dir}/flows/audit.md and EXECUTE the Audit flow (A1-A2).
   - `update` - LOAD {skill-dir}/flows/update.md and EXECUTE the Update flow (U1-U3).
   - `new` - LOAD {skill-dir}/flows/new.md and EXECUTE the New flow (N1-N2); the second argument is the task id.
   - `intake` - LOAD {skill-dir}/flows/intake.md and EXECUTE the Intake flow (I1-I9); remaining text is the raw request, when given.
   - `vocab` - LOAD {skill-dir}/flows/vocab.md and sub-dispatch on the next argument: none - the List flow (L1); `add` - the Add flow (VA1-VA2), third argument is the term slug; `extract` - the Extract flow (X1-X4), remaining text names the surfaces, when given.
   - `lang` - LOAD {skill-dir}/flows/lang.md and sub-dispatch on the next argument: none - the Lang Check flow (LC1); `extract` - the Lang Extract flow (LX1).
   Otherwise (no args, or a scaffold / `init` intent) LOAD {skill-dir}/flows/init.md and EXECUTE the Init interview, steps 1-6.
1. EXECUTE the loaded flow's steps in order, exactly as written there; every constraint below binds inside every flow.
2. REPORT as the flow's final step directs. A failed engine or missing module returns control to the conversation with the failure stated in one line - never a silent stop.
</instructions>

<constraints>
- Do NOT overwrite existing files. init is no-clobber by design; the merge targets are printed, never merged; never add a flag or step that forces an overwrite.
- Do NOT edit an existing contract without the user's explicit direction - contracts are immutable to implementers (write-surface rule); intake edits only the contract it is itself authoring.
- Do NOT touch Cairn strata (THEORY.md, MAP.md, STATE.md, CONVENTIONS.md, decisions/, docs/): recommend /cairn, never write on its behalf.
- Do NOT chain shell commands - every Bash call is a single segment: no pipes, no semicolons, no `&&`, no redirects.
- `audit` is report-only: never fix its findings unasked, never route it through a writing step.
- `update` is report-only by default: `--apply` writes exactly one named kit-owned file per user-directed call; merge targets and consumer-owned files are never applied; no bulk path exists.
- intake writes ONLY `specs/{id}/contract.yaml`; a red contract never hands off to development.
- Vocab writes land ONLY under `specs/vocabulary/`; the List flow is read-only.
- Lang flows are report-only; dictionary deltas are user-consented class-E edits on the 0014 lanes.
- NEVER flip a term's status to `ratified` unasked. Extraction and day-2 authoring are born `draft`; the single born-ratified path is the greenfield init seed, where the interviewee is the principal. A TC010/TC011 in a contract loop means fork the term or drop the ref - never ratify to turn a contract green.
- A failed engine or missing module returns control to the conversation with the failure stated in one line - never a silent stop.
</constraints>

<criteria>
- [ ] Dispatch honored: a subcommand argument never triggers the interview; no-arg runs init steps 1-6; `vocab` sub-dispatches to List / Add / Extract; every flow is loaded from its own file under {skill-dir}/flows/ before it runs.
- [ ] Target confirmed (cwd, or git root if chosen); git absence noted, never blocking; Cairn recommended when absent and its files untouched.
- [ ] Answers captured - project_name / adoption / stack, from the interview or supplied by the invocation; init.py invoked once; stdout reported with created / skipped / merge-by-hand surfaced.
- [ ] New flow: `taskcontract new` invoked; created path + loop line reported, or the failure + install hint.
- [ ] Intake flow: contract authored on its own scaffold; the unit graph rendered and every unit answered by a human before the contract is final, `confirmed_by` recorded when the seat term is ratified; validate looped (max 5) to ready-green or PARKED with a named blocker; handoff refused while red; nothing else written.
- [ ] Audit flow: audit.py ran by absolute path; findings reported verbatim; nothing written or fixed.
- [ ] Update flow: update.py ran by absolute path; drift reported by class (kit-owned / merge-target / consumer); apply only per-file on explicit user direction; merge targets and consumer files never applied.
- [ ] Vocab flows: listing computed and reported verbatim; add scaffolds red and draft; extract reads only declared surfaces, births 5-15 draft terms with sources, loops the door to green (max 5), and leaves every ratification to the user.
- [ ] Lang flows: one Bash call each, stdout verbatim, nothing written; deltas stay the user's lane.
- [ ] Greenfield init seeds 5-15 ratified terms through the interview and the same machinery; brownfield init recommends extract instead.
- [ ] Every Bash call a single segment; no overwrite anywhere.
</criteria>
