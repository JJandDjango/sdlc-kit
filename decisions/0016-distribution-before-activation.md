# 16. Distribution before activation: the /sdlc skill and the public sdlc-kit repo

Status: accepted
Date: 2026-07-26

## Context

The 0004 program closed at 54/54 `specified` (0015); the named next
program was activation, gated entirely on Q6 pilot selection. The user
re-sequenced: before any pilot, package the kit the way Cairn was
packaged - a skill plus a public repo - so any repo (greenfield or
brownfield) can be initialized under the kit: install -> `/cairn` (doc
spine) -> `/sdlc` (gate spine). Cairn (`JJandDjango/cairn`) supplies
the proven shape: `skills/<name>/` with a no-clobber renderer and a
report-only auditor, `.claude-plugin/marketplace.json`, README/USAGE/
LICENSE, install by shell copy or plugin marketplace. The kit already
carried the consumer model this needs: pip-installable
`sdlc-taskcontract`, F8/F12 consumer snippets, and F10 (`/intake`) +
F11 (`new <id>`) as named-deferred venues (0006).

## Decision

- **This repo goes public, renamed `sdlc-kit`**, and gains
  `skills/sdlc/` - single source of truth; no extraction repo.
- **Consumer model:** targets pip-install the validator machinery from
  GitHub; the skill distributes by shell copy or plugin marketplace,
  same as Cairn.
- **v1 subcommands:** `init` (interview + no-clobber scaffold: SDLC.md
  status page, `.sdlc/` config + clocks + reds seeds, `specs/` root,
  CI workflow, F8/F12 snippets), `new` (F11, shipped as a
  `taskcontract` CLI subcommand so every pip consumer gets it),
  `intake` (F10, the G0 venue as agent instructions), `audit`
  (report-only, exit 0/1/2).
- **Q6 reframed, not answered:** the pilot is now *the first repo
  initialized via the skill*. Activation build items land into the
  skill's payload as they are built.
- **Category line:** the skill, renderer, and auditor are
  *distribution machinery*, not 0008 build items (they close no
  condition shape); the build-item register is unchanged. The scaffold
  payload is profile-neutral - contracts, config, ledgers, and the
  validate job are ecosystem-free; .NET-bound checks stay commented
  stubs per 0008's no-speculation rule.
- **Lifecycle stance:** G0.1 stays `specified` kit-side. `enforced` is
  per-target: it flips in a repo when `/sdlc intake` runs live there.

## Consequences

- Publication dissolves the protect-main blocker - rulesets are free
  on public repos; the tracked ruleset JSON gets applied at publish.
- The kit's docs become the public product; README/USAGE join the
  repo as consumer-facing surfaces with feature-status markers.
- The skill prompt joins the enforcement layer's class-E perimeter
  (PL-PIPE.1 scope) once a pilot depends on it; until then it rides
  normal review. PromptLang form is validated from day one.
- Registry counts do not move; `docs/task-contract.md` drops its
  F10/F11 "deferred" line; MAP gains a distribution-skill component.
