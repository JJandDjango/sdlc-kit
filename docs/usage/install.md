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
.sdlc/hooks/protect_specs.py  session hook: the spec channel closed to sessions (§4)
.sdlc/REVIEW.md             the advisory review pass, yours to edit (§4)
.pre-commit snippet         task-contract ready check (written if absent, else printed)
.vscode/settings.json       YAML schema mapping for contract editing (written if absent, else printed)
.claude/settings.json       the hook wired for Edit/Write/MultiEdit/NotebookEdit (written if absent, else printed)
```

**Never overwrites.** Existing files are skipped and reported —
brownfield adoption is additive by construction.
