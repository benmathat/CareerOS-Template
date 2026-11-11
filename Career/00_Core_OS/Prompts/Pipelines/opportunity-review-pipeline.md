---
Last Update: 2026-04-22
Previous Update: 2026-04-22
---

# Opportunity Review Pipeline (Portfolio Pipeline Contract)

## 1. Purpose

Define the **portfolio-level orchestration process** for reviewing, reprioritizing, and managing all active opportunities in CareerOS.

This pipeline ensures:
- alignment with career strategy
- disciplined prioritization
- controlled workload
- continuous forward progress

It is the **portfolio management layer** of CareerOS and operates across multiple opportunities simultaneously.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only workflow-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It MUST:
- evaluate opportunities consistently
- enforce prioritization constraints
- assign actionable next steps
- update durable system state
- remain resumable and repeatable

It MUST NOT:
- duplicate logic from execution packs
- treat presentation artifacts as canonical truth
- allow undefined or unprioritized active opportunities

---

## 2. Scope

Use this pipeline when:

- reviewing all active opportunities (daily or weekly)
- reprioritizing effort allocation
- reassessing `hold` or `consider` opportunities
- deciding where to invest time next

This pipeline governs **portfolio state**, not individual artifact generation.

---

## 3. Pipeline Interface

### 3.1 Required Inputs

```yaml
request:
  opportunity_set:
    source: /06_Job_Opportunities/
  career_context:
    goals_and_constraints: /04_Career_Goals_and_Strategy/
```

### 3.2 Optional Inputs

```yaml
request:
  application_state: /07_Applications_and_Interviews/
  market_context: /09_Research_and_Market_Intelligence/
  personal_constraints: /05_Personal_Profile/
  constraints:
    max_active_opportunities: <integer>
    prioritization_focus: <string>
```

### 3.3 Outputs

```yaml
portfolio_state:
  prioritized_opportunities:
  updated_statuses:
  next_actions:
  closed_or_deferred:
```

### Output Rules

- All outputs MUST align with `output-standards.md`
- All outputs MUST include required disclosures (assumptions, gaps, warnings) when applicable
- Outputs MUST reflect context status (complete vs partial)
- Outputs MUST NOT modify canonical sources

---

## 4. State Model

Each opportunity MUST exist in one of the following states:

- `intake`
- `analyzing`
- `hold`
- `pursue`
- `applying`
- `submitted`
- `interviewing`
- `pass`
- `closed`

Rules:
- `closed` and `pass` are terminal states
- all non-terminal states MUST be reviewed during pipeline execution
- every `pursue` or `applying` opportunity MUST have a next action

---

## 5. Pipeline Overview

```text
Load Opportunity Set
    ↓
Evaluate Opportunities
    ↓
Reclassify Status
    ↓
Prioritize Portfolio
    ↓
Assign Next Actions
    ↓
Enforce Constraints
    ↓
Update Records
```

---

## 6. Pipeline Stages

## 6.1 Stage 1 — Load Opportunity Set

### Objective
Load all relevant opportunities into the working set.

### Sources
- `/06_Job_Opportunities/`

### Filters
- EXCLUDE: `closed`, `pass`
- INCLUDE:
  - intake
  - analyzing
  - hold
  - pursue
  - applying
  - submitted
  - interviewing

### Output
```yaml
opportunity_set:
  - opportunity_id
  - current_state
```

- Source resolution MUST be verifiable
- Missing opportunity records MUST be surfaced as gaps

---

## 6.2 Stage 2 — Evaluate Opportunities

### Objective
Perform a lightweight re-evaluation of each opportunity.

### Method
Evaluate each opportunity on:
- alignment to current goals
- recency and activity status
- probability of progress
- constraint alignment

Rules:
- All evaluations MUST be grounded in context or explicitly labeled assumptions
- Context gaps impacting evaluation MUST be surfaced

### Escalation Condition
Re-run **Opportunity Analysis Pack** ONLY if:
- significant new information exists
- prior analysis is incomplete or outdated

### Output
```yaml
evaluation_snapshot:
  - opportunity_id
  - alignment_score
  - activity_signal
  - risk_flags
```

---

## 6.3 Stage 3 — Reclassify Status

### Objective
Update lifecycle state based on evaluation.

### Rules

- stale or inactive → `closed` or `hold`
- strong alignment → `pursue`
- insufficient information → `hold`
- active engagement → retain current state
- State transitions MUST be explicitly justified
- No inferred transitions without supporting signals

