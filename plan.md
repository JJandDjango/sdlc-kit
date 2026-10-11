# Plan - Session 94 (2026-10-11) - g1-requirements-spec s4

```
Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     G1, the requirements gate: a feature's failure points are found before its development starts.
Feature  g1-requirements-spec: the kit computes G1 and refuses a task until G1 passes.
Unit     s4-tree, the fourth of six: the tree shows G1 with each condition's status, its diagnostics and the review.
```

This plan stands under three pages and repeats none of them:

- the feature page, `docs/features/g1-requirements-spec.md`: what is
  wanted, and why;
- the design page, `docs/features/g1-requirements-spec.design.md`: the
  shape of the solution;
- the contract, `specs/g1-requirements-spec/contract.yaml`: the signed
  sentences a build may not change.

A word the three pages do not define is glossed where it first stands
and listed in section 10.

## 1. The deliverable

By the session's end unit `s4-tree` stands on main through one PR, with
a passing independent grade.

## 2. Where this sits

A gate is a pass/fail checkpoint between two phases of the work. G1 is
the kit's second gate, and it holds three conditions (a condition is
one named part of a gate): G1.1 the lint, G1.2 the model check, G1.3
the signed review. The feature is built as six units, one a session,
and ships as kit 0.20.0. A unit is one slice of a feature, built and
graded by itself.

