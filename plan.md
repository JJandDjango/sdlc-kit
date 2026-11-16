# Session 159 plan: build `s10-words-and-folds`, which ships kit 0.22.2

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G1, the gate between intake and the first unit's test list, where a feature's requirements and spec are checked before development starts.
**Feature:** g1-requirements-spec (contract `g1-requirements-spec`): G1's three conditions, its venue `/sdlc g1`, and the refusal that keeps a task from starting before G1 passes; `s1` to `s9` on main, `s10` ready (design r19, contract rows r14 and r22).
**Unit:** `s10-words-and-folds`: each line `g1-record` shows stands in the design word for word, one reader reads a `Ready:` row, and kit 0.22.2 ships `s8` to `s10`.

## 1. The deliverable

`s10-words-and-folds` built by `/sdlc execute` to a Two-Key PASS, on a draft PR that carries kit 0.22.2.

## 2. Where this sits

PR #166 (`s9-one-line-refusals`) merged at `f84b75d` (2026-11-16). `s10` is the last of the three units that close G1's open edges (backlog Next 26); after it, G1 lists no open edge the user ruled a fix.

`s10` takes ten edges of session 150's list: B6, C3, D3, E1 to E5, G1 and H3 (design `docs/features/g1-requirements-spec.design.md:385-393`; Units row at `:471`). Its one check is SC1.1 (`specs/g1-requirements-spec/contract.yaml:200-213`). The Units row names one manual receipt, the install from the tag reading 0.22.2, and one retired test, the one that holds `g1.py`'s `Ready:` reader equal to the tree's. The backlog's matching edges stand under Open questions (`docs/backlog.md:746-765`, `:766-777`, `:791-792`, `:806-812`) and at Next 26's note on the fold (`:435-436`).

The installed plugin reads `9e59e28`. Between `c51dae4` and `f84b75d` nothing under `skills/`, `agents/` or `workflows/` changed, so the team that built `s9` builds `s10`, and no restart is needed.

## 3. The steps

1. Branch `session-159-s10-words-and-folds` off main at `f84b75d`; this plan committed and pushed.
2. `/sdlc execute g1-requirements-spec s10-words-and-folds`: QA drafts the test list and proves it red.
3. Stop: the user approves the test list (the tripwire).
4. The rest of the flow: prove-red, the test-retirer (the equal-readers test), the Developer (the release files with the code, as `s7` did at `5b5899e`), the receipts, the Dev verifier, then the QA verifier's mutations.
5. Close: the backlog's `s10` edges closed and Next 26 marked done, a row in `docs/session-metrics.md`, `plan.md` out, push, a draft PR with its readings at the top.
6. After the user merges: tag `v0.22.2` at the merge, the manual receipt (the install from the tag reads 0.22.2), then the self-pin PR.

## 4. Where Claude stops for the user

At step 3 (the test list, while the tripwire in `docs/session-metrics.md` stands), at the PR's review, and at the merge before step 6. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1, 2, 4 and 5, and step 6 once the user merges: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Claude answers a member's question from the design and lists each answer as a reading in the PR body.

## 6. Rulings needed

None before the build: the edges, the design row and the contract are signed. The test list is the user's at step 3.

One fold Claude adds under B6's rule (a docstring says what the code does), listed as a reading: `main_g1_check`'s docstring (`taskcontract/g1.py:938-941`) omits the exit-2 cases `s8` and `s9` added (a config that cannot be read, a reader that fails) and puts the statuses before the findings, where the code prints them after. It goes to the Developer with Claude's answers; if no question comes, it waits on the deferred list.

## 7. What could go wrong, already ruled

- QA's result too large to parse comes back empty (session 157, 17 KB): recover it from the member's transcript by a session-local run, as `s8` did.
- `prove.py`'s export holds no `.git`, so a test that lists files through git fails there: the drafter lists files from the disk.
- A kept draft from an earlier run shadows the committed test: start from no kept draft for `s10`.
- The QA verifier's mutation run meets the 600 s Bash cap: at about 100 s a mutation, it keeps to the minimum four.
- Two whole suites at once stop each other: run one at a time.
- The fold removes a reader that older tests call: the test-retirer amends them to the one reader, and retires only the equal-readers test the Units row names.
- The version bump fails a test that pins 0.22.1: the Developer moves the pin with the bump, as `s7` did for 0.22.1.
- A word test reads a page through a pipe on Windows: the tests read files as bytes and decode UTF-8.

## 8. This session's cost, with its basis

About 0.7M to 1.1M agent tokens. Basis: `s7` took 677K at one round (session 149); `s8` 1,164K over three restarts (session 157); `s9` 960K over three test rounds (session 158), each on a typed team whose starts run 18K to 27K. `s10` has one check against `s9`'s two, but ten edges of words, a fold and the release files. Each failed round adds about 100K to 200K.

## 9. Not in this session

- G2.
- Backlog Open questions outside the ten edges, including the edges the user ruled left (session 150).

## 10. Words

- **G1**: the gate a feature passes before development starts; active for a feature when `G1` is under `active_gates` in `.sdlc/config.yaml` and the feature is not on `g1.exempt`.
- **G1.1, G1.2, G1.3**: G1's conditions: each boundary schema lints clean; each hard core's model passes its checker; a person's review of 11 items on the feature's documents.
- **edge**: a case the signed design did not name, found after signing; the user ruled each in session 150 (letters A1 to H3 in that session's `plan.md`, `f35c4b2`).
- **fold**: two pieces of code that do one job made one; here, `g1.py`'s `Ready:` row reader and `tree.drift`'s.
- **`Ready:` row**: a revision-table row of a feature document that names the revision intake read, as `Ready: rN`.
- **R5**: the step of `/sdlc g1` that asks a person to answer each of G1.3's 11 items `checked` or `unchecked`.
- **reading**: a call Claude or a member made where the signed documents were silent; each is listed in the PR body for the user's review.
- **team, member**: the agents `/sdlc execute` starts: QA (drafts the tests), QA verifier, test-retirer, Developer, Dev verifier.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
