# Standing practice - sdlc_development_kit

How sessions in this repo work, moved verbatim from the retired `STATE.md` at
the Cairn 2.0 migration (2026-10-16). Entries still name `STATE.md`, `plan.md`
and session numbers as they stood when written. The rules that bind every
session are the house rules in [CONTRIBUTING.md](../../CONTRIBUTING.md).

- The process's cost (the user, 2026-10-12, session 96). A build is
  two sessions, split once the test list is approved and recorded: the
  first hands over by a file in the receipt folder, and the second
  starts from it. A session left overnight is not resumed, since its
  cache has expired and the resume writes the whole context again: a
  new session starts from the handoff file. Two-Key's receipts agent
  runs on Haiku 5.5 at `low`; the drafter, the developer and the
  grader stay on Opus 5.5 at `high`. A cost is quoted in tokens by
  kind and in shares, never in dollars, since the user is on a
  subscription. From the measure, Claude's own practice: each request
  sends the whole context again, so tool calls that do not depend on
  each other go out in one turn, bulk reading goes to an agent, and a
  long result lands in a file. `tools/session_cost.py` measures a
  session and its agents, and a build's wrap runs it.
- Test-runner scripts (the user, 2026-10-18, session 103). A script
  runs the tests and prints only the summary, the failing ids and the
  first assertion line of each; the full log goes to a file. An agent
  never copies, mutates, runs and restores by hand: the `s6-release`
  drafter took 299K tokens and 124 tool calls, mostly that plumbing.
  `prove.py` (in untracked `.claude/workflows/tools/`, built in
  session 105, signed list and readings in [prove-py.md](prove-py.md))
  is the drafter's red, green and mutation proof, and the drafter's
  brief names it. `receipts.py` (same folder, built in session 106, signed
  list and readings in [receipts-py.md](receipts-py.md)) runs Two-Key's
  receipts in the session with no agent; its JSON goes to the workflow as
  `receiptsResult`, and the receipts agent runs only when none is given.
  The whole suite runs on workers, `python -P -m pytest tests -q -n
  auto` (session 119: 2085 tests in about 70 s, 453 s one at a time);
  a one-file run stays serial. Run `receipts.py` with
  `run_in_background` and put a Monitor on `OUT/progress.json`, since a
  receipts list can still outlast the foreground cap.
- Session 98's lessons. A reading rules only where the signed pages are
  silent: before one goes into a test list, read it against the
  design's Constraints and Sources, not only its Decisions. Round 1 was
  lost to a reading that broke constraint 11 while the pins held its
  letter. A pin on a word's absence (`python -m`) is passed by a bare
  name: pin the behavior the constraint forbids. A live intake run that
  reaches I9 needs no saved pair: `intake_live.py` in the s5 receipt
  folder builds a repository with a seat roster and no contract, and a
  plain request with the plan answers in it takes two turns. Take a
  computed PASS whole only when every receipt command reports: the Haiku
  receipts agent returned one round with two commands running.
- Session 95's lessons. An escape typed into an Edit or a Write is
  decoded: backslash-u text becomes the character before the file is
  written. Prose that shows an escape is written by a script that
  builds the backslash with `chr(92)`, and the line is read back by its
  bytes. It cost Two-Key round 4. The trial of hostile inputs runs to
  the print's other end too, through a pipe with the output's encoding
  strict: a build that is whole can still stop at the write. The
  kit-print hash is taken from one clean worktree at each commit, since
  the working root's print holds the local progress records and its
  hash moves with each `progress` call. A failed round is the user's to
  waive, never Claude's: the plan stops there, and the progress record
  holds the waiver as the `two-key` task's reason.
- Session 94's three lessons, each paid for with a Two-Key round or
  with context. Guard a boundary, never the calls behind it: where a
  unit makes old code run in a new place (the tree running `g1-check`'s
  readers at every print), ask what the new place promises (the print
  never stops) and hold that promise at the one place the old code is
  entered; a trial of hostile inputs finds some causes and never proves
  there are no more. Name the session boundary before 40% of the
  context, at the plan's own boundary after the test list's approval:
  a build session with a lost round passes 50%. And hand an agent its
  brief as a file: a brief sent inline is sent once and echoed back in
  the agent's result.