| Unit | What it adds | State |
|---|---|---|
| `s1-lint` | G1.1, the record file and both commands | on main (PR #106) |
| `s2-model` | G1.2 | on main (PR #109) |
| `s3-review` | G1.3 and `/sdlc g1`, the flow where a person runs G1 | on main (PR #112) |
| `s4-tree` | the tree, the kit's printout of every feature's state, shows G1 | this session |
| `s5-start` | no task starts before G1 passes | to do |
| `s6-release` | the release, and G1 turned on in the kit's own repository | to do |

What this unit adds, each fixed by the design page (the tree at line
256, Sources at 307, Constraints at 327, the unit's row at 352):

- A feature's own active gates. A feature that needs G1 shows G1
  active, with G2 as the next gate, marked `inactive`. A feature on the
  `g1.exempt` list of `.sdlc/config.yaml` prints as today, byte for
  byte.
- G1's reading in the tree. Each condition takes its status and its
  diagnostics (a diagnostic is one thing a rule reported) from the
  rules `g1-check` runs, and the G1 line is their roll-up (the ratified
  rule by which a parent takes its status from its children).
- The review's evidence on the G1.3 line: `by po at r5, design r4`.
- The repository's line, `gates/G1`, names each feature that holds G1.
- A problem line for a record or a declaration that cannot be read, and
  for an exempt id that names no feature.
- The pane, the live view of the tree, watches `.sdlc/g1`.

The unit's done-means sentence, the one sentence it must make true:
"The tree shows G1 as an active gate where a feature needs it, with
each condition's status, diagnostics and review." Its checks, the
contract's testable lines, are SC5.1, SC5.2 and SC5.3
(`contract.yaml:120-139`). One older test retires, named by the design:
the hash that pins `tree.py`'s code.

Measured at this resume, on main at `1b86252`:

- The tree gives every feature the same active gates
  (`taskcontract/tree.py:309-318`) and reads G0's verdict alone
  (`tree.py:551-585`), so a G1 line and its conditions always read `to
  do`.
- `taskcontract/g1.py` already reads each condition: `read_lint` (line
  303), `read_model` (471) and `read_review` (639). `is_active` (197)
  says whether a feature needs G1, and `g1-check` prints from the three
  (668). The tree has one source to call.
- The kit's own `active_gates` holds G0 alone (`.sdlc/config.yaml:5`),
  so the kit's own print must keep every line. Today it prints 1,545
  lines in 4.4 seconds, the middle of five runs.
- The pane watches four folders, and `.sdlc/g1` is not one
  (`taskcontract/tree_view.py:77`).
- USAGE (`USAGE.md`, the user guide) holds this unit's text since
  `s1-lint`, under red marks that mean "described, not shipped"
  (`USAGE.md:2012-2048`). The marks stay red until `s6-release`.
- The pin that retires stands at
  `tests/test_document_split_release.py:488-489`, its hash at line 115.
- Not run at this resume: the whole suite. It read 1599 passed at
  session 92's close (`STATE.md`).

## 3. The steps

The unit is code alone, so one agent works at each step.

1. **Open (Claude).** Branch `session-94-g1-s4-tree` from `1b86252`.
   This plan is committed and pushed, and the build starts. The plan
   takes no approval (section 4).
2. **Draft (one drafter).** A drafter is an agent that writes a unit's
   tests before any code, proves each one fails today, and proves on a
   throwaway prototype that they can pass
   (`.claude/workflows/spec-channel-drafter.js`). Its prototype is a
   scratch copy of the `taskcontract` package.
3. **Overlay (Claude).** The prototype's changed files and the drafted
   tests are copied onto a scratch copy of the repository, and the
   whole suite runs there once. Claude retires the hash pin by hand,
   since the design names it. The retirer, an agent that retires the
   older tests a unit makes false (`.claude/workflows/test-retirer.js`),
   runs only if another older test fails for a reason this unit owns.
4. **Check the list (Claude).** Each fixed detail is read against the
   contract, both pages, the design's Constraints and Decisions, the
   ratified terms under `specs/vocabulary/` and USAGE's red text. Each
   rule that reads free text or a hand-written file is tried on the
   prototype with hostile inputs (section 6 names them).
5. **Approve the test list (Claude).** The approval is recorded `--by
   claude`. The list and what step 4 found are saved in the receipt
   folder and summed up at the top of the PR body. Then `progress`, the
   command that records each task, records each check's failing run.
6. **Green (one developer).** A developer is an agent that writes the
   real code from an interface note, a page of names and behavior, and
   never opens the tests (`.claude/workflows/unit-developer.js`). Claude
   then runs the whole suite.
7. **Commit (Claude).** The USAGE sentences section 6 adds, then the
   unit's commit. Each check reads green at the clean commit, and the
   kit's own contract and scope checks read green.
8. **Measure (Claude).** Two receipts, saved in untracked
   `RECEIPT_g1-requirements-spec-s4_2026-10-11/`. The kit's own print
   at the unit's commit is compared with main's, line for line. The
   print is timed on a scratch copy of the kit with G1 turned on for
   all 20 features, against today's 4.4 seconds (the design's Risks,
   9).
9. **Two-Key.** An agent that grades the unit from its own test runs
   and returns PASS or FAIL
   (`.claude/workflows/two-key-unit-verifier.js`). It reads both
   receipts. On PASS the unit is recorded done.
10. **The work's close.** The branch's last commit takes this plan out,
    so the PR's diff holds the unit alone. Then the push, and the PR
    once CI reads green and Two-Key reads PASS, with Claude's readings
    at the top of its body and a link to this plan at its commit. The
    user reviews it and says merge.
11. **The wrap, after the merge (Claude).** `STATE.md` rewritten, the
    memory index updated and one row appended to
    `docs/session-metrics.md`, in a PR of their own that Claude merges
    after green CI.

The session boundary, if context runs short: after step 5. The approved
list, the prototype and the interface note are copied to the receipt
folder, and step 6 opens the next session.

## 4. Where Claude stops for the user

Once: the work PR (step 10). The merge is the user's word.

The user ruled on 2026-10-11 that the feature page and the design page
are to hold enough for the build to run to that review with no
approval: not of this plan, and not of the test list. Before the PR,
Claude stops on two events only:

1. A case the three pages leave open and their purpose cannot settle,
   or one whose answer would change a signed contract sentence, a
   ratified term or an ADR (an architecture decision record under
   `decisions/`).
2. A discovery during the build that needs the user's decision.

Each such stop is also a finding against the pages: it names what
their vetting missed.

## 5. Where Claude goes on alone, and by what rule

Alone: everything before the PR. That is the branch and its pushes,
the agents' briefs, the overlay and each suite run, the hostile inputs,
the test list's approval and each change to it, the hash pin's
retirement, the unit's commit, the USAGE sentences, both receipts,
opening the PR, and the wrap's merge.

The rule: where the pages name no case, Claude rules from their
purpose, builds on that reading, and lists it at the top of the PR
body, where the user can overturn it. If the reading would change
signed text, Claude stops.

For an event this plan never names, ask what the unit is for: does the
tree give a condition of G1 the status `g1-check` gives it, for every
feature that holds a contract? The design names one source for both
(its Sources, line 321). If the event opens a path where the tree
reads `done` and `g1-check` does not, it is a defect, and it is fixed
before the commit. A question or a shortcut the developer returns is
put to the same test.

## 6. Rulings needed

None: this plan takes no approval. The seven cases below are ones the
design never names. Claude settles each from the pages' purpose, a tree
that shows the exact state of every feature's work, and lists it at the
top of the PR body. Each is also a gap to close when the design is next
amended.

1. **When G1.3 shows the review.** The design draws the evidence on a
   `done` line alone. The reading: it prints when G1.3 reads `done` or
   `failed`, since the last review counts in both and SC5.3 asks that a
   signed review show its seat and each revision it names. A review
   that does not count prints nothing, as an absent one: a record that
   is not well formed, or one that checks every item on revisions the
   contract was not derived from.
2. **What the evidence holds.** The record is a committed file a person
   can edit. The reading: the line prints the record's seat, then each
   revision the record names that reads as `r` and digits. A revision
   of any other form is left out, and the status is `g1-check`'s
   whatever the evidence shows.
3. **A feature before intake.** It holds no contract, so it has no
   scope to read. The reading: each of its three conditions reads `to
   do` and lists nothing, whatever stands under `.sdlc/g1/`. The design
   says such a feature shows G1 active and `to do` (line 276).
4. **The words of the problem lines.** The design says the tree prints
   one and gives no words. The reading: each takes the form the tree
   prints today, `unreadable <what>: <path> (<reason>)`, and the line
   for an exempt id that names no feature is worded beside it. A
   declaration's line prints once a print, never once a feature. Each
   line's words are listed at the top of the PR body.
5. **G1's lines with G1 off.** The reading: with `G1` absent from
   `active_gates` the tree reads no G1 file and prints no G1 problem
   line, so every repository that has not turned G1 on keeps every
   byte of its print, the kit's own among them.
6. **An exempt feature under a list that holds a later gate.** The
   design draws `active_gates` with G0 and G1 alone. The reading: an
   exempt feature's G1 line always prints with the `inactive` mark,
   since SC5.2 says such a feature shows G1 `inactive`. No gate after
   G1 is computed today.
7. **The query and the pane.** `tree <id>/G1/G1.3` prints its line with
   the evidence and its `page:` line, with no `file:` line and no
   diagnostic, as a condition's query prints today. The pane watches
   `.sdlc/g1` and no schema or model file, so a change to one of those
   shows at the next redraw another source causes.

The hostile inputs of step 4: `G1` active with `G0` off; an `exempt`
value that is no list; an exempt id in another letter case; a record
file that is no mapping, or that cannot be decoded; a review whose
seat, section or revision holds a tab, a terminal escape or 300
characters; a record that names a `design` revision where the feature
holds no design document; `specs/components.yaml` that the schema
refuses.

## 7. What could go wrong, already ruled

- **Two-Key fails a round.** One narrow fix round: the tests are placed
  first, tried against the same hostile inputs, and the developer's
  note names only the behavior to change. Round 2 names round 1's
  defects and asks for other paths of the same kind. After a third
  failure Claude stops.
- **An older test fails on the overlay.** The design counts 20 tests
  that pin the tree's print or its code (its Risks, 4). If the test
  pins a print this unit must change, it is amended and named at the
  top of the PR body; else the build is wrong. A fixture with G0 and G1
  active and no declaration must keep reading `to do`.
- **The print slows.** The tree reads two declarations and one record
  file a feature at every print. If the timed print passes twice
  today's, Claude names the cost at the top of the PR body, and the
  declarations are read once a print before the commit.
- **The tree and `g1-check` differ.** A defect by section 5's test: the
  tree calls the three readers `g1-check` calls, and a test holds the
  two equal on each fixture.
- **A drafter says which way a rule errs.** The claim is tried with
  hostile inputs before the list is approved. Session 90 lost a round
  to an untried one.
- **An agent passes about 400K tokens.** It is stopped and its work
  split.
- **A defect of a unit already on main shows.** Claude confirms it with
  a live run and names it at the top of the PR body, and the metrics
  row of the session that shipped it takes it. It is fixed here only if
  this unit cannot stand without the fix; else it joins section 9.
  Claude stops only if the fix needs a decision.

## 8. This session's cost, with its basis

About 0.6 million agent tokens, in a range of 0.5 to 0.75 million. The
basis is the two recorded code units, each at its first round: session
81's `d4` at 561K (drafter 213K, developers 94K and 75K, Two-Key 179K)
and session 90's `s2-model` at 563K (drafter 212K, developer 115K,
Two-Key 236K).

- A lost Two-Key round adds about 300K (session 90's cost 325K).
- A retirer round adds 62K to 159K.

Touches, the replies Claude needs from the user before the PR review:
none planned. The target is 0.

## 9. Not in this session

- `s5-start` and `s6-release`. So no task is refused yet, and the kit's
  own tree shows G1 `inactive` until the release turns it on.
- Session 90's first ruling (one G1.1 record that holds a result for
  each `g1.schemas` entry) and the fix of G1.1's escaped defect, in a
  session of their own before `s6-release`. Until that fix the tree
  shows what `g1-check` reads: G1.1 `done` for a contract whose scope
  cannot be read.
- One reader for the `Ready:` row. `g1.py` and `tree.py` each hold one,
  and the fold changes no print.
- A pane that watches schema and model files (ruling 7).
- The open edges of G1.1, G1.2 and G1.3, under `STATE.md`'s Open
  questions.
- The feature and design pages in the shapes of
  `NOTES_document-theory_2026-10-10.md`: a feature of its own.
- The pilot (`E:\ImSimProject\engine`), until G1 ships.
- A lean Claude Code launch profile, the user's to handle and no kit
  feature (`NOTES_lean-system-prompt_2026-10-11.md`, written this
  session): a replacement system prompt and a trimmed tool set, about
  17K fixed tokens against 44K, nothing installed. The wrap carries
  this line to `STATE.md`.
- The `google_workspace` server, which failed to connect again at this
  resume.

## 10. Words

| Word | Meaning |
|---|---|
| Unit | One slice of a feature, built and graded by itself. |
| Done means | The one sentence a unit must make true. |
| Check | One testable line of the contract, with an id such as SC5.1. |
| Suite | Every test in the kit, run together. |
| Tree | The kit's printout of every feature's state, derived at each print. |
| Pane | The live view of the tree in a terminal pane. |
| Evidence | The words a tree line prints after its status, such as `by po at r5`. |
| Problem line | The tree's line for a source it could not read. |
| Exempt | Named by `g1.exempt` in `.sdlc/config.yaml`, so G1 stays inactive for the feature. |
| Drafter | An agent that writes a unit's tests first and proves they fail today. |
| Prototype | The drafter's throwaway code. It proves the tests can pass. |
| Overlay | The prototype copied onto a scratch copy of the repository, where the suite runs. |
| Retirer | An agent that retires the older tests a unit makes false. |
| Developer | An agent that writes the real code. It may not read the tests. |
| Interface note | What a developer gets in place of the tests: the names and the behavior to build. |
| Two-Key | The independent grade of one unit, PASS or FAIL, from the grader's own test runs. |
| Receipt | The saved output of a run that proves a claim. |
| Hostile input | A value chosen to break a rule: empty, a wrong type, a wrong case, an escape. |
| Reading | A choice Claude makes where the signed text leaves room. Each is listed in the PR body. |
| Red mark | USAGE's sign for text that is described and not shipped yet. |
| `progress` | The command that records each task's start, its test runs and its end. |
| Wrap | The session's closing PR: `STATE.md`, the memory index and the metrics row. |
| Touch | One reply Claude needs from the user before the PR review. |
| Agent tokens | The measure of the agents' work, and so of its cost. |
