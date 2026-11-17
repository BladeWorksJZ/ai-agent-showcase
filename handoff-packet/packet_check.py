"""Check a handoff packet before it moves between agent systems.

Usage:  python packet_check.py <packet.md> [<packet.md> ...]
Exit code 0 = every packet PASSED, 1 = at least one STOPPED, 2 = usage error.

Reports reasons with line numbers only. It never prints packet text, so a secret
that slipped into a packet can't leak into a log.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

MAX_BYTES = 20 * 1024

HEADER_FIELDS = ["PACKET ID", "FROM", "TO", "TYPE", "REPLY TO", "APPROVAL"]
TYPES = {"request", "reply", "info"}
REQUIRED_SECTIONS = ["## WHAT I NEED", "## WHAT I NEED BACK"]

PACKET_ID_RE = re.compile(r"^[A-Z]{2,10}-(\d{8})-\d{2}$")
APPROVAL_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s+\S")

# Patterns that look like secrets. Kept broad on purpose: a false alarm costs a
# resend, a missed key costs a rotation.
SECRET_PATTERNS = [
    ("API key (sk-)", re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("password value", re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*\S+")),
    ("secret/token value", re.compile(r"(?i)\b(api[_ ]?key|secret|token)\s*[:=]\s*[A-Za-z0-9_\-]{12,}")),
]


@dataclass
class Result:
    path: str
    reasons: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.reasons

    def stop(self, line: int | None, reason: str) -> None:
        where = f"line {line}" if line else "file"
        self.reasons.append(f"{where}: {reason}")


def _real_date(text: str, fmt: str) -> bool:
    try:
        datetime.strptime(text, fmt)
        return True
    except ValueError:
        return False


def check_text(text: str, path: str = "<packet>") -> Result:
    result = Result(path)

    if len(text.encode("utf-8")) > MAX_BYTES:
        result.stop(None, f"over {MAX_BYTES // 1024} KB")

    lines = text.splitlines()

    # Header: the first six lines, in order.
    values: dict[str, str] = {}
    for i, name in enumerate(HEADER_FIELDS):
        line_no = i + 1
        line = lines[i] if i < len(lines) else ""
        prefix = f"{name}:"
        if not line.startswith(prefix):
            result.stop(line_no, f"expected header field '{name}'")
            continue
        value = line[len(prefix):].strip()
        if not value:
            result.stop(line_no, f"'{name}' is empty")
        values[name] = value

    packet_id = values.get("PACKET ID", "")
    if packet_id:
        m = PACKET_ID_RE.match(packet_id)
        if not m:
            result.stop(1, "packet ID must look like PREFIX-YYYYMMDD-NN")
        elif not _real_date(m.group(1), "%Y%m%d"):
            result.stop(1, "packet ID date is not a real date")

    ptype = values.get("TYPE", "")
    if ptype and ptype not in TYPES:
        result.stop(4, "TYPE must be request, reply or info")

    if ptype == "reply" and values.get("REPLY TO", "").lower() == "none":
        result.stop(5, "a reply must name the packet it answers")

    approval = values.get("APPROVAL", "")
    if approval:
        m = APPROVAL_RE.match(approval)
        if not m or not _real_date(m.group(1), "%Y-%m-%d %H:%M"):
            result.stop(6, "APPROVAL must start with 'YYYY-MM-DD HH:MM' then who approved")

    stripped = [ln.strip() for ln in lines]
    for section in REQUIRED_SECTIONS:
        if section not in stripped:
            result.stop(None, f"missing section '{section}'")

    for n, line in enumerate(lines, start=1):
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                result.stop(n, f"looks like a secret ({label})")
                break

    return result


def check_file(path: Path) -> Result:
    try:
        data = path.read_bytes()
    except OSError as exc:
        r = Result(str(path))
        r.stop(None, f"can't read file ({exc.__class__.__name__})")
        return r
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        r = Result(str(path))
        r.stop(None, "not UTF-8 text")
        return r
    return check_text(text, str(path))


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[2])
        return 2
    all_passed = True
    for arg in argv:
        r = check_file(Path(arg))
        print(f"{'PASS' if r.passed else 'STOP'}  {r.path}")
        for reason in r.reasons:
            print(f"      {reason}")
        all_passed = all_passed and r.passed
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
