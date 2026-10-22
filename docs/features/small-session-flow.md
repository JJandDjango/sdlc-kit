| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-21 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: Johnathan Hyden |
| 2026-10-21 | Johnathan Hyden | r2: Measured: the checks before signing, on the request half: 44 findings (CL006 41, CL008 3); ready checks 1 to 8: 1 OPEN |
| 2026-10-22 | Johnathan Hyden | r3: Measured: the checks before signing, on the request half: 40 findings (CL006 40); ready checks 1 to 8: 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r4: The request half finished: 11 sections written, 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r5: Signed: request half. The PO seat signs r4 |
| 2026-10-22 | intake | r6: Parked: Ready check 12: the reader's refusals of a node with no row, a row with no node, and an edge with no label have no drawn message. |
| 2026-10-22 | intake | r7: Ready: contract `small-session-flow` validates ready-green, derived from r4; the PO seat (Johnathan Hyden) signed the request half at r4 (r5) |

# small-session-flow - Workflow Nodes

`sdlc_development_kit` · seat: PO Johnathan Hyden · contract: `small-session-flow`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As the human developer, I want each step of the kit's flow to run as a workflow node with its own agent model, effort and operators, so that every session ends with one reviewed deliverable inside 400K tokens and the next session starts primed on where it stopped.

## Description

`[PO seat · authored]`

- Feature document: Opus at high or xhigh. The user and the PO team review; open questions get answered.
- Design document: Opus at high or xhigh. It produces the plan and task list; the user reviews.
- Execution: Sonnet at high. The orchestrator launches one subagent per task. A failed verifier sends Dev or QA back, up to 3 rounds. It ends in a draft PR for the user.
- Self PR review: agents plus the user's judgment, before final review.
- Operators apply to execution only (Sonnet at high): Developer (code and unit tests, cannot see functional tests), QA (functional tests, cannot see code or unit tests), Dev verifier, QA verifier, Orchestrator (asks the user on a question or repeated failure). The two document stages use seats: the PO seat for the requirements document, the engineer seat for the design document.
- Sessions: one small deliverable, under 200K tokens ideal and 400K hard. Closing saves notes through Cairn; the next session primes from them.
- Workflow file: one committed `.md` file in mermaid form. The diagram holds the order and hand-offs of the nodes; a table beside it holds each node's agent model, effort, and operator or seat.

## Background

`[PO seat · authored]`

The kit already splits the Dev and QA channels, and the 2026-10-12 process-cost ruling puts the drafter, developer and grader on Opus. Why now: a session that grows past 400K tokens raises cost and hallucination risk, and the user plans to make each step a workflow node so that nodes can later be swapped at the user's discretion.

### Existing behavior touched

1. Both agents use `model: inherit` (`agents/sdlc-developer.md:5`, `agents/sdlc-verifier.md:5`). Regression check: SC2.1.
2. The workflows set effort `high` and no agent model; the receipts step runs Haiku at low (`.claude/workflows/spec-channel-drafter.js:98`, `unit-developer.js:45`, `test-retirer.js:73`, `two-key-unit-verifier.js:139-140`). Regression checks: SC2.1, SC2.2.
3. The interview skill pins no agent model or effort (`skills/product-specification-interview/`, no match for either). Regression checks: SC2.1, SC2.2.
4. The session boundary is named before 40% of the context, and an agent is stopped past about 400K tokens (`docs/conventions/standing-practice.md:65`, `:282`); `CONTRIBUTING.md` states neither. Regression check: SC3.1.

## Success criteria

`[PO seat · authored]`

- SC1: The four stages are nodes of one committed `.md` workflow file in mermaid form, each node carrying its agent model, effort, and operator or seat, and each stage starts from the files the previous node left.
- SC2: Each node runs at the agent model and effort its row in the workflow file's settings table states.
- SC3: A session stays under 400K tokens, with 200K the target.
- SC4: A session closes with Cairn notes, and the next one starts primed from them.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added.
- No mechanism substitutes one node for another against a node contract (what a node reads and writes). A later feature adds it, after a second version of a node exists.
- The execution team (orchestrator, QA agent, verifiers, retry cap, draft PR, self-review) is a second document.
- No operators for the two document stages; they use seats.

## Prerequisites

`[PO seat · authored]`

1. `/cairn status` works for session notes (exists).
2. Changes to agent definitions pass the enforcement-layer approval channel (exists; class E, `docs/operators.md`).

## Acceptance criteria

`[PO seat · authored]`

### Checks

SC1: the workflow file
- SC1.1: verify the workflow file holds one mermaid flowchart with exactly four nodes, one per stage.
- SC1.2: verify each node in the diagram has one settings row naming its agent model, effort, and operator or seat.
- SC1.3: verify each edge of the diagram carries a label naming the file handed to the next node.

SC2: settings from the table
- SC2.1: verify that changing a node's agent model in its row changes the agent model that node runs at, with no other file edited.
- SC2.2: verify changing a node's effort in its row changes the effort that node runs at, with no other file edited.
- SC2.3: verify that a node whose row lacks an agent model or an effort does not start.

