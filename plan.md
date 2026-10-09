# Plan - Session 90 (2026-10-09) - g1-requirements-spec s2

**Deliverable:** unit `s2-model` of `g1-requirements-spec` on one PR,
with a Two-Key PASS. It is the second unit of kit 0.20.0.

## Overview

**The project.** `sdlc_development_kit` (the kit) is a set of gates for
software that AI agents write. A gate is a pass/fail checkpoint between
two phases of the work: the work goes on only when the gate reads
green. Each gate turns a human judgment into a written artifact plus a
mechanical check, so an agent cannot lower the quality of a codebase
unseen. A repository that uses the kit is a consumer. Release 0.19.0
computes one gate, G0 (planning and intake: a feature's contract is
ready to build).

**The feature.** `g1-requirements-spec` adds the second gate, G1. G1
finds a failure point before development starts, and it has three
conditions:

- G1.1: a linter reads each boundary schema clean.
- G1.2: a checker passes the model of each hard core.
- G1.3: a named person signs a review of 11 items.

The feature is built as six units, one a session, and ships as kit
0.20.0:

| Unit | What it adds | State |
|---|---|---|
| `s1-lint` | G1.1, and the base: the record file and both commands | on main |
| `s2-model` | G1.2 | this session |
| `s3-review` | G1.3, and the `/sdlc g1` flow a person runs | to do |
| `s4-tree` | the tree shows G1 | to do |
| `s5-start` | no task starts before G1 passes | to do |
| `s6-release` | the release, and G1 turned on at the kit | to do |

**This unit, in plain words.** Some parts of a system are costly to get
wrong: a defect there comes from concurrency or a protocol, shows late
and is costly to reverse. The kit calls such a part a hard core. Before
anyone writes its code, a person writes a model, a formal description
of its design, and a tool called a checker explores the model for a
state that breaks one of its rules. After this unit, G1.2 reads done
for a feature only when a committed record shows that the model of each
hard core in the feature passed its checker.

## Terms

The kit's words:

| Term | Meaning |
|---|---|
| Gate | A pass/fail checkpoint between two phases. G0 is planning and intake; G1 is requirements and spec. |
| Condition | One named part of a gate, such as G1.2. It reads `to do`, `done` or `failed`. |
| Rule | One test with a code. `RS201`: a hard core has no model. `RS202`: the checker is not installed. `RS203`: the model does not pass. |
| Feature | One piece of work with its own contract. Here: `g1-requirements-spec`. |
| Contract | `specs/<id>/contract.yaml`: what the feature must do. It is signed, and the builder may not change it. |
| Unit | The smallest part of a contract that is verified by itself. Here: `s2-model`. |
| Check | One testable line of the contract, with an id such as SC3.1. |
| `done_means` | The one sentence of a unit that says when it is done. |
| Pair | The feature's requirements document and its design document, under `docs/features/`. Both are signed. |
| Engineer seat | The role that signs the design. Here it is the user. |
| Intake, re-intake | Intake writes the contract from the signed pair. A re-intake runs it again after a document changes. |
| Text row | One line of a document's revision table that records a change to its text. A signature follows it. |
| ADR | An architecture decision record under `decisions/`. It is never edited: a later ADR amends it. |
| USAGE | `USAGE.md`, the kit's user guide. A red mark means "described, not shipped yet". |
| Pass zero | A feature's first step: its guide is written in USAGE, red, before any code. `s1-lint` did it for all six units. |
| Tree | `python -m taskcontract tree`: the view of each feature, gate and task. |
| `progress` | The command that records each task's start, its test runs and its end. |
| `STATE.md` | The file that says what is in flight. It is rewritten at each session's end. |

This unit's words:

| Term | Meaning |
|---|---|
| Component | A part of a consumer's system with its own paths. |
| Hard core | A component whose defect would come from concurrency or a protocol, show late, and be costly to reverse. All three hold (ADR 0007). |
| Component declaration record | `specs/components.yaml`, a file a person writes: each component's paths, whether it is a hard core, and a hard core's model and checker. |
| Model | A formal description of a hard core's design, in TLA+ or P. |
| Checker | The tool that explores a model: TLC for TLA+, or the P checker. |
| Boundary schema | A file that fixes the shape of data between two services: JSON Schema, OpenAPI or protobuf. |
| Linter | The tool that reads a boundary schema for errors: Spectral or `buf`. |
| Pin | A tool's settings, committed in the repository: a linter's ruleset, or a model's configuration. |
| `g1.schemas` | The list in `.sdlc/config.yaml` that names the boundary schemas, each pattern with its linter and pin. One item of the list is an entry. |
| `g1-record` | The command that starts a tool and writes what it found. `g1-record lint` is G1.1's; `g1-record model` is G1.2's, new here. |
| Record | One result that `g1-record` writes to `.sdlc/g1/<id>.yaml`, a committed file. |
| `g1-check` | The command that reads the records and prints G1's verdict. It starts no tool. |

The outside tools:

