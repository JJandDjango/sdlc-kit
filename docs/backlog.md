# Backlog - sdlc_development_kit

Next actions and open questions, carried from the retired `STATE.md` at the
Cairn 2.0 migration (2026-10-16). Session history stays in git:
`git show 5350d64:STATE.md`. With `git config cairn.plan docs/backlog.md`,
`/cairn status` reads its Next line from the first unfinished step below.

## Next

1. [x] Build session 90's first ruling: one G1.1 record a call that holds a
   run for each `g1.schemas` entry, with the fix of G1.1's escaped defect
   (a contract whose scope cannot be read reads `to do` and `lint` refuses
   it). Built in sessions 101 and 102 on the branch
   `session-101-g1-1-record`, Two-Key PASS in round 1; the PR waits for
   the user's review.
2. [x] Build `s6-release`, the sixth G1 unit and kit 0.20.0. Built in sessions
   103 and 104 on the branch `session-103-g1-s6-release`, Two-Key PASS in
   round 2; merged as PR #124 at `fb411c9`, and the user tagged `v0.20.0` there.
3. [x] After the user merges and tags `v0.20.0`: run USAGE's `uv` line against the
   tag with `python -P`, and open the self-pin PR (`.github/workflows/sdlc.yml:20`
   and `USAGE.md:1011` to `v0.20.0`); the wrap rides that PR. Session 104: the
   install from the tag read 0.20.0 and `ready-green`; the self-pin PR waits for
   the user's review.
4. Build `prove.py` and `receipts.py`, scripts that run tests and print only the
   minimum an agent needs (a standing practice, the user, session 103).
   `prove.py` is the drafter's copy, red, green and mutation loop; `receipts.py`
   is Two-Key's receipts, run by the session with no agent. In their own short
   session, `prove.py` first.

## Next actions

Opener: Next 4, `prove.py`. The readings of PRs #116 and #119 that
cost something (Open questions, G1) still wait for a design text row.
The Haiku receipts agent is the user's to rule on again (Open
questions); its receipts matched the session's own in both
`s6-release` rounds. Not folded in `s4-tree`: `g1.py`'s `Ready:` row
reader and `tree.drift`'s; `progress._target` has one caller left.

1. The pilot's config line, in the engine's session; the engine's
   install ref moves to the release that carries G1 (pull, not push).
   Its feature document needs a new intake before its G1.3 can pass:
   its `Ready:` rows read `signed r3` (reading 3, kept in session 93).

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
   of a design in a fresh context, a PR brief for the final reviewer);
   the tree names no feature in flight (the user, 2026-10-07); a design
   run's opening fixes no shape for its copy of the terms
   (`opening.md`); the interview's `SKILL.md` reads `$1` as the second
   word under this harness; `STATE.md` runs past 800 lines against its
   one-page contract, most of them Standing practice (session 89, the
   audit's `BUDGET-STATE`); the document theory
   (`NOTES_document-theory_2026-10-10.md`, session 91): the feature and
   design formats in the shapes agreed there, a feature of its own
   through the interview, with its open points (an area level in the
   tree, how the test is sat); that file's example, the tree opening on
   unfinished work, is the 2026-10-07 idea above, with a question on a
   test labelled SC2.3; a lean Claude Code launch profile, the user's to
   handle and no kit feature (`NOTES_lean-system-prompt_2026-10-11.md`,
   session 94): a replacement system prompt and a trimmed tool set,
   about 17K fixed tokens against 44K, nothing installed; the process's
   cost, what session 96 left parked
   (`NOTES_process-cost_2026-10-12.md`): a custom agent type with a
   smaller start than the 50K each agent pays before it reads a file,
   and Gemma for a narrow check with no tools, called from a script.
6. Deferred from `s6-release`'s sweep (Two-Key's advisories, session 104):
   `docs/gates.md`'s registry count lines (near line 98) say nothing of
   G1's three conditions, now `enforced` here; `README.md`'s "What ships
   today" omits the G1 venue and the `progress` refusal (it omits the tree
   and the vocabulary layer too, so it predates the unit); `USAGE.md:1275`
   ("An active gate the kit cannot compute yet reads `to do`") is vacuous
   now that both active gates compute; `docs/operators.md`'s deferred
   trigger says "a person signs each" beside venue rows that name
   `sdlc-spec` as the author (the release text's delta 14, pinned by a
   test).

## Open questions

- How does the user's subscription weigh a cached read against a fresh
  token (session 96)? The shares of the process's cost rest on the
  API's weights. The `/usage` readings of `s5-start`'s two sessions are
  the first measure (`USAGE-readings.md` in the s5 receipt folder).
- Keep Haiku 5.5 as the receipts agent (session 98)? It ran under the
  name `claude-haiku-5-5` at about a tenth of Opus's API weight, and in
  two rounds it once started a second whole suite and once returned
  with two commands still running, so its round was taken again on
  Opus. The default stays Haiku until the user rules.
- G1, two readings of PR #119 that cost something, for the design's
  next text row: in the tree's second build an exempt feature is
  refused, where ADR 0038 and the design say an exempt feature is never
  refused; and I9 reads the config as a person would, so where the
  config cannot be trusted the report can end as today while `progress`
  refuses every task.
