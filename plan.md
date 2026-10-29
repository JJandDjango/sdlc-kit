# Session 135 plan: restart a stopped run, the requirements document (backlog Next 24)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where `/sdlc execute` runs the team that builds one unit.
**Feature:** run-restart (proposed id): a stopped team run starts again in a fresh session from a stop record, not by `--resume`.
**Unit:** none yet: this session writes the feature's requirements document, the first of its two documents.

## 1. The deliverable

`docs/features/run-restart.md`, the requirements document, written through `/sdlc:product-specification-interview` and signed by the PO seat.

## 2. Where this sits

Kit 0.21.1 ships the execution team (tag `v0.21.1` at `ac0f228`). Today `task.py stop` and a third failed round delete the task file and the rounds file, so a stopped run keeps no state. Session 129 went on by `--resume`, and the headless session's starting context grew from 45K to 281K tokens over eight runs (31.0M cache reads). Backlog Next 24 (`docs/backlog.md:268-281`) names the feature; its precondition, e6 shipping 0.21.0, is met. A feature starts as an interviewed document, never as a request typed from a sketch.

## 3. The steps

1. Branch `session-135-run-restart` off main; this plan committed and pushed.
2. Opening (O1 to O6): the id, the origin, the title, the PO seat, and the backlog's Next 24 entry as material; the document written as r1.
3. The request half (Q1 to Q15), one question at a time, each section written into the document as it closes; then Terms and the Gherkin scenarios.
4. The checks before signing (P1 to P7), then the PO seat's signature.
5. Wrap: the backlog (Next 24 names the design run as its next step), `plan.md` out, the PR, draft until CI is green.

## 4. Where Claude stops for the user

At every interview question: the answers are the user's. At the PO seat's signature, and at the PR's review.

## 5. Where Claude goes on alone, and by what rule

Candidate answers drawn only from the user's own words and the records the backlog cites, each naming its source. The branch, the plan, the wrap and the draft PR: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

None before the interview; the interview is where they are made.

## 7. What could go wrong, already ruled

- The interview drifts into the solution (file names, `task.py` options): those belong to the design run; the requirements half names behavior a user sees.
- The material's "left out" line (a member that waits on the parent) is read as settled: it is shown as material and confirmed or struck like any other line.
- The main session's context passes 40%: Claude names the boundary, and the state file resumes the interview at the exact step.

## 8. This session's cost, with its basis

No agent runs: the interview runs in the main session, and the checks before signing are scripts. The cost is the session's own context, held under 40% by reading the flows one at a time.

## 9. Not in this session

- The design run (`/sdlc:product-specification-interview run-restart design`), intake and G1: later sessions.
- Next actions 11 (e2's and e3's advisories) and the backlog's other open items.

## 10. Words

- **run**: one `/sdlc execute` of a unit: the Orchestrator starts each member for each task until the unit passes or stops.
- **stop**: a run's end short of a pass: a member's question, `task.py stop`, or a third failed round.
- **stop record**: the proposed file a stop writes, so a fresh session can start where the run stopped.
- **`--resume`**: Claude Code's flag that continues an old session with its whole context.
- **headless session**: `claude -p`, a session with no terminal, its output in a file.
- **member**: a workflow agent the flow starts for one task: QA, the QA verifier, the Developer or the Dev verifier.
- **round**: one try at a task; a FAIL sends it back with its reasons, up to 3 rounds.
- **PO seat**: the person who answers and signs the requirements half.
- **requirements document**: `docs/features/{id}.md`, the request half; its design document, `docs/features/{id}.design.md`, comes next.
