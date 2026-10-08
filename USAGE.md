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

> 🟢 **Shipped** (kit 0.19.0, [ADR 0029](decisions/0029-feature-document-format-and-done.md)
> as ADRs 0033 to 0037 amend it, contract `specs/document-split/`). Kit
> 0.18.0's interview wrote one combined document, both halves in one file
> at `docs/features/<id>.md`: this page at tag `v0.18.0` is its guide.

Intake consumes a feature document (§8): a pair, the requirements
document and the design document of one feature. This skill writes each
in its own run, one question at a time, and has one seat sign each. Run
it in the target repo with the feature's id:

```
/sdlc:product-specification-interview csv-export          the requirements run: starts or resumes
/sdlc:product-specification-interview csv-export design   the design run: starts or resumes
```

🟢 **The two documents.** A requirements run writes the requirements
document at `docs/features/<id>.md`, the path a combined document held,
and its state file beside it, `docs/features/<id>.state.yaml`. A design
run writes the design document at `docs/features/<id>.design.md`, and its
state file at `docs/features/<id>.design.state.yaml`. An id holds no dot,
so `<id>.design.md` is never another feature's document. Each run writes
r1 at the end of its opening and each section as its step closes, so the
tree shows the feature before intake from the requirements document's
first revision (§9, "Features before intake").

🟢 **The requirements document** holds the request half, and the PO seat
signs it. It opens on its revision table, its title line `# <id> -
<title>`, and a status line. Drawn on a feature `x`, PO seat ann:

```
| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-07 | ann | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: ann |

# x - The outcome, in a few words

`repo` · seat: PO ann · contract: `x`, draft · PR: none · merge SHA: none
```

🟢 Then come the request half's sections in order, Statement to
Acceptance criteria, each with its heading and its tag as kit 0.18.0
writes them: owner and kind, such as `[PO seat · authored]`. The four
bug-fix sections appear only in a bug fix's document, with its incident
reference and regression scenario. Decisions and open questions and
Notes follow, each tagged `[PO seat · authored]`, then the Appendix with
its Gherkin and Terms blocks. The document holds no Proposed solution, no
Risks and cost, no Traceability, no Contract block and no `---` line. A
section with nothing to say reads "(none)", and one the interview has not
asked yet reads "(not yet asked)". The Gherkin carries no stamp until its
step writes it: it reads "(none: the Gherkin step writes one scenario per
check)" under `[PO seat · derived]`.

🟢 **The design document** holds the solution half, and one engineer seat
signs it. It names the requirements revision it stands against. Drawn
for the same feature, engineer seat raj:

```
| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-08 | raj | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r3. Engineer seat: raj |

# x - The outcome, in a few words

`repo` · seat: engineer raj · requirements: `docs/features/x.md` · contract: `x`, draft · PR: none · merge SHA: none
```

🟢 Then come Proposed solution with its seven sections (Scope, Out of
scope, Interfaces, Sources, Constraints, Units, Order), Risks and cost,
Consult cases, Decisions and open questions, Traceability (Links out,
Record), Notes, and the Appendix with its Contract block. Each authored
section is tagged `[Engineer seat · authored]`; Record and Contract keep
`[Intake · derived]`. The document holds no section tagged for the PO
seat. Before intake, the Contract block reads "(none: intake writes
`specs/<id>/contract.yaml`)", with no stamp. The Record reads "(none:
intake writes the record)" and keeps that line: kit 0.19.0 has no step
that writes the Record.

🟢 **The requirements run.** It asks for a PO seat and for no engineer
seat. It asks the request half's sections in order, then the Terms and
the Gherkin, one question at a time. It writes its state file after
every step, and a later run resumes at the step its `next` names.
Material you hand it at the opening is confirmed section by section, and
an answer that conflicts with it is asked, never settled silently. No
step asks Decisions and open questions or Notes: each holds the material
confirmed at the opening, else "(none)". At Non-goals it asks "a thing we
will not build, or a place we will not touch?": a thing stands as a
non-goal, and a place waits in the state file for the design run. A
sixth success criterion draws "Six criteria is two features. Which
criteria form the second document?". A section changed by hand since the
interview last wrote it is shown beside the answer, and you say which
stands.

🟢 **The Gherkin step.** Once the checks stand, the requirements run
proposes one scenario per check, joined to it by its id, and the PO seat
accepts, changes or drops each. The block is tagged `[PO seat · derived
from rN]`:

```
Scenario: SC1.1 A written document lands at its path
  Given a run for the id `x`, with no file at `docs/features/x.md`
  When the interview writes the document
  Then `docs/features/x.md` opens on its revision table, and its title line reads `# x - The outcome, in a few words`
```

🟢 A scenario whose Then needs a fact its check lacks is never offered:
the check is marked thin instead. A scenario the PO seat drops marks its
check thin too. Ready check 3 reads a thin check as an OPEN.

🟢 Each text row the requirements run writes moves the block's stamp to
that row, once every check changed since the last stamp has a confirmed
scenario again. A row written by hand moves no stamp, so the checks
before signing report the block stale.

🟢 The requirements run then runs the checks before the PO seat signs,
takes the signature, and ends by naming the design run as the next
command:

```
/sdlc:product-specification-interview <id> design
```

🟢 **The design run.** It reads the requirements document before it
writes anything, and stops with nothing written on:

```
No requirements document for x. Run the requirements interview first.
The requirements document is unsigned at r3. The PO seat signs before the design starts.
```

🟢 The first when no file stands at the path; the second when no
`Signed: request half` row signs the newest text revision, here r3. A
design run on a combined document stops too, with nothing written:
`docs/features/x.md is a combined document. Split it by hand, then run
the design interview.`

🟢 Then the design run asks for an engineer seat and for no PO seat. It
asks no origin and no title: it reads both from the requirements
document, with the check ids and the new terms. It reads the
requirements document and the requirements run's state file, and writes
neither. It asks the solution half's sections in order, then the four
cases, and resumes as a requirements run does. At Out of scope it shows
the engineer seat each place the PO seat refused at Non-goals. A thing
the engineer seat will not build goes under the design's Decisions and
open questions as `OPEN: a non-goal for the PO seat: {thing}`, and
nothing goes into the requirements document: the PO seat adds it through
a requirements run, and the engineer seat then closes the mark.

🟢 **Consult cases.** After Risks and cost the design run asks the
engineer seat the four cases, one at a time: the conditions under which
the seat asks another engineer before the PR. Each answer is yes or no,
and a yes takes two more answers, who was asked and what was decided:

```
## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | no | | |
| 2. More than one solution | yes | lee | the retry lives in the client, not the gateway |
| 3. A solution unconventional to the codebase | no | | |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | no | | |
```

🟢 **The revision a design names.** A design names one requirements
revision: the `requirements r{m}` of its newest text row that names one.
r1 names it first. Every design run, at any step, reads the requirements
document's newest text revision. On a newer one it shows the revisions
between and asks:

```
The design names requirements r3; the requirements stand at r5.
  r4: A non-goal added: no export to CSV
  r5: SC2.1 reworded
