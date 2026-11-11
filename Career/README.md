---
Last Update: 2026-11-11
Previous Update: 2026-10-09
---

# Career Workspace

This folder is a **career operating system**.

It is designed to support both:
- **Long-term career management** (clarity, direction, leverage)
- **Short-term job seeking** (focus, execution, learning)

The structure separates **thinking from doing**, **truth from presentation**, and **inputs from outputs**, allowing you to operate deliberately rather than reactively.

---

## Core Design Principles

### 1. Strategy Before Volume
This system prioritizes **clarity of direction** over mass applications.  
You should always know *why* you’re applying to something before you apply.

### 2. Truth Is Separate from Polish
Raw experience, metrics, and stories live separately from resumes and cover letters.  
This prevents rewriting history every time you tailor a resume.

### 3. One Source of Truth
Your experience, goals, preferences, and constraints live here — not in your head, inbox, or scattered documents.

### 4. Compounding Learning
Every application, interview, and rejection generates signal.  
This structure captures and reuses that signal.

### 5. Designed for Iteration
This workspace supports multiple searches, role pivots, pauses, and restarts without losing context.

### 6. Grounded Claims Only
Resumes, cover letters and analyses may state only what traces back to your canonical records (`02_`–`05_`). Scripts check employers, titles, dates, metrics and credentials against those records, and anything unsupported is flagged instead of written.

### 7. Commands With Contracts
Each step of a search (sourcing, intake, analysis, resume, application, logging, closing) is a command with a written contract in `00_Core_OS/Skills/` and a pass/fail conformance gate. See the command list in the root [`README.md`](../README.md).

---

## How the Structure Maps to the Career Process

Think of the folders as a **pipeline**, not a filing cabinet.

All folders described below are located within the `Career/` workspace:

- `Career/00_Core_OS/`
- `Career/01_Resume_and_Profiles/`
- `Career/02_Work_Experience/`
- `Career/03_Skills_and_Portfolio/`
- `Career/04_Career_Goals_and_Strategy/`
- `Career/05_Personal_Profile/`
- `Career/06_Job_Opportunities/`
- `Career/07_Applications_and_Interviews/`
- `Career/08_Networking_and_References/`
- `Career/09_Research_and_Market_Intelligence/`
- `Career/10_Coaching_Feedback_and_Notes/`
- `Career/11_Job_Search_Activities/`
- `Career/99_Archive/`
- `Career/INBOX/`

---

## INBOX — Staging Area for Incoming Documents

**Location:** `Career/INBOX/`

**Purpose:**  
Capture incoming documents and materials before processing and organizing them into the appropriate sections of CareerOS.

This folder serves as a **staging area** for:
- Documents received from recruiters, hiring managers, or contacts
- Job postings or role descriptions to be evaluated
- Company research materials
- Interview notes that need to be processed
- Feedback or coaching notes
- Any other career-related documents that need to be reviewed and filed

**Use this when:**
- You receive a document via email, message, or download
- You need to quickly capture something before you have time to process it
- You're unsure where something belongs and need to decide later
- You want to batch process multiple items at once

**Workflow:**
1. **Capture** - Drop incoming documents here immediately
2. **Process** - Regularly review and move items to their proper locations
3. **Archive** - Move processed items to `99_Archive/` if they're no longer needed

**Key Rules:**
- **Keep it lean** - Process items regularly (daily or weekly)
- **Don't let it accumulate** - Empty it as part of your weekly review
- **Use descriptive filenames** - Include dates and source when saving items
- **When in doubt, put it here** - Better to capture first, organize later

---

## 00_Core_OS — Orientation & Control

**Location:** `Career/00_Core_OS/`

**Purpose:**  
This is the control plane of the system.

- Defines what you are doing *right now*
- Links to active materials
- Prevents drift and context loss
- Holds the assistant's prompt runtime (`Prompts/`), the command contracts (`Skills/`) and a record of each command run (`Runs/`)

**Use this when:**
- You feel scattered
- You restart a search
- You want a weekly or monthly reset

---

## 01_Resume_and_Profiles — External Representation

**Location:** `Career/01_Resume_and_Profiles/`

**Purpose:**  
How you present yourself to the outside world.

