# Using the SDLC Kit

> 🟢 **v1 shipped** — every flow on this page is implemented and proven
> by the kit's regression suite plus live greenfield + brownfield smoke
> runs (no-clobber included). Sections marked 🔴 are ratified but not
> yet shipped.

The kit lays a **gate spine** into a repository: immutable task
contracts under `specs/`, a gate status page, config + ledgers under
`.sdlc/`, and CI that validates every contract. This is the explicit
guide; `README.md` is the short overview.

**The whole idea in one sentence:** a task may not enter development
until its contract validates `ready`, and nothing the implementer can
edit is allowed to weaken that check.

---

## 1. When to run it

| Situation | Run `/sdlc`? | Mode |
|---|---|---|
| Brand-new repo (start here) | Yes — after `/cairn` if you use it | greenfield |
| Existing codebase adopting gates | Yes | brownfield |
| Repo already initialized | No — use `intake` / `new` / `audit` | — |

Greenfield and brownfield get the same payload; the difference is
recorded in `.sdlc/config.yaml` (`adoption:`) and brownfield relies on
no-clobber — anything you already have is skipped, never overwritten.

---

## 2. Install

```bash
cp -r skills/sdlc ~/.claude/skills/sdlc                     # macOS / Linux
Copy-Item -Recurse skills\sdlc $HOME\.claude\skills\sdlc    # Windows
```

or, as a plugin:

```
/plugin marketplace add JJandDjango/sdlc-kit
/plugin install sdlc@sdlc-kit
```

(The plugin is named `sdlc`, the marketplace `sdlc-kit` — the qualified
id always resolves; bare `sdlc-kit` does not.) Pick **one** channel: if
you adopt the plugin after a skills-dir install, delete
`~/.claude/skills/sdlc` so `/sdlc` doesn't surface twice — the plugin
also tracks kit updates, the copied dir does not.

Target repos additionally consume the validator via pip (CI does this
automatically from the scaffolded workflow):

```bash
pip install git+https://github.com/JJandDjango/sdlc-kit.git
```

Reload the Claude Code session after installing — skills list at
startup.

---

## 3. `/sdlc` — initialize a repo

Run it in the target repo. It asks:

| # | Answer | What it drives |
|---|---|---|
| 1 | **project name** | Titles the gate status page. |
| 2 | **adoption** — greenfield / brownfield | Recorded in config; brownfield leans on no-clobber. |
| 3 | **stack** — free text (e.g. `dotnet`, `python`, `typescript`) | Recorded in config for the activation program; v1 payload is stack-neutral. |

