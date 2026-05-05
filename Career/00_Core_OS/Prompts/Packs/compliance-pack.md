---
Last Update: 2026-04-24
Previous Update:
---

# Compliance Pack

## 1. Purpose

Provide a **pre-configured prompt execution pack** for unemployment work-search compliance within CareerOS.

This pack standardizes how activities are:
- recorded (log entries)
- supported (evidence linkage)
- aggregated (weekly certifications)
- validated (audit readiness)

It ensures outputs are **audit-safe, deterministic, and grounded** in the canonical log.

This pack defines constraints, validation rules, and orchestration expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT execute logic directly; all execution is performed by runtime components.

---

## 2. Scope

This pack governs **documentation and certification only**.

It does NOT:
- determine eligibility for benefits
- replace TWC instructions or legal guidance
- modify canonical truth in other domains

---

## 3. Execution Profile

### Modes
- Primary: `execute`
- Secondary: `analyze` (for readiness assessment)

### Workflow Pattern

```
Activity → Log → Evidence → Weekly Snapshot → Submission Update
```

---

## 4. Governing Domains

### Canonical Log
- `/11_Job_Search_Activities/Work_Search_Log.md`

### Weekly Certifications
- `/11_Job_Search_Activities/Weekly_Certifications/`

### Evidence
- `/11_Job_Search_Activities/Evidence/`

### Related Context (read-only)
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/`
- `/08_Networking_and_References/`

Rules:

- Canonical log is the single source of truth
- Weekly certifications MUST NOT modify canonical log entries
- Evidence MUST be referenced, not embedded

---

## 5. Core Principles

### 5.1 Append-Only Logging
- Never edit or delete prior entries
- Corrections are appended as new entries

### 5.2 Truth Over Presentation
- Use factual, specific statements only
- Do not embellish outcomes

### 5.3 Minimal Sufficient Evidence
- Evidence is encouraged, not invented
- Missing evidence must be explicitly marked

### 5.4 Deterministic Structure
- All entries follow a strict schema
- All weekly files follow a strict template

### 5.5 Separation of Concerns
- Logging = event capture
- Certification = weekly aggregation

### 5.6 Context Integrity

- All entries MUST be grounded in actual user activity
- Assumptions MUST be explicitly labeled when present
- Missing information MUST be surfaced as gaps, not inferred

---

## 6. Activity Logging Contract

### Required Fields

Each log entry MUST include:

```yaml
activity_id:
activity_date:
activity_type:
twc_qualifying: true | false | needs_review
employer_or_platform:
role_or_subject:
method:
outcome_status:
evidence:
related_opportunity:
related_application:
retrospective: true | false
notes:
```

Additional Rules:

- All fields MUST be present; missing values must be marked `MISSING`
- No field may be silently omitted
- Assumptions MUST NOT replace required fields

### Activity Types (Normalized)
- application_submitted
- resume_sent
- recruiter_contact
- networking_message
- informational_interview
- interview
- follow_up
- job_research
- job_fair_or_event
- profile_update
- training_or_assessment
- other

### Method Types (Normalized)
- online_application
- email
- phone
- voicemail
- linkedin
- indeed
- company_website
- in_person
- video_call
- text_message
- other

---

### Qualifying Activity Decision Rule

Before recommending `/log-activity`, classify the event as either a qualifying candidate event or a non-qualifying internal event.

#### Qualifying Candidate Event (recommend `/log-activity`)
- application submitted
- resume sent to employer/recruiter
- interview scheduled
- interview completed
- networking contact made
- job fair attended
- employer follow-up sent
- recruiter communication completed

#### Non-Qualifying Internal Event (do NOT recommend `/log-activity`)
- resume drafted
- prompt run
- opportunity analyzed
- interview prep performed
- strategy updated
- artifact reorganized

#### Enforcement Rule
- Only recommend `/log-activity` for qualifying candidate events
- Do not recommend `/log-activity` for non-qualifying internal events
- If uncertain whether an event is candidate-facing or internal, mark `twc_qualifying: needs_review` before recommending a compliance action

---

## 7. Evidence Contract

### Storage
All evidence should be stored in:

```
/11_Job_Search_Activities/Evidence/
```

### Naming Standard

```
YYYY-MM-DD_<company-or-platform>_<activity-type>.<ext>
```

### Rules
- Do not fabricate evidence
- Preserve original files when possible
- Reference relative paths in log entries

Additional Rules:

- Evidence gaps MUST be explicitly tracked in log entries
- Evidence references MUST be verifiable and stable
- Absence of evidence MUST NOT block logging but MUST be disclosed

---

## 8. Weekly Certification Contract

### Inputs
- `Work_Search_Log.md`
- claim week (start/end)
- optional required activity count

### Outputs
- `Weekly_Certifications/YYYY-W##.md`

### Required Metrics
- total_activity_count
- qualifying_activity_count
- needs_review_activity_count
- nonqualifying_activity_count
- evidence_gap_count
- incomplete_entry_count

### Readiness States

#### ready
- required count provided
- qualifying >= required
- no missing required fields

#### needs_review
- required count missing OR
- some activities marked `needs_review` OR
- evidence gaps exist

#### incomplete
- missing required fields OR
- qualifying below requirement OR
- no activities

Execution Rules:

- Certification MUST reflect the exact state of the canonical log at time of generation
- No aggregation may introduce new or inferred data
- All assumptions and gaps MUST be surfaced in the certification output

---

## 9. Output Standards

### Log Entry
- appended to `Work_Search_Log.md`
- no reordering
- no mutation of prior entries

### Weekly Certification
- standalone snapshot
- never modifies source log
- includes summary, table, evidence review, and readiness

Additional Rules:

- Outputs MUST include required disclosures (assumptions, gaps, warnings)
- Outputs MUST align with `output-standards.md`
- Outputs MUST reflect context status (complete vs partial)

---

## 10. Command Mapping

### `/log-activity`
- writes new entries
- enforces schema
- links evidence

### `/generate-weekly-cert`
- reads canonical log
- aggregates weekly data
- produces certification file

Rules:

- Commands MUST NOT bypass runtime validation
- All command outputs MUST conform to output standards and pack constraints

---

## 12. Audit Safety Rules

- use true activity dates
- do not backdate creation (use retrospective flag)
- maintain traceability from log → evidence → certification
- ensure each activity is independently verifiable

---

## 13. Integration Notes

### With Application Pipeline
- application submission → recommend `/log-activity`

### With Networking
- outreach → recommend `/log-activity`

### With Interview Pipeline
- interview scheduled or completed → recommend `/log-activity`

---

## 14. Validation Hooks

- All log entries conform to schema
- No required fields are omitted
- All assumptions are explicitly labeled
- Evidence references are valid or gaps are disclosed
- Certifications accurately reflect log data
- No inferred or fabricated data is present

---

## 15. Summary

The Compliance Pack provides:

- a deterministic logging system
- an audit-safe weekly certification process
- strict data contracts for activities and evidence

It ensures deterministic, audit-safe, and fully traceable compliance tracking aligned with CareerOS runtime constraints.