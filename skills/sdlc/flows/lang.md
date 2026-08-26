---
name: sdlc-flow-lang
description: The Lang flows of /sdlc - the controlled-language door (lang-check) and its report-only calibration (lang-extract).
---

<purpose>
The Lang flows of the `/sdlc` skill: controlled language
(docs/controlled-language.md). A set-ratified dictionary at
specs/vocabulary/dictionary.yaml arms lang-check over contract prose
fields; absent = green. Form checked, meaning not. Dispatched by
{skill-dir}/SKILL.md on `/sdlc lang`, sub-dispatched on the next
argument to Check or Extract; its constraints and criteria bind here.
{skill-dir} is the directory holding SKILL.md.
</purpose>

<instructions>
LC1. CHECK - one Bash call: `python -m taskcontract lang-check`. REPORT stdout verbatim. Exempt warnings = the standing-red ratchet, never gating. On exit 1 fix exactly what each CLnnn names; cap 5; then report and return.

LX1. EXTRACT - one Bash call: `python -m taskcontract lang-extract`. REPORT stdout verbatim (candidates, banned hits, census; writes nothing). Handoff: dictionary deltas are class-E - adding takes the full lane, banning rides auto; the PR merge is the set-ratification record.
</instructions>
