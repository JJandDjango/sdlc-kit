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
4. [x] Build `prove.py`, the drafter's copy, red, green and mutation loop, a
   script that prints only the minimum an agent needs (a standing practice, the
   user, session 103). Built in session 105 on the branch `session-105-prove-py`
   against ten signed items (`docs/conventions/prove-py.md`), with an 18-test
   self-test; it lives in the untracked `.claude/workflows/tools/`; the PR waits
   for the user's review.
5. [x] Build `receipts.py`, Two-Key's receipts, run by the session with no
   agent, printing only the minimum an agent needs. Built in session 106 on the
   branch `session-106-receipts-py` against ten signed items
   (`docs/conventions/receipts-py.md`), with a 24-test self-test; it lives in
   the untracked `.claude/workflows/tools/`, and `two-key-unit-verifier.js`
   takes its JSON as `receiptsResult`; the PR waits for the user's review.
6. [x] Write small-session-flow's two documents. The requirements are signed at
   r5 (session 109, branch `session-109-flow-feature-doc`, PR #130), the design
   at r5 (session 110, branch `session-110-flow-design-doc`, stacked on it).
7. [x] Run `/sdlc intake docs/features/small-session-flow.md`: intake closes the
   design node and derives `specs/small-session-flow/contract.yaml`. Session
   111 on the branch `session-111-flow-intake`: the first read parked the pair
   on ready check 12, the design was signed again at r13 (r14), five terms and
   15 dictionary words were ratified, and the contract validates ready-green;
   the PR waits for the user's review.
8. [x] Use `prove.py` and `receipts.py` on the next unit's build, `w1-session-size`
   (small-session-flow's first unit), then compare the
   drafter with `s6-release`'s 299K tokens and 124 calls and the receipts with
   the agent's 54K-token start. Turn both pages' 🟡 marks 🟢 on that run, then
   delete the receipts agent's path in `two-key-unit-verifier.js` (item 9
   kept it until a real round used the script). Sessions 112 and 113 on the
   branch `session-112-w1-session-size`: the drafter took 129K tokens and 32
   calls; `receipts.py` ran the whole suite once in the background (2017
   passed, 453 s) with no agent, so Two-Key's grader ran alone at 96K and
   passed in round 1. Both pages read 🟢, the agent's path is gone, and the
   PR waits for the user's review.
9. [x] Build `w4-session-notes`, small-session-flow's second unit in build
   order: the close rule in `CONTRIBUTING.md` puts the next deliverable
   first in this list, and the next session's first `/cairn status` names
   it. Session 114 on the branch `session-114-w4-session-notes`: the line
   at `354ae76`, this item's tick as the rule's first close, and both
   receipts in `RECEIPT_small-session-flow-w4_2026-10-22/`; Two-Key PASS
   in round 1, and the PR waits for the user's review.
10. [x] Build `w2-workflow-file`, small-session-flow's third unit in build
    order: `.sdlc/workflow.md` holds one four-node flowchart, with a named
    file on each edge and one settings row per node, and the reader
    refuses a node whose row lacks an agent model or an effort. The
    session's first `/cairn status` is w4's second SC4.2 receipt: save it
    to w4's receipt folder. Session 115 on the branch
    `session-115-w2-workflow-file`, in one session: tests red at
    `292e2ce`, unit at `b2c68df` (the file and `taskcontract/workflow.py`);
    the drafter took 106K tokens, the developer 70K, Two-Key's grader 94K;
    PASS in round 1, and the PR waits for the user's review. The SC4.2
    receipt is `sc4_2-second-status.txt` in w4's folder.
11. [x] Build `w3-node-start`, small-session-flow's fourth and last unit:
    `python -m taskcontract node <id>` starts `claude` at the row's agent
    model and effort, read through w2's `settings()`, and the workflow
    scripts take both as arguments. Session 116 on the branch
    `session-116-w3-node-start`, in one session: tests red at `b4f1436`,
    unit at `95308e7`; the user ruled the missing-file line at the start
    (`Node {id} did not start: no workflow file at .sdlc/workflow.md.`).
    The four workflow scripts (untracked) now take `model` and `effort`,
    and the session passes the execution row's (`sonnet`, `high`); the
    receipts are in `RECEIPT_small-session-flow-w3_2026-10-23/`. Two-Key
    PASS in round 1, and the PR waits for the user's review.
12. [x] Describe `node` in `USAGE.md` and `docs/components.md`: the design's
    Scope names both, and no unit's done means carried them (w3's Two-Key
    advisory). Two gaps go with it to the design's next text row: the
    missing-file line, and `node` ending in a traceback when the path
    `shutil.which` found cannot be run (an `OSError` from `Popen`).
    Session 117 on the branch `session-117-node-usage`: a subsection at
    the end of USAGE section 4 and a "workflow nodes" row, each quoted
    line checked against `node`'s live output; no Two-Key round, since no
    code changed; both gaps stand in Open questions, and the PR waits for
    the user's review.
