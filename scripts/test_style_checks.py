#!/usr/bin/env python3
"""Tests for prose-style warnings (scripts/style_checks.py), stdlib only.

    python3 scripts/test_style_checks.py

Fixtures are synthetic (Acme Corp, Jordan Q. Public). They reproduce the patterns an editor
removed from real Claude drafts, without carrying any real application text.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style_checks as s  # noqa: E402

DRAFT_LETTER = """Dear Hiring Team,

I'm not the obvious profile for this seat, and I'd rather say so. I've repeatedly walked into unfamiliar teams and found how they actually work.

The harder part of strategy is deciding what not to do. For a vendor weighing a proprietary tool, I ran about 30 customer interviews, projected $1.5M in year one and $5M to launch, and recommended against building. At Acme, I built my own churn model, and it was a deciding factor in ceasing that pursuit. Where I lacked line authority, I earned alignment through analysis: quantifying a library update across roughly 250,000 servers and 1,800 providers led to a release pause and a revised plan that the whole group accepted afterwards.

Sincerely,
Jordan Q. Public
"""

FINAL_LETTER = """Dear Hiring Team,

My path to this role is not conventional. I quickly develop a point of view in unfamiliar organizations.

Strategy also requires deciding what not to do. For a vendor considering a proprietary tool, I conducted approximately 30 customer interviews, projected costs of $1.5 million in the first year and $5 million to launch, and recommended against proceeding. At Acme, a churn model I built was a deciding factor in ending pursuit of an acquisition target. At a prior employer, where I had no line authority, quantifying a library update across roughly 250,000 servers helped secure alignment around a release pause.

Sincerely,
Jordan Q. Public
"""

DRAFT_RESUME = """# Jordan Q. Public
Tomball, TX · 555-555-0100 · jordan@example.com

## Professional Experience

### Acme Corp. - Vice President of Product
**Nov 2020 – Jan 2024 | Austin, TX**
- **Product operating model:** Established a company-wide intake routing bugs and requests to the owning team.
- **Product strategy:** Defined the roadmaps for an unmanaged product line: a five-year strategy with phased roadmaps, separate narratives, and success metrics.
- **Portfolio prioritization:** Cut a portfolio to 6 priorities by framing every proposal against the roadmaps he built.
- **Packaging and pricing:** Built his own churn model; the model drove the decision; the team agreed.
- **Hands-on product development:** Built a word game in 12 days; solo work, customer adoption not yet established.
"""

FINAL_RESUME = """# Jordan Q. Public
Tomball, TX · 555-555-0100 · jordan@example.com

## Professional Experience

