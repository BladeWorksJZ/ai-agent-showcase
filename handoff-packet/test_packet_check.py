"""Tests for packet_check.py. Run: python -m unittest -v

Fake secrets are built at run time (string joins) so this file itself never
contains anything that looks like a real key.
"""

import unittest
from pathlib import Path

from packet_check import check_file, check_text

GOOD = """PACKET ID: DEMO-20261117-01
FROM: Builder Agent
TO: Review Agent
TYPE: request
REPLY TO: none
APPROVAL: 2026-11-17 10:30 not needed

## WHAT I NEED
Review the test page.

## WHAT I NEED BACK
PASS or a list of fixes.

## DO NOT
Publish anything.
"""


def with_line(old: str, new: str) -> str:
    assert old in GOOD
    return GOOD.replace(old, new, 1)


def add_body(extra: str) -> str:
    return GOOD + "\n" + extra + "\n"


class NormalUse(unittest.TestCase):
    def test_good_packet_passes(self):
        self.assertTrue(check_text(GOOD).passed)

    def test_example_file_passes(self):
        here = Path(__file__).parent
        self.assertTrue(check_file(here / "example-packet.md").passed)

    def test_reply_with_reply_to_passes(self):
        text = with_line("TYPE: request", "TYPE: reply")
        text = text.replace("REPLY TO: none", "REPLY TO: DEMO-20261116-03")
        self.assertTrue(check_text(text).passed)


class BadHeader(unittest.TestCase):
    def test_missing_field(self):
        r = check_text(with_line("FROM: Builder Agent\n", ""))
        self.assertFalse(r.passed)

    def test_empty_field(self):
        r = check_text(with_line("TO: Review Agent", "TO:"))
        self.assertIn("line 3: 'TO' is empty", r.reasons)

    def test_bad_packet_id(self):
        r = check_text(with_line("DEMO-20261117-01", "demo-17-1"))
        self.assertFalse(r.passed)

    def test_impossible_date_in_id(self):
        r = check_text(with_line("DEMO-20261117-01", "DEMO-20261341-01"))
        self.assertIn("line 1: packet ID date is not a real date", r.reasons)

    def test_unknown_type(self):
        r = check_text(with_line("TYPE: request", "TYPE: order"))
        self.assertFalse(r.passed)

    def test_reply_without_reply_to(self):
        r = check_text(with_line("TYPE: request", "TYPE: reply"))
        self.assertIn("line 5: a reply must name the packet it answers", r.reasons)

    def test_approval_without_date(self):
        r = check_text(with_line("APPROVAL: 2026-11-17 10:30 not needed", "APPROVAL: not needed"))
        self.assertFalse(r.passed)

    def test_approval_bad_time(self):
        r = check_text(with_line("2026-11-17 10:30", "2026-11-17 25:30"))
        self.assertFalse(r.passed)


class BadBody(unittest.TestCase):
    def test_missing_section(self):
        r = check_text(GOOD.replace("## WHAT I NEED BACK\n", ""))
        self.assertIn("file: missing section '## WHAT I NEED BACK'", r.reasons)

    def test_too_big(self):
        r = check_text(add_body("x" * (21 * 1024)))
        self.assertFalse(r.passed)


class Secrets(unittest.TestCase):
    def assert_blocked(self, line: str):
        r = check_text(add_body(line))
        self.assertFalse(r.passed, line)
        self.assertTrue(any("looks like a secret" in x for x in r.reasons))

    def test_sk_key(self):
        self.assert_blocked("key " + "sk-" + "a1B2" * 6)

    def test_github_token(self):
        self.assert_blocked("ghp" + "_" + "Z9y8" * 6)

    def test_aws_key(self):
        self.assert_blocked("AKIA" + "ABCD1234EFGH5678")

    def test_private_key(self):
        self.assert_blocked("-----BEGIN " + "RSA PRIVATE KEY-----")

    def test_password(self):
        self.assert_blocked("pass" + "word: hunter2")

    def test_reason_has_line_number_not_text(self):
        secret = "sk-" + "Q" * 24
        r = check_text(add_body(secret))
        joined = " ".join(r.reasons)
        self.assertNotIn(secret, joined)
        self.assertRegex(joined, r"line \d+: looks like a secret")

    def test_normal_word_password_is_fine(self):
        r = check_text(add_body("Never ask the client for a password in chat."))
        self.assertTrue(r.passed)


class BrokenInput(unittest.TestCase):
    def test_missing_file(self):
        r = check_file(Path("does-not-exist.md"))
        self.assertFalse(r.passed)

    def test_not_utf8(self, tmp=Path("_not_utf8.md")):
        tmp.write_bytes(b"\xff\xfe\x00bad")
        try:
            self.assertIn("file: not UTF-8 text", check_file(tmp).reasons)
        finally:
            tmp.unlink()

    def test_empty_text(self):
        self.assertFalse(check_text("").passed)


if __name__ == "__main__":
    unittest.main()
