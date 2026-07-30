# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-29 (session 18)._

## Now
- Session 18 (2026-07-29): **the stack answer went live** - tooling
  profiles ship as in-kit template overlays (ADR 0018:
  profiles/{stack}/profile.json, replace-by-target, drift classes
  single-sourced in init, no forced migration), dotnet's container
  live and deliberately empty; kit 0.5.0. The C# arc opened here:
  goal is per-gate executable baselines for .NET, gaps found in real
  work repos propagating back as kit fixes (promotion rule: project
  -> profile -> shape; findings cross, employer code never does).
- Contract `dotnet-profile-g0` (F1-F9 ratified whole) entered through
  its own intake: `tooling-profile` born TC011-red and user-ratified
  at the door (glossary 13/13). The G0 finding is load-bearing: both
  G0 conditions are artifact checks, zero stack delta - so the slice
  is container + docs/dotnet-profile.md (13-gate binding table, .NET
  fit notes, gap register with named triggers, G3 roadmap).
- Profile-authoring rule surfaced by the first red loop and now
  suite-locked: drift-checked overlay templates render from kit truth
  + date + stack only; interview-only variables land in the
  unrenderable review-by-hand net.
- Receipts: suite 95 -> 106; audit clean; PromptLang green. Self-pin
  lag learned the hard way (PR #11 CI run 1): a bump PR cannot pin
  itself to the tag its own merge creates - now doctrine in
  docs/distribution.md, with the #7 -> #8 sequence generalized.
- **PR #11 merged 2026-07-30** (the merge = the tooling-profile
  ratification record); **v0.5.0 tagged on the merge** and pushed.
  The self-pin PR closes the loop: both refs -> v0.5.0, self-run
  reads scaffold-current, and its green CI is the tag's install
  proof.

## Blockers
- None.

## Next actions
1. **G3 slice** (dotnet profile's first heavy payload):
   Directory.Build.props strict compile, .editorconfig +
   `dotnet format`, analyzer battery, inner-loop CI job - container
   decided, the work is binding content. Open sub-question: brownfield
   drift classes for .editorconfig/props (merge-target vs kit-owned).
2. **Per-gate agent arc** (0017 V4's neighbor, unchanged): harness,
   venue, verdict plumbing, plugin agents/ distribution.
3. **Pilot M0 session** (engine repo): now also the first
   profile-aware `/sdlc update` consumer; Q5 reality data.
4. Carried one-liners, two remaining: README.md tree line,
   CONVENTIONS.md schema ref (both still name the old root schemas/
   path).
5. Deferrals unchanged: Q4 numbers, PyPI publish (trigger stands),
   explainer PDF, V8 RDF map; new registered gaps behind triggers:
   Azure DevOps variant, Husky.NET hooks, dotnet-tool wrapper.

## Open questions
- Q4 thresholds, numeric only.
- Q5 two-channel decorrelation - M0 remains the first live data point.
- Per-gate agent shape: venue, context assembly, verdict format,
  plugin versioning.
- G3 slice's brownfield class call (above) - decide inside that
  contract, not before.
