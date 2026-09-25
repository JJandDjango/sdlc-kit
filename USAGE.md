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
Give it a raw request ("add CSV export"). 🟢 Intake first checks for a
ratified seat term (§8); with none, it stops before authoring and names
the file to author and the command that drafts it (kit 0.14.0). The
agent authors `specs/<task-id>/contract.yaml` — intent, scope,
non-goals, decomposition with a done-meaning and 1–3 acceptance-sketch
criteria per unit, dependencies, entities, provenance — then loops

```bash
python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
```

until green, and refuses the handoff to spec/implementation while red.
A blocked dependency parks the contract as a valid `draft`; `ready` is
what gates entry into development. 🟢 Intake also takes a human answer
per unit and records it under `confirmed_by` before the contract lands
(kit 0.12.0).

### What `ready` requires — two declarations 🟢

> 🟢 **Shipped** (kit 0.14.0, [ADR 0030](decisions/0030-a-doors-input-is-a-declaration.md),
> contract `specs/g0-declaration/`, schema 1.4.0).

🟢 At the `ready` profile, the input a door reads is required, so a green
G0 means every condition checked something. A contract carries
`entities:`, the glossary terms it operates on (§5). An empty list is valid
and is a statement: `entities: []` says the contract operates on no
glossary term. A contract with no field fails `TC017`. `/sdlc intake`
always writes the field, and writes `[]` only on the PO seat's confirmed
answer; `taskcontract new` names the field in a comment and sets no value.

🟢 Inside a specs tree, a ratified `intake-seat` (§8) must exist before any
contract reaches `ready`. With the term absent or at draft, every contract
fails `TC018`, and the diagnostic names the file to author:
`specs/vocabulary/intake-seat.yaml` (`/sdlc vocab add intake-seat` drafts
it; ratifying it is yours). Intake checks this first and stops before
authoring. Greenfield `/sdlc init` asks who holds the seats and seeds the
term ratified; brownfield `/sdlc init` ends its report with a note naming
the same command while the term is not ratified. A repo with one human
ratifies a one-value roster. The `draft` profile is unchanged: a parked
contract may carry neither.

🟢 **Adopting on an existing repo needs no re-intake.** The session hook
protects only a contract that validates `ready`, so a contract the new
doors fail is open to the edits that repair it. After the upgrade, a
`ready` contract with no `entities:` fails `TC017`, and in a repo with no
ratified roster it fails `TC018` too. Add the field. Ratify
`intake-seat`, and each contract fails `TC016` until its units carry
`confirmed_by`; stamp the answers. A contract locks again only when it
passes both doors, so adding `entities:` locks it on its own only where
the roster is already ratified and its units already carry answers.
Install the kit by pinned tag (§7, "Kit → your repo"), so an upgrade is a
choice, never a surprise.

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

Contracts declare `entities:`, the terms the task touches. G0
resolves each ref against **ratified** terms only: a missing or draft
term surfaces as an unresolved dependency naming the term — fork a
small vocabulary task; the work itself never fails for vocabulary.
Ratification stays deliberately human: flip `status: draft →
ratified` in the term file; the PR merge is the approval record.
Deprecation sets `sunset:`; the join warns inside the notice window
and errors past it.

🟢 From kit 0.14.0 ([ADR 0030](decisions/0030-a-doors-input-is-a-declaration.md))
the declaration is required at the `ready` profile; `entities: []`
states that the contract touches no term, and the `draft` profile still
accepts a contract without the field. See §4, "What `ready` requires".

