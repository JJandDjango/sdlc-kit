| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-30 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r4. Engineer seat: Johnathan Hyden |

# run-restart - Restart a stopped run in a fresh session

`sdlc_development_kit` · seat: engineer Johnathan Hyden · requirements: `docs/features/run-restart.md` · contract: `run-restart`, draft · PR: none · merge SHA: none

## Proposed solution

`[Engineer seat · authored]`

### Scope

- `workflows/tools/task.py`: `stop` and a third `fail` delete the task file and the rounds file today (`task.py:220-249`); they keep the rounds file and write the stop record. A new `restart` command reads the stop record, the progress records and the branch, and prints where the run starts or why it cannot.
- `skills/sdlc/flows/execute.md`: the restart ships in `/sdlc execute`. E2 runs `task.py restart` first; a refused task start stops with a stop record; each passed task saves what it hands on (QA's interface note, the draft, the base commit, the commit, the receipts) in the git folder beside the task file.
- `workflows/qa.js`, `workflows/qa-verifier.js`, `workflows/developer.js`, `workflows/dev-verifier.js`: each takes an `answer` argument, the user's answer with the stop's question or FAIL reasons (SC2.2).
- `tests/test_rounds.py`, `tests/test_team.py`: the new and changed behavior.
- `docs/usage/the-team.md`, `USAGE.md`, `CHANGELOG.md`: the restart, for a user.

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

### Sources

Today the running task stands in `{git folder}/sdlc-task.json` (task, operator and round, no unit: `task.py:214`); the failed reasons a task in `{git folder}/sdlc-rounds.json` (`task.py:159-172`); the task states in `.sdlc/progress/{contract}.yaml`, never committed (`progress.py:3-9`); QA's interface note, its draft and the base commit only in the session, the draft in a scratch folder a fresh session does not have (`execute.md:25, 34, 42`); the branch from `git branch --show-current` at E2 (`execute.md:25`). After the build:

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| State: stopped, abandoned or none | `stop.json` present: stopped; else `run.json` present: abandoned; else none | `stop.json` wins |
| The task to restart at | `stop.json`'s task; else `sdlc-task.json` when its unit matches; else `run.json`'s task in hand | in that order |
| Round n | `stop.json`'s round for a stopped run; else 1 plus the channel's failed rounds in `rounds.json`, as `task.py start` counts today | `rounds.json` wins at start |
| The question or FAIL reasons | `stop.json` | one source |
| The tasks already finished | `run.json`'s task in hand (every earlier task is done); the progress records show each task's state | `run.json` wins; a progress record that disagrees is shown in one line |
| The branch the run stopped on | `run.json`; this session's branch from `git branch --show-current` | compared, never reconciled (SC2.3) |
| The base commit | `run.json` (HEAD at the unit's first start) | one source |
| QA's interface note and test file name | `run.json`'s kept draft | one source |
| The test file | the kept `draft/` before prove-red passed; the working tree's file after | the working tree wins once prove-red passed |
| The commit and the receipts for two-key | `run.json`'s kept values | the kept commit wins over HEAD |
| The user's answer | `--answer`, else the reply in chat | `--answer` wins |

### Constraints

(not yet asked)

### Units

(not yet asked)

### Order

(not yet asked)

## Risks and cost

`[Engineer seat · authored]`

- An abandoned run leaves `sdlc-task.json` behind, and `task.py start` refuses every task while it stands (`task.py:200-202`).
- That file arms the wall only for a member's calls, never the session's own (`hooks/wall.py:12-15`).

## Consult cases

`[Engineer seat · authored]`

(not yet asked)

## Decisions and open questions

`[Engineer seat · authored]`

(not yet asked)

## Traceability

### Links out

`[Engineer seat · authored]`

(not yet asked)

### Record

`[Intake · derived]`

(none: intake writes the record)

## Notes

`[Engineer seat · authored]`

(not yet asked)

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/run-restart/contract.yaml`)
