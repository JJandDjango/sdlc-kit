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
24. [x] Restart a stopped run in a fresh session (the user, session 130).
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
    prompt. Session 135: the requirements document
    `docs/features/run-restart.md` is signed by the PO seat at r4 (r5):
    five criteria, 15 checks, 0 OPEN. Abandoned runs (a session that dies
    mid-task) are in; a stopped task's third FAIL restarts with three
    fresh rounds only on an answer the user rules enough. Session 136: the
    design run wrote `docs/features/run-restart.design.md` at r1 against
    requirements r4, S1 to S4 confirmed (scope, out of scope, interfaces,
    sources): one record folder a unit under the git folder, a new
    `task.py restart`, `--answer` and `--enough` on `/sdlc execute`. It
    paused at S5 with its candidate unanswered; the candidate found
    `execute.md` at 11,785 bytes (11,720 characters as the test counts)
    of its 12,000-character ceiling, so the restart's steps go in a new
    `flows/restart.md`. Session 137: the engineer seat signed the design
    at r4 (r5): 12 sections, 0 OPEN, five units `rs1-stop-record`,
    `rs2-restart`, `rs3-fresh-rounds`, `rs4-abandoned`, `rs5-release`
    (kit 0.22.0), built in that order, about 3.0M to 3.5M tokens.
    Session 138: intake found `rs2-restart` holding four checks with no
    `+` join; the design paired `SC2.3+SC5.3` and was signed again at r8
    (r9); the five terms were ratified and the dictionary took 20
    done-means words; `specs/run-restart/contract.yaml` validates
    ready-green, with `Ready:` rows at requirements r6 and design r10, and
    lang-check reads 0 on it. Session 139 (branch
    `session-139-rs1-stop-record`, no PR): G1 passed (`b4683fa`, the user
    signed G1.3); the team built `rs1-stop-record` at `bfda725` (suite
    2692); the Dev verifier failed round 1 on scope alone, since the
    contract lists `tests/test_rounds.py` and `tests/test_team.py` and the
    unit also touches `tests/test_stop_record.py` and
    `tests/test_flow_fixes.py` (scope-check SC001). The run stopped with a
    stop record. Session 140: the user ruled `tests/`; re-intake
    `025fdc4` (design r11 to r13, requirements r7) reopened G1.3, which
    the user signed again on design r11 (`173b47d`); both verifiers
    passed rs1 (the QA verifier caught 4 of 4 mutations); PR #156 merged
    at `7a1e96d`. Session 141 (branch `session-141-rs2-restart`, plan
    `f139b2b`, no PR): QA drafted `tests/test_restart.py` (105 tests),
    approve-tests and prove-red passed, and the Developer made them green
    (with the `--unit` drive-colon fix), uncommitted; 29 older tests
    pin the old behavior. The Developer asked two questions, so the run
    stopped at green with a stop record. Session 142 (same branch):
    green restarted with the handoff's answer (restart.md reads the base
    from `run.json`); the test-retirer retired 1 older test and amended
    28; unit `f2fae79` (suite 2796); both verifiers passed (the QA
    verifier's four mutations ran from the session, past the 600 s Bash
    cap); the SC2.1 receipt passed, a fresh headless session starting at
    green near 54K; PR #157 merged at `8c492dd`. Session 143 (branch
    `session-143-rs3-fresh-rounds`, plan `aa589a5`): every task passed
    round 1 and the unit landed at `4d0ef1e` (suite 2827), but the QA
    verifier caught 3 of 4 mutations: no test stopped at a peer task
    before `--go --fresh`. The QA channel's round 2 added five cases
    (`1893f47`, suite 2832, code unchanged); both verifiers passed; PR
    #158 merged at `cf23f04`. Session 144 (branch
    `session-144-rs4-abandoned`, plan `4d01e8e`): QA's 14 tests passed
    approve-tests and prove-red in round 1; the session's review failed
    green round 1 (R1's abandoned path skipped R5, which holds the kept
    values) and round 2 fixed it; the test-retirer amended one
    assertion; unit `8bafbd8` (suite 2846); the Dev verifier passed and
    the QA verifier caught 10 of 10 mutations; the SC5.1 receipt passed:
    a headless session killed mid-task left an abandoned run, a fresh one
    showed it and started nothing, and `--answer yes` restarted at
    write-tests. PR #159 merged at `e8d33b9`. Session 145 (branch
    `session-145-rs5-release`, plan `bea8678`): rs5 builds the design's
    Sources row the earlier units left out: `task.py restart` reads the
    progress records and its line gains `progress`, one line for each
    earlier task whose record is missing or not done, `run.json` winning.
    Approve-tests failed three rounds on SC4.2's source check, each round
    closing the holes named and the verifier finding narrower ones; the
    run stopped, and the user ruled the answer enough with a bar (fix
    round 3's three defects; any further evasion is advisory unless it
    shows a real transcript read). The fresh round passed; unit `46e30f5`
    (suite 2984). The Dev verifier failed two-key round 1 on order alone
    (the receipt and 0.22.0 not yet in the tree), so green round 2 shipped
    the release at `ad5d1e6`; both verifiers passed round 2 (QA verifier 9
    of 9). The SC4.1 and SC4.3 receipt: four headless restarts of one unit
    each read 40,074 tokens at the first request. 1,667K agent tokens plus
    2.31M receipt cache reads. Merged as PR #160 at `59bf526`, and tagged
    `v0.22.0` there on the user's word.
