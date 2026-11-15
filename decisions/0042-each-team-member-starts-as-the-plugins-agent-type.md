# 42. Each team member starts as the plugin's agent type

Status: accepted
Date: 2026-11-14

## Context

ADR 0040 ships the execution team in `workflows/`, where each workflow
starts its agent through `agent()` with its own brief. Given no agent
type, `agent()` starts the default workflow subagent, which takes the
session's whole tool set. Session 149's seven `s7` agents started at
50,068 to 54,243 tokens and called only Read, Grep, Glob, Edit, Write,
Bash and the schema's tool. The probe of 2026-11-13 (run
`wf_682248ad-4b4`) started an agent typed as `sdlc:sdlc-verifier` at
18,314 tokens against 49,831 as the default. e7's probe
(`RECEIPT_execution-team-e7_2026-11-14/probe.md`) found that a type
resolves by the plugin's name, a wrong name throws from `agent()` with
no fallback, the wall holds a typed agent, and `agent()`'s model wins
over the type's `model: inherit`. The design's Decisions 10 asks for
this ADR, written in e7.

## Decision

- **One type, `sdlc-team`.** The plugin ships `agents/sdlc-team.md`,
  allowing Read, Grep, Glob, Edit, Write and Bash, with `model: inherit`
  and no effort. Its body says only what every brief needs: the brief is
  the whole task, and the reply goes through the schema's tool.
- **The flow names the type; no workflow does.** `/sdlc execute` passes
  `"agentType": "{plugin}:sdlc-team"` at each member start. Each
  workflow takes `agentType` as a required argument and passes it to
  `agent()` beside model and effort. A workflow given no type starts no
  agent: QA, the Developer and the retirer return an error, and the
  verifiers return `INCOMPLETE`.
- **One type for every role.** Every role used Edit or Write in `s7`
  (the QA verifier writes its mutants), so one type per role saves
  nothing. The G3 operator definitions (`sdlc-developer`,
  `sdlc-verifier`) are not used: their prompts would reach the briefs.
- **This amends ADR 0040 in part.** A member runs its workflow's brief
  under the type's short body, no longer under the default workflow
  subagent's prompt. 0040's model rule stands: the execution row's model
  and effort, passed to `agent()`, win over the type's `inherit`. ADR
  0040 stays as written.

## Consequences

- Each agent start carries about 31.5K fewer tokens (63%), and every
  later request resends the start. At session 149's 135 requests, a unit
  sends about 4.0M fewer tokens, about 30% (estimate, `plan.md` of
  session 153).
- A member holds no PowerShell, WebFetch or Agent tool and loads no
  skill listing; a brief that needs one fails at the call.
- A retirer launched by hand passes `agentType` too, or it starts no
  agent.
- How `agent()` resolves a plugin's agent type is no public contract,
  like 0040's workflows folder: an update that drops it stops a run at
  its first member with an error, never a silent fallback to the whole
  tool set.
