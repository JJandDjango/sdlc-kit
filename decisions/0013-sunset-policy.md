# 13. Fix the sunset policy: authorship, notice, movement

Status: accepted
Date: 2026-07-26

## Context
G10.1 escalates deprecation warnings to errors at a sunset date, which
requires the date to be authored somewhere a compiler reads, a consumer
sees, and a policy governs. Authorship, minimum notice, movement rules,
and the notification obligation (G10's authored-here line, enforced by
no condition) were open. Forced at the S11 walk, stop 6.

## Decision
- Deprecation is a contract change. The deprecation record is class S,
  authored spec-channel: {api id, replacement ref, migration-spec ref
  where the path carries data/behavior, sunset date, notification ref,
  provenance}. The in-code mark is the record's compiled projection and
  carries the date into binary metadata; an analyzer checks coherence
  both ways - a sunset-bearing mark without a complete record (or the
  reverse) is a merge red, never a silently unarmed sunset.
- The clock starts at notification: a sunset date is valid only if >=
  notification time + the minimum-notice floor for its surface class
  (shipped surface per the G7.2 package set vs internal; floors live
  in clocks.yaml per 0012, numbers Q4). The notification ref is the
  G7.2 contract-diff payload of the release that shipped the mark -
  notice a consumer could not have seen is not notice.
- Movement is asymmetric: moving a date later is gate-loosening and
  takes the full second channel; moving it earlier is bounded - never
  below minimum notice from the original notification. All moves are
  record edits; attribute-only drift is caught by the coherence check.
- Sunset-bearing subjects are APIs and declared config surfaces,
  feature flags included: the flag schema requires a sunset date, and
  flag references past it read error - flags cannot rot invisible to
  the dead-code oracle (a flag check keeps both branches reachable).

## Consequences
- Notification is structurally unavoidable (record schema + clock
  rule); no separate notification condition exists (G10.4 rejected).
- The G10.1 analyzer is a 0009-family adoption, first tranche (Q6).
- Release-notes generation gets its content for free - the same diff
  payload serves notification and documentation (PL-DOC input, S12).
- Sunset dates join the deletion pipeline's paper trail: G10.1
  starves, G10.2 counts, G10.3 clears, G7.2 records the break.
