# Session 161 plan: close B6, the last open G1 edge (`tree.build`'s docstring)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G1, the gate between intake and the first unit's test list, where a feature's requirements and spec are checked before development starts.
**Feature:** g1-requirements-spec (contract `g1-requirements-spec`): G1's three conditions, its venue `/sdlc g1`, and the refusal that keeps a task from starting before G1 passes; `s1` to `s10` on main, released as kit 0.22.2.
**Unit:** none. B6 is a docstring edit to code already on main, ruled a fix for `s10` but not carried by its test list or interface note.

## 1. The deliverable

`tree.build`'s docstring (`taskcontract/tree.py:332-351`) says that in the second build the repository's G1 line, and each of its conditions, still names each feature that holds it; B6 closed on the backlog; a draft PR.

## 2. Where this sits

Kit 0.22.2 is released: PR #167 merged at `9514ff0`, tagged `v0.22.2` there, self-pin PR #168 merged at `cb70530`. Backlog Next 26 (G1's open edges) is marked done; B6 alone stands under Open questions (`docs/backlog.md:764-768`). The design asks it at `docs/features/g1-requirements-spec.design.md:393`: "`build`'s docstring says what the second build prints."

The gap, proved live this session by a scratch probe (G1's whole reading forced to fail on a fixture with two features): the second build prints `gates/G1 [to do]` with `apply-discount holds G1 at to do` and `refund-order holds G1 at to do`, and each condition `gates/G1/G1.1` to `G1.3` the same per feature. The docstring says each feature's G1 conditions and verdict read `to do` "with no diagnostic", and nothing of the gate line, so a reader takes the whole G1 print to carry no diagnostic.

## 3. The steps

1. Branch `session-161-b6-build-docstring` off main at `cb70530`; this plan committed and pushed.
2. Edit the docstring: one sentence on the repository's G1 line and its conditions in the second build.
3. Run the whole suite (`python -P -m pytest tests -q -n auto`); it must stay at 3281 passed.
4. Commit with the `Contract: g1-requirements-spec` and `Theory:` trailers.
5. Close: B6 out of Open questions, Next 26's note says B6 closed; `plan.md` out; push; a draft PR with its readings at the top.

## 4. Where Claude stops for the user

At the PR's review and merge only. Otherwise only on a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Every step: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The edit restates what the code does and changes no signed sentence.

## 6. Rulings needed

None. Two readings, each listed at the top of the PR body:

- No test pins the new sentence. A docstring is not printed; `s10`'s fold of `main_g1_check`'s docstring, taken under the same B6 rule, went in with no test. With no test list, the tripwire (a unit's test list goes to the user) does not apply.
- No Two-Key run. Two-Key grades a unit, and B6 is no unit and changes no behavior; the whole suite and CI are the check.

## 7. What could go wrong, already ruled

- A test pins `build`'s docstring words: none found (searched `tests/` for `get_docstring` and `build.__doc__`; the three hits read module docstrings). If the suite fails on one, the sentence is kept and the pin follows it.
- A line past the code's width: the edit keeps the docstring's 79-column wrap.

## 8. This session's cost, with its basis

No agent tokens: no team run. One whole suite, about 390 s at 3281 tests on this machine (session 159's receipts).

## 9. Not in this session

- G2.
- The other two advisories in B6's backlog entry: an error of another cause passing before the second build prints under G1's name for one print, and a `g1.exempt` entry that is no text printing whole. Both were ruled left (session 150).

## 10. Words

- **G1**: the gate a feature passes before development starts; active for a feature when `G1` is under `active_gates` in `.sdlc/config.yaml` and the feature is not on `g1.exempt`.
- **edge**: a case the signed design did not name, found after signing; the user ruled each in session 150 (letters A1 to H3).
- **second build**: what `tree.build` does when its first build ends on an exception while G1 is active: it builds the tree again reading no G1 source but `g1.exempt`, and adds one problem line naming the error.
- **the repository's G1 line**: the gate item `gates/G1` at the top of the tree print, which rolls up every feature's G1 verdict and names each feature not done.
- **reading**: a call Claude made where the signed documents were silent; each is listed in the PR body for the user's review.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
