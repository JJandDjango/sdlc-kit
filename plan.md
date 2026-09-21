# Plan - Session 38 (2026-09-21) - tree-view r3: the checks and the solution half

**Deliverable:** `REQUEST_tree-view_2026-09-21.md` at r3, with zero OPEN
marks: two or three checks per criterion, signed by the PO seat, and the
solution half, signed by the engineer seat. Intake (r4) is the next
session's.

Where things stand: r2 carries eight criteria and five decisions, signed by
the PO seat. Session 37 left two questions for r3: whether the request needs
its own ADR, and how the tree shows a red that "prove red" expects. ADR 0029
puts the checks above the line, so the PO seat signs them; the engineer seat
signs the half below.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a question r3 cannot close).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. Open. Branch `session-38-tree-view-r3`, STATE.md records PR #46's merge,
   this plan and its diagram. The open commit lands on your word.
2. The checks. The red-run call comes first, because it shapes SC3's checks.
   Then two or three checks per criterion, SC1 to SC8, in one batch, with
   any error message verbatim. The PO seat signs or amends.
3. The solution half. Two contested calls first: an ADR, and where the
   cursor comes from. Then scope, out of scope, interfaces, constraints,
   units, sequencing, and risks and cost, in one batch. The engineer seat
   signs or amends.
4. r3 into the REQUEST, both signatures in its revision row. If step 3 rules
   an ADR, ADR 0031 is drafted, shown in chat, and committed on your word.
5. Close. STATE.md regenerated, this plan struck through, the close commit
   and the PR. The PR merges on your word.

## Decisions: nine after this plan

Uncontested items come in batches. The three contested calls come one per
message, each with my lean.

1. The open commit.
2. Contested, the red run. Lean: a check's run records the result its task
   expects. A red under "prove red" reads doing, a green under "green" reads
   done, and only a run that misses its expectation reads failed. SC3's six
   values stand.
3. The checks, one batch: the PO seat signs.
4. Contested, an ADR. Lean: yes, 0031. Without one, r2's rulings (the fixed
   task list, the progress file and its writers, run records as display
   evidence only) live only in an untracked file, and this request builds
   the progress file ADR 0024 ruled but left unbuilt.
5. Contested, the cursor. Lean: no cursor field. The cursor is the task
   marked doing, else the first task to do in unit order; the progress file
   holds task states and check runs only.
6. The solution half, one batch: the engineer seat signs.
7. ADR 0031's commit, if step 3 rules one.
8. The close commit and the PR.
9. The merge.

Deferred, not this session:
- `tree-view` after r3: intake to ready (r4), the units, the herdr plugin.
- G1: the pilot's M0 code waits on its criteria review.
- `no-check-reads-the-source-document`: which request carries it.
- `derived-language`, `feature-document`, `spec-doc-type`; the demo intake
  in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b; the G4.6
  finding.
- The engine's uncommitted `plan.md` edit (its cursor ticked after the
  push) is the engine session's to commit.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer, alone in the final paragraph, on every commit that
touches a non-free path; uncontested decisions batched in one message,
contested ones one per message, each with a recommendation; approval
content shown in chat in full.
