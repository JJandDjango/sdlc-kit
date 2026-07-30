# Distribution - how the kit reaches consumers, and who picks the moment

<!-- covers: specs/distribution-reconciliation/contract.yaml -->

> **Contract** - one question: *how does a kit change reach a
> consumer, and on whose schedule is it reconciled?*
> Component deep page (MAP row lands when the first surface ships).
> Feature set ratified in-session 2026-07-29 (F1-F3 kept, F4 struck);
> task contract `specs/distribution-reconciliation/contract.yaml` -
> the first ready-green contract to resolve `entities:` through the
> G0.2 coverage join (`consumer`, `scaffold` - both accretion-born
> via TC010).

**Status legend:** 🔴 ratified, not yet shipped · 🟢 shipped ·
⚪ deferred behind a named trigger. Docs Pass 0 authored 2026-07-29,
before any implementation; markers flip as units land.

## The three channels

A kit change reaches a consumer on three surfaces with three update
models - reconciliation means knowing which surface moved and who
moves it:

| Channel | Carries | Update model |
|---|---|---|
| wheel (`pip install`) | validator + all three schemas | scaffolded CI installs per run - 🟢 pinned to the release tag (F1); consumers bump deliberately |
| plugin (marketplace) | `/sdlc` flows, engines, templates | manual `claude plugin update`; lags until pulled |
| committed scaffold | SDLC.md, `.sdlc/`, specs README, CI workflow, hook + editor settings | rendered once, no-clobber, consumer-owned; kit updates never rewrite it - 🟢 `/sdlc update` makes drift visible (F3) |

The safety rails that make updates survivable are already house law:
additive-first schema deltas (0005 amendment path; the 1.1.0
`entities` delta is the exemplar - old contracts stay valid, semantics
activate on presence), sunset windows for removals (0013; W001 warns
inside the window, TC012 errors past it), and stable diagnostic codes
so a break announces itself by name in the consumer's own CI.

## 🟢 Pinned install ref (F1 - unit: release-tagging)

The scaffolded workflow's install step pins to a release tag
(`git+...sdlc-kit.git@v{version}`, resolved from the packaged kit
version at render time) instead of floating main. The kit tags
`v{X.Y.Z}` on every version bump - tag-on-bump is release discipline,
recorded beside the delta-note rule. Effect: updates flip from push
(the kit chooses when every consumer takes HEAD) to pull (a consumer
upgrades by bumping one line, with the changelog in hand).

**Self-pin lag (kit repo only):** inside a bump PR the kit's own
committed scaffold keeps the *previous* release's pins - the new tag
is born at that PR's merge, so pinning to it pre-merge cannot
install (PR #11's first CI run is the receipt). Post-merge sequence,
now standing: tag the merge, then a self-pin PR moves the kit's own
refs to the fresh tag - its green CI is the tag's install proof (the
session-17 #7 → #8 sequence, generalized). Between the two merges
`/sdlc update` on main honestly names the two lagging surfaces.

## 🟢 CHANGELOG.md (F2 - unit: changelog)

The migration-notes venue, materialized at the repo root - the
"plugin changelog" the vocabulary docs promised now has an address.
Backfilled 0.1.0 → 0.3.0 with the task-contract 1.1.0 delta note as
the exemplar. House rule, stated in the file: **no schema `version:`
bump merges without its delta note.**

## 🟢 `/sdlc update` (F3 - unit: update-command)

The missing day-2 move for the frozen scaffold: a report-only engine
renders the current templates, diffs them against the consumer's
committed copies, and names each drifted file (exit 0 clean / 1
drift). Apply is per-file and consented - no bulk overwrite path
exists, so no-clobber survives the update story. Merge-target files
(consumer-owned by design) are distinguished from kit-owned scaffold
files in the report.

## ⚪ Deferred, triggers on record

- **PyPI publish (F4, struck 2026-07-29)** - tags deliver the pull
  model without release-pipeline overhead; publish when consumer
  count or install ergonomics demand version-specifier installs.
- **Tooled consumer migration** - manual lockstep with changelog
  notes until consumer count makes it untenable (0017's registered
  trigger).