Confirm the design against r4 and r5?
```

🟢 On yes the design takes a text row, and a signed design is asked for
its signature again:

```
| 2026-10-10 | raj | r5: Confirmed against requirements r5 |
| 2026-10-10 | raj | r6: Signed: solution half. The engineer seat signs r5 |
```

🟢 On no, nothing is written and the design is stale: it names a
requirements revision older than the requirements document's newest text
revision. The checks before the engineer seat signs report it, and intake
stops on it, with one message:

```
The design names requirements r3; the requirements stand at r5. Stale.
```

🟢 **The checks before signing.** Each seat's checks run on that seat's
own document and state file. Before the PO seat signs, the interview
runs the document's new terms as drafts through the vocabulary check and
`CL003`, and a draft contract of the statement, the non-goals and the
checks through the language check. It also reads each entry of Existing
behavior touched against the file or step the entry names. Before the
engineer seat signs, it runs each unit's `done_means` through the
language check, beside a copy of the requirements document's new terms,
and checks Scope against the release unit's paths. The runs go through
one command that reads a state file, never a document, and writes
nothing:

```
$ python -m taskcontract lang-check --draft docs/features/x.state.yaml
specs/vocabulary/dictionary.yaml: $.words[41].word: CL003 'check' collides with a glossary term name, alias, or slug - the glossary is the open class; keep the layers disjoint
docs/features/x.state.yaml: answers.statement: CL008 sentence of 41 words exceeds the descriptive cap of 25
docs/features/x.state.yaml: answers.checks[SC2.1]: CL012 acceptance sketch must open with an approved verb (got 'each')
docs/features/x.state.yaml: answers.terms[Seat]: CL014 new term 'seat' matches ratified term 'intake-seat' - map it to that term, or rename it
draft: 14 new terms, 1 amended; 9 non-goals; 14 checks; 0 units; 4 findings (CL003 1, CL008 1, CL012 1, CL014 1)

$ python -m taskcontract lang-check --draft docs/features/x.design.state.yaml
docs/features/x.design.state.yaml: answers.units[u2]: CL008 sentence of 31 words exceeds the descriptive cap of 25
draft: 2 new terms, 0 amended; 0 non-goals; 0 checks; 3 units; 1 findings (CL008 1)
```

🟢 `CL014` reports a new term that matches a ratified one; an amended
term replaces its ratified definition among the drafts and is never a
`CL014`. On the design's state file the command reports the copied
terms' findings again. The command exits 1 when any finding is an error,
as `lang-check` does. A state file missing or not YAML reads
`docs/features/x.state.yaml: $: CL000 unreadable draft: {reason}`, exit
1. With no repo dictionary only `CL014` runs, and the last line ends
`(no dictionary here - door at rest)`. A key the state file lacks reads
as empty. Without `--draft`, `lang-check` reads `specs/` as before.

🟢 Then the interview reads that document's ready checks, 1 to 8 for the
requirements document and 11 to 15 for the design document, and marks
each gap inline with its message:

```
- SC2.1: verify ...
  OPEN: Ready check 3: SC2.1 is thin: its Then needs the count it reports.
```

🟢 Ready check 15 asks whether each of the four cases has an answer, and
whether each yes names who was asked and what was decided. Its gaps,
each marked under Consult cases:

```
Ready check 15: case 2 has no answer. Marked OPEN.
Ready check 15: case 2 reads yes and names no one asked. Marked OPEN.
Ready check 15: case 2 reads yes and names no decision. Marked OPEN.
```

🟢 Each run of the checks then lands as one `Measured:` row in that
seat's document: the command's findings, the count of OPEN marks under
that document's ready checks, and for the design document the Scope
result. The interview reports each gap as `Ready check {n}: {gap}. Marked
OPEN.`, and a derived block stamped below the newest revision as `{block}
is stamped r{n}; the newest revision is r{m}. Stale.` The checks advise
and never block: the seat's word to sign or to write stands, whatever
the count.

🟢 **The signatures.** Each seat signs in its own document, with a row
that opens `rN: Signed: request half` or `rN: Signed: solution half`,
written right after the row it signs (ADR 0034). The tree then shows
that half `done`, by its signer at the revision signed (§9, "Revisions
and halves"). A design run changes no line of the requirements document.
The rows the interview and intake write, each numbered in its own table.
The requirements document's:

```
| 2026-10-07 | ann | r2: Measured: the checks before signing, on the request half: 4 findings (CL003 1, CL008 1, CL012 1, CL014 1); ready checks 1 to 8: 0 OPEN |
| 2026-10-07 | ann | r3: The request half finished: ... |
| 2026-10-07 | ann | r4: Signed: request half. The PO seat signs r3 |
| 2026-10-09 | intake | r5: Ready: contract `x` validates ready-green, derived from r3; the PO seat (ann) signed the request half at r3 (r4) |
```

🟢 The design document's:

```
| 2026-10-08 | raj | r2: Measured: the checks before signing, on the solution half: 1 findings (CL008 1); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-08 | raj | r3: The solution half finished: ... |
| 2026-10-08 | raj | r4: Signed: solution half. The engineer seat signs r3 |
| 2026-10-09 | intake | r5: Ready: contract `x` validates ready-green, derived from r3, against requirements r3; the engineer seat (raj) signed the solution half at r3 (r4) |
```

🟢 A write into a document after its seat signed adds a text row, and
the interview asks that seat to sign again, with a new `Signed:` row
right after it. The seat's word stands: a seat that declines keeps its
older signature, and the interview names the revision it covers. A
requirements run on a finished state reports its paths and the design
run's command, then offers the way back to a section.

🟢 **What it writes.** A run writes only its own document and its own
state file. It never writes under `specs/`, never writes a `Ready:` or
`Parked:` row, and never runs intake. A document at a run's path with no
state file of that run beside it gets "A document already exists at
{path}. Name another path." On request a run shows its own document, and
that one alone, as the Google Docs form, and writes that form nowhere. A
state file at the old `REQUEST_<slug>_*.state.yaml` path is never read: a
run for that id starts fresh.

🟢 **Intake takes the pair.** `/sdlc intake docs/features/<id>.md` takes
the requirements document's path and finds the design document beside
it. It stops, with nothing written, on a combined document and on a
missing design document:

```
docs/features/x.md is a combined document with no Ready: row. Intake reads a pair.
docs/features/x.md is a combined document through intake. Its contract stands.
No design document for x. Run the design interview first.
```

🟢 A combined document is one that holds a `## Proposed solution`
heading. The first message is for one with no `Ready:` row. The second
is for one with a `Ready:` row: it stays unchanged, and its contract
validates as before.

