# SDLC Kit

**Spec-first SDLC gates for agent-driven development — so agent-written
code cannot degrade the codebase.**

A gate is a human judgment converted into a text artifact plus a
mechanical check. The kit holds 54 conditions across eleven lifecycle
gates (G0 planning through G10 retirement), each with an exact pass
condition an agent can drive to green from its diagnostics alone. The
principles are in [ARCHITECTURE.md](ARCHITECTURE.md).

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

```
/plugin marketplace add JJandDjango/sdlc-kit
/plugin install sdlc@sdlc-kit
```

The skills-dir copy and the pip-installed validator: [USAGE.md](USAGE.md) §2.
Pairs with [Cairn](https://github.com/JJandDjango/cairn) for the docs spine.

## License

MIT © 2026 Johnathan Hyden
