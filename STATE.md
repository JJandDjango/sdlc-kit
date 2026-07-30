# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-30 (session 20 close)._

## Now
- Session 20 (2026-07-30): **the G3 slice shipped end to end** - the
  dotnet overlay's first real payload. Contract `dotnet-profile-g3`
  ready-green at intake on the first pass (entities tooling-profile /
  scaffold / consumer / gate; the parked drift-class sub-question
  ruled in-contract). Four surfaces: Directory.Build.props (strict
  flags + StyleCop wiring, merge-target), .editorconfig (layout +
  severity map, merge-target), sdlc-dotnet.yml (inner-loop echo,
  kit-owned), pre-commit replacement with the dotnet-format hook
  (merge-target). ADR 0019 records the class split as precedent:
  enforcement configs consumers extend are merge-target; tamper
  protection stays the suppression audit's job, orthogonal.
- Receipts: suite 106 -> 111; audit clean; docs Pass-0 red -> green
  at ship; kit 0.6.0. PR #15 merged (18431e8), v0.6.0 tagged there,
  self-pin PR #16 merged green (9e78fad) - its contracts job proved
  `pip install @v0.6.0`; main reads scaffold-current at the 0.6.0
  render.
- Session-20 opener closed: the output register **binds as a bias,
  not a gate; stands unchanged**. Two micro-violations observed in
  the resume reply (double-loaded sentence, name wobble), none after.
  Scope reading logged as precedent: "active voice" bans
  agent-hiding, not telegraph elision in status lines. User verdict:
  assume it is working.
- Husky.NET gap re-registered: its old trigger (the G3 slice) fired
  and closed on pre-commit; new trigger "a consumer without Python
  tolerance". Repo now auto-deletes merged branches
  (`gh repo edit --delete-branch-on-merge`, first proven on #16).

## Blockers
- None.

## Next actions
1. **G4 mechanical core slice** (roadmap step 3): echo, full test
   execution, secret/dependency audit - plus the four banked
   G4-session inputs on the G3 page (G3.1 echo step, four-vector
   suppression audit, unit-suite-green candidate condition,
   battery-CWE map).
2. **Per-gate agent arc** (unchanged): harness, venue, verdict
   plumbing, plugin agents/ distribution.
3. **Pilot M0 session** (engine repo): first profile-aware consumer -
   now with a real dotnet payload to take; Q5 reality data.
4. Carried one-liners, two remaining: README.md tree line,
   CONVENTIONS.md schema ref (both still name the old root schemas/
   path).
5. Deferrals unchanged: Q4 numbers, PyPI publish (trigger stands),
   explainer PDF, V8 RDF map; gaps behind triggers: Azure DevOps
   variant, Husky.NET (new trigger), dotnet-tool wrapper.

## Open questions
- Q4 thresholds, numeric only.
- Q5 two-channel decorrelation - M0 remains the first live data point.
- Q6 first analyzer tranche - rides pilot activation (ADR 0009's
  selection function needs real defect data).
- Per-gate agent shape: venue, context assembly, verdict format,
  plugin versioning.
