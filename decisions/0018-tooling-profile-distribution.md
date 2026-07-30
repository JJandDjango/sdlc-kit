# 18. Tooling profiles distribute as in-kit template overlays

Status: accepted
Date: 2026-07-29

## Context

The activation goal is per-gate executable enforcement, established
stack by stack against real repos (the user's C# work repos first),
with findings propagating back to the kit and out to every consumer.
The registry already carries the two-layer model
([0008](0008-two-layer-condition-model.md)): conditions are
language-agnostic *shapes*; the Check/Tooling columns are the .NET
reference profile. What never existed is the delivery mechanism - the
init interview records `stack:` but "the v1 payload is stack-neutral"
([0016](0016-distribution-before-activation.md)), so the parameter
selected nothing. The G0 slice (contract `dotnet-profile-g0`, feature
set F1-F9 ratified in-session 2026-07-29) makes it live. The intake
also produced a finding: G0's two conditions are artifact checks with
zero stack delta - so the G0 slice ships container plus documentation,
no new gate machinery.

## Decision

- **A tooling profile is an in-kit template overlay**:
  `skills/sdlc/templates/profiles/{stack}/` with a `profile.json`
  manifest declaring `{template: {target, class}}`. Init resolves base
  surfaces plus the stack's overlay - new targets append, colliding
  targets are replaced by the profile's render - under the same
  no-clobber and merge-target semantics. No or empty overlay renders
  the base exactly.
- **One distribution stream.** Profiles ship inside the kit: same
  plugin, same `KIT_VERSION`, same tag-on-bump and CHANGELOG, same
  `/sdlc update` engine. No per-profile repo or version. Revisit
  trigger: a profile that needs an independent release cadence.
- **Drift classes have one source.** `init.SURFACE_CLASSES` classifies
  base surfaces; manifest entries carry their own class
  (kit-owned / merge-target / consumer); update.py consumes both and
  keeps `unclassified` as the safety net. A consumer's stack is read
  from `.sdlc/config.yaml` at update time and compared as a real
  value; `date` stays the wildcard.
- **Profile-authoring rule** (surfaced by the first red loop):
  drift-checked overlay templates may reference kit truth, `date`,
  and `stack` only. Interview-only variables (`project_name`,
  `adoption`) make a surface unrenderable at update time - it reports
  review-by-hand rather than silently passing; the suite locks this.
- **No forced migration.** A consumer scaffolded before a profile
  slice ships sees the new surfaces as `absent` rows in
  `/sdlc update`, applied per-file on consent - the overlay composes
  with the pull model instead of amending it.
- **dotnet ships first, deliberately empty at G0.** The zero-delta
  finding is the content: the container is live, the first payload is
  the G3 slice (strict compile props, formatter, analyzer battery).
  0016's "payload is profile-neutral" line evolves, not breaks: the
  *base* stays neutral; ecosystem payload lives only in profiles, and
  0008's no-speculation rule is kept by empty manifests until a slice
  actually ships.
- **Promotion rule for findings from real repos**: project-specific
  results stay in the consumer's `.sdlc/` config and baselines;
  stack-specific results land in the profile binding; only
  cross-stack results touch a condition shape. Findings cross the
  boundary as defect classes, gap descriptions, and parameter values -
  never as consumer code.

## Consequences

- `stack:` selects behavior for the first time; SKILL.md's interview
  drops the stack-neutral caveat and names the overlay.
- `docs/dotnet-profile.md` becomes the profile's public status page:
  per-gate binding table, fit notes, gap register (Azure DevOps,
  Husky.NET, dotnet-tool wrapper - each behind a named trigger),
  slice roadmap.
- MAP gains the tooling-profile component row; the glossary gains the
  ratified `tooling-profile` term (born at this intake).
- Kit version bumps to 0.5.0 with its CHANGELOG delta note;
  `v0.5.0` tags the shipping merge.
- The G3 slice inherits a decided container: its work is binding
  content (props, editorconfig, analyzer set, CI job), not
  architecture.
