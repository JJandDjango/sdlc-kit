# 39. The kit ships plugin hooks, and a node starts at its row's settings

Status: accepted
Date: 2026-10-22

## Context

No file holds the steps of the kit's flow. Each step runs at the agent
model and effort of the session that starts it, and no rule holds a
session to one deliverable or to a size. The request is the pair
`docs/features/small-session-flow.md` (the PO seat signed r4 at r5) and
`docs/features/small-session-flow.design.md` (the engineer seat signed
r13 at r14), both on 2026-10-22; intake derived the contract
`small-session-flow` from them.

The design's consult case 3 names a solution new to the codebase: the
kit's first plugin hooks, and a command that starts an interactive
session. Its consult case 4 names a new public contract: the command
`python -m taskcontract node <id>` and the file format
`.sdlc/workflow.md`. Its Decisions ask for one ADR on both, drafted with
the first unit, `w1-session-size`.

Alternatives rejected, from the design: settings carried in each
agent's frontmatter (the agents keep `model: inherit`, so the
enforcement layer's approval channel, class E in `docs/operators.md`, is
not used); the workflow file under `docs/` (it is the kit's own working
file, so it lives in `.sdlc/`).

## Decision

- **The kit's plugin ships hooks.** `hooks/hooks.json` at the plugin root
  declares them, and each runs `python "${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py"`.
  A plugin hook never blocks: it exits 0 and only adds a message, prints
  nothing on an error, writes nothing in the repository, and stays silent
  in a repository with no `.sdlc/workflow.md`.
- **The first hook sizes the session.** `hooks/context_size.py` runs after
  each tool call and each user message. It reads the session's context
  from the transcript: the newest assistant message's input, cache-write
  and cache-read tokens, summed. Past 200K it shows `This session has
  passed 200K tokens, the target. Finish the deliverable and close.`;
  past 400K, `This session has passed 400K tokens, the limit. Save the
  notes and close now.` Each shows once a session, to the user and to the
  agent; a step past both shows only the second.
- **A node starts at its row's settings.** `python -m taskcontract node
  <id>` reads the node's row in `.sdlc/workflow.md` and starts `claude
  --model M --effort E` in the same terminal, found through
  `shutil.which` and started from an argument list with no shell;
  `--print` prints the line and starts nothing. A row that lacks either
  value starts nothing.
- **One file holds a node's settings.** No file but `.sdlc/workflow.md`
  holds a node's agent model or effort; the workflow scripts take both as
  arguments. No existing contract changes.

## Consequences

- Claude Code's transcript format is no public contract, so an update can
  silence the hook, and its never-block rule hides the error. The fixture
  tests pin the fields it reads, and a live receipt checks it once.
- The hook runs in every repository with the kit's plugin enabled and
  stays silent where no workflow file exists; only this repository holds
  one.
- The hook reaches a session only through the installed plugin, so a
  machine sees it after a plugin update or with `claude --plugin-dir`.
- `node` is the kit's first command that starts an interactive process;
  on Windows its terminal handling is checked by `w3-node-start`'s
  receipt, with `--print` as the fallback.
