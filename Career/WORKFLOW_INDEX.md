---
Last Update: 2026-11-06
Previous Update: 2026-11-05
---

# Workflow Index: Common Tasks to Document Locations

This index maps common tasks to the commands, folders and templates you'll need. Use it as a quick reference when you know what you want to do but aren't sure where to start.

**Commands.** Where a task has a command, the command's contract is `00_Core_OS/Skills/<command>/SKILL.md` and it takes precedence over any workflow prose. Each run writes a runtime IO file to `00_Core_OS/Runs/`; mechanical helpers (dates, slugs, frontmatter, closing, checks) are `scripts/careeros`. See `WORKFLOWS.md` for the narrative flow and `00_Core_OS/Prompts/Runtime/operator-runbook.md` for how a run works.

| Command | Use it to |
|---------|-----------|
| `/source-opportunities` | Save a weekly shortlist or broader on-demand report with sourcing history; intake remains separate |
| `/intake-job` | Stage a posting (PDF, URL or text) as a draft in `INBOX/Job_Postings/` |
| `/promote-opportunity` | File a reviewed draft as `06_Job_Opportunities/<company>_<role>_<date>/` |
| `/analyze-opportunity` | Write `analysis.md` (track, fit, ATS keywords, recommendation) |
| `/discuss-opportunity` | Weigh your fit thesis and risks against canonical evidence, reconcile disputes, write `discussion.md` and the resume/cover-letter strategy (required before building for opportunities added from 2026-11-03) |
| `/build-resume` | Write a tailored `resume.md` in the opportunity folder |
| `/build-application` | Write resume, cover letter, notes, record and next steps |
| `/log-activity` | Add an entry to the work search log (and tracker, if the lifecycle changed) |
| `/sync-application-tracker` | Reconcile the tracker with application records |
| `/close-opportunity` | Archive a passed, withdrawn, rejected or no-response opportunity |
| `/generate-weekly-cert` | Produce the weekly work-search certification summary |

---

## Starting a Job Search

**Workflow:** See `WORKFLOWS.md` → "Starting a New Job Search"

**Documents needed:**
- `00_Core_OS/career-index.md` - Set current focus
- `00_Core_OS/search-status.md` - Initialize search status
- `04_Career_Goals_and_Strategy/career-tracks.md` - Career tracks every opportunity is routed to
- `04_Career_Goals_and_Strategy/Role_Targets/role-target-template.md` - Define target roles
- `04_Career_Goals_and_Strategy/Career_Vision/career-vision-template.md` - Long-term vision (optional)
- `05_Personal_Profile/Work_Preferences/work-preferences-template.md` - Document preferences
- `07_Applications_and_Interviews/Applications/application-tracker.md` - Set up tracking

---

## Finding and Evaluating an Opportunity

**Workflow:** See `WORKFLOWS.md` → "Processing a New Opportunity"

**Sourcing:** `/source-opportunities` saves a report and sighting history in `09_Research_and_Market_Intelligence/Opportunity_Sourcing/`. Select candidates before intake.

**Commands after selection:** `/intake-job` → review the draft → `/promote-opportunity` → `/analyze-opportunity` → `/discuss-opportunity`

**Documents needed:**
- `INBOX/Job_Postings/` - Staged drafts (untracked by design)
- `06_Job_Opportunities/<company>_<role>_<date>/` - `job-opportunity.md`, `source-posting.pdf`, `analysis.md`
- `08_Networking_and_References/Contacts/` - Log recruiter contact
- `09_Research_and_Market_Intelligence/Company_Research/company-research-template.md` - Research company
- `09_Research_and_Market_Intelligence/Compensation_Data/compensation-research-template.md` - Research compensation
- `04_Career_Goals_and_Strategy/Role_Targets/` - Check alignment
- `05_Personal_Profile/Work_Preferences/` - Check fit

---

## Applying to a Role

**Workflow:** See `WORKFLOWS.md` → "Processing a New Opportunity" (Step 4)

**Commands:** `/build-resume` and/or `/build-application`, then `/log-activity` once submitted. Optionally `scripts/generate-resume-docx.sh` and `scripts/generate-cover-letter-docx.sh` for DOCX/PDF.

**Documents needed:**
- `06_Job_Opportunities/<company>_<role>_<date>/` - `resume.md`, `cover-letter.md`, `application-notes.md`, `application-record.md`, `next-steps.md`
- `07_Applications_and_Interviews/Applications/application-tracker.md` - Tracker row (points at the opportunity folder)
- `01_Resume_and_Profiles/Resume_Master/` - Reusable baseline (read-only input; tailored resumes do not go here)
- `01_Resume_and_Profiles/Templates/` - Resume and cover letter templates
- `11_Job_Search_Activities/Work_Search_Log.md` - Work search log (written by `/log-activity`)

