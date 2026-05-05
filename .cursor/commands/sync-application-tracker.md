# /sync-application-tracker

## Purpose
Repair and reconcile `Career/07_Applications_and_Interviews/Applications/application-tracker.md` so tracker rows accurately reflect current application records.

## Use When
- The tracker is out of sync with application detail files
- You imported or backfilled opportunities/applications
- Statuses changed via other workflows and tracker consistency needs to be restored
- You want a deterministic reconciliation pass before reporting or planning

## Required Inputs
- Tracker file:
  `Career/07_Applications_and_Interviews/Applications/application-tracker.md`
- Application detail source folder:
  `Career/07_Applications_and_Interviews/Applications/`

## Optional Inputs
- Scope filter (company, role, or application ID)
- Dry-run mode (preview only, no writes)
- Conflict policy:
  - prefer_detail_files
  - prefer_tracker
  - report_only

## Validation
Before execution, verify:
- tracker file exists
- application detail source folder exists
- tracker contains an `Active Applications` table
- detail files are parseable enough to derive:
  - ID
  - company
  - role
  - status

If validation fails:
- STOP execution
- return missing requirements
- do not modify tracker

## Governing Files
Use these CareerOS locations:

- Master tracker:
  `Career/07_Applications_and_Interviews/Applications/application-tracker.md`
- Application detail records:
  `Career/07_Applications_and_Interviews/Applications/*.md`
- Application template (for expected fields/shape):
  `Career/07_Applications_and_Interviews/Applications/application-detail-template.md`
- Workflow contracts:
  `Career/WORKFLOWS.md`
  `Career/WORKFLOW_INDEX.md`
  `Career/STATUS_DEFINITIONS.md`

## Instructions
1. Parse the `Active Applications` table in `application-tracker.md`.
2. Discover application detail files in `Career/07_Applications_and_Interviews/Applications/`.
3. Exclude non-record files from reconciliation:
   - `application-tracker.md`
   - `application-detail-template.md`
   - `README.md` (if present)
4. Build normalized keys for matching (preferred order):
   - explicit application ID
   - deterministic company+role+date key
   - filename fallback key
5. Reconcile rows with deterministic upsert behavior:
   - create missing tracker rows for valid detail records
   - update existing rows when detail records carry newer lifecycle state
   - never silently delete tracker rows
6. Keep these columns synchronized for matched rows:
   - `ID`
   - `Company`
   - `Role`
   - `Location`
   - `Source`
   - `Referral`
   - `Status`
   - `Last Action`
   - `Next Action`
   - `Resume Version`
7. Preserve user-authored narrative detail in tracker unless directly contradicted by structured fields from detail record.
8. For status reconciliation, use lifecycle precedence:
   - Identified
   - Applied
   - Recruiter Screen
   - Hiring Manager
   - Panel / Onsite
   - Final
   - Offer
   - Rejected
   - Withdrawn
   - On Hold
9. If conflict policy is `prefer_detail_files`, detail record wins for structured fields.
10. If conflict policy is `prefer_tracker`, keep tracker values but report mismatches.
11. If conflict policy is `report_only`, produce a discrepancy report and do not write.
12. Update tracker frontmatter:
    - set `Previous Update` to current `Last Update` when present
    - set `Last Update` to today's date (YYYY-MM-DD)
13. Write changes only when reconciliation is valid and deterministic.
14. Emit a concise reconciliation report with:
    - rows_created
    - rows_updated
    - rows_skipped
    - conflicts_found
    - unresolved_items

## Write Safety Rules
- Do not reorder historical sections unrelated to `Active Applications` unless required for table integrity.
- Do not remove rows without explicit user instruction.
- Do not fabricate missing fields; use `MISSING` when required.
- Keep markdown table structure valid after updates.

## Failure Handling

### Tracker Structure Invalid
- Stop and report exact table parsing failure
- suggest minimal repair needed before retry

### Ambiguous Record Match
- do not guess
- leave row unchanged
- include in unresolved_items report

### Unsupported Status Value
- do not coerce silently
- report unsupported status
- keep existing status unless user chooses mapping

### Partial Reconciliation
- if only some rows can be reconciled safely, apply safe updates and report unresolved items
- if deterministic guarantees cannot be met, halt writes unless user allows partial mode

## Output
- Updated tracker file:
  `Career/07_Applications_and_Interviews/Applications/application-tracker.md`
- Reconciliation report summary in command output

## Next Step
After sync:
- review unresolved items
- if external activity occurred, run:

```text
/log-activity
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
    command: /sync-application-tracker
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
- `scripts/run_command_gate.sh ".cursor/runtime/sync-application-tracker.runtime-io.yaml"`
- Happy path example: runtime file `.cursor/runtime/sync-application-tracker.runtime-io.yaml` -> run `scripts/run_command_gate.sh ".cursor/runtime/sync-application-tracker.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.
