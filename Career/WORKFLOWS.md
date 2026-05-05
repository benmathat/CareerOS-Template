---
Last Update: 2026-05-05
Previous Update: 2026-01-20
---

# Career Workspace Workflows

This document describes how workflows connect across folders in the Career workspace. Use these workflows to understand how to move information and activities through the system.

## Runtime-First Execution Note

These workflows describe domain process flow. Command execution in the current implementation is controlled by runtime contracts and command entrypoints:

- `00_Core_OS/Prompts/Runtime/operator-runbook.md`
- `.cursor/commands/*.md`
- `.cursor/runtime/<command>.runtime-io.yaml`
- `scripts/run_command_gate.sh ".cursor/runtime/<command>.runtime-io.yaml"`

When workflow guidance conflicts with command/runtime contracts, follow runtime contracts.

## Table of Contents

1. [Starting a New Job Search](#starting-a-new-job-search)
2. [Processing a New Opportunity](#processing-a-new-opportunity)
3. [Updating Resume from Work Experience](#updating-resume-from-work-experience)
4. [Archiving a Completed Search](#archiving-a-completed-search)
5. [Weekly Maintenance Routine](#weekly-maintenance-routine)
6. [Monthly Maintenance Routine](#monthly-maintenance-routine)

---

## Starting a New Job Search

**When to use:** Beginning a new job search, restarting after a pause, or pivoting to new target roles.

### Step 1: Set Strategic Foundation

**Location:** `04_Career_Goals_and_Strategy/`

1. **Define or update your career vision**
   - Use template: `Career_Vision/career-vision-template.md`
   - Document where you want to be in 5-10 years
   - Clarify values and long-term goals

2. **Define target roles**
   - Use template: `Role_Targets/role-target-template.md`
   - Create one file per target role type
   - Document requirements, alignment, and gaps

3. **Set compensation targets**
   - Use template: `Compensation_Targets/` (create compensation-research document)
   - Research market rates
   - Set realistic but ambitious targets

4. **If transitioning, create transition strategy**
   - Use template: `Transition_Strategy/transition-strategy-template.md`
   - Document current state, target state, and gap analysis
   - Create phased plan

### Step 2: Update Personal Profile

**Location:** `05_Personal_Profile/`

1. **Clarify work preferences**
   - Use template: `Work_Preferences/work-preferences-template.md`
   - Document location, schedule, team, and culture preferences
   - Identify must-haves vs. nice-to-haves

2. **Assess values alignment**
   - Use template: `Values_and_Principles/values-assessment-template.md`
   - Document core values and principles
   - Use to evaluate company fit

### Step 3: Update Control Documents

**Location:** `00_Core_OS/`

1. **Update `career-index.md`**
   - Set current focus
   - List primary and secondary target roles
   - Document geographic/remote preferences
   - Link to active materials (resumes, strategy docs)

2. **Initialize `search-status.md`**
   - Mark current phase (Exploration)
   - Set weekly priorities
   - Document active pipelines
   - Set up metrics tracking

### Step 4: Prepare Materials

**Location:** `01_Resume_and_Profiles/`

1. **Update master resume**
   - Pull from `02_Work_Experience/`
   - Ensure it reflects current state
   - Keep as source of truth

2. **Prepare tailored resume variants** (if needed)
   - Create role-specific versions
   - Store in `Tailored_Resumes/`

### Step 5: Set Up Tracking

**Location:** `07_Applications_and_Interviews/`

1. **Initialize application tracker**
   - Open `Applications/application-tracker.md`
   - Set up table structure
   - Prepare for tracking

2. **Review interview prep materials**
   - Check `Interview_Prep/story-inventory.md`
   - Ensure STAR/SOAR stories are ready
   - Update story inventory if needed

### Step 6: Begin Opportunity Intake

**Location:** `06_Job_Opportunities/`

1. **Set up opportunity tracking**
   - Use `Job_Postings/` for interesting roles
   - Use `Recruiter_Outreach/recruiter-outreach-log.md` for inbound messages
   - Use `Companies_of_Interest/` for target companies

**Result:** You now have a clear foundation, updated materials, and a system ready to capture opportunities.

---

## Processing a New Opportunity

**When to use:** You've identified an interesting role or received recruiter outreach and want to evaluate and potentially apply.

### Step 1: Capture the Opportunity

**Location:** `06_Job_Opportunities/`

**If it's a job posting:**
- Save posting details in `Job_Postings/`
- Note why it's interesting
- Add initial evaluation notes

**If it's recruiter outreach:**
- Log in `Recruiter_Outreach/recruiter-outreach-log.md`
- Use the template to capture contact info, role details, and initial conversation

**If it's a company of interest:**
- Add to `Companies_of_Interest/` if not already there
- Note why the company is interesting

### Step 2: Research and Evaluate

**Location:** `09_Research_and_Market_Intelligence/`

1. **Research the company**
   - Use template: `Company_Research/company-research-template.md`
   - Create one file per company
   - Document business model, culture, recent news, risks/opportunities

2. **Research compensation** (if relevant)
   - Use template: `Compensation_Data/compensation-research-template.md`
   - Research market rates for the role
   - Set negotiation targets

3. **Check role benchmarks**
   - Review `Role_Benchmarks/` for similar roles
   - Compare requirements against your experience

### Step 3: Evaluate Alignment

**Check against:**
- `04_Career_Goals_and_Strategy/Role_Targets/` — Does it match your targets?
- `05_Personal_Profile/Work_Preferences/` — Does it meet your preferences?
- `05_Personal_Profile/Values_and_Principles/` — Does it align with your values?
- `05_Personal_Profile/Non_Negotiables/` — Does it violate any deal-breakers?

**Decision point:** Apply, research more, or archive?

### Step 4: If Applying — Move to Execution

**Location:** `07_Applications_and_Interviews/`

1. **Create application detail file**
   - Use template: `Applications/application-detail-template.md`
   - Create file: `Applications/company-role.md`
   - Fill in snapshot, role understanding, company context, alignment

2. **Update application tracker**
   - Add row to `Applications/application-tracker.md`
   - Set status to "Applied"
   - Link to application detail file

3. **Prepare materials**
   - Select or create tailored resume
   - Write cover letter using `01_Resume_and_Profiles/Cover_Letters/cover-letter-template.md`
   - Link cover letter to application detail file

4. **Submit application**
   - Update application detail with date applied
   - Set follow-up reminder

### Step 5: Track Progress

**As the process continues:**

1. **Update application detail file** with:
   - Interview notes (use interview log section)
   - Feedback received
   - Status changes

2. **Update application tracker** with:
   - Current status
   - Last action date
   - Next action

3. **Capture feedback** in:
   - `10_Coaching_Feedback_and_Notes/Interview_Feedback/` (if received)
   - `10_Coaching_Feedback_and_Notes/Resume_Feedback/` (if received)

**Result:** Opportunity is tracked from initial interest through final outcome, with all context preserved.

---

## Updating Resume from Work Experience

**When to use:** After completing a project, achieving a milestone, or when preparing for applications.

### Step 1: Capture Raw Experience

**Location:** `02_Work_Experience/`

1. **Document the project/achievement**
   - Use template: `Projects/project-template.md`
   - Create file: `Projects/project-name.md`
   - Document context, problem, actions, outcomes, metrics

2. **Update role documentation** (if applicable)
   - Update file in `Roles/` for the relevant role
   - Add new responsibilities or achievements

3. **Extract metrics**
   - Add to `Metrics_and_Outcomes/` if significant
   - Quantify impact where possible

4. **Develop stories** (if interview-worthy)
   - Use templates: `Stories/STAR-story-template.md` or `SOAR-story-template.md`
   - Create story files in `Stories/`
   - Update `07_Applications_and_Interviews/Interview_Prep/story-inventory.md`

### Step 2: Update Master Resume

**Location:** `01_Resume_and_Profiles/Resume_Master/`

1. **Review new experience documents**
   - Read project files, role updates, metrics
   - Identify resume-worthy bullets

2. **Add to master resume**
   - Add new role/project if applicable
   - Update existing role with new achievements
   - Incorporate metrics and outcomes
   - Use resume-worthy bullets from project templates

3. **Maintain truth**
   - Keep master resume as source of truth
   - Don't exaggerate or invent
   - Ensure all claims are supported by experience docs

### Step 3: Create Tailored Versions (As Needed)

**Location:** `01_Resume_and_Profiles/Tailored_Resumes/`

1. **When applying to specific roles:**
   - Copy master resume
   - Tailor based on role requirements (from `04_Career_Goals_and_Strategy/Role_Targets/`)
   - Emphasize relevant experience
   - Adjust language to match role/industry

2. **Link to application**
   - Note which resume version used in application detail file
   - Track resume versions in application tracker

### Step 4: Update Online Profiles

**Location:** `01_Resume_and_Profiles/Online_Profiles/`

1. **Update LinkedIn and other profiles**
   - Sync with master resume (or tailored version)
   - Ensure consistency
   - Update as needed for different platforms

**Result:** Resume reflects latest experience, with source documentation preserved for future reference and interview prep.

---

## Archiving a Completed Search

**When to use:** After accepting an offer, deciding to pause, or completing a search cycle.

### Step 1: Finalize Active Applications

**Location:** `07_Applications_and_Interviews/`

1. **Update all application detail files**
   - Mark final status (Offer Accepted, Rejected, Withdrawn)
   - Document outcomes and key takeaways
   - Complete reflection sections

2. **Update application tracker**
   - Move closed applications to "Closed Applications" section
   - Add key lessons
   - Note whether you'd reapply

3. **Capture final feedback**
   - Save any rejection feedback to `10_Coaching_Feedback_and_Notes/Interview_Feedback/`
   - Document what worked and what didn't

### Step 2: Extract Learnings

**Location:** Various folders

1. **Update story inventory**
   - Note which stories worked well
   - Identify gaps in story coverage
   - Update `07_Applications_and_Interviews/Interview_Prep/story-inventory.md`

2. **Document lessons learned**
   - Add to `10_Coaching_Feedback_and_Notes/Self_Reflection/`
   - Capture insights about process, materials, or approach

3. **Update strategy based on learnings**
   - Revise `04_Career_Goals_and_Strategy/Role_Targets/` if needed
   - Update `05_Personal_Profile/Work_Preferences/` based on what you learned
   - Adjust `04_Career_Goals_and_Strategy/Compensation_Targets/` with new data

### Step 3: Archive Materials

**Location:** `99_Archive/`

1. **Move completed search materials**
   - Create folder: `99_Archive/search-YYYY-MM/`
   - Move:
     - Closed application detail files
     - Old tailored resumes (if not keeping active)
     - Search-specific notes

2. **Keep active materials**
   - Keep master resume active
   - Keep work experience docs active (they're permanent)
   - Keep strategy docs active (they inform future searches)

### Step 4: Update Control Documents

**Location:** `00_Core_OS/`

1. **Update `career-index.md`**
   - Clear active job searches table (or mark as complete)
   - Update current focus if starting new role
   - Archive old search status

2. **Update `search-status.md`**
   - Mark phase as "Paused / Maintenance" or "Complete"
   - Clear active pipelines
   - Document final metrics

3. **Archive `search-status.md`** (optional)
   - Copy to `99_Archive/search-YYYY-MM/` if starting fresh
   - Create new `search-status.md` for next search

### Step 5: Maintain Network

**Location:** `08_Networking_and_References/`

1. **Thank references**
   - Update `References/reference-template.md` files
   - Send thank-you notes
   - Maintain relationships

2. **Update contacts**
   - Note outcomes in `Contacts/contact-template.md` files
   - Maintain relationships with helpful contacts
   - Update `Informational_Interviews/` notes with outcomes

**Result:** Search is properly closed, learnings are captured, materials are archived, and network relationships are maintained.

---

## Weekly Maintenance Routine

**When:** Every week during an active search, or bi-weekly during maintenance mode.

### Monday: Orientation & Planning

**Location:** `00_Core_OS/`

1. **Review `career-index.md`**
   - Confirm current focus and targets
   - Check that active materials are up to date

2. **Update `search-status.md`**
   - Review last week's priorities
   - Set new weekly priorities (3 items max)
   - Update current phase if changed
   - Update active pipelines status

### Tuesday-Thursday: Execution

**Daily:**
- Log new opportunities in `06_Job_Opportunities/`
- Update application tracker as status changes
- Capture interview notes immediately after interviews
- Follow up on pending actions

### Friday: Reflection & Cleanup

**Location:** Various folders

1. **Update application tracker**
   - Review all active applications
   - Update statuses
   - Note follow-ups due next week

2. **Capture week's learnings**
   - Add to `10_Coaching_Feedback_and_Notes/Self_Reflection/`
   - Note what worked, what didn't

3. **Update metrics** (in `search-status.md`)
   - Applications sent this week
   - Interviews completed
   - Offers received

4. **Reality check** (in `search-status.md`)
   - What's working?
   - What's not?
   - What should I stop doing?
   - What should I double down on?

**Time investment:** 30-60 minutes per week

---

## Monthly Maintenance Routine

**When:** Once per month, regardless of search status.

### Strategic Review

**Location:** `04_Career_Goals_and_Strategy/`

1. **Review career vision**
   - Is it still aligned?
   - Update if priorities have shifted

2. **Review role targets**
   - Are targets still relevant?
   - Update based on market feedback
   - Add new targets if exploring

3. **Review transition strategy** (if applicable)
   - Update progress
   - Adjust timeline if needed
   - Celebrate milestones

### Personal Profile Review

**Location:** `05_Personal_Profile/`

1. **Review work preferences**
   - Have preferences changed?
   - Update based on new information

2. **Review values assessment**
   - Still accurate?
   - Any new insights?

### Materials Review

**Location:** `01_Resume_and_Profiles/`

1. **Review master resume**
   - Is it current?
   - Any new experience to add?
   - Any language to improve?

2. **Archive old tailored resumes**
   - Move unused tailored resumes to `99_Archive/`
   - Keep only active/recent versions

### Network Maintenance

**Location:** `08_Networking_and_References/`

1. **Review contacts**
   - Who haven't you talked to recently?
   - Schedule follow-ups
   - Update contact information

2. **Review references**
   - Are references still current?
   - Update contact information
   - Thank recent references

### Research Update

**Location:** `09_Research_and_Market_Intelligence/`

1. **Update compensation research**
   - Check for new market data
   - Update ranges if needed

2. **Review company research**
   - Update with recent news
   - Archive outdated research

### Archive Cleanup

**Location:** `99_Archive/`

1. **Review archive structure**
   - Ensure old searches are properly archived
   - Consolidate if needed

### Control Documents Update

**Location:** `00_Core_OS/`

1. **Review `career-index.md`**
   - Update current focus if changed
   - Ensure links are still valid
   - Update key people list

2. **Review activity log**
   - Check that it's being maintained
   - Look for patterns or gaps

**Time investment:** 2-3 hours per month

---

## Workflow Principles

### 1. Flow Direction
- **Truth flows up:** Raw experience (`02_Work_Experience/`) → Resumes (`01_Resume_and_Profiles/`)
- **Strategy guides execution:** Strategy (`04_Career_Goals_and_Strategy/`) → Applications (`07_Applications_and_Interviews/`)
- **Learning flows back:** Feedback (`10_Coaching_Feedback_and_Notes/`) → Strategy and Materials

### 2. Decision Points
- **06_Job_Opportunities/** → Evaluate → **07_Applications_and_Interviews/** (apply) or Archive (don't apply)
- **07_Applications_and_Interviews/** → Outcome → **99_Archive/** (closed) or Continue (active)

### 3. Maintenance Frequency
- **Daily:** Log activities, update trackers
- **Weekly:** Review status, set priorities, reflect
- **Monthly:** Strategic review, network maintenance, archive cleanup

### 4. Archive Philosophy
- Archive when complete, not when inconvenient
- Keep master materials active (resume, work experience, strategy)
- Archive execution materials (applications, tailored resumes from closed searches)

---

## Quick Reference: Common Workflows

### "I found an interesting job posting"
1. Save to `06_Job_Opportunities/Job_Postings/`
2. Research company in `09_Research_and_Market_Intelligence/Company_Research/`
3. Evaluate against `04_Career_Goals_and_Strategy/Role_Targets/` and `05_Personal_Profile/`
4. If applying: Create application detail in `07_Applications_and_Interviews/Applications/`
5. Update tracker

### "I had an interview"
1. Immediately capture notes in application detail file
2. Update application tracker status
3. Send thank-you note
4. Add to story inventory if new story emerged
5. Update interview prep based on questions asked

### "I completed a project at work"
1. Document in `02_Work_Experience/Projects/` using template
2. Extract resume-worthy bullets
3. Update master resume
4. Develop STAR/SOAR story if interview-worthy
5. Update story inventory

### "I received feedback"
1. Save to appropriate folder in `10_Coaching_Feedback_and_Notes/`
2. Extract actionable items
3. Update relevant materials (resume, stories, strategy)
4. Track improvements over time

---

## Notes

- These workflows are guidelines, not rigid rules
- Adapt workflows to your specific needs
- The goal is clarity and momentum, not perfection
- Regular maintenance prevents overwhelm and context loss
