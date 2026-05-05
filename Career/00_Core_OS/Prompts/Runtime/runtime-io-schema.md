---
Last Update: 2026-05-05
Previous Update:
---

# Runtime IO Schema (Canonical Runtime Object Contract)

## 1. Purpose

Define a single canonical input/output schema for CareerOS runtime execution.

This file standardizes:

- required runtime objects
- object order and dependencies
- status and blocking semantics
- minimum fields required for command-level emission

All runtime execution and command invocations MUST emit these objects explicitly.

---

## 2. Object Order (Required)

Runtime objects MUST be produced and persisted in this order:

1. `request`
2. `task`
3. `mode_selection`
4. `routing_output`
5. `context_block`
6. `prompt_object`
7. `output`
8. `validation_result`
9. `artifact_destination`
10. `execution_trace`

If execution halts, all upstream objects MUST still be emitted.

---

## 3. Status and Blocking Semantics

Where applicable, runtime objects MUST include:

- `status: valid | partial | invalid`
- `blocking: true | false`

Rules:

- `status = invalid` -> downstream execution MUST halt
- `blocking = true` -> downstream execution MUST halt
- `status = partial` with `blocking = false` -> execution MAY continue with explicit disclosures

---

## 4. Canonical Runtime Envelope (YAML)

```yaml
runtime_io:
  request:
  task:
  mode_selection:
  routing_output:
  context_block:
  prompt_object:
  output:
  validation_result:
  artifact_destination:
  execution_trace:
```

---

## 5. Object Schemas (YAML Examples)

### 5.1 request

```yaml
request:
  command: /build-resume
  intent: Generate role-tailored resume
  inputs:
    required:
      - /06_Job_Opportunities/<folder>/job-opportunity.md
      - /06_Job_Opportunities/<folder>/analysis.md
    optional:
      - /01_Resume_and_Profiles/<baseline>.md
  pack: resume-pack
  pipeline: application-pipeline
```

### 5.2 task

```yaml
task:
  id: build_resume_<timestamp>
  name: BuildTailoredResume
  objective: Create a role-tailored resume aligned to opportunity priorities.
  mode_intent: build
  artifact_state: new
  output_type: Document
  urgency: balanced
  transformation_intent: none
  inputs:
    required:
      - Work experience evidence
      - Skills evidence
      - Job opportunity context
    optional:
      - Existing resume baseline
  sources:
    required:
      - /02_Work_Experience/
      - /03_Skills_and_Portfolio/
      - /04_Career_Goals_and_Strategy/
      - /06_Job_Opportunities/<folder>/
    optional:
      - /01_Resume_and_Profiles/
    excluded:
      - /07_Applications_and_Interviews/ as canonical truth
  constraints:
    hard:
      - Page limit: 1
    soft:
      - Prefer concise quantified bullets
  scope:
    in_scope:
      - Resume content aligned to role priorities
    out_of_scope:
      - Cover letter generation
  assumptions:
    - assumption: Existing resume baseline is current enough for phrasing reference.
      reason: User provided baseline without freshness marker.
      risk: medium
      must_label_in_output: true
  context_gaps:
    - missing_information: Verified metric for one highlighted outcome.
      why_needed: Improves credibility and signal density.
      blocking: false
      suggested_source: /02_Work_Experience/
      suggested_user_action: Confirm metric before external submission.
  success_criteria:
    - Resume aligns to top role priorities
    - Claims remain traceable to canonical sources
  destination: /01_Resume_and_Profiles/
  mode_details:
    page_limit: 1
```

### 5.3 mode_selection

```yaml
mode_selection:
  status: valid
  blocking: false
  primary_mode: build
  secondary_mode:
  rationale: Objective requires net-new artifact creation.
  assumptions:
    - No transform intent detected.
  confidence: high
```

### 5.4 routing_output

```yaml
routing_output:
  status: valid
  blocking: false
  source_set:
    required:
      - /02_Work_Experience/
      - /03_Skills_and_Portfolio/
      - /04_Career_Goals_and_Strategy/
      - /06_Job_Opportunities/<folder>/
    optional:
      - /01_Resume_and_Profiles/
    excluded:
      - /01_Resume_and_Profiles/ as truth authority
  selection_rationale: Build mode with opportunity-specific resume workflow.
  conflict_rules_applied:
    - Canonical over presentation
  output_destination: /01_Resume_and_Profiles/
  assumptions:
    - Existing resume may be used for phrasing baseline only.
  completeness:
    required_sources_resolved: true
    assumptions_used: true
  confidence: high
```

