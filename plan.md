# Session 178 plan: the stop-entry fix, then `l4-loop-rules` closes

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session flow: how a kit session stops for the user, wraps and starts again.
**Feature:** session-loop (contract `session-loop`): a wrapped session restarts itself in the same pane until the user is needed; l1 to l4 merged (PR #180 at `c7ad046`), the stop entry failed live.
**Unit:** `l4-loop-rules`, its fix round: `hooks/loop_ask.py` denies AskUserQuestion in a loop, and the SessionStart line and `loop.md`'s L3 make every question a stop.

## 1. The deliverable

The stop-entry fix built, Two-Key PASS, its five-minute receipt passed live, and its PR open for review; `v0.23.0` is tagged on that PR's merge.

## 2. Where this sits

PR #180 merged at `c7ad046` (2026-11-24) before the fix; the user holds the `v0.23.0` tag and the self-pin PR until this fix merges. Session 177's sitting (`RECEIPT_session-loop-l4_2026-11-23/manual.md`): SC2.2, SC3.1, SC3.3 PASS; the stop entry FAIL, since both loop sessions asked by an AskUserQuestion dialog and ran no `loop.py stop`.

The fix: design r17 (`docs/features/session-loop.design.md`, Scope `:35`, Interfaces `:72` and `:82-88`, Constraints `:130`, Units row l4 `:140`), measured at r18 (0 findings, 0 OPEN); the draft and the tests it moves: `RECEIPT_session-loop-l4_2026-11-23/stop-entry-fix.md`.

## 3. The steps

1. Branch `session-178-l4-stop-entry` off main at `c7ad046`; this plan committed and pushed. The branch's last commit removes `plan.md`, which #180 left on main.
2. The engineer seat signs r17 (row r19), on the user's word.
3. `/sdlc intake session-loop`: the contract's scope adds `hooks/loop_ask.py` (row r20); no check, unit or done means changes.
4. `/sdlc g1 session-loop`: G1.3 signed again on design r17 (session 175's lesson: any re-intake needs it before a unit starts), on the user's word.
5. A fix round by `/sdlc execute session-loop l4-loop-rules`: QA amends `tests/test_loop_rules.py` by `stop-entry-fix.md` section 4 and proves it red; the QA verifier approves; the user approves the amended list (the tripwire); prove-red, the Developer, receipts, Dev verifier, QA verifier's mutations.
6. The receipt: a fresh loop pane in `.trial/clone` on this branch, `claude --plugin-dir E:/sdlc_development_kit`, `GH_REPO=JJandDjango/sdlc-kit`, the same un-nudged prompt (`... Ask me whether it should be trial-note.md or trial-note.txt ...`). Pass when `loop.py stop` runs before the question, no dialog stays open and `waiting.json` exists. Appended to `manual.md`.
7. The close: the usage page's stop-entry marker 🟢, `CHANGELOG.md`'s 0.23.0 entry names the deny hook, backlog Next 30, a row in `docs/session-metrics.md`, `plan.md` out, push, the PR with its readings at the top, CI green.

## 4. Where Claude stops for the user

Now: the r17 signature, the G1.3 answers on r17, and the words "run the workflow" (the auto-mode classifier refuses a team run without them). At step 5's test list, while the tripwire stands. At the PR's review, merge and the `v0.23.0` tag. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1, 3, 6 and 7, and step 5 but for the test list: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None beyond the signatures: r17 settles the fix. Readings Claude foresees, each listed in the PR body:

1. `loop_ask.py` finds `loop.json` as `loop_on.py` does (`git rev-parse --absolute-git-dir` of the event's `cwd`) and `{plugin}` from its own file's location (`loop_on.py:21`), not `CLAUDE_PLUGIN_ROOT`; on any failure, an unreadable event included, it exits 0 with no output.
2. The deny exits 2 with the reason on stderr (design `:88`, the wall hook's form), not a JSON `permissionDecision`.
3. The CHANGELOG's 0.23.0 entry gains the deny hook: 0.23.0 is not yet tagged, so no new version.

## 7. What could go wrong, already ruled

- `.trial/clone` sits on PR #180's branch: it pulls this branch before the receipt, and the pane runs `--plugin-dir` against the kit, so the installed plugin's age does not matter.
- A trial pane needs the trust prompt answered (`send-keys Down Enter`, from an argv list, never Git Bash).
- An idle-cron watcher ends on the event, inside the 1-hour cache, not at a fixed time.
- QA's draft is too big for a member's args: pass `"draft": {"file": ..., "read": ...}`.
- Two whole suites at once stop each other: run one at a time.

## 8. This session's cost, with its basis

About 0.25M to 0.4M agent tokens: QA's amendment 60K to 125K, QA verifier 90K to 130K (approve-tests, prove-red, two-key), Developer 40K to 90K, Dev verifier 55K to 115K, from l4's row (sessions 175 and 176, 457K) and l1's and l3's in `docs/session-metrics.md`. Each failed round adds about 100K. The receipt: about five minutes of one pane.

## 9. Not in this session

- The launcher's advisories carried from l2 and l3 (`wait_idle` exit and hang checks, `restart()` exit codes, a failed `pane get`, `wait_idle`'s name).
- The flaky `test_sc4_3_a_source_change_renders_within_two_seconds` (2.19 s once under `-n auto`).
- Next 31, `session-loop-sidebar` (SC6).

## 10. Words

- **loop**: on while `loop.json` sits in `{git folder}/sdlc-loop/`; `/sdlc loop on|off` writes and removes it.
- **stop entry**: the moment a session in a loop needs the user: it runs `loop.py stop`, sets its timer, then asks in a plain message.
- **deny hook**: `hooks/loop_ask.py`, a PreToolUse hook that refuses AskUserQuestion while `loop.json` exists and points at L3.
- **L3**: the stop rule in `skills/sdlc/flows/loop.md`.
- **SessionStart line**: what `hooks/loop_on.py` prints at a session start while the loop is on.
- **receipt**: a check run by hand and recorded in `manual.md`; here the five-minute stop-entry run.
- **reading**: a call made where the signed documents were silent; each is listed in the PR body.
- **team, member**: QA, QA verifier, Developer, Dev verifier, each started by its Workflow.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
