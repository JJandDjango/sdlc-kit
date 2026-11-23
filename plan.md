# Session 169 plan: build `l1-loop-files`, the first of session-loop's four units

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session flow: how a kit session stops for the user, wraps and starts again.
**Feature:** session-loop (contract `session-loop`): a wrapped session restarts itself in the same pane until the user is needed; G1 passed (session 168), no unit built yet.
**Unit:** `l1-loop-files`: `workflows/tools/loop.py`, the files and issues the loop runs on, which the launcher (l2) and the session's rules (l4) read.

## 1. The deliverable

`l1-loop-files` built by `/sdlc execute` to a Two-Key PASS, on a draft PR with green CI.

## 2. Where this sits

PR #174 merged at `eebad74` (2026-11-22): G1 passed, recorded in `.sdlc/g1/session-loop.yaml`. The units run in order: l1, then `l2-loop-launcher` and `l3-loop-stops` (both in `E:\herdr-sdlc`), then `l4-loop-rules`, which ships kit 0.23.0.

l1's done means and checks: `specs/session-loop/contract.yaml:49-69` (SC1.2, SC2.1, SC5.1+SC5.2). The file shapes and the six subcommands: design `docs/features/session-loop.design.md:59-71`; its Constraints `:112-121`; its Units row `:127` (git and `gh` behind a run seam; nothing written outside `{git folder}/sdlc-loop/`; no retirement). At G1.3 the user took item 9 with its gap: the timer's minute has no property spec, and l1's test list must pin one (backlog Next actions 24).

The installed plugin reads `95833c7`. Since then only `taskcontract/tree.py` changed, nothing under `skills/`, `agents/` or `workflows/`, so the installed team builds l1 with no restart.

## 3. The steps

1. Branch `session-169-l1-loop-files` off main at `eebad74`; this plan committed and pushed.
2. `/sdlc execute session-loop l1-loop-files`: QA drafts the test list, with the timer property, and proves it red.
3. Stop: the user approves the test list (the tripwire).
4. The rest of the flow: the QA verifier's prove-red, the Developer, the receipts, the Dev verifier, then the QA verifier's mutations.
5. Close: backlog Next 30 marks l1 built and Next actions 24 item 9 closed, a row in `docs/session-metrics.md`, `plan.md` out, push, a draft PR with its readings at the top, CI green.

## 4. Where Claude stops for the user

At step 3, while the tripwire in `docs/session-metrics.md` stands, and at the PR's review and merge. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1, 2, 4 and 5: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None: the requirements, design and contract are signed and G1 passed. Three readings Claude foresees, each ruled from the design's purpose and listed in the PR body:

- l1 builds all six subcommands of `loop.py` (`on`, `off` and `due` with `stop`, `reply` and `wrap`): the design's Scope names one file, `wrap` removes `loop.json`, and l2's launcher reads it. l4 routes `/sdlc loop on|off` to them.
- Times are local with no zone, as the design's examples show. The timer's minute is one pure function, so the property test runs it over many stop times without a clock.
- `wrap --self` removes `waiting.json` with `loop.json`: the session that waited ends, and the open issue stays the record (the design names only the issue).

## 7. What could go wrong, already ruled

- A test that reaches the real `gh` files a real issue on `JJandDjango/sdlc-kit`: every test passes a fake runner through the seam.
- The timer's property needs no new dependency: the kit has no property-test library, so the test sweeps every second of one day plus the month's and year's ends, and asserts 54 to 56 minutes and never :00 or :30.
- The cron line crosses midnight, a month's end or a year's end: the sweep's boundary days cover it.
- `prove.py`'s export holds no `.git`: the tests fake `git rev-parse --absolute-git-dir` to a temporary folder.
- Non-ASCII question text: subprocess output decodes as UTF-8 with errors replaced (design Constraints), and a test feeds such text.
- QA's result too large to parse comes back empty (session 157): recover it from the member's transcript.
- The QA verifier's mutation run meets the 600 s Bash cap: it keeps to the minimum four.
- Two whole suites at once stop each other: run one at a time.

## 8. This session's cost, with its basis

About 0.5M to 0.9M agent tokens. Basis: `s10` took 471K at one round (session 159), `s7` 677K (session 149), `s9` 960K over three test rounds (session 158). l1 is one new file with three checks and the timer property, and retires no test, so no test-retirer runs. Each failed round adds about 100K to 200K. If this session's context passes 200K at the test list, it hands over by a file in the receipt folder and a new session builds from it.

## 9. Not in this session

- l2, l3 and l4, and kit 0.23.0.
- The `needs-ruling` label on `JJandDjango/sdlc-kit`: l1's tests fake `gh`; check it before l4's live run.
- Next actions 24 item 8: failure criteria for herdr failing and `gh` unreachable.

## 10. Words

- **`needs-ruling` issue**: a GitHub issue with that label; it holds a question for the user, and `/cairn status` lists it under Waiting on you.
- **human-needed stop**: a point where a session needs the user's answer; in a loop it files a `needs-ruling` issue and waits.
- **git folder**: the folder `git rev-parse --absolute-git-dir` names; the loop's files live in its `sdlc-loop/`, never tracked.
- **`loop.json`, `waiting.json`, `sentinel.json`**: the loop is on; a stop is waiting; a wrap finished (its kind `continue`, `self-wrap` or `pick`).
- **sentinel**: the file a wrap writes last, after its push, which tells the launcher to restart the pane.
- **launcher**: `herdr_loop.py` (l2), a process outside any session that types `/clear` and `/resume-session` into the pane.
- **pick issue**: the one `needs-ruling` issue titled "Pick the next deliverable", filed when Next is empty.
- **self-wrap**: the wrap a session runs on itself when its 55-minute timer runs out with no reply.
- **run seam**: the one function through which `loop.py` runs git and `gh`, which tests replace with a fake.
- **property test**: a test that checks one rule over many inputs, here every stop time.
- **reading**: a call Claude or a member made where the signed documents were silent; each is listed in the PR body.
- **team, member**: the agents `/sdlc execute` starts: QA (drafts the tests), QA verifier, Developer, Dev verifier.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
