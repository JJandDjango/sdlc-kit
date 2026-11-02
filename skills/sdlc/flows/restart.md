---
name: sdlc-flow-restart
description: The Restart flow of /sdlc execute - a stopped run takes the user's answer and starts again at the stopped task, in a fresh session.
---

<purpose>
The Restart flow of the `/sdlc` skill: a run of `/sdlc execute {contract} {unit}`
that stopped, or was left abandoned, starts again here. Loaded by
{skill-dir}/flows/execute.md at E2, when the JSON line of `task.py restart`
holds `state` as `stopped` or `abandoned`; its constraints bind here.
{skill-dir} is the directory holding SKILL.md, and {contract}, {unit},
{scratch}, {model}, {effort} and {answer} are as E2 holds them. A restart
reads only the unit's run folder, the progress records and the branch, never
a turn of the stopped session; the values the earlier tasks kept stand in
that folder. The earlier tasks and steps stay done.
</purpose>

<instructions>
R1. HOLD the JSON line of E2 as {stop}, and its `task` as {task}, `operator` as {operator}, `round` as {n}, `kind` as {kind}, `text` as {text} and `kept` as {kept}. When `state` is `abandoned`, SHOW {stop}, then STOP, with no PR: an abandoned run starts nothing until rs4. When {kind} is `fail`, SHOW {stop}, then STOP, with no PR: a stop of kind `fail` restarts nothing until rs3, and no `--go` runs.

R2. SHOW:
    Execution stopped: {contract} unit {unit}, task {task}, round {n} of 3: {text}. Your answer?
    The user's answer comes from `--answer` first, else from chat. A headless session ends its turn at that question, and the user launches `/sdlc execute` again with `--answer`.

R3. HOLD the answer as {reply}, and {answer} as {"stopped": "{text}", "reply": "{reply}"}, each value quoted as {reasons} is in E2. The members get it through `"answer": {answer}`, and only the member of the task that stopped: once that task passes, HOLD {answer} as `null`.

R4. RUN `python {skill-dir}/../../workflows/tools/task.py restart --unit {contract}/{unit} --go --scratch {scratch}`, one Bash call. It removes the stop record and a leftover task file, and writes the kept draft test file under {scratch}/draft.

R5. HOLD the values {kept} holds, under the flow's names. `draft` is {draft}: its `test_file` is {testFile} and its `interface` is {note}; `draft-file` is the copy of the draft now at {scratch}/draft/{testFile}. `receipts` is {receipts} and `commit` is {sha}. A key {kept} lacks is not kept yet, and its step runs when it comes.
    READ {gitdir}/sdlc-run/{contract}/{unit}/run.json and HOLD its `base` as {base} for E5.

R6. Continue at the step of {task}, with the round `task.py start` prints there. No earlier task and no earlier step runs again:
    write-tests: E3
    approve-tests: E4
    prove-red: E5
    green: E6
    approve-commit: E7
    commit: E8
    two-key: E9
    Then each later step runs as execute.md says. When {operator} is `receipts` or `orchestrator`, the task has no member: SHOW the answer, then RUN the command of its step by the answer.
</instructions>
