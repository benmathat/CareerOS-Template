# Opportunity Folders

This section holds **one folder per opportunity**, from intake through application materials.

Each promoted opportunity folder typically contains:

```text
<company>_<role>_<YYYY-MM-DD>/
  job-opportunity.md
  source-posting.pdf          # or source-posting.md / source-record.json
  analysis.md
  resume.md                   # editable tailored resume
  cover-letter.md             # when present
  application-notes.md        # when present
  application-record.md       # when present
  next-steps.md               # when present
  <company>_<role>_resume_<date>.docx|.pdf
  <company>_<role>_cover_letter_<date>.docx|.pdf
```

New postings stage in `../INBOX/Job_Postings/` via `/intake-job`, then `/promote-opportunity` creates the opportunity folder above.

## Why This Exists
Keep everything for one role in one place: posting, analysis, tailored materials, and application execution artifacts.

Reusable baselines (master resume, templates, online profiles) stay in `../01_Resume_and_Profiles/`.
Cross-opportunity tracking and interview prep libraries stay in `../07_Applications_and_Interviews/`.
Company research lives in `../09_Research_and_Market_Intelligence/Company_Research/`.
Networking and recruiter contacts live in `../08_Networking_and_References/`.

<!-- BEGIN GENERATED: opportunity-index (careeros index --write) -->

_No opportunities yet. Run `scripts/careeros index --write` after `/promote-opportunity`._

<!-- END GENERATED: opportunity-index -->
