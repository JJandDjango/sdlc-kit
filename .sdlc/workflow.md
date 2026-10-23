# Workflow

The kit's flow, one node a stage. The diagram holds the order of the nodes, and each edge names the file it hands to the next node. The table holds each node's agent model, effort, and operator or seat, and is the one place for them. `taskcontract/workflow.py` reads both and refuses a fault.

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
