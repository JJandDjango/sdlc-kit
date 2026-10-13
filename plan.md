# Plan - Session 97 (2026-10-12) - g1-requirements-spec s5, first of two sessions

```
Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     G1, the requirements gate: a feature's failure points are found before its development starts.
Feature  g1-requirements-spec: the kit computes G1 and refuses a task until G1 passes.
Unit     s5-start, the fifth of six: intake's report names G1 as the next step, and no task starts or closes before G1 passes.
```

The pages above this plan: the feature page
(`docs/features/g1-requirements-spec.md`), the design page
(`docs/features/g1-requirements-spec.design.md`, "The refusal" and
"Intake's report") and the contract
(`specs/g1-requirements-spec/contract.yaml`, unit `s5-start`).

## 1. The deliverable

By this session's end the test list of unit `s5-start` stands recorded,
proven red on main's code and green on a throwaway prototype, with a
handoff file for the session that builds it. No code of the unit is
written here.

## 2. Where this sits

Four units of six stand on main. The kit can already lint a feature's
schemas (G1.1), run its model checker (G1.2), record a person's review
(G1.3) and show all three in the tree (the kit's printed outline of the
work). Nothing yet acts on that reading: a task can be recorded as
started with G1 failed. This unit adds the enforcement, in two halves.

- The code half. `progress` is the command that records a task as
  `doing`, `done` or `blocked`. `progress start` on a task, and
  `progress done` on a task, a unit or a contract, refuse while the
  feature's G1 is an active gate and does not read `done`. The call
  prints `{unit} cannot start: G1 has not passed for {feature}` on
  standard error, exits 2 and writes nothing. `block` and `run` stay
  open. An exempt feature is never refused.
- The prompt half. Intake is the flow that turns a signed feature
  document into a contract, and I9 is its last step, the report. For a
  ready contract whose feature needs G1 the report ends
  `Next step: G1. Run /sdlc g1 {id}.` Otherwise it ends as today.

The user ruled on 2026-10-12 (session 96) that a build is two sessions,
split at the test list. This is the first.

## 3. The steps

1. This plan, committed and pushed on branch `session-97-g1-s5-start`.
2. Two drafter agents side by side
   (`.claude/workflows/spec-channel-drafter.js`: a drafter writes a
   unit's tests, proves them red, and proves on a scratch prototype
   that code can satisfy them). One drafts the code half against a
   scratch copy of the `taskcontract` package. The other drafts the
   prompt half against a scratch copy of `skills/`. Each gets its brief
   as a file.
3. Both prototypes go onto one scratch worktree, and the session runs
   the whole suite there once. An older test that fails is read: either
   the draft is wrong, or the test pins a sentence this unit rewords.
4. The trial of hostile inputs on the code prototype, from a scratch
   `trial.py` kept in the receipt folder: the refusal against a
   repository whose G1 sources cannot be read, an exempt feature, a
   feature before intake, each kind of id, and the print through a pipe.
5. The session checks each fixed detail of both lists against the
   contract, the design's Decisions and the ratified terms, then
   records each list as approved by Claude in the progress record.
6. The handoff file, in
   `RECEIPT_g1-requirements-spec-s5_2026-10-12/HANDOFF.md`: both
   interface notes as files, both test files, the readings, the
   retirements, and the second session's steps.
7. The user's `/usage` reading, and the session ends. `plan.md` stays on
   the branch for the second session, which removes it before the PR.

The second session, from the handoff file: two developers, the two
reworded sentences, the suite, the commit, a live intake run as the
manual receipt, Two-Key (the independent grade), the PR, the wrap.

## 4. Where Claude stops for the user

Once: at this session's end, for the `/usage` reading. Before it, only
on a case the three pages leave open that their purpose cannot settle,
or one whose answer would change a signed sentence, a ratified term or
an ADR.

## 5. Where Claude goes on alone, and by what rule

