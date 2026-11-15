# Session 157 plan: build `s8-honest-reads` on the team e7 typed

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G1, the gate between intake and the first unit's test list, where a feature's requirements and spec are checked before development starts.
**Feature:** g1-requirements-spec (contract `g1-requirements-spec`): G1's three conditions, its venue `/sdlc g1`, and the refusal that keeps a task from starting before G1 passes; `s1` to `s7` on main since kit 0.22.1, `s8` to `s10` ready (design r19, contract rows r14 and r22).
**Unit:** `s8-honest-reads`: G1 reads `done` only for what a tool or a review checked, and only the config and the contract's origin say where G1 is active.

## 1. The deliverable

`s8-honest-reads` built by `/sdlc execute` to a Two-Key PASS, on a draft PR, with the first measure of agent starts under e7.

## 2. Where this sits

PR #164 merged at `9e59e28` (2026-11-15): e7 makes each team member start as the plugin's agent type `sdlc-team`, with only its own tools (ADR 0042). e7 ships no release of its own (`docs/features/execution-team.design.md:258`); kit 0.22.2, from `s10-words-and-folds`, carries it. The user ruled (session 157): no release now; the team builds `s8` from main, and e7 ships with 0.22.2. The installed plugin `sdlc@sdlc-kit` tracks main by sha (now `efbc8df`, before e7), and its marketplace updates from GitHub at start.

`s8` takes ten of the edges the user ruled in session 150: A1, A2 with F1, C1, C2, D1, D2, D5, D6, F2 and H1 (`docs/features/g1-requirements-spec.design.md`, Units row at `:469`; the edges in the backlog's Next 26). Its checks: SC2.1+SC3.1, SC4.1 and SC5.2 (`specs/g1-requirements-spec/contract.yaml:156-183`). Two manual receipts: a live TLC run on one passing model, and a live intake run on a request from an escape with G1 active, to its report's end (ADR 0041, rule 3).

## 3. The steps

1. Branch `session-157-s8-honest-reads` off main at `9e59e28`; this plan committed and pushed.
2. Stop: the user restarts Claude Code so the plugin loads at `9e59e28`, then runs `/resume-session`. Check: `installed_plugins.json` reads `9e59e28`, and the install holds `agents/sdlc-team.md`.
3. `/sdlc execute g1-requirements-spec s8-honest-reads`: QA drafts the test list and proves it red.
4. Stop: the user approves the test list (the tripwire).
5. The rest of the flow: prove-red, the test-retirer, the Developer, the receipts, the Dev verifier, then the QA verifier's mutations.
6. The two manual receipts, each to an untracked `RECEIPT_g1-requirements-spec-s8_<date>/` folder.
7. The after-measure: each member's start, read by `context_breakdown.py` from its transcript, against session 149's 50K to 54K.
8. Close: the backlog's `s8` edges closed, a row in `docs/session-metrics.md`, `plan.md` out, push, a draft PR with its readings at the top.

## 4. Where Claude stops for the user

At step 2 (the restart), at step 4 (the test list, while the tripwire in `docs/session-metrics.md` stands), and at the PR's review. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1, 3 and 5 to 8: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None before the build: the edges, the design row and the contract are signed. The test list is the user's at step 4.

## 7. What could go wrong, already ruled

- The restart does not move the plugin past `efbc8df`: update it by hand (`/plugin`, the sdlc-kit marketplace) and restart again.
- `prove.py`'s export holds no `.git`, so a test that lists files through git fails there (session 156, backlog Next actions 23): the drafter lists files from the disk.
- A kept draft from an earlier run shadows the committed test (Next actions 23): start from no kept draft for `s8`.
- The QA verifier's mutation run meets the 600 s Bash cap: at about 100 s a mutation, it keeps to the minimum four.
- Two whole suites at once stop each other: run one at a time.

## 8. This session's cost, with its basis

About 0.7M to 1.0M agent tokens at one round, session 150's estimate from `s7`'s 677K (`docs/session-metrics.md`, session 149); each failed round adds about 100K to 200K. e7 should cut this: a typed start measured 18,314 tokens against 49,831, and each request resends the start.

## 9. Not in this session

- `s9-one-line-refusals` and `s10-words-and-folds`, and kit 0.22.2.
- G2.

## 10. Words

- **G1**: the gate a feature passes before development starts; active for a feature when `G1` is under `active_gates` in `.sdlc/config.yaml` and the feature is not on `g1.exempt`.
- **G1.1, G1.2, G1.3**: G1's conditions: each boundary schema lints clean; each hard core's model passes its checker; a person's review of the feature's documents.
- **edge**: a case the signed design did not name, found after signing; the user ruled each in session 150.
- **e7**: unit `e7-agent-type` of contract `execution-team`, which types each team member's start.
- **agent start**: the tokens an agent holds before its first step (its prompt, tools and instructions), resent with each request it makes.
- **team, member**: the agents `/sdlc execute` starts: QA (drafts the tests), QA verifier, test-retirer, Developer, Dev verifier.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
- **manual receipt**: evidence from a live run a test cannot stand in for, kept in an untracked `RECEIPT_*` folder.
- **TLC, P**: the outside checkers G1.2 starts: TLC checks a TLA+ model, P checks a P project.
