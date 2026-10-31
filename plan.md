# Session 137 plan: restart a stopped run, the design document resumed at S5 (backlog Next 24)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the execution node, where `/sdlc execute` runs the team that builds one unit.
**Feature:** run-restart: a stopped team run starts again in a fresh session from a stop record, not by `--resume`.
**Unit:** none yet: this session finishes the feature's design document; the units are named in it.

## 1. The deliverable

`docs/features/run-restart.design.md`, finished from S5 through `/sdlc:product-specification-interview run-restart design` and signed by the engineer seat.

## 2. Where this sits

Session 135 signed the requirements document `docs/features/run-restart.md` at r4 (PR #152). Session 136 wrote the design at r1, S1 to S4 confirmed (scope, out of scope, interfaces, sources), and paused at S5 with its candidate unanswered (PR #153, merged at `8824592`). That candidate rests on one finding: `skills/sdlc/flows/execute.md` stands at 11,785 of its 12,000-character ceiling, so the restart's steps go in a new `skills/sdlc/flows/restart.md`. The state file holds the candidate; the interview shows it again. Intake reads both documents next.

## 3. The steps

1. Branch `session-137-run-restart-design` off main; this plan committed and pushed.
2. Resume the interview at S5: its candidate shown again; on the seat's yes, S1's scope gains `flows/restart.md` and `skills/sdlc/SKILL.md`.
3. S6 to S12, one question at a time: units, order, risks and cost, the four consult cases, decisions, links out, notes. Each section written as it closes.
4. The checks before signing (E1 to E7), then the engineer seat's signature.
5. Wrap: the backlog (Next 24 names intake as its next step), `plan.md` out, the PR, draft until CI is green.

## 4. Where Claude stops for the user

At every interview question: the answers are the engineer seat's. At the signature, and at the PR's review.

## 5. Where Claude goes on alone, and by what rule

Each question comes with a candidate answer drawn from the requirements document, S1 to S4, the code they cite and the user's past rulings, each naming its source. Before a candidate is shown it is tried against the checks, the terms and hostile inputs (an abandoned run with a half-written stop record, two stops of one unit, a restart after the branch moved). The branch, the plan, the wrap and the draft PR: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

None before the interview; the interview is where they are made.

## 7. What could go wrong, already ruled

- A candidate edits the requirements: a design run writes only its own two files; a thing we will not build goes to Decisions as `OPEN:` for the PO seat.
- A later section contradicts a confirmed one (S1 to S4): the interview reopens that section by name, never edits it silently.
- The main session's context passes 40%: Claude names the boundary, and the state file resumes the interview at the exact step.

## 8. This session's cost, with its basis

No agent runs: the interview runs in the main session, and the checks before signing are scripts. Code is read by the line ranges the documents cite, never whole files, to hold the session under 40%.

## 9. Not in this session

- Intake (`/sdlc intake docs/features/run-restart.md`), G1 and the build: later sessions.
- Next action 11 (e2's and e3's advisories) and the backlog's other open items.

## 10. Words

- **team run**: one `/sdlc execute` of one unit by the execution team, from its first task until it passes or stops.
- **stopped run**: a team run that ended short of a pass: a member's question or error, a third failed round, or a task start `task.py start` refuses.
- **stop record**: the file a stop writes so a fresh session can start where the run stopped (`stop.json` in the design).
- **abandoned run**: a team run whose session ended mid-task with no stop written.
- **restart**: an `/sdlc execute` in a fresh session that starts a stopped or abandoned run again at the task where it ended.
- **member**: a workflow agent the flow starts for one task: QA, the QA verifier, the Developer or the Dev verifier.
- **round**: one try at a task; a FAIL sends it back with its reasons, up to 3 rounds.
- **engineer seat**: the person who answers and signs the design document.
- **candidate**: the answer Claude proposes for a section, with its sources; the seat confirms, edits or rejects it.
- **consult case**: one of four situations (an ambiguity, more than one solution, an unconventional solution, a public contract change) where the design records who was asked and what was decided.
- **intake**: `/sdlc intake`, the G0 step that reads both documents and writes the contract.
