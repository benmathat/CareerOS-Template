#!/usr/bin/env python3
"""Tests for the repo-state checks behind `careeros check` (stdlib only).

    python3 scripts/test_state_checks.py

Unit tests exercise scripts/state_checks.py directly. Integration tests copy the
scripts into a throwaway git repo, stage a violation, and require
`careeros check --staged` to name it (and to stay quiet on the compliant version).
"""
import io
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import state_checks as sc  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
OPP = "Career/06_Job_Opportunities/acme_widget_lead_2026-10-08"
RECORD = """---
company: Acme
role: Widget Lead
intake_status: confirmed
track: track-4
date_added: 2026-10-08
source_pdf: source-posting.pdf
---

# Opportunity

## 1. Raw Source

## 2. Structured Extraction
"""
ANALYSIS = "# Opportunity Analysis\n\n" + "".join(
    f"## {s}\n\n" + ("- Track: track-4\n\n" if s == "Track" else "- pursue\n\n" if s == "Recommendation" else "x\n\n")
    for s in sc.ANALYSIS_SECTIONS)
ENTRY = """## 2026-10-08 — Acme application submitted

```yaml
activity_id: 2026-10-08_acme_application_submitted
activity_type: application_submitted
activity_date: 2026-10-08
qualifying: needs_review
employer_or_platform: Acme
role_or_subject: Widget Lead
method: online_application
outcome_status: submitted
evidence: MISSING
related_opportunity: MISSING
related_application: MISSING
retrospective: false
notes: >
  Test entry.
```
"""


def docx(text):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", f"<w:document><w:t>{text}</w:t></w:document>")
    return buf.getvalue()


class Records(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "source-posting.pdf").write_bytes(b"%PDF")

    def tearDown(self):
        shutil.rmtree(self.d)

    def probs(self, text):
        return sc.record_problems("r.md", text, self.d, "06_Job_Opportunities")

    def test_compliant_record(self):
        self.assertEqual(self.probs(RECORD), [])

    def test_missing_track(self):
        self.assertTrue(any("'track'" in p for p in self.probs(RECORD.replace("track: track-4\n", ""))))

    def test_invalid_track(self):
        self.assertTrue(any("track-8" in p for p in self.probs(RECORD.replace("track-4", "track-8"))))

    def test_track_5_is_valid(self):
        self.assertEqual(self.probs(RECORD.replace("track-4", "track-5")), [])

    def test_track_9_is_valid(self):
        self.assertEqual(self.probs(RECORD.replace("track-4", "track-9")), [])

    def test_empty_value_must_be_MISSING(self):
        self.assertTrue(any("empty" in p for p in self.probs(RECORD.replace("track: track-4", "track:"))))

    def test_draft_not_allowed_in_06(self):
        self.assertTrue(any("intake_status" in p for p in self.probs(RECORD.replace("confirmed", "draft"))))

    def test_missing_source_file(self):
        (self.d / "source-posting.pdf").unlink()
        self.assertTrue(any("not found" in p for p in self.probs(RECORD)))

    def test_missing_section(self):
        self.assertTrue(any("Structured Extraction" in p for p in self.probs(RECORD.replace("## 2. Structured Extraction", ""))))

    def test_scope_cutoff(self):
        self.assertFalse(sc.in_scope("2026-01-30", {}))
        self.assertTrue(sc.in_scope("2026-10-06", {}))
        self.assertTrue(sc.in_scope("2026-01-01", {"date_added": "2026-10-07"}))


class Analysis(unittest.TestCase):
    def test_compliant(self):
        self.assertEqual(sc.analysis_problems("a.md", ANALYSIS, RECORD), [])

    def test_missing_section(self):
        self.assertTrue(sc.analysis_problems("a.md", ANALYSIS.replace("## Risks", "## Other"), RECORD))

    def test_track_conflict(self):
        self.assertTrue(any("conflicts" in p for p in sc.analysis_problems("a.md", ANALYSIS, RECORD.replace("track-4", "track-2"))))

    def test_no_recommendation_value(self):
        self.assertTrue(sc.analysis_problems("a.md", ANALYSIS.replace("- pursue", "- maybe"), RECORD))

    def test_empty_ats_keywords(self):
        self.assertTrue(sc.analysis_problems("a.md", ANALYSIS.replace("## ATS Keywords\n\nx\n\n", "## ATS Keywords\n\n"), RECORD))


