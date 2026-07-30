# 20. Merge-gate distribution shape

Status: accepted
Date: 2026-07-30

## Context

The G4 walk fixed the gate's identity: merge queue authoritative, PR CI
advisory preview, queue-less fallback strict serial merges
([G4 page](../docs/gates/G4-pre-merge-ci.md)). The mechanical-core
slice (contract `dotnet-profile-g4`) is the first to distribute any of
it, and two shape questions had no precedent. Venue: does the overlay
ship one workflow or split inner loop from merge gate - and what may
the kit do about queue enablement, which lives in branch-protection
settings the kit never writes? Mechanism: the suppression audit is the
kit's first pipeline-native check - a program, not a config line - and
copying a script into consumers would fork it per repo, unversioned,
outside the pin.

## Decision

1. **One workflow serves both venues.** The overlay ships a single
   kit-owned merge-gate workflow triggered on `pull_request` (advisory
   preview on the test-merge ref), `merge_group` (authoritative under a
   queue), and push-main (standing echo). Duplicating steps across an
   inner-loop file and a gate file is the duplication entropy G4.8
   exists to catch, applied to ourselves.
2. **Diff-scoped steps gate off push runs.** Subject checks (secrets
   scan, suppression audit) run only where a candidate diff exists -
   `pull_request` and `merge_group`; the result-scoped core runs
   everywhere. The frame rubric (object = merged result vs candidate
   diff) becomes workflow `if:` conditions.
3. **Queue enablement is documented, never written.** Branch
   protection and merge-queue settings are the consumer's; the
   workflow is queue-ready and the fit notes name the queue-less
   fallback. The kit's write surface ends at the workflow file.
4. **Pipeline-native checks ship as kit modules behind the pin.**
   `python -m taskcontract suppression-audit` installs from the same
   pinned ref the G0 backstop uses - versioned, upgradeable by pin
   bump, one implementation for every consumer. Copied scripts are the
   anti-pattern; the pip package is the distribution channel for
   anything with logic.

## Consequences

- Consumers get G4 semantics at whatever queue maturity they have:
  advisory on plain PRs today, authoritative the day they enable the
  queue - no kit change either way.
- The workflow grows steps as later slices bind more conditions; the
  file stays kit-owned and applyable, and step count is bounded by the
  gate's minutes budget, not by file-split ergonomics.
- Every future pipeline-native check (traceability script,
  write-surface audit job, ratchet checks) has its residence question
  pre-answered: a taskcontract subcommand behind the pin.
- Accepted cost: the audit steps pay a Python setup on dotnet runners
  (~seconds); the dotnet-tool wrapper gap stands for shops where that
  is friction.
