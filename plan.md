# Session 174 plan: fold `E:\herdr-sdlc` into the kit as an opt-in `herdr/` folder

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session flow: how a kit session stops for the user, wraps and starts again.
**Feature:** session-loop (contract `session-loop`): l1 to l3 built (l3 on draft PR #178); l4 and kit 0.23.0 wait on this fold.
**Deliverable:** backlog Next 32: the herdr tools move into the kit, so 0.23.0 ships one repo.

## 1. The deliverable

`herdr_loop.py`, `herdr_seat.py`, their 109 tests and their README in the kit, the session-loop design and contract naming the new paths, on a draft PR stacked on #178 with green CI.

## 2. Where this sits

Session 173 built l3 at `E:\herdr-sdlc` `31918d6` (README `1602d9a`), then the user ruled the second repo a cost (`docs/backlog.md:496-505`): no remote, no CI, and `/sdlc execute` cannot commit there. ADR 0031's clause "A multiplexer plugin wraps that command outside the kit" (`decisions/0031-the-work-is-one-derived-tree.md:73-74`) gives way; its real line stays: the kit's core imports nothing from herdr and runs no herdr command. Today no file under `taskcontract/`, `skills/`, `workflows/` or `hooks/` names herdr.

Paths to change: design `docs/features/session-loop.design.md:29,39,52,81,117,144,156,180` and its state file's scope; contract `specs/session-loop/contract.yaml:26-28`; `.sdlc/config.yaml:59-60`; `docs/usage/the-tree.md:282-284`; `ARCHITECTURE.md`'s folder map.

## 3. The steps

1. Branch `session-174-herdr-fold` off `session-172-l3-loop-stops` at `32c0284`; this plan committed and pushed.
2. ADR 0043: the herdr tools ship in the kit's opt-in `herdr/` folder; it keeps ADR 0031's line and supersedes its outside-the-kit clause in part.
3. The fold commit: `herdr_loop.py`, `herdr_seat.py` and `README.md` copied into `herdr/`, the three test files into `tests/`; `pyproject.toml` adds `herdr` to pytest's `pythonpath`; paths in docstrings, README, `.sdlc/config.yaml`, `the-tree.md` and `ARCHITECTURE.md`; the source sha in the message.
4. Receipts: the three herdr test files alone (109 expected), then the whole suite once.
5. Design r13, the text row (Scope, Out of scope, Interfaces, Constraints, Risks, Consult case 4, Links out, the state file's `answers.scope`), and r14, the measured row (signing flow E1 to E3). Stop: the engineer seat signs r13.
6. r15 `Signed:`; re-intake r16: the contract's three `E:/herdr-sdlc/` scope lines become `herdr/`; validate ready; one `Intake r16:` commit.
7. Close: backlog Next 32 done and Next 30's text; `plan.md` out; push; a draft PR based on `session-172-l3-loop-stops`, readings at the top; CI green.

## 4. Where Claude stops for the user

At step 5, for the engineer seat's signature, and at the PR's review and merge (#178 merges first).

## 5. Where Claude goes on alone, and by what rule

Steps 1 to 4, 6 and 7: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation), and the user ruled the fold in session 173.

## 6. Rulings needed

The signature at step 5 only. Readings, each listed in the PR body:

1. A copy, not a history import: the scope check (G4.12) reads every commit in the PR's range, and herdr-sdlc's ten commits carry no `Contract:` trailer (SC002). `E:\herdr-sdlc` stays on disk as the history; the shas the backlog cites resolve there. Deleting it is the user's call.
2. The tests join the kit's `tests/`, so CI runs them and the wall's `functional` covers them; `herdr/` holds the two modules and the README.
3. `herdr_seat.py` moves under session-loop's contract, its behavior unchanged; the design's Out of scope line on it says so.
4. The requirements document keeps its two `E:\herdr-sdlc` lines: one cites the hook as it stood at signing, one records session 163's decision. Neither is a sentence the fold makes false, so no requirements signature.
5. ADR 0043 is written accepted on the user's session-173 ruling.

## 7. What could go wrong, already ruled

- An import collision on `pythonpath`: no kit module is named `herdr_loop` or `herdr_seat`.
- `python -P` drops the cwd from `sys.path`: pytest's `pythonpath` adds `herdr` from the rootdir regardless.
- A test that reaches the real herdr or `gh`: every test passes a fake runner, unchanged by the copy.
- CI's scope check on `herdr/` paths before re-intake: the PR stays draft until step 6.

## 8. This session's cost, with its basis

No agents: the copy is mechanical and the code unchanged, so the receipts are the moved tests rerun in the kit and CI. Main-session context only, about 150K to 200K tokens; one suite run, about 390 s.

## 9. Not in this session

- l4 and kit 0.23.0; the advisories carried to l4 (`wait_idle` holds on an exit or hang after a `continue`; `restart()` ignores herdr's exit codes).
- A test pinning ADR 0043's line (no core file names herdr).
- Deleting `E:\herdr-sdlc`.

## 10. Words

- **fold**: the move of `E:\herdr-sdlc`'s files into the kit.
- **launcher**: `herdr_loop.py`, run in the user's own pane; it restarts a Claude pane's session.
- **tree hook**: `herdr_seat.py`, the tree pane's `notify` command; it flags a waiting seat in herdr's sidebar.
- **scope check**: CI's G4.12 job; each commit's changed paths must stand in the scope of the contract its `Contract:` trailer names.
- **re-intake**: intake run again on a revised design, editing only what the revision names in the contract.
- **seat signature**: a `Signed:` row in the document's revision table, the seat's alone to give.
- **reading**: a call made where the signed documents were silent; each is listed in the PR body.
