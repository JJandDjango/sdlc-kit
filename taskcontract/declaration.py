"""The test declaration: the `test:` block of `.sdlc/config.yaml`.

A repository declares how its tests run, each command an argv list to run
with no shell: `command` (the whole suite), `file` (one test file, its path
from the repo root in place of `{file}`) and `build` (to run before
`file`). `read_test` returns the three lists, or None when the repository
declares no test command.

The `wall:` block beside it names what the Developer and QA seats may not
read during a task, each of its four keys (`functional`, `unit`, `code`,
`interface`) an argv-style list of paths, globs or folders (a trailing `/`).
`read_wall` returns the four lists, or None when the repository declares no
`wall:` mapping.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from .g1 import read_config


class Commands(NamedTuple):
    command: list[str]
    file: list[str]
    build: list[str]


def read_test(root: Path) -> Commands | None:
    """The root's `test:` block, or None without a `command` that is a
    non-empty list of non-empty strings; `file` and `build` read as empty
    when absent or malformed."""
    block = read_config(root).get("test")
    if not isinstance(block, dict):
        return None
    command = _argv(block.get("command"))
    if not command:
        return None
    return Commands(command, _argv(block.get("file")), _argv(block.get("build")))


class Wall(NamedTuple):
    functional: list[str]
    unit: list[str]
    code: list[str]
    interface: list[str]


def read_wall(root: Path) -> Wall | None:
    """The root's `wall:` block, or None when it is not a mapping; a key
    reads as empty when absent or malformed."""
    block = read_config(root).get("wall")
    if not isinstance(block, dict):
        return None
    return Wall(*(_argv(block.get(key)) for key in Wall._fields))


def _argv(value: object) -> list[str]:
    """The value as an argv list; anything but a list of non-empty strings is empty."""
    if not isinstance(value, list):
        return []
    if not all(isinstance(item, str) and item for item in value):
        return []
    return list(value)
