# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-10-07 (session 83, first wrap: document-split's
> d6-release is built, Two-Key PASS round 1; the release follows its
> merge)._

## Now
- **Session 83 (2026-10-07): `d6-release` is built, Two-Key PASS round
  1 at `2c66f4b`.** The unit stands as two commits on branch
  `session-83-document-split-d6`. `e4ac931`: intake reads at I2, before
  its four parts, whether the file is a combined document (one that
  holds a `## Proposed solution` heading), and stops with one of two
  messages and nothing written (SC4.3); USAGE reads green under 0.19.0
  banners, with the red mark in its two legend lines alone;
  `CHANGELOG.md` holds the 0.19.0 entry; `MAP.md`'s three rows and the
  G0 page's title row name the pair; `KIT_VERSION` and `pyproject.toml`
  read 0.19.0. `2c66f4b`: G1 stands as a pair, its design document at
  r1 against requirements r3, written by a live design run from
  `e4ac931` on the user's two answers (engineer seat `user`, no
  material); G1's requirements document keeps every byte. The receipts,
  at the clean commit: SC4.3 green at 10 tests, the unit's 28 tests,
  the whole suite at 1062 passed in a scratch venv, `prompt_lang` on
  both skill folders, `ready-green` on this contract and on the three
  combined documents' contracts, `scope-green` against `204b671`, and
  `lang-green`. The unit is closed in the progress record.
- **Not yet done: the release.** The tag `v0.19.0` does not exist until
  the user's word. After the merge come the annotated tag at the merge
  commit, manual receipt two (USAGE's `uv` line against the tag with
  `python -P` reads 0.19.0, and the plugin at the tag holds the new
  flows), and the self-pin through its own PR: `USAGE.md:706` and
  `.github/workflows/sdlc.yml:20` move from `v0.18.0`. The same install
  against `2c66f4b` already reads 0.19.0, in
  `RECEIPT_document-split-d6_2026-10-07/RECEIPT.md`. The contract is
  not closed in the progress record: `progress done document-split`
  follows the tag.
- The release text: the user approved it as twelve deltas, saved whole
  in `RECEIPT_document-split-d6_2026-10-07/release-text.md`. Beyond the
  six wording advisories, the end-to-end read found three green USAGE
  sentences the pair made inexact, and each is reworded: a design
  document is the one file under `docs/features/` that is no feature
  before intake; intake adds its `Ready:` row to each document's table;
  intake writes a `Parked:` row in each table when it parks a pair.
  `MAP.md`'s raw-request intake row reads `implemented (v1)`. Two
  parts of delta 12 were dropped on signed sources, each told to the
  user: the stale message keeps its letters `r{n}` and `r{m}`, since
  the feature document lists it verbatim, and I8 keeps "a parked
  document", a ratified term.
- Sizes, as the suites count them: `intake.md` 11,504 of 12,000
  characters, `signing.md` 11,830, `opening.md` 9,275, the interview's
  `SKILL.md` 11,152.
- What `d6` leaves standing. Two-Key's advisories, all wording: USAGE's
  "Intake copies it from the feature document's title line"
  (`USAGE.md:1324`) beside the G0 page's new words; "Drift from the
  feature document" carries no pointer to "A pair of documents" for the
  design's mark (`USAGE.md:1341`, `1368`); I2 says "in four parts" and
  then "First, before the four parts". Three pins the next work moves:
  `tests/test_document_split_g1_pair.py` and USAGE's drawing of G1 pin
  `design r1` and `[to do]`, so G1's next design row moves both;
  `tests/test_document_split_release.py` pins every line of `tree.py`
  below its docstring by a sha256, so the next unit that changes
  `tree.py` retires that assertion; the same file pins the red mark to
  USAGE's two legend lines, so the next feature's pass zero retires
  that test.
- G1: `docs/features/g1-requirements-spec.design.md` stands at r1, and
  its state file reads `next: S1`. The design run resumes there with
  `/sdlc:product-specification-interview g1-requirements-spec design`,
  once this machine's plugin holds 0.19.0's flows. Its copied term
  "Ready check" says 14 questions where ADR 0037 gives 15: G1's PO seat
  amends the requirements document before G1's intake. That document
  was written by hand and has no state file, so how a requirements run
  takes it is open.
