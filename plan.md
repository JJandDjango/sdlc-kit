# Plan - Session 82 (2026-10-07) - document-split d5

**Deliverable:** unit `d5-intake` of `document-split` on one PR, with a
Two-Key PASS:

- `skills/sdlc/flows/intake.md`: intake takes the requirements
  document's path, finds the design document beside it, and writes one
  contract from a pair that carries each seat's signature and no stale
  design. The statement, the non-goals, the checks and the terms come
  from the requirements document; the scope, the units and each
  `done_means`, word for word, from the design document. Its `Ready:`
  row lands in each table, and a `Parked:` row in each when a refusal
  stands in either document. Check SC4.1.
- Intake stops, with no row and no contract, and reports each case that
  holds, in USAGE's order: no PO signature on the requirements
  document's newest text revision, no engineer signature on the design
  document's, a stale design. Check SC4.2.
- `skills/product-specification-interview/flows/signing.md`: the
  engineer seat's checks before signing report a stale design with the
  message intake prints. Check SC3.2, in one sketch with SC4.2.
- `skills/sdlc/SKILL.md`: its three sentences on intake's row and its
  stops.
- Two manual receipts, each a live intake run on `d3`'s saved pair that
  ends in one turn: with a newer requirements text row it stops with
  the stale message and writes nothing; with one check left out of
  Units it writes a `Parked:` row in each table and no contract.
- Retired: intake's one r{m}, "the newest revision both seats signed",
  and its stop in free words; refusal 1's two "seat boundary"
  sentences; "intake's only write"; `skills/sdlc/SKILL.md`'s three
  one-row sentences; and the tests that pin them, found by test-retirer
  (seen: nine in `tests/test_intake_refusals.py`,
  `test_intake_writes_the_ready_row_in_the_shape_the_tree_reads`, and
  the release suite's `PARKS`, `SIGNATURE_STOP`, `SECTION_8`,
  `STRATA_EXCEPTION`, `INTAKE_WRITES` and `INTAKE_CRITERION`).
- Constraints in force: each prompt file `d5` touches passes `python -m
  prompt_lang`, keeps the PromptLang tag set and stays under 12,000
  characters (1); every authored command is one segment (2); no new
  `taskcontract` command, and intake keeps its four commands (3);
  intake writes one `Ready:` or `Parked:` row in each table and never a
  `Signed:` row (5); intake keeps I1 to I9 and their order, and the
  word `Signed:` stands in I2 and I7 alone (6); the row words stay byte
  for byte (7); no byte changes in the four documents Constraints 9
  names.

USAGE already holds `d5`'s text, red, from line 407 on, approved in
session 78, so there is no pass zero: the unit opens at the drafter. A
change to that text comes to the user in chat first.

The tight spots, two:

- `flows/signing.md` stands at 11,597 of 12,000 characters. E4's stale
  report replaces sentences. If it does not fit, the flow splits by run
  into another file and the older tests that pin the flow files are
  amended; Claude rules on that at step 4 and tells the user.
- `flows/intake.md` stands at 10,029, and `d6` needs room under the
  same ceiling for its two refusals on a combined document. The drafter
  reports the prototype's size, and Claude holds the list until what is
  left fits those two.

Claude's readings, each settled at step 4 and told to the user:

- USAGE's red text names three stops before the read: two on a combined
  document and one on a missing design document. The two on a combined
  document are SC4.3's, so `d6`'s. The missing design document's stop
  is `d5`'s: the pair read cannot run without it.
- Until `d6`, a combined document with no `Ready:` row meets that same
  stop, `No design document for x`. The plugin follows main, so this
  reaches the second machine on its next update after `d5`'s merge.
- The first receipt's hand edit adds a text row and its `Signed:` row
  to the requirements document, so the stale case alone holds.

Approvals split as in sessions 78 to 81: Claude approves the test list
and the unit's commit on review; the plan's commit, the push, the PR
and the merge stay on the user's word.

The session boundary, if context runs short: after step 4 (the approved
list, the prototype and the interface note copied to an untracked
folder in this root). A second one after step 6: the unit stands
committed, and the two live runs and Two-Key open the next session.

**Closed.** The deliverable is met: `d5-intake` stands at `4681b42`,
Two-Key PASS round 1. The receipts read green at the clean commit:
SC3.2 with SC4.2 at 8 tests and SC4.1 at 9, the unit's 17 tests, the
whole suite at 1036 passed in a scratch venv, `prompt_lang` on both
skill folders, `validate --profile ready`, and `scope-check` against
`cc0ebd2`. Both manual receipts hold, in
`RECEIPT_document-split-d5_2026-10-07/`: the stale pair stopped with
the stale message and nothing written, and the pair with SC3.2 left
out of Units took one `Parked:` row in each table and no contract.
Thirteen older tests retired and two were amended. `flows/signing.md`
stayed one file, at 11,730 of 12,000 characters, and `flows/intake.md`
stands at 11,005, which leaves `d6` about 990. The developer ran once.
The session did not need its boundary.