class Lifecycle(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "job-opportunity.md").write_text(RECORD)

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_resume_needs_analysis(self):
        (self.d / "resume.md").write_text("x")
        self.assertTrue(any("without analysis.md" in p for p in sc.lifecycle_problems("f", self.d)))

    def test_analysis_needs_confirmed(self):
        (self.d / "analysis.md").write_text("x")
        (self.d / "job-opportunity.md").write_text(RECORD.replace("confirmed", "reviewed"))
        self.assertTrue(any("not confirmed" in p for p in sc.lifecycle_problems("f", self.d)))

    def test_submitted_needs_application_record(self):
        (self.d / "analysis.md").write_text("x")
        (self.d / "job-opportunity.md").write_text(RECORD.replace("track: track-4", "track: track-4\nstatus: submitted"))
        self.assertTrue(any("application-record" in p for p in sc.lifecycle_problems("f", self.d)))

    def test_clean_folder(self):
        (self.d / "analysis.md").write_text("x")
        (self.d / "resume.md").write_text("x")
        self.assertEqual(sc.lifecycle_problems("f", self.d), [])


DISCUSSION = """---
discussion_status: closed
---

# Opportunity Discussion

## User Position

Fit thesis: strong.

## Claim Ledger

| id | claim | verdict | evidence | disposition |
|---|---|---|---|---|
| C1 | Built an org from scratch | supported | Roles/acme.md | agreed |
| C2 | Nonprofit experience | gap | none found | accepted-risk |

## Reconciliations

C2: accepted as a named risk.

## Canonical Proposals

- [applied] 02_Work_Experience/Roles/acme.md: add team size

## Keyword Map Deltas

None.

## Resume and Cover Letter Strategy

Lead with org building.

## Open Items

- [non-blocking] Ask about outside-work policy.
"""
NEW_OPP_RECORD = RECORD.replace("2026-10-08", "2026-11-03")


class Discussion(unittest.TestCase):
    def probs(self, text):
        return sc.discussion_problems("d.md", text)

    def test_compliant(self):
        self.assertEqual(self.probs(DISCUSSION), [])

    def test_missing_section(self):
        self.assertTrue(any("Open Items" in p for p in self.probs(DISCUSSION.replace("## Open Items", "## Other"))))

    def test_bad_status(self):
        self.assertTrue(self.probs(DISCUSSION.replace("discussion_status: closed", "discussion_status: done")))

    def test_bad_verdict(self):
        self.assertTrue(any("verdict" in p for p in self.probs(DISCUSSION.replace("| gap |", "| maybe |"))))

    def test_no_evidence_cited(self):
        self.assertTrue(any("cites no evidence" in p for p in self.probs(DISCUSSION.replace("Roles/acme.md | agreed", " | agreed"))))

    def test_unsupported_claim_cannot_be_merely_agreed(self):
        self.assertTrue(any("reconcile" in p for p in self.probs(DISCUSSION.replace("accepted-risk", "agreed"))))

    def test_closed_with_open_dispute(self):
        self.assertTrue(any("still open" in p for p in self.probs(DISCUSSION.replace("accepted-risk", "open"))))

    def test_open_discussion_may_have_open_dispute(self):
        text = DISCUSSION.replace("accepted-risk", "open").replace("status: closed", "status: open")
        self.assertEqual(self.probs(text), [])

    def test_closed_with_blocking_item(self):
        self.assertTrue(any("[blocking]" in p for p in self.probs(DISCUSSION.replace("[non-blocking]", "[blocking]"))))

    def test_closed_with_proposed_canonical_edit(self):
        self.assertTrue(any("[proposed]" in p for p in self.probs(DISCUSSION.replace("[applied]", "[proposed]"))))

    def test_unknown_proposal_status(self):
        self.assertTrue(any("proposal status" in p for p in self.probs(DISCUSSION.replace("[applied]", "[done]"))))

    def test_marker(self):
        self.assertTrue(any("marker" in p for p in self.probs(DISCUSSION.replace("Lead with", "TBD: lead with"))))


