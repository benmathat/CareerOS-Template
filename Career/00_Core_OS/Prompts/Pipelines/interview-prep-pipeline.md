---
Last Update: 2026-04-24
Previous Update: 2026-04-22
---

# Interview Prep Pipeline

## 1. Purpose

Define a **structured, repeatable workflow** for converting role context and canonical experience into:
- interview-ready stories
- concise, high-signal answers
- delivery-ready preparation
- tracked interview activity

This pipeline ensures interview preparation is:
- grounded in canonical truth
- tailored to role-specific competencies
- repeatable across opportunities
- integrated with compliance requirements

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only workflow-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

---

## 2. Scope

Use this pipeline when:
- preparing for a scheduled interview
- anticipating likely interview scenarios
- refining delivery of existing stories
- converting experience into interview-ready answers

This pipeline governs **preparation and tracking**, not opportunity evaluation.

---

## 3. Inputs

```yaml
inputs:
  opportunity_context:
    path: /06_Job_Opportunities/
    required_fields:
      - role
      - company
  interview_context:
    type: screen | behavioral | panel | technical | other
    scheduled: <boolean>
  canonical_sources:
    stories:
      path: /02_Work_Experience/Stories/
  optional_context:
    - /09_Research_and_Market_Intelligence/
    - /07_Applications_and_Interviews/
```

```yaml
validation:
  required_fields:
    - inputs.opportunity_context
    - inputs.interview_context.type
  failure_behavior: halt
```

## 4. Outputs

```yaml
outputs:
  competency_map:
    path: /07_Applications_and_Interviews/Interview_Prep/
  story_set:
    path: /07_Applications_and_Interviews/Interview_Prep/
  answer_drafts:
    path: /07_Applications_and_Interviews/Interview_Prep/
  delivery_scripts:
    path: /07_Applications_and_Interviews/Interview_Prep/
  prep_record:
    path: /07_Applications_and_Interviews/Interview_Prep/
  interview_event_record:
    path: /07_Applications_and_Interviews/
```

This pipeline produces:
- competency map
- selected story set
- structured answers
- refined delivery scripts
- interview prep records

---

## 5. State Model

- `role_context_captured`
- `competencies_mapped`
- `stories_selected`
- `answers_drafted`
- `answers_refined`
- `prep_record_updated`
- `interview_event_logged`

---

## 6. Stages

```text
Role Context Intake
    ↓
Competency Mapping
    ↓
Story Selection
    ↓
Answer Drafting
    ↓
Refinement and Timing
    ↓
Prep Record Update
```

### 6.1 Stage 1 — Role Context Intake

### Objective
Capture the role, company, and interview format.

### Sources
- `/06_Job_Opportunities/`
- `/09_Research_and_Market_Intelligence/`

### Output
- structured role and interview context

---

### 6.2 Stage 2 — Competency Mapping

### Objective
Identify likely competencies and question types.

### Inputs
- job description
- company signals
- role expectations

### Output
- prioritized competency list

---

### 6.3 Stage 3 — Story Selection

### Objective
Select canonical stories aligned to competencies.

### Sources
- `/02_Work_Experience/Stories/`

### Rules
- canonical stories remain unchanged
- select strongest evidence-based examples
- All selected stories MUST be traceable to canonical sources
- Any gaps in story coverage MUST be explicitly identified

### Output
- mapped story set

---

### 6.4 Stage 4 — Answer Drafting

### Objective
Create tactical interview responses.

### Actions
- transform canonical stories into structured answers
- enforce format: Situation → Action → Result
- align explicitly to mapped competencies
- remove non-relevant detail
- All claims MUST be grounded in canonical sources

### Output Location
- `/07_Applications_and_Interviews/Interview_Prep/`

### Output
- structured answer drafts

---

### 6.5 Stage 5 — Refinement and Timing

### Objective
Optimize answers for delivery.

### Actions
- compress answers to 60–120 seconds
- optimize clarity, impact, and sequencing
- ensure strong opening and clear outcome
- remove redundancy
- Refinement MUST NOT introduce new facts
- All changes MUST be traceable to original drafts

