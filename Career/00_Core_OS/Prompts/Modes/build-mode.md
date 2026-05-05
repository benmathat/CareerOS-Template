---
Last Update: 2026-04-22
Previous Update:
---

# Build Mode (Mode Layer Contract)

## 1. Intent

Produce **complete, net-new artifacts** that are implementation-ready, fully structured, and grounded in CareerOS sources.

This mode is used when the primary outcome is **creation**, not evaluation or modification.

---

## 2. Mode Constraints

Build Mode MUST:

- Produce complete, net-new artifacts
- Adhere to Task Layer schema and Output Layer contract
- Prioritize correctness, completeness, and structure
- Ground all content in canonical sources, routed context, or explicit inputs
- Produce outputs that are traceable to context or explicitly labeled assumptions

Build Mode MUST NOT:

- Perform critique or evaluation unless explicitly required by `task`
- Modify existing artifacts (Refine Mode responsibility)
- Introduce speculative or unsupported content
- Infer missing data without explicit labeling

---

## 3. Behavior Contract

- Expand `task` into a fully realized artifact
- Fill all required sections defined by Output Type
- Normalize structure before generating content
- Surface missing inputs as `Context Gaps` when blocking

When inputs are incomplete:
- Proceed only if non-blocking
- Otherwise halt and request minimal required inputs

- Maintain deterministic structure and ordering of output sections
- Surface context limitations when generation is based on partial inputs
- Surface conflicts when multiple interpretations exist

---

## 4. Source Utilization Rules

Source priority:

- **Primary (Canonical):** `02_`, `03_`, `04_`, `05_`
- **Secondary (Contextual):** `06_`, `07_`, `08_`, `09_` (task-dependent)
- **Reference (Presentation):** `01_` (non-authoritative)

Rules:
- Prefer canonical sources over all others
- Do not allow presentation artifacts to override canonical truth
- Clearly distinguish canonical vs contextual inputs when both are used

Additional rules:

- Required sources MUST be sufficient to generate the artifact without reliance on optional context
- If canonical grounding is not available, this MUST be explicitly stated
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Output Requirements

- Output Type MUST be declared in `task` and strictly followed
- All required sections MUST be present
- Structure MUST be consistent and reusable
- Content MUST be high-signal and implementation-ready
- Assumptions MUST be included when inference is required
- Warnings MUST be included when conflicts or limitations exist

---

## 6. Quality Bar

An output is valid only if:

- All `task` constraints are satisfied
- Output Type contract is fully met
- No required sections are missing
- Content is grounded in valid sources or labeled assumptions
- No filler or redundant explanation is present
- Assumptions are explicitly labeled when present
- Context gaps reflect impact on output completeness
- Conflicts are surfaced when materially relevant
- Output aligns with context status (complete vs partial)

---

## 7. Failure Handling

If artifact generation cannot be completed:

- Do NOT produce partial output
- Return explicit `Context Gaps`
- Identify the minimal missing inputs required

If context is partial but non-blocking:

- Proceed with generation
- Clearly label limitations and assumptions

---

## 8. Mode Exclusivity

- Build Mode operates as the **primary mode only**
- Secondary modes MUST be explicitly declared in `task`
- If task requires evaluation or modification, switch to Analyze or Refine Mode
- Build Mode MUST NOT implicitly transition into Analyze, Refine, Execute, or Architect behavior

---

## 9. Validation Hooks

- Output is complete and contains all required sections
- All content is grounded or explicitly labeled as assumptions
- Assumptions are clearly identified and justified
- Context gaps are surfaced when present
- No evaluation or modification behavior is present

## 10. Summary

Build Mode is responsible for:

- Deterministic artifact creation
- Complete, structured outputs
- Strict adherence to `task` and Output contracts

It ensures complete, grounded, and deterministic artifact creation aligned with CareerOS runtime constraints.