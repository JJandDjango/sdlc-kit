# Notes - what makes a feature, design or plan document good (2026-10-10)

Status: backlog. Material for the interview's materials step (O5) when
this becomes a feature. No contract, no ratified term. The shapes below
were agreed in talk (session 91), each on a filled-in page; none is a
format change yet.

Sources: eleven web searches on 2026-10-10 (listed at the end), and the
kit's own files as named.

## The idea

The goal, in the user's words: hold a proper understanding of a
codebase from its documents alone, without writing the code. The
understanding is needed at two moments: the plan review, before work
starts, and the PR review, after it.

The definition agreed: a document is good when a reader who holds only
the documents can judge a case they never name, and reaches the
author's verdict for the author's reasons.

A case the documents never name is the common one, since no document
lists every situation. Two examples:

- A sign says "No vehicles in the park". An ambulance arrives. The sign
  is silent, and a reader who knows why the rule exists lets it in.
- Session 90: the rule said a model is checked when its folder overlaps
  the feature's scope, and that a doubtful case counts as overlapping.
  No text named a folder written with no closing slash. The code read
  it as no overlap, nothing was checked, and the gate read `done`. A
  reader who knew the purpose (no model goes unchecked) would have
  called that wrong.

By document:

- The feature document passes when the reader rules on a behavior it
  never lists: wanted or not, in scope or not.
- The design document passes when the reader rules on a diff it never
  describes: right or wrong, and which rule it breaks.
- The plan passes when the reader rules on an event of the build it
  never names, and can say where Claude goes on and where it stops.
- A plan is itself such a case for the two documents above it: they
  pass when the reader can tell from them alone whether the plan is
  right.

Four other definitions were weighed and kept as means, not as the
definition:

1. The sentence: every statement passes a checklist (one reading, one
   point, checkable). The kit holds part of it in `lang-check`.
2. The trace: every need runs to a design statement, a test and a
   signature.
3. The reader's outcome: a named reader can find, understand and use
   what the document holds.
4. The decision: the reader makes the one decision the document serves
   with no author present.

The reader, ruled by the user: a reader with no context. A new session
of an LLM is that reader, a new developer is, and so is the user at a
review. Claude's reading of "no context": the reader knows software in
general and nothing of this project, its domain, its code, its history
or the session that wrote the document. Each field in the findings
below names its reader, and this is the kit's.

## The rules that follow

- The page stands alone. It leans on no session memory and no earlier
  talk, and what it needs from another page it names by path. Help
  with the domain stands in the page.
- Purpose at every level. A header gives the path down to the feature
  (project, area, feature), each line with its purpose in one sentence.
  When the feature's purpose cannot settle a case, the reader steps up
  one line.
- The path only, never the sibling features. The project and area lines
  are copied from one home, never typed again in each document.
- Layers. A reader can stop after any section and hold a true picture.
  The first three sections fit one screen.
- One worked example, a single story from start to finish.
- What stays out, each item with the reason it was left out.
- Hard cases already ruled, each with its reasoning, so the reader sees
  how to rule on the next one.
- What is not known is marked as not known.
- Each word is defined where it first stands, then listed.
- Each fact stands once. The plan holds only what is true of its
  session and points to the design for the rest.
- A shape is agreed on a filled-in page. The bare section list confused
  the talk, and each filled-in page was agreed in one reply.

## The three documents

| Document | The question it answers | Written | Lives |
|---|---|---|---|
| Feature | What do we want, and why? | once a feature | for good |
| Design | What shape does the solution take, and why that shape? | once a feature | for good, read at PR review |
| Plan | What happens in this one session, and where is the user asked? | once a session | until the session ends |

The user ruled: design and plan stay separate, and the plan is thin. A
plan is tied to a session by the user's standing rule; that it has also
meant one unit is habit.

## The shapes agreed

Feature page, a header and nine sections:

1. The point: three sentences on what changes, for whom, why now.
2. The problem: today's behavior, with one real instance.
3. Purpose and end state, closing on the one sentence to rule from.
4. One worked example, before and after.
5. What it must do: the checks, each a statement a test could hold.
6. What stays out, each with its reason.
7. Hard cases, already ruled.
8. What we do not know.
9. Words.

Design page, a header (with a line naming the feature page it answers)
and eleven sections:

1. The approach, in three sentences.
2. The parts: each part, its one job, and whether this change touches
   it.
3. The worked example, traced through the parts.
4. Rules that must always hold.
5. What a diff may touch, and what it must not.
6. Choices, and what was rejected.
7. Hard cases, already ruled.
8. Proof: each check with its test.
9. Unknowns, risk and cost.
10. Build order: the units, each with its done-means sentence.
11. Words.

