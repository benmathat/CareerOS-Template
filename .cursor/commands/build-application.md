# /build-application

## Purpose
Build a complete application package for a confirmed, analyzed opportunity using the CareerOS Application Pack.

## Use When
- A confirmed opportunity record exists
- Opportunity analysis is complete
- The opportunity recommendation is `pursue`, or the user explicitly overrides
- You need application-ready materials and an execution record

## Required Inputs
- `/06_Job_Opportunities/<company>_<role>_<date>/job-opportunity.md`
- `/06_Job_Opportunities/<company>_<role>_<date>/analysis.md`

## Optional Inputs
- Tailored resume from `/01_Resume_and_Profiles/`
- Existing cover letter baseline
- Recruiter or contact notes
- Application questions or required short-form responses
- Submission constraints or deadline

## Validation
Before execution, verify:
- `job-opportunity.md` exists
- `analysis.md` exists
- `intake_status: confirmed`
- analysis includes exactly one recommendation: `pursue`, `consider`, or `pass`
- recommendation is `pursue`, or explicit user override is provided

If validation fails:
- STOP execution
- return missing requirements
- do not create application artifacts

## Instructions
1. Use `Career/00_Core_OS/Prompts/Packs/application-pack.md` as the governing workflow.
2. Use the confirmed opportunity record as the role-truth source.
3. Use the opportunity analysis as the decision, positioning, and risk source.
4. Use canonical sources in `02_`–`05_` only for grounded career evidence.
5. Use `/01_Resume_and_Profiles/` only for presentation artifacts and baselines.
6. Build the application package with the required outputs:
   - tailored resume reference or generated resume if missing and requested
   - cover letter or supporting note if needed
   - application notes
   - next-step checklist
   - application execution record
7. Do not overwrite existing resume, cover letter, or application files silently.
8. If an artifact already exists:
   - ask whether to update, version, or leave unchanged
9. Save resume and cover letter artifacts to:
   `/01_Resume_and_Profiles/`
10. Save application notes, checklist, and execution record to:
    `/07_Applications_and_Interviews/`
11. Use normalized naming:
    - `<company>_<role>_resume_<YYYY-MM-DD>.md`
    - `<company>_<role>_cover_letter_<YYYY-MM-DD>.md`
    - `<company>_<role>_application_notes_<YYYY-MM-DD>.md`
    - `<company>_<role>_next_steps_<YYYY-MM-DD>.md`
    - `<company>_<role>_application_record_<YYYY-MM-DD>.md`
12. Preserve truth boundaries:
    - do not fabricate qualifications
    - do not overstate domain or role fit
    - do not let presentation artifacts override canonical evidence
13. Update the application record with:
    - company
    - role
    - status
    - linked opportunity
    - linked analysis
    - linked artifacts
    - next action
14. If the application is actually submitted during this workflow, update status to `submitted` and record submission metadata.

## Compliance Hook
If the application is actually submitted or an external application-related action occurs:

→ Recommend: `/log-activity`

Purpose:
- document the application submission or external action as a work search activity
- link evidence such as confirmation emails or submission screenshots
- connect the compliance entry to the application record

Do NOT recommend `/log-activity` merely because internal artifacts were created.

## Failure Handling
- If role alignment is too weak for credible application materials:
  - stop and state the positioning risk
  - do not create misleading artifacts
- If required application information is missing:
  - list missing inputs
  - create only non-submission artifacts if useful and explicitly allowed
- If submission evidence is unavailable:
  - allow application record update
  - mark evidence as `MISSING` if logging later

## Output
- Application package artifacts routed to the correct folders
- Application execution record in `/07_Applications_and_Interviews/`
- No canonical source files modified

## Next Step
After application materials are complete:
- submit externally if ready
- update application record
- run `/log-activity` only after a real-world qualifying action occurs

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
    command: /build-application
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
- `scripts/run_command_gate.sh ".cursor/runtime/build-application.runtime-io.yaml"`
- Happy path example: runtime file `.cursor/runtime/build-application.runtime-io.yaml` -> run `scripts/run_command_gate.sh ".cursor/runtime/build-application.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.