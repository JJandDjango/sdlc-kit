"""Drift-report suite for the /sdlc update engine (contract:
distribution-reconciliation, unit update-command)."""

from __future__ import annotations

from pathlib import Path

import pytest

ANSWERS = {"project_name": "demo", "adoption": "greenfield", "stack": "python"}

WORKFLOW = ".github/workflows/sdlc.yml"
VSCODE = ".vscode/settings.json"


def _templates(module) -> Path:
    return Path(module.__file__).parent / "templates"


def _scaffold(tmp_path, skill_init, today="2020-01-01"):
    """Render a consumer scaffold with a deliberately old date stamp."""
    skill_init.render_all(ANSWERS, _templates(skill_init), tmp_path, today)


def test_fresh_scaffold_is_clean(tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    rc = skill_update.main(["--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "scaffold current" in out
    # The old date stamp is per-consumer variance, never drift.
    assert "drift" not in out


def test_kit_owned_drift_named_and_exit_1(tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    workflow = tmp_path / WORKFLOW
    stale = workflow.read_text(encoding="utf-8").replace(
        skill_update.INIT.KIT_REF, "git+https://github.com/JJandDjango/sdlc-kit.git")
    workflow.write_text(stale, encoding="utf-8")
    rc = skill_update.main(["--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert WORKFLOW in out
    assert "kit-owned" in out


def test_consumer_files_never_diffed(tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    reds = tmp_path / ".sdlc/reds.yaml"
    reds.write_text(reds.read_text(encoding="utf-8").replace(
        "reds: []",
        "reds:\n  - {id: r1, condition: c, class: E, clock_origin: o, window: w, status: open}"),
        encoding="utf-8")
    rc = skill_update.main(["--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "existence only" in out


def test_merge_target_drift_distinguished_and_apply_refused(
        tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    settings = tmp_path / VSCODE
    mutated = settings.read_text(encoding="utf-8").replace(
        "raw.githubusercontent", "raw.example")
    settings.write_text(mutated, encoding="utf-8")

    rc = skill_update.main(["--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "merge-target" in out and VSCODE in out
    assert "never auto-applied" in out

    rc = skill_update.main(["--cwd", str(tmp_path), "--apply", VSCODE])
    err = capsys.readouterr().err
    assert rc == 1
    assert "refused" in err
    assert settings.read_text(encoding="utf-8") == mutated  # untouched


def test_apply_restores_kit_owned_file(tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    workflow = tmp_path / WORKFLOW
    workflow.write_text("jobs: {}\n", encoding="utf-8")
    rc = skill_update.main(["--cwd", str(tmp_path), "--apply", WORKFLOW])
    out = capsys.readouterr().out
    assert rc == 0
    assert "applied" in out
    restored = workflow.read_text(encoding="utf-8")
    assert f"@v{skill_update.INIT.KIT_VERSION}" in restored

    rc = skill_update.main(["--cwd", str(tmp_path)])
    capsys.readouterr()
    assert rc == 0  # applying converges to clean


def test_absent_surface_reported(tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    (tmp_path / "specs/README.md").unlink()
    rc = skill_update.main(["--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "absent" in out and "specs/README.md" in out


def test_show_prints_current_render(tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    rc = skill_update.main(["--cwd", str(tmp_path), "--show", WORKFLOW])
    out = capsys.readouterr().out
    assert rc == 0
    assert f"@v{skill_update.INIT.KIT_VERSION}" in out


def test_no_spine_exits_2(tmp_path, skill_update, capsys):
    rc = skill_update.main(["--cwd", str(tmp_path)])
    err = capsys.readouterr().err
    assert rc == 2
    assert "No SDLC gate spine" in err
