# /generate-weekly-cert

## Purpose
Generate an audit-safe weekly unemployment work-search certification summary from the canonical CareerOS work search log.

## Use When
- You are preparing to submit a weekly TWC payment request or certification
- You need a weekly snapshot of documented work-search activities
- You need to verify activity count, evidence coverage, and documentation completeness for a claim week

## Required Inputs
At minimum, provide:
- claim week start date
- claim week end date

Optional but recommended:
- TWC required activity count for the week
- whether the certification has already been submitted
- submission confirmation number or screenshot path, if available

## Validation
Before generation, verify:
- `Career/11_Job_Search_Activities/Work_Search_Log.md` exists
- claim week start date is present
- claim week end date is present
- date range is valid
- activities are filtered using the true activity date, not creation date

If validation fails:
- STOP execution
- return missing requirements
- do not create a weekly certification file

## Governing Files
Use these CareerOS locations:

- Canonical log:
  `Career/11_Job_Search_Activities/Work_Search_Log.md`
- Weekly certifications:
  `Career/11_Job_Search_Activities/Weekly_Certifications/`
- Evidence folder:
  `Career/11_Job_Search_Activities/Evidence/`
- Application records:
  `Career/07_Applications_and_Interviews/`
- Opportunity records:
  `Career/06_Job_Opportunities/`

## Instructions
1. Read `Career/11_Job_Search_Activities/Work_Search_Log.md`.
2. Select only activities with `activity_date` inside the requested claim week, inclusive.
3. Do not modify `Work_Search_Log.md`.
4. Count:
   - total activities
   - activities marked `twc_qualifying: true`
   - activities marked `twc_qualifying: needs_review`
   - activities marked `twc_qualifying: false`
5. Preserve evidence references exactly as logged.
6. Identify missing evidence but do not invent or infer evidence.
7. Identify entries with incomplete required fields.
8. Create a weekly certification file in:
   `Career/11_Job_Search_Activities/Weekly_Certifications/`
9. Use filename format:
   `YYYY-W##.md`
10. If the file already exists:
    - do not overwrite silently
    - ask whether to update, create a revision, or stop
11. Include a clear certification readiness assessment:
    - ready
    - needs_review
    - incomplete
12. Do not state that the week satisfies TWC requirements unless the required activity count is provided and the qualifying count meets or exceeds it.

## Weekly Certification File Structure
Create the weekly certification file using this structure:

```markdown
---
claim_week_start: YYYY-MM-DD
claim_week_end: YYYY-MM-DD
week_id: YYYY-W##
required_activity_count: <number | MISSING>
actual_activity_count: <number>
qualifying_activity_count: <number>
needs_review_activity_count: <number>
nonqualifying_activity_count: <number>
certification_status: draft
readiness: ready | needs_review | incomplete
submission_status: not_submitted | submitted
submission_date:
submission_confirmation:
---

# Weekly Certification — YYYY-W##

## 1. Claim Week

- Start: YYYY-MM-DD
- End: YYYY-MM-DD
- Required activities: <number | MISSING>

## 2. Summary

- Total logged activities: <number>
- Qualifying activities: <number>
- Needs review: <number>
- Non-qualifying activities: <number>
- Evidence gaps: <number>
- Incomplete entries: <number>

## 3. Readiness Assessment

Status: ready | needs_review | incomplete

Rationale:
- <brief factual rationale>

## 4. Activity Snapshot

| Date | Activity Type | Employer / Platform | Role / Subject | Method | Outcome | TWC Qualifying | Evidence |
|---|---|---|---|---|---|---|---|
| YYYY-MM-DD |  |  |  |  |  |  |  |

## 5. Evidence Review

### Evidence Present
- 

### Evidence Missing
- 

## 6. Issues / Gaps

- 

## 7. Submission Record

- Submitted to TWC: no
- Submission date:
- Confirmation / reference:
- Evidence of submission:

## 8. Declaration Notes

This file is a weekly snapshot generated from `Work_Search_Log.md` for documentation and review. It should reflect the activities recorded for the claim week and any available supporting evidence.
```

## Readiness Rules

### ready
Use only when:
- required activity count is provided
- qualifying activity count meets or exceeds required count
- no required fields are missing from qualifying activities

### needs_review
Use when:
- required activity count is missing
- one or more activities are marked `twc_qualifying: needs_review`
- evidence is missing but log entries are otherwise complete

### incomplete
Use when:
- required log fields are missing
- qualifying count is below the provided requirement
- claim week contains no logged activities

## Evidence Rules
- Evidence is not required to create the file, but gaps MUST be listed.
- Do not fabricate evidence references.
- If evidence is missing, preserve `MISSING` and list it under Evidence Missing.
- If submission evidence exists, link it in Submission Record.

## Audit-Safe Writing Rules
- Use true activity dates
- Preserve original logged facts
- Do not embellish outcomes
- Do not combine multiple activities into one unless they were logged that way
- Do not remove `needs_review` flags
- Do not edit historical log entries as part of this command

## Failure Handling

### No Activities Found
- Create the weekly certification only if the user explicitly wants a zero-activity record
- Otherwise stop and report that no activities were found for the claim week

### Existing Weekly Certification File
- Do not overwrite silently
- Ask whether to:
  - update existing file
  - create a revision file
  - stop

### Missing Required Activity Count
- Generate the file with `required_activity_count: MISSING`
- Set readiness to `needs_review` unless other issues make it `incomplete`

### Incomplete Log Entries
- Generate the file only if enough data exists to identify the activity
- Set readiness to `incomplete`
- list incomplete entries under Issues / Gaps

## Output
- Weekly certification file in:
  `Career/11_Job_Search_Activities/Weekly_Certifications/YYYY-W##.md`
- Summary of:
  - total activities
  - qualifying activities
  - review-needed activities
  - evidence gaps
  - readiness status

## Next Step
After submitting the weekly certification to TWC, update the weekly file with:
- `submission_status: submitted`
- `submission_date`
- `submission_confirmation`
- submission evidence path, if available

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
    command: /generate-weekly-cert
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
- `scripts/run_command_gate.sh ".cursor/runtime/generate-weekly-cert.runtime-io.yaml"`
- Happy path example: runtime file `.cursor/runtime/generate-weekly-cert.runtime-io.yaml` -> run `scripts/run_command_gate.sh ".cursor/runtime/generate-weekly-cert.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.