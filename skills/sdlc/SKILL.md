---
name: sdlc
description: Lay a spec-first SDLC gate spine into any repository - greenfield or brownfield. Interviews for project name, adoption (greenfield or brownfield), and stack - or takes them from the invocation args - then renders a no-clobber payload - SDLC.md gate status page, .sdlc/ config + clocks + standing-red ledger, the protected specs/ root for immutable task contracts, and a CI job validating every contract (the G0 backstop). Day-2 subcommands - `/sdlc intake` (the G0 venue - turn a raw request into a contract and loop the validator to green), `/sdlc new {id}` (scaffold a contract skeleton), `/sdlc audit` (report-only gate-health check). Pairs with /cairn - docs spine first, gate spine second; neither requires the other. Use when starting, adopting, or operating gated agent-driven development.
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
skill's own directory holds the engines and templates:
  {skill-dir}/init.py       (no-clobber renderer)
  {skill-dir}/audit.py      (report-only health check, exit 0/1/2)
  {skill-dir}/templates/*.template

Contract machinery (`python -m taskcontract` + the schema) comes from
the pip-installed kit:
  pip install "git+https://github.com/JJandDjango/sdlc-kit.git"
The scaffolded CI job installs it itself; local `new`/`validate` need it
once. If `python -m taskcontract` reports no such module, offer that
install command and continue with whatever needs no validator.

Payload (no-clobber; the two merge targets are printed instead of
written when they already exist):
  SDLC.md - .sdlc/config.yaml - .sdlc/clocks.yaml - .sdlc/reds.yaml -
  specs/README.md - .github/workflows/sdlc.yml -
  .pre-commit-config.yaml - .vscode/settings.json
</context>

<instructions>
0. DISPATCH. If this skill was invoked with a first argument naming a subcommand, do NOT run the interview:
   - `audit` - run the Audit flow (A1-A2).
   - `new` - run the New flow (N1-N2); the second argument is the task id.
   - `intake` - run the Intake flow (I1-I7); remaining text is the raw request, when given.
   Otherwise (no args, or a scaffold / `init` intent) run the Init interview, steps 1-5.

## Init interview

1. CONFIRM the target directory. Default to cwd. Run `git rev-parse --show-toplevel` via Bash; if it succeeds and differs from cwd, ASK the user (AskUserQuestion) whether to target the git root or cwd. A non-git directory is acceptable - NOTE that the CI job and protected-root enforcement only bite on a hosted repo, then proceed.

2. DETECT a Cairn spine: if THEORY.md and MAP.md are absent at the target, RECOMMEND running /cairn first (docs spine, then gate spine) - never require it, never write its files.

3. INTERVIEW batch - but SKIP the questions the invocation already answers: when the invoking text (a charter, script, or explicit user instruction) supplies project name, adoption, and stack, treat those as interview-equivalent and go straight to RENDER; ask only what is missing. Otherwise invoke AskUserQuestion with 3 questions in one call:
   - Q1 header "Project name": "Name for this project?" options: "Use cwd directory name" / "Use git remote name" (offer only if a remote exists) / Other.
   - Q2 header "Adoption": "Greenfield or brownfield?" options: "greenfield - gates from commit zero" / "brownfield - adopt gates additively (no-clobber protects what exists)".
   - Q3 header "Stack": "Primary stack? (recorded for gate activation; the v1 payload is stack-neutral)" options: "dotnet" / "python" / "typescript" - Other for anything else, free text.

4. RENDER - one Bash call:
       python {skill-dir}/init.py --answers '{json}'
   where {json} is the dict {"project_name": ..., "adoption": ..., "stack": ...} as a single-quoted shell argument (escape inner double quotes as the shell needs). Non-zero exit: REPORT stderr in one line and return to the conversation.

5. REPORT the engine's stdout verbatim (created / skipped / merge-by-hand blocks + next steps). If any merge-by-hand snippet printed, restate in one line which files the user must merge manually.

## New flow

N1. RUN - one Bash call: `python -m taskcontract new {id}`. The skeleton is deliberately red: TC007 trips until a real intent is authored, so a fresh contract can never pass the gate vacuously.

N2. REPORT stdout (the created path + the validate loop line). On failure REPORT stderr verbatim; for a missing module also offer the pip install command from the context section.

## Intake flow

The G0 venue: raw request in, ready contract out. G0.1 reads `enforced`
for this repo once this flow is how tasks enter development.

I1. COLLECT the raw request - the invocation text after `intake`, or ask the user for it.

I2. DERIVE a task id matching `^[a-z][a-z0-9-]{2,63}$` from the request; if the derivation is unclear, confirm it with the user (AskUserQuestion).

I3. SCAFFOLD - one Bash call: `python -m taskcontract new {id}`. If it fails because the contract already exists, ASK before touching anything - existing contracts are never silently edited.

I4. AUTHOR `specs/{id}/contract.yaml` from the request: intent in outcome terms (40-1200 chars - what is true after this task that is not true now); scope paths; non_goals; decomposition units each with done_means and 1-3 acceptance_sketch criteria; dependencies as {ref, status: resolved or blocked, blocked_by}; provenance origin `human-request` unless the task demonstrably originates from an operations escape (`g8-escape`, requires ref) or maintenance (`g9-maintenance`).

I5. LOOP - one Bash call per iteration:
       python -m taskcontract validate specs/{id}/contract.yaml --profile ready
    Fix exactly what each TCnnn diagnostic names. Cap at 5 iterations; if still red, REPORT the remaining violations and return to the conversation.

I6. PARKED CASE - if a dependency is blocked in fact: set {status: blocked, blocked_by}, VERIFY `--profile draft` passes, then REPORT the contract as PARKED with the named blocker and REFUSE the development handoff - `ready` is the entry gate.

I7. REPORT the contract path, its state (ready-green, or parked-draft + blocker), and a one-line scope summary. Development starts only from green.

## Audit flow

A1. RUN - one Bash call, by absolute path: `python "{skill-dir}/audit.py" --cwd .`

A2. REPORT stdout verbatim. Exit 0 = clean; 1 = findings, each carrying a code (e.g. CONTRACT-INVALID, SPINE-MISSING, REDS-SCHEMA); 2 = no gate spine here (offer the init interview instead). Do NOT fix findings unasked - audit automates detection; fixes stay with the user or an explicit follow-up task.
</instructions>

<constraints>
- Do NOT overwrite existing files. init is no-clobber by design; the merge targets are printed, never merged; never add a flag or step that forces an overwrite.
- Do NOT edit an existing contract without the user's explicit direction - contracts are immutable to implementers (write-surface rule); intake edits only the contract it is itself authoring.
- Do NOT touch Cairn strata (THEORY.md, MAP.md, STATE.md, CONVENTIONS.md, decisions/, docs/): recommend /cairn, never write on its behalf.
- Do NOT chain shell commands - every Bash call is a single segment: no pipes, no semicolons, no `&&`, no redirects.
- `audit` is report-only: never fix its findings unasked, never route it through a writing step.
- intake writes ONLY `specs/{id}/contract.yaml`; a red contract never hands off to development.
- A failed engine or missing module returns control to the conversation with the failure stated in one line - never a silent stop.
</constraints>

<criteria>
- [ ] Dispatch honored: a subcommand argument never triggers the interview; no-arg runs init steps 1-5.
- [ ] Target confirmed (cwd, or git root if chosen); git absence noted, never blocking; Cairn recommended when absent and its files untouched.
- [ ] Answers captured - project_name / adoption / stack, from the interview or supplied by the invocation; init.py invoked once; stdout reported with created / skipped / merge-by-hand surfaced.
- [ ] New flow: `taskcontract new` invoked; created path + loop line reported, or the failure + install hint.
- [ ] Intake flow: contract authored on its own scaffold; validate looped (max 5) to ready-green or PARKED with a named blocker; handoff refused while red; nothing else written.
- [ ] Audit flow: audit.py ran by absolute path; findings reported verbatim; nothing written or fixed.
- [ ] Every Bash call a single segment; no overwrite anywhere.
</criteria>
