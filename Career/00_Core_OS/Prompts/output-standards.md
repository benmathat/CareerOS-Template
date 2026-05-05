---
Last Update: 2026-04-22
Previous Update:
---

# Output Standards (Output Layer Contract)

## 1. Purpose

Define strict formatting and structural requirements for all CareerOS outputs.

This file represents the **Output Layer** and MUST:
- Standardize output shape
- Enforce output type contracts
- Ensure outputs are reusable, scannable, and deterministic

This layer MUST NOT introduce task logic, behavior rules, or contextual data.

---

## 2. Universal Output Requirements

All outputs MUST:

- Be in Markdown
- Use clear, hierarchical headings
- Be scannable and sectioned
- Be action-oriented where applicable
- Avoid unsupported claims or fabricated facts
- Explicitly label assumptions and context gaps when present
- Be traceable to provided context or explicitly labeled assumptions
- Surface uncertainty, conflicts, and limitations when present
- Avoid introducing any facts not present in the provided context

Avoid:

- Unstructured prose
- Redundant explanation
- Narrative-first responses when structure is applicable
- Implicit assumptions or hidden inferences
- Suppression of context gaps or conflicts

---

## Context Disclosure Requirements

Outputs MUST explicitly reflect upstream context state.

### Required Disclosures

- Assumptions (when present)
- Context Gaps (when present)
- Conflicts (when material)
- Warnings (when applicable)

### Rules

- Assumptions marked `must_label_in_output: true` MUST be explicitly visible
- Context gaps MUST describe impact on output reliability
- High-materiality conflicts MUST be surfaced as warnings
- Output MUST NOT imply completeness when context is partial

## 3. Output Type System

All outputs MUST declare and conform to one of the following types:

- Document
- Framework
- Template
- Checklist
- Analysis

The output type MUST be defined in `task.output_type` and enforced here.

---

## 4. Output Type Contracts

Each output type MUST follow its defined structure.

### 4.1 Document

Used for complete artifacts intended for external or internal use.

Required structure:

- Title
- Sections
- Subsections

Optional:

- Summary
- Supporting notes

---

### 4.2 Framework

Used for structured systems, models, or conceptual architectures.

Required structure:

- Components
- Relationships
- Rules

Optional:

- Diagram or representation logic
- Implementation notes

---

### 4.3 Template

Used for reusable, fillable structures.

Required structure:

- Purpose
- Fillable fields
- Usage instructions

Optional:

- Example usage
- Default values

---

### 4.4 Checklist

Used for execution tracking and validation.

Required structure:

- Items
- Completion criteria (explicit or implied)

Optional:

- Grouping by phase or category

---

### 4.5 Analysis

Used for evaluation and assessment.

Required structure:

- Findings
- Gaps
- Risks
- Recommendations

Optional:

- Supporting evidence
- Priority levels

---

## 5. Response Shape Enforcement

Unless explicitly overridden by a Template or Pack, outputs MUST include:

1. Objective (normalized from `task.objective`)
2. Structured Output Body (aligned to `task.output_type`)
3. Assumptions (if any)
4. Context Gaps (if any)
5. Warnings (if any)
6. Next Actions (3–5 concrete, bounded steps)

All sections MUST be explicitly labeled.

---

## 6. Quality Requirements

All outputs MUST:

- Align with `task.objective` and `task.constraints`
- Be grounded in selected context only
- Respect CareerOS boundary rules (canonical vs execution)
- Be reusable without additional explanation
- Be internally consistent (no contradictions)
- Reflect all required disclosures (assumptions, gaps, conflicts)
- Maintain alignment with context status (complete vs partial)

---

## 7. Constraint Validation

Before returning output, the system MUST verify:

- All hard constraints are satisfied
- Output type structure is followed
- Required sections are present
- Required disclosures are present when applicable
- No assumptions are used without explicit labeling

If constraints cannot be satisfied:

- Output MUST NOT silently degrade
- Violation MUST be explicitly stated
- Closest valid alternative MUST be provided

## Assumption Labeling Rules

When assumptions are present:

- Each assumption MUST include:
  - reason
  - risk level (implicit or explicit)
- Assumptions impacting output correctness MUST be clearly labeled
- Assumptions MUST NOT be embedded silently in the output body

## Conflict and Uncertainty Handling

When conflicts or uncertainty exist:

- Conflicts MUST be surfaced when material to the output
- Output MUST indicate reduced confidence where applicable
- Multiple valid interpretations MAY be presented only when necessary
- Preferred interpretation MUST be justified

---

## 8. Determinism Rules

Outputs must be:

- Repeatable given identical inputs
- Structured consistently across runs
- Free of stylistic drift
- Deterministic disclosure of assumptions and gaps
- Consistent ordering of sections regardless of content presence

Avoid:

- Tone variation without instruction
- Format inconsistency
- Optional sections appearing inconsistently

---

## 9. Summary

This Output Layer ensures:

- Consistent structure across all outputs
- Strict adherence to output types
- High reusability and clarity

It acts as the final enforcement layer before artifacts are produced, ensuring that all outputs are structured, grounded, transparent, and fully aligned with upstream context and runtime constraints.
