# Contributing to sdlc_development_kit

Read this before working or committing.

## Set up and test
Install `textual>=8.2,<9`, `pytest>=8`, `jsonschema>=4.18` and `PyYAML>=6`, then run `python -P -m pytest tests -q` (3 to 6 minutes). CI runs on every PR.

## Workflow
- Every change is a PR; main's ruleset requires one.
- A release is a PR, a merge commit, an annotated tag at the merge, then a self-pin through its own PR.
- A feature starts as a feature document from `/sdlc:product-specification-interview`, never a request typed from a sketch.
- `plan.md` lives on the work branch; its last commit removes it, so main holds no plan.
- A handoff mid-work stays in that work's own folder, never a top-level file.
- Two-Key: a unit is done only when the verifier, re-running the tests, grades PASS.
- A session ships one deliverable. Its context targets 200K tokens and stops at 400K.
- At close, the next deliverable goes first in `docs/backlog.md`'s Next.

## Delegation
- The signed feature and design documents are the gate: no approval before the final PR review. Claude commits units and records approvals `--by claude`.
- The user holds seat signatures, each release and tag, the work PR's merge, and any ruling that changes a signed contract sentence, a ratified term or an ADR.
- A reading no document settles is ruled from the documents' purpose and listed at the top of the PR body.
- Tripwire: an item returns to the user on one escaped defect traced to Claude's approval.

## House rules
Full wording and ADR links: [house rules](docs/conventions/house-rules.md).
- **Decisions get recorded**: an ADR for a choice a future you would question. ADRs are append-only; supersede, never edit.
- **Gates**: a gate is a phase's blocking venue, a condition a check on it; registry `docs/gates.md`, one deep page a gate (ADR 0003, 0004).
- **Task contracts**: `specs/<id>/contract.yaml`, valid under `python -m taskcontract validate` (0006); unit order in `depends_on` (0024); `confirmed_by` seats recorded (0025, 0030).
- **The raw request stays the requester's**: a change after ready re-intakes (0026).
- **Commits name their contract**: a `Contract: <id>` trailer alone in the final paragraph (0027).
- **Register boundary**: controlled register where prose is executed, free elsewhere (0022).

## Recipes
How each kind of unit is built, with session lessons: [standing practice](docs/conventions/standing-practice.md).
