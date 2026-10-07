# Plan - Session 78 (2026-10-06) - document-split d1

**Deliverable:** unit `d1-requirements` of `document-split` on one PR,
with a Two-Key PASS:

- `USAGE.md` gains the feature's new text first, in the interview's
  section and section 9, every status mark red; 0.18.0's interview text
  goes.
- `skills/product-specification-interview/`: a requirements run writes
  the requirements document at `docs/features/<id>.md`. It holds each
  Request half section in the ratified order, with its name and tag as
  0.18.0 writes them, then its own Decisions section and Notes, and the
  Appendix's Gherkin block and Terms block. It holds no Proposed
  solution, no Risks section, no Traceability and no Contract block. A
  fix's document holds all four fix sections. Check SC1.1.
- The run needs a PO seat and no engineer seat. It covers only the
  Request half's steps, the Terms and the Gherkin, runs the PO seat's
  checks before signing, stops at that signature, and names the design
  run as the next command. A later run goes on at the step its state
  file names. Check SC2.1.
- Retired: `templates/feature-document.md.template`, replaced by the
  requirements template; O4's engineer seat question; P7's hand-over to
  S1; ready check 8's "both seats" and its `no engineer seat is named`
  OPEN; W2's intake command after a requirements run; the count "fifteen
  of the eighteen sections"; and the tests that pin them, found by
  test-retirer (seen: `FEATURE_OUTLINE`, `TAGS`, `R1_CHANGES`, the three
  file-set tests,
  `test_sc2_2_no_engineer_seat_skips_the_solution_halfs_steps_checks_and_signature`,
  and the release suite's `BANNER`, `COUNT` and two red-mark tests).
- Every prompt file d1 touches passes `python -m prompt_lang`, keeps the
  PromptLang tag set and stays under 12,000 characters; every command it
  authors is one segment (Constraints 1 and 2). No byte changes in the
  four documents Constraints 9 names.

The second machine, read and not tested: `.claude-plugin/marketplace.json`
sets `source: "./"` with no ref, and both cached plugin copies here are
main commits, so the plugin follows main. A plugin update there after
d3's merge delivers both runs and their signing; no branch install is
needed. Intake reads a pair only after d5. The same fact has a cost: an
update there between d1's merge and d3's delivers an interview that
names a design run no flow holds yet. Recommendation: one PR a unit to
main, as before, and that machine holds its plugin at 0.18.0 until d3
merges. The user rules at step 8, before d1's merge.

Approvals split as in sessions 61 to 64 and 68 to 72: the user approves
the USAGE text in chat before any drafting; Claude approves the test
list and the unit's commit on review; the push, the PR and the merge
stay on the user's word.

The session boundary, if context runs short: after step 5. The approved
list, the prototype and the interface note are copied to an untracked
folder in this root, and the developer round opens the next session.

**Closed.** The deliverable is met: `d1-requirements` stands at
`6602242`, Two-Key PASS round 1, and pass zero at `bcd6600`. The
receipts read green at the clean commit: SC1.1 at 11 tests and SC2.1 at
6, the unit's 22 tests, the whole suite at 935 passed in a scratch venv,
`prompt_lang` on the skill's six prompt files, `validate --profile
ready`, and `scope-check` against `67ac09e`. Eight older test functions
retired and sixteen were amended. The session did not need its boundary.

## Steps

1. ~~Open.~~ Branch `session-78-document-split-d1` from `67ac09e`; this
   plan, committed on the user's word. A scratch venv for the suite, by
   `STATE.md`'s recipe: no Python here holds the pane extra.
2. ~~d1, pass zero.~~ Write USAGE's new text, marks red, shown in chat
   before and after. A red sentence in section 9 goes under its own red
   subsection at the section's end. A release-suite test the red text
   fails is amended or retired in the same commit, and each one is told
   to the user. Commit on the user's word.
3. ~~d1, draft.~~ `spec-channel-drafter.js` drafts the test list for SC1.1
   and SC2.1, proves it red, and proves it satisfiable on a scratch copy
   of the skill folder.
4. ~~d1, retire.~~ The session runs the overlaid suite in a scratch
   worktree and names the failing tests; `test-retirer.js` with
   `overlay` reads only their modules, and is told the template's
   deletion.
5. ~~d1, approve the list and prove red.~~ The whole suite on the prototype
   in a scratch worktree; each fixed detail checked against the
   contract, the feature document and its Constraints; session labels
   stripped; then `progress run <check> --expect red` for each check.
6. ~~d1, green.~~ `unit-developer.js` from the interface note; Claude runs
   the suite, `prompt_lang` and the size cap after each round, tests any
   deviation against `done_means`, and reads each new step against ADRs
   0029 and 0033 to 0037.
7. ~~d1, commit and Two-Key.~~ Commit with the `Contract:` trailer; each
   check green at the clean commit; `two-key-unit-verifier.js`;
   `progress done` on PASS.
8. ~~Close.~~ `STATE.md` regenerated; this plan struck; the memory index
   updated. The user rules on the second machine's plugin hold; the
   push, the PR and the merge on the user's word.

Steps 1 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: seven, as planned. The user's: (1) this plan
and its commit; (2) the USAGE text, with its five readings and six
retired tests, and its commit; (5) the second machine: one PR a unit to
main, as before, and that machine holds its plugin at 0.18.0 until `d3`
merges; (6) the push and the PR. (7) The merge waits on the user's
word. Claude's, on review: (3) the test list, with one assertion
stripped, since it held for this unit only (that W2 names no intake
command); (4) the unit's commit. Claude's readings, each in the unit's
commit message: ready check 8 "names the PO seat alone", in ADR 0037's
words; the two tree tests the Units table lists under `d3` retired in
`d1`, since they drew their document from the deleted template; O6's
Record clause dropped until `d2`; `SKILL.md`'s description and purpose
left as other suites pin them.

Deferred, not this session:
- `d2-design` to `d6-release` (ships 0.19.0), one unit a session.
- What `d1` leaves standing, listed in `STATE.md`'s Now: four Two-Key
  advisories and one line of the unit's commit message. `d2` owns four
  of the five: the design command's dispatch, `SKILL.md`'s description,
  purpose and solution lines, `flows/signing.md`'s context, and
  `flows/solution.md`'s S1. The fifth is `d3`'s: its retire list finds
  the two tree tests already gone.
- Whether the second machine's marketplace updates on its own: not
  checked, and the plugin hold rests on it.
- A test of the plugin update on the second machine, after d3's merge;
  the `pip` half there takes a commit sha in place of the tag.
- Whether combined documents are in flight on the second machine: not
  known, and the design holds either way.
- The interview's last step for this feature's own document, W1: the
  Google Docs form, when one is wanted. The `google_workspace` server
  failed to connect this session.
- G1's design document, through a design run once 0.19.0 ships.
- `test-retirer.js` waits on the whole suite inside its agent; the fix
  stays parked, and step 4 works around it.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; never two whole suites at
once; no spawn opens a window; a surprise mid-build is an OPEN and a
re-intake, never a silent edit.
