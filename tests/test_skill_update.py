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


# --- tooling-profile parity (contract: dotnet-profile-g0, ADR 0018) ---

import json
import shutil


def _steel_templates(skill_init, tmp_path):
    """Real templates plus a fixture overlay.

    Drift-checked overlay templates must render from kit truth + date +
    stack only (profile-authoring rule, ADR 0018); badge.txt models the
    mis-authored case - an interview-only variable - and must land in the
    unrenderable safety net, never silently pass.
    """
    templates = tmp_path / "templates-fixture"
    shutil.copytree(_templates(skill_init), templates)
    profile = templates / "profiles" / "steel"
    profile.mkdir(parents=True)
    (profile / "extra.txt.template").write_text(
        "steel tool config for {{ stack }}\n", encoding="utf-8")
    (profile / "hooks.yaml.template").write_text(
        "hooks: steel ({{ date }})\n", encoding="utf-8")
    (profile / "badge.txt.template").write_text(
        "badge for {{ project_name }}\n", encoding="utf-8")
    (profile / "profile.json").write_text(json.dumps({"templates": {
        "extra.txt.template": {"target": "tools/steel.txt", "class": "kit-owned"},
        "hooks.yaml.template": {"target": ".steel-hooks.yaml", "class": "merge-target"},
        "badge.txt.template": {"target": "tools/badge.txt", "class": "kit-owned"},
    }}), encoding="utf-8")
    return templates


def test_dotnet_fresh_scaffold_is_clean(tmp_path, skill_init, skill_update, capsys):
    """A dotnet consumer scaffolded from the current templates - G3 payload
    included - reads current."""
    skill_init.render_all({**ANSWERS, "stack": "dotnet"},
                          _templates(skill_init), tmp_path, "2020-01-01")
    rc = skill_update.main(["--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "scaffold current" in out


def test_dotnet_pre_slice_consumer_reports_absent_in_ruled_classes(
        tmp_path, skill_init, skill_update):
    """A dotnet consumer scaffolded before the G3 payload existed sees the
    new surfaces as honest rows in their manifest-declared classes
    (contract: dotnet-profile-g3, unit manifest-and-drift-classes)."""
    pre_slice = tmp_path / "templates-pre-slice"
    shutil.copytree(_templates(skill_init), pre_slice)
    manifest = pre_slice / "profiles" / "dotnet" / "profile.json"
    manifest.write_text(json.dumps({"templates": {}}), encoding="utf-8")
    consumer = tmp_path / "consumer"
    skill_init.render_all({**ANSWERS, "stack": "dotnet"}, pre_slice,
                          consumer, "2020-01-01")

    rows, is_spine = skill_update.scan(consumer, _templates(skill_init), "dotnet")
    assert is_spine
    by_path = {r.path: r for r in rows}
    assert by_path["Directory.Build.props"].status == "absent"
    assert by_path["Directory.Build.props"].klass == "merge-target"
    assert by_path[".editorconfig"].status == "absent"
    assert by_path[".editorconfig"].klass == "merge-target"
    assert by_path[".github/workflows/sdlc-dotnet.yml"].status == "absent"
    assert by_path[".github/workflows/sdlc-dotnet.yml"].klass == "kit-owned"
    # the replaced pre-commit target exists from the base render: drift,
    # merged by hand, never applied
    assert by_path[".pre-commit-config.yaml"].status == "drift"
    assert by_path[".pre-commit-config.yaml"].klass == "merge-target"


def test_dotnet_overlay_templates_render_from_kit_truth(skill_init, skill_update):
    """Profile-authoring rule (ADR 0018, suite-locked): every shipped dotnet
    overlay template renders from kit truth + date + stack only, so the
    drift engine can always compare it - no interview-only variables."""
    templates = _templates(skill_init)
    profile_dir = templates / "profiles" / "dotnet"
    variables = skill_update._compare_vars("dotnet")
    overlay = [s for s in skill_init.resolve_surfaces(templates, "dotnet")
               if s.path.parent == profile_dir]
    assert overlay  # the payload actually ships
    for surface in overlay:
        assert skill_update._render(surface, variables) is not None, surface.name


def test_read_stack_parses_value_comment_and_absence(tmp_path, skill_init, skill_update):
    _scaffold(tmp_path, skill_init)
    assert skill_update.read_stack(tmp_path) == "python"
    config = tmp_path / ".sdlc/config.yaml"
    config.write_text("kit: x\nstack: 'dotnet'  # quoted\n", encoding="utf-8")
    assert skill_update.read_stack(tmp_path) == "dotnet"
    config.write_text("kit: x\n", encoding="utf-8")
    assert skill_update.read_stack(tmp_path) == ""


def test_stackless_config_scans_base_surfaces_only(tmp_path, skill_init, skill_update, capsys):
    _scaffold(tmp_path, skill_init)
    config = tmp_path / ".sdlc/config.yaml"
    config.write_text("kit: pinned\n", encoding="utf-8")  # stack line gone
    rc = skill_update.main(["--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "scaffold current" in out


def test_overlay_surface_reports_in_declared_class(tmp_path, skill_init, skill_update):
    templates = _steel_templates(skill_init, tmp_path)
    consumer = tmp_path / "consumer"
    skill_init.render_all({**ANSWERS, "stack": "steel"}, templates, consumer, "2020-01-01")

    rows, is_spine = skill_update.scan(consumer, templates, "steel")
    assert is_spine
    by_path = {r.path: r for r in rows}
    assert by_path["tools/steel.txt"].status == "ok"
    assert by_path["tools/steel.txt"].klass == "kit-owned"
    # interview-only variables cannot be compared: the safety net holds
    assert by_path["tools/badge.txt"].status == "unrenderable"

    (consumer / "tools/steel.txt").unlink()
    rows, _ = skill_update.scan(consumer, templates, "steel")
    by_path = {r.path: r for r in rows}
    assert by_path["tools/steel.txt"].status == "absent"
    assert by_path["tools/steel.txt"].klass == "kit-owned"

    (consumer / ".steel-hooks.yaml").write_text("hooks: mutated\n", encoding="utf-8")
    rows, _ = skill_update.scan(consumer, templates, "steel")
    by_path = {r.path: r for r in rows}
    assert by_path[".steel-hooks.yaml"].status == "drift"
    assert by_path[".steel-hooks.yaml"].klass == "merge-target"


def test_overlay_apply_honors_classes(tmp_path, skill_init, skill_update):
    templates = _steel_templates(skill_init, tmp_path)
    consumer = tmp_path / "consumer"
    skill_init.render_all({**ANSWERS, "stack": "steel"}, templates, consumer, "2020-01-01")

    target = consumer / "tools/steel.txt"
    target.write_text("garbage\n", encoding="utf-8")
    ok, message = skill_update.apply_one(consumer, templates, "steel", "tools/steel.txt")
    assert ok and "applied" in message
    assert target.read_text(encoding="utf-8") == "steel tool config for steel\n"

    ok, message = skill_update.apply_one(consumer, templates, "steel", ".steel-hooks.yaml")
    assert not ok and "merge it by hand" in message

    ok, message = skill_update.apply_one(consumer, templates, "steel", "tools/badge.txt")
    assert not ok and "needs interview answers" in message
