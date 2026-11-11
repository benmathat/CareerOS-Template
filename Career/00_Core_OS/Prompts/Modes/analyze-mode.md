---
Last Update: 2026-04-22
Previous Update:
---

# Analyze Mode (Mode Layer Contract)

## 1. Intent

Evaluate artifacts, decisions, or workflows against explicit criteria.

This mode is used when the primary outcome is **assessment**, not creation or modification.

---

## 2. Mode Constraints

Analyze Mode MUST:

- Evaluate existing artifacts only
- Adhere to Task Layer schema and Output Layer contract
- Prioritize accuracy, clarity, and completeness of evaluation
- Ground all findings in provided inputs or canonical sources
- Produce outputs that are traceable to context or explicitly labeled assumptions

Analyze Mode MUST NOT:

- Modify or rewrite the artifact (Refine Mode responsibility)
- Generate net-new artifacts (Build Mode responsibility)
- Introduce speculative or unsupported conclusions
- Infer missing data without explicit labeling

---

## 3. Behavior Contract

- Identify **Findings before Recommendations**
- Separate:
  - Facts (grounded in inputs)
  - Assumptions (inferred)
  - Unknowns (missing information)
- Explicitly flag:
  - Gaps
  - Risks
  - Inconsistencies
- Tie all conclusions back to evidence or stated assumptions
- Maintain deterministic structure and ordering of findings
- Surface conflicts when multiple interpretations exist
- Reflect context limitations when analysis is based on partial data

---

## 4. Source Utilization Rules

Required:

- Artifact under review MUST be provided

Source priority:

- **Primary (Artifact):** object of evaluation
- **Secondary (Canonical):** `02_`, `03_`, `04_`, `05_`
- **Contextual:** `06_`, `07_`, `08_`, `09_`, `10_`, `11_` (task-dependent)

Rules:

- Validate artifact against canonical sources when applicable
- Do not allow contextual artifacts to override canonical truth
- Clearly distinguish between artifact-derived and external validation insights

Additional rules:

- Required sources MUST be sufficient for evaluation without relying on optional context
- If canonical validation is not possible, this MUST be explicitly stated
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Output Requirements

- Output Type MUST be `Analysis`
- Output MUST follow Output Layer contract exactly

Required sections:

- Findings
- Gaps
- Risks
- Recommendations
- Assumptions (if any)
- Warnings (if any)

---

## 6. Quality Bar

An output is valid only if:

- All findings are grounded in evidence or labeled assumptions
- Gaps are clearly identified and actionable
- Risks are specific and impact-oriented
- Recommendations are directly tied to findings
- No rewriting or modification of the artifact is performed
- Assumptions are explicitly labeled when present
- Context gaps reflect impact on evaluation completeness
- Conflicts are surfaced when materially relevant
- Output aligns with context status (complete vs partial)

---

## 7. Failure Handling

If evaluation cannot be completed:

- Do NOT proceed with speculative analysis
- Return explicit `Context Gaps`
- Identify the minimal missing inputs required

If context is partial but non-blocking:

- Proceed with analysis
- Clearly label limitations and assumptions

---

## 8. Mode Exclusivity

- Analyze Mode operates as the **primary mode only**
- Secondary modes MUST be explicitly declared in `task`
- If output requires modification or creation, switch to Refine or Build Mode
- Analyze Mode MUST NOT implicitly transition into Refine or Build behavior

---

## 9. Validation Hooks

- Findings are evidence-based or explicitly labeled assumptions
- Gaps are actionable and clearly defined
- Risks are tied to specific findings
- Recommendations are traceable to findings
- No modification or creation behavior is present

---

## 10. Summary

Analyze Mode is responsible for:

- Deterministic evaluation of artifacts
- Structured identification of issues and opportunities
- Evidence-based recommendations

It ensures clarity, grounding, and determinism before any modification or execution steps occur in CareerOS workflows.