Plan page, a header (with a line naming the session's unit) and ten
sections:

1. The deliverable, in one line.
2. Where this sits: which unit of how many, and what is built.
3. The steps, each with who does it.
4. Where Claude stops for the user.
5. Where Claude goes on alone, and by what rule.
6. Rulings needed with this approval, each with a recommendation.
7. What could go wrong, already ruled.
8. This session's cost, with its basis.
9. Not in this session.
10. Words, only those the two pages above do not define.

Sections 4 and 5 of the design page are the reviewer's list at PR
review. Sections 3 and 7 of the feature page, 6 and 7 of the design
page, and 5 and 7 of the plan page carry the definition.

## What the kit holds today

- The feature document's format stands under ADR 0029, amended by 0033
  to 0036, and ADR 0037 split it into a requirements document and a
  design document.
- The requirements document's headings (read from
  `docs/features/g1-requirements-spec.md`): Statement, Description,
  Background, Success criteria, Non-goals, Prerequisites, Acceptance
  criteria, Decisions and open questions, Notes, Appendix (Gherkin,
  Terms). By its headings it holds no purpose sentence to rule from, no
  worked example and no ruled hard cases.
- The design document's headings (read from
  `docs/features/g1-requirements-spec.design.md`): Proposed solution
  (Scope, Out of scope, Interfaces, Sources, Constraints, Units,
  Order), Risks and cost, Consult cases, Decisions and open questions,
  Traceability, Notes, Appendix. Interfaces runs 234 lines. By its
  headings it holds no picture of the parts, no worked example and no
  list of rules that must always hold.
- G1.3 is the human review of a feature's criteria for completeness and
  ambiguity (`docs/gates.md:152`); its 11 items land with `s3-review`.
- `lang-check` holds the sentence. The Traceability section, the
  `Contract:` trailer and `scope-check` hold the trace.
- The plan's fixed shape stands in `STATE.md`, Standing practice, first
  entry: the deliverable, an Overview, Terms, the steps, the rulings,
  the cost, the deferred list. New on the plan page: the header, and
  sections 4, 5 and 7 as headings of their own.
- The tree holds no area level: features stand under gates.

## Findings from other fields

| Field | What it holds a good document to |
|---|---|
| Software design docs (Google) | Goals, and non-goals that could reasonably have been goals. Alternatives, each with the trade-off that rejected it. The format is left loose. |
| Systems engineering (ISO/IEC/IEEE 29148, INCOSE) | Quality a statement and a set: unambiguous, singular, verifiable, understood with no other information. |
| Amazon (the six-page narrative, the PR/FAQ) | Narrative prose, six pages at most, the customer's words, no jargon. The hard questions answered in advance. Ten or more drafts. |
| Software architecture (Clements and others, "Views and Beyond") | Seven rules, among them: write for the reader, state each fact once, record rationale, review for fitness of purpose. |
| Medical devices (FDA, 21 CFR 820.30) | Needs turned into measurable terms. Outputs carry acceptance criteria. Signed, dated approval. A design history file as the record. |
| Plain language (ISO 24495-1:2023) | Four principles for the intended reader: relevant, findable, understandable, usable. |
| Documentation theory (Diataxis) | Four kinds kept apart: tutorial, how-to, reference, explanation. |
| Code review research (Bacchelli and Bird, 2013) | Understanding the change is the key part of a review, and tools do not supply it. |
| Military (commander's intent, bottom line up front) | Purpose and end state stated, so a subordinate acts rightly when the plan fails. The main point first. |
| Product (the Shape Up pitch) | Problem, appetite, solution, rabbit holes, no-gos. The solution at the level of parts and their relations. |
| Spec-driven development (2026) | The spec wins a disagreement with the code. No record yet of which spec produced which behavior. |

Where the fields agree: each states the purpose first and says what is
out; each that reviews work records the why; each names its reader. They
split in two: the regulated fields judge the text (definitions 1 and
2), and the narrative fields judge the reader (3, 4 and the one
agreed).

Limits: the seven architecture rules are from Claude's memory, since
the search found the section and not its text; both ISO standards were
read through summaries; no study was found of whether people understand
agent-written code from its specs alone.

## Open

- Does the area level of the header become a level of the tree?
- How the test is sat. A fresh-context agent is a reader with no
  context, so it can sit the test; the neighbor is `document-split`'s
  later feature, Claude's review of a design in a fresh context.
- The way into the kit. The plan's shape is standing practice, and the
  user ruled (session 91) that the next session's plan, for
  `s3-review`, is the first written in the plan page's shape. The
  feature and design formats stand under ADRs, so a change to either is
  a feature of its own, through the interview; it is parked.
- The example on the pages below is the user's idea of 2026-10-07 (the
  tree names no feature in flight), still not filed as a feature. A
  test labelled SC2.3 (`tests/test_tree_before_intake.py:590`) pins
  today's order by id; its signed sentence was looked for in two
  contracts and not found.

