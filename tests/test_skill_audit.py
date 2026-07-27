"""Report-only audit suite for the /sdlc audit engine (ADR 0016)."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from taskcontract.scaffold import scaffold

ANSWERS = {"project_name": "demo", "material": "greenfield", "stack": "python"}

VALID_DOC = {
    "id": "demo-task",
    "intent": ("Orders export as CSV from the billing screen; the download "
               "completes for accounts with zero orders."),
    "scope": ["billing/export/"],
    "non_goals": ["PDF export"],
    "decomposition": [{
        "unit": "export endpoint",
        "done_means": "GET /billing/export returns CSV",
        "acceptance_sketch": ["zero-order account downloads an empty CSV"],
    }],
    "dependencies": [],
    "provenance": {"origin": "human-request"},
}


def _init(tmp_path, skill_init):
    templates = Path(skill_init.__file__).parent / "templates"
    skill_init.render_all(ANSWERS, templates, tmp_path, "2026-07-26")


def _write_contract(tmp_path, doc):
    path = tmp_path / "specs" / doc["id"] / "contract.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def test_no_spine_exits_2(tmp_path, skill_audit, capsys):
    assert skill_audit.main(["--cwd", str(tmp_path)]) == 2
    assert "No SDLC gate spine" in capsys.readouterr().err


def test_fresh_init_is_clean(tmp_path, skill_init, skill_audit, capsys):
    _init(tmp_path, skill_init)
    assert skill_audit.main(["--cwd", str(tmp_path)]) == 0
    assert "clean" in capsys.readouterr().out


def test_red_skeleton_is_invalid_then_filled_is_clean(tmp_path, skill_init, skill_audit, capsys):
    _init(tmp_path, skill_init)
    scaffold("demo-task", root=tmp_path)
    assert skill_audit.main(["--cwd", str(tmp_path)]) == 1
    assert "CONTRACT-INVALID" in capsys.readouterr().out

    _write_contract(tmp_path, VALID_DOC)  # overwrite-in-test: fills the skeleton
    assert skill_audit.main(["--cwd", str(tmp_path)]) == 0


def test_parked_draft_reads_info_not_error(tmp_path, skill_init, skill_audit, capsys):
    _init(tmp_path, skill_init)
    doc = dict(VALID_DOC)
    doc["dependencies"] = [{"ref": "schema-migration", "status": "blocked",
                            "blocked_by": "auth-rework"}]
    _write_contract(tmp_path, doc)
    assert skill_audit.main(["--cwd", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "CONTRACT-PARKED" in out and "schema-migration" in out


def test_orphan_dir_and_id_mismatch_warn(tmp_path, skill_init, skill_audit, capsys):
    _init(tmp_path, skill_init)
    (tmp_path / "specs" / "empty-task").mkdir(parents=True)
    doc = dict(VALID_DOC)
    doc["id"] = "other-name"
    path = tmp_path / "specs" / "demo-task" / "contract.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")

    assert skill_audit.main(["--cwd", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "CONTRACT-ORPHAN" in out and "ID-MISMATCH" in out


def test_broken_ledger_yaml_errors(tmp_path, skill_init, skill_audit, capsys):
    _init(tmp_path, skill_init)
    (tmp_path / ".sdlc" / "reds.yaml").write_text("reds: [unclosed", encoding="utf-8")
    assert skill_audit.main(["--cwd", str(tmp_path)]) == 1
    assert "REDS-PARSE" in capsys.readouterr().out


def test_json_format_parses(tmp_path, skill_init, skill_audit, capsys):
    _init(tmp_path, skill_init)
    scaffold("demo-task", root=tmp_path)
    skill_audit.main(["--cwd", str(tmp_path), "--format", "json"])
    findings = json.loads(capsys.readouterr().out)
    assert any(f["code"] == "CONTRACT-INVALID" for f in findings)
