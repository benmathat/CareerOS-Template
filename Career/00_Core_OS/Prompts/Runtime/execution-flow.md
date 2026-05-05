---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Execution Flow (Runtime Orchestrator Contract)

## 1. Purpose

Define the standard runtime execution sequence for producing deterministic outputs from CareerOS.

This file is the **runtime orchestrator** that coordinates:

- task normalization
- mode selection
- source routing
- context loading
- prompt assembly
- execution
- output validation
- optional iteration
- artifact routing

It MUST:
- enforce the correct execution order
- preserve layer boundaries
- prevent hidden schema drift
- stop invalid runs before final output

It MUST NOT:
- redefine mode behavior
- perform source routing directly
- perform prompt assembly logic directly
- silently skip validation gates

---

## 2. Runtime Inputs

Execution flow operates on normalized runtime inputs:

```yaml
request:
mode_selection:
task:
routing_output:
context_block:
prompt_object:
output:
```

Not all inputs exist at the start of execution.

They are produced progressively by the runtime.

### Input Contract

- `request` MUST be present at start
- Downstream objects are produced in sequence and MUST conform to their respective contracts:
  - `mode_selection` → from `mode-selection.md`
  - `routing_output` → from `source-routing.md`
  - `context_block` → from `context-loader.md`
  - `prompt_object` → from `prompt-assembler.md`
  - `output` → must satisfy `output-standards.md`
  - full runtime object envelope → from `runtime-io-schema.md`

---

## 3. Standard Flow

Execution MUST follow this exact sequence:

```text
1) Load System Contracts
2) Normalize / Validate task
3) Select Mode
4) Route Sources
5) Load Context
6) Assemble Prompt
7) Execute
8) Validate Output
9) Run Command Conformance Gate
10) Route Artifact
11) (Optional) Enter Iteration Loop
```

No step may be skipped unless explicitly inapplicable.

---

## 3.1 Global Halt Gates

Execution MUST halt when any of the following are true:

1. System contracts are missing
2. task schema is invalid
3. Mode is incompatible with task
4. Routing `status` is `invalid`
5. Routing `blocking` is `true`
6. Required sources cannot be routed
7. Context `status` is `partial_blocking`
8. Required context cannot be loaded
9. Prompt assembly fails
10. Output validation fails

Halt behavior:

- Do NOT proceed to subsequent steps
- Return structured error or required clarification
- Preserve all upstream runtime objects for inspection

---

## 4. Step Definitions

### 1) Load System Contracts

Load invariant contracts:

- `system-prompt.md`
- `interaction-model.md`
- `output-standards.md`

Purpose:
- establish non-overridable execution rules

Validation:
- all required system contracts MUST be present

### 2) Normalize / Validate task

Construct or validate the `task` object using strict schema:

- `task.objective`
- `task.scope`
  - `task.scope.in_scope`
  - `task.scope.out_of_scope`
- `task.inputs`
  - `task.inputs.required`
  - `task.inputs.optional`
- `task.constraints`
  - `task.constraints.hard`
  - `task.constraints.soft`
- `task.success_criteria`
- `task.output_type`

Purpose:
- create a normalized execution target before mode or context decisions

Validation:
- required fields MUST exist
- `task.output_type` MUST map to Output Layer types
- invalid task schema MUST halt execution

### 3) Select Mode

Use:
- `mode-selection.md`

Purpose:
- choose exactly one primary mode
- identify optional secondary mode only if explicitly required

Validation:
- primary mode MUST be valid
- mode MUST be compatible with artifact state and output type

### 4) Route Sources

Use:
- `source-routing.md`

Purpose:
- determine required, optional, and excluded sources
- determine output destination

Validation:
- routed sources MUST align with selected mode and workflow scope
- output destination MUST match durability and workflow type

Validation (extended):
- `routing_output.status` MUST NOT be `invalid`
- `routing_output.blocking` MUST be `false` for execution to proceed
- `routing_output.completeness.required_sources_resolved` SHOULD be `true`

### 5) Load Context

Use:
- `context-loader.md`

Purpose:
- convert routed sources into normalized, high-signal context

Validation:
- required sources MUST be included
- excluded sources MUST NOT appear
- `context_gaps` MUST be preserved

Validation (extended):
- `context_block.status` MUST be one of:
  - `complete`
  - `partial_non_blocking`
- `context_block.status` MUST NOT be `partial_blocking`
- `handoff.prompt_assembler_ready` MUST be `true`
- `handoff.execution_may_continue` MUST be `true`

### 6) Assemble Prompt

Use:
- `prompt-assembler.md`

Purpose:
- combine system contracts, normalized context, mode contract, task object, and output contract into a single execution-ready prompt

Validation:
- layer order MUST be correct
- required layers MUST be present
- unresolved directive conflicts MUST fail assembly

Validation (extended):
- All required layers MUST be present:
  - system
  - mode
  - task
  - context
  - output contract
- No unresolved conflicts between directives
- Prompt MUST reflect context gaps and assumptions when present