Alone: everything in section 3. The rule: where the pages name no case,
Claude rules from their purpose, builds on that reading, and lists it at
the top of the PR body. The test for any case in this unit: the refusal
and the tree may never disagree. A task is refused exactly where the
tree prints that feature's G1 active and not `done`.

## 6. Rulings needed

None. The readings so far, each for the PR body and for the design's
next text row:

1. The refusal takes G1's status from the tree's own build, the one
   reading the print and the pane use, so it reads no G1 file itself.
   The design says so in one clause ("the refusal reads the tree's G1
   verdict").
2. The refusal stands after the checks of the id and of its kind, and
   before the checks of the options. An unknown id and a wrong kind
   keep their own lines, which older tests pin; a caller with a valid
   id learns of G1 first.
3. `{unit}` is the unit's own id, as the design's example prints
   `u1-rate` for the task `apply-discount/u1-rate/approve-tests`. For a
   contract's close it is the feature's id, as signed.
4. The words `cannot start` print on a refused `done` too. The message
   is signed word for word.
5. Where the tree cannot read G1 and prints each condition `to do`
   (session 95's guard), the refusal holds: nothing is proven, so
   nothing starts.
6. Where `.sdlc/config.yaml` cannot be read, the tree reads no gate
   active, so nothing is refused. This is a way past the refusal by a
   broken file, and it is older than this unit. Listed as an open edge;
   not built here.
7. I9 learns whether the feature needs G1 from the kit's own reading
   (the tree's `{id}/G1` line), never from its own read of the config,
   so the report and the refusal cannot disagree.

## 7. What could go wrong, already ruled

- A drafter returns a question: it is tested against each sentence of
  `done_means` and against section 5's rule. Only a case that fails
  both goes to the user.
- An older test fails on the prototype for a reason other than a
  reworded sentence: the draft is wrong and is amended, with red and
  green proven again.
- A drafter fixes a detail the pages do not give (a printed word, an
  order): it is checked against the contract, the design's Decisions
  and `specs/vocabulary/`, and against five hostile inputs where it
  sorts free text.
- The session's context nears 40% before both lists are recorded: the
  session ends at the last recorded state, and the handoff file says
  where.
- A session left overnight is not resumed: a new one starts from the
  handoff file.

## 8. This session's cost, with its basis

About 360K agent tokens here, and about 0.8 million for the unit. The
basis is session 92's `s3-review`, the last unit with a code half and a
prompt half: drafters 232K and 129K, developers 114K and 80K, Two-Key
226K, 781K in all, PASS in round 1. A lost Two-Key round adds about
300K. The session runs at `high` in place of `xhigh`, as a trial, and
`.claude/workflows/tools/session_cost.py` measures both sessions at the
wrap against session 92's row (183 requests, 61,137K tokens read, 101K
thinking). The user's `/usage` readings stand in the receipt folder's
`USAGE-readings.md`; the start reads 1% of the session and 16% of the
week.

## 9. Not in this session

- The unit's code, its commit, Two-Key, the PR and the wrap: the second
  session.
- Unit `s6-release`.
- Session 90's first ruling (one G1.1 record a call) and the fix of
  G1.1's escaped defect, in their own session before `s6-release`.
- Reading 6's edge, and the older ways a hand-written file stops a
  command (`STATE.md`, Open questions).
- `g1.py`'s `Ready:` row reader and `tree.drift`'s, still two.

## 10. Words

- Active gate: a gate the repository's config lists, for a feature not
  exempt from it.
- Exempt: named in the config's `g1.exempt` list, so G1 never applies.
- Handoff file: the page one session leaves so the next starts with no
  memory of it.
- Interface note: a drafter's account of what its tests assume, written
  for a developer who never reads the tests.
- Prototype: throwaway code that proves a test list can be met.
- Reading: Claude's ruling on a case the pages never name, listed for
  the PR reviewer.
- Receipt: a command's saved output, kept as proof of a claim.
- Red, green: a test run that fails as expected before the code exists,
  and passes once it does.
- Two-Key: a second agent runs the unit's receipts and grades it
  against the contract with no trust in the builder.
