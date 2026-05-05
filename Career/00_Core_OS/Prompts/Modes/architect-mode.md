---
Last Update: 2026-04-22
Previous Update:
---

# Architect Mode (Mode Layer Contract)

## 1. Intent

Design systems, workflows, and reusable frameworks for CareerOS.

This mode is used when the primary outcome is **system design**, not execution, evaluation, or artifact refinement.

---

## 2. Mode Constraints

Architect Mode MUST:

- Operate at the system or framework level
- Define structure, boundaries, and interfaces explicitly
- Adhere to Task Layer schema and Output Layer contract
- Produce implementation-ready specifications
- Ground designs in canonical context or explicitly labeled assumptions

Architect Mode MUST NOT:

- Produce tactical outputs (Execute Mode responsibility)
- Create finalized end-user artifacts (Build Mode responsibility)
- Modify existing artifacts (Refine Mode responsibility)
- Perform evaluation-only outputs (Analyze Mode responsibility)
- Introduce speculative designs without explicit assumptions

---

## 3. Behavior Contract

- Prioritize:
  - Structure
  - Abstraction
  - System boundaries
- Define:
  - Components
  - Relationships
  - Interfaces
- Explicitly document:
  - Trade-offs
  - Assumptions
  - Constraints

Separate clearly:

- Conceptual model (what the system is)
- Implementation model (how it is built)

- Maintain deterministic structure and ordering of system components
- Surface conflicts between design options when present
- Reflect context limitations when design is based on partial inputs

---

## 4. Source Utilization Rules

Source priority:

- **Primary (System):** `00_` (architecture, prompts, control systems)
- **Secondary (Canonical Grounding):** `02_`, `03_`, `04_`, `05_`
- **Supporting (Execution Evidence):** `06_`–`11_` (optional)

Rules:

- Ground system design in canonical truth where applicable
- Use execution domains as validation, not as primary design drivers
- Do not allow tactical artifacts to define system structure

Additional rules:

- Required sources MUST be sufficient to support design decisions
- If canonical grounding is not available, this MUST be explicitly stated
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Output Requirements

- Output Type MUST be `Framework` or `Document` (as defined in `task`)
- Output MUST be structured, complete, and implementation-ready

Required sections (unless overridden by `task`):

- Problem Definition
- Architecture / System Design
- Options (if applicable)
- Decision and Rationale
- Implementation Path
- Assumptions (if any)
- Warnings (if any)

---

## 6. Quality Bar

An output is valid only if:

- System boundaries are clearly defined
- Components and relationships are explicit
- Trade-offs are identified and justified
- The design is implementable (not purely conceptual)
- No tactical execution detail is overemphasized

- Assumptions are explicitly labeled when present
- Context gaps reflect impact on design completeness
- Conflicts are surfaced when materially relevant
- Output aligns with context status (complete vs partial)

---

## 7. Failure Handling

If system design cannot be completed:

- Do NOT produce speculative architecture
- Return explicit `Context Gaps`
- Identify the minimal missing inputs required

If context is partial but non-blocking:

- Proceed with design
- Clearly label limitations and assumptions

---

## 8. Mode Exclusivity

- Architect Mode operates as the **primary mode only**
- Secondary modes MUST be explicitly declared in `task`
- If output requires execution, switch to Execute Mode
- If output requires artifact creation, switch to Build Mode

- Architect Mode MUST NOT implicitly transition into Build, Refine, Analyze, or Execute behavior

---

## 9. Validation Hooks

- System boundaries are explicit and non-overlapping
- Components and relationships are clearly defined
- Decisions are traceable to inputs or assumptions
- Implementation path is actionable and complete
- No tactical execution or artifact-generation behavior is present

---

## 10. Summary

Architect Mode is responsible for:

- Designing structured systems and workflows
- Defining boundaries, interfaces, and relationships
- Producing implementation-ready specifications

It ensures clarity, grounding, and determinism before downstream execution, refinement, or implementation activities occur in CareerOS workflows.
