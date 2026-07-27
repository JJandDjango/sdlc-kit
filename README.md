# SDLC Kit

**Spec-first SDLC gates for agent-driven development — so agent-written
code cannot degrade the codebase.**

A gate is a human judgment converted into a text artifact plus a
mechanical check. This kit is a gate architecture for automated LLM
development: 54 conditions across eleven lifecycle gates (G0 planning
through G10 retirement) plus two cross-cutting lifecycles (PL-DOC
documentation, PL-PIPE pipeline integrity), each with an exact,
loopable pass condition an agent can drive to green from its
diagnostics alone. Specs are authored before and independently of the
implementation and stay immutable to the implementer; every escaped
defect becomes a new acceptance criterion.

> **Want to use it? → [USAGE.md](USAGE.md)** — install → initialize a
> repo → author task contracts → keep the gates honest.

## What ships today

| Feature | Status |
|---|---|
| Gate registry — 54 specified conditions, deep pages, taxonomy, catalog | 🟢 |
| Task-contract validator — `python -m taskcontract validate`, TC000–TC009, dual-profile schema | 🟢 |
| `/sdlc` init — interview + no-clobber scaffold (greenfield & brownfield) | 🟢 |
| `taskcontract new <id>` — contract skeleton (F11) | 🟢 |
| `/sdlc intake` — the G0 venue: request → contract → validate to green (F10) | 🟢 |
| `/sdlc audit` — report-only gate-health check, exit 0/1/2 | 🟢 |
| Plugin-marketplace install | 🟢 |

🟢 shipped · 🟡 partial · 🔴 not yet

## Install

### As a Claude Code skill (simplest)
Copy the skill into your Claude Code skills directory, then run `/sdlc`:

```bash
cp -r skills/sdlc ~/.claude/skills/sdlc            # macOS / Linux
```
```powershell
Copy-Item -Recurse skills\sdlc $HOME\.claude\skills\sdlc   # Windows
```

### As a Claude Code plugin

```
/plugin marketplace add JJandDjango/sdlc-kit
/plugin install sdlc
```

### The validator (target repos consume this via pip)

```bash
pip install git+https://github.com/JJandDjango/sdlc-kit.git
```

## How it works

`/sdlc` interviews you — target directory, greenfield vs brownfield,
stack — then renders the gate spine into your repo **without ever
overwriting** an existing file: a gate status page (`SDLC.md`), the
`.sdlc/` config and ledgers, the protected `specs/` root for immutable
task contracts, and a CI job that validates every contract. Day 2:
`/sdlc intake` turns a raw request into a validated contract before
any code is written; `/sdlc audit` reports gate health without writing
anything.

Pairs with [Cairn](https://github.com/JJandDjango/cairn) — run
`/cairn` first for the documentation spine, then `/sdlc` for the gate
spine. Neither requires the other.

## Layout

```
skills/sdlc/          # the /sdlc skill: SKILL.md + init.py + audit.py + templates/
taskcontract/         # pip-installable validator (+ contract scaffolding)
schemas/              # task-contract JSON Schema (draft + ready profiles)
docs/                 # gate registry, taxonomy, catalog, per-gate deep pages
decisions/            # ADRs 0001+ — the why, append-only
tests/                # validator + skill regression suite
```

## Principle

Earliest decidable point: cost determines cadence, never rigor.
Engineering effort pushes bug classes *up* the detectability ladder
(correct-by-construction > statically decidable > approximable >
dynamic > spec-relative) rather than accumulating detectors at the
bottom. The enforcement layer is the highest-privilege artifact set —
it gets its own approval channel and its own regression suite. See
[THEORY.md](THEORY.md).

## License

MIT © 2026 Johnathan Hyden
