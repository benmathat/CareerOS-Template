#!/usr/bin/env python3
"""Tests for the lapsed-applications report (scripts/lapsed.py), stdlib only.

    python3 scripts/test_lapsed.py
"""
import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lapsed as lp  # noqa: E402

TODAY = dt.date(2026, 11, 6)
HDR = "## Active Applications\n\n| ID | Company | Role | Location | Source | Referral | Status | Last Action | Next Action | Resume |\n|---|---|---|---|---|---|---|---|---|---|\n"


def row(i, status, last, folder=""):
    return f"| {i} | Co | Role | X | Y | — | {status} | {last} {folder} | n | r |\n"


class LapsedTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.root = Path(self.t.name)
        (self.root / "opps/acme_role_2026-09-01").mkdir(parents=True)
        (self.root / "opps/acme_role_2026-09-01/application-record.md").write_text("submission_date: 2026-09-02\n")
        (self.root / "log.md").write_text(
            "```yaml\nactivity_date: 2026-10-20\nrelated_opportunity: ../opps/acme_role_2026-09-01/job-opportunity.md\n```\n")
        (self.root / "tracker.md").write_text(
            HDR
            + row("A-1-2026-09-01", "Applied", "2026-09-02:", "acme_role_2026-09-01")
            + row("B-1-2026-10-01", "Applied", "2026-10-01:")
            + row("C-1-2026-09-01", "Identified", "2026-09-01:")
            + row("D-1-2026-09-01", "Applied", "2026-12-25 future")
            + "\n## Follow-Ups Due\n")

    def tearDown(self):
        self.t.cleanup()

    def test_log_entry_resets_clock_and_identified_is_excluded(self):
        rows = {r["id"]: r for r in lp.find(self.root, "opps", "tracker.md", "log.md", TODAY)}
        self.assertEqual(set(rows), {"A-1-2026-09-01", "B-1-2026-10-01", "D-1-2026-09-01"})
        self.assertEqual(rows["A-1-2026-09-01"]["last"], dt.date(2026, 10, 20))  # log beats submission
        self.assertEqual(rows["B-1-2026-10-01"]["days"], 36)
        self.assertIsNone(rows["D-1-2026-09-01"]["last"])  # future date ignored

    def test_threshold(self):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            lp.run(self.root, "opps", "tracker.md", "log.md", ["--days", "30"], TODAY)
        out = buf.getvalue()
        self.assertIn("B-1-2026-10-01", out)
        self.assertNotIn("A-1-2026-09-01", out)  # 17 days


if __name__ == "__main__":
    unittest.main()
