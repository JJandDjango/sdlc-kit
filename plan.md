# Plan - Session 36 (2026-09-21) - g0-declaration released

**Closed.** Every step is done: `g0-declaration` merged as PR #44 at
`1d306ea` by merge commit and is tagged `v0.14.0`; the self-pin rides PR
#45. The next session starts a new plan.

Where things stand: kit 0.14.0 is out. At the ready profile both G0
inputs are required declarations, `entities:` (TC017) and a ratified
`intake-seat` roster in a specs tree (TC018); the draft profile is
unchanged. All eight units passed Two-Key under the blocking bar, which
lives in the untracked verifier, `.claude/workflows/two-key-unit-verifier.js`.
d6, the release unit, passed in round 1 with the one repo-wide sweep. The
request ended at r8: d6's own sweep, run before the verifier, found two
`SKILL.md` lines outside scope stating retired rules, and the re-intake
added the file.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the units read left to right, human gates dropping onto
it from above, an exception lane below for a Verifier FAIL). Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Amend the request and re-intake.~~ Done at r6: SC4.3 and unit d7.
2. ~~d1 `d1-schema-entities`.~~ PASS at `6939082`.
3. ~~d2 `d2-roster-required`.~~ PASS at round 5, `c1af342` through
   `d420f80`; the two extra spec-channel writes, named in PR #44.
4. ~~d7 `d7-audit-parked-rule`.~~ PASS at round 3, `8ce629e` with
   `ff55f5b`.
5. ~~d3 `d3-scaffold-comment`.~~ PASS at `ee3ff6d`, after r7 ruled SC4.2.
6. ~~d4 `d4-intake-flow`.~~ PASS at round 2, `5114f74` with `13f0ca5`.
7. ~~d5 `d5-init-seeds-roster`.~~ PASS at `964f156`.
8. ~~d6 `d6-adoption-and-release`.~~ PASS at round 1, `cf518e5`, after
   r8 (`3ad6cb0`) brought `skills/sdlc/SKILL.md` into scope. Two of its
   four advisories closed at the self-pin; two wording nits stay open in
   `STATE.md`.
9. ~~Release.~~ PR #44 merged at `1d306ea`, tag `v0.14.0`, self-pin
   `af9e587` on PR #45 with this wrap.

Carried, unordered: `derived-language`, `feature-document`,
`spec-doc-type`; the demo intake in a sandbox consumer; wave B
(`playbook-loop`, V1-V6); 5b (graph emits Archify), unratified; the
engine's G4.6 finding once it has a request.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer, alone in the final paragraph, on every commit that
touches a non-free path; one decision per message, each with a
recommendation; approval content shown in chat in full.
