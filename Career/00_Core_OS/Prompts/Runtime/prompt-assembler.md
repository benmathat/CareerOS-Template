---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Prompt Assembler (Runtime Contract)

## 1. Purpose

Define how prompts are deterministically assembled from CareerOS runtime components.

This file is the **assembly layer** that converts:

- System contracts
- Selected mode
- Validated task
- Normalized context
- Output contract

into a **single, execution-ready prompt object**.

It MUST:
- Enforce strict layer order
- Prevent missing required layers
- Resolve or reject duplicate/conflicting directives
- Produce a normalized final prompt structure

It MUST NOT:
- Select sources directly (Routing responsibility)
- Load files directly (Context Loader responsibility)
- Introduce new task logic
- Modify runtime inputs silently

---

## 2. Core Concept

The Prompt Assembler is a **compiler**, not a template.

It consumes validated runtime components and emits a normalized prompt package for execution.

It does NOT:
- decide what sources to load
- infer missing required task fields
- perform context compression itself

Those functions are delegated to:
- `mode-selection.md`
- `source-routing.md`
- `context-loader.md`

---

## 3. Required Inputs

Every prompt assembly requires the following normalized inputs:

### 3.1 System Contracts

Load:
- `/00_Core_OS/Prompts/system-prompt.md`
- `/00_Core_OS/Prompts/interaction-model.md`
- `/00_Core_OS/Prompts/output-standards.md`

These define invariant rules and MUST always be present.

### 3.2 mode_selection Object

Required structure:

```yaml
mode_selection:
  status:
  blocking:
  primary_mode:
  secondary_mode:
  rationale:
  assumptions:
  confidence:
```

Rules:
- `mode_selection.primary_mode` MUST be present
- `mode_selection.status` MUST NOT be `invalid`
- `mode_selection.blocking` MUST be `false`
- `mode_selection.secondary_mode` is optional
- Any secondary mode MUST already be validated upstream

### 3.3 Validated `task` Object

Required structure:

```yaml
task:
  objective:
  scope:
    in_scope:
    out_of_scope:
  inputs:
    required:
    optional:
  constraints:
    hard:
    soft:
  success_criteria:
  output_type:
```

Source:
- `/00_Core_OS/Prompts/Templates/Tasks/`

The assembler MUST reject invalid or incomplete task objects.

### 3.4 Normalized Context Block

Input source:
- `context-loader.md`

Required structure:

```yaml
context_block:
  status: complete|partial_non_blocking|partial_blocking
  task_alignment:
    objective:
    mode:
    output_type:
    durability_class:
  canonical_context:
    - path:
      source_type:
      key_facts:
      key_metrics:
      constraints:
      decisions:
      freshness:
      relevance_to_task:
  contextual_context:
    - path:
      source_type:
      key_facts:
      key_metrics:
      constraints:
      decisions:
      freshness:
      relevance_to_task:
  supporting_context:
    - path:
      source_type:
      key_facts:
      constraints:
      freshness:
      relevance_to_task:
  context_gaps:
    - missing_information:
      why_needed:
      blocking: true|false
      suggested_source:
      suggested_user_action:
  conflicts:
    - conflict:
      sources:
      resolution:
      materiality: low|medium|high
  assumptions:
    - assumption:
      reason:
      risk:
      must_label_in_output: true|false
  warnings:
    - type:
      description:
  handoff:
    prompt_assembler_ready: true|false
    execution_may_continue: true|false
    required_user_clarification:
```

The assembler MUST consume this structure as-is and MUST NOT rebuild it.

### 3.5 Output Contract

Derived from:
- `task.output_type`
- `/00_Core_OS/Prompts/Templates/Outputs/`

If no explicit template exists, the assembler MUST fall back to:
- `/00_Core_OS/Prompts/output-standards.md`

---

## 4. Assembly Invariants

The assembler MUST enforce the following invariants:

## Assembly Preconditions

The assembler MUST reject assembly if:

- `task` is missing required fields
- `mode_selection` is missing or invalid
- `routing_output.status = invalid`
- `routing_output.blocking = true`
- `context_block.status = partial_blocking`
- `context_block.handoff.prompt_assembler_ready = false`
- output contract is missing
- source boundary warnings are unresolved

