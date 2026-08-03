# Plan - Session 24 (2026-08-03) - tag v0.9.0 + self-pin - EXECUTED

PR #26 merged (54717cf) but the v0.9.0 tag never landed - tagging is
step one, then the standing post-merge sequence: the self-pin PR,
this time also carrying the kit's own lang-check CI step (the v0.8.0
pin predates the subcommand; ADR 0022, STATE next-action 1).

## Steps

1. ~~Sync~~ - main to 54717cf, merged branch dropped.
2. ~~Tag v0.9.0~~ - annotated at 54717cf, pushed.
3. ~~Branch session-24-self-pin~~.
4. ~~sdlc.yml~~ - install ref -> v0.9.0 + the controlled-language
   step, mirroring the template exactly.
5. ~~.vscode/settings.json~~ - schema URL -> v0.9.0.
6. ~~Prove locally~~ - lang-green, exempt warnings only.
7. ~~Commit, push, PR~~ - db11ab4, PR #27, both checks green
   (contracts 15s proved the tag install + the door's first CI run);
   merged at 793c9b6, post-merge sync + branch cleanup done.

Next: pilot M0 session in the engine repo (STATE next-action 1).

House rules in force: no pipes/chains in any authored command string
(CI steps included); commit messages via Write + git commit -F.
