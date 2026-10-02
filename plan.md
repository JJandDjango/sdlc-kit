# Plan - Session 72 (2026-10-01 to 2026-10-02) - feature-document re-intake and f5

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

**Closed.** The deliverable is met: PR #84 merged at `771176e`, tagged
`v0.18.0`; the contract closed; Two-Key PASS at round 3; suite 928
passed; SC5.1's receipt taken against the tag. The self-pin and this
wrap ride branch `session-72-release`.

## Steps

1. ~~Open.~~ Branch `session-72-feature-document-f5` from `b69a923`;
   the plan at `e226ea1`.
2. ~~Re-intake.~~ At `6400e5d`: rows r12, r13 and r14; the contract's
   `scope` gains `skills/sdlc/SKILL.md`; the five units kept. No OPEN
   mark, no gap under ready checks 1 to 8 and 11 to 14, each check in
   one unit. Ready-green, suite 915.
3. ~~f5, sweep.~~ `USAGE.md` read end to end, with the interview's seven
   files, both `SKILL.md` files, `intake.md`, `MAP.md`, `CHANGELOG.md`
   and the test docstrings. The fix list and the release text went to
   the user in one batch.
4. ~~f5, release edits.~~ SC5.2's 13 tests from the drafter, red 13 of
   13 before the edits; then the text, typed in the session.
5. ~~f5, green and commit.~~ At `ad20034`: suite 928, scope-check green,
   `prompt_lang` green on both `SKILL.md` files.
6. ~~f5, Two-Key.~~ Round 1 FAIL on three defects (the Intake flow
   criterion's "else", two test comments that counted three rows),
   fixed at `f767494`. Round 2 FAIL on one (USAGE said a step writes
   the Record), fixed at `5fe7c0d`. Round 3 PASS, ten advisories.
7. ~~Release.~~ The CHANGELOG heading took the tag's date at `4d8139c`.
   PR #84 merged at `771176e`; annotated tag `v0.18.0` there; SC5.1's
   receipt against the tag; the unit and the contract closed.
8. ~~Close.~~ The self-pin at `ca99e7a`; `STATE.md` regenerated; this
   plan struck. The push, the PR and the merge of `session-72-release`
   wait on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: thirteen. The user's: (1) the re-intake first;
(2) the document's r12 edit; (3) the solution half signed alone at r13;
(4) the five units kept; (5) ready check 3 reads no gap on a document
with no Gherkin block; (6) the plan; (7) the sweep's wording fixes and
the release text; (8) what is parked; (9) the drafter and Two-Key
workflows; (10) the Record sentence and round 3; (11) the push and the
PR; (12) the CHANGELOG heading takes the tag's date; (13) the merge and
the tag. Claude's, on review: the test list, each commit, and the
one-string amendment of the test's pinned criterion in fix round 1,
told to the user. Two sentences of the CHANGELOG entry were tightened
after approval and told to the user: only the old state file is never
read, and a thin check is one whose scenario cannot be derived or is
dropped.

Deferred, not this session (in `STATE.md` Next actions 2):
- Each behavior change the sweep found in the interview: E2, S6, P6,
  E6, Q14, S3, the "sections written" count, S1's lines under no text
  row, and O6's placeholder for the Record, which no step writes.
- In `intake.md`: I5's `strike`, I3's "contract already exists", line
  23's two senses of "above", and the Appendix's Contract block and the
  status line left as the interview wrote them after a ready intake.
- `lang-check --draft`: its last line on a dictionary that cannot be
  read, and neither VT002 nor VT006 on a draft term.
- Pages: `docs/controlled-language.md` never names `CL014`; USAGE
  section 2 never says the interview needs the plugin; "each heading
  followed by its tag"; two senses of "parked" in
  `skills/sdlc/SKILL.md:91`; `MAP.md:41`; the signed document's own
  "eighteen sections" line and its missing Gherkin block.
- G1's solution half by hand (risk 5), next.
- `test-retirer.js`'s whole-suite wait, its overlay and its `tar` step.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`; no tracked file touched while a verifier runs;
never two whole suites at once; no spawn opens a window; a surprise
mid-build is an OPEN and a re-intake, never a silent edit.
