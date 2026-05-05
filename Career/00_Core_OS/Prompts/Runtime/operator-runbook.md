---
Last Update: 2026-05-05
Previous Update:
---

# Operator Runbook (Usable Now)

## Purpose

Provide a single operational runbook for executing CareerOS commands consistently.

For each command, this runbook defines:

- command input format
- required files
- expected outputs
- stop conditions
- recovery steps

This document is operator-facing and must be used with:

- `runtime-io-schema.md`
- `command-conformance-gate.md`
- `execution-flow.md`

---

## Universal Execution Protocol (All Commands)

1. Validate command inputs and required files.
2. Emit runtime objects (`request` -> `execution_trace`) to:
   - `.cursor/runtime/<command-name>.runtime-io.yaml`
3. Run deterministic conformance gate:
   - `Career/00_Core_OS/Prompts/Runtime/command-conformance-gate.md`
   - `scripts/run_command_gate.sh ".cursor/runtime/<command-name>.runtime-io.yaml"`
4. If gate passes, finalize artifact write/update.
5. If gate fails, stop and return structured failure state.

Hard rule:

- Do not write artifacts when `validation_result.passed: false`.

---

## Standard Command Input Format

Use this normalized format for command invocation:

```yaml
request:
  command: /command-name
  intent: <single explicit objective>
  inputs:
    required:
      - <required input>
    optional:
      - <optional input>
  pack: <pack-name | NONE>
  pipeline: <pipeline-name | NONE>
```

---

## Command Runbook Matrix

### /intake-job

- **Input format**
  - `command: /intake-job`
  - required input: raw source (PDF, URL, or text)
- **Required files**
  - Source in `Career/INBOX/Job_Postings/` OR provided URL/text
  - `Prompts/Pipelines/job-intake-pipeline.md`
  - `Prompts/Packs/job-intake-pack.md`
- **Expected outputs**
  - Staging file in `Career/INBOX/Job_Postings/`
  - Structured opportunity markdown with intake metadata
- **Stop conditions**
  - Missing/unreadable source
  - Required extraction fields unresolved and blocking
  - Conformance gate failure
- **Recovery steps**
  - Request minimal missing source input
  - Mark unresolved required fields as `MISSING`
  - Re-run pipeline stage from acquisition/extraction

### /promote-opportunity

- **Input format**
  - `command: /promote-opportunity`
  - required input: staged markdown + source PDF
- **Required files**
  - `Career/INBOX/Job_Postings/<company>_<role>_<YYYY-MM-DD>.md`
  - matching source PDF
- **Expected outputs**
  - `Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/`
  - `job-opportunity.md`
  - `source-posting.pdf`
- **Stop conditions**
  - Missing staged file or source PDF
  - Missing required metadata
  - Destination conflict unresolved
  - Conformance gate failure
- **Recovery steps**
  - Request missing staged/source file
  - Resolve naming/destination conflict (merge/version/replace decision)
  - Re-run promotion with corrected metadata

### /analyze-opportunity

- **Input format**
  - `command: /analyze-opportunity`
  - required input: confirmed `job-opportunity.md`
- **Required files**
  - `Career/06_Job_Opportunities/<folder>/job-opportunity.md`
  - `intake_status: confirmed`
- **Expected outputs**
  - `Career/06_Job_Opportunities/<folder>/analysis.md`
  - single recommendation: `pursue|consider|pass`
- **Stop conditions**
  - Missing opportunity file
  - Intake not confirmed
  - Required sections absent
  - Conformance gate failure
- **Recovery steps**
  - Run `/intake-job` or `/promote-opportunity` to repair intake state
  - Add missing required sections
  - Re-run analysis after validation

### /build-resume

- **Input format**
  - `command: /build-resume`
  - required input: opportunity file + analysis file
- **Required files**
  - `Career/06_Job_Opportunities/<folder>/job-opportunity.md`
  - `Career/06_Job_Opportunities/<folder>/analysis.md`
- **Expected outputs**
  - Resume artifact in `Career/01_Resume_and_Profiles/`
  - role-aligned, grounded `Document` output
- **Stop conditions**
  - Missing required opportunity/analysis input
  - Non-pursue recommendation without explicit override
  - Canonical evidence insufficient and blocking
  - Conformance gate failure
- **Recovery steps**
  - Complete/repair opportunity analysis first
  - Gather missing canonical evidence
  - Re-run with explicit override only when user-directed

### /build-application

- **Input format**
  - `command: /build-application`
  - required input: opportunity file + analysis file
- **Required files**
  - `Career/06_Job_Opportunities/<folder>/job-opportunity.md`
  - `Career/06_Job_Opportunities/<folder>/analysis.md`
- **Expected outputs**
  - Application artifacts across:
    - `Career/01_Resume_and_Profiles/`
    - `Career/07_Applications_and_Interviews/`
  - application record and next-step checklist
- **Stop conditions**
  - Missing required input files
  - Recommendation is `pass` without override
  - Required artifact conflicts unresolved
  - Conformance gate failure
- **Recovery steps**
  - Resolve missing inputs and recommendation state
  - Resolve artifact conflict via update/version decision
  - Re-run from build stage with validated inputs

### /log-activity

- **Input format**
  - `command: /log-activity`
  - required input: activity date, type, platform/employer, method, outcome
- **Required files**
  - `Career/11_Job_Search_Activities/Work_Search_Log.md`
- **Expected outputs**
  - Append-only compliant log entry in `Work_Search_Log.md`
  - evidence link or `MISSING`
- **Stop conditions**
  - Missing required activity fields
  - Invalid log schema for new entry
  - Conformance gate failure
- **Recovery steps**
  - Request missing required fields only
  - Keep prior entries unchanged; append correction entry if needed
  - Re-run append with normalized vocabulary

### /generate-weekly-cert

- **Input format**
  - `command: /generate-weekly-cert`
  - required input: claim week start/end dates
- **Required files**
  - `Career/11_Job_Search_Activities/Work_Search_Log.md`
- **Expected outputs**
  - `Career/11_Job_Search_Activities/Weekly_Certifications/YYYY-W##.md`
  - readiness status: `ready|needs_review|incomplete`
- **Stop conditions**
  - Missing/invalid date range
  - Canonical log missing
  - Existing weekly file conflict unresolved
  - Conformance gate failure
- **Recovery steps**
  - Request correct claim-week bounds
  - Resolve existing file behavior (update/revision/stop)
  - Re-run certification generation with exact log slice

---

## Deterministic Stop Conditions (Global)

Stop immediately when any of the following occurs:

- required input/file missing and blocking
- `mode_selection.status = invalid` or `blocking = true`
- `routing_output.status = invalid` or `blocking = true`
- `context_block.status = partial_blocking`
- prompt assembly failure
- output validation failure
- conformance gate failure

When stopped, always return:

- `validation_result.passed: false`
- `artifact_destination.write_allowed: false`
- populated `execution_trace.halted_at` and `execution_trace.reason`

---

## Recovery Protocol (Global)

1. Preserve all upstream runtime objects.
2. Return only minimal missing inputs/actions required to continue.
3. Do not fabricate missing facts.
4. Re-run from the earliest invalid stage (not from scratch unless required).
5. Re-emit runtime objects and re-run conformance gate before any write.

---

## Operator Sign-Off Checklist

- [ ] Command input format validated
- [ ] Required files resolved
- [ ] Runtime IO emitted
- [ ] Command conformance gate passed
- [ ] Expected outputs produced in correct destination
- [ ] Stop/recovery behavior executed correctly when applicable

