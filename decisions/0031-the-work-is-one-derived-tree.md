# 31. The work is one derived tree, and every unit follows one task list

Status: accepted
Date: 2026-09-21

## Context

The pilot consumer (ImSimEngine, session 10, against kit v0.14.0) kept its
session plan by hand: a `plan.md` with a generated Mermaid region and a
cursor, 295 lines of rules, session facts and 58 tasks. The user runs
sessions in a terminal multiplexer (herdr), where Mermaid does not render,
and proposed one tree of the whole project, stored as a JSON file or a
folder of small files. Mapped against the kit, every level but one already
has a home: contracts, units and their checks, gates and their findings.
Tasks, approvals and the cursor live only in the hand-kept plan. The
request is `REQUEST_tree-view_2026-09-21.md`, struck at r2 and signed by
both seats at r3.

Bound by: the render computed, never stored, and execution state at
`.sdlc/progress/<id>.yaml`, ruled but unbuilt and never a gate input
(0024); no committed plan (0027); no tooling reads a document's headings,
and checks sit above the line (0029); a finding carries no identifiers
(0023); the human census fixed at six (0015).

Alternatives weighed and rejected: a stored tree, the user's first
proposal, which reopens at project scale the drift 0024 and 0027 closed; a
committed progress file, the changing committed plan 0027 rejects; the
spec doc level in the first cut, which waits for `spec-doc-type` and a
ruling on reading documents; a multiplexer plugin in the kit, which ties
the kit to one terminal program; a stored cursor, as in the pilot's
`tools/plan_graph.py`, a second record of what the task states already
say; a seventh status for an expected red, which amends a signed
criterion; findings under each contract, which repeats every finding and
drops those whose gate is inactive or none.

## Decision

- **The tree is computed at print and never stored.** 0024's rule for the
  unit graph, carried to the whole work: the repository's gates with their
  findings, and its contracts, each with its verdict at every active gate,
  its units, their tasks and their checks. It reads the contracts,
  `.sdlc/config.yaml`, the findings, the progress files, git, and two name
  lists shipped in the package. It reads no document; a feature document
  appears only as a file reference. `taskcontract tree` prints it, queries
  one node, and with `--follow` keeps a pane on the cursor. It writes no
  file.
- **Execution state gets its first writers.** `.sdlc/progress/<id>.yaml`
  holds task states and check runs, written only by `taskcontract
  progress`. It is local (the folder ignores itself), disposable, and read
  by no gate, check, audit or hook. Every record carries its time and
  commit, and an approval the seat that gave it. The cursor is derived
  from the task states, never stored.
- **Every unit follows one task list, shown and never enforced.** Seven
  tasks: approve the test list, write the tests, prove red, green, approve
  the commit, commit, Two-Key PASS. Writing the tests and proving red are
  the spec channel's (G2.5); green is the developer's (G3). The approvals
  are task nodes, not conditions, so the census stays six. This carries
  0027's crosswalk from the unit graph down to each unit: a unit's plan is
  derived too, so it cannot drift from the contract.
- **A run is judged by its expectation.** A run during prove red expects
  red; any other expects green. A check never run reads to do, a red as
  expected doing, a green as expected done, and a miss failed, so a test
  that passes before its code exists shows failed. A run is display
  evidence: its command, result, expectation, commit, and a dirty mark
  when a tracked file differs from HEAD.
- **Each finding stands once, under its gate.** A finding names a gate and
  never a contract, so the gates stand at the repository level with their
  findings: a gate a finding names shows even when inactive, and
  `gate: none` has its own node. A finding records no status, so it shows
  its kind.
- **The notify command is the kit's edge.** When the cursor reaches an
  approval, the pane says so and runs the command set in
  `.sdlc/config.yaml` once, with the node's id in `SDLC_NODE`. A
  multiplexer plugin wraps that command outside the kit.

Recorded non-goals: no stored copy; no edits through the view; no
graphical renderer; no tree across repositories; no spec doc level before
`spec-doc-type`; no change to what any gate checks; no replacement for
STATE.md.

## Consequences

- A session can be followed from a terminal pane, and an agent reads one
  node in at most twenty lines instead of a document.
- The tree shows only what is recorded: until someone writes progress,
  every task reads to do. USAGE gives one command per task; the agent
  personas adopt them in a later request.
- The progress file dies with its clone. One `progress done` per contract
  rebuilds history; until then the kit's thirteen earlier contracts read
  to do.
- A check's id comes from its sketch's trailing parentheses, so a
  re-intake that rewrites a sketch orphans its runs, which then read to
  do, the safe side.
- A finding's closure stays invisible until the finding form gains a
  status field, a later request.
- No gate changes, so 0014's lanes do not apply. The contract schema stays
  1.4.0; the kit goes to 0.15.0.
