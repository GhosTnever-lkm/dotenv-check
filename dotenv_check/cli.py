"""dotenv-check [ENV] [--example FILE] [--strict] [--ignore KEY] [--json]"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .checks import compare
from .parser import ParseError, parse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dotenv-check", description="Compare .env with .env.example; values are never printed.")
    p.add_argument("env", nargs="?", default=".env", help="env file to check (default: .env)")
    p.add_argument("--example", default=".env.example", help="template file (default: .env.example)")
    p.add_argument("--strict", action="store_true", help="extra keys and warnings are errors")
    p.add_argument("--ignore", action="append", default=[], metavar="KEY", help="skip a template key, e.g. CI_TOKEN (repeatable)")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--version", action="version", version=__version__)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ignored = set(args.ignore)
    try:
        template = parse(Path(args.example).read_text(encoding="utf-8"), args.example)
        template = {k: v for k, v in template.items() if k not in ignored}
        env = parse(Path(args.env).read_text(encoding="utf-8"), args.env)
    except OSError as exc:
        print(f"dotenv-check: {exc.strerror}: {exc.filename}", file=sys.stderr)
        return 2
    except ParseError as exc:
        print(f"dotenv-check: {exc}", file=sys.stderr)
        return 2

    result = compare(template, env, strict_extra=args.strict)
    if args.json:
        print(json.dumps({"findings": [f.__dict__ for f in result.findings], "failed": result.failed}, indent=2))
    else:
        if not result.findings:
            print(f"OK: {args.env} matches {args.example}")
        for f in result.findings:
            print(f"[{f.level.upper()}] {f.code}: {f.key}")
    if args.strict and any(f.level == "warning" for f in result.findings):
        return 1
    return 1 if result.failed else 0