SC3: session size
- SC3.1: verify `CONTRIBUTING.md` states the session's one deliverable, 200K-token target and 400K-token limit, and `docs/conventions/standing-practice.md` still names the 40% boundary.
- SC3.2: verify the session shows a warning when its context passes 200K tokens.
- SC3.3: verify the session is told to close when its context passes 400K tokens.

SC4: session notes
- SC4.1: verify that at close the notes name the session's last done work and the next deliverable.
- SC4.2: verify that a new session's first `/cairn status` names that same next deliverable.

### Error messages, verbatim

- SC2.3: `Node {id} did not start: its row in the workflow file has no {agent model or effort}.`
- SC3.2: `This session has passed 200K tokens, the target. Finish the deliverable and close.`
- SC3.3: `This session has passed 400K tokens, the limit. Save the notes and close now.`

## Decisions and open questions

`[PO seat · authored]`

- Execution runs on Sonnet at high (user ruling 2026-10-21).
- Retry cap is 3 rounds per task; the 5 loops inside one check stay (user ruling 2026-10-21).
- Cairn carries the session notes (user ruling 2026-10-21).
- Operators apply to execution only; the document stages use seats (user ruling 2026-10-21).
- The execution team (the third failed round escalating to the user, the Dev/QA wall, the draft PR) moves to a second document, "Execution team" (user ruling 2026-10-21).
- The workflow is one committed `.md` file in mermaid form: the diagram holds order and hand-offs, and a table beside it, keyed by node id, holds each node's agent model, effort, and operator or seat. That table is the one place for stage settings (user ruling 2026-10-21).
- Swapping nodes is out of this feature; a later feature adds it, after a second version of a node exists (user ruling 2026-10-21).

## Notes

`[PO seat · authored]`

Carried to the "Execution team" document: the existing behavior of the 5-loop caps (`agents/sdlc-developer.md:72`, `agents/sdlc-verifier.md:62`) and of the Opus 5.5 ruling (`NOTES_process-cost_2026-10-12.md:110`), and two open questions: whether the QA verifier runs mostly through `prove.py` (recommended, not ratified), and whether the Sonnet ruling supersedes the 2026-10-12 process-cost ruling in an ADR.

## Appendix

### Gherkin

`[PO seat · derived from r4]`

```gherkin
Scenario: SC1.1 The workflow file holds one flowchart of four nodes
  Given the workflow file
  When its mermaid diagrams are read
  Then it holds one flowchart with exactly four nodes, one per stage

Scenario: SC1.2 Each node has one settings row
  Given the diagram's nodes
  When each is looked up in the settings table
  Then each has one row naming its agent model, effort, and operator or seat

Scenario: SC1.3 Each edge names the file it hands over
  Given the diagram
  When its edges are read
  Then each edge carries a label naming the file handed to the next node

Scenario: SC2.1 A changed agent model takes effect from the row
  Given a node's row
  When its agent model is changed and no other file is edited
  Then the node runs at the changed agent model

Scenario: SC2.2 A changed effort takes effect from the row
  Given a node's row
  When its effort is changed and no other file is edited
  Then the node runs at the changed effort

Scenario: SC2.3 A node with an incomplete row does not start
  Given a node whose row lacks an agent model or an effort
  When the node is asked to start
  Then it does not start

Scenario: SC3.1 The session size is stated and the 40% boundary stands
  Given CONTRIBUTING.md and docs/conventions/standing-practice.md
  When they are read
  Then CONTRIBUTING.md states the session's one deliverable, the 200K-token target and the 400K-token limit
  And docs/conventions/standing-practice.md still names the 40% boundary

Scenario: SC3.2 A session warns at 200K tokens
  Given a session
  When its context passes 200K tokens
  Then it shows a warning

Scenario: SC3.3 A session is told to close at 400K tokens
  Given a session
  When its context passes 400K tokens
  Then it is told to close

Scenario: SC4.1 A closing session's notes name what is done and what is next
  Given a session that is closing
  When its notes are written
  Then they name the last done work and the next deliverable

Scenario: SC4.2 The next session's first status names the same deliverable
  Given a new session after that close
  When /cairn status first runs
  Then it names that same next deliverable
```

### Terms

`[PO seat · authored]`

Decided at the interview's Q14 (2026-10-21). Two map to the kit's ratified terms: Seat (`intake-seat`, by its alias) and Operator (`operator`). The other five become terms to ratify at intake.

- **Stage**: One of the four steps of the flow: feature document, design document, execution, and self PR review.
- **Node**: A stage's place in the workflow file's diagram.
- **Workflow file**: The committed `.md` file whose mermaid diagram holds the nodes' order and hand-offs and whose settings table holds each node's agent model, effort, and operator or seat.
- **Agent model**: The language model an agent runs on, such as Opus or Sonnet. It is not the ratified term `model`, a formal description of a hard core's design.
- **Round**: One attempt by an operator, followed by its verifier's grade.
