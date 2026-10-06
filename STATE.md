# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-10-06 (session 76 close: document-split's ADR and terms
> stand on main; the language rewrite and intake open the next session)._

## Now
- **Session 76 (2026-10-06): `document-split`'s two prerequisites are
  met, and its contract is not yet written.** PR #88 merged at
  `1b4173b`. It holds ADR 0037 (`bd38eb6`), which amends ADR 0029 and
  ADRs 0033 to 0036 for the pair, and the term commit (`62cbe4a`): nine
  new terms, seven amended, the dictionary without `pair`. The glossary
  holds 75 terms. The session's deliverable was the contract at ready;
  the session ended at the plan's boundary, after step 4, on the user's
  word, so the language rewrite and intake have not run.
- The document stands as session 75 left it: both halves signed at r7
  in `docs/features/document-split.md` (`Signed: solution half. The
  engineer seat signs r6`), the state file at `phase: output`, `next:
  W1`. Five criteria, 13 checks, 13 scenarios, six units and no OPEN.
  The tree shows it `[doing] no contract: document r6`, both halves
  `[done]`.
- Two of the seven amendments rest on ADR 0037 and not on the document.
  The neighbor read found `ready-check` ("14 questions") and
  `drift-mark` ("the one mark") false under the ADR; the user ratified
  both. The document's Terms block still says five, and the term
  commit's message says why. `open-mark`'s "above the seat boundary"
  fits a combined document only and was left as it is.
- Plan step 5 is done: the document's Scope covers the release unit.
  Each file 0.18.0's release unit touched, the four that name the
  version (`pyproject.toml`, `skills/sdlc/init.py`, `sdlc.yml`,
  `USAGE.md`) and the four outside the interview's folder that speak of
  the feature document (`skills/sdlc/SKILL.md`, `intake.md`, `tree.py`,
  `tree_view.py`) are in Scope or on a free path. No text row is needed
  before intake.
- The design, as signed: the requirements document keeps
  `docs/features/<id>.md`, and the design document is
  `docs/features/<id>.design.md`, each with its own state file. A
  design run is the same skill with a second argument, `design`. Intake
  takes the requirements path and writes its row in both tables. Six
  units, `d1-requirements` to `d6-release`, ship as kit 0.19.0, one at a
  time; `d6` takes SC4.3 and opens G1's design document.
