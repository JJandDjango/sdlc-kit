# Session 170 plan: build `l2-loop-launcher`, the second of session-loop's four units

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session flow: how a kit session stops for the user, wraps and starts again.
**Feature:** session-loop (contract `session-loop`): a wrapped session restarts itself in the same pane until the user is needed; G1 passed, l1 built (PR #175).
**Unit:** `l2-loop-launcher`: `E:\herdr-sdlc\herdr_loop.py`, the launcher that reads l1's sentinel and types `/clear` and `/resume-session` into the pane.

## 1. The deliverable

`l2-loop-launcher` built to a Two-Key PASS in `E:\herdr-sdlc`, with its two manual receipts, recorded on a kit draft PR with green CI.

## 2. Where this sits

PR #175 merged at `2ad683b` (2026-11-22): `workflows/tools/loop.py` writes `loop.json`, `waiting.json` and `sentinel.json` under `{git folder}/sdlc-loop/`. l2 reads those shapes.

l2's done means and checks: `specs/session-loop/contract.yaml:70-89` (SC1.1, SC1.3, SC3.2). The launcher's behaviour: design `docs/features/session-loop.design.md:81-87`; its Sources `:93-110`; its Constraints `:112-121`; its Units row `:128` (herdr, `gh`, sleep and the clock faked; SC1.1 and SC1.3 also manual receipts).

`/sdlc execute` builds only in the repo it runs in: it commits with `git add` in `{repo}` and reads `.sdlc/config.yaml` there. `E:\herdr-sdlc` is a local repo with no remote, no `.sdlc/` and no specs. Session 43 built `herdr_seat.py` there by hand, with subagents and a Two-Key.

## 3. The steps

1. Branch `session-170-l2-loop-launcher` off main at `2ad683b`; this plan committed and pushed.
2. README first: `E:\herdr-sdlc\README.md` gains the launcher's section from the design, each behaviour marked 🔴; l3's stops listed 🔴 for l3.
3. Claude runs execute's tasks E3 to E9 by hand, as reading 1 says: QA drafts the test list and proves it red in a scratch export of `E:\herdr-sdlc`.
4. Stop: the user approves the test list (the tripwire).
5. The rest: the QA verifier's prove-red, the Developer, the receipts, the commit on `E:\herdr-sdlc` master, the Dev verifier, the QA verifier's mutations.
6. Manual receipts in herdr: SC1.1, a live restart in a scratch Claude pane whose new session names the sentinel's Next; SC1.3, the tree pane flagged while the launcher runs.
7. Close: README markers 🟢 (l2's), `python -m taskcontract progress done session-loop/l2-loop-launcher`, backlog Next 30, a row in `docs/session-metrics.md`, `plan.md` out, push, a kit draft PR naming the herdr-sdlc sha with its readings at the top, CI green.

## 4. Where Claude stops for the user

At step 4, while the tripwire in `docs/session-metrics.md` stands, and at the PR's review and merge. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1 to 3 and 5 to 7: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None: the requirements, design and contract are signed, G1 passed and l1 merged. Readings Claude foresees, each listed in the PR body:

1. The hand run: each member starts by its Workflow with `repo` `E:/herdr-sdlc`, the three sources by absolute path in the kit, `test.command` `[python, -P, -m, pytest, tests, -q]`, `test.file` `[python, -P, -m, pytest, "{file}", -q]` and the wall `tests/`. `task.py` keeps the unit's progress in the kit. The commit lands on `E:\herdr-sdlc` master, as session 43's did; the kit PR is the record and the review.
2. l2 holds the launcher's start, its `continue` restart and its quiet ends (`self-wrap`, `pick`, the loop off, no loop). The strike count, the exit check and the hang check are l3's (contract `:90-108`).
3. "Within 60 seconds of the sentinel": the launcher reads the folder at most every 5 seconds, so its idle wait has the rest of the minute.

## 7. What could go wrong, already ruled

- A test that reaches the real herdr types into a live pane: every test passes a fake runner, as `herdr_seat.py`'s `main(environ, run, sleep, clock)` does.
- The Dev verifier's scope check reads kit paths: the contract's scope names `E:/herdr-sdlc/herdr_loop.py` and `E:/herdr-sdlc/tests/`, and the verifier gets the repo prefix to strip.
- `prove.py` exports `E:\herdr-sdlc` at HEAD by `git archive`: it works on any git repo; the draft lands at `tests/`.
- The live restart types `/clear` into the wrong pane: it runs only in a scratch pane this session opens, with a scratch git folder, and the probe closes the panes it opens.
- Git Bash rewrites `/clear` (trial 2): the launcher calls herdr by argument list; the live check starts it from PowerShell.
- QA's result too large to parse comes back empty (session 157): recover it from the member's transcript.
- Two whole suites at once stop each other: run one at a time.

## 8. This session's cost, with its basis

About 0.4M to 0.8M agent tokens, plus the live check's scratch session (under 50K). Basis: l1 took 347K at one round (session 169), `s10` 471K (session 159), `s7` 677K (session 149). l2 is one new file with three checks and no retirement. Each failed round adds about 100K to 200K. If this session's context passes 200K at the test list, it hands over by a file in the receipt folder.

## 9. Not in this session

- l3 and l4, and kit 0.23.0.
- A GitHub remote for `E:\herdr-sdlc` (backlog question).
- The `needs-ruling` label on `JJandDjango/sdlc-kit`: l2 files no issue; check it before l4's live run.

## 10. Words

- **launcher**: `herdr_loop.py`, a process in the user's own herdr pane that watches one Claude pane and restarts its session.
- **sentinel**: `sentinel.json`, the file a wrap writes last, after its push; its `kind` is `continue`, `self-wrap` or `pick`.
- **`loop.json`**: the loop is on while it exists, in `{git folder}/sdlc-loop/`.
- **git folder**: the folder `git rev-parse --absolute-git-dir` names for the pane's working directory.
- **idle**: `herdr pane get`'s `agent_status` for the pane; the launcher types only then.
- **self-wrap, pick**: a wrap that ends the loop: no reply in 55 minutes, or an empty Next.
- **hand run**: execute's tasks E3 to E9 run by Claude step by step, since the flow cannot commit outside its own repo.
- **manual receipt**: a check run live by Claude in real herdr panes, its evidence quoted in the PR body.
- **reading**: a call Claude or a member made where the signed documents were silent; each is listed in the PR body.
- **team, member**: QA (drafts the tests), QA verifier, Developer, Dev verifier, each started by its Workflow.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