### Acme Corp. - Vice President of Product
**Nov 2020 – Jan 2024 | Austin, TX**
- **Product operating model:** Established a company-wide intake process that routed bugs and requests to the appropriate teams.
- **Product strategy:** Defined a five-year strategy and phased roadmaps for an unmanaged product line. Created separate narratives and success metrics.
- **Portfolio prioritization:** Cut a portfolio to 6 priorities by evaluating proposals against newly established roadmaps. Used $90K of savings to fund the work.
- **Customer research:** Built a churn model that drove the decision to end the pursuit.
"""


def text_of(warns):
    return "\n".join(warns)


class LetterTests(unittest.TestCase):
    def test_draft_patterns_are_flagged(self):
        t = text_of(s.style_warnings("cover-letter.md", DRAFT_LETTER, "letter"))
        for expect in ("contraction 'I'm'", "contraction 'I'd'", "contraction 'I've'", "'I'd rather'",
                       "'walked into'", "'actually'", "aphorism opener", "'$1.5M' abbreviated",
                       "'$5M' abbreviated", "does not say what it measures", "'my own'",
                       "'cease'", "'earned alignment'", "long sentence built on a colon"):
            self.assertIn(expect, t, expect)

    def test_final_text_is_clean(self):
        self.assertEqual(s.style_warnings("cover-letter.md", FINAL_LETTER, "letter"), [])

    def test_overlong_sentence_is_flagged(self):
        long = " ".join(["word"] * 46) + ".\n"
        self.assertIn("sentence of 46 words", text_of(s.style_warnings("cover-letter.md", long, "letter")))

    def test_curly_apostrophe_is_a_contraction(self):
        w = s.style_warnings("cover-letter.md", "I’m glad to apply.\n", "letter")
        self.assertTrue(any("contraction" in x for x in w))

    def test_possessive_is_not_a_contraction(self):
        self.assertEqual(s.style_warnings("cover-letter.md", "I admire HP's Commercial PC portfolio.\n", "letter"), [])

    def test_resume_abbreviation_is_allowed_but_letter_abbreviation_is_not(self):
        line = "Saved $90K per month.\n"
        self.assertEqual(s.style_warnings("resume.md", "- " + line, "resume"), [])
        self.assertTrue(s.style_warnings("cover-letter.md", line, "letter"))


class ResumeTests(unittest.TestCase):
    def test_draft_patterns_are_flagged(self):
        t = text_of(s.style_warnings("resume.md", DRAFT_RESUME, "resume"))
        for expect in ("pronoun 'he'", "pronoun 'his'", "colon inside a bullet body",
                       "two or more semicolons", "working notes ('not yet established')"):
            self.assertIn(expect, t, expect)

    def test_final_text_is_clean(self):
        self.assertEqual(s.style_warnings("resume.md", FINAL_RESUME, "resume"), [])

    def test_contact_and_heading_lines_are_not_prose(self):
        text = "# Jordan Q. Public\nTomball, TX · jordan@example.com\n\n## Experience\n"
        self.assertEqual(s.style_warnings("resume.md", text, "resume"), [])

    def test_line_numbers_account_for_frontmatter(self):
        text = "---\nLast Update: 2026-01-01\n---\n\n- Built it; he led it.\n"
        w = s.style_warnings("resume.md", text, "resume")
        self.assertTrue(w and w[0].startswith("resume.md:5:"), w)


class RoutingTests(unittest.TestCase):
    def test_doc_kind(self):
        self.assertEqual(s.doc_kind("resume.md"), "resume")
        self.assertEqual(s.doc_kind("resume-3page.md"), "resume")
        self.assertEqual(s.doc_kind("cover-letter.md"), "letter")
        for other in ("analysis.md", "application-notes.md", "resume_JQP-acme.docx", "resume.md.bak"):
            self.assertIsNone(s.doc_kind(other), other)

    def test_file_warnings_ignores_other_documents(self):
        self.assertEqual(s.file_warnings(Path("."), "Career/06_Job_Opportunities/x/analysis.md", "I'm fine\n"), [])

    def test_automatic_check_is_scoped_to_submitted_materials(self):
        bad = "- Work: it's here; a; b; c: d\n"
        for rel in ("Career/00_Core_OS/Prompts/Packs/resume-pack.md",
                    "Career/01_Resume_and_Profiles/Templates/resume-template.md"):
            self.assertEqual(s.file_warnings(Path("."), rel, bad), [], rel)
        for rel in ("Career/06_Job_Opportunities/acme_vp_2026-01-01/resume.md",
                    "Career/01_Resume_and_Profiles/resume-agentic-engineering.md"):
            self.assertTrue(s.file_warnings(Path("."), rel, bad), rel)

    def test_skills_and_credential_lists_may_use_colons_and_semicolons(self):
        text = "## Core Competencies\n- Change enablement: readiness; adoption; messaging\n\n## Experience\n- Led it: a; b; c\n"
        w = s.style_warnings("resume.md", text, "resume")
        self.assertEqual([x.split(":")[1] for x in w if "colon" in x or "semicolon" in x], ["5", "5"])

    def test_link_urls_and_descriptive_words_are_not_flagged(self):
        text = "## Experience\n- **Build:** Launched [Game](https://example.com), returning evidence rather than unverified text.\n"
        self.assertEqual(s.style_warnings("resume.md", text, "resume"), [])

    def test_warnings_are_deduplicated(self):
        w = s.style_warnings("cover-letter.md", "It's fine.\n", "letter")
        self.assertEqual(len(w), len(set(w)))


if __name__ == "__main__":
    unittest.main()
