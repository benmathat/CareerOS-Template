---
Last Update: 2026-04-22
Previous Update: 2026-04-22
---

# Resume Pack (Execution Pack Contract)

## 1. Purpose

Provide a **pre-configured execution pack** for generating and refining resumes using CareerOS.

This pack defines constraints, structure, and orchestration expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT:
- Perform mode selection directly
- Perform source routing
- Perform context loading
- Execute tasks directly

---

## 2. Pack Interface

### 2.1 Inputs (Required)

```yaml
request:
  target_role: <string>
  job_description: <text | file reference>
```

### 2.2 Inputs (Optional)

```yaml
request:
  base_resume: <file reference>
  story_inventory: <file reference>
  portfolio_artifacts: <file reference>
  constraints:
    page_limit: <1 | 2>
    emphasis: <string>
```

### 2.3 Outputs

```yaml
artifact:
  type: Document
  destination: /01_Resume_and_Profiles/
  naming:
    pattern: <company>_<role>_<YYYY-MM-DD>.md
```

---

## 3. Execution Profile

### Mode

- Primary: `build`
- Secondary (optional): `refine` (post-pass only)

### Workflow Pattern

**Canonical → Context → Output**

---

## 4. Routing Inputs (for source-routing.md)

The pack MUST provide normalized routing inputs:

```yaml
mode_selection:
  primary_mode: build
task:
  artifact_state: new | existing (if base_resume provided)
  output_type: Document
request:
  pipeline: resume
  intent: role-specific resume generation
```

Expected routing behavior:
- Canonical (`02_–05_`) as primary
- Execution (`06_`) for job context
- Presentation (`01_`) optional as baseline

Rules:

- Canonical sources are authoritative
- Contextual sources MUST NOT override canonical truth
- Missing canonical grounding MUST be surfaced as a gap
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. task (Strict Schema)

The pack MUST construct a valid `task` object:

```yaml
task:
  objective: Create a role-tailored resume aligned to the target role.
  scope:
    in_scope:
      - Resume content aligned to role priorities
      - Quantified achievements where available
    out_of_scope:
      - Cover letter generation
      - Portfolio site changes
  inputs:
    required:
      - Work experience (canonical)
      - Skills (canonical)
      - Job description (execution)
    optional:
      - Base resume
      - Story inventory
      - Portfolio artifacts
  constraints:
    hard:
      - Page limit: 1–2 pages (default 1 unless overridden)
    soft:
      - Prefer concise, high-signal bullets
      - Avoid generic phrasing
  success_criteria:
    - Aligns to top role priorities
    - Uses quantified impact where available
    - No filler content
  output_type: Document
```

task Rules:

- `task` MUST be complete and independently executable
- `task` MUST NOT contain execution logic
- All assumptions used to fill gaps MUST be explicitly labeled

---

## 6. Output Contract (Document)

The assembler MUST enforce Document structure:

Required sections:
- Title
- Sections
- Subsections

Pack-specific section schema:
- Header (Name + Contact)
- Summary
- Core Skills
- Professional Experience
- Education (if applicable)

Quality requirements:
- High signal density
- Role alignment
- Quantified achievements where available
- No fluff or repetition

Additional Rules:

- All claims MUST be grounded in context or explicitly labeled assumptions
- Metrics MUST be real or explicitly marked as gaps
- Output MUST align with `output-standards.md`
- Output MUST reflect context status (complete vs partial)

---

## 8. Refine Pass (Optional)

Trigger conditions:
- User request
- Validation improvements desired (clarity, concision)

Refine task (delta-focused):

```yaml
task:
  objective: Improve clarity, concision, and impact of the existing resume.
  scope:
    in_scope:
      - Bullet clarity
      - Redundancy removal
    out_of_scope:
      - Structural redesign
  inputs:
    required:
      - Generated resume
  constraints:
    hard:
      - Preserve content accuracy
    soft:
      - Increase signal density
  success_criteria:
    - Clearer bullets
    - Reduced redundancy
  output_type: Document
```

Rules:

- Refinement MUST NOT introduce new facts
- All improvements MUST be traceable to original content
- Assumptions MUST be explicitly labeled if introduced

---

## 9. Output Routing

Destination:
- `/01_Resume_and_Profiles/`

Versioning (recommended):
- `<company>_<role>_<YYYY-MM-DD>.md`

Rules:
- Do not overwrite canonical sources
- Treat resumes as presentation artifacts only

Additional Rules:

- Outputs MUST NOT modify canonical sources
- Outputs MUST be traceable to source context
- No artifacts may be written if validation fails

---

## 10. Validation Gates (Pack-Level)

Before finalization:
- [ ] Meets page constraint
- [ ] Matches Document structure
- [ ] Claims traceable to context or labeled assumptions
- [ ] No canonical vs presentation boundary violations

- [ ] Assumptions are explicitly labeled when present
- [ ] Context gaps are surfaced where applicable
- [ ] No unsupported claims exist
- [ ] Output aligns with context status (complete vs partial)

---

## 12. Example Invocation (Normalized)

```yaml
request:
  target_role: District Executive
  job_description: <file>
  base_resume: <optional file>

runtime:
  primary_mode: build
  output_type: Document
  workflow_type: resume
```

---

## 13. Summary

The Resume Pack:

- Provides a deterministic interface to the runtime
- Encodes task, routing inputs, and output contract
- Produces consistent, high-quality resume artifacts

It ensures deterministic, grounded, and role-aligned resume generation aligned with CareerOS runtime constraints.