Greenfield init seeds 5–15 terms through the interview (born
ratified), then asks who holds the seats and seeds `intake-seat` the
same way; brownfield repos start with `vocab extract`, ratify the
keepers, and ratify `intake-seat` (§8).

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
actually starts. 🟢 One step comes before it there: init's report names
the seat roster the repo needs, and intake stops until `intake-seat` is
ratified (kit 0.14.0).

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
uv run --no-project --with "sdlc-taskcontract @ git+https://github.com/JJandDjango/sdlc-kit.git@v0.15.0" python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
```

---

## 8. Intake with more than one seat 🟢

> 🟢 **Shipped** (kit 0.12.0, [ADR 0025](decisions/0025-intake-seats.md)):
> the seat term, `confirmed_by`, TC016, and intake's confirm-and-write step.

Intake takes a human answer for every unit before a contract lands.
When the humans are two teams (a PO team that owns the request, an
engineer team that owns the decomposition), the kit gives each a
**seat**, records which seats answered for each unit, and checks that
record at the door. 🟢 Every repo needs a roster (kit 0.14.0,
[ADR 0030](decisions/0030-a-doors-input-is-a-declaration.md)): a repo
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

---

## 9. Following the work 🟢

> 🟢 **Shipped** (kit 0.15.0, [ADR 0031](decisions/0031-the-work-is-one-derived-tree.md),
> contracts `specs/tree-view/` and `specs/pane-view/`).
>
> 🔴 **Ratified, not shipped:** the five subsections marked 🔴 at the end of
> this section (contract `specs/project-tree/`, kit 0.16.0). Their marks flip
> green at the release; until then, each 🟢 paragraph they change holds for
> 0.15.0.

🟢 `taskcontract tree` prints the repo's work as one tree, computed from
the kit's files at every run and never stored. It reads the contracts,
`.sdlc/config.yaml`, the findings, the progress files, git, and two name
lists the kit ships (`taskcontract/data/gates.yaml` and
`taskcontract/data/tasks.yaml`). It reads no document: nothing under
`docs/`, and no feature document, REQUEST, STATE or plan. It writes no
file; `taskcontract progress` is the only writer, and only under
`.sdlc/progress/`.

### What the tree holds 🟢

🟢 The gates come first, at the repository level: each gate in
`active_gates`, and any other gate a finding names, marked `inactive`.
Each finding under `.sdlc/findings/` prints once, under the gate its
`gate:` field names; `gate: none` prints under a `none` item, and the
form's `TEMPLATE.yaml` prints nothing. A finding is read only from a
`.yaml` file, so a `.yml` file there never shows. Then each contract,
with its verdict at every gate in `active_gates`, its units, each unit's
seven tasks, and its checks, one per `acceptance_sketch` line.

🟢 Every item has an id, a path you pass to the commands below:

| Item | Id |
|---|---|
| a gate, a finding, the no-gate item | `gates/G0`, `gates/G0/<finding>`, `gates/none` |
| a contract, its verdict at a gate | `<contract>`, `<contract>/G0` |
| a unit | `<contract>/<unit>` |
| a task | `<contract>/<unit>/<task>`, with the keys in "The seven tasks" |
| a check | `<contract>/<unit>/<check>`: the ids in the sketch's trailing parentheses, joined with `+` (`SC5.1+SC5.2`), else `sketch-<n>`, counted from 1 |

🟢 Each item's summary is its source's own text, with its ends stripped
and each line break read as one space: a contract's `intent`, a unit's
`done_means`, a check's sketch line, a finding's `statement`, and a
gate's or a task's one-line name from the kit's lists. Links come only
from source fields: a unit's `depends_on`, each entry once in the order it
first appears, and a finding's `gate`. A feature document shows only as a
file reference, found by the contract's id at `docs/features/<id>.md`.

🟢 Each item prints on one line, indented two spaces per level: its full
id, then its status in brackets (a finding shows `[kind: <kind>]` in its
place), its marks (`inactive` on a gate that is not active, `current` on
the current task), its evidence, its links (`depends_on: <contract>/<unit>`,
`gate: <value>`), a contract's `doc: docs/features/<id>.md`, and last
` | ` and its summary. Each part after the status prints only when the
item has it, and a line break inside a part, such as in a multi-line
`--reason`, reads as one space, so an item keeps one line.

### Six statuses 🟢

🟢 Every item but a finding shows one of six statuses: `to do`, `doing`,
`done`, `failed`, `blocked`, `waiting on a seat`. A finding records no
status, so it shows its `kind`.

- 🟢 A task reads the state `taskcontract progress` recorded for it; an
  approval that holds the current task reads `waiting on a seat`.
- 🟢 A check reads its last run, judged by what that run expected: never
  run, `to do`; red under `--expect red`, `doing`; green under the
  default, `--expect green`, `done`; a run that missed its expectation,
  `failed`. A test that passes before its code exists shows `failed`.
- 🟢 A contract's `G0` verdict comes from the validator: `done` at
  ready-green, `blocked` when draft-green with `TC003`, `to do` when
  draft-green otherwise, `failed` when draft-red. An active gate the kit
  cannot compute yet reads `to do`.
- 🟢 A parent takes the first of `failed`, `waiting on a seat`, `blocked`
  and `doing` that any child has. It reads `done` only when every child
  reads `done`, and `to do` when nothing under it has started.

🟢 An item names its evidence on its line. A done check names the run
that proved it, `via <command> at <commit>`. A done task names the commit
its own done record was written at, `at <commit>`, and a done approval
names its seat too, `by <seat> at <commit>`. A unit or contract that
reads `done` after a close with `progress done` names that close, `at
<commit>`; one that does not read `done`, such as a closed contract with
another active gate ("History, backfilled", below), names none. A blocked
task names its reason, `because <reason>`. A `G0` verdict, whatever it reads, names
the validator run behind it: `via python -m taskcontract validate
specs/<contract>/contract.yaml --profile ready at <commit>`.

🟢 Evidence ends in `dirty` in two cases. A run, a task's record or a
close reads `dirty` when a tracked file differed from `HEAD` as it was
recorded; untracked files do not count, so the untracked REQUESTs in a
repo's root never mark it. A `G0` verdict reads `dirty` when its own
contract file differs from `HEAD`: changed, staged or not, or not yet
committed. Outside a git repository the commit reads `no commit`, and
nothing reads `dirty`.

### The three modes 🟢

- 🟢 **`taskcontract tree`** prints the whole tree and exits 0. Each
  source it cannot read prints one line on stderr, and the rest of the
  tree still prints.
- 🟢 **`taskcontract tree <id>`** prints one item, for an agent that needs
  one fact without reading a document: its line as the whole tree prints
  it, cut after the evidence, then one labeled line per field it has:
  `summary:` whole, one line per link kind with its targets joined by
  `, `, `doc:`, `file:` and `page:`. A file reference is a repo path with
  the line the item starts at: line 1 for a contract, its verdicts and a
  finding, and the line its entry starts for a unit or a check; a
  contract's feature doc shows on its `doc:` line at line 1. A gate, a
  verdict and a task name the kit page that defines the gate or the task,
  a path in the kit's repository. So an item never takes more than seven
  lines, whatever its fields hold. Every id the tree prints works here,
  matched whole. An id that names two items (a check whose sketch names a
  task key, such as `(commit)`, or a unit named like an active gate)
  prints both, in the tree's order, with an empty line between them. An
  unknown id exits 2 with `no node '{id}' - print the tree to list every
  node id`, and an id with `--follow` exits 2 with `taskcontract tree:
  --follow takes no id - give the id or --follow, not both`.
- 🟢 **`taskcontract tree --follow`** keeps a terminal pane on the current
  task: every item on the path from the root to it shows, and the other
  items at each level fold to one line with their counts by status. For
  five contracts of seven units each, with the current task in the last
  unit, that is at most 15 lines. It renders again within two seconds of
  a change to a source file (a vocabulary change can take longer, below),
  and never while nothing changes. Ctrl-C exits 0. It needs no `curses`,
  so it runs on Windows: it reads
  modification times once a second and redraws with ANSI escape codes.

🟢 One check of this kit's own tree, queried when its first green run
was recorded at `c1380d5` (a later run names its own commit):

```
$ taskcontract tree tree-view/t6-query-face/SC6.1
tree-view/t6-query-face/SC6.1 [done] via python -m pytest tests/test_tree_query.py -q --tb=no -p no:cacheprovider -k sc6_1 at c1380d5
summary: verify an item id prints its source field, status, links and each file reference in at most 20 lines (SC6.1)
file: specs/tree-view/contract.yaml:186
```

🟢 The pane lists its sources once a second: every file under `specs/`,
`.sdlc/findings/`, `.sdlc/progress/` and `docs/features/`, plus
`.sdlc/config.yaml` and the kit's two lists. It redraws only when a file
was added, removed or changed, so a terminal resize alone does not
redraw, and a line cut at the old width wraps until the next change. It
keeps each contract's `G0` reading in memory until that contract's file
changes. A change under `specs/vocabulary/` drops every reading, so that
render runs the validator on every contract and can take longer than two
seconds on a repo with many contracts.

🟢 The current task is derived, never stored: the task marked `doing`
most recently; with none `doing`, the first `to do` task in the contract
that changed most recently; with no progress at all, none, and the pane
shows the root folded. Marking the current task done moves it on.

### The seven tasks 🟢

🟢 Every unit follows one task list, shown and never enforced: nothing
stops a unit that skips a task. Writing the tests and proving red belong
to the spec channel (G2.5), green to the developer (G3), and each
approval is a seat's answer. With `U` for the unit's id
(`<contract>/<unit>`), one command records each task:

| # | Task | Key | Record it with |
|---|---|---|---|
| 1 | Approve the test list | `approve-tests` | `taskcontract progress done U/approve-tests --by <seat>` |
| 2 | Write the tests | `write-tests` | `taskcontract progress done U/write-tests` |
| 3 | Prove red | `prove-red` | `taskcontract progress done U/prove-red` |
| 4 | Green | `green` | `taskcontract progress done U/green` |
| 5 | Approve the commit | `approve-commit` | `taskcontract progress done U/approve-commit --by <seat>` |
| 6 | Commit | `commit` | `taskcontract progress done U/commit` |
| 7 | Two-Key PASS | `two-key` | `taskcontract progress done U/two-key` |

🟢 The checks carry their own runs. During prove red, run each check's
test through the kit with the red it expects:

```bash
taskcontract progress run U/<check> --expect red -- <test command>
```

🟢 During green, run the same without `--expect`, which means `--expect
green`, so a check reads `done` only on a green that was meant to be
green.

### Recording progress 🟢

🟢 `taskcontract progress` writes `.sdlc/progress/<contract>.yaml`, one
local file per contract. The folder holds a `.gitignore` of `*`, so none
of it is committed; the file is disposable, and no gate, check, audit or
hook reads it. Every record carries its time and the `HEAD` commit, and
inside a git repository a `dirty` mark.

| Command | What it records |
|---|---|
| `taskcontract progress start <id>` | the task `doing` |
| `taskcontract progress done <id>` | the task `done`; on a unit or a contract, a close. An approval (`approve-tests` or `approve-commit`) needs `--by <seat>`, and no other item takes it |
| `taskcontract progress block <id> --reason <text>` | the task `blocked`, with its reason, which it needs |
| `taskcontract progress run <check> [--expect red\|green] -- <command>` | runs the command, then records red or green, the expectation (`green` unless given), the command, the commit, a `dirty` mark and the time; exits 0 when the result met the expectation, 1 when it missed |

🟢 A call the kit refuses writes nothing, exits 2 and prints one line on
stderr, and `run` refuses before it starts the command. `{action}` is
`start` or `block`:

```
no node '{id}' - print the tree to list every node id
taskcontract progress: '{id}' is a {kind}, not a check - run takes a check id
taskcontract progress: '{id}' is a {kind}, not a task - {action} takes a task id
taskcontract progress: '{id}' is a {kind}, not a task, unit or contract - done takes a task, unit or contract id
taskcontract progress: '{id}' is an approval - done needs --by <seat>
taskcontract progress: '{id}' is not an approval - only approve-tests and approve-commit take --by
taskcontract progress: block needs --reason <text> - say why '{id}' is blocked
taskcontract progress: unreadable progress: {path} ({reason})
taskcontract progress: cannot start {command} ({reason})
```

🟢 A malformed progress file prints one line naming it, and its contract
reads as having no progress. No writer touches it: a call on that
contract that passes its other checks is refused with the `unreadable
progress` line above, so fix or remove the file first.

🟢 **History, backfilled.** `taskcontract progress done` on a unit or a
contract closes every task and check under it; a close never covers a
verdict, which the validator reads. A closed unit reads `done`. A closed
contract reads `done` when its `G0` verdict does and no other gate is
active, since a verdict at any other gate reads `to do`. A contract
finished before the tree existed reads `to do` until it is closed, so one
command per contract backfills its history; a fresh clone, which starts
with no progress file, rebuilds it the same way.

### The notify command 🟢

🟢 When the current task is `approve-tests` or `approve-commit`, the
pane's first line reads `waiting on a seat: {approval} for {unit}`, and
the command set in `.sdlc/config.yaml` runs:

```yaml
tree:
  notify: <command>
