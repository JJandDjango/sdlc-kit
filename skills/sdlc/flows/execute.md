---
name: sdlc-flow-execute
description: The Execute flow of /sdlc - one unit of a ready contract run through seven tasks by the execution team, each task opened, run, shown and recorded in turn.
---

<purpose>
The Execute flow of the `/sdlc` skill: `/sdlc execute {contract} {unit}` runs
one unit of a ready contract from its tests to its Two-Key grade. Each task
has one operator: a member, started with the Workflow tool, or a command run
here. The flow shows one line a task and records the task done only on a
pass. Dispatched by {skill-dir}/SKILL.md on `/sdlc execute`; its constraints
and criteria bind here. {skill-dir} is the directory holding SKILL.md.
{contract} is the second argument and {unit} the third. The plugin root is
{skill-dir}/../.. . {plugin} is `sdlc` when the plugin is installed, else the
name of the plugin root's folder, when the session runs with `--plugin-dir`.
</purpose>

<instructions>
E1. READ `specs/{contract}/contract.yaml` and HOLD its `scope` list as {scope}. When the contract has no unit {unit}, PRINT on stdout, then STOP:
    Execution did not start: no unit {unit} in specs/{contract}/contract.yaml.
    Otherwise RUN `python -m taskcontract validate specs/{contract}/contract.yaml --profile ready`, one Bash call. On any non-zero exit PRINT on stdout, then STOP:
    Execution did not start: specs/{contract}/contract.yaml is not ready-green.

E2. RUN `python -m taskcontract node execution --print`, one Bash call, and SHOW its output, quoting `Node execution: claude --model {model} --effort {effort}`, before the header; HOLD {model} and {effort}. READ `.sdlc/config.yaml` and HOLD its `test:` block as {test}, its `wall:` block as {wall} and `scope_check.free_paths` as {free_paths}, the entries joined by a comma and a space. RUN `git rev-parse --show-toplevel` as {repo}, `git rev-parse --absolute-git-dir` as {gitdir} (the folder that holds the task file) and `git branch --show-current` as {branch}, one Bash call each. HOLD {scratch}, the session's scratch folder outside the repository. HOLD {argv0}, the first word of `test.command`. SHOW once, before any task:
    Execution: {contract} unit {unit}, {model} at {effort}, test command: {argv0}
    The rule for each task, E3 to E9, in this order: its `task.py start`; its member; its line; its `progress done`; then `rm -f {gitdir}/sdlc-task.json`, one Bash call. When `task.py start` exits 1, SHOW its line and STOP. {verdict} is `PASS`, or another verdict with its reasons in parentheses joined by `; `, as `FAIL (2 sketches failed)`. A member that returns `error` gets `ERROR ({error})` in place of `done`. When a member returns `error`, a verdict other than `PASS`, or a non-empty `questions`, SHOW the line, then each reason or question on its own line indented two spaces, RUN `rm -f {gitdir}/sdlc-task.json`, one Bash call, and STOP: the task is not recorded done.

E3. RUN `python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} --task write-tests --operator qa`, one Bash call. START `{plugin}:qa` with the Workflow tool and the args `{"model": "{model}", "effort": "{effort}", "unit": "{unit}", "contract": "{contract}", "repo": "{repo}", "scratch": "{scratch}", "pluginRoot": "{skill-dir}/../..", "test": {test}, "wall": {wall}, "sources": ["specs/{contract}/contract.yaml", "docs/features/{contract}.md", "docs/features/{contract}.design.md"]}`. QA writes the draft at `{scratch}/draft/{testFile}`: `draft.test_file` is {testFile}, and `draft.interface` is {note}. HOLD {testFile}, {note} and the whole `draft` as {draft}. SHOW:
    Task write-tests: QA, round 1: done
    Then RUN `python -m taskcontract progress done {contract}/{unit}/write-tests`, one Bash call.

E4. RUN `python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} --task approve-tests --operator qa-verifier`, one Bash call. START `{plugin}:qa-verifier` with the Workflow tool and the args `{"model": "{model}", "effort": "{effort}", "unit": "{unit}", "contract": "{contract}", "repo": "{repo}", "scratch": "{scratch}", "pluginRoot": "{skill-dir}/../..", "task": "approve-tests", "testFile": "{testFile}", "contractPath": "specs/{contract}/contract.yaml", "requestPath": "docs/features/{contract}.md", "designPath": "docs/features/{contract}.design.md", "draft": {draft}}`. SHOW:
    Task approve-tests: QA verifier, round 1: {verdict}
    Then RUN `python -m taskcontract progress done {contract}/{unit}/approve-tests --by qa-verifier`, one Bash call.