- `d1-requirements` stands at `6602242`, `d2-design` at `bfd4058`,
  `d3-signing` at `13901c3`, `d4-tree` at `1df7068` and `d5-intake` at
  `4681b42`, all on main (PRs #91 to #94, #96). The document's text is
  unchanged since intake: both halves signed at r7, the `Ready:` row at
  r8, the contract at `6ef6366`. Session 82's Now is at
  `204b671:STATE.md`.
- **The second machine** (the user wants this feature there as soon as
  possible, 2026-10-06). The plugin follows main:
  `.claude-plugin/marketplace.json` sets `source: "./"` with no ref, so
  after `d6`'s merge a `/plugin marketplace update sdlc-kit` there
  delivers 0.19.0's flows. A combined document with no `Ready:` row
  then meets its own message and is split by hand. The `pip` half
  takes a commit sha of main until the tag, then `@v0.19.0`. This repo
  holds no receipt of the install there, and the update there is not
  tested.
- Kit 0.18.0 stands released at `771176e`. This machine's installed
  `sdlc` plugin sits at `40eb767`, whose `skills/` equal that tag's, so
  `/sdlc:` here still runs 0.18.0's flows until the plugin is updated.
- This machine: the system Python (3.14.2) holds `textual` 8.2.8,
  `rich` and `pytest`; the whole suite is still run in a scratch venv,
  1062 passed. No Python here holds `prompt_lang`. `uv` 0.12.23 is
  installed through winget but is not on a session's PATH: it runs by
  its full path,
  `C:/Users/hyden/AppData/Local/Microsoft/WinGet/Packages/astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe/uv.exe`.
  The `google_workspace` server failed to connect again in session 83
  (`Connection closed`); the cause is not looked into.
- Carried: 20 features: 19 with a contract, 17 of them `[done]`;
  `document-split` `[doing]`, six units of six done, open until the
  tag; `glossary-alias-disjointness` parked by the user, `[to do]`;
  `g1-requirements-spec` before intake, `[doing]`, now a pair.

## Blockers
- None. `d6-release` is built, Two-Key PASS round 1 at `2c66f4b`. This
  file's commit rides the unit's PR. The push, the PR, the merge, the
  tag and the self-pin's merge are each on the user's word, and a later
  wrap records each as it lands.

## Next actions
Opener: the release of kit 0.19.0, wherever session 83 left it. In
order: the unit's PR merged on the user's word, after both CI checks
read green; the annotated tag `v0.19.0` at the merge commit; manual
receipt two (`uv run --no-project --with "sdlc-taskcontract @
git+https://github.com/JJandDjango/sdlc-kit.git@v0.19.0" python -P`,
then the version and a `validate`, and the plugin's `skills/` at the
tag against the unit's); `progress done document-split`; the self-pin
(`USAGE.md:706` and `.github/workflows/sdlc.yml:20` to `v0.19.0`)
through its own PR, which the wrap rides; this machine's plugin
updated to the tag. A `CHANGELOG.md` heading carries the tag's date:
it reads 2026-10-07, and a tag on a later day moves the heading and
`RELEASE_HEADING` in `tests/test_document_split_release.py` together.
The interview itself resumes at W1, the Google Docs form, when one is
wanted.

1. Behind the release: G1's design document, from S1 on, through a
   design run on 0.19.0's flows (`d6` opened it at r1), to ADRs 0033,
   0036 and 0037; open for it: where the component declaration
   record and the review record live, G1's rules and their codes, the
   venue, and how the 17 features done read G1 inactive once G1 is
   active. Then its intake, through 0.19.0's flow: the pair needs
   one scenario per check and every check in one unit, or it parks. The
   pilot's config line, in the engine's session; the engine's install
   ref moves to `v0.19.0` there (pull, not push).
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
   - Seen in `d3`'s live run, listed in the receipt folder's
     `RECEIPT.md`: Q15 withheld the scenario for a check Q11 had
     accepted, as thin; the requirements run wrote two state-file lines
     with an unquoted colon, so the draft check's first run could not
     read the file; S2 calls the engineer seat's own out-of-scope places
     refusals; E1 to E5 ran in the same turn as the Notes confirmation.
   - Seen in `d5`'s live runs: a design run lets a unit hold more than
     three checks with no `+` in its Checks cell (`hello-name`'s
     `u1-greeting` holds six), and I4 allows a unit three sketch
     entries, so intake could not place them.
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
  only after the draft reads zero. A baseline mode that builds the draft
  from the state file's `answers` lists the unknown words in one run
  (session 77: 177 findings to 0 in one rewrite). Read the whole
  document before the readback, not the state file alone: Interfaces and
  Sources settle a check's loose clause, as with SC4.1's "word for
  word". The standing line, `No new authorizations are added`, stays in
  the document only: the dictionary cannot say it, and `approval` is a
  term with another meaning (feature-document's r11, tree-first-level,
  document-split). The `Ready:` row keeps I7's exact shape; any other
  fact of the intake goes into its commit message.
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
  mark in its two legend lines only, and the release unit's suite pins
  that count: the next feature's pass zero retires that test, as
  session 78 did for 0.18.0's.
- Pass zero for a section a release already shipped (session 78): the
  whole section is rewritten red, with a callout that points to the last
  tag for the shipped guide, and the release suite's tests on that
  section retire in the same commit, each told to the user. Run the
  suite on the new text before the approval message: it names the
  tests, so the text, the readings and the retirements go to the user
  as one decision.
- A prompt unit's build (session 78, `d1`): the drafter's test finds
  the skill by the release suite's ROOT idiom, its red run starts in
  the repo root, and its prototype is `<scratch>/proto/skills/...` with
  a copy of the test at `proto/tests/`. The session overlays the
  prototype on a scratch worktree with a script that mirrors the skill
  folder, runs the whole suite there, and names the failing tests and
  their modules to the retirer, which runs only those modules. The
  developer gets the interface note as a file outside the drafter's
  folder, and `scratchRoot` names the folders it may not read. Run a
  `progress run` command alone first: its inner `python` is the system
  one, and a missing module would read as a red. Session 78's `d1`:
  drafter 198K, retirer 159K, developer 95K, Two-Key 215K, PASS round 1.
  Session 79's `d2`: drafter 207K, retirer 109K, developers 114K and
  58K, Two-Key 202K, PASS round 1. Session 80's `d3`: drafter 179K,
  retirer 91K, developers 107K and 60K, Two-Key 192K, PASS round 1. Three scratch scripts carry the
  hand-overs: one splits the drafter's journal into the interface note
  file and a printed list, one mirrors the prototype onto the worktree,
  and one starts a command in another working directory, which the
  retirer uses to run only the failing modules. After the developer
  returns, read its free wording against each step it touches: `d2`'s
  second round fixed three sentences no test pinned. The Bash hook reads
  a bare word after a flag as a file path, so `python -X utf8` is
  refused: set the encoding inside the script.
- A code unit's build (session 81, `d4`): the drafter's prototype is a
  scratch copy of the `taskcontract` package, and
  `.claude/workflows/tools/overlay_pkg.py` copies its changed files and
  the drafted test onto the scratch worktree. With a Retirements cell
  of "none", the retirer runs only if an older test fails there. Before
  approving the list, read each fixed detail against the ratified terms
  under `specs/vocabulary/` too: the drafter does not read them, and
  `d4`'s draft pinned a drift mark the `drift-mark` term does not list,
  on a suggestion in the session's own brief. A small amendment on
  review is the session's: change the test, the prototype and the
  interface note, prove red and green again, and tell the user. Remove
  the scratch worktree before the developer starts, since it holds the
  prototype. `tree_receipt.py` there takes a tree print as a receipt.
  Give Two-Key a focus pointer that says the grader reads and the
  receipts key runs: `d4`'s grader ran a second suite under the system
  Python at the same time. A workflow agent can see the user's last
  chat message: `d4`'s drafter read "skip this part" there and asked
  which part, so say in the brief when such a message is not for it.
  Session 81's `d4`: drafter 213K, developers 94K and 75K, Two-Key
  179K, PASS round 1.
- A prompt unit in two skill folders (session 82, `d5`): one drafter,
  its prototype a scratch copy of both folders under
  `<scratch>/proto/skills/`. `tools/overlay_files.py` copies named
  files onto the scratch worktree. Give the sizes as Python's
  `read_text` counts them: `wc -m` counts the CRLF bytes too and read
  `signing.md` 97 high. A new sentence set before a pinned sentence can
  break that sentence's opening words: `d5`'s draft broke
  `tests/test_tree_titles.py`, which the unit does not retire, and the
  session amended the draft, the prototype and the note. Tell the
  retirer which modules fail and have it run those alone; sweep the
  docstring of a module it thins. Tell the developer to run the named
  modules and leave the whole suite to the session. Session 82's `d5`:
  drafter 159K, retirer 117K, developer 78K, Two-Key 201K, PASS round
  1.
- A release unit with a prompt half, and a receipt that writes a
  tracked file (session 83, `d6`). The release text goes to the user as
  numbered deltas, and the approved text is saved whole, each delta's
  words after the change, in the receipt folder: the drafter pins from
  that file. Before a sweep rewording is proposed, read the feature
  document's "Error messages, verbatim" and the ratified terms under
  `specs/vocabulary/`: two parts of a delta the user had approved
  contradicted them and were dropped. The unit lands as two commits
  when a manual receipt runs "from the unit's commit" and writes a file
  the repo then holds: the tests that read that file are drafted with
  the rest, against a stand-in in the prototype, held out of the first
  commit and placed with the real file in the second. The prototype is
  a scratch copy of the repo's working files; `tools/changed.py` lists
  what it changed, and `tools/green_marks.py` turns a page's red marks
  green but for its legend lines. The session types its part first and
  amends the older tests its text moves, so only the developer's tests
  stay red; then the developer writes its part. The whole suite on the
  overlaid worktree, once per commit's state, names every older test
  that fails: when each is a replacement or a one-line change,
  `test-retirer.js` does not run. A design run through its opening is
  three turns, driven by the session with no seat agent: the first
  message from PowerShell, then `say` from Bash. A PowerShell call
  takes no pipe either. Session 83's `d6`: drafter 199K, developer 66K,
  Two-Key 281K with the sweep, PASS round 1.
- A live intake run on `d3`'s saved pair (session 82):
  `tools/intake_fixture.py` builds the pair by hand edit and checks
  what the run changed. The saved pair carries three OPEN marks, so a
  receipt of a stop needs them closed first. One plugin worktree and
  one consumer worktree a run, under `E:/`; `tools/make_driver.py`
  binds a driver to each; the first message goes from PowerShell. Two
  runs side by side each ended in one turn, in under two minutes.
- A live run of both runs (session 80, `d3`): two worktrees at the unit
  commit, and one driver folder a run, made by a script that copies
  `live-run-driver.py` with its `PLUGIN` and `WORKTREE` lines set and
  puts the settings file beside it as `live-settings.json`. The session
  sends each run's first message itself, from PowerShell: Git Bash
  rewrites a message that opens with a slash as a path. It then hands
  the first reply to `live-run-seats.js` as `opening`, with `cast`,
  `stop` and `label` naming the run. One seat a run: ann's script holds
  the request half's facts, raj's the design's, with one consult case a
  yes. Between the runs a script copies the requirements document and
  its state file; after the design run it compares both byte for byte,
  reads both tables and saves the pair. Session 80: 41 and 36 turns,
  about ten minutes a run, 66K and 63K tokens. The session's scratch
  scripts (overlay, run-in, journal split, splice, driver copy,
  receipt) are kept in untracked `.claude/workflows/tools/`.
- The form validator on this machine (session 78): put one line,
  `E:/foundations`, in a `foundations.pth` under the scratch venv's
  `Lib/site-packages`, and `pip install tiktoken` there. `python -m
  prompt_lang` takes one path, and a folder works.
- The whole suite runs 3 to 6 minutes; a local model holding RAM can get
  a background run killed for memory. A PR's CI waits through `gh pr
  checks <n> --watch` in the background; started right after a push it
  can end `no checks reported`, so watch again.
- The suite on this machine: since session 81 the system Python 3.14
  holds `textual`, so `python -P -m pytest tests -q` may run under it;
  that run is not yet seen green. Until it is, the scratch venv stands
  (session 76): `py -3.14 -m venv <scratch>/venv`, then that venv's
  `python -m pip install "textual>=8.2,<9" "pytest>=8"
  "jsonschema>=4.18" "PyYAML>=6"`, then its `python -P -m pytest tests
  -q` in the background. `lang-check` prints about 130 exempt lines
  before its last one: run it in the background and grep the output for
  `lang-green`.
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
- The second machine after `d6`'s merge: its plugin update is not
  tested, and whether that machine holds a combined document with no
  `Ready:` row is not known. Such a document now meets its own message
  there and is split by hand.
- G1's requirements document was written by hand and has no state
  file, and its copied term "Ready check" says 14 questions. Does a
  requirements run take a document it did not start, or does the PO
  seat amend G1's by hand before its intake?
- A pair through intake whose design table holds no `Ready:` row prints
  no mark for the design: the `drift-mark` term and USAGE name one
  drift mark for a design, the stale one. Add `design: no "Ready:" row`
  through a term amendment and a USAGE sentence, or leave it?
- The `google_workspace` server still fails to connect after a restart
  with `uv` installed (`Connection closed`, session 82). What stops its
  start, and does its Google token still hold?
- The way back from a finished state can ask a seat to sign twice: once
  at the section's write, under `SKILL.md`'s constraint on a write
  after a signature, and once at P7 or E7 after the checks run again.
  The requirements run reads so since `d1`, the design run since `d3`.
  The feature document's edge says "the checks run again, and the PO
  seat signs again". One signature, at the signature step, or both?
- A design run paused between O1 and O6 holds a state file and no
  design document, so DESIGN CONFIRM has no table to read and no
  document to take a row. The sources decide nothing here. Skip the
  step until r1 stands, or leave it?
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
