# Using the SDLC Kit

> 🟢 **v1 shipped** — every flow in these pages is implemented and proven
> by the kit's regression suite plus live greenfield + brownfield smoke
> runs (no-clobber included). Sections marked 🔴 are ratified but not
> yet shipped.

The kit lays a **gate spine** into a repository: immutable task
contracts under `specs/`, a gate status page, config + ledgers under
`.sdlc/`, and CI that validates every contract. This is the explicit
guide; `README.md` is the short overview.

**The whole idea in one sentence:** a task may not enter development
until its contract validates `ready`, and nothing the implementer can
edit is allowed to weaken that check.

---

## Pages

Each page holds one feature of the kit: read only the one at hand. The
§ column keeps the old section numbers, so a reference such as "USAGE
§8" still finds its page. A section split over pages reads in the
table's order: "above", "below" and "this section" in its pages follow
that order.

| § | Page | What it covers |
|---|---|---|
| 1-3 | [Install and initialize](docs/usage/install.md) | when to run `/sdlc`, the install, what `/sdlc` lays |
| 4 | [The feature document](docs/usage/feature-document.md) | `/sdlc:product-specification-interview` and its consult cases |
| 4 | [Intake](docs/usage/intake.md) | `/sdlc intake`, the G0 venue, and what `ready` requires |
| 4 | [G1](docs/usage/g1.md) | `/sdlc g1`, the G1 venue |
| 4 | [Contract tools](docs/usage/contract-tools.md) | `taskcontract new`, `/sdlc audit`, the session hook, `scope-check`, `.sdlc/REVIEW.md` |
| 4 | [Nodes](docs/usage/node.md) | `taskcontract node <id>`: a node's session at its row's settings |
| 4 | [The execution team](docs/usage/the-team.md) | `/sdlc execute`, the declaration, the wall, rounds and the draft PR |
| 5 | [Vocabulary](docs/usage/vocabulary.md) | executable shared language |
| 6 | [A worked example](docs/usage/worked-example.md) | a greenfield run end to end |
| 7 | [Restricted environments](docs/usage/restricted-environments.md) | the one-way membrane |
| 8 | [Intake with more than one seat](docs/usage/intake-seats.md) | the seats, their fields, the answer record, a worked example |
| 9 | [Following the work: the tree](docs/usage/the-tree.md) | what the tree holds, its statuses, modes and tasks, recording progress, notify |
| 9 | [Following the work: the pane](docs/usage/the-pane.md) | the pane's lines, conditions, names, drift, blocked work, the interactive pane |
| 9 | [Following the work: documents](docs/usage/documents-on-the-tree.md) | gates roll up, features before intake, revisions, parked and paired documents, G1 active |
| 10 | [Troubleshooting](docs/usage/troubleshooting.md) | each refusal code and its remedy |
