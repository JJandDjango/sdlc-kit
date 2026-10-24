## 8. Intake with more than one seat 🟢

> 🟢 **Shipped** (kit 0.12.0, [ADR 0025](../../decisions/0025-intake-seats.md)):
> the seat term, `confirmed_by`, TC016, and intake's confirm-and-write step.

Intake takes a human answer for every unit before a contract lands.
When the humans are two teams (a PO team that owns the request, an
engineer team that owns the decomposition), the kit gives each a
**seat**, records which seats answered for each unit, and checks that
record at the door. 🟢 Every repo needs a roster (kit 0.14.0,
[ADR 0030](../../decisions/0030-a-doors-input-is-a-declaration.md)): a repo
with one human ratifies a one-value roster before its first contract
reaches `ready`, and that one seat answers for every unit. See §4, "What
`ready` requires".

### The seats: a term you ratify

Seats are a `value-set` term in your own vocabulary, one value per
seat, ratified by you:

```yaml
# specs/vocabulary/intake-seat.yaml
term: intake-seat
name: Intake seat
definition: A human position that answers for a decomposition unit at intake.
kind: value-set
values: [po, engineer]
status: ratified
since: 2026-09-01
```

The roster is per-repo on purpose: who your humans are is your
meaning, not the kit's schema.

### The field each seat holds

The kit's default map for a PO team and an engineer team. It is policy
you record, never a check the door runs: the door reads the answer,
not the author.

| Field | Seat |
|---|---|
| `intent`, `non_goals`, `provenance` | PO, in their words |
| `entities` | PO: the ratified terms the request names, or `[]` on their answer |
| domain-term ratification | PO |
| `scope` (paths), `decomposition`, `depends_on`, `dependencies` | engineer |
| technical-term ratification | engineer |
| `acceptance_sketch` | both: the PO names the observable, the engineer confirms a test could decide it |
| the YAML itself | neither: the agent authors it and loops the doors; both seats answer |

🟢 The engineer seat's three answers are the playbook's plan questions,
asked in those words at I4 and I5: which files change (`scope`), in what
order (`depends_on`), which tests prove it (`acceptance_sketch`) (kit
0.13.0).

🟢 When the raw request is a feature document, intake reads the three
from its Scope, Order and Units sections and asks the engineer seat to
keep or change them.

### The answer record 🟢

Every unit names the seats that answered for it:

```yaml
  - id: discount-core
    unit: discount-core
    confirmed_by: [po, engineer]
    done_means: ...
```

- 🟢 `confirmed_by` (schema 1.3.0, additive): optional in the schema, a
  unique list of seat values, at least one. Adding it broke no contract
  written against 1.2.0.
- 🟢 G0.3 at the ready door: with `intake-seat` ratified, a unit with no
  `confirmed_by`, or one naming a seat the term lacks, fails with
  `TC016`. From kit 0.14.0 (ADR 0030), a draft term or no term fails
  every contract in the specs tree with `TC018`, which names the file to
  author. The `draft` profile never runs the check.
- 🟢 Intake writes it: after drafting the decomposition, intake renders
  the unit graph, asks for an answer per unit, writes `confirmed_by`,
  and only then writes the contract. A red door after the write reports
  the findings and returns.

The PR merge stays the outer record: `confirmed_by` says who answered
for each unit; the merge says the contract as a whole was approved.

### Running intake with both teams

One session, both seats present, one artifact. The agent authors the
YAML from the raw request and loops the doors; the seats answer what
the diagnostics ask. `non_goals` empty: "what is this not?" A unit with
no sketch: "what would you look at to know it is done?" A noun with no
ratified term: fork the term, and never ratify it just to go green.
The session ends ready-green or parked with a named blocker;
development starts only from green.

Brownfield, before the first intake: `/sdlc vocab extract` over your
declared surfaces (API baselines, schemas, domain types, docs); the PO
seat ratifies the domain terms and the engineer seat the technical
ones; then ratify `intake-seat`.

### Worked example: `ApplyDiscount`

Raw request: "add a helper that applies a percent discount to a line
price for the checkout summary." Intake lands this contract (shown as
it reads under 1.4.0, answers and declarations included):

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
    confirmed_by: [po, engineer]
    done_means: >-
      `Pricing.ApplyDiscount(decimal price, int percent)` returns the
      price reduced by the percent, rounded to cents by the house rule.
    acceptance_sketch:
      - verify 100.00 at 25 percent returns 75.00
      - verify a half-cent result rounds by the house rule
      - verify 0 percent returns the price and 100 percent returns 0
  - id: discount-guards
    unit: discount-guards
    confirmed_by: [po, engineer]
    depends_on: [discount-core]
    done_means: >-
      A percent outside 0 to 100 or a negative price raises an argument
      error naming the parameter.
    acceptance_sketch:
      - verify percent 101 and percent -1 each raise, naming percent
      - verify a negative price raises, naming price

dependencies: []

entities:  # terms this repo's glossary holds ratified (§5)
  - line-price
  - discount

provenance:
  origin: human-request
```

Notice what it leaves open: "the house rule" for rounding. That is
correct at G0, where the door checks that a sketch exists, never that
it is good. The decision belongs to the spec reviewer, taken on the
criteria before any code exists. Here it was: the third decimal
decides, 4 or less rounds down, 5 or more rounds up
(`MidpointRounding.AwayFromZero` for non-negative amounts), so
`ApplyDiscount(1.25m, 50)` returns `0.63m`. A reviewer who would have
caught that late in a PR now decides it once, up front, and it becomes
a test the implementer cannot edit.