`scripts/careeros check` verifies the resume and cover letter against canonical content (employers, titles, dates, figures, education and certifications).

---

## Preparing for an Interview

**Workflow:** See `WORKFLOWS.md` → "Processing a New Opportunity" (Step 5)

**Documents needed:**
- `06_Job_Opportunities/<company>_<role>_<date>/application-notes.md` and `next-steps.md` - Opportunity context
- `07_Applications_and_Interviews/Interview_Prep/story-inventory.md` - Review stories
- `07_Applications_and_Interviews/Interview_Prep/STAR-story-template.md` - Prepare STAR stories
- `07_Applications_and_Interviews/Interview_Prep/SOAR-story-template.md` - Prepare SOAR stories (leadership roles)
- `07_Applications_and_Interviews/Interview_Prep/interview-day-checklist.md` - Day-of checklist
- `07_Applications_and_Interviews/Interview_Prep/role-question-bank.md` - Question bank
- `09_Research_and_Market_Intelligence/Company_Research/[company].md` - Review company research
- `02_Work_Experience/Projects/` - Review relevant projects
- `02_Work_Experience/Stories/` - Canonical interview stories

---

## After an Interview

**Workflow:** See `WORKFLOWS.md` → "Processing a New Opportunity" (Step 5)

**Commands:** `/log-activity` (the interview is a lifecycle change and updates the tracker in the same run)

**Documents needed:**
- `06_Job_Opportunities/<company>_<role>_<date>/application-notes.md` - Post-interview reflection
- `07_Applications_and_Interviews/Applications/application-tracker.md` - Update status
- `07_Applications_and_Interviews/Interview_Prep/story-inventory.md` - Update if a new story emerged
- `10_Coaching_Feedback_and_Notes/Interview_Feedback/` - Save feedback if received

---

## Evaluating an Offer

**Workflow:** No dedicated workflow or command yet; use the documents below.

**Documents needed:**
- `07_Applications_and_Interviews/Applications/application-detail-template.md` - Offer decision matrix
- `07_Applications_and_Interviews/Offers_and_Negotiation/` - Offer and negotiation notes
- `04_Career_Goals_and_Strategy/Compensation_Targets/` - Check compensation targets
- `05_Personal_Profile/Work_Preferences/` - Check alignment
- `05_Personal_Profile/Non_Negotiables/` - Verify no deal-breakers
- `09_Research_and_Market_Intelligence/Compensation_Data/` - Reference compensation research

---

## Updating Your Resume

**Workflow:** See `WORKFLOWS.md` → "Updating Resume from Work Experience"

**Documents needed:**
- `02_Work_Experience/Projects/project-template.md` - Document new project
- `02_Work_Experience/Roles/` - Update role documentation
- `02_Work_Experience/Metrics_and_Outcomes/` - Add metrics
- `03_Skills_and_Portfolio/skills-inventory.md` - Education and certifications (checked against resumes)
- `01_Resume_and_Profiles/Resume_Master/` - Update master resume
- `/build-resume` - Create a tailored version in an opportunity folder

Facts in a resume or cover letter must exist in `02_`–`05_` first. If `scripts/careeros check` flags a true claim, add it to canonical content, or record a reasoned line in the opportunity folder's `grounding-waivers.md`.

---

## Documenting Work Experience

**Workflow:** See `WORKFLOWS.md` → "Updating Resume from Work Experience" (Step 1)

**Documents needed:**
- `02_Work_Experience/Projects/project-template.md` - Document project
- `02_Work_Experience/Roles/[role-name].md` - Update role info
- `02_Work_Experience/Metrics_and_Outcomes/` - Document metrics
- `07_Applications_and_Interviews/Interview_Prep/STAR-story-template.md` - Create interview story
- `02_Work_Experience/Stories/` - Canonical long-form stories
- `07_Applications_and_Interviews/Interview_Prep/story-inventory.md` - Add to inventory

---

## Networking Activities

**Workflow:** See `WORKFLOWS.md` → Various workflows

**Commands:** `/log-activity` records the outreach for the work search log.

**Documents needed:**
- `08_Networking_and_References/Contacts/contact-template.md` - Track contact
- `08_Networking_and_References/Informational_Interviews/informational-interview-template.md` - Info interview notes
- `08_Networking_and_References/References/reference-template.md` - Prepare reference
- `08_Networking_and_References/Contacts/` - Log recruiter outreach

---

## Weekly Maintenance

**Workflow:** See `WORKFLOWS.md` → "Weekly Maintenance Routine"

**Commands:** `/generate-weekly-cert`, `/sync-application-tracker`

**Documents needed:**
- `00_Core_OS/search-status.md` - Update priorities and status
- `00_Core_OS/career-index.md` - Review current focus
- `07_Applications_and_Interviews/Applications/application-tracker.md` - Update statuses
- `11_Job_Search_Activities/` - Work search log, weekly logs and certifications
- `10_Coaching_Feedback_and_Notes/Self_Reflection/` - Capture learnings

