# Controlled language - bounded interpretation for executed prose

<!-- covers: specs/controlled-language/contract.yaml -->

> **Contract** - one question: *which words and shapes may executed
> prose use, and what checks it?*
> Component deep page. Feature set ratified in-walk 2026-08-02
> (F1-F12 kept whole; rulings: standalone dictionary beside the
> glossary; first surface = the six contract prose fields; posture
> hard-at-intake, legacy per census; named "bounded interpretation" -
> never "determinism"). Shape precedents:
> [ADR 0022](../decisions/0022-controlled-language-shape.md).

**Status legend:** 🔴 ratified, not yet shipped · 🟢 shipped ·
⚪ deferred behind a named trigger. Docs Pass 0 authored 2026-08-02
before implementation; all v1 units shipped the same session (0.9.0).

## The claim, stated honestly

Controlled language does not make execution deterministic - the
executor stays stochastic regardless of input. It shrinks the surface
where stochasticity acts and converts prose checks from LLM judgment
into string operations: THEORY.md's gate move ("a human judgment
converted into a text artifact plus a mechanical check") applied to
the prose plane. The kit-specific leverage: the anti-gaming ruling
makes criterion prose the developer's only spec view - the contract
is the last open-natural-language input in the G3 loop; this door
closes it.

**Non-goals** (the door's own, in THEORY's voice):

- **Not** meaning, completeness, or correctness - form checked;
  meaning not checked. Wrong-but-clear passes; the oracle problem
  stays THEORY's non-goal; Two-Key verification remains the
  guarantee. V4 annotations + the human ratification seats own the
  residue.
- **Not** a police for raw human requests - intake translates raw ->
  controlled; the human speaks freely and ratifies meaning, never
  writes in the controlled register.
- **Not** a register for deliberated prose - THEORY, ADRs, docs
  literature stay free. Boundary principle: controlled where prose is
  *executed* (an operator loops on it), free where *deliberated* (a
  human thinks with it).

## The two-layer split, applied to words

STE's method, never its aviation dictionary: a closed core the
adopter cannot extend casually, open technical classes the adopter
supplies, checkable writing rules, a conformance checker. Mapping:
the ratified glossary is the open domain class (Technical Names);
the dictionary is the closed general class; disjointness between
them is mechanical (alias-aware, surface forms never stems;
constraint-registry entry `glossary-dictionary-disjointness`,
enforced). The seed is harvested from this repo's own ratified
corpus - restriction of choice within a familiar register, never an
alien one.

## 🟢 Dictionary artifact - `specs/vocabulary/dictionary.yaml` (F1)

Set-ratified, one file: approved entries (`word` / `pos` / `gloss`),
banned entries (`word` / `use_instead` - every ban names its
replacement or the reason to delete), the function-word block (the
`pos: function` subset), the style principle (*restricted choice,
never unnatural construction*), the exempt ratchet list, and the
field registry (F2). Schema
`taskcontract/schemas/dictionary.schema.json`, born 1.0.0, packaged
in the wheel. Deltas ride the 0014 lanes: adding a word loosens the
gate -> full human lane; banning or removing tightens -> auto lane.
One word, one approved part of speech - tagging is dictionary
lookup, so shape rules stay decidable without NLP dependencies.
Seed provenance (2026-08-02): 999-word harvest from the seven
ready-green contracts, full-corpus closure, zero bans (census showed
no banned hits to collapse); `exempt` + `binds` entered during
self-adoption. The filename joins RESERVED_STEMS - never a term; the
glossary terms carry the `controlled-` prefix.

## 🟢 Field registry (F2)

Rows of (artifact-kind, field-path, text-type) - the door's sole
scope authority; anything unnamed is out of scope by construction.
Kit defaults, the six contract prose fields:

| Field | Text type | Profile |
|---|---|---|
| `intent` | descriptive | cap 25 words/sentence |
| `scope[]`, `non_goals[]` | descriptive | cap 25 |
| `decomposition[].unit` | procedural | cap 20, modal policing |
| `.done_means` | procedural | cap 20, modal policing |
| `.acceptance_sketch[]` | procedural | cap 20, verb-first |

Extensions are class-E deltas (full lane): the boundary itself is a
gated artifact. Triage ladder before any field enters: enum it if
enumerable (schema), ref it if it names a concept (glossary),
control it only if irreducibly prose - the dictionary is the last
resort, not the first tool.

## 🟢 `lang-check` door (F3 + F4)

`python -m taskcontract lang-check` - verdict-contract native (exit
`0`/`1`, `--json`, stable CLnnn codes), absence of dictionary =
green (adoption pace, vocab-check precedent; no exit-2 lane in v1 -
documented conformance delta). Zero-dep, stdlib only.

