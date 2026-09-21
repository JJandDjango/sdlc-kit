# Plan - Session 34 (2026-09-20) - g0-declaration to release

Where things stand: branch `session-33-g0-declaration`, unpushed over main
(`5e26c1b`, kit 0.13.0). The OPEN at r5 is ruled: take the proposal, and the
fix gets its own unit rather than d2, which already holds four checks in
three sketches. The request is signed at r6, ADR 0030 stands, and the
contract is ready-green with eight units. The goal is the whole request
delivered and released, so a consumer on 0.14.0 gets a door that checks
something and an audit that reads a parked contract correctly.

Verified: d0 (`1ad319a`), d1 (`6939082`), d2 (round 5, `c1af342` through
`d420f80`), each PASS by an independent Two-Key round. d7 is committed at
`8ce629e` with `ff55f5b`: its three sketches PASS and `done_means` holds,
but its verdict stands FAIL on stale prose in this plan's own files, which
the blocking-bar fix below settles. Receipts at HEAD: suite 292 green,
thirteen contracts ready-green, `/sdlc audit` clean, the language door at
zero for this contract, `vocab-check` green at 18 terms and 8 constraints,
schema 1.4.0. The editable install is live (`sdlc-taskcontract` from the
working tree), so a standalone audit reads the working tree, not a pinned
copy.

## The blocking bar (apply first, next session)

Session 34 spent seven FAIL verdicts and about 1.5M subagent tokens, and
not one of them was a code defect: every sketch passed on its first round.
Each FAIL was a sentence somewhere else stating a rule the unit had
retired. The kit describes its own rules on about forty surfaces, and each
verifier round searched where the last had not, so the loop had no fixed
point. Three corrections, to apply before d3:

1. **Blocking** means a sketch fails, `done_means` is false, a path sits
   outside scope, a trailer is missing, or a *shipped* surface states
   something false: code, the schema, `docs/`, `USAGE.md`, `CHANGELOG.md`.
   Files regenerated at every wrap (`plan.md`, `plan.workflow.json`,
   `STATE.md`) are session scratch and do not gate a unit; they are fixed
   at the wrap, which is where they are rewritten anyway.
2. **The repo-wide stale-claim sweep runs once, inside d6**, where the
   release lives, not once per unit.
3. **The focus list per unit is its own sketches, fixed.** Session 34
   widened it every round, raising a bar and then failing it.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the units read left to right, human gates dropping onto
it from above, an exception lane below for a Verifier FAIL). Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed. Every code unit lands as one commit,
Developer then Verifier (Two-Key). The unit graph is computed
(`python -m taskcontract graph`), never committed.

## Steps

1. Amend the request and re-intake. The OPEN's answer written into the
   decision log; SC4.3 added under SC4 (`/sdlc audit` reads a parked
   contract that declares neither input as CONTRACT-PARKED at exit zero,
   and the finding names the missing declarations); `skills/sdlc/audit.py`
   added to scope; unit `d7-audit-parked-rule` added after d2, and d6
   depends on it; revision row r6. Then `/sdlc intake g0-declaration`
   re-derives the contract and re-stamps the appendix. Receipt: the
   contract validates ready-green and reads zero at the language door.
   No new ADR: 0030 carries the ruling and this is its consequence.
2. d1 `d1-schema-entities`. DONE, PASS at `6939082`. The WIP `3a3261a` was
   lifted out of the branch, so no unverified commit survives.
3. d2 `d2-roster-required`. DONE, PASS at round 5: `c1af342`, `b41229d`,
   `0851bb0`, `5abd3d0`, `d420f80`. Five rounds, and every failure was the
   same class: a surface still stating the rule the unit retired, each
   found where the last search had not looked (`docs/`, the G0 deep page,
   the schema's own `description`, a fixture's intent). The lesson, now
   standing practice for d3 to d6: run `git grep` for the retired claim
   across every tracked file while building the unit, not after the
   verifier fails it. Two writes landed in the spec channel beyond the two
   the request budgeted, `specs/vocabulary/constraints.yaml` and the
   class-S edit to `specs/vocabulary/task-contract.yaml`; the verifier
   ruled both legitimate corrections rather than scope creep. They trip
   different branches of the write-guard, the registry-file branch and the
   ratified-term branch, so the PR names them on two separate grounds.
4. d7 `d7-audit-parked-rule`. DONE in substance at `8ce629e` with
   `ff55f5b`: the parked rule reads TC003 present with every other error a
   declaration miss (TC017, TC018), the parked line names them, and the
   verifier built all four cases itself in a temp repo and confirmed the
   exact output lines and exit codes. Both rounds failed only on stale
   prose in `STATE.md` and `plan.workflow.json`, both fixed at this wrap.
   Under the blocking bar above, d7 is PASS; re-run one round next session
   to record it that way.
5. d3 `d3-scaffold-comment`. The skeleton names `entities` in a note line
   and sets no value. Two-Key.
6. d4 `d4-intake-flow`. Intake checks the roster before authoring and stops
   with the verbatim line; it always writes `entities`, and writes `[]` only
   on the PO seat's confirmed answer. This clears d1's advisory that
   `skills/sdlc/flows/intake.md:21` still says to omit the field when
   nothing matches, which would author contracts that fail ready on TC017.
   Two-Key.
7. d5 `d5-init-seeds-roster`. Greenfield init records the seats and writes a
   ratified `intake-seat`; brownfield init reports the need and names the
   command. Two-Key.
8. d6 `d6-adoption-and-release`. Hook tests for the unlock and the re-lock;
   USAGE marks flip green; kit 0.14.0. d6 also clears the five USAGE
   advisories d0's verifier raised: (a) section 8's worked example shows a
   contract with no `entities:`; (b) the green intake sentences near lines
   149-160 imply intake runs without a roster and omit `entities` from the
   fields intake authors; (c) "add the field, and it locks" is false read
   alone, so fold the both-doors condition into it; (d) the new section
   names greenfield init and omits the brownfield half; (e) section 9
   Troubleshooting needs TC017 and TC018 rows beside TC016. d1's verifier
   raised (a) again from the other side: the worked example at
   `USAGE.md:478-524` is the kit's flagship ready exemplar and would now
   fail ready. d2's verifier added the one that would otherwise slip: two
   sentences marked 🟢 state the retired rule, `USAGE.md:384-385` ("leave
   the seat term unratified and the check stays off") and `USAGE.md:448`
   ("a draft term or no term leaves the check off"). They read as honest
   only because the 🔴 paragraphs beside them mark 0.14.0 unreleased, so
   flipping the marks without rewriting them would publish both as green.
   d6 also takes `docs/gates/G0-planning-intake.md:114`, where G0.2's
   Lifecycle bullet still says "per-target elsewhere" although TC017 lives
   in the schema and fires in every tree, even outside one. And from d7:
   the parked line names rule ids only, so the TC017 and TC018 remedy text
   no longer reaches a consumer reading a parked contract's audit; section
   9 must let those ids resolve to their remedies. Two-Key.
9. Release, on the user's word: PR, merge by merge commit, tag v0.14.0, the
   self-pin in `.github/workflows/sdlc.yml` bound to this contract. Then
   STATE.md regenerated and this plan struck through.

Carried, unordered and not this session: `derived-language`,
`feature-document`, `spec-doc-type`; the demo intake in a sandbox consumer;
wave B (`playbook-loop`, V1-V6); 5b (graph emits Archify), unratified; the
engine's G4.6 finding once it has a request.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer on every commit that touches a non-free path; one
decision per message, each with a recommendation; approval content shown in
chat in full.
