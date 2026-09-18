# Plan - Session 32 (2026-09-18) - The feature document, then the release

Where things stand (2026-09-18): kit 0.13.0 released. PR #40 (the
interview skill, ADR 0028) merged at a0a9010, PR #41 (wave A of the
playbook guardrails) at 210d476, tag `v0.13.0` there; the self-pin PR #42
merged at f6fb265, main's tip. Session 32 started at the top of the
workflow: the user's seventeen-section work format was reconciled with
the kit's intake-ready template, call by call, and the definition of done
for a feature document was ratified. The record is
`NOTES_feature-document_2026-09-18.md`; the ruling is ADR 0029. Branch
`session-32-feature-document`, rebased on main, PR #43. Next: the
contract that implements 0029, its request written by hand.

## What 0029 changes

One format, eighteen sections, a seat boundary (request above the line,
solution below), an owner-and-kind tag on every section, two lists per
half (whitelist proved, blacklist recorded), three levels of proof
(criterion, signed checks with ids, derived Gherkin), derived blocks
read-only and stamped, measurement as a revision row, and done defined:
ready when intake can derive a ready-green contract without a new
question to the request half; zero OPEN marks at ready; an undecidable
question parks; a surprise in development enters the document first.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: one lane of plan steps read left to right, human
gates dropping onto it from above, an exception lane for parked contracts
and Verifier fails below, phases per release, five guided views starting
with "Where we are"). Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed. Every code unit lands as one commit,
Developer then Verifier (Two-Key). The unit graph per contract is computed
(`python -m taskcontract graph`), never committed; the diagram is the
session-level view.

## Steps

1. ~~Feature document format and definition of done: the six
   reconciliation calls, the tag rule, "Measured:" rows, the ten checks,
   the surprise loop; the note and ADR 0029; `NOTES_*.md` a free path.~~ -
   done, 2026-09-18 (d116ec8, bb725e3, d12f2c7 on
   `session-32-feature-document`).
2. ~~The release, on the user's word: merge #40, then #41; `git tag
   v0.13.0` at the merge; the self-pin PR moves the kit's own workflow
   ref and USAGE's install example to the tag and dates CHANGELOG's
   0.13.0 heading; delete both branches, sync main.~~ - done,
   2026-09-18: #40 at a0a9010, #41 at 210d476 (tagged), self-pin #42 at
   f6fb265. One lesson: `gh pr merge --delete-branch` deletes the base
   through the API, which closes a stacked PR instead of retargeting it;
   #41 was reopened by restoring the ref for a minute, retargeting, and
   deleting again. Then `session-32-feature-document` rebased onto main,
   PR #43 (the note, ADR 0029, the config line, this plan); merge on green.
3. Feature-document contract: the request is the first document written
   in the ratified format, by hand (the skill still writes the old shape
   until F1 and F2 ship); `/sdlc intake feature-document` to ready-green
   (ADR 0029 cited). Proposed units, the
   diagram's cards: F1 template (reorder, tags, status line, Terms,
   numbered revisions, three sections dissolved); F2 the sections flow
   follows the order; F3 readiness five rules to ten plus the stale stamp;
   F4 intake assigns every check to one unit, an orphan check or empty
   unit is a finding, an OPEN question parks; F5 Gherkin derived from
   checks, one interview step; F6 USAGE, CHANGELOG, MAP, marks green.
   One commit per unit with the `Contract:` trailer, Two-Key, PR, then on
   the user's word: merge, tag v0.14.0, self-pin. Version confirmed at
   intake.
   - 5b, proposed and unratified: `taskcontract graph` emits Archify beside
     its Mermaid, so a contract's picture is derived (0024). Two units, its
     own small contract, before the demo.
4. Demo intake in a sandbox consumer, on the ratified template: the user
   copies the Drive template for one real feature or runs the interview
   (reinstall the plugin from the tag first); intake consumes the document;
   USAGE gains the mapping section beside section 8 on the real template.
5. Wave B: `/sdlc intake playbook-loop` (V1-V5) plus V6, the hook refuses a
   commit while a derived block is stale or an OPEN mark stands (the
   surprise loop made mechanical); the hook's warning outside scope
   tightens to deny. Kit 0.15.0.
6. Session close: STATE.md regenerated, this plan struck through.

Carried: work-side upgrade to 0.13.0 (id migration, vocab extract, seats,
the hook and REVIEW.md via `/sdlc update`, trailers on every commit); G1
slice (Gherkin as the authoring format, fed by F5); prompt lexicon arc;
runner probe, M0 pilot, PL-PIPE.3 harness. Open: the four metrics for
wave B; render the hook command per stack (`python` vs `python3`).

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + git commit -F; Two-Key on every code unit; a
`Contract:` trailer on every commit that touches a non-free path.
