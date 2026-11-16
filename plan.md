# Session 158 plan: build `s9-one-line-refusals`

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G1, the gate between intake and the first unit's test list, where a feature's requirements and spec are checked before development starts.
**Feature:** g1-requirements-spec (contract `g1-requirements-spec`): G1's three conditions, its venue `/sdlc g1`, and the refusal that keeps a task from starting before G1 passes; `s1` to `s8` on main, `s9` and `s10` ready (design r19, contract rows r14 and r22).
**Unit:** `s9-one-line-refusals`: a file that cannot be read stops no command; `g1-check` and `g1-record` each exit 2 with one line, and the tree goes on.

## 1. The deliverable

`s9-one-line-refusals` built by `/sdlc execute` to a Two-Key PASS, on a draft PR.

## 2. Where this sits

PR #165 (`s8-honest-reads`) merged at `c51dae4` (2026-11-15). `s8` to `s10` ship together as kit 0.22.2 from `s10`, so no release now.

`s9` holds each reader's and writer's failure to one line where today a command ends on a traceback (`docs/features/g1-requirements-spec.design.md:376-383`; Units row at `:470`). Its checks: SC3.3 and SC5.1 (`specs/g1-requirements-spec/contract.yaml:184-199`). The Units row names no manual receipt. The backlog's matching edges stand under Open questions (G1.2's writer tracebacks, `docs/backlog.md:793-797`).

The installed plugin reads `9e59e28`. Between `9e59e28` and `c51dae4` only `skills/sdlc/flows/intake.md` changed in the plugin's flows and agents, so the team that builds `s9` is the one that built `s8`, and no restart is needed.

## 3. The steps

1. Branch `session-158-s9-one-line-refusals` off main at `c51dae4`; this plan committed and pushed.
2. `/sdlc execute g1-requirements-spec s9-one-line-refusals`: QA drafts the test list and proves it red.
3. Stop: the user approves the test list (the tripwire).
4. The rest of the flow: prove-red, the test-retirer, the Developer, the receipts, the Dev verifier, then the QA verifier's mutations.
5. Close: the backlog's `s9` edges closed, a row in `docs/session-metrics.md`, `plan.md` out, push, a draft PR with its readings at the top.

## 4. Where Claude stops for the user

At step 3 (the test list, while the tripwire in `docs/session-metrics.md` stands) and at the PR's review. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1, 2, 4 and 5: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None before the build: the edges, the design row and the contract are signed. The test list is the user's at step 3.

## 7. What could go wrong, already ruled

- QA's result too large to parse comes back empty (session 157, 17 KB): recover it from the member's transcript by a session-local run, as `s8` did.
- `prove.py`'s export holds no `.git`, so a test that lists files through git fails there: the drafter lists files from the disk.
- A kept draft from an earlier run shadows the committed test: start from no kept draft for `s9`.
- The QA verifier's mutation run meets the 600 s Bash cap: at about 100 s a mutation, it keeps to the minimum four.
- Two whole suites at once stop each other: run one at a time.
- A test that writes a non-UTF-8 byte or a NUL through a pipe reads differently on Windows: the tests write bytes, not text, and read output with `errors="replace"`.

## 8. This session's cost, with its basis

About 0.6M to 1.0M agent tokens at one round. Basis: `s7` took 677K at one round on the untyped team (session 149); `s8` took 1,164K over three restarts on the typed team (session 157), whose starts run 18K to 27K against 50K to 54K. `s9` has two checks and six design lines against `s8`'s four and eleven edges. Each failed round adds about 100K to 200K.

## 9. Not in this session

- `s10-words-and-folds`, and kit 0.22.2.
- G2.

## 10. Words

- **G1**: the gate a feature passes before development starts; active for a feature when `G1` is under `active_gates` in `.sdlc/config.yaml` and the feature is not on `g1.exempt`.
- **G1.1, G1.2, G1.3**: G1's conditions: each boundary schema lints clean; each hard core's model passes its checker; a person's review of the feature's documents.
- **reader, writer**: a reader (`tree._load`, `scope_check.contract_scope`, `g1._seat`, `g1-check`) reads a hand-written file; a writer (`g1-record`) writes G1's record.
- **traceback**: Python's multi-line error dump when a command ends on an uncaught error; `s9` replaces each with one line and exit 2.
- **edge**: a case the signed design did not name, found after signing; the user ruled each in session 150.
- **team, member**: the agents `/sdlc execute` starts: QA (drafts the tests), QA verifier, test-retirer, Developer, Dev verifier.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
- **RS302**: G1.3's error code for a feature with no feature document.
