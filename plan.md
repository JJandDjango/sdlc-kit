# Session 171 plan: run `l2-loop-launcher`'s two manual receipts in herdr

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session flow: how a kit session stops for the user, wraps and starts again.
**Feature:** session-loop (contract `session-loop`): a wrapped session restarts itself in the same pane until the user is needed; l1 and l2 built (PRs #175, #176).
**Unit:** `l2-loop-launcher`: `E:\herdr-sdlc\herdr_loop.py`, done at a Two-Key PASS; its two manual receipts are still open.

## 1. The deliverable

SC1.1 and SC1.3 run live in real herdr panes, their evidence in `RECEIPT_session-loop-l2_2026-11-22/manual.md` and quoted on a kit draft PR with green CI.

## 2. Where this sits

PR #176 merged at `b9d8aa6` (2026-11-22). l2's checks: `specs/session-loop/contract.yaml:79-86`. SC1.1: within 60 seconds of a `continue` sentinel the launcher types `/clear` and `/resume-session` into the same pane, and the new session names the Next the wrap recorded. SC1.3: while a loop runs, a session that stops with no wrap gets no keystroke, and the kit's `tree: notify:` command (`E:\herdr-sdlc\herdr_seat.py`) still flags the tree pane.

## 3. The steps

1. Branch `session-171-l2-manual-receipts` off main at `b9d8aa6`; this plan committed and pushed.
2. Scratch repo: a bare clone of the kit in the scratchpad as `origin`, a working clone at `E:\sdlc-loop-trial` on branch `loop-trial`, `cairn.plan` set to `docs/backlog.md`. One commit there makes backlog item 30 read `TRIAL-171: ...`, pushed to the scratch origin.
3. Panes: split `w9:p1` for the trial pane (Claude, Sonnet, cwd the trial clone). `loop.py on` in the trial clone; the launcher started on the trial pane as a background task, its log captured.
4. SC1.1: the trial session runs `loop.py wrap --next "<the trial's Next>"` and ends its turn. Evidence: the launcher's `restarted` line and its time against the sentinel's `at`, `/clear` and `/resume-session` in the pane, and the new session's report naming `TRIAL-171`.
5. SC1.3: a second split for the tree pane, running `python -m taskcontract tree --follow` in the trial clone, where session-loop waits on a seat. The trial session runs one short turn and stops with no wrap. Evidence: the tree pane reads `sdlc` `blocked` in `herdr pane get`, the launcher's log gains no line, and the trial pane shows no `/clear` for 90 seconds after it goes idle.
6. Teardown: Ctrl-C in the tree pane (the flag releases), `loop.py off` (the launcher prints `the session loop is off` and exits 0), both panes closed, both scratch clones deleted.
7. Close: backlog Next 30 updated, a row in `docs/session-metrics.md`, `plan.md` out, push, a kit draft PR with the evidence at the top, CI green.

## 4. Where Claude stops for the user

At the PR's review and merge. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1 to 7: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). A failed receipt is a finding: Claude records it and asks before any fix to `herdr_loop.py`.

## 6. Rulings needed

None. Readings Claude foresees, each listed in the PR body:

1. SC1.3's "team run stops with no wrap": the trial session ends a turn at a seat without a wrap. The launcher sees only the pane's idle state and the sentinel, so a full `/sdlc execute` run adds nothing it can see.
2. The launcher runs as a background task of this session, not in a pane of its own: the same argv, with its stdout kept as the receipt.
3. The scratch origin is a local bare clone, so no branch reaches GitHub.

## 7. What could go wrong, already ruled

- `/clear` typed into the wrong pane: the launcher names only the trial pane, whose cwd is the trial clone.
- Git Bash rewrites `/clear`: the launcher calls herdr by argument list; Claude's own prompts to the trial pane never start with `/`.
- The trial session stops at a trust or permission prompt: Claude reads the pane and answers by `send-keys`.
- The tree pane shows no seat in the clone: the progress it reads may be untracked; then Claude stages a seat by the trial's own `task.py`.

## 8. This session's cost, with its basis

About 100K to 150K tokens for the trial sessions (two starts at about 50K each, plus the short turns), no agents. Basis: a session starts near 50K (`reference-subagent-start-and-polling`); session 165's trials ran three such starts.

## 9. Not in this session

- l3 and l4, and kit 0.23.0. l3's carried items stay on Next 30.
- The `needs-ruling` label on `JJandDjango/sdlc-kit`: l2 files no issue.

## 10. Words

- **launcher**: `herdr_loop.py`, a process that watches one Claude pane and restarts its session.
- **sentinel**: `sentinel.json`, the file a wrap writes last, after its push; its `kind` is `continue`, `self-wrap` or `pick`.
- **trial pane, tree pane**: the two scratch herdr panes this session opens and closes.
- **manual receipt**: a check run live by Claude in real herdr panes, its evidence quoted in the PR body.
- **reading**: a call Claude made where the signed documents were silent; each is listed in the PR body.