If a Cairn spine is absent it recommends `/cairn` first (never
requires it, never touches Cairn's files).

### What you get

```
SDLC.md                     gate status page — which gates are live here (🟢/🔴)
.sdlc/config.yaml           adoption, stack, kit ref, active gates
.sdlc/clocks.yaml           numeric gate parameters — seeded placeholder defaults
.sdlc/reds.yaml             standing-red ledger — starts empty
.sdlc/findings/TEMPLATE.yaml  return-channel finding form (§7, the membrane)
.sdlc/NOTICE.md             provenance of the vendored scaffold (§7)
specs/README.md             the protected root: contracts live at specs/<task-id>/contract.yaml,
                            immutable to implementers (write-surface rule)
.github/workflows/sdlc.yml  CI: pip-install the kit, validate every contract
.pre-commit snippet         task-contract ready check (written if absent, else printed)
.vscode/settings.json       YAML schema mapping for contract editing (written if absent, else printed)
```

**Never overwrites.** Existing files are skipped and reported —
brownfield adoption is additive by construction.

---

## 4. Day 2 — the contract flow

### `/sdlc intake` — the G0 venue
Give it a raw request ("add CSV export"). The agent authors
`specs/<task-id>/contract.yaml` — intent, scope, non-goals,
decomposition with a done-meaning and 1–3 acceptance-sketch criteria
per unit, dependencies, provenance — then loops

```bash
python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
```

until green, and refuses the handoff to spec/implementation while red.
A blocked dependency parks the contract as a valid `draft`; `ready` is
what gates entry into development.

### `taskcontract new <id>` (or `/sdlc new <id>`)
Scaffolds the 8-field contract skeleton at
`specs/<id>/contract.yaml` with inline field guidance. The id must
match `^[a-z][a-z0-9-]{2,63}$`.

### `/sdlc audit`
Report-only health check — exit 0 clean / 1 findings / 2 no `.sdlc`
here. Checks: config + ledgers parse, every contract validates, the
payload surfaces exist, CI job present. It never writes; fixes stay
with you.

---

## 5. Vocabulary — executable shared language 🟢

> 🟢 **Shipped** (kit 0.3.0, [ADR 0017](decisions/0017-vocabulary-layer.md)) —
> deep page: [docs/vocabulary.md](docs/vocabulary.md), including the
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

Contracts may declare `entities:` — the terms the task touches. G0
resolves each ref against **ratified** terms only: a missing or draft
term surfaces as an unresolved dependency naming the term — fork a
small vocabulary task; the work itself never fails for vocabulary.
Ratification stays deliberately human: flip `status: draft →
ratified` in the term file; the PR merge is the approval record.
Deprecation sets `sunset:`; the join warns inside the notice window
and errors past it.

Greenfield init seeds 5–15 terms through the interview (born
ratified); brownfield repos start with `vocab extract` and ratify the
keepers.

---

## 6. A worked example (greenfield)

```
mkdir billing-service && cd billing-service && git init
/cairn        → document why the project exists
/sdlc         → name: billing-service · adoption: greenfield · stack: python
/sdlc intake  → "Add invoice PDF export"
              → writes specs/invoice-pdf-export/contract.yaml, validates ready
# implement only what the contract scopes; CI re-validates every contract on push
/sdlc audit   → exit 0
```

Brownfield is the same flow on an existing repo — init skips whatever
already exists, and the first `intake` is where gate discipline
actually starts.

---

## 7. Restricted environments — the one-way membrane

> 🟢 **Shipped** (kit 0.10.0, [ADR 0023](decisions/0023-work-adoption-membrane.md)) —
> the policy, the findings form (`.sdlc/findings/TEMPLATE.yaml`), and
> the scaffold NOTICE (`.sdlc/NOTICE.md`).

Running the kit on code you cannot show outside (an employer, a
client) is a supported posture. Two facts make it safe by
construction:

- **The kit never phones home.** Every check is deterministic local
  Python — no network calls, no telemetry, no LLM anywhere in the
  enforcement path. The only network step is the pip install itself,
  pulling *from* public GitHub.
- **Flow is one-way.** The kit reaches your environment by public
  tag; nothing about your code travels back.

The discipline, one rule per direction:

| Direction | Rule |
|---|---|
| Kit → your repo | Install by pinned tag (`@vX.Y.Z`), never `main`. Upgrades are pull-only: re-pin, then `/sdlc update`. |
| Findings → upstream | File findings in controlled-dictionary terms, gate IDs, and counts — never code, never identifiers. The form at `.sdlc/findings/TEMPLATE.yaml` admits nothing else by construction. |
| Patches → upstream | Don't. Code written in your environment stays there; file a finding instead, and upstream re-implements the idea. |

**Mark your copy.** Every init renders `.sdlc/NOTICE.md` — upstream
URL, the rendering tag, the MIT license — so the vendored scaffold
reads as open source, not homegrown tooling, and the upgrade path
stays legible. Mirroring the whole kit inside your org? Copy that
file to the mirror root too.

**Local runs without managing Python.** CI needs nothing — hosted
runners ship Python, and the scaffolded workflow installs the kit
itself. For pre-push checks on a machine where you'd rather not
manage a Python install, `uv` (a single static binary, no Python
required to install it) runs the validator in an ephemeral
environment:

```bash
uv run --no-project --with "sdlc-taskcontract @ git+https://github.com/JJandDjango/sdlc-kit.git@v0.9.0" python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
```

---

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "`/sdlc` isn't listed" | Reload the Claude Code session after installing. |
| "It didn't overwrite my file" | By design (no-clobber). Edit the file in place, or delete it and re-run. |
| `TC003 dependency unresolved` | The contract is a parked draft — resolve or re-scope the dependency; `ready` requires all resolved. |
| `TC005 unknown field` | Contracts reject stray keys (`additionalProperties: false`) — a typo or scope smuggling; both fail loudly. |
| CI job green with no contracts | Expected — the validate step is guarded until a `specs/*/contract.yaml` exists. |
| `audit` exit 2 | No `.sdlc/` here — run `/sdlc` init first. |