```

🟢 It runs through the shell at the repo root, once each time the current
task arrives at an approval, never on a redraw, with the item's id in
`SDLC_NODE` and its own output discarded. A pane that starts on an
approval has arrived there, so it runs the command at once. The pane
never waits on the command. One that ends nonzero prints `notify failed,
exit {code}: {command}` on stderr, whole, never cut to the pane's width,
and when the shell itself cannot start, the same line reads code 127. The
pane keeps running either way, and with no `notify` set it runs the
same. Ctrl-C ends the pane without stopping the commands it started,
though the same Ctrl-C can reach them, since they run in the pane's
terminal. The key is optional, and
the config template does not carry it. The command is the kit's edge: a
terminal multiplexer's plugin (herdr's, for one) wraps it outside the
kit.

### The pane's lines 🟢

🟢 The pane prints one **where-am-I line**: the current task's contract
file, then its contract, unit and task, joined by ` > `, the unit and the
task by the last segment of their ids:

```
specs/tree-view/contract.yaml > tree-view > t6-query-face > approve-tests
```

🟢 It stands directly under the waiting line (`waiting on a seat: ...`,
above) when the current task is an approval, and first otherwise; the
waiting line stays first, word for word, since a multiplexer's plugin may
read it. With no current task the pane prints none: it reads `no current
task`, then `<n> items: <counts>` for the top level.

🟢 Every pane line wider than the pane is cut to the pane's width and ends
in `...`. The cut counts characters, not display columns, so a line that
holds wide characters can still wrap.

🟢 Each item line under another item opens on the **last segment of its
id** (`t6-query-face`, `approve-tests`), since the lines above give the
rest; a top-level item's line opens on its full id. Everything else keeps
full ids: `taskcontract tree` with or without an id, the waiting line,
every link and `SDLC_NODE`.

🟢 Two optional keys under `tree: pane:` in `.sdlc/config.yaml` choose
what the lines hold. The pane reads them at each render, so a change
shows within two seconds; the config template does not carry them.

```yaml
tree:
  pane:
    parts: [status, marks]
    fold: names
