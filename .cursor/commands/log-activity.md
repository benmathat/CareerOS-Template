# /log-activity

## Purpose
Record a job-search activity in the CareerOS TWC compliance log with audit-safe detail and optional evidence linkage.

## Use When
- You apply for a job
- You send a networking or recruiter message
- You attend an interview or screening call
- You complete job-search research that may qualify as a work search activity
- You need to document an activity for unemployment benefits compliance

## Required Inputs
At minimum, provide:
- activity date
- activity type
- employer, contact, platform, or organization
- role or subject
- method of contact/activity
- outcome or current status

## Optional Inputs
- evidence file path
- related opportunity record
- related application record
- notes
- whether the activity was entered retrospectively

## Validation
Before logging, verify:
- activity date is present
- activity type is present
- employer/platform/contact is present
- method is present
- outcome/status is present

If validation fails:
- STOP execution
- return the missing fields
- do not append an incomplete compliance entry

## Governing Files
Use these CareerOS locations:

- Canonical log:
  `Career/11_Job_Search_Activities/Work_Search_Log.md`
- Evidence folder:
  `Career/11_Job_Search_Activities/Evidence/`
- Weekly certifications:
  `Career/11_Job_Search_Activities/Weekly_Certifications/`
- Related opportunities:
  `Career/06_Job_Opportunities/`
- Related applications/interviews:
  `Career/07_Applications_and_Interviews/`
- Networking context:
  `Career/08_Networking_and_References/`

## Activity Type Vocabulary
Use one of the following normalized activity types when possible:

- application_submitted
- resume_sent
- recruiter_contact
- networking_message
- informational_interview
- interview
- follow_up
- job_research
- job_fair_or_event
- profile_update
- training_or_assessment
- other

If the activity does not fit cleanly:
- use `other`
- explain in Notes

## Method Vocabulary
Use one of the following normalized methods when possible:

- online_application
- email
- phone
- voicemail
- linkedin
- indeed
- company_website
- in_person
- video_call
- text_message
- other

## Instructions
1. Use the activity details provided by the user.
2. Do not infer missing compliance facts.
3. Do not claim that an activity qualifies for TWC unless the user explicitly identifies it as qualifying or the record is marked `twc_qualifying: true` by the user.
4. If qualification is uncertain, set `twc_qualifying: needs_review`.
5. Append the activity to `Career/11_Job_Search_Activities/Work_Search_Log.md`.
6. Preserve existing log entries exactly as written.
7. Do not rewrite or reorder historical entries.
8. If correcting a prior entry, append a correction note instead of editing the original entry.
9. Link supporting evidence if provided.
10. If evidence is provided but not already stored in the Evidence folder, suggest moving it to:
    `Career/11_Job_Search_Activities/Evidence/`
11. If the activity relates to an opportunity or application, include a reference path.
12. If entered after the fact, mark it as retrospective and include the true activity date.

## Required Log Entry Fields
Every entry MUST include:

```yaml
activity_id:
date:
activity_type:
twc_qualifying: true | false | needs_review
employer_or_platform:
role_or_subject:
method:
outcome_status:
evidence:
related_opportunity:
related_application:
retrospective: true | false
notes:
```

## Activity ID Format
Generate `activity_id` using:

```text
YYYY-MM-DD_<company-or-platform>_<activity-type>
```

Normalization rules:
- lowercase
- spaces become underscores
- remove punctuation and special characters
- keep concise but recognizable

Example:

```text
2026-04-22_openland_credit_union_application_submitted
```

If multiple activities have the same base ID on one day:
- append `_02`, `_03`, etc.

## Evidence Naming Rule
If creating or recommending an evidence filename, use:

```text
YYYY-MM-DD_<company-or-platform>_<activity-type>.<ext>
```

Examples:

```text
2026-04-22_openland_credit_union_application_confirmation.pdf
2026-04-22_linkedin_recruiter_message.png
```

## Output Format for Work_Search_Log.md
Append entries in this format:

```markdown
## YYYY-MM-DD — <Activity Summary>

```yaml
activity_id: YYYY-MM-DD_company_activity
activity_type: application_submitted
activity_date: YYYY-MM-DD
twc_qualifying: needs_review
employer_or_platform: Company or Platform
role_or_subject: Role or Subject
method: online_application
outcome_status: submitted
evidence: Evidence/<filename or MISSING>
related_opportunity: ../06_Job_Opportunities/<path or MISSING>
related_application: ../07_Applications_and_Interviews/<path or MISSING>
retrospective: false
notes: >
  Brief factual note. Include no unsupported claims.
```
```

## Audit-Safe Writing Rules
- Be factual and specific
- Avoid vague phrases like “looked around” or “did job stuff”
- Include employer/platform names
- Include role titles when available
- Include method and outcome
- Preserve true dates
- Do not embellish
- Do not backdate creation; record retrospective status when applicable

## Failure Handling

### Missing Required Fields
- Stop
- list missing fields
- ask for only the missing data

### Evidence Missing
- allow entry if evidence is unavailable
- set `evidence: MISSING`
- note whether evidence should be added later

### Qualification Unclear
- set `twc_qualifying: needs_review`
- do not classify as qualifying without confirmation

### Duplicate Activity
- do not overwrite the prior entry
- append a new entry only if it is a distinct activity
- otherwise ask whether to append a correction note

## Output
- Updated `Career/11_Job_Search_Activities/Work_Search_Log.md`
- Optional evidence filename recommendation
- Optional references to related opportunity/application records

## Next Step
If the logged activity is part of an application workflow, update the related application record in:

```text
Career/07_Applications_and_Interviews/
```

If the week is complete, run:

```text
/generate-weekly-cert
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
    command: /log-activity
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
- `scripts/run_command_gate.sh ".cursor/runtime/log-activity.runtime-io.yaml"`
- Happy path example: runtime file `.cursor/runtime/log-activity.runtime-io.yaml` -> run `scripts/run_command_gate.sh ".cursor/runtime/log-activity.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.