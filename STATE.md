# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-08-03 (session 24 close)._

## Now
- Session 24 (2026-08-03): **the 0.9.0 post-merge sequence ran
  whole.** PR #26 had merged (54717cf) with the v0.9.0 tag still
  unlanded; the tag landed first (annotated, at the merge), then the
  self-pin PR #27 (db11ab4): both scaffold refs -> v0.9.0 and the
  kit's own workflow gained the controlled-language step the
  template already carried (the v0.8.0 pin predated the subcommand;
  ADR 0022). Merged at 793c9b6. The contracts job proved the tag
  install (pip install @v0.9.0) and ran the lang-check door in the
  kit's own CI for the first time - green (contracts 15s, test 13s);
  local run lang-green, the six pre-arc contracts printing exempt
  warnings, never gating.
- The #26 merge carried the dictionary set-ratification (seed grew
  by `exempt` + `binds` during self-adoption - flagged, ratified at
  merge).
- Receipts: kit 0.9.0 tagged + self-pinned; suite 188; validate 7/7
  ready-green; lang-green armed in CI; main 793c9b6, tree clean at
  close.
- Prior close: session 23 (7f5c21f) - controlled language v1
  designed in a live walk and shipped whole (dcb22c7, ADR 0022).

## Blockers
- None.

## Next actions
1. **Pilot M0 session** (engine repo): first profile-aware consumer -
   dotnet payload spans G3 + G4 core, operators to exercise, and the
   controlled-language machinery brownfield-style; Q5 reality data +
   the trace-fed curation feed both start here.
2. User act pending: class-S flips for `controlled-dictionary` +
   `controlled-field` (still drafts).
3. Registered continuations: PL-PIPE.3 eval harness (comprehension
   family - paired prose variants, loop counts, divergence);
   sdlc-spec / sdlc-qa defs behind venue existence; mechanical loop
   runner; verdict field-name convergence (dedicated pass).
4. Controlled-language deferrals, triggers on record: base verb
   promotion (self-host evidence), F-item region checking, prompt
   lexicon (foundations-side PromptLang extension), slot templates
   (per-field escape evidence), greenfield day-one arming.
5. Deferrals unchanged: Q4 numbers (lang caps + escape-rate
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
