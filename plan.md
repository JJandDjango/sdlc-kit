# Plan - Session 83 (2026-10-07) - document-split d6

**Deliverable:** unit `d6-release` of `document-split` on main through
one PR, with a Two-Key PASS:

- `skills/sdlc/flows/intake.md`: intake stops, with its message and
  nothing written, on a combined document that holds no `Ready:` row. A
  combined document that holds one stays unchanged, and its contract
  validates as before. Check SC4.3. The two messages stand in USAGE,
  red, at lines 413 and 414.
- G1's document stands as a pair: `docs/features/g1-requirements-spec.md`
  keeps every byte, and a design run opens
  `docs/features/g1-requirements-spec.design.md` beside it as r1 against
  requirements r3.
- The release text: USAGE's red marks go green under the 0.19.0 banner,
  a `CHANGELOG.md` entry, `MAP.md`'s interview, intake and tree rows,
  and `docs/gates/G0-planning-intake.md`'s title sentence.
- `KIT_VERSION` and `pyproject.toml` move to 0.19.0.
- The sweep: the wording advisories of `d3` (two), `d4` (one) and `d5`
  (three), listed in `STATE.md` under Now.
- Retired: the tests that pin what the list above changes, found by
  test-retirer (seen: the kit's own tree on G1,
  `tests/test_tree_halves.py:638`, and the pane test under it).
- Constraints in force: each prompt file `d6` touches passes `python -m
  prompt_lang`, keeps the PromptLang tag set and stays under 12,000
  characters (1); every authored command is one segment (2); no new
  `taskcontract` command, and intake keeps its four commands (3); intake
  keeps I1 to I9 and their order (6); the row words stay byte for byte
  (7); no byte changes in `feature-document.md`, `project-tree.md`,
  `tree-first-level.md` or `g1-requirements-spec.md` (9); no new
  dependency, and the contract's schema stays at 1.5.0 (10).

The release itself follows the merge: the annotated tag `v0.19.0` at
the merge commit, the second manual receipt, and the self-pin through
its own PR. It runs this session only if context holds; else it opens
session 84. The plugin follows main, so the merge alone delivers the
new flows to the second machine.

The tight spot, one: `flows/intake.md` stands at 11,005 of 12,000
characters. The two refusals and the sweep's two wording fixes there
share about 990. If they do not fit, Claude names the sentences to
shorten at step 5 and tells the user.

Claude's readings, each settled at step 5 and told to the user:

- The unit lands as two commits on one PR. Commit A holds the flows,
  the release text, the versions and the tests of the refusals and the
  text. The first manual receipt, a design run for
  `g1-requirements-spec`, runs "from the unit's commit", so it runs
  from A. Commit B holds the design document that run wrote, its state
  file, and the tests that read G1 as a pair. Two-Key grades B.
- The tests that read G1 as a pair are drafted with the rest against a
  stand-in design document, and held out of commit A, so the suite
  reads green at each commit.
- The design run's opening asks the engineer seat a few facts. The
  document it writes is G1's real design document, so the user gives
  those answers in chat, once, and the run's script carries them word
  for word.
- A design document at r1 with no signature changes the kit's own tree
  on G1. The drafter reads the new rows from `tree.py`; no code changes.

Approvals split as in sessions 78 to 82: Claude approves the test list
and the unit's commits on review; the plan's commit, the release text,
the opening's answers, the push, the PR, the merge and the tag stay on
the user's word.

The session boundary, if context runs short: after step 2 (the approved
release text saved to an untracked folder in this root); after step 5
(the approved list, the prototype and the interface note saved there);
after step 8 (the unit stands committed, and Two-Key opens the next
session). A release unit lost three rounds in session 72 and four in
session 64.

## Steps

1. Open. Branch `session-83-document-split-d6` from `204b671`; this
   plan, committed on the user's word. A scratch venv for the suite and
   the form validator, by `STATE.md`'s two recipes.