### 4.1 Layer Order

Final prompt order is fixed:

1. System Layer
2. Mode Layer
3. Task Layer
4. Context Layer
5. Output Layer

No reordering is allowed.

### 4.2 Required Layers

Required layers:
- System
- Context
- Mode
- Task

Optional layer:
- Output (defaults to system output standards if no explicit template is available)

Missing required layers MUST fail assembly.

### 4.3 Conflict Precedence

Directive precedence is:

1. System
2. Mode
3. Task
4. Output

Context provides facts/state only and MUST NOT override behavioral directives.

### 4.4 Duplicate Directives

Duplicate directives MAY be accepted only if they are semantically aligned.

If duplicate directives conflict:
- Higher-precedence layer wins when conflict is resolvable
- Unresolvable conflicts MUST fail assembly

### 4.5 Determinism

Given the same normalized inputs, the assembler MUST produce the same final prompt object.

---

## 5. Assembly Pipeline

### Step 1 — Load System Contracts

Load:
- `system-prompt.md`
- `interaction-model.md`
- `output-standards.md`

Validation:
- All three files MUST be present
- System-level directives MUST be treated as invariant

### Step 2 — Validate Mode Selection

Load:
- `mode_selection.primary_mode`
- `mode_selection.secondary_mode` (if present)

Validation:
- Exactly one primary mode
- Primary mode MUST map to `/Modes/{mode}-mode.md`
- Secondary mode(s), if present, MUST already be explicitly declared and compatible

### Step 3 — Load Mode Contract

Load:
- `/00_Core_OS/Prompts/Modes/{primary_mode}-mode.md`

Purpose:
- Define behavioral posture for this execution

The assembler MUST NOT restate mode logic outside the loaded mode contract except for normalization.

### Step 4 — Validate `task` Object

Validate required task fields:
- `task.objective` is singular and explicit
- `task.scope.in_scope` exists
- `task.scope.out_of_scope` exists
- `task.inputs.required` exists
- `task.constraints.hard` exists
- `task.success_criteria` is present and testable
- `task.output_type` is declared and valid

If validation fails:
- Stop assembly
- Return schema error with missing or invalid fields

### Step 5 — Load Normalized Context

Load the context block returned by `context-loader.md`.

Validation:
- `context_block.status` MUST be either:
  - `complete`
  - `partial_non_blocking`
- `context_block.status` MUST NOT be `partial_blocking`
- `handoff.prompt_assembler_ready` MUST be `true`
- All context tiers MUST preserve `relevance_to_task`
- `context_gaps`, `assumptions`, and `conflicts` MUST be preserved verbatim

### Step 6 — Resolve Output Contract

Use `task.output_type` to select the output contract.

Allowed types:
- `Document`
- `Framework`
- `Template`
- `Checklist`
- `Analysis`

Rules:
- If matching output template exists, attach it
- If not, apply system output standards as fallback
- Required sections for the chosen type MUST be preserved in output instructions

### Step 7 — Merge Layers

Merge layers in fixed order:

1. System contracts
2. Mode contract
3. `task` object
4. Context block
5. Output instructions

During merge:
- Preserve section labels
- Preserve source attribution inside Context
- Remove semantically duplicate directives only when safe
- Reject unresolved conflicts

Additional Rules:

- `context_gaps` MUST be surfaced in the prompt
- `assumptions` with `must_label_in_output: true` MUST be propagated into output instructions
- `conflicts` with `materiality: high` MUST be surfaced as warnings
- The assembler MUST NOT suppress uncertainty signals from context

### Step 8 — Emit Final Prompt Object

Return a single normalized prompt package.

---

## 6. Final Prompt Structure

The assembler MUST emit the following structure:

```yaml
prompt_object:
  system_contracts:
  mode_contract:
  task:
  routing:
    status:
    blocking:
  context:
    status:
  output_contract:
  validation_requirements:
```

Presentation variant for execution engines:

```text
[System Layer]

[Mode Layer]

[Task Layer]

[Context Layer]

[Output Layer]
```

Rules:
- No commentary
- No meta explanation
- No omitted required sections
- Routing and context status MUST be visible to downstream execution
- Any blocking or degraded context MUST be represented explicitly