```

- 🟢 **`parts:`** lists what each item line shows after its id, from
  `status`, `marks`, `evidence`, `links`, `doc` and `summary`. The id
  always shows, and listing `id` changes nothing. The parts print in that
  fixed order whatever order the list gives, and `[]` shows the id alone.
  Unset, each item line shows every part it has. The key leaves the
  waiting line, the where-am-I line, the fold lines and `taskcontract
  tree` unchanged.
- 🟢 **`fold: names`** makes each fold line name the items it folds in
  place of the counts: `<n> more: `, then each item as `<id> [<status>]`,
  the id as its own line would show it, joined by `, ` in the tree's
  order. With no current task, the `<n> items:` line names the top-level
  items the same way. `fold: counts`, or no `fold:`, keeps the counts by
  status.

🟢 A bad key never stops the pane. A `parts:` that is not a list, or that
names anything but the seven parts, is ignored as a whole, so each item
line shows every part it has. A `fold:` other than `names` or `counts`
keeps the counts. Either prints one line on stderr at each render, as an
unreadable source does. `{value}` is the first entry that names no part,
or the whole value when it is not a list, and for `fold:` the value, each
as YAML reads it, so `fold: yes` prints `True`:

```
taskcontract tree: pane parts ignored: {value} - give a list from id, status, marks, evidence, links, doc, summary
taskcontract tree: pane fold ignored: {value} - give names or counts
```

🟢 A `tree:` or `pane:` that is not a mapping reads as unset, as it does
for `notify:`.

🟢 A pane at t6's first approval, with the keys above, 80 columns wide:

```
waiting on a seat: approve-tests for tree-view/t6-query-face
specs/tree-view/contract.yaml > tree-view > t6-query-face > approve-tests
15 more: gates/G0 [to do], controlled-language [to do], distribution-reconcil...
tree-view [waiting on a seat]
  10 more: G0 [done], t0-usage-pass-zero [done], t1-tree-shape [done], t2-sum...
  t6-query-face [waiting on a seat]
    9 more: write-tests [to do], prove-red [to do], green [to do], approve-co...
    approve-tests [waiting on a seat] current