2. d6, the release text. Claude reads each page the unit changes end to
   end against the code (USAGE's sections under red marks, `MAP.md`'s
   three rows, the G0 page, the six advisories' sites), then shows the
   text in chat, before and after: the banner, the `CHANGELOG.md`
   entry, the rows, the title sentence and the sweep's fixes. The user
   approves it as one decision. Any USAGE sentence that narrows a
   contract sentence is flagged there.
3. d6, draft. `spec-channel-drafter.js` drafts the test list for SC4.3
   and pins the approved text; its prototype is a scratch copy of the
   files the unit changes, with a stand-in design document for G1. The
   version is pinned as a floor.
4. d6, retire. The session overlays the prototype on a scratch
   worktree, runs the whole suite there and names the failing tests and
   their modules; `test-retirer.js` with `overlay` runs only those
   modules.
5. d6, approve the list and prove red. Each fixed detail checked
   against the contract, the feature document, its Constraints, USAGE's
   text and the ratified terms under `specs/vocabulary/`; the two
   messages word for word; caps pinned against free text with line
   breaks; session labels stripped; then `progress run SC4.3 --expect
   red`, the command run alone first.
6. d6, green. `unit-developer.js` writes `intake.md`'s two refusals from
   the interface note; the session types the approved text and the two
   versions. Claude runs the suite, `prompt_lang` and the size cap
   after each round, and reads the developer's free wording against
   each step it touches and against every path of the flow.
7. d6, commit A. Commit with the `Contract:` trailer; the suite green
   at the clean commit.
8. d6, the design run for G1 (manual receipt one) and commit B. Two
   worktrees at commit A, outside Claude Code's temp tree; the run goes
   through its opening on the user's answers, and no spawn opens a
   window. The session checks the requirements document byte for byte,
   copies the design document and its state file into `docs/features/`
   and to untracked `RECEIPT_document-split-d6_2026-10-07/`, adds the
   held tests, and commits B. Then SC4.3 green at the clean commit,
   `ready-green`, `scope-green` against `204b671`, and `lang-green`.
9. d6, the install before the tag. USAGE's `uv` line run against commit
   B through a `git+file` address, with `python -P`; its text goes to
   Two-Key as a focus pointer.
10. d6, Two-Key. `two-key-unit-verifier.js` with `sweep: true`, both
    receipts' text as focus pointers that say the grader reads and the
    receipts key runs; `progress done` on PASS. A failed round is
    `progress block`, a fix, and `start` again, three rounds at most.
11. Close the unit. The push, the PR and the merge on the user's word,
    after CI reads green.
12. The release, if context holds. The annotated tag `v0.19.0` at the
    merge commit on the user's word; manual receipt two (USAGE's `uv`
    line against the tag reads 0.19.0, and the plugin at the tag holds
    the new flows); the self-pin (`sdlc.yml` and the install pins)
    through its own PR, which the wrap rides.
13. Close. `STATE.md` regenerated; this plan struck; the memory index
    updated.

Steps 1, 12 and 13 sit outside a contract unit, so the tree does not
show them.

Decisions this session: nine planned. The user's: (1) this plan and its
commit; (2) the release text; (3) the opening's answers for G1's design
run; (4) the push and the PR; (5) the merge; (6) the tag; (7) the
self-pin's merge. Claude's, on review: (8) the test list, with its
retirements and amendments; (9) the unit's two commits.

Deferred, not this session:
- Whether combined documents are in flight on the second machine: not
  known. After `d6`'s merge a combined document with no `Ready:` row
  meets its own message there, so the question closes with the merge.
- G1's design document past its opening, and G1's intake: the next
  feature's work, through 0.19.0's flows.
- Whether a design table with no `Ready:` row should get a mark of its
  own: a term amendment and a USAGE sentence, under `STATE.md`'s Open
  questions.
- Two edges the sources do not decide, under `STATE.md`'s Open
  questions: a seat asked to sign twice on the way back; DESIGN CONFIRM
  before r1.
- The whole suite under the system Python: not yet seen green, so the
  scratch venv stands this session.
- W1, the Google Docs form of this feature's own document. The
  `google_workspace` server failed to connect again at this resume.
- The engine's install ref and its pilot config line: the engine
  session's, after the tag.
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
