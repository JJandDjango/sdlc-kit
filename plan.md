# Session 153 plan: the team's agents take only their tools

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution team: the five workflow scripts under `workflows/` that `/sdlc execute` runs, each starting one agent through `agent()`.
**Feature:** none yet. Backlog Next 28; step 4 rules its path.
**Unit:** none yet.

## 1. The deliverable

Backlog Next 28's facts settled (a start measured, the probe run) and its path ruled; then the build, as far as the ruled path allows this session.

## 2. Where this sits

Session 152 made Next 28 the top priority, ahead of Next 26's `s8-honest-reads`. Main lacks Next 28 until the G1 branch merges, so this branch stacks on `session-150-g1-edges` at `8a1956b`; at the PR, the stacked-PR merge order applies (retarget to main before the lower branch is deleted). The five scripts call `agent()` with no `agentType` (`workflows/developer.js:79`, `qa.js:112`, `qa-verifier.js:153`, `dev-verifier.js:127`, `test-retirer.js:92`), so each agent takes the session's whole tool set. The Workflow reference documents `opts.agentType`, resolved from the same registry as the Agent tool. The plugin already ships two agents: `agents/sdlc-developer.md` (Bash, Read, Edit, Write, Glob, Grep) and `agents/sdlc-verifier.md` (Bash, Read, Glob, Grep), each with a G3 operator prompt that would replace the workflow subagent's own.

## 3. The steps

1. Branch `session-153-agent-tools` off `session-150-g1-edges` at `8a1956b`; this plan committed and pushed.
2. Measure a current start. Done: session 149's seven `s7` agents (session `491115f8`) started at 50,068 to 54,243 tokens and sent 13.3M tokens over 135 requests. They called Read, Grep, Glob, Edit, Write, Bash and StructuredOutput only; the retirer also called PowerShell twice, which Bash covers. The QA verifier's Two-Key run wrote and edited files (its mutants), so the verifiers need Edit and Write too.
3. The probe: one workflow, two agents, the same short prompt and a schema asking for their tool names. One runs as the default workflow subagent, one with `agentType: 'sdlc:sdlc-verifier'`. Done (run `wf_682248ad-4b4`): the type resolved; its tools were Bash, Read, Glob, Grep and StructuredOutput against the default's 16 tools and 191 deferred names; its skill listing was empty against 58 skills; both still loaded the global `CLAUDE.md` and the memory index. Starts: 18,314 tokens typed against 49,831 default, 31.5K less (63%).
4. Rule the path. Claude's call: amend the `execution-team` pair, since the five scripts are its surface: a design text row on `docs/features/execution-team.design.md` (one new agent definition with six tools and a short body, not the two G3 operator agents, whose prompts would reach the briefs), measured and signed, then re-intake adds one unit. The precedent is G1's edges (sessions 150 to 152). A new feature document would interview for a six-line change.
5. Build: one agent definition allowing Read, Grep, Glob, Edit, Write and Bash, passed as `agentType` in the five calls. Its body carries whatever the default workflow subagent prompt gave that the briefs rely on. Where it stands at session 153's close: the user ruled the path; design r18 (the text row: Interfaces 12, unit `e7-agent-type` with SC1.1 and SC1.3, Decisions 10 to 12 with the 63 kept readings) and r19 (`Measured:`, 7 copied-term findings, 0 OPEN) are written. Session 154: r20 fixes two points of r18 (the verifiers return `INCOMPLETE` on a missing type; whether `agent()`'s model beats the type's `model: inherit` joins the probe, Risks 12), r21 measured it, and the engineer seat signed at r22. Next: re-intake `/sdlc intake docs/features/execution-team.md` adds e7; then e7 through `/sdlc execute`, opening with the probe of Risks 9, 10 and 12 (a wrong name, a `--plugin-dir` load, one walled call as the agent, the model it runs at).
6. Measure after: a run's agent starts against step 2's.
7. Close: Next 28 closed on the backlog, a row in `docs/session-metrics.md`, `plan.md` out, push, a draft PR with its readings at the top.

## 4. Where Claude stops for the user

At step 3 (a workflow run takes the user's word), step 4 (the path), each unit's test list while the tripwire in `docs/session-metrics.md` stands, and the PR review.

## 5. Where Claude goes on alone, and by what rule

Steps 1, 2, 5 to 7: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

- Step 4's path.
- One agent type for all five scripts, or one per role. Claude's call: one, as Next 28 says; every role used Edit or Write in `s7`, so a per-role split saves nothing now.

## 7. What could go wrong, already ruled

- The custom type replaces the default workflow subagent prompt: step 3 compares the two agents' replies, and step 5 moves anything the briefs need into the definition.
- A plugin's agent type does not resolve inside `agent()`: step 3 finds out before any build; the path is then reruled.
- The allowlist drops StructuredOutput, which every script's schema needs: step 3 checks it.
- The 19K figure is from 2026-10-17: step 3 re-measures it.

## 8. This session's cost, with its basis

Steps 1 to 4: about 0.15M main-session tokens, plus the probe's about 0.11M (two starts near 50K, each with a short reply). The build through `/sdlc execute`, if one contract unit: about 0.7M to 1.0M agent tokens at one round (rs4 ran 634K, rs1 to rs3 about 1.0M each, `docs/session-metrics.md`). The return, by steps 2 and 3: 135 requests at about 30K less each (step 3's 31.5K, less Edit's and Write's definitions) is about 4.0M of a unit's 13.3M tokens sent, about 30%.

## 9. Not in this session

- Next 26's `s8-honest-reads` build.
- The rest of an agent's start: `CLAUDE.md`, the memory index and the skill listing (about 21K on 2026-10-17).
- The lean launch profile (backlog Open questions, item 5).

## 10. Words

- **agent start**: the tokens an agent's first request carries before it reads a file: system prompt, tool definitions, `CLAUDE.md`, memory index, skill listing and the brief. Each later request resends it.
- **agent type**: a named agent definition (`agents/*.md`) with a `tools:` allowlist; `agent()` takes it as `opts.agentType`.
- **workflow subagent**: the agent `agent()` starts when no type is given; it takes the session's whole tool set.
- **StructuredOutput**: the tool a schema-bound agent calls to return its reply.
- **the probe**: step 3's two-agent workflow.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