### 7) Execute

Run the assembled prompt exactly once for the current pass.

Purpose:
- produce the output artifact or result for validation

Rules:
- execution MUST use the assembled prompt object only
- no hidden schema or context mutation during execution

Rules (extended):
- Execution MUST NOT introduce new facts outside provided context
- Execution MUST propagate assumptions and uncertainty markers into output when required

### 8) Validate Output

Validate against:

- task constraints
- Output Layer contract
- source grounding expectations
- boundary rules

Checks:
- constraint compliance
- source grounding
- output structure compliance
- no hallucinated claims
- output-type section compliance (`Document`, `Framework`, `Template`, `Checklist`, `Analysis`)
- no source-of-truth boundary violations

If validation fails:
- execution MUST NOT finalize output
- failure MUST route into iteration logic or explicit error

Validation (extended):
- Assumptions marked `must_label_in_output: true` MUST be visible in output
- Output MUST respect `context_gaps` limitations
- Output MUST NOT contradict canonical context

### 9) Run Command Conformance Gate

Run deterministic end-of-run conformance pass:

- `command-conformance-gate.md`

Validation:

- all required runtime objects are present
- required statuses and blocking flags are valid
- source and boundary checks pass
- artifact writes remain blocked when conformance fails

If conformance fails:

- execution MUST halt
- `validation_result.passed` MUST be `false`
- `execution_trace.halted_at` MUST be populated

### 10) Route Artifact

After successful validation, route output to correct CareerOS destination.

Routing classes:

- canonical outputs → `02_`–`05_`
- presentation outputs → `01_`
- execution outputs → `06_`–`08_`
- reflection outputs → `10_`–`11_`

Rule:
- if content should remain true over time, prefer canonical routing
- if content is opportunity- or session-specific, prefer execution routing
- if content records learning, review, or compliance activity, prefer reflection routing

### 11) (Optional) Enter Iteration Loop

Iteration is allowed only when:

- quality gates fail
- user explicitly requests refinement
- workflow requires staged progression

Iteration MUST NOT be used as a substitute for missing required inputs.

---

## 5. Iteration Loop

Default improvement loop:

```text
Build -> Analyze -> Refine -> Finalize
```

Alternative loop behavior may occur when primary mode differs, but iteration MUST remain explicit and ordered.

Rules:
- each iteration MUST preserve task identity
- each iteration MUST validate output before proceeding
- iteration MUST stop once quality gates pass or blocking gaps remain

---

## 6. Quality Gates

Required before final output:

- all required sections present
- claims traceable to loaded context
- no source-of-truth boundary violations
- formatting matches output standards or explicit template
- hard constraints satisfied
- output is compatible with selected output type

Failure of any quality gate blocks finalization.

---

## 7. Failure Modes

### Ambiguous task

- return required clarification only if blocking
- otherwise proceed with explicit assumptions

### Missing Context

- return explicit `Context Gaps`
- do not hallucinate missing facts

### Conflicting Evidence

- prefer canonical sources by default
- surface material conflict explicitly

### Output Drift

- re-run through iteration only if task and context remain valid
- otherwise halt with explicit validation failure

### Invalid Runtime Object

- halt execution
- return contract error for the failing runtime component

### Invalid Routing or Context

- If `routing_output.status = invalid` → halt immediately
- If `routing_output.blocking = true` → halt immediately
- If `context_block.status = partial_blocking` → halt immediately
- Return required clarification or missing inputs

---

## 8. Runtime Output Contract

The orchestrator MUST produce or update the following runtime objects in order:

```yaml
task:
mode_selection:
routing_output:
  status:
  blocking:
context_block:
  status:
prompt_object:
output:
validation_result:
  passed: true|false
  failures:
artifact_destination:
execution_trace:
  steps_completed:
  halted_at:
  reason:
```

All object shapes and minimum fields MUST conform to:

- `runtime-io-schema.md`

### Output Rules

- All runtime objects MUST be internally consistent
- `execution_trace` MUST reflect actual flow progression
- If halted, `halted_at` and `reason` MUST be populated
- Partial executions MUST still return structured runtime state

---

## 9. Compliance Hook Timing

Compliance prompts MUST occur only after real-world job-search activity has occurred or is being explicitly prepared for execution.

Do NOT recommend `/log-activity` for:
- internal analysis
- prompt assembly
- resume editing alone
- strategy discussion
- hypothetical planning

Do recommend `/log-activity` after:
- application submission
- interview scheduled
- interview completed
- networking contact made
- follow-up sent
- recruiter/employer contact
- qualifying work-search activity completed

---

## 10. Summary

The Execution Flow:

- coordinates all CareerOS runtime components in the correct order
- enforces validation gates before final output
- supports controlled iteration without hidden drift
- routes validated artifacts to the correct destination

It is the deterministic execution spine of CareerOS, ensuring that every step either produces a valid runtime object or halts with explicit, inspectable failure conditions. It guarantees that no output is produced without validated task structure, grounded context, and compliant assembly.
