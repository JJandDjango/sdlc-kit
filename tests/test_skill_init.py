"""No-clobber renderer suite for the /sdlc init engine (ADR 0016)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ANSWERS = {"project_name": "demo", "material": "greenfield", "stack": "python"}

FULL_PAYLOAD = {
    "SDLC.md",
    ".sdlc/config.yaml",
    ".sdlc/clocks.yaml",
    ".sdlc/reds.yaml",
    "specs/README.md",
    ".github/workflows/sdlc.yml",
    ".pre-commit-config.yaml",
    ".vscode/settings.json",
}


def _templates(skill_init) -> Path:
    return Path(skill_init.__file__).parent / "templates"


def test_greenfield_creates_full_payload(tmp_path, skill_init):
    created, skipped, merges = skill_init.render_all(
        ANSWERS, _templates(skill_init), tmp_path, "2026-07-26")
    rels = {p.relative_to(tmp_path).as_posix() for p in created}
    assert rels == FULL_PAYLOAD
    assert skipped == [] and merges == []
    for p in created:
        assert "{{" not in p.read_text(encoding="utf-8"), f"unsubstituted var in {p}"
    assert "demo" in (tmp_path / "SDLC.md").read_text(encoding="utf-8")


def test_second_run_is_pure_no_clobber(tmp_path, skill_init):
    skill_init.render_all(ANSWERS, _templates(skill_init), tmp_path, "2026-07-26")
    created, skipped, merges = skill_init.render_all(
        ANSWERS, _templates(skill_init), tmp_path, "2026-07-27")
    assert created == []
    assert len(skipped) == 6  # the normal targets
    assert {rel for rel, _ in merges} == {".pre-commit-config.yaml", ".vscode/settings.json"}


def test_preexisting_merge_target_untouched(tmp_path, skill_init):
    sentinel = "repos: []  # my existing hooks\n"
    (tmp_path / ".pre-commit-config.yaml").write_text(sentinel, encoding="utf-8")
    created, _, merges = skill_init.render_all(
        ANSWERS, _templates(skill_init), tmp_path, "2026-07-26")
    assert (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8") == sentinel
    assert [rel for rel, _ in merges] == [".pre-commit-config.yaml"]
    assert "taskcontract" in merges[0][1]  # the snippet still reaches the user
    rels = {p.relative_to(tmp_path).as_posix() for p in created}
    assert rels == FULL_PAYLOAD - {".pre-commit-config.yaml"}


@pytest.mark.parametrize("bad", [
    {**ANSWERS, "material": "legacy"},
    {**ANSWERS, "project_name": "a/b"},
    {**ANSWERS, "stack": "  "},
])
def test_bad_answers_rejected(tmp_path, skill_init, bad):
    with pytest.raises(ValueError):
        skill_init.render_all(bad, _templates(skill_init), tmp_path, "2026-07-26")


def test_cli_round_trip(tmp_path, skill_init, capsys):
    rc = skill_init.main(["--answers", json.dumps(ANSWERS), "--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "created" in out and "Next steps" in out

    rc = skill_init.main(["--answers", json.dumps(ANSWERS), "--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "merge-by-hand" in out and "Nothing new to create" in out
