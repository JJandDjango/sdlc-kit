# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-08-26 (session 27 close, home machine)._

## Now
- Session 27 (2026-08-25 to 2026-08-26) walked Phase 0 for a two-team
  consumer (PO team + engineer team), captured the walk in
  NOTES_phase0_2026-08-25.md (valid before sound; the doors; the three
  human seats; the seat map; do/don't on the ApplyDiscount toy), then
  ran the `intake-seats` contract to completion on branch
  `session-27-intake-seats`: nine units, ten unit commits plus this
  close, every unit confirmed in chat and committed on the user's Go.
- What landed (kit 0.12.0, ADR 0025): an intake seat is a per-repo
  `value-set` term; every unit records who answered under
  `confirmed_by` (schema 1.3.0, additive); G0.3 unit confirmation at
  the ready door (TC016, armed only by a ratified `intake-seat` term,
  draft profile and loose files never enter); `/sdlc intake` I5-I6
  render, ask per unit, write the record, then the contract (closes
  unit-dag's `g0-intake-review`, so unit-dag is 8/8); the seven skill
  flows moved to `skills/sdlc/flows/<flow>.md` (SKILL.md 3978 -> 1852
  tokens, description trimmed on the user's word); the kit's own seat
  term ratified (`user`) and 66 units stamped, adds only; registry row
  `g0-3-unit-confirmation`; G0 registry and deep page (G0 count 1 -> 3,
  total 54 -> 56, G0.2 had gone uncounted); USAGE section 8; CHANGELOG
  0.12.0 with the delta note; CONVENTIONS line; pyproject + KIT_VERSION
  0.12.0.
- Receipts on the branch tip, zero-trust: suite 222 (213 + 8 door
  tests + 1 fixture); validate 10/10 ready-green with the door armed;
  vocab-green 18 terms, registry 7; lang-check exit 0 (six pre-arc
  contracts exempt); prompt_lang 8/8; Cairn 0 errors (ADR budgets stand,
  ADR-EDITED 0024 expected, DOCS-STALE from the adds-only migration).
- The plan graph is published as an artifact (private):
  https://claude.ai/code/artifact/44b0c146-6441-4a00-8163-bad5ea6bee20
- Rulings on record this session: REQ-002 for the toy rounds half up
  on the third decimal (1.25 at 50 -> 0.63); the seat map is consumer
  policy in USAGE section 8, never a check on the author.

## Blockers
- None in-kit. The branch is pushed and its PR open at close; merge,
  tag, and self-pin are the user's acts (Next actions 1-2).
- `/sdlc audit` on this machine reports TC005 on every `id`: audit.py
  imports `taskcontract` and gets the pip-installed copy pinned at
  e81f9a5 (July), while `python -m taskcontract` from the repo root
  shadows it and is current. Fix: `pip install -e E:\sdlc_development_kit`
  here (and the same on the work machine). Not a finding against the
  code.

## Next actions
1. Merge the PR on green. The kit's CI validates with the branch's
   validator regardless of the pin (`python -m` from the checkout
   root shadows the install; verified against PR #33's run). The
   plugin marketplace tracks main, so the other machine sees 0.12.0
   only after the merge: `/plugin marketplace update sdlc-kit`, then
   `/plugin update`.
2. Tag `v0.12.0` at the merge commit; self-pin PR moving the workflow
   pin and the USAGE uv line to v0.12.0 (contracts check proves the tag
   installs), per the v0.11.0 precedent.
3. Work-side upgrade (work machine): re-pin to v0.12.0; the id
   migration is still owed there (v0.10.0 -> 1.3.0: add `id` per unit,
   TC001 until done); then `/sdlc vocab extract`, the PO seat ratifies
   domain terms, the engineer seat technical ones, ratify `intake-seat`
   with `[po, engineer]`, stamp `confirmed_by` in the same commit.
4. Prompt lexicon arc (user's stated intent, a later session): bring
   the skill prompts under the controlled dictionary. Measured
   2026-08-26: 395 of 1990 checkable words unknown (20%). A decision
   first (new controlled surface, ~200-300 dictionary additions on the
   full lane; PromptLang owns form), never a tidy-up.
5. The G1 slice is the next kit surface the user's stated goal needs
   (plan -> tests): `criteria.yaml` + `[Criterion]` trait + the G4.3
   join (ADR 0011, designed, unbuilt); the ApplyDiscount toy is its
   first fixture. Small graph follow-ups banked: `graph --labels`
   (summaries in nodes), `graph --done` (ready set from a done list).
6. Registered continuations unchanged: PL-PIPE.3 eval harness,
   sdlc-spec / sdlc-qa defs, mechanical loop runner, verdict field-name
   convergence, `.sdlc/progress/<id>.yaml`, direction classifier (0014
   Q6), runner probe at work.

## Open questions
- Order of the next two arcs: the G1 slice (the user's stated goal) or
  the prompt lexicon (the user's stated intent). Recommend G1 first;
  the lexicon waits on a PromptLang-side extension either way.
- Q4 thresholds, Q5 decorrelation, Q6 first analyzer tranche,
  comprehension empirics (PL-PIPE.3): unchanged from 25.
