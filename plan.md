# Plan - Session 92 (2026-10-11) - g1-requirements-spec s3

```
Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     G1, the requirements gate: a feature's failure points are found before its development starts.
Feature  g1-requirements-spec: the kit computes G1 and refuses a task until G1 passes.
Unit     s3-review, the third of six: a named person signs a review of 11 items, at a flow the kit runs.
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

By the session's end unit `s3-review` stands on main through one PR,
with a passing independent grade.

## 2. Where this sits

A gate is a pass/fail checkpoint between two phases of the work. G1 is
the kit's second gate, and it holds three conditions (a condition is
one named part of a gate). The feature is built as six units, one a
session, and ships as kit 0.20.0. A unit is one slice of a feature,
built and graded by itself.

| Unit | What it adds | State |
|---|---|---|
| `s1-lint` | G1.1: a linter reads each boundary schema clean. Also the base: the record file and both commands | on main (PR #106) |
| `s2-model` | G1.2: a checker passes the model of each hard core | on main (PR #109) |
| `s3-review` | G1.3: a named person signs a review of 11 items. Also `/sdlc g1`, the flow where a person runs G1 | this session |
| `s4-tree` | the tree, the kit's printout of every feature's state, shows G1 | to do |
| `s5-start` | no task starts before G1 passes | to do |
| `s6-release` | the release, and G1 turned on in the kit's own repository | to do |

What this unit adds:

- `python -m taskcontract g1-record review <id>`, with the flags
  `--by`, `--seat`, `--checked` and `--unchecked`. It appends one
  review record to `.sdlc/g1/<id>.yaml`, the committed file that holds
  a feature's G1 results. The record holds the signer's name, the seat
  (the position the signer answers from, such as `po`), the date, the
  revisions reviewed and each item's answer.
- G1.3's one rule, `RS301`, in `g1-check`, the command that prints G1's
  verdict. Its message: `G1.3: item {n} {item} is unchecked in
  {section}`. G1.3 reads `done` only when the last review checks all 11
  items on the revisions the contract was derived from.
- `taskcontract/data/g1-items.yaml`: the 11 items, each a number and a
  name, held equal by a test to the ratified list at
  `docs/gates/G1-requirements-spec.md:128`.
- `skills/sdlc/flows/g1.md`: the venue, `/sdlc g1 <id>`. It is a prompt
  file that leads a person through seven steps, R1 to R7. With it come
  four additions to `skills/sdlc/SKILL.md`: the dispatch line, the flow
  list, one constraint and one criterion.

The design page fixes each of these: Interfaces (line 73), the record's
drawing (line 220), Sources (line 307), Constraints (line 327) and the
unit's row (line 351). The unit's done-means sentence, the one sentence
it must make true: "A seat reads G1.3's 11 items at the venue, and G1.3
reads done only from a review with a signature." Its checks, the
contract's testable lines, are SC1.1, SC1.2 and SC1.3
(`contract.yaml:97-119`). No older test retires.

Measured at this resume, on main at `c411702`:

- G1.3 always reads `to do` today (`taskcontract/g1.py:512`), and
  `taskcontract/data/gates.yaml:34` already lists `RS301` under it.
- `skills/sdlc/flows/g1.md` does not exist. `skills/sdlc/SKILL.md`
  holds 8,576 of the 12,000 characters a prompt file may hold.
- USAGE (`USAGE.md`, the user guide) holds this unit's text since
  `s1-lint`, under red marks that mean "described, not shipped"
  (`USAGE.md:531`; step R5 at line 793). The marks stay red until
  `s6-release`.
- The kit's own list of seats holds one value, `user`
  (`specs/vocabulary/intake-seat.yaml:18`). The code that reads the
  list stands at `taskcontract/vocabulary.py:317`.
- Not run at this resume: the whole suite. It read 1216 passed at
  session 90's close (`STATE.md`).

## 3. The steps

The unit has a code half (`taskcontract/`) and a prompt half
(`skills/sdlc/`). Each agent works on one half, so each reads little.

1. **Open (Claude).** Branch `session-92-g1-s3-review` from `c411702`.
   This plan is committed and pushed, and the build starts. The plan
   takes no approval (section 4).
2. **Draft (two drafters, side by side).** A drafter is an agent that
   writes a unit's tests before any code, proves each one fails today,
   and proves on a throwaway prototype that they can pass
   (`.claude/workflows/spec-channel-drafter.js`). One drafts the code
   half: SC1.1 and SC1.2, on a scratch copy of the `taskcontract`
   package. One drafts the prompt half: text tests on the flow and on
   `SKILL.md`, and SC1.3, on a scratch copy of `skills/`.
3. **Overlay (Claude).** Both prototypes are copied onto a scratch copy
   of the repository, and the whole suite runs there once. The retirer,
   an agent that retires the older tests a unit makes false
   (`.claude/workflows/test-retirer.js`), runs only if an older test
   fails.
4. **Check the lists (Claude).** Each fixed detail is read against the
   contract, both pages, the design's Constraints and Decisions, the
   ratified terms under `specs/vocabulary/` and USAGE's red text. Each
   rule that sorts free text (the item numbers, the section, the
   signer's name, the seat) is tried against five hostile inputs on the
   prototype.
5. **Approve the test list (Claude).** The approval is recorded `--by
   claude`. The lists, each rule's table and what step 4 found are
   saved in the receipt folder and summed up at the top of the PR body.
   Then `progress`, the command that records each task, records each
   check's failing run.
6. **Green (two developers, side by side).** A developer is an agent
   that writes the real code from an interface note, a page of names
   and behavior, and never opens the tests
   (`.claude/workflows/unit-developer.js`). One writes the code half,
   one the prompt half. Claude then runs the whole suite, and runs the
   form validator (`python -m prompt_lang`, from a scratch environment)
   on each prompt file.
7. **Commit (Claude).** The unit's commit. Each check reads green at
   the clean commit, and the kit's own contract and scope checks read
   green.
8. **Manual receipt (Claude, with a seat agent).** A live run of
   `/sdlc g1` on an invented feature, in a small repository a script
   builds outside the kit. A second Claude session runs the flow from
   the unit's commit, with no window, and an agent answers as the
   person (`.claude/workflows/live-run-seats.js`). The text is saved in
   untracked `RECEIPT_g1-requirements-spec-s3_2026-10-11/`.
9. **Two-Key.** An agent that grades the unit from its own test runs
   and returns PASS or FAIL
   (`.claude/workflows/two-key-unit-verifier.js`). It reads the
   receipt's text. On PASS the unit is recorded done.
10. **The work's close.** The push, then the PR once CI reads green and
    Two-Key reads PASS, with Claude's readings at the top of its body.
    The user reviews it and says merge.
11. **The wrap, after the merge (Claude).** `STATE.md` rewritten, this
    plan struck, the memory index updated and one row appended to
    `docs/session-metrics.md`, in a PR of their own that Claude merges
    after green CI.

The session boundary, if context runs short: after step 5. The approved
lists, the prototypes and the interface notes are copied to the receipt
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
the test list's approval and each change to it, the unit's commit, the
USAGE sentences, the live run, opening the PR, and the wrap's merge.

The rule: where the pages name no case, Claude rules from their
purpose, builds on that reading, and lists it at the top of the PR
body, where the user can overturn it. If the reading would change
signed text, Claude stops.

For an event this plan never names, ask what the unit is for: can G1.3
read `done` without a named person's signature over all 11 items, on
the revisions the contract was derived from? If the event opens such a
path, it is a defect, and it is fixed before the commit. A question or
a shortcut a developer returns is put to the same test.

## 6. Rulings needed

None: this plan takes no approval. The four cases below are ones the
design never names. Claude settles each from the pages' purpose, a
review that binds a named person to named text, and lists it at the top
of the PR body. Each is also a gap to close when the design is next
amended.

1. **Several unchecked items.** The design draws one, `--unchecked
   6=Statement`. A real section name holds a comma ("Error messages,
   verbatim", `docs/features/g1-requirements-spec.md:224`), so a list
   split at commas would cut it in two. The reading: `--unchecked` is
   given once for each unchecked item, and `--checked` stays one list
   of numbers. The design's drawing reads the same either way. USAGE
   gains one red sentence.
2. **An empty section or name.** The design checks no section against
   the document (its Risks, 10), and the message prints the section on
   one line. The reading: the command refuses a section or a signer's
   name that is empty or holds a line break. It exits 2 and writes
   nothing. Any other text is kept as the person wrote it, with the
   spaces at its ends cut.
3. **A feature with no revision to name.** A review names the revisions
   the contract was derived from, and the kit reads them from each
   document's `Ready:` row, the row intake writes when it derives the
   contract. Two cases have none: a feature with no feature document,
   and a document with no `Ready:` row. The reading: `g1-record review`
   refuses both, exits 2 and writes nothing, and G1.3 reads `to do`. A
   review tied to no text proves nothing, and session 90 ruled the same
   side for G1.2 after a defect escaped. The cost: a feature taken in
   with no feature document cannot pass G1 until it holds one. The
   pilot's one feature holds a document with a `Ready:` row (read
   today).
4. **Who answers in the live run.** The contract says no agent signs a
   G1.3 review, and step 8's receipt needs a seat that answers the 11
   items. The reading: an agent plays an invented person in the
   throwaway repository, as the interview's live runs did. Its record
   never enters the kit, and the receipt says an agent sat the seat.
   Two short runs: one checks all 11 and ends on `g1-green`; one leaves
   item 6 unchecked and ends on the `RS301` line.

Three smaller readings:

- R5 asks each item "in the item's own words", and `g1-items.yaml`
  holds only a number and a name. The flow file holds the 11 items word
  for word, and a test holds that copy equal to G1's page.
- A contract that cannot be read, or that holds no `scope`, is refused
  by `review`, as `model` refuses it.
- The refusals of rulings 2 and 3 print lines whose words no signed
  text gives, as `s1-lint`'s and `s2-model`'s did. Each is listed at
  the top of the PR body.

## 7. What could go wrong, already ruled

- **Two-Key fails a round.** One narrow fix round: the tests are placed
  first, tried against the same hostile inputs, and the developer's
  note names only the behavior to change. Round 2 names round 1's
  defects and asks for other paths of the same kind. After a third
  failure Claude stops.
- **An older test fails on the overlay.** The unit retires none, so it
  is a finding. If the test pins what this unit must change, it is
  amended and named at the top of the PR body; else the build is wrong.
- **A drafter says which way a rule errs.** The claim is tried with
  hostile inputs before the list is shown. Session 90 lost a round to
  an untried one.
- **A prompt file fails the form validator or passes 12,000
  characters.** Its developer fixes it before the commit. The flow file
  starts empty, and `SKILL.md` has 3,424 characters free.
- **The flow signs with no person's word.** In the live run, a flow
  that runs `g1-record review` before the seat gives a name and says to
  sign is a defect: a fix commit, and the receipt is taken again.
- **The record file cannot be read.** It counts as absent (the design,
  line 183), and `review` refuses to append to it, as `lint` and
  `model` do.
- **An agent passes about 400K tokens.** It is stopped and its work
  split. The two halves keep each agent's reading narrow.
- **A defect of a unit already on main shows.** Claude confirms it with
  a live run and names it at the top of the PR body, and the metrics
  row of the session that shipped it takes it. It is fixed here only if
  this unit cannot stand without the fix; else it joins section 9.
  Claude stops only if the fix needs a decision.

## 8. This session's cost, with its basis

About 0.9 million agent tokens, in a range of 0.7 to 1.05 million. The
basis is the two recorded units that held a code half and a prompt
half, counted without their retirer, amendment and third developer
rounds: session 71's at 697K (drafters 147K and 166K, developers 62K
and 59K, Two-Key 263K) and session 70's at 1,032K (drafters 222K and
255K, developers 108K and 113K, Two-Key 334K).

- A lost Two-Key round adds about 300K (session 90's cost 325K).
- A retirer round adds 62K to 159K.
- The live run's seat agents stand outside the total, as the metrics
  page counts them: about 65K a run at most, on session 80's 66K and
  63K for runs of 41 and 36 turns. These runs are shorter, about 15
  turns each (an estimate).

Touches, the replies Claude needs from the user before the PR review:
none planned. The target is 0.

## 9. Not in this session

- `s4-tree`, `s5-start` and `s6-release`. So the tree does not print
  the review yet, and no task is refused yet.
- Session 90's first ruling (one G1.1 record that holds a result for
  each `g1.schemas` entry) and the fix of G1.1's escaped defect, in a
  session of their own before `s6-release`.
- Checking that a named section exists in the document (the design's
  Risks, 10).
- The open edges of G1.1 and G1.2, under `STATE.md`'s Open questions.
- The kit's own G1 declarations and its `g1.exempt` list: `s6-release`.
- A live run of `buf` and of P, the two tools never run here.
- The feature and design pages in the shapes of
  `NOTES_document-theory_2026-10-10.md`: a feature of its own.
- The pilot (`E:\ImSimProject\engine`), until G1 ships.
- The `google_workspace` server, which failed to connect again at this
  resume.

## 10. Words

| Word | Meaning |
|---|---|
| Unit | One slice of a feature, built and graded by itself. |
| Done means | The one sentence a unit must make true. |
| Check | One testable line of the contract, with an id such as SC1.1. |
| Suite | Every test in the kit, run together. |
| Drafter | An agent that writes a unit's tests first and proves they fail today. |
| Prototype | The drafter's throwaway code or text. It proves the tests can pass. |
| Overlay | The prototype copied onto a scratch copy of the repository, where the suite runs. |
| Retirer | An agent that retires the older tests a unit makes false. |
| Developer | An agent that writes the real code or prompt text. It may not read the tests. |
| Interface note | What a developer gets in place of the tests: the names and the behavior to build. |
| Two-Key | The independent grade of one unit, PASS or FAIL, from the grader's own test runs. |
| Receipt | The saved output of a run that proves a claim. A manual receipt comes from a live run. |
| Live run | A second Claude session that runs the real flow, turn by turn, in a throwaway repository. |
| Seat agent | An agent that answers a live run as the person would. |
| Hostile input | A value chosen to break a rule: empty, a line break, a comma, a repeat, a wrong case. |
| Form validator | `python -m prompt_lang`, which checks a prompt file's form. |
| Reading | A choice Claude makes where the signed text leaves room. Each is listed in the PR body. |
| Red mark | USAGE's sign for text that is described and not shipped yet. |
| `progress` | The command that records each task's start, its test runs and its end. |
| Wrap | The session's closing PR: `STATE.md`, this plan, the memory index and the metrics row. |
| Touch | One reply Claude needs from the user before the PR review. |
| Agent tokens | The measure of the agents' work, and so of its cost. |
