# Plan - Session 33 (2026-09-20) - Four requests, the door first

Where things stand (2026-09-20): kit 0.13.0 released (tag at 210d476, main at
5e26c1b after PR #43). Session 32 ratified the feature document's format and
its definition of done (ADR 0029) and settled the Google Docs look. Since
then the pilot consumer, ImSim Engine, wrote the first spec doc by hand and
sent three requests through the return channel; with the kit's own, four
wait in the inbox, all in 0029's format. Order agreed with the user,
2026-09-20: the door that passes on nothing first, then the language
boundary that the two document contracts need, then the documents.

## The four requests

1. `g0-declaration` (engine, 09-20): G0.2 reads `entities:` and G0.3 reads a
   ratified `intake-seat`; both inputs are optional, so a contract passes
   both green having checked nothing. At ready, `entities:` must be present
   (an empty list allowed and meaningful) and a ratified seat roster must
   exist. Draft unchanged. Adoption needs no re-intake; USAGE says so.
2. `derived-language` (engine, 09-19): the controlled language binds derived
   text only (the contract, the Gherkin), never authored sections; intake
   loops the door beside the validator; a check id at the head of a sketch
   survives the verb-first rule; a contract names its source document.
3. `feature-document` (the kit's own, 09-18): units F1-F6 implement 0029 in
   the template, the flows, readiness and intake.
4. `spec-doc-type` (engine, 09-19): the spec doc, cut from the engine's
   feature map; amends 0028's non-goal.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: one lane of plan steps read left to right, human gates
dropping onto it from above, an exception lane for parked contracts and
Verifier fails below, five guided views starting with "Where we are"). Render
and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed. Every code unit lands as one commit,
Developer then Verifier (Two-Key). The unit graph per contract is computed
(`python -m taskcontract graph`), never committed.

## Steps

1. `g0-declaration`. (a) Read the two findings in the engine's return
   channel. (b) The engineer half of the request, one decision per message:
   scope, out of scope, units, sequencing, the schema delta (`entities`
   loses `minItems: 1`; version bump and CHANGELOG delta note), the two new
   diagnostic ids. (c) An ADR under 0014's lane (an enforcement change).
   (d) `/sdlc intake g0-declaration` to ready-green; sketches verb-first
   with the check id trailing until step 2 lands. (e) Units, one commit each
   with the `Contract:` trailer, Two-Key by a workflow verifier. (f) The
   kit's own contracts and vocabulary must pass the new door first: every
   ready contract declares `entities:`, `intake-seat` stays ratified.
   (g) PR, then on the user's word: merge, tag v0.13.1 or v0.14.0 (decided
   at intake by the schema delta), self-pin.
2. `derived-language`: same discipline. Its SC3 (the token rule) unblocks
   leading check ids for steps 3 and 4.
3. `feature-document`: fold the queued 0029 amendments into the note and the
   ADR first (state in revision rows, no Statement heading, three-column
   revision table, no owner tags, a spec doc is living); then intake and
   units F1-F6. The styled rendering joins as its own small request.
4. `spec-doc-type`: intake from the engine's request; the engine's feature
   map is the worked example.
5. Carried, unordered: the demo intake in a sandbox consumer; wave B
   (`playbook-loop`, V1-V6); 5b (graph emits Archify), unratified; the
   engine's G4.6 finding (the write-guard binds an editing-tool list) once
   it has a request.
6. Session close: STATE.md regenerated, this plan struck through.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + git commit -F; Two-Key on every code unit; a
`Contract:` trailer on every commit that touches a non-free path; one
decision per message, each with a recommendation; approval content shown in
chat in full.