E5. RUN `python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} --task prove-red --operator qa-verifier`, one Bash call. START `{plugin}:qa-verifier` with the Workflow tool and the args `{"model": "{model}", "effort": "{effort}", "unit": "{unit}", "contract": "{contract}", "repo": "{repo}", "scratch": "{scratch}", "pluginRoot": "{skill-dir}/../..", "task": "prove-red", "testFile": "{testFile}"}`. SHOW:
    Task prove-red: QA verifier, round 1: {verdict}
    On PASS, READ `{scratch}/draft/{testFile}` and WRITE it unchanged to `{testFile}`. Then RUN `python -m taskcontract progress done {contract}/{unit}/prove-red`, one Bash call.

E6. RUN `python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} --task green --operator developer`, one Bash call. START `{plugin}:developer` with the Workflow tool and the args `{"model": "{model}", "effort": "{effort}", "unit": "{unit}", "contract": "{contract}", "repo": "{repo}", "branch": "{branch}", "testFile": "{testFile}", "scratchRoot": "{scratch}", "files": {scope}, "sources": ["specs/{contract}/contract.yaml", "docs/features/{contract}.md", "docs/features/{contract}.design.md"], "interface": {note}, "test": {test}, "wall": {wall}}`. SHOW:
    Task green: Developer, round 1: done
    Then RUN `python -m taskcontract progress done {contract}/{unit}/green`, one Bash call.

E7. RUN `python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} --task approve-commit --operator receipts`, one Bash call. WRITE `{scratch}/receipts.json`, a JSON list holding `test.command` as its one argv list. RUN `python {skill-dir}/../../workflows/tools/receipts.py --repo {repo} --receipts {scratch}/receipts.json --out {scratch}/receipts`, one Bash call, and HOLD its JSON as {receipts}. SHOW, with its exit code:
    Task approve-commit: receipts, round 1: exit {code}
    When the code is not 0, RUN `rm -f {gitdir}/sdlc-task.json`, one Bash call, and STOP. Otherwise RUN `python -m taskcontract progress done {contract}/{unit}/approve-commit --by receipts`, one Bash call.

E8. RUN `python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} --task commit --operator orchestrator`, one Bash call. WRITE `{scratch}/commit-message.txt`; its final paragraph holds the trailers `Contract: {contract}` and `Theory: {why}`. RUN `git add` naming the unit's files, one Bash call, then `git commit -F {scratch}/commit-message.txt`, one Bash call, then `git rev-parse --short HEAD` as {sha}, one Bash call. The flow stages and commits nowhere else. SHOW:
    Task commit: Orchestrator: {sha}
    Then RUN `python -m taskcontract progress done {contract}/{unit}/commit`, one Bash call.

E9. RUN `python {skill-dir}/../../workflows/tools/task.py start --unit {contract}/{unit} --task two-key --operator dev-verifier`, one Bash call. START `{plugin}:dev-verifier` with the Workflow tool and the args `{"model": "{model}", "effort": "{effort}", "unit": "{unit}", "contract": "{contract}", "repo": "{repo}", "branch": "{branch}", "commit": "{sha}", "contractPath": "specs/{contract}/contract.yaml", "requestPath": "docs/features/{contract}.md", "designPath": "docs/features/{contract}.design.md", "freePaths": "{free_paths}", "receiptsResult": {receipts}}`. SHOW:
    Task two-key: Dev verifier, round 1: {verdict}
    After the Dev verifier's line shows PASS, START `{plugin}:qa-verifier` with the Workflow tool and the args `{"model": "{model}", "effort": "{effort}", "unit": "{unit}", "contract": "{contract}", "repo": "{repo}", "scratch": "{scratch}", "pluginRoot": "{skill-dir}/../..", "task": "two-key", "testFile": "{testFile}", "commit": "{sha}", "contractPath": "specs/{contract}/contract.yaml", "requestPath": "docs/features/{contract}.md"}`. SHOW, with a PASS carrying ` (mutations: {caught} of {total} caught)` read from the `mutations` of its result:
    Task two-key: QA verifier, round 1: {verdict}
    When both verifiers are PASS, RUN `python -m taskcontract progress done {contract}/{unit}/two-key`, one Bash call. This is the last step: the flow ends here, with no other final line.
</instructions>