🟢 **Intake's refusals** are read on both documents. Intake refuses
ready while an OPEN mark stands in either document, a ready check has a
gap (1 to 8 on the requirements document, 11 to 15 on the design
document), a check of the requirements document stands in no unit or in
two of the design document's Units, or a unit delivers no check. It
names the id:

```
Check {id} is assigned to no unit.
Check {id} is assigned to units {a} and {b}.
Unit {id} delivers no check.
```

🟢 A refusal parks the pair: intake writes one row in each table,
`r{n}: Parked: {what stands}`, numbered in its own table, and no
contract. Both rows hold the same list, which names every thing that
stands, the requirements document's things first. A `Parked:` row
changes no text: like `Ready:`, `Measured:` and `Signed:` rows, it never
ages a stamp or the drift mark, never moves the newest revision, and is
never the row a `Signed:` row signs.

🟢 Intake reads the signatures only when nothing stands. It then stops
before any contract, writes no row, and reports each case that holds, in
this order:

```
The requirements document has no PO signature on r5.
The design document has no engineer signature on r5.
The design names requirements r3; the requirements stand at r5. Stale.
```

🟢 The seat signs, or confirms the design, through its own run, and
intake runs again.

🟢 On ready, intake writes one contract. It takes the title, the
statement, the non-goals, the checks and the terms from the requirements
document, and the scope, the units, the order and the tests from the
design document. It copies each unit's `done_means` word for word from
its row under Units, where `+` joins two checks that share a sketch, and
a unit of more than three checks pairs two in one sketch that names both
ids. It writes one `Ready:` row in each table, as drawn above: each
names its own seat and the revision that seat signed, and its `derived
from r{m}` names its own table's signed text revision. Intake still
stops without a ratified seat roster, confirms each unit with its seats,
and holds a contract with a `blocked` dependency at draft.

🟢 **Next step:** a requirements run ends by naming the design run, and a
design run ends by naming the command that consumes the pair:

```
/sdlc intake docs/features/<id>.md
```

🟢 Every prompt file of the skill passes `python -m prompt_lang` and stays
under 12,000 characters, and a structural test in the suite holds the
shape.

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
uv run --no-project --with "sdlc-taskcontract @ git+https://github.com/JJandDjango/sdlc-kit.git@v0.18.0" python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
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

---

## 9. Following the work 🟢

> 🟢 **Shipped** (kit 0.15.0, [ADR 0031](decisions/0031-the-work-is-one-derived-tree.md),
> contracts `specs/tree-view/` and `specs/pane-view/`; kit 0.16.0,
> [ADR 0032](decisions/0032-plain-names-conditions-drift-and-an-outline.md),
> contract `specs/project-tree/`, "Gates and their conditions" to "The
> interactive pane"; kit 0.17.0,
> [ADR 0034](decisions/0034-a-seat-signs-its-half-in-a-revision-row.md) and
> [ADR 0035](decisions/0035-gates-roll-up-and-a-feature-shows-before-intake.md),
> contract `specs/tree-first-level/`, "Gates roll up their features" to
> "Revisions and halves"; kit 0.18.0,
> [ADR 0036](decisions/0036-the-appendix-names-the-contract-and-a-unit-row-holds-done.md),
> contract `specs/feature-document/`, "A parked document"; kit 0.19.0,
> [ADR 0037](decisions/0037-a-feature-document-is-a-pair-and-each-document-has-one-seat.md),
> contract `specs/document-split/`, "A pair of documents").

