"""No-clobber renderer suite for the /sdlc init engine (ADR 0016)."""

from __future__ import annotations

import json
import shutil
import tomllib
from pathlib import Path

import pytest

ANSWERS = {"project_name": "demo", "adoption": "greenfield", "stack": "python"}

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
    {**ANSWERS, "adoption": "legacy"},
    {**ANSWERS, "project_name": "a/b"},
    {**ANSWERS, "stack": "  "},
])
def test_bad_answers_rejected(tmp_path, skill_init, bad):
    with pytest.raises(ValueError):
        skill_init.render_all(bad, _templates(skill_init), tmp_path, "2026-07-26")


def test_rendered_scaffold_pins_release_tag(tmp_path, skill_init):
    skill_init.render_all(ANSWERS, _templates(skill_init), tmp_path, "2026-07-29")
    workflow = (tmp_path / ".github/workflows/sdlc.yml").read_text(encoding="utf-8")
    assert f"@v{skill_init.KIT_VERSION}" in workflow
    assert 'sdlc-kit.git"' not in workflow  # floating install ref shape
    settings = (tmp_path / ".vscode/settings.json").read_text(encoding="utf-8")
    assert f"/v{skill_init.KIT_VERSION}/" in settings
    assert "/main/" not in settings  # floating schema-URL shape


def test_kit_version_matches_packaged_version(skill_init):
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject.open("rb") as fh:
        packaged = tomllib.load(fh)["project"]["version"]
    assert skill_init.KIT_VERSION == packaged


