"""G1's document stands as a pair (contract: document-split, unit
d6-release, SC4.3).

`docs/features/g1-requirements-spec.md` holds no solution half, so it
stands unchanged as a requirements document, its request half's text and
signature as they were. Its design document stands beside it, and its
first revision row, r1, is a text row that names requirements r3.

The tests which read the kit's own tree, its pane and USAGE's drawing
retired when the engineer seat signed G1's design, because they pinned the
pair as it stood before that signature.

The design document's own words are a seat's: no test here reads its
seat's name, its date or a section of it.

The test reads the two documents and runs no model.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

_HERE = Path(__file__).resolve().parent.parent
# Beside a tree that holds the skill, read that tree; a copy run from any
# other folder reads the tree pytest was started in.
ROOT = _HERE if (_HERE / "skills" / "sdlc").is_dir() else Path.cwd()

G1 = "g1-requirements-spec"
REQUIREMENTS = f"docs/features/{G1}.md"
DESIGN = f"docs/features/{G1}.design.md"
# sha256 of the requirements document's text, read as UTF-8 text: the build
# changes no byte of it.
REQUIREMENTS_TEXT = "eb81d41780bae6fde7a37dfcc45f922540f450370d520623c10d00434f0399f3"
STATUS_ROWS = ("Ready:", "Measured:", "Signed:", "Parked:")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _table(text: str) -> list[list[str]]:
    """The rows of a document's first table, each as its cells, the header
    and the rule below it left out."""
    rows = []
    for line in text.splitlines():
        if line.startswith("|"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif rows:
            break
    return rows[2:]


# --- SC4.3: the two documents ----------------------------------------------------

def test_sc4_3_g1s_design_document_stands_at_r1_against_requirements_r3_beside_an_unchanged_request_half():
    assert (ROOT / DESIGN).is_file(), f"no design document at {DESIGN}"
    rows = _table(_read(ROOT / DESIGN))
    assert rows, "the design document opens on no revision table"
    first = rows[0][-1]
    # r1 is a text row, and it names the requirements revision the design stands against.
    assert first.startswith("r1: ")
    assert not first[len("r1: "):].startswith(STATUS_ROWS)
    assert re.search(r"\brequirements r3\b", first), first
    # The requirements document keeps its text, its signature row among it.
    text = _read(ROOT / REQUIREMENTS)
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == REQUIREMENTS_TEXT
    assert "## Proposed solution" not in text
