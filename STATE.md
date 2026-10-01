# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-10-01 (session 71 close, feature-document f4 built)._

## Now
- **`f4-intake` is built and closed** (session 71, branch
  `session-71-feature-document-f4`): the flow, the tree and the tests at
  `b654e6d`; USAGE at `40c16ce` (intake reads the plan answers from
  Scope, Order and Units) and `e5680cd` (a `Parked:` row is no text row,
  a red subsection at the end of section 9). On a feature document, I2
  reads the document before the scaffold, in three parts. REFUSALS: an
  OPEN mark, a gap under ready checks 1 to 8 and 11 to 14, a check in no
  unit or in two, a unit with no check. PARK: one `r{n}: Parked:` row
  that names every thing that stands, and no contract. SIGNATURES, read
  only when nothing stands: a half with no `Signed:` row, or a text row
  above the newest signed revision, stops intake with no row. I4 copies
  each `done_means` word for word; a pair of checks in one sketch entry
  reads `(SC2.2, SC2.3)`; I7's `Ready:` cell names both seats and the
  revision each signed; I4 and I5 no longer read an Implementation
  section. `_NOT_TEXT` gained `Parked:`. Two-Key PASS at round 1, suite
  915. One unit remains: `f5-release` (SC5.1, SC5.2).
- The rulings (user, 2026-10-01): intake parks before it stops, so a
  missing signature never hides a refusal and gets no `Parked:` row; a
  copied `done_means` is never reworded at intake, and a change goes to
  the document's Units row through the interview and a new signature.
  A reading told to the user: one `Parked:` row names every thing that
  stands, in a fixed order.
- SC4.1's manual receipt is taken: two headless intake runs at `b654e6d`
  on f3's `hello-name.md`, one turn each. Run A parked on the two OPEN
  marks (`r8`). Run B, after a hand edit signed at r10, parked with
  `Check SC2.2 is assigned to no unit.` (`r11`). Neither wrote a
  contract, and the tree read the solution half `done by raj at r9`. The
  documents and transcripts stand untracked in
  `RECEIPT_feature-document-f4_2026-10-01/`, beside f3's receipt folder.
- `f1-format` closed in session 68, `f2-sections` in session 69,
  `f3-signing` in session 70.
- The contract at intake (session 67): ADR 0036 and 15 terms at
  `fde018d`, the contract at `63508f2`, six readings kept at readback.
- Risk 5 stands: the interview never picks up a document it did not
  start, so G1's solution half is written by hand from the two NOTES
  files.
- Kit 0.17.0 is released and self-pinned (PR #76 merged at `e833283`).
  The user's order (2026-09-29) stands: `feature-document` (0.18.0) before
  G1's solution half. When it ships, tell the user the kit is ready on
  the other machine, with the tag to install. Until then another machine
  installs `v0.17.0` and runs the interview by hand from the two
  `NOTES_feature-document_*` files.
- Carried: 19 features: 18 with a contract, 16 of them `[done]`;
  `glossary-alias-disjointness` parked by the user, `[to do]`;
  `feature-document` `[doing]`, f1 to f4 closed; `g1-requirements-spec` before
  intake, `[doing]`.

## Blockers
- None. Session 71's branch waits for the push, the PR and the merge,
  each on the user's word.

## Next actions
1. Release 0.18.0: `f5-release` (session 72), the last unit of
   `feature-document`. Its Retirements row names what moves: `KIT_VERSION`,
   `pyproject.toml` and `sdlc.yml` to 0.18.0, USAGE's marks to green, a
   `CHANGELOG.md` entry, `MAP.md:42`'s v1 interview row. Its Two-Key runs
   with `sweep: true`. Carried for it:
   - f5's sweep, intake (f4's Two-Key, six advisories): USAGE's green
     text at `:1170` and `:1427` lists three row kinds and must gain
     `Parked:` when the marks turn; `USAGE.md:594` says "asks the seats"
     where the flow asks the engineer seat; the red paragraph at
     `USAGE.md:593` stands inside green section 8; `intake.md:23` uses
     "above" for a table position and for a higher revision number; I5
     still offers `strike`, which on a feature document leaves checks in
     no unit after I2's refusals ran; and `skills/sdlc/SKILL.md` (an open
     question below). From the drafter: after a `done_means` change goes
     back to the document at I5 or I7, a contract file exists, and the
     next run meets I3's "contract already exists, ASK".
   - f5's sweep, the signing flow (f3's Two-Key and live run): E2 gives
     a free path (`CHANGELOG.md`, `MAP.md`) no exemption, so a release
     row that names one reads `outside Scope`; S6 never asks which unit
     is the release unit; P6 writes `next: P1` before Q15 proposes a
     changed check's scenario again, so a pause there skips it (the
     stale report then shows it); E6's path back into a request-half
     section runs neither Q15 nor P1 to P5 again, and leaves the order
     of the PO seat's new signature and E1 unsaid; Q14 never asks
     whether a term amends another; S3 never asks for each output kind,
     so ready check 12 opens with no turn to answer it; the "sections
     written" count in the finished rows is one a seat cannot check;
     with no engineer seat, S1's Out of scope lines land under no text
     row. In the live run E1 showed 3 of the command's 16 lines, against
     "SHOW its lines as printed".
   - f5's sweep, the command: with a repo dictionary that cannot be
     read, `--draft` prints its `CL000` line and still ends `(no
     dictionary here - door at rest)`.
   - f5's sweep, wording: `SKILL.md` and `USAGE.md:139` say "then
     eighteen sections" after the status line, but ADR 0029's eighteen
     count the table, the title and the status line; USAGE says the PO
     seat "accepts, edits or drops", the flow "accept, change or drop",
     the contract's words.
