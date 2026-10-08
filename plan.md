# Plan - Session 87 (2026-10-08) - G1, to a ready contract

**Deliverable:** `specs/g1-requirements-spec/contract.yaml` at ready,
derived by intake from the pair `docs/features/g1-requirements-spec.md`
and `docs/features/g1-requirements-spec.design.md` under kit 0.19.0.

Session 86 met the two prerequisites: ADR 0038 and the 14 terms stand on
main (PR #102 at `9f2f9dd`), and its wrap merged as PR #103 at
`04e65c8`. Both halves stand signed at r6, and the design names r6. Two
things are left before the contract: the language door, then intake.

Approvals: four points stay on the user's word. (1) This plan and its
commit; (2) the seats' confirmations at intake, one batch, with the
draft's rewritten sentences shown in chat before and after, and
intake's commit; (3) the push, the PR and the merge of the work, after
CI reads green; (4) the wrap's commit, its PR and its merge. The user
holds both seats.

No code changes this session, so no Two-Key round. The receipts are
`validate --profile ready`, the tree and the whole suite.

No Workflow is planned, so the cost in agent tokens is none (session
77's intake of document-split ran none either).

Claude's readings, each told to the user here:

- The contract derives from r6, the newest text revision both seats
  signed, never from a `Signed:` row.
- Each `done_means` is copied word for word from the design's Units
  table (ADR 0036). Six units, `s1-lint` to `s6-release`.
- The language door rewrites the contract's wording only. The signed
  pair stays as it is, its four stale design sentences among it.
- The standing line, `No new authorizations are added`, stays in the
  document only.
- After intake, USAGE's drawing of G1 as a feature before intake
  (`USAGE.md:1644`) reads as a dated example. It stays, on the user's
  decision; `s6-release` redraws it.

The session boundary, if context runs short: after step 3. The draft
that reads zero is copied to an untracked file in this root, and intake
opens the next session.

## Steps

1. ~~Open.~~ Branch `session-87-g1-intake` from `04e65c8`; this plan,
   committed on the user's word (`d1442b7`).
2. ~~The plugin.~~ Read at resume: the cache holds `863506491ca9`, and
   `git diff --stat v0.19.0 HEAD -- skills/` prints nothing, so the
   installed flows are 0.19.0's.
3. ~~The language door, on a draft.~~ A scratch script builds the
   lexicon with the 89 ratified terms and runs `check_contract` on a
   draft contract outside `specs/`, built from the state files'
   `answers`. Its findings (r5's measure: 79 unknown words, 12
   sentences over the cap) are rewritten there in the contract's
   wording until it reads zero.
4. ~~Intake.~~ `/sdlc:sdlc intake docs/features/g1-requirements-spec.md`
   through the installed plugin: I1 the seat roster, I2 the read of
   both documents (a stop or a park here writes nothing under
   `specs/`), I3 the scaffold, the seats' confirmations in one batch,
   I6 the write, I7 the loop to ready-green, and the `Ready:` rows it
   writes. Then its own commit, with the `Contract:` trailer
   (`84e64c0`).
5. ~~Receipts.~~ `validate --profile ready` on the contract,
   `vocab-check`, `lang-check`, `scope-check --base 04e65c8`,
   `taskcontract tree` showing `gates/G0` done and
   `g1-requirements-spec` with a ready contract, and the whole suite
   under the system Python, each read from its output.
6. ~~The work's close.~~ The push, the PR and the merge, on the user's
   word after CI reads green (PR #104, on main at `fe8bd7b`).
7. ~~The wrap, after the merge.~~ `STATE.md` regenerated, this plan
   struck and the memory index updated on a new branch off main, in a
   wrap-only PR that names the work's merge commit; merged on the
   user's word.

Decisions this session: four planned, all the user's, in four replies
before the wrap. (1) The deliverable and this plan, with its commit;
(2) the readback in one reply: six units kept, the three plan answers,
`user` for both seats, 38 entities, the wording with its five readings,
and intake's commit; (3) the push and the PR, then the merge after CI
read green; (4) the wrap's commit, its PR and its merge.

As it went. Step 3: the requirements document was written by hand and
holds no state file, so the draft was written from the pair, never
built from `answers`. `tools/door.py` ran `check_contract` on it: a
first rewrite read 66 findings, all CL006, and the second read 0, with
each `done_means` at zero as signed. Step 4: I2 found nothing standing
and no stop. The draft went onto the scaffold with `cp`, byte for
byte, and `validate` read ready-green on the loop's first run once
`confirmed_by` stood. The rows are r8 in the requirements document and
r7 in the design document. Step 5, at `84e64c0`: every receipt green,
and the whole suite at 1058 passed in 194 seconds. Step 6: the first
CI watch ended `no checks reported`, and the second read `contracts`
and `test` green. No test changed, and no agent ran.

**Closed.** The deliverable is met: `specs/g1-requirements-spec/contract.yaml`
stands at ready on main at `fe8bd7b` (PR #104, merged 2026-10-08).

Deferred, not this session:
- The build, `s1-lint` to `s6-release`, as kit 0.20.0. `s1-lint` opens
  with pass zero.
- The engine's install ref, its pilot config line and M0's code: after
  G1 ships.
- The `google_workspace` server failed to connect again at this resume.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command
string; commit messages via Write + `git commit -F`; a `Contract:`
trailer, alone in the final paragraph, on every commit that touches a
bound path; never two whole suites at once; no spawn opens a window.