---

## Monthly Maintenance

**Workflow:** See `WORKFLOWS.md` → "Monthly Maintenance Routine"

**Documents needed:**
- `04_Career_Goals_and_Strategy/Career_Vision/` - Review vision
- `04_Career_Goals_and_Strategy/Role_Targets/` - Update targets
- `05_Personal_Profile/Work_Preferences/` - Review preferences
- `01_Resume_and_Profiles/Resume_Master/` - Update resume
- `08_Networking_and_References/Contacts/` - Review contacts
- `09_Research_and_Market_Intelligence/Compensation_Data/` - Update compensation data
- `99_Archive/` - Archive old materials

---

## Closing a Search

**Workflow:** See `WORKFLOWS.md` → "Archiving a Completed Search"

**Commands:** `/close-opportunity <folder> <pass|withdrawn|rejected|no_response> <your reason>`. It moves the folder to `99_Archive/Closed_Searches/`, marks it closed, and updates the Closed Searches README and the tracker. The reason must come from you.

**Documents needed:**
- `10_Coaching_Feedback_and_Notes/Interview_Feedback/` - Save feedback
- `10_Coaching_Feedback_and_Notes/Self_Reflection/` - Document learnings
- `00_Core_OS/career-index.md` and `search-status.md` - Update when the whole search ends

---

## Quick Reference: Document Types

### Control & Orientation
- `00_Core_OS/career-index.md` - Strategic control center
- `00_Core_OS/search-status.md` - Tactical status tracking
- `00_Core_OS/careeros-structure-map.md` - Where content belongs
- `STATUS_DEFINITIONS.md` - Status reference guide

### Runtime
- `00_Core_OS/Skills/<command>/SKILL.md` - Command contracts
- `00_Core_OS/Runs/` - One runtime IO file per command run
- `00_Core_OS/Prompts/` - Runtime, packs and pipelines

### Strategy & Planning
- `04_Career_Goals_and_Strategy/career-tracks.md` - Career tracks
- `04_Career_Goals_and_Strategy/Career_Vision/` - Long-term vision
- `04_Career_Goals_and_Strategy/Role_Targets/` - Target roles
- `04_Career_Goals_and_Strategy/Transition_Strategy/` - Career transitions
- `04_Career_Goals_and_Strategy/Compensation_Targets/` - Compensation goals

### Personal Profile
- `05_Personal_Profile/Work_Preferences/` - Work style preferences
- `05_Personal_Profile/Values_and_Principles/` - Core values
- `05_Personal_Profile/Non_Negotiables/` - Deal-breakers

### Opportunities, Applications & Interviews
- `06_Job_Opportunities/<company>_<role>_<date>/` - Everything for one opportunity
- `07_Applications_and_Interviews/Applications/application-tracker.md` - Master tracker
- `07_Applications_and_Interviews/Applications/application-detail-template.md` - Detail and offer matrix template
- `07_Applications_and_Interviews/Interview_Prep/story-inventory.md` - Story mapping
- `07_Applications_and_Interviews/Interview_Prep/STAR-story-template.md` - STAR stories
- `07_Applications_and_Interviews/Interview_Prep/SOAR-story-template.md` - SOAR stories

### Research
- `09_Research_and_Market_Intelligence/Company_Research/company-research-template.md` - Company research
- `09_Research_and_Market_Intelligence/Compensation_Data/compensation-research-template.md` - Compensation research

### Networking
- `08_Networking_and_References/Contacts/contact-template.md` - Contact tracking
- `08_Networking_and_References/Informational_Interviews/informational-interview-template.md` - Info interviews
- `08_Networking_and_References/References/reference-template.md` - Reference prep

---

## Link Format Standard

All links in this workspace use **relative paths** from the document's location:

- **Same folder:** `filename.md`
- **Parent folder:** `../filename.md`
- **Two levels up:** `../../filename.md`
- **Subfolder:** `subfolder/filename.md`
- **Parent subfolder:** `../subfolder/filename.md`

**Example from `07_Applications_and_Interviews/Applications/application-detail-template.md`:**
- To company research: `../../09_Research_and_Market_Intelligence/Company_Research/`
- To application tracker: `application-tracker.md` (same folder)
- To work experience: `../../02_Work_Experience/`

---

## Related Documents

- **Full workflows:** `WORKFLOWS.md` - Detailed step-by-step workflows
- **Quick start:** `QUICK_START.md` - Getting started guide
- **Status reference:** `STATUS_DEFINITIONS.md` - Status values and transitions
- **Main README:** `README.md` - System overview
- **Assistant contract:** `Career_Workspace_Assistant_prompt.md` - How the assistant operates here
