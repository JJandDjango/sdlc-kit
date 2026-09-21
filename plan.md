# Plan - Session 34 (2026-09-20) - g0-declaration to release

Where things stand: branch `session-33-g0-declaration`, unpushed over main
(`5e26c1b`, kit 0.13.0). The OPEN at r5 is ruled: take the proposal, and the
fix gets its own unit rather than d2, which already holds four checks in
three sketches. The request is signed at r6, ADR 0030 stands, and the
contract is ready-green with eight units. The goal is the whole request
delivered and released, so a consumer on 0.14.0 gets a door that checks
something and an audit that reads a parked contract correctly.

Verified so far: d0 (`1ad319a`) and d1 (`6939082`), each PASS by an
independent Two-Key round. Receipts at d1: suite 285 green, thirteen
contracts ready-green, `/sdlc audit` clean, the language door at zero for
this contract, schema 1.4.0, the TC017 string byte-equal to the request. The
editable install is live (`sdlc-taskcontract` from the working tree), so a
standalone audit reads the working tree, not a pinned copy.

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
3. d2 `d2-roster-required`. `confirmation_join` returns TC018 when
   `intake-seat` is absent or draft, at the ready profile only; the G0 gate
   page. The joins fire only for `specs/<id>/contract.yaml`
   (`taskcontract/checker.py:142`), and the audit and init tests build that
   shape in a tmp repo with no roster, so d2 seeds a ratified `intake-seat`
   in those helpers: that is SC2.3, behavior exactly today's with the roster
   ratified. d2 also clears three of d1's advisories, all of them the same
   sentence in three places, that `entities:` is optional:
   `docs/gates/G0-planning-intake.md:85` (the authoritative field table,
   which `docs/task-contract.md:13` defers to), `docs/vocabulary.md:63`, and
   the missing clause row in the G0.1 table at `docs/task-contract.md:27`.
   Two-Key.
4. d7 `d7-audit-parked-rule`. The parked rule reads TC003 present with every
   other error a declaration miss (TC017, TC018), and the parked finding
   names the misses. Two-Key.
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
   fail ready. Two-Key.
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
