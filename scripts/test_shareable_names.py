#!/usr/bin/env python3
"""Tests for the shareable resume / cover letter file-name convention.

    python3 scripts/test_shareable_names.py

Convention: `resume_<INITIALS>-<terse company and role>-<YYYY-MM>` and
`cover-letter_<INITIALS>-<terse company and role>-<YYYY-MM>`.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "resume_docx"))
import docx_common as dc  # noqa: E402


class TerseSlug(unittest.TestCase):
    def test_drops_filler_and_abbreviates(self):
        self.assertEqual(dc.terse_slug("acme_head_of_software_development"),
                         "acme-head-sw-dev")

    def test_senior_manager(self):
        self.assertEqual(dc.terse_slug("globex_international_senior_manager_technical_solution_engineer"),
                         "globex-international-sr-mgr-tech-solution-eng")

    def test_vice_president_phrase(self):
        self.assertEqual(dc.terse_slug("initech_holdings_vice_president_product_management"),
                         "initech-holdings-vp-product-mgmt")

    def test_longest_phrase_wins(self):
        self.assertEqual(dc.terse_slug("acme_senior_vice_president_engineering"), "acme-svp-eng")

    def test_company_suffix_dropped(self):
        self.assertEqual(dc.terse_slug("acme_inc_director_of_it"), "acme-dir-it")


class OwnerInitials(unittest.TestCase):
    def _initials(self, heading):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "resume.md"
            p.write_text(f"---\nx: 1\n---\n{heading}\nCity\n", encoding="utf-8")
            return dc.owner_initials(p)

    def test_three_names(self):
        self.assertEqual(self._initials("# Jane Q. Public"), "JQP")

    def test_two_names(self):
        self.assertEqual(self._initials("# Jane Public"), "JP")

    def test_suffix_ignored(self):
        self.assertEqual(self._initials("# Jane Q. Public Jr."), "JQP")

    def test_missing_name_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "resume.md"
            p.write_text("no heading\n", encoding="utf-8")
            with self.assertRaises(dc.DocGenError):
                dc.owner_initials(p)


class ShareableStem(unittest.TestCase):
    def test_resume(self):
        self.assertEqual(
            dc.shareable_stem("resume", "JQP", "acme_head_of_software_development", "2026-10-29"),
            "resume_JQP-acme-head-sw-dev-2026-10")

    def test_cover_letter(self):
        self.assertEqual(
            dc.shareable_stem("cover_letter", "JQP", "acme_head_of_software_development", "2026-10-29"),
            "cover-letter_JQP-acme-head-sw-dev-2026-10")


if __name__ == "__main__":
    unittest.main()
