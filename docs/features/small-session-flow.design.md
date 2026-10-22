| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-22 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r4. Engineer seat: Johnathan Hyden |
| 2026-10-22 | Johnathan Hyden | r2: Measured: the checks before signing, on the solution half: 21 findings (CL006 19, CL008 2); Scope against the release unit's paths: no release unit, check skipped; ready checks 11 to 15: 6 OPEN |
| 2026-10-22 | Johnathan Hyden | r3: Measured: the checks before signing, on the solution half: 18 findings (CL006 18); Scope against the release unit's paths: no release unit, check skipped; ready checks 11 to 15: 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r4: The solution half finished: 12 sections written, 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r5: Signed: solution half. The engineer seat signs r4 |
| 2026-10-22 | intake | r6: Parked: Ready check 12: the reader's refusals of a node with no row, a row with no node, and an edge with no label have no drawn message. |
| 2026-10-22 | Johnathan Hyden | r7: Interfaces: the reader's three refusals drawn (a node with no row, a row with no node, an edge with no label) |
| 2026-10-22 | Johnathan Hyden | r8: Measured: the checks before signing, on the solution half: 18 findings (CL006 18); Scope against the release unit's paths: no release unit, check skipped; ready checks 11 to 15: 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r9: The solution half finished: 12 sections written, 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r10: Signed: solution half. The engineer seat signs r9 |
| 2026-10-22 | Johnathan Hyden | r11: Scope: `decisions/` added for the ADR. Units: w2 pairs SC1.1+SC1.3 in one sketch entry |
| 2026-10-22 | Johnathan Hyden | r12: Measured: the checks before signing, on the solution half: 18 findings (CL006 18); Scope against the release unit's paths: no release unit, check skipped; ready checks 11 to 15: 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r13: The solution half finished: 12 sections written, 0 OPEN |
| 2026-10-22 | Johnathan Hyden | r14: Signed: solution half. The engineer seat signs r13 |
| 2026-10-22 | intake | r15: Ready: contract `small-session-flow` validates ready-green, derived from r13, against requirements r4; the engineer seat (Johnathan Hyden) signed the solution half at r13 (r14) |

# small-session-flow - Workflow Nodes

`sdlc_development_kit` · seat: engineer Johnathan Hyden · requirements: `docs/features/small-session-flow.md` · contract: `small-session-flow`, draft · PR: none · merge SHA: none

## Proposed solution

`[Engineer seat · authored]`

### Scope

- `.sdlc/workflow.md` (new): the workflow file, its mermaid diagram and its settings table.
- `taskcontract/workflow.py` (new) and `taskcontract/__main__.py`: read and check the rows; `python -m taskcontract node <id>` starts the node's session as `claude --model M --effort E`.
- `hooks/hooks.json` and `hooks/context_size.py` (new, plugin hooks): the 200K and 400K messages.
- `CONTRIBUTING.md`: the session size and the close rule for `docs/backlog.md`'s Next; `USAGE.md` and `docs/components.md` describe the command.
- `tests/`: one test file each for the reader, `node`, and the hook.
- `decisions/`: one ADR records the plugin hook and the `node` command, drafted with w1.
- `.claude/workflows/*.js` (untracked, this machine only): the pinned `effort: 'high'` gives way to the row's values, passed in as arguments.

### Out of scope

- `agents/sdlc-developer.md` and `agents/sdlc-verifier.md` keep `model: inherit`: no enforcement-layer change.
- `skills/`: neither skill changes; the `sdlc` scaffold does not lay the workflow file into other repos.
- `docs/conventions/standing-practice.md` keeps its 40% boundary (SC3.1).
- `.sdlc/config.yaml`: the retry cap goes with the "Execution team" document.
- `specs/` (intake writes it) and Cairn's `status.py`, read as it stands.

### Interfaces

The workflow file, `.sdlc/workflow.md`:

```mermaid
flowchart LR
  feature[Feature document] -->|docs/features/{id}.md| design[Design document]
  design -->|specs/{id}/contract.yaml| execution[Execution]
  execution -->|.sdlc/progress/{id}.yaml| review[Self PR review]
```

| Node | Agent model | Effort | Operator or seat |
| :-- | :-- | :-- | :-- |
| feature | opus | xhigh | PO seat |
| design | opus | xhigh | engineer seat |
| execution | sonnet | high | Developer, QA, Dev verifier, QA verifier, Orchestrator |
| review | opus | high | engineer seat |

The command:

```
python -m taskcontract node design            prints the line below, then starts that session in the terminal
Node design: claude --model opus --effort xhigh
python -m taskcontract node design --print    prints the line and starts nothing
```

