# /build-resume

## Purpose
Generate a tailored resume for a confirmed opportunity using CareerOS canonical evidence and the Resume Pack.

## Use When
- A confirmed opportunity record exists
- Opportunity analysis is complete
- You want to generate or update a role-tailored resume

## Required Inputs
- `/06_Job_Opportunities/<company>_<role>_<date>/job-opportunity.md`
- `/06_Job_Opportunities/<company>_<role>_<date>/analysis.md`

## Optional Inputs
- Existing resume in `/01_Resume_and_Profiles/`
- Story inventory
- Portfolio artifacts
- Page limit override

## Validation
Before execution, verify:
- `job-opportunity.md` exists
- `analysis.md` exists
- `intake_status: confirmed`
- Opportunity recommendation is `pursue` or explicit user override is provided

If validation fails:
- STOP execution
- return missing requirements

## Instructions
1. Use `Career/00_Core_OS/Prompts/Packs/resume-pack.md` as the governing workflow.
2. Use the confirmed opportunity record as the role-truth source.
3. Use the opportunity analysis as the positioning and prioritization source.
4. Use canonical sources in `02_`–`05_` as the source of experience, skills, goals, and constraints.
5. Use `/01_Resume_and_Profiles/` only as an optional presentation baseline.
6. Build a role-tailored resume that:
   - aligns to the role priorities identified in `analysis.md`
   - uses quantified achievements where available
   - does not overstate domain or functional fit
   - preserves canonical truth
7. Apply Resume Pack task and output contract requirements.
8. If an existing resume is provided:
   - treat it as a baseline only
   - do not allow it to override canonical truth
9. Use default page limit of 1 page unless user explicitly overrides to 2 pages.
10. Save output to `/01_Resume_and_Profiles/` using normalized naming:
    `<company>_<role>_resume_<YYYY-MM-DD>.md`
11. If requested, or if output quality needs improvement, run a refine pass focused on:
    - clarity
    - concision
    - signal density
    - role alignment

## Failure Handling
- If canonical evidence is weak:
  - use strongest grounded evidence available
  - explicitly surface evidence gaps
  - do not fabricate fit
- If role alignment is too weak for a credible resume:
  - stop and note that positioning is insufficient without overclaiming

## Output
- Tailored resume in `/01_Resume_and_Profiles/`
- Resume MUST:
  - satisfy Document structure
  - reflect role-specific positioning
  - remain truth-aligned
  - avoid filler and generic phrasing

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
    command: /build-resume
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
- `scripts/run_command_gate.sh ".cursor/runtime/build-resume.runtime-io.yaml"`
- Happy path example: runtime file `.cursor/runtime/build-resume.runtime-io.yaml` -> run `scripts/run_command_gate.sh ".cursor/runtime/build-resume.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.