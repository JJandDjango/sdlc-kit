# Conventions - sdlc_development_kit

> **Contract** - one question: *how do we do things here?*
> <=1 page - update when a rule is adopted / revised / retired - hand-edited,
> significant entries link their ADR.

<!-- An index, not an essay: one line per rule (bold name + statement, ADR link
     when significant). Detail overflows to docs/conventions/ pages. Inferred
     entries carry "(inferred - confirm)" - confirm them and delete the tag. -->

- **Decisions get recorded.** A choice a future you would question gets an ADR
  ([[0001-record-architecture-decisions]]).
- **Gate vocabulary.** A *gate* is a phase's blocking enforcement venue
  (G0-G10, PL-*); a *condition* is a check attached to it, lifecycle
  `registered -> specified -> enforced`. Registry: `docs/gates.md`
  ([[0003-gate-vocabulary-and-registry]]).
- **Gate pages.** Each gate gets a deep page `docs/gates/<ID>-<slug>.md` on
  the fixed template; the registry stays the one-line index; PROPOSED roster
  changes enter only on user ratification
  ([[0004-per-gate-documentation-program]]).
- **Task contracts.** One per task at `specs/<task-id>/contract.yaml`, valid
  against `taskcontract/schemas/task-contract.schema.json` (`ready`
  profile) via `python -m taskcontract validate`
  ([[0006-task-contract-enforcement]]).
- **Unit order lives in the contract.** Every decomposition unit carries an
  `id`; a unit that must follow another names it in `depends_on`. The door
  rejects duplicates, dangling refs, and cycles (TC013-TC015); the picture
  is `python -m taskcontract graph`, computed on demand and never committed
  ([[0024-unit-dependency-graph]]).
- **Intake answers are recorded.** Every unit names the seats that answered
  for it under `confirmed_by`; seats are the repo's ratified `intake-seat`
  value-set, and the ready door demands the record (TC016). The term
  itself is required at ready, not the switch that arms the check: a repo
  without it gets TC018 until the roster is authored and ratified
  ([[0030-a-doors-input-is-a-declaration]]). Who holds which field is
  policy (USAGE §8), never a check on the author ([[0025-intake-seats]]).
- **The raw request stays the requester's.** Intake consumes the consumer's
  own document; the contract is what the venue produces from it, never a
  replacement, and a change after ready re-intakes. The request holds worth
  and design, the contract form and entry; unit tests enter neither
  ([[0026-feature-document-as-raw-request]]).
- **Commits name their contract.** Every commit carries a `Contract: <id>`
  trailer in its final paragraph (git's trailer block). G4.12,
  `python -m taskcontract scope-check`, fails a pull request whose commit
  touches a bound path outside the named contract's `scope`; free paths
  (`.sdlc/config.yaml` `scope_check.free_paths`) need no trailer, and
  `specs/` is the spec channel, never in remit
  ([[0027-playbook-crosswalk-and-closures]]).
- **Register boundary.** Controlled register where prose is executed -
  contract prose fields, checked by `python -m taskcontract lang-check`;
  free register where prose is deliberated (THEORY, ADRs, docs
  literature, conversation). Raw human requests are never
  lexicon-policed ([[0022-controlled-language-shape]]).
<!-- Example code rule - adapt or delete:
- **Match the idiom.** New code follows the touched layer's dominant pattern.
-->
