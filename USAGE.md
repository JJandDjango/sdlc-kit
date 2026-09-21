# Using the SDLC Kit

> 🟢 **v1 shipped** — every flow on this page is implemented and proven
> by the kit's regression suite plus live greenfield + brownfield smoke
> runs (no-clobber included). Sections marked 🔴 are ratified but not
> yet shipped.

The kit lays a **gate spine** into a repository: immutable task
contracts under `specs/`, a gate status page, config + ledgers under
`.sdlc/`, and CI that validates every contract. This is the explicit
guide; `README.md` is the short overview.

**The whole idea in one sentence:** a task may not enter development
until its contract validates `ready`, and nothing the implementer can
edit is allowed to weaken that check.

---

## 1. When to run it

| Situation | Run `/sdlc`? | Mode |
|---|---|---|
| Brand-new repo (start here) | Yes — after `/cairn` if you use it | greenfield |
| Existing codebase adopting gates | Yes | brownfield |
| Repo already initialized | No — use `intake` / `new` / `audit` | — |

Greenfield and brownfield get the same payload; the difference is
recorded in `.sdlc/config.yaml` (`adoption:`) and brownfield relies on
no-clobber — anything you already have is skipped, never overwritten.

---

## 2. Install

```bash
cp -r skills/sdlc ~/.claude/skills/sdlc                     # macOS / Linux
Copy-Item -Recurse skills\sdlc $HOME\.claude\skills\sdlc    # Windows
```

or, as a plugin:

```
/plugin marketplace add JJandDjango/sdlc-kit
/plugin install sdlc@sdlc-kit
```

(The plugin is named `sdlc`, the marketplace `sdlc-kit` — the qualified
id always resolves; bare `sdlc-kit` does not.) Pick **one** channel: if
you adopt the plugin after a skills-dir install, delete
`~/.claude/skills/sdlc` so `/sdlc` doesn't surface twice — the plugin
also tracks kit updates, the copied dir does not.

Target repos additionally consume the validator via pip (CI does this
automatically from the scaffolded workflow):

```bash
pip install git+https://github.com/JJandDjango/sdlc-kit.git
```

Reload the Claude Code session after installing — skills list at
startup.

---

## 3. `/sdlc` — initialize a repo

Run it in the target repo. It asks:

| # | Answer | What it drives |
|---|---|---|
| 1 | **project name** | Titles the gate status page. |
| 2 | **adoption** — greenfield / brownfield | Recorded in config; brownfield leans on no-clobber. |
| 3 | **stack** — free text (e.g. `dotnet`, `python`, `typescript`) | Recorded in config for the activation program; v1 payload is stack-neutral. |

