### `taskcontract node <id>`: a node's session at its row's settings 🟢

> 🟢 **Shipped** (contract `specs/small-session-flow/`,
> [ADR 0039](../../decisions/0039-the-kit-ships-plugin-hooks-and-a-node-starts-at-its-rows-settings.md)).

🟢 `.sdlc/workflow.md` draws a flow as nodes, one node a stage. Its
mermaid flowchart holds the nodes in order, and each edge's label names
the file that edge hands to the next node. Its settings table, headed
`| Node | Agent model | Effort | Operator or seat |`, holds each node's
agent model and effort; no other file holds either. `/sdlc init` does
not lay the file. The kit's own repository holds one,
[.sdlc/workflow.md](../../.sdlc/workflow.md), with four nodes: `feature`,
`design`, `execution` and `review`.

🟢 `python -m taskcontract node <id>` prints the node's line, then starts
`claude` at the row's agent model and effort:

```
python -m taskcontract node design            prints the line below, then starts that session in this terminal
Node design: claude --model opus --effort xhigh
python -m taskcontract node design --print    prints the line and starts nothing
```

🟢 `node` finds `claude` on the path and starts it from an argument list,
with no shell and no new window. A Ctrl+C reaches `claude` and leaves
`node` waiting; when the session ends, `node` exits with `claude`'s exit
code. `--print` never looks for `claude`, so it runs where none is
installed. `--root` names the repository (default `.`). An id matches a
node of the diagram exactly, letter case included.

🟢 Each refusal goes to stderr, exits 1 and starts nothing:

- No `claude` on the path, checked first and never under `--print`:
  `Node {id} did not start: no claude command on the path.`
- No workflow file: `Node {id} did not start: no workflow file at .sdlc/workflow.md.`
- An id that is no node, the list naming the diagram's nodes in order:
  `No node {id} in .sdlc/workflow.md. Nodes: feature, design, execution, review.`
- A row that lacks its agent model, its effort or both, one line each,
  agent model first:
  `Node {id} did not start: its row in the workflow file has no agent model.`
  and `Node {id} did not start: its row in the workflow file has no effort.`

🟢 A file that breaks the diagram or the table refuses every id, whatever
the asked node's row holds:

- A node with no row: `Node {id} has no row in the settings table of .sdlc/workflow.md.`
- A row with no node: `Row {id} in the settings table of .sdlc/workflow.md has no node in the diagram.`
- An edge with no label: `The edge from {a} to {b} in .sdlc/workflow.md names no file.`

Several faults print each on its own line: diagram faults first, then
table faults, each in file order.
