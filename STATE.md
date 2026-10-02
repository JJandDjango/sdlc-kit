# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-10-02 (session 72 close, feature-document released as 0.18.0)._

## Now
- **Kit 0.18.0 is released** (session 72): PR #84 merged at `771176e`,
  tagged `v0.18.0` there, contract `feature-document` closed. The
  self-pin is `ca99e7a` on branch `session-72-release`: the kit's own
  workflow and USAGE's `uv` line take the tag. This wrap rides it.
- The session's commits. `6400e5d`: the re-intake, the document's rows
  r12 (Scope gains `skills/sdlc/SKILL.md`), r13 (the engineer seat signs
  the solution half again) and r14 (`Ready:`, derived from r12); the
  contract's `scope` gained one line and no unit changed. `ad20034`:
  `f5-release`, with USAGE's interview section green, the CHANGELOG
  entry, `MAP.md:42`, the three lines of `skills/sdlc/SKILL.md`, and
  `tests/test_feature_document_release.py` (13 tests). `f767494` and
  `5fe7c0d`: two fix rounds. `4d8139c`: the CHANGELOG heading takes the
  tag's date. Two-Key PASS at round 3; suite 928.
- SC5.1's receipt is taken: USAGE's `uv` line against the tag, run with
  `python -P`, installs 0.18.0 and reads `specs/feature-document`
  ready-green. Both receipts, before and after the tag, stand untracked
  in `RECEIPT_feature-document-f5_2026-10-01/`.
- The rulings and readings (user, session 72): at the re-intake, ready
  check 3 reads no gap on this feature's own document, which holds no
  Gherkin block; the release sweep fixes wording against the code and
  parks each change of behavior; USAGE says no step writes the Record
  yet; the CHANGELOG heading carries the tag's date.
- Another machine installs `v0.18.0` through the plugin (`/plugin
  marketplace add JJandDjango/sdlc-kit`, `/plugin install
  sdlc@sdlc-kit`). The copy channel carries `skills/sdlc` alone: no
  interview, and intake's ready-check questions point into the
  interview's folder.
- Risk 5 stands: the interview never picks up a document it did not
  start, so G1's solution half is written by hand from the two NOTES
  files.
- Carried: 19 features: 18 with a contract, 17 of them `[done]`;
  `glossary-alias-disjointness` parked by the user, `[to do]`;
  `g1-requirements-spec` before intake, `[doing]`.

## Blockers
- None. Branch `session-72-release` waits for the push, the PR and the
  merge, each on the user's word.

## Next actions
1. G1's solution half, by hand from the two NOTES files (risk 5), to
   ADRs 0033 and 0036; open for it: where the component declaration
   record and the review record live, G1's rules and their codes, the
   venue, and how the 17 features done read G1 inactive once G1 is
   active. Then its intake, through 0.18.0's flow: the document needs
   one scenario per check and every check in one unit, or it parks. The
   pilot's config line, in the engine's session; the engine's install
   ref moves to `v0.18.0` there (pull, not push).
2. Deferred from 0.18.0's sweep (Two-Key's advisories, rounds 1 to 3),
   each a change of behavior or a sentence a test pins word for word.
   A measure comes first: which of them a consumer meets.
   - The interview: E2 gives a free path (`CHANGELOG.md`, `MAP.md`) no
     exemption; S6 never asks which unit is the release unit; P6 writes
     `next: P1` before Q15 proposes a changed check's scenario again;
     E6's path back into a request-half section runs neither Q15 nor P1
     to P5 again; Q14 never asks whether a term amends another; S3 never
     asks for each output kind; the "sections written" count is one a
     seat cannot check; with no engineer seat, S1's Out of scope lines
     land under no text row. O6 writes "(none: intake writes the
     record)" into each document, and no step writes the Record; a test
     pins the string.
   - Intake: I5 still offers `strike` on a feature document; I3's
     "contract already exists, ASK" says nothing for a re-intake;
     `intake.md:23` uses "above" for a table position and for a higher
     revision number; after a ready intake the Appendix's Contract block
     and the status line's `draft` stay as the interview wrote them,
     against ADR 0036.
   - The command: with a repo dictionary that cannot be read, `--draft`
     prints its `CL000` line and still ends `(no dictionary here - door
     at rest)`; it runs no rule of `vocab-check`, while USAGE and the
     contract's SC2.1 say "through the vocabulary check".
   - Pages: `docs/controlled-language.md` never names `CL014` or
     `--draft`; USAGE section 2 never says the interview needs the
     plugin; "each heading followed by its tag", where Traceability and
     the Appendix carry tags on their blocks (a test pins it);
     `skills/sdlc/SKILL.md:91` uses "parked" for a contract held at
     draft and for a parked document; `MAP.md:41` still reads `designed`
     for raw-request intake; the signed document's own line 413 says
     "eighteen sections" after the status line.
3. Prerequisite 7: feature documents for the 15 contracts without one,
   each through its own interview.
