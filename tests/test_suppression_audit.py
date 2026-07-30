"""Fixture corpus for the G4.10 four-vector suppression audit."""

from __future__ import annotations

import json
import subprocess

import pytest

from taskcontract.__main__ import main
from taskcontract.suppression_audit import audit_diff_text, parse_diff, resolve_base


def one_file_diff(path, added=(), removed=()):
    lines = [f"diff --git a/{path} b/{path}",
             f"--- a/{path}", f"+++ b/{path}",
             f"@@ -10,{len(removed)} +10,{len(added)} @@"]
    lines += [f"-{text}" for text in removed]
    lines += [f"+{text}" for text in added]
    return "\n".join(lines) + "\n"


def vectors(findings):
    return sorted({f.vector for f in findings})


# --- V1: in-source suppression constructs ---

@pytest.mark.parametrize("added", [
    "#pragma warning disable CA2000",
    "    [SuppressMessage(\"Design\", \"CA1062\")]",
    "[assembly: SuppressMessage(\"Style\", \"SA1101\")]",
    "// Stryker disable all",
    "    [Fact(Skip = \"flaky on CI\")]",
    "    [Ignore(\"broken\")]",
])
def test_v1_in_source_constructs_trip(added):
    findings = audit_diff_text(one_file_diff("src/Service.cs", [added]))
    assert vectors(findings) == [1]
    assert "PL-PIPE.1" in findings[0].line


def test_v1_global_suppressions_file_trips_on_any_addition():
    diff = one_file_diff("src/GlobalSuppressions.cs",
                         ["[assembly: System.Something]"])
    findings = audit_diff_text(diff)
    assert vectors(findings) == [1]
    assert "GlobalSuppressions.cs" in findings[0].construct


def test_v1_removing_a_pragma_is_clean():
    diff = one_file_diff("src/Service.cs",
                         removed=["#pragma warning disable CA2000"])
    assert audit_diff_text(diff) == []


# --- V2: severity downgrades in analysis config ---

def test_v2_paired_downgrade_trips():
    diff = one_file_diff(
        ".editorconfig",
        added=["dotnet_diagnostic.CA2000.severity = suggestion"],
        removed=["dotnet_diagnostic.CA2000.severity = error"])
    findings = audit_diff_text(diff)
    assert vectors(findings) == [2]
    assert "error -> suggestion" in findings[0].line


def test_v2_unpaired_weak_introduction_trips():
    diff = one_file_diff(".globalconfig",
                         added=["dotnet_diagnostic.SA1101.severity = none"])
    findings = audit_diff_text(diff)
    assert vectors(findings) == [2]
    assert "introduced at none" in findings[0].line


def test_v2_tightening_and_strong_introduction_pass():
    tighten = one_file_diff(
        ".editorconfig",
        added=["dotnet_diagnostic.CA2000.severity = error"],
        removed=["dotnet_diagnostic.CA2000.severity = suggestion"])
    strong = one_file_diff(
        ".editorconfig",
        added=["dotnet_diagnostic.IDE0055.severity = warning"])
    assert audit_diff_text(tighten) == []
    assert audit_diff_text(strong) == []


def test_v2_severity_syntax_outside_config_files_is_clean():
    diff = one_file_diff("docs/notes.md",
                         added=["dotnet_diagnostic.CA2000.severity = none"])
    assert audit_diff_text(diff) == []


# --- V3: strictness-flag weakening in build config ---

@pytest.mark.parametrize("added,construct", [
    ("    <TreatWarningsAsErrors>false</TreatWarningsAsErrors>",
     "<TreatWarningsAsErrors>false"),
    ("    <Nullable>disable</Nullable>", "<Nullable>disable"),
    ("    <RunAnalyzers>false</RunAnalyzers>", "<RunAnalyzers>false"),
    ("    <AnalysisLevel>latest-recommended</AnalysisLevel>",
     "<AnalysisLevel>latest-recommended"),
    ("    <NuGetAudit>false</NuGetAudit>", "<NuGetAudit>false"),
])
def test_v3_weak_flag_values_trip(added, construct):
    findings = audit_diff_text(one_file_diff("Directory.Build.props", [added]))
    assert vectors(findings) == [3]
    assert construct in findings[0].construct


def test_v3_nowarn_addition_trips():
    diff = one_file_diff("src/App/App.csproj",
                         added=["    <NoWarn>$(NoWarn);CA2000</NoWarn>"])
    findings = audit_diff_text(diff)
    assert vectors(findings) == [3]


def test_v3_strong_values_pass():
    diff = one_file_diff("Directory.Build.props", added=[
        "    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>",
        "    <Nullable>enable</Nullable>",
        "    <AnalysisLevel>latest-all</AnalysisLevel>",
    ])
    assert audit_diff_text(diff) == []


# --- V4: exclusion-scope widening ---

