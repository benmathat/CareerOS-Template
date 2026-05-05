---
Last Update: 2026-04-24
Previous Update:
---

# Transform Mode

## 1. Purpose

Convert an existing artifact into a different structure or format **without changing its underlying meaning**.

Transform Mode preserves semantic intent while adapting presentation, structure, or target context.

This mode is used for:
- resume → cover letter
- story → interview answer
- notes → structured document
- document → checklist/template

---

## 2. Mode Constraints

Transform Mode MUST:

- Operate on one or more existing source artifacts
- Preserve original meaning, facts, and claims
- Adhere to Task Layer schema and Output Layer contract
- Perform structural or format conversion only
- Ground all content in provided context or explicit inputs
- Produce outputs that are traceable to source content or explicitly labeled assumptions

Transform Mode MUST NOT:

- Introduce new facts or claims
- Perform evaluation-only outputs (Analyze Mode responsibility)
- Create net-new content beyond structural transformation (Build Mode responsibility)
- Modify intent or meaning (Refine Mode responsibility)
- Introduce speculative or unsupported content
- Infer missing data without explicit labeling

---

## 3. Behavior Contract

- Map source structure to target structure deterministically
- Preserve all essential information unless explicitly instructed to omit
- Normalize output to target format before populating content
- Maintain ordering and grouping consistent with target structure

When inputs are incomplete:
- Proceed only if non-blocking
- Otherwise return `Context Gaps`

Additional rules:

- Maintain deterministic structure and ordering of output sections
- Surface context limitations when transformation is based on partial inputs
- Surface conflicts when multiple interpretations exist

---

## 4. Source Utilization Rules

Required:

- Source artifact(s) MUST be provided

Source priority:

- **Primary:** provided artifact(s)
- **Secondary (Canonical):** `02_`, `03_`, `04_`, `05_` (for validation only)
- **Contextual (Optional):** `06_`, `07_`, `08_`, `09_` (task-dependent)

Rules:

- Preserve canonical truth from source artifacts
- Do not allow contextual inputs to alter original meaning
- Clearly distinguish between transformed content and any supplemental inputs

Additional rules:

- Required sources MUST be sufficient to perform transformation
- If canonical validation is not possible, this MUST be explicitly stated
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Output Requirements

- Output Type MUST be declared in `task` and strictly followed
- Output MUST reflect target structure completely
- Content MUST preserve original meaning and intent
- Structure MUST be consistent, reusable, and scannable

Additional requirements:

- Assumptions MUST be included when inference is required
- Warnings MUST be included when conflicts or limitations exist

---

## 6. Fidelity Requirements

Transform Mode MUST preserve:

- Facts
- Metrics
- Outcomes
- Ownership

Transform Mode MAY:

- Reorder content
- Reframe phrasing for clarity or audience
- Compress or expand content to fit target format

Transform Mode MUST NOT:

- Change meaning
- Introduce new claims
- Omit critical information without justification

---

## 7. Quality Bar

An output is valid only if:

- All required sections are present in target structure
- Content meaning matches source artifact(s)
- No unsupported claims are introduced
- Structure improves usability for the target format

Additional requirements:

- Assumptions are explicitly labeled when present
- Context gaps reflect impact on transformation completeness
- Conflicts are surfaced when materially relevant
- Output aligns with context status (complete vs partial)

---

## 8. Failure Handling

If transformation cannot be completed:

- Do NOT produce partial or speculative output
- Return explicit `Context Gaps`
- Identify the minimal missing inputs required

If context is partial but non-blocking:

- Proceed with transformation
- Clearly label limitations and assumptions

---

## 9. Mode Exclusivity

- Transform Mode operates as the **primary mode only**
- Secondary modes MUST be explicitly declared in `task`
- If task requires creation of new content, switch to Build Mode
- If task requires modification of intent, switch to Refine Mode
- If task requires evaluation, switch to Analyze Mode

- Transform Mode MUST NOT implicitly transition into Build, Refine, Analyze, Execute, or Architect behavior

---

## 10. Validation Hooks

- Output structure matches target format exactly
- All content is traceable to source artifact(s) or labeled assumptions
- Meaning is preserved across transformation
- Assumptions are clearly identified and justified
- Context gaps are surfaced when present

---

## 11. Summary

Transform Mode is responsible for:

- Structural conversion of artifacts
- Preservation of meaning and truth
- Deterministic, format-aligned outputs

It ensures accurate, grounded, and reusable transformations aligned with CareerOS runtime constraints.