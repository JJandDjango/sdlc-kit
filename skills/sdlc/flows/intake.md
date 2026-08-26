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

I5. RENDER + CONFIRM - one Bash call: `python -m taskcontract graph specs/{id}/contract.yaml`. SHOW the Mermaid and every unit's `done_means` inline. Every unit needs a human answer before the contract is final: ASK per unit (AskUserQuestion, up to four units per call) - keep, change (the answer names the change), or strike. When `vocab-list` shows `intake-seat` ratified, ASK which seats answered for each unit, or take them from the invocation when it names them; a seat is one of the term's own values.

I6. WRITE the confirmed contract: apply every change and strike, and when the seat term is ratified add `confirmed_by: [seats]` to every unit from the answers. Without a ratified seat term, write no `confirmed_by`. This write is the contract; nothing before it is final.

I7. LOOP - one Bash call per iteration:
       python -m taskcontract validate specs/{id}/contract.yaml --profile ready
    Fix exactly what each TCnnn diagnostic names. A TC010/TC011 means the vocabulary lacks the term: fork it (`/sdlc vocab add {slug}`, own small task) or drop the ref - NEVER ratify a term just to turn a contract green. A TC016 means a unit went unanswered or an answer named a seat the term lacks: return to I5 for that unit. Cap at 5 iterations; if still red, REPORT the remaining violations and return to the conversation.

I8. PARKED CASE - if a dependency is blocked in fact: set {status: blocked, blocked_by}, VERIFY `--profile draft` passes, then REPORT the contract as PARKED with the named blocker and REFUSE the development handoff - `ready` is the entry gate.

I9. REPORT the contract path, its state (ready-green, or parked-draft + blocker), the seats recorded, and a one-line scope summary. Development starts only from green.
</instructions>
