---
name: sdlc-flow-new
description: The New flow of /sdlc - scaffold a deliberately red contract skeleton at specs/{id}/contract.yaml.
---

<purpose>
The New flow of the `/sdlc` skill: scaffold one contract skeleton.
Dispatched by {skill-dir}/SKILL.md on `/sdlc new {id}`; its constraints
and criteria bind here. {skill-dir} is the directory holding SKILL.md.
</purpose>

<instructions>
N1. RUN - one Bash call: `python -m taskcontract new {id}`. The skeleton is deliberately red: TC007 trips until a real intent is authored, so a fresh contract can never pass the gate vacuously.

N2. REPORT stdout (the created path + the validate loop line). On failure REPORT stderr verbatim; for a missing module also offer the pip install command from SKILL.md's context section.
</instructions>
