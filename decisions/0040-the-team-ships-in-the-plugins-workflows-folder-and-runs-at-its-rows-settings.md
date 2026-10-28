# 40. The team ships in the plugin's workflows folder, and runs at its row's settings

Status: accepted
Date: 2026-10-27

## Context

The kit's sessions ran the execution team through workflow files that
stood untracked in `.claude/workflows/`, on one machine only, so no
consumer could run them. The request is the pair
`docs/features/execution-team.md` and
`docs/features/execution-team.design.md`; intake derived the contract
`execution-team` from them. The design's consult case 3 names a solution
new to the codebase: `workflows/`, a new folder at the plugin root,
beside `agents/`, `skills/` and `hooks/`. Its Decisions 2 asks for one
ADR, written with `e4-team`, that records the folder and the Sonnet
ruling.

Two earlier rulings meet this one. The 2026-10-12 process-cost ruling
kept the drafter, the developer and the grader on Opus 5.5 at `high`
(`NOTES_process-cost_2026-10-12.md:110`). The user ruled on 2026-10-21
that execution runs on Sonnet at `high`
(`docs/features/small-session-flow.md:107`), carried into the
execution-team request. And ADR 0039 says a plugin hook never blocks,
while the design's consult case 4 adds a PreToolUse hook that refuses a
tool call across the wall.

The probe of 2026-10-27
(`RECEIPT_execution-team-e4_2026-10-27/workflow_probe.md`) measured the
design's risk 1: Claude Code serves a plugin's `workflows/` folder, and a
session, headless or not, starts one of its workflows by
`{plugin}:{name}`.

## Decision

- **The team ships in `workflows/`.** The folder sits at the plugin
  root and git tracks it, so the plugin ships it (the marketplace source
  is `./`). One file holds each team member that runs as an agent,
  named by its operator id: `qa.js`, `qa-verifier.js`, `developer.js`
  and `dev-verifier.js`; `test-retirer.js` is the kit's own tool;
  `workflows/tools/` holds the scripts they run. `/sdlc execute` starts
  each member by its plugin name, `{plugin}:{operator}`, and runs the
  scripts from the plugin root, so nothing is copied into a consumer.
  `.claude/workflows/` keeps only this repository's session tools, which
  never ship.
- **Execution runs at its row's settings.** The execution row of
  `.sdlc/workflow.md` (Sonnet at `high`) holds the model and effort of
  every team member: the flow passes both to each member, and no
  workflow names either. This replaces the 2026-10-12 ruling that the
  drafter, the developer and the grader stay on Opus 5.5.
- **A plugin hook may refuse a call to hold the wall.** This amends ADR
  0039's "A plugin hook never blocks": `hooks/wall.py` refuses, by exit
  2, each tool call that crosses the wall while the task file names a
  walled operator, and refuses nothing when no task runs. Every other
  plugin hook keeps 0039's rule, `hooks/context_size.py` among them.
  ADR 0039 stays as written.

## Consequences

- A plugin update delivers the team, and a consumer copies no file. The
  plugin's name prefixes each member: `sdlc` once installed, the
  folder's name for a worktree loaded with `--plugin-dir`.
- The way Claude Code serves a plugin's workflows is no public contract:
  an update that drops it stops a run at its first member. The probe
  measured it once, and e6's live run measures it again.
- One model setting covers the whole run, so the row is the one place
  to change it; a run's agents cost what Sonnet costs.
- From e5 on, the kit builds its own units with the shipped team.
