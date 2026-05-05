---
Last Update: 2026-04-22
Previous Update:
---

# Application Pack (Execution Pack Contract)

## 1. Purpose

Provide a **pre-configured execution pack** for running end-to-end application workflows for a single opportunity.

This pack orchestrates **multi-artifact execution** across the CareerOS runtime:
- Resume generation
- Cover letter generation (optional)
- Application notes
- Next-step tracking

It defines constraints, orchestration structure, and expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It MUST NOT:
- Perform routing logic directly
- Perform context loading
- Perform prompt assembly
- Execute tasks directly

---

## 2. Pack Interface

### 2.1 Inputs (Required)

```yaml
request:
  opportunity:
    job_description: <text | file reference>
    company: <string>
    role: <string>
```

### 2.2 Inputs (Optional)

```yaml
request:
  base_resume: <file reference>
  cover_letter_baseline: <file reference>
  recruiter_notes: <text | file reference>
  constraints:
    page_limit: <1 | 2>
    include_cover_letter: <true | false>
```

### 2.3 Outputs

```yaml
artifacts:
  - resume:
      type: Document
      destination: /01_Resume_and_Profiles/
  - cover_letter:
      type: Document
      destination: /01_Resume_and_Profiles/
  - application_notes:
      type: Document
      destination: /07_Applications_and_Interviews/
  - next_steps:
      type: Checklist
      destination: /07_Applications_and_Interviews/
```

### Output Rules

- Output types MUST align with `output-standards.md`
- All artifacts MUST include required disclosures (assumptions, gaps, warnings) when applicable
- Artifacts MUST remain scoped to the opportunity and MUST NOT modify canonical sources

---

## 3. Execution Profile

### Mode Sequence (Deterministic)

This pack is **multi-phase** and MUST NOT rely on a single mode.

Execution order:

1. `analyze` → understand opportunity + extract requirements
2. `build` → generate resume + cover letter
3. `execute` → produce notes + checklist
4. `refine` (optional) → improve outputs if needed

Rules:
- Modes MUST be executed sequentially, not blended
- Each phase MUST use its own `task` object

---

## 4. Routing Inputs (for source-routing.md)

Each phase MUST provide normalized routing inputs:

```yaml
request:
  pipeline: application
  intent: opportunity-specific application workflow
```

### Phase Overrides

#### Analyze Phase

```yaml
mode_selection:
  primary_mode: analyze
task:
  artifact_state: none
  output_type: Analysis
```

#### Build Phase

```yaml
mode_selection:
  primary_mode: build
task:
  artifact_state: new | existing (if base_resume provided)
  output_type: Document
```

#### Execute Phase

```yaml
mode_selection:
  primary_mode: execute
task:
  artifact_state: none
  output_type: Checklist | Document
```

Rules:

- Routing inputs MUST be minimal and normalized
- Each phase MUST NOT override runtime routing decisions
- Required sources MUST be sufficient for each phase independently

---

## 5. Source Expectations

Routing should result in:

- Canonical grounding → `02_–05_`
- Opportunity context → `06_`
- Execution artifacts → `07_`
- Market context → `09_`

Rules:
- Canonical sources remain authoritative
- Execution sources provide context only
- Presentation (`01_`) is baseline only, never truth

Additional Rules:

- Conflicts between canonical and contextual sources MUST be surfaced
- Contextual sources MUST NOT override canonical truth
- Missing canonical grounding MUST be surfaced as a gap

---

## 6. task Definitions (Per Phase)

task Rules:

- Each phase MUST define a complete `task` object
- Tasks MUST NOT contain execution logic
- Tasks MUST be independently valid and executable

### 6.1 Analyze task

```yaml
task:
  objective: Evaluate opportunity and extract role priorities and positioning requirements.
  scope:
    in_scope:
      - Role requirements
      - Key success signals
    out_of_scope:
      - Resume generation
  inputs:
    required:
      - Job description
    optional:
      - Market research
  constraints:
    hard:
      - No artifact generation
  success_criteria:
    - Clear role priorities identified
  output_type: Analysis
```

---

### 6.2 Resume Build task

Reuse Resume Pack `task` structure (aligned with `resume-pack.md`).

---

### 6.3 Cover Letter task (Optional)

```yaml
task:
  objective: Generate a role-specific cover letter aligned to the opportunity.
  scope:
    in_scope:
      - Role alignment
      - Motivation narrative
    out_of_scope:
      - Resume duplication
  inputs:
    required:
      - Job description
      - Resume
    optional:
      - Baseline letter
  constraints:
    hard:
      - 1 page maximum
  success_criteria:
    - Clear alignment to role
  output_type: Document
```

---

### 6.4 Application Notes task

```yaml
task:
  objective: Generate structured application notes for tracking and preparation.
  scope:
    in_scope:
      - Key signals
      - Talking points
    out_of_scope:
      - Resume content
  inputs:
    required:
      - Job description
  constraints:
    hard:
        - Concise format
  success_criteria:
    - Useful for interview prep
  output_type: Document
```

---

### 6.5 Next Steps task

```yaml
task:
  objective: Generate actionable next steps for the application process.
  scope:
    in_scope:
      - Submission steps
      - Follow-up actions
    out_of_scope:
      - Analysis content
  inputs:
    required:
      - Opportunity context
  constraints:
    hard:
      - Checklist format
  success_criteria:
    - Immediately actionable
  output_type: Checklist
```

---

## 8. Output Routing

- Resume / Cover Letter → `/01_Resume_and_Profiles/`
- Application Notes → `/07_Applications_and_Interviews/`
- Next Steps → `/07_Applications_and_Interviews/`

Rules:
- No canonical domains are modified
- Outputs remain scoped to the opportunity

Additional Rules:

- No artifacts may be written if validation fails
- Outputs MUST be traceable to the originating opportunity

---

## 9. Validation Gates (Pack-Level)

Before finalization:

- [ ] Resume meets constraints and role alignment
- [ ] Cover letter (if present) is distinct from resume
- [ ] Notes are structured and usable
- [ ] Checklist is actionable
- [ ] No cross-artifact inconsistency

- [ ] All assumptions are explicitly labeled
- [ ] Context gaps are surfaced where applicable
- [ ] No unsupported claims exist across artifacts
- [ ] All outputs align with context status (complete vs partial)

---

## 11. Example Invocation (Normalized)

```yaml
request:
  opportunity:
    company: Scouting America
    role: District Executive
    job_description: <file>
  base_resume: <optional file>

runtime:
  workflow_type: application
```

---

## 12. Summary

The Application Pack:

- Orchestrates multi-step, multi-artifact execution
- Enforces deterministic sequencing across modes
- Produces a complete application package
- Integrates directly with CareerOS runtime

It ensures deterministic, multi-phase execution aligned with CareerOS runtime constraints while preserving grounding, traceability, and output integrity.