25. [x] After the user merges and tags `v0.22.0`: the self-pin PR
    (`.github/workflows/sdlc.yml:20`, `docs/usage/restricted-environments.md:40`
    and any other pinned install line) to `v0.22.0`, the 0.21.1 shape (PR #151).
    Session 146 on `session-146-self-pin`: no other pinned install line
    exists; the `uv` line, run against the tag with `python -P`, installs
    `sdlc-taskcontract 0.22.0` and reads `specs/run-restart` ready-green;
    the suite passes (2984).
28. [x] Give the team's agents only the tools they use (the user, session 152:
    highest priority, ahead of Next 26's `s8-honest-reads`). The five
    workflow scripts call `agent()` with no agent type
    (`workflows/developer.js:79`, `qa.js:112`, `qa-verifier.js:153`,
    `dev-verifier.js:127`, `test-retirer.js:92`), so each agent takes the
    session's whole tool set. An agent's start read 53,782 tokens on
    2026-10-17, tool definitions about 24K of it (`Artifact` alone about
    13K). One agent definition allowing Read, Grep, Glob, Edit, Write and
    Bash, passed as the agent type in the five calls, takes about 19K off
    each start. Session 153 on `session-153-agent-tools`: a probe agent
    started at 18,314 tokens as `sdlc:sdlc-verifier` against 49,831 as
    the default; the path amends `execution-team` (design r18, measured
    r19). Session 154: r20 fixes two points of r18 (the verifiers'
    `INCOMPLETE` on a missing type; the model check joins e7's probe,
    Risks 12), measured r21, signed r22; re-intake added
    `e7-agent-type` (Ready r7 and r23) and G1 passed again (G1.3
    re-signed). Session 155: the probe of Risks 9, 10 and 12 held
    (`RECEIPT_execution-team-e7_2026-11-14/probe.md`); QA's round 1
    stopped on three questions, and the user approved its 18-test list
    with both rulings. Session 156: QA's rerun kept the draft unchanged,
    so approve-tests went `--by user`; unit `2721e7e` (suite 3086), with
    Ruling 1's hand amendments in five test files. Two-key stopped once:
    `prove.py`'s export has no `.git`, and the user ruled `listed()`
    amended by hand (`471622f`); both verifiers then passed round 1 (QA
    verifier 11 of 11), ADR 0042. The after-measure waits for the first
    unit built on a kit release carrying e7: this run used the installed
    kit, whose members start untyped.
26. [x] Close G1's open edges before any G2 work (the user, session 146).
    The first edge is closed: G1 was unreachable from a plain request
    (the engine's finding of 2026-11-12, an escape of `s5-start`;
    `NOTES_g1-plain-request-post-mortem_2026-11-12.md`). Unit
    `s7-plain-request` (session 149, kit 0.22.1, commit `5b5899e`) makes
    `new` refuse a feature G1 gates with no feature document, and G1.3
    name the missing document with RS302; merged as PR #162 at
    `268c88e`, tagged `v0.22.1` there, and the self-pin PR (session 150,
    `session-150-self-pin`) moves the kit's own pins to that tag. The
    engine's stuck contract is the engine's to clear. The rest stand under Open questions: the readings of PRs #116 and #119
    that cost something (an exempt feature refused in the tree's second
    build; I9 trusting a config that cannot be trusted), the
    hand-written files that stop the print or a command (sessions 94 and
    95), G1.3's seven unnamed cases, G1.2's (model files no record binds,
    P with no live run, a `tlc.cmd` at the root), G1.1's four, and the
    three smaller ones; with them the `s4-tree` folds left in Next
    actions' opener. Each waits for a text row of
    `docs/features/g1-requirements-spec.design.md`: the engineer seat
    rules each edge (fix it, or leave it and say so), signs the row, and
    a re-intake reopens G1.3 before the build. Session 150 listed 37
    edges on `session-150-g1-edges` (`plan.md`, section 6), and the user
    ruled all as called: 29 fixes in three units (`s8` to `s10`), 7 left,
    1 already left. Session 151 wrote design r16, which takes the kept
    readings ADR 0041 rule 1 owes, measured it (r17), and the user signed
    it (r18): 28 fixes in `s8` to `s10` (kit 0.22.2), 8 left, and 1
    (`tree.py`'s docstrings) found closed by `s4-tree`. Session 152's
    re-intake found `s8` with four checks against the schema's three
    sketch entries; design r19 joins `SC2.1+SC3.1` (the user signed r21),
    and the contract took `s8` to `s10` ready-green (rows r14 and r22).
    The checks before signing hold no check for a unit of more than three
    checks with no `+` pair; r17 missed it. Session 157 built
    `s8-honest-reads` (`e62a4e2`, `e00f346`; A1, A2 with F1, C1, C2, D1,
    D2 in part, D5, D6, F2, H1), on a draft PR; Two-Key ended with one
    mutant the user ruled equivalent. Session 158 built
    `s9-one-line-refusals` (`37b14ea`, `a192f0f`; B1 to B5, D4, H2), on a
    draft PR. Session 159 built `s10-words-and-folds` (`02fc83e`; C3,
    D3, E1 to E5, G1, H3; B6 not taken), merged as PR #167 at `9514ff0`
    and tagged `v0.22.2` there (session 160: the install from the tag
    read 0.22.2 and `ready-green`); the self-pin PR moves the kit's own
    pins to that tag. Session 161 closed B6, the last edge: `tree.build`'s
    docstring says the second build's G1 line and its conditions still
    name each feature that holds them.
29. [x] Write session-loop's requirements document (the user, session
    163): sessions that wrap and restart themselves until the user is
    needed. Session 164 finished the interview: five criteria, 18 checks,
    the PO seat signed r4 (r5) with one OPEN (ready check 3: SC1 holds
    five checks and SC2 four, since Q11's regression step adds checks
    past the cap). SC6, the herdr sidebar, split to Next 31. The O5
    material shape hid every draft-check finding (Next actions 2):
    reshaped to flat keys, the check read 60.
30. [x] Build session-loop's four units, l1 to l4 (kit 0.23.0). Session
    178 closed l4 on branch `session-178-l4-stop-entry`: the user signed
    design r17 (r19), intake r20 added `hooks/loop_ask.py` to the scope,
    G1 signed again on r17; the fix round's unit `934c72e` (27 tests in
    `tests/test_loop_stop_entry.py`, the user's assertion A and reading B,
    five older pins moved), Two-Key PASS in round 1 (QA verifier 9 of 9
    mutants). The stop entry passed live (`manual.md`, issue #183): with
    no nudge, the session ran `loop.py stop` before asking in a plain
    message; the deny hook never had to fire. The `v0.23.0` tag and the
    self-pin PR follow the user's merge. Carried:
    `tests/test_pane_renders.py::test_sc4_3_a_source_change_renders_within_two_seconds`
    failed once at 2.19 s under `-n auto` and passed on the rerun.
    Session 177 ran the sitting (`RECEIPT_session-loop-l4_2026-11-23/manual.md`):
    SC2.2, SC3.1 and SC3.3 PASS live; the stop entry FAIL, since both
    loop sessions asked by an AskUserQuestion dialog with no `loop.py
    stop`; the user took the fix into l4 as design r17. Clones
    `.trial/clone` and `.trial/clone-b` stay. Session 176 built l4 on
    branch `session-175-l4-loop-rules`, PR #180 (merged at `c7ad046`):
    unit `4845b4f`, CHANGELOG fix `f176624`, Two-Key PASS in round 2.
    Session 175 stopped at the test list: 51 tests red, QA verifier PASS,
    the user approved with readings A to D. Session 174 folded the
    launcher and the tree hook into the kit's `herdr/` folder (Next 32,
    ADR 0043), so l4 runs `/sdlc execute` with no hand run or shim;
    `E:\herdr-sdlc` keeps the history the shas below name. Session 173
    built `l3-loop-stops` on branch `session-172-l3-loop-stops`:
    `E:\herdr-sdlc` `31918d6` (README `1602d9a`), 109 tests, Two-Key
    PASS in round 1 (Dev verifier PASS, QA verifier 11 of 11 mutants
    caught). Session 172 drafted the 18-test list and stopped at the
    tripwire; the user approved it with readings A (l2's
    `assert_well_formed` takes `process-info --pane P`) and B (a failed
    `gh` or toast at a stop stays unpinned) and the added assertion C
    (the issue is filed from the pane's folder). Carried to l4, from
    l3's Dev verifier: `wait_idle` polls with no exit or hang check, so
    a session that exits or hangs after a `continue` sentinel, before
    the pane reads ready, holds the launcher forever; a half-written
    sentinel at the same poll as an exit stops with the exit message.
    Still carried from l2: `restart()` ignores the herdr calls' exit
    codes; no test pins a failed `pane get` or a missing status during
    the wait; `wait_idle`'s name still says idle.
    Session 171 ran l2's manual receipts live: SC1.1 failed
    first (herdr reads a finished turn nobody has looked at as `done`, and
    the launcher waited for exactly `idle`), was fixed at `E:\herdr-sdlc`
    `27cb671` (Two-Key PASS round 1, 68 tests) and passed on the rerun
    (`/clear` 3.4 s after the sentinel, the new session naming the Next);
    SC1.3 passed (`RECEIPT_session-loop-l2_2026-11-22/manual.md`). The
    trial setup stays for l4's live receipts: clone `.trial/clone` (kit
    progress copied in, `cairn.plan` set), origin `.trial/origin.git`,
    both in the kit folder and listed in `.git/info/exclude`. Session 170 built
    `l2-loop-launcher`: `E:\herdr-sdlc\herdr_loop.py`, commit `c6aee1b`
    on that repo's master (no remote), 26 tests, Two-Key PASS in round
    1. `/sdlc execute` commits only in its own repo, so Claude ran its
    tasks by hand: the members got `repo` `E:/herdr-sdlc`, a prove.py
    shim as their `pluginRoot`, and the repo's new `.sdlc/config.yaml`
    test declaration (`ef3f0d1`); `task.py` kept the progress in the
    kit. The kit's wall hook refuses a wrapped command naming `tests`, so
    the Orchestrator ran the Developer's suite as the receipts. Session 169 built
    `l1-loop-files` (`workflows/tools/loop.py`, 39 tests with the
    timer-minute property, Two-Key PASS in round 1). Session 168 passed
    G1: the user signed
    all 11 items of G1.3 on requirements r9 and design r10
    (`.sdlc/g1/session-loop.yaml`); items 8 and 9 were checked with their
    gaps in Next actions 24. Session 167 took the
    contract to lang-check zero (129 findings to 0): the ten terms of the
    requirements ratified, 12 words the done_means force added to the
    dictionary, the rest of the prose rewritten. Session 166's intake
    parked the pair on four OPEN marks; the requirements merged 18
    checks to 14 (r9), the design cut the units to four, at most three
    sketch entries each (r10), and the contract validates ready-green
    (`specs/session-loop/contract.yaml`). Session 165 ran the
    design run: three live trials closed the requirements' OPEN 9 to 11
    (`CronCreate` woke the idle session; herdr typed `/clear` and a
    skill into a Claude pane; `PushNotification` is the notice), and
    the engineer seat signed r4 (r5) with 0 OPEN and 20 CL006 findings
    answered in Notes. The user reports the `needs-ruling` label created
    (session 168), but `gh label list` on `JJandDjango/sdlc-kit` showed
    none that session; check it before the first live run.
