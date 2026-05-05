---
Last Update: 2026-04-24
Previous Update: 2026-04-22
---

# Application Pipeline (Pipeline Contract)

## 1. Purpose

Define the **standard orchestration flow** for moving from a new opportunity to a completed application workflow inside CareerOS.

This pipeline coordinates runtime components and execution packs so that opportunities are handled consistently, with explicit decision gates, state transitions, artifact routing, and resumability.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only workflow-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It is the orchestration layer connecting:

- Opportunity Analysis Pack
- Resume Pack
- Application Pack
- Interview Pack
- application-specific artifacts and records

It MUST:
- define ordered stages
- define stage inputs and outputs
- define decision gates and state transitions
- define artifact routing and record updates
- include automatic synchronization of `07_Applications_and_Interviews/Applications/application-tracker.md` when application state changes
- support resume-from-last-valid-stage execution

It MUST NOT:
- duplicate runtime logic owned by packs or runtime contracts
- treat presentation artifacts as canonical truth
- silently skip decision gates or validation steps

---

## 2. Scope

Use this pipeline when:

- a new opportunity is added to CareerOS
- an existing opportunity is being reconsidered
- a role is being advanced from evaluation to active pursuit
- application materials need to be generated in a consistent way
- interview preparation needs to be attached to an active application

This pipeline governs **workflow orchestration**, not the content logic of any single artifact.

---

## 3. Pipeline Interface

### 3.1 Required Inputs

```yaml
request:
  opportunity:
    job_description: <text | file reference>
    company: <string>
    role: <string>
  career_context:
    goals_and_constraints: <file reference | structured input>

validation:
  required_fields:
    - opportunity.job_description
    - opportunity.company
    - opportunity.role
  failure_behavior: halt
```

### 3.2 Optional Inputs

```yaml
request:
  compensation_details: <text | file reference>
  company_research: <file reference>
  existing_resume_variant: <file reference>
  existing_networking_context: <file reference>
  prior_application_notes: <file reference>
```

### 3.3 Pipeline Outputs

```yaml
pipeline_outputs:
  opportunity_record:
    path: /06_Job_Opportunities/
  fit_risk_review:
    path: /06_Job_Opportunities/
  tailored_resume:
    path: /01_Resume_and_Profiles/
  messaging_draft_package:
    path: /01_Resume_and_Profiles/
  submission_preparation_record:
    path: /07_Applications_and_Interviews/
  application_record:
    path: /07_Applications_and_Interviews/
  follow_up_plan:
    path: /07_Applications_and_Interviews/
```

### Output Rules

- All outputs MUST align with `output-standards.md`
- All artifacts MUST include required disclosures (assumptions, gaps, warnings) when applicable
- Outputs MUST reflect context status (complete vs partial)
- Outputs MUST NOT modify canonical sources

---

## 4. Pipeline State Model

Allowed opportunity lifecycle states:

- `intake`
- `fit_risk_reviewed`
- `resume_targeted`
- `drafting`
- `submission_prepared`
- `submitted`
- `compliance_recommended`
- `follow_up_planned`
- `pass`
- `hold`
- `closed`

Rules:
- Every stage transition MUST update pipeline state
- State changes MUST be explicit and durable
- A pipeline run MUST be resumable from the last completed valid state

Additional Rules:

- State transitions MUST be validated before persistence
- Invalid state transitions MUST halt execution
- State MUST remain consistent with artifact availability

---

## 5. Pipeline Overview

```text
Opportunity Intake
    ↓
Fit / Risk Review
    ↓
Resume Targeting
    ↓
Cover Letter / Message Drafting
    ↓
Submission Preparation
    ↓
Submission Confirmation
    ↓
Compliance Logging Recommendation
    ↓
Follow-up Planning
```

---

## 6. Pipeline Stages

## Application Pipeline Stages

1. Opportunity Intake
2. Fit / Risk Review
3. Resume Targeting
4. Cover Letter / Message Drafting
5. Submission Preparation
6. Submission Confirmation
7. Compliance Logging Recommendation
8. Follow-up Planning

---

## 6.1 Stage 1 — Opportunity Intake

### Objective
Capture and normalize the opportunity as a structured record.

### Inputs
- job description or role summary
- company
- role title
- source/date metadata (if available)

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

Rules:
- Intake MUST NOT introduce inferred or fabricated data
- All missing fields MUST be marked as `MISSING`

### Sources
- `/06_Job_Opportunities/`
- `/09_Research_and_Market_Intelligence/` (optional)

### Actions
- store the job description or role summary
- capture employer, role title, source, and date
- attach known company, compensation, or research context
- classify the opportunity as:
  - new
  - active
  - revisited

### Output
```yaml
opportunity_record:
  id:
  company:
  role:
  status: intake
  source:
  created_date:
  linked_context:
```

### Save To
- `/06_Job_Opportunities/`

---

## 6.2 Stage 2 — Fit / Risk Review

### Objective
Evaluate fit, risks, and whether to proceed.

### Trigger
- new opportunity added
- updated opportunity requires reassessment
- opportunity resumed from `hold`

### Pack
- **Opportunity Analysis Pack**

