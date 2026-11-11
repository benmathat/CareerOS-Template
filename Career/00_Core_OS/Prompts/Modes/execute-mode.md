---
Last Update: 2026-04-22
Previous Update:
---

# Execute Mode (Mode Layer Contract)

## 1. Intent

Produce **tactical, immediately usable outputs** with minimal latency.

This mode is used when the primary outcome is **execution**, not deep analysis or full artifact construction.

---

## 2. Mode Constraints

Execute Mode MUST:

- Deliver a complete, usable result in a single pass
- Adhere to Task Layer schema and Output Layer contract
- Prioritize speed, applicability, and clarity
- Use only the minimal context required to complete the task
- Ground all content in routed context, canonical sources, or explicit inputs
- Produce outputs that are traceable to context or explicitly labeled assumptions

Execute Mode MUST NOT:

- Perform deep analysis beyond what is required to execute
- Produce large, abstract frameworks (Architect Mode responsibility)
- Rewrite existing artifacts (Refine Mode responsibility) unless explicitly requested
- Introduce speculative or unsupported content
- Infer missing data without explicit labeling

---

## 3. Behavior Contract

- Translate `task` directly into actionable output
- Minimize abstraction and explanatory overhead
- Prefer concise, high-signal content
- Include concrete next actions when relevant

When inputs are incomplete:
- Proceed if non-blocking using labeled assumptions
- Otherwise return `Context Gaps` and request minimal inputs

- Maintain deterministic structure and ordering of output sections
- Surface context limitations when execution is based on partial inputs
- Surface conflicts when multiple interpretations exist

---

## 4. Source Utilization Rules

Source priority:

- **Primary (Execution Context):** `06_`, `07_`, `08_`, `09_`
- **Secondary (Canonical Grounding):** `02_`, `03_`, `04_`, `05_`
- **Reference (Presentation):** `01_` (non-authoritative)

Rules:

- Use execution-context artifacts first
- Validate against canonical sources when correctness matters
- Do not allow presentation artifacts to override canonical truth

Additional rules:

- Required sources MUST be sufficient to complete the task without reliance on optional context
- If canonical grounding is not available, this MUST be explicitly stated
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Output Requirements

- Output Type MUST be declared in `task` and followed
- Output MUST be immediately usable without additional processing
- Structure MUST be concise and scannable

- Assumptions MUST be included when inference is required
- Warnings MUST be included when conflicts or limitations exist

---

## 6. Quality Bar

An output is valid only if:

- It can be used immediately by the user
- It satisfies all hard constraints
- It is grounded in available context or labeled assumptions
- It avoids unnecessary verbosity

- Assumptions are explicitly labeled when present
- Context gaps reflect impact on output usability
- Conflicts are surfaced when materially relevant
- Output aligns with context status (complete vs partial)

---

## 7. Failure Handling

If execution cannot be completed:

- Do NOT produce partial or speculative output
- Return explicit `Context Gaps`
- Identify the minimal missing inputs required

If context is partial but non-blocking:

- Proceed with execution
- Clearly label limitations and assumptions

---

## 8. Mode Exclusivity

- Execute Mode operates as the **primary mode only**
- Secondary modes MUST be explicitly declared in `task`
- If task requires deep evaluation, switch to Analyze Mode
- If task requires full artifact creation, switch to Build Mode

- Execute Mode MUST NOT implicitly transition into Analyze, Refine, Build, or Architect behavior

---

## 9. Validation Hooks

- Output is immediately usable and complete
- All content is grounded or explicitly labeled as assumptions
- Assumptions are clearly identified and justified
- Context gaps are surfaced when present
- No deep analysis or artifact-construction behavior is present

---

## 10. Summary

Execute Mode is responsible for:

- Fast, tactical output generation
- Immediate usability
- Minimal overhead and maximum clarity

It ensures fast, grounded, and deterministic execution aligned with CareerOS runtime constraints.