### Output
- delivery-ready responses

---

### 6.6 Stage 6 — Prep Record Update

### Objective
Maintain a record of preparation and readiness.

### Actions
- update prep notes
- track readiness by competency
- identify gaps and additional drills
- No inferred readiness signals

### Output Location
- `/07_Applications_and_Interviews/Interview_Prep/`

---

### 6.7 Stage 7 — Interview Event Tracking

### Objective
Capture real-world interview activity.

### Triggers
- interview scheduled
- interview completed

### Actions
- update interview status in application records
- record interview details (date, format, participants, outcome if known)
- All event data MUST be verifiable
- No inferred interview outcomes

### Compliance Hooks

#### After Interview Scheduled

→ Recommend: `/log-activity`

Purpose:
- document interview scheduling as a work search activity
- capture employer, role, and method (email, phone, platform)
- optionally link scheduling confirmation

#### After Interview Completed

→ Recommend: `/log-activity`

Purpose:
- document interview completion as a work search activity
- capture interview type (phone, video, in-person)
- record outcome or status
- link notes or follow-up actions if applicable

---

## 7. Stage Transition Rules

- Stage 1 -> Stage 2 when role context is captured
- Stage 2 -> Stage 3 when competencies are defined
- Stage 3 -> Stage 4 when stories are selected
- Stage 4 -> Stage 5 when answer drafts are created
- Stage 5 -> Stage 6 when refinement is complete
- Stage 6 -> Stage 7 when interview scheduling or completion events occur

---

## 8. Artifact Routing

Allowed sources by stage:

- Stage 1–3:
  - /06_Job_Opportunities/
  - /02_Work_Experience/
  - optional: /09_

- Stage 4–6:
  - /02_Work_Experience/
  - /07_Applications_and_Interviews/

- Stage 7:
  - /07_Applications_and_Interviews/

Rules:
- canonical stories are read-only
- all derived artifacts must be written to tactical directories
- no mutation of canonical sources

Additional Rules:

- Canonical sources are authoritative
- Contextual sources MUST NOT override canonical truth
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 9. Workflow Validation Hooks

- Competency maps are role-grounded and prioritized
- Selected stories are canonical and evidence-based
- Answer drafts remain mapped to competencies
- Refinement improves delivery without adding new facts
- Interview events are recorded with verifiable details

---

## 10. Control Logic

```text
IF opportunity_context provided:
    run Stage 1 (Role Context Intake)

IF context_captured:
    run Stage 2 (Competency Mapping)

IF competencies_defined:
    run Stage 3 (Story Selection)

IF stories_selected:
    run Stage 4 (Answer Drafting)

IF drafts_created:
    run Stage 5 (Refinement and Timing)

IF refinement_complete:
    run Stage 6 (Prep Record Update)

IF interview scheduled:
    run Stage 7 (Interview Event Tracking - scheduled)

IF interview completed:
    run Stage 7 (Interview Event Tracking - completed)
```

---

## 11. Cadence Model

### Pre-Interview
- complete full pipeline

### Day-of
- rehearse key stories
- review competency mapping

### Post-Interview
- update prep records
- capture outcomes

---

## 12. Integration Points

### Runtime Integration Contract

- prompt-assembler.md
  - constructs prompts for answer drafting and refinement

- context-loader.md
  - loads canonical stories and opportunity context

- source-routing.md
  - enforces source boundaries and write locations

- execution-flow.md
  - governs sequencing and failure handling

This pipeline defines workflow intent and state progression.
Runtime defines execution mechanics.

### Application Pipeline
- triggered after application submission

### Compliance Pipeline
- interview events → recommend `/log-activity`

---

## 13. Summary

The Interview Prep Pipeline ensures:

- structured preparation from canonical truth
- role-aligned answer development
- delivery-ready responses
- integration with compliance tracking

It ensures deterministic, grounded, and fully traceable interview preparation workflows aligned with CareerOS workflow constraints.