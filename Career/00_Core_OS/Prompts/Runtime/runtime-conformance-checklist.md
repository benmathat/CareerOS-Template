---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Runtime Conformance Checklist (System Validation Contract)

## Purpose

Validate that CareerOS runtime behavior remains fully aligned with:

- `careeros-prompt-architecture-spec.md`
- Runtime contracts (`mode-selection`, `source-routing`, `context-loader`, `prompt-assembler`, `execution-flow`)

This checklist is a **validation artifact**, not guidance. All items are enforceable.

---

## 1. Layer Order Contract

- [ ] Final assembled prompt order is exactly: **System → Mode → Task → Context → Output**
- [ ] `Runtime/prompt-assembler.md` enforces this order (not just documents it)
- [ ] No runtime component introduces alternate ordering
- [ ] No layer injects content into another layer’s responsibility

---

## 2. Runtime Object Integrity

- [ ] All runtime objects exist and are explicitly defined:
  - `request`
  - `task`
  - `mode_selection` (must include `status`, `blocking`, `confidence`)
  - `routing_output` (must include `status`, `blocking`, `confidence`)
  - `context_block` (must include `status`, `handoff`)
  - `prompt_object`
  - `output`
  - `validation_result`
  - `artifact_destination`
  - `execution_trace`
- [ ] Objects are produced in correct sequence (per `execution-flow.md`)
- [ ] No runtime step mutates upstream objects without validation

---

## 3. Task Schema Enforcement

- [ ] `task.objective` is singular and explicit
- [ ] `task.scope.in_scope` and `task.scope.out_of_scope` are both present
- [ ] `task.inputs.required` exists
- [ ] `task.constraints.hard` exists and is testable
- [ ] `task.success_criteria` is measurable
- [ ] `task.output_type` is valid (`Document`, `Framework`, `Template`, `Checklist`, `Analysis`)
- [ ] Invalid task schema halts execution before mode selection or routing

---

## 4. Mode Selection Integrity

- [ ] Exactly one primary mode is selected
- [ ] Secondary mode(s), if present, are explicitly declared
- [ ] Mode selection is derived from normalized task inputs (not ad hoc inference)
- [ ] Mode is compatible with:
  - artifact state
  - output type
  - objective
- [ ] `mode_selection.status` is not `invalid`
- [ ] `mode_selection.blocking` is `false`
- [ ] `confidence` reflects ambiguity level
- [ ] Any assumptions used in selection are explicitly recorded

---

## 5. Mode Boundary Enforcement

- [ ] `Build` produces net-new artifacts only
- [ ] `Analyze` performs evaluation only (no modification)
- [ ] `Refine` performs delta improvements only
- [ ] `Execute` prioritizes speed and minimizes abstraction
- [ ] `Architect` operates at system level only
- [ ] `Transform` preserves meaning and introduces no net-new facts
- [ ] No mode violates another mode’s responsibility

---

## 6. Source Routing Integrity

- [ ] Routing uses normalized inputs (`mode_selection`, `task`, etc.)
- [ ] Routing output includes:
  - `status`
  - `blocking`
  - `source_set.required`
  - `source_set.optional`
  - `source_set.excluded`
  - `output_destination`
  - `confidence`
- [ ] `routing_output.status` is not `invalid`
- [ ] `routing_output.blocking` is `false`
- [ ] Required sources are sufficient for task completion
- [ ] Optional sources are loaded only when necessary
- [ ] Excluded sources are never used
- [ ] Canonical vs contextual rules are enforced

---

## 7. Context Loader Integrity

- [ ] Context is derived ONLY from routing output
- [ ] Explicit inputs are always included first
- [ ] Context is compressed into structured blocks
- [ ] Extraction includes:
  - facts
  - metrics
  - constraints
  - decisions
  - gaps
- [ ] Context does NOT include:
  - redundant narrative
  - presentation phrasing
- [ ] `context_gaps` are explicitly recorded
- [ ] No hallucinated data is introduced
- [ ] `context_block.status` is either `complete` or `partial_non_blocking`
- [ ] `context_block.status` is NOT `partial_blocking`
- [ ] `handoff.prompt_assembler_ready = true`
- [ ] `handoff.execution_may_continue = true`
- [ ] `conflicts` are recorded when present
- [ ] `assumptions` include `must_label_in_output` when required

---

## 8. Prompt Assembler Integrity

- [ ] Assembler consumes:
  - system contracts
  - normalized context
  - mode contract
  - validated task
  - output contract
- [ ] Assembler does NOT:
  - perform routing
  - perform context loading
  - modify task schema
- [ ] Layer order is strictly enforced
- [ ] Conflicts are resolved via precedence or fail explicitly
- [ ] Assembler rejects invalid routing or blocking context
- [ ] Routing and context status are preserved in prompt
- [ ] Context gaps, assumptions, and conflicts are surfaced in prompt
- [ ] No uncertainty signals are suppressed

---

## 9. Execution Integrity

- [ ] Execution uses only the assembled prompt object
- [ ] No hidden context injection occurs during execution
- [ ] No schema drift occurs between assembly and execution
- [ ] Execution respects context limitations and gaps
- [ ] Assumptions requiring labeling are surfaced in output
- [ ] No new facts are introduced outside provided context

---

## 10. Output Validation

- [ ] Output satisfies all hard constraints
- [ ] Output matches required `task.output_type` structure
- [ ] All claims are traceable to context or labeled assumptions
- [ ] No hallucinated or fabricated content exists
- [ ] No canonical vs presentation boundary violations occur
- [ ] Output reflects all required assumption labels
- [ ] Output reflects context gaps where relevant
- [ ] Output does not contradict canonical context

---

## 11. Artifact Routing Integrity

- [ ] Output is routed to correct domain:
  - canonical (`02_–05_`) for durable truth
  - presentation (`01_`) for external artifacts
  - execution (`06_–08_`) for active workflows
  - reflection (`10_–11_`) for learning/compliance
- [ ] Routing aligns with content durability and workflow scope

---

## 12. Iteration Control

- [ ] Iteration occurs only when:
  - validation fails
  - user explicitly requests refinement
  - pipeline requires staged progression
- [ ] Iteration preserves original task identity
- [ ] Iteration does NOT compensate for missing required inputs
- [ ] Iteration does NOT proceed if routing or context is blocking

---

## 13. Determinism and Grounding

- [ ] Same inputs produce same outputs (determinism)
- [ ] Canonical-over-contextual precedence is enforced
- [ ] Explicit inputs are never overridden
- [ ] Missing context is surfaced explicitly and classified as blocking or non-blocking
- [ ] Determinism tie-breakers are consistently applied (mode, routing, context)
- [ ] Confidence levels reflect ambiguity accurately

---

## 14. Halt and Failure Enforcement

- [ ] Execution halts when:
  - routing status is `invalid`
  - routing is `blocking`
  - context is `partial_blocking`
  - prompt assembly fails
  - output validation fails
- [ ] Halt conditions produce structured runtime state
- [ ] `execution_trace.halted_at` and `reason` are populated

---

## 15. Documentation Integrity

- [ ] All runtime files are consistent with architecture spec
- [ ] Terminology is consistent across all documents
- [ ] Cross-references are valid and current
- [ ] No runtime file duplicates responsibilities of another

---

## 16. Sign-Off

- [ ] Conformance review completed
- [ ] Deviations documented with rationale
- [ ] Remediation actions defined and tracked