2. Then G1's solution half, by hand from the two NOTES files (the
   interview never picks up a document it did not start, feature-document
   risk 5), to ADRs 0033 and 0036; open for it: where the component declaration record and
   the review record live, G1's rules and their codes, the venue, and how
   the 16 features done read G1 inactive once G1 is active. Then its
   intake. The pilot's config line, in the engine's session; the engine's
   install ref moves to the newest tag there (pull, not push).
3. Prerequisite 7: feature documents for the 15 contracts without one,
   each through its own interview.
4. Small, parked: `test-retirer.js` has its agent wait on the whole
   suite, and the run dies when the agent returns (session 68); hand the
   suite run to the session. Its overlay cannot delete a file, and its
   `tar` step needs `--force-local` under Git Bash (session 69). t4's four Two-Key advisories (USAGE:904's "The `G0`
   verdict still reads from the validator" unqualified; wrap nits at
   USAGE:686, :1101, :1142; the ratified Diagnostic term,
   `specs/vocabulary/diagnostic.yaml`, still says "under its condition",
   which only a ratification changes); `taskcontract/__main__.py:85`'s
   `--follow` help still describes the 0.15.0 pane; Two-Key's wording
   advisories (CHANGELOG's and ADR 0032's "a closed contract reads done
   whatever its verdicts read" omit the later-record limit); two test gaps
   (no pane test for a `parts:` list without `evidence` hiding a seat;
   `tests/conftest.py`'s row pattern splits a plain name at its first
   ` [`).
5. Deferred, carried: `glossary-alias-disjointness` (parked by the user,
   2026-09-26); `derived-language` (prerequisite 5); ADR 0029's appendix
   copy and Gherkin for project-tree; flag the Claude pane itself; the
   hook's key action and its four known edges, in its README;
   `.sdlc/config.yaml` still lists `plan.workflow.json` as a free path;
   the advisories at `a800c34:STATE.md` Next actions 4; `spec-doc-type`;
   the demo intake; wave B; 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; the prototype renderer's two gaps
   (`styled-rendering`).

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
- A new feature starts as a feature document written through an
  interview, in the format ADR 0029 ratified and 0033 to 0036 amended,
  tracked at `docs/features/<id>.md`; never a request typed from a sketch.
  Until `feature-document` lands, the interview runs by hand from
  `NOTES_feature-document_2026-09-18.md` and
  `NOTES_feature-document-amendment_2026-09-27.md`. A seat signs its half
  with a row `rN: Signed: request half` or `rN: Signed: solution half`,
  written right after the row it signs (ADR 0034). The checks before
  signing run from a scratch script: add the document's new terms as
  drafts to `load_terms`, report CL003 through
  `lang.validate_dictionary_doc`, and run `lang.check_contract` on a draft
  contract holding the statement, the non-goals, the checks and each
  unit's `done_means` (the Units table's Done means cell, which intake
  copies word for word); a `Violation`'s code is its `rule` field.
- A deferred item that waits on a prerequisite is measured again once the
  prerequisite lands, before it becomes work.