| Term | Meaning |
|---|---|
| TLA+ | A language for writing a model of a design. |
| TLC | The checker for TLA+. It is a Java program. |
| `tla2tools.jar` | The one file that holds TLC. A jar is a packaged Java program, started as `java -cp tla2tools.jar tlc2.TLC`. |
| Java, Temurin | TLC needs Java. Temurin is the name of the free Java build installed here, at version 21. |
| P | A second modeling language, with its own checker. |
| Spectral, `buf` | The two linters. Spectral is installed here since session 88. |
| PATH | The list of folders where the system looks for a command by its name. |
| Wrapper script | A short script named `tlc` that starts Java with the jar, so that `tlc` works as a command. On Windows it is `tlc.cmd`. |
| Exit code | The number a program returns when it ends. 0 means success. |

The build's words:

| Term | Meaning |
|---|---|
| Drafter | An agent that writes the unit's tests first and proves they fail before any code exists (red). |
| Stand-in | A small fake tool the tests start in place of TLC, so the suite needs no real checker. |
| Prototype | The drafter's throwaway code. It proves the tests can pass. |
| Overlay | The prototype copied onto a scratch copy of the repository, where the whole test suite runs. |
| Retirer | An agent that retires the older tests a unit makes false. |
| Developer | An agent that writes the real code. It may not read the tests. |
| Interface note | What the developer gets in place of the tests: the names and the behavior to build. |
| Two-Key | The independent verifier's grade of one unit, PASS or FAIL. It runs the tests again by itself. |
| Receipt | The saved output of a run that proves a claim. A manual receipt comes from a live run of the real tool. |
| Probe | A scratch script that starts the real tool and prints what it does. |
| Explorers | Four read-only agents that mapped the kit's code for the design in session 84. Their notes stand in a receipt folder. |
| Reading | A choice Claude makes where the signed text leaves room. Each is listed at the top of the PR body. |
| Wrap | The session's closing PR: `STATE.md`, this plan, the memory index and the metrics row. |
| Agent tokens | The measure of the agents' work, and so of its cost. |
| `d4` | The fourth unit of an earlier feature, `document-split`. It is a cost basis. |

## What the unit ships

- The schema of the component declaration record,
  `taskcontract/schemas/component-declaration.schema.json` at 1.0.0,
  and its reader in `taskcontract/g1.py`.
- `g1-record model <id>`: it starts the checker of each hard core in
  scope and appends one G1.2 record.
- G1.2's three rules in `g1-check`: `RS201`, `RS202` and `RS203`.
- The unit's `done_means`: with a hard core in a feature's scope, G1.2
  reads done only when the record shows its model passes the checker.
  Checks SC3.1, SC3.2 and SC3.3.
- SC3.1 also takes a manual receipt: a live TLC run on one passing
  model and one failing model.
- No older test retires. One that fails on the prototype is an
  amendment or a finding, listed at the top of the PR body.