- A row that lacks a value: `Node {id} did not start: its row in the workflow file has no {agent model or effort}.` Exit 1.
- An id with no node: `No node {id} in .sdlc/workflow.md. Nodes: feature, design, execution, review.` Exit 1.

The hook shows each message once a session, to the user and to the agent:

- Past 200K tokens: `This session has passed 200K tokens, the target. Finish the deliverable and close.`
- Past 400K tokens: `This session has passed 400K tokens, the limit. Save the notes and close now.`

- One step that passes both 200K and 400K: only the 400K message shows.
- `node` with no `claude` on the path: `Node {id} did not start: no claude command on the path.` Exit 1.

The reader refuses a file that breaks the diagram or the table. Each refusal exits 1, and `node` starts nothing:

- A node with no row: `Node {id} has no row in the settings table of .sdlc/workflow.md.`
- A row with no node: `Row {id} in the settings table of .sdlc/workflow.md has no node in the diagram.`
- An edge with no label: `The edge from {a} to {b} in .sdlc/workflow.md names no file.`
- Several faults at once: each on its own line, diagram faults first, then table faults, each in file order.

The lines `CONTRIBUTING.md` gains:

```
A session ships one deliverable. Its context targets 200K tokens and stops at 400K.
At close, the next deliverable goes first in `docs/backlog.md`'s Next.
```

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| A node's agent model and effort | The settings table in `.sdlc/workflow.md` | The table wins over `/model` and over any value pinned in a workflow script. |
| The nodes and their order | The mermaid diagram in `.sdlc/workflow.md` | A node with no row, or a row with no node, fails the reader; neither wins. |
| The session's context size | The hook's `transcript_path`: the newest assistant message's input, cache-write and cache-read tokens, summed | The transcript wins over `/context`. |
| The 200K and 400K thresholds | Constants in `hooks/context_size.py` | A test fails when `CONTRIBUTING.md` names other numbers. |
| The next deliverable | The first item of `docs/backlog.md`'s Next (`cairn.plan`) | The backlog wins over `plan.md`'s deferred list. |
| The file each edge hands over | The edge's label in the mermaid diagram | The label wins; the reader fails an edge with no label. |
| The session's last done work | Git log and merged PRs, through `/cairn status` | Git wins over any note written by hand. |

### Constraints

1. The hook never blocks: it exits 0 and only adds a message; on an error it prints nothing.
2. The hook reads the transcript backward and stops at the newest assistant message; it finishes in under 500 ms on a 50 MB transcript.
3. The hook keeps its once-a-session marker in the temp directory, keyed by session id; it writes nothing in the repo.
4. `node` finds `claude` through `shutil.which` and starts it from an argument list, with no shell, in the same terminal; it opens no new window.
5. Subprocess output is decoded with `encoding="utf-8", errors="replace"`.
6. The reader adds no dependency to `taskcontract`.
7. No file but `.sdlc/workflow.md` holds a node's agent model or effort; the workflow scripts take both as arguments.
8. The hook stays silent in a repo with no `.sdlc/workflow.md`.

### Units

| Unit | Checks | Done means | Tests by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| w1-session-size | SC3.1, SC3.2+SC3.3 | `CONTRIBUTING.md` states the one deliverable, the 200K target and the 400K limit. The plugin hook shows each message verbatim once a session when the context passes its threshold. | SC3.1 automated; SC3.2, SC3.3 automated on fixture transcripts, and a manual receipt: the hook's message in a live session past 200K | none |
| w2-workflow-file | SC1.1+SC1.3, SC1.2, SC2.3 | `.sdlc/workflow.md` holds one four-node flowchart, with a named file on each edge and one settings row per node. The reader refuses a node whose row lacks an agent model or an effort, with SC2.3's message. | SC1.1, SC1.2, SC1.3, SC2.3 automated, on the real file and on fixtures | none |
| w3-node-start | SC2.1+SC2.2 | `python -m taskcontract node <id>` starts `claude` at the row's agent model and effort, and the workflow scripts take both as arguments. | SC2.1, SC2.2 automated through `--print` with only the row changed; a manual receipt: a session started by `node design` | the pinned `effort: 'high'` in four workflow scripts; no tests pin it |
| w4-session-notes | SC4.1, SC4.2 | The close rule in `CONTRIBUTING.md` puts the next deliverable first in the Next list of `docs/backlog.md`, and the next session's first `/cairn status` names it. | SC4.1 a manual receipt at a session's close; SC4.2 a manual receipt at the next session's start | none |

The draft check's CL006 words in the done means go to intake's full lane as dictionary candidates: deliverable, limit, message, verbatim, threshold, four-node, flowchart, edge, reader, refuses, effort, starts, arguments, close, puts.