31. Write session-loop-sidebar's requirements document (the user,
    session 164): the herdr sidebar shows each loop's position, strike
    count and waiting state. Split from session-loop's SC6.
32. [x] Fold `E:\herdr-sdlc` into the kit as an opt-in `herdr/` folder, after
    l3 and before l4 (the user, session 173). A second repo is a second
    dependency for one workflow: it has no remote (no one else can
    install it, no backup), CI never runs its tests, and `/sdlc execute`
    cannot commit there, so sessions 170 to 172 ran the team by hand
    through a prove.py shim. Keep ADR 0031's real line (the kit's core
    imports nothing from herdr and runs no herdr command) in a new ADR
    that supersedes its "multiplexer plugin outside the kit" clause;
    revise session-loop's design and contract paths; move `herdr_loop.py`,
    `herdr_seat.py`, their tests and README, so 0.23.0 ships one repo.
    Done in session 174: ADR 0043; the copy from `E:\herdr-sdlc`
    `1602d9a` (no history import: the scope check flags commits with no
    `Contract:` trailer); design r13 to r15 and re-intake r16 move the
    contract's scope to `herdr/`; the 109 tests pass in the kit. Left
    open: a test pinning ADR 0043's line, and deleting `E:\herdr-sdlc`
    (the user's call).

## Next actions

Opener: Next 26, G1's open edges, is closed (B6 last, session 161). The
engine's M0 passed G1 and its unit 1 ran G2.5 by hand (`d2dafba`),
so the user's 2026-10-20 hold on G2's venue and G1's open edges is
lifted. The readings of PRs #116 and #119 that cost something entered
design r16 and closed with `s8-honest-reads` (session 157). The Haiku receipts agent's question
closed with Next 8: Two-Key now takes its receipts from `receipts.py`
alone. `s10-words-and-folds` folded `g1.py`'s `Ready:` row reader and
`tree.drift`'s into `g1.ready_revision` (session 159);
`progress._target` has one caller left.

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
   measured in session 162 against main at `0c2f9f6` and the engine's
   record (`E:/ImSimProject/engine`: `m0-window-vulkan-cleared-frame`
   and `subset-lint`, each through both interview runs and intake). The
   2026-10-05 feedback named none. A consumer met four of the 27, and
   the measure found a fifth; each is a unit candidate, in no unit yet:
   - S3 never asks for each output kind (`solution.md:50`, unchanged
     since 0.18.0): in both designs ready check 12 found outputs S3 had
     not drawn, each closed by a way back after signing (engine
     `subset-lint.design.state.yaml:326,332`,
     `m0-window-vulkan-cleared-frame.design.state.yaml:246,252`).
   - No step writes the Record: O6 writes "(none: intake writes the
     record)" (`opening.md:36`; a test pins the string) and intake never
     names it. Both features wrote it by hand at merge (engine
     `b1b11b7`, `e029f96`).
   - After a ready intake the design's Contract block still reads
     "(none: intake writes `specs/{id}/contract.yaml`)" (engine
     `subset-lint.design.md:615`,
     `m0-window-vulkan-cleared-frame.design.md:322`), and the status
     line moved to merged by hand (`b1b11b7`), against ADR 0036.
   - I3's "contract already exists, ASK" says nothing for a re-intake
     (`intake.md:26`): m0's re-intake removed the r3 contract by hand,
     since the write-guard denies a session on a ready contract (engine
     `7116a92`).
   - Found by the measure: O5 records material "under
     `answers.{section}` with `source: material`" (`opening.md:34`).
     Both engine runs read that as a mapping, and the draft check reads
     a mapping as no entries (`taskcontract/lang.py:482-484`), so it
     reports 0 findings on 0 checks. Each run reshaped its answers by
     hand before the check (engine `subset-lint.state.yaml:129`,
     `subset-lint.design.state.yaml:325`).
   Parked: each stands on main, and the engine never ran its path or ran
   it with no symptom. Each is a change of behavior or a sentence a test
   pins word for word.
   - The interview: E2 gives a free path (`CHANGELOG.md`) no exemption
     (both designs had no release unit, so E2 skipped); P6 writes
     `next: P1` before Q15 proposes a changed check's scenario again
     (the engine went back twice, no check changed); Q14 names `amends`
     but never asks it, and its record has no field for it; the
     "sections written" count is one a seat cannot check (all four
     documents wrote it, no symptom); Q15 withheld the scenario for a
     check Q11 accepted, as thin (`d3`); a state-file line with an
     unquoted colon makes the file unreadable and no step says to quote
     (`d3`; the same class broke the engine's hand-written
     `specs/components.yaml`, `1da34dd`); S12 routes into E1 to E5 in
     the same turn (`d3`); a design run lets a unit hold four or more
     checks with no `+`, and I4 places only a pair a `+` joins (`d5`;
     every engine unit holds two or three).
   - Intake: I5 still offers `strike` on a feature document.
   - The command: with a repo dictionary that cannot be read, `--draft`
     prints its `CL000` line and still ends `(no dictionary here - door
     at rest)` (`lang.py:566-599`); it runs no rule of `vocab-check`,
     while `docs/usage/feature-document.md:202` and the contract's SC2.1
     say "through the vocabulary check".
   - Pages: `docs/controlled-language.md` never names `CL014` or
     `--draft`; `docs/usage/install.md` section 2 never says the
     interview needs the plugin, nor pins its `pip` line; "each heading
     followed by its tag" (the interview's `SKILL.md:56`), where
     Traceability and the Appendix carry tags on their blocks (a test
     pins it; the engine writes no tag lines, by its own ruling);
     `skills/sdlc/SKILL.md:97` uses "parked" for a contract held at
     draft and for a parked pair.
   Closed by the measure. Gone on main: S6's release unit (E2 asks the
   seat when the rows leave it unclear); E6's way back into a
   request-half section (a design run writes nothing there); the case
   with no engineer seat (a design run always asks for one); S2 calling
   the engineer seat's places refusals (they are the PO seat's now);
   `intake.md`'s two meanings of "above" (one left); `MAP.md:41` (the
   file left in the Cairn 2.0 migration). Kept as history:
   `docs/features/feature-document.md:413`'s "eighteen sections", a
   signed record of a released feature whose count ADR 0037 amends.
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
   2026-09-26; it needs a pair before it unparks, and reads G1.3 `failed`
   with RS302 until then, requirements r10); `derived-language` (prerequisite 5); ADR 0029's appendix
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
17. The interview's W1 (`skills/product-specification-interview/flows/output.md`)
    offers the Google Docs form as Markdown to paste; the user (session
    135) wants a link to a real Google Doc, or no question at all. The
    route exists: the styled-rendering prototype writes a .docx, and the
    Workspace connector's `import_to_google_doc` takes it from
    `~/.workspace-mcp/attachments` by a `file:///` URL (sessions 32, 50).
