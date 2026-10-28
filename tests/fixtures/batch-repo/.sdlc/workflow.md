# Workflow

The fixture repository's flow.

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
