# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-08-06 (post-25 reconcile, home machine)._

## Now
- Reconcile session (2026-08-06, home): the session-25 terminal
  was killed 8/6 with no formal wrap; transcript replay proved the
  close ran whole on 8/3 - STATE + plan committed, close PR #31
  merged at 5fd4c90, pushed. The only post-close exchange was a
  fetch-channels Q&A already recorded in USAGE 2/7. Nothing lost;
  no spine edit needed.
- Receipts re-verified 2026-08-06, zero-trust: suite 190 green;
  validate 7/7 ready-green; vocab-green 17 terms; lang-green (six
  pre-arc exempt only); /sdlc audit clean (6 informational); tag
  v0.10.0 -> e7421e8; origin/main unchanged at 5fd4c90; tree clean.
- Cairn audit ran (first since the close): 0 errors, two chronic
  classes. 12 ADRs (0012-0023) exceed the half-page budget -
  recommendation: stand, append-only outranks the budget. 13
  docs/gates/ pages orphaned by the row-link check - MAP.md names
  them in prose only; one-row MAP fix offered, unratified.
- Session 25 (2026-08-03) shipped v0.10.0 whole (ADR 0023): work
  adoption behind a one-way membrane - USAGE 7, findings form
  `.sdlc/findings/TEMPLATE.yaml` + `.sdlc/NOTICE.md` as kit-owned
  surfaces, dotnet day-one posture menu in docs/dotnet-profile.md,
  tag + self-pin proven by the CI install (PRs #29-#31).

## Blockers
- None.

## Next actions
1. **Work-side day one** (session 26 opens from the work machine,
   fetching this repo): runner probe (GitHub-hosted vs self-hosted;
   scratch pip-step run if self-hosted); install the skill via the
   Cairn channel; init the work repo brownfield/dotnet pinned
   v0.10.0; adoption commit carries the posture picks
   (GenerateDocumentationFile true; CS1591 + CA1303 none - menu in
   docs/dotnet-profile.md). Findings return only through the form.
2. M0 pilot (engine repo) is the second consumer - starts with work
   findings in hand. Cargo lane parked until ImSim (Rust)
   initializes.
3. User acts pending: class-S flips for `controlled-dictionary` +
   `controlled-field` (still drafts); rule on the MAP.md row for
   docs/gates/ (apply the one-row fix or accept the standing
   orphan infos).
4. Registered continuations unchanged: PL-PIPE.3 eval harness,
   sdlc-spec / sdlc-qa defs behind venue existence, mechanical loop
   runner, verdict field-name convergence.
5. Parked with triggers (0023 register): dotnet-tool wrapper (Python
   present at work), Husky.NET, mirror + configurable KIT_REPO and
   wheel-on-release (both behind the runner probe), uvx console
   script (offered, not ratified), PyPI; Azure DevOps variant killed
   (work is GitHub). Controlled-language deferrals + Q4 numbers +
   explainer PDF + V8 RDF map + battery-CWE map unchanged.

## Open questions
- Runner posture at work - GitHub-hosted or self-hosted? First fact
  of session 26; decides whether the parked distribution fallbacks
  wake.
- Q4 thresholds, numeric only (unchanged).
- Q5 decorrelation - two feeds: M0 raw traces + work findings
  pre-sanitized by the form (the lexicon as channel-invariant).
- Q6 first analyzer tranche - rides pilot activation.
- Comprehension empirics (PL-PIPE.3 + trace tagging) unchanged.
