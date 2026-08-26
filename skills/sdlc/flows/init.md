---
name: sdlc-flow-init
description: The Init interview of /sdlc - confirm the target, detect Cairn, interview, render the no-clobber payload, seed greenfield terms, report.
---

<purpose>
The Init interview of the `/sdlc` skill: lay the gate spine into the
target repo. Dispatched by {skill-dir}/SKILL.md when `/sdlc` runs with
no subcommand (or a scaffold / `init` intent); its constraints and
criteria bind here. {skill-dir} is the directory holding SKILL.md.
</purpose>

<instructions>
1. CONFIRM the target directory. Default to cwd. Run `git rev-parse --show-toplevel` via Bash; if it succeeds and differs from cwd, ASK the user (AskUserQuestion) whether to target the git root or cwd. A non-git directory is acceptable - NOTE that the CI job and protected-root enforcement only bite on a hosted repo, then proceed.

2. DETECT a Cairn spine: if THEORY.md and MAP.md are absent at the target, RECOMMEND running /cairn first (docs spine, then gate spine) - never require it, never write its files.

3. INTERVIEW batch - but SKIP the questions the invocation already answers: when the invoking text (a charter, script, or explicit user instruction) supplies project name, adoption, and stack, treat those as interview-equivalent and go straight to RENDER; ask only what is missing. Otherwise invoke AskUserQuestion with 3 questions in one call:
   - Q1 header "Project name": "Name for this project?" options: "Use cwd directory name" / "Use git remote name" (offer only if a remote exists) / Other.
   - Q2 header "Adoption": "Greenfield or brownfield?" options: "greenfield - gates from commit zero" / "brownfield - adopt gates additively (no-clobber protects what exists)".
   - Q3 header "Stack": "Primary stack? (selects the tooling profile overlay at render - dotnet's container is live, per-gate payload lands slice by slice)" options: "dotnet" / "python" / "typescript" - Other for anything else, free text.

4. RENDER - one Bash call:
       python {skill-dir}/init.py --answers '{json}'
   where {json} is the dict {"project_name": ..., "adoption": ..., "stack": ...} as a single-quoted shell argument (escape inner double quotes as the shell needs). Non-zero exit: REPORT stderr in one line and return to the conversation.

5. SEED (greenfield only) - elicit 5-15 seed terms from the interview (each: slug, display name, one-line meaning, kind - AskUserQuestion, or the invocation text when it supplies them). Author each at specs/vocabulary/{slug}.yaml via the Add flow's machinery ({skill-dir}/flows/vocab.md, VA1), then set `status: ratified` directly - the interviewee is the principal, so answers are interview-equivalent (ADR 0017 V5). LOOP `python -m taskcontract vocab-check` to green (one Bash call per iteration, cap 5). Brownfield: SKIP seeding - RECOMMEND `/sdlc vocab extract` as the day-2 follow-up instead.

6. REPORT the engine's stdout verbatim (created / skipped / merge-by-hand blocks + next steps). If any merge-by-hand snippet printed, restate in one line which files the user must merge manually. When step 5 seeded terms, append the vocab-list line counts.
</instructions>
