# Plan - Session 55 (2026-09-26) - project-tree o7, release 0.16.0

**Deliverable:** unit `o7-release` of `project-tree` with its Two-Key
PASS, then the release: the merge, the annotated tag `v0.16.0` at the
merge, and the self-pin through its own PR. o7's done_means: kit 0.16.0
ships with the `USAGE.md` marks all green, its `CHANGELOG.md` entry and
ADR 0032; `taskcontract tree` still prints every item and exits 0, and
`taskcontract tree <id>` answers every id in at most seven lines (SC1.3).

**Rulings at plan review** (the user's; Claude's recommendation first):

1. Merge PR #63 by merge commit once CI reads green, then cut
   `session-55-project-tree-o7` from main's new tip. Cutting from session
   54's tip would stack two unmerged PRs.
2. The live run comes first, before any release text: the pane runs in a
   herdr pane on Windows, and the user drives its keys. A defect it finds
   is an OPEN and a re-intake, never a silent fix inside o7, whose
   done_means covers no pane behavior.
3. No test list for o7. o1's tests already pin SC1.3
   (`tests/test_tree_conditions.py:801` and `:842`), so o7 records
   SC1.3's run green on them, as t9 did for tree-view. The feature
   document names `tests/test_tree_view.py`, which no longer exists; the
   contract names no test file, and Two-Key grades the contract.
4. Claude writes the release text: the USAGE sweep, the CHANGELOG entry,
   ADR 0032 and MAP's work-tree row. The user approves all of it in one
   batch, shown in chat as before and after, and then approves the commit
   (o7's seat is `user`). Two-Key runs through the verifier Workflow.

## Steps

1. Open: PR #63 merged; the branch cut; this plan committed.
2. The live run: Claude splits a herdr pane with `--no-focus` and runs
   `python -m taskcontract tree --follow` in the kit's root; the user
   drives the keys, the clicks and the wheel, and watches a render and
   Ctrl-C; Claude closes the pane after.
3. The release text, one batch for approval:
   - `USAGE.md`: every project-tree mark green; the sweep from STATE.md
     (the top of section 9, the green paragraphs at 622-624, 630-632 and
     767-771, "The pane's lines", the `--follow` bullet of "The three
     modes", "Plain names and titles", a finding counted by its kind, o3's
     tie-break, an `rM` above the document's revision).
   - ADR 0031 line 43; ADR 0032 (new); `CHANGELOG.md`'s 0.16.0 entry;
     MAP's work-tree row names the Textual outline and ADR 0032.
   - Code-side wording: the schema's top-level `description` names
     `title`; `tree_view.py`'s docstring says "id" where `_fold` prints
     one; `tests/test_pane.py` drops its unused `tree_view` import and its
     cut sentence names the group.
4. The version: `pyproject.toml` and `KIT_VERSION` read `0.16.0`.
5. o7's commit, approved by the user; SC1.3 run green after it with no
   tracked file modified; the suite run whole.
6. Two-Key; o7 and the contract closed through `taskcontract progress`.
7. Close: STATE.md regenerated, this plan struck; the push and the PR on
   the user's word.
8. Release: the merge on the user's word, the annotated tag `v0.16.0` at
   the merge, then the self-pin (`.github/workflows/sdlc.yml` line 20 and
   `USAGE.md` line 377 to `@v0.16.0`) through its own PR, with USAGE's
   `uv` line run against the new tag.

Steps 1, 2, 7 and 8 sit outside a contract unit, so the tree does not show
them.

Decisions this session: nine, all the user's. (1) This plan and rulings 1
to 4; (2) the merge of PR #63; (3) the live run's verdict; (4) the release
text batch; (5) o7's commit; (6) the push and the PR; (7) the merge; (8)
the tag and its message; (9) the self-pin PR.

Deferred, not this session:
- Test gaps: no pane test checks that a `parts:` list without `evidence`
  hides an approval's seat; the row pattern in `tests/conftest.py` splits
  a plain name at its first ` [`.
- Prerequisites 7 to 9 on the kit's own tree (titles, feature documents,
  progress records).
- G1, the pilot's config line, and the rest of STATE.md's carried list.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on every
commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; every herdr probe closes the
panes it opens; the merge, the tag, the push and the PR on the user's word.
