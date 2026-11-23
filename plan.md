# Session 172 plan: build `l3-loop-stops`, the third of session-loop's four units

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session flow: how a kit session stops for the user, wraps and starts again.
**Feature:** session-loop (contract `session-loop`): a wrapped session restarts itself in the same pane until the user is needed; l1 and l2 built and merged (PRs #175 to #177).
**Unit:** `l3-loop-stops`: the launcher's three stops in `E:\herdr-sdlc\herdr_loop.py`: two strikes, Claude gone from the pane, a 60-minute hang.

## 1. The deliverable

`l3-loop-stops` built to a Two-Key PASS in `E:\herdr-sdlc`, recorded on a kit draft PR with green CI.

## 2. Where this sits

PR #177 merged at `cca66a0` (2026-11-23). `herdr_loop.py` (at `E:\herdr-sdlc` `27cb671`) restarts the pane on a `continue` sentinel and ends quietly on `self-wrap`, `pick` or the loop turned off.

l3's done means and checks: `specs/session-loop/contract.yaml:90-108` (SC4.1, SC4.2, SC4.3). The messages, verbatim: requirements `docs/features/session-loop.md:104-106`. The stop's issue, toast and exit: design `docs/features/session-loop.design.md:86`; its Sources `:97`, `:108-110`; its Units row `:129`: all three checks automated, herdr, `gh`, sleep and the clock faked. No manual receipt: the backlog's "l3's live receipts" was session 171's slip; `.trial/` stays for l4's live sitting.

Documentation first is done: `E:\herdr-sdlc\README.md` feature 3, Stops, is 🔴 since session 170.

## 3. The steps

1. Branch `session-172-l3-loop-stops` off main at `cca66a0`; this plan committed and pushed.
2. The hand run's setup, as session 170's: a scratch folder and a `prove.py` shim (it runs the kit's `prove.py` from `E:\herdr-sdlc`) in this session's scratchpad.
3. Execute's task E3: QA drafts the test list and proves it red in a scratch export of `E:\herdr-sdlc`. Its `answer` carries readings 2 to 6 and the measured herdr shapes.
4. E4: the QA verifier approves the test list. Stop: the user approves it too (the tripwire).
5. E5 to E9: the QA verifier's prove-red, the Developer, the receipts, the commit on `E:\herdr-sdlc` master, the Dev verifier, the QA verifier's mutations.
6. Close: README feature 3 🟢, `python -m taskcontract progress done session-loop/l3-loop-stops`, backlog Next 30, a row in `docs/session-metrics.md`, `plan.md` out, push, a kit draft PR naming the herdr-sdlc sha with its readings at the top, CI green.

## 4. Where Claude stops for the user

At step 4, while the tripwire stands, and at the PR's review and merge. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1 to 3 and 5 to 6: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The user said "run the workflow" for this session. Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None: the documents are signed and l2 merged. Readings Claude foresees, each listed in the PR body:

1. The hand run, as session 170's: `repo` `E:/herdr-sdlc`, the three sources by absolute path, `E:\herdr-sdlc\.sdlc\config.yaml` for the tests, the shim as `pluginRoot`, `task.py` keeping the progress in the kit, the Orchestrator running the suite as the receipts.
2. Strikes live in the launcher's memory. The first `continue` sentinel after the launcher starts counts none (its start is unknown). A sentinel whose position equals the previous one's is a strike; a changed position sets the count to zero; the second strike in a row stops the loop before any typing.
3. Claude is gone when `herdr pane process-info --pane P` names no foreground process `claude.exe` or `claude`, read at each poll with no sentinel. A failed call is not read as gone: the hang check is the net.
4. The hang clock: the transcript `~/.claude/projects/*/{id}.jsonl`, `{id}` from `herdr pane get`'s `agent_session.value` (an object, measured), read again at each check, since `/clear` starts a new id. Hung is 60 minutes since the later of the transcript's last write and the launcher's own last start or restart, with no sentinel.
5. `gh issue create` runs in the pane's working directory, so the issue lands in the loop's repo. "Last sentinel" in the body is the `sentinel.seen.json` path, or `none` before the first.
6. A sentinel of an unknown kind ends at the hang check; the docstring says so.

## 7. What could go wrong, already ruled

- A fake that differs from herdr (l2's escape in session 171): QA's fakes take the shapes measured this session, quoted in its `answer`.
- A test that reaches the real herdr or `gh`: every test passes a fake runner.
- The Dev verifier's scope check reads kit paths: the scope names `E:/herdr-sdlc/herdr_loop.py` and `E:/herdr-sdlc/tests/`.
- QA's result too large to parse comes back empty (session 157): recover it from the member's transcript.
- Two whole suites at once stop each other: run one at a time.

## 8. This session's cost, with its basis

About 0.3M to 0.6M agent tokens. Basis: l1 took 347K (session 169), l2 305K (session 170), l2's fix 162K (session 171). l3 adds three checks to one file. Each failed round adds about 100K to 200K. If this session's context passes 200K at the test list, it hands over by a file in the receipt folder.

## 9. Not in this session

- l4 and kit 0.23.0; the `needs-ruling` label check before l4's live run.
- Session 170's advisories outside l3's checks: `restart()` ignores the herdr calls' exit codes; `wait_idle`'s name; no test pins a failed `pane get` during the wait.
- A GitHub remote for `E:\herdr-sdlc`.

## 10. Words

- **launcher**: `herdr_loop.py`, run in the user's own pane; it watches one Claude pane and restarts its session.
- **sentinel**: `sentinel.json`, a wrap's last write; its `kind` is `continue`, `self-wrap` or `pick`. The launcher renames a `continue` one `sentinel.seen.json`.
- **position**: the sentinel's `position`, the plan step and task the wrap recorded.
- **strike**: a session that ends at the position it started from; two in a row stop the loop.
- **hung**: no change in the session's transcript for 60 minutes with no sentinel.
- **stop**: one `needs-ruling` issue, a herdr toast, `loop.json` removed, exit 1.
- **hand run**: execute's tasks E3 to E9 run by Claude step by step, since the flow commits only in its own repo.
- **shim**: a `prove.py` stand-in that runs the kit's `prove.py` from `E:\herdr-sdlc`.
- **reading**: a call made where the signed documents were silent; each is listed in the PR body.
- **team, member**: QA (drafts the tests), QA verifier, Developer, Dev verifier, each started by its Workflow.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
