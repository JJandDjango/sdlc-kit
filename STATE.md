# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-08-31 (session 27 release wrap, home machine)._

## Now
- v0.12.0 is released. Session 27 (2026-08-25 to 2026-08-31) walked
  Phase 0 for a two-team consumer (PO team + engineer team), captured
  the walk in NOTES_phase0_2026-08-25.md, then ran the `intake-seats`
  contract to completion: nine units, each confirmed in chat and
  committed on the user's word. PR #36 merged at 8fbaa7f; tag v0.12.0
  annotated there and pushed; self-pin PR #37 carries the pin move and
  this regeneration, both checks green (the contracts job is the proof
  the tag installs). Merging #37 is the last act of the release.
- What shipped (ADR 0025, detail in CHANGELOG 0.12.0): an intake seat
  is a per-repo `value-set` term; every unit records who answered under
  `confirmed_by` (schema 1.3.0, additive); G0.3 unit confirmation at
  the ready door (TC016, armed only by a ratified `intake-seat` term,
  draft profile and loose files never enter); `/sdlc intake` I5-I6
  render, ask per unit, write the record, then the contract (this
  closed unit-dag's `g0-intake-review`, so unit-dag is 8/8); the seven
  skill flows moved to `skills/sdlc/flows/<flow>.md` (SKILL.md 3978 ->
  1852 tokens); the kit's own seat term ratified (`user`) and 66 units
  stamped, adds only; G0 registry and deep page (G0 count 1 -> 3, total
  54 -> 56, G0.2 had gone uncounted); USAGE section 8.
- Receipts, zero-trust: suite 222; validate 10/10 ready-green with the
  door armed; vocab-green 18 terms, registry 7; lang-check exit 0 (six
  pre-arc contracts exempt); prompt_lang 8/8; Cairn 0 errors.
- CI note worth keeping: GitHub Actions was in a major outage when #36
  merged, so that merge rode local receipts; the runs landed green
  afterwards (#36, the push to main, and #37). The kit's workflow runs
  `python -m taskcontract` from the checkout root, so the working
  directory shadows the pinned install: the kit's own CI always
  validates with the branch's validator, never the pin.
- Plan graph published (private artifact):
  https://claude.ai/code/artifact/44b0c146-6441-4a00-8163-bad5ea6bee20

## Blockers
- None. `/sdlc audit` on this machine still reports TC005 on every
  `id` and `confirmed_by`: audit.py imports `taskcontract` and gets the
  pip install pinned at e81f9a5 (July). Fix here and at work:
  `pip install -e E:\sdlc_development_kit`. Not a finding against the
  code.

## Next actions
1. Merge PR #37 (green), then sync main and delete the branch.
2. **Work-side upgrade** (work machine): `/plugin marketplace update
   sdlc-kit`, then `/plugin update`; re-pin the work repo to v0.12.0.
   Its contracts are still pre-1.2.0, so the id migration is owed
   first (TC001 until every unit carries an `id`), then `/sdlc vocab
   extract`, the PO seat ratifies domain terms and the engineer seat
   technical ones, ratify `intake-seat` with `[po, engineer]`, and
   stamp `confirmed_by` in the same commit as that flip.
3. **G1 slice** - the next kit surface the stated goal needs (a plan
   that executes into tests): `criteria.yaml` + the `[Criterion]`
   trait + the G4.3 join (ADR 0011, designed, unbuilt). The
   ApplyDiscount toy in USAGE section 8 is its first fixture. Two
   small graph follow-ups banked: `graph --labels` (unit summaries in
   nodes) and `graph --done` (ready set from a done list).
4. **Prompt lexicon arc** (user's stated intent, later session): bring
   the skill prompts under the controlled dictionary. Measured
   2026-08-26: 395 of 1990 checkable words unknown (20%). A decision
   first (new controlled surface, ~200-300 dictionary additions on the
   full lane; PromptLang owns form), never a tidy-up.
5. Runner probe at work; M0 pilot as the second consumer.
6. Registered continuations unchanged: PL-PIPE.3 eval harness,
   sdlc-spec / sdlc-qa defs, mechanical loop runner, verdict
   field-name convergence, `.sdlc/progress/<id>.yaml`, direction
   classifier (0014 Q6).

## Open questions
- Order of the next two arcs: the G1 slice or the prompt lexicon.
  Recommend G1 first; the lexicon waits on a PromptLang-side
  extension either way.
- Q4 thresholds, Q5 decorrelation, Q6 first analyzer tranche,
  comprehension empirics (PL-PIPE.3): unchanged from 25.
