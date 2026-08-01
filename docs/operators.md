# Operators - the agent layer of the gate architecture

<!-- covers: specs/operator-layer/contract.yaml -->

> **Contract** - one question: *who operates each gate, and how does
> an agent drive it to green from diagnostics alone?*
> Component deep page. Feature set ratified in-session 2026-07-31
> (F1-F9 kept whole; rulings: developer + verifier ship first, spec +
> qa register behind venue existence; profile command bindings kept;
> verdict retrofit document-only); task contract
> `specs/operator-layer/contract.yaml`.

**Status legend:** 🔴 ratified, not yet shipped · 🟢 shipped ·
⚪ deferred behind a named trigger. Docs Pass 0 authored 2026-07-31,
before any implementation; markers flip as units land.

## The roster - personas, not per-gate files

The registry already names the operators
([gates.md](gates.md), mutability model): Spec agent authors G0-G2
artifacts, Developer works only inside G3, QA executes G4-G7 and owns
the class-E configs of the scheduled venues, Verifier is
cross-cutting. A gate is a venue; an operator is an actor convening
in several venues. The file count follows the census of actors, not
the count of venues - "per-gate" lives in each def's venue bindings,
never in per-gate files. This is the two-layer model
([0008](../decisions/0008-two-layer-condition-model.md)) applied to
agents: the persona is the shape, the gate binding is the profile.

| Operator | Convenes at | Write surface | Status |
|---|---|---|---|
| `sdlc-developer` | G3 inner loop; G4 local preflight | implementation + unit tests only ([0010](../decisions/0010-write-surface-immutability.md)) | 🟢 0.8.0 |
| `sdlc-verifier` | cross-cutting - subject checks + zero-trust re-runs | none - writes nothing | 🟢 0.8.0 |
| `sdlc-spec` | G0-G2 authoring venues | spec artifacts | ⚪ registered - ships at the first bound G1/G2 authoring surface; `/sdlc intake` is the live G0 flow today |
| `sdlc-qa` | G4-G7 execution; G8-G10 config ownership | committed configs (class E) | ⚪ registered - ships at the first consumer G5-G7 pipeline |

Human seats never delegate: G1.3 criteria review, G6.1/G6.2 (the
human principal), G8.3 (the operations principal), PL-PIPE.1 (the
sixth census seat). Agents assist at most - scouting, clustering,
drafting; suggestions, never verdicts.

## 🟢 Verdict contract (F1 - unit: verdict-contract)

Every pipeline-native check speaks one contract - the extension of
ADR [0020](../decisions/0020-merge-gate-distribution-shape.md)'s
residence rule: a check is a taskcontract subcommand behind the pin,
*speaking the verdict contract*.

- **Exit codes:** `0` green · `1` red, findings emitted · `2` not
  applicable or unusable invocation (no spine, unresolvable base).
- **`--json`:** findings as a JSON array, one object per finding,
  fields stable per surface - diagnostics are never prose-only.
- **Codes:** stable and greppable (TCnnn, VTnnn/VCnnn/W001, G410-Vn,
  audit codes) - a break announces itself by name in the consumer's
  own CI.

Conformance today (documented fact - no module's exit semantics
change in this slice):

| Surface | Exit | `--json` fields | Delta vs contract |
|---|---|---|---|
| `taskcontract validate` | 0/1 | file, path, rule, message, severity | no not-applicable lane (2 = argparse usage only) |
| `taskcontract vocab-check` | 0/1 | same Violation shape | vocabulary absence = green by design (adoption pace), never 2 |
| `taskcontract suppression-audit` | 0/1/2 | file, line_no, vector, construct, detail | the exemplar 2-lane; field names differ (vector, not rule) |
| `audit.py` (skill engine) | 0/1/2 | - | line diagnostics with codes; no `--json` yet |
| `update.py` (skill engine) | 0/1/2 | - | row report; no `--json` yet |

Field-name convergence (code, location, message, severity uniform
across surfaces) is a registered follow-up riding the next
pipeline-native module - not this slice.

## 🟢 Loop protocol (F2 - unit: loop-protocol)

Generalized from the intake flow's I5 - the discipline every
operator def instantiates verbatim:

1. One check invocation per iteration - a single chain-free segment.
2. Read the findings; fix exactly what each diagnostic names -
   nothing else.
3. Cap 5 iterations per check venue. Persistent red: report the
   remaining findings verbatim and return control - never silent,
   never a sixth try.
