---
name: sdlc-flow-update
description: The Update flow of /sdlc - report scaffold drift vs the current kit templates; apply one kit-owned file per user-directed call.
---

<purpose>
The Update flow of the `/sdlc` skill. The committed scaffold is
rendered once and never rewritten by the kit (no-clobber); this flow
makes the drift visible when the kit moves on, and applies fixes only
file by file on the user's word. Dispatched by {skill-dir}/SKILL.md on
`/sdlc update`; its constraints and criteria bind here. {skill-dir} is
the directory holding SKILL.md.
</purpose>

<instructions>
U1. RUN - one Bash call, by absolute path: `python "{skill-dir}/update.py" --cwd .`

U2. REPORT stdout verbatim. Exit 0 = scaffold current; 1 = drift or absence, one row per surface with its class - `kit-owned` (applyable), `merge-target` (hand-merged; `--show {rel}` prints the current render), `consumer` (existence-only by design - SDLC.md, config, clocks, reds are the consumer's data); 2 = no gate spine (offer the init interview instead).

U3. APPLY only on the user's explicit per-file direction - one Bash call per file: `python "{skill-dir}/update.py" --cwd . --apply {rel}`. Kit-owned surfaces only; the engine refuses merge targets and consumer files. NEVER loop apply over the whole report - each file is its own consent.
</instructions>
