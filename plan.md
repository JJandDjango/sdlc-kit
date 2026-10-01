# Plan - Session 72 (2026-10-01) - feature-document re-intake and f5

**Deliverable:** `feature-document` released as kit 0.18.0, on one PR,
with a Two-Key PASS on `f5-release`:

- A re-intake first: the document's Scope gains `skills/sdlc/SKILL.md`,
  the engineer seat signs the solution half again, and intake writes the
  contract's `scope` and a new `Ready:` row. No check, no `done_means`
  and no unit changes.
- `f5-release` (SC5.1, SC5.2): `KIT_VERSION`, `pyproject.toml` and
  `sdlc.yml` read 0.18.0; USAGE's interview and intake marks read green;
  `CHANGELOG.md` names the release; `MAP.md:42` names this interview;
  `skills/sdlc/SKILL.md`'s three lines on what intake writes are true.
- The sweep fixes wording against the code. A finding that needs a
  change of behavior is parked as one deferred line.
- SC5.1's manual receipt after the tag: USAGE's `uv` line, run with
  `python -P`, reads 0.18.0, and the plugin at the tag holds the new
  flows.

Approvals split as in session 71: Claude approves a commit on review;
the plan, any ruling, the document's rows and signature, the USAGE text,
the push, the PR, the merge and the tag stay on the user's word.

## Steps

1. Open. Branch `session-72-feature-document-f5` from `b69a923`; this
   plan, committed on its own.
2. Re-intake. The document takes text row r12 (Scope, f5's Retirements
   cell, one decision entry) and `r13: Signed: solution half`. Intake
   then reads the document (I2), adds `skills/sdlc/SKILL.md` to the
   contract's `scope`, keeps the five units, validates ready-green and
   writes `r14: Ready:`. One commit, `Contract: feature-document`.
3. f5, sweep. Read each changed page end to end against the code:
   `USAGE.md`, `skills/sdlc/SKILL.md`, the interview's files and
   `intake.md`, with the carried list in `STATE.md` Next actions 1.
4. f5, release edits. The three version strings, USAGE's marks, the
   `CHANGELOG.md` entry, `MAP.md:42`. SC5.2's test first, proved red.
5. f5, green and commit. The whole suite in the session, scope-check,
   `prompt_lang` on each prompt file touched.
6. f5, Two-Key with `sweep: true`.
7. Release. The push, the PR, the merge commit, the annotated tag
   `v0.18.0` at the merge; then SC5.1's receipt and the unit's close.
8. Close. The self-pin through its own PR, with the wrap; tell the user
   the kit is ready for the other machine, with the tag to install.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Deferred, not this session:
- Each behavior change the sweep finds (seen so far: I5 still offers
  `strike` on a feature document; S6 never asks which unit is the
  release unit; P6 writes `next: P1` before Q15 runs again; E2 gives a
  free path no exemption; S3 never asks for each output kind).
- `lang-check --draft` runs neither VT002 nor VT006 on a draft term.
- G1's solution half by hand (risk 5), after 0.18.0.
- `test-retirer.js`'s whole-suite wait, its overlay and its `tar` step.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`; no tracked file touched while a verifier runs;
never two whole suites at once; no spawn opens a window; a surprise
mid-build is an OPEN and a re-intake, never a silent edit.