Tier-1 rules (one unit with the dictionary - the word list alone
never ships): CL006 unknown-word (skip classes: code spans, raw
`-`-prefixed flags, paths/identifiers, digit-bearing tokens,
all-caps acronyms, off-start capitalized proper names, glossary
phrases consumed longest-first), CL007 banned-word with the
replacement in the diagnostic, CL008 sentence caps by text type,
CL009 modal policing, CL010 pronoun-subject restriction, CL011
comparative-without-number, CL012 verb-first sketch items. Modals
and comparatives are rule-owned classes - approved by their rule
outside its red condition, never dictionary rows.

Integrity set: CL000 unreadable, CL001 schema, CL002 duplicates,
CL003 glossary/dictionary disjointness (alias-aware), CL004/CL005
`use_instead` reference integrity (no dangling refs, no ban
chains - repo artifact only; base bans are suggestion-only so a
base bump can never brick a consumer), CL013 base-shadowing at
info. Exempt contracts take prose findings at warning severity -
visible, never gating. The `--json` envelope carries the fixed
note: *form checked; meaning not checked*.

## 🟢 `lang-extract` (F5)

Report-only: tokenizes the registry-bound fields -> candidate words
with frequencies + banned hits + per-contract census. Writes
nothing; runs BEFORE the door arms - calibration before enforcement.
First run (2026-08-02, seven contracts): 999 candidates, zero
banned hits, census clean on bans and material on caps/verb-first -
which set the legacy disposition (F12).

## 🟢 Venue joins (F6)

The scaffolded CI workflow template carries the backstop step (one
chain-free segment); the kit's own committed workflow gains it in
the self-pin PR - the v0.8.0 pin predates the subcommand. The audit
reports `LANG-INVALID` (error) and `LANG-EXEMPT` (info); the skill
carries `/sdlc lang` + `/sdlc lang extract`; intake loops the door
like TCnnn (cap 5 - rewrite friction lands on the agent, never the
human).

## 🟢 Distribution - two layers (F7)

Machinery (schema, door, extractor, rules) rides wheel + skill.
Base layer - function words + bans only in v1, at
`taskcontract/data/base_dictionary.yaml` - rides the wheel, never
copied per repo (the agents/ anti-fork doctrine); domain layer
lives per-repo in `specs/vocabulary/`. The door unions
base ∪ domain ∪ glossary with local-glossary-shadows-base
precedence (CL013, info). Greenfield arms at its own pace: absence
is green, write contracts freely, extract-ratify-arm once corpus
exists. Base verb promotion waits on self-host evidence - nothing
enters core speculatively.

## 🟢 Trace-fed curation (F8)

Observed misreadings - M0 traces, verifier divergence, rework
tagging - become ban / word / rule deltas through draft -> ratify,
never auto-entry. Delta provenance records the observation (the
g8-escape pattern transposed): the dictionary's history shows it
grew from evidence, not taste. The convergence loop, ported to
language: every escaped ambiguity becomes a new mechanical check.
Mechanism rides M0; the discipline is normative now.

## 🟢 Measurement (F9 + F10)

The door's honest KPI is the escape rate among greens - contracts
that passed lang-check whose downstream failures trace to prose
ambiguity - expected to fall as bans accrete; numeric threshold
deferred to the Q4 clocks. Comprehension empirics are front-run and
say so: PL-PIPE.3 gains a comprehension eval family (paired prose
variants; G3 loop count, first-pass verifier rate, divergence
events); M0 trace tagging is the observational channel. A null
result re-prices one benefit; semantic diffs, machine-operability,
and mechanical checkability stand regardless.

## 🟢 Vocabulary drafts + register line (F11)

`controlled-dictionary` (disjoint_with: vocabulary-term) and
`controlled-field` (part_of: task-contract) are draft terms,
`sources:` naming this page; ratification stays the user's class-S
flip. CONVENTIONS carries the register line: controlled where
executed, free where deliberated.

## 🟢 Self-host adoption (F12)

The kit is its own proof instance: door armed 2026-08-02,
hard-at-intake for new and changed contracts. Census disposition:
zero banned hits; caps/verb-first material (~130 findings) -> the
six pre-arc contracts ride the `exempt:` ratchet (warnings, never
gating), paired with ledger entry `cl-legacy-tranche`. A contract
leaves the list at its next edit; new contracts never enter. The
`controlled-language` contract itself passed the door after
rewrite - the first hard-at-intake conformance.

## ⚪ Deferred, triggers on record

- **Base-layer verb promotion** - trigger: self-host evidence names
  the verbs that earn core status.
- **F-item region checking** (controlled islands in markdown) -
  trigger: the record-artifact answer proves insufficient.
- **Prompt lexicon** - trigger: a foundations-side PromptLang
  extension (PL owns form; the kit does not unilaterally gate a
  surface another standard owns).
- **Slot templates per field** (given/when/then shapes) - trigger:
  per-field escape evidence despite tier-1.
- **Greenfield day-one arming** - trigger: base-layer maturity.
