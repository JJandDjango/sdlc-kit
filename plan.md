# Plan - Session 79 (2026-10-07) - document-split d2

**Deliverable:** unit `d2-design` of `document-split` on one PR, with a
Two-Key PASS:

- `skills/product-specification-interview/`: a design run is the same
  skill with a second argument, `design`. It writes the design document
  at `docs/features/<id>.design.md`, with its own state file, from a new
  design template. The document names the text revision of the
  requirements document the design stands against. It then holds the
  seven Proposed solution sections in the ratified order, the Risks
  section, each consult case, its own Decisions section, Traceability,
  Notes and the Appendix's Contract block. It holds no section tagged
  for the PO seat. The Google Docs form of either document shows only
  that one. Check SC1.2.
- The run starts only when the requirements document holds the PO
  seat's signature on its last text revision; otherwise it stops with
  its error and writes nothing. It needs an engineer seat and no PO
  seat, shows that seat each entry the PO seat rejected at Non-goals,
  and covers only the Solution half's steps and the consult cases. A
  later run goes on at the step its state file names. Check SC2.2.
- The run covers the four consult cases with the engineer seat, one at
  a time, at S9, and writes each answer as `yes` or `no`. A `yes` needs
  an entry under `Who was asked` and under `What was decided`, and the
  document shows both. Check SC5.1.
- Retired: S1's branch for no engineer seat and S11's hand-over for it;
  "both seats answer S8"; S2's write into Non-goals and its PO
  signature; the span `S1-S11`, now S1 to S12; and the tests that pin
  them, found by test-retirer (seen: `SOLUTION_STEPS`,
  `test_sc1_2_engineer_seat_decides_whether_the_solution_half_is_asked`,
  `test_sc1_3_solution_flows_purpose_agrees_with_the_step_both_seats_answer`).
- What `d1` left standing, owned here: the dispatch reads `$1` only, so
  `{id} design` re-enters the `complete` route; `SKILL.md`'s
  description, purpose and its lines for S1-S11, with
  `tests/test_interview_signing.py:558` pinning two of its sentences;
  `flows/signing.md`'s context, which names Contract and Record as
  blocks P4 may report; `flows/solution.md` S1's sentence on ready
  check 8; O6's Record clause, back for the design document.
- Constraints in force: every prompt file d2 touches passes `python -m
  prompt_lang`, keeps the PromptLang tag set and stays under 12,000
  characters, and a flow that outgrows the ceiling splits by run into
  another flow file (1); every authored command is one segment (2); the
  skill folder holds Markdown and two templates, no code (3); a design
  run changes no line of the requirements document or of its state
  file (5); the design template's seven sections and Risks and cost
  keep their headings and order (8); no byte changes in the four
  documents Constraints 9 names.

USAGE already holds `d2`'s text, red, approved in session 78, so there
is no pass zero: the unit opens at the drafter. A change to that text
comes to the user in chat first.

The design run's checks before signing, its `Measured:` row and its
`Signed:` row are `d3`'s. `d2`'s run ends where the Solution half's
steps end.

The second machine holds its plugin at 0.18.0 until `d3` merges (user,
2026-10-07). `d2`'s merge to main falls inside that hold.

Approvals split as in session 78: Claude approves the test list and the
unit's commit on review; the plan's commit, the push, the PR and the
merge stay on the user's word.

The session boundary, if context runs short: after step 4. The approved
list, the prototype and the interface note are copied to an untracked
folder in this root, and the developer round opens the next session.

**Closed.** The deliverable is met: `d2-design` stands at `bfd4058`,
Two-Key PASS round 1. The receipts read green at the clean commit:
SC1.2 at 7 tests, SC2.2 at 9 and SC5.1 at 3, the unit's 30 tests, the
whole suite at 962 passed in a scratch venv, `prompt_lang` on the
skill's six prompt files, `validate --profile ready`, and `scope-check`
against `29aedba`. Three older test functions retired and twelve were
amended. The developer ran twice: the second round fixed three
sentences of free wording found on review. The session did not need its
boundary.