- **The user wants this feature on the second machine as soon as
  possible** (2026-10-06). Nothing session 76 merged is installable
  there: the ADR and the terms change the record, not the skills. What
  stands between today and that install: the language rewrite, intake,
  the six units and the tag. What an install takes, read from the files
  in session 73: the plugin (`/plugin marketplace add
  JJandDjango/sdlc-kit`, `/plugin install sdlc@sdlc-kit`) and `pip
  install git+https://github.com/JJandDjango/sdlc-kit.git@v<tag>`, since
  the interview's P1 and E1 run `python -m taskcontract lang-check
  --draft`. The interview needs no `/sdlc` setup in the repo; intake
  does. This repo holds no receipt of the install there.
- Kit 0.18.0 stands released: PR #84 merged at `771176e`, tagged
  `v0.18.0` there. The installed `sdlc` plugin sits at `40eb767`, and
  `git diff --stat v0.18.0 main -- skills/` prints nothing, so its flows
  are 0.18.0's. Session 75's Now is at `686df2e:STATE.md`.
- This machine: no Python here holds `rich` (3.14, 3.13 and 3.10), so
  the 77 tests that import the pane fail under each, and `uv` is not
  installed. The whole suite read green, 928 passed, in a scratch venv
  that holds the test extra. `py -m pip install "textual>=8.2,<9"` into
  3.14 would end that step; the user has not said.
- G1's design is written through the interview once 0.19.0 ships, not
  by hand from the two NOTES files. It waits behind `document-split`'s
  build.
- Carried: 20 features: 18 with a contract, 17 of them `[done]`;
  `glossary-alias-disjointness` parked by the user, `[to do]`;
  `g1-requirements-spec` and `document-split` before intake, `[doing]`.

## Blockers
- None. This wrap reaches `main` through a PR from branch
  `session-76-wrap`; the push, the PR and the merge are each on the
  user's word.

## Next actions
Opener: `document-split` goes to intake, under kit 0.18.0. The ADR and
the terms stand on main, and the Scope check is done. First the language
door on a draft (plan step 6): a scratch script builds the lexicon with
the ratified terms and runs `check_contract` on a draft contract outside
`specs/`; the draft check's 179 findings are rewritten in the contract's
wording until it reads zero, and each `done_means` is copied as it
stands. `case` alone is an unknown word, and the checks say "the four
cases". Then `/sdlc:sdlc intake docs/features/document-split.md` through
the installed plugin, the seats' confirmations in one batch, and its own
commit with the `Contract:` trailer. Then the receipts: `validate
--profile ready`, the tree, the whole suite. Then the build, `d1` to
`d6`, as kit 0.19.0; a re-intake during it runs through that plugin too,
since after `d5` the repo's own intake reads a pair. The interview
itself resumes at W1, the Google Docs form, when one is wanted. Still
unanswered: whether combined documents are in flight on the second
machine (asked twice on 2026-10-06; the document records it as not
known, and the design holds either way).

1. Behind `document-split`: G1's design document, through a design run
   once 0.19.0 ships (`d6` opens it at r1), to ADRs 0033, 0036 and
   0037; open for it: where the component declaration
   record and the review record live, G1's rules and their codes, the
   venue, and how the 17 features done read G1 inactive once G1 is
   active. Then its intake, through 0.18.0's flow: the document needs
   one scenario per check and every check in one unit, or it parks. The
   pilot's config line, in the engine's session; the engine's install
   ref moves to `v0.18.0` there (pull, not push).
2. Deferred from 0.18.0's sweep (Two-Key's advisories, rounds 1 to 3),
   each a change of behavior or a sentence a test pins word for word.
   A measure comes first: which of them a consumer meets. The
   2026-10-05 feedback named none.
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
   (`styled-rendering`); honest and dishonest functions, conditions on
   checking and generating tests
   (`NOTES_honest-functions_2026-10-04.md`, a feature document once it
   becomes work); `document-split`'s three later features (the fourth
   case computed from a list of public contract paths, Claude's review
   of a design in a fresh context, a PR brief for the final reviewer).

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
- An idea that is not yet a feature goes into a `NOTES_*.md` file (a
  free path, `.sdlc/config.yaml:10`) with one line under Next actions 5;
  the interview's materials step reads the file when the idea becomes a
  feature. Before filing it, grep `docs/gates.md` and the gate pages for
  what the kit already holds (session 73).
- A wrap written before its own PR merges words its Blockers line so it
  stays true after the merge: sessions 71 and 72 each left a line the
  next resume had to correct.
- Intake from a feature document: ratify its new terms first, in their
  own commit, with any ADR the document's prerequisites name. A term
  whose single-word name or slug equals a dictionary word trips CL003;
  the dictionary cedes the word in the same commit. Check each amended
  term's neighbors for a definition the change contradicts, and read
  the glossary against the feature's ADR too: the Terms block is decided
  before the design, and session 76 found `ready-check` and `drift-mark`
  false under ADR 0037 (each amended in the term commit on the ADR's
  authority, on the user's word). Check the
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
- The suite on this machine (session 76): no Python holds the `pane`
  extra, so run it from a scratch venv: `py -3.14 -m venv
  <scratch>/venv`, then that venv's `python -m pip install
  "textual>=8.2,<9" "pytest>=8" "jsonschema>=4.18" "PyYAML>=6"`, then
  its `python -P -m pytest tests -q` in the background. `lang-check`
  prints about 130 exempt lines before its last one: run it in the
  background and grep the output for `lang-green`.
- A session that ends at the plan's boundary (session 76): its commits
  land through the session's PR, and the wrap rides its own PR from a
  new branch off main.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  against the new tag with `python -P`. main's ruleset requires a PR for
  every change.
- The interview in this repo (session 74): before `/sdlc:`, list
  `C:/Users/hyden/.claude/plugins/cache/sdlc-kit/sdlc` and check it
  holds main's tip; else run the flows from `skills/` here, which equal
  the tag when `git diff --stat v<tag> HEAD -- skills/` prints nothing.
  The user answers in batches: propose each section's text, say the
  count first, and one reply covers it (the request half took nine
  replies). `lang-check --draft` reads the state file alone, so
  `answers.statement`, `answers.non_goals`, `answers.checks[].text` and
  `answers.terms[]` hold the full text, and a YAML list item that opens
  on a quoted word is quoted whole. A gap the seat's answer closes
  before the `Measured:` row is never marked.
- A solution half (session 75): read the materials first, one narrow
  read-only explorer per slice (the interview skill, intake, the
  `taskcontract` code, the release unit and pages), each returning
  change sites, pinning tests and design questions with `file:line`;
  split the result into one file per slice with a scratch script. Lead
  the first batch with the shape calls Scope depends on. Before the
  `Measured:` row, probe each `done_means` through `lang-check --draft`
  on a scratch state file that holds the real terms, and reword to
  zero: intake copies them word for word, the cap is 20 words, a term
  of several words counts as one, and `document`, `engineer` and `case`
  alone are unknown words. A Decisions line never says "an OPEN" in
  prose: intake parks on an OPEN mark there. Five batches and the
  signature took eight replies.
- This repo is public. A document's Background words a consumer's
  feedback plainly, without quoting it, and a NOTES file leaves out a
  remark the user made in confidence.

## Open questions
- The second machine and the build (2026-10-06, the user wants the
  feature there as soon as possible): the interview's two runs and their
  signing exist after `d3`. Can that machine take the plugin from the
  build's branch then, before `d6` tags 0.19.0? Not checked: how the
  plugin channel pins a ref, and whether that machine runs intake.
- The interview's flows ask one question at a time, and session 74's
  seat answered in batches of proposed text. Does the flow gain a batch
  path, or does the rule stay and the session keep its own practice?
- This feature's own document holds no Gherkin block and reads "eighteen
  sections" at line 413; the Record waits for a step no release has
  built. Write the 14 scenarios and the count through a text row and
  both signatures, or leave the document as the record of how it was
  written? And which feature carries the Record's step?
- Should USAGE section 2 say the interview, and intake on a feature
  document, need the plugin channel, or should the copy line carry both
  skill folders? On the copy channel, intake's ready-check questions
  point into the interview's folder. Beside it (session 73): section 2's
  `pip` line carries no tag and does not say the interview's draft
  checks need the package.
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