### Output
```yaml
status_updates:
  - opportunity_id
  - new_state
  - rationale
```

---

## 6.4 Stage 4 — Prioritize Portfolio

### Objective
Rank opportunities by strategic importance.

### Factors
- career alignment
- probability of success
- timeline urgency
- compensation potential
- strategic value

Rules:
- Ranking MUST be based on explicit criteria
- Assumptions in scoring MUST be labeled

### Output
```yaml
prioritized_opportunities:
  - opportunity_id
  - priority_rank
  - priority_score
```

---

## 6.5 Stage 5 — Assign Next Actions

### Objective
Define the immediate next step for each active opportunity.

### Action Types
- run Application Pipeline
- update resume via Resume Pack
- initiate or continue networking
- prepare interview materials via Interview Pack
- gather missing information

### Rules
- every `pursue` or `applying` opportunity MUST have exactly one next action
- `hold` opportunities MAY have a data-gathering action
- All actions MUST be grounded in opportunity state and context
- No unsupported or arbitrary actions may be assigned

### Output
```yaml
next_actions:
  - opportunity_id
  - action_type
  - action_detail
```

---

## 6.6 Stage 6 — Enforce Constraints

### Objective
Ensure portfolio size and focus constraints are respected.

### Rules

IF `max_active_opportunities` is defined:
- keep only top N opportunities in active states (`pursue`, `applying`)
- move excess opportunities to `hold`

IF prioritization focus is defined:
- re-rank to favor matching opportunities

- Constraint application MUST be deterministic
- Adjustments MUST be traceable and justified

### Output
```yaml
constraint_adjustments:
  - opportunity_id
  - adjustment_action
```

---

## 6.7 Stage 7 — Update Records

### Objective
Persist all changes to CareerOS.

### Actions
- update opportunity state
- record priority rank
- record next action
- add review timestamp

### Save To
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/` (if active)

- All updates MUST be traceable to pipeline outputs
- No partial or invalid records may be persisted

### Output
```yaml
portfolio_update:
  timestamp:
  updated_records:
```

---

## 7. Control Logic

### Standard Flow

```text
FOR each opportunity IN opportunity_set:
    evaluate
    update status

SORT opportunities by priority

ASSIGN next actions

APPLY constraints

UPDATE records
```

---

### Escalation Logic

```text
IF high priority AND no progress:
    escalate action urgency or change strategy
```

---

### Deactivation Logic

```text
IF opportunity is stale OR misaligned:
    move to closed OR hold
```

---

### Resume Logic

```text
IF pipeline interrupted:
    resume from last completed stage
```

---

## 8. Review Cadence

### Daily (Light Pass)
- validate top priorities
- confirm next actions

### Weekly (Full Pass)
- execute full pipeline
- reprioritize entire portfolio

### Event-Driven
- new opportunity added
- interview scheduled
- rejection received
- major market or personal change

---

## 9. Routing Rules

### Canonical Truth
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`

### Opportunity Data
- `/06_Job_Opportunities/`

### Execution State
- `/07_Applications_and_Interviews/`

### Market Context
- `/09_Research_and_Market_Intelligence/`

Rules:
- canonical sources define priorities and constraints
- opportunity data defines state
- execution state informs progress and actions

Additional Rules:

- Canonical sources are authoritative
- Contextual sources MUST NOT override canonical truth
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 10. Failure Handling

### Too Many Opportunities
- reduce to top priority set
- move excess to `hold`

### Conflicting Priorities
- defer to career alignment and constraints

### Missing Data
- assign "gather information" action

### No Progress on High Priority
- escalate or reconsider opportunity

---

## 11. Minimal Invocation

```yaml
request:
  run: opportunity_review_pipeline
```

---

## 12. Full Invocation

```yaml
request:
  run: opportunity_review_pipeline
  constraints:
    max_active_opportunities: 5
    prioritization_focus: leadership_roles
```

---

## 13. Validation Hooks

- All stage outputs are valid runtime objects
- All decisions are traceable to context or labeled assumptions
- No unsupported or fabricated conclusions are present
- State transitions are valid and consistent
- Portfolio prioritization is deterministic and justified
- All required disclosures are present

---

## 14. Summary

The Opportunity Review Pipeline:

- manages the full opportunity portfolio
- enforces prioritization discipline
- ensures every active opportunity has a defined next action
- maintains a clean and focused system state

It ensures deterministic, grounded, and fully traceable portfolio management aligned with CareerOS runtime constraints.