Read at this resume: main stands at `8625df9` (PR #108), equal to
GitHub's, with untracked files only. Tag `v0.19.0` stands at `7fe6342`.
Java 21 is installed. TLC is not: no `tlc` command is on PATH, and no
`tla2tools.jar` stands where one was looked for (the VS Code
extensions).

The flow is "plan approved, then PR review", in its first build. This
plan's approval decides the three rulings below. After it, the next
word needed from the user is the work PR's merge. A reading that
surfaces mid-build is Claude's, listed at the top of the PR body; one
that would change a signed contract sentence, a ratified term or an ADR
stops for the user.

The tight spot is the design's second risk. TLC has no command of its
own, and it ends on more exit codes than a linter. Step 2 probes it
live before any test names its call. It reads the exit code for a
passing model, for a broken invariant (a rule the model must always
keep), for a deadlock (a state with no next step) and for an error of
TLC's own, and it finds where TLC writes its working files. P gets no
live run: its call is read from its reference page and held by a
stand-in, as `buf`'s was.

## Rulings

1. **Two linters in one feature.** `g1-record lint` works today for a
   feature whose schemas all stand under one `g1.schemas` entry, with
   one linter. A feature with two entries, such as OpenAPI files under
   Spectral beside protobuf files under `buf`, is refused, so its G1.1
   can never read done. The fix needs a form for the record.
   Recommendation: each call writes one record that holds a result for
   each entry, each with its own linter and pin. ADR 0038 says "Each
   call appends one record, and the last record of a condition counts",
   and the design and USAGE repeat it. This form keeps that sentence
   true, and the G1.2 record already has it: one result for each hard
   core, each with its tool. The other form, one record for each entry,
   keeps the tests `s1-lint` wrote on the record's shape, and it makes
   the ADR's sentence false, so it costs an amending ADR. The build is
   not this session's. Either form changes signed design text, so the
   build takes a design text row, the engineer seat's signature and a
   re-intake, in its own session before `s6-release`. This session only
   gives the G1.2 record the matching form.
2. **How the kit starts TLC.** TLC comes as a jar with no command of
   its own. Recommendation: `g1-record model` looks for a command named
   `tlc` on PATH, as `lint` looks for `spectral`. A consumer whose
   install is the jar alone writes a wrapper script of that name. The
   other way, the kit starting `java` with a jar path from a new config
   key, adds a key the signed design does not draw. USAGE gains one red
   sentence that tells a consumer so.
3. **TLC on this machine.** The probe and the manual receipt need a
   real TLC here. Recommendation: download `tla2tools.jar` from release
   v1.7.4 of `tlaplus/tlaplus` on GitHub (2024-08-05, the newest that
   is no pre-release) into `C:/Users/hyden/tools/tlaplus/`, with a
   `tlc.cmd` wrapper beside it. No system setting changes: the probe
   and the receipt script add that folder to PATH for their own run
   only.

Claude's readings, each told here:

- The unit builds the schema and the reader. The kit's own
  `specs/components.yaml` is a file a person writes, and it lands when
  `s6-release` turns G1 on at the kit.
- USAGE holds the unit's guide, red, since pass zero. Its marks stay
  red until `s6-release`.
- Step 2's finding fixes which of TLC's exit codes mean "the model
  fails" and which mean "TLC could not run it". Lint's rule is the
  pattern: a tool that ends on an error of its own gives no result, so
  `model` prints the tool's lines, writes nothing and exits 2.

## Steps

1. Open. Branch `session-90-g1-s2-model` from `8625df9`; this plan,
   committed and pushed, then shown for approval.
2. Probe TLC. Download the jar by ruling 3. A scratch script starts TLC
   by the name `tlc` from Python on a passing model, a failing one, a
   deadlock, a model that does not parse and an absent configuration,
   and prints each call, its exit code and its output. The script and
   its output go to untracked
   `RECEIPT_g1-requirements-spec-s2_2026-10-09/`.
3. Draft. The drafter (`spec-channel-drafter.js`) writes the test list
   for SC3.1, SC3.2 and SC3.3 with a stand-in checker, proves it red
   from the repo root, and proves it can pass on a prototype, a scratch
   copy of the `taskcontract` package. It reads the probe's files and
   the explorers' `rules.md`.
4. Overlay. The session overlays the prototype on a scratch copy of the
   repository and runs the whole suite there. The retirer
   (`test-retirer.js`) runs only if an older test fails, on the failing
   modules alone.
5. Approve the list and prove red (Claude). Each fixed detail is
   checked against the contract, the pair, its Constraints and
   Decisions, the ratified terms under `specs/vocabulary/` and USAGE's
   red text; then `progress run <check> --expect red` records each
   check's failing run.
6. Green. The developer (`unit-developer.js`) writes the code from the
   interface note. Claude runs the suite after each round and tests
   each deviation and each question it returns against `done_means`.
7. Commit (Claude). The unit's commit, with ruling 2's USAGE sentence;
   each check green at the clean commit; the kit's own contract and
   scope checks green.
8. Manual receipt. A live TLC run through `g1-record model` on one
   passing model and one failing model, in a small consumer repository
   a script builds. Its text goes to the receipt folder.
9. Two-Key. The verifier (`two-key-unit-verifier.js`) grades the unit,
   with the receipt's text to read; `progress done` on PASS.
10. The work's close. The push, then the PR once CI reads green and
    Two-Key reads PASS, with Claude's readings at the top of its body.
    The merge is on the user's word.
11. The wrap, after the merge. `STATE.md` regenerated, this plan
    struck, the memory index updated and one row appended to
    `docs/session-metrics.md`, on a new branch off main in a wrap-only
    PR that Claude merges after green CI.

Steps 1, 2, 10 and 11 sit outside a contract unit, so the tree does not
show them.

The session boundary, if context runs short: after step 5. The approved
list, the prototype and the interface note are copied to the receipt
folder, and the developer round opens the next session.

## Cost

About 0.6 million agent tokens, in a range of 0.55 to 0.7 million. The
basis is two recorded code units: `d4` at 561K (drafter 213K,
developers 94K and 75K, Two-Key 179K) and `s1-lint`'s first round at
594K (drafter 225K, developers 104K and 60K, Two-Key 205K). A lost
Two-Key round adds about 300K: `s1-lint`'s second cost 316K (developer
69K, Two-Key 247K). A retirer round, if an older test fails, adds 62K
to 159K.

## Deferred, not this session

- `s3-review` to `s6-release` (ships 0.20.0), one unit a session.
- Ruling 1's build: the design's text row, its signature, the re-intake
  and the change to `lint`, before `s6-release`.
- G1.1's four other open edges and the four smaller ones, under
  `STATE.md`'s Open questions.
- A live run of P, and of `buf`.
- The engine (the pilot consumer, `E:\ImSimProject\engine`): its
  install ref, its config line and its first code, after G1 ships.
- The `google_workspace` server failed to connect again at this resume.
- `STATE.md` runs past its one-page budget.
- `STATE.md` Next actions 2 to 5 and its other open questions, carried.
