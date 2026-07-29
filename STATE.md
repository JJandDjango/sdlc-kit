# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-29._

## Now
- Session 17 (2026-07-29): **the glossary is fully ratified and the
  distribution loop goes pull** - four PRs merged (#6 ratification
  walk, #7 distribution-reconciliation, #8 self-pin, #9 vscode
  one-liner), tags v0.3.0 + v0.4.0 on origin, kit 0.4.0.
- The ratification walk: all 7 draft terms flipped after stop-by-stop
  source verification, one user decision per term (PR #6 merge = the
  approval record). House convention settled en route: value-sets
  carry no structural relations (provenance-origin shed its part_of;
  contract-profile is the exemplar).
- distribution-reconciliation: the first contract through the
  ratified vocabulary - first real `entities:` declaration, resolved
  against the kit's first TC010 accretion-born terms (consumer,
  scaffold - user-ratified at intake). Shipped whole: pinned install
  refs (KIT_VERSION single-sourced in init.py, test-locked to
  pyproject; tag-on-bump house rule, first executed at v0.4.0),
  CHANGELOG.md (migration-notes venue, backfilled 0.1.0-0.3.0, the
  1.1.0 delta note as exemplar), /sdlc update (report-only drift
  engine - kit-owned / merge-target / consumer classes,
  date-wildcard compare, per-file consented apply; Update flow in
  SKILL.md, PromptLang-green). Docs Pass 0 authored
  docs/distribution.md red first; markers green; MAP row landed.
- Dogfood receipts: the engine's first live run named this repo's own
  two drifted surfaces; the self-pin PR's CI proved `pip install
  @v0.4.0`; `/sdlc update` reads scaffold-current (exit 0) on main -
  first time ever. Suite 85 -> 95 green; audit clean; glossary 12/12
  ratified (registry 5 constraints); plugin cache at post-merge HEAD
  (restart applies). Morning check: the first GitHub runs of the
  vocab-check step came back green - the 0.3.0 loop closed before
  the walk began.

## Blockers
- None.

## Next actions
1. **Per-gate agent arc** (0017 V4's named neighbor): harness, venue,
   verdict plumbing, plugin agents/ distribution; G0's vocabulary
   interface fixed by V4.
2. **Pilot M0 session** (engine repo): first consumer of `/sdlc vocab
   extract` and now `/sdlc update` (its scaffold predates the pin);
   Q5 reality data.
3. Carried one-liners, two remaining: README.md tree line,
   CONVENTIONS.md schema ref - both still name the old root schemas/
   path (.vscode cleared this session).
4. Deferrals unchanged: Q4 numbers (sunset notice floor included),
   PyPI publish (F4 struck 2026-07-29; trigger stands), explainer
   PDF; V8 RDF map trigger-gated. Registered v1 edge from this
   session: no consumer opt-out for a deliberately-absent merge
   target (update reports absence forever).

## Open questions
- Q4 thresholds, numeric only.
- Q5 two-channel decorrelation - the M0 session remains the first
  live data point.
- Per-gate agent shape: venue, context assembly, verdict format,
  plugin versioning - G0's judgments fixed; the rest open.
