---
name: sync-application-tracker
description: Reconcile the application tracker with current application records.
---

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
- Application detail sources:
  `Career/06_Job_Opportunities/*/application-record.md` (primary)
  `Career/07_Applications_and_Interviews/Applications/*.md` (legacy fallback only if still present)

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
- at least one detail source exists (opportunity-folder `application-record.md` files and/or legacy `Applications/*.md`)
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
- Application detail records (primary):
  `Career/06_Job_Opportunities/<company>_<role>_<date>/application-record.md`
- Application template (for expected fields/shape):
  `Career/07_Applications_and_Interviews/Applications/application-detail-template.md`
- Workflow contracts:
  `Career/WORKFLOWS.md`
  `Career/WORKFLOW_INDEX.md`
  `Career/STATUS_DEFINITIONS.md`

## Instructions
1. Parse the `Active Applications` table in `application-tracker.md`.
2. Discover application detail files from opportunity folders:
   `Career/06_Job_Opportunities/*/application-record.md`.
3. Also scan legacy `Career/07_Applications_and_Interviews/Applications/*.md` if any remain, excluding:
   - `application-tracker.md`
   - `application-detail-template.md`
   - `README.md` (if present)
   Prefer opportunity-folder records when both exist for the same opportunity.
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

## Must NOT
- create, edit, move, or delete opportunity folders, `application-record.md` files, or any file other than `application-tracker.md`
- remove or archive a row (closing is `/close-opportunity`) or touch the Closed Applications table
- write to the work search log (use `/log-activity`)
- coerce an unsupported status or guess an ambiguous match
- write at all under `report_only`
- commit, push, or stage anything unless the user asks

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

Start the run file with `scripts/careeros new-run sync-application-tracker <slug>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
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
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_sync-application-tracker_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_sync-application-tracker_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_sync-application-tracker_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.
