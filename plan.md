# Plan - Session 64 (2026-09-29) - tree-first-level t4, release 0.17.0

**Deliverable:** unit `t4-release` of `tree-first-level` with its Two-Key
PASS, then the release: the merge, the annotated tag `v0.17.0` at the
merge, and the self-pin through its own PR. t4's done_means: kit `0.17.0`
ships with the `USAGE.md` marks all green and its `CHANGELOG.md` entry;
`KIT_VERSION` reads `0.17.0`. Its check: SC4.2, a feature with a contract
reads its plain name from its contract's `title`, never from its doc.

**Rulings at plan review** (Claude's recommendation; the user's to make):

1. No test list for t4. t2's tests already pin SC4.2:
   `tests/test_tree_before_intake.py:640` and `:668` write a doc titled
   "Apply one discount code per order" beside a contract titled "The
   contract's own title for this feature", and read the contract's. t4
   records SC4.2's run green on them, as o7 did with SC1.3; write-tests
   and prove-red are skipped.
2. Session 55's split: Claude writes the release text, the user approves
   it in one batch shown in chat as before and after, then approves the
   commit (t4's seat is `user`). No developer agent, since t4 changes only
   text and two version strings. Two-Key runs through the verifier
   Workflow with `sweep: true`.
3. A new ADR 0035 rides the release text. ADR 0034 records only the
   signature form. The gate item's roll-up and the feature before intake
   (the tree now reads a doc with no contract, its title line included)
   amend ADR 0032's "the tree reads one part of one document", and no ADR
   says so yet. o7 shipped ADR 0032 the same way.
4. The sweep fixes each advisory that still has a text to fix: USAGE's
   "Six statuses" (`USAGE.md:632`), the 0.16.0 drift text
   (`USAGE.md:994`), the no-signature list (about `USAGE.md:1272`),
   `tree_view.py`'s docstring, `tree.py:14`, `:67` and `:87`. Three stay
   as they are: the SC1.1 sketch (a ready contract is immutable),
   `709d2cc`'s message (history) and the `Theory:` placement (the house
   form).

## Steps

1. Open. PR #74 merged at `a5ba12c`; branch
   `session-64-tree-first-level-t4` cut from it; this plan committed on
   its own.
2. The release text, drafted by Claude: section 9's three 🔴 subsections
   go 🟢 and its "Ratified, not shipped" note folds into the shipped note
   (kit 0.17.0, ADR 0034, ADR 0035, contract `specs/tree-first-level/`);
   the CHANGELOG 0.17.0 entry; ADR 0035; MAP's work-tree row (gate
   roll-up, features before intake, the 0034 and 0035 links); the sweep of
   ruling 4. The user approves it in one batch.
3. The version: `0.17.0` in `pyproject.toml` and `skills/sdlc/init.py`.
   The whole suite runs before the commit.
4. t4's commit, on the user's approval; then SC4.2's run green with no
   tracked file modified.
5. Two-Key, `sweep: true`. A FAIL gets a fix commit on the user's
   approval, then another round.
6. Close: `STATE.md` regenerated, this plan struck; the push and the PR on
   the user's word.
7. Release: the merge once CI reads green; the annotated tag `v0.17.0` at
   the merge; the self-pin (`.github/workflows/sdlc.yml` and USAGE's `uv`
   line move to `v0.17.0`) on its own PR, which the wrap rides. USAGE's
   `uv` line, run with `python -P` against the tag, must install 0.17.0
   and read `specs/tree-first-level` ready-green.

Steps 1, 6 and 7 sit outside a contract unit, so the tree does not show
them.

Decisions this session, all the user's: (1) this plan and rulings 1 to 4;
(2) the release text batch; (3) t4's commit; (4) a fix commit, if Two-Key
fails; (5) the push and the PR; (6) the merge; (7) the tag and its
message; (8) the self-pin PR.

Deferred, not this session:
- `feature-document` (0.18.0), next: interview its REQUEST into
  `docs/features/`, intake, build, release. When it ships, tell the user
  the kit is ready to use on another machine.
- G1's solution half, then its intake.
- `STATE.md` Next actions 4 to 6 and its open questions, carried
  unchanged.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; the merge, the tag, the push
and the PR on the user's word.
