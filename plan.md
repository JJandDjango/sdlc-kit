# Plan - Session 77 (2026-10-06) - document-split, to a ready contract

**Deliverable:** `specs/document-split/contract.yaml` at ready, derived
by intake from `docs/features/document-split.md` under kit 0.18.0.

Session 76 met the two prerequisites: ADR 0037 and the terms stand on
main (PR #88 at `1b4173b`), and its wrap merged as PR #89 at `7ddbb6f`.
The document stands signed at r7, and its Scope covers the release
unit. Two things are left before the contract: the language door, then
intake.

Approvals: four points stay on the user's word. (1) This plan and its
commit; (2) the seats' confirmations at intake, one batch, with the
draft's rewritten sentences shown in chat before and after; (3)
intake's commit; (4) the wrap's commit, the push, the PR and the merge.
The user holds both seats.

No code changes this session, so no Two-Key round. The receipts are
`validate --profile ready`, the tree and the whole suite.

The session boundary, if context runs short: after step 3. The draft
that reads zero is copied to an untracked file in this root, and intake
opens the next session.

## Steps

1. Open. Branch `session-77-document-split` from `7ddbb6f`; this plan,
   committed on the user's word.
2. The plugin. List `C:/Users/hyden/.claude/plugins/cache/sdlc-kit/sdlc`
   and read `git diff --stat v0.18.0 main -- skills/`: when it prints
   nothing, the installed flows are 0.18.0's.
3. The language door, on a draft. A scratch script builds the lexicon
   with the ratified terms and runs `check_contract` on a draft contract
   outside `specs/`. The draft check's 179 findings are rewritten there
   in the contract's wording until it reads zero. Each `done_means` is
   copied word for word from the Units table. `case` alone is an unknown
   word, and the checks say "the four cases".
4. Intake. `/sdlc:sdlc intake docs/features/document-split.md` through
   the installed plugin: I1 the seat roster, I2 the document read (a
   stop or a park here writes nothing under `specs/`), I3 the scaffold,
   the seats' confirmations in one batch, I6 the write, I7 the loop to
   ready-green, and the `Ready:` row in the document. Then its own
   commit, with the `Contract:` trailer.
5. Receipts. `validate --profile ready` on the contract, `taskcontract
   tree` showing `document-split` with a ready contract, and the whole
   suite from a scratch venv, each read from its output.
6. Close. `STATE.md` regenerated, this plan struck, the memory index
   updated. The commit, the push, the PR and the merge wait on the
   user's word.

Deferred, not this session:
- The build, `d1-requirements` to `d6-release`, as kit 0.19.0.
- Whether the second machine can take the plugin from the build's
  branch after `d3`, before the 0.19.0 tag: not checked, and the build's
  first session opens on it.
- The interview's last step, W1: the Google Docs form, when one is
  wanted. The `google_workspace` server failed to connect this session.
- G1's design document, through a design run once 0.19.0 ships.
- Whether combined documents are in flight on the second machine: not
  known, and the design holds either way.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer,
alone in the final paragraph, on every commit that touches a non-free
path; no spawn opens a window.
