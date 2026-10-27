"""The interface of one Python file: its public signatures, with no bodies.

`python -m taskcontract interface FILE` prints, in file order, each public
top-level function and class: decorators, the header, and the first line of
the docstring (` ...` after it when the docstring runs on). A class also
prints its annotated public fields and its public methods and `__init__`.
Nothing else prints: no module docstring, assignment, import, private name,
other dunder method, nested class or body.

A file with no interface to read refuses on one stderr line and exits 2.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def main_interface(args) -> int:
    """Print the file's interface; exit 2 on one stderr line when it has none."""
    file = args.file
    path = Path(file)
    refusal = None
    tree = None
    if not file.endswith(".py"):
        refusal = "only a .py file has one"
    elif not path.is_file():
        refusal = "no such file"
    else:
        try:
            tree = ast.parse(path.read_bytes())
        except SyntaxError as exc:
            refusal = f"line {exc.lineno} does not parse: {exc.msg}"
        except OSError:
            refusal = "no such file"
    if refusal is not None:
        print(f"No interface for {file}: {refusal}.", file=sys.stderr)
        return 2
    for line in interface_lines(tree):
        print(line)
    return 0


def interface_lines(tree: ast.Module) -> list[str]:
    """The lines of the module's interface, in file order."""
    lines: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                lines.extend(_function(node, 0))
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            lines.extend(_class(node))
    return lines


def _function(node: ast.FunctionDef | ast.AsyncFunctionDef, indent: int) -> list[str]:
    """A def's decorators, header and docstring line, at the indent."""
    pad = " " * indent
    lines = [f"{pad}@{ast.unparse(decorator)}" for decorator in node.decorator_list]
    word = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    lines.append(f"{pad}{word} {node.name}({ast.unparse(node.args)}){returns}:")
    lines.extend(_docstring(node, indent + 4))
    return lines


def _class(node: ast.ClassDef) -> list[str]:
    """A class's decorators, header and docstring line, then its public fields and methods."""
    lines = [f"@{ast.unparse(decorator)}" for decorator in node.decorator_list]
    bases = [ast.unparse(base) for base in node.bases]
    for keyword in node.keywords:
        value = ast.unparse(keyword.value)
        bases.append(f"{keyword.arg}={value}" if keyword.arg else f"**{value}")
    lines.append(f"class {node.name}({', '.join(bases)}):" if bases else f"class {node.name}:")
    lines.extend(_docstring(node, 4))
    for member in node.body:
        if (isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name)
                and not member.target.id.startswith("_")):
            lines.append(f"    {member.target.id}: {ast.unparse(member.annotation)}")
        elif isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not member.name.startswith("_") or member.name == "__init__":
                lines.extend(_function(member, 4))
    return lines


def _docstring(node: ast.AST, indent: int) -> list[str]:
    """The docstring's first line at the indent, ` ...` after it when more lines follow."""
    doc = ast.get_docstring(node)
    if not doc:
        return []
    first, *rest = doc.splitlines()
    return [f'{" " * indent}"""{first}{" ..." if rest else ""}"""']