🟢 `taskcontract tree` prints the repo's work as one tree, computed from
the kit's files at every run and never stored. It reads the contracts,
`.sdlc/config.yaml`, the findings, the progress files, git, and two name
lists the kit ships (`taskcontract/data/gates.yaml` and
`taskcontract/data/tasks.yaml`). Of the documents, it reads only each
feature document's revision table ("Drift from the feature document",
below), and the title line of one with no contract ("Features before
intake"): nothing else under `docs/`, and no REQUEST, STATE or plan. It
writes no file; `taskcontract progress` is the only writer, and only under
`.sdlc/progress/`.

### What the tree holds 🟢

🟢 The gates come first, at the repository level: each gate in
`active_gates`, and any other gate a finding names, marked `inactive`.
Each finding under `.sdlc/findings/` prints once, under the gate its
`gate:` field names, or under that gate's condition when the field names
one ("Gates and their conditions", below); `gate: none` prints under a
`none` item, and the form's `TEMPLATE.yaml` prints nothing. A finding is
read only from a `.yaml` file, so a `.yml` file there never shows. Then
each feature: a contract, with its verdict at every gate in
`active_gates` and at the next gate, marked `inactive`, its units, each
unit's seven tasks, and its checks, one per `acceptance_sketch` line; or a
feature before intake, with its verdicts and its two halves ("Features
before intake", below).

🟢 Every item has an id, a path you pass to the commands below:

| Item | Id |
|---|---|
| a gate, a finding, the no-gate item | `gates/G0`, `gates/G0/<finding>`, `gates/none` |
| a feature, its verdict at a gate | `<feature>`, `<feature>/G0` |
| a half | `<feature>/request`, `<feature>/solution` |
| a unit | `<contract>/<unit>` |
| a task | `<contract>/<unit>/<task>`, with the keys in "The seven tasks" |
| a check | `<contract>/<unit>/<check>`: the ids in the sketch's trailing parentheses, joined with `+` (`SC5.1+SC5.2`), else `sketch-<n>`, counted from 1 |

🟢 An item's summary and its plain name ("Plain names and titles",
below) are its source's own text, with their ends stripped and each line
break read as one space. Only a contract has a summary, its `intent`. The
plain names are a contract's `title`, the words of a feature before
intake's title line after its first ` - `, a half's `Request half` or
`Solution half`, a unit's `done_means`, a check's sketch line, a finding's
`statement`, and a gate's, a condition's or a task's name from the kit's
lists. Links come only from source fields: a unit's `depends_on`, each
entry once in the order it first appears, and a finding's `gate`. A
feature document shows as a file reference, found by the feature's id at
`docs/features/<id>.md`.

🟢 Each item prints on one line, indented two spaces per level: its full
id, its plain name, then its status in brackets (a finding shows `[kind:
<kind>]` in its place), its marks (`inactive` on a gate that is not
active, `current` on the current task, a contract's drift mark, a feature
before intake's revision mark), its evidence, its links (`depends_on:
<contract>/<unit>`, `gate: <value>`), a feature's
`doc: docs/features/<id>.md`, and last ` | ` and its summary.
The plain name and each part after the status print only when the item
has them, and a line break inside a part, such as in a multi-line
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
- 🟢 A unit or a feature takes the first of `failed`, `waiting on a
  seat`, `blocked` and `doing` that any child has. It reads `done` only
  when every child reads `done`, and `to do` when nothing under it has
  started. Two children never count: a feature's inactive gate ("Gates
  and their conditions") and, once a contract is closed, its verdicts
  ("Blocked and waiting, named"). A feature before intake never reads
  `done` ("Revisions and halves"). A gate item and its conditions read the
  roll-up of the features' verdicts instead ("Gates roll up their
  features").

🟢 An item names its evidence on its line. A done check names the run
that proved it, `via <command> at <commit>`. A done task names the commit
its own done record was written at, `at <commit>`, and a done approval
names its seat too, `by <seat> at <commit>`. A unit or contract that
reads `done` after a close with `progress done` names that close, `at
<commit>`; one that a later record changed, such as a task started again
or a check's red run, reads as that record says and names none. A
blocked task names its reason, `because <reason>`. A contract's `G0`
verdict, whatever it reads, names the validator run behind it:
`via python -m taskcontract validate specs/<contract>/contract.yaml
--profile ready at <commit>`; a feature before intake's names none, since
no validator runs ("Features before intake"). A signed half names its
signature, `by <signer> at rN` ("Revisions and halves").

🟢 Evidence ends in `dirty` in two cases. A run, a task's record or a
close reads `dirty` when a tracked file differed from `HEAD` as it was
recorded; untracked files do not count, so the untracked REQUESTs in a
repo's root never mark it. A contract's `G0` verdict reads `dirty` when
its own contract file differs from `HEAD`: changed, staged or not, or not
yet committed. Outside a git repository the commit reads `no commit`, and
nothing reads `dirty`.

### The three modes 🟢

- 🟢 **`taskcontract tree`** prints the whole tree and exits 0. Each
  source it cannot read prints one line on stderr, and the rest of the
  tree still prints.
- 🟢 **`taskcontract tree <id>`** prints one item, for an agent that needs
  one fact without reading a document: its line as the whole tree prints
  it, cut after the evidence, then one labeled line per field it has:
  `summary:` whole, on a contract only, one line per link kind with its
  targets joined by `, `, `doc:`, `file:` and `page:`. A file reference
  is a repo path with the line the item starts at: line 1 for a contract,
  its verdicts and a finding, the line its entry starts for a unit or a
  check, and for a half the line of its counting signature, else line 1;
  a feature's document shows on its `doc:` line at line 1. A gate, a
  verdict, a condition and a task name the kit page that defines the gate
  or the task, a path in the kit's repository. So an item never takes
  more than seven lines, whatever its fields hold. Every id the tree
  prints works here, matched whole. An id that names two items (a check whose sketch names a
  task key, such as `(commit)`, or a unit named like an active gate)
  prints both, in the tree's order, with an empty line between them. An
  unknown id exits 2 with `no node '{id}' - print the tree to list every
  node id`, and an id with `--follow` exits 2 with `taskcontract tree:
  --follow takes no id - give the id or --follow, not both`.
- 🟢 **`taskcontract tree --follow`**, with the `pane` extra, runs the
  interactive pane ("The interactive pane", below): the whole tree as an
  outline, moved through with the keys and the mouse. It renders again
  within two seconds of a change to a source file (a vocabulary change
  can take longer, below), and never while nothing changes. Ctrl-C exits
  0. It runs on Windows.

🟢 One check of this kit's own tree: its sketch line is its plain name,
and its evidence names the commit of its last green run:

```
$ taskcontract tree tree-view/t6-query-face/SC6.1
tree-view/t6-query-face/SC6.1 verify an item id prints its source field, status, links and each file reference in at most 20 lines (SC6.1) [done] via python -m pytest tests/test_tree_query.py -q --tb=no -p no:cacheprovider -k sc6_1 at 7945f13
file: specs/tree-view/contract.yaml:186
```

🟢 The pane lists its sources once a second: every file under `specs/`,
`.sdlc/findings/`, `.sdlc/progress/` and `docs/features/`, plus
`.sdlc/config.yaml` and the kit's two lists. It renders again only when a
file was added, removed or changed; a terminal resize cuts each line
again to the new width without a render. It keeps each contract's `G0` reading in memory until that contract's file
changes. A change under `specs/vocabulary/` drops every reading, so that
render runs the validator on every contract and can take longer than two
seconds on a repo with many contracts.

🟢 The current task is derived, never stored: the task marked `doing`
most recently; with none `doing`, the first `to do` task in the contract
that changed most recently; with no progress at all, none, and the pane's
cursor starts on its first line. Marking the current task done moves it on.

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
contract reads `done` whatever its verdicts read, and each verdict keeps
the validator's reading on its own line. A record written after a close
still counts, so a task started again or a check's red run changes what
the closed item reads. A contract
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
task arrives at an approval, never on a render, with the item's id in
`SDLC_NODE` and its own output discarded. A pane that starts on an
approval has arrived there, so it runs the command at once. The pane
never waits on the command. One that ends nonzero shows `notify failed,
exit {code}: {command}` inside the pane, whole, under the outline, until
the next render; when the shell itself cannot start, the same line reads
code 127. The pane keeps running either way, and with no `notify` set it
runs the same. Ctrl-C ends the pane and leaves the commands it started
running. The key is optional, and
the config template does not carry it. The command is the kit's edge: a
terminal multiplexer's plugin (herdr's, for one) wraps it outside the
kit.

### The pane's lines 🟢

🟢 The waiting line (`waiting on a seat: ...`, above) stands first while
the current task is an approval, word for word, since a multiplexer's
plugin may read it.

🟢 Each item line under another item opens on the **last segment of its
id** (`o7-release`, `approve-tests`), since the lines above give the
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

- 🟢 **`parts:`** lists what each item line shows after its id and plain
  name, from `status`, `marks`, `evidence`, `links`, `doc` and `summary`.
  The id and the plain name always show, and listing `id` changes
  nothing. The parts print in that fixed order whatever order the list
  gives, and `[]` shows the id and the plain name alone. Unset, each item
  line shows every part it has. The key leaves the waiting line, the
  cursor line and `taskcontract tree` unchanged.
- 🟢 **`fold: names`** makes each closed item's group name the items it
  holds in place of the counts: each item as `<id> [<status>]`, the id as
  its own line would show it, joined by `, ` in the tree's order.
  `fold: counts`, or no `fold:`, keeps the counts by status.

🟢 A bad key never stops the pane. A `parts:` that is not a list, or that
names anything but the seven parts, is ignored as a whole, so each item
line shows every part it has. A `fold:` other than `names` or `counts`
keeps the counts. Either shows one line inside the pane at each render,
as an unreadable source does. `{value}` is the first entry that names no part,
or the whole value when it is not a list, and for `fold:` the value, each
as YAML reads it, so `fold: yes` prints `True`:

```
taskcontract tree: pane parts ignored: {value} - give a list from id, status, marks, evidence, links, doc, summary
taskcontract tree: pane fold ignored: {value} - give names or counts
```

🟢 A `tree:` or `pane:` that is not a mapping reads as unset, as it does
for `notify:`.

### Gates and their conditions 🟢

🟢 Each gate opens into its **conditions**, the named parts its kit page
lists, in the page's order. `taskcontract/data/gates.yaml` lists every
gate's conditions, 57 in all, each an id and a plain name: the page's
heading without its date note and without a last word "check" or "join"
(`G0.1 Definition-of-ready`, `G0.2 Vocabulary coverage`, `G0.3 Unit
confirmation`).

🟢 Each feature shows its gates first: each gate in `active_gates`, then
the first gate after them in the kit's order, marked `inactive`, the gate
its work reaches next. With `active_gates: [G0]`, every contract shows `G0`,
then `G1` marked `inactive`. An inactive gate and its conditions read `to
do`, and never count toward the contract's status, so a closed contract
still reads `done`.

🟢 Under a contract, each of G0's conditions takes its status from the
rules it owns, read as the `G0` verdict is read: `failed` when one of its
rules fails the draft profile, `done` when none fails the ready profile,
`blocked` when `TC003` fails it, and `to do` otherwise. A feature before
intake's conditions read `to do` ("Features before intake"), and a gate
item's read the roll-up of the features' ("Gates roll up their
features").

| Condition | Its rules |
|---|---|
| G0.1 Definition-of-ready | TC000 to TC009, TC013 to TC015 |
| G0.2 Vocabulary coverage | TC010 to TC012, TC017, W001 |
| G0.3 Unit confirmation | TC016, TC018 |

🟢 Every code the validator emits belongs to exactly one condition. A
warning (`W001`) never changes a status and never shows. The `G0` verdict
still reads from the validator, as above, so it agrees with its
conditions: `failed` when one reads `failed`, else `blocked` when one reads
`blocked`, `done` when all three read `done`, and `to do` otherwise. A
contract the tree cannot read as a mapping, one it names on stderr as an
`unreadable contract`, reads `failed` at G0.1 and `to do` at G0.2 and
G0.3, since their joins read nothing from it. A feature's conditions at
every other gate read `to do`: the kit computes none of them yet.

🟢 A condition that is not `done` lists what its rules report, one line
under it per diagnostic: `- `, then the validator's message without its
code. A message repeated word for word prints once. A `failed` condition
lists the draft profile's messages, any other the ready profile's. A
contract at draft-green with one draft term, before intake has written
its `Ready:` row:

```
apply-discount Apply one discount code per order [to do] no "Ready:" row doc: docs/features/apply-discount.md | Checkout applies one discount code per order.
  apply-discount/G0 Planning / Intake [to do] via python -m taskcontract validate specs/apply-discount/contract.yaml --profile ready at 1a2b3c4
    apply-discount/G0/G0.1 Definition-of-ready [done]
    apply-discount/G0/G0.2 Vocabulary coverage [to do]
      - entity 'discount-code' is not ratified (status: draft) - draft does not resolve; ratify the term or fork the vocabulary task
    apply-discount/G0/G0.3 Unit confirmation [done]
  apply-discount/G1 Requirements / Spec [to do] inactive
    apply-discount/G1/G1.1 Spec/schema linting [to do]
    apply-discount/G1/G1.2 Model checking [to do]
    apply-discount/G1/G1.3 Criteria completeness + ambiguity review [to do]
```

🟢 At the repository level each gate opens into its conditions too, and a
finding whose `gate:` names a condition stands once under that condition,
never under a feature. A finding that names the gate itself, or a
condition its gate does not list, stands under the gate, after its
conditions.

| Item | Id |
|---|---|
| a condition | `gates/<gate>/<condition>`, `<feature>/<gate>/<condition>` |
| a finding that names a condition | `gates/<gate>/<condition>/<finding>` |

🟢 `taskcontract tree <id>` prints a condition as it prints a gate: its
line, which carries its plain name, and the gate's `page:`. Its
diagnostics print with the whole tree.

### Plain names and titles 🟢

🟢 Each item line opens on its id and its **plain name**, the words that
say what it is, then the parts `tree: pane: parts:` selects: `G0.2
Vocabulary coverage`, never `G0.2` alone. `parts:` never leaves out the
plain name, as it never leaves out the id, so `[]` shows both.

| Item | Its plain name |
|---|---|
| a gate, a verdict | the gate's name in `taskcontract/data/gates.yaml` |
| a condition | its name in `taskcontract/data/gates.yaml` |
| a task | its name in `taskcontract/data/tasks.yaml` |
| a feature with a contract | its contract's `title`, else `(no title)` |
| a feature before intake | its document's title line, after the first ` - `, else `(no title)` |
| a half | `Request half` or `Solution half` |
| a unit | its `done_means` |
| a check | its sketch line |
| a finding | its `statement` |

🟢 A plain name follows the summary rule above: its ends stripped, each
line break read as one space. An item whose source gives no text, such as
`gates/none` or a unit without `done_means`, shows no plain name; only a
feature shows `(no title)` in its place. A unit's, a check's and a
finding's plain name is the text that closed their line in 0.15.0, now
after the id, so the `summary` part holds only a contract's `intent`, and
`taskcontract tree <id>` prints its `summary:` line only for a contract.
An excerpt:

```
apply-discount Apply one discount code per order [doing] doc: docs/features/apply-discount.md | Checkout applies one discount code per order.
  apply-discount/u1-code-field The checkout form validates a discount code before it applies it. [doing]
    apply-discount/u1-code-field/approve-tests Approve the test list [done] by user at 1a2b3c4
    apply-discount/u1-code-field/write-tests Write the tests [doing] current
```

🟢 Once a feature has a contract, its plain name is the contract's
`title`, an optional field of one line that holds more than blanks. The
contract schema moves from 1.4.0 to 1.5.0 for it, and a `title` that is
blank or holds a line break fails the draft profile with `TC002`, under
G0.1. The tree reads the `title` from the contract, never from the
document. Intake copies it from the feature document's title line,
`# <id> - <title>`: the words after `<id> - `, or the whole heading when
it opens on anything else. A contract without a `title`, as every contract
written before 0.16.0 is until one is added, shows `(no title)`.

🟢 The pane's item lines open the same way, on the last segment of the id
and then the plain name. The waiting line keeps the id alone.

🟢 The pane's cursor line and `taskcontract tree <id>` show each item's
plain name and document reference from its source: a feature's title and
its feature document; a half's name and the row of its counting
signature, else the document's line 1 ("Revisions and halves"); a unit's
`done_means` and a check's sketch line, each with its contract file and
line; a gate's, a condition's and a task's name and kit page.

### Drift from the feature document 🟢

🟢 For a feature with a contract, the tree opens its document at
`docs/features/<id>.md` for its revision table only: the first table in
the file. A row counts when its last cell, the changes made, opens on
`r<N>:`; the tree skips every other row. Two revisions come from the rows
that count:

- 🟢 The **document's revision** is the highest `rN` of a row that is
  none of a `Ready:` row (its cell opens `rN: Ready:`), a `Measured:` row
  (`rN: Measured:`), a `Signed:` row (`rN: Signed:`, a signature or
  not) or a `Parked:` row (`rN: Parked:`).
- 🟢 The **contract's revision** is the `rM` that the newest `Ready:` row
  names, the one with the highest `rN` among those whose cell holds
  `derived from rM`. Intake writes the row in that fixed shape, `rN:
  Ready: ... derived from rM ...`. When two such rows share that `rN`,
  the lower one in the table wins, and a row that names more than one
  `rM` gives its first.

🟢 The feature's line names what the tree finds, as a mark after its
status:

- 🟢 `stale: document rN, contract from rM` when the document's revision
  is higher than the contract's.
- 🟢 `no feature document` when there is no file at
  `docs/features/<id>.md`.
- 🟢 `no "Ready:" row` when the file holds no `Ready:` row that names its
  `rM`, or cannot be read as text.

🟢 With none of the three marks, the contract matches its document; a
contract's `rM` above the document's revision matches too. A
document whose table runs `r1`, `r2`, `r3: Ready: ... derived from r2`,
`r4`:

```
apply-discount Apply one discount code per order [doing] stale: document r4, contract from r2 doc: docs/features/apply-discount.md | Checkout applies one discount code per order.
```

🟢 The pane already lists `docs/features/`, so an edit to a document
shows within two seconds. The contract records nothing new for this.

🟢 When the request is a feature document at `docs/features/<id>.md`,
intake adds one row to each document's revision table once the contract
validates ready-green: the date, `intake`, and a changes cell that opens
``rN: Ready: contract `<id>` validates ready-green, derived from rM``,
with `rN` the next revision in that table and `rM` that table's signed
text revision.

### Blocked and waiting, named 🟢

🟢 Each unit and each task shows `done`, `doing` or `to do` from the
progress record, as "Six statuses" reads them. A closed unit reads `done`.
A closed contract reads `done`, whatever its verdicts read; each verdict
still shows the validator's reading on its own line.

🟢 A task blocked by its own record names its reason on its own line,
`because <reason>`, the `--reason` that `taskcontract progress block` took.
Only a task takes a `--reason`, so a unit or contract that reads `blocked`
through one of its tasks names none; the task does.

🟢 The approval that holds the current task reads `waiting on a seat` and
names the seats it waits on, `seat: <seats>`: its unit's `confirmed_by`,
the seats that answered for the unit at intake, joined by `, `. Nothing
else records a seat before the approval's answer. A unit without
`confirmed_by` names none. The waiting line keeps its words.

```
    apply-discount/u1-code-field/approve-commit Approve the commit [waiting on a seat] current seat: user
```

🟢 Both print as the line's evidence, so a `tree: pane: parts:` list
without `evidence` leaves them out.

### The interactive pane 🟢

🟢 With the `pane` extra, `taskcontract tree --follow` runs an interactive
outline of the whole tree. The extra installs Textual (`>=8.2,<9`), a
terminal-UI library; every other command still needs only jsonschema and
PyYAML.

```bash
pip install 'sdlc-taskcontract[pane]'
```

🟢 The pane holds, top to bottom: the waiting line, when the current task
is an approval; the outline; the lines the pane reports (below); and the
cursor line. 0.15.0's where-am-I line, fold lines and `no current task`
line give way to the outline.

🟢 The outline holds every line `taskcontract tree` prints, in its order:
each item, and each diagnostic under its condition or gate item. An
item's line opens as "The pane's lines" gives, a top-level item on its
full id and any other on the last segment of its id, then its plain name
and the parts `tree: pane: parts:` selects. Each line shows its text as
written, so `[to do]` reads as brackets, never as a style.

🟢 The pane opens with each feature open, so a contract shows its units
and a feature before intake its verdicts and halves, and every other item
closed, whether or not a task is in flight. A task in flight
also opens its own unit, so the current task shows. Its line carries
`current` whatever `parts:` selects, the cursor starts on it, and the
window scrolls to it. With no current task the cursor starts on the first
line.

🟢 A closed item's line shows what it holds, in parentheses after its
status: `(<n> items: <counts>)`, the items one level below it counted by
status in the order "Six statuses" gives, zeros left out, then each
finding by its kind, `<n> kind: <kind>`; or under `fold: names` each item
as `<id> [<status>]`, joined by `, `. A closed condition or gate item
counts its diagnostics, `(<n> diagnostics)`.

🟢 A plain name that would push the status, those parentheses and the
current task's `current` past the pane's right edge is cut where they
still fit, ending in `...`; the other parts after them are cut at the
edge. The cursor line shows the name whole.

🟢 This kit's own tree at o7's first approval, in a pane 57 columns wide
with the cursor on the current task; the waiting line wraps at this
width, and `...` rows stand for rows left out here:

```
waiting on a seat: approve-tests for
project-tree/o7-release
...
▼ project-tree (no title) [waiting on a seat] doc: docs/f
├── ▶ G0 Planning / Intake [done] (3 items: 3 done) via p
├── ▶ G1 Requirements / Spec [to do] (3 items: 3 to do) i
...
├── ▶ o6-pane-keys `Up` and... [done] (10 items: 10 done)
└── ▼ o7-release Kit `0.16.0` ship... [waiting on a seat]
    ├── approve-tests Appr... [waiting on a seat] current
USAGE.md | Approve the test list
```

🟢 The **cursor line** shows the item at the cursor: its document
reference, then ` | ` and its plain name, whole, wrapping onto as many
rows as it needs. The reference is the one `taskcontract tree <id>`
prints: a feature's `doc:`, or its `file:` when it has no feature
document; a unit's, a check's, a finding's and a half's `file:`; a
gate's, a verdict's, a condition's and a task's `page:`. An item with no plain name
shows its reference alone, and one with neither shows its id. On a
diagnostic, the cursor line shows the diagnostic whole.

```
specs/project-tree/contract.yaml:134 | With the pane extra, `taskcontract tree --follow` shows all of the tree as an outline, each feature open down to its units. ...
```

🟢 Up and Down move the cursor one line. Right opens the item at the
cursor and Left closes it; on an item that holds nothing, or is already
open or closed, they change nothing. A click opens or closes the item it
lands on and puts the cursor there. The wheel scrolls the window and
leaves the cursor where it is.

🟢 The pane lists its sources as "The three modes" gives and renders
again within two seconds of a change, never while nothing changes. A render
keeps the cursor on the same item and every item open or closed as it
was, each item known by its path from the root, so two items that share
an id never trade places. An item new to the tree opens as at the start.
When the item at the cursor is gone, the cursor moves to its nearest
parent that remains. When a render moves the current task to another
task, the pane opens the items above the new one and scrolls it into
view, as at the start; the cursor stays where it was.

🟢 The waiting line stays the pane's first line, word for word. The
notify command runs as "The notify command" gives, once per arrival at an
approval, never on a render, with the item's id in `SDLC_NODE`. Ctrl-C
ends the pane with exit 0.

🟢 Each problem line (an unreadable source, a bad `tree: pane:` key, a
failed notify command) shows word for word inside the pane, under the
outline, each whole. A render replaces the
lines the one before it reported, and a notify failure stays until the
next render. The pane writes nothing to stderr while it runs.

🟢 Without the extra, `--follow` prints one line on stderr and exits 2;
an id with `--follow` still gets its own line first:

```
taskcontract tree: --follow needs the pane extra - pip install 'sdlc-taskcontract[pane]'
```

### Gates roll up their features 🟢

🟢 A gate item at the first level reads the roll-up of the features'
verdicts at its gate, and each of its conditions reads the roll-up of
that condition across the same verdicts: each feature's own reading of
the condition ("Gates and their conditions", above). A verdict marked
`inactive` never counts. A closed feature's verdicts count as they read:
a close governs only its own feature's roll-up.

🟢 The roll-up takes the first of `failed`, `waiting on a seat`,
`blocked` and `doing` that any verdict reads. Otherwise it reads `done`
when every verdict reads `done`, `to do` when every verdict reads `to
do`, and `doing` when some read `done` and some `to do`. A gate or
condition that no verdict counts in reads `to do`, as it does in a
repository with no feature.

🟢 A gate item or condition that is not `done` names each feature
holding it back: each feature whose counted verdict, or whose reading of
that condition, is not `done`. Each prints as one line under the item,
`- ` then the message, in the tree's order of features, before the
item's conditions and findings:

```
{feature} holds {id} at {status}
```

🟢 `{feature}` is the feature's id, `{id}` the gate's or condition's own
id (`G0`, `G0.1`), and `{status}` what that verdict or condition reads.
The pane folds a closed gate item that names features as it folds a
condition, `(<n> diagnostics)`, and shows a `holds` line whole on the
cursor line.

🟢 A finding still stands once, under the condition or gate its `gate:`
field names, and shows its kind, never a status. It counts in no
roll-up, so a finding never changes what a gate or condition reads.

🟢 With two features, `apply-discount` at `to do` as in "Gates and their
conditions" and `ship-rates` `done` at G0:

```
gates/G0 Planning / Intake [doing]
  - apply-discount holds G0 at to do
  gates/G0/G0.1 Definition-of-ready [done]
  gates/G0/G0.2 Vocabulary coverage [doing]
    - apply-discount holds G0.2 at to do
  gates/G0/G0.3 Unit confirmation [done]
```

### Features before intake 🟢

🟢 Each `.md` file directly under `docs/features/` that has no
`specs/<id>/contract.yaml` shows as a feature at the first level: a
**feature before intake**, from its first revision on. A design
document, `<id>.design.md`, is the one exception ("A pair of
documents"). A document whose table holds no revision shows too. Its id
is the file's name without `.md`. The features with a contract keep the
order of `specs/`, and a feature before intake stands among them by its
id.

🟢 Its plain name is the words of its document's title line, the first
`# ` line, after the first ` - `. For a title line in the template's
form, `# <id> - <title>`, those are the words intake copies into the
contract's `title`. A document with no title line, a title line with no
words after a ` - `, or a document that cannot be read as text reads `(no
title)`. The tree reads such a document once per print, its first table
and its title line, and prints none of its other words.

🟢 It shows its verdicts as a feature with a contract does: its G0
verdict, then its next gate marked `inactive`, each opening into its
conditions. Its G0 verdict and those conditions read `to do` and name no
validator run, since there is no contract to validate. That verdict
counts in `gates/G0`'s roll-up, and `gates/G0` names the feature: `<id>
holds G0 at to do`.

🟢 `taskcontract tree <id>` prints a feature before intake's line, then
`doc: docs/features/<id>.md:1`; the cursor line shows the same
reference. Its verdicts name their `page:` and no `file:`, since no file
decides them.

🟢 Once intake writes `specs/<id>/contract.yaml`, the feature stays one
item: it shows its contract's verdicts, units and drift mark, and none of
the revision and halves below. Its plain name comes from the contract's
`title` from then on, never from its document.

### Revisions and halves 🟢

🟢 A feature before intake names its document's revision as a mark, `no
contract: document rN`. `rN` is the highest revision of a **text row**: a
row that counts and opens on none of `Ready:`, `Measured:`, `Signed:` or
`Parked:`. A document with no text row, or that cannot be read as text,
shows `no revision table` in its place.

🟢 After its verdicts come its two **halves**, one item each:

| Item | Id | Plain name |
|---|---|---|
| the request half | `<feature>/request` | Request half |
| the solution half | `<feature>/solution` | Solution half |

🟢 A seat signs its half with a revision row whose changes cell opens
`rN: Signed: request half` or `rN: Signed: solution half`, free words
after (ADR 0034). After `rN:` those words are fixed: case as shown, one
space between them, the half's name ending at a word's end. The row
changes no text: it signs the text row above it with the highest
revision, a tie going to the lower row. A signed half reads `done` and
names its signature as evidence, `by <signer> at rN`: the signer is the
row's `Revised By` cell, `rN` the row it signs. The half names its seat:
the PO seat signs the request half, the engineer seat the solution half.
When a half has more than one signature, the row with the highest
revision counts, a tie going to the lower row. A half with none reads `to
do`. A row is no signature when it takes any other form, names neither
half, has no text row above it, or has a blank `Revised By` cell, the
cell before the last, so a row of fewer than three cells signs nothing.

```
| 2026-09-28 | user | r4: Signed: request half. The PO seat signs r3 |
```

🟢 A feature before intake rolls up its verdicts, but not the inactive
one, and its halves: it reads `to do` until a seat signs a half, then
`doing`. G1's feature before intake, with its request half signed and
its design document at r1 ("A pair of documents"):

```
g1-requirements-spec Failure points found before development starts [doing] no contract: document r3 design r1 doc: docs/features/g1-requirements-spec.md
  g1-requirements-spec/G0 Planning / Intake [to do]
    g1-requirements-spec/G0/G0.1 Definition-of-ready [to do]
    g1-requirements-spec/G0/G0.2 Vocabulary coverage [to do]
    g1-requirements-spec/G0/G0.3 Unit confirmation [to do]
  g1-requirements-spec/G1 Requirements / Spec [to do] inactive
    g1-requirements-spec/G1/G1.1 Spec/schema linting [to do]
    g1-requirements-spec/G1/G1.2 Model checking [to do]
    g1-requirements-spec/G1/G1.3 Criteria completeness + ambiguity review [to do]
  g1-requirements-spec/request Request half [done] by user at r3
  g1-requirements-spec/solution Solution half [to do]
```

🟢 `taskcontract tree <id>` prints a half's line, then its `file:`: the
line of the row whose signature counts, or line 1 when it has none. The
cursor line shows the same reference.

```
g1-requirements-spec/request Request half [done] by user at r3
file: docs/features/g1-requirements-spec.md:6
```

🟢 A `Signed:` row never ages a contract: the document's revision in
"Drift from the feature document" leaves out every row that opens
`Signed:`, a signature or not.

### A parked document 🟢

🟢 A `Parked:` row is no text row either: intake writes one in each
table when it parks a pair, and it never moves `rN`.

### A pair of documents 🟢

🟢 The tree shows a pair before intake as one feature.
`docs/features/<id>.design.md` is never a feature of its own, and a
design document with no requirements document beside it prints nothing.
The feature's line gains a second mark, the design document's newest
text revision, and the solution half reads its signature from the design
document. The feature's line and its two halves, with the verdicts
between them left out:

```
x The outcome, in a few words [doing] no contract: document r3 design r3 doc: docs/features/x.md
  x/request Request half [done] by ann at r3
  x/solution Solution half [done] by raj at r3

$ python -m taskcontract tree x/solution
x/solution Solution half [done] by raj at r3
file: docs/features/x.design.md:6
```

🟢 With no design document, a feature prints as kit 0.18.0 prints it:
one mark, and the solution half from the document's own `Signed:
solution half` row, else `[to do]`. Once a design document stands, its
table alone gives the solution half. A design document with no text row
shows the mark `design: no revision table`.

🟢 For a pair through intake, the drift mark reads each table against
that table's `Ready:` row. The design's mark reads `stale: design r5,
contract from r3`, after the requirements document's mark. A combined
document through intake prints byte for byte as before. Before intake
the tree shows no mark for a stale design: the interview and intake
report it.

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
