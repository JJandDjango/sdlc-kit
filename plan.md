# Session 175 plan: build `l4-loop-rules`, the last of session-loop's four units

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session flow: how a kit session stops for the user, wraps and starts again.
**Feature:** session-loop (contract `session-loop`): a wrapped session restarts itself in the same pane until the user is needed; l1 to l3 built and merged (PRs #175 to #178, the herdr fold in #179).
**Unit:** `l4-loop-rules`: `/sdlc loop on|off`, the rules a session in a loop follows at a stop, a reply and a wrap, the SessionStart hook, and kit 0.23.0.

## 1. The deliverable

`l4-loop-rules`' test list drafted, proved red and approved by the QA verifier and the user; the build, the live sitting and the PR follow in session 176.

## 2. Where this sits

PR #178 merged at `49b64f1` (2026-11-23) with l3 and the fold: `herdr/herdr_loop.py` restarts, ends quietly and stops; `workflows/tools/loop.py` already has `on`, `off`, `stop`, `reply`, `due` and `wrap` (l1).

l4's done means and checks: `specs/session-loop/contract.yaml:107-127` (SC2.2, SC2.3, SC3.1+SC3.3). What l4 builds: design `docs/features/session-loop.design.md:31-32` (scope), `:77-83` (the session's rules and the hook's line), `:134` (Units row: SC2.3 a text test on `loop.md`; SC2.2 and SC3.1+SC3.3 manual receipts in one live sitting of two panes).

This is the first unit built by the normal `/sdlc execute` since the fold (ADR 0043): no hand run, no shim.

## 3. The steps

1. Branch `session-175-l4-loop-rules` off main at `49b64f1`; this plan committed and pushed.
2. Documentation first: `docs/usage/session-loop.md`, the user's page for the loop, from the design's Interfaces; each feature marked 🟢 (l1 to l3) or 🔴 (l4's).
3. `/sdlc execute session-loop l4-loop-rules`, tasks E1 to E3: QA drafts the test list and proves it red.
4. E4: the QA verifier approves the test list. Stop: the user approves it too (the tripwire). This session hands over at the test list, by a file in `RECEIPT_session-loop-l4_2026-11-23/`.
5. Session 176, E5 to E9: prove-red, the Developer, the receipts, the commit, the Dev verifier, the QA verifier's mutations.
6. Session 176, the live sitting: `gh label create needs-ruling` (missing on `JJandDjango/sdlc-kit`, checked today); two loop panes in herdr from `.trial/clone`, one answered at 54 minutes (SC2.2), one left past 55 (SC3.1), then `/cairn status` in a fresh session (SC3.3). Receipt: `RECEIPT_session-loop-l4_*/manual.md`.
6a. Session 177 ran the sitting (`manual.md`): SC2.2, SC3.1, SC3.3 PASS; the stop entry FAIL (both sessions asked by AskUserQuestion, no `loop.py stop`). The user took the fix into l4: design r17 (amended by hand) and r18 (measured, 0 findings, 0 OPEN), from `RECEIPT_session-loop-l4_2026-11-23/stop-entry-fix.md`.
6b. Session 178: the engineer seat signs r17 (r19); intake re-derives the contract (scope adds `hooks/loop_ask.py`); `/sdlc g1` re-signs on r17; then a fix round by `/sdlc execute session-loop l4-loop-rules` (QA's list amended and proved red, the Developer, Two-Key); then the five-minute stop-entry receipt in a fresh loop pane, with the same un-nudged prompt.
7. Then the close: the usage page's markers 🟢, backlog Next 30, a row in `docs/session-metrics.md`, `ARCHITECTURE.md` trimmed if l4's rows need room, `plan.md` out, push, the PR with its readings at the top, CI green.

## 4. Where Claude stops for the user

Now, for the words "run the workflow" (the auto-mode classifier refuses a team run without them). At step 4, while the tripwire stands. At the PR's review, merge and the 0.23.0 tag. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1 to 3 and 5 to 7: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None: the documents are signed and l1 to l3 merged. Readings Claude foresees, each listed in the PR body:

1. The hook finds `{plugin}` from `CLAUDE_PLUGIN_ROOT` and `loop.json` under `git rev-parse --absolute-git-dir` of the session's folder. Outside git, or on any failure, it prints nothing and exits 0: a session start never fails on the loop.
2. SC2.3's text test reads `loop.md`: the stop rule ends the turn on the question; the wrap rule's closing message asks nothing. QA may also pin the route and the hook's line; the design names SC2.3 alone.
3. The self-wrap's closing message names the open issue and asks nothing; `/cairn status` carries the question under Waiting on you (SC3.3).
4. Kit 0.23.0 lands in the unit's commit (`pyproject.toml`, `skills/sdlc/init.py`, `CHANGELOG.md`); the tag and the self-pin PR (`.github/workflows/sdlc.yml`) follow the user's merge.

## 7. What could go wrong, already ruled

- A `CronCreate` one-shot fires only while the session is idle: the live sitting leaves both panes idle until their minute.
- `loop.py stop` exits 1 with no label: the label is created before the sitting.
- `PushNotification` is held back while the terminal is active: no check reads it.
- QA's result too large to parse comes back empty (session 157): recover it from the member's transcript.
- Two whole suites at once stop each other: run one at a time.

## 8. This session's cost, with its basis

This session: about 0.15M to 0.25M agent tokens (QA 96K to 136K, QA verifier's approve-tests 49K to 65K, from l1's and l3's rows in `docs/session-metrics.md`). Session 176: about 0.2M to 0.35M, plus an hour's sitting, idle while the timers run. Each failed round adds about 100K to 200K.

## 9. Not in this session

- The launcher's advisories carried from l2 and l3: `wait_idle` has no exit or hang check after a `continue` sentinel; `restart()` ignores the herdr calls' exit codes; no test pins a failed `pane get`; `wait_idle`'s name. None is one of l4's checks.
- Next 31, `session-loop-sidebar` (SC6).

## 10. Words

- **loop**: on while `loop.json` sits in `{git folder}/sdlc-loop/`; `/sdlc loop on|off` writes and removes it.
- **human-needed stop**: the session files a `needs-ruling` issue by `loop.py stop`, sets its timer and ends its turn on the question.
- **timer**: a one-shot `CronCreate` at the stop's time plus 55 minutes; with no reply it starts the self-wrap.
- **reply**: the user's next message while `waiting.json` exists; the session deletes the timer, closes the issue and goes on.
- **self-wrap**: the wrap the timer starts; its sentinel's kind `self-wrap` ends the loop, and the issue stays open.
- **sentinel**: `sentinel.json`, a wrap's last write; the launcher restarts the pane only on kind `continue`.
- **launcher**: `herdr/herdr_loop.py`, run in the user's own pane; it watches one Claude pane.
- **hook**: `hooks/loop_on.py`, run at each session start; it tells a fresh session the loop is on.
- **live sitting**: the manual receipts, run in real herdr panes with real timers.
- **reading**: a call made where the signed documents were silent; each is listed in the PR body.
- **team, member**: QA (drafts the tests), QA verifier, Developer, Dev verifier, each started by its Workflow.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
