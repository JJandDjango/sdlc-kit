# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-18 (session 31 close, home machine)._

## Now
- Two pull requests open, both CI-green, neither merged; main is still at
  16426dd (PR #39). PR #40 `session-31-spec-interview` (eight commits,
  fb51daa..47bf089): the specification interview ships as the plugin's
  second skill, `/sdlc:product-specification-interview` (ADR 0028, contract
  `spec-interview`). PR #41 `session-31-wave-a` (stacked on #40,
  6f8e92e..13f3709 plus this close): wave A, contract `playbook-guardrails`:
  the session hook, `taskcontract scope-check` (G4.12), `.sdlc/REVIEW.md`,
  the engineer's three questions at intake; version 0.13.0 in pyproject and
  `KIT_VERSION`; the tag and the self-pin wait on the merge.
- Session 31 (2026-09-17 to 2026-09-18) built and verified plan steps 4 and
  5. Both Two-Key passes ran as Workflow verifiers (one receipts agent, one
  zero-trust grader per unit): 5/5 and 9/9 units PASS; their advisories
  closed in ad95d65 and 9f8c33a. Every unit landed as one commit.
- Decisions taken 2026-09-17 on the recommendation: (1) the diff-to-contract
  binding is a `Contract:` trailer, in git's final paragraph with the
  attribution lines; every kit commit carries one from intake A on (the first
  live scope-check found six wave-A commits with the trailer in a paragraph
  of its own, and they were rewritten before their first push). (2) Class-E
  paths get no special case: the hook denies `specs/`, warns outside the
  bound contract's scope, and denial there is wave B.
- Receipts at close: suite 282, prompt_lang skills 13/13 and agents 2/2,
  twelve contracts ready-green, lang-check 0 (new contracts are not exempt;
  the authoring recipe is in project memory), scope-check green over
  `session-31-spec-interview..HEAD`, Cairn audit 0 errors / 25 warnings (23
  known, a budget note on 0028, and STATE-STALE cleared by this file).
- Inbox, untracked by the kit rules: `REQUEST_spec-interview_2026-09-17.md`
  and `REQUEST_playbook-guardrails_2026-09-17.md` (the kit's first two
  requests in the feature-document template) and
  `REQUEST_unit-dag_2026-08-22.md`.

## Blockers
- None. The stale pip install persists (`sdlc-taskcontract` 0.10.0,
  non-editable); `pip install -e E:\sdlc_development_kit` on the user's
  word. `python -m` from the repo root shadows it, so every receipt above
  ran the checkout; CI installs editable, which is why one hook test needed
  a fake `checker.py` (13f3709).

## Next actions (plan.md step numbers)
1. **The release, on the user's word:** merge #40, then #41 (GitHub retargets
   it to main); `git tag v0.13.0` at the merge; the self-pin PR moves the
   kit's own `.github/workflows/sdlc.yml` ref (`@v0.12.0`) and USAGE's
   install example to the tag, and gives CHANGELOG's "0.13.0 - unreleased"
   heading its date and tag. Then delete the two branches and sync main.
2. Step 5b, proposed and unratified: `taskcontract graph` emits Archify
   beside its Mermaid, so a contract's picture is derived (0024). Two units,
   its own contract, before the demo.
3. Step 6, the demo intake in a sandbox consumer: the user copies the Drive
   template or runs `/sdlc:product-specification-interview` there (its first
   live run; reinstall the plugin from the tag first, or the command does
   not exist in the session); intake consumes the document (I4 reads the
   Implementation section); USAGE gains the mapping section beside §8 on
   the real template.
4. Step 7: `/sdlc intake playbook-loop` (V1-V5) after fixing the re-scan
   cadence and the metric set; the hook's warning outside scope tightens to
   deny there.
5. Carried: work-side upgrade to 0.13.0 (id migration, vocab extract, seats,
   the hook and REVIEW.md via `/sdlc update`, trailers on every commit); G1
   slice (Gherkin as the authoring format); prompt lexicon arc; runner probe,
   M0 pilot, PL-PIPE.3 harness.

## Open questions
- Promote "plans as Archify diagrams" to the global CLAUDE.md preferences?
- Ratify step 5b into the plan?
- The rendered hook command names `python`; USAGE documents the manual swap
  to `python3` where only that resolves. Render per stack instead?
  (verifier advisory on u2 and u3)
- Gap 4: which four metrics stay. Q4 thresholds, Q5 decorrelation, Q6 first
  analyzer tranche, PL-PIPE.3 comprehension empirics: unchanged from 25.
