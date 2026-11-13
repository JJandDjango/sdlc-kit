# Session 150 plan: G1's remaining edges, listed and ruled

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G1, the gate between intake and the first unit's test list, where a feature's requirements and spec are checked before development starts.
**Feature:** g1-requirements-spec (contract `g1-requirements-spec`): G1's three conditions, its venue `/sdlc g1`, and the refusal that keeps a task from starting before G1 passes; units s1 to s7 on main since kit 0.22.1.
**Unit:** none yet. This session lists G1's open edges for the engineer seat to rule, then drafts the design text row that records each ruling; the units that build the fixes come out of that row.

## 1. The deliverable

Next 26's remaining edges, each ruled by the engineer seat (fix it, or leave it and say so), and the design text row of `docs/features/g1-requirements-spec.design.md` that records every ruling, measured and signed.

## 2. Where this sits

Kit 0.22.1 is tagged at `268c88e` (PR #162) and the self-pin merged (PR #163, main at `efbc8df`). Unit `s7-plain-request` closed Next 26's first edge. The rest stand in three places: the backlog's Open questions (the G1 entries, `docs/backlog.md:686-792`), the `s4-tree` folds in Next actions' opener (`:393-394`), and PR #162's reading 7 and its two advisories. Each is a reading kept outside the design, the first cause in ADR 0041; this session moves each into the design text. `g1-requirements-spec` is on `g1.exempt` (`.sdlc/config.yaml:18`), so the re-intake after the row binds the contract's new units, not a G1.3 review of its own.

## 3. The steps

Where it stands at session 151's close: steps 4 and 5 done. Design r16 (the text row) and r17 (`Measured:`) are written: 14 findings, each the copied-term CL014 r13 answered; 0 OPEN; F3 found closed by `s4-tree` (`6350bec`). No requirements row: no sentence the PO seat signed changes (H1 stays inside SC4's "where G1 is active"). Step 6 done: the user signed r16 (row r18). Next: step 7, re-intake. Session 150's inputs, kept for the record:

- **The rulings.** All 37 edges as called in section 6.
- **The readings owed (ADR 0041 rule 1)**, each taken as built, since the user kept each at its review. Where one is an edge, the row takes it with the edge's ruling. PR #112: 1 (E1), 2 (E2), 9 (E3), and 4 to 8 and 10 to 12 as built (each item once; the seat equals an `intake-seat` value at the call; the last G1.3 record alone counts; an unreadable scope is refused; the flow holds the 11 items word for word; 14 lines with no source, pinned; `g1.py`'s own `Ready:` row reader, G1; an agent sat the seat only in throwaway live runs). PR #116 (s4-tree): 1 to 15 as built, except 12, which A1 overturns (the second build reads `g1.exempt`); 9 and 10 are C2's and B1's ground; 14 is B8; 15 is B5's half the tree already holds. PR #119 (s5-start): 1 to 4 and 8 to 12 as built; 5 is A1; 6 and 9 are F1; 7 is A2. PR #162: 1 to 6 are process notes (the row names them as taken, no text); 7 is H1.
- **The checks.** Each new unit takes existing checks, and each built unit keeps at least one. Proposed: `s8-honest-reads` takes SC2.1 (from `s1-lint`), SC3.1 (`s2-model`), SC4.1 (`s7-plain-request`) and SC5.2 (`s4-tree`); `s9-one-line-refusals` takes SC5.1 (`s4-tree`) and SC3.3 (`s2-model`); `s10-words-and-folds` takes SC1.1 (`s3-review`). Two moves from section 6's grouping: F2 to `s8` (the same pattern walk as C2), H2 to `s9` (the print). A moved check's requirements text stays, so no PO row, except where step 5 finds an edge that changes a check's words.
- **The design's layout** (`docs/features/g1-requirements-spec.design.md`, 531 lines): revision table at lines 1 to 17, the next row r16; Units `:381-393`; Order `:395-406`; Risks `:408-431`; Consult cases `:433-442` (case 4 takes C1's exit 2, D1's record entry and the new refusals); Decisions `:444-479`. Interfaces `:84-341` holds each command's edges; read it by section. The contract's units and acceptance sketches: `specs/g1-requirements-spec/contract.yaml:63-188`.

