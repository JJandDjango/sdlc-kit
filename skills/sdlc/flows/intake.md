---
name: sdlc-flow-intake
description: The Intake flow of /sdlc - the G0 venue - raw request in, ready contract out, doors looped to green, handoff refused while red.
---

<purpose>
The Intake flow of the `/sdlc` skill, the G0 venue: raw request in,
ready contract out. G0.1 reads `enforced` for a repo once this flow is
how tasks enter development. Dispatched by {skill-dir}/SKILL.md on
`/sdlc intake`; its constraints and criteria bind here. {skill-dir} is
the directory holding SKILL.md.
</purpose>

<instructions>
I1. COLLECT the raw request - the invocation text after `intake`, or ask the user for it.

I2. DERIVE a task id matching `^[a-z][a-z0-9-]{2,63}$` from the request; if the derivation is unclear, confirm it with the user (AskUserQuestion).

I3. SCAFFOLD - one Bash call: `python -m taskcontract new {id}`. If it fails because the contract already exists, ASK before touching anything - existing contracts are never silently edited.

I4. AUTHOR `specs/{id}/contract.yaml` from the request: intent in outcome terms (40-1200 chars - what is true after this task that is not true now); scope paths; non_goals; decomposition units each with a unique `id`, done_means and 1-3 acceptance_sketch criteria, plus `depends_on` where order matters; dependencies as {ref, status: resolved or blocked, blocked_by}; provenance origin `human-request` unless the task demonstrably originates from an operations escape (`g8-escape`, requires ref) or maintenance (`g9-maintenance`). Check `vocab-list`: when the request's nouns match ratified terms, declare them under `entities:`; when nothing matches, omit the field.

I5. LOOP - one Bash call per iteration:
       python -m taskcontract validate specs/{id}/contract.yaml --profile ready
    Fix exactly what each TCnnn diagnostic names. A TC010/TC011 means the vocabulary lacks the term: fork it (`/sdlc vocab add {slug}`, own small task) or drop the ref - NEVER ratify a term just to turn a contract green. Cap at 5 iterations; if still red, REPORT the remaining violations and return to the conversation.

I6. PARKED CASE - if a dependency is blocked in fact: set {status: blocked, blocked_by}, VERIFY `--profile draft` passes, then REPORT the contract as PARKED with the named blocker and REFUSE the development handoff - `ready` is the entry gate.

I7. REPORT the contract path, its state (ready-green, or parked-draft + blocker), and a one-line scope summary. Development starts only from green.
</instructions>
