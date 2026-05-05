---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Prompt Library

This folder contains the CareerOS **execution system**: invariant system contracts, runtime orchestration, domain packs, and multi-step pipelines.

## Purpose

Define a deterministic, composable execution architecture so CareerOS operates as a system rather than ad hoc prompt fragments.

This library standardizes:

- interaction behavior and communication policy
- context selection and grounding rules
- mode-based execution behavior
- reusable domain packs
- multi-step workflow orchestration

---

## Execution Architecture

CareerOS operates using a layered + runtime model.

### Layer Stack (Final Prompt Shape)

```text
[System Layer]
[Mode Layer]
[Task Layer]
[Context Layer]
[Output Layer]
```

Each layer has a **single responsibility** and is enforced by runtime components.

---

## System Layer (Invariant Behavior)

- `system-prompt.md`
- `interaction-model.md` (User Interaction Policy)
- `output-standards.md`

Purpose:
- define behavior constraints
- define communication posture
- enforce output quality and structure

These files do NOT control execution flow.

---

## Mode Layer (Execution Posture)

- `Modes/build-mode.md`
- `Modes/analyze-mode.md`
- `Modes/refine-mode.md`
- `Modes/execute-mode.md`
- `Modes/architect-mode.md`
- `Modes/transform-mode.md`

Purpose:
- define how the system operates for a given task

Mode selection is handled by runtime (`Runtime/mode-selection.md`).

---

## Task Layer (Intent Definition)

- `Templates/Tasks/*.md`

Purpose:
- define objective, constraints, inputs, and expected output

---

## Context Layer (Runtime-Resolved)

Context is no longer statically injected.

It is dynamically constructed via:

- `Runtime/source-routing.md`
- `Runtime/context-loader.md`

Purpose:
- provide grounded, minimal, and relevant context
- enforce canonical vs contextual boundaries

---

## Output Layer (Structure Enforcement)

- `Templates/Outputs/*.md`
- `output-standards.md`

Purpose:
- enforce deterministic output structure
- ensure reusability and clarity

---

## Runtime Components (Execution Engine)

Runtime components orchestrate the full execution lifecycle:

- `Runtime/mode-selection.md` → mode decision rules
- `Runtime/source-routing.md` → domain and file routing
- `Runtime/context-loader.md` → context retrieval and normalization
- `Runtime/prompt-assembler.md` → final prompt construction
- `Runtime/execution-flow.md` → execution lifecycle and halt gates
- `Runtime/runtime-io-schema.md` → canonical runtime object input/output schema
- `Runtime/command-conformance-gate.md` → deterministic end-of-command conformance pass
- `Runtime/operator-runbook.md` → command operations runbook (inputs, outputs, stop/recovery)
- `Runtime/runtime-conformance-checklist.md` → system integrity validation

These define the **actual behavior of the system**.

---

## Packs (Domain-Specific Constraints)

Packs define reusable domain logic and validation rules.

- `Packs/resume-pack.md`
- `Packs/interview-pack.md`
- `Packs/application-pack.md`
- `Packs/opportunity-analysis-pack.md`
- `Packs/networking-pack.md`
- `Packs/strategy-pack.md`
- `Packs/stories-pack.md`

Purpose:
- provide domain-specific constraints
- define quality gates and expectations
- integrate with runtime execution

Packs do NOT execute logic—they constrain it.

---

## Pipelines (Multi-Step Orchestration)

Pipelines define multi-step workflows across tasks.

- `Pipelines/application-pipeline.md`
- `Pipelines/opportunity-review-pipeline.md`
- `Pipelines/interview-prep-pipeline.md`
- `Pipelines/networking-pipeline.md`

Purpose:
- orchestrate sequences of tasks
- enforce workflow-level consistency

---

## How to Use

### 1. Runtime Invocation (Primary Model)

Provide:
- `task` object
- Optional pack
- Optional pipeline

Runtime handles:
- mode selection
- source routing
- context loading
- prompt assembly
- execution
- validation
- runtime object emission (`request` -> `execution_trace`)

---

### 2. Pack-Based Invocation

Example:

```
Use Stories Pack
task.name: CreateCanonicalStory
Inputs: [...]
```

---

### 3. Pipeline Invocation

Example:

```
Use Application Pipeline
Inputs: [...]
```

---

## Design Rules

- Keep layers strictly separated
- Runtime owns execution behavior
- Packs define constraints, not logic
- Pipelines define workflows, not execution mechanics
- Canonical truth lives in `Career/`
- Never allow contextual artifacts to override canonical truth
- Minimize context while preserving signal
- Prefer determinism over flexibility

---

## Composition Reference

Final assembled prompt shape:

```text
[System Layer]
[Mode Layer]
[Task Layer]
[Context Layer]
[Output Instructions]
```

See: `Runtime/prompt-assembler.md`

---

## Related Documents

- `careeros-prompt-architecture-spec.md`
- `../career-index.md`
- `../../Career_Workspace_Assistant_prompt.md`
- `../../WORKFLOWS.md`