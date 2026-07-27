"""Round-trip suite for the F11 scaffold (ADR 0016).

`new <id>` writes a deliberately red skeleton - TC007 on the TODO intent
is the tripwire - that turns green only once a real contract is authored.
"""

from __future__ import annotations

import pytest
import yaml

from taskcontract.__main__ import main
from taskcontract.checker import validate_path
from taskcontract.scaffold import scaffold


def test_new_round_trip_fill_then_green(tmp_path):
    path = scaffold("csv-export", root=tmp_path)
    assert path == tmp_path / "specs" / "csv-export" / "contract.yaml"

    rules = {v.rule for v in validate_path(path, profile="ready")}
    assert rules == {"TC007"}, "fresh skeleton must be red on exactly the intent tripwire"

    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    doc["intent"] = ("Orders export as CSV from the billing screen; the download "
                     "completes for accounts with zero orders.")
    doc["scope"] = ["billing/export/"]
    doc["non_goals"] = ["PDF export"]
    doc["decomposition"] = [{
        "unit": "export endpoint",
        "done_means": "GET /billing/export returns CSV",
        "acceptance_sketch": ["zero-order account downloads an empty CSV"],
    }]
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    assert validate_path(path, profile="ready") == []


def test_new_rejects_bad_id(tmp_path):
    with pytest.raises(ValueError):
        scaffold("Bad_Id", root=tmp_path)
    assert not (tmp_path / "specs").exists()


def test_new_refuses_clobber(tmp_path):
    scaffold("csv-export", root=tmp_path)
    with pytest.raises(FileExistsError):
        scaffold("csv-export", root=tmp_path)


def test_cli_new_exit_codes(tmp_path, capsys):
    assert main(["new", "csv-export", "--root", str(tmp_path)]) == 0
    assert (tmp_path / "specs" / "csv-export" / "contract.yaml").exists()
    out = capsys.readouterr().out
    assert "created" in out

    assert main(["new", "csv-export", "--root", str(tmp_path)]) == 1
    assert "already exists" in capsys.readouterr().err