4. No retry-to-green: an unchanged input never reruns hoping for a
   different verdict (G5's rule, applied to the inner loop).
5. The check and every gating config are read-only to the looping
   agent. Weakening the check to pass is the G4.10 defect class -
   stated as def discipline, caught mechanically at the merge gate
   regardless (never prompt-only enforcement).

## 🟢 The shipped pair (F3 + F4 - unit: operator-defs)

`agents/` lands at the plugin root (marketplace source `./`), so the
defs ride the plugin channel - versioned with the kit, delivered by
`claude plugin update`, never copied per repo (0020's anti-fork
doctrine applied to prompt artifacts). Both defs are class-E
artifacts - PL-PIPE scopes agent prompts - and each header names it.

**`sdlc-developer`** - G3's operator.

- MUST READ: the task contract (criteria, scope, non-goals), check
  diagnostics, the code it touches, `.sdlc/config.yaml` (stack ->
  profile command bindings).
- MUST NOT READ: acceptance-test source - criteria + diagnostics
  only. The session-7 anti-gaming ruling, Q5's decidable half: an
  agent that reads the test can satisfy the test; an agent that
  reads the criterion must satisfy the criterion.
- WRITES: implementation + unit tests, nothing else - in-prompt here,
  mechanically enforced at G4.6.
- LOOPS: the profile's G3 commands, then the G4 preflight set before
  any handoff.

**`sdlc-verifier`** - the cross-cutting zero-trust grader.

- MUST READ: the candidate diff and every check's `--json` verdict.
- RE-RUNS: validate, vocab-check, suppression-audit, `/sdlc audit` -
  itself, fresh. A reported green is hearsay.
- WRITES: nothing. The grade is PASS/FAIL with verdicts attached.

## 🟢 Venue map (F5 - unit: venue-map)

| Gate | Operator | Agent venue | Today |
|---|---|---|---|
| G0 intake | `sdlc-spec` (⚪) | conversation flow (`/sdlc intake`) | 🟢 venue live ([0016](../decisions/0016-distribution-before-activation.md)); def registered |
| G1 requirements | `sdlc-spec` authors; G1.3 human | conversation flow + human sign-off | ⚪ unbound |
| G2 design | `sdlc-spec` authors; G2.3 human | conversation flow + human sign-off | ⚪ unbound |
| G3 implementation | `sdlc-developer` | local inner loop (profile commands) | 🟢 0.8.0 - dotnet bindings; python has no G3 battery |
| G4 pre-merge CI | QA result-scoped; Verifier subject checks | **local preflight**; CI authoritative, agentless | 🟢 0.8.0 - preflight bindings + verifier re-runs |
| G5 integration | `sdlc-qa` (⚪) | scheduled pipeline - agentless execution | ⚪ unbound |
| G6 UAT | QA operates; human principal grades | human-graded (assist ceiling) | ⚪ unbound |
| G7 release | `sdlc-qa` (⚪) | ci-mechanical - agentless | ⚪ unbound |
| G8 operations | QA owns configs; operations principal grades G8.3 | standing invariants + human-graded (.3) | ⚪ unbound |
| G9 maintenance | `sdlc-qa` (⚪) | scheduled - unattended, agentless | ⚪ unbound |
| G10 retirement | mechanical in existing venues | agentless | ⚪ unbound |
| PL-DOC | mechanical arms riding G4/G9 | agentless | ⚪ unbound |
| PL-PIPE | .1 human seat; .2 mechanical; .3 evals | human + ci-mechanical | ⚪ unbound - eval obligation named on shipped defs |

Two rulings:

- **G4 preflight.** The merge gate's agent venue is local preflight -
  the same modules CI runs, driven green before push. CI stays
  authoritative and agentless: the queue evaluates the merged
  result; no agent convenes there.
- **Assist ceiling.** Human conditions take agent assist at most -
  suggestions, never verdicts (registry language, echoed as def
  constraints).

## 🟢 Profile command bindings (F6 - unit: profile-commands)

`profile.json` gains `commands:` keyed by binding - dotnet: `g3`
(format verify, strict build) and `g4-preflight` (solution test,
suppression audit) - every command one chain-free segment. Defs stay
stack-independent: an operator resolves the stack from the
consumer's `.sdlc/config.yaml`, then binds that profile's commands.
A profile without the block binds nothing - honest for python today,
which has no G3 battery. The block is data for operator defs, not
scaffold: `init.py` renders nothing from it.

## 🟢 Vocabulary drafts (unit: vocab-drafts)

`operator` and `verdict` scaffold as draft terms, `sources:` naming
this page. Ratification stays the user's class-S flip - never this
slice's act.

## Distribution - the plugin channel

Agents ride the plugin (channel 2 of
[distribution.md](distribution.md)'s three): `claude plugin update`
delivers them; the wheel does not carry them; and `/sdlc update`
deliberately does not cover `agents/` - it audits the committed
scaffold, and defs are never committed into consumers. Fit note: a
consumer wanting a local deviation forks the def into its own
`.claude/agents/` under a different name - kit defs are never merge
targets.

## ⚪ Deferred, triggers on record

- **`sdlc-spec` def** - trigger: first bound G1/G2 authoring
  surface (`/sdlc intake` already carries G0 live).
- **`sdlc-qa` def** - trigger: first consumer G5-G7 pipeline.
- **PL-PIPE.3 eval harness** - its own arc; the defs name the
  obligation (five invariant families per persona) so the debt
  stays visible.
- **Q5 decorrelation mechanism** - M0 reality data first; context
  manifests rule content only until then.
- **Mechanical loop runner** - def-embedded discipline this slice; a
  runner executable (a taskcontract subcommand per 0020) is a later
  build item.
- **Verdict field-name convergence** - rides the next
  pipeline-native module's build.

Shape precedents: [ADR 0021](../decisions/0021-operator-layer-shape.md).