13. [x] Trim what sessions load (the user, session 117). Cut each
    `MEMORY.md` entry to its one-line hook: the index loads every
    session, about 4.5K tokens. Split `USAGE.md` (2,193 lines, about 27K
    tokens) into a short index plus one page per feature under `docs/`,
    so a reader loads only the feature at hand, as the gate pages do.
    The backlog stays as it is: a session searches it, never reads it
    whole. Session 118 on the branch `session-118-usage-split`:
    `MEMORY.md` went from 17.6K to 9.6K characters, all 66 entries kept;
    `USAGE.md` is a 42-line index of 14 pages under `docs/usage/`, cut
    whole at sections and subsections, and the tests read the index and
    its pages joined (`tests/conftest.py`'s `usage_text`). Left out:
    "§N" references as links, and a page for each task in `tasks.yaml`.
    The PR waits for the user's review.
14. [x] Make the whole suite faster: it runs 2085 tests one at a time in
    about 460 s, most of Two-Key's time and every build's. Measure with
    `--durations=25` first, then try `pytest-xdist` (not installed) in a
    scratch worktree, then adopt it in `receipts.py` if the suite stays
    green (the user's question, session 116). Session 119 on the branch
    `session-119-faster-suite`: serial, 453 s, the slowest test 12.1 s,
    and at `-n auto` 64 s, both under the session's Python 3.13; in a
    scratch worktree on 3.14, three runs at `-n auto` passed all 2085 in
    62 to 69 s and one at `-n 4` (CI's worker count) in 148 s. The setup
    line, standing practice, the receipts example and the three agent
    briefs run `-n auto`; a one-file run stays serial. Left out: CI on
    workers, since `ci.yml` sits in no contract's scope and
    `pyproject.toml` not in `small-session-flow`'s, so `scope-check`
    fails them under it (the user's ruling: a contract home or a scope
    line); speeding up the slowest tests; `prove.py`. The PR waits for
    the user's review.
15. [x] Run CI's suite on workers (Next 14's Left out). The design's r16
    put `.github/workflows/ci.yml` and `pyproject.toml` in Scope, r19
    signed it, and session 120's intake brought both into the contract
    (`bc8f9b2`). CI's test job runs `pytest -q -n auto`, and the `test`
    extra gains `pytest-xdist>=3`. Session 120 on the branch
    `session-119-ci-workers`: CI's pytest step went from 199 s serial
    (main's run at `1c5a102`) to 100 s on 4 workers, and the test job
    from 3m30s to 1m58s; locally 2085 passed in 68.5 s at `-n auto`.
    `test_pane.py`'s exact `test` extra list gained the same pin. The PR
    waits for the user's review.
16. [x] Write execution-team's design document:
    `/sdlc:product-specification-interview execution-team design`, the
    user as engineer seat. The user's priority (session 121): the
    execution team in place for the engine's M0 work first, then G1's
    open edges (Open questions). The requirements document
    (`docs/features/execution-team.md`, "Standard Development Workflow")
    is signed at r3 (r4), 0 OPEN, 49 language findings for intake's
    door. Session 121 on the branch `session-121-execution-team`. For
    the design: how QA gets an existing function's signature without its
    body (C++ headers split them, a Python file does not); where a
    consumer declares its test command; the five workflows and
    `prove.py` and `receipts.py` call pytest today. Session 122 on the
    same branch: `docs/features/execution-team.design.md` signed at r4
    (r5), against requirements r3; 16 language findings (CL006 16) for
    intake's door. Answers: `.sdlc/config.yaml` gains `test:` and
    `wall:`; QA reads `.h` files or `python -m taskcontract interface`;
    a plugin hook holds the wall; QA writes no prototype, and the QA
    verifier's mutations run at two-key. Six units, e1 to e6; e6 ships
    kit 0.21.0. One OPEN: whether a workflow's agent fires the session's
    hooks, which the probe that opens e3 answers.
17. [x] Intake execution-team: `/sdlc intake docs/features/execution-team.md`,
    the pair signed (requirements r3, design r4). Intake ratifies seven
    new terms and the `operator` amendment, and takes the 65 language
    findings (49 and 16) at its door. Then build e1 to e6 in order.
    Session 123 on the same branch: the first run parked the pair
    (requirements r5, design r6) on the design's OPEN mark and four
    outputs with no drawing, and e5's five checks had no `+` pair. A
    one-agent workflow probe answered the OPEN: a session's PreToolUse
    hook refused the agent's piped Bash call
    (`RECEIPT_execution-team-design_2026-10-25/hook_probe.md`). The design
    run drew the outputs, paired e5's checks, added `task.py`'s rounds
    file and its `taskcontract progress` calls (r7, r9), then four Scope
    paths (r13); signed at r15 (r16). Seven terms ratified, `operator`
    amended, 14 dictionary words (`fd8a70f`). Contract ready-green
    (`7b92e64`; Ready rows r6 and r17); G1 passed, the review signed with
    11 items checked. The PR waits for the user's review.
18. [x] Build `e1-declaration`, the first execution-team unit, once PR #142
    merges: a repository declares `test:` and `wall:` in
    `.sdlc/config.yaml`, the kit declares its own, and `task.py start`
    with no `test.command` prints SC2.3's message. Session 124 on the
    branch `session-124-e1-declaration`, in one session: the usage page
    `docs/usage/the-team.md` written red at `59e875d`, tests red at
    `951ab4a`, unit at `2741265` (`taskcontract/declaration.py`,
    `workflows/tools/task.py start`). `test_g1_release.py`'s red-mark
    count, which pinned 0.20.0's state, leaves out the team's page
    (`bfa860e`). Two-Key PASS in round 3: rounds 1 and 2 failed on one
    docstring's dependency claim (fixes `c609110`, `f6fcdc5`). The PR
    waits for the user's review.
19. [x] Build `e2-scripts`, the second execution-team unit, once e1's PR
    merges: `prove.py` and `receipts.py` move to `workflows/tools/` with
    their tests, and run the declared test command through e1's
    `read_test`, pytest only where it is declared, with no prototype.
    Session 125 on the branch `session-125-e2-scripts`, in one session:
    the move at `362de21`, tests red at `82d4484`
    (`tests/test_declared_command.py`), `test_prove.py`'s seven
    retirements and eleven amendments at `a030f55`, unit at `c91634b`,
    docs at `7835e42`. Two-Key PASS in round 1. The PR waits for the
    user's review.
20. [x] Build `e3-wall`, the third execution-team unit: `python -m
    taskcontract interface` prints a Python file's signatures without
    bodies, and a PreToolUse hook in the plugin refuses each tool call
    across the wall while a task runs. Session 126 on the branch
    `session-126-e3-wall`, stacked on e2's branch while PR #144 is open,
    in one session. The probe came first: a plugin's PreToolUse hook
    refuses a workflow agent's call by exit 2
    (`RECEIPT_execution-team-e3_2026-10-27/hook_probe.md`). Tests red at
    `a62fdbb` (`tests/test_wall.py`), unit at `618a356` (`hooks/wall.py`,
    `taskcontract/interface.py`, `read_wall`), docs at `c77ccdb`. Two-Key
    PASS in round 1. The PR waits for the user's review.
21. [x] Build `e4-team`, the fourth execution-team unit: the team ships
    in the plugin's `workflows/` folder, one workflow per member, started
    by `/sdlc execute` (`skills/sdlc/flows/execute.md`) as
    `{plugin}:{operator}` at the execution row's settings. Sessions 127
    and 128 on `session-127-e4-team`, split at the test list. Tests red
    at `7f3bc40`, unit `23ca13f`, docs and ADR 0040 `b6e04c8`. The
    manual receipt (`RECEIPT_execution-team-e4_2026-10-27/team_start.md`)
    ran every task at Haiku in a scratch consumer and found the
    Developer running its walled test file: fixed at `0433749` (tests)
    and `551066b`. Two-Key PASS in round 1. The untracked copies moved
    to the receipt folder's `retired/`.
22. [x] Build `e5-rounds`, the fifth execution-team unit: `task.py end`,
    `fail` and `stop`, the rounds file and the draft PR. Session 129 on
    `session-129-e5-rounds`, the first unit the shipped team built:
    `/kit-e5:sdlc execute` in a headless Sonnet session, the plugin from
    a worktree of main, so the run used e4's one-round flow and the
    session resumed it for each round. Before the run, `60c52b7` (the
    kit's test command names no walled folder, Next actions 13) and
    `a697403` (e4's one-round pins retired). Unit `0e90241`, rounds
    `1505170`, `dfa091a` and `d90e938`. The QA channel took four rounds,
    the fourth on the user's waiver of the cap; green took three. Two-Key
    PASS on `d90e938`. QA's tests ruled Next actions 12.
23. [x] Build `e6-batch-run`, the release unit: one unit from write-tests to
    two-key in a batch-file fixture repository, ending green, on e5's
    flow, and kit 0.21.0. Session 131 on `session-131-e6-batch-run`: the
    fixture `tests/fixtures/batch-repo/` at `2839daf` (`test.command:
    [test.bat]`), its PATH fix `acf7d29`, the release `5f3dad8`. The
    receipt (`RECEIPT_execution-team-e6_2026-10-28/batch_run.md`): run 1
    stopped when GNU `find` walked the C: drive; run 2 ran every task in
    round 1, both verifiers PASS, 8 of 8 mutations caught. Two-Key PASS
    in round 3: round 1 failed on five stale statements, three from the
    release sweep (fixed `ad4b076`), round 2 on `receipts.py`'s
    docstring (`1dfec56`). Merged as PR #148 at `0fa7441`, and tagged
    `v0.21.0` there on the user's word (session 132).
25. [x] After the user merges and tags `v0.21.0`: the self-pin PR, moving
    `.github/workflows/sdlc.yml:20` and
    `docs/usage/restricted-environments.md:40` to `v0.21.0`, as PR #125
    did for 0.20.0. Then tell the engine its pull is ready, with the
    PATH rule of Next actions 15. Session 132 on `session-132-self-pin`:
    the `uv` line, run against the tag with `python -P`, installs
    `sdlc-taskcontract 0.21.0` and reads `specs/execution-team` ready-green;
    the suite passes (2545). The engine's note went to the user that
    session, to carry to the engine's own session.
26. [x] Fix the team's defects in Next actions 13 to 15 (the user,
    session 133), as kit 0.21.1. Session 133 on `session-133-team-fixes`:
    a headless probe showed the session's own call reaches a plugin hook
    with no `agent_id` and a member's with one
    (`RECEIPT_execution-team-fixes_2026-10-28/hook_probe.md`). e3-wall
    `a4d5e44` and `548150f` (Two-Key PASS in round 2), e5-rounds with
    e4-team `b7beb4c` (PASS in round 1), their wording `be14743`, the
    release `255892d`, `b28ecdf`, `ee0fd67` and `99ea0a7` (PASS in round
    2, with the sweep). execution-team's units and contract are closed in
    this machine's `.sdlc/progress/`, which git ignores. Merged as PR
    #150 at `ac0f228`, and tagged `v0.21.1` there on the user's word.
27. [x] After the user merges and tags `v0.21.1`: the self-pin PR, moving
    `.github/workflows/sdlc.yml:20` and
    `docs/usage/restricted-environments.md:40` to `v0.21.1`, as Next 25
    did for 0.21.0. Then tell the engine its pull is ready: the wall now
    passes its declared command and the Orchestrator's own calls.
    Session 134 on `session-134-self-pin`: the `uv` line, run against
    the tag with `python -P`, installs `sdlc-taskcontract 0.21.1` and
    reads `specs/execution-team` ready-green; the suite passes (2594).
    `ARCHITECTURE.md` drops to Cairn's 3072-byte budget (#150's
    `workflows/` row put it at 3100). The engine's note went to the user
    that session, to carry to the engine's own session.
24. Restart a stopped run in a fresh session (the user, session 130).
    `task.py stop` and a third failed round remove the task file and the
    rounds file, so a stopped run keeps no state; session 129 went on by
    `--resume`, and the headless session's starting context grew from 45K
    to 281K tokens over eight runs (31.0M cache reads). The feature: a
    stop writes a stop record (unit, task, round counts, the question or
    the FAIL reasons), and `/sdlc execute` reads it, the progress records
    and the branch, takes the user's ruling and starts at the stopped
    task, near a first launch's 45K. It ships in `/sdlc execute`, not a
    personal skill. Left out: a member that waits on the parent, since a
    headless session kills a waiting workflow after 10 minutes and keeps
    its whole context. Starts as a feature document once e6 ships 0.21.0;
    if e6 stops first, restart it by hand with a fresh launch and a short
    prompt.

## Next actions

Opener: no Next item is open; the user names the next. The
engine's M0 passed G1 and its unit 1 ran G2.5 by hand (`d2dafba`),
so the user's 2026-10-20 hold on G2's venue and G1's open edges is
lifted. The readings of PRs #116 and #119 that cost something (Open questions, G1)
still wait for a design text row. The Haiku receipts agent's question
closed with Next 8: Two-Key now takes its receipts from `receipts.py`
alone. Not folded in `s4-tree`: `g1.py`'s `Ready:` row
reader and `tree.drift`'s; `progress._target` has one caller left.

1. [x] The pilot's config line, in the engine's session; the engine's
   install ref moves to the release that carries G1 (pull, not push).
   Its feature document needs a new intake before its G1.3 can pass:
   its `Ready:` rows read `signed r3` (reading 3, kept in session 93).
   Done in the engine's own sessions, found in session 121: its CI pin
   moved to `v0.20.0` at `6d0c999` (2026-10-18), `G1` joined
   `active_gates` at `7fecf43`, intake wrote r9 from the request half at
   r7, and G1.3 passed all 11 items, signed by the engineer seat on
   requirements r7 and design r7, at `1da34dd` (2026-10-20).

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
6. Left by session 107's sweep of `s6-release`'s advisories: `README.md`'s
   "What ships today" omits the tree and the vocabulary layer, and its
   "54 specified conditions" row reads 57 in `docs/gates.md`.
7. `w1-session-size`'s Two-Key advisories (session 113): the hook looks
   for `.sdlc/workflow.md` in the event's `cwd`, so it goes silent once a
   session's `cwd` moves to a subfolder; `hooks.json` runs bare `python`,
   which exits non-zero on a machine without it; `main()` leaves the
   stdout write unguarded; ADR 0039's "only this repository holds one"
   holds since w2 (session 115).

8. `w2-workflow-file`'s Two-Key advisories (session 115): the reader
   skips a diagram line it cannot parse (`ghost(Ghost)`, `a --- b`), so a
   node in another shape escapes every check; a second row for one node
   is ignored with no refusal; the table reader takes the line after the
   header as its separator, whatever it holds. None touches the real file.

9. A watched `node` session (the user's question, session 123):
   `taskcontract node` starts an interactive `claude` with no prompt, no
   log and none of the spawn watchdog's three marks
   (`docs/usage/node.md:15-27`), so no session can watch one it starts.
   Parked: execution-team's e4 and e5 give the session the Orchestrator
   seat through workflows, which report progress and notify at their end.

10. Four enforcement gaps, found against Dave Kiss's talk "Eulogy for the
    Software Engineer" (session 124), in no feature yet: the
    `protect-main` ruleset requires a PR but no status check, so a red
    `ci` or `sdlc` run still merges; no CI job runs the declared test
    command before a merge (G4.11, named only in
    `.github/workflows/sdlc.yml:31-33`; e1 declares the command); the kit
    has no root `CLAUDE.md`, so no session loads `README.md`,
    `ARCHITECTURE.md` or the ADRs; no hook checks the `Theory:` trailer
    here, and none of the eight commits before session 124 carries one.

11. `e2-scripts`' Two-Key advisories (session 125), for e4 to e6: on
    Windows `prove.py`'s timeout kills only the direct child, so a
    `test.bat` that starts a hung program may outlast it (`receipts.py`
    kills the tree; e6's batch run meets this first); a build that
    cannot start names the test command in its 254 line;
    `--mutations` with an empty list passes with no mutation run, so
    the QA verifier must give at least one; `tarfile`'s `filter="data"`
    needs Python 3.10.12 or later, under `requires-python >=3.10`.
    `e3-wall`'s (session 126): the hook splits a Bash command into words
    only, so a walled path glued to a shell operator (`cat
    tests/run_a.bat;`) is one word that misses a glob entry (folder
    entries still hold); on Windows a Git Bash path (`/e/repo/tests/...`)
    resolves outside the root and passes. Both stand on the usage page
    among the calls that can still pass. ADR 0040 (e4) amends ADR
    0039's "a plugin hook never blocks" for `hooks/wall.py`.
12. For e5: the wall refuses the end of a walled task when the contract's
    id starts a walled path. e4's manual receipt
    (`RECEIPT_execution-team-e4_2026-10-27/team_start.md`, run A): with
    `wall.code: [greet/]` and contract `greet`, the hook refused the
    session's own `progress done greet/greeting/write-tests`, since the
    task file still named QA. e4's flow removes the task file after
    `progress done`; e5's `task.py end --unit {contract}/{unit}` meets
    the same hook. Closed by e5 (session 129): the flow removes the task
    file before each `task.py end`, `fail` and `stop`, as QA's tests pin.
13. The wall refuses the Developer's run of a declared `test.command`
    that names a walled folder: probe (session 129) `python -P -m pytest
    tests -q -n auto` under `functional: [tests/]` gives `Task green:
    Developer reads no functional test: tests`. A defect of e3 with e4
    (e4's receipt ran `pytest -q`). The kit's declaration dropped the
    word at `60c52b7`; every consumer whose command names its functional
    folder still meets it. Session 129's reading: the hook passes the
    declared `test.command` and `test.build` word for word. Closed by
    session 133 (`a4d5e44`, kit 0.21.1): it does, and the kit's command
    names `tests` again.
14. `e5-rounds`' Two-Key advisories and questions (session 129), for e6:
    the flow passes verifier text to Bash in double quotes (`--reason
    "{reasons}"`, `--question "{question}"`), so backticks, `$` and quotes
    in a reason run or break the call (a file would not); after a
    QA-channel FAIL at two-key, prove-red cannot prove red against code
    already green (session 129 ran it at the unit's base by hand; the
    QA verifier takes no `--at`); a QA verifier question at two-key
    reports "from Dev verifier"; the rounds file outlives an abandoned
    run; `gh pr create` has no failure path past a non-zero exit; the
    stop sample's join (`: ` and `, `) differs from the flow's `; `; the
    design's e5 row reads "Retirements: none" and names
    `gh pr create --draft` alone (the flow pushes first). A headless
    `claude -p` session kills a background workflow after 10 minutes of
    waiting (the QA verifier's two-key, 22:18 to 22:28), so the
    parent session ran that member twice. Session 133 (`b7beb4c`, kit
    0.21.1) closed the quoting (single quotes), prove-red after a
    two-key FAIL (it runs at the run's base, `--at`), the question's
    name (`qa-verifier`) and the join (the stop sample's); the
    `gh pr create` failure path was closed already (E9). Still open: the
    rounds file after an abandoned run (Next 24 decides what a stopped
    run keeps); the design's e5 row text (a signed document, no behavior
    turns on it); the 10-minute kill (Claude Code's limit).
15. `e6-batch-run`'s findings (session 131): while a task file stands,
    the wall refuses the Orchestrator's own calls as the running
    member's (`Glob **/*` during write-tests, refused as QA's), since
    `hooks/wall.py` reads only the task file's operator; the usage page
    now says so, and the design never drew it. The flow records tasks,
    never a check, so after a green run the tree reads the unit `doing`
    and its checks `to do`. On Windows the team's Git Bash puts GNU
    `find` and `sort` before System32's, so a batch suite must put
    System32 first itself (the engine's `test.bat` before its first team
    run). The Dev verifier's advisories on the fixture: a name holding
    `&` or `^` breaks `greet.bat`; its prompt points at feature-document
    sections a consumer's document may not have. Its round 3 advisories
    on the release: `standing-practice.md:13-14` still says Two-Key's
    receipts agent runs on Haiku; the changelog's e2 bullet says
    `receipts.py` runs `test.file`, though it runs the receipts file's
    lists; its e4 bullet and `ARCHITECTURE.md:38` say each member is a
    workflow, though the Orchestrator and `receipts` are not. Session 133
    (kit 0.21.1) closed the Orchestrator's refusal (the hook holds only a
    call with an `agent_id`, `a4d5e44`), the tree after a green run (the
    flow closes the unit, `b7beb4c`), the Dev verifier's sections
    (`b7beb4c`) and the three stale pages (`255892d`, `7e51796`). Still
    open: the engine's `test.bat` puts System32 first (the engine's
    repository); `&` or `^` in the fixture's name (no consumer runs it).
16. Session 133's Two-Key advisories, in no unit yet: the hook cuts each
    `--opt=value` word to its value before it compares with the declared
    commands, so a declared word of that form never matches (the usage
    page states the limit); the flow's `"reasons": {reasons}` arg is a
    joined string the Orchestrator must put in JSON quotes, and the flow
    never says so; the unit's close (`progress done {contract}/{unit}`)
    has no failure path; the hook runs `git` (once, twice while a task
    runs) for each of the session's own calls before it reads
    `agent_id`, which could pass them first.

## Open questions

- small-session-flow, two gaps for the design's next text row (w3's
  Two-Key advisories, recorded in session 117). The missing-file line,
  `Node {id} did not start: no workflow file at .sdlc/workflow.md.`,
  which the user ruled in session 116 and `USAGE.md` states, stands in
  no design text. And `node` ends on a Python traceback when the
  `claude` that `shutil.which` found cannot be run (`Popen` raises
  `OSError`); the design draws no line for it.
- How does the user's subscription weigh a cached read against a fresh
  token (session 96)? The shares of the process's cost rest on the
  API's weights. The `/usage` readings of `s5-start`'s two sessions are
  the first measure (`USAGE-readings.md` in the s5 receipt folder).
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