class DiscussionLifecycle(unittest.TestCase):
    def setUp(self):
        root = Path(tempfile.mkdtemp())
        self.root = root
        self.d = root / "acme_widget_lead_2026-11-03"
        self.d.mkdir()
        (self.d / "job-opportunity.md").write_text(NEW_OPP_RECORD)
        (self.d / "analysis.md").write_text("x")

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_resume_needs_discussion(self):
        (self.d / "resume.md").write_text("x")
        self.assertTrue(any("without discussion.md" in p for p in sc.lifecycle_problems("f", self.d)))

    def test_cover_letter_needs_discussion(self):
        (self.d / "cover-letter.md").write_text("x")
        self.assertTrue(any("without discussion.md" in p for p in sc.lifecycle_problems("f", self.d)))

    def test_resume_needs_closed_discussion(self):
        (self.d / "resume.md").write_text("x")
        (self.d / "discussion.md").write_text(DISCUSSION.replace("status: closed", "status: open"))
        self.assertTrue(any("not closed" in p for p in sc.lifecycle_problems("f", self.d)))

    def test_resume_with_closed_discussion_passes(self):
        (self.d / "resume.md").write_text("x")
        (self.d / "discussion.md").write_text(DISCUSSION)
        self.assertEqual(sc.lifecycle_problems("f", self.d), [])

    def test_discussion_needs_analysis(self):
        (self.d / "analysis.md").unlink()
        (self.d / "discussion.md").write_text(DISCUSSION)
        self.assertTrue(any("without analysis.md" in p for p in sc.lifecycle_problems("f", self.d)))

    def test_older_opportunity_is_exempt(self):
        old = self.root / "acme_widget_lead_2026-11-02"
        old.mkdir()
        (old / "job-opportunity.md").write_text(RECORD.replace("2026-10-08", "2026-11-02"))
        (old / "analysis.md").write_text("x")
        (old / "resume.md").write_text("x")
        self.assertEqual(sc.lifecycle_problems("f", old), [])

    def test_only_discuss_command_may_create_discussion(self):
        path = f"{OPP}/discussion.md"
        self.assertTrue(sc.provenance_problems([path], {"analyze-opportunity"}))
        self.assertEqual(sc.provenance_problems([path], {"discuss-opportunity"}), [])


class Deliverables(unittest.TestCase):
    def test_resume_markers(self):
        self.assertTrue(sc.deliverable_problems("a/resume.md", b"Led team. MISSING metric"))

    def test_docx_markers(self):
        self.assertTrue(sc.deliverable_problems("a/r.docx", docx("Hello TODO later")))

    def test_clean(self):
        self.assertEqual(sc.deliverable_problems("a/r.docx", docx("Hello world")), [])
        self.assertEqual(sc.deliverable_problems("a/resume.md", b"All good"), [])

    def test_cover_letter_notes_may_say_missing(self):
        self.assertEqual(sc.deliverable_problems("a/cover-letter.md", b"Context gaps: MISSING"), [])

    def test_corrupt_docx(self):
        self.assertTrue(sc.deliverable_problems("a/r.docx", b"not a zip"))