## Appendix: the three filled-in pages

Each page is an illustration, unsigned. The numbers were measured on
main at `532f368`; the checks and rulings are Claude's proposals.

### Feature page

```
Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     The tree: the exact state of every feature's work, in one printout.
Feature  Unfinished first: the tree opens on the work that is not done.
```

1. The point. The tree will open on the features that are not done.
   Today the one feature being built starts at line 589 of 1,545, below
   eight finished ones. The tree is opened to see where the work
   stands, so the first screen should say it.
2. The problem. The tree prints the project's own gate block first,
   then every feature in alphabetical order. Its first feature line is
   `controlled-language`, finished long ago. The feature in flight,
   `g1-requirements-spec`, is the ninth.
3. Purpose and end state. The tree exists to answer "where does the
   work stand?" at a glance. When this is done, whoever opens the tree
   sees each unfinished feature and its state without scrolling.
   Finished work stays in the tree and never stands in front of
   unfinished work. When in doubt: unfinished before finished.
4. One worked example. Before: line 1 reads `gates/G0 ... [done]`, line
   5 `controlled-language ... [done]`, and 588 lines stand above
   `g1-requirements-spec`. After: the first feature line reads
   `g1-requirements-spec ... [waiting on a seat]`, the parked
   `glossary-alias-disjointness [to do]` comes next, then the 18
   finished features.
5. What it must do. C1: every feature not done prints before every
   feature done. C2: among features not done, one in flight prints
   before one not started. C3: no line is lost; the tree holds the same
   lines in a new order. C4: when every feature is done, the tree
   prints as it does today.
6. What stays out. Hiding or folding finished features: the tree
   promises the state of every feature. A new banner line for the
   current feature: one ordering rule does the job with no new kind of
   line. Any change to how a state is worked out: this feature moves
   lines and never changes what they say.
7. Hard cases, already ruled. Two features in flight: both print first,
   alphabetical between themselves, since the purpose takes no side
   between two unfinished. A feature waiting on a signature: in flight,
   since it is the work that needs the user. A parked feature: after
   features in flight and before finished ones.
8. What we do not know. Whether the gate block (four lines, `gates/G0`)
   stays first; the user's note named it as the problem line. Whether
   the live pane shows the same order as the printout.
9. Words. Tree: the kit's one printout of every feature and its state.
   In flight: started and not done. Done: every unit closed. Parked:
   stopped on the user's word, not started.

### Design page

```
Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     The tree: the exact state of every feature's work, in one printout.
Feature  Unfinished first: the tree opens on the work that is not done.
Answers  the feature page above
```

1. The approach. The tree's order is decided in one place: `build`, at
   `taskcontract/tree.py:322`, sorts the features by id. The change
   gives that sort a new rule: in flight, then not started, then done,
   with id breaking ties. Nothing else in the tree changes.
2. The parts. `tree.py`, `build`: puts every line in print order;
   changes, one sort. `tree.py`, `STATUSES`: names the six states a
   line can hold; read only. `tree_view.py`: prints the tree;
   untouched. `pane.py`: shows the live pane; untouched. `progress.py`:
   reads the tree to find the current task; untouched. All three
   readers take their lines from `build`, so one change moves all
   three (read from their imports, not run).
3. The worked example, traced. `build` reads the 20 features and works
   out each one's state (lines 316 to 320). At line 322 it sorts by id,
   so `controlled-language` leads. Under the new rule
   `g1-requirements-spec` leads, `glossary-alias-disjointness` follows,
   then the 18 done features by id. The gate block is added before the
   features (lines 312 and 326) and does not move.
4. Rules that must always hold. R1: a line's words never change, only
   its position. R2: the units inside a feature keep their order. R3:
   the same state always prints the same order; id breaks every tie.
5. What a diff may touch. May: the sort in `tree.py`, tests under
   `tests/test_tree*.py`, USAGE's tree section, the CHANGELOG. Must
   not: `pane.py`, `tree_view.py`, `progress.py`, anything under
   `specs/`. A diff that touches these owes a reason.
6. Choices, and what was rejected. Reorder once in `build`; rejected:
   reorder in each reader, three places to keep equal. Three groups by
   state; rejected: order by latest activity, which shifts on every
   record and is hard for a test to pin.
7. Hard cases, already ruled. A feature that reads `failed` or
   `blocked`: in flight. A feature with a document and no intake yet:
   not started. Two ids that differ only in capitals: today's tie
   order, which a test pins.