### 5.5 context_block

```yaml
context_block:
  status: partial_non_blocking
  task_alignment:
    objective: Create a role-tailored resume aligned to opportunity priorities.
    mode: build
    output_type: Document
    durability_class: execution
  canonical_context:
    - path: /02_Work_Experience/
      source_type: canonical
      key_facts:
        - Led delivery programs with cross-functional teams.
      key_metrics:
        - Reduced cycle time by 30 percent.
      constraints:
        - Must preserve factual ownership.
      decisions:
        - Prioritize leadership and measurable impact.
      freshness: current
      relevance_to_task: primary evidence for resume bullets
  contextual_context:
    - path: /06_Job_Opportunities/<folder>/job-opportunity.md
      source_type: contextual
      key_facts:
        - Role emphasizes leadership, execution, and stakeholder alignment.
      key_metrics:
      constraints:
        - Resume must stay concise.
      decisions:
        - Prioritize delivery and influence examples.
      freshness: current
      relevance_to_task: role targeting input
  context_gaps:
    - missing_information: One metric not yet verified.
      why_needed: Improve output confidence for external use.
      blocking: false
      suggested_source: /02_Work_Experience/
      suggested_user_action: Confirm metric.
  assumptions:
    - assumption: Unverified metric placeholder remains excluded from final bullet.
      reason: Prevent unsupported claims.
      risk: low
      must_label_in_output: true
  warnings:
    - type: partial_context
      description: Non-blocking metric gap remains.
  handoff:
    prompt_assembler_ready: true
    execution_may_continue: true
    required_user_clarification:
```

### 5.6 prompt_object

```yaml
prompt_object:
  system_contracts:
    - system-prompt.md
    - interaction-model.md
    - output-standards.md
  mode_contract:
    primary_mode: build
  task:
    id: build_resume_<timestamp>
    output_type: Document
  routing:
    status: valid
    blocking: false
  context:
    status: partial_non_blocking
  output_contract:
    template: document-template.md
    required_sections:
      - Title
      - Sections
      - Subsections
  validation_requirements:
    - Ground claims in context
    - Label required assumptions
    - Respect context gaps
```

### 5.7 output

```yaml
output:
  output_type: Document
  status: partial
  blocking: false
  artifact_preview:
    title: District Executive Resume - Tailored Version
    sections:
      - Summary
      - Core Skills
      - Professional Experience
  disclosures:
    assumptions_labeled: true
    context_gaps_labeled: true
    warnings_included: true
```

### 5.8 validation_result

```yaml
validation_result:
  passed: true
  checks:
    constraints_satisfied: true
    output_structure_compliant: true
    source_grounding_compliant: true
    boundary_rules_compliant: true
    assumption_labels_present: true
  failures:
  warnings:
    - Non-blocking metric gap surfaced in output disclosures.
  conformance_gate:
    protocol: command-conformance-gate.md
    status: pass
    checks_run:
      total: 30
      passed: 30
      failed: 0
    failures:
    evaluated_at_step: end_of_command_run
```

### 5.9 artifact_destination

```yaml
artifact_destination:
  class: presentation
  path: /01_Resume_and_Profiles/
  filename: <company>_<role>_resume_<YYYY-MM-DD>.md
  write_allowed: true
  write_reason: Validation passed and destination matches workflow scope.
```

### 5.10 execution_trace

```yaml
execution_trace:
  steps_completed:
    - load_system_contracts
    - validate_task
    - select_mode
    - route_sources
    - load_context
    - assemble_prompt
    - execute
    - validate_output
    - route_artifact
  halted_at:
  reason:
  runtime_state: finalized
```

### 5.11 Complete `runtime_io` document (validator reference)

Single YAML document containing all root objects as mappings. Use this shape for `.cursor/runtime/*.runtime-io.yaml` and for `scripts/validate_runtime_io.py`.