def test_v4_generated_code_glob_trips():
    diff = one_file_diff(".editorconfig", added=["generated_code = true"])
    findings = audit_diff_text(diff)
    assert vectors(findings) == [4]


def test_v4_exclude_from_code_coverage_trips():
    diff = one_file_diff("src/Service.cs",
                         added=["    [ExcludeFromCodeCoverage]"])
    findings = audit_diff_text(diff)
    assert vectors(findings) == [4]


def test_v4_quarantine_list_addition_trips():
    diff = one_file_diff(".sdlc/test-quarantine.txt",
                         added=["Flaky.Integration.LoginTest"])
    findings = audit_diff_text(diff)
    assert vectors(findings) == [4]


# --- parsing, diagnostics, clean runs ---

def test_clean_diff_has_no_findings():
    diff = one_file_diff("src/Service.cs", added=[
        "public int Add(int a, int b) => a + b;",
        "// a normal comment",
    ])
    assert audit_diff_text(diff) == []


def test_added_line_numbers_come_from_hunk_headers():
    diff = one_file_diff("src/Service.cs",
                         added=["var x = 1;", "#pragma warning disable CA2000"])
    findings = audit_diff_text(diff)
    assert findings[0].line_no == 11  # hunk starts at 10; second added line


def test_finding_line_names_vector_location_and_route():
    findings = audit_diff_text(
        one_file_diff("src/Service.cs", ["#pragma warning disable CA2000"]))
    text = findings[0].line
    assert text.startswith("G410-V1 src/Service.cs:10:")
    assert "route:" in text


def test_multi_vector_diff_reports_each():
    diff = (one_file_diff("src/Service.cs", ["#pragma warning disable CA2000"])
            + one_file_diff(".editorconfig",
                            ["dotnet_diagnostic.CA2000.severity = none"])
            + one_file_diff("Directory.Build.props",
                            ["    <Nullable>disable</Nullable>"]))
    assert vectors(audit_diff_text(diff)) == [1, 2, 3]


def test_resolve_base_requires_event(monkeypatch):
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    with pytest.raises(ValueError, match="--base"):
        resolve_base()


def test_resolve_base_reads_pull_request_event(tmp_path, monkeypatch):
    event = tmp_path / "event.json"
    event.write_text(json.dumps(
        {"pull_request": {"base": {"sha": "abc123"}}}), encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    assert resolve_base() == "abc123"


def test_resolve_base_rejects_zero_sha(tmp_path, monkeypatch):
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"before": "0" * 40}), encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    with pytest.raises(ValueError, match="no diffable base"):
        resolve_base()


# --- CLI integration over a real repository ---

def _git(repo, *argv):
    subprocess.run(["git", "-C", str(repo), *argv], check=True,
                   capture_output=True, encoding="utf-8", errors="replace")


@pytest.fixture()
def audit_repo(tmp_path):
    repo = tmp_path / "consumer"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "Service.cs").write_text("public class Service { }\n",
                                     encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "--quiet", "-m", "base")
    return repo


def _head(repo) -> str:
    out = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                         capture_output=True, check=True,
                         encoding="utf-8", errors="replace")
    return out.stdout.strip()


def test_cli_green_and_red_paths(audit_repo, capsys):
    base = _head(audit_repo)
    (audit_repo / "Service.cs").write_text(
        "public class Service { public int X; }\n", encoding="utf-8")
    _git(audit_repo, "add", ".")
    _git(audit_repo, "commit", "--quiet", "-m", "clean change")

    rc = main(["suppression-audit", "--base", base,
               "--repo", str(audit_repo)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "suppression-green" in out

    (audit_repo / "Service.cs").write_text(
        "#pragma warning disable CA2000\npublic class Service { }\n",
        encoding="utf-8")
    _git(audit_repo, "add", ".")
    _git(audit_repo, "commit", "--quiet", "-m", "suppress")

    rc = main(["suppression-audit", "--base", base,
               "--repo", str(audit_repo)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "G410-V1" in out


def test_cli_json_shape(audit_repo, capsys):
    base = _head(audit_repo)
    (audit_repo / "Service.cs").write_text(
        "#pragma warning disable CA2000\npublic class Service { }\n",
        encoding="utf-8")
    _git(audit_repo, "add", ".")
    _git(audit_repo, "commit", "--quiet", "-m", "suppress")

    rc = main(["suppression-audit", "--base", base, "--json",
               "--repo", str(audit_repo)])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert payload[0]["vector"] == 1
    assert payload[0]["file"] == "Service.cs"


def test_cli_missing_base_is_environment_error(audit_repo, capsys,
                                               monkeypatch):
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    rc = main(["suppression-audit", "--repo", str(audit_repo)])
    out = capsys.readouterr().out
    assert rc == 2
    assert "--base" in out
