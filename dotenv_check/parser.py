"""Minimal .env parser: KEY=VALUE lines, comments, optional 'export ' prefix and quotes."""

from __future__ import annotations

import re
from dataclasses import dataclass

_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")


@dataclass(frozen=True)
class Entry:
    key: str
    value: str
    line: int


class ParseError(ValueError):
    pass


def parse(text: str, source: str = "<input>") -> dict[str, Entry]:
    """Return {key: Entry}. Later duplicates are reported via ParseError."""
    entries: dict[str, Entry] = {}
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            raise ParseError(f"{source}:{number}: line has no '=' sign")
        key, value = line.split("=", 1)
        key = key.strip()
        if not _KEY_RE.match(key):
            raise ParseError(f"{source}:{number}: invalid key {key!r}")
        if key in entries:
            raise ParseError(f"{source}:{number}: duplicate key {key} (first at line {entries[key].line})")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        entries[key] = Entry(key=key, value=value, line=number)
    return entries