## Steps

1. ~~Open.~~ Branch `session-79-document-split-d2` from `29aedba`; this
   plan, committed on the user's word. A scratch venv for the suite and
   the form validator, by `STATE.md`'s two recipes: no Python here holds
   the pane extra or `prompt_lang`.
2. ~~d2, draft.~~ `spec-channel-drafter.js` drafts the test list for
   SC1.2, SC2.2 and SC5.1, proves it red from the repo root, and proves
   it satisfiable on a scratch copy of the skill folder. One drafter, as
   `d1` (198K tokens for two checks); its reading stays on the skill
   folder, the contract, the document's Solution half and USAGE's red
   text.
3. ~~d2, retire.~~ The session overlays the prototype on a scratch
   worktree, runs the whole suite there and names the failing tests and
   their modules; `test-retirer.js` with `overlay` runs only those
   modules.
4. ~~d2, approve the list and prove red.~~ Each fixed detail checked
   against the contract, the feature document, its Constraints and
   USAGE's red text; caps pinned against free text with line breaks;
   session labels stripped; then `progress run <check> --expect red`
   for each of the three checks, the command run alone first.
5. ~~d2, green.~~ `unit-developer.js` from the interface note, handed
   over as a file outside the drafter's folder; Claude runs the suite,
   `prompt_lang` and the size cap after each round, tests any deviation
   against `done_means`, and reads each new step against ADRs 0029 and
   0033 to 0037.
6. ~~d2, commit and Two-Key.~~ Commit with the `Contract:` trailer; each
   check green at the clean commit; `ready-green` and `scope-green`
   against `29aedba`; `two-key-unit-verifier.js`; `progress done` on
   PASS.
7. ~~Close.~~ `STATE.md` regenerated; this plan struck; the memory index
   updated; the push, the PR and the merge on the user's word.

Steps 1 and 7 sit outside a contract unit, so the tree does not show
them.

Decisions this session: five, as planned. The user's: (1) this plan and
its commit. (2) The push and the PR, and (3) the merge, wait on the
user's word. Claude's, on review: (4) the test list, with three
retirements, twelve amendments and two docstring lines the session
corrected in the amended modules; (5) the unit's commit. Claude's
readings, each in the unit's commit message: the design template holds
a `{cases}` placeholder and S9 writes the table; `SKILL.md`'s
description and purpose stand, since each seat still signs its half in
its own document; the stop on a combined document is pinned in `d2`, as
the feature document's edge states it.

Deferred, not this session:
- `d3-signing` to `d6-release` (ships 0.19.0), one unit a session.
- What `d2` leaves standing, listed in `STATE.md`'s Now, all `d3`'s:
  Two-Key's three advisories on the skill (`flows/solution.md`'s
  frontmatter description, `SKILL.md`'s criteria at lines 107 and 110,
  `flows/signing.md`'s E1 and E6), `SKILL.md`'s step 2 and constraints
  on "a half after its seat signed", and the way back to a section from
  a finished design state.
- The fifth thing `d1` left standing is `d3`'s: its retire list finds
  the two tree tests already gone.
- Whether the second machine's marketplace updates on its own: not
  checked, and the plugin hold rests on it.
- A test of the plugin update on the second machine, after `d3`'s
  merge; the `pip` half there takes a commit sha in place of the tag.
- Whether combined documents are in flight on the second machine: not
  known, and the design holds either way.
- The interview's last step for this feature's own document, W1: the
  Google Docs form, when one is wanted. The `google_workspace` server
  failed to connect again this session.
- G1's design document, through a design run once 0.19.0 ships.
- `test-retirer.js` waits on the whole suite inside its agent; the fix
  stays parked, and step 3 works around it.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; never two whole suites at
once; no spawn opens a window; a surprise mid-build is an OPEN and a
re-intake, never a silent edit.