---

## 7. Source and Context Integration Rules

The assembler MUST:
- Consume routed + loaded context only
- Respect canonical vs contextual distinctions already encoded in context
- Preserve `context_gaps` and assumptions
- Avoid re-prioritizing source order independently of the loader

### Context Integrity Enforcement

The assembler MUST:

- Preserve all context tiers exactly as provided
- Preserve all context gaps, assumptions, and conflicts
- Avoid collapsing or flattening structured context

The assembler MUST NOT:

- reinterpret context priority
- introduce new facts or inferred context
- remove uncertainty indicators

## Context Mutation Prohibition

The assembler MUST NOT:
- add sources
- reinterpret source priority
- resolve context gaps
- rewrite factual context
- infer missing career facts

It may only arrange validated components into the final prompt object.

The assembler MUST NOT:
- Pull in additional files
- Re-compress context differently by mode
- Drop material gaps silently

---

## 8. Output Contract Enforcement

When applying output instructions, the assembler MUST ensure the selected output type includes required sections:

- `Document` → Title, Sections, Subsections
- `Framework` → Components, Relationships, Rules
- `Template` → Purpose, Fillable fields, Usage instructions
- `Checklist` → Items, Completion Criteria
- `Analysis` → Findings, Gaps, Risks, Recommendations

If explicit template and system output standards conflict:
- Use precedence order
- Fail assembly if conflict is materially unresolvable

Additional Rules:

- Output instructions MUST include:
  - any required assumption labeling
  - any context limitations derived from `context_gaps`
- Output MUST be constrained to available context

---

## 9. Failure Handling

### Missing Required Layer

- Stop assembly
- Return explicit missing-layer error

### Invalid `task` Schema

- Stop assembly
- Return field-level validation error

### Invalid Context Block

- Stop assembly
- Return context contract error

### Conflicting Directives

- Resolve using precedence when possible
- Otherwise fail assembly explicitly

### Missing Explicit Output Template

- Apply fallback output standards
- Do NOT fail assembly solely because a specialized template is unavailable

### Invalid Routing or Context State

- If `routing_output.status = invalid` → fail assembly
- If `routing_output.blocking = true` → fail assembly
- If `context_block.status = partial_blocking` → fail assembly
- If `prompt_assembler_ready = false` → fail assembly

---

## 10. Validation Checks

Before emitting the final prompt object, the assembler MUST verify:

- Layer order is correct
- Required layers are present
- Mode, `task`, and Output types are compatible
- Routing and context status are valid
- Context block is normalized and grounded
- Context gaps, assumptions, and conflicts are preserved
- No unresolved conflicts remain
- Output contract is complete and consistent
- Final prompt contains all required sections

If validation fails:
- Recompute only if failure is mechanical
- Otherwise fail with explicit error

---

## 11. Simplified Example

```yaml
prompt_object:
  system_contracts:
    - system-prompt
    - interaction-model
    - output-standards
  context:
    sources:
      - path: /02_Work_Experience/
        type: canonical
        key_facts:
        key_metrics:
        constraints:
        decisions:
        relevance_to_task: supports tailored resume evidence
  mode_contract:
    primary_mode: build
  task:
    objective: Create tailored resume
    scope:
      in_scope:
        - Resume content updates aligned to role priorities
      out_of_scope:
        - Cover letter generation
    inputs:
      required:
        - Base resume
        - Job description
      optional:
        - Story inventory
    constraints:
      hard:
        - 1 page
      soft:
        - Prefer concise, high-signal bullets
    success_criteria:
      - Resume addresses top role priorities with measurable impact statements
    output_type: Document
  output_contract:
    required_sections:
      - Title
      - Sections
      - Subsections
  routing_output:
  validation_requirements:
```

---

## 12. Summary

The Prompt Assembler:

- Converts validated CareerOS runtime components into a single execution-ready prompt
- Enforces layer order, compatibility, and conflict handling
- Produces deterministic prompt packages for downstream execution

It is the deterministic assembly engine of CareerOS, ensuring that only valid, grounded, and fully contextualized prompts are emitted for execution. It guarantees that no prompt is constructed on invalid routing, incomplete context, or unresolved conflicts.
