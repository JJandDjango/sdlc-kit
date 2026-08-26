# Phase 0 notes - intake between a PO team and an engineer team

_Session 27, 2026-08-25. Working notes, not a Cairn stratum. Graduates to
USAGE.md if it earns a permanent home._

## The claim

- **Valid** = the contract passes the doors. Mechanical, shipped, loops on
  the agent in seconds.
- **Sound** = the contract says what the PO meant. Human. The kit checks
  form, never meaning ("wrong-but-clear passes"; THEORY names the oracle
  problem a non-goal).
- Order: valid first, sound second. Human attention is the scarce
  resource; spend it only on artifacts that already pass form.

## The doors (valid)

Three rejection reasons (criteria unwritable, dependencies unresolved,
scope unbounded) decomposed into eight fields (ADR 0005). Each diagnostic
is a question the agent asks, never a guess it makes:

| Diagnostic | The question it forces |
|---|---|
| TC002 `non_goals` empty | "What is this not?" |
| TC004 unit without a sketch | "What would you look at to know it is done?" No answer = unwritable. |
| TC007 intent out of bounds | the scaffold is born red; nothing passes vacuously |
| TC003 dependency unresolved | park as draft, name the blocker, refuse handoff |
| TC010 / TC011 term missing or draft | fork `specs/vocabulary/<term>.yaml`; never ratify to go green |
| TC013-TC015 unit graph | duplicate id, dangling `depends_on`, cycle |
| CL006 / CL008 / CL009 / CL012 | unknown word, sentence cap, modal, verb-first sketch: the agent rewrites; the PO never writes the controlled register |

Venue: `/sdlc intake` (SKILL.md I1-I7). Doors: `taskcontract validate
--profile ready`, the G0.2 vocabulary join, `lang-check`.

## The seats (sound)

1. **Term ratification.** "discount" becomes an executable definition both
   teams are bound to. Class-S flip; the PR merge is the record. Shipped;
   the strongest Phase 0 lever.
2. **Per-unit confirmation.** The venue renders the unit graph and needs a
   human answer per `done_means` before writing. Approved session 26,
   unlanded (SKILL.md at the 4000-token wall).
3. **`intent` and `non_goals` in the PO's words.** Every G1 criterion must
   reconcile with the intent (ADR 0005); non-goals fix the negative space
   scope-creep detection needs.

Bridge: `acceptance_sketch`. Existence is mechanical, goodness is human;
writing one is the cheapest soundness probe there is.

## Seat map (ratified 2026-08-26)

| Field | Seat |
|---|---|
| `intent`, `non_goals`, `provenance` | PO team, their words |
| domain-term ratification | PO team (the principal for meaning) |
| `scope` (paths), `decomposition`, `depends_on`, `dependencies` | engineer team |
| technical-term ratification | engineer team |
| `acceptance_sketch` | both: PO names the observable, engineer confirms a test could decide it |
| the YAML | neither; the agent authors and loops, both answer |

The intake session is the meeting. One artifact, both teams present,
ready-green or parked with a named blocker at the end.

## Not ensured at Phase 0

- Completeness over requirements. G0 checks completeness over units. "Did
  we think of everything" is G1.3 items 4-8 (complete over units, covers
  the sketch, consistent, respects non-goals, boundary + error path per
  input surface).
- Meaning. Judged at G1.3 on criteria. Escapes return as
  `provenance: g8-escape` tasks and new immutable criteria; prose
  ambiguities become dictionary bans. The set converges; it is never
  asserted complete.

## Example - `Pricing.ApplyDiscount(decimal price, int percent)`

Ready-green at schema 1.2.0 (validated 2026-08-25 as a loose file: schema
only, no vocabulary join). Graph: `discount-core --> discount-guards`.

```yaml
id: apply-discount

intent: >-
  The checkout summary needs one pure function that applies a whole
  percent discount to a line price and returns the discounted price in
  cents. Out-of-range input fails loudly. Rounding follows the house
  money rule.

scope:
  - src/Checkout/Pricing/
  - tests/unit/Checkout/Pricing/

non_goals:
  - No compound or stacked discounts.
  - No currency handling. Input and output share one currency.
  - No persistence and no UI.

decomposition:
  - id: discount-core
    unit: discount-core
    done_means: >-
      `Pricing.ApplyDiscount(decimal price, int percent)` returns the
      price reduced by the percent, rounded to cents by the house rule.
    acceptance_sketch:
      - verify 100.00 at 25 percent returns 75.00
      - verify a half-cent result rounds by the house rule
      - verify 0 percent returns the price and 100 percent returns 0
  - id: discount-guards
    unit: discount-guards
    depends_on: [discount-core]
    done_means: >-
      A percent outside 0 to 100 or a negative price raises an argument
      error naming the parameter.
    acceptance_sketch:
      - verify percent 101 and percent -1 each raise, naming percent
      - verify a negative price raises, naming price

dependencies: []

provenance:
  origin: human-request
```

**Do**

- Intent in outcome terms, PO words: what is true after that is not true
  now.
- Non-goals name the tempting neighbors: stacking, currency, UI.
- One sketch per observable, verb-first, with numbers: "verify 100.00 at
  25 percent returns 75.00".
- Scope as paths (`src/Checkout/Pricing/`): the baseline later diffs are
  checked against.
- Declare `entities: [discount, line-price]` once ratified; fork the term
  when TC010 fires.
- Carry the ambiguity forward visibly: "rounds by the house rule" is a
  valid sketch and an unsound criterion. G1.3 decides it. Decided
  2026-08-26: the third decimal decides, 4 or less rounds down, 5 or
  more rounds up (`MidpointRounding.AwayFromZero` for non-negative
  amounts); REQ-002 reads "ApplyDiscount(1.25m, 50) returns 0.63m".

**Do not**

- Let the agent pick the house rule. A sketch carries it only if the PO
  said it.
- Ratify a term to turn the contract green.
- Write scope as feature names, or decomposition as implementation steps.
- Use "should" or an unbounded comparative ("faster"): CL009 / CL011
  reject them, and G1.3 item 2 rejects the survivors.
- Treat ready-green as sound, or hand off from red or parked.
- Edit a ready contract. It is immutable to implementers (write-surface
  rule, ADR 0010).

## Decided 2026-08-26 (the plan's own intake confirmation, by hand)

- Plan to completeness: `specs/intake-seats/contract.yaml`, all nine
  units kept; graph via `taskcontract graph`; draft term
  `specs/vocabulary/intake-seat.yaml`; steps in `plan.md`.
- Skill flows: split into reference files (not a one-time trim); the
  ADR records it.
- Seat map: as tabled above.
- REQ-002 rounding: half up on the third decimal (0.63), see the example.

## Open

- ~~I5 render + confirm~~: landed 2026-08-26 (units 3 and 8; `flows/intake.md`
  I5-I6). The three seats now have mechanical form: seat term
  (`intake-seat`), `confirmed_by` per unit, TC016 at the door.
- The G1 handoff is paper today: `criteria.yaml`, the `[Criterion]` trait,
  and the G4.3 join are designed (ADR 0011), unbuilt; a separate task by
  the plan's own non-goal.

Sources: docs/gates/G0-planning-intake.md; decisions/0005, 0006, 0010,
0011, 0017, 0022, 0024; skills/sdlc/SKILL.md (I1-I7); docs/vocabulary.md;
docs/controlled-language.md; docs/task-contract.md.
