### `taskcontract new <id>` (or `/sdlc new <id>`)
Scaffolds the 8-field contract skeleton at
`specs/<id>/contract.yaml` with inline field guidance. The id must
match `^[a-z][a-z0-9-]{2,63}$`.

### `/sdlc audit`
Report-only health check — exit 0 clean / 1 findings / 2 no `.sdlc`
here. Checks: config + ledgers parse, every contract validates, the
payload surfaces exist, CI job present. It never writes; fixes stay
with you.

### The session hook — `.sdlc/hooks/protect_specs.py` 🟢

> 🟢 **Shipped** (kit 0.13.0, [ADR 0027](../../decisions/0027-playbook-crosswalk-and-closures.md)
> gaps 1, 2, and 6a, contract `specs/playbook-guardrails/`).

🟢 `/sdlc init` renders a Claude Code hook at `.sdlc/hooks/protect_specs.py`
and wires it into `.claude/settings.json` (a merge target: written when
absent, printed when present) for Edit, Write, MultiEdit, and NotebookEdit.
Under `specs/` the hook denies: a contract that validates `ready` ("a
change re-intakes"), a term with `status: ratified` ("a class-S edit in
review"), and every other file there (the spec channel). Drafts stay
writable: intake edits the contract it is authoring. With no kit installed
the hook denies everything under `specs/`. The wired command names
`python`; where only `python3` resolves (macOS, some Linux), change the
word in the settings file, which is yours after the first write.

🟢 Outside `specs/`, the hook warns, never denies, when a write leaves the
bound contract's `scope`. The session's contract is the branch name when
`specs/<branch>/` exists, else `SDLC_CONTRACT`; with neither, the hook
stays silent. Denial outside the spec channel waits for wave B.

🟢 An organization pins the hook for every session with managed settings,
which user and project settings cannot override: copy
`skills/sdlc/templates/reference/managed-settings.json` from the kit to
the platform's managed-settings path (`/Library/Application
Support/ClaudeCode/managed-settings.json` on macOS,
`/etc/claude-code/managed-settings.json` on Linux,
`C:\ProgramData\ClaudeCode\managed-settings.json` on Windows). Its command
runs the hook only where `.sdlc/hooks/protect_specs.py` exists, so repos
without the kit are untouched. `/sdlc update` tracks drift on the rendered
hook (kit-owned), never on your settings file.

### `taskcontract scope-check` — G4.12 and the `Contract:` trailer 🟢

🟢 Every commit names its contract in a git trailer, parsed like the
`Theory:` trailer:

```
Contract: csv-export
```

🟢 `python -m taskcontract scope-check --base <sha>` reads the trailers of
the range, resolves each contract's `scope`, and fails on a path outside
it: SC001 (a path outside scope), SC002 (a commit with no trailer touching
a bound path), SC003 (a trailer naming no contract). A commit with no
trailer passes when it touches only free paths (`scope_check.free_paths`
in `.sdlc/config.yaml`, seeded with the docs spine, the plan, the
changelog). `--json` emits the findings envelope; exit 1 on findings, 2
when no base can be resolved.

🟢 The scaffolded CI runs it on every pull request as G4.12, "the diff
stays within its contract's scope" (registry: [docs/gates.md](../gates.md)).

### `.sdlc/REVIEW.md` — the advisory review pass 🟢

🟢 `/sdlc init` renders `.sdlc/REVIEW.md`, yours to edit (consumer class):
what a reviewer, human or agent, checks on a pull request beyond the
mechanical gates: the diff against the contract's `scope` and `non_goals`,
each unit's `acceptance_sketch` against the tests that landed, and the
write surface (nothing under `specs/`, no test weakened). The pass is
advisory: it blocks nothing. An escape it should have caught adds an
agent eval in wave B (`playbook-loop`).
