## 10. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "`/sdlc` isn't listed" | Reload the Claude Code session after installing. |
| "It didn't overwrite my file" | By design (no-clobber). Edit the file in place, or delete it and re-run. |
| `TC003 dependency unresolved` | The contract is a parked draft — resolve or re-scope the dependency; `ready` requires all resolved. 🟢 `/sdlc audit` reads it `CONTRACT-PARKED` at exit 0, and a `still to declare:` suffix names what it also owes: `TC017`, `TC018` or both (rows below). |
| `TC005 unknown field` | Contracts reject stray keys (`additionalProperties: false`) — a typo or scope smuggling; both fail loudly. |
| `TC016 unit not confirmed` (🟢 0.12.0) | The seat term is ratified here and a unit lacks `confirmed_by`, or names a seat the term does not list. Run intake's confirm step, or fix the value (§8). On a parked contract `/sdlc audit` does not park it: `TC003` beside `TC016` reads `CONTRACT-INVALID` until the units carry answers. |
| `TC017 contract declares no entities` (🟢 0.14.0) | The field is required at `ready`. List the glossary terms the contract operates on, or write `entities: []` to state that it operates on none: an edit, not a re-intake (§4, "What `ready` requires"). |
| `TC018 no seat roster` or `seat roster not ratified` (🟢 0.14.0) | The repo holds no ratified `intake-seat`, so no contract under `specs/` reaches `ready`. Author `specs/vocabulary/intake-seat.yaml` (`/sdlc vocab add intake-seat` drafts it) and ratify it; one remedy clears every contract, and ratifying arms `TC016` (§8). |
| CI job green with no contracts | Expected — the validate step is guarded until a `specs/*/contract.yaml` exists. |
| `audit` exit 2 | No `.sdlc/` here — run `/sdlc` init first. |
