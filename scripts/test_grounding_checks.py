#!/usr/bin/env python3
"""Tests for claim-grounding checks (scripts/grounding_checks.py), stdlib only.

    python3 scripts/test_grounding_checks.py
"""
import shutil
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import grounding_checks as g  # noqa: E402

ROLE = """---
Last Update: 2026-10-08
---

# Acme Corp - VP of Product

- **Company:** Acme Corp.
- **Title:** Vice President of Product
- **Timeframe:** March 2010 – June 2015

Grew the team to **40+** people and revenue by 25%. Saved $90,000 per month.
"""
RESUME = """# Name
Town, TX · a@example.com

## Summary
Leader with 10+ years building teams.

## Professional Experience

### Acme Corp - Vice President of Product
**Mar 2010 – Jun 2015 | Houston, TX**
- Grew the team to **40+** people and revenue **25%**; avoided **$90K** per month.
"""

INVENTORY = """# Skills

### Certifications
- **Pragmatic Marketing Certified** - Pragmatic Institute
- **Certified Scrum Master (CSM)** - CollabNet

## Education

- **Bachelor of Science in Biology** - Northern Kentucky University (Class of 2001)
- **Independent Study in Computer Science** - Southern Illinois University Edwardsville (2000-2002)
"""
CREDS = """
## Education
### Northern Kentucky University
**Bachelor of Science in Biology**
*2001*
### Southern Illinois University Edwardsville
*Independent Study in Computer Science, 2000–2002*

## Professional Development
- **Pragmatic Marketing Certified** - Pragmatic Institute
- **Certified Scrum Master (CSM)** - CollabNet
"""


