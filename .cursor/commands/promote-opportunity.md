# /promote-opportunity

## Purpose
Promote a reviewed job opportunity from `Career/INBOX/Job_Postings/` into the durable CareerOS opportunity structure.

## Use When
- A staged opportunity markdown file has been created by `/intake-job`
- The staged file has been reviewed for extraction accuracy
- The opportunity is ready to become a durable CareerOS record

## Required Inputs
- Staged opportunity file:
  `Career/INBOX/Job_Postings/<company>_<role>_<YYYY-MM-DD>.md`
- Source PDF:
  `Career/INBOX/Job_Postings/<source-file>.pdf`

## Validation
Before execution, verify:
- staged markdown file exists
- source PDF exists
- staged file includes `intake_status: reviewed` or `intake_status: confirmed`
- staged file includes required sections:
  - Raw Source
  - Structured Extraction
- required metadata fields are present:
  - company
  - role
  - date_added or date_downloaded
  - source_pdf

If validation fails:
- STOP execution
- return missing requirements
- do not move files

## Instructions
1. Use the staged opportunity file as the source of truth for folder naming.
2. Normalize the destination folder name using the same filename normalization rules from `/intake-job`:
   - lowercase
   - replace spaces with underscores
   - remove punctuation and special characters
   - remove common company suffixes only when clearly redundant
   - use normalized role title
   - use date in `YYYY-MM-DD` format
3. Create destination folder:
   `Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/`
4. Move the staged markdown file into the destination folder and rename it:
   `job-opportunity.md`
5. Move the source PDF into the destination folder and rename it:
   `source-posting.pdf`
6. Update `job-opportunity.md` metadata:
   - set `intake_status: confirmed`
   - set or update `promoted_date`
   - update `source_pdf: source-posting.pdf`
   - set `status: intake` unless another valid lifecycle status is already present
7. Ensure all internal references point to the local promoted files.
8. Do not perform opportunity analysis.
9. Do not assign pursue / consider / pass.
10. Do not generate resume, cover letter, or application artifacts.

## Destination Structure
Final structure MUST be:

```text
Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/
  job-opportunity.md
  source-posting.pdf
```

## Failure Handling
- If destination folder already exists:
  - do not overwrite files silently
  - ask whether to merge, replace, or create a versioned folder
- If PDF cannot be matched confidently:
  - stop and ask for the correct source PDF
- If metadata is incomplete:
  - mark missing fields explicitly
  - do not promote until required fields are corrected

## Output
- Confirmed opportunity folder in `Career/06_Job_Opportunities/`
- Promoted `job-opportunity.md`
- Promoted `source-posting.pdf`
- No analysis artifacts created

## Next Step
After successful promotion, suggest running:

```text
/analyze-opportunity
```

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
    command: /promote-opportunity
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
- `scripts/run_command_gate.sh ".cursor/runtime/promote-opportunity.runtime-io.yaml"`
- Happy path example: runtime file `.cursor/runtime/promote-opportunity.runtime-io.yaml` -> run `scripts/run_command_gate.sh ".cursor/runtime/promote-opportunity.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.