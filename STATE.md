# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-21 (session 35 wrap)._

## Now
- Branch `session-33-g0-declaration`, unpushed, over main (`5e26c1b`, kit
  0.13.0). Only `g0-declaration` is in flight; `derived-language`,
  `feature-document` and `spec-doc-type` queue behind it.
- The request stands at **r7**. SC4.2 claimed the `new` skeleton validates
  draft; its TODO intent trips TC007 at both profiles by design (ADR 0016),
  so SC4.2 now checks that the draft verdict is unchanged, TC007 only.
  Re-intaked at `a4d5b5e`; the contract is ready-green with eight units and
  reads zero at the language door.
- **Verified**: d0 `1ad319a`, d1 `6939082`, d2 `c1af342`..`d420f80`, d7
  `8ce629e`+`ff55f5b` (round 3), d3 `ee3ff6d`, d4 `5114f74`+`13f0ca5`
  (round 2), d5 `964f156`. Only **d6** remains, then the release.
- The **blocking bar is applied** in the verifier,
  `.claude/workflows/two-key-unit-verifier.js` (untracked): blocking only
  on a shipped surface; a blocking defect in `plan.md`,
  `plan.workflow.json` or `STATE.md` is demoted by the verdict code and
  listed under `demoted`; `sweep: true` only for d6. All five rounds this
  session passed, about 700K subagent tokens, and still caught real gaps:
  I7's fix loop could empty `entities` without the PO seat, and two
  CHANGELOG lines overclaimed.
- Receipts at HEAD (d5's round, `964f156`): pytest **297 passed**,
  `prompt_lang` 13 of 13, `/sdlc audit` clean, lang-green, `vocab-check`
  green at 18 terms and 8 constraints, schema 1.4.0.
- Two writes landed in the spec channel beyond the two the request
  budgeted, both ruled legitimate: `specs/vocabulary/constraints.yaml` and
  the class-S edit to `specs/vocabulary/task-contract.yaml`. They trip
  different branches of the write-guard, so **the PR must name them on two
  separate grounds**. The r7 re-intake's write to
  `specs/g0-declaration/contract.yaml` is intake's own.

## Blockers
- None.

## Next actions (plan.md step numbers)
1. Step 8, d6 `d6-adoption-and-release`. Read `USAGE.md` whole first. Hook
   tests for SC5.1 (the unlock) and SC5.2 (the re-lock); the USAGE marks
   flip green only after the rewrites step 8 lists: the eight USAGE
   advisories, `docs/gates/G0-planning-intake.md:114`, section 9 resolving
   TC017 and TC018 to their remedies, and `CHANGELOG.md:56`'s parked
   contract that turns invalid once the roster arms TC016; 0.14.0 in
   `pyproject.toml` and `KIT_VERSION`, and the release heading. One commit,
   then Two-Key with `sweep: true`.
2. Launch the verifier by `scriptPath`, never by name, and check that the
   result carries `demoted`.
3. Step 9, on the user's word: PR, merge by merge commit, tag v0.14.0, the
   self-pin in `.github/workflows/sdlc.yml` bound to this contract.
4. Then `derived-language`, `feature-document`, `spec-doc-type`; carried:
   the demo intake, wave B, 5b, the engine's G4.6 finding.

## Standing practice, learned this session
- A saved workflow launched by name ran its pre-edit text; after editing
  one, launch it by `scriptPath` (memory `feedback-workflow-name-snapshot`).
- Probe a unit's premise before building it: `taskcontract new` plus a
  draft validate in scratch showed SC4.2 false before any code was written.
- Each unit's `focus` is its own sketches, unchanged between rounds. An
  advisory that breaks a unit's promise (d4's I7) gets a follow-up commit
  and a new round; the rest stay recorded in `plan.md`.
- Read a file whole before editing it; say only what was checked; run
  anything whose exit code is a receipt through Bash.

## Open questions
- To `feature-document`: a check can carry a false premise about today's
  behavior, and intake derives it unchecked (SC4.2, "still validates
  draft"). Carried: a closing release unit has no check to deliver; checks
  and sketches are not one to one under the three-sketch cap; a
  hand-pasted appendix copy ages at once; a derived `done_means` can read
  broader than the request's verbatim line (d7's "names each missing
  field").
- Its own request: `/sdlc audit` drops a `W001` warning that sits beside an
  error, because the verdict branches are chained.
- Should TC016 ride the parked line? `CHANGELOG.md:56`'s case raises it;
  another request's question, not this contract's.
- Track `.claude/workflows/two-key-unit-verifier.js`? It now holds the
  gate's rules, and untracked it exists only on this machine.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
  Q4, Q5, Q6, PL-PIPE.3: unchanged.
