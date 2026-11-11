---
Last Update: 2026-04-24
Previous Update: 2026-04-22
---

# Networking Pipeline

## 1. Purpose

Define a **structured, repeatable workflow** for converting networking intent into:
- targeted outreach
- tracked interactions
- follow-up execution
- relationship development

This pipeline ensures networking is:
- intentional (not ad hoc)
- traceable
- integrated with opportunities and applications

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only workflow-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

---

## 2. Scope

Use this pipeline when:
- identifying people or organizations to connect with
- initiating outreach
- following up on prior communication
- tracking networking outcomes

This pipeline governs **execution and tracking**, not relationship strategy design.

---

## 3. Pipeline Contract

### 3.1 Inputs

```yaml
inputs:
  objective:
    description: <text>
  target_segment:
    type: companies | roles | individuals
  optional_context:
    opportunity_context:
      path: /06_Job_Opportunities/
    existing_contacts:
      path: /08_Networking_and_References/Contacts/
    prior_interactions:
      path: /08_Networking_and_References/
```

```yaml
validation:
  required_fields:
    - inputs.objective
    - inputs.target_segment
  failure_behavior: halt
```

### 3.2 Outputs

```yaml
outputs:
  target_list:
    path: /08_Networking_and_References/
  prioritized_contacts:
    path: /08_Networking_and_References/
  outreach_drafts:
    path: /08_Networking_and_References/
  interaction_records:
    path: /08_Networking_and_References/Contacts/
  follow_up_schedule:
    path: /08_Networking_and_References/
  relationship_updates:
    path: /08_Networking_and_References/Contacts/
```

### Output Rules

- All outputs MUST align with `output-standards.md`
- All artifacts MUST include required disclosures (assumptions, gaps, warnings) when applicable
- Outputs MUST reflect context status (complete vs partial)
- Outputs MUST NOT modify canonical sources

---

## 4. Outputs

This pipeline produces:
- prioritized contact list
- outreach messages
- logged contact interactions
- follow-up schedule
- updated relationship records

---

## 5. Pipeline Overview

```text
Target Selection
    ↓
Contact Prioritization
    ↓
Outreach Drafting
    ↓
Send Outreach
    ↓
Log Interaction
    ↓
Follow-Up Scheduling
    ↓
Relationship Update
```

---

## 6. Pipeline Stages

## 6.1 Stage 1 — Target Selection

### Objective
Identify companies, roles, or individuals aligned with current goals.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- Target selection MUST be grounded in defined objective or context
- Missing targeting criteria MUST be surfaced as gaps

### Sources
- `/04_Career_Goals_and_Strategy/`
- `/06_Job_Opportunities/`

### Output
- list of target organizations or individuals

---

## 6.2 Stage 2 — Contact Prioritization

### Objective
Rank contacts by relevance, access, and likelihood of response.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- Prioritization MUST be justified by explicit criteria
- Assumptions in ranking MUST be labeled

### Criteria
- role relevance
- network proximity (warm vs cold)
- timing and opportunity alignment

### Output
- prioritized outreach list

---

## 6.3 Stage 3 — Outreach Drafting

### Objective
Create personalized, context-aware outreach messages.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- All personalization MUST be traceable to context signals
- No unsupported claims or fabricated familiarity

### Sources
- `/08_Networking_and_References/`
- `/06_Job_Opportunities/` (if applicable)

### Output
- outreach drafts

---

## 6.4 Stage 4 — Send Outreach

### Objective
Execute outreach in the real world.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure
- Outreach must be verified as sent or explicitly marked failed

### Actions
- send message via appropriate channel (LinkedIn, email, etc.)

### Output
- outbound communication sent

### Compliance Hook
After sending outreach:

→ Recommend: /log-activity

Purpose:
- capture the outbound communication as a work search activity
- record method, contact, and outcome
- optionally link message evidence (email, LinkedIn screenshot)

---