## Steps

1. ~~Open.~~ Branch `session-82-document-split-d5` from `cc0ebd2`; this
   plan, committed on the user's word. A scratch venv for the suite and
   the form validator, by `STATE.md`'s two recipes.
2. ~~d5, draft.~~ `spec-channel-drafter.js` drafts the test list for the
   two sketches (SC3.2 with SC4.2, and SC4.1), proves it red from the
   repo root, and proves it satisfiable on a scratch copy of the two
   skill folders. One drafter, as `d3` (179K tokens for three checks);
   its reading stays on `intake.md`, `skills/sdlc/SKILL.md`,
   `signing.md`, the contract, the feature document's intake text and
   USAGE's red text.
3. ~~d5, retire.~~ The session overlays the prototype on a scratch
   worktree, runs the whole suite there and names the failing tests and
   their modules; `test-retirer.js` with `overlay` runs only those
   modules.
4. ~~d5, approve the list and prove red.~~ Each fixed detail checked
   against the contract, the feature document, its Constraints, USAGE's
   red text and the ratified terms under `specs/vocabulary/`; the three
   messages word for word; caps pinned against free text with line
   breaks; session labels stripped; then `progress run <check> --expect
   red` for each of the three checks, the command run alone first.
5. ~~d5, green.~~ `unit-developer.js` from the interface note, handed over
   as a file outside the drafter's folder; Claude runs the suite,
   `prompt_lang` and the size cap after each round, tests any deviation
   against `done_means`, reads the developer's free wording against
   each step it touches, and reads each new step against ADRs 0029 and
   0033 to 0037.
6. ~~d5, commit.~~ Commit with the `Contract:` trailer; each check green at
   the clean commit; `ready-green` and `scope-green` against `cc0ebd2`.
7. ~~d5, two live intake runs (the manual receipts).~~ Two worktrees at the
   unit's commit, outside Claude Code's temp tree, and one driver copy
   and `live/` folder a run. `d3`'s `pair/` is copied under the
   repository worktree's `docs/features/` and hand-edited for each run.
   The session sends the intake command and reads the one turn; no
   spawn opens a window. Receipt one: the stale message, no row, no
   contract. Receipt two: a `Parked:` row in each table, no contract.
   Both go to untracked `RECEIPT_document-split-d5_2026-10-07/`.
8. ~~d5, Two-Key.~~ `two-key-unit-verifier.js`, with both receipts' text as
   a focus pointer that says the grader reads and the receipts key
   runs; `progress done` on PASS.
9. ~~Close.~~ `STATE.md` regenerated; this plan struck; the memory index
   updated; the push, the PR and the merge on the user's word.

Steps 1 and 9 sit outside a contract unit, so the tree does not show
them.

Decisions this session: five planned. The user's: (1) this plan and its
commit; (2) the push and the PR; (3) the merge. Claude's, on review:
(4) the test list, with its retirements and amendments; (5) the unit's
commit. A sixth only if USAGE's red text must change.

As it went: five, as planned, and no sixth. (1) The user approved this
plan and its commit, `d82144d`. (2) The user gave the word for the
push and the PR, #96, and (3) for the merge once CI read green:
`72ac76e`. Claude's, on review: (4) the test list,
with one amendment before approval, thirteen retirements and two
amended tests; (5) the unit's commit. The amendment: the draft's
sentence of field sources opened on the title sentence's own first
words, which broke `tests/test_tree_titles.py`, a test the unit does
not retire; it now opens "For a pair". The readings named above held.
One more: `d3`'s saved pair carries three OPEN marks, so the receipts'
hand edit closed those too, or the pair would have parked before
intake read the stale design.

Deferred, not this session:
- `d6-release` (ships 0.19.0), the next session.
- Two-Key's three wording advisories (I2's placeholder letters, I8's
  "a parked document", a section comment in
  `tests/test_intake_refusals.py`), for `d6`'s sweep.
- A design run lets a unit hold more than three checks with no `+` in
  its Checks cell: seen in both live runs, under `STATE.md` Next
  actions 2.
- Whether combined documents are in flight on the second machine: not
  known. It decides only whether that machine's plugin update waits for
  `d6`.
- Whether a design table with no `Ready:` row should get a mark of its
  own: a term amendment and a USAGE sentence, under `STATE.md`'s Open
  questions.
- Two-Key's advisory on `tree.py`'s docstring for a contract folder
  named `x.design`, and `d3`'s two wording advisories, for `d6`'s
  sweep.
- Two edges the sources do not decide, under `STATE.md`'s Open
  questions: a seat asked to sign twice on the way back; DESIGN CONFIRM
  before r1.
- The whole suite under the system Python: not yet seen green, so the
  scratch venv stands this session.
- W1, the Google Docs form of this feature's own document. The
  `google_workspace` server failed to connect again this session, after
  the restart that followed `uv`'s install.
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