### Inputs
- `opportunity_record`
- current career goals and constraints
- relevant canonical evidence
- optional market/company context

### Sources
- `/06_Job_Opportunities/`
- `/09_Research_and_Market_Intelligence/`
- `/04_Career_Goals_and_Strategy/`
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/05_Personal_Profile/`

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

Rules:
- All evaluations MUST be grounded in context or explicitly labeled assumptions
- Context gaps MUST be surfaced when impacting decision quality

### Output
```yaml
fit_risk_review:
  recommendation: Pursue | Consider | Pass
  findings:
  gaps:
  risks:
  rationale:
```

### Save To
- `/06_Job_Opportunities/`

### State Transitions
- `intake` → `fit_risk_reviewed`
- `fit_risk_reviewed` → `pass` (stop)
- `fit_risk_reviewed` → `hold` (pause)
- `fit_risk_reviewed` → continue to Stage 3 when recommendation = `Pursue`

---

## 6.3 Stage 3 — Resume Targeting

### Objective
Generate a role-aligned resume based on canonical career evidence plus opportunity context.

### Trigger
- Stage 2 recommendation = `Pursue`

### Pack
- **Resume Pack**

### Inputs
- `opportunity_record`
- `fit_risk_review`
- canonical experience and skills
- optional existing resume variant

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

- All claims MUST be traceable to canonical sources or labeled assumptions

### Output
```yaml
tailored_resume:
  artifact_path:
  role_alignment_notes:
```

### Save To
- `/01_Resume_and_Profiles/`
- optionally linked from `/07_Applications_and_Interviews/`

### State Transition
- `fit_risk_reviewed` → `resume_targeted`

---

## 6.4 Stage 4 — Cover Letter / Message Drafting

### Objective
Create role-specific written messaging that matches the targeted resume.

### Pack
- **Application Pack**

### Inputs
- `opportunity_record`
- `fit_risk_review`
- `tailored_resume`
- optional cover letter baseline
- relevant canonical experience

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

- No unsupported claims may be introduced
- All personalization MUST be grounded in context signals

### Possible Artifacts
- cover letter
- outreach/supporting message
- short-form application responses
- custom positioning notes

### Output
```yaml
messaging_draft_package:
  cover_letter:
  message:
  short_form_responses:
  notes:
```

### Save To
- `/01_Resume_and_Profiles/` (cover letter / messages)
- `/07_Applications_and_Interviews/` (draft references)

### State Transition
- `resume_targeted` → `drafting`

---

## 6.5 Stage 5 — Submission Preparation

### Objective
Assemble and validate a submission-ready package, without claiming submission is complete.

### Inputs
- `opportunity_record`
- `fit_risk_review`
- `tailored_resume`
- `messaging_draft_package`

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

- All required artifacts MUST exist and be valid
- No inferred data may be introduced

### Actions
- validate required fields and attachments
- link generated artifacts
- generate final submission checklist
- prepare destination/channel details

### Output
```yaml
submission_preparation_record:
  opportunity_id:
  linked_artifacts:
  checklist:
  destination:
  ready_for_submission: true
```

### Save To
- `/07_Applications_and_Interviews/`

### State Transition
- `drafting` → `submission_prepared`

### Tracker Sync (Required)
- Automatically create or update the matching row in `07_Applications_and_Interviews/Applications/application-tracker.md`
- Set `Status` to `Identified` or `Applied` based on available submission evidence
- Update `Last Action` and `Next Action` from submission preparation outputs
- Link the current application detail file in `Resume Version` (or equivalent artifact column)

---

## 6.6 Stage 6 — Submission Confirmation

### Objective
Confirm submission occurred and record durable proof.

### Inputs
- `opportunity_record`
- `submission_preparation_record`
- submission evidence (confirmation screen, email, or tracking id)

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

- Confirmation evidence MUST be present and verifiable

### Actions
- record submission date/time
- capture confirmation evidence
- set application status to submitted
- store initial follow-up anchor
- automatically update `07_Applications_and_Interviews/Applications/application-tracker.md` for the same opportunity

### Output
```yaml
application_record:
  opportunity_id:
  current_status: submitted
  submission_date:
  confirmation_evidence:
  initial_follow_up_anchor:
```

### Save To
- `/07_Applications_and_Interviews/`

### State Transition
- `submission_prepared` → `submitted`

### Tracker Sync (Required)
- Upsert tracker row keyed by opportunity/application ID
- Set `Status` to `Applied` (or the active interview-stage status if already advanced)
- Append submission confirmation details to `Last Action`
- Recompute `Next Action` with follow-up date anchor

---

## 6.7 Stage 7 — Compliance Logging Recommendation

### Objective
Recommend compliance logging only after submission is confirmed.

### Compliance Hook
After Stage 6 only, recommend:

> This appears to be a qualifying job-search activity. Consider running `/log-activity` to capture it.

Do not recommend compliance logging before submission is confirmed.

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

### State Transition
- `submitted` → `compliance_recommended`

---

## 6.8 Stage 8 — Follow-up Planning

### Objective
Create next-step follow-up actions after submission is confirmed.

### Inputs
- `opportunity_record`
- `application_record`
- communication channel details
- timeline constraints

### Validation
- all required inputs must be present
- inputs must resolve to valid sources
- pipeline must halt if validation fails

- Follow-up plan MUST be grounded in actual submission context
- No unsupported assumptions may be introduced

### Output
```yaml
follow_up_plan:
  first_follow_up_date:
  follow_up_channel:
  cadence:
  notes:
