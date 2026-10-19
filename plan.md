# plan.md: session 107

**Deliverable:** the `s6-release` sweep advisories (backlog Next actions 6) settled in the docs.
**Branch:** `session-107-s6-sweep`. **Gate:** the signed documents (`CONTRIBUTING.md:17`); no approval before the PR review.

1. Branch off `main`. Done.
2. `docs/gates.md:98`: add one sentence saying G1.1 to G1.3 are `enforced` here since kit 0.20.0 (source: `docs/gates.md:147`).
3. `README.md` "What ships today": add a `/sdlc g1` row and a `progress` refusal row (sources: `USAGE.md:531`, `USAGE.md:1364`).
4. `USAGE.md:1275`: cut "An active gate the kit cannot compute yet reads `to do`." (G0 and G1 both compute now).
5. `docs/operators.md` trigger: no change. The sentence is pinned (`tests/test_g1_release.py:217`) and the signed design backs it (`g1-requirements-spec.design.md:433`: a flow a person signs is no agent's authoring surface). List this reading at the top of the PR body.
6. Check: the suite through one summary script, `/cairn audit`, and a `git grep` for each stale phrase.
7. `docs/backlog.md`: strike Next actions 6; Next 6 stays open, since this sweep adds no test and so does not use `prove.py`.
8. Commit in atomic pieces; the last commit removes `plan.md`; the PR body links it by sha.

**Deferred (one line each):**
- `README.md` omits the tree and the vocabulary layer, and still says "54 specified conditions" (now 57).
