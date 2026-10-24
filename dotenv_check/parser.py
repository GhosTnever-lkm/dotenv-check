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
        if value.startswith(("\"", "'")):
            quote = value[0]
            end = None
            for index in range(1, len(value)):
                if value[index] != quote:
                    continue
                backslashes = 0
                cursor = index - 1
                while cursor > 0 and value[cursor] == "\\":
                    backslashes += 1
                    cursor -= 1
                if quote != '"' or backslashes % 2 == 0:
                    end = index
                    break
            if end is None:
                raise ParseError(f"{source}:{number}: unterminated quoted value for {key}")
            trailing = value[end + 1:].strip()
            if trailing and not trailing.startswith("#"):
                raise ParseError(f"{source}:{number}: unexpected text after quoted value for {key}")
            value = value[1:end]
        else:
            comment = re.search(r"\s+#", value)
            if comment:
                value = value[:comment.start()].rstrip()
        entries[key] = Entry(key=key, value=value, line=number)
    return entries
