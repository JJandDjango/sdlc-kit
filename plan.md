# Session 167 plan: session-loop's contract to lang-check zero (backlog Next 30)

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G0, the gate where `/sdlc intake` turns a signed pair of feature documents into a ready task contract.
**Feature:** session-loop: sessions that wrap and restart themselves until a human is needed.
**Unit:** none built: this session makes the contract's prose pass the controlled register, so PR #173's `lang-check` door turns green.

## 1. The deliverable

`specs/session-loop/contract.yaml` at 0 lang-check findings, still ready-green, with its ten new terms ratified and the dictionary words its `done_means` force added.

## 2. Where this sits

Session 166 wrote the contract ready-green (PR #173, draft) but left it at 129 lang-check findings, so CI is red. Session 138 did the same step for run-restart (`6d82964`, `9e0e7ca`); this session follows it. G1 and the four units follow in later sessions.

## 3. The steps

1. This plan committed and pushed to `session-166-session-loop-intake`.
2. The ten entries of the requirements' Terms (r9) become term files, word for word: wrap, launcher, sentinel, position, strike, `needs-ruling`, session loop, human-needed stop, self-wrap, hung. The user ratifies them.
3. The dictionary adds the 12 words the four `done_means` still hold after the terms: continues, hang, issue, pick, reply, seconds, sets, strikes, timer, types, waiting, wraps. The user approves them. One commit with step 2; vocab-check green.
4. The intent, the non-goals and the 12 sketch entries rewritten in dictionary words, each check's meaning kept; the `done_means` stand word for word; the ten terms join the entities. Validate `--profile ready` green, lang-check 0, the suite green. One commit.
5. Wrap: the backlog's Next 30 names G1 as its next step, `plan.md` out, push; PR #173 leaves draft once CI is green.

## 4. Where Claude stops for the user

Once, at steps 2 and 3 together: ratifying terms and adding dictionary words are the user's (class-S flip and the full lane). Then at PR #173's review.

## 5. Where Claude goes on alone, and by what rule

The plan, the rewrite, the checks, the commits, the push and the wrap: in this repository no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

Steps 2 and 3 only. The rewrite is already drafted and checked in the scratchpad: with the 12 words it reads 0.

## 7. What could go wrong, already ruled

- A term or word is struck: its `done_means` uses stay unknown and the contract cannot reach 0, so the design's Units row would need a new signature; Claude reports which and stops.
- A new term's name equals a dictionary word (CL003): none does; `wrap` and `strike` stay terms, `wraps` and `strikes` go in as words, as `restart` and `restarts` did.
- A plural of a single-word term is still unknown (the glossary matches only the name): hence `wraps` and `strikes` in the word list.

## 8. This session's cost, with its basis

No agent runs: everything runs in the main session. One full suite run (about 390 s at 3086 tests, the last measured count).

## 9. Not in this session

- `/sdlc g1 session-loop` and the build of `l1-loop-files`: later sessions.
- The `needs-ruling` label on the remote (the user's prerequisite, before l1's first live run).
- session-loop-sidebar (Next 31) and the backlog's other open items.

## 10. Words

- **lang-check**: `python -m taskcontract lang-check`, which reads each contract's prose against the controlled dictionary (`specs/vocabulary/dictionary.yaml`) and the glossary terms.
- **CL006**: lang-check's "unknown word" finding; **CL008**: a sentence past its cap (25 words descriptive, 20 procedural).
- **term**: one ratified glossary entry, `specs/vocabulary/<slug>.yaml`; its name passes lang-check, its plurals do not.
- **full lane**: the path a dictionary addition takes, with the user as approver, since each word loosens the gate.
- **`done_means`**: a unit's finish line, copied from the signed design word for word, so intake cannot rewrite it.
- **ready-green**: `taskcontract validate --profile ready` exits with no diagnostic.
