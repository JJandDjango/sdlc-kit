# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-08-02 (session 23 close)._

## Now
- Session 23 (2026-08-02): **the controlled-language layer shipped
  whole** - designed in a live walk (pros, cons 1-7 at depth, three
  decisions ruled) and landed the same session. Named "bounded
  interpretation," never "determinism": form checked, meaning not
  checked. Shipped: dictionary schema (born 1.0.0) + set-ratified
  seed at specs/vocabulary/dictionary.yaml (999 words harvested from
  the seven ready-green contracts; zero bans - census-driven); base
  layer (function words + vagueness/evasive bans) in the wheel;
  `lang-check` (CLnnn, verdict-contract native, absence = green,
  glossary disjointness + use_instead integrity + base shadowing) +
  `lang-extract` (report-only census); field registry binding the six
  contract prose fields with text-types; exempt ratchet for the six
  pre-arc contracts (ledger `cl-legacy-tranche` - warnings, never
  gating, ratchet on next edit); venue joins (template CI step, audit
  LANG-INVALID/LANG-EXEMPT, /sdlc lang flows); ADR 0022. The
  `controlled-language` contract passed its own door after rewrite -
  the first hard-at-intake conformance.
- Receipts: suite 158 -> 188; validate 7/7 ready-green; vocab-green
  17 terms / registry 6 constraints; lang-green armed; audit clean
  (6 LANG-EXEMPT INFO); kit 0.9.0 (tag rides the shipping merge).
- PR #26 open at close (branch controlled-language, dcb22c7); user
  acts at review:
  set-ratify the dictionary via the merge (seed grew by `exempt` +
  `binds` during self-adoption - flagged), class-S flips for
  `controlled-dictionary` + `controlled-field` drafts when ready.
- Prior close: PR #25 (c077331) - session-23 opener queued; operator
  + verdict ratified post-close (PR #24).

## Blockers
- None.

## Next actions
1. **Self-pin PR after the v0.9.0 tag** - bumps the kit's own
   workflow pin AND adds its lang-check CI step (the 0.8.0 pin
   predates the subcommand; sequenced deliberately, ADR 0022).
2. **Pilot M0 session** (engine repo): first profile-aware consumer -
   dotnet payload spans G3 + G4 core, operators to exercise, and now
   the controlled-language machinery brownfield-style; Q5 reality
   data + the trace-fed curation feed both start here.
3. Registered continuations: PL-PIPE.3 eval harness (now carrying
   the comprehension family - paired prose variants, loop counts,
   divergence); sdlc-spec / sdlc-qa defs behind venue existence;
   mechanical loop runner; verdict field-name convergence (lang-check
   shipped the envelope shape - convergence still rides a dedicated
   pass).
4. Controlled-language deferrals, triggers on record: base verb
   promotion (self-host evidence), F-item region checking, prompt
   lexicon (foundations-side PromptLang extension), slot templates
   (per-field escape evidence), greenfield day-one arming.
5. Deferrals unchanged: Q4 numbers (now also lang caps + escape-rate
   threshold), PyPI publish, explainer PDF, V8 RDF map; gaps behind
   triggers: Azure DevOps variant, Husky.NET, dotnet-tool wrapper,
   battery-CWE map.

## Open questions
- Q4 thresholds, numeric only (lang sentence caps + escape-rate KPI
  join the clock list).
- Q5 decorrelation mechanism - rides M0; the controlled lexicon is
  the channel-invariant (ADR 0022 note).
- Q6 first analyzer tranche - rides pilot activation.
- Comprehension empirics (front-run, admitted): does restriction
  help the model reader? PL-PIPE.3 family + M0 trace tagging answer;
  a null result re-prices one benefit, kills nothing.
- Operator activation in consumers - M0 surfaces the shape.