```

### Gates and their conditions 🔴

🔴 Each gate opens into its **conditions**, the named parts its kit page
lists, in the page's order. `taskcontract/data/gates.yaml` lists every
gate's conditions, 57 in all, each an id and a plain name: the page's
heading without its date note and without a last word "check" or "join"
(`G0.1 Definition-of-ready`, `G0.2 Vocabulary coverage`, `G0.3 Unit
confirmation`).

🔴 Each feature shows its gates first: each gate in `active_gates`, then
the first gate after them in the kit's order, marked `inactive`, the gate
its work reaches next. With `active_gates: [G0]`, every contract shows `G0`,
then `G1` marked `inactive`. An inactive gate and its conditions read `to
do`, and never count toward the contract's status, so a closed contract
still reads `done`.

🔴 Each of G0's conditions takes its status from the rules it owns, read
as the `G0` verdict is read: `failed` when one of its rules fails the
draft profile, `done` when none fails the ready profile, `blocked` when
`TC003` fails it, and `to do` otherwise.

| Condition | Its rules |
|---|---|
| G0.1 Definition-of-ready | TC000 to TC009, TC013 to TC015 |
| G0.2 Vocabulary coverage | TC010 to TC012, TC017, W001 |
| G0.3 Unit confirmation | TC016, TC018 |

🔴 Every code the validator emits belongs to exactly one condition. A
warning (`W001`) never changes a status and never shows. The `G0` verdict
still reads from the validator, as above, so it agrees with its
conditions: `failed` when one reads `failed`, else `blocked` when one reads
`blocked`, `done` when all three read `done`, and `to do` otherwise. A
contract the tree cannot read as a mapping, one it names on stderr as an
`unreadable contract`, reads `failed` at G0.1 and `to do` at G0.2 and
G0.3, since their joins never ran. The conditions of every other gate read
`to do`: the kit computes none of them yet.

🔴 A condition that is not `done` lists what its rules report, one line
under it per diagnostic: `- `, then the validator's message without its
code. A `failed` condition lists the draft profile's messages, any other
the ready profile's. A contract at draft-green with one draft term:

```
apply-discount [to do] | Checkout applies one discount code per order.
  apply-discount/G0 [to do] via python -m taskcontract validate specs/apply-discount/contract.yaml --profile ready at 1a2b3c4 | Planning / Intake
    apply-discount/G0/G0.1 [done] | Definition-of-ready
    apply-discount/G0/G0.2 [to do] | Vocabulary coverage
      - entity 'discount-code' is not ratified (status: draft) - draft does not resolve; ratify the term or fork the vocabulary task
    apply-discount/G0/G0.3 [done] | Unit confirmation
  apply-discount/G1 [to do] inactive | Requirements / Spec
    apply-discount/G1/G1.1 [to do] | Spec/schema linting
    apply-discount/G1/G1.2 [to do] | Model checking
    apply-discount/G1/G1.3 [to do] | Criteria completeness + ambiguity review
