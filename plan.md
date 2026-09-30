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

**Closed.** The deliverable is met: t4 at `dd225b2` and its fixes
`3076424`, `3da0128` and `b9d080c`, Two-Key PASS at round 4,
`tree-first-level` closed at `b9d080c`; PR #75 merged at `4a9fec0`,
tagged `v0.17.0`; the self-pin at `6c748f6`. Suite 749 passed.

## Steps

1. ~~Open.~~ PR #74 merged at `a5ba12c`; the branch cut from it; the plan
   at `9c4edb2`.
2. ~~The release text.~~ Approved in one batch, 15 edits: section 9 green,
   the green paragraphs t1 to t3 changed rewritten, ADR 0035 (it also
   amends 0029's "no headings read by the tooling"), the CHANGELOG entry,
   MAP's row, the docstring sweep.
3. ~~The version.~~ `0.17.0` in both; suite 749 passed.
4. ~~t4's commit.~~ At `dd225b2`, approved by the user; SC4.2 green after
   it.
5. ~~Two-Key.~~ Round 1 FAIL: USAGE's outline paragraph and two test
   docstrings, fixed at `3076424`. Round 2 FAIL: two more test
   docstrings, fixed at `3da0128` with its five advisories. Round 3 FAIL:
   USAGE's condition id row; the user approved a fourth round past the
   cap, on an end-to-end read of section 9 against the code, which found
   the evidence paragraph too: fix `b9d080c`. Round 4 PASS; t4 and the
   contract closed.
6. ~~Close.~~ `STATE.md` regenerated, this plan struck; they ride the
   self-pin PR.
7. ~~Release.~~ PR #75 merged at `4a9fec0` once CI read green; the
   annotated tag `v0.17.0` there; the self-pin at `6c748f6` on
   `session-64-release`. USAGE's `uv` line, run with `python -P` against
   the tag, installed 0.17.0 and read `specs/tree-first-level`
   ready-green. The self-pin PR's merge waits on the user's word.

Steps 1, 6 and 7 sit outside a contract unit, so the tree does not show
them.

Decisions this session, all the user's: (1) the merge of PR #74; (2) this
plan and rulings 1 to 4; (3) the release text batch; (4) t4's commit; (5)
to (7) three fix commits; (8) the fourth Two-Key round; (9) the push and
the PR; (10) the merge and the tag; (11) the self-pin PR's merge.

Deferred, not this session:
- `feature-document` (0.18.0), next: interview its REQUEST into
  `docs/features/`, intake, build, release. When it ships, tell the user
  the kit is ready to use on another machine.
- t4's four Two-Key advisories (wording), in `STATE.md` Next actions 4.
- G1's solution half, then its intake.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; the merge, the tag, the push
and the PR on the user's word.
