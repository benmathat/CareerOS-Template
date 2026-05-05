---
Last Update: 2026-04-24
Previous Update:
---

# Compliance Pipeline

## 1. Purpose

Define the **operational workflow for unemployment work-search compliance** within CareerOS.

This pipeline ensures:
- all qualifying activities are captured
- evidence is linked and preserved
- weekly certifications are generated consistently
- audit-ready records are maintained

It is the **execution control layer** for compliance, built on top of the Compliance Pack.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only workflow-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

---

## 2. Scope

Use this pipeline to manage:
- daily activity logging
- evidence tracking
- weekly certification generation
- submission tracking

This pipeline governs **how compliance work is performed**, not eligibility decisions.

---

## 3. Pipeline Contract

### 3.1 Inputs

```yaml
inputs:
  work_search_log:
    path: /11_Job_Search_Activities/Work_Search_Log.md
  activity_event:
    type: application | networking | interview | research | other
    description: <text>
    timestamp: <datetime>
  context_refs:
    optional:
      - /06_Job_Opportunities/
      - /07_Applications_and_Interviews/
      - /08_Networking_and_References/
  twc_requirements:
    required_count_per_week: <integer | optional>
```

```yaml
validation:
  required_fields:
    - inputs.work_search_log
  failure_behavior: halt
```

### 3.2 Outputs

```yaml
outputs:
  log_entry:
    append_to: /11_Job_Search_Activities/Work_Search_Log.md
  evidence_link:
    path: /11_Job_Search_Activities/Evidence/
  weekly_certification:
    path: /11_Job_Search_Activities/Weekly_Certifications/
  submission_record:
    path: /11_Job_Search_Activities/Weekly_Certifications/
```

### Output Rules

- All outputs MUST align with `output-standards.md`
- All outputs MUST include required disclosures (assumptions, gaps, warnings) when applicable
- Outputs MUST reflect context status (complete vs partial)
- Outputs MUST NOT modify canonical sources

---

## 4. Outputs

This pipeline produces:
- log entries (append-only)
- evidence references
- weekly certification files
- submission records

---

## 5. Pipeline Overview

```text
Activity Occurs
    ↓
Log Activity
    ↓
Attach Evidence
    ↓
Daily Review (Optional)
    ↓
Weekly Aggregation
    ↓
Certification Generation
    ↓
Submission Update
```

## 6. Pipeline Stages

## 6.1 Stage 1 — Activity Capture

### Objective
Capture a work-search activity as soon as it occurs.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- All required fields MUST be present or marked `MISSING`
- No inferred or fabricated activity data is allowed

### Trigger
- application submitted
- networking outreach
- interview activity
- job search action

### Action
Run:

```text
/log-activity
```

### Output
- new log entry in `Work_Search_Log.md`

---

## 6.2 Stage 2 — Evidence Attachment

### Objective
Ensure supporting documentation is preserved.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- Evidence references MUST be valid and resolvable
- Missing evidence MUST be explicitly marked, not inferred

### Action
- store evidence in:
  `/11_Job_Search_Activities/Evidence/`
- ensure log entry references evidence

### Output
- traceable link from activity → evidence

---

## 6.3 Stage 3 — Daily Review (Optional)

### Objective
Maintain log completeness and accuracy.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- All context gaps MUST be surfaced explicitly
- No silent corrections or inferred updates

### Actions
- verify all activities are logged
- confirm required fields are populated
- confirm evidence references where available

### Output
- clean, complete log for the day

---

## 6.4 Stage 4 — Weekly Aggregation

### Objective
Prepare activity set for certification.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- Aggregation MUST reflect exact log state
- No inferred or reconstructed activity is allowed

### Trigger
- end of claim week

### Action
- identify claim week date range
- confirm all activities for the week are logged

---

## 6.5 Stage 5 — Certification Generation

### Objective
Create an audit-safe weekly certification snapshot.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- Certification MUST be fully traceable to log entries
- Assumptions MUST be explicitly labeled if present

### Action
Run:

```text
/generate-weekly-cert
```

### Output
- `Weekly_Certifications/YYYY-W##.md`

---

## 6.6 Stage 6 — Submission Update

### Objective
Record submission to TWC.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- Submission metadata MUST be verifiable
- No inferred submission data may be introduced

### Actions
- update weekly certification file:
  - `submission_status: submitted`
  - `submission_date`
  - `submission_confirmation`
- attach submission evidence if available

### Output
- completed certification record

---

## 7. Control Logic

```text
IF activity_event detected:
    run Stage 1 (Activity Capture)

IF log_entry_created:
    run Stage 2 (Evidence Attachment)

IF end_of_day:
    optionally run Stage 3 (Daily Review)

IF end_of_week:
    run Stage 4 (Weekly Aggregation)

IF aggregation_complete:
    run Stage 5 (Certification Generation)

IF certification_generated:
    run Stage 6 (Submission Update)
```

---

## 8. Cadence Model

### Real-Time (Required)
- log activity immediately after it occurs

### Daily (Recommended)
- review log completeness

### Weekly (Required)
- generate certification
- submit to TWC

---

## 9. Source Routing

Allowed sources by stage:

- Stage 1–2:
  - /11_Job_Search_Activities/
  - optional references: /06_, /07_, /08_

- Stage 3–6:
  - /11_Job_Search_Activities/

Rules:
- canonical log is source of truth
- no cross-stage inference
- all references must resolve to existing artifacts

Additional Rules:

- Canonical log is authoritative
- No cross-stage inference is allowed
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 10. Failure Handling

### Stage Failure Conditions
- missing required input → halt
- unresolved reference → halt
- invalid log structure → halt
- missing evidence (if required) → mark MISSING, continue

---

## 11. Compliance Safeguards

- append-only log (no edits)
- explicit missing data marking
- evidence traceability
- weekly snapshot immutability
- no inference of qualifying status

---

## 12. Integration Points

### Application Pipeline
- after application → recommend `/log-activity`

### Networking Pipeline
- after outreach → recommend `/log-activity`

### Interview Pipeline
- after interview → recommend `/log-activity`

---

## 12.1 Runtime Integration Contract

- prompt-assembler.md
  - builds commands (/log-activity, /generate-weekly-cert)

- context-loader.md
  - resolves log, evidence, and references

- source-routing.md
  - enforces allowed directories per stage

- execution-flow.md
  - enforces sequencing and halt behavior

This pipeline defines workflow intent.
Runtime defines execution mechanics.

## 13. Validation Hooks

- All stage outputs are valid runtime objects
- All entries are traceable to source or explicitly labeled assumptions
- No unsupported or fabricated data is present
- Evidence references are valid or explicitly marked missing
- Pipeline state progression is valid and consistent
- All required disclosures are present

## 14. Summary

The Compliance Pipeline ensures:

- continuous capture of work-search activities
- structured evidence management
- consistent weekly certification generation
- audit-safe documentation

It ensures deterministic, audit-safe, and fully traceable compliance workflows aligned with CareerOS runtime constraints.