- Intake from a feature document: ratify its new terms first, in their
  own commit, with any ADR the document's prerequisites name. A term
  whose single-word name or slug equals a dictionary word trips CL003;
  the dictionary cedes the word in the same commit. Check each amended
  term's neighbors for a definition the change contradicts. Check the
  document's Scope against the release unit's needs:
  `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml`.
  Intake copies the document's title line into the contract's `title`,
  and derives from the newest text revision both seats signed, never from
  a `Signed:` row. A unit holds at most three sketches: pair two checks in
  one sketch ending in both ids. Each `done_means` is copied word for word
  from the document's Units table (ADR 0036). For the language door, a
  scratch script builds `lang._Lexicon(load_repo_dictionary,
  load_terms)`, runs `check_contract` on a draft outside `specs/`, and
  probes words; scaffold only after the draft reads zero.
- A plan is plan.md's numbered steps, shown in chat for the user's
  overview. A USAGE refinement never narrows a contract sentence
  silently: flag any narrowing or reading to the user before approval. A
  release rewrite that simplifies a rule gets checked against the code
  first.
- A release sweep reads each changed page end to end against the code,
  besides a `git grep` per stale class: grep finds a sentence by its
  words, and a table row or a general "a verdict" carries none of the
  words a new kind of item brings (session 64 lost three rounds to it).
  Sweep test docstrings too; the grader counts them as shipped.
- ADRs are append-only (`DOCS-SYSTEM.md:45`): a later ADR amends an
  earlier one in its own text, never an edit.
