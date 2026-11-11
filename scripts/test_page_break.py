#!/usr/bin/env python3
"""Tests for the manual `<!-- page-break -->` directive in resume markdown.

    python3 scripts/test_page_break.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "resume_docx"))
import docx_common as dc  # noqa: E402
import resume_docx as rd  # noqa: E402

LINES = """### Acme - Engineer
**Jan 2020 – Jan 2021 | Austin, TX**
- Did a thing.

<!-- page-break -->
### Globex - Lead
**Jan 2018 – Jan 2019 | Austin, TX**
- Did another thing.
""".splitlines()


def unit(force=False, height=100.0):
    return dc.LayoutUnit(section="", is_section_start=False, height_pt=height,
                         paragraphs=[], force_break_before=force)


def plan(units, page_height=1000.0):
    return dc.simulate_pagination(units, page_height, metrics=None, styles={}, width_pt=500,
                                  tighten_factor=1.0, tightenable_keys=frozenset())


class Parser(unittest.TestCase):
    def test_directive_marks_next_entry_only(self):
        entries = rd._parse_experience(LINES)
        self.assertEqual([e.page_break_before for e in entries], [False, True])

    def test_directive_is_not_description_text(self):
        entries = rd._parse_experience(LINES)
        self.assertNotIn("page-break", " ".join(entries[0].bullets + entries[0].description))


class Planner(unittest.TestCase):
    def test_forced_break_mid_page(self):
        p = plan([unit(), unit(), unit(force=True), unit()])
        self.assertEqual(p.pages_used, 2)
        self.assertEqual(list(p.breaks_before), [2])

    def test_forced_break_at_page_top_is_skipped(self):
        # Page holds exactly two units, so the third already starts page 2.
        p = plan([unit(height=500), unit(height=496), unit(force=True, height=100)], page_height=1000.0)
        self.assertEqual(p.pages_used, 2)
        self.assertEqual(list(p.breaks_before), [2])

    def test_no_directive_no_break(self):
        self.assertEqual(plan([unit(), unit(), unit()]).pages_used, 1)


if __name__ == "__main__":
    unittest.main()
