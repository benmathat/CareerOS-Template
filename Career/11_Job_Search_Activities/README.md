---
Last Update: 2026-11-11
Previous Update: 2026-04-19
---

# Job Search Activities — Unemployment Work-Search Compliance

**Location:** `Career/11_Job_Search_Activities/`

**Purpose:**  
Documents work search activities in compliance with your unemployment agency's eligibility requirements. This folder provides an audit-safe, ready-to-use system for tracking and certifying job search activities.

**This section is optional.** If you are not claiming unemployment benefits, ignore it and skip the `log-activity` and `generate-weekly-cert` commands.

## Set Up Your Agency First

CareerOS does not assume an agency or a state. Fill in `compliance-profile.md` (in a fresh template it ships blank):

- the agency and its short name
- the jurisdiction and program
- certification frequency and the number of qualifying activities required
- what the agency counts as qualifying, how you submit, and how long to keep records

The commands read that file. Where a value is `[unknown]`, they ask you instead of guessing. Take every value from your claim notice and your agency's published rules, not from this repo.

This folder serves three key functions:
1. **Compliance:** Meets your agency's requirements for documenting work search activities
2. **Audit Protection:** Provides detailed, contemporaneous records that protect you in case of disputes or audits
3. **Accountability:** Maintains a clear record of your search efforts and progress

**Use this when:**
- Filing periodic unemployment certifications
- Documenting required work search activities
- Tracking your search activity levels
- Providing proof of work search efforts if audited

---

## What Goes Here

- **Compliance Profile:** Your agency and its rules (`compliance-profile.md`)
- **Work Search Log:** Canonical record of all work search activities (`Work_Search_Log.md`)
- **Weekly Certifications:** Snapshots of what was submitted to the agency
- **Evidence:** Supporting documentation (application confirmations, emails, interview invites)

---

## Key Principles

1. **Document Immediately:** Record activities as they happen, not at the end of the week
2. **Be Specific:** Include dates, company names, role titles, contact information, and outcomes
3. **Over-Comply:** A format that exceeds the minimum reads like a professional compliance record
4. **Maintain Evidence:** Save proof of activities (confirmations, emails, screenshots) in the Evidence folder
5. **Retrospective entries:** If you tracked activities elsewhere first, add them to `Work_Search_Log.md` using the true activity date and a note in the Notes column
6. **Don't self-certify qualification:** Mark an activity `qualifying: true` only when you know your agency counts it; use `needs_review` when unsure

---

## What Agencies Typically Require

Rules vary by jurisdiction, so check yours. The log captures the elements most agencies ask for:

| Typical requirement | Where It's Covered |
|---------------------|--------------------|
| Date of activity | Date column in `Work_Search_Log.md` |
| Type of work search | Activity Type column |
| Employer/contact | Employer / Platform column |
| Method of contact | Method column |
| Result of activity | Outcome / Status column |
| Proof upon request | Evidence folder |
| Periodic compliance | Weekly Certification Summary |

---

## Folder Structure

```
11_Job_Search_Activities/
├── README.md                          ← This file
├── compliance-profile.md              ← Your agency and its rules
├── Work_Search_Log.md                 ← ⭐ Canonical record (update daily)
├── Weekly_Certifications/             ← Snapshots of each submission
│   ├── README.md
│   └── YYYY-W##.md
└── Evidence/                          ← Supporting documentation
    ├── README.md
    └── Interviews/
```

Keep your own notes on your agency's rules (for example `Agency_Requirements.md`) in this folder and point to them from `compliance-profile.md`.

---

## How the Pieces Work Together

**`Work_Search_Log.md`** is the canonical record. Updated daily; the source of truth if audited.

**`Weekly_Certifications/`** is a snapshot per period that mirrors what you submit and references rows from the log.

**`Evidence/`** holds application confirmations, email screenshots, interview invitations and any other proof.

This separation keeps compliance clean, the narrative intact and evidence traceable.

---

## Integration with Other Folders

- `Career/00_Core_OS/search-status.md` — High-level dashboard (active claim, requirements, certification dates)
- `Career/07_Applications_and_Interviews/` — Detailed application tracking and interview prep
- `Career/08_Networking_and_References/` — Networking activities and relationship management
- `Career/06_Job_Opportunities/` — Job research and opportunity evaluation

**Key difference:** This folder focuses on **documentation for agency compliance**, while other folders focus on **strategy and execution**.

---

## Recommended Daily Workflow (5–7 minutes)

1. **Do activity** (apply, network, research)
2. **Immediately add a row** with `log-activity`
3. **Drop any proof** into `Evidence/`
4. **End of each certification period:**
   - Count activities
   - Run `generate-weekly-cert`
   - Submit to your agency by its required method, then record the submission in the certification file

---

CareerOS documents your activity; it does not determine eligibility or replace your agency's instructions or legal advice. Keep it simple, keep it current, and keep it complete.
