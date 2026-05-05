# /intake-job

## Purpose
Process a raw job-posting source (PDF, URL, or text) through the Job Intake Pipeline to produce a structured staging opportunity file.

## Use When
- A new PDF job posting has been downloaded
- The opportunity has not yet been structured
- Job Intake Pack should be run
- A job source (PDF, URL, or text) needs to be ingested into CareerOS

## Required Inputs
- A job source in `Career/INBOX/Job_Postings/` (PDF preferred), OR
- A URL or raw text of the job posting

## Validation
Before execution, verify:
- A readable source exists (PDF, URL, or text)
- The source is the intended target

If validation fails:
- STOP execution
- request correct input

## Instructions
1. Invoke the Job Intake Pipeline:
   - `Career/00_Core_OS/Prompts/Pipelines/job-intake-pipeline.md`

2. Use the artifact template:
   - `Career/00_Core_OS/Prompts/Templates/Artifacts/job-opportunity-template.md`

3. Ensure the pipeline produces a staging file in:
   - `Career/INBOX/Job_Postings/`

4. Enforce filename normalization (applied during pipeline normalization stage):
   - `<company>_<role>_<YYYY-MM-DD>.md`

5. Ensure metadata fields are populated:
   - source_pdf (or source reference)
   - source_platform (if known)
   - date_downloaded
   - intake_status = draft

6. Ensure outputs comply with:
   - `job-intake-pack.md`
   - `output-standards.md`

7. DO NOT:
   - bypass the pipeline
   - perform manual extraction outside pipeline stages
   - infer missing facts
   - perform opportunity analysis

8. Ensure all missing required fields are set to `MISSING`

9. Ensure all context gaps are surfaced explicitly in the output

## Failure Handling
- Follow pipeline failure handling:
  - halt on blocking conditions
  - surface context gaps
  - request minimal required inputs

- Do NOT perform recovery logic outside the pipeline

## Output
- Staging opportunity file in `Career/INBOX/Job_Postings/`
- Output MUST be produced via the Job Intake Pipeline
- File MUST include:
  - metadata
  - Raw Source
  - Structured Extraction
  - no empty required fields

## Runtime IO Emission (Required)
Before finalizing, explicitly emit runtime objects defined in:

- `Career/00_Core_OS/Prompts/Runtime/runtime-io-schema.md`

Required object order:

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

Rules:

- Do not skip objects.
- Preserve upstream objects if halted.
- Set `execution_trace.halted_at` and `execution_trace.reason` on failure.
- Do not write artifacts when `validation_result.passed` is `false`.

### Runtime Emission Template (Copy/Paste)

```yaml
runtime_io:
  request:
    command: /intake-job
    intent:
    inputs:
      required:
      optional:
    pack:
    pipeline:
  task:
    id:
    name:
    objective:
    mode_intent:
    artifact_state:
    output_type:
    urgency:
    transformation_intent:
    inputs:
      required:
      optional:
    sources:
      required:
      optional:
      excluded:
    constraints:
      hard:
      soft:
    scope:
      in_scope:
      out_of_scope:
    assumptions:
    context_gaps:
    success_criteria:
    destination:
    mode_details:
  mode_selection:
    status:
    blocking:
    primary_mode:
    secondary_mode:
    rationale:
    assumptions:
    confidence:
  routing_output:
    status:
    blocking:
    source_set:
      required:
      optional:
      excluded:
    selection_rationale:
    conflict_rules_applied:
    output_destination:
    assumptions:
    completeness:
      required_sources_resolved:
      assumptions_used:
    confidence:
  context_block:
    status:
    task_alignment:
      objective:
      mode:
      output_type:
      durability_class:
    canonical_context:
    contextual_context:
    supporting_context:
    context_gaps:
    conflicts:
    assumptions:
    warnings:
    handoff:
      prompt_assembler_ready:
      execution_may_continue:
      required_user_clarification:
  prompt_object:
    system_contracts:
      - system-prompt.md
      - interaction-model.md
      - output-standards.md
    mode_contract:
      primary_mode:
    task:
      id:
      output_type:
    routing:
      status:
      blocking:
    context:
      status:
    output_contract:
      template:
    validation_requirements:
  output:
    output_type:
    status:
    blocking:
    artifact_preview:
    disclosures:
      assumptions_labeled:
      context_gaps_labeled:
      warnings_included:
  validation_result:
    passed:
    checks:
      constraints_satisfied:
      output_structure_compliant:
      source_grounding_compliant:
      boundary_rules_compliant:
      assumption_labels_present:
    failures:
    warnings:
    conformance_gate:
      protocol: command-conformance-gate.md
      status: pass
      checks_run:
        total:
        passed:
        failed:
      failures:
      evaluated_at_step: end_of_command_run
  artifact_destination:
    class:
    path:
    filename:
    write_allowed:
    write_reason:
  execution_trace:
    steps_completed:
    halted_at:
    reason:
    runtime_state:
```

## Deterministic Conformance Gate (Required)
At end of command run, execute:

- `Career/00_Core_OS/Prompts/Runtime/command-conformance-gate.md`
- `scripts/run_command_gate.sh ".cursor/runtime/intake-job.runtime-io.yaml"`
- Happy path example: runtime file `.cursor/runtime/intake-job.runtime-io.yaml` -> run `scripts/run_command_gate.sh ".cursor/runtime/intake-job.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.