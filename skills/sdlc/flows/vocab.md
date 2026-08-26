---
name: sdlc-flow-vocab
description: The Vocab flows of /sdlc - List (computed listing), Add (draft term skeleton), Extract (draft terms from declared surfaces); ratification stays human.
---

<purpose>
The Vocab flows of the `/sdlc` skill: shared language as executable
definitions (ADR 0017). One term per file at
specs/vocabulary/{term-slug}.yaml, the filename is the stable ID, and
G0 joins contract `entities:` refs against ratified terms. Dispatched
by {skill-dir}/SKILL.md on `/sdlc vocab`, sub-dispatched on the next
argument to List, Add, or Extract; its constraints and criteria bind
here. {skill-dir} is the directory holding SKILL.md.
</purpose>

<instructions>
L1. LIST - one Bash call: `python -m taskcontract vocab-list`. REPORT stdout verbatim - the listing is computed from the term files at call time; there is no stored index to trust or drift.

VA1. ADD - one Bash call: `python -m taskcontract vocab-add {slug}`. The skeleton is deliberately red - VT002 trips on the TODO definition - and born `status: draft`.

VA2. REPORT stdout (the created path + the vocab-check loop line). On failure REPORT stderr verbatim; for a missing module also offer the pip install command from SKILL.md's context section.

X1. SURFACES - collect the declared surfaces to extract from: the invocation text after `extract`, or ask the user (API baselines, schemas, domain types, docs). Extraction reads ONLY what the user declares - never sweep the repo.

X2. DRAFT - read the surfaces and identify candidate terms: recurring nouns, closed value sets, implicit relations. Cap one run at 5-15 candidates - vocabulary grows at the rate work demands it (0017 V7a). For each candidate: scaffold via `python -m taskcontract vocab-add {slug}` (one Bash call per term), then author definition, kind, relations, values as the surface evidences them, and set `sources:` to the exact surface paths read. Status stays `draft` - extraction NEVER ratifies.

X3. LOOP - one Bash call per iteration: `python -m taskcontract vocab-check`. Fix exactly what each VTnnn diagnostic names. Cap at 5 iterations; if still red, REPORT the remaining violations and return to the conversation.

X4. REPORT - the vocab-list output, then one line stating the handoff: ratification is the user's flip of `status: draft` to `ratified` per term (a class-S edit; the PR merge is the interim approval record).
</instructions>