- No approval before the final PR review (the user, 2026-10-11, session
  92). The signed feature and design documents are the gate. Neither
  the plan nor the test list takes an approval, and Claude records each
  `--by claude`. The plan is written in the plan page's shape, pushed,
  named in one line with its GitHub link, and the build starts. Before
  the PR Claude stops on two events only: a case the feature document,
  the design document and the contract leave open that their purpose
  cannot settle, or whose answer would change a signed contract
  sentence, a ratified term or an ADR; and a discovery during the build
  that needs the user's decision. A case the documents never name is
  ruled from their purpose, built on, and listed at the top of the PR
  body as a reading, never put to the user as a ruling with a
  recommendation. It is also listed as a gap for the design's next text
  row, since the user reads each stop as a failure of the documents'
  vetting. A defect found in a unit already on main is confirmed, named
  in the PR body and charged in the metrics, and stops the build only
  if its fix needs a decision. The plan page's section 6 then reads
  "Rulings needed: none", with the readings under it. This entry
  replaces the plan's approval and the 2026-10-09 return of the test
  list in the entry below; that entry's other terms stand.
- A plan stays out of a PR's diff and off main (the user, 2026-10-11,
  session 93). `plan.md` is written at the repo root and committed on
  the work branch at the session's start, so GitHub shows it at its
  commit. The branch's last commit before the review removes it (`git
  rm plan.md`), so the PR's diff holds the work alone and main's tree
  holds no plan. The PR body links the plan by its commit,
  `https://github.com/JJandDjango/sdlc-kit/blob/<sha>/plan.md`: the
  link names a commit, so it holds after the branch goes, since the
  merge commit keeps that commit in history. The wrap copies no plan
  onto main. The reasons: a plan is read before the work, by the
  person who supervises the session; a reviewer reads the PR body; and
  a tracked root plan would conflict between a team's open branches
  (the last reason is Claude's, accepted by the user). First applied
  on PR #112 at `753c1de`.
- A unit with a code half and a prompt half, under no approvals
  (session 92, `s3-review`). Two drafters side by side by `scriptPath`,
  each with its own scratch folder; the prompt drafter's notes say its
  prototype is a copy of `skills/`. Both prototypes go onto one scratch
  worktree for one whole-suite run. Before a developer starts, the
  session tries each free-text rule on the prototype with inputs the
  drafter's tables lack, from a scratch `trial.py` kept in the receipt
  folder: it found a name of one zero-width space read as a signature.
  A small amendment is the session's: the test, the prototype and the
  note, then red and green again. Two developers side by side, each
  told to leave the whole suite to the session and given its note as a
  file outside the drafters' folder.
  `tools/g1_review_live.py <workflows> <plugin worktree> <root>
  <driver folder>` builds a throwaway repository for a live run of
  `/sdlc g1` and a driver whose second session finds the kit's package
  through PYTHONPATH; the first message goes from PowerShell, and
  `live-run-seats.js` takes the first reply as `opening`. A run takes
  14 to 16 turns and about 58K tokens. After a wording fix to the flow,
  one run is taken again from the fix commit. `split_journal.py` splits
  a journal at `\n` alone, since a note that held U+2028 broke
  `splitlines`. Run pytest with `-rN` when many cases fail: the summary
  lines passed 30K characters once. A `rm -rf` of a folder under `E:/`
  is refused by a safety check: leave such a folder to the user.
  Session 92: drafters 232K and 129K, developers 114K and 80K, Two-Key
  226K, PASS round 1.
- Plan approved, then PR review (the user, 2026-10-08, session 89). An
  approved plan is the only gate before the build, and the user is
  next needed at the work PR's review. The user holds: the plan's
  approval; the work PR, which Claude opens after green CI and a
  Two-Key PASS and merges on the user's word; a ruling that changes a
  signed contract sentence, a ratified term or an ADR; each seat
  signature; each release and tag; and, since the tripwire fired on
  2026-10-09 (session 90), the unit's test list and each later
  amendment of it, shown in chat before the developer starts and
  recorded `--by user`. Claude holds: the unit's commits; USAGE text
  that only restates the signed design; the
  commit and push of `plan.md` to the work branch before its approval;
  the wrap PR's merge after green CI. A reading that surfaces
  mid-build: Claude builds on its own reading and lists it at the top
  of the PR body, and stops for the user only when the reading would
  change a signed contract sentence, a ratified term or an ADR. The
  plan's fixed shape, since session 91 (the user, 2026-10-10): the plan
  page of `NOTES_document-theory_2026-10-10.md`, a header (project,
  area, feature and unit, each with its purpose in one sentence) and
  ten sections: the deliverable in one line; where this sits; the
  numbered steps, each agent named by its role, with a gloss, beside
  its script; where Claude stops for the user; where Claude goes on
  alone, and by what rule; each foreseeable ruling with a
  recommendation, in plain words (the approval rules on them); what
  could go wrong, already ruled; the session's cost with its basis; the
  deferred list; and the words. It is written for a reader with no
  context and holds only its session's facts. The header and "where
  this sits" do the work of session 90's Overview, and a gloss at each
  word's first use with the closing list does the work of its Terms
  (the user, session 90: the first draft could not be read). Each time
  it is shown, a GitHub link to `plan.md` on the pushed branch goes
  with it. The tripwire: a delegated item returns to the user at once on one
  escaped defect traced to an approval Claude gave, or on two overturns
  of the same kind at PR review. Where an entry below sends one of
  Claude's items to the user, this entry governs. Before saying who
  approved a step, read `.sdlc/progress/<id>.yaml`.
- A document's reader has no context (the user, session 91). A feature
  document, a design document and a plan are each written so that a
  new session of an LLM or a new developer can judge a case the page
  never names: the page stands alone, glosses each word at its first
  use, and names by path what it needs from another page. A new shape
  or a new word is put to the user on a filled-in page, never as a
  bare list of sections: the list confused the talk, and each
  filled-in page was agreed in one reply.
- Session metrics (session 89). Each build session's wrap appends one
  row to `docs/session-metrics.md`, by the eight measures the page
  lists; a session that ships no unit adds none. An escaped defect
  found later changes the row of the session that shipped it. Raise the
  first look at the resume after five build rows past session 89's
  marker, and the full review after ten.
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
- The wrap follows the merge (the user, 2026-10-08). The work PR merges
  first, on the user's word after CI. Then `STATE.md` and the memory
  index (with `plan.md`, until session 93) are written on a new branch
  off main and ride a
  wrap-only PR, which Claude merges after green CI (since session 89;
  before it, on the user's word). So the wrap names the work's
  merge commit and its PR as facts, and its Blockers line names only the
  wrap's own branch. A plan's close is two steps: the push, the PR and
  the merge of the work; then the wrap in its own PR. A wrap committed
  inside the work PR could not name the merge: sessions 71 and 72 left
  a line the next resume corrected, session 84's said the PR waited,
  and session 86's resume read git to learn that PR #101 had merged.
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
- A plan is plan.md in the fixed shape of this section's first entry,
  shown in chat for the user's overview with its GitHub link. A USAGE
  refinement never narrows a contract sentence silently: a narrowing
  stops for the user, and any other reading is listed at the top of the
  PR body (session 89). A
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
- A design run in batches (session 84). Four read-only explorers come
  first, a slice each (the rules, the tree, the progress record, intake
  and the release), through one inline Workflow with a structured
  result; `tools/split_explorers.py` splits its journal into one file a
  slice. Then the shape calls as one batch, before S1, and four batches
  of sections. Each batch shows only the details that carry a decision,
  with the full text on request. `tools/state_text.py` copies each
  section from the document into the state file (text, list, table or
  question and answer), so the two cannot differ. Probe the done-means
  sentences through `tools/probe_units.py` before the user sees them:
  four runs took 17 unknown words to none. A release unit must hold a
  check, or intake refuses it. Check each done-means sentence against
  every path of the design: one was false of a contract's close, and
  the design changed. Count a list after it is written, never before:
  the session quoted two counts wrong. Source a cost from the recorded
  figures and show the basis. Tokens: explorers 897K, retirer 62K; the
  session closed near 40% of a 1M context.
- A hand amendment of a signed requirements document (session 85).
  Measure first, with no agent: the tree, the counts, the design's
  words for each call, ADR 0037's shape, and intake's I2 against the
  document. Two batches: the changed sentences, before and after, then
  the Gherkin, where every fact of a scenario comes from its check (the
  interview's Q15). The checks before signing run through `lang-check
  --draft` on a scratch state file that a script builds from the
  document: the statement, the non-goals, the checks and the new terms.
  Three rows follow: `Measured:`, the text row, `Signed:`; the Gherkin
  tag names the text row. The text row says what changed, since DESIGN
  CONFIRM shows it to the engineer seat. Start the design run while the
  suite runs: DESIGN CONFIRM writes nothing before the seat's answer.
  Before the seat answers, read the design against the new revision
  and name each sentence that reads stale. Write the state file's new
  copy of the terms as the list. Grep `tests/` for a removed module's
  name: two docstrings named it. Run `lang-check` in the background and
  grep for `lang-green`: run in the session, its 130 lines land in the
  context.
- The terms and an ADR before intake (session 86). Two commits, the
  ADR first, since an amended term rests on it. Draft the ADR as an
  untracked file before its batch, so the user ratifies real text from
  a list of its decisions. Read each ADR whose sentences the design
  changes, besides the one it names: 0032 held "each feature shows its
  active gates". An amended definition can stand in no signed text:
  propose the words, widen and never narrow, and keep the requirements'
  words where the design's differ. The neighbor read is one grep of
  every `definition:` under `specs/vocabulary/`. Two files there are no
  term, `dictionary.yaml` and `constraints.yaml`: take the count from
  `vocab-check`. No test pins a definition or counts the dictionary's
  words, so the suite read green unchanged, and no page counts the
  terms. `MAP.md` names an ADR beside a component a release built, so
  it waits for the release unit.
- Intake of a pair written by hand (session 87). The requirements
  document holds no state file, so the draft contract is written from
  the pair, outside `specs/`. `tools/door.py <root> <draft> [word ...]`
  runs `check_contract` on the draft and probes each word after it:
  one run lists the unknown words, the next probes their substitutes.
  These read unknown alone: `active` and `inactive` (only "active
  gate" is a term), `fails`, `failed`, `starts`, `started`, `asks`,
  `person`, `signs`, `derived`, `installed`, `summary` and `ends`.
  These are known: `derives`, `install`, `covers`, `human` and
  `closes`. A status value or a printed word goes in backticks. A
  plural of a term reads unknown: write "each feature already done, all
  18". Copy the draft onto the scaffold with `cp`, so the contract is
  the draft byte for byte. A draft outside the repository validates
  ready-green with no `confirmed_by`: TC016 showed only once the file
  stood under `specs/`. The readback is one reply: the decisions
  counted first, then only the readings that could change what a test
  pins, with the full text on request. `git diff --no-index --stat`
  proves the plugin's flow file equal to the repository's. Session 87
  took four replies from the user and no agent.
- A code unit that runs an outside tool (session 88, `s1-lint`). Probe
  the real tool first, from a scratch script that prints each argv, its
  exit code and both streams, and save the script with its output in
  the receipt folder: the drafter reads them as the tool's measured
  interface. Probe the exit code for each severity, the output with and
  without each flag, and a start by the bare name from Python: on
  Windows an npm tool is a `.CMD`, and only `shutil.which` finds it.
  The tests use a stand-in that runs as a real child process on a PATH
  each test sets, a `.cmd` beside a Python script on Windows and an
  executable `sh` script elsewhere, so no test needs the tool and CI on
  ubuntu passes. `tools/g1_lint_receipt.py <repo> <root> <receipt>`
  takes the live receipt on a small consumer repository it builds; take
  it again after a fix commit. `overlay_pkg.py` leaves out a file new
  in the prototype: copy it with `overlay_files.py`. It also reports a
  file whose line ends differ; `git diff --stat` on the worktree shows
  the true changes. Read the design's "Decisions and open questions"
  before a reading goes to the user: line 417 answered a question the
  session had put to the user another way. Test each question a
  developer returns against `done_means`, as a deviation is tested: a
  path that reaches `done` with no record is a defect, never an edge to
  park. In a second Two-Key round, name round 1's defects and ask the
  grader to look for other paths of the same class. A callout over red
  text says what holds through the whole build, never what is absent
  today. Session 88's `s1-lint`: drafter 225K, developers 104K, 60K
  and 69K, Two-Key 205K and 247K, PASS round 2.
- A code unit whose tool is a checker (session 90, `s2-model`). The
  probe takes two runs: the first finds what breaks (TLC did not find a
  model by a forward-slash path from the root, and two runs in one
  second collided on its working folder), and the second gives every
  call its own `-metadir` and reads each exit code. A findings file
  beside the probes holds three parts: measured; read and not run; the
  session's readings. The drafter and the developer both read it. A
  tool with no live run (P) gets its facts from its own repository
  through `gh search code` and `gh api`, never from memory: memory gave
  P's exit codes wrong. `tools/g1_model_receipt.py <repo> <root>
  <receipt> <tool folder>` takes the live receipt, with the tool's
  folder first on PATH for its own child; run it once before the commit
  as a rehearsal. Before a rule that sorts free text is approved (file
  or folder, in or out of scope), try five hostile inputs against it:
  no trailing slash, a leading `./` or `/`, `..`, letter case, a
  doubled slash. Make each "cannot tell" land on the safe side, say in
  USAGE what form the input must take, and stop there: round 1 was lost
  to a folder written with no slash. A test that pins a file's hash
  plants a failure in a later unit: drop it and let Two-Key read `git
  show --stat`. A fix round is narrow: the tests are placed first, on
  the user's approval, and the note names only the behavior to change.
  Wording that Two-Key marks as an advisory is fixed in one commit
  after the PASS, with the suite run again and the PR body saying so.
  Session 90's `s2-model`: drafter 212K, developers 115K, 76K, 61K and
  59K, Two-Key 236K and 205K, PASS round 2.
- The form validator on this machine (session 78): put one line,
  `E:/foundations`, in a `foundations.pth` under the scratch venv's
  `Lib/site-packages`, and `pip install tiktoken` there. `python -m
  prompt_lang` takes one path, and a folder works.
- The whole suite runs about a minute at `-n auto`, 8 minutes one at a
  time; a local model holding RAM can get a background run killed for
  memory. A PR's CI waits through `gh pr
  checks <n> --watch` in the background; started right after a push it
  can end `no checks reported`, so watch again.
- The suite on this machine: a session's `python` is miniconda's 3.13
  (`E:\miniconda3`, first on PATH), which holds `textual` and, since
  session 119, `pytest-xdist` 3.8.0, so `python -P -m pytest tests -q
  -n auto` runs under it. A scratch venv
  is needed only for the form validator (session 76): `py -3.14 -m venv <scratch>/venv`, then that venv's
  `python -m pip install "textual>=8.2,<9" "pytest>=8" "pytest-xdist>=3"
  "jsonschema>=4.18" "PyYAML>=6"`, then its `python -P -m pytest tests
  -q -n auto` in the background. `lang-check` prints about 130 exempt lines
  before its last one: run it in the background and grep the output for
  `lang-green`.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  (`docs/usage/restricted-environments.md`) against the new tag with
  `python -P`. main's ruleset requires a PR for
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
