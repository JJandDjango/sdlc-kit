# Documentation system (Cairn)

This project's documentation is **pace-layered**: each file changes at its own
rate under a fixed contract, so fast edits never tear slow truth. Read
`THEORY.md` -> `MAP.md` -> `STATE.md` (~2-3k tokens) to know *what, how, and
where*; descend into `decisions/` and `docs/` only on demand.

Scaffolded by **Cairn** - a durable documentation spine for any project.

## The six strata

| Stratum | Question it answers | Budget | Update trigger | Mode |
|---|---|---|---|---|
| `THEORY.md` | Why exist? What must stay true? | <=1 page | purpose / invariants change | hand-edited, rare |
| `MAP.md` | What are the pieces & how connected? | <=2 pages | Component add / remove / rewire | hand-edited |
| `decisions/` | Why done this way? | <=1/2 page each | a new significant decision | **append-only, never edited** |
| `docs/` | How does each piece work? | mirrors structure | internals change | authored on touch (or generated) |
| `STATE.md` | What's in flight now? | <=1 page | every session end | regenerated, disposable |
| `CONVENTIONS.md` | How do we do things here? | <=1 page | a rule is adopted / revised / retired | hand-edited (entries link ADRs) |

## Day 2 - the routine

Each file has exactly ONE trigger - touch it only then, and only that file. This is
the drill between the strata table (the model) and the audit checklist (the proof).

| File | Touch it when... | How |
|---|---|---|
| `THEORY.md` | purpose or an invariant changes (rare) | Hand-edit in place. If the intent is still tagged `(inferred)`, confirm it and delete the tag. |
| `MAP.md` | you add / remove / rewire a Component | Update that Component's row (add / edit / delete). |
| `decisions/` | you make a choice a future you would question | Copy `ADR-template.md` -> `NNNN-short-title.md`; fill Context / Decision / Consequences. |
| `docs/<piece>.md` | you first work on a piece in depth | Author its page then - on first deep touch, not upfront. |
| `STATE.md` | the end of every work session | Overwrite it wholesale - it is disposable, your running handoff. |
| `CONVENTIONS.md` | you adopt / revise / retire a house rule | One line per rule, ADR-linked when significant; detail overflows to `docs/conventions/` pages. |

**If you keep only one rule:** decisions are append-only and `STATE.md` is
throwaway - everything else is edited in place, and rarely.

**Automating the routine:** `/cairn audit` checks the list at the bottom
mechanically (report-only; exit 1 on findings). `/cairn maintain` has your agent
walk this whole routine at session end - it touches MAP / docs / STATE grounded
in what actually changed, never THEORY, CONVENTIONS, or old ADRs, and leaves
every edit uncommitted for your review.

## Maintenance rules
- **ADRs are append-only.** Never edit one; supersede it with a new record (mark the old `superseded by NNNN`). Copy `decisions/ADR-template.md` to start a new record.
- **One diagram per project**, in `MAP.md`, at ~container zoom. Nothing deeper - it rots faster than you can maintain it.
- **`STATE.md` is disposable** - regenerate it at session end; never hand-patch it mid-session.
- **`CONVENTIONS.md` is an index, not an essay** - one line per rule (ADR-linked when significant); overflow lives in `docs/conventions/` pages. Inferred entries stay tagged `(inferred - confirm)` until a human confirms.
- **Definition of done includes the doc touch** - a change to a Component's responsibility updates its `MAP.md` row (and its `docs/` page if one exists).

## Audit checklist
Run `/cairn audit` to check every box below mechanically.
- [ ] ADRs are never edited; superseding records exist where decisions changed.
- [ ] Exactly one diagram in the project, located in `MAP.md`.
- [ ] `THEORY.md` <=1 page - `MAP.md` <=2 pages - each ADR <=1/2 page - `STATE.md` <=1 page - `CONVENTIONS.md` <=1 page.
- [ ] `STATE.md` was regenerated at the last session end, not hand-patched.
- [ ] Every `MAP.md` row links a `docs/` page or is marked "no doc yet".
- [ ] `THEORY.md` intent and `CONVENTIONS.md` entries are confirmed (no lingering `(inferred)` tags).
- [ ] Every `CONVENTIONS.md` entry's ADR link resolves to a current (not superseded) ADR.
