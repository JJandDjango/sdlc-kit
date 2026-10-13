# Notes - the process's cost (2026-10-12)

> An idea, not yet a feature. The user opened it at session 95's close,
> after unit `s4-tree` took 1,642K agent tokens against a plan of about
> 0.6 million. The user ruled on it in session 96, on 2026-10-12: see
> "Ruled" below. What stands above that section is the record of the
> talk's start.

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

## What session 96 measured

The script is `.claude/workflows/tools/session_cost.py` (untracked, this
machine). It reads each session's transcript and its agents'.

- **A workflow's `agent()` call takes `model`, `effort` and
  `agentType`, each call** (the workflow authoring reference). No
  workflow set a model. The receipts agent set no effort, so it ran at
  the session's `xhigh`.
- **A run's cost is the sum over its requests.** Each request sends the
  whole context again. So "agent tokens" as `STATE.md` records them,
  the context at the last request, is not the cost. An agent makes many
  requests: the middle run made 6 for a developer, 10 for the grader,
  18 for the receipts agent and 28 for the drafter. Its 50K start is
  written to the cache once and read back on each later request.
- **The sessions cost more than their agents.** The six sessions that
  ran agents since 2026-10-08, weighed at API list prices: the
  sessions' own loops 71%, their agents 29%. Inside a session's loop:
  reading its own context again 55%, cache writes 25%, thinking 12%,
  visible output 9%. Of the whole: the sessions' re-reads 39%, all
  thinking 11% (8% the sessions, 3% the agents; about half the agents'
  share is estimated from the output's size).
- **By role, the same six sessions:** all 14 developer runs are 5% of
  the whole and the nine receipts runs 3.6%. The same tokens priced as
  Sonnet 5.5 for every agent would cut 11% of the whole, if no round is
  lost. A 17K start for every agent would cut 6%.
- **A resumed session writes its context again.** Four sessions were
  resumed after 6 to 15 hours. The cache had expired, so each wrote its
  whole context once more (112K to 484K tokens).
- **The baseline for ruling 4,** session 92 (`s3-review`, Two-Key PASS
  in round 1, the session at `xhigh`), in thousands of tokens: 183
  requests, a peak of 498; 1,040 written, 61,137 read, 101 thinking, 97
  visible. Its agents: 886 written, 11,656 read, 47 thinking, 62
  visible.
- **The user is on a subscription, not API billing** (the user,
  2026-10-12). The counts are measured. The weights are the API's, and
  how the plan weighs a cached read against a fresh token is not known,
  so the shares above are an assumption there. Quote tokens and shares,
  never dollars.

## Ruled, 2026-10-12 (session 96)

The user ruled all four as Claude wrote them, with the `/usage` reading
added.

1. **The receipts agent runs on Haiku 5.5 at `low`.** It only runs
   commands. Applied in `.claude/workflows/two-key-unit-verifier.js`
   (untracked, this machine) and not run yet: `s5-start`'s first
   Two-Key round is its first run. If the launch refuses the model's
   name or the agent returns nothing, the two options come out and the
   round runs as before.
2. **The drafter, the developer and the grader stay on Opus 5.5 at
   `high`.** This withdraws the Sonnet developer of Claude's first take:
   one lost Two-Key round costs about what the cheaper model saves in a
   unit.
3. **A build splits into two sessions at the test list.** A session's
   re-reads grow with its size, so two short sessions read less than one
   long one (about a third less, by arithmetic and not yet measured). A
   session left overnight is not resumed: a new session starts from the
   handoff file.
4. **`s5-start` runs with the session at `high` in place of `xhigh`,**
   as a trial of one unit. The script measures it against session 92's
   row, and the user reads `/usage` before and after each session, as
   the subscription's own measure. Thinking stays in the context and is
   read again on every later request, so lower effort also shrinks the
   re-reads.

The first take's order stands: documents first. `s3-review` passed in
round 1 and took one session. `s4-tree` failed four rounds on cases the
design never named and took two.

Parked, not ruled: a custom agent type with a smaller start (the 6%
above), and Gemma for a narrow check with no tools, called from a
script.

## Not checked

- Whether the launch takes `claude-haiku-5-5` as written, and whether
  Haiku's receipts agent returns its result in the schema.
- How the subscription weighs the four kinds of token.
- What a custom agent type's start weighs against the 50K of the
  default one, and whether it can follow the lean launch profile of
  `NOTES_lean-system-prompt_2026-10-11.md`.
- What `high` against `xhigh` changes in a session's requests and
  rounds: ruling 4's trial.
- How LM Studio's local server would be reached from a script here.
- Which of the 15 readings a design section on "what each new place
  promises" would have caught before the build.
