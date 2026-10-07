# Plan - Session 81 (2026-10-07) - document-split d4

**Deliverable:** unit `d4-tree` of `document-split` on one PR, with a
Two-Key PASS:

- `taskcontract/tree.py`: before intake the tree shows a pair as one
  feature, with each document's newest text revision and its signature.
  A feature with a requirements document and no design document yet
  also shows as one feature. A combined document through intake prints
  byte for byte as today. Check SC1.3.
- The unit's `done_means` adds one thing the sketch does not name: the
  tree "marks a design document past its contract". A pair through
  intake gets a drift mark for each table.
- `taskcontract/tree_view.py` and `taskcontract/pane.py` take docstring
  words only.
- SC1.3 also takes a manual receipt: `taskcontract tree` on `d3`'s
  saved pair prints one feature with both marks and both signers.
- Retired: none. The unit's Retirements cell reads "none", so an older
  test that fails on the prototype is an amendment or a finding, and
  each goes to the user.

USAGE already holds `d4`'s text, red, under "A pair of documents"
(`USAGE.md:1672`), approved in session 78, so there is no pass zero:
the unit opens at the drafter. A change to that text comes to the user
in chat first.

The tight spot: `d4` is the first code unit of this build. The
drafter's prototype is a scratch copy of the `taskcontract` package,
not of the skill folder. "Byte for byte as today" is pinned by the tree
tests that stand, so the whole suite on the prototype is the proof, and
it runs in the scratch venv: no Python on this machine holds the pane
extra.

Approvals split as in sessions 78 to 80: Claude approves the test list
and the unit's commit on review; the plan's commit, the push, the PR
and the merge stay on the user's word.

The session boundary, if context runs short: after step 4 (the approved
list, the prototype and the interface note copied to an untracked
folder in this root).

## Steps

1. Open. Branch `session-81-document-split-d4` from `1030c8e`; this
   plan, committed on the user's word. A scratch venv for the suite, by
   `STATE.md`'s recipe.
2. d4, draft. `spec-channel-drafter.js` drafts the test list for SC1.3,
   proves it red from the repo root, and proves it satisfiable on a
   scratch copy of the `taskcontract` package. Its reading stays on
   `tree.py`, the contract, the feature document's tree text, USAGE's
   red text and `d3`'s saved pair.
3. d4, retire. The session overlays the prototype on a scratch
   worktree and runs the whole suite there. `test-retirer.js` runs only
   if an older test fails, on the failing modules alone.
4. d4, approve the list and prove red. Each fixed detail checked
   against the contract, the feature document, its Constraints and
   USAGE's red text; session labels stripped; then `progress run SC1.3
   --expect red`, the command run alone first.
5. d4, green. `unit-developer.js` from the interface note, handed over
   as a file outside the drafter's folder; Claude runs the suite after
   each round and tests any deviation against `done_means`.
6. d4, commit. Commit with the `Contract:` trailer; SC1.3 green at the
   clean commit; `ready-green` and `scope-green` against `1030c8e`.
7. d4, manual receipt. `d3`'s `pair/` copied under a scratch root's
   `docs/features/`; `taskcontract tree` there prints one feature with
   both marks and both signers. The text goes to untracked
   `RECEIPT_document-split-d4_2026-10-07/`.
8. d4, Two-Key. `two-key-unit-verifier.js`, with the receipt's text as
   a focus pointer; `progress done` on PASS.
9. Close. `STATE.md` regenerated; this plan struck; the memory index
   updated; the push, the PR and the merge on the user's word.

Steps 1 and 9 sit outside a contract unit, so the tree does not show
them.

Decisions this session: five planned. The user's: (1) this plan and its
commit; (2) the push and the PR; (3) the merge. Claude's, on review:
(4) the test list, with any amendment; (5) the unit's commit. A sixth
only if USAGE's red text must change.

Deferred, not this session:
- `d5-intake` and `d6-release` (ships 0.19.0), one unit a session.
- `d3`'s two wording advisories (`opening.md`'s purpose and
  `SKILL.md`'s file list do not name DESIGN CONFIRM), for `d6`'s sweep.
- Two edges the sources do not decide, under `STATE.md`'s Open
  questions: a seat asked to sign twice on the way back; DESIGN CONFIRM
  before r1.
- A test of the plugin update on the second machine: the hold ended
  with `d3`'s merge at `1030c8e`.
- Whether combined documents are in flight on the second machine: not
  known, and the design holds either way.
- W1, the Google Docs form of this feature's own document. The
  `google_workspace` server failed to connect again this session.
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
