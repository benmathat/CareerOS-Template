---
Last Update: 2026-11-05
Previous Update: 2026-10-07
---

# INBOX

**Location:** `Career/INBOX/`

**Purpose:**  
Capture incoming documents before they are processed into the rest of CareerOS. This is a staging area, not a permanent home.

## Layout

```text
Career/INBOX/
  README.md              # this file (tracked)
  .gitignore             # ignores staging drops; keeps README/.gitignore tracked
  Job_Postings/          # job PDFs + staged opportunity markdown from /intake-job
  <other drops>          # temporary captures pending filing
```

## What Goes Here

- Job posting PDFs (or links/text) awaiting `/intake-job`
- Recruiter / hiring-manager documents not yet filed
- Company research downloads pending review
- Interview notes, feedback, or other career materials waiting to be routed

## Job Posting Path (Primary)

1. Drop the source PDF (preferred) into `Job_Postings/`
2. Run `/intake-job` → staged file `Job_Postings/<company>_<role>_<YYYY-MM-DD>.md`
3. Review extraction; set `intake_status` to `reviewed` / `confirmed`
4. Run `/promote-opportunity` → durable folder  
   `06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/`  
   (`job-opportunity.md` + `source-posting.pdf`)

URL- or text-only intakes are staged in `Job_Postings/` like any other. When the staged file captures the whole posting verbatim, `/promote-opportunity` promotes it without a PDF (`source_pdf: MISSING`; see the full-text-capture exception in that skill). Prefer a source PDF whenever one is available.

## Filing Map (Non-Job Items)

| Capture type | File to |
|--------------|---------|
| Company research | `09_Research_and_Market_Intelligence/Company_Research/` |
| Interview notes / prep | `07_Applications_and_Interviews/Interview_Prep/` |
| Application evidence (confirmations, screenshots) | `11_Job_Search_Activities/Evidence/` |
| Feedback / coaching | `10_Coaching_Feedback_and_Notes/` |
| Work experience updates | `02_Work_Experience/` |
| Closed / historical materials | `99_Archive/` (e.g. `Closed_Searches/`) |

Opportunity-scoped resumes, cover letters, and application records belong in the opportunity folder under `06_Job_Opportunities/`, not here.

## Git Note

`.gitignore` ignores everything in this folder except `README.md` and `.gitignore`. Staging PDFs and draft intake markdown are local until promoted into tracked CareerOS sections.

## Rules

- Keep it lean — process daily or at least weekly
- Empty it as part of weekly review
- Use descriptive filenames (date + source when possible)
- When in doubt, capture here first, then file

## Processing Checklist

- [ ] Review INBOX (root + `Job_Postings/`)
- [ ] Run `/intake-job` / `/promote-opportunity` for new postings
- [ ] Move non-job items to the destinations above
- [ ] Update tracker / work search log when an external action occurred
- [ ] Delete or archive processed drops so INBOX is empty again

---

**Note:** This folder should be empty most of the time. If it is accumulating, schedule dedicated processing time.
