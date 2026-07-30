# 19. Enforcement-config drift classes

Status: accepted
Date: 2026-07-30

## Context

ADR [0018](0018-tooling-profile-distribution.md) gave profile overlays
per-surface drift classes but left each surface's ruling to the slice
that ships it. The G3 slice ships the first enforcement configs -
`Directory.Build.props` and `.editorconfig` - plus a CI workflow and a
pre-commit replacement; STATE parked the merge-target vs kit-owned
question for the two configs, to be decided inside contract
`dotnet-profile-g3`. The tension: kit-owned drift is applyable (the kit
can push strictness updates), but consumers legitimately extend both
files - severity tuning, repo-specific style, company-wide props - so
kit-owned semantics would report their own content as drift forever.

## Decision

1. **Enforcement configs consumers extend are merge-target.**
   `.editorconfig` and `Directory.Build.props` (and their analogues in
   future profiles: ruff/mypy config, tsconfig strictness) are written
   when absent, printed as snippets when present, and their drift is
   reported but never applied. The consumer owns the merged result.
2. **Kit process artifacts are kit-owned.** Workflow files the consumer
   has no reason to extend (`sdlc-dotnet.yml`, like `sdlc.yml`) stay
   applyable per-file.
3. **Replacement surfaces inherit their base target's class** unless the
   slice rules otherwise - the dotnet pre-commit config replaces a
   merge-target and stays one.
4. **Tamper protection is not the drift engine's job.** Weakened flags
   and severity downgrades are the suppression audit's catch (G3.2
   clause 3; G4 locus) and PL-PIPE governance operationally. Drift
   classes govern kit-to-consumer sync only - the two concerns stay
   orthogonal.

## Consequences

- No spurious drift on consumer-extended files; `/sdlc update` stays
  honest on dotnet consumers from day one.
- Accepted cost: the kit cannot push strictness updates into the two
  configs - CHANGELOG migration notes plus `--show` snippets are the
  channel; consumers merge by hand.
- Precedent binds future profiles' G3-family slices; deviating needs a
  new ADR naming why.
