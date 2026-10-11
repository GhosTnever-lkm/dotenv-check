import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from dotenv_check.checks import compare
from dotenv_check.cli import main
from dotenv_check.parser import ParseError, parse


def write(tmp: Path, name: str, text: str) -> str:
    path = tmp / name
    path.write_text(text, encoding="utf-8")
    return str(path)


class ParserTests(unittest.TestCase):
    def test_parses_comments_export_and_quotes(self):
        entries = parse('# c\n\nexport A=1\nB="two words"\nC=\'x\'\n')
        self.assertEqual(entries["A"].value, "1")
        self.assertEqual(entries["B"].value, "two words")
        self.assertEqual(entries["C"].value, "x")

    def test_duplicate_key_is_error(self):
        with self.assertRaises(ParseError):
            parse("A=1\nA=2\n")

    def test_invalid_line_is_error(self):
        with self.assertRaises(ParseError):
            parse("NOT A PAIR\n")

    def test_value_may_contain_equals(self):
        self.assertEqual(parse("URL=postgres://u:p@h/db?x=1")["URL"].value, "postgres://u:p@h/db?x=1")


class CompareTests(unittest.TestCase):
    def test_missing_and_empty_are_errors(self):
        tpl = parse("A=\nB=\n")
        env = parse("A=\n")
        codes = {(f.code, f.key) for f in compare(tpl, env).findings}
        self.assertIn(("MISSING_KEY", "B"), codes)
        self.assertIn(("EMPTY_VALUE", "A"), codes)

    def test_placeholder_is_warning(self):
        result = compare(parse("A=\n"), parse("A=changeme\n"))
        self.assertEqual([(f.level, f.code) for f in result.findings], [("warning", "PLACEHOLDER_VALUE")])
        self.assertFalse(result.failed)

    def test_extra_key_is_warning_unless_strict(self):
        self.assertFalse(compare(parse("A=1\n"), parse("A=1\nX=2\n")).failed)
        self.assertTrue(compare(parse("A=1\n"), parse("A=1\nX=2\n"), strict_extra=True).failed)

    def test_findings_never_contain_values(self):
        result = compare(parse("A=1\n"), parse("A=\nX=supersecret\n"))
        blob = json.dumps([f.__dict__ for f in result.findings])
        self.assertNotIn("supersecret", blob)


class CliTests(unittest.TestCase):
    def run_cli(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = main(argv)
        return code, buf.getvalue()

    def test_ok_exit_zero(self):
        tmp = Path(tempfile.mkdtemp())
        ex = write(tmp, ".env.example", "A=\n")
        env = write(tmp, ".env", "A=real\n")
        code, out = self.run_cli([env, "--example", ex])
        self.assertEqual(code, 0)
        self.assertIn("OK", out)

    def test_missing_key_exit_one(self):
        tmp = Path(tempfile.mkdtemp())
        ex = write(tmp, ".env.example", "A=\nB=\n")
        env = write(tmp, ".env", "A=real\n")
        code, out = self.run_cli([env, "--example", ex])
        self.assertEqual(code, 1)
        self.assertIn("MISSING_KEY: B", out)

    def test_parse_error_exit_two(self):
        tmp = Path(tempfile.mkdtemp())
        ex = write(tmp, ".env.example", "A=\n")
        env = write(tmp, ".env", "broken line\n")
        with contextlib.redirect_stderr(io.StringIO()):
            code, _ = self.run_cli([env, "--example", ex])
        self.assertEqual(code, 2)

    def test_missing_file_exit_two(self):
        with contextlib.redirect_stderr(io.StringIO()):
            code, _ = self.run_cli(["/nope/.env", "--example", "/nope/.env.example"])
        self.assertEqual(code, 2)

    def test_ignore_skips_template_key(self):
        tmp = Path(tempfile.mkdtemp())
        ex = write(tmp, ".env.example", "A=\nCI_TOKEN=\n")
        env = write(tmp, ".env", "A=real\n")
        self.assertEqual(self.run_cli([env, "--example", ex])[0], 1)
        self.assertEqual(self.run_cli(["--ignore", "CI_TOKEN", env, "--example", ex])[0], 0)

    def test_json_output(self):
        tmp = Path(tempfile.mkdtemp())
        ex = write(tmp, ".env.example", "A=\n")
        env = write(tmp, ".env", "A=\n")
        code, out = self.run_cli(["--json", env, "--example", ex])
        data = json.loads(out)
        self.assertTrue(data["failed"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