1. Branch `session-150-g1-edges` off main at `efbc8df`; this plan committed and pushed.
2. The edge list (section 6), published as a page for review.
3. Stop: the engineer seat rules each edge: keep Claude's call, flip it, or strike the edge. Done: the user ruled "all as called" (session 150).
4. Draft the design text row: each kept fix with its rule, each edge left named as left, and the fixes grouped into units with their order (the proposal is in section 6). ADR 0041 rule 1 also binds this row: it takes every reading kept at a PR review since r9 that r12 left for Next 26 (PR #112's readings 1, 2 and 4 to 12, PR #116's 1 to 15, PR #119's 1 to 12) and PR #162's 1 to 7, or names each one it leaves out and why. The user kept each at its review, so each is taken as built. The new units take existing checks, as `s7` did at r12: G1 holds five success criteria, the interview's limit, so a new check would make a second feature.
5. The checks before signing, recorded as a `Measured:` row: `lang-check`, the design's own checks, each edge's source re-read at its line.
6. Stop: the engineer seat signs the row. An edge that changes what the PO seat signed gets a requirements row too.
7. Re-intake: `/sdlc intake docs/features/g1-requirements-spec.md` adds the units and writes the `Ready:` rows.
8. Build each unit through `/sdlc execute`, one at a time, each to a Two-Key PASS (later sessions).
9. Close each unit: the backlog's edges closed, a row in `docs/session-metrics.md`, `plan.md` out, push, a draft PR with its readings at the top.

This session aims at steps 1 to 6. Past 40% of its window it stops with a handoff in this plan's section 3.

## 4. Where Claude stops for the user

At step 3 (the rulings), at step 6 (the signature), at each unit's test list while the tripwire in `docs/session-metrics.md` stands, and at each PR's review. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Steps 1, 2, 4, 5 and 7 to 9: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Rulings and signatures are the user's.

## 6. Rulings needed: the edge list

Claude's rule for each call: **fix** where G1 can read `done` or not active for something it never checked, where a hand-written file ends a command on a traceback, or where shipped words stand in no source; **leave, and say so** where only an outside tool's live run would settle it, or the cost is a cosmetic print. 29 fixes, 7 leaves, 1 already left. Rule by id.

**A. The readings of PRs #116 and #119 that cost something**

- **A1 Fix.** In the tree's second build an exempt feature is refused, where ADR 0038 and the design say an exempt feature is never refused. The second build skips it, as the first does.
- **A2 Fix.** Intake's I9 reads `.sdlc/config.yaml` as a person would, so where the file cannot be trusted its report can end as today while `progress` refuses every task. I9 reports what the kit's own reader returns (with F1).

**B. Hand-written files that end the print or a command (sessions 94 and 95)**

- **B1 Fix.** With G0 active, a contract that is not UTF-8, or whose scope holds a number past 4300 digits, stops the whole print. The print marks that contract unreadable and goes on.
- **B2 Fix.** `tree._load` and `scope_check.contract_scope` let the YAML loader's ValueError through (an unquoted date no calendar holds). `g1-record lint` refuses it since session 102, with no test. Both catch it; a test feeds one.
- **B3 Fix.** `g1._seat` lets the same error through for the seat term's file. As B2.
- **B4 Fix.** `g1-check` calls its three readers bare. Each failure becomes one line, exit 2.
- **B5 Fix.** `g1-check` and the other commands write through `print`, so on Windows a text outside the code page ends them through a pipe. The entry point writes UTF-8 with replacement.
- **B6 Fix (words).** `build`'s docstring says each G1 condition reads `to do` with no diagnostic in the second build, and the repository's G1 line still lists the features that hold it. The docstring says what the code does.
- **B7 Leave.** An error of another cause before the second build prints under G1's name, for that one print. The next print names it right; the design says so.
- **B8 Leave.** A `g1.exempt` entry that is not text prints whole in its problem line, however long. A cosmetic print of the user's own file.

**C. G1.1, the schema lint (session 88)**

- **C1 Fix.** With no `g1.schemas` key, `lint` prints `G1.1: no boundary schema in scope` and exits 0, while `g1-check` reads G1.1 `to do`. `lint` refuses (exit 2), as it refuses an unreadable declaration.
- **C2 Fix.** A pattern such as `./api/*.yaml`, one whose folder differs from the disk in case alone, one that is absolute or holds `..`, or one the system refuses, matches no file: its schema leaves the scope in silence and G1.1 reads `done` with nothing linted. Strip a leading `./`; refuse an absolute or `..` pattern; a pattern that matches no file reads G1.1 `to do` and names the pattern.
- **C3 Fix (words).** Five refusal lines of `g1-record` carry words no source gives and no test pins, and `g1-green: {id}` had no test before `s3-review`. The row adopts each line word for word; tests pin them.
- **C4 Leave.** `buf` has had no live run: its exit code on a violation (100), its JSON report and its version line are read from its reference page. The design says so; the first consumer with a protobuf schema measures it.

**D. G1.2, the model check (session 90)**

- **D1 Fix.** A record binds two files, the model and its configuration. A file the model extends or includes is not bound, nor a P project's sources, so G1.2 can read `done` for text no checker ran on. The record hashes the model's folder. This changes the record's entry, which is signed design text: this row is where.
- **D2 Fix, in part.** P has had no live run, and what `p check` returns with several test cases and none named is not measured; if 0, a configuration with no `-tc` records a pass with nothing checked. Refuse a P configuration with no `-tc`. The live run stays open, and the design says so.
- **D3 Fix (words).** Five refusal lines of `g1-record model` carry words no source gives. As C3.
- **D4 Fix.** Three paths end either writer on a traceback with exit 1, writing nothing: a record file that cannot be written, a NUL in a declared path or a P configuration, and a damaged schema file in the install; `contract_scope` does not catch a contract that is not UTF-8. Each becomes one line, exit 2.
- **D5 Fix.** On Windows the system finds a tool in the repository's root before PATH, so a `tlc.cmd` committed at the root is the one started, and a linter's too. Refuse a tool that resolves inside the repository: a committed file could report any pass it likes.
- **D6 Fix.** Two components with one `id`, and a `model` path that leaves the repository, are each taken as declared. Refuse both, exit 2.
- **D7 Leave.** A second name for one folder (a link, an absolute path with no drive, two Unicode forms of a name, a Windows short name) is not seen as an overlap. USAGE already states the limit.

**E. G1.3, the review (session 92; PR #112's readings).** `s7` named the no-document case; five unnamed cases remain, and a seventh from the review.

- **E1 Fix (words).** Several unchecked items: `--unchecked <n>=<section>`, once for each. The design adopts PR #112's reading 1 as built.
- **E2 Fix (words).** A name or a section with nothing in it: one line holding a letter or a digit, else exit 2. Adopt reading 2.
- **E3 Fix (words).** A declined signature: no record, and the verdict reads not passed. Adopt reading 9.
- **E4 Fix (words).** What the writer prints when all 11 items are checked. Adopt as built.
- **E5 Fix (words).** How the flow passes a section that holds a quote or a dollar sign. Adopt as built.
- **E6 Leave, and say so.** An item that does not apply to the feature is answered `checked` today, since an answer is checked or unchecked alone. The flow says at the ask that `checked` covers "does not apply"; a third answer adds a state to every record for little gain. Uncertain: a reader of the record cannot tell the two apart.
- **E7 Already left (session 93); the row records it.** A shortened flag (`--check`) is taken; a name or a section may hold a terminal escape; on Windows an id in capitals reaches the same contract.
- **E8 Leave.** A path `docs/features/<id>.design.md` that is a folder counts as no design document. That is the right reading; the row says so.

**F. Three smaller ones**

- **F1 Fix.** An unreadable `.sdlc/config.yaml` reads as empty, so G1 reads not active and gates nothing. An unreadable config is refused by name, never read as G1 off (with A2).
- **F2 Fix.** A pattern at the root walks the whole repository, `.git` with it. The walk skips `.git`.
- **F3 Fix (words).** `tree.py`'s docstrings at lines 288 and 655 say `rules:` is G0's alone. Correct them.

**G. The `s4-tree` folds (Next actions' opener)**

- **G1 Fix.** `g1.py`'s `Ready:` row reader and `tree.drift`'s are two readers a test holds equal. Fold them into one: two readers of one row can drift.
- **G2 Leave.** `progress._target` has one caller left. A helper with one caller costs nothing.

**H. From PR #162**

- **H1 Fix (your call matters most here).** Where G1 is active, `new` refuses a contract born from an escape or from maintenance (`provenance.origin` `g8-escape` or `g9-maintenance`) with no feature document of its own id. G1 does not gate those origins: they fix or keep behavior a gated feature already specified. Uncertain: an escape fix that adds behavior then skips a review.
- **H2 Fix.** The tree may show a stale review's evidence beside the RS302 line (`taskcontract/tree.py:710`). With RS302 the tree shows no review evidence.
- **H3 Fix (words).** One over-long line in `docs/usage/g1.md:218`.

**The units the fixes would make** (ruled at step 4, shown here for size):

- `s8-honest-reads`: G1 reads only what it checked. A1, A2 with F1, C1, C2, D1, D2, D5, D6, H1.
- `s9-one-line-refusals`: no hand-written file ends a command on a traceback. B1 to B5, D4.
- `s10-words-and-folds`: the shipped words stand in the design, and the small folds. B6, C3, D3, E1 to E5, F2, F3, G1, H2, H3.

## 7. What could go wrong, already ruled

- An edge's line has moved since it was recorded: step 5 re-reads each source at its line before signing.
- An edge was closed by a later unit and the backlog missed it: step 5's re-read drops it, and the row says which unit closed it.
- The design document is large: it is read by section and by `Grep`, never whole.
- New prose fails the controlled-register check: step 5 runs `lang-check` before the signature.

## 8. This session's cost, with its basis

About 0.2M to 0.3M tokens for steps 1 to 6: the list from about 200 backlog lines and two PR bodies, then one drafted row and its checks, the size of session 147's two rows. The build, in later sessions: three units at about 0.7M to 1.0M agent tokens each at one round (rs4 ran 634K, rs1 to rs3 about 1.0M each, `docs/session-metrics.md`), about 2M to 3M in all; each failed round adds about 100K to 200K.

## 9. Not in this session

- The build of the units (steps 7 to 9).
- The engine's contract made from a plain request: the engine's to clear.
- The backlog's Open questions that are not G1's.
- G2.

## 10. Words

- **G1**: the gate a feature passes before development starts; active for a feature when `G1` is under `active_gates` in `.sdlc/config.yaml` and the feature is not on `g1.exempt`.
- **G1.1, G1.2, G1.3**: G1's three conditions: each boundary schema lints clean; each hard core's model passes its checker; a person's review of 11 items on the feature's documents.
- **edge**: a case the signed design does not name, found after it was signed, and kept on the backlog until the engineer seat rules it.
- **engineer seat, PO seat**: the roles that sign a document's halves: the design and the requirements.
- **text row, `Measured:` row, `Ready:` row**: rows of a document's revision table: a change to its text; the checks run before signing; intake's record that the contract was derived from a signed revision.
- **re-intake**: intake run again on a changed pair, so the contract follows the documents.
- **exempt list**: `g1.exempt`, the features G1 does not gate.
- **record**: a line `g1-record` appends to `.sdlc/g1/<id>.yaml`, the evidence a condition reads.
- **TLC, P, buf**: the outside checkers G1 starts: TLC checks a TLA+ model, P checks a P project, buf lints a protobuf schema.
- **the print, the tree**: `taskcontract tree`, the page of every feature's gates and units.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **tripwire**: the rule in `docs/session-metrics.md` that sends a unit's test list to the user after an escape traced to a test list Claude approved.