This folder contains reusable presentation assets:
- A comprehensive master resume content pool (`Resume_Master/`)
- Per-career-track resume baselines, with page-limited variants
- DOCX and markdown templates (`Templates/`)
- Online profile text

Resumes and cover letters tailored to a specific opportunity live in that opportunity's folder in `06_Job_Opportunities/`, not here.

**Key rule:**  
This folder consumes information from other folders — it does not originate it.

---

## 02_Work_Experience — Raw Career Data

**Location:** `Career/02_Work_Experience/`

**Purpose:**  
This is your **career memory**.

It captures:
- Employers and roles
- Projects and initiatives
- Achievements and failures
- Metrics and outcomes
- Long-form canonical story inventory in `Career/02_Work_Experience/Stories/`

**Use this when:**
- Updating resumes
- Preparing interview stories
- Answering “tell me about a time…”

This folder grows over time and should never be “cleaned up.”

---

## 03_Skills_and_Portfolio — Proof of Capability

**Location:** `Career/03_Skills_and_Portfolio/`

**Purpose:**  
Demonstrates *what you can actually do*.

Includes:
- Technical skills
- Leadership examples
- Writing, presentations, artifacts
- Portfolio items

This folder bridges **experience** and **evidence**.

---

## 04_Career_Goals_and_Strategy — Direction & Constraints

**Location:** `Career/04_Career_Goals_and_Strategy/`

**Purpose:**  
Defines where you are going and what you are optimizing for.

Includes:
- Career vision
- Career tracks (`career-tracks.md`) and the role targets that govern positioning for each
- Search strategy and interviewing strategy
- Compensation and lifestyle constraints
- Transition strategy

**Use this when:**
- Evaluating opportunities
- Saying no
- Avoiding panic-driven decisions

If this folder is empty, the job search will feel chaotic.

---

## 05_Personal_Profile — Self-Knowledge

**Location:** `Career/05_Personal_Profile/`

**Purpose:**  
Aligns work with how you actually operate.

Includes:
- Values and principles
- Personality assessments
- Strengths and weaknesses
- Work preferences and non-negotiables

This folder protects you from repeating bad-fit roles.

---

## 06_Job_Opportunities — One Folder per Opportunity

**Location:** `Career/06_Job_Opportunities/`

**Purpose:**  
Holds every opportunity you have decided to pursue or evaluate, from posting through application.

Each opportunity gets its own `<company>_<role>_<YYYY-MM-DD>/` folder containing the posting record, analysis, tailored resume and cover letter, application notes and record, and next steps. New postings stage in `INBOX/Job_Postings/` first (`intake-job`), and `promote-opportunity` creates the folder.

The README keeps a generated index of open opportunities grouped by career track (`scripts/careeros index --write`). Finished opportunities move to `99_Archive/Closed_Searches/` via `close-opportunity`.

This prevents prematurely converting curiosity into obligation.

---

## 07_Applications_and_Interviews — Execution & Feedback Loop

**Location:** `Career/07_Applications_and_Interviews/`

**Purpose:**  
This is the execution engine.

Tracks:
- Applications (the cross-opportunity tracker lives in `Applications/application-tracker.md`)
- Interview prep
- Interview notes
- Offers and negotiation
- Purpose-built, application-specific story variants in `Career/07_Applications_and_Interviews/Interview_Prep/Stories/`

This folder turns activity into insight.

Every interaction should leave a trace here.

**Story boundary rule:** Canonical long-form stories belong in `Career/02_Work_Experience/Stories/`. Use `Career/07_Applications_and_Interviews/Interview_Prep/Stories/` only for role/application-specific variants prepared for active interview loops.

---

## 08_Networking_and_References — People, Not Postings

**Location:** `Career/08_Networking_and_References/`

**Purpose:**  
Career progress is driven by relationships, not listings.

Includes:
- Contacts
- Informational interviews
- Mentors and advisors
- References

This folder compounds quietly over time.

---

## 09_Research_and_Market_Intelligence — Context & Leverage

**Location:** `Career/09_Research_and_Market_Intelligence/`

**Purpose:**  
Informs decisions and negotiation.

Includes:
- Industry trends
- Company research
- Role benchmarks
- Compensation data
- Saved opportunity sourcing reports and sighting history (`Opportunity_Sourcing/`, produced by `source-opportunities`)