- A hand-written file that stops the print or a command (sessions 94
  and 95; the two handoff files name each with its receipt). On main
  G1's three readers hold their known causes, the tree holds whatever a
  reader ends on, `tree.build` holds whatever G1's part of a build ends
  on, and the print writes a character its output cannot hold as its
  escape. Still open, each older than `s4-tree`: with G0 active a
  contract that is not UTF-8, or one whose scope holds a number past
  4300 digits, stops the whole print in the validator's path;
  `tree._load` and `scope_check.contract_scope` let a plain ValueError
  from the YAML loader through (an unquoted date no calendar holds;
  since session 102 `g1-record lint` catches it and refuses the
  contract, with no test that feeds it one);
  `g1._seat` does too, for the seat term's file; `g1-check` calls its
  three readers bare; and `g1-check` and the other commands write
  through `print`, so a text outside the code page stops them through a
  pipe on Windows. Left from round 4, both advisory: `build`'s
  docstring says each G1 condition reads `to do` with no diagnostic in
  the second build, and the repository's G1 line still lists the
  features that hold it; and an error of another cause that passes
  before the second build prints under G1's name for that one print. A
  `g1.exempt` entry that is no text prints whole in its problem line,
  however long. The open edge of G1.1 widens by a case: a schema
  pattern the system refuses matches no file, so G1.1 can read `done`
  with nothing linted.
- G1.3 (session 92; PR #112's body names each). The user kept all 12
  readings at the review (session 93), so a feature with no feature
  document cannot pass G1. For the design's next text row: the six
  cases it never named, and a seventh from the review, what a person
  answers for an item that does not apply to the feature (an answer is
  checked or unchecked alone today, so such an item is answered
  checked). Three edges left as they are: a shortened flag (`--check`)
  is taken; a name or a section may hold a terminal escape; on Windows
  an id in capitals reaches the same contract. A path
  `docs/features/<id>.design.md` that is a folder counts as no design
  document.
- Session 89's delegation stands in this file, in memory and in the
  user's global `CLAUDE.md`, in no ADR and not in `CONVENTIONS.md`.
  Record it in either, or wait for the metrics review? Beside it: the
  delegation rests on Two-Key as the independent check, and its scripts
  stand untracked on this machine (the `.claude/workflows/` question
  below).
- G1.2, for the engineer seat (session 90; PR #109's body names each).
  - A record binds two files of a model, the model's and its
    configuration's, as the design draws the entry. A file the model
    extends or includes is not bound, and a P project's sources never
    are, so G1.2 can read `done` for text no checker ran on. Hash the
    model's folder, or a declared list of files? Either changes the
    record's entry, which is signed design text.
  - P has had no live run. Its two calls, its configuration as a text
    file of `p check`'s arguments, and its exit codes (0, 1 and 2, from
    `ExitCode.cs` at `260da92`) are read, not run. What `p check`
    returns with several test cases and none named is not measured: if
    it is 0, a configuration with no `-tc` records a pass with nothing
    checked. P writes inside the project's folder.
  - Five refusal lines of `g1-record model` carry words no source
    gives, beside G1.1's six.
  - Three paths end either writer on a traceback with exit 1, each
    writing nothing: a record file that cannot be written, a NUL in a
    declared path or in a P configuration, and a damaged schema file in
    the install. `contract_scope` does not catch a contract that is no
    UTF-8.
  - On Windows the system finds a tool in the repository's root before
    PATH by default, so a `tlc.cmd` committed at the root is the one
    started, and a linter's too. Refuse it, or leave it?
  - Two components with one `id`, and a `model` path that leaves the
    repository, are each taken as declared.
  - Overlap's tail, under USAGE's stated limit: a second name for one
    folder (a link, an absolute path with no drive, two Unicode forms
    of a name, a Windows short name) is not seen.
- G1.1, four edges for the engineer seat (session 88; Two-Key's
  advisories on `79b4a5b`). Session 102 closed two others: a feature
  whose schemas stand under two `g1.schemas` entries now gets one record
  that holds a run for each, and a contract whose scope cannot be read
  reads G1.1 `to do`, which `lint` refuses.
  - With the `g1.schemas` key absent, `lint` prints `G1.1: no boundary
    schema in scope` and exits 0, by the design's letter, while
    `g1-check` reads G1.1 `to do`. Refuse the call (exit 2), as an
    unreadable declaration is refused, or leave it?
  - A pattern such as `./api/*.yaml`, one whose folder differs from
    the disk in case alone, or one that is absolute or holds `..`
    matches nothing, so its schema leaves the scope in silence and
    G1.1 reads `done`. The design's guard is review item 10. Strip a
    leading `./` and refuse the rest, or leave it?
  - Five refusal lines carry words no source gives and no test pins,
    each on stderr with exit 2: `{id}: G1 is not active` on
    `g1-record`; `{id}: no contract at specs/{id}/contract.yaml`;
    `{id}: g1.schemas names a linter the kit does not know: {value}`;
    `taskcontract g1-record: unreadable record: {path} ({reason})`;
    `{id}: g1.schemas cannot be read: {reason}`. None stands in USAGE's or the design's exit-2 list.
    `g1-green: {id}` has no test before `s3-review`.
  - `buf` has had no live run: its exit code on a violation (100, from
    memory), its JSON report (one object a line) and where an older
    release prints its version are read from its reference page and a
    stand-in.
- G1, three smaller ones from the same round. An unreadable
  `.sdlc/config.yaml` reads as empty, so G1 reads not active: how the
  tree and the refusal read that is `s4-tree`'s and `s5-start`'s. A
  pattern at the root walks the whole repository, `.git` with it;
  `s4-tree` measures the print. `tree.py`'s docstrings at lines 288 and
  655 say `rules:` is G0's alone.
- The second machine after `d6`'s merge: its plugin update is not
  tested, and whether that machine holds a combined document with no
  `Ready:` row is not known. Such a document now meets its own message
  there and is split by hand.
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