```

### Save To
- `/07_Applications_and_Interviews/`

### State Transition
- `compliance_recommended` → `follow_up_planned`

### Tracker Sync (Required)
- Automatically update `Next Action` and `Last Action` to reflect follow-up plan output
- If state transitions to `pass`, `closed`, `withdrawn`, or `rejected`, move entry to the tracker archive section according to tracker policy

---

## 7. Control Logic

## 7.1 Standard Flow

```text
IF state == intake:
    run Stage 2 (Fit / Risk Review)

IF state == fit_risk_reviewed AND recommendation == Pursue:
    run Stage 3 (Resume Targeting)

IF state == resume_targeted:
    run Stage 4 (Cover Letter / Message Drafting)

IF state == drafting:
    run Stage 5 (Submission Preparation)

IF state == submission_prepared:
    run Stage 6 (Submission Confirmation)

IF state == submitted:
    run Stage 7 (Compliance Logging Recommendation)

IF state == compliance_recommended:
    run Stage 8 (Follow-up Planning)
```

---

## 7.2 Hold Logic

```text
IF recommendation == Consider:
    set state = hold
    collect missing information
    resume from Fit / Risk Review when new inputs exist
```

---

## 7.3 Stop Logic

```text
IF recommendation == Pass:
    set state = pass
    stop pipeline
    retain evaluation record
```

---

## 7.4 Resume Logic

```text
IF pipeline interrupted:
    resume from last completed valid stage

IF required stage output missing or invalid:
    do not advance
```

---

## 8. Routing Rules

### Canonical Truth
Use as source-of-truth:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`

### Contextual Inputs
Use for opportunity-specific decisions:
- `/06_Job_Opportunities/`
- `/09_Research_and_Market_Intelligence/`
- `/07_Applications_and_Interviews/`

### Presentation Artifacts
Use only as reference or output destination:
- `/01_Resume_and_Profiles/`

Rules:
- presentation artifacts never override canonical truth
- opportunity-specific artifacts remain execution-scoped

---

## 9. Stage Validation Rules

A stage may complete only if:
- all required inputs are present and valid
- all referenced sources resolve correctly
- pack execution completes without error
- output structure matches declared schema
- output is written to the correct destination
- state transition is explicitly recorded
- the corresponding tracker sync succeeds for stages that change application state

Failure conditions:
- missing required input → halt
- invalid output schema → halt
- unresolved source reference → halt
- pack execution failure → halt
- tracker sync failure → halt

The pipeline MUST NOT advance under any failure condition.

- All assumptions MUST be explicitly labeled
- Context gaps MUST be surfaced when present
- Outputs MUST align with context status (complete vs partial)

---

## 10. Failure Handling

### Missing Opportunity Data
- mark analysis incomplete
- request or collect missing inputs
- do not force recommendation

### Weak Evidence for Resume Positioning
- fall back to strongest canonical evidence
- identify gaps explicitly
- avoid fabrication

### Invalid Pack Output
- stop pipeline at failing stage
- preserve prior valid state
- record remediation needed

### Pipeline Interruption
- preserve current stage status
- store partial but valid outputs
- allow resume from last completed stage

---

## 11. Minimal Invocation

```yaml
request:
  opportunity:
    job_description: <job description or role summary>
    company: <string>
    role: <string>
```

---

## 12. Full Invocation

```yaml
request:
  opportunity:
    job_description: <job description>
    company: <string>
    role: <string>
  compensation_details: <optional>
  company_research: <optional>
  existing_resume_variant: <optional>
  constraints:
    must_align_with_leadership_trajectory: true
    prioritize_long_term_upside: true
```

---

## 13. Validation Hooks

- All stage outputs are valid runtime objects
- All artifacts are traceable to context or labeled assumptions
- No unsupported or fabricated content is present
- State transitions are valid and consistent
- All required disclosures are present
- Pipeline execution is fully deterministic

## 14. Summary

The Application Pipeline defines the standard flow for:

- evaluating opportunities
- determining fit/risk before writing assets
- generating targeted submission materials
- confirming submission before compliance recommendation
- maintaining durable records and follow-up plans

It ensures deterministic, grounded, and fully traceable application workflows aligned with CareerOS runtime constraints.

---

## 15. Integration Contract

This pipeline integrates with runtime components as follows:

- prompt-assembler.md
  - constructs stage-specific prompts
  - injects required context per stage

- context-loader.md
  - resolves canonical and contextual inputs
  - enforces source-of-truth hierarchy

- source-routing.md
  - constrains allowed sources per stage
  - prevents cross-layer leakage

- execution-flow.md
  - governs runtime execution behavior
  - enforces sequencing and halt conditions

This pipeline defines *what executes*.
Runtime contracts define *how execution occurs*.