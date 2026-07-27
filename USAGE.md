# Using the SDLC Kit

> 🟢 **v1 shipped** — every flow on this page is implemented and proven
> by the kit's regression suite plus live greenfield + brownfield smoke
> runs (no-clobber included).

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
recorded in `.sdlc/config.yaml` (`material:`) and brownfield relies on
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
/plugin install sdlc
```

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
| 2 | **material** — greenfield / brownfield | Recorded in config; brownfield leans on no-clobber. |
| 3 | **stack** — free text (e.g. `dotnet`, `python`, `typescript`) | Recorded in config for the activation program; v1 payload is stack-neutral. |

If a Cairn spine is absent it recommends `/cairn` first (never
requires it, never touches Cairn's files).

### What you get

```
SDLC.md                     gate status page — which gates are live here (🟢/🔴)
.sdlc/config.yaml           material, stack, kit ref, active gates
.sdlc/clocks.yaml           numeric gate parameters — seeded placeholder defaults
.sdlc/reds.yaml             standing-red ledger — starts empty
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

## 5. A worked example (greenfield)

```
mkdir billing-service && cd billing-service && git init
/cairn        → document why the project exists
/sdlc         → name: billing-service · material: greenfield · stack: python
/sdlc intake  → "Add invoice PDF export"
              → writes specs/invoice-pdf-export/contract.yaml, validates ready
# implement only what the contract scopes; CI re-validates every contract on push
/sdlc audit   → exit 0
```

Brownfield is the same flow on an existing repo — init skips whatever
already exists, and the first `intake` is where gate discipline
actually starts.

---

## 6. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "`/sdlc` isn't listed" | Reload the Claude Code session after installing. |
| "It didn't overwrite my file" | By design (no-clobber). Edit the file in place, or delete it and re-run. |
| `TC003 dependency unresolved` | The contract is a parked draft — resolve or re-scope the dependency; `ready` requires all resolved. |
| `TC005 unknown field` | Contracts reject stray keys (`additionalProperties: false`) — a typo or scope smuggling; both fail loudly. |
| CI job green with no contracts | Expected — the validate step is guarded until a `specs/*/contract.yaml` exists. |
| `audit` exit 2 | No `.sdlc/` here — run `/sdlc` init first. |
