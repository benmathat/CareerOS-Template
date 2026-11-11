---
Last Update: 2026-11-11
Previous Update: 2026-10-07
---

# CareerOS Compressed Structure Map

Use this file as the compact, high-level map of CareerOS organization for prompt contexts.

## Top-Level Intent Map (`Career/`)

- `INBOX/` - Staging area for incoming material before filing
- `00_Core_OS/` - Orientation, control, core maps, and prompt packs
- `01_Resume_and_Profiles/` - Reusable presentation baselines (master, templates, online profiles, shareable)
- `02_Work_Experience/` - Canonical career memory (roles, projects, metrics, long-form stories)
- `03_Skills_and_Portfolio/` - Capability proof and skill evidence
- `04_Career_Goals_and_Strategy/` - Direction, role targets, constraints, transition strategy
- `05_Personal_Profile/` - Values, preferences, assessments, non-negotiables
- `06_Job_Opportunities/` - Per-opportunity folders (posting, analysis, tailored resume/cover letter, application notes/record/next-steps)
- `07_Applications_and_Interviews/` - Cross-opportunity tracker, interview prep library, offers/negotiation
- `08_Networking_and_References/` - Contacts, informational interviews, references, advisors
- `09_Research_and_Market_Intelligence/` - Market, company, role, and compensation intelligence
- `10_Coaching_Feedback_and_Notes/` - Coaching inputs and reflection loop
- `11_Job_Search_Activities/` - Unemployment work-search compliance (agency and rules set in `compliance-profile.md`)
- `99_Archive/` - Deactivated history preserved without clutter

## Boundary Rules

- Canonical long-form stories: `02_Work_Experience/Stories/`
- Application/interview-loop story variants: `07_Applications_and_Interviews/Interview_Prep/Stories/`
- Story index and competency mapping: `07_Applications_and_Interviews/Interview_Prep/story-inventory.md`
- Opportunity-scoped materials: `06_Job_Opportunities/<company>_<role>_<date>/`

## Decision Rule

- If content should still be true next month, prefer canonical sections (especially `02_`, `04_`, `05_`).
- If content is specific to one opportunity, place it in that opportunity folder under `06_`.
- If content is shared across opportunities (tracker, interview library), place it in `07_`.