4. Small, parked: `test-retirer.js` has its agent wait on the whole
   suite, and the run dies when the agent returns (session 68); hand the
   suite run to the session. Its overlay cannot delete a file, and its
   `tar` step needs `--force-local` under Git Bash (session 69). t4's
   four Two-Key advisories (USAGE's "The `G0` verdict still reads from
   the validator" unqualified; three wrap nits; the ratified Diagnostic
   term, `specs/vocabulary/diagnostic.yaml`, still says "under its
   condition", which only a ratification changes);
   `taskcontract/__main__.py:85`'s `--follow` help still describes the
   0.15.0 pane; Two-Key's wording advisories (CHANGELOG's and ADR 0032's
   "a closed contract reads done whatever its verdicts read" omit the
   later-record limit); two test gaps (no pane test for a `parts:` list
   without `evidence` hiding a seat; `tests/conftest.py`'s row pattern
   splits a plain name at its first ` [`).
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
- A new feature starts as a feature document written through
  `/sdlc:product-specification-interview` (kit 0.18.0), in the format ADR
  0029 ratified and 0033 to 0036 amended, tracked at
  `docs/features/<id>.md`; never a request typed from a sketch. A
  document the interview did not start (G1's) is still written by hand
  from `NOTES_feature-document_2026-09-18.md` and
  `NOTES_feature-document-amendment_2026-09-27.md`. A seat signs its half
  with a row `rN: Signed: request half` or `rN: Signed: solution half`,
  written right after the row it signs (ADR 0034). For a document written
  by hand, the checks before signing run from a scratch script: add the
  document's new terms as drafts to `load_terms`, report CL003 through
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
  `skills/sdlc/init.py` (`KIT_VERSION`), `.github/workflows/sdlc.yml`,
  and every file whose sentences the feature makes false, both skills'
  `SKILL.md` among them (session 72's re-intake). Intake copies the
  document's title line into the contract's `title`, and derives from the
  newest text revision both seats signed, never from a `Signed:` row. A
  unit holds at most three sketches: pair two checks in one sketch ending
  in both ids. Each `done_means` is copied word for word from the
  document's Units table (ADR 0036). For the language door, a scratch
  script builds `lang._Lexicon(load_repo_dictionary, load_terms)`, runs
  `check_contract` on a draft outside `specs/`, and probes words; scaffold
  only after the draft reads zero.
- A re-intake during a build (session 72): the document takes one text
  row (the Scope bullet, the unit's Retirements cell, one decision
  entry) and a `Signed:` row from the seat whose half changed; intake
  reads the document by I2, edits only what the row names in the
  contract, validates, and writes a new `Ready:` row in I7's exact
  shape. One commit, titled `Intake rN:`, with the `Contract:` trailer.
- A plan is plan.md's numbered steps, shown in chat for the user's
  overview. A USAGE refinement never narrows a contract sentence
  silently: flag any narrowing or reading to the user before approval. A
  release rewrite that simplifies a rule gets checked against the code
  first.
- A release sweep reads each changed page end to end against the code,
  besides a `git grep` per stale class: grep finds a sentence by its
  words, and a table row or a general "a verdict" carries none of the
  words a new kind of item brings (session 64 lost three rounds to it).
  Sweep test docstrings and comments too, by count words ("three",
  "none of the"); the grader counts them as shipped. Before a paragraph
  turns green, check that each step it names exists: "until its step
  writes it" was false of the Record. A sentence with "else" or
  "otherwise" is read against every path of the flow (session 72 lost
  two rounds to these).
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
  developer 131K and 62K); session 72's f5: 339K, 357K and 360K (drafter
  133K). A workflow agent's whole-suite run can die when the agent
  returns: run it in the session and classify from its output. For the
  retirer, run the overlaid suite in a scratch worktree first, then name
  the failing tests in `context`, have it run only their module, and say
  any file deletion there. Never run two whole suites at once: the
  session's run was stopped three minutes in while a developer's ran
  (session 69). For a prompt-only unit, the drafter's prototype is a
  scratch copy of the skill folder, not the `taskcontract` package (say
  so in its `notes`).
- A release unit (session 72): the user approves the release text
  first; the drafter then pins that text, its prototype a scratch copy
  of the files the unit changes, run by a launcher that sets the
  prototype as the working directory; the session types the text. A fix
  round that changes a pinned sentence moves the test's copy with it, a
  one-string amendment the session writes and tells the user. Pin the
  version as a floor, never a literal, and leave the install pins to the
  self-pin.
- A check whose receipt needs the tag (SC5.1): before Two-Key, run the
  same install against the unit's commit, `uv run --no-project --with
  "sdlc-taskcontract @ git+file:///E%3A/sdlc_development_kit@<sha>"
  python -P ...` (the drive's colon percent-encoded), and hand its text
  to the grader as a focus pointer; take the real receipt after the tag.
- A CHANGELOG heading carries the tag's date, and a test may pin it:
  when a session crosses midnight before the merge, move both.
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
  subsections free of red marks. After a release USAGE holds the red
  mark in its two legend lines only, and
  `tests/test_feature_document_release.py` pins that count: the next
  feature's pass-zero red text retires or amends that test.
- The whole suite runs 3 to 6 minutes; a local model holding RAM can get
  a background run killed for memory. A PR's CI waits through `gh pr
  checks <n> --watch` in the background; started right after a push it
  can end `no checks reported`, so watch again.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  against the new tag with `python -P`. main's ruleset requires a PR for
  every change.

## Open questions
- This feature's own document holds no Gherkin block and reads "eighteen
  sections" at line 413; the Record waits for a step no release has
  built. Write the 14 scenarios and the count through a text row and
  both signatures, or leave the document as the record of how it was
  written? And which feature carries the Record's step?
- Should USAGE section 2 say the interview, and intake on a feature
  document, need the plugin channel, or should the copy line carry both
  skill folders?
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
  45 to 47, 52 to 54, 61 to 63, 68 to 72). Does the term need a word for
  a delegated approval? Beside it: G0.3's unit confirmation repeated the
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
