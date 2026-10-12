# Notes - the process's cost (2026-10-12)

> An idea, not yet a feature. The user opened it at session 95's close,
> after unit `s4-tree` took 1,642K agent tokens against a plan of about
> 0.6 million. Nothing here is ruled.

## The user's two thoughts

1. Too much thinking is spent after the feature document and the design
   document. Those two should be enough to let the sessions that follow
   them, or at least their agents, run at lower effort.
2. Another model for the agents: one Anthropic hosts, or one hosted on
   this machine. A card with 16 GB of video memory runs Gemma 4 here
   through LM Studio.

## What session 95 measured

- **Agent tokens stay out of the session's context.** Three agent runs
  spent 364K. Their results took 10.6K of the session's 325K context,
  3.3%.
- **An agent's count is its context at its last request, and most of it
  is the fixed start.** The second developer run counted 60,488 tokens:
  50,196 the first request (system prompt, tools, CLAUDE.md, memory
  index, skill list, the brief), 5,935 files read, about 4,400 the
  rest. The change itself was 20 lines. A Two-Key round runs two
  agents, so about 100K of its 214K is fixed start.
- **The session's own context at the PR:** thinking 86K (26.5%), files
  read 68K (20.8%), files and briefs it wrote 50K (15.5%), the fixed
  start 57K (17.5%), command output 28K (8.7%).
- **Effort as the workflows set it:** `high` for the drafter, the
  developer, the retirer and Two-Key's grader; none for Two-Key's
  receipts agent, which only runs commands; `medium` for a live run's
  seat agent. No workflow sets a model.
- **Where the unit's tokens went:** Two-Key 919K over four rounds, the
  developers 467K over five runs, the drafter 256K.
- **Why the rounds failed:** rounds 1 to 3 on one promise the signed
  design never stated, that the print never stops for a hand-written
  text. Round 4 on one USAGE sentence the session mistyped. PR #116
  lists 15 readings, each a case the design never named.

## Claude's first take, given to the user on 2026-10-12

1. Documents first, then lower effort. The thinking went into ruling
   the 15 cases. Lowering effort before the design carries such cases
   would buy more failed rounds, and a failed round costs more than any
   effort setting saves.
2. A hosted smaller model is the cheap win for the mechanical agents:
   the fixed start is a token count that lower effort cannot cut and a
   cheaper model can. Haiku 5.5 for the receipts agent, Sonnet 5.5 for
   a developer that works from a fix note, the drafter and the grader
   left as they are.
3. Gemma on a 16 GB card is no fit as a Claude Code agent: the 50K
   fixed start and the tool calls are the wrong load for it. A narrow
   check with a small prompt and no tools, called from a script, is the
   fit to try later.

## Not checked

- Whether a workflow's `agent()` call takes a model.
- Whether a workflow agent can start under the lean launch profile of
  `NOTES_lean-system-prompt_2026-10-11.md` (about 17K fixed against 44K
  for a session).
- What an agent's thinking costs: the agent transcript measured holds
  no thinking tokens, so `high` against `medium` has no figure yet.
- How LM Studio's local server would be reached from a script here.
- Which of the 15 readings a design section on "what each new place
  promises" would have caught before the build.
