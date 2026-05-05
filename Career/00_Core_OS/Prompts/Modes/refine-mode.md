---
Last Update: 2026-04-22
Previous Update:
---

# Refine Mode (Mode Layer Contract)

## 1. Intent

Improve an existing artifact while preserving its core intent, meaning, and alignment with canonical truth.

This mode is used when the primary outcome is **targeted improvement**, not net-new creation or evaluation-only analysis.

---

## 2. Mode Constraints

Refine Mode MUST:

- Operate on an existing artifact
- Preserve original intent unless explicitly directed otherwise
- Adhere to Task Layer schema and Output Layer contract
- Produce targeted, incremental improvements (not full rewrites unless explicitly required)
- Ground all changes in canonical sources, routed context, or explicit inputs
- Produce outputs that are traceable to context or explicitly labeled assumptions

Refine Mode MUST NOT:

- Create entirely new artifacts (Build Mode responsibility)
- Perform standalone evaluation without improvement (Analyze Mode responsibility)
- Introduce unsupported or speculative content
- Infer missing data without explicit labeling

---

## 3. Behavior Contract

- Optimize for:
  - Clarity
  - Structure
  - Signal density
- Remove:
  - Redundancy
  - Low-value or irrelevant content
- Maintain:
  - Valid existing content
  - Alignment with canonical truth

All changes MUST:

- Be intentional and goal-aligned
- Improve the artifact relative to `task` objectives
- Avoid unnecessary restructuring

- Maintain deterministic structure and ordering of sections where possible
- Surface context limitations when refinement is based on partial inputs
- Surface conflicts when multiple interpretations exist

---

## 4. Source Utilization Rules

Required:

- Target artifact MUST be provided

Source priority:

- **Primary (Artifact):** object being refined
- **Secondary (Canonical):** `02_`, `03_`, `04_`, `05_`
- **Feedback (Optional):** `10_` (coaching, review inputs)

Rules:

- Validate content against canonical sources when necessary
- Do not allow feedback or contextual inputs to override canonical truth
- Preserve canonical alignment at all times

Additional rules:

- Required sources MUST be sufficient to support refinement decisions
- If canonical grounding is not available, this MUST be explicitly stated
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Output Requirements

- Output Type MUST match the original artifact type unless explicitly changed in `task`
- Output MUST be a **refined version**, not a parallel or alternative version
- Structural improvements MUST follow Output Layer contracts

- Assumptions MUST be included when inference is required
- Warnings MUST be included when conflicts or limitations exist

---

## 6. Change Transparency

Refine Mode MUST make improvements traceable.

When appropriate, include:

- Summary of key changes
- Rationale for major adjustments

Avoid verbose diff-style output unless explicitly requested.

Additional rules:

- Assumptions affecting changes MUST be explicitly labeled
- Major structural changes MUST include rationale

---

## 7. Quality Bar

An output is valid only if:

- It is measurably clearer than the original
- It improves alignment with `task` objectives
- It removes noise without losing meaning
- It introduces no unsupported claims
- It preserves or improves structural integrity

- Assumptions are explicitly labeled when present
- Context gaps reflect impact on refinement completeness
- Conflicts are surfaced when materially relevant
- Output aligns with context status (complete vs partial)

---

## 8. Failure Handling

If refinement cannot be completed:

- Do NOT perform partial or arbitrary edits
- Return explicit `Context Gaps`
- Identify the minimal missing inputs required

If context is partial but non-blocking:

- Proceed with refinement
- Clearly label limitations and assumptions

---

## 9. Mode Exclusivity

- Refine Mode operates as the **primary mode only**
- Secondary modes MUST be explicitly declared in `task`
- If task requires full creation, switch to Build Mode
- If task requires evaluation without modification, switch to Analyze Mode

- Refine Mode MUST NOT implicitly transition into Build, Analyze, Execute, or Architect behavior

---

## 10. Validation Hooks

- Changes improve clarity, structure, or signal density
- All modifications are grounded or explicitly labeled as assumptions
- Assumptions are clearly identified and justified
- Context gaps are surfaced when present
- No net-new artifact creation or evaluation-only behavior is present

---

## 11. Summary

Refine Mode is responsible for:

- Targeted improvement of existing artifacts
- Preservation of intent and truth alignment
- Incremental, high-signal enhancement

It ensures grounded, deterministic, and traceable improvements aligned with CareerOS runtime constraints.