### Order

w1-session-size, w4-session-notes, w2-workflow-file, w3-node-start: one unit a session. The two session rules come first because they govern every later build session; w4's SC4.2 receipt lands at the start of w2's session. w3 comes last because `node` reads w2's reader.

## Risks and cost

`[Engineer seat · authored]`

Risks:

1. The hook reads Claude Code's transcript format, which is no public contract; an update can silence it, and constraint 1 hides the error. The fixture tests pin the fields it reads, and w1's live receipt checks it once.
2. Plugin hooks run in every repo with the kit's plugin enabled, `deadlock-mod` among them. Constraint 8 keeps the hook silent where `.sdlc/workflow.md` is absent.
3. The aliases `opus` and `sonnet` follow new model releases, so a node's agent model can change with no row changed. A row may name a full model id instead.
4. w3's change to the workflow scripts is untracked, so neither the PR nor Two-Key sees it. w3's manual receipt covers it.
5. On Windows, Python starting an interactive `claude` can mishandle the terminal or Ctrl+C. w3's receipt tests it; `--print` is the fallback.
6. SC4.2 rests on Cairn's `status.py`, outside the kit, and no kit test covers it. The receipt at each session's start catches a break.

Cost, in agent tokens, from `docs/session-metrics.md`: a unit built in one round took 546K to 781K, so w1, w2 and w3 take about 1.65M to 2.34M. w4 has no automated test and needs only Two-Key, about 200K to 300K (`s6-release`'s rounds took 211K and 220K). The total is about 1.9M to 2.6M; each failed round adds 200K to 325K (session 90's lost round).

## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | yes | Johnathan Hyden, PO and engineer seat, at S3 | The review row, left unset, runs Opus at high; "high or xhigh" becomes xhigh; the execution-to-review edge names `.sdlc/progress/{id}.yaml`, since a PR is no file. |
| 2. More than one solution | yes | Johnathan Hyden, at S1 and S3 | The file lives in `.sdlc/`, not `docs/`; settings reach a node through `claude --model --effort`, not agent frontmatter; intake closes the design node. |
| 3. A solution unconventional to the codebase | yes | Johnathan Hyden, at S1 and S8 | The kit's first plugin hooks (`hooks/`), and a command that starts an interactive session. |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | yes | Johnathan Hyden, at S3 | A new `taskcontract` command, `node`, and a new file format, `.sdlc/workflow.md`; no existing contract changes. |

## Decisions and open questions

`[Engineer seat · authored]`

- The workflow file is `.sdlc/workflow.md`, in this repo; no other repo gets it (engineer seat, 2026-10-22).
- Settings reach a node at session start through `claude --model M --effort E`; the agents keep `model: inherit` (engineer seat, 2026-10-22).
- Intake closes the design node, so execution starts from `specs/{id}/contract.yaml` (engineer seat, 2026-10-22).
- The review row runs Opus at high, and both document rows run at xhigh (engineer seat, 2026-10-22).
- The token messages ship as a plugin hook, silent in a repo with no workflow file (engineer seat, 2026-10-22).
- The `.claude/workflows/*.js` change stays local until the workflows are tracked (engineer seat, 2026-10-22).
- The build order is w1, w4, w2, w3 (engineer seat, 2026-10-22).
- One ADR records the plugin hook and the `node` command (consult cases 3 and 4), drafted with w1 for the user's approval (engineer seat, 2026-10-22).

## Traceability

### Links out

`[Engineer seat · authored]`

- `docs/features/small-session-flow.md`: the requirements, r4, signed at r5; PR #130 carries it.
- `docs/conventions/standing-practice.md:65`, `:282`: the 40% boundary and the ~400K agent stop.
- `NOTES_process-cost_2026-10-12.md`: the process-cost ruling this flow's agent models revisit.
- `docs/session-metrics.md`: the basis of the cost.
- `docs/operators.md`: the enforcement-layer approval channel (class E), which this design does not use.
- The "Execution team" document, not yet written: the retry cap, QA, the verifiers and the draft PR.

### Record

`[Intake · derived]`

(none: intake writes the record)

## Notes

`[Engineer seat · authored]`

- Claude drafted each section from requirements r4 and a read of the files it names; the engineer seat confirmed each. There was no other material.
- The hook reaches a session only through the installed plugin; this machine's sits at `8635064`, so w1's live receipt runs after a plugin update, or with `claude --plugin-dir .`.
- The requirements' two open questions (whether the QA verifier runs through `prove.py`, and whether an ADR records the Sonnet ruling) stay with the "Execution team" document.

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/small-session-flow/contract.yaml`)
