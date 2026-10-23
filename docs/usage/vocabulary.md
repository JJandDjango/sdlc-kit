## 5. Vocabulary — executable shared language 🟢

> 🟢 **Shipped** (kit 0.3.0, [ADR 0017](../../decisions/0017-vocabulary-layer.md)) —
> deep page: [docs/vocabulary.md](../vocabulary.md), including the
> constraint registry (`specs/vocabulary/constraints.yaml`, class E).

The terms your tasks operate on become per-term YAML files under
`specs/vocabulary/` — validated at the door, joined at G0.

| Command | What it does |
|---|---|
| `/sdlc vocab` | Computed listing of the glossary (no stored index) |
| `/sdlc vocab add <slug>` | Scaffold one term skeleton, born `draft` |
| `/sdlc vocab extract` | Draft terms from declared surfaces (APIs, schemas, docs) with `sources:` provenance |

Engine equivalents for CI and scripts: `python -m taskcontract
vocab-list` / `vocab-add <slug>` / `vocab-check` (the door — VTnnn
diagnostics; the scaffolded CI workflow runs it as a backstop step).

Contracts declare `entities:`, the terms the task touches. G0
resolves each ref against **ratified** terms only: a missing or draft
term surfaces as an unresolved dependency naming the term — fork a
small vocabulary task; the work itself never fails for vocabulary.
Ratification stays deliberately human: flip `status: draft →
ratified` in the term file; the PR merge is the approval record.
Deprecation sets `sunset:`; the join warns inside the notice window
and errors past it.

🟢 From kit 0.14.0 ([ADR 0030](../../decisions/0030-a-doors-input-is-a-declaration.md))
the declaration is required at the `ready` profile; `entities: []`
states that the contract touches no term, and the `draft` profile still
accepts a contract without the field. See §4, "What `ready` requires".

Greenfield init seeds 5–15 terms through the interview (born
ratified), then asks who holds the seats and seeds `intake-seat` the
same way; brownfield repos start with `vocab extract`, ratify the
keepers, and ratify `intake-seat` (§8).
