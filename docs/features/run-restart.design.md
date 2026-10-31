| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-30 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r4. Engineer seat: Johnathan Hyden |
| 2026-10-31 | Johnathan Hyden | r2: Measured: the checks before signing, on the solution half: 33 findings (CL006 29, CL008 4); Scope against the release unit's paths: pyproject.toml, skills/sdlc/init.py, .github/workflows/sdlc.yml outside Scope; ready checks 11 to 15: 3 OPEN |
| 2026-10-31 | Johnathan Hyden | r3: Measured: the checks before signing, on the solution half: 30 findings (CL006 30); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-31 | Johnathan Hyden | r4: The solution half finished: 12 sections written, 0 OPEN |
| 2026-10-31 | Johnathan Hyden | r5: Signed: solution half. The engineer seat signs r4 |
| 2026-10-31 | Johnathan Hyden | r6: Units: rs2 pairs SC2.3+SC5.3 in one sketch entry |
| 2026-10-31 | Johnathan Hyden | r7: Measured: the checks before signing, on the solution half: 30 findings (CL006 30); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-31 | Johnathan Hyden | r8: The solution half finished: 12 sections written, 0 OPEN |
| 2026-10-31 | Johnathan Hyden | r9: Signed: solution half. The engineer seat signs r8 |
| 2026-10-31 | intake | r10: Ready: contract `run-restart` validates ready-green, derived from r8, against requirements r4; the engineer seat (Johnathan Hyden) signed the solution half at r8 (r9) |

# run-restart - Restart a stopped run in a fresh session

`sdlc_development_kit` · seat: engineer Johnathan Hyden · requirements: `docs/features/run-restart.md` · contract: `run-restart`, draft · PR: none · merge SHA: none

## Proposed solution

`[Engineer seat · authored]`

### Scope