```yaml
runtime_io:
  request:
    command: /build-resume
    intent: Generate role-tailored resume
    inputs:
      required:
        - /06_Job_Opportunities/<folder>/job-opportunity.md
        - /06_Job_Opportunities/<folder>/analysis.md
      optional:
        - /01_Resume_and_Profiles/<baseline>.md
    pack: resume-pack
    pipeline: application-pipeline
  task:
    id: build_resume_<timestamp>
    name: BuildTailoredResume
    objective: Create a role-tailored resume aligned to opportunity priorities.
    mode_intent: build
    artifact_state: new
    output_type: Document
    urgency: balanced
    transformation_intent: none
    inputs:
      required:
        - Work experience evidence
      optional: []
    sources:
      required:
        - /02_Work_Experience/
        - /03_Skills_and_Portfolio/
        - /04_Career_Goals_and_Strategy/
        - /06_Job_Opportunities/<folder>/
      optional:
        - /01_Resume_and_Profiles/
      excluded:
        - /07_Applications_and_Interviews/ as canonical truth
    constraints:
      hard:
        - Page limit: 1
      soft: []
    scope:
      in_scope:
        - Resume content aligned to role priorities
      out_of_scope:
        - Cover letter generation
    assumptions: []
    context_gaps: []
    success_criteria:
      - Resume aligns to top role priorities
    destination: /01_Resume_and_Profiles/
    mode_details:
      page_limit: 1
  mode_selection:
    status: valid
    blocking: false
    primary_mode: build
    secondary_mode:
    rationale: Net-new resume artifact.
    assumptions: []
    confidence: high
  routing_output:
    status: valid
    blocking: false
    source_set:
      required:
        - /02_Work_Experience/
      optional: []
      excluded: []
    selection_rationale: Build resume workflow.
    conflict_rules_applied: []
    output_destination: /01_Resume_and_Profiles/
    assumptions: []
    completeness:
      required_sources_resolved: true
      assumptions_used: false
    confidence: high
  context_block:
    status: partial_non_blocking
    task_alignment:
      objective: Create a role-tailored resume aligned to opportunity priorities.
      mode: build
      output_type: Document
      durability_class: execution
    canonical_context: []
    contextual_context: []
    supporting_context: []
    context_gaps: []
    conflicts: []
    assumptions: []
    warnings: []
    handoff:
      prompt_assembler_ready: true
      execution_may_continue: true
      required_user_clarification:
  prompt_object:
    system_contracts:
      - system-prompt.md
      - interaction-model.md
      - output-standards.md
    mode_contract:
      primary_mode: build
    task:
      id: build_resume_<timestamp>
      output_type: Document
    routing:
      status: valid
      blocking: false
    context:
      status: partial_non_blocking
    output_contract:
      template: document-template.md
    validation_requirements: []
  output:
    output_type: Document
    status: valid
    blocking: false
    artifact_preview:
      title: District Executive Resume - Tailored Version
      sections:
        - Summary
        - Core Skills
    disclosures:
      assumptions_labeled: true
      context_gaps_labeled: true
      warnings_included: true
  validation_result:
    passed: true
    checks:
      constraints_satisfied: true
      output_structure_compliant: true
      source_grounding_compliant: true
      boundary_rules_compliant: true
      assumption_labels_present: true
    failures:
    warnings: []
    conformance_gate:
      protocol: command-conformance-gate.md
      status: pass
      checks_run:
        total: 30
        passed: 30
        failed: 0
      failures:
      evaluated_at_step: end_of_command_run
  artifact_destination:
    class: presentation
    path: /01_Resume_and_Profiles/
    filename: resume.md
    write_allowed: true
    write_reason: Validation passed and destination matches workflow scope.
  execution_trace:
    steps_completed:
      - validate_task
    halted_at:
    reason:
    runtime_state: finalized
```

---

## 6. JSON Example (Single Pass)

```json
{
  "runtime_io": {
    "request": {},
    "task": {},
    "mode_selection": {},
    "routing_output": {},
    "context_block": {},
    "prompt_object": {},
    "output": {},
    "validation_result": {},
    "artifact_destination": {},
    "execution_trace": {}
  }
}
```

---

## 7. Command-Level Enforcement Rules

All commands (for example: `/intake-job`, `/analyze-opportunity`, `/build-resume`, `/build-application`, `/promote-opportunity`, `/log-activity`, `/generate-weekly-cert`) MUST:

- emit all runtime objects in the canonical order
- preserve upstream objects on any failure
- set `status` and `blocking` consistently
- set `execution_trace.halted_at` and `execution_trace.reason` when halted
- avoid artifact writes when `validation_result.passed = false`

---

## 8. Failure Example (Blocking)

```yaml
validation_result:
  passed: false
  failures:
    - Missing required source: /06_Job_Opportunities/<folder>/job-opportunity.md
artifact_destination:
  write_allowed: false
  write_reason: Validation failed
execution_trace:
  halted_at: validate_task
  reason: Missing required opportunity input
```

---

## 9. Summary

This document is the canonical runtime IO contract for CareerOS.

It ensures:

- deterministic object emission
- explicit halt behavior
- consistent command-level runtime traces
- reusable and auditable execution state across all workflows