def test_cli_round_trip(tmp_path, skill_init, capsys):
    rc = skill_init.main(["--answers", json.dumps(ANSWERS), "--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "created" in out and "Next steps" in out

    rc = skill_init.main(["--answers", json.dumps(ANSWERS), "--cwd", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "merge-by-hand" in out and "Nothing new to create" in out


# --- tooling-profile overlay (contract: dotnet-profile-g0, ADR 0018) ---

STACK_BEARING = {"SDLC.md", ".sdlc/config.yaml"}  # the only {{ stack }} templates


def _fixture_profile(templates_src: Path, tmp_path: Path, stack: str = "steel") -> Path:
    """Copy the real templates and inject a fixture overlay for `stack`."""
    templates = tmp_path / "templates-fixture"
    shutil.copytree(templates_src, templates)
    profile = templates / "profiles" / stack
    profile.mkdir(parents=True)
    (profile / "extra.txt.template").write_text(
        "steel tool config for {{ project_name }}\n", encoding="utf-8")
    (profile / "hooks.yaml.template").write_text(
        "hooks: steel ({{ date }})\n", encoding="utf-8")
    (profile / "steel-specs-README.md.template").write_text(
        "steel specs root\n", encoding="utf-8")
    (profile / "profile.json").write_text(json.dumps({"templates": {
        "extra.txt.template": {"target": "tools/steel.txt", "class": "kit-owned"},
        "hooks.yaml.template": {"target": ".steel-hooks.yaml", "class": "merge-target"},
        "steel-specs-README.md.template": {"target": "specs/README.md", "class": "kit-owned"},
    }}), encoding="utf-8")
    return templates


def _assert_base_render(base_dir, stack_dir, stack):
    for rel in FULL_PAYLOAD:
        base_text = (base_dir / rel).read_text(encoding="utf-8")
        stack_text = (stack_dir / rel).read_text(encoding="utf-8")
        if rel in STACK_BEARING:
            assert stack_text.replace(stack, "python") == base_text, rel
        else:
            assert stack_text == base_text, rel


def test_absent_overlay_renders_base_payload_exactly(tmp_path, skill_init):
    """No shipped overlay (ruby) is byte-identical to the base render
    outside the recorded stack values."""
    base_dir, stack_dir = tmp_path / "base", tmp_path / "other"
    skill_init.render_all(ANSWERS, _templates(skill_init), base_dir, "2026-07-29")
    skill_init.render_all({**ANSWERS, "stack": "ruby"},
                          _templates(skill_init), stack_dir, "2026-07-29")
    _assert_base_render(base_dir, stack_dir, "ruby")


def test_empty_overlay_renders_base_payload_exactly(tmp_path, skill_init):
    """An empty manifest renders the base exactly - the pre-payload dotnet
    shape, kept covered by fixture now that dotnet ships surfaces."""
    templates = tmp_path / "templates-fixture"
    shutil.copytree(_templates(skill_init), templates)
    hollow = templates / "profiles" / "hollow"
    hollow.mkdir(parents=True)
    (hollow / "profile.json").write_text(
        json.dumps({"templates": {}}), encoding="utf-8")
    base_dir, stack_dir = tmp_path / "base", tmp_path / "other"
    skill_init.render_all(ANSWERS, templates, base_dir, "2026-07-29")
    skill_init.render_all({**ANSWERS, "stack": "hollow"},
                          templates, stack_dir, "2026-07-29")
    _assert_base_render(base_dir, stack_dir, "hollow")


def test_overlay_adds_and_replaces_by_target(tmp_path, skill_init):
    templates = _fixture_profile(_templates(skill_init), tmp_path)
    out = tmp_path / "consumer"
    created, skipped, merges = skill_init.render_all(
        {**ANSWERS, "stack": "steel"}, templates, out, "2026-07-29")
    rels = {p.relative_to(out).as_posix() for p in created}
    assert rels == FULL_PAYLOAD | {"tools/steel.txt", ".steel-hooks.yaml"}
    assert (out / "tools/steel.txt").read_text(encoding="utf-8") == \
        "steel tool config for demo\n"
    # replace-by-target: the overlay's render wins over the base template
    assert (out / "specs/README.md").read_text(encoding="utf-8") == "steel specs root\n"
    assert skipped == [] and merges == []


def test_overlay_respects_no_clobber_and_merge_semantics(tmp_path, skill_init):
    templates = _fixture_profile(_templates(skill_init), tmp_path)
    out = tmp_path / "consumer"
    answers = {**ANSWERS, "stack": "steel"}
    skill_init.render_all(answers, templates, out, "2026-07-29")
    created, skipped, merges = skill_init.render_all(answers, templates, out, "2026-07-30")
    assert created == []
    # overlay kit-owned entries no-clobber like base ones (6 base + 1 overlay)
    assert len(skipped) == 7
    # overlay merge-targets print their snippet instead of writing
    merge_rels = {rel for rel, _ in merges}
    assert merge_rels == {".pre-commit-config.yaml", ".vscode/settings.json",
                          ".steel-hooks.yaml"}
    snippet = dict(merges)[".steel-hooks.yaml"]
    assert snippet == "hooks: steel (2026-07-30)\n"


def test_malformed_profile_manifest_rejected(tmp_path, skill_init):
    templates = _fixture_profile(_templates(skill_init), tmp_path)
    manifest = templates / "profiles" / "steel" / "profile.json"
    manifest.write_text(json.dumps({"templates": {
        "extra.txt.template": {"target": "tools/steel.txt", "class": "root-owned"},
    }}), encoding="utf-8")
    with pytest.raises(ValueError, match="class"):
        skill_init.render_all({**ANSWERS, "stack": "steel"},
                              templates, tmp_path / "consumer", "2026-07-29")


def test_cli_dotnet_note_is_stack_conditional(tmp_path, skill_init, capsys):
    rc = skill_init.main(["--answers", json.dumps({**ANSWERS, "stack": "dotnet"}),
                          "--cwd", str(tmp_path / "dn")])
    out = capsys.readouterr().out
    assert rc == 0
    assert "docs/dotnet-profile.md" in out

    rc = skill_init.main(["--answers", json.dumps(ANSWERS),
                          "--cwd", str(tmp_path / "py")])
    out = capsys.readouterr().out
    assert rc == 0
    assert "docs/dotnet-profile.md" not in out


# --- dotnet G3 payload (contract: dotnet-profile-g3) ---

DOTNET_G3_NEW = {"Directory.Build.props", ".editorconfig",
                 ".github/workflows/sdlc-dotnet.yml"}

PROPS_SETTINGS = (
    "<Nullable>enable</Nullable>",
    "<TreatWarningsAsErrors>true</TreatWarningsAsErrors>",
    "<AnalysisLevel>latest-all</AnalysisLevel>",
    "<CheckForOverflowUnderflow>true</CheckForOverflowUnderflow>",
    "<AllowUnsafeBlocks>false</AllowUnsafeBlocks>",
    "<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>",
    'Include="StyleCop.Analyzers"',
)


def test_dotnet_render_adds_g3_surfaces(tmp_path, skill_init):
    created, skipped, merges = skill_init.render_all(
        {**ANSWERS, "stack": "dotnet"}, _templates(skill_init), tmp_path,
        "2026-07-30")
    rels = {p.relative_to(tmp_path).as_posix() for p in created}
    assert rels == FULL_PAYLOAD | DOTNET_G3_NEW
    assert skipped == [] and merges == []

    props = (tmp_path / "Directory.Build.props").read_text(encoding="utf-8")
    for needle in PROPS_SETTINGS:
        assert needle in props, needle

    editorconfig = (tmp_path / ".editorconfig").read_text(encoding="utf-8")
    assert "[*.cs]" in editorconfig
    assert ("dotnet_analyzer_diagnostic.category-Style.severity = warning"
            in editorconfig)

    precommit = (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "taskcontract" in precommit   # base hook survives the replacement
    assert "dotnet format" in precommit  # the G3.1 fix-channel hook


def test_dotnet_workflow_steps_are_chain_free(tmp_path, skill_init):
    """House rule: every authored CI run step is a single segment - no
    pipes, chains, semicolons, or redirects."""
    skill_init.render_all({**ANSWERS, "stack": "dotnet"},
                          _templates(skill_init), tmp_path, "2026-07-30")
    workflow = (tmp_path / ".github/workflows/sdlc-dotnet.yml").read_text(
        encoding="utf-8")
    run_lines = [line.split("run:", 1)[1]
                 for line in workflow.splitlines() if "run:" in line]
    assert run_lines
    for command in run_lines:
        assert not any(c in command for c in ";|&>"), command


# --- dotnet G4 mechanical core (contract: dotnet-profile-g4) ---

PROPS_G4_SETTINGS = (
    "<RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>",
    "<NuGetAudit>true</NuGetAudit>",
    "<NuGetAuditMode>all</NuGetAuditMode>",
    "<NuGetAuditLevel>low</NuGetAuditLevel>",
    "NU1901;NU1902;NU1903;NU1904",
)


def test_dotnet_workflow_carries_g4_mechanical_core(tmp_path, skill_init):
    skill_init.render_all({**ANSWERS, "stack": "dotnet"},
                          _templates(skill_init), tmp_path, "2026-07-30")
    workflow = (tmp_path / ".github/workflows/sdlc-dotnet.yml").read_text(
        encoding="utf-8")
    assert "merge_group:" in workflow          # queue-authoritative venue
    assert "fetch-depth: 0" in workflow        # history for diff-scoped steps
    # the mechanical core in gate order: locked restore -> echo -> tests
    restore = workflow.index("dotnet restore --locked-mode")
    build = workflow.index("dotnet build --no-restore")
    tests = workflow.index("dotnet test --no-build")
    assert restore < build < tests
    assert "TreatNoTestsAsError=true" in workflow  # zero-tests FAIL guard
    # diff-scoped steps: masked secrets scan + the audit from the pinned kit
    assert "gitleaks" in workflow and "--redact" in workflow
    assert "python -m taskcontract suppression-audit" in workflow
    assert f"@v{skill_init.KIT_VERSION}" in workflow
    assert workflow.index("pip install") < workflow.index(
        "python -m taskcontract suppression-audit")


def test_dotnet_props_carry_dependency_audit_block(tmp_path, skill_init):
    skill_init.render_all({**ANSWERS, "stack": "dotnet"},
                          _templates(skill_init), tmp_path, "2026-07-30")
    props = (tmp_path / "Directory.Build.props").read_text(encoding="utf-8")
    for needle in PROPS_G4_SETTINGS:
        assert needle in props, needle


def test_dotnet_diff_scoped_steps_skip_push_runs(tmp_path, skill_init):
    """The secrets scan and suppression audit are diff-scoped (G4.10 frame):
    they run on pull_request and merge_group, never on push-main where no
    candidate diff exists."""
    skill_init.render_all({**ANSWERS, "stack": "dotnet"},
                          _templates(skill_init), tmp_path, "2026-07-30")
    workflow = (tmp_path / ".github/workflows/sdlc-dotnet.yml").read_text(
        encoding="utf-8")
    gates = workflow.count("if: github.event_name != 'push'")
    assert gates == 4  # secrets, setup-python, kit install, audit


def test_dotnet_enforcement_configs_are_merge_targets(tmp_path, skill_init):
    sentinel_props = "<Project>mine</Project>\n"
    sentinel_ec = "root = true  # mine\n"
    (tmp_path / "Directory.Build.props").write_text(sentinel_props,
                                                    encoding="utf-8")
    (tmp_path / ".editorconfig").write_text(sentinel_ec, encoding="utf-8")
    created, _, merges = skill_init.render_all(
        {**ANSWERS, "stack": "dotnet"}, _templates(skill_init), tmp_path,
        "2026-07-30")
    assert (tmp_path / "Directory.Build.props").read_text(
        encoding="utf-8") == sentinel_props
    assert (tmp_path / ".editorconfig").read_text(
        encoding="utf-8") == sentinel_ec
    merge_rels = {rel for rel, _ in merges}
    assert {"Directory.Build.props", ".editorconfig"} <= merge_rels
    rels = {p.relative_to(tmp_path).as_posix() for p in created}
    assert ".github/workflows/sdlc-dotnet.yml" in rels  # kit-owned still writes