8. Proof. C1, C2, C3: one new test each. C4: today's order tests on a
   fixture where every feature is done. Changed or retired:
   `tests/test_tree.py:201` and `tests/test_tree_before_intake.py:590`
   pin today's order; two more follow it and need a look.
9. Unknowns, risk and cost. The SC2.3 question (Open, above). Cost: one
   unit, about 0.5 million agent tokens, on `d4`'s recorded 561K
   (session 81), the nearest code unit in size.
10. Build order. One unit. Done means: the tree prints each feature not
    done before each feature done.
11. Words. Sort rule: what a list is ordered by. Group: in flight, not
    started, or done.

### Plan page

```
Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     The tree: the exact state of every feature's work, in one printout.
Feature  Unfinished first: the tree opens on the work that is not done.
Unit     the only one: the new order in `build`
```

1. The deliverable. By the session's end the tree prints unfinished
   features first, on main, with a passing independent grade.
2. Where this sits. The feature has one unit and nothing is built yet.
3. The steps. (1) Claude opens a work branch and pushes the plan. (2)
   The drafter, an agent that writes tests and never the code, drafts
   the test list from the design's Proof section and proves each test
   fails today. (3) The user approves the test list, shown in chat. (4)
   The developer, an agent that writes the code and never opens the
   tests, makes the tests pass. (5) Claude runs the whole suite. (6)
   Two-Key, an agent that grades the unit from its own runs, returns
   PASS or FAIL. (7) Claude opens the PR after green CI and a PASS; the
   user reviews it and says merge. (8) Claude writes the wrap in its
   own PR after the merge.
4. Where Claude stops for the user. Twice: the test list and the PR. A
   third stop only if something would change signed text, a ratified
   term or an ADR.
5. Where Claude goes on alone, and by what rule. The unit's commits,
   USAGE sentences that restate the design, the wrap's merge. The rule:
   Claude builds on its own reading and lists it at the top of the PR;
   if the reading would change signed text, Claude stops.
6. Rulings needed with this approval. If today's order by id is signed
   text, Claude stops and the document is amended first (recommended).
   The gate block stays first in this unit (recommended).
7. What could go wrong, already ruled. Two-Key fails a round: one
   narrow fix round, tests first, on the user's approval; after a third
   failure Claude stops. The developer proposes a shortcut: it is
   tested against the done-means sentence, and a path that reaches
   "done" another way is a defect. An older test fails that the plan
   never named: if it pins today's order it changes and the user is
   told; if it pins anything else the build is wrong.
8. This session's cost, with its basis. About 0.5 million agent tokens
   and two touches from the user, on `d4`'s recorded 561K (drafter
   213K, developers 94K and 75K, Two-Key 179K). A lost round adds about
   300K.
9. Not in this session. Moving the gate block. Hiding finished
   features. Any change to the live pane's look.
10. Words. Unit: one buildable slice of a feature. Done means: the one
    sentence a unit must make true. Suite: every test in the kit, run
    together.

## Sources

- Google design docs: https://www.industrialempathy.com/posts/design-doc-a-design-doc/
- INCOSE guide, summary sheet: https://www.incose.org/docs/default-source/working-groups/requirements-wg/guidetowritingrequirements/incose_rwg_gtwr_v4_summary_sheet.pdf
- INCOSE characteristics: https://www.incose.org/wp-content/uploads/legacy/presentation/IS2018-pdf/6-6-1.pdf
- Amazon PR/FAQ: https://www.koji.so/docs/working-backwards-pr-faq-guide
- Amazon narratives: https://commoncog.com/product-development-iterated-taste/
- Views and Beyond: https://www.pearson.com/en-us/subject-catalog/p/Clements-Documenting-Software-Architectures-Views-and-Beyond-2nd-Edition/P200000000186/
- 21 CFR 820.30: https://www.law.cornell.edu/cfr/text/21/820.30
- FDA design controls deck: https://fda.gov/media/116762/download
- ISO 24495-1, summary: https://www.iplfederation.org/the-iso-plain-language-standard-part1
- Diataxis at Canonical: https://ubuntu.com/blog/diataxis-a-new-foundation-for-canonical-documentation
- Bacchelli and Bird, 2013: https://web.eecs.umich.edu/~weimerw/2018-481/readings/codereview.pdf
- Commander's intent: https://en.wikipedia.org/wiki/Intent_(military)
- Bottom line up front: https://en.wikipedia.org/wiki/BLUF_(communication)
- Shape Up, the pitch: https://basecamp.com/shapeup/1.5-chapter-06
- Spec-driven development: https://arxiv.org/pdf/2609.00252