```

🔴 At the repository level each gate opens into its conditions too, and a
finding whose `gate:` names a condition stands once under that condition,
never under a feature. A finding that names the gate itself, or a
condition its gate does not list, stands under the gate, after its
conditions.

| Item | Id |
|---|---|
| a condition | `gates/<gate>/<condition>`, `<contract>/<gate>/<condition>` |
| a finding that names a condition | `gates/<gate>/<condition>/<finding>` |

🔴 `taskcontract tree <id>` prints a condition as it prints a gate: its
line, `summary:` and the gate's `page:`. Its diagnostics print with the
whole tree.

### Plain names and titles 🔴

🔴 Each item line opens on its id and its **plain name**, the words that
say what it is, before the parts `tree: pane: parts:` selects: `G0.2
Vocabulary coverage`, never `G0.2` alone. A gate's, a condition's and a
task's plain names come from the kit's lists. A feature's is its
contract's `title`, an optional one-line field that intake copies from
the feature document's title line; the tree never reads the document's
heading. A contract without a `title` shows `(no title)`. The contract
schema moves from 1.4.0 to 1.5.0 for the field.

🔴 The pane's cursor line and `taskcontract tree <id>` show each item's
plain name and document reference from its source: a feature's title and
its feature document; a unit's `done_means` and a check's sketch line,
each with its contract file and line; a gate's, a condition's and a
task's name and kit page.

### Drift from the feature document 🔴

🔴 The tree opens each feature's document at `docs/features/<id>.md` for
its revision table only, and the feature's line names what it finds:

- 🔴 `stale: document rN, contract from rM` when the table holds a row
  `rN` after the `rM` its contract derives from. Intake's `Ready:` rows
  and `Measured:` rows never count.
- 🔴 `no feature document` when the file is missing.
- 🔴 `no "Ready:" row` when the table holds no `Ready:` row the tree can
  read.

🔴 The `rM` is the revision the newest `Ready:` row names. Intake writes
that row's changes cell in a fixed shape, `rN: Ready: ... derived from rM
...`; a row the tree cannot read is skipped. The contract records nothing
new for this.

### Blocked and waiting, named 🔴

🔴 Each unit and each task shows `done`, `doing` or `to do` from the
progress record, and a closed unit or contract reads `done`. A `blocked`
item names its `--reason`, and an approval that waits on a seat names that
seat, each on the item's own line.

### The interactive pane 🔴

🔴 With the `pane` extra, `taskcontract tree --follow` runs an interactive
outline of the whole tree. The extra installs Textual, a terminal-UI
library; every other command still needs only jsonschema and PyYAML.

```bash
pip install 'sdlc-taskcontract[pane]'
```

🔴 The outline opens with each feature open down to its units, whether or
not a task is in flight, and the current task carries its mark and stays
in view. A line under the outline shows the plain name and document
reference of the item at the cursor. Up and Down move the cursor, Right
opens the item at the cursor and Left closes it; a click opens or closes
the item it lands on, and the wheel scrolls. A closed item's line counts
what it holds, or names it under `fold: names`.

🔴 The waiting line stays the pane's first line, word for word. A redraw
within two seconds of a source change keeps the cursor and every open and
closed item as they were. The notify command runs as it does today, once
per arrival at an approval, and Ctrl-C ends the pane with exit 0. Each
line the pane prints on stderr today shows word for word inside the pane,
under the outline.

🔴 Without the extra, `--follow` prints one line on stderr and exits 2:

```
taskcontract tree: --follow needs the pane extra - pip install 'sdlc-taskcontract[pane]'
```

---

## 10. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "`/sdlc` isn't listed" | Reload the Claude Code session after installing. |
| "It didn't overwrite my file" | By design (no-clobber). Edit the file in place, or delete it and re-run. |
| `TC003 dependency unresolved` | The contract is a parked draft — resolve or re-scope the dependency; `ready` requires all resolved. 🟢 `/sdlc audit` reads it `CONTRACT-PARKED` at exit 0, and a `still to declare:` suffix names what it also owes: `TC017`, `TC018` or both (rows below). |
| `TC005 unknown field` | Contracts reject stray keys (`additionalProperties: false`) — a typo or scope smuggling; both fail loudly. |
| `TC016 unit not confirmed` (🟢 0.12.0) | The seat term is ratified here and a unit lacks `confirmed_by`, or names a seat the term does not list. Run intake's confirm step, or fix the value (§8). On a parked contract `/sdlc audit` does not park it: `TC003` beside `TC016` reads `CONTRACT-INVALID` until the units carry answers. |
| `TC017 contract declares no entities` (🟢 0.14.0) | The field is required at `ready`. List the glossary terms the contract operates on, or write `entities: []` to state that it operates on none: an edit, not a re-intake (§4, "What `ready` requires"). |
| `TC018 no seat roster` or `seat roster not ratified` (🟢 0.14.0) | The repo holds no ratified `intake-seat`, so no contract under `specs/` reaches `ready`. Author `specs/vocabulary/intake-seat.yaml` (`/sdlc vocab add intake-seat` drafts it) and ratify it; one remedy clears every contract, and ratifying arms `TC016` (§8). |
| CI job green with no contracts | Expected — the validate step is guarded until a `specs/*/contract.yaml` exists. |
| `audit` exit 2 | No `.sdlc/` here — run `/sdlc` init first. |
