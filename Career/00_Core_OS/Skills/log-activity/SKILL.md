---
name: log-activity
description: Record a job-search activity in the work search compliance log.
argument-hint: "<date> <activity type> <employer or contact> <role or subject> <method>"
---

# /log-activity

## Purpose
Record a job-search activity in the CareerOS work-search compliance log with audit-safe detail and optional evidence linkage.

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
3. Do not claim that an activity qualifies with the agency named in `compliance-profile.md` unless the user explicitly identifies it as qualifying or the record is marked `qualifying: true` by the user.
4. If qualification is uncertain, set `qualifying: needs_review`. New entries use `qualifying`; never rewrite older entries that use the legacy name `twc_qualifying`.
5. Append the activity to `Career/11_Job_Search_Activities/Work_Search_Log.md`.
6. Preserve existing log entries exactly as written.
7. Do not rewrite or reorder historical entries.
8. If correcting a prior entry, append a correction note instead of editing the original entry.
9. Link supporting evidence if provided.
10. If evidence is provided but not already stored in the Evidence folder, suggest moving it to:
    `Career/11_Job_Search_Activities/Evidence/`
11. If the activity relates to an opportunity or application, include a reference path.
12. If entered after the fact, mark it as retrospective and include the true activity date.
13. If the activity relates to an application lifecycle change (application submitted, interview, follow-up, rejection, withdrawal, hold), automatically update `Career/07_Applications_and_Interviews/Applications/application-tracker.md` in the same run.
14. For tracker updates, upsert the matching row and keep `Status`, `Last Action`, and `Next Action` in sync with the new activity.
15. If the tracker update cannot be completed safely, STOP and report a blocking error instead of logging only a partial workflow update.

## Required Log Entry Fields
Every entry MUST include:

```yaml
activity_id:
date:
activity_type:
qualifying: true | false | needs_review
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
qualifying: needs_review
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

## Must NOT
- edit, reorder, reformat, or delete any existing log entry (corrections are appended notes)
- mark an activity `qualifying: true` on its own judgment
- create or move evidence files, or create a weekly certification (see `/generate-weekly-cert`)
- touch the tracker except the lifecycle upsert in instruction 13, and no other tracker row
- touch opportunity folders, resumes, or `02_`–`05_` canonical sections
- backdate creation; retrospective entries carry the true date and a retrospective flag
- commit, push, or stage anything unless the user asks

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
- set `qualifying: needs_review`
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

Start the run file with `scripts/careeros new-run log-activity <slug>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
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

The run file skeleton comes from `scripts/careeros new-run`; its shape is defined in `Prompts/Runtime/runtime-io-schema.md`. Do not hand-write the YAML from scratch.

## Deterministic Conformance Gate (Required)
At end of command run, execute:

- `Career/00_Core_OS/Prompts/Runtime/command-conformance-gate.md`
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_log-activity_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_log-activity_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_log-activity_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.