class WorkLog(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_compliant(self):
        self.assertEqual(sc.log_problems("l.md", ENTRY, self.d), [])

    def test_missing_field(self):
        self.assertTrue(sc.log_problems("l.md", ENTRY.replace("method: online_application\n", ""), self.d))

    def test_legacy_twc_qualifying_accepted(self):
        self.assertEqual(sc.log_problems("l.md", ENTRY.replace("qualifying:", "twc_qualifying:"), self.d), [])

    def test_missing_qualifying(self):
        self.assertTrue(any("qualifying" in p for p in sc.log_problems("l.md", ENTRY.replace("qualifying: needs_review\n", ""), self.d)))

    def test_bad_qualifying(self):
        self.assertTrue(sc.log_problems("l.md", ENTRY.replace("needs_review", "yes"), self.d))

    def test_date_mismatch(self):
        self.assertTrue(sc.log_problems("l.md", ENTRY.replace("activity_date: 2026-10-08", "activity_date: 2026-10-09"), self.d))

    def test_duplicate_id(self):
        self.assertTrue(any("duplicate" in p for p in sc.log_problems("l.md", ENTRY + "\n" + ENTRY, self.d)))

    def test_evidence_path_must_exist(self):
        bad = ENTRY.replace("evidence: MISSING", "evidence: Evidence/nope.pdf")
        self.assertTrue(any("does not exist" in p for p in sc.log_problems("l.md", bad, self.d)))
        (self.d / "Evidence").mkdir()
        (self.d / "Evidence/nope.pdf").write_bytes(b"x")
        self.assertEqual(sc.log_problems("l.md", bad, self.d), [])

    def test_opportunity_path_follows_archive(self):
        bad = ENTRY.replace("related_opportunity: MISSING", "related_opportunity: ../06_Job_Opportunities/acme_2026-10-08/job-opportunity.md")
        self.assertTrue(any("does not exist" in p for p in sc.log_problems("l.md", bad, self.d)))
        arch = self.d / "../99_Archive/Closed_Searches/acme_2026-10-08"
        arch.mkdir(parents=True)
        (arch / "job-opportunity.md").write_text("x")
        try:
            self.assertEqual(sc.log_problems("l.md", bad, self.d), [])
        finally:
            shutil.rmtree(self.d / "../99_Archive")

    def test_append_only(self):
        self.assertEqual(sc.log_append_only_problems("l", ENTRY, ENTRY + "\n## 2026-10-09 — Next\n"), [])
        self.assertTrue(sc.log_append_only_problems("l", ENTRY, ENTRY.replace("Test entry.", "Edited.")))
        self.assertTrue(sc.log_append_only_problems("l", ENTRY, "# empty\n"))


class Provenance(unittest.TestCase):
    ADDED = [f"{OPP}/job-opportunity.md", f"{OPP}/source-posting.pdf"]

    def test_intake_cannot_create_06_records(self):
        self.assertEqual(len(sc.provenance_problems(self.ADDED, {"intake-job"})), 2)

    def test_promote_can(self):
        self.assertEqual(sc.provenance_problems(self.ADDED, {"intake-job", "promote-opportunity"}), [])

    def test_analysis_needs_analyze_run(self):
        self.assertTrue(sc.provenance_problems([f"{OPP}/analysis.md"], {"build-resume"}))

    def test_unlisted_files_and_archive_ignored(self):
        self.assertEqual(sc.provenance_problems([f"{OPP}/notes.md", "Career/99_Archive/Closed_Searches/a_b_2026-10-08/analysis.md"], set()), [])


class StagedIntegration(unittest.TestCase):
    """End to end through `careeros check --staged` in a throwaway repo."""

    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "scripts").mkdir()
        for f in ("careeros", "state_checks.py", "grounding_checks.py", "style_checks.py", "new_run.py", "opp_index.py", "lapsed.py", "validate_runtime_io.py", "run_command_gate.sh",
                  "requirements-runtime-validator.txt"):
            shutil.copy(SCRIPTS / f, self.d / "scripts" / f)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        (self.d / "Career/00_Core_OS/Runs").mkdir(parents=True)
        (self.d / "Career/11_Job_Search_Activities").mkdir(parents=True)
        (self.d / "Career/11_Job_Search_Activities/Work_Search_Log.md").write_text("# Log\n\n" + ENTRY)
        (self.d / "README.md").write_text("x")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

    def tearDown(self):
        shutil.rmtree(self.d)

    def git(self, *a):
        return subprocess.run(["git", *a], cwd=self.d, capture_output=True, text=True)

    def write(self, rel, text):
        p = self.d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        self.git("add", rel)

    def check(self):
        r = subprocess.run([str(self.d / "scripts/careeros"), "check", "--staged"], cwd=self.d, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def stage_record(self):
        self.write(f"{OPP}/job-opportunity.md", RECORD)
        (self.d / OPP / "source-posting.pdf").write_bytes(b"%PDF")
        self.git("add", f"{OPP}/source-posting.pdf")

    def run_file(self, command):
        self.write(f"Career/00_Core_OS/Runs/2026-10-08_{command}_acme.runtime-io.yaml", "runtime_io: {}\n")

    def test_intake_overreach_is_named(self):
        self.stage_record()
        self.run_file("intake-job")
        rc, out = self.check()
        self.assertEqual(rc, 1)
        self.assertIn("added without a run file for promote-opportunity", out)

    def test_promote_run_satisfies_provenance(self):
        self.stage_record()
        self.run_file("promote-opportunity")
        _, out = self.check()
        self.assertNotIn("added without a run file", out)
        self.assertNotIn("job-opportunity.md:", out)

    def test_out_of_scope_legacy_folder_is_skipped(self):
        legacy = "Career/06_Job_Opportunities/old_role_2026-01-30"
        self.write(f"{legacy}/job-opportunity.md", "---\ncompany: Old\nrole: R\nintake_status: draft\n---\n")
        self.run_file("promote-opportunity")
        _, out = self.check()
        self.assertNotIn("track", out)

    def test_editing_existing_log_entry_fails(self):
        self.write("Career/11_Job_Search_Activities/Work_Search_Log.md", "# Log\n\n" + ENTRY.replace("Test entry.", "Rewritten."))
        rc, out = self.check()
        self.assertEqual(rc, 1)
        self.assertIn("edited or removed", out)

    def test_appending_log_entry_passes(self):
        new = ENTRY.replace("2026-10-08_acme", "2026-10-09_acme").replace("## 2026-10-08", "## 2026-10-09").replace(
            "activity_date: 2026-10-08", "activity_date: 2026-10-09")
        self.write("Career/11_Job_Search_Activities/Work_Search_Log.md", "# Log\n\n" + ENTRY + "\n" + new)
        rc, out = self.check()
        self.assertEqual(rc, 0, out)

    def test_resume_with_marker_fails(self):
        self.stage_record()
        self.write(f"{OPP}/analysis.md", ANALYSIS)
        self.write(f"{OPP}/resume.md", "# Name\n\nMISSING metric\n")
        self.run_file("promote-opportunity")
        self.run_file("analyze-opportunity")
        self.run_file("build-resume")
        _, out = self.check()
        self.assertIn("unresolved marker", out)

    def test_ungrounded_figure_in_resume_variant_fails(self):
        self.write("Career/02_Work_Experience/Roles/README.md", "No numbers.\n")
        self.stage_record()
        self.write(f"{OPP}/analysis.md", ANALYSIS)
        self.write(f"{OPP}/resume-3page.md", "# Name\n\n## Summary\nCut cost 73%.\n")
        for c in ("promote-opportunity", "analyze-opportunity", "build-resume"):
            self.run_file(c)
        rc, out = self.check()
        self.assertEqual(rc, 1)
        self.assertIn("'73%' not found in canonical content", out)

    def test_marker_in_resume_variant_fails(self):
        self.stage_record()
        self.write(f"{OPP}/analysis.md", ANALYSIS)
        self.write(f"{OPP}/resume-3page.md", "# Name\n\nMISSING metric\n")
        for c in ("promote-opportunity", "analyze-opportunity", "build-resume"):
            self.run_file(c)
        _, out = self.check()
        self.assertIn("unresolved marker", out)

    def test_ungrounded_figure_in_resume_fails(self):
        self.write("Career/02_Work_Experience/Roles/README.md", "No numbers.\n")
        self.stage_record()
        self.write(f"{OPP}/analysis.md", ANALYSIS)
        self.write(f"{OPP}/resume.md", "# Name\n\n## Summary\nCut cost 73%.\n")
        for c in ("promote-opportunity", "analyze-opportunity", "build-resume"):
            self.run_file(c)
        rc, out = self.check()
        self.assertEqual(rc, 1)
        self.assertIn("'73%' not found in canonical content", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