Use this to:
- Ask better interview questions
- Price yourself accurately
- Detect red flags early

---

## 10_Coaching_Feedback_and_Notes — Improvement Engine

**Location:** `Career/10_Coaching_Feedback_and_Notes/`

**Purpose:**  
Captures external perspective and reflection.

Includes:
- Resume feedback
- Interview feedback
- Coaching notes

This folder ensures you improve deliberately, not accidentally.

---

## 11_Job_Search_Activities — Unemployment Compliance

**Location:** `Career/11_Job_Search_Activities/`

**Purpose:**  
Documents work search activities in compliance with your unemployment agency's eligibility requirements. Provides an audit-safe system for tracking and certifying job search activities. The agency, jurisdiction and certification rules are configured in `compliance-profile.md`; skip this section if you are not claiming benefits.

Includes:
- Work search activity log (canonical record)
- Weekly certifications (snapshots submitted to your agency)
- Evidence folder (supporting documentation)

**Use this when:**
- Filing weekly unemployment certifications
- Documenting required work search activities
- Providing proof of activities if audited
- Protecting yourself in case of disputes

This folder focuses on **compliance and audit protection**, while other folders focus on strategy and execution.

---

## 99_Archive — Preserve Without Clutter

**Location:** `Career/99_Archive/`

**Purpose:**  
Keeps the system lean without losing history.

Includes:
- Old resumes
- Closed searches (`Closed_Searches/`, filled by `close-opportunity` with an outcome and reason)
- Past offers
- Legacy materials

Nothing is deleted — it is just deactivated.

---

## How to Use This System Week to Week

1. Process `Career/INBOX/` - Review and file incoming documents
2. Review `Career/00_Core_OS/search-status.md`
3. Source and screen new postings (`source-opportunities`), then stage the ones worth a look (`intake-job`, `promote-opportunity`)
4. Work each opportunity through `analyze-opportunity`, `discuss-opportunity`, `build-resume` and `build-application`
5. Keep the application tracker current (`sync-application-tracker`); check for stalled applications with `scripts/careeros lapsed`
6. If you claim unemployment benefits, log work search activities as they happen (`log-activity`) and certify each period (`generate-weekly-cert`)
7. Capture interview notes immediately
8. Extract lessons into stories or strategy
9. Close finished searches (`close-opportunity`) and archive aggressively

## Runtime-First Command Path (Primary Execution)

For command-driven CareerOS execution, use this path first:

1. `00_Core_OS/Prompts/README.md`
2. `00_Core_OS/Prompts/Runtime/operator-runbook.md`
3. `Career/00_Core_OS/Skills/*/SKILL.md` command contracts
4. `Career/00_Core_OS/Runs/<YYYY-MM-DD>_<command-name>_<slug>.runtime-io.yaml` runtime emission files
5. `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_<command-name>_<slug>.runtime-io.yaml"` before final writes

Start each run with `scripts/careeros new-run <command> <slug>`, which writes the runtime IO skeleton. Mechanical rules (date, slugs, frontmatter rotation, closing, indexing, validation) live in `scripts/careeros`, and `scripts/careeros check` is the pre-commit gate. Enable it once per clone with `git config core.hooksPath scripts/hooks`.

`QUICK_START.md` and `WORKFLOWS.md` remain useful for workspace setup and general process guidance, but runtime command behavior is governed by prompt runtime contracts and command docs.

If you are unsure where something belongs:
- Ask: **Is this thinking, doing, or learning?**
- Then place it accordingly.

---

## Starting an Assistant Session

- **Claude Code (primary):** `CLAUDE.md` imports `AGENTS.md` and `Career_Workspace_Assistant_prompt.md`, so the assistant contract loads automatically. Run commands as slash commands (`/intake-job`, `/build-resume`, ...). In Codex, use `$<name>` or `/skills`.
- **Cursor, Codex, other agents:** these read `AGENTS.md`. To start an interactive session, use an explicit load instruction with the prompt reference, since a bare file reference may not consistently trigger startup behavior:
  - `Load @Career/Career_Workspace_Assistant_prompt.md`

---

## Final Note

This workspace is not just for “finding a job.”

It is meant to:
- Reduce anxiety
- Increase clarity
- Preserve leverage
- Support long-term career ownership

Treat it as infrastructure — not a temporary folder.