If a Cairn spine is absent it recommends `/cairn` first (never
requires it, never touches Cairn's files).

### What you get

```
SDLC.md                     gate status page — which gates are live here (🟢/🔴)
.sdlc/config.yaml           adoption, stack, kit ref, active gates
.sdlc/clocks.yaml           numeric gate parameters — seeded placeholder defaults
.sdlc/reds.yaml             standing-red ledger — starts empty
.sdlc/findings/TEMPLATE.yaml  return-channel finding form (§7, the membrane)
.sdlc/NOTICE.md             provenance of the vendored scaffold (§7)
specs/README.md             the protected root: contracts live at specs/<task-id>/contract.yaml,
                            immutable to implementers (write-surface rule)
.github/workflows/sdlc.yml  CI: pip-install the kit, validate every contract
.sdlc/hooks/protect_specs.py  session hook: the spec channel closed to sessions (§4)
.sdlc/REVIEW.md             the advisory review pass, yours to edit (§4)
.pre-commit snippet         task-contract ready check (written if absent, else printed)
.vscode/settings.json       YAML schema mapping for contract editing (written if absent, else printed)
.claude/settings.json       the hook wired for Edit/Write/MultiEdit/NotebookEdit (written if absent, else printed)
```

**Never overwrites.** Existing files are skipped and reported —
brownfield adoption is additive by construction.

---

## 4. Day 2 — the contract flow

### `/sdlc:product-specification-interview` — writing the feature document 🟢

> 🟢 **Shipped** (kit 0.13.0, [ADR 0028](decisions/0028-specification-interview-skill.md),
> contract `specs/spec-interview/`); the tag lands with `playbook-guardrails`.

Intake consumes a feature document (§8, ADR 0026). This skill writes one.
Run it in the target repo with a slug for the feature:

```
/sdlc:product-specification-interview csv-export
```

🟢 It asks the template's sections one question at a time: the path, the
origin (feature or bug fix; a bug fix also takes the incident reference
and its regression scenario), the seats, and any material you paste
first; then
the story and background, three to five success criteria with two or
three Gherkin scenarios each, non-goals, previously defined items,
prerequisites, business requirements, and open questions. The
Implementation section is asked only when an engineer seat is named. A
sixth success criterion prompts a split into two documents. State saves
after every section to a file beside the document, so a later run resumes
at the exact question.

🟢 Before writing, it reads the document back and checks what intake will
need: an outcome-shaped story, a non-goal, scenarios under every
criterion, seats named. Gaps are marked OPEN. The check advises and never
blocks, because the document is yours.

🟢 **What it writes:** the document, in the template's shape, at a path
you confirm (default `REQUEST_<slug>_<date>.md` at the repo root), plus
its state file. It never overwrites, never touches `specs/`, and never
runs intake. On request it renders the same document paste-ready for
Google Docs.

**Next step:** it ends by naming the command that consumes the document:

```
/sdlc intake REQUEST_<slug>_<date>.md
```

🟢 Every prompt file of the skill passes `python -m prompt_lang`, and a
structural test in the suite holds the shape.

### `/sdlc intake` — the G0 venue
Give it a raw request ("add CSV export"). The agent authors
`specs/<task-id>/contract.yaml` — intent, scope, non-goals,
decomposition with a done-meaning and 1–3 acceptance-sketch criteria
per unit, dependencies, provenance — then loops

```bash
python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
```

until green, and refuses the handoff to spec/implementation while red.
A blocked dependency parks the contract as a valid `draft`; `ready` is
what gates entry into development. 🟢 With a ratified seat term (§8),
intake also takes a human answer per unit and records it under
`confirmed_by` before the contract lands (kit 0.12.0).

### What `ready` requires — two declarations 🔴

> 🔴 **Ratified, not shipped** ([ADR 0030](decisions/0030-a-doors-input-is-a-declaration.md),
> contract `specs/g0-declaration/`, kit 0.14.0, schema 1.4.0). Marks flip green as the units land.

🔴 At the `ready` profile, the input a door reads is required, so a green
G0 means every condition checked something. A contract carries
`entities:`, the glossary terms it operates on (§5). An empty list is valid
and is a statement: `entities: []` says the contract operates on no
glossary term. A contract with no field fails `TC017`. `/sdlc intake`
always writes the field, and writes `[]` only on the PO seat's confirmed
answer; `taskcontract new` names the field in a comment and sets no value.

🔴 Inside a specs tree, a ratified `intake-seat` (§8) must exist before any
contract reaches `ready`. With the term absent or at draft, every contract
fails `TC018`, and the diagnostic names the file to author:
`specs/vocabulary/intake-seat.yaml` (`/sdlc vocab add intake-seat` drafts
it; ratifying it is yours). Intake checks this first and stops before
authoring. Greenfield `/sdlc init` asks who holds the seats and seeds the
term; a repo with one human ratifies a one-value roster. The `draft`
profile is unchanged: a parked contract may carry neither.

🔴 **Adopting on an existing repo needs no re-intake.** The session hook
protects only a contract that validates `ready`, so a contract the new
door fails is open to the edit that repairs it, and locks again once it
passes. After the upgrade, a `ready` contract with no `entities:` fails
`TC017`: add the field, and it locks. The roster works the same way:
ratify `intake-seat`, each contract fails `TC016` until its units carry
`confirmed_by`, stamp the answers, and the contracts lock again. Pin the
kit ref in your workflow (§2) so an upgrade is a choice, never a surprise.

### `taskcontract new <id>` (or `/sdlc new <id>`)
Scaffolds the 8-field contract skeleton at
`specs/<id>/contract.yaml` with inline field guidance. The id must
match `^[a-z][a-z0-9-]{2,63}$`.

### `/sdlc audit`
Report-only health check — exit 0 clean / 1 findings / 2 no `.sdlc`
here. Checks: config + ledgers parse, every contract validates, the
payload surfaces exist, CI job present. It never writes; fixes stay
with you.

### The session hook — `.sdlc/hooks/protect_specs.py` 🟢

> 🟢 **Shipped** (kit 0.13.0, [ADR 0027](decisions/0027-playbook-crosswalk-and-closures.md)
> gaps 1, 2, and 6a, contract `specs/playbook-guardrails/`).

🟢 `/sdlc init` renders a Claude Code hook at `.sdlc/hooks/protect_specs.py`
and wires it into `.claude/settings.json` (a merge target: written when
absent, printed when present) for Edit, Write, MultiEdit, and NotebookEdit.
Under `specs/` the hook denies: a contract that validates `ready` ("a
change re-intakes"), a term with `status: ratified` ("a class-S edit in
review"), and every other file there (the spec channel). Drafts stay
writable: intake edits the contract it is authoring. With no kit installed
the hook denies everything under `specs/`. The wired command names
`python`; where only `python3` resolves (macOS, some Linux), change the
word in the settings file, which is yours after the first write.

🟢 Outside `specs/`, the hook warns, never denies, when a write leaves the
bound contract's `scope`. The session's contract is the branch name when
`specs/<branch>/` exists, else `SDLC_CONTRACT`; with neither, the hook
stays silent. Denial outside the spec channel waits for wave B.

🟢 An organization pins the hook for every session with managed settings,
which user and project settings cannot override: copy
`skills/sdlc/templates/reference/managed-settings.json` from the kit to
the platform's managed-settings path (`/Library/Application
Support/ClaudeCode/managed-settings.json` on macOS,
`/etc/claude-code/managed-settings.json` on Linux,
`C:\ProgramData\ClaudeCode\managed-settings.json` on Windows). Its command
runs the hook only where `.sdlc/hooks/protect_specs.py` exists, so repos
without the kit are untouched. `/sdlc update` tracks drift on the rendered
hook (kit-owned), never on your settings file.

### `taskcontract scope-check` — G4.12 and the `Contract:` trailer 🟢

🟢 Every commit names its contract in a git trailer, parsed like the
`Theory:` trailer:

```
Contract: csv-export
```

🟢 `python -m taskcontract scope-check --base <sha>` reads the trailers of
the range, resolves each contract's `scope`, and fails on a path outside
it: SC001 (a path outside scope), SC002 (a commit with no trailer touching
a bound path), SC003 (a trailer naming no contract). A commit with no
trailer passes when it touches only free paths (`scope_check.free_paths`
in `.sdlc/config.yaml`, seeded with the docs spine, the plan, the
changelog). `--json` emits the findings envelope; exit 1 on findings, 2
when no base can be resolved.

🟢 The scaffolded CI runs it on every pull request as G4.12, "the diff
stays within its contract's scope" (registry: [docs/gates.md](docs/gates.md)).

### `.sdlc/REVIEW.md` — the advisory review pass 🟢

🟢 `/sdlc init` renders `.sdlc/REVIEW.md`, yours to edit (consumer class):
what a reviewer, human or agent, checks on a pull request beyond the
mechanical gates: the diff against the contract's `scope` and `non_goals`,
each unit's `acceptance_sketch` against the tests that landed, and the
write surface (nothing under `specs/`, no test weakened). The pass is
advisory: it blocks nothing. An escape it should have caught adds an
agent eval in wave B (`playbook-loop`).

---

## 5. Vocabulary — executable shared language 🟢

> 🟢 **Shipped** (kit 0.3.0, [ADR 0017](decisions/0017-vocabulary-layer.md)) —
> deep page: [docs/vocabulary.md](docs/vocabulary.md), including the
> constraint registry (`specs/vocabulary/constraints.yaml`, class E).

The terms your tasks operate on become per-term YAML files under
`specs/vocabulary/` — validated at the door, joined at G0.

| Command | What it does |
|---|---|
| `/sdlc vocab` | Computed listing of the glossary (no stored index) |
| `/sdlc vocab add <slug>` | Scaffold one term skeleton, born `draft` |
| `/sdlc vocab extract` | Draft terms from declared surfaces (APIs, schemas, docs) with `sources:` provenance |

Engine equivalents for CI and scripts: `python -m taskcontract
vocab-list` / `vocab-add <slug>` / `vocab-check` (the door — VTnnn
diagnostics; the scaffolded CI workflow runs it as a backstop step).

Contracts may declare `entities:` — the terms the task touches. G0
resolves each ref against **ratified** terms only: a missing or draft
term surfaces as an unresolved dependency naming the term — fork a
small vocabulary task; the work itself never fails for vocabulary.
Ratification stays deliberately human: flip `status: draft →
ratified` in the term file; the PR merge is the approval record.
Deprecation sets `sunset:`; the join warns inside the notice window
and errors past it.

Greenfield init seeds 5–15 terms through the interview (born
ratified); brownfield repos start with `vocab extract` and ratify the
keepers.

---

## 6. A worked example (greenfield)

```
mkdir billing-service && cd billing-service && git init
/cairn        → document why the project exists
/sdlc         → name: billing-service · adoption: greenfield · stack: python
/sdlc intake  → "Add invoice PDF export"
              → writes specs/invoice-pdf-export/contract.yaml, validates ready
# implement only what the contract scopes; CI re-validates every contract on push
/sdlc audit   → exit 0
```

Brownfield is the same flow on an existing repo — init skips whatever
already exists, and the first `intake` is where gate discipline
actually starts.

---

## 7. Restricted environments — the one-way membrane

> 🟢 **Shipped** (kit 0.10.0, [ADR 0023](decisions/0023-work-adoption-membrane.md)) —
> the policy, the findings form (`.sdlc/findings/TEMPLATE.yaml`), and
> the scaffold NOTICE (`.sdlc/NOTICE.md`).

Running the kit on code you cannot show outside (an employer, a
client) is a supported posture. Two facts make it safe by
construction:

- **The kit never phones home.** Every check is deterministic local
  Python — no network calls, no telemetry, no LLM anywhere in the
  enforcement path. The only network step is the pip install itself,
  pulling *from* public GitHub.
- **Flow is one-way.** The kit reaches your environment by public
  tag; nothing about your code travels back.

The discipline, one rule per direction:

| Direction | Rule |
|---|---|
| Kit → your repo | Install by pinned tag (`@vX.Y.Z`), never `main`. Upgrades are pull-only: re-pin, then `/sdlc update`. |
| Findings → upstream | File findings in controlled-dictionary terms, gate IDs, and counts — never code, never identifiers. The form at `.sdlc/findings/TEMPLATE.yaml` admits nothing else by construction. |
| Patches → upstream | Don't. Code written in your environment stays there; file a finding instead, and upstream re-implements the idea. |

**Mark your copy.** Every init renders `.sdlc/NOTICE.md` — upstream
URL, the rendering tag, the MIT license — so the vendored scaffold
reads as open source, not homegrown tooling, and the upgrade path
stays legible. Mirroring the whole kit inside your org? Copy that
file to the mirror root too.

**Local runs without managing Python.** CI needs nothing — hosted
runners ship Python, and the scaffolded workflow installs the kit
itself. For pre-push checks on a machine where you'd rather not
manage a Python install, `uv` (a single static binary, no Python
required to install it) runs the validator in an ephemeral
environment:

```bash
uv run --no-project --with "sdlc-taskcontract @ git+https://github.com/JJandDjango/sdlc-kit.git@v0.13.0" python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
```

---

## 8. Intake with more than one seat 🟢

> 🟢 **Shipped** (kit 0.12.0, [ADR 0025](decisions/0025-intake-seats.md)):
> the seat term, `confirmed_by`, TC016, and intake's confirm-and-write step.

Intake takes a human answer for every unit before a contract lands.
When the humans are two teams (a PO team that owns the request, an
engineer team that owns the decomposition), the kit gives each a
**seat**, records which seats answered for each unit, and checks that
record at the door. A repo with one human changes nothing: leave the
seat term unratified and the check stays off.

🔴 From kit 0.14.0 ([ADR 0030](decisions/0030-a-doors-input-is-a-declaration.md))
the roster is required: a repo with one human ratifies a one-value roster
before its first contract reaches `ready`. See §4, "What `ready` requires".

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
| domain-term ratification | PO |
| `scope` (paths), `decomposition`, `depends_on`, `dependencies` | engineer |
| technical-term ratification | engineer |
| `acceptance_sketch` | both: the PO names the observable, the engineer confirms a test could decide it |
| the YAML itself | neither: the agent authors it and loops the doors; both seats answer |

🟢 The engineer seat's three answers are the playbook's plan questions,
asked in those words at I4 and I5: which files change (`scope`), in what
order (`depends_on`), which tests prove it (`acceptance_sketch`). When the
raw request is a feature document with an Implementation section, intake
reads the three from it and asks the seats to keep or change them (kit
0.13.0).

### The answer record 🟢

Every unit names the seats that answered for it:

```yaml
  - id: discount-core
    unit: discount-core
    confirmed_by: [po, engineer]
    done_means: ...
```

- 🟢 `confirmed_by` (schema 1.3.0, additive): optional in the schema, a
  unique list of seat values, at least one. Contracts written against
  1.2.0 stay valid.
- 🟢 G0.3 at the ready door: with `intake-seat` ratified, a unit with no
  `confirmed_by`, or one naming a seat the term lacks, fails with
  `TC016`. A draft term or no term leaves the check off; a parked
  `draft` contract is never asked.
- 🔴 From kit 0.14.0 (ADR 0030): a draft term or no term fails every
  contract at the ready door with `TC018`, which names the file to
  author. A parked `draft` contract is still never asked.
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
it reads under 1.3.0, answers included):

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

---

## 9. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "`/sdlc` isn't listed" | Reload the Claude Code session after installing. |
| "It didn't overwrite my file" | By design (no-clobber). Edit the file in place, or delete it and re-run. |
| `TC003 dependency unresolved` | The contract is a parked draft — resolve or re-scope the dependency; `ready` requires all resolved. |
| `TC005 unknown field` | Contracts reject stray keys (`additionalProperties: false`) — a typo or scope smuggling; both fail loudly. |
| `TC016 unit not confirmed` (🟢 0.12.0) | The seat term is ratified here and a unit lacks `confirmed_by`, or names a seat the term does not list. Run intake's confirm step, or fix the value (§8). |
| CI job green with no contracts | Expected — the validate step is guarded until a `specs/*/contract.yaml` exists. |
| `audit` exit 2 | No `.sdlc/` here — run `/sdlc` init first. |