18. `rs2-restart`'s Two-Key advisories and receipt findings (session
    142), for rs3 to rs5: E3's `keep --value '{draft}'` and E7's
    `--value '{receipts}'` carry no quoting rule, and the SC2.1 receipt's
    E7 call failed once on a Windows path's backslashes (`--file` avoids
    both); `--answer` on a unit with no stop record reaches the members
    as text, not an object; `restart --go` removed a task file that named
    another unit (fixed by rs4); the restart reads no progress record, though the usage
    page, `restart.md` and the design say it does; `end --run` leaves the
    empty contract folder. And the kit's `test.file` runs without `-n
    auto`, so the QA verifier's four mutations on `tests/test_restart.py`
    (about 170 s a run) outlast the 600 s Bash cap.
19. `rs3-fresh-rounds`'s Two-Key advisories (session 143), for rs4 and
    rs5: `--fresh` clears the channel on a stop of any kind, and on an
    abandoned run, though only a third FAIL's enough ruling passes it;
    `--enough` is named only in `restart.md`, not in `execute.md`'s E2
    (at 11,991 of 12,000 characters); the not-enough block stands
    between R3 and R4 outside a numbered step. And the QA verifier
    starts each two-key with more mutations than the 600 s cap holds (7,
    then 9, about 100 s a run), so each round lost one killed run before
    it cut to four.
20. `rs4-abandoned`'s Two-Key advisories and review findings (session
    144), for rs5: `--go`'s help text (`task.py:200`) still says it
    removes the task file, though it now removes one only when it names
    the unit; R4's `--fresh` paragraph opens "On yes", which an
    abandoned run's yes could be read to reach, and only the first
    paragraph's "never `--fresh`" settles it; no test pins that R1's
    abandoned path goes through R5, the defect the session's review
    caught. And the SC5.1 receipt's three headless launches read 1.40M
    from the cache, against a plan of 0.4M to 0.7M: each re-reads E1's
    and E2's files over 7 to 13 messages before its first flow call.
21. `rs5-release`'s findings (session 145). The team's flow has no
    notion of a manual-receipt check: approve-tests requires every sketch
    pinned by a test (`qa-verifier.js:131`), and the Dev verifier grades
    two-key on the files as they stand, so a unit whose checks are
    receipts fails both until the session's answer or the receipt lands
    first. After a third FAIL the answer reaches only the channel's member
    (`restart.md` R3), never the verifier whose bar it sets. A text test
    of "reads only" over flow prose invites an open-ended hunt; the
    allow-list lint held only under the user's bar. `task.py restart`
    drops `read_progress`'s problem lines, so a progress file that does
    not parse shows as "no record" lines with no reason; `RESTART_ORDER`
    copies the seven tasks' order; the module docstring's `--go` sentence
    reads "the task file, the task file only when it names this unit".
    The restart line carries the whole kept draft (about 10K characters
    at an approve-tests stop). The QA verifier's two-key ran `prove.py`
    with `-n auto` added to fit the 600 s cap, and started with 12
    mutations before cutting to nine.
22. Score seat prompts on behavior, not only form (the user, session 155,
    after DSPy's "program, don't prompt", dspy.ai). PromptLang checks a
    prompt's form; nothing checks that an edited seat prompt still reaches
    the verdicts it reached before, so a prompt can drift unseen. The
    untracked `RECEIPT_*` folders hold past runs whose verdicts are known: a
    replay of a changed seat prompt against them, scored by verdict
    agreement, would catch the drift before it ships. Later, on that score
    alone: mine the verifiers' FAIL reasons for seat-prompt edits (DSPy's
    GEPA). Not before e7.
23. Give `prove.py`'s export a git (e7's two-key, session 156). The
    export is a `git archive` with no `.git`, so a pin that asks git
    fails the mutation pass's baseline and no mutation runs. e7's
    `listed()` falls back to the file's presence there (`471622f`), so a
    mutant that only untracks a file goes uncaught. And `prove.py`
    overlays `{scratch}/draft/` on the export, so after a hand amendment
    a stale kept draft shadows the committed test: e7's QA verifier
    deleted it to pass its baseline. Clear or refresh the draft before
    two-key.
24. session-loop's G1.3 gaps (session 168), checked by the user with each
    gap recorded here. Item 8: two external dependencies have no failure
    criterion: herdr failing under the launcher's pane calls, and `gh`
    unreachable or signed out (only the missing label has one); the loop
    falls back to today's hand restart. Item 9: the timer's minute rule
    (design Constraints: the stop plus 55 minutes, cut to the minute,
    moved off :00 and :30) has no property spec; at l1's approve-tests,
    pin it as one: for any stop time, the timer lands 54 to 56 minutes
    later and never at :00 or :30. Item 9 closed in session 169:
    `tests/test_loop_files.py` sweeps every second of one day and the
    last hour of three month and year ends.
25. A timing flake (session 169): `tests/test_pane_renders.py::
    test_sc4_3_a_source_change_renders_within_two_seconds` failed once at
    2.22 s against its 2.0 s bound under `-n auto`, then passed.

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
- A hand-written file that stops the print or a command (sessions 94
  and 95; the two handoff files name each with its receipt). On main
  G1's three readers hold their known causes, the tree holds whatever a
  reader ends on, `tree.build` holds whatever G1's part of a build ends
  on, and the print writes a character its output cannot hold as its
  escape. `s9-one-line-refusals` (session 158) closed the five older
  causes: a contract that is not UTF-8 or holds a number past 4300
  digits, the loader's ValueError in `tree._load`, `contract_scope` and
  `g1._seat`, `g1-check`'s bare readers, and a character outside the
  code page through a pipe. Still open: the tree ends on a vocabulary
  file that is not UTF-8 or holds a date no calendar holds; it reads
  that file through `checker.py` and `vocabulary.py`, outside
  `g1-requirements-spec`'s scope (QA's question, session 158). Left
  from round 4, advisory: an error of another cause that passes
  before the second build prints under G1's name for that one print. A
  `g1.exempt` entry that is no text prints whole in its problem line,
  however long.
- G1.3 (session 92; PR #112's body names each). The user kept all 12
  readings at the review (session 93), so a feature with no feature
  document cannot pass G1; since `s5-start` it can start no task, and
  that case is Next 26's first edge (session 147). Design r16 named the
  six cases and a seventh from the review, an item that does not apply
  to the feature; `s10-words-and-folds` (session 159) pins their words,
  and R5 now says that `checked` covers such an item. Three edges left as they are: a shortened flag (`--check`)
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
  - P has had no live run. Its two calls, its configuration as a text
    file of `p check`'s arguments, and its exit codes (0, 1 and 2, from
    `ExitCode.cs` at `260da92`) are read, not run. What `p check`
    returns with several test cases and none named is not measured;
    since `s8-honest-reads`, `model` refuses a configuration with no
    `-tc`. P writes inside the project's folder.
  - `g1-check` on a damaged kit schema exits 2 with
    `G1.2 (KitFault: ...)` since `s9-one-line-refusals` (the Developer's
    reading, session 158); no test pins it. `s9` closed the three paths
    that ended either writer on a traceback.
  - Overlap's tail, under USAGE's stated limit: a second name for one
    folder (a link, an absolute path with no drive, two Unicode forms
    of a name, a Windows short name) is not seen.
- G1.1, one edge for the engineer seat (session 88; Two-Key's
  advisories on `79b4a5b`). Session 102 closed two others: a feature
  whose schemas stand under two `g1.schemas` entries now gets one record
  that holds a run for each, and a contract whose scope cannot be read
  reads G1.1 `to do`, which `lint` refuses. `s8-honest-reads` closed two
  more: `lint` with no `g1.schemas` key, and patterns that match no file.
  `s10-words-and-folds` closed the refusal lines no test pinned: the
  design adopts each, and `tests/test_g1_words_pinned.py` holds them.
  - `buf` has had no live run: its exit code on a violation (100, from
    memory), its JSON report (one object a line) and where an older
    release prints its version are read from its reference page and a
    stand-in.
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
