---
Last Update: 2026-11-05
Previous Update: 2026-10-26
---

# Application Record Template

## Template Rules

- This template defines structure only (no execution logic)
- All fields MUST be populated or set to `MISSING`
- All content MUST be grounded in actual activity or explicitly labeled assumptions
- No fabricated or inferred application data is allowed
- This artifact tracks a single application lifecycle

---

## Application Overview

- Company: <string | MISSING>
- Role: <string | MISSING>
- Track: <track-2 | track-3 | track-4 | track-5 | track-9 | MISSING>
- Role Target: <canonical role-target file path | MISSING>
- Track Source: <analysis.md section or job-opportunity.md frontmatter | MISSING>
- Job Reference: <job-opportunity.md link | MISSING>
- Application Date: <YYYY-MM-DD | MISSING>
- Application Method: <career site | referral | recruiter | other | MISSING>

---

## Application Materials

### Resume Used
- path: <file path | MISSING>
- Baseline Used: <file path | NONE>
- Positioning Rationale: <how the resolved track and posting guided the resume | MISSING>

### Cover Letter Used
- path: <file path | NONE>

### Additional Materials
- <portfolio | case study | other | NONE>

---

## Submission Details

- Submission Status: <draft | submitted | failed | MISSING>
- Submission Timestamp: <YYYY-MM-DD HH:MM | MISSING>
- Confirmation Received: <yes | no | MISSING>
- Confirmation Reference: <email | screenshot | NONE>

---

## Contact Information

- Recruiter Name: <string | MISSING>
- Recruiter Contact: <email | linkedin | NONE>
- Hiring Manager: <string | MISSING>

---

## Status Tracking

- Current Status: <submitted | screening | interviewing | rejected | offer | closed | MISSING>
- Last Status Update: <YYYY-MM-DD | MISSING>

---

## Follow-Up

- Follow-Up Required: <yes | no | MISSING>
- Follow-Up Date: <YYYY-MM-DD | MISSING>
- Follow-Up Method: <email | linkedin | other | MISSING>

---

## Interview Tracking

### Stages
- <list | NONE>

### Scheduled Interviews
- <date + type | NONE>

### Outcomes
- <notes | NONE>

---

## Notes

- <freeform notes | MISSING>

---

## Assumptions

- <list | NONE>

## Context Gaps

- <list | NONE>

---

## Validation Checklist

- [ ] All fields are populated or `MISSING`
- [ ] Track and role target match the resolved opportunity assignment before targeted materials are finalized
- [ ] Track provenance is internal and excluded from submitted resume/cover-letter content
- [ ] No fabricated or inferred data is present
- [ ] Submission details are verifiable
- [ ] Status tracking reflects actual application state
- [ ] Assumptions and Context Gaps are included where applicable
- [ ] Structure matches template exactly
