# Plan - Session 80 (2026-10-07) - document-split d3

**Deliverable:** unit `d3-signing` of `document-split` on one PR, with a
Two-Key PASS:

- `skills/product-specification-interview/`: each seat's signature lands
  in that seat's own document, as a row `rN: Signed: request half` or
  `rN: Signed: solution half`, right after the row it covers, with no
  row between. Each seat's checks before signing run on that seat's
  document and land there as a `Measured:` row. A design run changes no
  line of the requirements document. Check SC2.3, which also takes a
  manual receipt: a live run of both runs on a small feature.
- A design document names one text revision of the requirements
  document: the last one the engineer seat accepted the design against.
  A design run that goes on while a later text revision stands names
  each revision between and asks the engineer seat whether the design
  still stands against each. On the seat's word the design document
  gains a text revision that names the later one, and the run then
  needs a new signature. Check SC3.1.
- The engineer seat's checks before signing report as an OPEN, with its
  notice, each consult case with no answer and each `yes` that lacks an
  entry under `Who was asked` or under `What was decided`. The seat's
  word to sign still stands. Check SC5.2.
- Retired: E6's way back into the request half; E7's move of the
  Gherkin stamp; E1's path to the one state file; the span "ready
  checks 11 to 14"; and the tests that pin them, found by test-retirer
  (seen: `DRAFT_COMMAND`, `MEASURED_SOLUTION`,
  `test_sc2_2_ready_checks_11_to_14_stand_as_questions_before_the_engineer_seat_signs`;
  the two tree tests the Retirements cell names are already gone).
- What `d2` left standing, owned here: `flows/solution.md`'s
  frontmatter description omits Consult cases; `SKILL.md`'s criteria at
  lines 107 and 110 speak for the requirements run alone; `SKILL.md`'s
  step 2 and constraints still say "a half after its seat signed"; a
  finished design state has no way back to a section; what stands under
  the template's `{cases}` placeholder for a consult case with no
  answer.
- Constraints in force: every prompt file d3 touches passes `python -m
  prompt_lang`, keeps the PromptLang tag set and stays under 12,000
  characters, and a flow that outgrows the ceiling splits by run into
  another flow file (1); every authored command is one segment (2); the
  skill folder holds Markdown and two templates, no code (3); a design
  run changes no line of the requirements document or of its state
  file (5); the design template's seven sections and Risks and cost
  keep their headings and order (8); no byte changes in the four
  documents Constraints 9 names.

USAGE already holds `d3`'s text, red, approved in session 78, so there
is no pass zero: the unit opens at the drafter. A change to that text
comes to the user in chat first.

The tight spot: `flows/signing.md` stands near 10,700 of its 12,000
characters. The drafter replaces sentences first. If the design run's
steps do not fit, it splits the flow by run into another file, and the
four older tests that pin the five flow files are amended; Claude rules
on that at step 4 and tells the user.

`d3`'s merge ends the second machine's plugin hold (user, 2026-10-07).

Approvals split as in sessions 78 and 79: Claude approves the test list
and the unit's commit on review; the plan's commit, the push, the PR
and the merge stay on the user's word.

The session boundary, if context runs short: after step 4, as in
session 79 (the approved list, the prototype and the interface note
copied to an untracked folder in this root). A second one after step 6:
the unit stands committed, and the live run and Two-Key open the next
session.

## Steps

1. Open. Branch `session-80-document-split-d3` from `58eb097`; this
   plan, committed on the user's word. A scratch venv for the suite and
   the form validator, by `STATE.md`'s two recipes.
2. d3, draft. `spec-channel-drafter.js` drafts the test list for SC2.3,
   SC3.1 and SC5.2, proves it red from the repo root, and proves it
   satisfiable on a scratch copy of the skill folder. One drafter, as
   `d2` (207K tokens for three checks); its reading stays on the skill
   folder, the contract, the feature document's signing and revision
   text, and USAGE's red text.
3. d3, retire. The session overlays the prototype on a scratch
   worktree, runs the whole suite there and names the failing tests and
   their modules; `test-retirer.js` with `overlay` runs only those
   modules.
4. d3, approve the list and prove red. Each fixed detail checked
   against the contract, the feature document, its Constraints and
   USAGE's red text; caps pinned against free text with line breaks;
   session labels stripped; then `progress run <check> --expect red`
   for each of the three checks, the command run alone first.
5. d3, green. `unit-developer.js` from the interface note, handed over
   as a file outside the drafter's folder; Claude runs the suite,
   `prompt_lang` and the size cap after each round, tests any deviation
   against `done_means`, reads the developer's free wording against
   each step it touches, and reads each new step against ADRs 0029 and
   0033 to 0037.
6. d3, commit. Commit with the `Contract:` trailer; each check green at
   the clean commit; `ready-green` and `scope-green` against `58eb097`.
7. d3, live run (SC2.3's manual receipt). Two worktrees at the unit's
   commit, outside Claude Code's temp tree. `live-run-driver.py` drives
   a requirements run to the PO seat's signature, then a design run to
   the engineer seat's, with `live-run-seats.js` answering as the
   seats; no spawn opens a window. The receipt: each `Signed:` row in
   its own document, and the requirements document byte for byte the
   same before and after the design run. The pair, both state files and
   the transcripts go to untracked
   `RECEIPT_document-split-d3_2026-10-07/`; `d4` and `d5` take their
   manual receipts from that pair.
8. d3, Two-Key. `two-key-unit-verifier.js`, with the live run's text as
   a focus pointer; `progress done` on PASS.
9. Close. `STATE.md` regenerated; this plan struck; the memory index
   updated; the push, the PR and the merge on the user's word.

Steps 1 and 9 sit outside a contract unit, so the tree does not show
them.

Decisions this session: five planned. The user's: (1) this plan and its
commit; (2) the push and the PR; (3) the merge. Claude's, on review:
(4) the test list, with its retirements and amendments; (5) the unit's
commit. A sixth only if USAGE's red text must change.

Deferred, not this session:
- `d4-tree` to `d6-release` (ships 0.19.0), one unit a session.
- A test of the plugin update on the second machine, after `d3`'s
  merge; the `pip` half there takes a commit sha in place of the tag.
- Whether the second machine's marketplace updates on its own: not
  checked; it matters only until `d3` merges.
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
