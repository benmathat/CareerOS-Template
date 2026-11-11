#!/usr/bin/env python3
"""Tests for the opportunity index (scripts/opp_index.py), stdlib only.

    python3 scripts/test_opp_index.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import opp_index as oi  # noqa: E402

TRACKS = "| `track-2` | Product Leadership | x |\n| `track-9` | Opportunistic | x |\n"


def make(root, name, company, track, added, extra=()):
    d = root / "opps" / name
    d.mkdir(parents=True)
    (d / "job-opportunity.md").write_text(
        f"---\ncompany: {company}\nrole: R | x\nstatus: intake\ndate_added: {added}\ntrack: {track}\n---\n# x\n")
    for f in extra:
        (d / f).write_text("x")


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.root = Path(self.t.name)
        (self.root / "Career/04_Career_Goals_and_Strategy").mkdir(parents=True)
        (self.root / oi.TRACKS_FILE).write_text(TRACKS)
        make(self.root, "a_2026-01-01", "A", "track-9", "2026-01-01")
        make(self.root, "b_2026-02-01", "B", "track-2", "2026-02-01", ["analysis.md"])
        make(self.root, "c_2026-03-01", "C", "track-2", "2026-03-01")
        make(self.root, "d_2026-04-01", "D", "MISSING", "2026-04-01")

    def tearDown(self):
        self.t.cleanup()

    def test_grouping_order_and_sorting(self):
        out = oi.render(self.root, "opps")
        order = [out.index(h) for h in ("Product Leadership (2)", "Opportunistic (1)", "Unrouted")]
        self.assertEqual(order, sorted(order))
        self.assertLess(out.index("[C]"), out.index("[B]"))  # newest first
        self.assertIn("analysis", out)
        self.assertIn("R \\| x", out)  # pipes escaped

    def test_write_is_idempotent_and_preserves_prose(self):
        readme = self.root / "opps" / "README.md"
        readme.write_text("# Intro\n\nkeep me\n")
        self.assertEqual(oi.run(self.root, "opps", ["--check"]), 1)
        oi.run(self.root, "opps", ["--write"])
        first = readme.read_text()
        self.assertIn("keep me", first)
        oi.run(self.root, "opps", ["--write"])
        self.assertEqual(first, readme.read_text())
        self.assertEqual(oi.run(self.root, "opps", ["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