- `workflows/tools/task.py`: `stop` and a third `fail` delete the task file and the rounds file today (`task.py:220-249`); they keep the rounds file and write the stop record. A new `restart` command reads the stop record, the progress records and the branch, and prints where the run starts or why it cannot.
- `skills/sdlc/flows/execute.md`: the restart ships in `/sdlc execute`. E2 runs `task.py restart` first; a refused task start stops with a stop record; each passed task saves what it hands on (QA's interface note, the draft, the base commit, the commit, the receipts) in the git folder beside the task file.
- `skills/sdlc/flows/restart.md` (new) and `skills/sdlc/SKILL.md`: the restart's steps, in their own flow file since `execute.md` stands near its ceiling (see Constraints); `SKILL.md` lists the new file among its flow files.
- `workflows/qa.js`, `workflows/qa-verifier.js`, `workflows/developer.js`, `workflows/dev-verifier.js`: each takes an `answer` argument, the user's answer with the stop's question or FAIL reasons (SC2.2).
- `tests/test_rounds.py`, `tests/test_team.py`: the new and changed behavior.
- `docs/usage/the-team.md`, `USAGE.md`, `CHANGELOG.md`: the restart, for a user.
- `pyproject.toml`, `skills/sdlc/init.py` (`KIT_VERSION`): the release, kit 0.22.0; `.github/workflows/sdlc.yml` takes the `v0.22.0` tag in the self-pin PR after the merge.

### Out of scope

- The design document and the design run: the restart never edits or starts them. When the user's answer is not enough, the restart stops and the user starts the design run.
- `hooks/wall.py`: the wall is unchanged; the restart removes a leftover task file before `task.py start`, as every task does today.
- `taskcontract/progress.py`: the progress format and its writers are read, never changed.
- `workflows/tools/prove.py`, `workflows/tools/receipts.py`, `workflows/test-retirer.js`.

### Interfaces

A stop writes a stop record: the unit, the task, the round counts, and the question or the FAIL reasons. `/sdlc execute` reads the stop record, the progress records and the branch, takes the user's answer, and starts at the stopped task. The run's records stand in one folder a unit under the git folder, so two stopped units never overwrite each other.

```
Files, in {git folder}/sdlc-run/{contract}/{unit}/ (never committed):
  run.json    branch, base, the task in hand, and the values kept for later tasks
  stop.json   the stop record: task, operator, kind (question|error|refusal|fail),
              round counts, the question or each round's FAIL reasons, at
  rounds.json the failed reasons a task (moved here from {git folder}/sdlc-rounds.json)
  draft/      QA's draft test file
{git folder}/sdlc-task.json gains "unit".

task.py start   (unchanged output) the first start of a unit writes run.json: branch, base
task.py keep    --unit C/U --key draft|draft-file|receipts|commit (--file PATH | --value TEXT)
task.py stop    --unit C/U --task T --operator O --kind question|error|refusal --question TEXT
                prints as today; keeps run.json and rounds.json; writes stop.json; exit 1
task.py fail    third round: prints as today; writes stop.json; keeps run.json; exit 1
task.py restart --unit C/U   (read-only) one JSON line on stdout, exit 0:
                {"state": "none"|"stopped"|"abandoned", "task", "operator", "round",
                 "kind", "text", "kept": {...}}
                wrong branch: the SC2.3 line on stderr, exit 1
task.py restart --unit C/U --go [--fresh] --scratch DIR
                removes stop.json and a leftover task file; --fresh clears the task's
                rounds (three fresh rounds); writes the kept draft into DIR/draft/
task.py end --run --unit C/U   removes the task file and the unit's folder (a pass)

/sdlc execute {contract} {unit} [--answer TEXT] [--enough]
  Execution stopped: c unit u, task green, round 3 of 3: 2 sketches failed. Your answer?
  Is that answer enough to give green three fresh rounds?            (third FAIL only)
  Execution did not restart: c unit u stays stopped at green. The design may need revisiting.
  Execution was abandoned: c unit u, task green, round 2. Restart at green?
  Execution did not restart: the run stopped on branch b; this session is on main.
  Each member takes "answer": {"stopped": "<question or reasons>", "reply": "<answer>"}, else null.
```

An interactive session asks both questions in chat. A headless session ends its turn at each, and the user launches again with `--answer` (and `--enough` after a third FAIL). No endpoint table: nothing here is HTTP.

```
stop.json, a question; an error or a refusal has the same shape with its own kind:
  {"unit": "c/u", "task": "green", "operator": "developer", "kind": "question",
   "round": 2, "failed": {"write-tests": 0, "green": 1},
   "text": "Which header declares parse_args?", "at": "2026-11-02T14:05:11Z"}
stop.json, a third FAIL: each round's reasons in place of "text":
  {"unit": "c/u", "task": "green", "operator": "dev-verifier", "kind": "fail",
   "round": 3, "failed": {"write-tests": 0, "green": 3},
   "reasons": ["2 sketches failed: SC5.1, SC5.2", "1 sketch failed: SC5.2", ""],
   "at": "2026-11-02T15:40:02Z"}
run.json, green in hand after prove-red passed:
  {"unit": "c/u", "branch": "feat/c-u", "base": "8824592", "task": "green",
   "kept": {"draft": {"test_file": "tests/test_cli.py", "interface": "parse_args(argv) -> Args"},
            "draft-file": "draft/test_cli.py", "commit": null, "receipts": null}}
run.json, at the unit's first start: "task": "write-tests" and "kept": {}
```

### Sources

Today the running task stands in `{git folder}/sdlc-task.json` (task, operator and round, no unit: `task.py:214`); the failed reasons a task in `{git folder}/sdlc-rounds.json` (`task.py:159-172`); the task states in `.sdlc/progress/{contract}.yaml`, never committed (`progress.py:3-9`); QA's interface note, its draft and the base commit only in the session, the draft in a scratch folder a fresh session does not have (`execute.md:25, 34, 42`); the branch from `git branch --show-current` at E2 (`execute.md:25`). After the build:

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| State: stopped, abandoned or none | `stop.json` present: stopped; else `run.json` present: abandoned; else none | `stop.json` wins |
| The task to restart at | `stop.json`'s task; else `sdlc-task.json` when its unit matches; else `run.json`'s task in hand | in that order |
| Round n | `stop.json`'s round for a stopped run; else 1 plus the channel's failed rounds in `rounds.json`, as `task.py start` counts today | `rounds.json` wins at start |
| The question, error, refusal or FAIL reasons | `stop.json`'s `text`, or its `reasons` after a third FAIL | one source |
| The tasks already finished | `run.json`'s task in hand (every earlier task is done); the progress records show each task's state | `run.json` wins; a progress record that disagrees is shown in one line |
| The branch the run stopped on | `run.json`; this session's branch from `git branch --show-current` | compared, never reconciled (SC2.3) |
| The base commit | `run.json` (HEAD at the unit's first start) | one source |
| QA's interface note and test file name | `run.json`'s kept draft | one source |
| The test file | the kept `draft/` before prove-red passed; the working tree's file after | the working tree wins once prove-red passed |
| The commit and the receipts for two-key | `run.json`'s kept values | the kept commit wins over HEAD |
| The user's answer | `--answer`, else the reply in chat | `--answer` wins |

### Constraints

- A restart starts at most 50K tokens: it reads only the unit's run folder, the progress records and the branch, never a transcript (SC4.1, SC4.2).
- `stop.json` holds only the latest stop and `run.json` only the current values, so the fourth restart reads no more than the first (SC4.3).
- Nothing starts before the user's answer or word, and nothing starts on another branch (SC2.3, SC5.1, non-goals).
- Only `task.py` writes in the git folder; members write only in the session's scratch folder, as today.
- A unit with no run folder runs as today; the lines `task.py start`, `end`, `fail` and `stop` print today keep their wording (SC5.3).
- `skills/sdlc/flows/execute.md` stands at 11,720 of its 12,000-character ceiling as the test counts it (`tests/test_team.py:49, 810`): the restart's steps go in a new flow file, `skills/sdlc/flows/restart.md`, which E2 loads only on a stopped or abandoned run; whatever `execute.md` gains, it trims elsewhere. `skills/sdlc/SKILL.md` (9,505 characters) names the new file.
- No new permissions: the headless launch keeps its tool list (non-goal 1).
- Every Bash call is one segment; values are quoted the way `{reasons}` is today (`execute.md:28`).
- `task.py` writes `run.json` and `stop.json` whole: to a temporary file in the same folder, then `os.replace`, so a killed session leaves the old file or the new one, never half. A record that does not parse is reported, never guessed. Today `task.py:214, 232` write in place.

### Units

| Unit | Checks | Done means | Tests by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| rs1-stop-record | SC1.1, SC1.2, SC1.3 | A question, an error, a refused task start or a third FAIL writes `stop.json` in the unit's run folder. The record names the unit, the task, the round counts, and the question, error, refusal or each round's FAIL reasons. The run then ends with no PR and no task file. | SC1.1, SC1.2, SC1.3: automated (`task.py` on fixture repositories; a text test on the flow's refused-start step) | The rounds file's deletes at `task.py:211, 235, 246`; `sdlc-rounds.json` beside the task file, moved to the run folder as `rounds.json`; the usage page's three "removes both files" sentences (`docs/usage/the-team.md:206, 217, 225`); the tests that pin them, found by test-retirer (seen: `tests/test_rounds.py:162, 195, 403-404, 414, 521, 582, 630, 691`) |
| rs2-restart | SC2.1, SC2.2, SC2.3+SC5.3 | `/sdlc execute {contract} {unit} --answer TEXT` in a fresh session on the run's branch starts at the stopped task. The stopped task takes what the earlier tasks kept and the user's answer, and no earlier task runs again. On another branch nothing starts; a unit with no run folder starts as today. | SC2.1: automated (`task.py keep` and `restart` on a fixture run folder), and a manual receipt: a restart at green in a fresh session. SC2.2: automated (each member's `answer` argument). SC2.3, SC5.3: automated. | none |
| rs3-fresh-rounds | SC3.1, SC3.2, SC3.3 | After a third FAIL, an answer the user rules enough (`--enough`) restarts the task at round 1. The task then has three fresh rounds. An answer ruled not enough starts nothing and keeps the stop record. | SC3.1, SC3.2, SC3.3: automated | none |
| rs4-abandoned | SC5.1, SC5.2 | A run folder with no stop record reads as abandoned. `/sdlc execute` shows the unit and the task, and waits for the user's word. On that word it removes the leftover task file and starts at that task. | SC5.1: automated, and a manual receipt: a session killed mid-task. SC5.2: automated. | none |
| rs5-release | SC4.1, SC4.2, SC4.3 | A headless restart's first turn holds at most 50K tokens, the fourth restart of one unit too, and kit 0.22.0 ships. | SC4.2: automated (a text test: `restart.md` reads only the run folder, the progress records and the branch). SC4.1, SC4.3: manual receipts, the context-breakdown script on the first and the fourth restart's transcripts. | none |

Every check stands in one unit. `rs5-release` is the release unit: it ships kit 0.22.0 through `pyproject.toml` and `skills/sdlc/init.py` (`KIT_VERSION`), and the self-pin PR after the merge moves `.github/workflows/sdlc.yml` to the `v0.22.0` tag. The usage page's restart section is written in `rs1` with every marker red; each unit turns its own markers green as it ships.

The draft check's CL006 words in the done means go to intake's full lane as dictionary candidates: refused, start, third, folder, refusal, execute, fresh, stopped, takes, earlier, tasks, restart, restarts, rounds, keeps, abandoned, removes, leftover, headless, turn, tokens, fourth.

### Order

`rs1-stop-record`, then `rs2-restart`, then `rs3-fresh-rounds`, then `rs4-abandoned`, then `rs5-release`. Each unit reads what the one before it writes: `rs2` restarts from `rs1`'s stop record; `rs3` adds `--enough` to `rs2`'s restart path; `rs4` takes the same path from a run folder with no stop record; `rs5` measures the finished restart and ships it. `rs3` and `rs4` do not depend on each other, but both edit `task.py restart` and `restart.md`, so they are built in turn.

## Risks and cost

`[Engineer seat · authored]`

- An abandoned run leaves `sdlc-task.json` behind, and `task.py start` refuses every task while it stands (`task.py:200-202`). `rs4` removes it on the user's word.
- That file arms the wall only for a member's calls, never the session's own (`hooks/wall.py:12-15`), so the restart's own commands pass.
- Nothing marks a run live, so a run still going in another session reads as abandoned. The guard is SC5.1: nothing starts before the user's word, and the message names the task.
- A commit made by hand on the run's branch after the stop goes unseen: the restart checks the branch's name only (SC2.3), and two-key takes the kept commit over HEAD. Accepted: the user's answer can say so; the design adds no HEAD check.
- Only manual receipts hold the 50K ceiling (SC4.1, SC4.3), so a later edit could grow a restart's start unseen. The guard: `restart.md` takes `execute.md`'s 12,000-character ceiling test.

Cost: about 3.0M to 3.5M tokens over five build sessions at one round each: `rs1` 0.5M, `rs2` 0.8M, `rs3` 0.4M, `rs4` 0.5M, `rs5` 0.75M. Basis: the execution team's rows in `docs/session-metrics.md`, e1 to e4 at 0.49M to 0.81M on the same files and e6's release with live receipts at 0.76M. A unit that takes four rounds can run to 1.85M alone (e5's row).

## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | yes | The engineer seat, Johnathan Hyden (also the PO seat), at S3 in session 136 | SC2.2 leaves open how a headless session, which cannot take a reply, receives the answer. `/sdlc execute` takes `--answer` and `--enough`: an interactive session asks in chat; a headless one ends its turn and the user relaunches with `--answer`. |
| 2. More than one solution | yes | The engineer seat, Johnathan Hyden, at S3 in session 136 and S5 in session 137 | One folder a unit (`sdlc-run/{contract}/{unit}/`) over one shared file, so two stopped units never overwrite each other. The restart's steps in a new `restart.md` over `execute.md`, which stands at 11,720 of its 12,000-character ceiling. |
| 3. A solution unconventional to the codebase | no | | |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | yes | The engineer seat, Johnathan Hyden, at S3 in session 136 | `/sdlc execute` gains `--answer` and `--enough`; each member gains `answer`; `task.py` gains `keep` and `restart`, and `stop` gains `--unit` and `--kind`; `run.json` and `stop.json` are a new format, and `sdlc-rounds.json` moves. Every change is additive, the lines `task.py` prints today keep their wording (SC5.3), only `task.py` reads `sdlc-rounds.json`, and the kit ships as minor 0.22.0. |

## Decisions and open questions

`[Engineer seat · authored]`

- Does the restart ship in `/sdlc execute` or as a personal skill? In `/sdlc execute` (the PO seat, in the requirements).
- How does a headless session take the user's answer? A relaunch with `--answer`, and `--enough` (Consult case 1).
- Where do the run records live? One folder a unit under the git folder, never committed (Consult case 2).
- Where do the restart's steps go? A new `skills/sdlc/flows/restart.md` (Constraints).
- How is a stopped run told from an abandoned one? `stop.json` present: stopped; `run.json` alone: abandoned (Sources).
- What clears the records? `task.py end --run --unit` removes the unit's folder after the draft PR (Interfaces).
- Does the restart check HEAD, or detect a live run? Neither: it checks the branch's name and waits for the user's word (Risks and cost).

No question is open.

## Traceability

### Links out

`[Engineer seat · authored]`

- `docs/features/run-restart.md`: the requirements, r4, signed at r5 (PR #152)
- `docs/features/execution-team.design.md`: the team this design restarts: `task.py`, the flow, the four members
- `docs/usage/the-team.md`: the usage page the units change
- `docs/backlog.md`, Next 24: the feature's origin, session 129's eight `--resume` runs
- `docs/session-metrics.md`, sessions 124 to 133: the cost basis
- ADR 0040 (the team ships in the plugin's `workflows/` folder) and ADR 0037 (a feature document is a pair, one seat each), in `decisions/`

### Record

`[Intake · derived]`

(none: intake writes the record)

## Notes

`[Engineer seat · authored]`

Character counts in this design are the test's count: `Path.read_text`, which reads each Windows line end as one newline. A byte count on a Windows checkout reads one more a line: `execute.md` is 11,785 bytes with 65 line ends, which is how session 136 recorded 11,785.

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/run-restart/contract.yaml`)
