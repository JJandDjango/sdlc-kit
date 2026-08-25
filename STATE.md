# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-08-24 (session 26 close, home machine)._

## Now
- Session 26 (2026-08-22 to 2026-08-24) shipped v0.11.0, the
  unit-graph release (ADR 0024): unit ordering moves into the task
  contract. Every decomposition unit carries a required `id`;
  `depends_on` names the units it comes after; the door rejects
  duplicate ids (TC013), dangling refs (TC014), and cycles (TC015) in
  both profiles; `taskcontract graph <file>` renders Mermaid,
  byte-identical across runs, computed and never committed. Schema
  1.1.0 -> 1.2.0 is breaking; CHANGELOG 0.11.0 carries the delta
  note and migration recipe. PR #33 (12 commits) merged at 257ca1c,
  tag v0.11.0 -> 257ca1c, self-pin PR #34 merged at 3a172c3; the
  contracts check proved the tag installs. main == origin/main ==
  3a172c3, tree clean apart from the untracked request doc.
- Intake for the 2026-08-22 relayed request ran through `/sdlc
  intake`: specs/unit-dag/contract.yaml, ready-green first pass,
  prose authored inside the closed dictionary with zero delta (links
  for edges, loop for cycle, unit for node, execution state for
  progress). The orphaned specs/glossary-alias-disjointness/ contract
  (drafted 8/7, never committed) was validated ready-green and landed
  unedited at 65d52c1.
- Four approvals taken in chat on rendered before/after text, each
  its own commit: G0.1 class-E tightening (da3e66c);
  controlled-dictionary + controlled-field ratified, glossary now
  17/17 ratified (6c52216); MAP.md row naming all 13 gate deep pages,
  Cairn orphans 13 -> 0 (074d13a); intake I4 authors ids and
  depends_on (2005c93, partial - see Blockers).
- unit-dag contract: 7 of 8 units closed. Open: g0-intake-review.
- Record corrections this session: docs/task-contract.md E1 ("No
  per-unit id") now carries the 0024 amendment; ADR 0024 amended in
  place pre-merge to own the supersession (Cairn reports ADR-EDITED
  on it, expected). ADR 0014's direction classifier does not exist
  yet - class-E tightenings still take the human lane; recorded in
  0024 and PR #33.
- Receipts at close, zero-trust on main: suite 213 (190 -> 213);
  validate 9/9 ready-green; vocab-green 17 terms, registry 6;
  lang-green with the six pre-arc contracts exempt; /sdlc audit
  clean, 6 informational; Cairn audit 0 errors, 21 warnings (13 ADR
  budget - stand; ADR-EDITED 0024; 6 DOCS-STALE from the id
  migration touching contracts whose pages did not change - accept;
  STATE-STALE clears with this regeneration).

## Blockers
- g0-intake-review cannot close as approved: skills/sdlc/SKILL.md
  sits at ~3978 tokens against PromptLang's 4000 fail threshold, and
  the approved I5 RENDER + CONFIRM step costs ~45 even at one line
  (measured: approved wording 4149, maximal compression 4036, step
  dropped passes). No workaround taken - raising the threshold or
  compressing unrelated approved text are both the user's call.
  Recommended: trim the frontmatter `description` (~200 tokens of
  subcommand re-listing) on the class-E lane, then land the step.

## Next actions
1. **Work-side upgrade** (from the work machine): update the plugin
   (`/plugin marketplace update sdlc-kit`, then `/plugin`); bump the
   work repo's workflow pin to `@v0.11.0`; migrate its contracts
   (add `id` per unit, derived from the unit slug; the scratchpad
   migration script from this session is not in the kit - offered as
   a kit surface if wanted). Expect TC001 on every pre-1.2.0 contract
   until migrated. Note the local plugin cache pin was e81f9a5
   (2026-07-29, session 17) - two releases behind - which is why
   audit.py reported false TC005s against ids this session.
2. **Close g0-intake-review**: rule on the SKILL.md headroom (see
   Blockers), then land I5 RENDER + CONFIRM and the criteria line.
3. **Runner probe** at work (GitHub-hosted vs self-hosted) - still
   the first fact that decides whether the parked distribution
   fallbacks wake. Unchanged from session 25.
4. M0 pilot (engine repo) remains the second consumer, starting
   with work findings in hand. Cargo lane parked until ImSim.
5. Registered continuations unchanged: PL-PIPE.3 eval harness,
   sdlc-spec / sdlc-qa defs, mechanical loop runner, verdict
   field-name convergence, `.sdlc/progress/<id>.yaml` execution
   state (ruled in 0024, unbuilt), direction classifier (0014 Q6).

## Open questions
- SKILL.md headroom: trim the description, split flows into a
  reference file, or leave the render step open? Every future
  addition to the intake venue hits the same wall.
- Should the id-migration script ship as a kit surface (a
  `taskcontract migrate` subcommand or a skill step) before the
  work repo upgrades, or is the CHANGELOG recipe enough?
- Runner posture at work (unchanged).
- Q4 thresholds, Q5 decorrelation, Q6 first analyzer tranche,
  comprehension empirics (PL-PIPE.3) - all unchanged from 25.
