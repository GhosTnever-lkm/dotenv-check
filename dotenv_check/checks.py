"""Compare an env file against a template. Values are never included in findings."""

from __future__ import annotations

from dataclasses import dataclass, field

from .parser import Entry

PLACEHOLDER_HINTS = ("changeme", "your_", "your-", "<", "xxx", "todo", "replace_me")


@dataclass
class Finding:
    level: str  # error | warning
    code: str
    key: str


@dataclass
class Result:
    findings: list[Finding] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return any(f.level == "error" for f in self.findings)


def compare(template: dict[str, Entry], env: dict[str, Entry], strict_extra: bool = False) -> Result:
    result = Result()
    for key in sorted(template):
        if key not in env:
            result.findings.append(Finding("error", "MISSING_KEY", key))
            continue
        value = env[key].value
        if value == "":
            result.findings.append(Finding("error", "EMPTY_VALUE", key))
        elif any(hint in value.lower() for hint in PLACEHOLDER_HINTS):
            result.findings.append(Finding("warning", "PLACEHOLDER_VALUE", key))
    for key in sorted(set(env) - set(template)):
        level = "error" if strict_extra else "warning"
        result.findings.append(Finding(level, "EXTRA_KEY", key))
    return result
