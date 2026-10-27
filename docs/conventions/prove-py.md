# prove.py - the red proof and the mutation proof, in one command

Signed by the user in session 105 (2026-10-18): all ten items kept, item 10 as
written. Source: the user's standing practice of session 103 (a script runs
the tests and prints only what an agent needs), recorded in
`docs/backlog.md` Next 4. Status: 🔴 not built; 🟡 built, self-tested (18
tests) and run once on a real placed test (session 105), the brief naming it;
🟢 used by a real drafter run.

Since execution-team's `e2-scripts` (session 125, 2026-10-27) the script is
tracked at `workflows/tools/prove.py`, ships in the plugin and runs the test
command the repository declares, with no prototype (design Interfaces 7 and
9, [the team's page](../usage/the-team.md)). Items 1 to 5, 7, 8 and 10 read
as that unit changed them. The untracked session copy in
`.claude/workflows/tools/` keeps the old behavior until e4 retires it.

The drafter of a unit's test list proves three things by hand: the list is red
against the repo, green against a prototype, and each pinned behavior is caught
by a one-line mutation. Session 103's `s6-release` drafter spent 299K tokens and
124 tool calls, mostly copying, mutating, running and restoring. `prove.py` does
that plumbing and prints the minimum.

| # | Feature | Status |
| :-: | :-- | :-: |
| 1 | **Command**: `python workflows/tools/prove.py --scratch DIR --test PATH [--at REV] [--mutations FILE]`, run from the repository root, prints one compact JSON object. It exits 0 only when red holds, or every mutation is caught. | 🟢 |
| 2 | **Setup**: exports REV (default HEAD) afresh into `DIR/export/` each run, and copies the draft from `DIR/draft/PATH` over `export/PATH` when one sits there; else the committed file at PATH runs. The repository is never changed. | 🟢 |
| 3 | **Red run**: runs `test.build` when declared, then `test.file` with `{file}` as PATH, or `test.command` when no `file` is declared, from the export's root. `red_ok`: for a pytest command every test failed on an assertion, none on a fixture, import or collection error; for any other command the run exited 1. | 🟢 |
| 4 | **Green run**: retired in `e2-scripts` with the prototype (the package copy, the green run, the package probe). | retired |
| 5 | **Mutation loop**: with `--mutations`, a JSON list of `{name, file, old, new}`, `file` relative to the export's root. The unmutated export must pass first. Each mutation is applied, run, and restored byte for byte, even after a crash; `caught_by` lists failing ids for pytest and PATH otherwise, or "not caught". Refuses an `old` that matches zero times or more than once. | 🟢 |
| 6 | **Compact output**: each run prints the summary line, failing ids and first assertion line only. The full log goes to `DIR/logs/<run>.log`, and the JSON names its path. | 🟢 |
| 7 | **Harness hygiene**: sets `PYTHONUTF8` and decodes with `errors="replace"`. Default timeout is 600 s a run, with no popup window and stderr in `DIR/logs/`. Exit codes: 0 all hold, 1 a check failed, 2 usage, 254 the test command never started. | 🟢 |
| 8 | **Self-test**: `tests/test_prove.py` on a toy package, and `tests/test_declared_command.py` on a pytest fixture and a batch-file fixture. | 🟢 |
| 9 | **Drafter wiring**: the `spec-channel-drafter.js` brief names this one command in place of its red, prototype and mutation recipe. It names the untracked session copy; e4 points the team at this script. | 🟢 |
| 10 | **Home**: `workflows/tools/prove.py`, tracked and shipped in the plugin. | 🟢 |

## Readings the build chose where the list was silent

- Item 7: the timeout default is 600 s, so an override exists: `--timeout SECONDS`.
- Item 3: red prints only the tests that did not fail on an assertion
  (`passed`, `skipped`, `not_assertion` with each one's exception name), since
  the expected state is every test failing.
- Item 5: each run exports afresh, so a mutation a killed run left cannot
  survive into the next; the journal and `recovered` that guarded the
  prototype across runs retired with it (`e2-scripts`). When the unmutated
  export does not pass, the loop is skipped: every mutation would read as
  caught.
- Item 6: `log` prints relative to the scratch folder, which the JSON names
  once under `scratch`.
- A mutation that makes a run time out reads `caught_by: ["(timeout)"]`.
- Measure: the first drafter run that uses it (the next unit's) is compared
  in `docs/session-metrics.md` with `s6-release`'s 299K tokens and 124 calls.
  Items go 🟢 on that run. This session added no metrics row, since the record
  keeps rows for sessions that ship a unit.

## Why this page is not under `docs/features/`

The tree reads feature documents from `docs/features/`, so a page there would
enter it as a feature. `prove.py` is a workflow tool, not a kit feature.