- Record each task as it finishes through `taskcontract progress`, and
  each check's run through `progress run <check> [--expect red] --
  <test command>` with `-k`. Run a check's green after its commit with no
  tracked file modified: commit a plan edit on its own first. Close each
  unit with `progress done` once its Two-Key passes. A failed round is
  `progress block <unit>/two-key --reason`, then `start` again. A release
  unit that writes no tests skips write-tests and prove-red.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- A delegated session: one Workflow per step, launched by `scriptPath`
  from `.claude/workflows/`. Keep each agent's reading narrow (the user
  stops an agent past about 400K tokens). `test-retirer.js` takes
  `overlay` (the prototype's changed files) when no name goes. The release
  unit's Two-Key runs with `sweep: true`. Every Two-Key receipt must exit
  0. Session 64's Two-Key rounds: 278K, 242K, 254K and 243K; session
  68's f1: 226K; session 69's f2: 263K (drafter 221K, retirer 80K,
  developer 131K and 62K). A workflow agent's whole-suite run can die
  when the agent returns: run it in the session and classify from its
  output. For the retirer, run the overlaid suite in a scratch worktree
  first, then name the failing tests in `context`, have it run only
  their module, and say any file deletion there. Never run two whole
  suites at once: the session's run was stopped three minutes in while
  a developer's ran (session 69). For
  a prompt-only unit, the drafter's prototype is a scratch copy of the
  skill folder, not the `taskcontract` package (say so in its `notes`).
- Before approving a drafted list: run the whole suite on the prototype
  in a scratch worktree (`git worktree add --detach`, overlay, `python -P
  -m pytest <worktree>/tests`); check each fixed detail against the
  contract, the feature document and its Constraints; pin caps against
  free text holding line breaks; strip session labels; check for a
  repeated name. An edge left unpinned must still agree with the USAGE
  text the user approved.
- Before accepting a developer deviation, test it against every
  done_means sentence. Run the suite yourself after every developer round;
  a developer whose suite run outlasts its turn leaves Claude's run as the
  receipt. A path wrapper left with no caller goes. For a prompt unit,
  read each new step against the ADRs the format cites, besides the
  interface note: f2's S6 lacked ADR 0033's tests and retirements until
  a second developer round (session 69).
- A manual receipt (a live pane) is taken after the commit and handed to
  Two-Key as a focus pointer holding its text. The herdr probe: `herdr
  pane split --pane <own> --direction down --cwd <root> --no-focus`, `pane
  run <new> "python -m taskcontract tree --follow --root <root>"`, `pane
  wait-output <new> --match <text>`, `pane send-keys <new> down ...` to
  move, `pane read <new> --source visible`, `pane close <new>`. Own pane:
  `printenv HERDR_PANE_ID`. Never report state on another session's pane.
- A live run of the interview (session 70): two worktrees at the unit
  commit, outside Claude Code's temp tree. One is the plugin folder
  (`--plugin-dir`), the other the repository the session runs in; a
  session may not write in its own plugin's folder, where every write
  reads "a sensitive file". The skill's name takes the plugin folder's
  name (`<folder>:product-specification-interview`), never `sdlc:`,
  which is the installed release. The second session runs headless
  (`claude -p`, then `--resume <id>` per turn) through
  `.claude/workflows/live-run-driver.py`, which runs each turn detached
  and hidden (`CREATE_NO_WINDOW`: a window that takes the focus is not
  acceptable); `.claude/workflows/live-run-seats.js` has one agent answer
  as the seats from a script, blind to the skill's files. About 100
  turns, 35 minutes, 85K tokens. Copy the document, its state file and
  the transcript to an untracked `RECEIPT_*` folder before the worktrees
  go.
- A unit with a code half and a prompt half (session 70): two drafter
  runs side by side, each with its own scratch folder and test file,
  then two developers side by side on separate files, each told not to
  run the whole suite; the session runs it once after both. Session
  70's f3: drafters 222K and 255K, retirer 93K, developers 108K, 113K
  and 74K, Two-Key 334K. Hand each developer its interface note as a
  file, written from the drafter's result by a script. Session 71's f4:
  drafters 147K and 166K, an amendment round 116K, retirer 69K,
  developers 62K and 59K, Two-Key 263K. A ruling that lands after the
  draft goes through a narrow amendment round of the same drafter: it
  copies the draft and the prototype to a new scratch folder, changes
  both only as the pins need, and returns the whole interface note.
- A live intake run (session 71): the same two worktrees and driver as
  the interview's live run, one driver copy and `live/` folder per run.
  The first message is `/<plugin folder>:sdlc intake
  docs/features/<id>.md`; a document that parks ends in one turn, so the
  session drives it and no seat agent is needed. A hand edit that stands
  in for the interview adds a text row, a `Signed:` row after it, and
  moves the Gherkin's stamp.
- A red USAGE sentence in section 9 goes under its own red subsection at
  the section's end: `tests/test_tree_conditions.py:752` holds the green
  subsections free of red marks.
- The whole suite runs 3 to 6 minutes; a local model holding RAM can get
  a background run killed for memory. A PR's CI waits through `gh pr
  checks <n> --watch` in the background.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  against the new tag with `python -P`. main's ruleset requires a PR for
  every change.

## Open questions
- `skills/sdlc/SKILL.md:75`, `:79` and `:91` say intake writes only
  `specs/{id}/contract.yaml` and never touches `docs/`, while the flow
  writes `Ready:` and `Parked:` rows into the document (the `Ready:` row
  since 0.17.0). `SKILL.md` stands outside `feature-document`'s Scope:
  widen the Scope through a re-intake before f5, or give the fix its own
  small contract? (f4's Two-Key, an advisory.)
- `lang-check --draft` runs none of vocab-check's own rules on a draft
  term, as the feature document's Interfaces draws it. A term with a
  definition under 20 characters (VT002) or a name that fails the slug
  pattern (VT006) reads clean before the PO seat signs and fails once
  intake writes its term file. Add the two rules to the command, or
  leave them to intake? (f3's Two-Key, an advisory.)
- `lang` skips an ALL-CAPS token before it matches a glossary phrase, so
  "OPEN mark" never matches its own term (`mark` reads unknown); the
  contract says "an OPEN". Fix in `lang.py`, or leave?
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42,
  45 to 47, 52 to 54, 61 to 63). Does the term need a word for a
  delegated approval? Beside it: G0.3's unit confirmation repeated the
  engineer seat's signature on project-tree and tree-first-level.
- A feature before intake's id compares as an exact string, so on
  Windows `docs/features/Ready.md` beside `specs/ready/` shows as a
  second feature. Leave it, or match ids without case?
- `lang-check` does not resolve a plural of a glossary term (`features`
  against Feature, `halves` against Half).
- Should `page:` print a URL (the kit's repo at the pinned tag)?
- Push `E:\herdr-sdlc` to GitHub, so herdr can install it as a plugin?
- Which request carries `no-check-reads-the-source-document`?
- d6's two open advisories, wording only (USAGE section 8's
  `confirmed_by` label; the G0.2 hook test's replace).
- `taskcontract/__init__.py` says `__version__ = "0.3.0"`; nothing reads it.
- `/sdlc audit` drops a `W001` warning beside an error.
- Should TC016 ride the parked line?
- Track `.claude/workflows/`? Its four scripts hold the session method and
  exist only on this machine; the Two-Key grade prompt still names a
  Co-Authored-By line, and another machine has none of them.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
- The engine's `plan.md` holds an uncommitted edit; the engine session's
  to commit.