class Grounding(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "Career/02_Work_Experience/Roles").mkdir(parents=True)
        (self.d / "Career/02_Work_Experience/Roles/acme.md").write_text(ROLE)
        for s in g.CANON_DIRS[1:]:
            (self.d / "Career" / s).mkdir(parents=True)
        (self.d / "Career/03_Skills_and_Portfolio/skills-inventory.md").write_text(INVENTORY)
        self.opp = self.d / "Career/06_Job_Opportunities/x_y_2026-10-08"
        self.opp.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.d)

    def probs(self, resume=None, letter=None, year=2026):
        if resume is not None:
            (self.opp / "resume.md").write_text(resume)
        if letter is not None:
            (self.opp / "cover-letter.md").write_text(letter)
        return g.grounding_problems(self.d, self.opp, "opp", year)

    def test_compliant_resume(self):
        self.assertEqual(self.probs(RESUME), [])

    def test_positions_section_allows_sub_positions(self):
        role = ROLE.replace("Grew the team", "## Positions\n\n- **Developer:** March 2010 – June 2011\n- **Vice President of Product:** June 2011 – June 2015\n\nGrew the team", 1)
        (self.d / "Career/02_Work_Experience/Roles/acme.md").write_text(role)
        resume = RESUME.replace("### Acme Corp - Vice President of Product\n**Mar 2010 – Jun 2015 | Houston, TX**",
                                "### Acme Corp - Vice President of Product\n**Jun 2011 – Jun 2015 | Houston, TX**\n\n### Acme Corp - Developer\n**Mar 2010 – Jun 2011 | Houston, TX**\n- Built things.")
        self.assertEqual(self.probs(resume), [])
        bad = resume.replace("Mar 2010 – Jun 2011", "Mar 2009 – Jun 2011")
        self.assertTrue(self.probs(bad))

    def test_value_compare_not_text(self):
        self.assertEqual(self.probs(RESUME.replace("$90K", "$90,000")), [])

    def test_invented_metric(self):
        out = self.probs(RESUME.replace("**25%**", "**60%**"))
        self.assertEqual(len(out), 1)
        self.assertIn("'60%'", out[0])

    def test_small_bare_numbers_ignored(self):
        self.assertEqual(self.probs(RESUME + "- Led 7 teams.\n"), [])

    def test_small_marked_number_checked(self):
        self.assertTrue(self.probs(RESUME + "- Cut cost 7%.\n"))

    def test_years_and_contact_ignored(self):
        self.assertEqual(self.probs(RESUME), [])

    def test_wrong_title(self):
        out = self.probs(RESUME.replace("Vice President of Product", "Chief Product Officer"))
        self.assertTrue(any("matches no canonical role" in p and "Vice President of Product" in p for p in out))

    def test_unknown_employer(self):
        self.assertTrue(any("no role at that employer" in p for p in self.probs(RESUME.replace("Acme Corp -", "Globex -"))))

    def test_company_suffix_and_case_tolerated(self):
        self.assertEqual(self.probs(RESUME.replace("Acme Corp -", "ACME Inc. -")), [])

    def test_changed_dates(self):
        out = self.probs(RESUME.replace("Mar 2010", "Mar 2008"))
        self.assertTrue(any("differ from canonical" in p for p in out))

    def test_present_vs_dated_end(self):
        self.assertTrue(any("differ" in p for p in self.probs(RESUME.replace("Jun 2015", "Present"))))

    def test_tenure_over_span(self):
        self.assertTrue(any("exceeds" in p for p in self.probs(RESUME.replace("10+ years", "30+ years"))))

    def test_tenure_within_span(self):
        self.assertEqual(self.probs(RESUME.replace("10+ years", "16 years")), [])

    def test_cover_letter_figure_and_notes_section(self):
        letter = "# Name\n\nI grew revenue 25%, then 70%.\n\n## Assumptions\n- 999% is internal.\n"
        out = self.probs(letter=letter)
        self.assertEqual(len(out), 1)
        self.assertIn("70%", out[0])

    def test_letter_requisition_and_date_lines_skipped(self):
        self.assertEqual(self.probs(letter="2026-10-08\n\nRole — Requisition 3168705\n\nHi 25%.\n"), [])

    def test_credentials_compliant(self):
        self.assertEqual(self.probs(RESUME + CREDS), [])

    def test_credentials_oneline_and_abbrev_forms(self):
        alt = RESUME + "\n## Education\n**Northern Kentucky University** — B.S. Biology, Class of 2001\n"
        self.assertEqual(self.probs(alt), [])
        alt = RESUME + "\n## Education & Certifications\n**Education:** B.S. Biology, Northern Kentucky University; " \
                       "**Certifications:** Pragmatic Marketing Certified · CSM\n"
        self.assertEqual(self.probs(alt), [])

    def test_credentials_invented_degree(self):
        out = self.probs(RESUME + CREDS.replace("Bachelor of Science in Biology", "Master of Science in Biology"))
        self.assertEqual(len(out), 1)
        self.assertIn("Master of Science", out[0])

    def test_credentials_wrong_year(self):
        self.assertTrue(self.probs(RESUME + CREDS.replace("*2001*", "*2003*")))

    def test_credentials_wrong_institution(self):
        self.assertTrue(self.probs(RESUME + CREDS.replace("Northern Kentucky University", "Rice University")))

    def test_credentials_invented_certification(self):
        out = self.probs(RESUME + CREDS + "- **PMP** - PMI\n")
        self.assertEqual(len(out), 1)
        self.assertIn("PMP", out[0])

    def test_credentials_issuer_mismatch(self):
        self.assertTrue(self.probs(RESUME + CREDS.replace("CollabNet", "PMI")))

    def test_credentials_not_checked_in_cover_letter(self):
        self.assertEqual(self.probs(letter="## Education\n- MBA, Harvard\n"), [])

    def test_credentials_waiver(self):
        bad = RESUME + CREDS + "- **PMP** - PMI\n"
        (self.opp / "grounding-waivers.md").write_text("- **PMP** - PMI — earned 2026-09, canonical entry pending\n")
        self.assertEqual(self.probs(bad), [])

    def test_waiver_needs_reason(self):
        bad = RESUME.replace("**25%**", "**60%**")
        (self.opp / "grounding-waivers.md").write_text("- 60%\n")
        self.assertTrue(self.probs(bad))
        (self.opp / "grounding-waivers.md").write_text("- 60% — confirmed by user 2026-10-08, to be added to the role file\n")
        self.assertEqual(self.probs(bad), [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