## 6.5 Stage 5 — Log Interaction

### Objective
Record outreach and responses in CareerOS.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure

### Actions
- update contact record in:
  `08_Networking_and_References/Contacts/`
- capture message, date, and status
- All logged data MUST be verifiable
- Missing data MUST be marked as `MISSING`

### Compliance Note
If this stage reflects a real-world activity that has not yet been logged for compliance:

→ Recommend: /log-activity

---

## 6.6 Stage 6 — Follow-Up Scheduling

### Objective
Ensure consistent follow-up behavior.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure

### Actions
- define next follow-up date
- track pending responses
- Follow-up timing MUST be grounded in defined cadence or context
- Assumptions in timing MUST be labeled

### Output
- scheduled follow-up actions

---

## 6.7 Stage 7 — Relationship Update

### Objective
Maintain an up-to-date view of relationship status.

### Validation
- required inputs must be present
- inputs must resolve to valid sources
- pipeline halts on failure

### Actions
- update contact notes
- record outcomes (no response, engaged, referral, etc.)
- link to opportunities or applications if applicable
- All relationship status changes MUST be traceable to interaction data
- No inferred relationship progression

### Compliance Hook
After meaningful interaction (reply received, conversation, informational interview):

→ Recommend: `/log-activity`

Purpose:
- document interaction as a work search activity
- capture outcome and any next steps

---

## 7. Source Routing

Allowed sources by stage:

- Stage 1–2:
  - /04_Career_Goals_and_Strategy/
  - /06_Job_Opportunities/

- Stage 3–5:
  - /08_Networking_and_References/
  - optional: /06_

- Stage 6–7:
  - /08_Networking_and_References/

Rules:
- contact records are canonical for relationships
- all interactions must be written to contact records
- no mutation of unrelated directories

Additional Rules:

- Canonical contact records are authoritative
- Contextual sources MUST NOT override canonical truth
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 8. Control Logic

```text
IF objective defined:
    run Stage 1 (Target Selection)

IF targets_selected:
    run Stage 2 (Contact Prioritization)

FOR each prioritized_contact:
    run Stage 3 (Outreach Drafting)
    run Stage 4 (Send Outreach)
    run Stage 5 (Log Interaction)

IF interaction_logged:
    run Stage 6 (Follow-Up Scheduling)

IF response_received:
    run Stage 7 (Relationship Update)
```

---

## 9. Cadence Model

### Daily (Optional)
- send outreach
- log interactions

### Weekly (Recommended)
- review contact list
- follow up on pending outreach

---

## 10. Failure Handling

### Stage Failure Conditions
- missing required input → halt
- unresolved contact data → halt
- invalid outreach draft → halt
- failed send (unknown status) → halt

### Non-blocking Conditions
- no response → continue with follow-up schedule
- partial contact data → log with gaps

---

## 11. Integration Points

### Application Pipeline
- networking tied to a role → link to opportunity record

### Compliance Pipeline
- outreach and interactions → recommend `/log-activity`

---

## 11.1 Runtime Integration Contract

- prompt-assembler.md
  - constructs outreach and logging prompts

- context-loader.md
  - loads contact data and opportunity context

- source-routing.md
  - enforces directory constraints

- execution-flow.md
  - governs sequencing and iteration

This pipeline defines workflow intent.
Runtime defines execution mechanics.
---

## 12. Validation Hooks

- All stage outputs are valid runtime objects
- All outreach content is traceable to context signals
- No unsupported or fabricated claims are present
- Interaction records are complete and consistent
- Relationship updates are grounded in actual interactions
- Pipeline execution is deterministic and complete
- All required disclosures are present

## 13. Summary

The Networking Pipeline ensures:

- structured outreach execution
- consistent follow-up behavior
- durable relationship tracking
- integration with compliance requirements

It ensures deterministic, grounded, and fully traceable networking workflows aligned with CareerOS runtime constraints.
